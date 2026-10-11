"""Reconstruct every saved action's accounting and target losses from raw data."""
import json,hashlib
import numpy as np
from scipy.linalg import cho_factor,cho_solve
from mvrl.historical import ROOT,data,french_monthly
from mvrl.covariance import estimate_covariance

out=ROOT/'results/historical/covariance';report=[]
for path in sorted(out.glob('[0-9]*_*.json')):
    result=json.loads(path.read_text());n=result['n_assets'];est=result['estimator']
    frame=data(n);R=frame.iloc[:,:-1].to_numpy();rf=frame.RF.to_numpy();dates=frame.index.to_numpy()
    factors=french_monthly(ROOT/'data/raw/F-F_Research_Data_Factors_CSV.zip').loc[dates,['Mkt-RF','SMB','HML']].to_numpy()
    bydate={s['date']:s for s in result['states']};group={}
    for r in result['records']:group.setdefault(r['date'],{})[r['method']]=r
    prev={k:np.ones(n)/n for k in next(iter(group.values()))};baseline_prev=np.ones(n)/n
    errors=dict(return_net=0.,turnover=0.,distance=0.,target_gap=0.,identity=0.,drift=0.,gaussian_score=0.)
    bound_violation=0.;anchor_violation=0.;count=0
    for t,date in enumerate(dates):
        if date<199001:continue
        rows=group[int(date)];state=bydate[int(date)]
        assert state['fit_start']==int(dates[t-120]) and state['fit_end']==int(dates[t-1])
        x=R[t-120:t]-rf[t-120:t,None]
        m,v,info=estimate_covariance(x,est,factors[t-120:t]);target=np.array(rows['target']['audit_weights'])
        common=np.array(rows['target']['common_prev']);assert np.max(abs(common-prev['target']))<1e-12
        A=1+10*m@target;M=v+np.outer(m,m)
        F=lambda w:float(m@w-5*w@v@w-.001*abs(w-common).sum())
        base=np.array(state['baseline_target']);alt=np.array(state['cross_target'])
        assert np.max(abs(baseline_prev-state['baseline_prev']))<1e-12
        for w in (base,alt):assert abs(w.sum()-1)<1e-7 and w.min()>-1e-7
        s=np.cov(x,rowvar=False);vbase=.9*s+.1*np.diag(s.diagonal())
        Fb=lambda w:float(m@w-5*w@vbase@w-.001*abs(w-baseline_prev).sum())
        gap=Fb(base)-Fb(alt);dist=np.linalg.norm(base-alt)
        assert abs(gap-state['cross_target_gap'])<1e-12 and abs(dist-state['cross_target_distance'])<1e-12
        bound_violation=max(bound_violation,gap-state['transfer_bound']['target_gap_upper'])
        assert gap<=state['transfer_bound']['target_gap_upper']+1e-9
        baseline_prev=base*(1+R[t])/(1+base@R[t])
        centered=R[t]-rf[t]-m;ch=cho_factor(v,lower=True)
        score=float(2*np.log(np.diag(ch[0])).sum()+centered@cho_solve(ch,centered))
        assert np.isfinite(state['gaussian_score'])
        errors['gaussian_score']=max(errors['gaussian_score'],abs(score-state['gaussian_score']))
        for name,r in rows.items():
            count+=1;w=np.array(r['weights']);aw=np.array(r['audit_weights']);p=prev[name]
            for a in (w,aw):assert np.isfinite(a).all() and abs(a.sum()-1)<1e-7 and a.min()>-1e-7
            assert r['fit_end']==int(dates[t-1])
            errors['drift']=max(errors['drift'],float(np.max(abs(p-r['own_prev']))))
            assert np.max(abs(common-r['common_prev']))<1e-12
            turnover=abs(w-p).sum();net=w@R[t]-.001*turnover
            checks={'return_net':net,'turnover':turnover,'distance':np.linalg.norm(aw-target),'target_gap':F(target)-F(aw)}
            for key,val in checks.items():errors[key]=max(errors[key],float(abs(val-r[key])))
            Q=m@aw-5/A*aw@M@aw-.001/A*abs(aw-common).sum()
            rhs=F(aw)-5*(m@aw-m@target)**2+5*(m@target)**2
            errors['identity']=max(errors['identity'],float(abs(A*Q-rhs)))
            if r['certificate'] is not None:assert r['certificate']<=2e-7
            assert r['own_certificate']<=2e-7
            prev[name]=w*(1+R[t])/(1+w@R[t])
        for a in [a for a in result['anchors'] if a['date']==date]:
            u=np.array(a['weights']);anchor=a['anchor'];b=a['bound'];agap=F(target)-F(u)
            assert abs(agap-a['target_gap'])<1e-12
            assert abs(b['target_gap_upper']-(5*(m@target-anchor)**2+b['A']*a['certificate']))<1e-12
            anchor_violation=max(anchor_violation,agap-b['target_gap_upper'])
            assert agap<=b['target_gap_upper']+1e-9
            assert np.linalg.norm(u-target)<=b['distance_upper']+1e-5
    assert all(v<1e-12 for k,v in errors.items() if k!='gaussian_score')
    assert errors['gaussian_score']<1e-7
    report.append(dict(file=path.name,decisions=count,states=len(bydate),errors=errors,
        max_transfer_bound_violation=bound_violation,max_anchor_bound_violation=anchor_violation,
        sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    print(path.name,count,'PASS',flush=True)
assert len(report)==18
(out/'verification.json').write_text(json.dumps(report,indent=2))
print('TOTAL',sum(r['decisions'] for r in report),'decisions independently reconstructed')
