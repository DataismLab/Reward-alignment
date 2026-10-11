# Final IAFM research and verification report

9 October 2026. Canonical submission: `submissions/iafm/paper.tex` and `paper.pdf`.
Title: **Certifying Reward Alignment in Portfolio Reinforcement Learning**.
This report supersedes the five-seed pilot's conclusions where final results differ. Earlier finance experiments and pilot outputs remain available; the incoming paper is preserved in `archive/2026-10-09-before-final-rl/iafm/`.

## The final contribution

The main result is an a posteriori financial decision certificate. In the stated finite exogenous-state market, a candidate policy's action-gradient error and the propagated span of its continuation-critic residual bound the gain from a one-step deviation under conditional terminal mean–variance preferences. The proof does not require the equilibrium policy. It handles vector returns and, through feasible critic-objective improvement, convex action constraints. Constant offsets to a critic at each date do not affect the certificate. This matters because absolute critic error may be large but decision-irrelevant, whereas a zero actor gradient can conceal a financially consequential critic error.

The contribution is deliberately narrower than a new general equilibrium-learning algorithm. Backward policy iteration, equilibrium RL, continuation hedges, mean auxiliaries, critic centring and empirical Bernstein bounds have established predecessors. The paper identifies these sources. It does not claim to be the first of any broad class or to outperform recent financial RL agents on investment returns. The final journal text of Lesmana–Pun was not available: the algorithm discussion is explicitly based on its 2021 primary preprint, with 2025 journal metadata verified. Exhaustive priority remains open, as in any targeted rather than systematic novelty search.

## Results and their status

**Proved under stated assumptions.** The residual-span deviation bound, actor/reward/critic triangle bound, vector covariance projection inequality, convex-action corollary and fixed-policy independent-data confidence construction. The paper includes the complete principal proof and the data-audit construction. Existing exact scalar-mismatch and constrained risk/cost calibration results remain, with their assumptions and prior mean-auxiliary interpretation. These are not distribution-free guarantees for arbitrary historical trajectories, wealth-dependent policies, hidden regimes, market impact or unknown return support.

**Numerically verified: final neural study.** We extended the unchanged pilot to twenty seeds in nine markets (three transition persistences by three horizons). This is 540 training runs and 1,620 checkpoint records, not 1,620 independent seeds. The final budget is 3,000 updates; all runs are included. Sample data, initialisation, inverse-curvature scaling and optimisation settings are shared across arms. No oracle equilibrium enters training.

| Variant | Policy distance | Maximum deviation | Model-based bound |
|---|---:|---:|---:|
| Myopic reward | 0.610183 | 0.00319845 | 0.00642326 |
| Continuation, ordinary critic | 0.250692 | 0.00060636 | 0.00222929 |
| Continuation, centred critic | 0.249259 | 0.00059405 | 0.00162536 |

The centred construction reduces distance by **59.2%** and deviation by **81.4%** versus the matched myopic learner. Its distance difference is −0.360924, with a paired 95% seed-bootstrap interval [−0.389878, −0.328846]. The additional distance reduction from centring is only **0.57%**, although its mean certificate is 27.1% smaller. The centring distance difference is −0.001433 [−0.002526, −0.000301]; its initial-value difference interval includes zero. Most policy improvement comes from the continuation term. The earlier five-seed 61.0%/81.6% results are pilot results, not the final abstract numbers. These intervals average fixed markets within seed and resample seeds, rather than treating every market as independent.

**Numerically verified: standard PPO reward intervention.** Forty runs cross two markets, ten seeds and two reward arms, with 32,768 steps per run. Stable-Baselines3 clipped PPO receives bounded actions, observed time/regime, identical conditional datasets, and the same sample-only backward continuation evaluation access. The fitted continuation is frozen within a rollout and refreshed between rollouts; the myopic arm ignores its covariance term. This is a structured hybrid intervention, not a replication of a published financial agent.

| PPO reward | Policy distance | Maximum feasible deviation | Bound |
|---|---:|---:|---:|
| Myopic | 1.728010 | 0.02349156 | 0.03279087 |
| Continuation-aware | 1.152519 | 0.01180378 | 0.01723406 |

Distance improves by **33.3%** and deviation by **49.8%**. The paired distance difference is −0.575491 [−0.739003, −0.403600]. Both reference policies lie within the action bounds; the audit uses feasible deviations. Training budgets are matched inside PPO, not between PPO and the separate direct-gradient neural study. The learner is not presented as a proven convergent general solution to time inconsistency.

**Numerically verified: independent-data audits.** Twenty fixed tabular policies have mean true maximum deviation 0.000902 and exact-model bound 0.001257. A Hoeffding-only data certificate averages 0.036141; an empirical Bernstein/mixing refinement averages 0.004911. Each audit uses 786,432 independent conditional observations. Each confidence construction covers its fixed policy's cells jointly at 95%; there is no 95% family guarantee across every policy and construction. The refinements followed inspection of the primary bounds and are described as sequential extensions. All twenty policies are covered in the saved checks; the mathematical concentration argument, not this observed coverage, provides the guarantee. Nonpositive variance lower bounds trigger abstention.

**Numerically verified: finance experiments retained.** The real-data audit uses 10, 30 and 49 value-weighted US industry portfolios from Kenneth French's archived August 2026 data vintage, 120-month lagged estimation and 432 evaluation months in 1990–2025. Six covariance models cross three universes. Joint calibration preserves its own fitted allocation reference in all eighteen cases, while transferring the unconstrained scalar correction worsens alignment in all twelve larger-universe cases. This is distinct from identifying the true market optimum. Joint calibration does not outperform raw reward in realised MV; minimum variance leads the quadratic comparators. The historical experiment is not a backtest of the new RL learners.

**Open extensions, not missing results behind present claims.** A chronological historical RL deployment; multi-asset neural experiments and larger state spaces; dependent-audit concentration and adaptive policy selection; learning-rate/architecture generalisation; faithful full SPERL or DPG-FPI replication; tighter sample bounds; and exhaustive novelty priority. The paper is complete as the scoped certification/controlled-learning study, without asserting these extensions are finished.

## Code and verification

New finalisation code adds the PPO environment and trainer (`mvrl/ppo_alignment.py`), unchanged-protocol twenty-seed runner, PPO runner, final reconstruction/figure generator, and four PPO tests. The tests independently enumerate sampled continuation paths, check paired rewards, seed resets, terminal handling and critic-offset invariance, and run an actual PPO smoke training. Research dependencies are declared as optional extras; the installed final environment is saved.

**78 tests passed**, including the 50 pre-extension tests. All 1,660 final neural/PPO records were reconstructed from saved actions and critics: maximum numerical discrepancy 4.44e−16, zero tested bound violations. The earlier 2,160 tabular records were also independently reconstructed in the preceding verification. The pre-extension tracked research files differ only in the intentionally revised canonical IAFM source/PDF; the tracked finance code and results are unchanged. This preservation check does not claim that later-created files existed in the earlier manifest.

Reproduce using a scientific Python environment with the optional `research` and `test` extras. Exact tested package versions are in `results/rl-extension/final-environment.txt`. Commands from the project root:

```text
python -m pytest -q
python scripts/run_neural_final.py
python scripts/run_ppo_alignment.py
python scripts/finalise_rl_results.py
python scripts/plot_final_covariance.py
```

The runners reuse saved per-seed outputs; move the corresponding result directory to an archive in a separate research copy to retrain. No market oracle is passed to the neural/PPO training modules. Full replay against saved outputs is substantially faster than retraining. The paper is edited directly; the older covariance source builder now refuses to overwrite it.

## Manuscript, literature and delivery

The final anonymous ACM manuscript has eight pages including references and appendices, 29 cited references, three figures and two tables. The ledger contains 39 primary-paper records, with publication metadata, actual inspected versions, exact comparison locations and project roles. PPO's original Eq. (7), Algorithm 1 and experimental setting are recorded; it is a standard optimiser reference, not a finance backtest comparator.

Section 7 explains financial decision interpretation: distinguish altered opportunities (covariance), altered preferences (reward), and implementation error (actor/critic). It connects the certificate to faithful evaluation and model-risk validation, matching IAFM's subject without inventing an LLM contribution. The historical table retains dated source/role entries, finance controls, and a final bold joint-calibration row. The new RL table distinguishes matched experimental panels. The new audit figure shows the cost and conservatism of independent-data certification.

Official IAFM and central ICAIF workshop rules were checked on 9 October: double-blind ACM format, at most eight total pages including references/appendices; extended deadline **12 October 2026, 23:59 AoE**, notification 16 October. Primary rules: https://iafm-icaif.netlify.app/ and https://icaif2026.org/workshop.html. A saved official IAFM HTML snapshot is in `notes/rl-extension/`.

The full-project compiler produces the delivery PDF. The native editor's single-file compiler cannot resolve external project inputs; this is an editor limitation, not a successful native compilation claim. Portable-source rebuilding, PDF anonymity, citations, layout and page count are checked separately. The private reproducibility ZIP is not an anonymous submission supplement. No submission or organiser contact has been made. The author remains responsible for required declarations and the submission portal.
