"""Package current workshop outputs without overwriting historical proposals."""
from pathlib import Path
import zipfile,shutil,hashlib,json
r=Path(__file__).resolve().parents[1];dest=r.parent;w=r/'workshop'
shutil.copy2(w/'paper.pdf',dest/'paper-iafm-2026.pdf')
for name in ['WORKLOG.md','FINDINGS.md','IMPLEMENTATION_REPORT.md']:shutil.copy2(r/name,dest/name)
with zipfile.ZipFile(dest/'iafm-2026-latex.zip','w',zipfile.ZIP_DEFLATED) as z:
    for name in ['paper.tex','references.bib','results_table.tex','paper.bbl']:
        z.write(w/name,name)
    for p in sorted((w/'figures').glob('*.pdf')):z.write(p,'figures/'+p.name)
    for name in ['acmart.cls','ACM-Reference-Format.bst']:
        if (w/name).exists():z.write(w/name,name)
    z.writestr('README.txt','Anonymous IAFM 2026 paper. Select paper.tex; use current TeX Live or Overleaf. Compile pdfLaTeX, BibTeX, pdfLaTeX three times. Official ACM class/fonts required. Four figures; six pages. No submission has been made. Workshop is non-archival.\n')
# Full private research archive includes prior editions; it is not anonymous.
exclude={'__pycache__','.pytest_cache','qa','.git','tmp'}
files=[p for p in r.rglob('*') if p.is_file() and not any(x in exclude for x in p.relative_to(r).parts) and p.suffix not in {'.aux','.out','.log','.blg','.fls','.fdb_latexmk'} and p.name not in {'.DS_Store','delivery_manifest.json'}]
manifest={str(p.relative_to(r)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}
(r/'results/delivery_manifest.json').write_text(json.dumps(manifest,indent=2));files.append(r/'results/delivery_manifest.json')
with zipfile.ZipFile(dest/'mvrl-complete-updated-code.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in files:z.write(p,str(Path(r.name)/p.relative_to(r)))
    z.write(dest/'CONTINUE_HERE.md','CONTINUE_HERE.md')
for name in ['iafm-2026-latex.zip','mvrl-complete-updated-code.zip']:
    with zipfile.ZipFile(dest/name) as z:assert z.testzip() is None
    print(name,round((dest/name).stat().st_size/1e6,2),'MB; integrity PASS')
