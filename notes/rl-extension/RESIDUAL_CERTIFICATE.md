# A posteriori equilibrium audit — derivation, 9 October 2026

**Status: proved algebraically under the assumptions below; numerical checks pending
at first writing. Novelty/priority remains open.** This is not a general continuous-
state actor–critic convergence theorem, nor an investment-superiority result.

## Setup

Exogenous finite Markov state Z, transition P_t, possibly vector excess return R_t
jointly distributed with Z_(t+1), conditional mean m_t and positive definite covariance
Sigma_t. X_(t+1)=s X_t+R_t' u_t(Z_t), H_t=s^(T-t-1), phi>0. Deterministic policies
are wealth-independent; current deviations may take any vector in R^d. Conditional
on next state, future innovations are independent of the current return. All moments
exist. Define continuation terminal excess-gain mean

    a_T=0; a_t=H_t m_t' u_t+P_t a_(t+1).

One-step deviation value, fixing ALL future decisions at the candidate policy, is
quadratic in current action v, up to an action-independent term:

    J_t(v)=H_t m_t'v - phi H_t² v'Sigma_t v
           -2 phi H_t Cov_t(R_t,a_(t+1)(Z'))'v + constant.

This follows by writing terminal wealth as s^(T-t)x+H_t R_t'v+future_gain.
The Markov assumption makes Cov(R_t,future_gain)=Cov(R_t,a_(t+1)(Z')).
It is essential: simply conditioning on Z' is not valid for arbitrary hidden memory.

Define d_t=gradient J_t(u_t). Completing the square proves the exact deviation gain

    E_t = max_v [J_t(v)-J_t(u_t)]
        = ||Sigma_t^(-1/2) d_t||² / (4 phi H_t²).                 (1)

max_(t,z) E_t is an epsilon-equilibrium certificate. It is not global-policy regret.
Zero at every state gives an equilibrium in this policy class, including deviations
depending on current wealth because the best response is wealth-independent here.

## Critic and actor certificate

For ANY critic c_t(z), including an imperfect terminal c_T, let

    e_t=c_t-H_t m_t'u_t-P_t c_(t+1),  delta_t=c_t-a_t,
    g_t=H_t m_t-2 phi H_t Cov(R_t,c_(t+1))-2 phi H_t² Sigma_t u_t.

Then delta_t=e_t+P_t delta_(t+1), delta_T=c_T. Set S_T=span(c_T),
S_t=span(e_t)+rho_t S_(t+1), where
rho_t=0.5 max_(z,w) sum_j |P_t(z,j)-P_t(w,j)|. Stochastic-kernel span contraction
gives span(delta_t)<=S_t by backward induction. Therefore

    sqrt(E_t) <= ||Sigma_t^(-1/2)g_t||/(2 sqrt(phi) H_t)
                 + sqrt(phi) S_(t+1)/2.                        (2)

Proof of the last term: d_t=g_t+2 phi H_t Cov(R_t,delta_(t+1)). For any random
scalar D, Cov(R,D)'Sigma^(-1)Cov(R,D)<=Var(D), since the residual variance after
linear projection on R is nonnegative. Popoviciu's bound gives Var(D)<=span(D)²/4.
Apply the triangle inequality to (1). This is also valid in dimension d>1 and has
no explicit dimension factor; estimating Sigma reliably still depends on dimension.
The factor 1/2 is attainable for a two-point D linearly explained by R; this does
not establish sharpness of the entire multi-time bound in every market.

If a learner uses another reward with action gradient h_t, split g_t=h_t+(g_t-h_t):
the first term in (2) can be bounded by

    actor = ||Sigma^(-1/2)h_t||/(2 sqrt(phi) H_t),
    reward = ||Sigma^(-1/2)(g_t-h_t)||/(2 sqrt(phi) H_t).

Thus sqrt(E)<=actor+reward+critic. This split is an upper bound, not an additive
identity of signed returns; cancellation may make it loose. A small parameter
gradient of a saturated neural actor does NOT imply a small action gradient h_t.
Audit actions, not only neural optimiser loss.

## Why the span matters

Adding any state-constant offset to c_t leaves Cov(R,c_(t+1)) unchanged. Although
such offsets can make ordinary value-error norms arbitrarily large, they do not
change the actor decision. Span residuals remove that irrelevant component. If
rho_t<=rho<1 and span(e_t)<=epsilon, c_T constant, then S_(t+1) is at most
epsilon (1-rho^(T-t-1))/(1-rho), rather than a linear-horizon sum. This is standard
Dobrushin contraction used here for the specific mean–variance deviation audit.
It must not be advertised as a new contraction principle.

## A sample reward and independent-data certificate

Two independent conditional observations (R_1,Z'_1),(R_2,Z'_2) give reward

    L_c(v)=H (R_1+R_2)'v/2
           -phi/2 [H(R_1-R_2)'v+c(Z'_1)-c(Z'_2)]².             (3)

Its expected action gradient is g_t. This is a standard unbiased paired covariance
construction, used as a structured sample-based backward actor update. Learning c
backwards from sampled targets H R'u+c_next requires no solved equilibrium. This
specialisation inherits ideas from SPERL; it is not claimed as a new general solver.

For scalar returns |R|<=B and a policy/critic fixed INDEPENDENTLY of the audit
data, use n independent pairs at every (t,z). The gradient sample from (3) has
absolute bound M=H B+2 phi H B span(c_next)+4 phi H² B² |u|.
Hoeffding gives |g-g_hat|<=2M sqrt(log(2/q)/(2n)). The pair variable
(R_1-R_2)²/2 lies in [0,2B²], so v>=v_hat-2B² sqrt(log(2/q)/(2n)).
Single-observation Bellman targets have range <=2H B|u|+span(c_next);
their mean radius uses 2n observations. Residual intervals [l_z,h_z] imply
span(e_t)<=max_z h_z-min_z l_z. Use rho=1 unless independently certified.
Union-bound all 3*T*K assertions with q=alpha/(3*T*K). If any variance lower
bound is nonpositive, return an infinite certificate, not an invented floor.
Insert |g_hat|+radius and the variance lower bound in (2). This certifies all
states simultaneously with probability >=1-alpha, conditional on training output.
Training on the audit set or selecting among policies using it invalidates the
single-policy statement unless a further valid multiple-testing procedure is used.

The scalar implementation is intentionally conservative. Small empirical residuals
alone are not a certificate; neither are model-based residuals observable in reality.
At this first stage, constraint extensions, continuous states, dependent audit
samples, finite-sample vector covariance estimation and tight adaptive stopping
were open. The constrained deterministic extension below subsequently resolves
the first item for fixed convex action sets, not for general trading frictions.

## Sequential refinement after the first Hoeffding experiment

The first observable bounds were valid but loose. Two standard refinements are
implemented separately, preserving the initial Hoeffding outputs:

1. Maurer–Pontil (COLT 2009), Theorem 4, PDF p.2, for a variable of known range
   width W: radius sqrt(2 sample_variance log(4/q)/n)+7 W log(4/q)/(3(n-1)).
   The log(4/q) allocates q/2 to each tail; sample variance uses n-1. This is an
   application of their bound, not a new concentration inequality.
2. Estimate each conditional transition entry from independent audit observations.
   Simultaneous Hoeffding entry error <=eta implies rho_t<=min(1,rho_hat+K eta)
   by the triangle inequality. Include T*K*K additional events in the same union
   bound; use the certified upper rho in the residual-span recursion.

Neither changes the trained policy. The primary guarantee is conditional on a
single frozen training output, simultaneous over states. Comparing multiple bound
constructions after looking at them does not confer joint 95% coverage unless
alpha is allocated across constructions. Report their separate pointwise coverage
and preserve this distinction. See run_certificate_refinement.py.

## Convex-action extension (same research session)

**Status: proved under the same exogenous-state/wealth-independent assumptions.**
For a fixed nonempty closed convex feasible set C_t(z) with an attained maximiser,
let E_c=max_(v in C)[J_c(v)-J_c(u)], where J_c uses c_next in the continuation
covariance. Then, for feasible u, the constrained true deviation gain satisfies

    sqrt(E_true) <= sqrt(E_c)+sqrt(phi) S_next/2.               (4)

Proof: write J_true(v)=J_c(v)+b'v+constant with
b=2 phi H Cov(R,c_next-a_next). Set v_c=argmax_C J_c and k=phi H².
Strong concavity and the variational inequality at v_c give
J_c(v)-J_c(v_c)<=-k ||v-v_c||_Sigma² and
||u-v_c||_Sigma<=sqrt(E_c/k). Thus

    J_true(v)-J_true(u)
    <= E_c+||b||_(Sigma^-1) sqrt(E_c/k)
          +sup_w [b'w-k||w||_Sigma²]
    = (sqrt(E_c)+||b||_(Sigma^-1)/(2 sqrt(k)))².

Apply the same covariance projection and span bounds. For scalar box actions,
v_c=clip(u+g/(2 phi H² variance),lower,upper), so E_c is directly computable.
The implementation returns zero at an exact boundary optimum even when the
ordinary action gradient is nonzero. Bounds on gradient norm alone cannot do
that. This is a quadratic perturbation corollary, not a new general KKT theorem.

Only this exact-model constrained certificate and projected tabular updates are
implemented/tested. The independent-data certificate currently bounds unrestricted
deviations (a valid but possibly loose upper bound for constrained ones). General
transaction-cost states, neural constrained learning, and vector constrained
numerical experiments remain unfinished.
