"""Objective and gradient for fitting population eigenvalues to sample eigenvalues.

Port of QuEST_v027/QuESTmse.m and QuESTdmse.m: a quadratic-penalty objective
in sample-eigenvalue space, used by QuESTimate.m to search for the
population eigenvalues (`tau`) whose QuEST-implied sample eigenvalues best
match an observed sample covariance matrix's eigenvalues.

MATLAB threads the optimizer's shared per-iteration state (the sorted `tau`,
its permutation, and the resulting `lambda`) through two globals, `US_A` and
`USER_DEFINED_PARAMETERS`, so that QuESTdmse can reuse what QuESTmse just
computed for the same `tau`. Here both functions are stateless: each takes
its inputs as plain arguments and recomputes the forward pass or gradient
independently, at the cost of one redundant QuEST forward pass per
mse+dmse pair evaluated at the same `tau`.
"""

from __future__ import annotations

import numpy as np

from ._types import FloatArray
from .core import quest
from .gradient import quest_grad


def quest_mse(
    tau: FloatArray,
    lambda_target: FloatArray,
    n: float,
    tau_scaling: float,
    obj_scaling: float,
) -> float:
    """Scaled mean squared distance between QuEST-implied and target sample eigenvalues."""
    tausort = np.sort(tau)
    lambda_, _, _ = quest(tausort / tau_scaling, n)
    return float(np.mean((lambda_ - lambda_target) ** 2) * obj_scaling)


def quest_dmse(
    tau: FloatArray,
    lambda_target: FloatArray,
    n: float,
    tau_scaling: float,
    obj_scaling: float,
) -> FloatArray:
    """Gradient of quest_mse wrt tau, in the original (unsorted) tau order."""
    p = tau.shape[0]
    isort = np.argsort(tau)
    tausort = tau[isort]

    lambda_, _, _ = quest(tausort / tau_scaling, n)
    dlambda = quest_grad(tausort / tau_scaling, n)

    dysort = (2.0 / p) * (dlambda.T @ (lambda_ - lambda_target)) * obj_scaling / tau_scaling

    dy = np.empty(p)
    dy[isort] = dysort
    return dy
