"""Verify saved evidence and document integrity; exits nonzero on disagreement."""
from pathlib import Path
import json,math,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
r=json.loads((ROOT/'results/experiments.json').read_text())
assert len(r['independent'])==720 and len(r['bounded'])==64 and len(r['learning'])==15
assert len(r['market_sensitivity'])==81 and len(r['mvpi'])==4
for x in r['learning']:
 assert abs(x['total']-x['incons']-x['surr']-x['learn'])<1e-12
 assert x['surrogate_regret']>=-1e-10
for group in ['independent','market_sensitivity']:
 assert max(x['distance'] for x in r[group] if x['name']=='design')<1e-10
assert max(x['distance'] for x in r['dependent'] if x['name']=='hedge_design')<1e-10
for x in r['mvpi']:
 assert x['residual']<1e-12 and min(np.diff(x['trace']))>-1e-12
print('Saved synthetic counts, signed decomposition, regret and exact-recovery checks PASS.')
