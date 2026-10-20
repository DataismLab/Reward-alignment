import json
import numpy as np
import pandas as pd
from mvrl.historical import ROOT

out=ROOT/'results/historical/covariance';results=[];series={}
for f in sorted(out.glob('[0-9]*_*.json')):
    d=json.loads(f.read_text());n=d['n_assets'];e=d['estimator'];frame=pd.DataFrame(d['records'])
    target=frame[frame.method=='target'].sort_values('date')
    series[n,e]=(target.return_net-target.rf).to_numpy()
    results.append(dict(n_assets=n,estimator=e,summary=d['summary'],bootstrap=d['bootstrap'],
        cross_target_distance=float(np.mean([s['cross_target_distance'] for s in d['states']])),
        cross_target_gap=float(np.mean([s['cross_target_gap'] for s in d['states']])),
        mean_condition=float(np.mean([s['condition'] for s in d['states']])),
        mean_shrinkage=float(np.mean([s['shrinkage'] for s in d['states']])) if 'shrinkage' in d['states'][0] else None,
        mean_gaussian_score=float(np.mean([s['gaussian_score'] for s in d['states']])),subperiods=d['subperiods']))
assert len(results)==21
keys=[k for k in series if k[1]!='diag10'];rng=np.random.default_rng(8128)
score=lambda x:x.mean(-1)-5*x.var(-1,ddof=1)
est=np.array([score(series[k])-score(series[k[0],'diag10']) for k in keys]);boot=[]
for _ in range(1000):
    idx=((rng.integers(432,size=36)[:,None]+np.arange(12))%432).ravel()
    boot.append([score(series[k][idx])-score(series[k[0],'diag10'][idx]) for k in keys])
boot=np.array(boot);q=float(np.quantile(np.max(abs(boot-est),axis=1),.95))
paired=[dict(n_assets=k[0],estimator=k[1],delta=float(est[i]),ci95=np.quantile(boot[:,i],[.025,.975]).tolist(),
    simultaneous95=[float(est[i]-q),float(est[i]+q)]) for i,k in enumerate(keys)]
anchors=[]
for f in out.glob('49_*.json'):
    d=json.loads(f.read_text());anchors.extend([dict(estimator=d['estimator'],**a) for a in d['anchors']])
report=dict(results=results,estimator_comparisons=paired,simultaneous_band_halfwidth=q,
    anchor_summary=pd.DataFrame([dict(estimator=a['estimator'],anchor_type=a['anchor_type'],target_gap=a['target_gap'],upper=a['bound']['target_gap_upper'],distance=a['distance']) for a in anchors]).groupby(['estimator','anchor_type']).mean().reset_index().to_dict('records'))
(out/'summary.json').write_text(json.dumps(report,indent=2))
sim=[]
for p in (ROOT/'results/covariance_simulation').glob('n*.json'):sim+=json.loads(p.read_text())
sf=pd.DataFrame(sim);means=sf.groupby(['n_assets','window','design','estimator']).mean(numeric_only=True).reset_index()
means.to_csv(ROOT/'results/covariance_simulation/summary.csv',index=False)
sim_pairs=[]
for (n,L,design),g in sf.groupby(['n_assets','window','design']):
    base=g[g.estimator=='sample'].sort_values('seed').target_true_gap.to_numpy()
    for name,h in g.groupby('estimator'):
        z=h.sort_values('seed').target_true_gap.to_numpy()-base
        # Matched seeds, t interval; descriptive, no selected-method superiority claim.
        from scipy.stats import t
        se=z.std(ddof=1)/np.sqrt(len(z));hw=float(t.ppf(.975,len(z)-1)*se)
        sim_pairs.append(dict(n_assets=int(n),window=int(L),design=design,estimator=name,mean=float(z.mean()),ci95=[float(z.mean()-hw),float(z.mean()+hw)]))
(ROOT/'results/covariance_simulation/paired.json').write_text(json.dumps(sim_pairs,indent=2))
print('21 cases; estimator comparisons with simultaneous path bands; 2160 simulated fitted problems')
for r in results:
    s={v['method']:v for v in r['summary']}
    print(r['n_assets'],r['estimator'],'covD',round(r['cross_target_distance'],5),'rawD',round(s['raw']['distance'],5),'jointD',f"{s['joint']['distance']:.3g}")
print('simultaneous halfwidth bp',q*1e4)
