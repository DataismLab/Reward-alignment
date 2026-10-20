# Reward Alignment

**Certifying Reward Alignment in Portfolio Reinforcement Learning**

Reference implementation and experiment outputs for auditing whether a portfolio reward and its learned policy implement a terminal mean–variance objective.

The implementation separates reward-design error, learning error and covariance-estimation error. It includes exact policy benchmarks, continuation-aware actor–critic and PPO experiments, residual-based deviation certificates, and historical allocation comparisons with trading costs.

## Installation

Python 3.10 or newer is required. Use a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[research,test]'
python -m pytest -q
```

The core package depends on NumPy and SciPy. The `research` extra adds pandas, Matplotlib, scikit-learn, PyTorch, Gymnasium and Stable-Baselines3. The complete test suite requires these extras. Package versions used for the final learning experiments are recorded in `results/rl-extension/final-environment.txt`.

## Experiments

| Study | Configuration | Saved outputs |
|---|---|---|
| Exact reward benchmarks | Independent and observed-regime returns; scalar calibration, terminal-unit rewards and constrained comparisons | `results/experiments.json` |
| Tabular learning | Nine markets × four sample budgets × twenty seeds × three methods | `results/rl-extension/tabular_runs.csv` |
| Neural actor–critic | Nine markets × twenty seeds × three methods; checkpoints at 250, 1,000 and 3,000 updates | `results/rl-extension/neural-final/` |
| PPO reward intervention | Two markets × ten seeds × two reward arms; 32,768 environment steps per run | `results/rl-extension/ppo-final/` |
| Historical allocation | Seven covariance estimators × 10, 30 and 49 industry portfolios; 432 evaluation months | `results/historical/covariance/` |
| Known-covariance simulation | 2,160 fitted problems; dimensions 10, 49 and 100; two estimation windows and two residual structures | `results/covariance_simulation/` |

The final neural comparison reduces mean policy distance by 59.2% relative to the matched myopic-reward learner; the separate PPO comparison reduces it by 33.3%. Budgets are matched within each experiment. These are controlled-market alignment results, not evidence of superior historical investment returns.

The covariance comparison includes sample covariance, fixed diagonal shrinkage, Ledoit–Wolf identity and constant-correlation linear shrinkage, the 2017 QuEST nonlinear estimator, and market/three-factor models. The known-covariance simulation retains its original six estimators; nonlinear shrinkage was added to the historical study separately.

Historical joint calibration preserves its fitted target across all twenty-one estimator/universe configurations. It does not establish better realised mean–variance performance. The historical allocation study is separate from the new RL learners.

## Verify the saved results

Run commands from the repository root:

```bash
python scripts/check_outputs.py
python scripts/check_historical.py
python scripts/verify_dimensions.py
python scripts/verify_covariance_audit.py
python scripts/verify_covariance_simulation.py
python scripts/verify_quest_grid.py
python scripts/finalise_rl_results.py
```

These checks reconstruct quantities from raw returns and saved policies. They cover 4,320 primary historical decisions, 9,072 dimension-study decisions, 67,392 covariance-study decisions, 2,160 known-covariance problems and 1,660 final neural/PPO records. The final learning reconstruction has maximum discrepancy 4.44e−16 and no tested certificate violations.

`finalise_rl_results.py` also writes numerical tables and figures to `results/paper_assets/`. `plot_final_covariance.py` generates the corresponding historical comparison figure. These are generated research outputs; manuscript and submission-preparation files are maintained separately.

## Run experiments

```bash
# Final learning comparisons.
python scripts/run_neural_final.py
python scripts/run_ppo_alignment.py

# Tabular study and independent-data certificates.
python scripts/run_equilibrium_audit.py
python scripts/run_certificate_refinement.py

# Historical covariance comparisons.
python scripts/run_covariance_audit.py --assets 10
python scripts/run_covariance_audit.py --assets 30
python scripts/run_covariance_audit.py --assets 49

# Known-covariance and financing experiments.
python scripts/run_covariance_simulation.py
python scripts/run_financing_audit.py
```

Nonlinear covariance fits are cached by source-and-input hash in `results/historical/covariance/quest_cache/`. The included 1,296 past-window fits allow the historical reconstruction to run without repeating the nonlinear optimisations. `scripts/verify_quest_grid.py` checks six fixed endpoint windows against a finer integration grid. `scripts/verify_quest_optimizer.py --upstream /path/to/LedoitWolf-QuEST` optionally compares fits with the upstream optimiser; the pinned upstream tree is recorded in `mvrl/_vendor/quest/NOTICE.txt`.

The final neural, PPO and historical covariance runners reuse saved outputs when present; other runners may recompute and overwrite their outputs. For a fresh experiment, use a separate checkout and move the relevant output directory aside. Do not reuse old caches after changing a protocol. Seeds and numerical settings are specified in the runners. The five-seed neural pilot is retained in `results/rl-extension/neural/`; the paper's final results use `neural-final/`.

Saved actions, critics and metrics are included. Optional Stable-Baselines3 model ZIPs can be regenerated by retraining. Source-hash and environment records describe the original runs; later documentation and output-path changes do not change those recorded experiments.

## Data and evaluation

`data/raw/` contains the archived August 2026 vintage of Kenneth French's monthly industry portfolios and market, size and value factors. Data provenance is recorded in `results/september26_downloads.json` and the historical manifests. The main historical comparisons estimate moments from the preceding 120 months and evaluate January 1990 through December 2025, with a long-only simplex constraint and 10-basis-point proportional turnover costs. The archived research portfolios are not a point-in-time investable stock universe.

Policy distance, financial deviation gain, fitted-objective loss and optimisation certificates are evaluated separately from realised returns and Sharpe ratios. Paired learning comparisons resample seed averages. Historical uncertainty uses shared circular twelve-month blocks conditional on the realised strategy paths.

## Code layout

| Path | Purpose |
|---|---|
| `mvrl/` | Market models, analytic references, allocation solvers, covariance estimators, learners and certificates |
| `tests/` | Independent mathematical, numerical, data-accounting and learning checks |
| `scripts/` | Fixed experiment runners, output reconstruction and scientific figures |
| `data/raw/` | Archived public input data |
| `results/` | Experiment records, policies, critics and verification outputs |
| `figures/` | Generated figures for the original benchmark |
| `archive/` | Historical Python implementations, retained for provenance and excluded from current experiments |

## Scope

The certificate bounds the gain from a one-step deviation under the stated finite exogenous-state assumptions; it is not global-policy regret. Its independent-data version requires a fixed policy and critic, independent conditional observations and known return bounds. A nonpositive variance lower bound yields no finite certificate. The current neural experiments use one risky asset and two observed regimes. Multi-asset neural learning, dependent historical audit samples and a chronological real-data RL backtest remain outside the reported implementation.

## Third-party code

The vendored QuEST implementation is distributed under GPL-3.0; its licence and provenance are retained in `mvrl/_vendor/quest/LICENSE` and `NOTICE.txt`. The fitted covariance wrapper implements the 2017 Ledoit–Wolf nonlinear estimator; it does not reproduce their original CRSP backtest.
