"""Generate publication tables/figures directly from checked saved results."""
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mvrl.historical import ROOT

w=ROOT/'results/paper_assets';out=ROOT/'results/historical/covariance'
(w/'figures').mkdir(parents=True,exist_ok=True)
report=json.loads((out/'summary.json').read_text());cases={(r['n_assets'],r['estimator']):r for r in report['results']}
def summary(n,e,method):return next(r for r in cases[n,e]['summary'] if r['method']==method)
names={'sample':'Sample','diag10':'Fixed diagonal','lw_identity':'LW identity','lw_correlation':'LW correlation','market':'Market factor','ff3':'Three factors','lw_nonlinear':'LW nonlinear'}
order=['sample','diag10','lw_identity','lw_correlation','market','ff3','lw_nonlinear']

# All Table 1 distances use the SAME original-diagonal target common states.
# Covariance-model changes are explicitly different from within-estimator gaps.
primary=json.loads((ROOT/'results/historical/summary.json').read_text())['summary'];old={r['method']:r for r in primary}
rows=[]
def add(label,source,method=None,estimator=None,bold=False):
    r=old[method] if estimator is None else summary(10,estimator,'target')
    distance=r['distance'] if estimator is None else cases[10,estimator]['cross_target_distance']
    gap=r['target_gap'] if estimator is None else cases[10,estimator]['cross_target_gap']
    vals=[label,source,f'{distance:.5f}',f'{max(gap,0)*1e4:.4f}',f"{r['sharpe']:.3f}",f"{r['mv_month']*1e4:.3f}"]
    if bold:vals=[r'\textbf{'+v+'}' for v in vals]
    rows.append(' & '.join(vals)+r' \\')
add('Fitted MV reference','Markowitz (1952)',method='target')
add('Minimum variance','Markowitz (1952)',method='minvar')
add('MV, LW identity','Ledoit--Wolf (2004)',estimator='lw_identity')
add('MV, LW correlation','Ledoit--Wolf (2004)',estimator='lw_correlation')
add('MV, market factor','Fan et al. (2008)',estimator='market')
add('MV, three factors','Fan et al. (2008)',estimator='ff3')
add('Equal weight','DeMiguel et al. (2009)',method='equal')
add('MV, LW nonlinear','Ledoit--Wolf (2017)',estimator='lw_nonlinear')
add('Raw second moment','Kolm--Ritter (2019)',method='raw')
add('MVPI adaptation','Zhang et al. (2021)',method='mvpi')
old['one_step_mvpi']=summary(10,'diag10','one_step_mvpi')
add('One MVPI step','Zhang et al. (2021)',method='one_step_mvpi')
pnl=summary(10,'diag10','pnl25');old['pnl25']=pnl
add('Assetwise PnL, restricted','Habibnia--Soltanzadeh (2024)',method='pnl25')
add('Log minus variance','Jiang et al. (2025)',method='log_variance')
add('MV, sample covariance','Sample control (2026)',estimator='sample')
add('Log utility','Log-utility control (2026)',method='log')
add('Unconstrained scalar','Analytical control (2026)',method='scalar')
add('Risk-only calibration','Calibration ablation (2026)',method='penalty_only')
rows.append(r'\midrule');add('Joint calibration (ours)','This study (2026)',method='joint',bold=True)
table=r'''\begin{tabular}{@{}p{.235\textwidth}p{.25\textwidth}rrrr@{}}\toprule
Method & Source / role & \shortstack{Allocation\\distance} & \shortstack{Reference gap\\(bp)} & \shortstack{Excess\\Sharpe} & \shortstack{Realised MV\\(bp)}\\\midrule
'''+ '\n'.join(rows)+ '\n'+r'\bottomrule\end{tabular}'+'\n'
(w/'results_table.tex').write_text(table)

rows=[]
for n in [10,30,49]:
    for e in order:
        raw=summary(n,e,'raw');scalar=summary(n,e,'scalar');joint=summary(n,e,'joint');mv=summary(n,e,'target');mini=summary(n,e,'minvar')
        mant,exp=f"{joint['distance']:.2e}".split('e')
        jd=r'$\mathbf{'+mant+r'\times10^{'+str(int(exp))+'}}$'
        rows.append(f"{n} & {names[e]} & {raw['distance']:.5f} & {scalar['distance']:.5f} & {jd} & {mv['mv_month']*1e4:.3f} & {mini['mv_month']*1e4:.3f}"+r' \\')
    if n!=49:rows.append(r'\midrule')
table=r'''\begin{tabular}{rlrrrrr}\toprule
$N$ & Covariance & Raw distance & Scalar distance & \textbf{Joint (ours)} & \shortstack{Target/joint\\MV (bp)} & \shortstack{Minimum-variance\\MV (bp)}\\\midrule
'''+ '\n'.join(rows)+'\n'+r'\bottomrule\end{tabular}'+'\n'
(w/'covariance_table.tex').write_text(table)
pd.DataFrame([dict(n_assets=n,estimator=e,**s) for (n,e),r in cases.items() for s in r['summary']]).to_csv(out/'all_methods.csv',index=False)

print('Tables generated from saved results; use plot_final_covariance.py for the final figure')
