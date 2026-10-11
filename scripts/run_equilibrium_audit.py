"""Protocol-fixed 20-seed dependent-return study; no tuning on evaluation."""
from pathlib import Path
import csv,hashlib,json,platform,time
import numpy as np
from mvrl.dependent import demo_market,RegimePolicy,equilibrium,distance,evaluate
from mvrl.equilibrium_learning import collect_samples,fit_backward
from mvrl.equilibrium_audit import exact_audit,continuation,independent_sample_certificate


def main():
    dest=Path('results/rl-extension');dest.mkdir(parents=True,exist_ok=True)
    rows=[];policies={};start=time.time()
    for persistence in (.5,.8,.95):
        for T in (4,12,24):
            m=demo_market(persistence=persistence,horizon=T)
            eq,_=equilibrium(m,1.)
            for n in (128,512,2048,8192):
                for seed in range(20):
                    r,j=collect_samples(m,n,seed)
                    for method in ('myopic','paired_actor','paired_exact'):
                        u,c=fit_backward(r,j,1.,m.riskless,method=method)
                        audit=exact_audit(m,u,c,1.)
                        policy=RegimePolicy(np.zeros_like(u),u)
                        key=f'p{persistence}_T{T}_n{n}_seed{seed}_{method}'
                        policies[key+'_u']=u;policies[key+'_c']=c
                        rows.append(dict(persistence=persistence,horizon=T,n=n,seed=seed,method=method,
                            transitions=r.size,D=distance(m,policy,eq),
                            max_deviation=audit['exploitability'].max(),
                            certificate=audit['bound'].max(),**evaluate(m,policy,1.)))
            print(f'finished p={persistence}, T={T}',flush=True)
    with (dest/'tabular_runs.csv').open('w') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    np.savez_compressed(dest/'tabular_policies.npz',**policies)
    # Fixed diagnostic: no policy selection using independent audit samples.
    diagnostic=[]
    for seed in range(20):
        m=demo_market(horizon=12);r,j=collect_samples(m,2048,seed)
        u,c=fit_backward(r,j,1.,m.riskless)
        ar,aj=collect_samples(m,32768,100000+seed)
        finite=independent_sample_certificate(u,c,ar,aj,1.,m.riskless,.21)
        exact=exact_audit(m,u,c,1.)
        shifted=exact_audit(m,u,c+10*np.arange(13)[:,None],1.)
        diagnostic.append(dict(seed=seed,true_max=exact['exploitability'].max(),
            model_bound=exact['bound'].max(),data_bound=finite['bound'].max(),
            covered=bool(np.all(exact['exploitability']<=finite['bound'])),
            shift_bound_difference=float(np.max(np.abs(exact['bound']-shifted['bound']))),
            shifted_uniform_bound=shifted['uniform_bound'].max(),audit_observations=ar.size))
    (dest/'independent_audit.json').write_text(json.dumps(diagnostic,indent=2))
    protocol=Path('notes/rl-extension/PROTOCOL.md')
    meta=dict(protocol_sha256=hashlib.sha256(protocol.read_bytes()).hexdigest(),
        numpy=np.__version__,python=platform.python_version(),rows=len(rows),
        seconds=time.time()-start,seed_count=20,training_uses_oracle=False,
        date='2026-10-09',stage='A, controlled simulation, preliminary research')
    (dest/'manifest.json').write_text(json.dumps(meta,indent=2))
    print(json.dumps(meta,indent=2))


if __name__=='__main__':main()
