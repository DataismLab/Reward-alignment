# Kolm–Ritter (2025): full-text reading and integration

Read on 9 October 2026 from the complete journal PDF. All 15 PDF pages were read, including all three exhibits, the conclusion and references. Printed pagination is 81–95; PDF page k corresponds to printed page 80+k. This supersedes the earlier abstract-only record. The separately read CFA chapter is a different publication.

**Exact reference:** Petter N. Kolm and Gordon Ritter. 2025. “Reinforcement Learning for Asset and Portfolio Management.” *The Journal of Portfolio Management* 52(2), 81–95. DOI: [10.3905/jpm.2025.1.782](https://doi.org/10.3905/jpm.2025.1.782). The title and authors agree with the supplied final journal PDF; the previously verified publisher metadata supplies volume, issue and DOI. The local source path, SHA-256 and reading coverage are recorded in `literature/covariance-update/kolm2025-fulltext-manifest.json`.

## What kind of paper this is

On printed p. 82 the authors explicitly describe their goal as an accessible, equation-free educational overview. They do not present a new algorithm, reward formula, dataset or backtest. They also distinguish their article from an exhaustive survey. The three exhibits illustrate the agent/environment cycle, an application workflow and a qualitative summary of strengths/challenges/recommendations. None is an experimental performance table.

This matters for our comparison: it is a recent journal source for the problem and the practical role of our audit, not a numerical strategy against which we can claim outperformance. The existing Kolm–Ritter 2019 table row remains a separately identified adaptation of the earlier technical paper. It must not be relabelled “2025.”

## Complete comparison record

| Field | Finding from the full article |
|---|---|
| Problem | Explain when RL is useful for sequential financial decisions, and what practitioners need for adoption. |
| Financial objective | Multiple mandates: trading cost, hedging risk, portfolio performance, drawdown/risk preferences and investor-specific objectives. No single objective defines a new strategy in this article. |
| Reward used | Conceptual examples include PnL, risk-adjusted return, variance reduction, costs and preferences (p. 83; pp. 89–91). No operational equation or calibration coefficient is supplied. |
| Algorithm used | Reviews RL/DRL, actor–critic/PPO, recurrent methods and inverse RL through cited applications. No original algorithm implementation or tuned configuration. |
| Market/data | No new market dataset. Discusses historical data, market simulation and examples from other studies. |
| Evaluation metric | Discusses objectives and reported benefits of other work; does not calculate an original Sharpe, MV score, turnover, allocation error or confidence interval. |
| Main result | Qualitative recommendations: use RL for genuinely sequential problems, combine it with strong forecasts/classical structure, validate simulators and align rewards with mandates. |
| Does it study what the reward optimises? | Yes, explicitly at a conceptual level: poor reward choices can produce unintended behaviour (p. 90), and rewards should represent investor objectives (p. 91). It does not derive a reward-to-policy equivalence or quantitative mismatch theorem. |
| Does it address time inconsistency? | Discusses intertemporal trade-offs and delayed rewards, but contains no formal precommitment/equilibrium or terminal-MV time-consistency analysis. These concepts should not be conflated. |
| Known benchmark? | Discusses earlier known-policy benchmarks, especially Brini–Kolm on p. 87 and hedging examples on p. 86. It does not construct or test a new benchmark itself. |
| Direct connection to our work | Our scoped analytical and numerical audit makes the mandate/reward relationship testable under fixed beliefs, costs and constraints. It is a concrete response to their recommendation, not the first recognition of reward alignment or known-policy validation. |

## Page-by-page reading map

| Printed pages | Content and relevance |
|---|---|
| 81–82 | Key findings, abstract and introduction. Classical structure and learned policies are complementary; the article's nontechnical scope is explicit. |
| 83 | RL ingredients and Exhibit 1. Reward examples span genuinely different preferences. Different induced allocations do not alone establish that a reward is defective. |
| 84 | Exhibit 2: state definition, action definition, reward specification, training and deployment/adaptation. This gives a concrete location for a reward-to-mandate check before training. |
| 84–85 | Why sequential dynamics, feedback and delayed consequences motivate RL; start of trading applications. This does not justify calling our rolling static optimiser a sequentially optimal RL policy. |
| 85–86 | Trading and hedging applications, including frictions and the earlier 2019 Kolm–Ritter study. These are accounts of other papers, not new performance evidence. |
| 87–88 | Portfolio allocation, prior known-policy validation, forecasts and scalability. Large non-RL portfolio optimisation already exists; our 49-industry/100-asset checks are not proof of scalable learned control. |
| 88 | Inverse RL infers objectives from actions. Our method instead takes a stated mandate as an input and checks its implementation. |
| 88–89 | Benefits and flexibility of RL, including simulation and alternative objectives. Choice of MV is a declared benchmark preference, not a claim that every financial reward should optimise MV. |
| 89–90 | Data efficiency, overfitting, reward design, interpretation and scalability. Reward design is explicitly recognised as a prior problem. |
| 90–91 | Practitioner recommendations. Static problems may favour classical optimisation; simulator validity, mandate alignment and forecast quality all matter. This directly motivates keeping estimation, reward design and numerical error separate. |
| 91–93 | Outlook and Exhibit 3 (p. 92): hybrid approaches, richer states, reproducible benchmarks, continual learning and simulator development. These are a research agenda, not established performance guarantees. |
| 93–95 | References. Relevant follow-up leads include Brini–Kolm on PPO and Sood et al. on matched-objective MVO comparisons. Their primary papers would need separate verification before attributing equations or numerical results to them. |

## How the current manuscript uses it

1. **Introduction:** cites pp. 90–91 for the already recognised mandate-alignment problem. Our question is how to test the correspondence, not whether we were first to notice it.
2. **Related work:** uses pp. 82, 84, 87 and 90–92 plus Exhibits 2–3. It identifies the article as conceptual guidance with no new empirical comparator and acknowledges that known-policy validation has precedents.
3. **Dimension interpretation:** cites pp. 88 and 90 to distinguish our covariance/alignment robustness checks from institutional-scale RL learning.
4. **Section 7:** inserts an explicit audit between reward specification and training: fix the financial mandate and information; compare its optimum with the reward optimum; separately evaluate the learner's numerical error; record changes to risk estimates and constraints. The paper presents this as our proposed use of the audit, not an experiment measuring its effect on an end-to-end training pipeline.
5. **Section 7's practical interpretation:** connects the distinction between forecasts and decisions (p. 91) to our result that exact fitted alignment does not imply superior realised investment performance. It explains why using the direct optimiser is reasonable when the reference is tractable (p. 90).
6. **Novelty boundary:** explicitly distinguishes given-mandate validation from inverse preference inference (p. 88). No first-reward-alignment, first-known-benchmark or new-general-MVPI claim follows from this reading.

The abstract was also tightened: joint scaling is stated as a sufficient reference-preserving construction. The earlier phrase “only when” could imply a universal necessity theorem, which we do not prove—special cases can retain the same maximiser without every coefficient change. The algebra and numerical results are unchanged.

## What this changes about the contribution

The stronger positioning is: a recent finance-journal article explains why reward design must reflect the investment mandate; our study supplies exact tests, calibrated constructions and error bounds for specified mean–variance settings, then checks them across costs and covariance models. We can diagnose which decision change arose from estimated risk, a different reward preference or incomplete optimisation.

This supports the relevance of the project without granting it automatic novelty. The exact terminal mismatch coefficient remains the specific theoretical increment under its stated assumptions. The constrained identity and one-step update remain applications of established MVPI. The new full text contains no formula contradicting these results and no original numerical experiment that can be reproduced as a “Kolm–Ritter 2025 baseline.” That is a statement about this article, not an exhaustive prior-art conclusion.

## What did not change

No investment algorithm, estimator, dataset, hyperparameter, numerical result or figure changed in this revision. There was no reason to rerun the historical experiment merely to add a conceptual reference. The previously verified 50 tests, 58,320 historical records, 2,160 simulated problems and 50 financing states retain their existing evidence dates. Manuscript compilation, citations, anonymity, page count and visual layout are checked again after the text edits. The literature ledger and access-status notes now record the completed full-text reading.

The source PDF is not included in the LaTeX or code delivery archives. Those archives contain our citations and analysis, not redistributed journal content.
