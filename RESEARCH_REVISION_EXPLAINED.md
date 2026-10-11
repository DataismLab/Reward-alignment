# What changed in the research: the finance and dimensionality extension

Prepared for Matin Tavakoli · 5 October 2026

This report explains the scientific changes between the manuscript immediately before the 1 October finance revision and the current manuscript, **When Portfolio Rewards Miss the Target: Exact Mismatch and Policy Alignment**. It excludes changes to table layout, ordering, citation presentation, fonts and other formatting. It distinguishes new experiments from earlier results that were retained and given a clearer interpretation.

## 1. The main change in the argument

The earlier work already showed that an additive portfolio reward can select a different policy from the investor's intended mean–variance objective. It already contained the independent-return theory, a historical ten-industry study, a calibration identity with trading costs, and an optimisation diagnostic.

The revision makes a more specific argument: **portfolio estimation, reward specification and numerical optimisation are different problems, and evidence about one does not settle the others.** We can hold the estimated market and trading state fixed, establish what preference a reward actually implements, identify a precise distortion, and test a correction. We then evaluate investment performance separately.

The new finance literature explains why this separation matters. The additional industry universes show that the calibration result is not confined to the original ten-dimensional example. Crucially, those experiments also show that faithfully implementing an estimated objective can produce worse realised outcomes. That finding narrows the investment claim but strengthens the distinction the paper is trying to establish.

| Research component | What changed substantively |
|---|---|
| Financial foundations | Added five primary papers from The Journal of Finance and The Review of Financial Studies, each with a specific role in the argument. |
| Portfolio dimension | Extended the historical audit from 10 to 30 and 49 industry portfolios under a fixed comparison protocol. |
| Empirical evidence | Found that unconstrained scalar calibration worsens alignment in both larger universes, while joint calibration still recovers the fitted policy numerically. |
| Investment interpretation | Explicitly incorporated the unfavourable realised results rather than treating alignment as evidence of superior investment performance. |
| Contribution | Distinguished the exact scalar-mismatch result from equivalent-objective methods that already exist in the literature. |
| Decision interpretation | Rebuilt Section 7 around financial meaning, controlled tests of policy fidelity and model validation. |
| Implementation assurance | Generalised the data pipeline, added dimension tests, and independently reconstructed all 9,072 decisions in the three-universe comparison. |

These substantive changes apply to the manuscript. The report describes the October finance revision; the subsequent RL extension is documented separately.

## 2. What we learned from DeMiguel, Garlappi and Uppal

The requested paper is Victor DeMiguel, Lorenzo Garlappi and Raman Uppal, **“Optimal Versus Naive Diversification: How Inefficient is the 1/N Portfolio Strategy?”**, *The Review of Financial Studies* 22(5), 1915–1953 (2009). [Journal reference](https://doi.org/10.1093/rfs/hhm075).

Its central issue is **estimation error in portfolio choice**, not a rule that a credible portfolio experiment must have many assets. An optimiser can be optimal for estimated means and covariances while those estimates are sufficiently noisy that the resulting portfolio performs poorly out of sample.

The authors compare fourteen allocation models with equal weighting across seven datasets. Their empirical conclusion is that none of those models consistently outperforms 1/N across the datasets and evaluation criteria. This does not prove that equal weighting is always optimal, or that optimisation cannot work. It establishes a demanding practical comparison: the gains from using estimated information must justify the errors introduced by estimating it.

Three details were especially relevant to our revision:

1. **Ten industries are a legitimate controlled benchmark.** Their Table 2 and Appendix A.2 include ten industry portfolios plus the market. This is not exactly our universe, but it contradicts the idea that using ten industries is inherently inadequate.
2. **Dimension must be considered relative to information.** Proposition 1, Figure 1 and Appendix B relate estimation requirements to the number of assets and the underlying investment opportunities. The often-cited examples of approximately 3,000 months for 25 assets and 6,000 months for 50 assets are model-calibrated illustrations, not universal minimum sample sizes.
3. **Evaluation must include economically meaningful controls and costs.** Section 2, Eqs. (12)–(17), and Tables 3–5 consider Sharpe, certainty-equivalent performance, turnover and transaction-cost consequences. A favourable allocation-distance result alone cannot establish investment superiority.

We used these lessons constructively in three ways. First, we retained 1/N and minimum variance as serious financial controls. Second, we expanded the opportunity sets while keeping the estimation and trading protocol fixed. Third, we made the distinction between a faithful reward and a good estimated investment policy central to the interpretation.

We did **not** reproduce their fourteen methods, sample periods or cost assumptions. Nor did we use their findings to excuse any negative result: the larger-universe performance results remain evidence against a broad outperformance claim. Their work explains why that question is separate from whether a reward implements its stated objective.

## 3. What “portfolio dimension” means here

The dimension is the number of allocation weights. A ten-industry portfolio has ten weights, one for each industry portfolio; a forty-nine-industry portfolio has forty-nine weights. These are not ten or forty-nine individual companies. Each industry return series aggregates companies in that industry, with value weighting inside the industry.

Our outer allocation is long-only and fully invested, so its weights sum to one. There are therefore N weights but N−1 independent allocation degrees of freedom. Estimating their joint return distribution still requires an N-dimensional mean and an N-by-N covariance matrix.

The covariance matrix is symmetric, so the number of distinct mean and covariance entries is

\[
N+\frac{N(N+1)}{2}.
\]

| Industry universe | Allocation weights | Mean entries | Distinct covariance entries | Total moment entries | N / 120-month window |
|---|---:|---:|---:|---:|---:|
| 10 industries | 10 | 10 | 55 | 65 | 0.0833 |
| 30 industries | 30 | 30 | 465 | 495 | 0.2500 |
| 49 industries | 49 | 49 | 1,225 | 1,274 | 0.4083 |

These counts illustrate the growth in estimation burden; they are not counts of statistically independent parameters. More assets can improve diversification while simultaneously making input estimation harder.

The experiment now covers a broader decision space, but it is not a pure causal experiment in dimension. The 10-, 30- and 49-industry classifications change the assets and their aggregation as well as N. They also cover the same US market over overlapping dates, so they are not three independent market replications. None has N greater than the 120-month estimation window.

## 4. What we implemented for the dimension extension

We added the public Kenneth French 30- and 49-industry value-weighted monthly returns and retained the original ten-industry results. All use the same August 2026 data vintage and risk-free series. This is historical research-portfolio data, not a newly built collection of tradable funds or point-in-time stock constituents.

The extension protocol was recorded before inspecting the additional outcomes. Its main settings were:

- Estimation data: January 1970–December 2025.
- Evaluation: January 1990–December 2025, giving 432 monthly decisions.
- Information available at each decision: the preceding 120 months only.
- Estimates: sample excess-return means and unbiased covariance, with 10% shrinkage toward the covariance diagonal.
- Preferences: risk coefficient 5 and a turnover coefficient of 0.001, or 10 basis points per unit of L1 turnover.
- Constraints: long-only, fully invested; equal initial holdings.

Seven methods were evaluated in each universe: the fitted mean–variance target, the raw second-moment reward, unconstrained scalar calibration, risk-only calibration, joint calibration, equal weighting and minimum variance.

This gives 7 × 432 × 3 = **9,072 saved decisions**: 6,048 new decisions for the two added universes and 3,024 comparable decisions from the original ten-industry study. The broader ten-industry comparison also contains MVPI and log-based methods. Those were not rerun at 30 and 49 industries. Likewise, the existing seventeen-setting robustness grid remains a ten-industry experiment, not a seventeen-setting grid for every universe.

Two separate evaluations prevent an important confounding problem:

**Common-state evaluation:** every reward faces the same estimated moments, constraints and pre-trade holdings. Differences in the resulting allocations can then be attributed to the objective being optimised, subject to numerical accuracy.

**Own-state investment evaluation:** every strategy carries forward its own holdings, lets them drift with returns, rebalances and pays its own turnover costs. This measures the realised consequences of following that strategy over time.

The first answers whether the reward represents the requested preference. The second answers how the resulting strategy performed historically. Combining them into one test would obscure the distinction.

## 5. The new numerical findings

### 5.1 Joint calibration preserves fitted-policy alignment across universes

The following values are mean Euclidean distances from the fitted target allocation, measured on common states. They are distances between weight vectors, not percentages of lost return.

| Reward construction | 10 industries | 30 industries | 49 industries |
|---|---:|---:|---:|
| Raw second moment | 0.00843 | 0.01852 | 0.02079 |
| Unconstrained scalar calibration | 0.00540 | 0.02183 | 0.05354 |
| Risk-only calibration | 0.00510 | 0.00758 | 0.00820 |
| Joint calibration | 1.40 × 10⁻⁸ | 7.33 × 10⁻⁸ | 1.29 × 10⁻⁷ |

**Status: numerically verified.** Joint calibration agrees with the fitted reference to numerical precision in all three universes. Its exact policy-preservation identity is also proved under the stated assumptions.

The unconstrained scalar rule improves alignment at N=10 but makes it worse at N=30 and N=49. At N=49 its mean distance is about 2.58 times the raw reward's distance. This is a useful concrete finding: applying a formula derived for an unconstrained setting is not a reliable correction once constraints and costs are present.

Allocation distance should be accompanied by the loss in the intended objective. In monthly basis-point units, the raw fitted losses are approximately 0.0148, 0.0803 and 0.1182; the scalar-calibration losses are 0.00434, 0.1099 and 0.7043. Joint calibration's fitted loss is numerically zero. The absolute raw losses are small, especially in the original universe. We should therefore claim precise identification and removal of this discrepancy, not a large economic gain based solely on a visually striking distance reduction.

### 5.2 Better alignment does not imply better realised performance

Realised monthly mean–variance is the sample mean of net excess returns minus five times their sample variance. It is an objective score, not the mean return itself. A negative score does not mean the portfolio necessarily lost money.

| Method | 10 industries | 30 industries | 49 industries |
|---|---:|---:|---:|
| Raw reward | −7.182 bp | −20.880 bp | −24.897 bp |
| Joint calibration / fitted target, to rounding | −8.497 bp | −26.096 bp | −30.567 bp |
| Equal weight | −11.893 bp | −31.669 bp | −30.592 bp |
| Minimum variance | +5.274 bp | −0.416 bp | −4.808 bp |

Joint calibration's realised MV difference from the raw reward is:

| Universe | Joint minus raw | Paired 95% path-bootstrap interval |
|---|---:|---:|
| 10 industries | −1.315 bp | [−3.318, +0.343] bp |
| 30 industries | −5.216 bp | [−10.044, −0.903] bp |
| 49 industries | −5.670 bp | [−10.747, −0.882] bp |

**Status: preliminary historical evidence.** These saved comparisons are reproducible, but their generalisation beyond the observed data remains uncertain. The intervals use 1,000 paired circular-block resamples with twelve-month blocks. They condition on the realised strategy paths, do not refit every estimator, and are not adjusted for multiple comparisons. The universes overlap.

Minimum variance has the highest realised MV of the seven methods in each universe. All joint-versus-equal-weight intervals include zero. We therefore do not establish superiority over naive diversification or minimum variance.

This does not invalidate the calibration identity. It shows that the identity solves a narrower problem: implementing a fitted preference. The underlying means and covariances can still produce a poor investment decision. The experiment does not identify the unknown true moments, so it cannot measure exactly how much underperformance is caused by estimation error rather than other aspects of model specification or market variation.

An existing ten-industry result also illustrates why Sharpe alone is insufficient: equal weighting has higher Sharpe than the fitted target, but lower realised MV at the specified risk coefficient. These metrics answer different preference questions.

## 6. The finance references and what each actually contributes

The revision added five primary finance papers. Their role is substantive rather than simply increasing the bibliography. The current manuscript cites eighteen references; the wider project ledger contains additional inspected sources.

**Harry Markowitz (1952), “Portfolio Selection,” The Journal of Finance 7(1), 77–91.** [DOI](https://doi.org/10.1111/j.1540-6261.1952.tb01525.x). The relevant material is on pp. 77, 81–83 and 89–91. This supplies the mean–variance foundation and the distinction between beliefs about returns and decisions made using those beliefs. It helps locate our question: even with the same beliefs, does replacing the objective with a reward change the decision? We do not claim to introduce the mean–variance objective.

**DeMiguel, Garlappi and Uppal (2009), “Optimal Versus Naive Diversification: How Inefficient is the 1/N Portfolio Strategy?”** [DOI](https://doi.org/10.1093/rfs/hhm075). This supplies the estimation-risk perspective, the equal-weight hurdle and the motivation for the dimension extension, as explained above. Its empirical findings are not presented as our replicated results.

**Nicolae Gârleanu and Lasse Heje Pedersen (2013), “Dynamic Trading with Predictable Returns and Transaction Costs,” The Journal of Finance 68(6), 2309–2340.** [DOI](https://doi.org/10.1111/jofi.12080). Section II, Eqs. (3)–(5), Section III, Propositions 2–3, and Section VI/Table II provide the comparison. Their dynamic policy optimises an explicitly stated economic objective with predictable returns and quadratic costs. This shows that finance already has principled objective-based controls. Our rolling one-period L1-cost reference is different; it is not their dynamic optimum. Their contribution motivates preserving cost preferences and being precise about continuation decisions.

**Olivier Ledoit and Michael Wolf (2017), “Nonlinear Shrinkage of the Covariance Matrix for Portfolio Selection: Markowitz Meets Goldilocks,” The Review of Financial Studies 30(12), 4349–4388.** [DOI](https://doi.org/10.1093/rfs/hhx052). Sections 1–3 and Section 4.3, Eqs. (17)–(20)/Table 1, connect covariance estimation to portfolio-specific losses and realised consequences. This clarifies that improving inputs and correcting reward semantics are complementary interventions. Our fixed 10% diagonal shrinkage is not their nonlinear estimator, and we do not claim to outperform it.

**Victor DeMiguel, Alberto Martín-Utrera and Raman Uppal (2024), “A Multifactor Perspective on Volatility-Managed Portfolios,” The Journal of Finance 79(6), 3859–3891.** [DOI](https://doi.org/10.1111/jofi.13395). Sections I.A–C, Eqs. (3), (6), (10), and Tables II–III give a recent example of mean–variance portfolio design that incorporates costs directly. We use it as a positive comparison: financial research already treats trading costs as part of the preference. Our contribution is to check whether a reward transformation preserves that preference. We did not reproduce its factor strategy.

The older papers establish foundations; the 2024 addition and retained 2024–2026 financial-learning papers provide recent context. Recency and venue reputation do not substitute for relevance to the exact claim.

### How the retained learning papers constrain our claims

- **Zhang, Liu and Whiteson (2021), “Mean-Variance Policy Iteration for Risk-Averse Reinforcement Learning,” AAAI 35(12), 10905–10913:** its mean auxiliary already supplies the transformation underlying the historical calibration identity. Our MVPI adaptation also reaches the fitted target. We cannot claim to beat it on asymptotic alignment. [DOI](https://doi.org/10.1609/aaai.v35i12.17302)
- **Jiang, Olmo and Atwi (2025), “High-dimensional multi-period portfolio allocation using deep reinforcement learning,” International Review of Economics and Finance 98, 103996:** Eq. (8) motivates the adapted log-minus-variance comparator; Eq. (19) describes their soft constraints. We compare reward preferences under common data and constraints, not their complete learning architecture. [DOI](https://doi.org/10.1016/j.iref.2025.103996)
- **Jiang, Olmo and Atwi (2024), “Deep reinforcement learning for portfolio selection,” Global Finance Journal 62, 101016:** Eq. (4) motivates attention to how value, variance and costs are combined. Its TD3/PPO/DDPG algorithms were not reproduced here. [DOI](https://doi.org/10.1016/j.gfj.2024.101016)
- **Simon, Weibels and Zimmermann (2026), “Deep Parametric Portfolio Policies,” Management Science, Articles in Advance:** Section 4.1, Eq. (17), directly uses centred MV utility, and Section 3.6 handles turnover costs. This is evidence against a sweeping claim that financial learning neglects the investor's objective. [DOI](https://doi.org/10.1287/mnsc.2025.00721)
- **Gollart and Okhrin (2025), “A reinforcement learning approach to dynamic portfolio optimization,” Annals of Operations Research:** Section 4.2.1/Table 1 validates learned policies against an analytical benchmark. Known-policy validation is therefore prior practice, not an invention of this project. [DOI](https://doi.org/10.1007/s10479-025-06649-x)
- **Cong, Tang and Wang (2026), “AlphaPortfolio: Goal-Oriented Investment Management Through Deep Reinforcement Learning,” NBER Working Paper 35195:** Eqs. (19)–(20) allow trajectory objectives, including Sharpe. This is a working paper and an example of a different legitimate preference, not an algorithm we empirically surpassed. [DOI](https://doi.org/10.3386/w35195)

Thus five additional finance references do not mean five additional algorithm replications. The empirical comparison is a controlled reward-formulation comparison, with conventional portfolio controls and an MVPI adaptation.

## 7. The proposed method, explained directly

The method begins with an investor's objective rather than choosing a reward and later interpreting its backtest:

1. Specify the intended financial preference and constraints.
2. Obtain its reference policy in a tractable benchmark.
3. Solve for the policy induced by the proposed reward.
4. Measure both allocation discrepancy and loss under the intended objective.
5. Derive a correction where possible, or quantify what the reward family cannot recover.
6. Evaluate the correction's realised performance separately from its alignment.

For the historical experiment, write the fitted preference as

\[
F(u)=m^\top u-\varphi u^\top\Sigma u-\lambda\|u-p\|_1.
\]

Here m is the estimated excess-return mean, Σ the covariance, p the pre-trade holdings, φ the risk coefficient and λ the turnover coefficient. Let u* maximise F over the simplex. Define M = Σ + mmᵀ, y* = mᵀu* and A = 1 + 2φy*, requiring A > 0.

The joint-calibrated second-moment objective is

\[
Q(u)=m^\top u-\frac{\varphi}{A}u^\top M u
-\frac{\lambda}{A}\|u-p\|_1.
\]

Its policy preservation follows from the identity

\[
AQ(u)=F(u)-\varphi(m^\top u-y^*)^2+\varphi(y^*)^2.
\]

At u*, the additional negative square vanishes and F is maximal. Positive scaling by A preserves the maximiser. Under the paper's convexity and positive-definiteness conditions, the optimum is unique.

The practical mechanism is that **risk and costs must be calibrated together**. Dividing only the risk coefficient by A leaves an additional effective turnover penalty of 2φy*λ after normalisation. For positive y*, that changes the economic preference toward avoiding trades. It does not imply that every realised turnover sequence must decrease monotonically.

This construction uses the target mean y*, obtained from the reference policy. It is a certificate and validation device, not a shortcut that avoids solving the target. If the target is already tractable, directly using it is reasonable. The adapted MVPI method is an existing constructive way of computing that optimum without first inserting the target mean.

## 8. What is distinctive, and what was not newly invented

The strongest theoretical result remains the **exact leading minimum policy discrepancy after the best common scalar calibration** of a quadratic wealth-increment reward. This result existed before the latest finance revision; the revision clarifies its relationship to prior work.

In the independent-return, unrestricted-dollar-position benchmark, the terminal objective is expected terminal wealth minus φ times its variance. The reference is the time-consistent equilibrium, not the precommitment optimum. For a horizon T ≥ 2 and gross risk-free return s near one,

\[
\min_{\kappa>0}D=c_T|s-1|+O((s-1)^2),
\]

with an explicit positive coefficient c_T derived in the manuscript. At s = 1, exact scalar matching is possible. At s ≠ 1, exact matching is impossible under the stated assumptions. The raw increment reward creates wealth dependence that the equilibrium allocation does not have; tuning one coefficient cannot remove that structural difference.

**Status: proved within the benchmark.** The expansion is for fixed T, and it is not a theorem about arbitrary historical markets, constraints or reward families. Although the coefficient grows like T³ᐟ², the paper does not claim a uniform joint large-horizon/small-interest approximation.

The literature review prevents three overclaims. Equivalent-objective approaches already exist in time-inconsistent control. The historical auxiliary identity comes from prior MVPI theory. Validating learned policies against known optima is also established practice. We credit those foundations instead of claiming the whole framework is unprecedented.

The defensible contribution combines a particular quantitative impossibility result, an explicit explanation of cost distortion, and a reproducible audit across realistic estimated allocation states. The new dimension experiments strengthen this package by identifying where an apparently reasonable scalar correction fails and demonstrating that the joint identity survives the larger feasible problems.

The review supports this more precise positioning, but it is not an exhaustive certificate that no previous paper has any overlapping result. Adding citations does not itself create novelty. The candidate theoretical increment is the exact best-scalar mismatch coefficient and its proof for the specified family.

**A concise statement of the contribution:** We quantify when scalar reward tuning cannot implement a terminal mean–variance equilibrium, and show how to preserve a fitted constrained mean–variance preference by calibrating risk and costs together. Historical tests across 10, 30 and 49 industries demonstrate policy alignment while separating it from realised investment performance.

## 9. Financial interpretation and model validation

Section 7 is now **“Financial semantics and model validation.”** It explains what changes in an allocation mean when the model, reward or numerical approximation changes.


### Interpreting a decision through its objective

The first subsection makes the reward's financial meaning explicit. Risk-only calibration changes the effective turnover preference by a calculable amount. The terminal raw reward introduces wealth dependence absent from the reference policy. These are explanations of a decision rule that generate testable predictions about what will happen if the reward is changed.

This gives a concrete connection to financial semantics: return, variance, costs, wealth and the investor's mandate have defined mathematical roles. The explanation is supported by an identity or theorem rather than inferred from a favourable performance chart.

### A controlled test of policy fidelity

The second subsection connects interpretability to verification. Holding information and holdings fixed creates a controlled intervention on the reward. Allocation distance reports the decision change; fitted objective loss reports its economic importance. The small ten-industry raw loss is included so that a visible allocation difference is not mistaken for a large financial loss.

The existing finite-budget softmax experiment adds a separate optimisation check. It uses five matched seeds and several optimisation budgets on historical fitted states. It does not test neural-policy generalisation: each state has its own logits. Its role is to distinguish a reward's limiting policy from an imperfect numerical approximation to that policy.

The target-value decomposition has a reward-design term and a **signed** finite-optimisation transfer term. The latter is not the nonnegative own-reward optimisation gap. Keeping these quantities separate avoids attributing every observed policy discrepancy to reward design.

### What the audit establishes about model risk

The third subsection explains what a validator can inspect: the intended objective, the induced allocation, the numerical certificate, the proposed correction and its consequences. The dimension study supplies a particularly useful example: an aligned reward can still lead to disappointing investment outcomes, while a good backtest cannot certify that the requested preference was implemented.

This is a substantive model-validation connection. It is not a claim to explain neural circuits, improve human understanding through a user study, validate an LLM, or satisfy a regulatory standard. Those experiments were not performed. The interpretation is limited to the decision rules and tests actually studied.

## 10. Code, verification and supporting evidence

The revision included research-code changes, not only manuscript changes:

- **Data and experiment pipeline:** `mvrl/historical.py` now accepts the selected industry dimension while retaining ten as the default. The parser restricts validation to the intended date range, rejects missing values within that range, and checks for a complete monthly sequence. Earlier missing entries in the 49-industry file are excluded by the date boundary, not filled in.
- **Dimension experiment:** `scripts/run_dimensions.py` runs the fixed protocol and saves allocations, metrics, bootstrap comparisons and data provenance.
- **Independent verification:** `scripts/verify_dimensions.py` reconstructs quantities from original returns and saved actions rather than simply trusting summary tables.
- **Tests:** `tests/test_dimensions.py` adds dimension/calibration checks and a parser-boundary check. The recorded completed revision passed 35 tests, up from 31.

The independent reconstruction covers all 9,072 decisions in the dimension comparison. Maximum discrepancies were about 4.17 × 10⁻¹⁷ for net returns, 2.56 × 10⁻¹⁶ for turnover, 3.47 × 10⁻¹⁸ for fitted gaps, and 7.38 × 10⁻¹⁸ for the calibration identity. Quadratic optimisations also use first-order certificates computed through a separate linear programme, rather than relying solely on an optimiser's success message.

These are recorded results of the completed revision, not newly rerun experiments for this explanatory document. No new predictive architecture, PPO/DDPG replication or nonlinear-shrinkage implementation was added.

The manuscript's visual evidence continues to connect four questions: the analytic mismatch law, historical alignment versus realised rankings, robustness across seventeen ten-industry specifications, and optimisation error versus reward-design error. The added dimension results and appendix verification provide the new empirical extension. The appendix also preserves the complete robustness specifications and explains numerical certificates and uncertainty, making the main claims easier to inspect.

## 11. What the revision enables—and what remains outside its evidence

A reader can now use the project to ask a more precise question than whether a risk-adjusted reward produces a good Sharpe ratio: **does optimising this reward implement the specified return–risk–cost preference, and if not, what exactly changes?** In the tractable settings, the project supplies a reference, a discrepancy measure, an explanation, a correction or impossibility result, and independently checked numerical evidence.

The following boundaries remain important:

- **Proved:** the scalar-matching obstruction and leading discrepancy in the independent-return benchmark; the constrained joint-calibration identity under its assumptions.
- **Numerically verified:** fitted-policy recovery across the three industry universes; scalar-calibration deterioration in the two larger universes; the saved accounting and identity checks.
- **Preliminary:** historical investment comparisons and their path-bootstrap uncertainty. They do not support a general superiority claim.
- **Open extensions:** a true historical dependent-return terminal-equilibrium benchmark with continuation hedges; richer investable, point-in-time universes; predictive policies that generalise across states; broader estimation and dimension stress tests.

The current historical study uses a rolling one-period fitted reference. It does not silently turn the independent-return terminal theorem into a theorem for real dependent markets. It also does not isolate the unknown population estimation error or show that the correction outperforms recent published learning systems.

The revision is stronger because its financial foundations, experimental scope, mechanisms and contribution are more explicit and mutually consistent. Its value is the ability to diagnose and verify the financial objective implemented by a reward. The evidence does not support presenting it as a new strategy that beats contemporary portfolio benchmarks on real data.

## Evidence and project records

The following files provide the underlying record for this explanation:

- [Current manuscript](<manuscript/paper.tex>) — definitions, proofs, empirical interpretation and Section 7.
- [Scientific revision note](<notes/DIMENSION_STUDY_NOTES.md>) — what was changed and what was retained.
- [Fixed dimension protocol](<notes/DIMENSION_PROTOCOL.md>) — settings specified before inspecting additional outcomes.
- [Finance-paper reading records](<literature/finance-foundations/records.json>) — exact versions, sections, tables, objectives and project roles for the five additions.
- [Dimension results](<results/historical/dimensions/summary.json>) — full-precision metrics and paired intervals.
- [Independent verification results](<results/historical/dimensions/verification.json>) — reconstructed decision counts and numerical residuals.
- [WORKLOG](<WORKLOG.md>) — chronological research and verification history.
