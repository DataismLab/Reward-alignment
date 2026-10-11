# Covariance estimation, reward alignment and financing: research revision

7 October 2026; full-text integration updated 9 October. This report describes the substantive extension to the IAFM manuscript, not editorial changes. The incoming version is preserved in `archive/2026-10-07-before-covariance-revision/iafm/`. Earlier proposal, implementation reports and other workshop papers describe earlier stages.

## What changed in the research question

The previous historical experiment used one fixed covariance estimator: sample covariance with 10% diagonal shrinkage. It established alignment conditional on that model, but could not show whether the conclusion survived a different risk estimate. The new experiment changes covariance estimation and reward design separately. It asks three questions: how much does the risk model change the intended portfolio, how faithfully does a reward implement that portfolio, and how does the resulting strategy perform subsequently?

The stronger contribution is a quantitative separation of those questions. Exact calibration remains valid across linear shrinkage and observed-factor estimates; approximate calibration has an explicit value-error bound; and estimation experiments show why accurate reward implementation is not sufficient for investment success. This is a method for validating a financial preference and diagnosing a decision change. It is not a claim to have invented shrinkage, factor models, MVPI, or a superior investment algorithm.

## Covariance methods and common information

Six estimators now run on the same 120 lagged monthly observations:

1. Sample covariance, without shrinkage.
2. The original fixed 10% shrinkage toward the sample diagonal.
3. Ledoit–Wolf data-driven linear shrinkage toward a scaled identity.
4. Ledoit–Wolf data-driven linear shrinkage toward constant correlation.
5. An observed market-factor model with diagonal residual covariance.
6. An observed three-factor model using market excess return, SMB and HML, again with diagonal residual covariance.

The two Ledoit–Wolf intensities are computed from centred fourth moments, rather than treating the old fixed 10% penalty as data-driven shrinkage. Their ML covariance estimates are rescaled by L/(L−1) to match the sample-covariance units elsewhere in the study. Factor regressions include an intercept, use L−1 for factor covariance and L−K−1 for residual variances. These finite-sample conventions are disclosed adaptations of the primary references, not claims of exact replication of every convention in those papers.

Historical data remain Kenneth French's value-weighted 10, 30 and 49 US industry portfolios, with the archived August 2026 vintage. Factors and the risk-free series come from the same archived source. Estimation data begin in 1970; out-of-sample decisions cover January 1990–December 2025, 432 months. Means are unshrunk sample excess-return means. Risk aversion is 5, costs are 0.001 per unit L1 turnover, and historical allocations are long-only and fully invested. No new hyperparameter was selected for attractive realised results.

These are revised research portfolios, not a point-in-time investable stock universe. Changing industry classification changes investment opportunities as well as dimension. The experiment therefore does not identify a causal effect of dimension alone. DeMiguel–Garlappi–Uppal's warning about estimation error remains central: more dimensions do not by themselves make the method stronger, and 1/N and minimum variance remain meaningful controls.

For reward comparisons, all methods see the same pre-trade holdings of their estimator's reference. For covariance comparisons, alternative estimators share the original diagonal-reference state. Realised investment performance uses each method's own evolving holdings. Keeping these records separate prevents a change in estimated risk from being labelled a reward-design error.

## Main historical findings — numerically verified

All eighteen estimator/universe combinations preserve joint-calibration alignment: the largest mean Euclidean allocation distance is below 1.60e−7. Raw second-moment reward distances range from 0.00827 to 0.02249. The unconstrained scalar calibration worsens both distance and fitted regret in all twelve 30/49-industry cases. This is stronger evidence than the previous single-estimator dimension check: changing to linear shrinkage or factors does not fix the inappropriate transfer of an unconstrained calibration formula.

Covariance changes themselves can be much larger. In 49 industries, switching from fixed diagonal to the market-factor model moves the target by 0.09392 on average. Within that market-factor model, raw reward error is 0.02174 and joint error is 1.36e−7. These numbers refer to different interventions and should not be added or ranked as if they were one error.

There is no established historical investment winner among the covariance alternatives. Market-factor target MV exceeds fixed-diagonal target MV by 3.758, 1.330 and 3.887 basis-point units per month for 10, 30 and 49 industries. However, all fifteen paired 95% intervals contain zero. Simultaneous bands across these fifteen comparisons also contain zero; their common half-width is 12.8263 bp. The intervals use 1,000 paired circular twelve-month-block resamples, seed 8128, conditional on realised paths; they do not refit the entire estimation procedure.

Minimum variance has the highest realised MV among the quadratic methods in every estimator/universe case. Joint calibration remains below raw reward in realised MV in every case. The intended fitted MV objective is not the unknown population objective. Reward fidelity should therefore be reported as fidelity, not converted into an investment-superiority claim.

## A practical comparison without a supplied target

After the primary covariance results, we added a sequential exploratory comparison: initialise the MVPI auxiliary mean at the estimated mean return of current holdings, then perform exactly one portfolio update. This uses an existing MVPI step, with its risk and deterministic costs scaled together. It needs no precomputed optimal reference on its own investment path. The comparison has no tuned parameter and was run for all eighteen cases, but it is explicitly not a prespecified experiment.

This update reduces mean allocation distance by 97.8–98.6% relative to the raw reward across the eighteen cases. Under the original diagonal covariance, mean distances are 0.000141, 0.000307 and 0.000343 for 10, 30 and 49 industries, versus raw distances 0.00843, 0.01852 and 0.02079. Exact joint calibration remains the stronger fidelity certificate; the one-step result demonstrates a useful approximate implementation. Neither establishes investment superiority or a new iterative algorithm.

## New mathematical results — proved under stated assumptions

The established mean auxiliary identity extends to any convex deterministic cost g on a convex feasible set. This includes turnover, borrowing spreads and short-position fees. With F(u)=m'u−φu'Σu−g(u), M=Σ+mm', an anchor a and A=1+2φa>0, the reward Q_a(u)=m'u−(φ/A)u'Mu−g(u)/A obeys

    A Q_a(u) = F(u) − φ(m'u−a)^2 + φa^2.

If the reward solution is ε-optimal, its target-value regret is at most φ(y*−a)^2+Aε, where y*=m'u*. When Σ is positive definite, division by φ times its smallest eigenvalue also bounds squared allocation distance. A certified approximate reference bounds the unknown y*, making the bound computable without an exact optimum. The value bound survives singular covariance; uniqueness and the Euclidean distance bound need not.

A second sensitivity bound holds when only covariance changes. For E=Σ1−Σ0, reference covariance Σ0 positive definite, and the alternative target u1, target displacement is at most ||Eu1||/λmin(Σ0), and reference-objective loss is at most φ||Eu1||²/λmin(Σ0). A first-order optimisation certificate adds a numerical allowance. This compares two fitted models, not either model with the unobserved true historical covariance.

These are useful corollaries and sensitivity arguments, not asserted first discoveries of the auxiliary identity or strong-concavity bounds. Proofs appear in the manuscript and `notes/FINITE_CALIBRATION_AND_ESTIMATION.md`. The previously proved fixed-horizon leading scalar-mismatch coefficient remains the project's specific theoretical increment; exhaustive priority is not certified.

## Factor-model stress test — numerically verified

We generated 360 matched synthetic markets: 30 seeds, three dimensions (10, 49, 100), two estimation lengths (60, 120), and two residual-covariance designs. Applying six estimators gives 2,160 fitted problems. Known population means isolate covariance estimation error. Known population covariance supplies a separate population-optimal constrained portfolio. Cases with N>L deliberately test singular sample covariance without using an invalid inverse-based scalar rule.

At N=100 and L=120 with independent residuals, the three-factor estimator lowers population MV regret from the sample estimator's 1.40 to 1.11 bp. The paired difference is −0.291 bp with a 30-seed t interval [−0.459, −0.124]. With correlated residuals, the same factor estimator gives 1.33 versus 1.29 bp; the paired difference is +0.044 bp with interval [−0.131, 0.219]. These are descriptive matched-seed intervals, not a multiple-comparison selection claim.

The market-only estimator misses two true factors in this simulation and has substantially greater population regret (5.66/6.45 bp in these two designs). Yet joint reward calibration still matches its fitted target. Maximum absolute joint fitted regret across all 2,160 problems is below 1e−12. A factor model can help when its structure is appropriate; precise reward alignment cannot compensate for omitted risks or false residual assumptions.

## Habibnia–Soltanzadeh and financing

We read the actual 2024 arXiv paper, including Eq. (8), Table 2 and the experiment tables. Their framework uses SAC, CNN/multi-head attention, crypto perpetual instruments, shorts and lending. Our comparator is explicitly a restriction: long-only weights, unit deployed capital, assetwise monthly PnL, the reported loss penalty 25, and its cost multiplier 25/5. Penalties 1 and 5 are recorded sensitivity checks. This is not a reproduction of their SAC architecture or reported crypto returns.

Under that restriction, positive/negative assetwise PnL is linear in long-only weights and depends only on marginal return distributions. A three-asset counterexample proves it cannot distinguish covariance-sensitive diversification: equal symmetric marginals give the same reward scores with independence or with correlation 1/2 between assets 1 and 2, whereas the MV targets are respectively (1/3,1/3,1/3) and (2/7,2/7,3/7). This claim does not apply to an unrestricted dynamic agent or a portfolio-level downside reward. It explains a difference in preferences, not failure at the original authors' stated goal.

A separate controlled financing experiment permits shorting, borrowing and cash. Across fifty six-asset states, scaling all deterministic costs gives mean allocation discrepancy 1.51e−7; scaling turnover alone while leaving financing penalties unchanged gives 0.00997. Thirty-seven target portfolios borrow and all fifty short, so the relevant terms are active. This validates the general cost identity in an expanded feasible set; it is not real-data crypto evidence.

## Literature and IAFM Section 7

The paper now cites 24 references; the complete project ledger has 33 records. New sources include both original Ledoit–Wolf linear-shrinkage papers, Fan–Fan–Lv on observed-factor covariance, Kolm–Ritter's 2025 JPM overview, and Habibnia–Soltanzadeh's 2024 framework. Kolm–Ritter's 2019 reward formulation is also explicitly cited in the updated comparison. Earlier Journal of Finance and Review of Financial Studies references remain: Markowitz, DeMiguel–Garlappi–Uppal, Gârleanu–Pedersen, DeMiguel–Martín-Utrera–Uppal and nonlinear shrinkage.

**Update, 9 October:** the user supplied the complete 15-page Kolm–Ritter JPM article. All pages, three exhibits and references have now been read. The introduction, related work and Section 7 use its actual discussion of reward design and mandate alignment (pp. 90–91), workflow (Exhibit 2, p. 84), known-policy comparisons (p. 87), inverse RL (p. 88), scalability (pp. 88/90) and forecasts versus decisions (p. 91). It is an equation-free overview with no new empirical strategy, so no numerical benchmark row was invented. The earlier abstract-only access limitation is resolved. The separately read CFA chapter remains a different source. See `notes/KOLM_RITTER_2025_FULLTEXT_REVIEW.md` for the complete reading and comparison record.

Section 7 now explains model changes using three distinct interventions: change the covariance model, change the reward's financial preference, or change numerical accuracy. It uses the covariance displacement bound, financing experiment, approximate-anchor budget and downside counterexample as concrete mechanisms. This fits IAFM's financial-semantic explanations, faithful evaluation, robustness and model-validation topics. We do not claim a human interpretability study, neural representation analysis or a causal explanation of market returns. Workshop topics and the eight-page format are based on the archived official call already collected; current submission availability has not been reconfirmed.

## Verification and reproducibility

- All 50 unit tests pass, including fifteen added covariance/financing tests.
- All 58,320 saved historical decision records were reconstructed from archived returns and saved weights. This count includes 7,776 one-step records. Accounting, chronology, common/own states, identities and covariance/anchor bounds pass.
- All 2,160 synthetic fitted problems were independently regenerated and checked, including their known-covariance objectives; all fifty financing identities pass.
- The 144 January anchor checks use zero and previous-holdings anchors in the 49-industry identity-shrinkage and three-factor cases. Bounds hold but can be loose.
- Identity shrinkage is checked against scikit-learn, and constant-correlation intensity against a separate elementwise fourth-moment calculation. Numerical optimisers have independent first-order LP certificates in original objective units.
- The environment is recorded in `results/environment-covariance-20261007.txt`. Raw data and literature download hashes, saved-result hashes, protocols and verification outputs are retained. Initial Gaussian-score warnings were independently checked against a Cholesky calculation; the runner now uses Cholesky directly. They did not affect portfolio optimisation.

Primary code additions are `mvrl/covariance.py`, `mvrl/financing.py`, the covariance/simulation/financing runners, their verifiers, and the table/figure generator. Existing historical and synthetic results are preserved. New historical outputs are in `results/historical/covariance/`; controlled results are in `results/covariance_simulation/`.

To reproduce in a Python environment with the project requirements and development requirements installed, run from the project root with `PYTHONPATH=.` and single-threaded BLAS:

```sh
python -m pytest -q
python scripts/run_covariance_audit.py --assets 10
python scripts/run_covariance_audit.py --assets 30
python scripts/run_covariance_audit.py --assets 49
python scripts/run_covariance_simulation.py
python scripts/run_financing_audit.py
python scripts/verify_covariance_audit.py
python scripts/verify_covariance_simulation.py
python scripts/summarise_covariance_audit.py
python scripts/make_covariance_outputs.py
```

Runners preserve completed result files. For a fresh rerun, copy the project and move those cached result files aside in that copy. `add_one_step_covariance.py` exists to extend pre-one-step caches without recomputing old decisions; the main runner now includes that comparator directly. Compile the current `submissions/iafm/paper.tex` with its supplied class, bibliography, table inputs and figure assets. Do not use legacy manuscript generators: they describe earlier versions.

## Status and remaining scope

**Proved:** scoped terminal mismatch result retained; deterministic-cost calibration identity; approximate-anchor and fitted-covariance sensitivity bounds; restricted assetwise-downside counterexample.

**Numerically verified:** eighteen historical covariance/universe cases, all reported fidelity metrics, one-step reductions, simulation comparisons, financing example, saved-action reconstruction and formula tests. Historical investment rankings are sample results, not population theorems.

**Preliminary:** practical significance of one-step calibration beyond these fixed settings; generality of the known-factor simulation; real-world model-validation usefulness without a user study. Priority for a new general algorithm is neither claimed nor established.

**Open:** predictive end-to-end neural RL replication, point-in-time investable instruments, true dependent-return terminal-equilibrium identification, unrestricted DSR, factor selection/nonlinear shrinkage, parameter-selection uncertainty and exhaustive novelty review. These extensions are not hidden inside a claim that the research proves universal superiority. The present revision completes the specified covariance/factor/financing audit and provides a defensible, reproducible paper about reward alignment.

## Complete covariance comparison

The table below is generated from the saved results. Distances are within each estimator; realised monthly MV uses separate own-state paths. “One step” is the exploratory existing-MVPI update. Numerical units are allocation-weight Euclidean distance and basis-point units of the monthly MV score.

| N | Estimator | Raw distance | Scalar distance | One step | Joint | Target MV (bp) | Minimum-variance MV (bp) |
|---|---|---|---|---|---|---|---|
| 10 | diag10 | 0.00843 | 0.00540 | 0.000141 | 1.40e-08 | -8.497 | 5.274 |
| 10 | ff3 | 0.00873 | 0.00653 | 0.000193 | 2.84e-09 | -8.532 | 3.758 |
| 10 | lw_correlation | 0.01034 | 0.00637 | 0.000196 | 1.28e-08 | -11.917 | 2.684 |
| 10 | lw_identity | 0.00838 | 0.00545 | 0.000138 | 8.50e-09 | -8.442 | 5.513 |
| 10 | market | 0.00827 | 0.00809 | 0.000171 | 7.15e-09 | -4.738 | 4.783 |
| 10 | sample | 0.00874 | 0.00642 | 0.000174 | 1.24e-08 | -10.114 | 4.600 |
| 30 | diag10 | 0.01852 | 0.02183 | 0.000307 | 6.87e-08 | -26.096 | -0.416 |
| 30 | ff3 | 0.01921 | 0.03129 | 0.000287 | 7.02e-08 | -28.840 | -0.012 |
| 30 | lw_correlation | 0.01889 | 0.02717 | 0.000362 | 5.78e-08 | -26.613 | -3.158 |
| 30 | lw_identity | 0.01789 | 0.02273 | 0.000276 | 9.23e-08 | -25.583 | -0.025 |
| 30 | market | 0.01782 | 0.04360 | 0.000320 | 7.93e-08 | -24.766 | 3.947 |
| 30 | sample | 0.01967 | 0.04343 | 0.000323 | 5.52e-08 | -26.902 | -3.284 |
| 49 | diag10 | 0.02079 | 0.05354 | 0.000343 | 1.57e-07 | -30.567 | -4.808 |
| 49 | ff3 | 0.02249 | 0.06158 | 0.000322 | 1.19e-07 | -31.047 | -3.013 |
| 49 | lw_correlation | 0.02232 | 0.06635 | 0.000409 | 1.40e-07 | -32.948 | -5.934 |
| 49 | lw_identity | 0.02007 | 0.05244 | 0.000305 | 1.48e-07 | -29.570 | -4.062 |
| 49 | market | 0.02174 | 0.08354 | 0.000367 | 1.36e-07 | -26.680 | 0.190 |
| 49 | sample | 0.02205 | 0.11244 | 0.000414 | 1.59e-07 | -30.077 | -6.492 |
