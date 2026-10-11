from pathlib import Path
import json,csv,time
import numpy as np
from mvrl.dependent import demo_market,RegimePolicy,equilibrium,distance,evaluate
from mvrl.equilibrium_learning import collect_samples
from mvrl.equilibrium_audit import exact_audit
from mvrl.ppo_alignment import train_ppo

dest=Path('results/rl-extension/ppo-final');dest.mkdir(parents=True,exist_ok=True)
rows=[];start=time.time()
for persistence in (.8,.95):
    m=demo_market(persistence,12);eq,_=equilibrium(m,1.)
    assert np.max(np.abs(eq.beta))<3 # The reference also solves the bounded game.
    for seed in range(10):
        r,j=collect_samples(m,2048,seed)
        for method in ('myopic','continuation'):
            key=f'p{persistence}_seed{seed}_{method}';cache=dest/(key+'.npz')
            if cache.exists():
                data=np.load(cache);u,c=data['u'],data['c']
            else:
                u,c,model=train_ppo(r,j,1.,m.riskless,method,seed)
                np.savez_compressed(cache,u=u,c=c);model.save(dest/key)
            au=exact_audit(m,u,c,1.,action_bounds=(-3,3));pol=RegimePolicy(np.zeros_like(u),u)
            rows.append(dict(persistence=persistence,seed=seed,method=method,D=distance(m,pol,eq),
                max_deviation=au['exploitability'].max(),certificate=au['bound'].max(),**evaluate(m,pol,1.)))
        print(f'finished p={persistence}, seed={seed}',flush=True)
with (dest/'runs.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(dest/'runtime.json').write_text(json.dumps(dict(seconds=time.time()-start,rows=len(rows)),indent=2))
