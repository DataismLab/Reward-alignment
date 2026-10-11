from pathlib import Path
import subprocess,concurrent.futures
import argparse
a=argparse.ArgumentParser();a.add_argument('--tex-bin',default='');args=a.parse_args()
r=Path(__file__).resolve().parents[1]/'submissions';b=(args.tex_bin.rstrip('/')+'/') if args.tex_bin else ''
def build(name):
 p=r/name
 with open(p/'build.txt','w') as f:
  for exe,args in [('pdflatex',['-interaction=nonstopmode','-halt-on-error','paper.tex']),('bibtex',['paper'])]+[('pdflatex',['-interaction=nonstopmode','-halt-on-error','paper.tex'])]*3:
   subprocess.run([b+exe,*args],cwd=p,stdout=f,stderr=subprocess.STDOUT,check=True)
 return name
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 for name in pool.map(build,['iafm','raiops4fin','market-microstructure']):print(name,'built',flush=True)
