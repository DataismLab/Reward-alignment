"""Structured sample-based backward actor/mean-critic learning.

Specialises existing SPERL principles; not a reproduction of its full algorithm.
Only collect_samples sees the simulator. Fit functions cannot access an oracle.
"""
import numpy as np


def collect_samples(market, n, seed):
    if n < 4 or n % 2:
        raise ValueError('even n>=4 required')
    rng = np.random.default_rng(seed)
    r = np.empty((market.horizon,market.regimes,n))
    j = np.empty(r.shape,dtype=int)
    for t in range(market.horizon):
        for z in range(market.regimes):
            p,nxt,ret = market.branches(z)
            indices = rng.choice(len(p),size=n,p=p)
            r[t,z],j[t,z] = ret[indices],nxt[indices]
    return r,j


def fit_backward(returns, next_states, phi, riskless, method='paired_actor',
                 actor_steps=40, step_fraction=.25, action_bounds=None):
    """Frozen-data backward updates; phi and known self-financing rate are inputs.

    paired_actor: gradient ascent on sampled paired quadratic reward.
    paired_exact: exact best response on SAME sampled paired reward, an optimisation
      control rather than a second independent RL algorithm.
    myopic: omits continuation covariance; uses same variance and sample access.
    """
    r,j = np.asarray(returns,float),np.asarray(next_states)
    if r.ndim!=3 or r.shape!=j.shape or r.shape[2]<4 or r.shape[2]%2:
        raise ValueError('data shape and even samples required')
    if phi<=0 or riskless<=0 or actor_steps<0 or not 0<step_fraction<=1:
        raise ValueError('invalid learning configuration')
    if method not in ('paired_actor','paired_exact','myopic'):
        raise ValueError('unknown method')
    if not np.isfinite(r).all() or not np.issubdtype(j.dtype,np.integer):
        raise ValueError('data values')
    T,K,_ = r.shape
    if (j<0).any() or (j>=K).any():raise ValueError('next-state indices')
    u = np.zeros((T,K));c = np.zeros((T+1,K))
    if action_bounds is not None:
        lower,upper=action_bounds
        if not np.isfinite([lower,upper]).all() or lower>=upper:raise ValueError('invalid action bounds')
        u[:]=np.clip(0.,lower,upper)
    for t in range(T-1,-1,-1):
        H = riskless**(T-t-1)
        for z in range(K):
            x = r[t,z];cn = c[t+1,j[t,z]]
            dr = x[::2]-x[1::2];dc = cn[::2]-cn[1::2]
            v = np.mean(dr**2)/2
            if v<=1e-14:
                raise ValueError('degenerate sampled variance; no silent regularisation')
            cov = 0. if method=='myopic' else np.mean(dr*dc)/2
            linear = H*np.mean(x)-2*phi*H*cov
            curvature = 2*phi*H*H*v
            if method in ('paired_exact','myopic'):
                u[t,z] = linear/curvature
                if action_bounds is not None:u[t,z]=np.clip(u[t,z],lower,upper)
            else:
                for _ in range(actor_steps):
                    u[t,z] += step_fraction*(linear-curvature*u[t,z])/curvature
                    if action_bounds is not None:u[t,z]=np.clip(u[t,z],lower,upper)
            c[t,z] = np.mean(H*x*u[t,z]+cn)
    return u,c
