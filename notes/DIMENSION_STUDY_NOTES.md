# Dimension study — 1 October 2026

This note records the 1 October finance revision. The current manuscript and later RL results are described in `FINAL_RESEARCH_REPORT.md`.

## Scientific changes

- Stronger finance foundations: Markowitz (1952 JF), DeMiguel/Garlappi/Uppal (2009 RFS), Gârleanu/Pedersen (2013 JF), Ledoit/Wolf (2017 RFS), DeMiguel/Martín-Utrera/Uppal (2024 JF). Existing recent 2024–2026 financial-learning papers retained. Read versions, precise locators and comparison roles: `literature/finance-foundations/records.json` and the main 27-record ledger. These are five literature additions, not five new algorithm replications.
- DGU (2009) Table 2 uses ten industries plus the market; Proposition 1/Figure 1 address dimension relative to estimation length. It does not demand large portfolios. Its 3000/6000-month numbers are model-dependent examples. Its Section 6.1 also considers finer industry/size-value classifications. Our common-environment extension uses N=10/30/49, without claiming exact replication.
- Dimension protocol fixed before new outcomes: `DIMENSION_PROTOCOL.md`. Same August 2026 vintage, 120-month past-only window, phi=5, 10bp L1 cost, 10% diagonal covariance shrinkage, simplex, 432 months (1990–2025). Added 6048 decisions for 30/49; reused 3024 comparable ten-industry decisions. All available in `results/historical/dimensions/`.
- Joint mean allocation distances: 1.40e-8, 7.33e-8, 1.29e-7. Raw: .00843/.01852/.02079. Scalar: .00540/.02183/.05354. Scalar correction worsens alignment at N=30 and N=49. These are NUMERICALLY VERIFIED within the stated experiments.
- Joint minus raw realised monthly MV: −1.315/−5.216/−5.670 bp. Path-bootstrap intervals: [−3.318,.343], [−10.044,−.903], [−10.747,−.882]. These are PRELIMINARY historical comparisons; intervals are unadjusted and universes overlap. Joint minus 1/N intervals all include zero. Minimum variance gives the highest realised MV of the seven methods in each universe. The larger-universe results contradict any broad claim that alignment improves investment performance, and the manuscript reports this explicitly.
- Original proof results unchanged: exact best-scalar leading mismatch is the candidate theoretical increment; no exhaustive novelty certificate. Joint historical calibration is PROVED as a corollary of the existing MVPI identity and requires the target mean. Existing MVPI also computes the target. The contribution is a quantified reward audit and validated correction, not a superior estimator, investment algorithm or new general equivalent-objective theorem.

## Code and verification

`mvrl/historical.py`: optional dimension selection with original default 10; date-bounded parser rejects missing in-window values and checks every expected month. `scripts/run_dimensions.py`: fixed-protocol extension, summaries, bootstrap, hashes. `scripts/verify_dimensions.py`: independent reconstruction from saved actions and original returns; all 9072 decisions verified. Max return error 4.17e-17, turnover error 2.56e-16, fitted-gap error 3.47e-18, calibration-identity error 7.38e-18. `tests/test_dimensions.py`: dimension/calibration and missing-date/block-boundary checks. All 35 tests pass.

Reproduce from project root with a scientific Python environment:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH=. python -m pytest -q
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH=. python scripts/run_dimensions.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH=. python scripts/verify_dimensions.py
```

Existing raw files and ten-industry results were preserved. No PPO/DDPG architecture, predictive generalisation experiment, N>L case, point-in-time constituents or exact execution-cost model added. These are scope boundaries, not unfinished steps hidden in this revision. Report V2 remains the earlier ten-industry implementation report; this note documents its new dimension extension.
