"""Past-only covariance estimators, in unbiased sample-covariance units.

The two Ledoit--Wolf intensities use centred ML covariance and fourth moments;
their final estimates are multiplied by L/(L-1) to match the existing study.
Observed-factor fits include an intercept and residual degrees-of-freedom
correction. See notes/COVARIANCE_PROTOCOL.md for exact adaptation boundaries.
"""
import numpy as np

ESTIMATORS = ('sample', 'diag10', 'lw_identity', 'lw_correlation', 'market', 'ff3')


def estimate_covariance(history, estimator, factors=None):
    x = np.asarray(history, dtype=float)
    if x.ndim != 2 or len(x) < 3 or not np.isfinite(x).all():
        raise ValueError('finite two-dimensional history with >=3 rows required')
    t, n = x.shape
    z = x-x.mean(axis=0)
    s = z.T@z/t
    info = {'estimator': estimator, 'observations': t, 'assets': n}
    if estimator == 'sample':
        v = s*t/(t-1)
    elif estimator == 'diag10':
        v = (.9*s+.1*np.diag(np.diag(s)))*t/(t-1)
        info['shrinkage'] = .1
    elif estimator == 'lw_identity':
        target = np.eye(n)*np.trace(s)/n
        delta = float(np.sum((s-target)**2))
        beta = max(0., float((np.sum(np.sum(z*z, axis=1)**2)/t-np.sum(s*s))/t))
        alpha = min(1., beta/delta) if delta > 0 else 0.
        v = ((1-alpha)*s+alpha*target)*t/(t-1)
        info['shrinkage'] = alpha
    elif estimator == 'lw_correlation':
        variances = np.diag(s)
        if np.min(variances) <= 0:
            raise ValueError('constant-correlation estimator requires positive variances')
        sd = np.sqrt(variances)
        corr = s/np.outer(sd, sd)
        rbar = (corr.sum()-n)/(n*(n-1)) if n > 1 else 0.
        target = rbar*np.outer(sd, sd)
        np.fill_diagonal(target, variances)
        pi = (z*z).T@(z*z)/t-s*s
        # theta_ij = E[(z_i^2-s_ii)(z_i z_j-s_ij)].
        theta = (z**3).T@z/t-variances[:, None]*s
        np.fill_diagonal(theta, 0.)
        rho = float(np.trace(pi)+rbar*np.sum((sd[None, :]/sd[:, None])*theta))
        gamma = float(np.sum((target-s)**2))
        alpha = float(np.clip((pi.sum()-rho)/(t*gamma), 0, 1)) if gamma > 1e-30 else 1.
        v = ((1-alpha)*s+alpha*target)*t/(t-1)
        info.update(shrinkage=alpha, mean_correlation=float(rbar))
    elif estimator in ('market', 'ff3'):
        f = np.asarray(factors, dtype=float)
        k = 1 if estimator == 'market' else 3
        if f.ndim != 2 or len(f) != t or f.shape[1] < k or not np.isfinite(f).all() or t <= k+1:
            raise ValueError('aligned finite factors and residual degrees of freedom required')
        f = f[:, :k]-f[:, :k].mean(axis=0)
        beta, _, rank, _ = np.linalg.lstsq(f, z, rcond=None)
        if rank != k:
            raise ValueError('rank-deficient factor history')
        residual = z-f@beta
        residual_var = np.sum(residual**2, axis=0)/(t-k-1)
        v = beta.T@(f.T@f/(t-1))@beta+np.diag(residual_var)
        info.update(factors=k, residual_dof=t-k-1,
                    min_residual_variance=float(residual_var.min()))
    else:
        raise ValueError(f'unknown covariance estimator {estimator}')
    v = (v+v.T)/2
    eig = np.linalg.eigvalsh(v)
    if eig.min() < -1e-12 or not np.isfinite(v).all():
        raise ValueError('invalid covariance estimate')
    info.update(min_eigenvalue=float(eig.min()), max_eigenvalue=float(eig.max()),
                condition=float(eig.max()/eig.min()) if eig.min() > 1e-15 else None)
    return x.mean(axis=0), v, info


def calibration_bounds(m, v, phi, target, candidate, anchor, certificate=0.):
    """A certificate for an approximate anchor and approximate reward optimum."""
    A = 1+2*phi*anchor
    if A <= 0 or certificate < 0:
        raise ValueError('positive scaling and nonnegative certificate required')
    upper = phi*(float(m@target)-anchor)**2+A*certificate
    smallest = float(np.linalg.eigvalsh(v).min())
    return dict(A=float(A), target_gap_upper=float(upper),
                distance_upper=float(np.sqrt(upper/(phi*smallest))) if smallest > 1e-15 else None)


def covariance_transfer_bounds(v_reference, v_alternative, alternative_target, phi):
    """Same mean/cost/state: bound target displacement caused by covariance.

    ||u_ref-u_alt|| <= ||(V_alt-V_ref)u_alt||/lambda_min(V_ref).
    F_ref(u_ref)-F_ref(u_alt) <= phi*||E u_alt||^2/lambda_min(V_ref).
    """
    smallest = float(np.linalg.eigvalsh(v_reference).min())
    if smallest <= 0:
        raise ValueError('positive definite reference required')
    norm = float(np.linalg.norm((v_alternative-v_reference)@alternative_target))
    return dict(distance_upper=norm/smallest, target_gap_upper=phi*norm**2/smallest)
