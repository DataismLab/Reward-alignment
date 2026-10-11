"""Create blind-review variants without altering the named main manuscripts."""
from pathlib import Path
import argparse,subprocess,concurrent.futures,pymupdf
p=argparse.ArgumentParser();p.add_argument('--tex-bin',default='');a=p.parse_args();b=a.tex_bin.rstrip('/')+'/' if a.tex_bin else ''
r=Path(__file__).resolve().parents[1]/'submissions'
def build(key):
 w=r/key;s=(w/'paper.tex').read_text().replace('[sigconf,review]','[sigconf,anonymous,review]').replace('\\author{Matin Tavakoli}','\\author{Anonymous Author(s)}');(w/'paper-anonymous.tex').write_text(s)
 with (w/'anonymous-build.txt').open('w') as f:
  for exe,args in [('pdflatex',['-interaction=nonstopmode','-halt-on-error','paper-anonymous.tex']),('bibtex',['paper-anonymous'])]+[('pdflatex',['-interaction=nonstopmode','-halt-on-error','paper-anonymous.tex'])]*3:
   subprocess.run([b+exe,*args],cwd=w,stdout=f,stderr=subprocess.STDOUT,check=True)
 d=pymupdf.open(w/'paper-anonymous.pdf');assert not d.metadata.get('author');assert 'Tavakoli' not in '\n'.join(x.get_text() for x in d)
 assert len(d)==(7 if key=='raiops4fin' else 8)
 return key+' anonymous PASS'
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 for x in pool.map(build,['iafm','raiops4fin','market-microstructure']):print(x,flush=True)
