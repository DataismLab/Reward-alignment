# Calibration with imperfect anchors, estimated covariance and financing costs

7 October 2026. These are proved consequences of the existing mean auxiliary and convex optimisation, not claims to have invented that identity or general sensitivity analysis.

## 1. General deterministic cost and an imperfect mean anchor

On a convex feasible set C, let F(u)=m'u-phi*u'V*u-g(u), phi>0, V positive definite, g convex. The function g may include turnover, deterministic borrow/lend spreads and short-position fees. Define M=V+mm', arbitrary anchor a, and A=1+2*phi*a>0. Let Q_a(u)=m'u-phi/A*u'M*u-g(u)/A.

For every u,

    A Q_a(u) = F(u) - phi*(m'u-a)^2 + phi*a^2.

Let u* maximise F, y*=m'u*, and let uhat be epsilon-optimal for Q_a: max_C Q_a-Q_a(uhat)<=epsilon. Comparing Q_a(uhat) with Q_a(u*) gives

    0 <= F(u*)-F(uhat)
      <= phi*(y*-a)^2 - phi*(m'uhat-a)^2 + A*epsilon
      <= phi*(y*-a)^2 + A*epsilon.

Strong concavity and optimality on C give F(u*)-F(u)>=phi*lambda_min(V)*||u-u*||^2. Consequently

    ||uhat-u*|| <= sqrt((phi*(y*-a)^2+A*epsilon)/(phi*lambda_min(V))).

An a posteriori version does not require y*: any independently certified feasible reference u0 with F(u*)-F(u0)<=eta obeys ||u0-u*||<=sqrt(eta/(phi*lambda_min(V))). Hence

    |y*-a| <= |m'u0-a| + ||m||*sqrt(eta/(phi*lambda_min(V))).

Use this upper bound in the preceding inequality. Thus a certified approximate reference gives an implementable error budget; a point estimate without a reference certificate is not a guarantee. With singular V the value bound survives but the Euclidean bound does not follow, nor does uniqueness.

All deterministic preference terms in g must be divided by A. Rescaling turnover but leaving a financing spread unchanged changes the objective. For a convex g and compact polytope, the same epigraph linear-programme first-order certificate bounds epsilon. A stochastic financing rate correlated with returns must be incorporated into the random payoff/moments; it is not covered by pretending it is deterministic g.

## 2. Changing covariance is not a reward-design error

Use the same m, phi, g and C, but let V0 be the reference covariance and V1 the alternative. Let u0 maximise F0 and u1 maximise F1, and E=V1-V0. If lambda=lambda_min(V0)>0, optimality of u1 and strong concavity yield, with d=u0-u1,

    F0(u0)-F0(u1) <= 2*phi*(E u1)'d - phi*lambda*||d||^2
                       <= phi*||E u1||^2/lambda.

Combining with F0(u0)-F0(u1)>=phi*lambda*||d||^2 gives

    ||u0-u1|| <= ||E u1||/lambda.

If u1 is approximate with first-order certificate c1 for the convex negative F1, add c1 to the upper value bound, and use its square-root consequence for distance. Approximation of u0 can understate the measured F0 gap; no equality with the unknown exact optimum is assumed in the numerical audit.

This quantifies changes between two fitted models. It does not estimate the unknown true historical covariance. For joint calibration fitted to V1, convergence to u1 is consistent with a nonzero distance to u0.

## 3. A dependence-blind restriction of an assetwise PnL reward

Habibnia/Soltanzadeh (2024) Eq.8 motivates the explicitly restricted no-loan, unit-capital, long-only reward

    E sum_i [(u_i R_i)^+ - k*(u_i R_i)^-] - (k/5)*lambda*||u-p||_1.

Since u_i>=0, positive homogeneity makes it a linear-return score: sum_i u_i*(E R_i^+ - k E R_i^-) minus the turnover penalty. It depends on asset marginals, not cross-asset dependence. This fact concerns this restriction, not their SAC policy/environment as a whole. A portfolio-level downside penalty (u'R)^- is different and does depend on joint returns.

Counterexample: three zero-mean assets with equal symmetric marginals and unit variances. In market A all are independent (V=I); in market B only assets 1 and 2 have correlation 1/2. For long-only full investment and no costs, every k assigns equal marginal scores, so the restricted reward has the whole simplex as its argmax in both markets. The unique MV reference is (1/3,1/3,1/3) in A and (2/7,2/7,3/7) in B. No unique reference is identified by this reward; adding a tie-breaker using covariance changes the decision mechanism beyond the specified reward. This is a simple explanatory counterexample, not a priority claim or criticism of a downside mandate.
