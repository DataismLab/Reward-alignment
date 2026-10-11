"""Package final workshop alternatives and a separate private research archive."""
from pathlib import Path
import zipfile, shutil, hashlib, json
r=Path(__file__).resolve().parents[1]; dest=r.parent; s=r/'submissions'
deliveries=[]
for key in ['iafm','raiops4fin','market-microstructure','ai4f']:
    w=s/key; pdf=dest/f'paper-{key}-2026.pdf'; shutil.copy2(w/'paper.pdf',pdf)
    archive=dest/f'{key}-2026-latex.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for name in ['paper.tex','references.bib','results_table.tex','paper.bbl','acmart.cls','ACM-Reference-Format.bst']:
            z.write(w/name,name)
        for p in sorted((w/'figures').glob('*.pdf')):z.write(p,'figures/'+p.name)
        z.writestr('README.txt',f'Matin Tavakoli: {key} named manuscript source. Select paper.tex in Overleaf/current TeX Live. Compile pdfLaTeX, BibTeX, then pdfLaTeX three times. No submission has been made. See the accompanying submission guide for venue rules.\n')
    deliveries.extend([pdf,archive])
    if key=='ai4f':continue
    anonpdf=dest/f'paper-{key}-2026-anonymous.pdf';shutil.copy2(w/'paper-anonymous.pdf',anonpdf)
    anonzip=dest/f'{key}-2026-anonymous-latex.zip'
    with zipfile.ZipFile(anonzip,'w',zipfile.ZIP_DEFLATED) as z:
        for source,target in [('paper-anonymous.tex','paper.tex'),('paper-anonymous.bbl','paper.bbl'),('references.bib','references.bib'),('results_table.tex','results_table.tex'),('acmart.cls','acmart.cls'),('ACM-Reference-Format.bst','ACM-Reference-Format.bst')]:z.write(w/source,target)
        for q in sorted((w/'figures').glob('*.pdf')):z.write(q,'figures/'+q.name)
        z.writestr('README.txt','Anonymous blind-review source. Compile paper.tex with pdfLaTeX and BibTeX. No submission made.\n')
    deliveries.extend([anonpdf,anonzip])
shutil.copy2(s/'SUBMISSION_GUIDE.md',dest/'SUBMISSION_GUIDE.md')
shutil.copy2(s/'ai4f/SUBMISSION_READINESS.md',dest/'AI4F_SUBMISSION_READINESS.md')
with zipfile.ZipFile(dest/'ai4f-2026-submission-kit.zip','w',zipfile.ZIP_DEFLATED) as z:
    for name in ['paper-ai4f-2026.pdf','ai4f-2026-latex.zip','AI4F_SUBMISSION_READINESS.md']:z.write(dest/name,name)
    z.write(s/'ai4f/OPENREVIEW_FIELDS.txt','OPENREVIEW_FIELDS.txt')
with zipfile.ZipFile(dest/'icaif-2026-submission-kit.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in deliveries:z.write(p,('anonymous/' if 'anonymous' in p.name else 'named/')+p.name)
    z.write(dest/'AI4F_SUBMISSION_READINESS.md','AI4F_SUBMISSION_READINESS.md')
    z.write(s/'ai4f/OPENREVIEW_FIELDS.txt','AI4F_OPENREVIEW_FIELDS.txt')
    for ext in ['pdf','tex']:z.write(r/f'IMPLEMENTATION_REPORT_V2.{ext}',f'report/IMPLEMENTATION_REPORT_V2.{ext}')
    for name in ['SUBMISSION_GUIDE.md','CMT_FIELDS.txt','verification.json']:z.write(s/name,name)
for ext in ['pdf','tex']:shutil.copy2(r/f'IMPLEMENTATION_REPORT_V2.{ext}',dest/f'IMPLEMENTATION_REPORT_V2.{ext}')
for name in ['WORKLOG.md','FINDINGS.md','IMPLEMENTATION_REPORT.md']:shutil.copy2(r/name,dest/name)
exclude={'__pycache__','.pytest_cache','qa','qa-v2','report-v2-qa','final-three-qa','.git','tmp'}
files=[p for p in r.rglob('*') if p.is_file() and not any(x in exclude for x in p.relative_to(r).parts) and p.suffix not in {'.aux','.out','.log','.blg','.fls','.fdb_latexmk','.toc'} and p.name not in {'.DS_Store','delivery_manifest.json'}]
manifest={str(p.relative_to(r)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}
(r/'results/delivery_manifest.json').write_text(json.dumps(manifest,indent=2));files.append(r/'results/delivery_manifest.json')
with zipfile.ZipFile(dest/'mvrl-complete-updated-code.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in files:z.write(p,str(Path(r.name)/p.relative_to(r)))
    z.write(dest/'CONTINUE_HERE.md','CONTINUE_HERE.md')
for p in [x for x in deliveries if x.suffix=='.zip']+[dest/'icaif-2026-submission-kit.zip',dest/'mvrl-complete-updated-code.zip']:
    with zipfile.ZipFile(p) as z:assert z.testzip() is None
    print(p.name,round(p.stat().st_size/1e6,2),'MB; integrity PASS')
