"""Finite-budget softmax policy optimisation on lagged historical states.
This is a contextual direct-gradient diagnostic, NOT a full RL reproduction.
Each state has independent logits; no cross-state generalisation is asserted.
"""
import json
import numpy as np
from .historical import ROOT,data,moments

def run(steps=(50,250,1000,5000),seeds=range(5)):
    import torch
    torch.set_num_threads(1);torch.set_default_dtype(torch.float64)
    frame=data();asset=frame.iloc[:,:-1].to_numpy();rf=frame.RF.to_numpy()
    records=json.loads((ROOT/'results/historical/primary.json').read_text())
    by={(r['date'],r['method']):r for r in records}
    ms=[];vs=[];ps=[];targets=[];raw=[];joint=[];dates=[]
    prev=np.ones(10)/10
    for t,date in enumerate(frame.index):
        if date<199001:continue
        m,v=moments(asset[t-120:t]-rf[t-120:t,None]);ms.append(m);vs.append(v);ps.append(prev.copy());dates.append(int(date))
        for name,dest in [('target',targets),('raw',raw),('joint',joint)]:dest.append(by[(date,name)]['audit_weights'])
        w=np.array(by[(date,'target')]['weights']);prev=w*(1+asset[t])/(1+w@asset[t])
    m,v,p,tgt=map(torch.tensor,[np.array(ms),np.array(vs),np.array(ps),np.array(targets)])
    M=v+m[:,:,None]*m[:,None,:];A=1+10*(m*tgt).sum(1);out=[]
    def score(w,H,k):return (m*w).sum(1)-torch.einsum('bi,bij,bj->b',w,H,w)-k*(w-p).abs().sum(1)
    fstar=score(tgt,5*v,.001)
    for seed in seeds:
        for method,exact,H,k in [('target',targets,5*v,.001),('raw',raw,5*M,.001),('joint',joint,5*M/A[:,None,None],.001/A)]:
            torch.manual_seed(seed);logits=torch.nn.Parameter(.1*torch.randn(m.shape));opt=torch.optim.Adam([logits],lr=.05)
            exact=torch.tensor(np.array(exact));qstar=score(exact,H,k);design=fstar-score(exact,5*v,.001)
            for step in range(1,max(steps)+1):
                opt.zero_grad();w=logits.softmax(1);loss=-1000*score(w,H,k).mean();loss.backward();opt.step()
                if step in steps:
                    with torch.no_grad():
                        w=logits.softmax(1);total=fstar-score(w,5*v,.001);transfer=score(exact,5*v,.001)-score(w,5*v,.001)
                        if not torch.allclose(total,design+transfer,atol=1e-14):raise AssertionError('decomposition')
                        out.append(dict(seed=seed,method=method,steps=step,reward_learning_gap=float((qstar-score(w,H,k)).mean()),target_gap=float(total.mean()),design_gap=float(design.mean()),signed_learning_difference=float(transfer.mean()),policy_distance=float(torch.linalg.vector_norm(w-tgt,dim=1).mean()),own_policy_distance=float(torch.linalg.vector_norm(w-exact,dim=1).mean())))
            print(seed,method,flush=True)
    dest=ROOT/'results/historical/learning.json';dest.write_text(json.dumps(dict(protocol='Independent softmax logits on 432 past-only fitted states; Adam lr .05; five seeds; no architecture reproduction or cross-state generalisation.',records=out),indent=2))
    return out
if __name__=='__main__':run()
