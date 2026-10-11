"""Legacy exact illustration of reward/financial-objective disagreement.
Current calibrated comparisons and limitations are in mvrl.experiments.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import minimize_scalar

from .equilibrium import solve_equilibrium
from .evaluate import exact_affine_objective
from .market import Market
from .policies import AffinePolicy, li_ng_precommitted
from .surrogate import (
    Reward,
    additive_objective,
    optimise_surrogate,
    policy_distance,
)


def demo_market() -> Market:
    mu = np.array([0.06, 0.04, 0.02])
    vol = np.array([0.18, 0.12, 0.08])
    corr = np.array(
        [[1.00, 0.30, -0.10], [0.30, 1.00, 0.05], [-0.10, 0.05, 1.00]]
    )
    return Market(
        mu_excess=mu,
        cov_excess=np.outer(vol, vol) * corr,
        riskless=1.02,
        horizon=4,
    )


def unboundedness_evidence(market: Market, x0: float) -> list[tuple[int, float]]:
    """Evaluate the plain-return surrogate along a ray of increasing leverage."""
    T, n = market.horizon, market.n_assets
    direction = np.linalg.solve(market.M(0), market.m(0))
    rows = []
    for scale in (1, 10, 100, 1_000, 10_000, 100_000):
        policy = AffinePolicy(
            alpha=np.zeros((T, n)), beta=np.tile(scale * direction, (T, 1))
        )
        rows.append(
            (scale, additive_objective(market, policy, Reward("plain"), x0))
        )
    return rows


def main() -> None:
    market = demo_market()
    phi, x0 = 1.0, 1.0

    precommitted = li_ng_precommitted(market, phi, x0)
    equilibrium = solve_equilibrium(market, phi).policy
    j_pre = exact_affine_objective(market, precommitted, phi, x0).objective
    j_eq = exact_affine_objective(market, equilibrium, phi, x0).objective

    def surrogate_for(kappa: float) -> tuple[float, AffinePolicy]:
        policy = optimise_surrogate(
            market, Reward("varpen", kappa=float(kappa)), x0, n_restarts=6
        )
        return exact_affine_objective(market, policy, phi, x0).objective, policy

    # ------------------------------------------------------------------ (1)
    print("=" * 74)
    print("1.  Plain return is unbounded when positions are unconstrained")
    print("=" * 74)
    print("""The plain-return reward r_t = x_{t+1} - x_t carries no risk term, so
the additive objective rewards unbounded leverage.  Along a ray of increasing
position size:""")
    print(f"\n{'leverage scale':>16} {'E[sum of rewards]':>22}")
    for scale, value in unboundedness_evidence(market, x0):
        print(f"{scale:16d} {value:22.4f}")
    print("""
Expected cumulative return grows along this unconstrained leverage ray.
The mean-variance reference below includes a risk penalty. Adding portfolio
constraints would define a different optimisation problem.""")

    # ------------------------------------------------------------------ (2)
    print("\n" + "=" * 74)
    print("2.  With a risk term, the surrogate optimum is a third policy")
    print("=" * 74)

    j_natural, policy_natural = surrogate_for(phi)
    search = minimize_scalar(
        lambda k: -surrogate_for(k)[0],
        bounds=(0.4, 2.0),
        method="bounded",
        options={"xatol": 1e-9},
    )
    kappa_star = float(search.x)
    j_star, policy_star = surrogate_for(kappa_star)

    print(f"\n  J(pi_pre)                = {j_pre:12.9f}")
    print(f"  J(pi_eq)                 = {j_eq:12.9f}")
    print(f"  J(pi_r), kappa = phi     = {j_natural:12.9f}")
    print(f"  J(pi_r), kappa = kappa*  = {j_star:12.9f}    kappa* = {kappa_star:.6f}")

    print(f"\n  eps_surr = J(pi_eq) - J(pi_r)  =  {j_eq - j_star:+.9f}")
    print(f"  shortfall against pre-committed =  {j_pre - j_star:.9f}"
          f"   ({100*(j_pre-j_star)/(j_pre-j_eq):.1f}% of eps_incons)")

    print(f"\n  distance(pi_r, pi_eq)  = {policy_distance(market, policy_star, equilibrium, x0):9.6f}")
    print(f"  distance(pi_r, pi_pre) = {policy_distance(market, policy_star, precommitted, x0):9.6f}")

    print("""
The selected surrogate policy differs from both reference policies. The signed
financial-value difference against equilibrium is negative in this example;
it is not a nonnegative optimisation regret. The bounded search selects a risk
penalty different from phi.""")
    print(f"  bounded-search kappa* = {kappa_star:.6f}, not phi = {phi}")
    print(f"  cost of the natural choice = {j_star - j_natural:.9f}")

    # ------------------------------------------------------------------ (3)
    print("\n" + "=" * 74)
    print("3.  Sharpe and mean-variance rankings differ")
    print("=" * 74)

    print(f"\n  {'policy':<20}{'E[x_T]':>10}{'sd':>10}{'Sharpe':>10}{'J':>14}")
    print("  " + "-" * 64)
    rows = [
        ("pre-committed", precommitted),
        ("equilibrium", equilibrium),
        ("surrogate, kappa*", policy_star),
        ("surrogate, kappa=phi", policy_natural),
    ]
    table = []
    for name, policy in rows:
        ev = exact_affine_objective(market, policy, phi, x0)
        sd = float(np.sqrt(ev.variance))
        sharpe = (ev.mean - x0 * np.prod([market.s(t) for t in range(market.horizon)])) / sd
        table.append((name, sharpe, ev.objective))
        print(f"  {name:<20}{ev.mean:10.4f}{sd:10.4f}{sharpe:10.4f}"
              f"{ev.objective:14.6f}")

    by_sharpe = [n for n, _, _ in sorted(table, key=lambda r: -r[1])]
    by_objective = [n for n, _, _ in sorted(table, key=lambda r: -r[2])]
    print(f"\n  ranked by Sharpe ratio: {' > '.join(by_sharpe)}")
    print(f"  ranked by J:            {' > '.join(by_objective)}")

    equilibrium_row = next(r for r in table if r[0] == "equilibrium")
    natural_row = next(r for r in table if r[0] == "surrogate, kappa=phi")
    if natural_row[1] > equilibrium_row[1] and natural_row[2] < equilibrium_row[2]:
        print(f"""
  The kappa = phi surrogate has the HIGHER Sharpe ratio
      {natural_row[1]:.4f} against {equilibrium_row[1]:.4f}
  and the LOWER mean-variance objective
      {natural_row[2]:.6f} against {equilibrium_row[2]:.6f}.

  The two metrics rank this pair differently. A higher Sharpe ratio does not
  establish a higher mean-variance objective for the specified risk aversion.""")

    print('This example shows ranking disagreement. It is not a claim against Sharpe as a different objective.')

if __name__ == '__main__': main()
