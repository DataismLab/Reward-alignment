"""Known-covariance experiment isolating estimation from reward semantics."""
import json,time
import numpy as np
from mvrl.historical import ROOT, solve_quadratic, objective
from mvrl.covariance import PRIMARY_ESTIMATORS as ESTIMATORS, estimate_covariance

out=ROOT/'results/covariance_simulation';out.mkdir(exist_ok=True)
for n in (10,49,100):
    path=out/f'n{n}.json'
    if path.exists():continue
    rows=[];tic=time.time()
    rng=np.random.default_rng(20261007+n)
    B=rng.normal(.4,.35,size=(3,n));B[0]+= .6
    factor_cov=np.diag([.03**2,.02**2,.025**2])
    sd=np.linspace(.015,.035,n);mean=np.linspace(.003,.007,n)
    p=np.ones(n)/n;phi=5.;cost=.001
    for design in ('diagonal','correlated'):
        corr=np.eye(n)
        if design=='correlated':
            for i in range(n):
                for j in range(n):
                    if i!=j and i//5==j//5:corr[i,j]=.4
        residual_cov=corr*np.outer(sd,sd)
        truth=B.T@factor_cov@B+residual_cov
        oracle,ocert=solve_quadratic(mean,phi*truth,p,cost)
        for length in (60,120):
            for seed in range(30):
                gen=np.random.default_rng(50000+1000*n+10*seed+length)
                factors=gen.multivariate_normal(np.zeros(3),factor_cov,size=length)
                residual=gen.multivariate_normal(np.zeros(n),residual_cov,size=length)
                x=mean+factors@B+residual
                for estimator in ESTIMATORS:
                    _,v,info=estimate_covariance(x,estimator,factors)
                    target,tc=solve_quadratic(mean,phi*v,p,cost)
                    M=v+np.outer(mean,mean);A=1+2*phi*(mean@target)
                    raw,rc=solve_quadratic(mean,phi*M,p,cost)
                    joint,jc=solve_quadratic(mean,phi/A*M,p,cost/A)
                    value=lambda u:objective(mean,v,u,phi,p,cost)
                    truevalue=lambda u:objective(mean,truth,u,phi,p,cost)
                    rows.append(dict(n_assets=n,window=length,design=design,seed=seed,estimator=estimator,
                        covariance_relative_error=float(np.linalg.norm(v-truth,'fro')/np.linalg.norm(truth,'fro')),
                        target_true_gap=truevalue(oracle)-truevalue(target),raw_true_gap=truevalue(oracle)-truevalue(raw),
                        joint_true_gap=truevalue(oracle)-truevalue(joint),raw_fit_gap=value(target)-value(raw),
                        joint_fit_gap=value(target)-value(joint),joint_distance=float(np.linalg.norm(joint-target)),
                        target_distance=float(np.linalg.norm(target-oracle)),min_eigenvalue=info['min_eigenvalue'],
                        max_certificate=max(ocert,tc,rc,jc),target=target.tolist(),raw=raw.tolist(),joint=joint.tolist()))
            print(n,design,length,'complete',round(time.time()-tic,1),flush=True)
    path.write_text(json.dumps(rows));print('SAVED',n,len(rows),flush=True)
