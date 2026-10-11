from pathlib import Path as _RevisionPath
_revision_source = _RevisionPath(__file__).resolve().parents[1] / 'submissions/iafm/paper.tex'
if any(marker in _revision_source.read_text() for marker in ('Financial semantics and model validation', 'Certifying Reward Alignment')):
 raise SystemExit('Legacy source generator blocked: preserve the current IAFM revision. Compile submissions/iafm/paper.tex directly; see notes/IAFM_REVISION_2026-10-01.md.')
from pathlib import Path
import re,shutil
r=Path(__file__).resolve().parents[1]
rows=[('Target','Reference objective',['0.00000','0.0000','0.570','-8.497']),('Raw second moment','Uncalibrated baseline',['0.00843','0.0148','0.573','-7.182']),('Unconstrained scalar','Analytical baseline',['0.00540','0.0043','0.568','-8.882']),('Risk-only calibration','Calibration ablation',['0.00510','0.0033','0.571','-8.365']),('MVPI adaptation',r'Zhang et al. (2021)~\cite{zhang2021}',['0.00000','0.0000','0.570','-8.497']),('Log minus variance',r'Jiang et al. (2025)~\cite{jiang2025}',['0.01286','0.0287','0.572','-7.123']),('Log utility','Log-utility control',['0.54848','39.7855','0.344','-133.295']),('Equal weight','Standard control',['0.43495','46.2626','0.622','-11.893']),('Minimum variance','Standard control',['0.23843','9.0252','0.645','5.274']),('Joint calibration (ours)','This study',['0.00000','0.0000','0.570','-8.497'])]
t=r'''\begin{tabular}{@{}p{.23\textwidth}p{.24\textwidth}rrrr@{}}\toprule
Method & Source / role & \shortstack{Allocation\\distance} & \shortstack{Fitted gap\\(bp)} & \shortstack{Excess\\Sharpe} & \shortstack{Realised MV\\(bp)}\\\midrule
'''
for m,source,vals in rows:
 cells=[m,source,*vals]
 if '(ours)' in m:t+='\\midrule\n';cells=[r'\textbf{'+v+'}' for v in cells]
 t+=' & '.join(cells)+r' \\'+'\n'
t+=r'\bottomrule\end{tabular}'+'\n'
for key in ['ai4f','iafm','raiops4fin']:
 w=r/'submissions'/key;a=r/'archive/2026-09-29-before-table-layout'/key;a.mkdir(parents=True,exist_ok=True)
 for n in ['paper.tex','paper.pdf','results_table.tex']:
  if not (a/n).exists():shutil.copy2(w/n,a/n)
 (w/'results_table.tex').write_text(t)
 s=(w/'paper.tex').read_text()
 s=s.replace('\\twocolumn[{\n\\section{Complete robustness results}', '\\twocolumn[{\n\\section*{Appendix}\n\\section{Complete robustness results}')
 s=re.sub(r'\\textbf\{(\d+\.\d+)e-(\d+)\}',lambda m:r'$\mathbf{'+m[1]+r'\times10^{-'+str(int(m[2]))+'}}$',s)
 s=s.replace('120 & 2 & 0 & 0.1 &','\\midrule\n120 & 2 & 0 & 0.1 &').replace('240 & 5 & 10 & 0 &','\\midrule\n240 & 5 & 10 & 0 &') if '\\midrule\n120 & 2' not in s else s
 (w/'paper.tex').write_text(s);(w/'paper-anonymous.tex').write_text(s)
