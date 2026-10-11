"""Package the canonical IAFM manuscript without regenerating its source."""
from pathlib import Path
import shutil,zipfile
root=Path(__file__).resolve().parents[1];w=root/'submissions/iafm';dest=root.parent
files=['paper.tex','paper.bbl','references.bib','results_table.tex','rl_table.tex','rl_numbers.tex','acmart.cls','ACM-Reference-Format.bst']
readme='''Certifying Reward Alignment in Portfolio Reinforcement Learning
Final IAFM research manuscript — 9 October 2026
Anonymous ACM sigconf review manuscript, eight pages including references and appendix.
Compile paper.tex with its figures, bibliography and supplied ACM class (e.g. tectonic paper.tex, or a normal LaTeX/BibTeX workflow).
This archive contains complete paper source, not third-party literature PDFs or research datasets.
29 cited references, three figures and two tables. Contains the deviation-certificate proof, convex-action extension and independent-data construction; 20-seed neural and 10-seed PPO reward comparisons; six covariance estimators across 10/30/49 industries; historical estimation and calibration controls.
The contribution is financial reward alignment and finite-budget learning validation, not demonstrated historical investment superiority. All methods' final-budget runs are retained.
Use the PDF for the anonymous submission. Submission portal metadata, declarations and actual submission remain the author's responsibility. No submission has been made.
The native single-file editor cannot resolve this project's external inputs; the complete archive is compiled and checked independently.
'''
with zipfile.ZipFile(dest/'iafm-2026-latex.zip','w',zipfile.ZIP_DEFLATED) as z:
    z.writestr('README.txt',readme)
    for name in files:z.write(w/name,name)
    for name in ('rl_learning.pdf','audit_bounds.pdf','covariance.pdf'):
        p=w/'figures'/name;z.write(p,'figures/'+p.name)
with zipfile.ZipFile(dest/'iafm-2026-latex.zip') as z:assert z.testzip() is None
shutil.copy2(dest/'iafm-2026-latex.zip',dest/'iafm-2026-anonymous-latex.zip')
for name in ('paper-iafm-2026.pdf','paper-iafm-2026-anonymous.pdf'):shutil.copy2(w/'paper.pdf',dest/name)
shutil.copy2(w/'paper.pdf',dest/'final-three-papers/IAFM.pdf')
for ext in ('tex','pdf','bbl','aux','log','out'):
    p=w/('paper.'+ext)
    if p.exists():shutil.copy2(p,w/('paper-anonymous.'+ext))
print('Packaged current anonymous IAFM paper and portable source.')
