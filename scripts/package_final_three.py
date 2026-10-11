from pathlib import Path
import shutil,zipfile
r=Path(__file__).resolve().parents[1];root=r.parent;d=root/'final-three-papers';d.mkdir(exist_ok=True)
for k,n in [('ai4f','AI4F'),('iafm','IAFM'),('raiops4fin','RAIOps4Fin')]:
 stem='paper';shutil.copy2(r/'submissions'/k/(stem+'.pdf'),d/(n+'.pdf'))
with zipfile.ZipFile(root/'final-three-papers.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(d.glob('*.pdf')):z.write(p,p.name)
with zipfile.ZipFile(root/'final-three-papers-latex.zip','w',zipfile.ZIP_DEFLATED) as z:
 z.write(d/'README.txt','README.txt')
 for k,n in [('ai4f','AI4F'),('iafm','IAFM'),('raiops4fin','RAIOps4Fin')]:
  stem='paper';w=r/'submissions'/k
  for source,target in [(stem+'.tex','paper.tex'),(stem+'.bbl','paper.bbl'),('references.bib','references.bib'),('results_table.tex','results_table.tex'),('acmart.cls','acmart.cls'),('ACM-Reference-Format.bst','ACM-Reference-Format.bst')]:z.write(w/source,n+'/'+target)
  if (w/'dimension_table.tex').exists():z.write(w/'dimension_table.tex',n+'/dimension_table.tex')
  for p in (w/'figures').glob('*.pdf'):z.write(p,n+'/figures/'+p.name)
for p in [root/'final-three-papers.zip',root/'final-three-papers-latex.zip']:
 with zipfile.ZipFile(p) as z:assert z.testzip() is None
 print(p.name,'integrity PASS')
