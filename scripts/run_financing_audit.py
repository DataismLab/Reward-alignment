import json
import numpy as np
from mvrl.historical import ROOT
from mvrl.financing import solve_financing,financing_cost

rows=[]
for seed in range(50):
    gen=np.random.default_rng(7000+seed);n=6;m=gen.uniform(-.02,.04,n)
    B=gen.normal(size=(n,n));v=.0002*(B@B.T)+np.eye(n)*.0005;p=np.ones(n)/n;phi=5.
    target,tc=solve_financing(m,phi*v,p);A=1+2*phi*(m@target);M=v+np.outer(m,m)
    joint,jc=solve_financing(m,phi/A*M,p,.001/A,.002/A,.0005/A)
    partial,pc=solve_financing(m,phi/A*M,p,.001/A,.002,.0005)
    F=lambda u:m@u-phi*u@v@u-financing_cost(u,p)
    rows.append(dict(seed=seed,m=m.tolist(),covariance=v.tolist(),prev=p.tolist(),A=float(A),
        target=target.tolist(),joint=joint.tolist(),partial=partial.tolist(),
        joint_distance=float(np.linalg.norm(joint-target)),partial_distance=float(np.linalg.norm(partial-target)),
        joint_gap=float(F(target)-F(joint)),partial_gap=float(F(target)-F(partial)),
        borrowing=float(max(target.sum()-1,0)),shorting=float(np.maximum(-target,0).sum()),
        max_certificate=max(tc,jc,pc)))
out=ROOT/'results/covariance_simulation';out.mkdir(exist_ok=True)
(out/'financing.json').write_text(json.dumps(rows,indent=2))
print('50 financing states; mean joint/partial distance',np.mean([r['joint_distance'] for r in rows]),np.mean([r['partial_distance'] for r in rows]))
