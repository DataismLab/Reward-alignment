"""Private final reproducibility archive, distinct from anonymous submission ZIP."""
from pathlib import Path
import hashlib
import json
import zipfile

root=Path(__file__).resolve().parents[1]
destination=root.parent/'mvrl-final-research-code.zip'
paths=set()
for folder in ('mvrl','tests','scripts','notes','data','results'):
    for p in (root/folder).rglob('*'):
        if p.is_file() and '__pycache__' not in p.parts and p.suffix in {
                '.py','.md','.json','.csv','.txt','.zip','.npz','.toml','.png','.pdf'}:
            paths.add(p)
for name in ('README.md','FINDINGS.md','WORKLOG.md','COVARIANCE_RESEARCH_REPORT.md',
             'RL_EXTENSION_REPORT.md','FINAL_RESEARCH_REPORT.md','pyproject.toml',
             'requirements.txt','requirements-dev.txt','pytest.ini'):
    if (root/name).exists():paths.add(root/name)
for p in (root/'literature').rglob('*'):
    if p.is_file() and p.suffix in {'.json','.md','.bib'}:paths.add(p)
w=root/'submissions/iafm'
for name in ('paper.tex','paper.pdf','paper.bbl','references.bib','results_table.tex',
             'rl_table.tex','rl_numbers.tex','acmart.cls','ACM-Reference-Format.bst',
             'SUBMISSION_READY.md'):
    paths.add(w/name)
for name in ('rl_learning.pdf','audit_bounds.pdf','covariance.pdf'):
    paths.add(w/'figures'/name)
manifest={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}
with zipfile.ZipFile(destination,'w',zipfile.ZIP_DEFLATED) as z:
    z.writestr('START_HERE.txt',
        'Final IAFM research, 9 October 2026. PRIVATE reproducibility archive, not an anonymous submission.\n'
        'Read mvrl-surrogate-gap/FINAL_RESEARCH_REPORT.md. All code, tests, cached research results,\n'
        'public market data and the current IAFM paper are included. Downloaded external papers are excluded.\n'
        'Install this project with research and test extras; exact tested environment is saved under results/rl-extension.\n'
        'Runners reuse saved outputs. Retrain in a separate copy after archiving the corresponding caches.\n'
        'No upload or contact has occurred. Author declarations and actual submission remain to be completed.\n')
    z.writestr('SHA256.json',json.dumps(manifest,indent=2))
    for p in sorted(paths):z.write(p,'mvrl-surrogate-gap/'+str(p.relative_to(root)))
with zipfile.ZipFile(destination) as z:assert z.testzip() is None
print(f'{len(paths)} files; {destination.stat().st_size/1e6:.1f} MB; {destination.name}')
