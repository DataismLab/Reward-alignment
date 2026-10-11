# Certifying Reward Alignment in Portfolio Reinforcement Learning

Research code, proofs, experiments and the final IAFM manuscript for checking whether a portfolio reward and its learned policy implement a specified financial objective.

**Current research version: 9 October 2026. Repository updated: 11 October 2026.**

- [Final anonymous paper (PDF)](submissions/iafm/paper.pdf) · [LaTeX source](submissions/iafm/paper.tex)
- [Research and implementation report](FINAL_RESEARCH_REPORT.md)
- [What changed and why the contribution shifted](RESEARCH_EVOLUTION_REPORT.md)
- [Covariance, factor and financing report](COVARIANCE_RESEARCH_REPORT.md)
- [Findings and assumptions](FINDINGS.md) · [39-paper literature ledger](literature/LITERATURE_LEDGER.md)

The current paper has eight pages, 29 references, three figures and two tables. Earlier root-level papers/proposals and other workshop editions are preserved historical versions. The canonical manuscript is **`submissions/iafm/paper.tex`**.

## What the project establishes

The main result bounds a learned policy's **one-step financial deviation gain**: the improvement obtainable by changing one decision while retaining its future policy. In a finite exogenous-state market, actor/reward gradients and continuation-critic residual spans give an upper bound without requiring the solved equilibrium policy. The proof covers vector returns and convex action constraints under the stated assumptions. The independent-data implementation is scalar and requires a fixed policy, independent conditional samples and known bounded return support.

Earlier exact reward-mismatch and calibration results remain part of the study. A separate historical audit crosses six covariance estimators with 10, 30 and 49 industry portfolios, separating fitted-model changes, reward changes and realised performance.

| Evidence | Result |
|---|---|
| Shared neural actor–critic: 9 markets, 20 seeds, 3 variants | Continuation-aware centred variant reduces mean policy distance **59.2%** and maximum deviation gain **81.4%** relative to the matched myopic learner |
| Clipped PPO: 2 markets, 10 seeds, 2 reward arms | Continuation correction reduces distance **33.3%** and maximum feasible deviation gain **49.8%** |
| Historical covariance/reward audit: 18 configurations, 432 months | Joint calibration preserves its own fitted target, with mean allocation distance below **1.60e−7** |
| Final verification | **78 tests**; 1,660 final neural/PPO records reconstructed with maximum discrepancy **4.44e−16** and zero tested certificate violations |

Budgets are matched within each learning comparison, not between neural and PPO panels. Historical alignment does **not** establish better investment returns. The new RL learners have not been backtested on the French industry data. The backward learner, MVPI auxiliary, critic centring and concentration inequalities build on credited prior work; no universal algorithm-superiority or first-ever priority claim is made.

## Install and test

Use Python 3.10 or newer in a virtual environment. The full research extras include PyTorch, Gymnasium, Stable-Baselines3, pandas, plotting and covariance-validation dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[research,test]'
python -m pytest -q
```

For older document-rendering workflows, also install `requirements-dev.txt`. The exact environment used for the final RL runs is recorded in [final-environment.txt](results/rl-extension/final-environment.txt). It is an evidence record of the original run; the package metadata declares supported minimum dependencies.

The core package requires only NumPy/SciPy. Running the **complete** suite requires the research extras; a lightweight installation can skip optional PPO tests or lack historical/covariance dependencies.

## Reproduce and verify the current results

Run commands from the repository root. Original fixed protocols are in [notes/rl-extension](notes/rl-extension) and [COVARIANCE_PROTOCOL.md](notes/COVARIANCE_PROTOCOL.md). Runners reuse completed cached outputs. To retrain, work in a separate copy and move the corresponding output directory aside; do not mix partially changed settings with existing caches.

### RL evidence

```bash
# Reconstruct every final saved neural/PPO policy; regenerate numbers and figures.
python scripts/finalise_rl_results.py

# Reuse caches or train the unchanged final protocols.
python scripts/run_neural_final.py
python scripts/run_ppo_alignment.py

# Earlier tabular study and independent-data audit/refinement.
python scripts/run_equilibrium_audit.py
python scripts/run_certificate_refinement.py
```

The final neural outputs contain 540 runs × three checkpoints = 1,620 records. PPO adds 40 runs. [final_summary.json](results/rl-extension/final_summary.json) records all means, paired seed-bootstrap intervals and reconstruction checks. Saved actions and critics are included; optional SB3 model ZIPs are excluded and can be regenerated by retraining.

The five-seed neural pilot remains under `results/rl-extension/neural/`; the final twenty-seed study is under `neural-final/`. Pilot figures and reports must not replace the final manuscript numbers.

### Historical and covariance evidence

```bash
python scripts/check_historical.py
python scripts/verify_dimensions.py
python scripts/verify_covariance_audit.py
python scripts/verify_covariance_simulation.py

# Reuse caches or calculate all six estimators for each universe.
python scripts/run_covariance_audit.py --assets 10
python scripts/run_covariance_audit.py --assets 30
python scripts/run_covariance_audit.py --assets 49
python scripts/run_covariance_simulation.py
python scripts/run_financing_audit.py

# Render the final covariance figure from saved results.
python scripts/plot_final_covariance.py
```

The checks reconstruct 58,320 covariance-study decisions and 2,160 known-covariance fitted problems. Historical estimates use the previous 120 monthly observations; evaluation runs from January 1990 through December 2025. The public input ZIPs in `data/raw/` are the archived August 2026 Kenneth French vintage. These revised research portfolios are not a point-in-time investable stock universe. Source information and hashes are retained in the historical manifests.

## Build and check the paper

```bash
cd submissions/iafm
tectonic paper.tex --keep-logs
cd ../..
python scripts/check_current_submission.py
```

A normal LaTeX/BibTeX workflow also works with the supplied ACM class/style and figure assets. The paper checker uses pypdf (`python -m pip install pypdf`). It checks the eight-page limit, anonymity, citation placeholders, expected figures/tables, source inputs and numerical macros. The saved PDF was visually reviewed and independently rebuilt from its portable source archive.

The source is edited directly. Legacy multi-workshop generators are historical tools; guards prevent them from replacing the current IAFM manuscript. `scripts/package_iafm_revision.py` packages the current paper into the parent directory. Other packaging scripts likewise create local delivery archives rather than publishing them.

## Repository map

| Path | Contents |
|---|---|
| `mvrl/` | Independent/dependent market benchmarks, fitted historical allocation, covariance/financing methods, RL learners and certificates |
| `tests/` | Analytical, independent numerical, data-accounting and learning tests |
| `scripts/` | Experiment runners, independent reconstruction, figures and document tooling |
| `data/raw/` | Archived public monthly portfolio/factor input ZIPs |
| `results/historical/` | Original historical, dimension and covariance audits |
| `results/covariance_simulation/` | Known-population covariance experiments |
| `results/rl-extension/` | Tabular, pilot, final neural/PPO and independent-audit evidence |
| `notes/` | Proofs, fixed protocols, reading records and assumptions |
| `literature/` | Version-specific comparison ledger and provenance; downloaded newer papers are not redistributed |
| `submissions/iafm/` | Current anonymous source, PDF, tables and figures |
| `archive/` | Preserved earlier manuscript/research states |

## Scope and remaining research

The certificate bounds local equilibrium deviations, not global-policy regret. Conditional moments or qualifying audit samples are required; a nonpositive variance lower bound produces an uninformative bound. The current learned policies use one risky asset and two observed regimes. Multi-asset neural learning, hidden regimes, dependent historical audit samples, chronological real-data RL, broader hyperparameter checks and full matched SPERL/DPG-FPI reproductions remain extensions.

The [evolution report](RESEARCH_EVOLUTION_REPORT.md) explains why the main contribution shifted from calibration of a known optimum to certification of a learned policy, and evaluates both the benefits and the trade-offs. The covariance work remains supporting evidence. Required author declarations and submission handling are separate from this code repository; no upload to a workshop is performed by the reproduction commands.
