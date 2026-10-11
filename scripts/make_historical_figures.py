from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'results/historical/figures';OUT.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
s=pd.DataFrame(json.loads((ROOT/'results/historical/summary.json').read_text())['summary']).set_index('method')
names=['raw','scalar','penalty_only','joint','mvpi','log_variance','log'];labels=['Raw','Scalar','Risk only','Joint','MVPI','Log + risk','Log']
fig,ax=plt.subplots(1,2,figsize=(7,2.3));colors=['#bc5b46']*3+['#177e89']*2+['#7c6fa1']*2
ax[0].barh(labels,np.maximum(s.loc[names,'distance'],1e-10),color=colors);ax[0].set_xscale('log');ax[0].set_xlabel('Mean allocation distance (log scale)');ax[0].invert_yaxis()
ax[1].scatter(s.sharpe,1e4*s.mv_month,c='#177e89');
for k,dx,dy in [('joint',-55,12),('equal',3,-6),('minvar',-48,6),('log',4,2)]:ax[1].annotate({'joint':'Target / joint','log_variance':'Log + risk'}.get(k,k.capitalize()),(s.loc[k,'sharpe'],1e4*s.loc[k,'mv_month']),xytext=(dx,dy),textcoords='offset points',fontsize=7)
ax[1].set_xlabel('Realised annualised excess Sharpe');ax[1].set_ylabel('Monthly MV (bp)');fig.tight_layout();fig.savefig(OUT/'historical.pdf');fig.savefig(OUT/'historical.png',dpi=180);plt.close(fig)
r=json.loads((ROOT/'results/historical/robustness.json').read_text());fig,ax=plt.subplots(1,2,figsize=(7,2.3))
for method,color in [('raw','#bc5b46'),('scalar','#ba9a34'),('penalty_only','#7c6fa1'),('joint','#177e89')]:
    vals=[next(z['distance'] for z in x['summary'] if z['method']==method) for x in r];ax[0].plot(range(1,len(vals)+1),np.maximum(vals,1e-10),'.-',label=method.replace('_',' '),color=color)
ax[0].set_yscale('log');ax[0].set_xlabel('Prespecified setting (1–17)');ax[0].set_ylabel('Mean allocation distance');ax[0].legend(fontsize=6,ncol=2)
b=json.loads((ROOT/'results/historical/summary.json').read_text())['bootstrap'][:3]
for i,x in enumerate(b):
    lo,hi=np.array(x['ci95'])*1e4;y=x['estimate']*1e4;ax[1].errorbar(y,i,xerr=[[y-lo],[hi-y]],fmt='o',color='#177e89',capsize=3)
ax[1].axvline(0,c='grey',lw=.8);ax[1].set_yticks(range(3),['Joint − raw','Joint − scalar','Joint − risk only']);ax[1].set_xlabel('Monthly MV difference (bp), 95% interval');fig.tight_layout();fig.savefig(OUT/'robustness.pdf');fig.savefig(OUT/'robustness.png',dpi=180);plt.close(fig)
l=pd.DataFrame(json.loads((ROOT/'results/historical/learning.json').read_text())['records']);fig,ax=plt.subplots(1,2,figsize=(7,2.2))
for method,c in [('target','#222222'),('raw','#bc5b46'),('joint','#177e89')]:
    g=l[l.method==method].groupby('steps')
    for a,col in zip(ax,['reward_learning_gap','target_gap']):
        a.plot(g[col].mean().index,np.maximum(g[col].mean(),1e-12),'.-',label=method,color=c);a.fill_between(g[col].mean().index,np.maximum(g[col].min(),1e-12),np.maximum(g[col].max(),1e-12),color=c,alpha=.2);a.set_xscale('log');a.set_yscale('log');a.set_xlabel('Gradient steps')
ax[0].set_ylabel('Own-reward gap');ax[1].set_ylabel('Target MV gap');ax[1].axhline(s.loc['raw','target_gap'],c='#bc5b46',ls=':',label='exact raw design gap');ax[1].legend(fontsize=6);fig.tight_layout();fig.savefig(OUT/'learning.pdf');fig.savefig(OUT/'learning.png',dpi=180)
# Compact machine-produced paper table, with unrounded JSON retained separately.
rows=[]
for k,label in [('target','Target'),('raw','Raw second moment'),('scalar','Unconstrained scalar'),('penalty_only','Risk-only calibration'),('joint','Joint calibration'),('mvpi','MVPI adaptation'),('log_variance','Log minus variance'),('log','Log utility'),('equal','Equal weight'),('minvar','Minimum variance')]:
    q=s.loc[k];rows.append(f"{label} & {q.distance:.5f} & {max(q.target_gap,0)*1e4:.4f} & {q.sharpe:.3f} & {q.mv_month*1e4:.3f} \\\\")
(OUT.parent/'results_table.tex').write_text(r'\begin{tabular}{lrrrr}\toprule'+'\n'+r'Method & Mean allocation distance & Fitted MV gap (bp) & Excess Sharpe & Realised MV (bp)\\\midrule'+'\n'+'\n'.join(rows)+'\n'+r'\bottomrule\end{tabular}'+'\n')
print(l[l.steps==5000].groupby('method')[['reward_learning_gap','target_gap','policy_distance']].mean().to_string())
# Single-column theorem figure: readable at the actual ACM column width.
evidence=json.loads((ROOT/'results/experiments.json').read_text())
fig,ax=plt.subplots(figsize=(3.35,2.25))
for T,c in zip([2,4,10,16],['#bc5b46','#ba9a34','#177e89','#7c6fa1']):
    a=sorted([q for q in evidence['scaling'] if q['T']==T and q['e']>0],key=lambda q:q['e'])
    ax.loglog([q['e'] for q in a],[q['distance'] for q in a],'o-',ms=3,label=f'T={T}',c=c)
    ax.loglog([q['e'] for q in a],[q['prediction'] for q in a],'--',lw=1,c=c)
ax.set_xlabel('Interest increment |s − 1|');ax.set_ylabel('Minimum policy discrepancy');ax.legend(fontsize=7,ncol=2);fig.tight_layout();fig.savefig(OUT/'theory.pdf');fig.savefig(OUT/'theory.png',dpi=180)
