"""Run the fixed dimension extension. See notes/DIMENSION_PROTOCOL.md."""
import hashlib,json
from mvrl.historical import ROOT,data,run,summary,bootstrap
out=ROOT/'results/historical/dimensions';out.mkdir(parents=True,exist_ok=True)
results=[]
for n in (10,30,49):
    path=out/f'industry{n}.json'
    if n==10:
        records=[x for x in json.loads((out.parent/'primary.json').read_text()) if x['method'] not in ('mvpi','log','log_variance')]
    elif path.exists():
        records=json.loads(path.read_text())
    else:
        print(f'Running {n} industries',flush=True)
        records=run(include_mvpi=False,include_log=False,n_assets=n)
    path.write_text(json.dumps(records))
    row=dict(n_assets=n,n_over_window=n/120,moment_entries=n+n*(n+1)//2,
        summary=summary(records),bootstrap=[bootstrap(records,base=k) for k in ('raw','equal')],
        max_certificate=max(x['max_certificate'] for x in records),
        max_joint_distance=max(x['distance'] for x in records if x['method']=='joint'))
    results.append(row);(out/'summary.json').write_text(json.dumps(results,indent=2))
    print(json.dumps(row),flush=True)
manifest=[]
for n in (10,30,49):
    p=ROOT/f'data/raw/{n}_Industry_Portfolios_CSV.zip'
    manifest.append(dict(n_assets=n,file=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
        source=f'https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/{n}_Industry_Portfolios_CSV.zip',
        vintage='202608',retrieved='2026-09-26' if n==10 else '2026-10-01',months=len(data(n))))
(out/'manifest.json').write_text(json.dumps(manifest,indent=2))
