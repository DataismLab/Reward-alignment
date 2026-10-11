"""One-step equilibrium audits for wealth-independent finite-regime policies.

Exact-model functions are EVALUATION ONLY. The independent-sample certificate
does not access a market object. See the accompanying paper.
"""
import numpy as np


def _validate(actions, critic, phi, riskless):
    u, c = np.asarray(actions, float), np.asarray(critic, float)
    if u.ndim != 2 or c.shape != (u.shape[0] + 1, u.shape[1]):
        raise ValueError('actions (T,K), critic (T+1,K) required')
    if not (np.isfinite(u).all() and np.isfinite(c).all()):
        raise ValueError('finite policy and critic required')
    if phi <= 0 or riskless <= 0:
        raise ValueError('positive phi and riskless required')
    return u, c


def continuation(market, actions):
    u = np.asarray(actions, float)
    if u.shape != (market.horizon, market.regimes):
        raise ValueError('policy shape')
    a = np.zeros((market.horizon + 1, market.regimes))
    for t in range(market.horizon - 1, -1, -1):
        H = market.riskless ** (market.horizon - t - 1)
        for z in range(market.regimes):
            p, j, r = market.branches(z)
            a[t, z] = p @ (H * r * u[t, z] + a[t + 1, j])
    return a


def exact_audit(market, actions, critic, phi, reward_gradient=None, action_bounds=None):
    """True-model certificate and exact deviations, not an observable data bound."""
    u, c = _validate(actions, critic, phi, market.riskless)
    T, K = u.shape
    a = continuation(market, u)
    residual = np.zeros_like(u)
    grad = np.zeros_like(u)
    true_grad = np.zeros_like(u)
    scale = np.zeros_like(u)
    curvature = np.zeros_like(u)
    for t in range(T):
        H = market.riskless ** (T - t - 1)
        for z in range(K):
            p, j, r = market.branches(z)
            m = p @ r
            v = p @ ((r - m) ** 2)
            if v <= 0:
                raise ValueError('positive conditional variance required')
            residual[t, z] = c[t, z] - p @ (H * r * u[t, z] + c[t + 1, j])
            grad[t, z] = H*m - 2*phi*H*(p @ ((r-m)*c[t+1,j])) - 2*phi*H*H*v*u[t,z]
            true_grad[t,z] = H*m - 2*phi*H*(p @ ((r-m)*a[t+1,j])) - 2*phi*H*H*v*u[t,z]
            scale[t,z] = 2*np.sqrt(phi)*H*np.sqrt(v)
            curvature[t,z] = phi*H*H*v
    rho = .5 * np.max(np.abs(market.transition[:,None,:] - market.transition[None,:,:]).sum(-1))
    spans = np.zeros(T+1)
    spans[T] = np.ptp(c[T])
    uniform = np.zeros(T+1)
    uniform[T] = np.max(np.abs(c[T]))
    for t in range(T-1,-1,-1):
        spans[t] = np.ptp(residual[t]) + rho*spans[t+1]
        uniform[t] = np.max(np.abs(residual[t])) + uniform[t+1]
    h = grad if reward_gradient is None else np.asarray(reward_gradient, float)
    if h.shape != u.shape or not np.isfinite(h).all():
        raise ValueError('reward gradient shape or values')
    actor = np.abs(h)/scale
    reward = np.abs(grad-h)/scale
    true_gap=(true_grad/scale)**2
    if action_bounds is not None:
        lower,upper=action_bounds
        if not np.isfinite([lower,upper]).all() or lower>=upper or np.any(u<lower) or np.any(u>upper):
            raise ValueError('feasible actions and ordered finite bounds required')
        if reward_gradient is not None:
            raise ValueError('bounded reward-gradient split not implemented')
        def gain(g):
            delta=np.clip(u+g/(2*curvature),lower,upper)-u
            return np.maximum(0.,g*delta-curvature*delta**2)
        actor=np.sqrt(gain(grad));true_gap=gain(true_grad)
    critic_term = np.broadcast_to(np.sqrt(phi)*spans[1:,None]/2, u.shape).copy()
    return dict(exploitability=true_gap,
                bound=(actor+reward+critic_term)**2,
                uniform_bound=(actor+reward+np.sqrt(phi)*uniform[1:,None])**2,
                actor=actor, reward=reward, critic=critic_term,
                gradient=grad, true_gradient=true_grad, residual=residual,
                critic_span_bound=spans, true_critic_error=c-a, rho=float(rho))


def independent_sample_certificate(actions, critic, returns, next_states,
                                   phi, riskless, return_bound, alpha=.05,
                                   interval='hoeffding', estimate_mixing=False):
    """Hoeffding certificate, conditional on policy/critic fixed before audit.

    returns/next_states have shape (T,K,N), N even >=4, independent conditional
    observations in each cell. Known absolute support return_bound is required.
    Never reuse these data for fitting or checkpoint selection. Independence
    cannot be inferred from numeric arrays; the caller must enforce it.
    """
    u,c = _validate(actions, critic, phi, riskless)
    r,j = np.asarray(returns,float), np.asarray(next_states)
    T,K = u.shape
    if r.ndim != 3 or r.shape[:2] != (T,K) or j.shape != r.shape:
        raise ValueError('audit data shape')
    N = r.shape[2]
    if N < 4 or N % 2 or not (0 < alpha < 1) or return_bound <= 0:
        raise ValueError('even N>=4, positive support, alpha in (0,1) required')
    if not np.isfinite(r).all() or np.max(np.abs(r)) > return_bound + 1e-14:
        raise ValueError('observed returns outside known support')
    if not np.issubdtype(j.dtype,np.integer) or np.any(j<0) or np.any(j>=K):
        raise ValueError('next-state indices')
    if interval not in ('hoeffding','bernstein'):raise ValueError('interval method')
    claims=3*T*K+(T*K*K if estimate_mixing else 0)
    q=alpha/claims
    def radius(samples,width):
        count=len(samples)
        if interval=='hoeffding':
            return width*np.sqrt(np.log(2/q)/(2*count))
        # Maurer–Pontil (COLT 2009), Theorem 4, applied to both tails.
        log=np.log(4/q)
        return np.sqrt(2*np.var(samples,ddof=1)*log/count)+7*width*log/(3*(count-1))
    rho_upper=np.ones(T)
    if estimate_mixing:
        eps=np.sqrt(np.log(2/q)/(2*N))
        for t in range(T):
            phat=np.array([np.bincount(j[t,z],minlength=K)/N for z in range(K)])
            rh=.5*np.max(np.abs(phat[:,None,:]-phat[None,:,:]).sum(-1))
            rho_upper[t]=min(1.,rh+K*eps)
    lo,hi,g_upper,v_lower = (np.zeros_like(u) for _ in range(4))
    for t in range(T):
        H = riskless**(T-t-1)
        Cspan = np.ptp(c[t+1])
        for z in range(K):
            x = r[t,z]; cn = c[t+1,j[t,z]]
            dr = x[::2]-x[1::2]; dc = cn[::2]-cn[1::2]
            gs=H*(x[::2]+x[1::2])/2 - phi*H*dr*(H*dr*u[t,z]+dc)
            ghat = np.mean(gs)
            M = H*return_bound + 2*phi*H*return_bound*Cspan + 4*phi*H*H*return_bound**2*abs(u[t,z])
            g_upper[t,z] = abs(ghat)+radius(gs,2*M)
            vs=dr**2/2
            v_lower[t,z] = np.mean(vs)-radius(vs,2*return_bound**2)
            targets=H*x*u[t,z]+cn
            ehat = c[t,z]-np.mean(targets)
            rad = radius(targets,2*H*return_bound*abs(u[t,z])+Cspan)
            lo[t,z],hi[t,z] = ehat-rad,ehat+rad
    span = np.zeros(T+1);span[T] = np.ptp(c[T])
    for t in range(T-1,-1,-1):
        span[t] = max(0.,hi[t].max()-lo[t].min())+rho_upper[t]*span[t+1]
    bounds = np.full_like(u,np.inf)
    for t in range(T):
        H = riskless**(T-t-1)
        good = v_lower[t]>0
        bounds[t,good] = (g_upper[t,good]/(2*np.sqrt(phi)*H*np.sqrt(v_lower[t,good]))+np.sqrt(phi)*span[t+1]/2)**2
    return dict(bound=bounds,variance_lower=v_lower,gradient_upper=g_upper,
                residual_lower=lo,residual_upper=hi,critic_span_bound=span,
                alpha=float(alpha),audit_observations=int(r.size),rho_upper=rho_upper,
                interval=interval,estimate_mixing=estimate_mixing)
