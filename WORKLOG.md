# Research worklog

## September 2026 — analytical benchmark and corrections

Implemented the independent-return mean–variance references, quadratic-reward Bellman solution, policy-distance decomposition and exact moment evaluation. The subsequent audit corrected the distinction between second moments and variance, precommitment and equilibrium, and signed financial-value differences and nonnegative surrogate regret. Unsupported 519-case and 93.1% claims were withdrawn. The fixed-decay EWMA consistency claim was disproved. Details and retained benchmark values are in `FINDINGS.md` and `notes/PROOFS.md`.

Extended the benchmark to changing moments, observed return regimes, bounded action trees, differential Sharpe rewards, estimated moments and return-law stress tests. The fixed-horizon mismatch coefficient was proved; a uniform joint horizon/interest limit was not established. Comparisons with published reward designs were recorded as adaptations, not full algorithm replications.

## 26–27 September — historical allocation

Added monthly Kenneth French industry portfolios and factors, lagged estimation, long-only allocations, turnover costs and independent first-order optimisation certificates. The initial ten-industry experiment evaluates 432 months in 1990–2025, seventeen robustness specifications and sixty finite-budget optimisation records. Independent reconstruction checks net returns, portfolio drift, common-state gaps and past-only estimates. Historical fitted-policy alignment improved; realised investment superiority was not established.

## 1–2 October — dimensionality and finance literature

Read DeMiguel–Garlappi–Uppal alongside Markowitz, Gârleanu–Pedersen and subsequent estimation-risk research. Extended the fixed historical protocol to 30 and 49 industries while retaining the ten-industry case. All 9,072 dimension-study decisions reconstructed. Joint calibration preserved fitted alignment in all three universes; unconstrained scalar calibration worsened alignment in the larger universes. The dimension study treats estimation error as a separate source of decision error.

## 7 October — covariance and financing

Added six covariance estimators: sample, fixed diagonal shrinkage, two data-driven linear-shrinkage estimators, market factor and three-factor models. Evaluated eighteen historical configurations and 2,160 known-covariance problems with dimensions up to 100. Added fifty borrowing/shorting/financing states and 144 approximate-anchor checks. All 58,320 historical covariance decisions reconstructed. Fifty tests passed at this stage.

Joint mean alignment remained below 1.60e−7. The scalar correction worsened alignment in all twelve larger-universe configurations. A single exploratory mean-auxiliary update reduced mean distance by 97.8–98.6%, without a supplied target. Factor-model benefits depended on residual specification. Joint calibration did not establish realised investment superiority. Methods and results are detailed in `COVARIANCE_RESEARCH_REPORT.md`.

## 9 October — literature integration and RL certification

Read the complete Kolm–Ritter journal article, including all fifteen pages, exhibits and references. Integrated its discussion of reward mandates, known-policy comparisons and forecasting versus decision quality. Recent equilibrium-RL and critic-seminorm papers narrowed the novelty claim to a financial residual certificate; the underlying learning ideas were credited to prior work.

Derived the one-step financial deviation identity, critic residual-span bound, actor/reward/critic split and convex-action corollary. Added fixed-policy independent-data certificates with explicit support and sampling assumptions. Twenty audited policies were covered by the saved constructions; this observed coverage is distinct from the concentration proof. Bernstein and mixing refinements reduced the mean data bound from 0.036141 to 0.004911, against true mean maximum deviation 0.000902, using 786,432 conditional observations per policy.

Completed 2,160 tabular records and a five-seed neural pilot. Extended the unchanged neural protocol to twenty seeds, nine markets and 540 runs, retaining 1,620 checkpoints. Added forty matched PPO runs. Final distance/deviation reductions were 59.2%/81.4% for the neural comparison and 33.3%/49.8% for PPO. Critic centring added 0.57% distance reduction beyond ordinary continuation. No historical RL backtest was performed.

All 78 tests passed. All 1,660 final neural/PPO records reconstructed to 4.44e−16, with zero tested certificate violations. Finance algorithms and saved results were preserved. The paper reports the final twenty-seed study; the pilot remains separately available.

## 11 October — reproducibility and public documentation

Integrated the completed research into the repository in separate historical, covariance, RL and documentation commits. Repeated the full test suite, historical reconstruction, covariance/financing checks and final-policy reconstruction. Added continuous integration and a manuscript checker.

Added a venue-neutral current paper under `manuscript/` and replaced duplicated progress summaries with research documentation. Historical editorial copies and preparation utilities remain in their existing locations and in Git history. Research algorithms and numerical experiment outputs are unchanged. Figure-generation and manuscript-checking paths follow the new layout.
