"""QuEST nonlinear covariance shrinkage for the 2017 portfolio estimator.

The forward map/Jacobian are a pinned port of Ledoit--Wolf QuEST v027.
The fit uses the authors' trace constraint, eigenvalue bounds and linear
initialization, with normalized variables and SciPy SLSQP instead of fmincon.
"""
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.optimize import minimize
from ._vendor.quest.core import quest
from ._vendor.quest.mse import quest_mse, quest_dmse


def nonlinear_covariance(history, cache_dir=None):
    x = np.asarray(history, dtype=float)
    if x.ndim != 2 or not np.isfinite(x).all() or len(x) < 3:
        raise ValueError('finite history with at least three observations required')
    t, p = x.shape
    if p >= t-1:
        raise ValueError('this fitting wrapper requires assets < effective observations')
    paths = [Path(__file__), *sorted((Path(__file__).parent/'_vendor/quest').glob('*.py'))]
    digest = hashlib.sha256(b''.join(f.read_bytes() for f in paths))
    digest.update(np.asarray(x.shape, dtype=np.int64).tobytes())
    digest.update(np.ascontiguousarray(x).tobytes())
    key = digest.hexdigest()
    dest = Path(cache_dir)/f'{key}.json' if cache_dir else None
    if dest is not None and dest.exists():
        saved = json.loads(dest.read_text())
        return np.array(saved['covariance']), saved['info']
    z = x-x.mean(0)
    n = t-1
    sample = z.T@z/n
    lam, u = np.linalg.eigh(sample)
    if lam[0] <= 0:
        raise ValueError('positive sample eigenvalues required by this wrapper')
    scale = lam.mean()
    target = lam/scale
    fourth = np.sum((z*z).T@(z*z)/n-2*(z.T@z)*sample/n+sample**2)
    gamma = np.sum((sample-scale*np.eye(p))**2)
    alpha = float(np.clip(fourth/(gamma*n), 0, 1)) if gamma > 0 else 1.
    start = 1+np.sqrt(1-alpha)*(target-1)
    args = (target, n, 1., 100.)
    constraint = {'type': 'eq', 'fun': lambda a: a.mean()-1,
                  'jac': lambda a: np.ones(p)/p}
    settings = dict(args=args, jac=quest_dmse, method='SLSQP',
                    bounds=[(target[0], target[-1])]*p, constraints=[constraint])
    result = minimize(quest_mse, start, **settings,
                      options={'ftol': 1e-9, 'maxiter': 250})
    retried = not result.success
    if retried:
        result = minimize(quest_mse, result.x, **settings,
                          options={'ftol': 1e-9, 'maxiter': 1000})
    if not result.success or abs(result.x.mean()-1) > 1e-8:
        raise RuntimeError(f'QuEST fit failed: {result.message}')
    fitted, delta, _ = quest(np.sort(result.x), n)
    v = (u*(delta*scale))@u.T
    v = (v+v.T)/2
    if not np.isfinite(v).all() or np.linalg.eigvalsh(v).min() <= 0:
        raise RuntimeError('QuEST returned a nonpositive covariance')
    info = dict(quest_success=True, quest_iterations=int(result.nit),
                quest_retried=retried, effective_observations=n,
                quest_normalized_mse=float(np.mean((fitted-target)**2)),
                quest_initial_mse=float(quest_mse(start, *args)/100),
                quest_population_eigenvalues=(np.sort(result.x)*scale).tolist(),
                quest_sample_eigenvalues=lam.tolist(),
                quest_shrunk_eigenvalues=(delta*scale).tolist(),
                quest_cache_key=key)
    if dest is not None:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(dict(covariance=v.tolist(), info=info)))
    return v, info
