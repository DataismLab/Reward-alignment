"""Independently reconstruct saved holdings, returns, gaps and calibration identity."""
import json
import numpy as np
from mvrl.historical import ROOT,data
out=ROOT/'results/historical/dimensions';report=[]
for n in (10,30,49):
    rows=json.loads((out/f'industry{n}.json').read_text());f=data(n)
    names=sorted({r['method'] for r in rows});prev={k:np.ones(n)/n for k in names}
    errors=dict(return_net=0.,turnover=0.,target_gap=0.,distance=0.,identity=0.)
    assert len(rows)==432*7
    for date in f.index[f.index>=199001]:
        rs=[r for r in rows if r['date']==date];assert len(rs)==7
        t=f.index.get_loc(date);h=f.iloc[t-120:t];x=h.iloc[:,:-1].to_numpy()-h.RF.to_numpy()[:,None]
        m=x.sum(0)/120;center=x-m;v=center.T@center/119;v=.9*v+.1*np.diag(np.diag(v))
        common=prev['target'].copy();target=np.asarray(next(r['audit_weights'] for r in rs if r['method']=='target'))
        F=lambda w:float(m@w-5*w@v@w-.001*abs(w-common).sum())
        A=1+10*m@target;assert A>0
        for r in rs:
            w=np.array(r['weights']);aw=np.array(r['audit_weights']);k=r['method']
            assert len(w)==n and len(aw)==n and r['fit_end']==f.index[t-1] and r['fit_start']==f.index[t-120]
            assert r['max_certificate']<=2e-7
            for q in (w,aw):assert min(q)>=-1e-7 and abs(q.sum()-1)<1e-7
            turn=abs(w-prev[k]).sum();gross=w@f.iloc[t,:-1].to_numpy()
            checks=dict(return_net=gross-.001*turn,turnover=turn,target_gap=F(target)-F(aw),distance=np.linalg.norm(aw-target))
            for key,val in checks.items():errors[key]=max(errors[key],abs(val-r[key]))
            joint_reward=m@aw-5/A*aw@(v+np.outer(m,m))@aw-.001/A*abs(aw-common).sum()
            rhs=F(aw)-5*(m@aw-m@target)**2+5*(m@target)**2
            errors['identity']=max(errors['identity'],abs(A*joint_reward-rhs))
            prev[k]=w*(1+f.iloc[t,:-1].to_numpy())/(1+gross)
    assert max(errors.values())<1e-10,errors
    report.append(dict(n_assets=n,records=len(rows),max_absolute_errors=errors))
(out/'verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
