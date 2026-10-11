# Historical extension — completed 27 September 2026

## Scope and status

| Result | Status | Evidence |
|---|---|---|
| Fixed-horizon optimal scalar mismatch coefficient | proved; publication priority not certified | notes/PROOFS.md, original exact experiments |
| Terminal-unit independent-return equilibrium reward | proved; implements prior control ideas | notes/PROOFS.md, prior-variance mapping tests |
| Joint constrained risk/cost calibration identity | proved; corollary of existing mean auxiliary | notes/CONSTRAINED_CALIBRATION.md |
| Penalty-only effective cost distortion | proved | same note, regression test |
| Historical joint-reference alignment | numerically verified | 432 months, 17 settings; maximum setting-mean distance1.5354e−7 |
| Existing MVPI-reference alignment | numerically verified in primary setting | results/historical/primary.json |
| Realised investment superiority | not established | all three principal paired MV intervals include0 |
| Finite-budget softmax diagnosis | preliminary | five seeds; contextual optimisation, not out-of-sample neural generalisation |
| True dependent historical terminal equilibrium | open | rolling one-period study does not establish it |
| Unrestricted/infinite-action DSR claims | open | earlier bounded DSR results unchanged |
| Universal novelty / priority | open | specific prior comparisons verified; access gaps recorded |

## Data and implementation

Two original French ZIPs are in data/raw; retrieved26September2026, current202608vintage. Returns1970–2025, test1990–2025. A current revised data vintage cannot simulate point-in-time availability of all constituent data. The ten research industry portfolios do not model internal portfolio construction/execution costs. The README links the provider; hashes are in results/september26_downloads.json. See notes/REAL_DATA_PROTOCOL.md for fixed primary and robustness settings.

mvrl/historical.py adds parsing, strict lagged moments, simplex/L1-cost convex optimisation, independent linear-programme certificates, adapted MVPI, log-utility comparisons, separate common-state audit/own-state paths, moving-block bootstrap and17-setting cached robustness. Four new tests bring pytest to31;10original verification checks also pass. The solver now rejects infeasible retry candidates and certifies accepted quadratic iterates. Primary maximum saved common-state certificate4.2675e−9.

mvrl/historical_learning.py adds five-seed direct softmax policy optimisation on each historical fitted state. There is no held-out cross-state generalisation claim and no reproduction of published PPO/DDPG/DPG architectures. Each state only sees its past return estimates. Identical initialisations and budgets across target/raw/joint allow finite-budget comparison. At5000steps own-reward gaps around4e−6 exceed the raw design gap1.48e−6. The signed target decomposition holds exactly; own-reward suboptimality is reported separately.

scripts/check_historical.py independently reconstructs constraints, drift, costs, lag dates, common-state distances/regrets, summaries and signed decomposition from saved results. It verifies4320primary decisions,17robustness summaries and60learning records. Full raw paths for each robustness case are saved for inspection, not just selected summary statistics.

## Literature and attribution

21-paper ledger, exact locators/access notes in literature/LITERATURE_LEDGER.md and ledger.json. Five recent additions span2024–2026, including Management Science, International Review of Economics and Finance, Global Finance Journal, Annals of Operations Research and an explicitly labelled NBER working paper. Foundational Mathematical Finance and Review of Financial Studies references remain necessary. The paper contrasts positive objective-aware methods with adapted reward designs; it does not say the whole financial-RL literature neglects objectives. The joint calibration identity is not claimed to outperform MVPI, and the reference-dependent formula is not a computational shortcut.

## Main historical numbers

Mean allocation distance: raw.008430, unconstrained scalar.005402, risk-only.005103, log-minus-variance.012860; joint and MVPI numerical0. Raw mean fitted monthly MV gap1.4801e−6. Joint minus raw realised monthly MV: −1.3151bp,95%CI[−3.3184,.3429]bp. Joint minus scalar:.3850bp,CI[−.5703,1.3515]bp. Joint minus risk-only:−.1315bp,CI[−.8886,.6337]bp. Paired circular block bootstrap12months,1000repetitions. Intervals condition on realised policy-return paths; no estimator refitting uncertainty claimed.

Minimum variance beats the fitted target in both realised MV and Sharpe in the primary sample. Equal weight beats target Sharpe but loses on realised MV. Precise fitted alignment is useful for interpretability; it does not solve estimation risk.

## Reproduction

From the canonical project root with PYTHONPATH=.: install requirements.txt; torch is optional for the contextual diagnostic. Run `python -m pytest -q`; `python -m mvrl.verify`; `python -m mvrl.historical --robust`; `python -m mvrl.historical_learning`; `python scripts/make_historical_figures.py`; `python scripts/check_historical.py`.

Historical runner intentionally reuses saved caches. To rerun after changing data/objectives, move results/historical to a dated archive first, then rerun; do not mix old cached runs with changed code. Saved seeds and data hashes specify this run. Original synthetic experiments remain unchanged. The current manuscript is in `manuscript/`; earlier versions remain in Git history.
