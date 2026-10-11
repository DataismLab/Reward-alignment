"""Compile the anonymous paper with installed official ACM/TeX Live packages."""
from pathlib import Path
import argparse,subprocess
p=argparse.ArgumentParser();p.add_argument('--tex-bin',default='');a=p.parse_args()
root=Path(__file__).resolve().parents[1]/'workshop'
def call(name,*args):
    exe=str(Path(a.tex_bin)/name) if a.tex_bin else name
    subprocess.run([exe,*args],cwd=root,check=True)
call('pdflatex','-interaction=nonstopmode','-halt-on-error','paper.tex')
call('bibtex','paper')
for _ in range(3):call('pdflatex','-interaction=nonstopmode','-halt-on-error','paper.tex')
