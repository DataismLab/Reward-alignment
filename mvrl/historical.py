"""Reproducible walk-forward reward audit; no future observations in estimates.

Targets are FITTED one-period mean-variance preferences, not a true historical
multiperiod equilibrium. Costs use a first-order proportional L1 convention.
"""
from pathlib import Path
import csv, io, json, zipfile
import numpy as np
import pandas as pd
from scipy.optimize import minimize, LinearConstraint

ROOT=Path(__file__).resolve().parents[1]

def french_monthly(path, marker=None, start_date=None, end_date=None):
    with zipfile.ZipFile(path) as z:
        text=z.read(z.namelist()[0]).decode('utf-8-sig')
    lines=text.splitlines()
    start=next(i for i,l in enumerate(lines) if (marker in l if marker else l.startswith(',Mkt-RF')))
    if marker:start+=1
    names=[x.strip() for x in lines[start].split(',')][1:]
    rows=[];seen_month=False
    for line in lines[start+1:]:
        cells=[x.strip() for x in line.split(',')]
        if len(cells[0])!=6 or not cells[0].isdigit():
            if seen_month:break
            continue
        seen_month=True
        date=int(cells[0])
        if start_date is not None and date<start_date:continue
        if end_date is not None and date>end_date:continue
        vals=np.array([float(x) for x in cells[1:]])
        if np.any(vals<=-99):raise ValueError('missing French return')
        rows.append([int(cells[0]),*(vals/100)])
    if not rows:raise ValueError('no monthly block')
    return pd.DataFrame(rows,columns=['date',*names]).set_index('date').rename_axis('date')

def data(n_assets=10):
    if n_assets not in (10,30,49):raise ValueError('unsupported industry universe')
    assets=french_monthly(ROOT/f'data/raw/{n_assets}_Industry_Portfolios_CSV.zip','Average Value Weighted Returns -- Monthly',197001,202512)
    rf=french_monthly(ROOT/'data/raw/F-F_Research_Data_Factors_CSV.zip')['RF']
    frame=assets.join(rf,how='inner').loc[197001:202512]
    expected=pd.period_range('1970-01','2025-12',freq='M').strftime('%Y%m').astype(int)
    if (frame.isna().any().any() or frame.index.duplicated().any()
            or not np.array_equal(frame.index,expected) or frame.shape[1]!=n_assets+1):
        raise ValueError('invalid data')
    return frame

def moments(history,shrink=.1):
    x=np.asarray(history,float)
    m=x.mean(axis=0);v=np.cov(x,rowvar=False,ddof=1)
    v=(1-shrink)*v+shrink*np.diag(np.diag(v))
    if np.linalg.eigvalsh(v).min()<=0:raise ValueError('singular covariance')
    return m,v

def solve_quadratic(m,hessian,prev,cost=0.,scale=1000.):
    """Max m'w - w'Hw - cost |w-prev| on simplex, epigraph QP.

    Returns a feasible solution and Frank-Wolfe certificate from a linear
    programme over the SAME epigraph polytope (upper bound on objective gap).
    """
    from scipy.optimize import linprog
    m=np.asarray(m);n=len(m);prev=np.asarray(prev)
    H=np.asarray(hessian)
    # L1 epigraph z >= +/- (w-prev); z <=1 is valid for simplex positions.
    B=np.block([[np.eye(n),-np.eye(n)],[-np.eye(n),-np.eye(n)]])
    bounds=[(0,1)]*(2*n)
    eq=np.r_[np.ones(n),np.zeros(n)][None,:]
    con=[LinearConstraint(eq,[1],[1]),LinearConstraint(B,-np.inf,np.r_[prev,-prev])]
    x0=np.r_[prev,np.zeros(n)]
    def fun(x):return scale*(x[:n]@H@x[:n]-m@x[:n]+cost*np.sum(x[n:]))
    def jac(x):return scale*np.r_[2*H@x[:n]-m,np.full(n,cost)]
    res=minimize(fun,x0,jac=jac,bounds=bounds,constraints=con,method='SLSQP',options={'ftol':1e-11,'maxiter':300})
    if not np.isfinite(res.x).all():raise RuntimeError(res.message)
    w=res.x[:n]
    if abs(w.sum()-1)>1e-7 or min(w)<-1e-7:raise RuntimeError('infeasible')
    grad=jac(res.x)/scale
    lp=linprog(grad,A_ub=B,b_ub=np.r_[prev,-prev],A_eq=eq,b_eq=[1],bounds=bounds,method='highs')
    if not lp.success:raise RuntimeError(lp.message)
    certificate=max(0.,float(grad@(res.x-lp.x)))
    if certificate>2e-7 or not res.success:
        # SLSQP can declare success after a poorly scaled step. Re-solve and
        # accept only an independently certified iterate, never the success flag.
        best=(certificate,res.x.copy())
        for retry_scale in [10.,1.,100.]:
            rr=minimize(lambda x:fun(x)*retry_scale/scale,res.x,
                jac=lambda x:jac(x)*retry_scale/scale,bounds=bounds,constraints=con,
                method='SLSQP',options={'ftol':1e-13,'maxiter':1000})
            if (not np.isfinite(rr.x).all() or abs(rr.x[:n].sum()-1)>1e-8
                    or np.min(rr.x)<-1e-8 or np.max(B@rr.x-np.r_[prev,-prev])>1e-8):
                continue
            gg=jac(rr.x)/scale
            ll=linprog(gg,A_ub=B,b_ub=np.r_[prev,-prev],A_eq=eq,b_eq=[1],bounds=bounds,method='highs')
            if not ll.success:raise RuntimeError(ll.message)
            cc=max(0.,float(gg@(rr.x-ll.x)))
            if cc<best[0]:best=(cc,rr.x.copy())
            if cc<1e-8:break
        certificate,xx=best;w=xx[:n]
        if certificate>2e-7:raise RuntimeError(f'QP certificate {certificate}')
    return w,certificate

def mvpi(m,v,phi,prev,cost,tol=1e-10):
    M=v+np.outer(m,m);y=0.;trace=[]
    for i in range(200):
        w,cert=solve_quadratic((1+2*phi*y)*m,phi*M,prev,cost)
        yn=float(m@w);trace.append(float(m@w-phi*w@v@w-cost*abs(w-prev).sum()))
        if abs(yn-y)<tol:return w,dict(iterations=i+1,residual=abs(yn-y),certificate=cert,trace=trace)
        y=yn
    raise RuntimeError('MVPI did not converge')

def objective(m,v,w,phi,prev,cost):return float(m@w-phi*w@v@w-cost*np.abs(w-prev).sum())

def solve_family(m,v,phi,prev,cost,names=None):
    names=names or ['target','raw','scalar','penalty_only','joint','mvpi','equal','minvar']
    out={};certs={};target,ct=solve_quadratic(m,phi*v,prev,cost)
    M=v+np.outer(m,m);nu=float(m@np.linalg.solve(M,m));A=1+2*phi*(m@target)
    if A<=0:raise ValueError('joint calibration needs positive linear coefficient')
    for name in names:
        if name=='target':w,cert=target,ct
        elif name=='raw':w,cert=solve_quadratic(m,phi*M,prev,cost)
        elif name=='scalar':w,cert=solve_quadratic(m,phi*(1-nu)*M,prev,cost)
        elif name=='penalty_only':w,cert=solve_quadratic(m,phi/A*M,prev,cost)
        elif name=='joint':w,cert=solve_quadratic(m,phi/A*M,prev,cost/A)
        elif name=='mvpi':w,info=mvpi(m,v,phi,prev,cost);cert=info['certificate']
        elif name=='equal':w,cert=np.ones(len(m))/len(m),0.
        elif name=='minvar':w,cert=solve_quadratic(np.zeros_like(m),phi*v,prev,cost)
        else:raise ValueError(name)
        out[name]=w;certs[name]=cert
    return out,dict(A=float(A),nu=nu,certificates=certs)

def log_policy(history,v,phi,prev,cost):
    """Adaptation: E log(1+w'R) - phi w'Vw - linear turnover cost."""
    n=len(prev);x=np.asarray(history);B=np.block([[np.eye(n),-np.eye(n)],[-np.eye(n),-np.eye(n)]])
    def f(z):
        w=z[:n];g=1+x@w
        return 1000*(-np.log(g).mean()+phi*w@v@w+cost*z[n:].sum())
    def j(z):
        w=z[:n];return 1000*np.r_[-(x/(1+x@w)[:,None]).mean(0)+2*phi*v@w,np.full(n,cost)]
    r=minimize(f,np.r_[prev,np.zeros(n)],jac=j,bounds=[(0,1)]*(2*n),constraints=[LinearConstraint(np.r_[np.ones(n),np.zeros(n)][None,:],1,1),LinearConstraint(B,-np.inf,np.r_[prev,-prev])],method='SLSQP',options={'ftol':1e-10,'maxiter':300})
    if not r.success:raise RuntimeError(r.message)
    return r.x[:n]

def run(window=120,phi=5.,cost=.001,shrink=.1,include_mvpi=True,include_log=True,n_assets=10):
    frame=data(n_assets);returns=frame.iloc[:,:-1].to_numpy();rf=frame.RF.to_numpy();dates=frame.index.to_numpy(dtype=int)
    names=['target','raw','scalar','penalty_only','joint','equal','minvar']+(['mvpi'] if include_mvpi else [])+(['log','log_variance'] if include_log else [])
    prev={k:np.ones(returns.shape[1])/returns.shape[1] for k in names};records=[]
    for t,date in enumerate(dates):
        if date<199001 or t<window:continue
        hist=returns[t-window:t];excess=hist-rf[t-window:t,None];m,v=moments(excess,shrink)
        # common state is the target's actual pre-trade portfolio; no other policy's
        # past affects the cross-reward alignment comparison.
        common=prev['target'].copy()
        audit,info=solve_family(m,v,phi,common,cost,[k for k in names if not k.startswith('log')])
        for name in [k for k in names if k.startswith('log')]:audit[name]=log_policy(hist,v,phi if name=='log_variance' else 0.,common,cost)
        target_value=objective(m,v,audit['target'],phi,common,cost)
        for name in names:
            aw=audit[name]
            if name.startswith('log'):w=log_policy(hist,v,phi if name=='log_variance' else 0.,prev[name],cost)
            elif np.max(abs(prev[name]-common))<1e-12:w=aw
            else:w=solve_family(m,v,phi,prev[name],cost,[name])[0][name]
            turnover=float(abs(w-prev[name]).sum());gross=float(w@returns[t]);net=gross-cost*turnover
            records.append(dict(date=int(date),method=name,window=window,phi=phi,cost=cost,shrink=shrink,return_gross=gross,return_net=net,rf=float(rf[t]),turnover=turnover,distance=float(np.linalg.norm(aw-audit['target'])),target_gap=target_value-objective(m,v,aw,phi,common,cost),A=info['A'],fit_end=int(dates[t-1]),fit_start=int(dates[t-window]),weights=w.tolist(),audit_weights=aw.tolist(),max_certificate=max(info['certificates'].values())))
            prev[name]=w*(1+returns[t])/(1+gross)
    return records

def summary(records):
    rows=[]
    for name,g in pd.DataFrame(records).groupby('method',sort=False):
        net=g.return_net.to_numpy();ex=net-g.rf.to_numpy();wealth=np.r_[1.,np.cumprod(1+net)]
        rows.append(dict(method=name,n=len(g),start=int(g.date.min()),end=int(g.date.max()),distance=float(g.distance.mean()),target_gap=float(g.target_gap.mean()),ann_mean=float(net.mean()*12),ann_vol=float(net.std(ddof=1)*np.sqrt(12)),sharpe=float(ex.mean()/ex.std(ddof=1)*np.sqrt(12)),mv_month=float(ex.mean()-g.phi.iloc[0]*ex.var(ddof=1)),max_drawdown=float(np.min(wealth/np.maximum.accumulate(wealth)-1)),turnover=float(g.turnover.mean()),terminal_wealth=float(wealth[-1])))
    return rows

def bootstrap(records,base='raw',other='joint',seed=8128,reps=1000,block=12):
    df=pd.DataFrame(records);a=df[df.method==base].sort_values('date');b=df[df.method==other].sort_values('date');assert np.array_equal(a.date,b.date)
    x=(a.return_net-a.rf).to_numpy();y=(b.return_net-b.rf).to_numpy();phi=float(a.phi.iloc[0]);n=len(x);rng=np.random.default_rng(seed)
    deltas=[]
    for _ in range(reps):
        starts=rng.integers(n,size=int(np.ceil(n/block)));idx=((starts[:,None]+np.arange(block))%n).ravel()[:n]
        xx,yy=x[idx],y[idx];deltas.append((yy.mean()-phi*yy.var(ddof=1))-(xx.mean()-phi*xx.var(ddof=1)))
    return dict(base=base,other=other,reps=reps,block=block,seed=seed,estimate=float((y.mean()-phi*y.var(ddof=1))-(x.mean()-phi*x.var(ddof=1))),ci95=np.quantile(deltas,[.025,.975]).tolist())

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--robust',action='store_true');args=p.parse_args()
    out=ROOT/'results/historical';out.mkdir(exist_ok=True)
    primary=json.loads((out/'primary.json').read_text()) if (out/'primary.json').exists() else run();(out/'primary.json').write_text(json.dumps(primary,indent=2));s=summary(primary)
    result=dict(summary=s,bootstrap=[bootstrap(primary,base=k) for k in ['raw','scalar','penalty_only','mvpi']],protocol='historical walk-forward: settings in mvrl/historical.py')
    for lo,hi in [(199001,200712),(200801,201512),(201601,202512)]:result[str(lo)+'-'+str(hi)]=summary([x for x in primary if lo<=x['date']<=hi])
    (out/'summary.json').write_text(json.dumps(result,indent=2));print(json.dumps(s,indent=2),flush=True)
    if args.robust:
        robust=[]
        settings={(120,p,c,.1) for p in [2.,5.,10.] for c in [0.,.001,.0025]}|{(w,5.,.001,h) for w in [60,120,240] for h in [0.,.1,.5]}
        for w,p,c,h in sorted(settings):
            key=f'w{w}_p{p}_c{c}_s{h}'
            cached=out/(key+'.json')
            r=json.loads(cached.read_text()) if cached.exists() else run(w,p,c,h,False,False)
            (out/(key+'.json')).write_text(json.dumps(r));robust.append(dict(window=w,phi=p,cost=c,shrink=h,summary=summary(r)));print(key,flush=True)
        (out/'robustness.json').write_text(json.dumps(robust,indent=2))
