# Final IAFM submission — 9 October 2026

**Current:** `submissions/iafm/paper.tex` / `paper.pdf`, **Certifying Reward Alignment in Portfolio Reinforcement Learning**. Read `FINAL_RESEARCH_REPORT.md` and `results/rl-extension/final_summary.json`. The manuscript now incorporates the residual certificate, twenty-seed neural extension and ten-seed PPO comparison. 78 tests pass; 1,660 final RL records reconstructed with error below 4.45e−16. Final neural distance reduction is 59.2%, PPO 33.3%; no historical investment-superiority claim. Earlier dated material below is retained history and may describe the superseded five-seed pilot or earlier manuscript. No submission made.

---

# Full-text integration — 9 October 2026

**Verified literature finding:** Kolm–Ritter (2025), pp. 90–91, already identifies mandate-aligned reward design as important; Exhibit 2 (p. 84) supplies a workflow to which our audit adds a quantitative check. The article is equation-free and has no original numerical strategy to benchmark. It discusses known-policy validation (p. 87), so neither recognition of reward alignment nor benchmark comparison is a first contribution here. The existing exact mismatch theorem, calibrated constructions and numerical results remain the scoped contribution. No new experiment is claimed. The abstract now states joint scaling as sufficient; the former “only when” wording did not establish universal necessity.

# Latest result register — 7 October 2026

- **Proved:** the prior scoped terminal mismatch theorem remains; convex deterministic-cost calibration, imperfect-anchor value/distance bounds, fitted-covariance perturbation bounds, and the explicitly restricted assetwise-downside counterexample are documented in `notes/FINITE_CALIBRATION_AND_ESTIMATION.md`. Auxiliary identities and strong-concavity arguments are credited to prior methods; no new general MVPI claim.
- **Numerically verified:** six estimators × three industry universes, 58,320 reconstructed historical decisions; joint mean distance <1.60e−7 in all eighteen cases. Unconstrained scalar calibration worsens distance and fitted regret in all twelve larger-universe cases. One existing MVPI update reduces mean distance 97.8–98.6%; sequential exploratory comparator, not a new algorithm.
- **Numerically verified, limited investment implication:** joint realised MV is below raw in all eighteen cases; minimum variance has the highest realised MV among their quadratic methods. All fifteen covariance-target-vs-diagonal paired 95% intervals and simultaneous bands contain zero. No empirical superiority claim.
- **Numerically verified:** 2,160 known-covariance problems (N up to 100, L=60/120); factor benefit depends on residual specification. All fifty financing identities pass, mean full joint discrepancy 1.51e−7 versus partial scaling 0.00997. All 50 tests pass.
- **Preliminary/open:** generalisation of one-step usefulness, predictive neural RL, point-in-time investment universe, true dependent terminal-equilibrium identification, unrestricted DSR and exhaustive priority. Kolm–Ritter 2025 was subsequently fully read on 9 October; the manuscript now uses exact full-text locators. See notes/KOLM_RITTER_2025_FULLTEXT_REVIEW.md.

See `COVARIANCE_RESEARCH_REPORT.md` for exact conventions and complete tables. This entry supersedes outdated manuscript/result counts below, without altering earlier experiments.

# Current IAFM revision — 1 October 2026

Use **submissions/iafm/paper.pdf** and **paper.tex**: anonymous, eight pages, 18 references. This supersedes the reading instructions and named-copy descriptions below. The primary ten-industry study is now accompanied by 30/49-industry checks. Joint calibration preserves fitted alignment; scalar calibration worsens alignment in the larger universes, where joint calibration also has lower realised MV than raw. No investment-superiority claim. See [revision and reproduction notes](notes/IAFM_REVISION_2026-10-01.md), [dimension protocol](notes/DIMENSION_PROTOCOL.md), and `results/historical/dimensions/`. Verification: 35 tests; 9072 dimension-study decisions independently reconstructed. The literature ledger has 27 records, 18 cited in IAFM. Earlier proposal, report V2 and other workshop editions remain historical versions.

# Current revision — 27 September 2026

The current paper is **submissions/iafm/paper.pdf** (anonymous ACM sigconf for IAFM 2026). The completed historical extension, result status and reproduction steps are in [HISTORICAL_IMPLEMENTATION.md](notes/HISTORICAL_IMPLEMENTATION.md). The 21-paper ledger includes five recent primary papers. Historical calibration improves fitted policy alignment, not demonstrably realised performance. Earlier proposal/paper PDFs and the separate presentation proposal are preserved historical editions.

# Current findings — 22 September 2026

This file supersedes earlier claims. Historical versions are preserved in archive/2026-09-21-before-audit and the original delivered ZIP. PROVED means a mathematical derivation under the stated assumptions, not independent peer review or established publication priority. NUMERICALLY VERIFIED means verified in the specified finite experiment. PRELIMINARY means evidence limited by sampling/model scope. OPEN means unresolved. No current conjecture is used as an established premise.

| Result | Status | Evidence / limitation |
|---|---|---|
| Li–Ng precommitted policy and equilibrium reference | PROVED, known theory; numerically verified implementation | Existing verifier; primary literature ledger |
| Raw quadratic increment Bellman recursion | PROVED | notes/PROOFS.md §2; exact inner optimisation |
| Zero-interest κ=φ(1−ν) calibration | PROVED; not claimed novel | Also the fixed point of the adapted existing MVPI |
| General fixed-horizon mismatch coefficient | PROVED | notes/PROOFS.md §3; analytic remainder and global local-in-interest minimiser |
| c_T asymptotic T^(3/2) | PROVED as a coefficient asymptotic | Not a uniform joint T→∞, s→1 theorem |
| Exact terminal-unit reward redesign | PROVED | Independent moments, unconstrained dollars, equilibrium target |
| Common-penalty lower bound for changing moments | PROVED | Weighted dispersion; not automatically positive for all time variation |
| Observed-regime equilibrium and oracle hedge correction | PROVED | Joint return/next-regime law, scalar risky asset, solved continuation |
| DSR finite-horizon well-posedness and local identity | PROVED | Bounded returns, positive initial EWMA variance; no full fixed-penalty equivalence |
| Fixed-decay EWMA consistency | DISPROVED; correction PROVED | Limiting variance eta*sigma²/(2−eta)>0 for iid inputs |
| Exact sweeps and published reward adaptations | NUMERICALLY VERIFIED | 120 base configurations, 27 moment configurations, finite action trees |
| Five-seed learning comparison | PRELIMINARY | No learned mean–variance improvement from redesign at current budget |
| Moment estimation / frozen-policy stress | PRELIMINARY | Thirty estimation seeds; ten stress batches; AR(1) reverses design-vs-raw J |
| Publication priority of quantitative results | OPEN | Targeted primary-paper search; no broad “first” claim |
| Unrestricted/infinite-horizon DSR | OPEN | Finite grid is not a continuous/unbounded proof |
| General dependent multi-asset, constraints and transaction costs | OPEN | Scoped regime/long-only evidence only |
| Historical or PPO/DDPG algorithm replications | OPEN / not performed | Reward adaptations are not algorithm replications |

## Headline, with the right scope

A scalar penalty on squared wealth increments generally cannot recover the terminal mean–variance equilibrium at nonzero interest. Its best local policy mismatch has an explicit coefficient for every fixed horizon. Measuring excess gains in terminal units and applying date-specific moment calibration exactly recovers equilibrium under independent returns and unconstrained dollar holdings.

This is a concrete diagnostic and conditional design result. The zero-interest calibration alone is insufficient novelty: Zhang–Liu–Whiteson's existing MVPI reduces to the same fixed point. Equilibrium RL and associated time-consistent objectives also predate this project.

## Main exact comparison

Three risky assets, T=4, phi=1, s=1.02, wealth1; fixed equilibrium occupancy distance:

| Method | Distance | Terminal J | Terminal excess Sharpe |
|---|---:|---:|---:|
| Precommitted reference | 3.312087 | 1.425799 | 1.171951 |
| Equilibrium | 0 | 1.323644 | .982266 |
| Raw penalty κ=φ | .797127 | 1.316580 | .987285 |
| Scalar κ=φ(1−ν) | .195347 | 1.326115 | .987292 |
| Best scalar within raw family | .186435 | 1.326093 | .987292 |
| Terminal-unit design | numerical zero | 1.323644 | .982266 |
| Existing MVPI adaptation | .313586 | 1.325487 | .987293 |

Equilibrium alignment is not maximisation of initial J. Scalar and adapted MVPI can exceed equilibrium J. Sharpe is not annualised; the risk-free terminal payoff is subtracted correctly.

## Negative and limiting results

In the bounded 21-point long-only tree, design distance .041366 improves on raw .058485, but design J=1.107729 is slightly lower than raw J=1.107849 and scalar J=1.108217. The exact-recovery theorem does not extend through wealth-dependent constraints. Grid refinement changes small J differences, so broad ranking claims are not justified.

Five-seed learned J means: raw1.305628, scalar1.302556, design1.300671. Mean distances .8638, .8312, .8079 respectively. The learned design has better average alignment but substantial residual error and lower J. This is preliminary and not evidence of algorithm superiority.

Frozen iid-designed policies under AR(1) returns: design minus raw J=−.03813 (batch SE .00027), compared with +.00713 (SE .00018) under Gaussian iid. Neither frozen iid policy is asserted optimal under dependence.

## Corrections to the delivered proposal/paper

- Squared increments penalise second moment, not variance. Conditional variance rewards differ.
- Additive objectives admit Bellman optimisation on an adequate Markov state. Their mere additivity is not time inconsistency.
- Precommitment and equilibrium are different targets. Log growth is a valid separate objective.
- Analytic dollar holdings are unconstrained; simplex experiments require separate reference policies.
- Signed financial-value differences are not three nonnegative error terms. Report nonnegative surrogate regret separately.
- nu<1 needs positive-definite covariance; uniqueness requires nonzero mean. Single-period matching needs a positive feasible penalty and only matches at initial wealth.
- The global Lambda bound is false as κ→0. The local expansion is now proved.
- General-horizon coefficient is no longer open; old approximate linear-in-horizon wording is withdrawn.
- DSR state-dependent scaling cannot be discarded in a dynamic optimisation. Fixed-decay EWMA is not consistent.
- Volatility clustering is dependent; t(4) fourth-moment uncertainty was problematic. Revised stress uses t(8).
- The old 519-case / 93.1% claims had no delivered generator/output and are withdrawn.
- Sharpe now subtracts x0 times compounded risk-free growth. Learning rate is .02, not .03.
- Broad novelty statements are removed. Dai et al. explicitly learn equilibrium, while Bisi/Zhang explicitly analyse risk objectives/reward transformations.

See proposal.pdf for the research case, paper.pdf and notes/PROOFS.md for derivations, IMPLEMENTATION_REPORT.md for protocols, literature/LITERATURE_LEDGER.md for exact comparisons, and results/experiments.json for every current numerical claim.


## RL extension — 9 October 2026 (separate from frozen IAFM submission)
See RL_EXTENSION_REPORT.md and notes/rl-extension/RESIDUAL_CERTIFICATE.md. Proved under finite exogenous regimes: actor/reward/critic residual certificate for one-step terminal-MV deviation, invariant to critic constants; convex-action corollary. Candidate novelty remains OPEN relative to recent equilibrium-RL and seminorm theory. Numerically verified2160tabular records and405neural checkpoints. Five-seed neural pilot:61.0% distance and81.6% deviation reduction vsmyopic comparator; centredvsordinary continuationcritic adds only1.48%/2.91%. Preliminary, not a published-algorithm replication or real-dataoutperformance. Independent-data certification feasible butsample-heavy; bestexploratorymeanbound.004911 vsactual.000902. Existing finance conclusions unchanged.
