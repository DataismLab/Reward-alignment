"""Gradient of the Quantized Eigenvalues Sampling Transform.

Port of QuEST_v027/QuESTgrad.m. Computes the Jacobian of the sample
eigenvalues with respect to the population eigenvalues, via the implicit
function theorem applied to each root found in the forward pass (core.py) --
no root-finding happens here, only closed-form chain-rule arithmetic.

Each private function below mirrors one MATLAB subfunction of the same role,
called in the same order:

    _support_grad -> _net_grid_grad -> _solve_stieltjes_grad
                   -> _density_grad -> _distribution_grad -> _integrate_grad

The differentiation is against the full `def.tau`/`def.weight` arrays
(length p, duplicates and zeros included), not the deduplicated `Def2` used
internally by the forward pass's `_support` -- so duplicate-tau columns come
out identical and zero-tau columns come out zero without any special-casing.

QuESTgrad.m's public output is only the Jacobian of the sample eigenvalues
(`dlambda`); it never differentiates the nonlinear shrinkage formulas
delta/deltainv, so neither does this module.
"""

from __future__ import annotations

import numpy as np

from ._types import (
    ComplexArray,
    DDen,
    DDis,
    DInt,
    DNet,
    DSol,
    DSup,
    FloatArray,
    QuESTContext,
)
from .core import _forward


def quest_grad(tau: FloatArray, n: float) -> FloatArray:
    """Gradient of the sample eigenvalues wrt the population eigenvalues.

    Parameters
    ----------
    tau : population eigenvalues, shape (p,)
    n   : sample size

    Returns
    -------
    dlambda : shape (p, p); entry (i, j) is d(lambda_i) / d(tau_j)
    """
    ctx = _forward(tau, n)
    dsup = _support_grad(ctx)
    dnet = _net_grid_grad(ctx, dsup)
    dsol = _solve_stieltjes_grad(ctx, dnet)
    dden = _density_grad(ctx, dsol)
    ddis = _distribution_grad(ctx, dsup, dden)
    dint = _integrate_grad(ctx, ddis)
    return dint.lambda_


def _support_grad(ctx: QuESTContext) -> DSup:
    """Port of supgrd01: gradient of the support endpoints in u-space."""
    def_, sup = ctx.def_, ctx.sup
    tau = def_.tau[None, None, :]
    weight = def_.weight[None, None, :]
    u = sup.u_Fbar[:, :, None]

    denom_sum = np.sum(weight * tau**2 / (tau - u) ** 3, axis=2, keepdims=True)
    du_Fbar = weight * tau * u / (tau - u) ** 3 / denom_sum
    dendpoint = def_.c * u**2 * weight / (tau - u) ** 2
    if def_.p == def_.n:
        dendpoint[0, 0, :] = 0.0

    return DSup(u_Fbar=du_Fbar, endpoint=dendpoint)


def _net_grid_grad(ctx: QuESTContext, dsup: DSup) -> DNet:
    """Port of netgrd02: gradient of the xi grid."""
    flat = np.concatenate([dsup.u_Fbar[:, 0, :], dsup.u_Fbar[:, 1, :]], axis=0)
    return DNet(xi=ctx.net.sup2xi @ flat)


def _solve_stieltjes_grad(ctx: QuESTContext, dnet: DNet) -> DSol:
    """Port of solgrd01: gradient of -1/m_Fbar(z) via implicit differentiation."""
    def_, net, sol = ctx.def_, ctx.net, ctx.sol
    tau = def_.tau[None, :]
    weight = def_.weight[None, :]
    xi = net.xi[:, None]
    yxi = np.imag(sol.zxi)[:, None]

    t_x = tau - xi
    cplxnorm = t_x**2 + yxi**2
    cplxnorm2 = cplxnorm**2
    wt2 = weight * tau**2

    numerator = 2.0 * np.sum(wt2 * t_x / cplxnorm2, axis=1)
    denominator = 2.0 * np.sum(wt2 * yxi / cplxnorm2, axis=1)

    dyxi_dtau = (2.0 * weight * tau / cplxnorm - 2.0 * wt2 * t_x / cplxnorm2) / denominator[:, None]
    dyxi_dxi = numerator / denominator
    dyxi = dyxi_dtau + dyxi_dxi[:, None] * dnet.xi

    zxi: ComplexArray = dnet.xi + 1j * dyxi
    return DSol(zxi=zxi)


def _density_grad(ctx: QuESTContext, dsol: DSol) -> DDen:
    """Port of dengrd02: gradient of the density of sample eigenvalues."""
    def_, sol, den = ctx.def_, ctx.sol, ctx.den
    tau = def_.tau[None, :]
    weight = def_.weight[None, :]
    z = sol.zxi[:, None]
    dz = dsol.zxi

    df = np.imag(dz / z**2) / (np.pi * def_.c)

    sum_term = np.sum(weight * tau / (tau - z) ** 2, axis=1)
    dm_LF: ComplexArray = -z * weight / (tau - z) ** 2 + dz * sum_term[:, None]

    dx = np.real(dz * (1.0 - def_.c * den.m_LF)[:, None] - def_.c * z * dm_LF)
    dzeta = (1.0 / den.a) * dx * (den.x ** (1.0 / den.a - 1.0))[:, None]
    dg = (den.a * (den.a - 1)) * dzeta * (den.f * den.zeta ** (den.a - 2))[:, None] + den.a * (
        den.zeta ** (den.a - 1)
    )[:, None] * df

    return DDen(x=dx, f=df, zeta=dzeta, g=dg, m_LF=dm_LF)


def _distribution_grad(ctx: QuESTContext, dsup: DSup, dden: DDen) -> DDis:
    """Port of disgrd03: gradient of the cdf of sample eigenvalues."""
    def_, sup, net, den, dis = ctx.def_, ctx.sup, ctx.net, ctx.den, ctx.dis
    p = def_.p
    dzeta = np.full((dis.numx, p), np.nan)
    dG = np.full((dis.numx, p), np.nan)

    start = 0
    for i in range(sup.numint):
        intlength = int(sup.numeig[i]) * net.mult + 2
        end = start + intlength
        isin = net.interval == i

        left = (1.0 / den.a) * sup.endpoint[i, 0] ** (1.0 / den.a - 1.0) * dsup.endpoint[i, 0, :]
        right = (1.0 / den.a) * sup.endpoint[i, 1] ** (1.0 / den.a - 1.0) * dsup.endpoint[i, 1, :]
        dzeta[start:end, :] = np.vstack([left, dden.zeta[isin, :], right])

        if start == 0 and def_.p == def_.n:
            dzeta[0, :] = 0.0

        g = np.concatenate(([0.0], den.g[isin], [0.0]))
        dg = np.vstack([np.zeros(p), dden.g[isin, :], np.zeros(p)])

        dseg = np.diff(dzeta[start:end, :], axis=0)
        gseg = ((g[:-1] + g[1:]) / 2.0)[:, None]
        term1 = np.cumsum(dseg * gseg, axis=0)

        dzeta_fwd = np.diff(dis.zeta[start:end])[:, None]
        dgseg = (dg[:-1, :] + dg[1:, :]) / 2.0
        term2 = np.cumsum(dzeta_fwd * dgseg, axis=0)

        dGraw = np.vstack([np.zeros(p), term1 + term2])

        wdif = dis.toweight[i] - dis.fromweight[i]
        graw_last = dis.Graw[i][-1]
        dG[start:end, :] = (
            wdif * dGraw / graw_last
            - wdif * dis.Graw[i][:, None] * dGraw[-1, :][None, :] / graw_last**2
        )

        start = end

    return DDis(zeta=dzeta, G=dG)


def _integrate_grad(ctx: QuESTContext, ddis: DDis) -> DInt:
    """Port of intgrd02: gradient of the quantized sample eigenvalues."""
    def_, sup, dis, den, int_ = ctx.def_, ctx.sup, ctx.dis, ctx.den, ctx.int_
    p = def_.p
    dlambda = np.full((p, p), np.nan)

    n0tau = int(np.sum(def_.tau == 0))
    pn = int(round(p - def_.n))
    if pn > n0tau:
        dlambda[:pn, :] = 0.0
    elif n0tau > 0:
        lo = max(0, pn)
        dlambda[lo:n0tau, :n0tau] = 1.0 - def_.c
        dlambda[lo:n0tau, n0tau:] = 0.0

    for i in range(sup.numint):
        idx = np.where(dis.interval == i)[0]
        F, i1 = np.unique(dis.G[idx], return_index=True)
        idx = idx[i1]
        x = dis.x[idx]

        dF = ddis.G[idx, :]
        dx = den.a * (dis.zeta[idx] ** (den.a - 1))[:, None] * ddis.zeta[idx, :]

        bin0 = int_.bin[i]
        quant = int_.quant[i]
        indic = int_.indic[i]

        dseg = (dF[1:, :] - dF[:-1, :]) * ((x[:-1] + x[1:]) / 2.0)[:, None] + (
            F[1:] - F[:-1]
        )[:, None] * (dx[:-1, :] + dx[1:, :]) / 2.0

        frac = quant - F[bin0]
        gap = F[bin0 + 1] - F[bin0]
        slope_x = (x[bin0 + 1] - x[bin0]) / gap

        part = (
            quant[:, None] * dx[bin0, :]
            - dx[bin0, :] * F[bin0][:, None]
            - dF[bin0, :] * x[bin0][:, None]
            - 2.0 * dF[bin0, :] * (frac * slope_x / 2.0)[:, None]
            + (dx[bin0 + 1, :] - dx[bin0, :]) * (frac**2 / gap / 2.0)[:, None]
            - (dF[bin0 + 1, :] - dF[bin0, :]) * (frac**2 * slope_x / gap / 2.0)[:, None]
        )

        total = indic @ dseg + part
        lo = int(round(F[0] * p))
        hi = int(round(F[-1] * p))
        dlambda[lo:hi, :] = np.diff(total, axis=0) * p

    return DInt(lambda_=dlambda)
