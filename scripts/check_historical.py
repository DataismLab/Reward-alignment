"""Validate saved historical evidence independently of strategy execution."""
from pathlib import Path
import json,hashlib
import numpy as np
from mvrl.historical import data,moments,objective,summary
ROOT=Path(__file__).resolve().parents[1];path=ROOT/'results/historical'
for item in json.loads((ROOT/'results/september26_downloads.json').read_text()):
    if item.get('sha256') and item['path'].startswith('data/'):
        assert hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest()==item['sha256']
r=json.loads((path/'primary.json').read_text());f=data();assets=f.iloc[:,:-1].to_numpy();rf=f.RF.to_numpy();ix={int(d):i for i,d in enumerate(f.index)}
assert len(r)==4320
prev={name:np.ones(10)/10 for name in {x['method'] for x in r}}
common=np.ones(10)/10;count=0
for date in sorted({x['date'] for x in r}):
    t=ix[date];g=[x for x in r if x['date']==date];m,v=moments(assets[t-120:t]-rf[t-120:t,None]);target=next(x for x in g if x['method']=='target');u=np.array(target['audit_weights']);best=objective(m,v,u,5,common,.001)
    for x in g:
        w=np.array(x['weights']);a=np.array(x['audit_weights']);assert x['fit_end']<date and x['fit_start']==int(f.index[t-120])
        assert abs(w.sum()-1)<1e-7 and w.min()>-1e-7
        turn=abs(w-prev[x['method']]).sum();gross=w@assets[t]
        assert abs(turn-x['turnover'])<1e-10
        assert abs(gross-.001*turn-x['return_net'])<1e-10
        gap=best-objective(m,v,a,5,common,.001)
        assert abs(gap-x['target_gap'])<1e-12 and gap>-1e-8
        assert abs(np.linalg.norm(a-u)-x['distance'])<1e-12
        prev[x['method']]=w*(1+assets[t])/(1+gross);count+=1
    common=prev['target'].copy()
saved=json.loads((path/'summary.json').read_text())['summary']
for x,y in zip(saved,summary(r)):
    for k in x:
        if isinstance(x[k],(float,int)):assert abs(x[k]-y[k])<1e-10
rob=json.loads((path/'robustness.json').read_text());assert len(rob)==17
assert max(next(z['distance'] for z in a['summary'] if z['method']=='joint') for a in rob)<2e-7
learn=json.loads((path/'learning.json').read_text())['records'];assert len(learn)==60
for x in learn:
    assert abs(x['target_gap']-x['design_gap']-x['signed_learning_difference'])<1e-12
    assert x['reward_learning_gap']>-1e-8
print(f'PASS: {count} decisions, past-only dates, constraints, drift/cost accounting, common-state gaps, summaries, 17 settings and 60 optimisation records.')
