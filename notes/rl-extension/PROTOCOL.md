# RL extension protocol — 9 October 2026

Recorded before running the new experiments. Existing IAFM manuscript and financial
results are frozen while this extension is investigated.

## Research question and priority boundary

Can we audit a learned terminal mean–variance equilibrium without knowing its policy,
and distinguish a misspecified reward from an inaccurate continuation critic and an
unfinished actor update? Candidate contribution: a posteriori, constant-shift-invariant
one-step deviation bounds, with a separate independent-data uncertainty allowance.
This is a candidate theoretical contribution, not an established priority claim.

SPERL/BPI already learns time-inconsistent equilibria (Lesmana–Pun, 2021 preprint /
2025 SIAM publication). Guo–Huang–Yu (2026 arXiv:2606.11798) already uses auxiliary
functions and modified rewards in deterministic actor–critic learning. Sangadi et al.
(arXiv:2406.07892v2, 2025) already gives finite-sample actor–critic analysis for a
discounted return mean–variance objective. Do not claim any of those ideas as new.
Paired-sample variance estimators and span contraction are also established tools.

## Stage A: falsifiable controlled study

Use the existing dependent-return, two-regime market. No true transition probabilities,
means, variances, equilibrium action, or exact continuation value are given to training.
The learner receives independent conditional return/next-regime samples from a
generative simulator; this is stronger access than a single historical trajectory.
Known structure: exogenous regimes, linear self-financing dynamics, deterministic
riskless rate, terminal mean–variance preference and wealth-independent actions.
Closed-form moments and equilibrium are used ONLY by the evaluator.

Methods: zero-action control; sample-based myopic variance calibration; sample-based
backward equilibrium learning with a continuation-mean critic and paired quadratic
actor reward; plug-in backward best-response control with the same data; exact
equilibrium as reference. The backward learner is an adaptation of existing SPERL
principles, not a full reproduction of the published general algorithm. Evaluate
unfinished actor updates and deliberately misspecified critics separately. A later
shared neural actor experiment must be labelled separately from the tabular study.

Primary grid: persistence {0.5,0.8,0.95}, horizon {4,12,24}, phi=1,
conditional samples per time/state {128,512,2048,8192}, seeds 0–19.
Raw transition count is T*K*n; paired construction uses n/2 independent pairs.
All compared learners receive identical samples. No seed deletion or tuning on
evaluation equilibrium distances. Report each seed plus mean, median and paired
uncertainty. Primary metrics: maximum one-step deviation gain over time/regimes;
policy distance under reference regime occupancy; initial terminal MV (secondary).
An equilibrium need not maximise precommitment value, so higher initial MV alone
is not a success criterion. Record terminal mean and variance as well.

Theory tests: independent direct terminal moment deviations; random policies and
critics; exact equilibrium; critic constant shifts; iid and dependent branches;
terminal boundary errors; finite-sample support and audit/training separation.
Use true-model residuals to test the deterministic theorem, explicitly distinguish
them from observable sample bounds. Independent-data certificates must never use
true model variance/transition probability under an empirical label.

## Stage B and remaining scope

Neural pilot fixed before viewing neural results: same 9 markets, n=2048 per
time/state, seeds 0–4, budgets 250/1000/3000 joint updates. Actor and critic each
two 32-unit tanh hidden layers, inputs normalised time and regime one-hot;
Adam learning rate .003, target-critic averaging .02, batch64 per time/state.
Compare paired reward with ordinary mean critic, paired reward with state-centred
critic/TD targets, and myopic reward with the same ordinary critic architecture.
All use identical frozen samples and matched initial network weights. No oracle
initialisation, label or validation stopping. State centring removes only a
time-dependent constant and is motivated by the span proof. This is a pilot,
not sufficient evidence for broad neural-RL superiority. Sample-based approximate
curvature normalises actor updates; all methods use the same normalisation.
Observe all excess returns: actions do not affect exogenous markets, so policy
exploration is not required for conditional sample identification in this benchmark.

Investigate shared neural actor/critic, representation error and optimisation budgets,
then meaningful PPO/other published baselines under their actual objectives. A
PPO wrapper by itself is not novelty. Genuine real-data sequential RL requires a
separate frozen chronological train/validation/test protocol. Historical observations
do not certify a true-market equilibrium; do not transfer simulator coverage claims.
Do not rewrite the submission as if these stages had already succeeded.

## Decision rules

Report failures and loose/non-informative certificates. Revise the candidate if prior
art covers it. Keep the strongest reproducible evidence, not the most favourable
backtest. Preserve source/version/reading coverage in a companion literature table.
