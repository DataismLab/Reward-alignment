"""Reconstruct policy outputs, summarise paired seeds and produce research figures."""
from pathlib import Path
import hashlib,json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator,ScalarFormatter,NullLocator
from mvrl.dependent import demo_market,RegimePolicy,equilibrium,distance,evaluate,local_calibration
from mvrl.equilibrium_audit import exact_audit,continuation


def main():
    dest=Path('results/rl-extension');figdir=dest/'figures';figdir.mkdir(exist_ok=True)
    df=pd.read_csv(dest/'tabular_runs.csv');policies=np.load(dest/'tabular_policies.npz')
    controls=[]
    for persistence in (.5,.8,.95):
        for T in (4,12,24):
            market=demo_market(persistence,T);eq,_=equilibrium(market,1.)
            for method,u in [('zero',np.zeros_like(eq.beta)),('exact_equilibrium',eq.beta),
                             ('exact_myopic',local_calibration(market,1.).beta)]:
                critic=continuation(market,u);au=exact_audit(market,u,critic,1.)
                pol=RegimePolicy(np.zeros_like(u),u)
                controls.append(dict(persistence=persistence,horizon=T,method=method,
                    D=distance(market,pol,eq),max_deviation=au['exploitability'].max(),**evaluate(market,pol,1.)))
    pd.DataFrame(controls).to_csv(dest/'exact_controls.csv',index=False)
    residual=0.;bound_violations=0
    for row in df.itertuples():
        m=demo_market(row.persistence,int(row.horizon));eq,_=equilibrium(m,1.)
        key=f'p{row.persistence}_T{row.horizon}_n{row.n}_seed{row.seed}_{row.method}'
        u,c=policies[key+'_u'],policies[key+'_c'];pol=RegimePolicy(np.zeros_like(u),u)
        au=exact_audit(m,u,c,1.)
        residual=max(residual,abs(distance(m,pol,eq)-row.D),abs(evaluate(m,pol,1.)['J']-row.J),
                     abs(au['exploitability'].max()-row.max_deviation))
        bound_violations+=int(np.any(au['exploitability']>au['bound']+1e-12))
    neural=pd.read_csv(dest/'neural/runs.csv')
    for row in neural.itertuples():
        m=demo_market(row.persistence,int(row.horizon));eq,_=equilibrium(m,1.)
        saved=np.load(dest/'neural'/f'p{row.persistence}_T{row.horizon}_seed{row.seed}_{row.method}.npz')
        u,c=saved[f'u{row.step}'],saved[f'c{row.step}'];au=exact_audit(m,u,c,1.)
        residual=max(residual,abs(au['exploitability'].max()-row.max_deviation),abs(au['bound'].max()-row.certificate))
        bound_violations+=int(np.any(au['exploitability']>au['bound']+1e-12))
    df.groupby(['persistence','horizon','n','method'])[['D','max_deviation','certificate','J']].agg(['mean','median','std']).to_csv(dest/'tabular_summary.csv')
    neural.groupby(['persistence','horizon','step','method'])[['D','max_deviation','certificate','J']].agg(['mean','median','std']).to_csv(dest/'neural_summary.csv')
    # Paired bootstrap on seed-level averages: each seed appears in every market.
    final=neural[neural.step==3000]
    seed_means=final.groupby(['seed','method'])[['D','max_deviation','certificate']].mean()
    comparisons=[];rng=np.random.default_rng(1009)
    for baseline in ('myopic','paired_mean'):
        for metric in ('D','max_deviation','certificate'):
            a=seed_means.xs('paired_centered',level='method')[metric].to_numpy()
            b=seed_means.xs(baseline,level='method')[metric].to_numpy()
            diff=a-b;boots=diff[rng.integers(len(diff),size=(10000,len(diff)))].mean(1)
            comparisons.append(dict(baseline=baseline,metric=metric,mean_difference=float(diff.mean()),
                paired_bootstrap95=np.quantile(boots,[.025,.975]).tolist(),seeds=len(diff)))
    (dest/'neural_paired_comparisons.json').write_text(json.dumps(comparisons,indent=2))
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,axes=plt.subplots(1,3,figsize=(11,3.4),sharey=True)
    for ax,T in zip(axes,(4,12,24)):
        for method,label,color in [('myopic','Myopic reward','#b35806'),('paired_actor','Learned continuation','#2166ac')]:
            sub=df[(df.persistence==.8)&(df.horizon==T)&(df.method==method)]
            g=sub.groupby('n').D
            means=g.mean();se=g.std()/np.sqrt(20)
            ax.plot(means.index,means,'o-',color=color,label=label)
            ax.fill_between(means.index,means-1.96*se,means+1.96*se,color=color,alpha=.15)
        m=demo_market(.8,T);eq,_=equilibrium(m,1.)
        ax.axhline(distance(m,local_calibration(m,1.),eq),color='#b35806',ls=':',label='Exact myopic mismatch')
        ax.set(xscale='log',yscale='log',title=f'Horizon {T}',xlabel='Samples per time/state')
    axes[0].set_ylabel('Policy distance to equilibrium');axes[2].legend(fontsize=8)
    fig.suptitle('More data reduces learning error; myopic reward mismatch persists',fontsize=12)
    fig.tight_layout();fig.savefig(figdir/'sample_learning.png',dpi=180);fig.savefig(figdir/'sample_learning.pdf');plt.close(fig)
    fig,axes=plt.subplots(1,3,figsize=(11,3.4))
    labels={'myopic':'Myopic','paired_mean':'Ordinary critic','paired_centered':'Centred critic'}
    colors={'myopic':'#b35806','paired_mean':'#777777','paired_centered':'#2166ac'}
    for ax,metric,title in zip(axes,['D','max_deviation','certificate'],['Policy distance','True deviation gain','Model-based audit bound']):
        for method in labels:
            # Average over nine fixed markets within each seed, then over seeds.
            byseed=neural[neural.method==method].groupby(['step','seed'])[metric].mean()
            mean=byseed.groupby('step').mean();se=byseed.groupby('step').std()/np.sqrt(5)
            ax.plot(mean.index,mean,'o-',label=labels[method],color=colors[method])
            ax.fill_between(mean.index,np.maximum(1e-8,mean-1.96*se),mean+1.96*se,alpha=.15,color=colors[method])
        ax.set(xscale='log',yscale='log',xlabel='Neural updates',title=title)
        ax.xaxis.set_major_locator(FixedLocator([250,1000,3000]))
        ax.xaxis.set_major_formatter(ScalarFormatter())
        ax.xaxis.set_minor_locator(NullLocator())
    axes[2].legend(fontsize=8);fig.suptitle('Shared neural actor–critic: five seeds, nine fixed markets',fontsize=12)
    fig.tight_layout();fig.savefig(figdir/'neural_learning.png',dpi=180);fig.savefig(figdir/'neural_learning.pdf');plt.close(fig)
    # Scientific integrity checks: previous work still byte-identical.
    old=json.loads(Path('notes/rl-extension/existing_work_manifest.json').read_text())
    changed=[p for p,h in old.items() if hashlib.sha256(Path(p.replace('submissions/'+'iafm', 'manuscript')).read_bytes()).hexdigest()!=h]
    unexpected=[p for p in changed if p not in {'submissions/'+'iafm/paper.tex','submissions/'+'iafm/paper.pdf'}]
    verification=dict(tabular_records=len(df),neural_records=len(neural),max_reconstruction_error=residual,
                      certificate_violations=bound_violations,changed_existing_research_files=changed,unexpected_changed_research_files=unexpected)
    (dest/'verification.json').write_text(json.dumps(verification,indent=2))
    print(json.dumps(verification,indent=2));print(json.dumps(comparisons,indent=2))
    assert residual<1e-10 and bound_violations==0 and not unexpected


if __name__=='__main__':main()
