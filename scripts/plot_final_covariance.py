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

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
fig,axes=plt.subplots(1,2,figsize=(9.8,3.1))
x=np.arange(6)
for offset,key,label,color in [(-.23,'cross','Covariance-model change','#555555'),(0,'raw','Raw reward discrepancy','#cf7c22'),(.23,'joint','Joint discrepancy','#197a68')]:
    vals=[cases[49,e]['cross_target_distance'] if key=='cross' else summary(49,e,key)['distance'] for e in order]
    axes[0].bar(x+offset,np.maximum(vals,1e-9),.22,label=label,color=color)
axes[0].set_yscale('log');axes[0].set_ylim(1e-9,1);axes[0].set_xticks(x,['Sample','Fixed\ndiagonal','LW\nidentity','LW\ncorr.','Market','Three\nfactors']);axes[0].set_ylabel('Mean allocation distance');axes[0].set_title('(a) What changes the 49-industry allocation?')
comps={r['estimator']:r for r in report['estimator_comparisons'] if r['n_assets']==49};es=[e for e in order if e!='diag10']
for i,e in enumerate(es):
    r=comps[e];v=r['delta']*1e4;lo,hi=np.array(r['ci95'])*1e4
    axes[1].plot([lo,hi],[i,i],color='#197a68',linewidth=2);axes[1].plot(v,i,'o',color='#197a68',markersize=5)
axes[1].axvline(0,color='.6',ls='--',lw=1);axes[1].set_yticks(range(5),[names[e] for e in es]);axes[1].invert_yaxis();axes[1].set_xlabel('Monthly realised MV difference (bp)\nPaired 95% path intervals');axes[1].set_title('(b) Target versus fixed diagonal, N=49')
handles,labels=axes[0].get_legend_handles_labels()
fig.legend(handles,labels,loc='upper center',ncol=3,fontsize=8,frameon=False)
fig.tight_layout(rect=(0,0,1,.89))
fig.savefig(w/'figures/covariance.pdf',metadata={'CreationDate':None});fig.savefig(w/'figures/covariance.png',dpi=180);plt.close(fig)
