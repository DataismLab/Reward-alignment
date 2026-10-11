# Constraint and transaction-cost calibration: derivation

Let C be a convex feasible set, Sigma positive definite, m expected excess return, and c(u) a convex deterministic turnover cost. Target F(u)=m'u−phi u'Sigma u−lambda c(u). Denote unique maximiser u*, y*=m'u*, M=Sigma+mm', and A=1+2phi y*>0.

Then Q(u)=m'u−[phi/A]u'Mu−[lambda/A]c(u) has exactly the same maximiser. Proof, for any feasible u:

    A Q(u) = F(u) − phi(m'u−y*)² + phi(y*)².

At u* the added square is zero, while F(u)<=F(u*). Thus Q(u)<=Q(u*); strict concavity gives uniqueness. This proof actually needs no convexity for a given global target maximiser; convexity ensures efficient solution/uniqueness. It is a direct consequence of the known mean–variance auxiliary-variable identity, not claimed as a novel generic transformation.

If only the quadratic coefficient is changed to phi/A but the turnover coefficient remains lambda, then

    A Q_penalty_only(u) = F(u) − phi(m'u−y*)² − 2phi y* lambda c(u) + phi(y*)².

For positive y*, penalty-only calibration adds an unintended turnover penalty; for negative y* it lowers it. The direction need not translate into a monotone realised turnover or Sharpe ranking under constraints. This is the economically interpretable distortion to test.

The unconstrained zero-cost formula phi(1−nu) uses A=1/(1−nu) at its particular target. Under constraints, substituting that A without accounting for the new target generally fails.

For any second-moment reward optimiser u and 1−2kappa m'u>0, first-order conditions identify effective preferences phi_eff=kappa/(1−2kappa m'u), lambda_eff=lambda_raw/(1−2kappa m'u), up to the feasible-set normal cone. Thus a scalar reward can change both risk and turnover preferences. Active constraints can prevent unique identification of preference parameters; this is a sufficient interpretation, not a unique inverse solution.

Joint calibration may be computed by the existing MVPI-style auxiliary iteration: start y=0; maximise (1+2phi y)m'u−phi u'Mu−lambda c(u); set y=m'u; repeat. Its joint quadratic part in (u,y) has positive Schur complement Sigma, so the maximisation is jointly strictly concave (with convex c). Exact block optimisation converges to the unique target solution. We will include this strong prior-art baseline; no superiority over exact MVPI is claimed.

Status: algebraic identities PROVED; implementation and historical tests completed (see dated verification below). Novelty of the specific cost-coupling diagnosis is not certified. The earlier finite-horizon mismatch coefficient remains the main candidate theoretical increment.

26 September completion: four new regression tests pass; historical primary and all17 robustness settings completed. Joint mean distance <=1.54e−7 across settings. Primary MVPI adaptation agrees with target. Historical performance superiority not established. Full evidence: results/historical/ and notes/REAL_DATA_PROTOCOL.md.
