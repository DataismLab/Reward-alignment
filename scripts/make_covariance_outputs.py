"""Generate publication tables/figures directly from checked saved results."""
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mvrl.historical import ROOT

w=ROOT/'submissions/iafm';out=ROOT/'results/historical/covariance'
report=json.loads((out/'summary.json').read_text());cases={(r['n_assets'],r['estimator']):r for r in report['results']}
def summary(n,e,method):return next(r for r in cases[n,e]['summary'] if r['method']==method)
names={'sample':'Sample','diag10':'Fixed diagonal','lw_identity':'LW identity','lw_correlation':'LW correlation','market':'Market factor','ff3':'Three factors'}
order=['sample','diag10','lw_identity','lw_correlation','market','ff3']

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

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
fig,axes=plt.subplots(1,2,figsize=(9.8,3.1),layout='constrained')
x=np.arange(6)
for offset,key,label,color in [(-.23,'cross','Covariance-model change','#555555'),(0,'raw','Raw reward discrepancy','#cf7c22'),(.23,'joint','Joint discrepancy','#197a68')]:
    vals=[cases[49,e]['cross_target_distance'] if key=='cross' else summary(49,e,key)['distance'] for e in order]
    axes[0].bar(x+offset,np.maximum(vals,1e-9),.22,label=label,color=color)
axes[0].set_yscale('log');axes[0].set_ylim(1e-9,1);axes[0].set_xticks(x,['Sample','Fixed\ndiagonal','LW\nidentity','LW\ncorr.','Market','Three\nfactors']);axes[0].set_ylabel('Mean allocation distance');axes[0].set_title('(a) What changes the 49-industry allocation?');axes[0].legend(fontsize=7,loc='upper left')
comps={r['estimator']:r for r in report['estimator_comparisons'] if r['n_assets']==49};es=[e for e in order if e!='diag10']
for i,e in enumerate(es):
    r=comps[e];v=r['delta']*1e4;lo,hi=np.array(r['ci95'])*1e4
    axes[1].plot([lo,hi],[i,i],color='#197a68',linewidth=2);axes[1].plot(v,i,'o',color='#197a68',markersize=5)
axes[1].axvline(0,color='.6',ls='--',lw=1);axes[1].set_yticks(range(5),[names[e] for e in es]);axes[1].invert_yaxis();axes[1].set_xlabel('Monthly realised MV difference (bp)');axes[1].set_title('(b) Target versus fixed diagonal, N=49');axes[1].text(.98,.04,'Paired 95% path intervals',transform=axes[1].transAxes,ha='right',fontsize=8)
fig.savefig(w/'figures/covariance.pdf');fig.savefig(w/'figures/covariance.png',dpi=180);plt.close(fig)

df=pd.read_csv(ROOT/'results/covariance_simulation/summary.csv');df=df[(df.n_assets==100)&(df.window==120)]
fig,ax=plt.subplots(1,2,figsize=(9.8,2.55),layout='constrained')
for i,(metric,title) in enumerate([('covariance_relative_error','(a) Covariance error'),('target_true_gap','(b) Population MV regret (bp)')]):
    for shift,design,color in [(-.18,'diagonal','#197a68'),(.18,'correlated','#cf7c22')]:
        vals=[float(df[(df.estimator==e)&(df.design==design)][metric].iloc[0])*(1e4 if i else 1) for e in order]
        ax[i].bar(x+shift,vals,.35,label=design.capitalize()+' residuals',color=color)
    ax[i].set_xticks(x,['Sample','Fixed\ndiagonal','LW\nidentity','LW\ncorr.','Market','Three\nfactors']);ax[i].set_title(title);ax[i].set_ylim(bottom=0)
ax[0].set_ylabel('Relative Frobenius error');ax[1].set_ylabel('Mean regret');ax[0].legend(fontsize=8)
fig.savefig(w/'figures/covariance_simulation.pdf');fig.savefig(w/'figures/covariance_simulation.png',dpi=180);plt.close(fig)
print('Tables and figures generated from saved results')
