from pathlib import Path
import csv,json,time
import numpy as np
from mvrl.dependent import demo_market,RegimePolicy,equilibrium,distance,evaluate
from mvrl.equilibrium_learning import collect_samples
from mvrl.equilibrium_audit import exact_audit
from mvrl.neural_equilibrium import train


def main():
    dest=Path('results/rl-extension/neural');dest.mkdir(parents=True,exist_ok=True)
    start=time.time();rows=[]
    for persistence in (.5,.8,.95):
        for T in (4,12,24):
            m=demo_market(persistence=persistence,horizon=T);eq,_=equilibrium(m,1.)
            for seed in range(5):
                r,j=collect_samples(m,2048,seed)
                for method in ('paired_mean','paired_centered','myopic'):
                    key=f'p{persistence}_T{T}_seed{seed}_{method}'
                    cache=dest/(key+'.npz')
                    if cache.exists():
                        saved=np.load(cache)
                        records=[dict(step=s,actions=saved[f'u{s}'],critic=saved[f'c{s}'],
                                      critic_loss=float(saved[f'cl{s}']),actor_loss=float(saved[f'al{s}'])) for s in (250,1000,3000)]
                    else:
                        records=train(r,j,1.,m.riskless,seed,method)
                        saved={}
                        for rec in records:
                            s=rec['step'];saved.update({f'u{s}':rec['actions'],f'c{s}':rec['critic'],f'cl{s}':rec['critic_loss'],f'al{s}':rec['actor_loss']})
                        np.savez_compressed(cache,**saved)
                    for rec in records:
                        u,c=rec['actions'],rec['critic'];au=exact_audit(m,u,c,1.)
                        pol=RegimePolicy(np.zeros_like(u),u)
                        rows.append(dict(persistence=persistence,horizon=T,seed=seed,method=method,step=rec['step'],
                            D=distance(m,pol,eq),max_deviation=au['exploitability'].max(),certificate=au['bound'].max(),
                            critic_loss=rec['critic_loss'],**evaluate(m,pol,1.)))
                print(f'finished p={persistence}, T={T}, seed={seed}',flush=True)
    with (dest/'runs.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (dest/'runtime.json').write_text(json.dumps(dict(seconds=time.time()-start,rows=len(rows)),indent=2))


if __name__=='__main__':main()
