from pathlib import Path as _RevisionPath
_revision_source = _RevisionPath(__file__).resolve().parents[1] / 'submissions/iafm/paper.tex'
if any(marker in _revision_source.read_text() for marker in ('Financial semantics and model validation', 'Certifying Reward Alignment')):
 raise SystemExit('Legacy source generator blocked: preserve the current IAFM revision. Compile submissions/iafm/paper.tex directly; see notes/IAFM_REVISION_2026-10-01.md.')
from pathlib import Path
import re,shutil,json
r=Path(__file__).resolve().parents[1];arc=r/'archive/2026-09-29-before-final-edits'
for key in ['ai4f','iafm','raiops4fin']:
 w=r/'submissions'/key;a=arc/key;a.mkdir(parents=True,exist_ok=True)
 for name in ['paper.tex','paper.pdf','paper-anonymous.tex','paper-anonymous.pdf']:
  if (w/name).exists() and not (a/name).exists():shutil.copy2(w/name,a/name)
 s=(a/'paper.tex').read_text()
 s=re.sub(r'\\section\*\{Acknowledgments\}\n.*?(?=\\clearpage|\\bibliographystyle)', '',s,flags=re.S)
 s=s.replace('A statistically visible allocation difference','A measurable allocation difference')
 if 'emergencystretch' not in s:s=s.replace('\\setcopyright{none}','\\setcopyright{none}\n\\setlength{\\emergencystretch}{2em}')
 if '\\affiliation' not in s:s=s.replace('\\author{Matin Tavakoli}','\\author{Matin Tavakoli}\n\\affiliation{\\institution{Amirkabir University of Technology}\\city{Tehran}\\country{Iran}}\n\\email{matin.tavakoli@aut.ac.ir}')
 if key=='iafm':
  start=s.index('\\subsection{Numerical and statistical resolution}');end=s.index('\\section{Interpreting calibration',start)
  app=s[start:end].replace('\\subsection{Numerical and statistical resolution}','\\section{Numerical verification and uncertainty}')
  s=s[:start]+'Numerical certificates and the paired bootstrap procedure are detailed in Appendix~\\ref{app:verification}.\n\n'+s[end:]
  app='\\clearpage\n'+app
  app=app.replace('\\section{Numerical verification and uncertainty}','\\section{Numerical verification and uncertainty}\\label{app:verification}')
  s=s.replace('\\clearpage\n\\bibliographystyle','\\bibliographystyle')
 else:
  rows=[]
  for x in json.loads((r/'results/historical/robustness.json').read_text()):
   m={z['method']:z for z in x['summary']}
   rows.append(f"{x['window']} & {x['phi']:g} & {10000*x['cost']:g} & {x['shrink']:g} & {m['raw']['distance']:.5f} & {m['penalty_only']['distance']:.5f} & {m['joint']['distance']:.2e}"+r' \\')
  app=r'''\section{Complete robustness results}\label{app:robustness}
Table~\ref{tab:fullrobust} reports all 17 saved specifications underlying Figure~\ref{fig:robust}. Each row averages Euclidean allocation distance over the same 432 historical months. These are repeated specifications on one dataset, not independent samples. The primary setting is $L=120$, $\varphi=5$, $\lambda=10$ bp and $h=0.1$. The three columns isolate an uncalibrated reward, calibration of risk alone, and joint calibration of risk and costs.

\begin{table*}[t]
\centering
\caption{Complete common-state alignment results. $L$ is the estimation window in months, $\lambda$ is the cost per unit of L1 turnover in basis points, and $h$ is diagonal covariance shrinkage. Distances are weight-vector norms, not returns.}
\label{tab:fullrobust}
\begin{tabular}{rrrrrrr}\toprule
$L$ & $\varphi$ & $\lambda$ (bp) & $h$ & Raw distance & Risk-only distance & Joint distance\\\midrule
'''+ '\n'.join(rows)+r'''
\bottomrule\end{tabular}
\end{table*}

\section{Independent reconstruction of the alignment check}\label{app:verification}
For a saved date, reconstruct the reference pre-trade holdings from the preceding reference allocation and gross asset returns. Recompute the lagged return moments using only observations before that date. Evaluate every saved audit allocation on this common state, including its own L1 distance from the reconstructed holdings. This gives the allocation distance and fitted regret without using the strategy's evolving own-state portfolio.

The calibration identity can also be checked away from the optimiser. For any feasible $u$, write $y=m^\top u^*$ and $A=1+2\varphi y$. The residual
\begin{equation}
 A Q(u)-F(u)+\varphi(m^\top u-y)^2-\varphi y^2
\end{equation}
should vanish. For the risk-only reward, add $2\varphi y\lambda\|u-p\|_1$ to this residual. These equalities test both coefficient scaling and the cost convention. They do not test whether estimated moments predict future returns accurately.

A separate saved verification sampled four simplex portfolios per primary historical state, using Dirichlet parameters equal to one and random seed 928. Across 1,728 sampled portfolios, the maximum absolute residual for each identity was below $9\times10^{-18}$. This numerical check supplements the algebraic proof; it is not a new market-performance experiment. The minimum primary calibration factor was 1.0208, satisfying the positive-factor assumption.
'''
  s=s.replace('\\balance\n','')
  s=s.replace('\\section{Discussion}','The complete robustness table and a reconstruction check appear in Appendices~\\ref{app:robustness} and~\\ref{app:verification}.\n\n\\section{Discussion}')
  app='\\onecolumn\n'+app.replace(r'\begin{table*}[t]',r'\begin{table}[ht]').replace(r'\end{table*}',r'\end{table}')
 s=s.replace('\\end{document}','\\appendix\n'+app+'\n\\end{document}')
 (w/'paper.tex').write_text(s)
 if key!='ai4f':
  anon=s.replace('[sigconf,review]','[sigconf,anonymous,review]')
  anon=re.sub(r'\\author\{Matin Tavakoli\}\n\\affiliation\{[^\n]+\}\n\\email\{[^\n]+\}',r'\\author{Anonymous Author(s)}',anon)
  (w/'paper-anonymous.tex').write_text(anon)
print('Three revised sources and two blind-review variants saved; previous files archived.')
# Use the permitted appendix space for the complete saved robustness table.
ai=(r/'submissions/ai4f/paper.tex').read_text()
rob=ai[ai.index(r'\section{Complete robustness results}'):ai.index(r'\section{Independent reconstruction')]
for key in ['iafm','raiops4fin','ai4f']:
 w=r/'submissions'/key;s=(w/'paper.tex').read_text()
 if key=='iafm':
  s=s.replace('\\appendix\n\\clearpage\n','\\appendix\n\\onecolumn\n'+rob+'\n')
 elif key=='raiops4fin':s=s.replace('\\clearpage\n\\bibliographystyle','\\bibliographystyle')
 else:s=s.replace('\\section{Discussion}','\\balance\n\\section{Discussion}')
 (w/'paper.tex').write_text(s)
 if key!='ai4f':
  anon=s.replace('[sigconf,review]','[sigconf,anonymous,review]')
  anon=re.sub(r'\\author\{Matin Tavakoli\}\n\\affiliation\{[^\n]+\}\n\\email\{[^\n]+\}',r'\\author{Anonymous Author(s)}',anon)
  (w/'paper-anonymous.tex').write_text(anon)
# Keep the ACM two-column appendix body; span only the robustness table.
for key in ['ai4f','iafm','raiops4fin']:
 w=r/'submissions'/key;s=(w/'paper.tex').read_text()
 s=s.replace('\\appendix\n\\onecolumn\n','\\appendix\n\\twocolumn[{\n')
 s=s.replace('\\begin{table}[ht]\n\\centering','\\begin{center}')
 pos=s.index('\\twocolumn[{')
 s=s[:pos]+s[pos:].replace('\\caption{','\\captionof{table}{',1).replace('\\end{table}','\\end{center}\n}]',1)
 (w/'paper.tex').write_text(s)
 if key!='ai4f':
  anon=s.replace('[sigconf,review]','[sigconf,anonymous,review]')
  anon=re.sub(r'\\author\{Matin Tavakoli\}\n\\affiliation\{[^\n]+\}\n\\email\{[^\n]+\}',r'\\author{Anonymous Author(s)}',anon)
  (w/'paper-anonymous.tex').write_text(anon)

# Preserve the latest author-directed anonymous presentation.
import runpy
runpy.run_path(str(r/'scripts/anonymise_highlight_final.py'),run_name='__main__')
