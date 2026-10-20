"""Quantized Eigenvalues Sampling Transform (QuEST).

Port of QuEST_v027/QuEST.m. See Olivier Ledoit and Michael Wolf, "Spectrum
Estimation: A Unified Framework for Covariance Matrix Estimation and PCA in
Large Dimensions", Journal of Multivariate Analysis (2015), Section 2.2,
equations (2.11)-(2.17); and "Optimal Estimation of a Large-Dimensional
Covariance Matrix under Stein's Loss", Bernoulli (2018), Theorems 5.2 and 6.2.

Each private function below corresponds to one MATLAB subfunction of the same
role (named in its docstring) and is called in the same order:

    _check_inputs -> _support -> _net_grid -> _solve_stieltjes
                   -> _density -> _distribution -> _integrate

Two deviations from the literal MATLAB translation, both confirmed:
  - checkinputs01/intfun03: the inverse-covariance branch used the
    covariance-branch mask (`j` instead of `jinv`) at one point; fixed here
    to use `jinv`/`~jinv` consistently.
  - denfun03: MATLAB's `.^` gives a complex result for a negative base with
    fractional exponent, so a tiny floating-point-noise negative value of
    `den.x` (mathematically >= 0) silently self-corrects in MATLAB. NumPy's
    real power instead returns NaN, which would propagate. `den.x` is
    clipped to be non-negative to avoid that.
"""

from __future__ import annotations

from collections.abc import Callable

import numpy as np
from scipy.optimize import brentq

from ._types import (
    BoolArray,
    ComplexArray,
    Def,
    Def2,
    Den,
    Dis,
    FloatArray,
    Int,
    IntArray,
    Net,
    QuESTContext,
    Sol,
    Sup,
)


def quest(tau: FloatArray, n: float) -> tuple[FloatArray, FloatArray, FloatArray]:
    """Quantized Eigenvalues Sampling Transform.

    Parameters
    ----------
    tau : population eigenvalues, shape (p,)
    n   : sample size

    Returns
    -------
    lambda_  : sample eigenvalues, shape (p,)
    delta    : nonlinear shrinkage for the covariance matrix, shape (p,)
    deltainv : nonlinear shrinkage for the inverse covariance matrix, shape (p,)
    """
    ctx = _forward(tau, n)
    return ctx.int_.lambda_, ctx.int_.delta, ctx.int_.deltainv


def _forward(tau: FloatArray, n: float) -> QuESTContext:
    def_ = _check_inputs(tau, n)
    sup = _support(def_)
    net = _net_grid(def_, sup)
    sol = _solve_stieltjes(def_, net)
    den = _density(def_, net, sol)
    dis = _distribution(def_, sup, net, den)
    int_ = _integrate(def_, sup, dis, den)
    return QuESTContext(def_=def_, sup=sup, net=net, sol=sol, den=den, dis=dis, int_=int_)


def _check_inputs(tau: FloatArray, n: float) -> Def:
    """Port of checkinputs01: validate/sort tau, fill in p, c, weight."""
    tau = np.array(tau, dtype=np.float64).reshape(-1)
    p = tau.shape[0]

    if n <= 0:
        raise ValueError("n must be strictly positive")
    if n < p and n != round(n):
        raise ValueError("n must be integer if it is strictly less than p")

    lefttoler = 1e-8
    toler = 1e-12
    tau[(tau < 0) & (np.abs(tau) < lefttoler)] = 0.0
    tau[(tau >= 0) & (np.abs(tau) < toler)] = 0.0
    if np.any(tau < 0):
        raise ValueError(f"the elements of tau must be non-negative (min(tau) = {tau.min()})")

    if p > 1 and np.any(np.diff(tau) < 0):
        tau = np.sort(tau)
    for i in range(1, p):
        if tau[i] < tau[i - 1] + toler:
            tau[i] = tau[i - 1]

    weight = np.full(p, 1.0 / p)
    return Def(tau=tau, n=float(n), p=p, c=p / n, weight=weight)


def _unique_weighted(tau: FloatArray, weight: FloatArray, c: float) -> tuple[Def2, float]:
    """Port of the def2/zeroweight construction at the top of supfun07."""
    t = np.unique(tau)
    w = np.array([np.sum(weight[tau == value]) for value in t])

    zeroweight = 0.0
    if t.shape[0] > 1:
        keep = w != 0
        t, w = t[keep], w[keep]
        if np.any(t == 0):
            zeroweight = float(w[t == 0][0])
            keep = t != 0
            t, w = t[keep], w[keep]

    if abs(np.sum(w) - np.mean(tau != 0)) > 1e-5 / tau.shape[0]:
        raise ValueError("weights must sum up to mean(tau != 0)")

    K = t.shape[0]
    return Def2(tau=t, weight=w, c=c, ntau=K, WT2=w * t**2), zeroweight


def _find_separations(
    def2: Def2, phi: Callable[[float], float], zeroweight: float
) -> FloatArray:
    """Port of the spectral-separation search loop in supfun07.

    Returns an (m, 4) array, one confirmed separation per row: [lo_root,
    hi_root, cumulative_left_weight, cumulative_right_weight].
    """
    t, w, K = def2.tau, def2.weight, def2.ntau
    if K <= 1:
        return np.empty((0, 4))

    xhat = (t[:-1] * t[1:]) ** (2 / 3) * (
        w[:-1] ** (1 / 3) * t[1:] ** (1 / 3) + w[1:] ** (1 / 3) * t[:-1] ** (1 / 3)
    ) / (w[:-1] ** (1 / 3) * t[:-1] ** (2 / 3) + w[1:] ** (1 / 3) * t[1:] ** (2 / 3))

    with np.errstate(divide="ignore", invalid="ignore"):
        theta = (
            w[:-1] * t[:-1] ** 2 / (t[:-1] - xhat) ** 2
            + w[1:] * t[1:] ** 2 / (t[1:] - xhat) ** 2
        )
    # MATLAB replaces non-finite entries with max(theta(~isfinite(theta))),
    # which is a no-op in effect: a non-finite entry stays >= 1/c under the
    # `theta < 1/c` test below either way (Inf fails it; NaN comparisons are
    # False in both MATLAB and NumPy), so it is omitted here.

    if K > 2:
        gaps = np.arange(K - 1)
        cols = np.arange(K)
        with np.errstate(divide="ignore", invalid="ignore"):
            minleft = (w * t**2)[None, :] / (t[None, :] - t[1:, None]) ** 2
            minright = (w * t**2)[None, :] / (t[None, :] - t[:-1, None]) ** 2
        minleft = np.where(cols[None, :] < gaps[:, None], minleft, 0.0)
        minright = np.where(cols[None, :] >= gaps[:, None] + 2, minright, 0.0)
        theta = theta + minleft.sum(axis=1) + minright.sum(axis=1)

    kk = np.where(theta < 1.0 / def2.c)[0]
    separation = np.full((K - 1, 4), np.nan)
    if kk.size == 0:
        return separation[~np.isnan(separation[:, 0])]

    dpsi = 2.0 * np.sum(def2.WT2[None, :] / (t[None, :] - xhat[kk, None]) ** 3, axis=1)

    def psi_prime(x: float) -> float:
        return 2.0 * np.sum(def2.WT2 / (t - x) ** 3)

    tolx = np.finfo(np.float64).eps

    for idx, g in enumerate(kk):
        xhat_g = xhat[g]
        dpsi_g = dpsi[idx]

        if abs(dpsi_g) <= np.spacing(xhat_g):
            xstar = xhat_g
        elif dpsi_g > 0:
            lobound = t[g] + (
                2 * w[g] * t[g] ** 2
                / (2 * w[g + 1] * t[g + 1] ** 2 / (t[g + 1] - xhat_g) ** 3 + dpsi_g)
            ) ** (1 / 3)
            xstar = (
                (lobound + xhat_g) / 2
                if abs(lobound - xhat_g) <= tolx
                else brentq(psi_prime, lobound, xhat_g)
            )
        elif dpsi_g < 0:
            hibound = t[g + 1] - (
                2 * w[g + 1] * t[g + 1] ** 2
                / (-2 * w[g] * t[g] ** 2 / (t[g] - xhat_g) ** 3 - dpsi_g)
            ) ** (1 / 3)
            xstar = (
                (hibound + xhat_g) / 2
                if abs(hibound - xhat_g) <= tolx
                else brentq(psi_prime, xhat_g, hibound)
            )
        else:
            raise RuntimeError("unexpected case for dpsi")

        phi_val = phi(xstar)
        if phi_val >= 0:
            continue

        tail_left = np.sum(
            w[g + 1 :] * t[g + 1 :] ** 2
            * (1.0 / (t[g + 1 :] - xstar) ** 2 - 1.0 / (t[g + 1 :] - t[g]) ** 2)
        )
        blo = t[g] + np.sqrt(
            w[g] * t[g] ** 2 / (w[g] * t[g] ** 2 / (t[g] - xstar) ** 2 - phi_val + tail_left)
        )
        separation[g, 0] = brentq(phi, blo, xstar)

        tail_right = np.sum(
            w[: g + 1] * t[: g + 1] ** 2
            * (1.0 / (t[: g + 1] - xstar) ** 2 - 1.0 / (t[: g + 1] - t[g + 1]) ** 2)
        )
        bhi = t[g + 1] - np.sqrt(
            w[g + 1] * t[g + 1] ** 2
            / (w[g + 1] * t[g + 1] ** 2 / (t[g + 1] - xstar) ** 2 - phi_val + tail_right)
        )
        separation[g, 1] = brentq(phi, xstar, bhi)
        separation[g, 2] = np.sum(w[: g + 1]) + zeroweight
        separation[g, 3] = np.sum(w[g + 1 :])

    return separation[~np.isnan(separation[:, 0])]


def _support(def_: Def) -> Sup:
    """Port of supfun07: support of the limiting sample spectral distribution."""
    def2, zeroweight = _unique_weighted(def_.tau, def_.weight, def_.c)
    t, w = def2.tau, def2.weight

    def phi(u: float) -> float:
        return float(np.sum(def2.WT2 / (t - u) ** 2) - 1.0 / def2.c)

    separation = _find_separations(def2, phi, zeroweight)

    expect2 = np.sum(w * t**2)
    leftlo = t[0] - np.sqrt(def_.c * expect2) - 1.0
    lefthi = t[0] - np.sqrt(def_.c * w[0] * t[0] ** 2) / 2.0
    leftmost = brentq(phi, leftlo, lefthi)

    rightlo = t[-1] + np.sqrt(def_.c * w[-1] * t[-1] ** 2) / 2.0
    righthi = t[-1] + np.sqrt(def_.c * expect2) + 1.0
    rightmost = brentq(phi, rightlo, righthi)

    numint = 1 + separation.shape[0]
    u_Fbar = np.full((numint, 2), np.nan)
    u_Fbar[0, 0] = leftmost
    u_Fbar[-1, 1] = rightmost
    if separation.shape[0] > 0:
        u_Fbar[1:, 0] = separation[:, 1]
        u_Fbar[:-1, 1] = separation[:, 0]

    m_LF = np.sum((w * t)[None, None, :] / (t[None, None, :] - u_Fbar[:, :, None]), axis=2)
    endpoint = np.maximum(0.0, u_Fbar - def_.c * u_Fbar * m_LF)
    if def_.p == def_.n:
        endpoint[0, 0] = 0.0

    if numint > 1:
        numeig_f = np.full(numint, np.nan)
        numeig_f[0] = separation[0, 2] - max(zeroweight, 1.0 - def_.n / def_.p)
        numeig_f[1:-1] = np.diff(separation[:, 2])
        numeig_f[-1] = separation[-1, 3]
        numeig = np.round(numeig_f * def_.p).astype(np.intp)
    else:
        numeig = np.array(
            [def_.p - max(np.sum(def_.tau == 0), def_.p - def_.n)], dtype=np.intp
        )

    return Sup(endpoint=endpoint, u_Fbar=u_Fbar, m_LF=m_LF, numeig=numeig, numint=numint, def2=def2)


def _net_grid(def_: Def, sup: Sup) -> Net:
    """Port of netfun02: grid over [u_1, u_2] tailored to spectrum separation."""
    minnxi = 100
    count_nonzero = int(np.sum(def_.tau != 0))
    base = min(count_nonzero, def_.n)
    nxi0 = max(minnxi, base)
    mult = int(np.ceil(nxi0 / base))
    nxi = int(round(mult * base))

    sup2xi = np.zeros((nxi, sup.numint * 2))
    interval = np.full(nxi, -1, dtype=np.intp)

    start = 0
    for i in range(sup.numint):
        m = int(sup.numeig[i]) * mult
        grid01 = np.sin((np.pi / 2) * np.linspace(0.0, 1.0, m + 2)) ** 2
        grid01 = grid01[1:-1]
        end = start + m
        sup2xi[start:end, i] = 1.0 - grid01
        sup2xi[start:end, i + sup.numint] = grid01
        interval[start:end] = i
        start = end

    xi = sup2xi @ np.concatenate([sup.u_Fbar[:, 0], sup.u_Fbar[:, 1]])
    return Net(xi=xi, sup2xi=sup2xi, nxi=nxi, mult=mult, interval=interval)


def _solve_stieltjes(def_: Def, net: Net) -> Sol:
    """Port of solfun02: solve for Im(-1/m_Fbar(z)) at each net.xi gridpoint."""
    tau, weight, c = def_.tau, def_.weight, def_.c
    kernel2 = c * weight * tau**2
    yxi = np.zeros(net.nxi)

    for iz in range(net.nxi):
        dif2 = (tau - net.xi[iz]) ** 2
        mindif2 = np.min(dif2)
        ismin = dif2 == mindif2
        lobound = np.sqrt(max(0.0, c * np.sum(weight[ismin] * tau[ismin] ** 2) - mindif2)) / 2.0
        hibound = np.sqrt(np.sum(kernel2) - mindif2) + 1.0

        if lobound == hibound:
            yxi[iz] = lobound
        elif lobound < hibound:
            yxi[iz] = brentq(
                lambda y, iz=iz: 1.0 - np.sum(kernel2 / ((tau - net.xi[iz]) ** 2 + y**2)),
                lobound,
                hibound,
            )
        else:
            raise RuntimeError("unexpected ordering of the bounds")

    return Sol(zxi=net.xi + 1j * yxi)


def _density(def_: Def, net: Net, sol: Sol) -> Den:
    """Port of denfun03: density of the limiting sample eigenvalue distribution."""
    a = 4
    tau = def_.tau[None, :]
    weight = def_.weight[None, :]
    zxi = sol.zxi[:, None]

    m_LF: ComplexArray = np.sum(weight * tau / (tau - zxi), axis=1)
    x = np.maximum(np.real(sol.zxi - def_.c * sol.zxi * m_LF), 0.0)
    f = np.imag(sol.zxi) / (np.pi * def_.c * np.abs(sol.zxi) ** 2)
    zeta = x ** (1 / a)
    g = a * zeta ** (a - 1) * f

    return Den(a=a, x=x, f=f, zeta=zeta, g=g, m_LF=m_LF)


def _distribution(def_: Def, sup: Sup, net: Net, den: Den) -> Dis:
    """Port of disfun04: cdf of the limiting sample eigenvalue distribution."""
    numx = net.nxi + 2 * sup.numint
    x = np.full(numx, np.nan)
    zeta = np.full(numx, np.nan)
    m_LF: ComplexArray = np.full(numx, np.nan, dtype=np.complex128)
    interval = np.full(numx, -1, dtype=np.intp)
    fromweight = np.full(sup.numint, np.nan)
    toweight = np.full(sup.numint, np.nan)
    Graw: list[FloatArray] = [np.empty(0) for _ in range(sup.numint)]
    G = np.full(numx, np.nan)

    weight0 = max(float(np.sum(def_.weight[def_.tau == 0])), 1.0 - 1.0 / def_.c)

    start = 0
    cum_numeig = 0
    for i in range(sup.numint):
        intlength = int(sup.numeig[i]) * net.mult + 2
        end = start + intlength
        interval[start:end] = i

        isin = net.interval == i
        x[start:end] = np.concatenate(([sup.endpoint[i, 0]], den.x[isin], [sup.endpoint[i, 1]]))
        zeta[start:end] = np.concatenate(
            (
                [sup.endpoint[i, 0] ** (1.0 / den.a)],
                den.zeta[isin],
                [sup.endpoint[i, 1] ** (1.0 / den.a)],
            )
        )
        m_LF[start:end] = np.concatenate(([sup.m_LF[i, 0]], den.m_LF[isin], [sup.m_LF[i, 1]]))
        g = np.concatenate(([0.0], den.g[isin], [0.0]))

        fromweight[i] = weight0 + cum_numeig / def_.p
        cum_numeig += int(sup.numeig[i])
        toweight[i] = weight0 + cum_numeig / def_.p

        seg_zeta = zeta[start:end]
        graw_i = np.concatenate(([0.0], np.cumsum(np.diff(seg_zeta) * (g[:-1] + g[1:]) / 2.0)))
        Graw[i] = graw_i
        G[start:end] = fromweight[i] + (toweight[i] - fromweight[i]) * graw_i / graw_i[-1]

        start = end

    return Dis(
        numx=numx,
        x=x,
        zeta=zeta,
        G=G,
        m_LF=m_LF,
        interval=interval,
        weight0=weight0,
        fromweight=fromweight,
        toweight=toweight,
        Graw=Graw,
    )


def _integrate(def_: Def, sup: Sup, dis: Dis, den: Den) -> Int:
    """Port of intfun03: quantize onto p sample eigenvalues + shrinkage formulas."""
    p, n, c = def_.p, def_.n, def_.c
    lambda_ = np.full(p, np.nan)
    delta = np.full(p, np.nan)
    deltainv = np.full(p, np.nan)
    nquant = np.zeros(sup.numint, dtype=np.intp)
    bin_list: list[IntArray] = [np.empty(0, dtype=np.intp) for _ in range(sup.numint)]
    quant_list: list[FloatArray] = [np.empty(0) for _ in range(sup.numint)]
    indic_list: list[BoolArray] = [np.empty((0, 0), dtype=bool) for _ in range(sup.numint)]

    n_zero_tau = int(np.sum(def_.tau == 0))
    n_null = max(n_zero_tau, p - n)
    limit0: float | None = None
    limitinv0: float | None = None

    if n_null > 0:
        n_null_i = int(round(n_null))
        lambda_[:n_null_i] = 0.0
        if p - n > n_zero_tau:
            lobound = np.min(def_.tau) - c * np.sum(def_.weight * def_.tau) - 1.0
            hibound = (1.0 - sup.def2.weight[0]) * sup.def2.tau[0]
            uFbar0 = brentq(
                lambda u: np.sum(sup.def2.weight * sup.def2.tau / (sup.def2.tau - u))
                - 1.0 / sup.def2.c,
                lobound,
                hibound,
            )
            nulladjust = uFbar0 / (1.0 - c)
            nulladjustinv = 1.0 / (
                1.0 / (1.0 - 1.0 / c) * np.sum(sup.def2.weight / sup.def2.tau) + 1.0 / uFbar0
            )
            delta[:n_null_i] = nulladjust
            deltainv[:n_null_i] = nulladjustinv
        else:
            delta[:n_null_i] = 0.0
            deltainv[:n_null_i] = 0.0

    if p == n:
        if np.all(def_.tau > 0):
            limit0 = float(1.0 / np.sum(sup.def2.weight / sup.def2.tau))
            limitinv0 = float(
                np.sum(sup.def2.weight / sup.def2.tau)
                / np.sum(sup.def2.weight / sup.def2.tau**2)
            )
        else:
            limit0 = 0.0
            limitinv0 = 0.0

    for i in range(sup.numint):
        idx = np.where(dis.interval == i)[0]
        F, i1 = np.unique(dis.G[idx], return_index=True)
        idx = idx[i1]
        x = dis.zeta[idx] ** den.a
        nidx = x.shape[0]

        nq = int(sup.numeig[i]) + 1
        nquant[i] = nq
        quant = np.linspace(F[0], F[-1], nq)

        bin0 = np.searchsorted(F[:-1], quant, side="right") - 1
        if bin0[0] != 0 or bin0[-1] != nidx - 2:
            raise RuntimeError("unexpected bin allocation")

        j0 = np.arange(nidx - 1)
        indic = j0[None, :] < bin0[:, None]

        def integral(values: FloatArray, F=F, quant=quant, bin0=bin0, indic=indic) -> FloatArray:
            seg = (F[1:] - F[:-1]) * (values[:-1] + values[1:]) / 2.0
            frac = quant - F[bin0]
            part = frac * (
                values[bin0]
                + frac * (values[bin0 + 1] - values[bin0]) / (F[bin0 + 1] - F[bin0]) / 2.0
            )
            total = indic @ seg + part
            return np.diff(total) * p

        lo = int(round(F[0] * p))
        hi = int(round(F[-1] * p))
        lambda_[lo:hi] = integral(x)

        denom = np.abs(1.0 - c * dis.m_LF[idx]) ** 2
        y = np.empty_like(x)
        if p == n:
            zero_mask = (x == 0) & (denom == 0)
            y[zero_mask] = limit0
            y[~zero_mask] = x[~zero_mask] / denom[~zero_mask]
        else:
            y = x / denom
        delta[lo:hi] = integral(y)
        if p == n:
            delta[lo:hi] = np.maximum(delta[lo:hi], limit0)

        denominv = 1.0 + c - 2.0 * c * np.real(dis.m_LF[idx])
        z = np.empty_like(x)
        if p == n:
            zero_mask_inv = (x == 0) & (denominv == 0)
            z[zero_mask_inv] = limitinv0
            z[~zero_mask_inv] = x[~zero_mask_inv] / denominv[~zero_mask_inv]
        else:
            z = x / denominv
        deltainv[lo:hi] = integral(z)
        if p == n:
            deltainv[lo:hi] = np.maximum(deltainv[lo:hi], limitinv0)

        bin_list[i] = bin0
        quant_list[i] = quant
        indic_list[i] = indic

    return Int(
        lambda_=lambda_,
        delta=delta,
        deltainv=deltainv,
        nquant=nquant,
        bin=bin_list,
        quant=quant_list,
        indic=indic_list,
        limit0=limit0,
        limitinv0=limitinv0,
    )
