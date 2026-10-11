# Primary-paper comparison ledger

Updated 7 October 2026: 33 records. Locators identify the version actually inspected. Full-text access limitations are explicit. Reported results of external papers are not replications by this project. Download manifests and detailed records remain in their literature subdirectories.

| ID | Verified citation | Access / version | Relation to this project |
|---|---|---|---|
| kolm2019 | Petter N. Kolm; Gordon Ritter (2019). [Dynamic Replication and Hedging: A Reinforcement Learning Approach](https://doi.org/10.3905/jfds.2019.1.1.159). The Journal of Financial Data Science 1(1), 159–171. | 16-page author manuscript at smallake.kr; figures are missing in this manuscript. Text and equations read; journal PDF unavailable. | Closest raw-reward baseline. We isolate policy mismatch in a different allocation benchmark; do not infer failure of their hedger. Published κ/2=.05 is a units-sensitive diagnostic only. |
| jiang2017 | Zhengyao Jiang; Dixing Xu; Jinjun Liang (2017). [A Deep Reinforcement Learning Framework for the Financial Portfolio Management Problem](https://arxiv.org/abs/1706.10059). arXiv preprint 1706.10059. | arXiv v2, 16 July 2017; saved PDF. | Adapt log growth on an identical bounded action set. Different target preferences explain disagreement; their own growth objective is not mis-specified. |
| yang2020 | Hongyang Yang; Xiao-Yang Liu; Shan Zhong; Anwar Walid (2020). [Deep Reinforcement Learning for Automated Stock Trading: An Ensemble Strategy](https://doi.org/10.1145/3383455.3422540). Proceedings of the First ACM International Conference on AI in Finance (ICAIF), 8 pages. | Columbia-hosted author manuscript; saved PDF. Do not use the later 2025 arXiv upload as a 2020 identifier. | Adapt value increments with zero costs and undiscounted finite horizon. Measures preference alignment; does not reproduce PPO/DDPG or the historical result. |
| moody2001 | John Moody; Matthew Saffell (2001). [Learning to Trade via Direct Reinforcement](https://doi.org/10.1109/72.935097). IEEE Transactions on Neural Networks 12(4), 875–889. | IDSIA-hosted 17-page manuscript, visually read because text encoding is corrupted. | Adapt unscaled DSR on an augmented (wealth,A,B) tree. Original online gradient update is not identical to maximising an undiscounted sum of DSR signals. |
| bisi2020 | Lorenzo Bisi; Luca Sabbioni; Edoardo Vittori; Matteo Papini; Marcello Restelli (2020). [Risk-Averse Trust Region Optimization for Reward-Volatility Reduction](https://doi.org/10.24963/ijcai.2020/632). Proceedings of IJCAI-20, 4583–4589. | Published proceedings PDF, saved and read. | Direct prior art against broad reward-analysis novelty. We compare its per-step criterion with an independently specified terminal equilibrium; do not call its chosen short-term objective wrong. |
| zhang2021 | Shangtong Zhang; Bo Liu; Shimon Whiteson (2021). [Mean-Variance Policy Iteration for Risk-Averse Reinforcement Learning](https://doi.org/10.1609/aaai.v35i12.17302). Proceedings of AAAI 35(12), 10905–10913. | arXiv:2004.10888v6, 7 April 2022; differs in date from published 2021 proceedings. | Finite-horizon uniform-time adaptation added. At zero interest its iid fixed point equals our scalar calibration: that formula alone is not a defensible novelty claim. |
| wang2020 | Haoran Wang; Xun Yu Zhou (2020). [Continuous-Time Mean-Variance Portfolio Selection: A Reinforcement Learning Framework](https://doi.org/10.1111/mafi.12281). Mathematical Finance 30(4), 1273–1308. | arXiv:1904.11392, saved 39-page preprint; section references refer to this version. | Essential positive control: objective-faithful RL already exists. Our discrete reward-family audit asks a different question; no EMV replication claimed. |
| dai2023 | Min Dai; Yuchao Dong; Yanwei Jia (2023). [Learning Equilibrium Mean-Variance Strategy](https://doi.org/10.1111/mafi.12402). Mathematical Finance 33(4), 1166–1212. | NUS RMI Working Paper 2021-02, March 2021, 52 pages, read via web PDF. Local download blocked; journal section numbering not asserted. | Refutes any first-equilibrium-RL claim. Our target is discrete terminal wealth MV and an audit of common rewards, not their log-MV learning problem. |
| ling2000 | Duan Li; Wan-Lung Ng (2000). [Optimal Dynamic Portfolio Selection: Multiperiod Mean-Variance Formulation](https://doi.org/10.1111/1467-9965.00100). Mathematical Finance 10(3), 387–406. | Journal PDF mirrored at tianjiablog.wordpress.com; saved. | Our precommitment reference is established theory. Reward-design comparisons must specify whether this or equilibrium is the intended target. |
| basak2010 | Suleyman Basak; Georgy Chabakauri (2010). [Dynamic Mean-Variance Asset Allocation](https://doi.org/10.1093/rfs/hhq028). The Review of Financial Studies 23(8), 2970–3016. | Author thesis chapter 2, “Dynamic Mean-Variance Asset Allocation”, read; journal full text unavailable. Chapter numbering is not journal numbering. | Foundational benchmark and hedge precedent. Our finite-regime correction is a discrete audit construction, not the discovery of intertemporal hedging or inverse objectives. |
| ng1999 | Andrew Y. Ng; Daishi Harada; Stuart Russell (1999). [Policy Invariance under Reward Transformations: Theory and Application to Reward Shaping](https://ai.stanford.edu/~ang/papers/shaping-icml99.pdf). Proceedings of ICML, 278–287. | Author-hosted 10-page conference paper; visually read due to encoding. No DOI asserted. | Our redesign deliberately changes the raw reward optimum. Policy-invariant shaping cannot by itself correct a mismatched target. |
| bjork2014 | Tomas Björk; Agatha Murgoci (2014). [A Theory of Markovian Time-Inconsistent Stochastic Control in Discrete Time](https://doi.org/10.1007/s00780-014-0234-y). Finance and Stochastics 18(3), 545–592. | Publisher metadata and abstract only; full-text verification OPEN. Not counted as a paper fully read. | Requires conservative novelty: existence of an equivalent reward problem is prior art. Exact theorem-level comparison remains open. |
| czichowsky2013 | Christoph Czichowsky (2013). [Time-consistent mean-variance portfolio selection in discrete and continuous time](https://doi.org/10.1007/s00780-012-0189-9). Finance and Stochastics 17(2), 227–271. | 45-page arXiv:1205.4748 manuscript; relevant full-text sections inspected and saved in novelty-audit/. Publisher metadata verified. | Our scalar observed-regime hedge is a specialisation, with gamma=2phi and terminal-unit increments. Local perturbation and feedback concepts agree here because continuation is wealth-independent; no general equivalence claimed. |
| bkm2016 | Tomas Björk; Mariana Khapko; Agatha Murgoci (2016). [Time Inconsistent Stochastic Control in Continuous Time: Theory and Examples](https://arxiv.org/abs/1612.03650). arXiv preprint 1612.03650v1. | 58-page version submitted 12 December 2016, cover dated 10 January 2016. Related shortened journal paper: On time-inconsistent stochastic control in continuous time, Finance and Stochastics 21 (2017), 331–360, DOI 10.1007/s00780-017-0327-5. Cited propositions belong to the longer preprint. | Existence of a reward implementing equilibrium and terminal-unit variance penalisation are prior ideas. Our sampled second-moment design is a finite-step implementation with a rank-one correction, not a new general principle. Oracle dependence is acknowledged in their §8 too. |
| chaouki2020 | Ayman Chaouki; Stephen Hardiman; Christian Schmidt; Emmanuel Sérié; Joachim de Lataillade (2020). [Deep deterministic portfolio optimization](https://doi.org/10.1016/j.jfds.2020.06.002). The Journal of Finance and Data Science 6, 16–30. | arXiv:2003.06497v2, 9 April 2020; 25-page author manuscript saved. Publisher metadata verified. | Known-policy financial-RL benchmarks and action-distance evaluation are not new. Our additional comparison is reward optimum versus separately specified equilibrium, before learning; no DDPG reproduction is claimed. |
| dixon2020 | Matthew F. Dixon; Igor Halperin (2020). [G-Learner and GIRL: Goal Based Wealth Management with Reinforcement Learning](https://arxiv.org/abs/2002.10990). arXiv preprint 2002.10990v1. | 20-page version, 25 February 2020; saved. No unverified journal venue assigned. | Inferring/designing rewards from target behaviour and quadratic portfolio reward analysis predate us. Our declared equilibrium target and exact raw-family mismatch differ from imitation; no new general inverse-RL method is claimed. |
| simon2026 | Frederik Simon; Sebastian Weibels; Tom Zimmermann (2026). [Deep Parametric Portfolio Policies](https://doi.org/10.1287/mnsc.2025.00721). Management Science, Articles in Advance, 1–19; published 3 June 2026. | Published 19-page PDF read via web; local download 403. DOI contains 2025 but publication is 2026. | Strong positive prior: objective-faithful learning already exists. Our covariance-MV reference implements its MV preference in a different common market, not the full DPPP architecture or stock dataset. |
| jiang2025 | Yifu Jiang; Jose Olmo; Majed Atwi (2025). [High-dimensional multi-period portfolio allocation using deep reinforcement learning](https://doi.org/10.1016/j.iref.2025.103996). International Review of Economics and Finance 98, 103996. | Published PDF from University of Zaragoza repository, saved. | Adapt log-minus-variance preference with common monthly data and hard simplex; first-order costs replace their log cost factor. No architecture or performance replication claimed. |
| jiang2024 | Yifu Jiang; Jose Olmo; Majed Atwi (2024). [Deep reinforcement learning for portfolio selection](https://doi.org/10.1016/j.gfj.2024.101016). Global Finance Journal 62, 101016. | Published PDF from University of Zaragoza repository, saved. | Motivates separate risk/cost coefficients. Do not silently reinterpret the printed portfolio-value term as our excess-return increment or call our code a replication. |
| gollart2025 | Maximilian Gollart; Yarema Okhrin (2025). [A reinforcement learning approach to dynamic portfolio optimization](https://doi.org/10.1007/s10479-025-06649-x). Annals of Operations Research; published online 25 June 2025. | Published 26-page PDF saved; volume/page assignment not asserted. | Recent positive control for objective-first RL and known-policy validation; our task audits a different reward family. |
| cong2026 | Lin William Cong; Ke Tang; Jingyuan Wang (2026). [AlphaPortfolio: Goal-Oriented Investment Management Through Deep Reinforcement Learning](https://doi.org/10.3386/w35195). NBER Working Paper 35195, May 2026. | NBER PDF saved. This version has three authors; do not merge authors/title from the earlier four-author manuscript. No journal publication asserted. | Refutes broad claims that financial RL only uses additive rewards. Our exact audit is complementary; no AlphaPortfolio reproduction. |
| finrobot2024 | Hongyang Yang; Boyu Zhang; Neng Wang; Cheng Guo; Xiaoli Zhang; Likun Lin; Junlin Wang; Tianyu Zhou; Mao Guan; Runjia Zhang; Christina Dan Wang (2024). [FinRobot: An Open-Source AI Agent Platform for Financial Applications using Large Language Models](https://arxiv.org/abs/2405.14767v2). arXiv:2405.14767v2; revised 27 May 2024. | v2 primary PDF read; saved locally. | Motivates tool-boundary validation only; not implemented, evaluated or claimed to fail. |
| markowitz1952 | Harry Markowitz (1952). [Portfolio Selection](https://doi.org/10.1111/j.1540-6261.1952.tb01525.x). The Journal of Finance 7(1), 77–91. | Final journal scan, Berkeley-hosted, 16 PDF pages including cover. | Supplies target/control foundation, not a claimed new objective or empirical algorithm reproduction. |
| demiguel2009 | Victor DeMiguel; Lorenzo Garlappi; Raman Uppal (2009). [Optimal Versus Naive Diversification: How Inefficient is the 1/N Portfolio Strategy?](https://doi.org/10.1093/rfs/hhm075). The Review of Financial Studies 22(5), 1915–1953. | Final 39-page journal PDF linked by Garlappi; advance access 3 December 2007, issue May 2009. | Retain 1/N, add N=30/49 checks at fixed L=120; distinguish estimation from reward mismatch. Not a reproduction of their dates, 14 methods, 50bp costs or normalised tangency portfolios. |
| ledoit2017 | Olivier Ledoit; Michael Wolf (2017). [Nonlinear Shrinkage of the Covariance Matrix for Portfolio Selection: Markowitz Meets Goldilocks](https://doi.org/10.1093/rfs/hhx052). The Review of Financial Studies 30(12), 4349–4388. | Final 40-page journal PDF on ledoit.net. | Motivates objective-specific evaluation and estimation controls. Our 10% diagonal shrinkage is NOT this estimator; no replication or performance superiority claimed. |
| garleanu2013 | Nicolae Gârleanu; Lasse Heje Pedersen (2013). [Dynamic Trading with Predictable Returns and Transaction Costs](https://doi.org/10.1111/jofi.12080). The Journal of Finance 68(6), 2309–2340. | Final 32-page author-hosted journal PDF. | Explains why continuation/cost-aware benchmarks matter. Our rolling one-period L1-cost target is neither their dynamic optimum nor a reproduction. |
| demiguel2024 | Victor DeMiguel; Alberto Martín-Utrera; Raman Uppal (2024). [A Multifactor Perspective on Volatility-Managed Portfolios](https://doi.org/10.1111/jofi.13395). The Journal of Finance 79(6), 3859–3891. | Publisher full text, 27 October 2024. | Positive cost-aware finance example; motivates preserving cost preferences. Not reproduced. |
| kolm2025 | Petter N. Kolm; Gordon Ritter (2025). [Reinforcement Learning for Asset and Portfolio Management](https://doi.org/10.3905/jpm.2025.1.782). The Journal of Portfolio Management 52(2), 81–95. | Publisher metadata and abstract verified in browser, 7 October 2026. Full text requires access and was NOT read. | Motivates hybrid validation; no performance or novelty exclusion inferred from inaccessible text. |
| habibnia2024 | Ali Habibnia; Mahdi Soltanzadeh (2024). [Optimizing Portfolio with Two-Sided Transactions and Lending: A Reinforcement Learning Framework](https://arxiv.org/abs/2408.05382). arXiv:2408.05382v1. | 24-page arXiv v1 PDF and HTML read. | Explicit long-only unit-capital assetwise reward restriction; no SAC, loans or crypto replication. Separate convex-financing theorem/test is not their environment. |
| ledoit2004identity | Olivier Ledoit; Michael Wolf (2004). [A well-conditioned estimator for large-dimensional covariance matrices](https://doi.org/10.1016/S0047-259X(03)00096-4). Journal of Multivariate Analysis 88(2), 365–411. | 47-page journal PDF on ENS Lyon academic host read. | Implemented centred estimator; final covariance multiplied by L/(L−1); checked independently against scikit-learn. No guarantee of realised MV superiority. |
| ledoit2004correlation | Olivier Ledoit; Michael Wolf (2004). [Honey, I Shrunk the Sample Covariance Matrix](https://doi.org/10.3905/jpm.2004.110). The Journal of Portfolio Management 30(4), 110–119. | November 2003 Barcelona Economics Working Paper 92, full PDF read; journal identity checked separately. | Implemented target and fourth-moment intensity; unbiased-unit rescaling; direct elementwise formula test. Different long-only monthly industry environment. |
| fan2008 | Jianqing Fan; Yingying Fan; Jinchi Lv (2008). [High dimensional covariance matrix estimation using a factor model](https://doi.org/10.1016/j.jeconom.2008.09.017). Journal of Econometrics 147(1), 186–197. | 12-page final journal PDF read; 43-page arXiv predecessor also archived. | Market and three-factor adaptations use intercept and residual dof L−K−1, unlike their no-intercept ML residual convention. Correlated-residual simulation tests misspecification. |
| halperin2025chapter | Igor Halperin; Petter N. Kolm; Gordon Ritter (2025). [Reinforcement Learning and Inverse Reinforcement Learning: A Practitioner’s Guide for Investment Management](https://rpc.cfainstitute.org/research/foundation/2025/chapter-6-reinforcement-learning-inverse-reinforcement-learning). Chapter 6 in AI in Asset Management: Tools, Applications, and Frontiers, CFA Institute Research Foundation. | 35-page official chapter PDF read for background; distinct from requested JPM article. | Accessible primary background; not silently substituted for the paywalled JPM article and not needed for its unverified details. |

## kolm2019

- **Exact locator:** “Automatic hedging in theory”, manuscript pp. 7–8, Eqs. (8)–(10), footnote 4; “Automatic hedging in practice”, pp. 9–14, Exhibits 1–5.
- **Problem:** Discrete option hedging with nonlinear trading costs.
- **Financial/statistical objective:** Terminal wealth mean–variance, then a simplified sum of increment variances.
- **Reward:** Δw − (κ/2)(Δw)², explicitly approximate.
- **Algorithm:** Batch fitted action-value learning with one-step SARSA targets and nonlinear regression.
- **Market/data:** Simulated GBM European call; strike/spot 100, 10 days, 5 decisions/day; κ=.1.
- **Evaluation metric:** Hedging P&L, costs, volatility; comparison to delta hedging.
- **Reported result:** Reports lower cost across 10,000 test paths; volatility difference not significant at 99%.
- **Reward/objective analysis:** Yes: explicitly discusses covariance and approximation.
- **Time inconsistency:** Does not formulate a subgame equilibrium in the inspected derivation.
- **Known benchmark:** BSM hedge in frictionless limit; not a solved frictional optimum.
- **Project comparison:** Closest raw-reward baseline. We isolate policy mismatch in a different allocation benchmark; do not infer failure of their hedger. Published κ/2=.05 is a units-sensitive diagnostic only.

## jiang2017

- **Exact locator:** §§2.2–2.4, §4.2 Eqs. (21)–(22), §4.3; Tables 1–2; §6.
- **Problem:** Long-only cryptocurrency allocation with costs.
- **Financial/statistical objective:** Portfolio growth.
- **Reward:** Average log portfolio growth including transaction-cost factor.
- **Algorithm:** Direct gradient ascent; EIIE CNN/RNN/LSTM policies and portfolio-vector memory.
- **Market/data:** Poloniex, 11 noncash assets plus Bitcoin cash, 30-minute decisions; three 2016–2017 backtests.
- **Evaluation metric:** Final accumulated value, Sharpe, maximum drawdown.
- **Reported result:** EIIE variants report leading accumulated values in all three tests (Table 2).
- **Reward/objective analysis:** Yes: log reward corresponds to multiplicative growth.
- **Time inconsistency:** No terminal mean–variance equilibrium objective.
- **Known benchmark:** Trading comparators, no known true market optimum.
- **Project comparison:** Adapt log growth on an identical bounded action set. Different target preferences explain disagreement; their own growth objective is not mis-specified.

## yang2020

- **Exact locator:** §3.3 Eq. (4); §5 ensemble selection; §6.1 and Fig. 4; §6.2.4 and Table 2.
- **Problem:** Automated constrained stock trading.
- **Financial/statistical objective:** Portfolio value growth with costs and turbulence control.
- **Reward:** Change in portfolio value net of transaction costs.
- **Algorithm:** PPO, A2C, DDPG; rolling Sharpe-based ensemble selection.
- **Market/data:** Dow 30 daily WRDS data; training 2009–2015, testing Jan. 2016–8 May 2020.
- **Evaluation metric:** Return, volatility, drawdown, Sharpe.
- **Reported result:** Table 2: ensemble Sharpe 1.30, DJIA .47, minimum variance .45.
- **Reward/objective analysis:** Defines value-change objective; no identity with terminal MV.
- **Time inconsistency:** No equilibrium mean–variance treatment.
- **Known benchmark:** DJIA and minimum-variance comparator, no true dynamic optimum.
- **Project comparison:** Adapt value increments with zero costs and undiscounted finite horizon. Measures preference alignment; does not reproduce PPO/DDPG or the historical result.

## moody2001

- **Exact locator:** §II-D, Eqs. (12)–(17), PDF pp. 3–4; §III-A Eq. (31); §IV-A, Fig. 5; §IV-C.2, Fig. 8.
- **Problem:** Trading and stock/T-bill allocation.
- **Financial/statistical objective:** Risk-adjusted trading performance.
- **Reward:** Differential Sharpe Eq. (14), EWMA updates Eq. (15); also differential downside-deviation reward.
- **Algorithm:** Recurrent reinforcement learning; Q-learning/advantage updating comparisons.
- **Market/data:** Synthetic prices; USD/GBP; monthly S&P500/T-bills with 1970–1994 test period.
- **Evaluation metric:** Profit and Sharpe; downside risk in FX example.
- **Reported result:** §IV-C.2 reports annualised Sharpe .83 for RRL, .63 for Q-trader, .34 buy-and-hold.
- **Reward/objective analysis:** Yes: derives DSR as first-order Sharpe change.
- **Time inconsistency:** No terminal MV equilibrium equivalence.
- **Known benchmark:** Simple market examples; no known optimal real-market policy.
- **Project comparison:** Adapt unscaled DSR on an augmented (wealth,A,B) tree. Original online gradient update is not identical to maximising an undiscounted sum of DSR signals.

## bisi2020

- **Exact locator:** §3 Eqs. (3)–(6); §§4–5, Algorithm 1; §7.1–7.2, Fig. 1(a)–(d).
- **Problem:** Trading with short-term risk control.
- **Financial/statistical objective:** Expected reward minus occupancy-weighted per-step reward variance.
- **Reward:** Trading P&L minus turnover costs; policy-dependent centred quadratic transformation.
- **Algorithm:** Trust Region Volatility Optimization (TRVO), extending TRPO.
- **Market/data:** Daily S&P500 through 2019; minute USD/EUR and USD/JPY, train 2017/test 2018.
- **Evaluation metric:** Mean-volatility and mean-variance frontiers.
- **Reported result:** Fig. 1 reports broader/frontier improvements over exponential rewards; S&P results are in-sample.
- **Reward/objective analysis:** Yes: reward-volatility Bellman/gradient theory and return-variance bound.
- **Time inconsistency:** Distinguishes risk measures; does not target the terminal-MV subgame equilibrium here.
- **Known benchmark:** No closed-form optimum for historical tasks.
- **Project comparison:** Direct prior art against broad reward-analysis novelty. We compare its per-step criterion with an independently specified terminal equilibrium; do not call its chosen short-term objective wrong.

## zhang2021

- **Exact locator:** “Mean-Variance RL”, Eq. (2); “Mean-Variance Policy Iteration”, Eqs. (3)–(4), Algorithm 1, Propositions 1–2; “Experiments”, Table 1.
- **Problem:** Scalable risk-averse RL.
- **Financial/statistical objective:** Discounted-occupancy per-step mean–variance.
- **Reward:** Transformed reward r − λr² + 2λry; y updated by policy evaluation.
- **Algorithm:** MVPI, instantiated with TD3; offline density-ratio variant.
- **Market/data:** Eight noisy-action MuJoCo tasks and an offline benchmark; not financial prices.
- **Evaluation metric:** Risk-aware score, mean, variance, Sharpe-like ratio.
- **Reported result:** Reports strong risk-aware results versus TD3 and risk-averse baselines; not universal dominance on every metric.
- **Reward/objective analysis:** Yes, explicitly distinguishes per-step and total-return variance.
- **Time inconsistency:** No financial subgame-equilibrium target.
- **Known benchmark:** Small illustrative MDP; no closed-form MuJoCo optimum.
- **Project comparison:** Finite-horizon uniform-time adaptation added. At zero interest its iid fixed point equals our scalar calibration: that formula alone is not a defensible novelty claim.

## wang2020

- **Exact locator:** §2 Eq. (11); §3 Theorems 1 and 3; §4; §5.1 Table 1, §§5.2–5.3.
- **Problem:** Learn continuous-time mean–variance allocation.
- **Financial/statistical objective:** Precommitted terminal MV via a mean constraint and quadratic embedding.
- **Reward:** Terminal squared deviation plus entropy regularisation.
- **Algorithm:** Exploratory mean–variance (EMV), policy evaluation/improvement.
- **Market/data:** Simulated GBM parameter grid and nonstationary simulations.
- **Evaluation metric:** Terminal return, variance, Sharpe; algorithm comparisons.
- **Reported result:** §5.1 reports EMV best Sharpe in 23 of 28 tested cases.
- **Reward/objective analysis:** Yes: objective and optimal exploratory control derived.
- **Time inconsistency:** Uses precommitment; not an equilibrium solver.
- **Known benchmark:** Closed-form Gaussian exploratory policy and classical limit.
- **Project comparison:** Essential positive control: objective-faithful RL already exists. Our discrete reward-family audit asks a different question; no EMV replication claimed.

## dai2023

- **Exact locator:** Working version §§2–3, §4.2 Theorem 2; §5 Algorithm 1; §6.1–6.2, Fig. 1.
- **Problem:** Learn equilibrium allocation under stochastic investment opportunities.
- **Financial/statistical objective:** Mean–variance of log returns plus entropy.
- **Reward:** Objective-specific equilibrium TD/policy updates, not arbitrary additive wealth increments.
- **Algorithm:** Exploratory equilibrium policy iteration and parameterised learning.
- **Market/data:** Simulated Gaussian mean-return model; perfect/noisy factor observations.
- **Evaluation metric:** Policy deviation from theoretical solution and convergence.
- **Reported result:** Fig. 1 shows learned policies close to the analytic target, with increased error under observation noise.
- **Reward/objective analysis:** Yes.
- **Time inconsistency:** Yes, explicitly central.
- **Known benchmark:** Semi-analytic equilibrium; closed form in Gaussian factor model.
- **Project comparison:** Refutes any first-equilibrium-RL claim. Our target is discrete terminal wealth MV and an audit of common rewards, not their log-MV learning problem.

## ling2000

- **Exact locator:** §§3–4, Theorems 1–2 (embedding); §5 riskless-asset case.
- **Problem:** Multiperiod portfolio selection.
- **Financial/statistical objective:** Terminal mean–variance at the initial date.
- **Reward:** No RL reward; auxiliary quadratic terminal objective.
- **Algorithm:** Embedding and stochastic linear-quadratic control.
- **Market/data:** Independent, potentially time-varying return moments.
- **Evaluation metric:** Efficient frontier and terminal mean/variance.
- **Reported result:** Analytic optimal policies/frontiers via embedding.
- **Reward/objective analysis:** Analyses the objective transformation, not additive RL rewards.
- **Time inconsistency:** Supplies precommitted optimum, not subgame equilibrium.
- **Known benchmark:** Yes, core exact reference.
- **Project comparison:** Our precommitment reference is established theory. Reward-design comparisons must specify whether this or equilibrium is the intended target.

## basak2010

- **Exact locator:** Thesis chapter 2 §2.2.2, Proposition 2.1, Eqs. (148)–(149); §2.2.2 Remark 1; §2.2.4; discrete-time extension in §2.4.
- **Problem:** Dynamic allocation under stochastic opportunities.
- **Financial/statistical objective:** Time-consistent terminal wealth mean–variance.
- **Reward:** No RL reward; equilibrium control and associated utility interpretation.
- **Algorithm:** Recursive equilibrium analysis and analytic specialisations.
- **Market/data:** Continuous-time incomplete-market models; discrete-time extensions.
- **Evaluation metric:** Policy, hedging demand, terminal moments.
- **Reported result:** Decomposes risky demand into myopic and intertemporal hedging components.
- **Reward/objective analysis:** Discusses objectives giving the same policy (Remark 1).
- **Time inconsistency:** Yes.
- **Known benchmark:** Analytic equilibria in tractable market models.
- **Project comparison:** Foundational benchmark and hedge precedent. Our finite-regime correction is a discrete audit construction, not the discovery of intertemporal hedging or inverse objectives.

## ng1999

- **Exact locator:** §3 Theorem 1, Eq. (2), Corollary 2; §4 Figures 1–2; Appendix A.
- **Problem:** Reward shaping without changing optimal policies.
- **Financial/statistical objective:** Expected discounted reward.
- **Reward:** Potential difference γΦ(s′)−Φ(s).
- **Algorithm:** Policy-invariance theorem; SARSA gridworld examples.
- **Market/data:** Synthetic gridworlds, not markets.
- **Evaluation metric:** Policy invariance and learning steps.
- **Reported result:** Potential shaping preserves optimal policies under stated conditions and can accelerate learning.
- **Reward/objective analysis:** Yes.
- **Time inconsistency:** Not a mean–variance equilibrium treatment.
- **Known benchmark:** Known small MDPs.
- **Project comparison:** Our redesign deliberately changes the raw reward optimum. Policy-invariant shaping cannot by itself correct a mismatched target.

## bjork2014

- **Exact locator:** Publisher abstract only; no theorem number or detailed comparison asserted.
- **Problem:** Markovian time-inconsistent control.
- **Financial/statistical objective:** General time-inconsistent criteria.
- **Reward:** Not extracted from full text.
- **Algorithm:** Game-theoretic extended dynamic programming (abstract).
- **Market/data:** General control setting (abstract).
- **Evaluation metric:** Equilibrium policies and values (abstract).
- **Reported result:** Abstract states an associated time-consistent problem can reproduce equilibrium control and value.
- **Reward/objective analysis:** Abstract supports existence of an equivalent control problem.
- **Time inconsistency:** Yes.
- **Known benchmark:** Not independently extracted.
- **Project comparison:** Requires conservative novelty: existence of an equivalent reward problem is prior art. Exact theorem-level comparison remains open.

## czichowsky2013

- **Exact locator:** §3 Definition 3.1 and Lemma 3.2, Eq. (3.3), manuscript pp. 8–9; §2 defines the criterion and numeraire.
- **Problem:** Time-consistent mean–variance portfolio choice.
- **Financial/statistical objective:** Conditional mean minus gamma/2 times variance of terminal wealth.
- **Reward:** No RL reward; local mean–variance criterion.
- **Algorithm:** Backward local optimisation; semimartingale analysis.
- **Market/data:** General price models; scalar discrete-time derivation.
- **Evaluation metric:** Equilibrium conditions and policy characterisation.
- **Reported result:** Eq. (3.3) gives myopic demand minus covariance with future gains divided by conditional variance.
- **Reward/objective analysis:** Analyses financial objective; not RL reward misspecification.
- **Time inconsistency:** Yes: local mean–variance efficiency.
- **Known benchmark:** Explicit discrete recursion.
- **Project comparison:** Our scalar observed-regime hedge is a specialisation, with gamma=2phi and terminal-unit increments. Local perturbation and feedback concepts agree here because continuation is wealth-independent; no general equivalence claimed.

## bkm2016

- **Exact locator:** §8 Proposition 8.1, Eq. (32), p. 23; §10.1 Propositions 10.1–10.2, pp. 32–33.
- **Problem:** Time-inconsistent stochastic control.
- **Financial/statistical objective:** General equilibrium objectives; terminal wealth mean–variance in §10.1.
- **Reward:** Equivalent objective E[X_T − gamma*sigma²/2 times integral of exp(2r(T−s))*u_s² ds].
- **Algorithm:** Extended HJB and verification; no RL algorithm.
- **Market/data:** Continuous-time diffusion and other theoretical models.
- **Evaluation metric:** Equilibrium control and value.
- **Reported result:** Proposition 8.1 constructs an associated standard control problem; Proposition 10.2 supplies terminal-unit variance penalisation for MV.
- **Reward/objective analysis:** Yes: explicit objective equivalence.
- **Time inconsistency:** Yes.
- **Known benchmark:** Analytic scalar MV equilibrium.
- **Project comparison:** Existence of a reward implementing equilibrium and terminal-unit variance penalisation are prior ideas. Our sampled second-moment design is a finite-step implementation with a rank-one correction, not a new general principle. Oracle dependence is acknowledged in their §8 too.

## chaouki2020

- **Exact locator:** §1.1 Eqs. (1)–(5); §1.2; §2.1.1 Eqs. (9)–(12); §3 Fig. 2, Figs. 3–5 and Tables 1–3.
- **Problem:** Test DDPG on trading problems with known or near-optimal controls.
- **Financial/statistical objective:** Additive expected P&L minus trading costs and position risk.
- **Reward:** Quadratic case: position*predictor − Gamma*trade² − lambda*position², Eq. (9).
- **Algorithm:** DDPG with replay and target networks.
- **Market/data:** Simulated autoregressive predictor; quadratic/linear costs; quadratic risk or position bound; noisy and noiseless rewards.
- **Evaluation metric:** Reward, P&L, l1 position difference from reference, variability across 16 seeds.
- **Reported result:** Near-reference policies/rewards; noise worsens performance; some bounded-position agents fail. Fig. 2 explicitly excludes failed agents in that setting.
- **Reward/objective analysis:** Derives additive control model and compares learned policy to its reward optimum; does not audit equivalence to our terminal-MV equilibrium.
- **Time inconsistency:** No terminal-MV equilibrium comparison in the inspected formulation.
- **Known benchmark:** Yes; LQR and other exact/approximate controls.
- **Project comparison:** Known-policy financial-RL benchmarks and action-distance evaluation are not new. Our additional comparison is reward optimum versus separately specified equilibrium, before learning; no DDPG reproduction is claimed.

## dixon2020

- **Exact locator:** §3 Eqs. (19)–(23); §4 Eqs. (30)–(40); §5 Eqs. (41)–(46); §6 Table 1 and Fig. 2.
- **Problem:** Goal-based wealth management and reward inference from investor behaviour.
- **Financial/statistical objective:** Periodic wealth targets, contributions and costs, with entropy regularisation.
- **Reward:** Eq. (21): negative cash contribution, expected squared target shortfall and quadratic transaction cost; Eq. (22) defines target.
- **Algorithm:** G-learning (entropy-regularised LQR); GIRL inverse RL via trajectory likelihood.
- **Market/data:** Simulated 99 stocks plus bond, 30 quarterly periods, 1000 paths.
- **Evaluation metric:** Reward-parameter recovery, return paths and Sharpe versus unrebalanced allocation.
- **Reported result:** Table 1 and Fig. 2 report inferred parameters and imitation of the G-learner; parameter recovery is approximate.
- **Reward/objective analysis:** Yes: quadratic approximation and reward inference are explicit.
- **Time inconsistency:** No terminal-MV subgame equilibrium analysis.
- **Known benchmark:** Semi-analytic Gaussian policy for specified quadratic model.
- **Project comparison:** Inferring/designing rewards from target behaviour and quadratic portfolio reward analysis predate us. Our declared equilibrium target and exact raw-family mismatch differ from imitation; no new general inverse-RL method is claimed.

## simon2026

- **Exact locator:** §2.1 Eqs. (1)–(4); §3.4.2 Table 2; §4.1 Eq. (17), Table 4; §3.6 Eqs. (14)–(16), Table 3.
- **Problem:** Flexible direct portfolio choice.
- **Financial/statistical objective:** Investor utility; CRRA, mean–variance, loss aversion.
- **Reward:** MV Eq. (17) centres portfolio returns by their sample mean.
- **Algorithm:** Feed-forward deep parametric portfolio policy.
- **Market/data:** US equities, Open Source Asset Pricing characteristics; 1971–2020.
- **Evaluation metric:** Certainty-equivalent returns, Sharpe, turnover, drawdown.
- **Reported result:** Reports utility gains over linear policies and objective-specific comparisons.
- **Reward/objective analysis:** Yes: direct utility and risk preferences.
- **Time inconsistency:** One-period utility framework; not our terminal-MV equilibrium.
- **Known benchmark:** Linear policies and empirical comparators.
- **Project comparison:** Strong positive prior: objective-faithful learning already exists. Our covariance-MV reference implements its MV preference in a different common market, not the full DPPP architecture or stock dataset.

## jiang2025

- **Exact locator:** §2 Eqs. (5)–(9); §3.3.1 Eq. (19); §4.1; §4.3 Fig. 3/Table 2.
- **Problem:** Multi-period allocation with risk and trading constraints.
- **Financial/statistical objective:** Discounted sum of log-return minus variance and constraint penalties.
- **Reward:** Eq. (8): net log return minus lambda*sigma²; Eq. (19) adds soft turnover/weight violations.
- **Algorithm:** DPG with CNN/WaveNet cross-asset representation.
- **Market/data:** S&P100, DJIA, S&P/TSX; 2010–2023, test 2019–July2023.
- **Evaluation metric:** Accumulated value, Sharpe, maximum drawdown.
- **Reported result:** Table 2: horizon affects return/volatility; best Sharpe horizon varies by universe.
- **Reward/objective analysis:** Defines additive utility explicitly; not an identity with terminal MV.
- **Time inconsistency:** Discounted additive objective, not terminal equilibrium.
- **Known benchmark:** Competing learned/myopic strategies.
- **Project comparison:** Adapt log-minus-variance preference with common monthly data and hard simplex; first-order costs replace their log cost factor. No architecture or performance replication claimed.

## jiang2024

- **Exact locator:** §3 Eq. (4); §4.1 Fig. 2/Table 2; §4.2.
- **Problem:** Risk- and cost-sensitive trading.
- **Financial/statistical objective:** Additive portfolio-value reward with variance and trading penalties.
- **Reward:** Eq. (4): p_t transpose m_t minus beta*sigma² minus xi*p_t transpose |k_t|.
- **Algorithm:** CNN/LSTM with TD3; PPO/DDPG comparators.
- **Market/data:** DJIA30 and S&P100 stocks.
- **Evaluation metric:** Return, Sharpe, maximum drawdown, Calmar.
- **Reported result:** Reports strong CNN-TD3 performance in the stated backtests.
- **Reward/objective analysis:** Defines objective; no induced-terminal-equilibrium proof.
- **Time inconsistency:** Not treated as a terminal-MV game.
- **Known benchmark:** Minimum variance and max-Sharpe; no true market optimum.
- **Project comparison:** Motivates separate risk/cost coefficients. Do not silently reinterpret the printed portfolio-value term as our excess-return increment or call our code a replication.

## gollart2025

- **Exact locator:** §4.2.1 Table 1; §4.2.2 Algorithm 2; §5 numerical experiments.
- **Problem:** Dynamic expected-utility portfolio choice.
- **Financial/statistical objective:** Expected utility of terminal wealth.
- **Reward:** Zero intermediate rewards; terminal U(V_T).
- **Algorithm:** Modified DDPG.
- **Market/data:** Simulated Heston–Nandi GARCH market.
- **Evaluation metric:** Deviation from theoretical strategy and expected utility.
- **Reported result:** Learns approximately optimal policies against the analytical reference.
- **Reward/objective analysis:** Yes: explicitly maps financial problem to RL.
- **Time inconsistency:** Expected utility is the target; no terminal-MV equilibrium claim.
- **Known benchmark:** Analytical control benchmark.
- **Project comparison:** Recent positive control for objective-first RL and known-policy validation; our task audits a different reward family.

## cong2026

- **Exact locator:** §3 pathwise-gradient Eqs. (19)–(20), printed pp. 20–21; empirical sample discussion and baseline results.
- **Problem:** Direct goal-oriented allocation with path-dependent objectives.
- **Financial/statistical objective:** Trajectory objectives including window Sharpe and terminal utility.
- **Reward:** Differentiable whole-trajectory score; baseline 12-month Sharpe.
- **Algorithm:** Transformer representation, cross-asset attention, deterministic pathwise policy gradients.
- **Market/data:** US stocks; main OOS1990–2016.
- **Evaluation metric:** Sharpe, alpha, costs and economic restrictions.
- **Reported result:** Reports Sharpe above two in main and restricted universes.
- **Reward/objective analysis:** Yes; explicitly accommodates non-additive objectives.
- **Time inconsistency:** Distinguishes additive Bellman from path objectives, not our equilibrium target.
- **Known benchmark:** Empirical benchmark portfolios; no known true market policy.
- **Project comparison:** Refutes broad claims that financial RL only uses additive rewards. Our exact audit is complementary; no AlphaPortfolio reproduction.

## finrobot2024

- **Exact locator:** Section 3.1, Figure 2; Section 5; Section 6 future work.
- **Problem:** LLM financial workflows.
- **Financial/statistical objective:** Task-specific forecasting and reporting; no single terminal-MV objective.
- **Reward:** No portfolio-reward benchmark used here.
- **Algorithm:** LLM agents, tools, FinGPT forecasting.
- **Market/data:** US/Chinese-stock forecasting and report demonstrations.
- **Evaluation metric:** Illustrative outputs in the cited sections.
- **Reported result:** Platform demonstrations; allocation listed as future work.
- **Reward/objective analysis:** No portfolio reward-to-MV identity in the cited sections.
- **Time inconsistency:** Not treated in the cited sections.
- **Known benchmark:** Not a closed-form allocation control comparison.
- **Project comparison:** Motivates tool-boundary validation only; not implemented, evaluated or claimed to fail.

## markowitz1952

- **Exact locator:** pp. 77, 81–83 and 89–91; Figures 1–7.
- **Problem:** Portfolio choice given return beliefs.
- **Financial/statistical objective:** Efficient mean–variance combinations.
- **Reward:** Not RL; portfolio mean and covariance-based variance.
- **Algorithm:** Geometric efficient-set construction.
- **Market/data:** Stylised securities; no historical backtest.
- **Evaluation metric:** Expected return and variance.
- **Reported result:** Characterises efficient portfolios and the role of covariance in diversification.
- **Reward/objective analysis:** Direct objective formulation; no reward-surrogate experiment.
- **Time inconsistency:** Static model.
- **Known benchmark:** Known efficient frontier conditional on beliefs.
- **Project comparison:** Supplies target/control foundation, not a claimed new objective or empirical algorithm reproduction.

## demiguel2009

- **Exact locator:** Table 1 methods; Table 2 and Appendix A.2 industry data; Section 2, Eqs. (12)–(17); Tables 3–6; Proposition 1, Figure 1 and Appendix B; Section 6.1.
- **Problem:** Allocation under estimation error.
- **Financial/statistical objective:** Mean–variance utility and out-of-sample certainty equivalent.
- **Reward:** No RL reward; mean minus gamma/2 times variance.
- **Algorithm:** 14 plug-in, Bayesian, constrained, combination and robust models versus rebalanced 1/N.
- **Market/data:** Seven monthly datasets, including ten industries plus market; simulated N=10,25,50.
- **Evaluation metric:** Sharpe, CEQ, turnover and transaction-cost return loss.
- **Reported result:** No method consistently beats 1/N across datasets and metrics; required estimation length depends on N and true investment opportunities.
- **Reward/objective analysis:** Studies utility loss from estimation; not additive reward distortion.
- **Time inconsistency:** No equilibrium time-inconsistent control.
- **Known benchmark:** Known population optimum in Gaussian analysis/simulation; 1/N empirical hurdle.
- **Project comparison:** Retain 1/N, add N=30/49 checks at fixed L=120; distinguish estimation from reward mismatch. Not a reproduction of their dates, 14 methods, 50bp costs or normalised tangency portfolios.

## ledoit2017

- **Exact locator:** Sections 1–3 (portfolio loss and nonlinear shrinkage); Section 4.1 data; Section 4.3, Eqs. (17)–(20), Table 1.
- **Problem:** Covariance estimation in large portfolios.
- **Financial/statistical objective:** Minimise variance or portfolio-specific estimation loss.
- **Reward:** No RL reward.
- **Algorithm:** Rotation-equivariant nonlinear covariance eigenvalue shrinkage, with a factor-preconditioned extension.
- **Market/data:** CRSP daily stocks; 1973–2011 out-of-sample; N=30,50,100,250,500; 250-day covariance windows.
- **Evaluation metric:** Out-of-sample standard deviation primarily; excess return and Sharpe also.
- **Reported result:** Nonlinear shrinkage improves on linear shrinkage in Table 1; gains stronger at larger N.
- **Reward/objective analysis:** Matches evaluation loss to objective; not RL surrogate calibration.
- **Time inconsistency:** Static estimated allocation.
- **Known benchmark:** Population GMV formula; empirical competitors including 1/N.
- **Project comparison:** Motivates objective-specific evaluation and estimation controls. Our 10% diagonal shrinkage is NOT this estimator; no replication or performance superiority claimed.

## garleanu2013

- **Exact locator:** Section II Eqs. (3)–(5); Section III Propositions 2–3; Section VI and Tables I–II.
- **Problem:** Optimal trading with predictable returns and costly rebalancing.
- **Financial/statistical objective:** Discounted expected excess gains minus per-period variance and quadratic trading costs.
- **Reward:** The additive control objective is explicitly defined; not an RL reward approximation to terminal MV.
- **Algorithm:** Closed-form dynamic programming, partial adjustment toward an aim portfolio.
- **Market/data:** 15 commodity futures, daily, January 1996–January 2009.
- **Evaluation metric:** Gross and net Sharpe; comparison with frictionless Markowitz and static-cost controls.
- **Reported result:** Table II: dynamic net Sharpe .58/.53 versus static alternatives under two cost settings.
- **Reward/objective analysis:** Direct economic objective; no reward mismatch audit.
- **Time inconsistency:** Time-consistent discounted stage objective, not terminal-MV equilibrium.
- **Known benchmark:** Closed-form optimal policy under the model.
- **Project comparison:** Explains why continuation/cost-aware benchmarks matter. Our rolling one-period L1-cost target is neither their dynamic optimum nor a reproduction.

## demiguel2024

- **Exact locator:** Sections I.A–C; Eqs. (3), (6), (10); Tables II–III.
- **Problem:** Multifactor volatility timing.
- **Financial/statistical objective:** Mean–variance net of costs.
- **Reward:** No RL reward.
- **Algorithm:** Nonnegative factor weights affine in inverse market volatility.
- **Market/data:** Nine equity factors; CRSP/Compustat; out-of-sample 1977–2020.
- **Evaluation metric:** Net Sharpe, alpha, costs.
- **Reported result:** Table II: conditional/unconditional Sharpe 1.062/.940; p=.006.
- **Reward/objective analysis:** Direct objective; no surrogate audit.
- **Time inconsistency:** No terminal equilibrium.
- **Known benchmark:** Unconditional portfolio comparator.
- **Project comparison:** Positive cost-aware finance example; motivates preserving cost preferences. Not reproduced.

## kolm2025

- **Exact locator:** Publisher abstract only; no section/table-specific claim.
- **Problem:** Educational overview of financial RL.
- **Financial/statistical objective:** Multiple investment objectives discussed; no single benchmark established from abstract.
- **Reward:** Not extracted: full text unavailable.
- **Algorithm:** Overview, not an implemented comparator in this project.
- **Market/data:** Not extracted.
- **Evaluation metric:** Not extracted.
- **Reported result:** Abstract recommends hybrid approaches combining RL and classical models.
- **Reward/objective analysis:** Not assessed beyond abstract.
- **Time inconsistency:** Not assessed.
- **Known benchmark:** Not assessed.
- **Project comparison:** Motivates hybrid validation; no performance or novelty exclusion inferred from inaccessible text.

## habibnia2024

- **Exact locator:** Section 3.4 Eqs.2–8; Tables 2–4; Section 4.1.
- **Problem:** Two-sided crypto allocation with lending.
- **Financial/statistical objective:** Profit with asymmetric loss/cost penalties.
- **Reward:** Eq.8: (sum Profit − penalty*(sum Loss + sum Cost/5))/deployed capital; penalty=25.
- **Algorithm:** SAC with CNN and multi-head attention.
- **Market/data:** 12 Binance perpetual crypto futures; two 16-month periods, each 12 training/4 testing; four-hour rebalancing.
- **Evaluation metric:** Return, Sharpe, Sortino, drawdown, Calmar.
- **Reported result:** Table4 reports total returns 575.585% and 145.627%; not reproduced here.
- **Reward/objective analysis:** Defines reward and empirical comparison; no equivalence to our MV reference established.
- **Time inconsistency:** No terminal-MV equilibrium analysis identified.
- **Known benchmark:** Return-RL/MV/MAD/CVaR controls, not a known dynamic optimum.
- **Project comparison:** Explicit long-only unit-capital assetwise reward restriction; no SAC, loans or crypto replication. Separate convex-financing theorem/test is not their environment.

## ledoit2004identity

- **Exact locator:** Section 3.3, Lemmas 3.2–3.4 and Theorem 3.2; Section 4 simulations.
- **Problem:** Ill-conditioned high-dimensional sample covariance.
- **Financial/statistical objective:** Quadratic covariance estimation loss.
- **Reward:** Not RL.
- **Algorithm:** Data-driven linear shrinkage toward scaled identity.
- **Market/data:** Monte Carlo covariance models.
- **Evaluation metric:** Covariance quadratic loss and conditioning.
- **Reported result:** Asymptotic optimality within linear shrinkage class; finite-sample simulation support.
- **Reward/objective analysis:** No RL reward analysis.
- **Time inconsistency:** Not applicable.
- **Known benchmark:** Known population covariance in simulation.
- **Project comparison:** Implemented centred estimator; final covariance multiplied by L/(L−1); checked independently against scikit-learn. No guarantee of realised MV superiority.

## ledoit2004correlation

- **Exact locator:** Working paper Section 3, Appendix A Eq.3, Appendix B Eq.5; Section 4 Tables 1–3.
- **Problem:** Noisy covariance inputs in active portfolio management.
- **Financial/statistical objective:** Covariance quadratic loss; active portfolio risk.
- **Reward:** Not RL.
- **Algorithm:** Sample covariance shrunk toward constant correlation with estimated intensity.
- **Market/data:** Monthly US stocks, 1983–2002 evaluation in inspected working paper.
- **Evaluation metric:** Realised information ratio and tracking error.
- **Reported result:** Reports improved information ratios relative to sample covariance.
- **Reward/objective analysis:** No RL surrogate audit.
- **Time inconsistency:** Not applicable.
- **Known benchmark:** Index-relative portfolio comparators.
- **Project comparison:** Implemented target and fourth-moment intensity; unbiased-unit rescaling; direct elementwise formula test. Different long-only monthly industry environment.

## fan2008

- **Exact locator:** Final Section 2 Eqs.2–5; Section 4 portfolio allocation; Section 5 simulation.
- **Problem:** Covariance estimation with observed factors and growing dimension.
- **Financial/statistical objective:** Covariance estimation and portfolio risk.
- **Reward:** Not RL.
- **Algorithm:** OLS factor loadings, factor covariance and diagonal residual covariance.
- **Market/data:** Simulation with observed factor structure.
- **Evaluation metric:** Covariance error, inverse error, portfolio risk.
- **Reported result:** Convergence results describe when factor structure provides substantial or limited benefits.
- **Reward/objective analysis:** No reward calibration.
- **Time inconsistency:** Not applicable.
- **Known benchmark:** Known covariance and population portfolios in simulations.
- **Project comparison:** Market and three-factor adaptations use intercept and residual dof L−K−1, unlike their no-intercept ML residual convention. Correlated-residual simulation tests misspecification.

## halperin2025chapter

- **Exact locator:** Risk-Aware RL: Beyond Expected Returns, printed pp.99–100; policy and validation discussion.
- **Problem:** Practical financial RL/IRL introduction.
- **Financial/statistical objective:** Multiple risk-sensitive financial objectives.
- **Reward:** Includes expected return minus variance penalty.
- **Algorithm:** Tutorial; no single empirical comparator.
- **Market/data:** Illustrative applications.
- **Evaluation metric:** Multiple application-specific measures.
- **Reported result:** Emphasises risk objectives and validation.
- **Reward/objective analysis:** Discusses risk-sensitive objective formulation.
- **Time inconsistency:** No terminal-equilibrium claim used here.
- **Known benchmark:** Not used as numerical benchmark.
- **Project comparison:** Accessible primary background; not silently substituted for the paywalled JPM article and not needed for its unverified details.
