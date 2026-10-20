"""Data structures for the QuEST forward pass.

Each dataclass mirrors a MATLAB struct from QuEST_v027/QuEST.m, with the same
field names, so a given stage can be checked directly against the MATLAB
function that produces it:

    Def  <- checkinputs01   Net  <- netfun02   Dis <- disfun04
    Def2 <- supfun07        Sol  <- solfun02   Int <- intfun03
    Sup  <- supfun07        Den  <- denfun03

Every dataclass is frozen and built via a complete constructor: a stage
function takes the previous stage's struct(s) and returns a brand new one,
never mutates in place.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

FloatArray = npt.NDArray[np.float64]
ComplexArray = npt.NDArray[np.complex128]
IntArray = npt.NDArray[np.intp]
BoolArray = npt.NDArray[np.bool_]


@dataclass(frozen=True)
class Def:
    """Problem definition: population eigenvalues and sample size."""

    tau: FloatArray  # (p,) sorted, non-negative population eigenvalues
    n: float
    p: int
    c: float  # p / n
    weight: FloatArray  # (p,) equal to 1/p


@dataclass(frozen=True)
class Def2:
    """Alternative definition with unique, strictly positive tau's (sup.def2)."""

    tau: FloatArray  # (K,)
    weight: FloatArray  # (K,) aggregated weight per unique tau
    c: float
    ntau: int  # K
    WT2: FloatArray  # (K,) weight * tau**2


@dataclass(frozen=True)
class Sup:
    """Support of the limiting sample spectral distribution, in u-space."""

    endpoint: FloatArray  # (numint, 2)
    u_Fbar: FloatArray  # (numint, 2)
    m_LF: FloatArray  # (numint, 2) -- real: evaluated at real support endpoints
    numeig: IntArray  # (numint,)
    numint: int
    def2: Def2


@dataclass(frozen=True)
class Net:
    """Grid over [u_1, u_2], the real part of -1/m_Fbar(z)."""

    xi: FloatArray  # (nxi,)
    sup2xi: FloatArray  # (nxi, numint * 2)
    nxi: int
    mult: int
    interval: IntArray  # (nxi,)


@dataclass(frozen=True)
class Sol:
    """Solution to the Marcenko-Pastur equation in -1/m_Fbar(z) space."""

    zxi: ComplexArray  # (nxi,)


@dataclass(frozen=True)
class Den:
    """Density of the limiting sample eigenvalue distribution."""

    a: int  # exponent of the power transform of the abscissa (= 4)
    x: FloatArray  # (nxi,)
    f: FloatArray  # (nxi,)
    zeta: FloatArray  # (nxi,) x**(1/a)
    g: FloatArray  # (nxi,) dG(zeta)/dzeta
    m_LF: ComplexArray  # (nxi,)


@dataclass(frozen=True)
class Dis:
    """Cdf of the limiting sample eigenvalue distribution, per support interval."""

    numx: int
    x: FloatArray  # (numx,)
    zeta: FloatArray  # (numx,)
    G: FloatArray  # (numx,)
    m_LF: ComplexArray  # (numx,)
    interval: IntArray  # (numx,)
    weight0: float  # mass point of the sample cdf at zero
    fromweight: FloatArray  # (numint,)
    toweight: FloatArray  # (numint,)
    Graw: list[FloatArray]  # ragged, one array per support interval


@dataclass(frozen=True)
class Int:
    """Quantized sample eigenvalues and nonlinear shrinkage formulas."""

    lambda_: FloatArray  # (p,) sample eigenvalues
    delta: FloatArray  # (p,) shrinkage for covariance matrix eigenvalues
    deltainv: FloatArray  # (p,) shrinkage for inverse covariance matrix
    nquant: IntArray  # (numint,)
    bin: list[IntArray]  # ragged, one array per support interval
    quant: list[FloatArray]  # ragged, one array per support interval
    indic: list[BoolArray]  # ragged, one 2-D array per support interval
    limit0: float | None = None  # set only when p == n
    limitinv0: float | None = None  # set only when p == n


@dataclass(frozen=True)
class QuESTContext:
    """Everything produced by one run of the QuEST forward pass.

    Replaces MATLAB's `global US_D`: QuESTgrad reruns the forward pass to
    obtain this bundle rather than reaching into module-level state.
    """

    def_: Def
    sup: Sup
    net: Net
    sol: Sol
    den: Den
    dis: Dis
    int_: Int


# --- Gradient-side mirrors -------------------------------------------------
#
# Each field gains a trailing p dimension: one column per population
# eigenvalue being differentiated against. Differentiation is against the
# full def.tau/def.weight arrays (length p, duplicates and zeros included),
# not the deduplicated Def2, so there is no DDef/DDef2. QuESTgrad.m's public
# output is only the Jacobian of the sample eigenvalues (dlambda) -- it never
# differentiates delta/deltainv -- so DInt carries only lambda_.


@dataclass(frozen=True)
class DSup:
    """Gradient of Sup wrt population eigenvalues (supgrd01)."""

    u_Fbar: FloatArray  # (numint, 2, p)
    endpoint: FloatArray  # (numint, 2, p)


@dataclass(frozen=True)
class DNet:
    """Gradient of Net wrt population eigenvalues (netgrd02)."""

    xi: FloatArray  # (nxi, p)


@dataclass(frozen=True)
class DSol:
    """Gradient of Sol wrt population eigenvalues (solgrd01)."""

    zxi: ComplexArray  # (nxi, p)


@dataclass(frozen=True)
class DDen:
    """Gradient of Den wrt population eigenvalues (dengrd02)."""

    x: FloatArray  # (nxi, p)
    f: FloatArray  # (nxi, p)
    zeta: FloatArray  # (nxi, p)
    g: FloatArray  # (nxi, p)
    m_LF: ComplexArray  # (nxi, p)


@dataclass(frozen=True)
class DDis:
    """Gradient of Dis wrt population eigenvalues (disgrd03)."""

    zeta: FloatArray  # (numx, p)
    G: FloatArray  # (numx, p)


@dataclass(frozen=True)
class DInt:
    """Gradient of sample eigenvalues wrt population eigenvalues (intgrd02)."""

    lambda_: FloatArray  # (p, p)
