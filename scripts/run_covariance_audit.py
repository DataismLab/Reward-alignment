"""Factorial covariance/reward audit, with separately defined references.

Run independently for --assets 10/30/49. Never overwrites previous experiments.
"""
import argparse, hashlib, json, time
import numpy as np
from scipy.linalg import cho_factor, cho_solve
from scipy.optimize import linprog
from mvrl.historical import ROOT, data, french_monthly, moments, solve_family, solve_quadratic, objective, summary, bootstrap
from mvrl.covariance import ESTIMATORS, estimate_covariance, covariance_transfer_bounds, calibration_bounds

OUT=ROOT/'results/historical/covariance'; OUT.mkdir(parents=True,exist_ok=True)
NAMES=['target','raw','scalar','penalty_only','joint','minvar']


def pnl_policy(history, prev, cost, penalty):
    """Explicit long-only, no-loan, assetwise restriction of H&S Eq.8.

    sum_i (w_i R_i)^+ - penalty sum_i (w_i R_i)^- is linear on w>=0.
    Costs retain the published penalty/5 multiplier. Capital is fixed at one.
    """
    n=len(prev)
    score=np.maximum(history,0).mean(0)-penalty*np.maximum(-history,0).mean(0)
    B=np.block([[np.eye(n),-np.eye(n)],[-np.eye(n),-np.eye(n)]])
    r=linprog(np.r_[-score,np.full(n,penalty/5*cost)],A_ub=B,b_ub=np.r_[prev,-prev],
        A_eq=np.r_[np.ones(n),np.zeros(n)][None,:],b_eq=[1],bounds=[(0,1)]*(2*n),method='highs')
    if not r.success:raise RuntimeError(r.message)
    return r.x[:n]


def run_case(n,estimator):
    frame=data(n); R=frame.iloc[:,:-1].to_numpy();rf=frame.RF.to_numpy();dates=frame.index.to_numpy(dtype=int)
    factors=french_monthly(ROOT/'data/raw/F-F_Research_Data_Factors_CSV.zip').loc[dates,['Mkt-RF','SMB','HML']].to_numpy()
    names=NAMES+['one_step_mvpi']+(['pnl1','pnl5','pnl25'] if estimator=='diag10' else [])
    prev={name:np.ones(n)/n for name in names};base_prev=np.ones(n)/n
    records=[];states=[]; anchors=[];start=time.time()
    for t,date in enumerate(dates):
        if date<199001:continue
        hist=R[t-120:t]; x=hist-rf[t-120:t,None];m,v,info=estimate_covariance(x,estimator,factors[t-120:t],cache_dir=OUT/'quest_cache')
        _,base_v=moments(x);common=prev['target'].copy()
        audit,ai=solve_family(m,v,5.,common,.001,NAMES)
        one_A=1+10*m@common
        if one_A<=0:raise ValueError('one-step auxiliary requires positive scale')
        audit['one_step_mvpi'],ai['certificates']['one_step_mvpi']=solve_quadratic(m,5/one_A*(v+np.outer(m,m)),common,.001/one_A)
        base_target,base_cert=solve_quadratic(m,5*base_v,base_prev,.001)
        alternative,alt_cert=solve_quadratic(m,5*v,base_prev,.001)
        ref_value=objective(m,base_v,base_target,5,base_prev,.001)
        transfer=covariance_transfer_bounds(base_v,v,alternative,5)
        # Approximate alternative optimum contributes its independent certificate.
        transfer['target_gap_upper']+=alt_cert
        transfer['distance_upper']=float(np.sqrt(transfer['target_gap_upper']/(5*np.linalg.eigvalsh(base_v).min())))
        centered=R[t]-rf[t]-m
        chol=cho_factor(v,lower=True)
        ld=2*np.log(np.diag(chol[0])).sum()
        states.append(dict(date=int(date),fit_start=int(dates[t-120]),fit_end=int(dates[t-1]),
            **info,cross_target_distance=float(np.linalg.norm(alternative-base_target)),
            cross_target_gap=ref_value-objective(m,base_v,alternative,5,base_prev,.001),
            cross_certificate=float(alt_cert),cross_target=alternative.tolist(),
            baseline_target=base_target.tolist(),baseline_prev=base_prev.tolist(),transfer_bound=transfer,
            gaussian_score=float(ld+centered@cho_solve(chol,centered)),A=ai['A']))
        if n==49 and estimator in ('ff3','lw_identity') and date%100==1:
            for label,anchor in [('zero',0.),('holdings',float(m@common))]:
                A=1+10*anchor
                if A<=0:raise ValueError('nonpositive approximate scaling')
                u,cert=solve_quadratic(m,5/A*(v+np.outer(m,m)),common,.001/A)
                bound=calibration_bounds(m,v,5,audit['target'],u,anchor,cert)
                gap=objective(m,v,audit['target'],5,common,.001)-objective(m,v,u,5,common,.001)
                anchors.append(dict(date=int(date),anchor_type=label,anchor=anchor,certificate=cert,
                    target_mean=float(m@audit['target']),target_gap=gap,distance=float(np.linalg.norm(u-audit['target'])),
                    weights=u.tolist(),target=audit['target'].tolist(),prev=common.tolist(),bound=bound))
        target_value=objective(m,v,audit['target'],5,common,.001)
        for name in names:
            if name.startswith('pnl'):aw=pnl_policy(hist,common,.001,int(name[3:]))
            else:aw=audit[name]
            own_cert=0.
            if np.max(abs(prev[name]-common))<1e-12:
                w=aw;own_cert=ai['certificates'].get(name,0.)
            elif name.startswith('pnl'):w=pnl_policy(hist,prev[name],.001,int(name[3:]))
            elif name=='raw':w,own_cert=solve_quadratic(m,5*(v+np.outer(m,m)),prev[name],.001)
            elif name=='scalar':w,own_cert=solve_quadratic(m,5*(1-ai['nu'])*(v+np.outer(m,m)),prev[name],.001)
            elif name=='minvar':w,own_cert=solve_quadratic(np.zeros_like(m),5*v,prev[name],.001)
            elif name=='one_step_mvpi':
                own_A=1+10*m@prev[name]
                if own_A<=0:raise ValueError('one-step auxiliary requires positive scale')
                w,own_cert=solve_quadratic(m,5/own_A*(v+np.outer(m,m)),prev[name],.001/own_A)
            else:
                own,oi=solve_family(m,v,5,prev[name],.001,[name]);w=own[name];own_cert=oi['certificates'][name]
            turnover=float(abs(w-prev[name]).sum());gross=float(w@R[t])
            records.append(dict(date=int(date),method=name,n_assets=n,estimator=estimator,phi=5.,cost=.001,
                return_gross=gross,return_net=gross-.001*turnover,rf=float(rf[t]),turnover=turnover,
                distance=float(np.linalg.norm(aw-audit['target'])),target_gap=target_value-objective(m,v,aw,5,common,.001),
                weights=w.tolist(),audit_weights=aw.tolist(),common_prev=common.tolist(),own_prev=prev[name].tolist(),
                certificate=ai['certificates'].get(name),own_certificate=float(own_cert),fit_end=int(dates[t-1])))
            prev[name]=w*(1+R[t])/(1+gross)
        base_prev=base_target*(1+R[t])/(1+float(base_target@R[t]))
        if date%100==12 and date//100%6==1:print(n,estimator,int(date),round(time.time()-start,1),flush=True)
    result=dict(n_assets=n,estimator=estimator,records=records,states=states,anchors=anchors,
        summary=summary(records),bootstrap=bootstrap(records),
        subperiods={f'{lo}-{hi}':summary([r for r in records if lo<=r['date']<=hi])
            for lo,hi in [(199001,200712),(200801,201512),(201601,202512)]})
    path=OUT/f'{n}_{estimator}.json';path.write_text(json.dumps(result))
    print('DONE',n,estimator,round(time.time()-start,1),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--assets',type=int,required=True);p.add_argument('--estimator',choices=ESTIMATORS)
    args=p.parse_args()
    for estimator in ([args.estimator] if args.estimator else ESTIMATORS):
        if (OUT/f'{args.assets}_{estimator}.json').exists():
            print('Preserving completed',args.assets,estimator,flush=True);continue
        run_case(args.assets,estimator)
