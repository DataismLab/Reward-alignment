"""Reconstruct final saved policies and generate manuscript numbers and figure."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, ScalarFormatter, NullLocator
from mvrl.dependent import demo_market, RegimePolicy, equilibrium, distance, evaluate
from mvrl.equilibrium_audit import exact_audit

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results/rl-extension'
PAPER = ROOT / 'submissions/iafm'


def main():
    neural = pd.read_csv(OUT / 'neural-final/runs.csv')
    ppo = pd.read_csv(OUT / 'ppo-final/runs.csv')
    assert len(neural) == 1620 and len(ppo) == 40
    error = 0.; violations = 0
    for frame, kind in [(neural, 'neural'), (ppo, 'ppo')]:
        for row in frame.itertuples():
            T = int(row.horizon) if kind == 'neural' else 12
            m = demo_market(row.persistence, T); eq, _ = equilibrium(m, 1.)
            if kind == 'neural':
                key = f'p{row.persistence}_T{T}_seed{row.seed}_{row.method}'
                with np.load(OUT/'neural-final'/(key+'.npz')) as saved:
                    u, c = saved[f'u{row.step}'], saved[f'c{row.step}']
                bounds = None
            else:
                key = f'p{row.persistence}_seed{row.seed}_{row.method}'
                with np.load(OUT/'ppo-final'/(key+'.npz')) as saved:
                    u, c = saved['u'], saved['c']
                bounds = (-3, 3)
                assert np.max(np.abs(eq.beta)) < 3
            au = exact_audit(m, u, c, 1., action_bounds=bounds)
            pol = RegimePolicy(np.zeros_like(u), u)
            actual = dict(D=distance(m, pol, eq), max_deviation=au['exploitability'].max(),
                          certificate=au['bound'].max(), **evaluate(m, pol, 1.))
            error = max(error, *(abs(val-getattr(row, key)) for key, val in actual.items()))
            violations += int(np.any(au['exploitability'] > au['bound']+1e-12))
    assert error < 1e-10 and violations == 0
    final = neural[neural.step == 3000]
    metrics = ['D', 'max_deviation', 'certificate', 'J']
    nm = final.groupby('method')[metrics].mean()
    pm = ppo.groupby('method')[metrics].mean()
    comparisons = []
    rng = np.random.default_rng(1009)
    for name, frame, intervention, baselines in [
            ('neural', final, 'paired_centered', ['myopic', 'paired_mean']),
            ('ppo', ppo, 'continuation', ['myopic'])]:
        seed_means = frame.groupby(['seed', 'method'])[metrics].mean()
        for baseline in baselines:
            for metric in metrics:
                a = seed_means.xs(intervention, level='method')[metric].to_numpy()
                b = seed_means.xs(baseline, level='method')[metric].to_numpy()
                diff = a-b
                boot = diff[rng.integers(len(diff), size=(10000, len(diff)))].mean(1)
                comparisons.append(dict(experiment=name, baseline=baseline, metric=metric,
                    difference=float(diff.mean()), ci95=np.quantile(boot, [.025, .975]).tolist(),
                    seeds=len(diff)))
    summary = dict(neural_means=nm.to_dict('index'), ppo_means=pm.to_dict('index'),
        comparisons=comparisons, reconstruction=dict(neural_records=len(neural), ppo_records=len(ppo),
        max_error=error, certificate_violations=violations))
    (OUT/'final_summary.json').write_text(json.dumps(summary, indent=2))
    def reduction(frame, a, b, col): return 100*(1-frame.loc[a, col]/frame.loc[b, col])
    macros = dict(NSeeds='20', MyopicD=f'{nm.loc["myopic","D"]:.6f}',
        OrdinaryD=f'{nm.loc["paired_mean","D"]:.6f}', CentredD=f'{nm.loc["paired_centered","D"]:.6f}',
        MyopicE=f'{nm.loc["myopic","max_deviation"]:.6f}', OrdinaryE=f'{nm.loc["paired_mean","max_deviation"]:.6f}',
        CentredE=f'{nm.loc["paired_centered","max_deviation"]:.6f}',
        DistanceReduction=f'{reduction(nm,"paired_centered","myopic","D"):.1f}',
        DeviationReduction=f'{reduction(nm,"paired_centered","myopic","max_deviation"):.1f}',
        CentreReduction=f'{reduction(nm,"paired_centered","paired_mean","D"):.2f}')
    pc = [c for c in comparisons if c['experiment']=='ppo' and c['metric']=='D'][0]
    macros['PpoText'] = (f'With PPO, the continuation correction reduces mean distance by '
        f'{reduction(pm,"continuation","myopic","D"):.1f}\\% and maximum deviation gain by '
        f'{reduction(pm,"continuation","myopic","max_deviation"):.1f}\\%. '
        f'The paired distance difference is {pc["difference"]:.3f} '
        f'(95\\% seed-bootstrap interval [{pc["ci95"][0]:.3f}, {pc["ci95"][1]:.3f}]).')
    (PAPER/'rl_numbers.tex').write_text('% Generated from all final saved policies.\n'+
        '\n'.join('\\newcommand{\\'+key+'}{'+value+'}' for key,value in macros.items())+'\n')
    rows = [r'\begin{tabular}{lrrr}', r'\toprule',
        r'Method & $D$ & $\mathcal E$ & Bound \\', r'\midrule',
        r'\multicolumn{4}{l}{A. Shared neural actor--critic} \\']
    for key, label in [('myopic','Myopic reward'), ('paired_mean','Continuation, ordinary'),
                       ('paired_centered','Continuation, centred (ours)')]:
        values = [label, f'{nm.loc[key,"D"]:.4f}', *(f'{nm.loc[key,col]:.5f}' for col in metrics[1:3])]
        if key=='paired_centered':values=[r'\textbf{'+v+'}' for v in values]
        rows.append(' & '.join(values)+r' \\')
    rows += [r'\midrule',r'\multicolumn{4}{l}{B. Clipped PPO; separate matched comparison} \\']
    for key,label in [('myopic','PPO, myopic'), ('continuation','PPO, continuation (ours)')]:
        values=[label,f'{pm.loc[key,"D"]:.4f}',*(f'{pm.loc[key,col]:.5f}' for col in metrics[1:3])]
        if key=='continuation':values=[r'\textbf{'+v+'}' for v in values]
        rows.append(' & '.join(values)+r' \\')
    rows += [r'\bottomrule',r'\end{tabular}']
    (PAPER/'rl_table.tex').write_text('\n'.join(rows)+'\n')
    plt.rcParams.update({'font.size':10, 'axes.spines.top':False,'axes.spines.right':False})
    fig, axes = plt.subplots(1,3,figsize=(10.8,3.05))
    labels={'myopic':'Myopic reward','paired_mean':'Continuation: ordinary','paired_centered':'Continuation: centred'}
    colors={'myopic':'#b35806','paired_mean':'#777777','paired_centered':'#2166ac'}
    for ax,metric,title in zip(axes,metrics[:3],['Policy distance','Maximum deviation gain','Model-based certificate']):
        for method in labels:
            seed = neural[neural.method==method].groupby(['step','seed'])[metric].mean()
            means=seed.groupby('step').mean();se=seed.groupby('step').std()/np.sqrt(20)
            ax.plot(means.index,means,'o-',label=labels[method],color=colors[method],markersize=4)
            ax.fill_between(means.index,np.maximum(1e-8,means-1.96*se),means+1.96*se,
                            alpha=.14,color=colors[method])
        ax.set(xscale='log',yscale='log',xlabel='Training updates',title=title)
        ax.xaxis.set_major_locator(FixedLocator([250,1000,3000]))
        ax.xaxis.set_major_formatter(ScalarFormatter());ax.xaxis.set_minor_locator(NullLocator())
    axes[-1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(PAPER/'figures/rl_learning.pdf',metadata={'CreationDate':None})
    fig.savefig(OUT/'figures/neural_final.png',dpi=200)
    plt.close(fig)
    audit=pd.read_json(OUT/'independent_audit.json').sort_values('seed')
    refined=pd.read_json(OUT/'certificate_refinement.json')
    refined=refined[(refined.interval=='bernstein')&refined.mixing].sort_values('seed')
    fig,ax=plt.subplots(figsize=(3.5,2.65))
    for values,label,color,marker in [
        (audit.model_bound,'Exact-model certificate','#2166ac','o'),
        (audit.data_bound,'Independent data: Hoeffding','#b35806','^'),
        (refined.bound,'Independent data: Bernstein + mixing','#1b9e77','s')]:
        ax.scatter(audit.true_max,values,s=17,color=color,marker=marker,label=label,alpha=.85)
    ax.plot([.0003,.003],[.0003,.003],':',color='#666666',lw=1,label='Equality')
    ax.set(xscale='log',yscale='log',xlabel='True maximum deviation gain',ylabel='Upper bound',
           xlim=(.0003,.0025),ylim=(.0003,.07))
    ax.xaxis.set_major_locator(FixedLocator([.0005,.001,.002]))
    ax.xaxis.set_major_formatter(ScalarFormatter())
    ax.xaxis.set_minor_locator(NullLocator())
    ax.set_xticklabels(['0.0005','0.001','0.002'])
    ax.legend(fontsize=6.4,loc='lower left',bbox_to_anchor=(0,1.01),borderaxespad=0,frameon=False)
    ax.tick_params(labelsize=8)
    fig.tight_layout(pad=.6)
    fig.savefig(PAPER/'figures/audit_bounds.pdf',metadata={'CreationDate':None})
    fig.savefig(OUT/'figures/audit_bounds.png',dpi=200)
    plt.close(fig)
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
