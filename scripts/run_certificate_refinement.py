"""Exploratory tighter bounds after primary Hoeffding audit; frozen policies."""
import json
from pathlib import Path
import numpy as np
from mvrl.dependent import demo_market
from mvrl.equilibrium_learning import collect_samples,fit_backward
from mvrl.equilibrium_audit import exact_audit,independent_sample_certificate

m=demo_market(horizon=12);rows=[]
for seed in range(20):
    u,c=fit_backward(*collect_samples(m,2048,seed),1.,m.riskless)
    r,j=collect_samples(m,32768,100000+seed)
    true=exact_audit(m,u,c,1.)['exploitability']
    for interval in ('hoeffding','bernstein'):
        for mixing in (False,True):
            out=independent_sample_certificate(u,c,r,j,1.,m.riskless,.21,
                interval=interval,estimate_mixing=mixing)
            rows.append(dict(seed=seed,interval=interval,mixing=mixing,
                true_max=float(true.max()),bound=float(out['bound'].max()),
                covered=bool(np.all(true<=out['bound'])),
                max_rho=float(out['rho_upper'].max())))
Path('results/rl-extension/certificate_refinement.json').write_text(json.dumps(rows,indent=2))
for interval in ('hoeffding','bernstein'):
    for mixing in (False,True):
        rr=[x for x in rows if x['interval']==interval and x['mixing']==mixing]
        print(interval,mixing,'mean bound',np.mean([x['bound'] for x in rr]),'coverage',sum(x['covered'] for x in rr))
