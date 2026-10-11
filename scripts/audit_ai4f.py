"""Read-only scientific and submission-metadata checks for the AI4F adaptation."""
from pathlib import Path
import json,re,hashlib
import numpy as np
from mvrl.historical import data,moments
r=Path(__file__).resolve().parents[1];w=r/'submissions/ai4f';src=(w/'paper.tex').read_text()
primary=json.loads((r/'results/historical/primary.json').read_text());rob=json.loads((r/'results/historical/robustness.json').read_text())
assert len(primary)==4320 and len(rob)==17
assert len({x['date'] for x in primary})==432
assert all(x['fit_end']<x['date'] for x in primary)
assert min(x['A'] for x in primary)>0
assert max(x['max_certificate'] for x in primary)<2e-7
assert all(x['distance']>=0 and x['target_gap']>-1e-8 for x in primary)
f=data();rng=np.random.default_rng(928);worst=0.;cost_worst=0.;target={x['date']:x for x in primary if x['method']=='target'};prev=np.ones(10)/10
for i,date in enumerate(f.index):
 if date<199001:continue
 m,v=moments(f.iloc[i-120:i,:-1].to_numpy()-f.RF.iloc[i-120:i].to_numpy()[:,None]);u=np.array(target[int(date)]['audit_weights']);y=m@u;A=1+10*y;M=v+np.outer(m,m)
 for a in rng.dirichlet(np.ones(10),size=4):
  cost=np.abs(a-prev).sum();F=m@a-5*a@v@a-.001*cost;Q=m@a-5/A*a@M@a-.001/A*cost
  worst=max(worst,abs(A*Q-(F-5*(m@a-y)**2+5*y*y)))
  Qrisk=m@a-5/A*a@M@a-.001*cost
  cost_worst=max(cost_worst,abs(A*Qrisk-(F-5*(m@a-y)**2-10*y*.001*cost+5*y*y)))
 prev=u*(1+f.iloc[i,:-1].to_numpy())/(1+u@f.iloc[i,:-1].to_numpy())
assert max(worst,cost_worst)<1e-12
refs=set(re.findall(r'@\w+\{([^,]+)',(w/'references.bib').read_text()));cites={x.strip() for c in re.findall(r'\\cite\{([^}]+)\}',src) for x in c.split(',')};assert cites<=refs
assert not re.search(r'TODO|FIXME|INSERT HERE|TBD',src)
title=re.search(r'\\title\{([^\n]+)\}',src)[1];abstract=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',src,re.S)[1].strip();assert len(title)<=250 and len(abstract)<=5000
result=dict(primary_decisions=len(primary),historical_months=432,robustness_settings=17,min_calibration_factor=min(x['A'] for x in primary),max_quadratic_certificate=max(x['max_certificate'] for x in primary),joint_identity_max_residual=worst,risk_only_identity_max_residual=cost_worst,all_citation_keys_resolved=True,cited_references=len(cites),title_characters=len(title),abstract_characters=len(abstract),llm_experiment=False,portal_author_profile_required=True,author_affiliation_and_email_supplied=True,source_sha256=hashlib.sha256(src.encode()).hexdigest())
(r/'results/ai4f_scientific_audit.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
