# How the research changed: from covariance estimation to RL certification

Prepared 9 October 2026. This report compares the project immediately before the covariance-estimator extension, the completed covariance/financing version, and the final IAFM paper. It describes substantive research changes rather than table formatting or editorial adjustments.

## 1. Did the idea and contribution pivot?

**Yes: the headline contribution pivoted, but the underlying research problem did not.** Throughout the project, the question has been whether the decisions produced by a financial reward agree with a specified financial objective. What changed is the object we can inspect and the information our main result requires.

The earlier paper primarily asked: **“Given an intended policy that we can calculate, which policy does this reward produce, and can we calibrate the reward to match the intended policy?”** The covariance extension then asked whether that conclusion survived changing the estimated risk model, portfolio dimension and financing costs.

The final paper asks a further question: **“Given a trained RL policy and its continuation critic, can we bound how much an investor could improve the intended objective by changing one decision, without first calculating the equilibrium policy?”** That is the new centre of the paper. It brings the analysis from reward specifications and exact optimisation to imperfectly learned agents.

This is a substantive extension, not merely a new title. It is also a repositioning: the exact reward-mismatch result and calibration constructions are now supporting theory; the residual-based financial decision certificate is the principal result. The covariance research remains important evidence that correct implementation and correct market estimation are different problems.

| Aspect | Before the covariance extension | After covariance/financing work | Final RL paper |
|---|---|---|---|
| Main question | Does a reward implement a known financial target? | Does alignment survive different risk estimates and costs? | Can a learned policy's financial decision error be bounded without the equilibrium policy? |
| Principal object | Reward optimum versus reference optimum | Fitted portfolios under six covariance models | Learned actor, continuation critic and one-step deviations |
| Main source of evidence | Exact benchmark and historical fitted allocation | Factorial historical audit and controlled estimation/financing experiments | New theorem, tabular learning, shared neural learning, PPO intervention and independent-data audit |
| Target information | Usually a solved reference for measuring alignment | A fitted reference under each estimator; approximate-anchor alternatives | No equilibrium policy needed for the certificate; moments or suitable independent audit data are still needed |
| Defensible benefit | Identify and correct reward-induced preference changes | Separate estimated-risk changes from reward changes | Quantify remaining financial decision error after learning |
| Claim not established | General investment superiority | A universally best covariance estimator | General deep-RL convergence or superior real-data trading performance |

**The research has not become a project about inventing a covariance estimator. It has also not become a project about beating every recent portfolio-RL paper on returns.** Its consistent subject is financial objective alignment, with a more concrete RL validation result now at the centre.

## 2. Exactly where we started

At the starting point of this comparison, the historical study already included **10, 30 and 49 US industry portfolios**. The dimension extension and the DeMiguel–Garlappi–Uppal discussion therefore predate the covariance-estimator work; they should not be counted as new contributions of the final RL revision.

The project already had a controlled terminal mean–variance benchmark, a result showing that optimal scalar tuning cannot generally eliminate the mismatch of a particular quadratic wealth-increment reward, and constrained one-period calibration with turnover costs. It also had historical comparisons of adapted published reward formulations. The historical risk model was sample covariance with **fixed 10% shrinkage toward the diagonal**.

The important limitation was that a conclusion about alignment was conditional on that one covariance construction. The earlier learning diagnostic also did not establish a shared sequential RL agent: statewise neural optimisation and a predictive multiperiod policy are different experiments. In the dependent-return construction, the correction relied on a supplied continuation quantity. These were the reasons to extend the finance side first and then the RL side.

The preserved starting manuscript is `archive/2026-10-07-before-covariance-revision/iafm/paper.tex`. The complete finance version immediately before the RL rewrite is `archive/2026-10-09-before-final-rl/iafm/paper.tex`. Both used the title **When Portfolio Rewards Miss the Target: Exact Mismatch and Policy Alignment**. The final title is **Certifying Reward Alignment in Portfolio Reinforcement Learning**.

## 3. What the covariance-estimator extension added

### Six risk models under the same information

We expanded the historical experiment from one covariance estimator to six. A covariance matrix describes individual asset variances and how assets move together; changing it can change the desired portfolio even if the investor's objective remains identical.

| Estimator | What it does | Why it was included |
|---|---|---|
| Sample covariance | Estimates covariance directly from the lagged returns | Unregularised reference |
| Fixed diagonal shrinkage | Mixes sample covariance with its diagonal using the original fixed 10% weight | Preserves the previous benchmark |
| Ledoit–Wolf identity shrinkage | Uses a data-dependent intensity to shrink toward a scaled identity matrix | Tests established linear regularisation rather than a fixed coefficient |
| Ledoit–Wolf constant-correlation shrinkage | Shrinks toward a matrix with common correlation and individual variances | Tests another financially interpretable linear target |
| Market-factor covariance | Fits observed market exposure plus diagonal residual risk | Tests covariance built from an economic factor model |
| Three-factor covariance | Fits market, SMB and HML exposures plus diagonal residual risk | Tests a richer observed-factor model |

The two Ledoit–Wolf intensities are estimated from the data. They are not simply different names for the original fixed 10% shrinkage. The factor models use regressions with intercepts and disclosed finite-sample variance conventions. Their diagonal residual covariance is an assumption, not a fact guaranteed by historical data. Nonlinear shrinkage was discussed as literature, but was **not implemented**.

All six methods use the same 120 lagged monthly observations, unshrunk sample excess-return means, risk-aversion coefficient 5, long-only/full-investment constraints and L1 turnover-cost coefficient 0.001. Six models across three industry universes produce **18 configurations**. Historical evaluation still covers **432 months, January 1990–December 2025**, using the archived August 2026 Kenneth French data vintage.

These are revised research-portfolio returns. This extension did not introduce point-in-time investable funds, individual-stock trading, new transaction data or a new historical dataset.

### Three questions are now tested separately

1. **Changing estimated opportunities:** how much does the intended portfolio move when covariance changes?
2. **Changing the implemented preference:** under the same estimated moments, holdings and constraints, how far does a reward move the decision from its intended target?
3. **Subsequent investment performance:** how does each strategy perform along its own evolving holdings path?

The first two use controlled common states. The third uses each method's actual simulated portfolio path. Without this separation, an estimator change or a different previous portfolio could be mislabelled as a reward error.

**Numerically verified finding:** joint calibration preserves its own fitted target across all 18 configurations, with mean allocation distance below **1.60 × 10⁻⁷**. Raw reward distances range from **0.00827 to 0.02249**. The unconstrained scalar correction worsens distance and fitted regret in **all 12 larger-universe configurations** with 30 or 49 industries.

For a concrete example, in the 49-industry market-factor case, changing the covariance model moves the fitted target by **0.09392** on average. Within that model, raw reward discrepancy is **0.02174**, while joint-calibration discrepancy is about **1.36 × 10⁻⁷**. These are different interventions, not three additive components of one measured error.

This supported a stronger finance-side conclusion: reward alignment survives several materially different risk models, and replacing the estimator does not by itself repair a misapplied reward formula.

## 4. What DeMiguel–Garlappi–Uppal changed in our interpretation

Their diversification study compares estimated optimal allocation rules with equal weights and shows how estimation error can offset theoretical diversification benefits. It does not say that a portfolio experiment becomes credible only above a particular asset count. Its long estimation-window illustrations depend on the model and investment opportunities.

We used that lesson constructively in three ways: retained simple allocation controls, examined multiple portfolio dimensions, and then introduced shrinkage/factor models to study estimation directly. The covariance extension makes the third part much more concrete.

With a 120-month estimation window, the asset-to-observation ratio increases from **0.083** for 10 industries to **0.250** for 30 and **0.408** for 49. The number of mean and unique covariance entries rises from **65** to **495** and **1,274**. These are estimated entries, not independent observations or necessarily independent free parameters in a factor model.

Higher dimension therefore makes estimation more demanding. It does not invalidate the joint-calibration identity: that identity is conditional on the fitted inputs. Also, 10/30/49 industry classifications change the investment opportunity set, so their comparison does not isolate asset count as the sole causal factor.

The resulting distinction is central to both versions: **a method can faithfully implement an estimated mandate even when the estimates lead to disappointing realised investments.** We do not use DeMiguel and colleagues as an excuse to ignore performance. We use their evidence to avoid confusing estimation risk with implementation error.

## 5. What the factor-model simulations taught us

Historical covariance is unknown, so historical data alone cannot reveal which covariance estimate is closest to the true matrix. We added simulations with known population covariance to address that question separately.

There are **360 matched synthetic market instances**: 30 seeds × three dimensions (10, 49, 100) × two window lengths (60, 120) × two residual-covariance designs. Applying six estimators gives **2,160 fitted problems**. Known population means isolate covariance-estimation effects. Cases with more assets than observations deliberately include singular sample covariance.

At 100 assets and 120 observations:

| Residual structure | Sample-covariance population MV regret | Three-factor population MV regret | Interpretation |
|---|---:|---:|---|
| Independent residuals | 1.40 bp | 1.11 bp | Factor structure helps when its residual assumption fits |
| Correlated residuals | 1.29 bp | 1.33 bp | No demonstrated factor advantage under this misspecification |

The paired difference in the first case is −0.291 bp, with a descriptive 30-seed interval [−0.459, −0.124]. In the second it is +0.044 bp, with interval [−0.131, 0.219]. These are not selected-method, multiple-comparison-adjusted superiority claims.

The market-only model omits two true factors in this simulation and has substantially larger population regret. Yet joint reward calibration still matches that model's fitted target. That is useful evidence about the mechanism: a reward correction can preserve a decision rule without correcting omitted risk factors.

**The 100-asset result is a covariance/optimisation simulation. It is not a 100-asset neural RL experiment.** The later RL experiment uses one risky asset and two observed regimes. Those dimensions must not be merged in a description of our achievement.

## 6. Costs, approximate calibration and the Habibnia comparison

### Joint scaling of risk and costs

The financial objective is fitted expected return minus a variance penalty and deterministic costs. Through the established mean auxiliary used in MVPI, we can construct a quadratic reward with the same maximiser when the anchor is correct. The covariance revision generalised the deterministic cost term to include turnover, borrowing spreads and short-position fees.

The practical point is that calibrating risk while leaving another cost coefficient unchanged can alter the investor's trade-off. Scaling all relevant deterministic costs together preserves the intended objective under the stated identity. This is a sufficient construction; we corrected wording that could have implied it was universally necessary in every special case.

A controlled financing test used **50 six-asset states**. All targets shorted and 37 borrowed, so the extra charges were active. Full joint scaling gives mean discrepancy **1.51 × 10⁻⁷**. Scaling turnover while leaving financing charges unchanged gives **0.00997**. This is controlled financing evidence, not a crypto backtest.

### Moving beyond an exact supplied anchor

Exact calibration can look circular when its anchor is calculated from the already-solved desired portfolio. We therefore added an approximate-anchor bound. In words:

> Loss in the fitted financial objective is bounded by a squared mean-anchor error plus the remaining optimisation error, with the latter scaled by the calibration factor.

Positive-definite covariance converts this value bound into an allocation-distance bound. These are proved consequences of the auxiliary identity and strong concavity; the underlying identity and general optimisation arguments are prior methods.

We also tested **one existing MVPI update**, starting from the estimated mean return of current holdings. It does not require supplying the optimal portfolio to that update. Across all 18 historical configurations, this reduces mean allocation distance by **97.8–98.6%** relative to raw reward. It was a sequential exploratory addition, and we credit it as an MVPI adaptation rather than inventing a new algorithm name.

### What we actually did with Habibnia–Soltanzadeh

We inspected their 2024 primary paper, including the asymmetric PnL reward, and adapted that reward to the common long-only, unit-capital historical setting. We did not reproduce their SAC architecture, attention/CNN components, crypto perpetual market, shorting/lending environment or reported returns.

A restricted assetwise positive/negative PnL score depends on marginal returns and can be insensitive to cross-asset dependence. Our three-asset counterexample makes this explicit: identical marginals produce identical reward scores under two dependence structures, but the MV-optimal weights change from (1/3, 1/3, 1/3) to (2/7, 2/7, 3/7). This is a proved statement about that restriction. It does not establish that their complete agent is defective or that downside preferences should be replaced by MV.

## 7. Why the newer literature changed the novelty story

The literature made the argument more precise and ruled out several overbroad claims.

The user-supplied Kolm–Ritter 2025 journal article was read in full: all 15 pages, exhibits and references. It already identifies mandate-aligned reward design as important and discusses validation against known policies. It is a conceptual overview rather than a new empirical strategy, so there is no legitimate “our returns versus Kolm–Ritter 2025 returns” comparison to invent. Its contribution to our work is motivation and positioning.

The recent RL readings showed that equilibrium RL, backward policy iteration, modified rewards, auxiliary critics and finite-sample mean–variance actor–critic analysis already exist. Critic centring and seminorm geometry also have precedents. Consequently, neither “we used actor–critic for mean–variance” nor “we learned an auxiliary reward” is a defensible standalone novelty claim.

The narrower contribution is the connection between observable or model-based learning residuals and the financial gain from a one-step deviation of a given policy. That is the result the final paper derives and tests. A targeted literature search does not prove publication priority. We do not claim that nobody has previously derived any related bound.

Reading coverage is not uniform: Kolm–Ritter 2025 was fully read; other RL papers received targeted primary-text readings of relevant algorithms, theorem statements and experiments. For Lesmana–Pun, we read the 2021 preprint for algorithm details and verified the 2025 journal metadata; the final journal full text was not obtained. The paper explicitly respects that distinction.

## 8. The substantive RL extension

### Why returns that depend on regimes matter

With dependent returns, today's action can be correlated with tomorrow's investment opportunities. A reward that treats each period in isolation can miss the resulting continuation hedge. More training on that myopic reward does not automatically recover the intended terminal equilibrium.

The earlier dependent-return correction supplied an analytical continuation quantity. The new implementation learns a continuation critic from conditional return/successor-state samples. It then uses paired samples to estimate both immediate variance and covariance with future opportunities. The training modules do not receive the exact equilibrium policy.

The controlled market has one risky asset, two observed regimes, three transition-persistence settings and horizons of 4, 12 and 24. It provides conditional samples at every time/state. This is a stronger data-access assumption than learning from one historical time series. The simulator is a controlled test, not a regime model fitted to the French industries.

### What the certificate says

For a fixed policy, consider replacing its action at one date and state while following its existing future policy afterwards. The maximum improvement in conditional terminal mean–variance is the **one-step deviation gain**. A small gain everywhere means an approximate equilibrium in this stated sense. It is not the same as small regret against a globally optimal precommitment policy.

The theorem bounds the square root of that gain using an action-gradient term and a continuation-critic term. If the learner follows a different reward gradient, a triangle inequality separates actor, reward and critic contributions. These are conservative error allowances, not an exact additive decomposition of returns or a unique causal attribution of every failure.

The critic term uses the range of its Bellman residual across states, propagated backwards through the transition dynamics. A time-specific constant added to every state's critic value changes absolute values but not the relevant covariance. The certificate correctly ignores such offsets. With convex action constraints, feasible critic-objective improvement replaces an unconstrained gradient norm, so a valid boundary optimum is not incorrectly penalised.

**Status: proved within the stated market and policy assumptions.** The theorem extends to vector returns with positive-definite covariance; the numerical learner/auditor is scalar. No equilibrium policy is required to compute the bound. The exact-model version still requires conditional moments. A separate independent-data version requires suitable samples and known support bounds. “No target-policy oracle” therefore does not mean “no assumptions, model information or data requirements.”

### Two diagnostics we could not provide before

A constructed case has zero critic-based action gradients but actual maximum deviation gain **0.10263**. Its bound is **0.89674**, correctly refusing to certify a small error. This demonstrates why actor convergence alone can be misleading; it is not evidence that a named published algorithm usually fails.

Conversely, adding large state-constant critic offsets changes the certificate by less than **1.7 × 10⁻¹⁵** in the saved checks. Absolute critic error could change substantially without changing the policy-relevant hedge. This explains why the geometry of critic error matters.

## 9. What the new learning experiments actually show

### Tabular experiment

The tabular grid contains **2,160 records**: nine markets, four conditional-sample budgets, twenty seeds and three methods. At 8,192 samples per time/state, continuation-aware mean policy distance is about **0.1649**, compared with **0.5871** for myopic reward. Corresponding maximum deviation gains are **0.000273** and **0.003319**.

A control solves the same sampled actor objective exactly. Its distance differs from forty iterative actor steps by at most approximately **5.24 × 10⁻⁵**. This helps distinguish sampling/reward effects from an unfinished numerical optimiser.

### Shared neural actor–critic

The final neural study has **540 training runs**, producing **1,620 checkpoint records**. There are twenty seeds, nine markets and three reward/critic variants, evaluated after 250, 1,000 and 3,000 updates. The final comparison uses every run at the fixed final budget. It does not select the best checkpoint using the oracle benchmark.

| Final neural variant | Policy distance | Maximum deviation gain | Mean model-based certificate |
|---|---:|---:|---:|
| Myopic reward | 0.610183 | 0.00319845 | 0.00642326 |
| Continuation, ordinary critic | 0.250692 | 0.00060636 | 0.00222929 |
| Continuation, centred critic | 0.249259 | 0.00059405 | 0.00162536 |

The centred continuation method improves distance by **59.2%** and deviation gain by **81.4%** relative to the matched myopic network. The paired distance difference is −0.360924, with 95% seed-bootstrap interval [−0.389878, −0.328846]. Markets are averaged within each seed before bootstrapping.

Most of this improvement comes from including continuation. Centring adds only **0.57%** distance improvement beyond the ordinary continuation critic, while reducing the mean certificate by **27.1%**. Its initial-value difference interval includes zero. We should not describe centring as a dramatic new investment algorithm.

The earlier five-seed pilot reported 61.0% and 81.6%. Those are preserved pilot results; the final twenty-seed values replace them in the submission.

### Genuine PPO comparison

We then added a standard clipped PPO optimiser through Stable-Baselines3, with two reward arms. Both have the same data access, sample-only continuation evaluation, rollout refresh schedule, network specification and training budget. The reward differs by whether it includes continuation covariance.

The comparison has **40 runs**: two markets × ten seeds × two arms, with **32,768 environment steps per run**. Actions are bounded in [−3, 3], and the reference policies are verified to lie inside those bounds.

| PPO reward | Policy distance | Maximum feasible deviation gain |
|---|---:|---:|
| Myopic | 1.728010 | 0.02349156 |
| Continuation-aware | 1.152519 | 0.01180378 |

Distance improves by **33.3%** and deviation gain by **49.8%**. The paired distance difference is −0.575491, with interval [−0.739003, −0.403600]. This supports the reward intervention inside a familiar policy optimiser.

This is neither a full replication of a recent financial RL paper nor a fair speed ranking against the separate direct-gradient neural experiment: their compute budgets and training mechanisms differ. We also did not reproduce the full SPERL or DPG-FPI algorithms and claim to beat them. They are theoretical/algorithmic comparison points in the literature, not falsely labelled benchmark rows.

## 10. The independent-data audit: a new capability with a real cost

The exact-model certificate is useful in a controlled environment, but a practical audit cannot assume that true conditional moments are automatically available. We therefore added a version using independent observations, confidence bounds on the required quantities, and a policy/critic fixed before auditing.

Twenty saved policies were tested with **32,768 observations per time/state**, totalling **786,432 audit observations per policy**.

| Quantity, averaged over the twenty policies | Value |
|---|---:|
| Actual maximum deviation gain | 0.000902 |
| Exact-model certificate | 0.001257 |
| Independent-data Hoeffding bound | 0.036141 |
| Independent-data Bernstein bound with mixing allowance | 0.004911 |

The refinements make the certificate much less conservative, but they do not eliminate its statistical cost. The Bernstein/mixing extension followed inspection of the first bounds and is reported accordingly. Each construction has a 95% simultaneous-over-states guarantee for a fixed policy under its assumptions; there is no blanket 95% guarantee covering all policies and all tried constructions together.

All twenty saved policies were covered numerically. The guarantee comes from the proof, not from this observed coverage. If a positive variance lower bound cannot be established, the audit can return an infinite bound. It must not silently return a reassuring small number when data are insufficient.

This is not yet a certified audit of a single dependent historical return series, nor does it permit repeatedly selecting policies on the audit data without further analysis.

## 11. What happened to the real-data findings?

They were retained, not replaced by better-looking synthetic results. The final RL phase did not rerun historical finance results with tuned parameters to improve their ranking. The recorded preservation check covers 31 pre-extension files; only the intentionally rewritten canonical IAFM source/PDF changed among those tracked files.

The historical conclusions are still mixed in an economically meaningful way. Joint calibration closely matches the fitted target, but its realised MV is below raw reward in all eighteen configurations. Minimum variance has the highest realised MV among the quadratic comparators in those configurations. All fifteen covariance-target comparisons against fixed diagonal have paired 95% intervals containing zero; simultaneous bands also contain zero.

That means we have evidence of **better fidelity to the specified fitted objective**, not demonstrated superior investment performance. A different reward can accidentally produce a better realised portfolio because the fitted target is estimated imperfectly. It is still important to disclose that outcome, rather than redefine the objective after observing it.

The final study consequently has two distinct empirical arms:

- **Historical finance:** multiple assets, real monthly returns, estimated moments, costs, constrained allocation and covariance/reward comparisons.
- **Controlled RL:** observed regimes, sampled dependent returns, learned policies, known evaluation benchmark and residual certification.

They support complementary parts of the argument. They do not combine into evidence that the new neural/PPO policy has traded the French portfolios successfully. **No new chronological real-data RL backtest was completed.**

## 12. What remained, what was compressed, and what left the eight-page paper

The eight-page limit required changing the allocation of space. Research preserved in the project is broader than the material printed in the final paper.

| Earlier material | Treatment in the final paper |
|---|---|
| Exact leading scalar reward-mismatch result | Retained in Section 3; derivation in Appendix B |
| Independent-return reference-preserving reward | Retained in Section 3 |
| Joint risk/cost identity and approximate-anchor bound | Retained in Section 3 |
| Six covariance models and 10/30/49-industry protocol | Retained in the historical protocol/results |
| Published reward-formulation comparisons | Retained in the historical table, with adaptation scope disclosed |
| Full eighteen-case covariance table | Preserved in research report/results; not reproduced in full in the final paper |
| Covariance sensitivity bound and detailed derivation | Preserved in the technical note and finance archive; no longer a displayed theorem in the final paper |
| Three-asset restricted PnL counterexample | Preserved in the technical note; final paper summarises the marginal-payoff issue rather than printing its full construction |
| Known-covariance and financing simulations | Summarised in final results; full outputs and details remain in the project |
| Old theory and covariance-simulation figures | Replaced by neural learning and independent-audit evidence |
| Covariance-comparison figure | Retained, with clearer layout |
| Previous statewise learning diagnostic | Superseded in the main story by actual shared neural and PPO experiments; earlier research remains archived |
| New residual certificate | Main Section 4, including proof and convex-action extension |
| New statistical certificate | Explained in the main text and Appendix A |

The bibliography grows from 24 cited references in the finance version to **29** in the final paper. The project ledger grows from 33 records to **39**. The difference is intentional: the ledger records more inspected literature than the paper can use directly. Six RL/learning references were added to the final citation set, while the earlier Chaouki reference is no longer cited there. It remains in the project literature record.

## 13. How Section 7 and the workshop fit changed

The finance version's Section 7 explained changes to estimated risk, financial preferences and numerical accuracy. The final Section 7 retains that structure and makes learned-agent errors explicit.

Its interpretation is at the level of decisions: did the portfolio change because the covariance model changed, because the reward represents a different trade-off, or because actor/critic learning has not implemented the specified decision criterion accurately? A constant critic offset should not trigger the same interpretation as a state-dependent continuation error that changes hedging.

This fits IAFM through **financial decision interpretation, objective alignment, faithful evaluation and model validation**. It does not claim neural-feature attribution, an investor user study, causal explanations of market returns, or formal regulatory approval. The practical output is an auditable statement of assumptions, data access, acceptable deviation and remaining error.

The shift strengthens the RL relevance of the paper because the main result now applies to a trained policy rather than only to the optimum of a supplied reward. The tractable benchmark still has an analytical solution for evaluation, and direct optimisation remains sensible where it solves the problem. We do not need to pretend RL is necessary for the benchmark in order to use the benchmark to test an RL audit.

## 14. What changed in code and verification

The covariance phase added covariance estimation, financing-cost models, historical factorial runners, known-covariance simulations, independent verification and plotting. Principal modules are `mvrl/covariance.py` and `mvrl/financing.py`.

The RL phase added `mvrl/equilibrium_audit.py`, `mvrl/equilibrium_learning.py`, `mvrl/neural_equilibrium.py` and `mvrl/ppo_alignment.py`. These implement exact-model/independent-data audits, backward sample learning, shared neural learning and the PPO reward experiment. New runners save every configuration and seed; final summarisation reconstructs metrics from saved policies before producing paper numbers and figures.

| Check | Evidence |
|---|---|
| Unit tests before covariance extension | 35 |
| After covariance/financing extension | 50 |
| Final version | 78 passing tests |
| Historical reconstruction | 58,320 saved decisions |
| Known-covariance reconstruction | 2,160 fitted problems |
| Financing/anchor checks | 50 financing states; 144 anchor checks |
| Tabular RL reconstruction | 2,160 records |
| Final neural/PPO reconstruction | 1,620 checkpoint records + 40 PPO runs |
| Maximum final RL reconstruction discrepancy | 4.44 × 10⁻¹⁶ |
| Tested final RL certificate violations | Zero |

Numerical checks support implementation correctness; they do not substitute for proofs or establish universal statistical coverage. The tests include independently computed terminal moments, critic shifts, constraints, support checks, sampled PPO rewards, continuation-path enumeration and a PPO training smoke test.

No experiment was rerun merely to write this retrospective report. The report does not alter the final submission or its results.

## 15. What we can now claim—and what the pivot does not solve

The earlier practical capability was: **given a tractable fitted financial reference, identify and reduce the policy mismatch caused by a reward.**

The new capability is: **under the stated market/data assumptions, examine a learned policy and critic and bound the financial benefit of changing one decision, without supplying the equilibrium policy; then test a continuation-aware reward intervention that reduces measured mismatch in controlled learning experiments.**

This is a stronger and more specifically RL contribution. It also has a narrower empirical boundary than a general portfolio-performance paper. The covariance work makes its financial interpretation credible; the new theorem and learners make its RL content substantive. Neither part establishes that our agent beats all recent finance-RL methods on real data.

The following remain open extensions: historical sequential RL with a chronological protocol; multi-asset neural experiments; larger or hidden state spaces; audit confidence bounds for dependent trajectories and adaptive policy selection; broader architecture/hyperparameter sensitivity; full matched reproductions of recent equilibrium-RL frameworks; and exhaustive priority verification.

The candid answer to the pivot question is therefore: **we retained the same financial alignment problem, changed the headline from exact reward calibration to learned-policy certification, and added evidence to justify that change.** We did not discard the finance research, discover a universally superior covariance model, or complete the real-data RL extensions by implication.

## 16. Is the shifted contribution genuinely better? Assessment and defence

**My judgment is yes: the final version is a stronger contribution for a paper about RL alignment and validation, provided we keep its claims at their demonstrated scope. It is not stronger on every dimension.** The old version was more focused and easier to explain; the new version addresses a more consequential gap between a mathematical reward construction and a trained agent. This is an assessment of research value from the available evidence, not an experimental finding that the entire new paper is “better,” a guarantee of novelty priority, or a prediction of acceptance.

### The strongest reason to prefer the new contribution

The old calibration result largely answers a question about ideal optimisation: if we solve the reward objective correctly, does its optimum match a financial reference? An actual RL implementation adds a second problem. Its actor may not optimise the reward accurately, and its critic may supply an inaccurate picture of future investment opportunities. Exact reward alignment does not settle either issue.

The new certificate addresses the policy we actually obtained. It connects finite-iterate actor and critic errors to a specific financial quantity: the benefit from a one-step deviation. That closes a logical gap left by reward calibration alone. The constructed zero-gradient/non-equilibrium example demonstrates the gap, while the theorem explains how to bound it. This is more than adding another benchmark or training algorithm to the paper.

The target-policy requirement also changes. Direct policy-distance evaluation needs the reference policy. The certificate needs no solved equilibrium policy: it uses moments and residuals, or suitable independent data with confidence allowances. This is a genuine change in what the analysis can establish. It is not a claim that the data requirements are weak or that computing an equilibrium in our small benchmark is difficult.

### A comparison of research strength

| Criterion | Earlier calibration contribution | New certification contribution | Assessment |
|---|---|---|---|
| Clarity of the central result | A specific reward mismatch and correction are easy to state | A decision-error bound requires more definitions and assumptions | Earlier version is simpler |
| Relevance to actual RL training | Limited by ideal optimisation and supplied continuation information | Examines a learned actor/critic at a finite training budget | New version is stronger |
| Need for the solved target policy | Important for direct mismatch measurement and the exact anchor construction | Not required by the certificate, although model/data assumptions remain | New version adds a capability |
| Treatment of learning failure | Mostly optimisation diagnostics separate from the reward argument | Explicit actor/reward/critic bound and false-convergence example | New version is stronger |
| Empirical learning evidence | Historical allocation and statewise optimisation diagnostics | Tabular, shared neural and genuine PPO reward experiments | New version is stronger within controlled markets |
| Historical investment evidence | Substantial covariance/cost audit, with no established superiority | Same historical evidence; new RL learners not historically backtested | No improvement on this criterion |
| Breadth and accessibility of the proof | Narrow exact mismatch law and familiar calibration arguments | Broader vector/convex-action residual statement under restrictive dynamics | A useful expansion, with a more demanding explanation |
| Evidence of publication novelty | Specific exact-law candidate, with acknowledged prior identities | Specific certification candidate, with substantial prior components | Neither has exhaustive priority certification |
| Fit with IAFM | Financial preference interpretation and model validation | Retains these and adds an explicit learned-policy validation criterion | Stronger fit by reasoned assessment, not guaranteed acceptance |

### Why this is not simply moving away from disappointing backtests

A weak pivot would hide the negative historical result and replace it with a favourable synthetic ranking. The final paper retains the historical evidence, states that calibration does not establish realised investment superiority, and separates that experiment from the new RL experiments. It does not relabel synthetic learning gains as historical trading gains.

The new research question is justified independently of the backtest outcome: even if joint calibration had produced higher realised returns, we would still need to know whether a finite-budget actor–critic implementation faithfully implements the intended equilibrium. Critic error and actor convergence would still be unresolved by an exact reward identity. The certificate therefore addresses a real additional problem rather than providing a new metric solely to rescue an unfavourable ranking.

At the same time, the new scope must not be offered as completion of every earlier ambition. If the required contribution were specifically “a new multi-asset RL strategy that outperforms recent agents on chronological market data,” this version would not meet it. Its defended contribution is financial decision validation, with controlled learning evidence and a separate real-data calibration audit.

### Objections a reviewer could reasonably raise

**“The bound uses standard inequalities. Is that enough?”**

Standard ingredients alone are not novelty. The proposed increment is their specific assembly into a financial decision certificate: one-step terminal-MV deviation, actor/reward/continuation residuals, state-constant-offset invariance, transition-dependent propagation, feasible-action treatment and an independent-data construction. The question is whether that resulting statement provides a distinct and useful guarantee relative to prior work. The proof and experiments make that question inspectable. They do not establish priority by themselves, and the final journal-version access gap should not be concealed. If closer prior art contains the same guarantee, the novelty claim would need further narrowing.

**“Why use RL when the benchmark is analytically solvable?”**

The analytical solution is used to check the learner and the audit; it is not supplied to training. A known answer lets us measure actual error and certificate conservatism instead of treating a backtest metric as ground truth. That is a valid use of a controlled benchmark. It does not prove that RL is computationally necessary, cheaper than direct optimisation, or preferable for this small market. We should defend the benchmark as a test of certification, not manufacture a computational advantage.

**“The new learner may just be an existing equilibrium method in a specialised environment.”**

That is substantially the correct interpretation of the learning construction. The paper credits backward equilibrium learning and does not make the learner itself the main novelty claim. Its purpose is to test the continuation correction without supplying the equilibrium and to produce imperfect policies that the certificate can assess. PPO supplies a separate matched intervention inside a standard optimiser. Neither experiment establishes superiority over full SPERL or DPG-FPI implementations.

**“Centring improves policy distance by only 0.57%. Is the contribution small?”**

The 0.57% is the incremental effect of centring over an already continuation-aware critic. It should not be inflated. The larger 59.2% reduction compares the continuation-aware method with the myopic reward; it is evidence about the missing continuation term. The theorem's value is also not measured solely by centring's policy improvement: it distinguishes harmless offsets from policy-relevant errors and bounds deviation for a given policy. The 27.1% reduction in the mean model-based certificate supports that auditing interpretation, without turning it into an investment-performance claim.

**“The independent audit requires hundreds of thousands of observations. Is it practical?”**

The current requirement is a serious limitation. The experiment establishes that the data-based construction can be evaluated and that variance/mixing refinements materially tighten it. It does not establish a low-data deployment solution. The defensible claim is an explicit conditional guarantee with a visible cost and an abstention mechanism. Practical efficiency and dependent historical sampling remain open. Calling it production-ready would weaken the defence.

**“Has the new RL story displaced the strongest finance evidence?”**

It has displaced some detail from the eight-page paper, including full covariance tables and a simulation figure, but not the underlying research or the principal historical findings. That is a real presentation trade-off. The retained historical comparison explains why faithful reward implementation, good risk estimation and realised returns should not be conflated. It supports the same validation question from a financial angle; it should not be presented as empirical validation of the new sequential-RL theorem.

### What would reverse this assessment?

I would reconsider the claim that the new version is stronger if the central certificate were shown to duplicate existing work without a meaningful extension; if its numerical checks failed; if its use required effectively supplying the same unavailable object it claims to avoid; or if the intended venue valued a focused covariance/calibration contribution over learned-policy validation. The current evidence does not show the latter two mathematical/implementation failures: the certificate avoids a supplied equilibrium policy, and the reconstruction and tests pass. Exhaustive prior-art priority is still unresolved.

There is also a communication risk. If we explain the paper as three disconnected projects—covariance estimation, reward calibration and another RL algorithm—the earlier version may read more coherently. The defence depends on maintaining one line of argument: **fix the financial objective, distinguish input changes from preference changes, and then verify the decisions made by the trained agent.** Covariance experiments establish the first distinction; the new certificate addresses the final verification step.

### The contribution I would defend

> The earlier work showed how a portfolio reward can distort a specified financial preference and how to correct that distortion in tractable settings. The new work carries the same question through learning: it bounds the remaining one-step financial deviation of a trained policy using actor and continuation-critic residuals, without requiring the solved equilibrium policy. Controlled neural and PPO comparisons show that including continuation reduces mismatch, while the retained historical evidence explains why policy fidelity must be evaluated separately from investment returns.

That is a stronger, more specifically RL contribution than calibration alone. Its strength comes from the new guarantee and the question it answers—not from the number of experiments, a change of title, a claim to have invented all its mathematical ingredients, or an unsupported trading-performance ranking.


## 17. Where to inspect the evidence

- Starting paper: `archive/2026-10-07-before-covariance-revision/iafm/paper.tex`.
- Completed finance paper before the pivot: `archive/2026-10-09-before-final-rl/iafm/paper.tex`.
- Final paper: `submissions/iafm/paper.tex`.
- Finance methods and full results: [COVARIANCE_RESEARCH_REPORT.md](COVARIANCE_RESEARCH_REPORT.md).
- Finance proofs: [FINITE_CALIBRATION_AND_ESTIMATION.md](notes/FINITE_CALIBRATION_AND_ESTIMATION.md).
- Full Kolm–Ritter reading: [KOLM_RITTER_2025_FULLTEXT_REVIEW.md](notes/KOLM_RITTER_2025_FULLTEXT_REVIEW.md).
- RL proof: [RESIDUAL_CERTIFICATE.md](notes/rl-extension/RESIDUAL_CERTIFICATE.md).
- Final experiment summary and intervals: [final_summary.json](results/rl-extension/final_summary.json).
- Full primary-paper comparison ledger: [LITERATURE_LEDGER.md](literature/LITERATURE_LEDGER.md).
- Final implementation/delivery record: [FINAL_RESEARCH_REPORT.md](FINAL_RESEARCH_REPORT.md).

The citation register below uses the exact metadata already verified and saved in the project. It records the papers most relevant to this change history; it is not a claim that all of them supplied reproduced numerical baselines.

## Citation register

| Authors / year | Paper and verified outlet or version | Role in this progression |
|---|---|---|
| Victor DeMiguel; Lorenzo Garlappi; Raman Uppal (2009) | [Optimal Versus Naive Diversification: How Inefficient is the 1/N Portfolio Strategy?](https://doi.org/10.1093/rfs/hhm075). The Review of Financial Studies 22(5), 1915–1953. | Estimation risk, simple controls and dimension interpretation. |
| Olivier Ledoit; Michael Wolf (2004) | [A well-conditioned estimator for large-dimensional covariance matrices](https://doi.org/10.1016/S0047-259X(03)00096-4). Journal of Multivariate Analysis 88(2), 365–411. | Data-driven identity shrinkage. |
| Olivier Ledoit; Michael Wolf (2004) | [Honey, I Shrunk the Sample Covariance Matrix](https://doi.org/10.3905/jpm.2004.110). The Journal of Portfolio Management 30(4), 110–119. | Data-driven constant-correlation shrinkage. |
| Jianqing Fan; Yingying Fan; Jinchi Lv (2008) | [High dimensional covariance matrix estimation using a factor model](https://doi.org/10.1016/j.jeconom.2008.09.017). Journal of Econometrics 147(1), 186–197. | Observed-factor covariance construction. |
| Petter N. Kolm; Gordon Ritter (2025) | [Reinforcement Learning for Asset and Portfolio Management](https://doi.org/10.3905/jpm.2025.1.782). The Journal of Portfolio Management 52(2), 81–95. | Mandate alignment and validation motivation; no new empirical baseline. |
| Ali Habibnia; Mahdi Soltanzadeh (2024) | [Optimizing Portfolio with Two-Sided Transactions and Lending: A Reinforcement Learning Framework](https://arxiv.org/abs/2408.05382). arXiv:2408.05382v1. | Restricted reward adaptation and financing motivation. |
| Shangtong Zhang; Bo Liu; Shimon Whiteson (2021) | [Mean-Variance Policy Iteration for Risk-Averse Reinforcement Learning](https://doi.org/10.1609/aaai.v35i12.17302). Proceedings of AAAI 35(12), 10905–10913. | Prior mean auxiliary and one-step policy update; not our invention. |
| Nixie Sapphira Lesmana; Chi Seng Pun (2025) | [A Subgame Perfect Equilibrium Reinforcement Learning Approach to Time-Inconsistent Problems](https://doi.org/10.1137/23M1594510). SIAM Journal on Financial Mathematics 16(1), 68–122. | Prior equilibrium/backward learning; algorithm reading uses the 2021 preprint. |
| Xin Guo; Yijie Huang; Xiang Yu (2026) | [Deterministic Policy Gradient for Learning Equilibrium in Time-Inconsistent Control Problems](https://arxiv.org/abs/2606.11798). arXiv preprint 2606.11798v1. | Prior modified-reward equilibrium actor–critic; theoretical comparison, not a replicated baseline. |
| Tejaram Sangadi; Prashanth L.A.; Krishna Jagannathan (2025) | [A Finite-Sample Analysis of an Actor-Critic Algorithm for Mean-Variance Optimization in a Discounted MDP](https://arxiv.org/abs/2406.07892). arXiv:2406.07892v2. | Prior finite-sample MV actor–critic analysis; different audited target. |
| Zaiwei Chen; Sheng Zhang; Zhe Zhang; Shaan Ul Haque; Siva Theja Maguluri (2025) | [A Non-Asymptotic Theory of Seminorm Lyapunov Stability: From Deterministic to Stochastic Iterative Algorithms](https://arxiv.org/abs/2502.14208). arXiv preprint 2502.14208v1. | Prior seminorm and critic-offset geometry. |
| Andreas Maurer; Massimiliano Pontil (2009) | [Empirical Bernstein Bounds and Sample Variance Penalization](https://www.cs.mcgill.ca/~colt2009/papers/012.pdf). Proceedings of COLT 2009. | Established concentration inequality for the data audit. |
| John Schulman; Filip Wolski; Prafulla Dhariwal; Alec Radford; Oleg Klimov (2017) | [Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347). arXiv:1707.06347v2. | Standard clipped optimiser for our matched reward intervention. |
