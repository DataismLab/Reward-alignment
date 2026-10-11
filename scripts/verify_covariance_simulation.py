import json
import numpy as np
from mvrl.historical import ROOT,solve_quadratic,objective
from mvrl.covariance import estimate_covariance
from mvrl.financing import financing_cost

report=[]
for n in [10,49,100]:
    rows=json.loads((ROOT/f'results/covariance_simulation/n{n}.json').read_text())
    gen=np.random.default_rng(20261007+n);B=gen.normal(.4,.35,size=(3,n));B[0]+=.6
    fc=np.diag([.03**2,.02**2,.025**2]);sd=np.linspace(.015,.035,n);m=np.linspace(.003,.007,n);p=np.ones(n)/n
    oracle={};maxerror=0.;identity_error=0.
    for design in ['diagonal','correlated']:
        corr=np.eye(n)
        if design=='correlated':
            for i in range(n):
                for j in range(n):
                    if i!=j and i//5==j//5:corr[i,j]=.4
        noise=corr*np.outer(sd,sd);truth=B.T@fc@B+noise
        oracle[design]=solve_quadratic(m,5*truth,p,.001)[0]
        for L in [60,120]:
            for seed in range(30):
                rng=np.random.default_rng(50000+1000*n+10*seed+L)
                factors=rng.multivariate_normal(np.zeros(3),fc,size=L)
                x=m+factors@B+rng.multivariate_normal(np.zeros(n),noise,size=L)
                for r in [r for r in rows if r['design']==design and r['window']==L and r['seed']==seed]:
                    _,v,_=estimate_covariance(x,r['estimator'],factors)
                    target=np.array(r['target']);raw=np.array(r['raw']);joint=np.array(r['joint'])
                    F=lambda u:float(m@u-5*u@v@u-.001*abs(u-p).sum())
                    T=lambda u:float(m@u-5*u@truth@u-.001*abs(u-p).sum())
                    checks=dict(covariance_relative_error=float(np.linalg.norm(v-truth)/np.linalg.norm(truth)),
                        target_true_gap=T(oracle[design])-T(target),raw_true_gap=T(oracle[design])-T(raw),joint_true_gap=T(oracle[design])-T(joint),
                        raw_fit_gap=F(target)-F(raw),joint_fit_gap=F(target)-F(joint),joint_distance=float(np.linalg.norm(joint-target)))
                    for k,a in checks.items():maxerror=max(maxerror,abs(a-r[k]))
                    for u in [target,raw,joint]:assert abs(u.sum()-1)<1e-7 and u.min()>-1e-7
                    A=1+10*m@target;Q=lambda u:m@u-5/A*u@(v+np.outer(m,m))@u-.001/A*abs(u-p).sum()
                    identity_error=max(identity_error,abs(A*Q(joint)-F(joint)+5*(m@joint-m@target)**2-5*(m@target)**2))
    assert maxerror<1e-10 and identity_error<1e-12
    report.append(dict(n_assets=n,problems=len(rows),max_reconstruction_error=maxerror,max_identity_error=identity_error))
fin=json.loads((ROOT/'results/covariance_simulation/financing.json').read_text());error=0.
for r in fin:
    m=np.array(r['m']);v=np.array(r['covariance']);p=np.array(r['prev']);target=np.array(r['target']);A=r['A'];joint=np.array(r['joint'])
    for name in ['target','joint','partial']:
        u=np.array(r[name]);assert u.min()>=-.5-1e-7 and u.max()<=.8+1e-7 and abs(u).sum()<=1.6+1e-7 and -1e-7<=u.sum()<=1.5+1e-7
        F=m@u-5*u@v@u-financing_cost(u,p)
        Q=m@u-5/A*u@(v+np.outer(m,m))@u-financing_cost(u,p)/A
        error=max(error,abs(A*Q-F+5*(m@u-m@target)**2-5*(m@target)**2))
assert error<1e-12
(ROOT/'results/covariance_simulation/verification.json').write_text(json.dumps(dict(simulation=report,financing_states=len(fin),financing_identity_error=error),indent=2))
print(report,'financing',error)
