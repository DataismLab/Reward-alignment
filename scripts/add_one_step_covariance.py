"""Sequential exploratory comparator; preserve all previous saved decisions."""
import json
import numpy as np
from mvrl.historical import ROOT,data,french_monthly,solve_quadratic,objective,summary
from mvrl.covariance import estimate_covariance

out=ROOT/'results/historical/covariance'
for path in sorted(out.glob('[0-9]*_*.json')):
    d=json.loads(path.read_text())
    if any(r['method']=='one_step_mvpi' for r in d['records']):continue
    n=d['n_assets'];e=d['estimator'];frame=data(n);R=frame.iloc[:,:-1].to_numpy();rf=frame.RF.to_numpy();dates=frame.index.to_numpy()
    factors=french_monthly(ROOT/'data/raw/F-F_Research_Data_Factors_CSV.zip').loc[dates,['Mkt-RF','SMB','HML']].to_numpy()
    refs={r['date']:r for r in d['records'] if r['method']=='target'};prev=np.ones(n)/n
    extra=[]
    for t,date in enumerate(dates):
        if date<199001:continue
        m,v,_=estimate_covariance(R[t-120:t]-rf[t-120:t,None],e,factors[t-120:t]);M=v+np.outer(m,m)
        ref=refs[int(date)];common=np.array(ref['common_prev']);target=np.array(ref['audit_weights'])
        A=1+10*m@common;own_A=1+10*m@prev
        if min(A,own_A)<=0:raise ValueError('positive auxiliary scaling required')
        aw,cert=solve_quadratic(m,5/A*M,common,.001/A)
        w,ocert=solve_quadratic(m,5/own_A*M,prev,.001/own_A)
        turnover=float(abs(w-prev).sum());gross=float(w@R[t])
        extra.append(dict(date=int(date),method='one_step_mvpi',n_assets=n,estimator=e,phi=5.,cost=.001,
            return_gross=gross,return_net=gross-.001*turnover,rf=float(rf[t]),turnover=turnover,
            distance=float(np.linalg.norm(aw-target)),target_gap=objective(m,v,target,5,common,.001)-objective(m,v,aw,5,common,.001),
            weights=w.tolist(),audit_weights=aw.tolist(),common_prev=common.tolist(),own_prev=prev.tolist(),
            certificate=cert,own_certificate=ocert,fit_end=int(dates[t-1])))
        prev=w*(1+R[t])/(1+gross)
    d['records']+=extra;d['summary']=summary(d['records'])
    d['subperiods']={f'{lo}-{hi}':summary([r for r in d['records'] if lo<=r['date']<=hi]) for lo,hi in [(199001,200712),(200801,201512),(201601,202512)]}
    path.write_text(json.dumps(d));print('ADDED',path.name,len(extra),flush=True)
