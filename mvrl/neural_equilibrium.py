"""Shared neural actor/continuation critic pilot using frozen conditional samples.

Known financial dynamics, sampled conditional market outcomes. Not a generic
black-box environment algorithm, and no oracle target enters this module.
"""
import numpy as np


def train(returns,next_states,phi,riskless,seed=0,method='paired_centered',
          checkpoints=(250,1000,3000),batch_size=64):
    import torch
    from torch import nn
    torch.set_num_threads(1)
    torch.manual_seed(seed)
    rng=np.random.default_rng(seed+7919)
    r=np.asarray(returns,float);j=np.asarray(next_states)
    if r.ndim!=3 or r.shape!=j.shape or r.shape[2]<4 or r.shape[2]%2:
        raise ValueError('conditional samples (T,K,N), even N>=4')
    if method not in ('paired_centered','paired_mean','myopic'):
        raise ValueError('unknown method')
    if phi<=0 or riskless<=0 or batch_size<2 or batch_size%2:
        raise ValueError('invalid preference or batch')
    if not checkpoints or min(checkpoints)<1:raise ValueError('positive checkpoints')
    T,K,N=r.shape
    if not np.issubdtype(j.dtype,np.integer) or np.any(j<0) or np.any(j>=K) or not np.isfinite(r).all():
        raise ValueError('invalid samples')
    features=np.array([[t/T,*np.eye(K)[z]] for t in range(T+1) for z in range(K)])
    x=torch.tensor(features,dtype=torch.float32)
    def network():
        return nn.Sequential(nn.Linear(K+1,32),nn.Tanh(),nn.Linear(32,32),nn.Tanh(),nn.Linear(32,1))
    actor,critic=network(),network()
    target=network();target.load_state_dict(critic.state_dict())
    ao=torch.optim.Adam(actor.parameters(),lr=.003)
    co=torch.optim.Adam(critic.parameters(),lr=.003)
    H=torch.tensor(riskless**np.arange(T-1,-1,-1),dtype=torch.float32)[:,None]
    # Data-only normalisation, frozen identically for all algorithms.
    v=np.mean((r[:,:,::2]-r[:,:,1::2])**2,axis=2)/2
    if np.any(v<=1e-14):raise ValueError('degenerate conditional sample variance')
    curvature=2*phi*H**2*torch.tensor(v,dtype=torch.float32)
    time=torch.arange(T)[:,None,None]
    def values(net):
        raw=net(x).reshape(T+1,K)
        out=torch.cat((raw[:-1],torch.zeros_like(raw[-1:])),dim=0)
        return out-out.mean(1,keepdim=True) if method=='paired_centered' else out
    records=[]
    for step in range(1,max(checkpoints)+1):
        idx=rng.integers(N,size=(T,K,batch_size))
        rb=torch.tensor(np.take_along_axis(r,idx,axis=2),dtype=torch.float32)
        jb=torch.tensor(np.take_along_axis(j,idx,axis=2),dtype=torch.long)
        with torch.no_grad():
            future=values(target)[time+1,jb]
            u_fixed=actor(x[:T*K]).reshape(T,K)
            td=(H[:,:,None]*rb*u_fixed[:,:,None]+future).mean(2)
            if method=='paired_centered':td=td-td.mean(1,keepdim=True)
        prediction=values(critic)[:T]
        critic_loss=((prediction-td)**2).mean()
        co.zero_grad();critic_loss.backward();co.step()
        with torch.no_grad():
            cnext=values(critic)[time+1,jb]
            dc=cnext[:,:,::2]-cnext[:,:,1::2]
            if method=='myopic':dc=torch.zeros_like(dc)
        u=actor(x[:T*K]).reshape(T,K)
        dr=rb[:,:,::2]-rb[:,:,1::2]
        linear=H*rb.mean(2)-phi*H*(dr*dc).mean(2)
        quad=phi*H**2*(dr**2).mean(2)/2
        actor_loss=-((linear*u-quad*u*u)/curvature).mean()
        ao.zero_grad();actor_loss.backward();ao.step()
        with torch.no_grad():
            for tp,cp in zip(target.parameters(),critic.parameters()):
                tp.mul_(.98).add_(cp,alpha=.02)
        if step in checkpoints:
            with torch.no_grad():
                records.append(dict(step=step,actions=actor(x[:T*K]).reshape(T,K).numpy().copy(),
                    critic=values(critic).numpy().copy(),critic_loss=float(critic_loss.detach()),
                    actor_loss=float(actor_loss.detach())))
    return records
