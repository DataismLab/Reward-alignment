from pathlib import Path as _RevisionPath
_revision_source = _RevisionPath(__file__).resolve().parents[1] / 'submissions/iafm/paper.tex'
if any(marker in _revision_source.read_text() for marker in ('Financial semantics and model validation', 'Certifying Reward Alignment')):
 raise SystemExit('Legacy source generator blocked: preserve the current IAFM revision. Compile submissions/iafm/paper.tex directly; see notes/IAFM_REVISION_2026-10-01.md.')
"""Apply the author's anonymous-delivery and comparison-highlighting edits."""
from pathlib import Path
import re,shutil
r=Path(__file__).resolve().parents[1]
for key in ['ai4f','iafm','raiops4fin']:
 w=r/'submissions'/key;a=r/'archive/2026-09-29-before-anonymous-highlight'/key;a.mkdir(parents=True,exist_ok=True)
 for n in ['paper.tex','paper.pdf','results_table.tex']:
  if not (a/n).exists():shutil.copy2(w/n,a/n)
 s=(a/'paper.tex').read_text().replace('[sigconf,review]','[sigconf,anonymous,review]')
 s=re.sub(r'\\author\{Matin Tavakoli\}\n\\affiliation\{[^\n]+\}\n\\email\{[^\n]+\}',r'\\author{Anonymous Author(s)}',s)
 s=s.replace('\\hypersetup{pdfauthor={Matin Tavakoli}}','\\hypersetup{pdfauthor={}}')
 s=s.replace('Primary historical comparison, 1990--2025.','Reward-formulation comparison on historical data, 1990--2025. Published rewards are adapted to a common environment; complete published algorithms are not reproduced. Bold identifies our joint-calibration construction, not the best realised performance.')
 s=s.replace('Distances are weight-vector norms, not returns.','Distances are weight-vector norms, not returns. Bold identifies joint calibration (ours).')
 s=s.replace('Joint distance\\\\\\midrule',r'\textbf{Joint (ours)}\\\midrule')
 lines=s.splitlines()
 for i,line in enumerate(lines):
  if re.match(r'^\d+ & ',line) and line.count('&')==6:
   left,right=line.rsplit('&',1);v=right.replace('\\\\','').strip();lines[i]=left+'& '+r'\textbf{'+v+r'} \\'
 s='\n'.join(lines)+'\n';(w/'paper.tex').write_text(s);(w/'paper-anonymous.tex').write_text(s)
 t=(a/'results_table.tex').read_text().replace('Mean allocation distance','Allocation distance').replace('MVPI adaptation &',r'MVPI (Zhang et al., 2021)~\cite{zhang2021} &').replace('Log minus variance &',r'Log--variance (Jiang et al., 2025)~\cite{jiang2025} &')
 lines=t.splitlines()
 for i,line in enumerate(lines):
  if line.startswith('Joint calibration &'):
   cells=line.replace('\\\\','').split('&');cells[0]='Joint calibration (ours)';lines[i]=' & '.join(r'\textbf{'+v.strip()+'}' for v in cells)+r' \\'
 (w/'results_table.tex').write_text('\n'.join(lines)+'\n')
print('All three main sources anonymised; primary rows and robustness columns highlighted.')

import runpy
runpy.run_path(str(r/'scripts/refine_comparison_layout.py'),run_name='__main__')
