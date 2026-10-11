# Primary-paper comparison ledger

Updated 9 October 2026: 39 records. Versions and reading coverage are explicit. External reported results are not replications. RL extension is preliminary and separate from the frozen manuscript.

| ID | Verified citation | Access / version | Relation |
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
| kolm2025 | Petter N. Kolm; Gordon Ritter (2025). [Reinforcement Learning for Asset and Portfolio Management](https://doi.org/10.3905/jpm.2025.1.782). The Journal of Portfolio Management 52(2), 81–95. | Final 15-page journal PDF supplied by user; all pages, Exhibits 1–3 and references read on 9 October 2026. Supersedes abstract-only record. | Full-text motivation for a quantitative mandate-alignment check between reward specification and training (Exhibit2). Separates forecast quality from reward fidelity, and given-mandate validation from inverse preference inference. No invented 2025 performance row; 2019 raw-reward adaptation remains distinct. |
| habibnia2024 | Ali Habibnia; Mahdi Soltanzadeh (2024). [Optimizing Portfolio with Two-Sided Transactions and Lending: A Reinforcement Learning Framework](https://arxiv.org/abs/2408.05382). arXiv:2408.05382v1. | 24-page arXiv v1 PDF and HTML read. | Explicit long-only unit-capital assetwise reward restriction; no SAC, loans or crypto replication. Separate convex-financing theorem/test is not their environment. |
| ledoit2004identity | Olivier Ledoit; Michael Wolf (2004). [A well-conditioned estimator for large-dimensional covariance matrices](https://doi.org/10.1016/S0047-259X(03)00096-4). Journal of Multivariate Analysis 88(2), 365–411. | 47-page journal PDF on ENS Lyon academic host read. | Implemented centred estimator; final covariance multiplied by L/(L−1); checked independently against scikit-learn. No guarantee of realised MV superiority. |
| ledoit2004correlation | Olivier Ledoit; Michael Wolf (2004). [Honey, I Shrunk the Sample Covariance Matrix](https://doi.org/10.3905/jpm.2004.110). The Journal of Portfolio Management 30(4), 110–119. | November 2003 Barcelona Economics Working Paper 92, full PDF read; journal identity checked separately. | Implemented target and fourth-moment intensity; unbiased-unit rescaling; direct elementwise formula test. Different long-only monthly industry environment. |
| fan2008 | Jianqing Fan; Yingying Fan; Jinchi Lv (2008). [High dimensional covariance matrix estimation using a factor model](https://doi.org/10.1016/j.jeconom.2008.09.017). Journal of Econometrics 147(1), 186–197. | 12-page final journal PDF read; 43-page arXiv predecessor also archived. | Market and three-factor adaptations use intercept and residual dof L−K−1, unlike their no-intercept ML residual convention. Correlated-residual simulation tests misspecification. |
| halperin2025chapter | Igor Halperin; Petter N. Kolm; Gordon Ritter (2025). [Reinforcement Learning and Inverse Reinforcement Learning: A Practitioner’s Guide for Investment Management](https://rpc.cfainstitute.org/research/foundation/2025/chapter-6-reinforcement-learning-inverse-reinforcement-learning). Chapter 6 in AI in Asset Management: Tools, Applications, and Frontiers, CFA Institute Research Foundation. | 35-page official chapter PDF read for background; distinct from requested JPM article. | Accessible primary background; not silently substituted for the paywalled JPM article and not needed for its unverified details. |
| lesmana2025 | Nixie Sapphira Lesmana; Chi Seng Pun (2025). [A Subgame Perfect Equilibrium Reinforcement Learning Approach to Time-Inconsistent Problems](https://doi.org/10.1137/23M1594510). SIAM Journal on Financial Mathematics 16(1), 68–122. | Journal metadata/abstract verified. Targeted full-text reading of arXiv:2110.14295v1 (27 October 2021), NOT the 2025 final text; saved filename lesmana2025.pdf denotes citation year, not file version. | Backward equilibrium learning is prior art. Our learner is a structured adaptation, not a published-algorithm reproduction. Candidate addition is a finite-iterate deviation certificate; final-version overlap still needs checking. |
| guo2026 | Xin Guo; Yijie Huang; Xiang Yu (2026). [Deterministic Policy Gradient for Learning Equilibrium in Time-Inconsistent Control Problems](https://arxiv.org/abs/2606.11798). arXiv preprint 2606.11798v1. | 10 June 2026, 40-page primary PDF. Targeted reading, not full-proof verification. | Rules out novelty in merely learning auxiliary rewards or using DPG for equilibrium. Our proposed audit concerns finite-iterate discrete-state deviation gains, not their general continuous-time method. |
| sangadi2025 | Tejaram Sangadi; Prashanth L.A.; Krishna Jagannathan (2025). [A Finite-Sample Analysis of an Actor-Critic Algorithm for Mean-Variance Optimization in a Discounted MDP](https://arxiv.org/abs/2406.07892). arXiv:2406.07892v2; publication venue not used without final-version concordance. | 12 March 2025, 49-page primary preprint. Targeted reading. | Finite-sample MV actor–critic guarantees already exist. Our audit seeks per-state one-step equilibrium deviation, a different certificate, not a better general convergence rate. |
| chen2025seminorm | Zaiwei Chen; Sheng Zhang; Zhe Zhang; Shaan Ul Haque; Siva Theja Maguluri (2025). [A Non-Asymptotic Theory of Seminorm Lyapunov Stability: From Deterministic to Stochastic Iterative Algorithms](https://arxiv.org/abs/2502.14208). arXiv preprint 2502.14208v1. | 20 February 2025, 59-page primary PDF. Targeted reading of introduction, §2 and opening §5. | Constant-shift invariance, quotient critics and seminorm learning are prior art. Candidate contribution is their specific link to MV deviation gain; no claim to invent centring. |
| maurer2009 | Andreas Maurer; Massimiliano Pontil (2009). [Empirical Bernstein Bounds and Sample Variance Penalization](https://www.cs.mcgill.ca/~colt2009/papers/012.pdf). Proceedings of COLT 2009. | 9-page conference PDF; targeted reading of §1 and Theorem4. | We use Theorem4, p.2, on both tails of fixed-policy audit quantities; the concentration inequality is not ours. |
| schulman2017 | John Schulman; Filip Wolski; Prafulla Dhariwal; Alec Radford; Oleg Klimov (2017). [Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347). arXiv:1707.06347v2. | 28 August 2017, 12-page primary preprint. Targeted reading of Sections 1–3, 5 and 6.1; not a claim to have reproduced its full experimental suite. | A standard optimiser used in a matched reward intervention. SB3 implementation and sample-only continuation refresh are disclosed. We do not replicate the original nonfinancial tasks, claim to improve PPO generally, or equate its compute budget with the direct-gradient learner. |

## kolm2019

| Field | Extraction |
|---|---|
| locator | “Automatic hedging in theory”, manuscript pp. 7–8, Eqs. (8)–(10), footnote 4; “Automatic hedging in practice”, pp. 9–14, Exhibits 1–5. |
| problem | Discrete option hedging with nonlinear trading costs. |
| objective | Terminal wealth mean–variance, then a simplified sum of increment variances. |
| reward | Δw − (κ/2)(Δw)², explicitly approximate. |
| algorithm | Batch fitted action-value learning with one-step SARSA targets and nonlinear regression. |
| market | Simulated GBM European call; strike/spot 100, 10 days, 5 decisions/day; κ=.1. |
| metric | Hedging P&L, costs, volatility; comparison to delta hedging. |
| result | Reports lower cost across 10,000 test paths; volatility difference not significant at 99%. |
| studies_reward_objective | Yes: explicitly discusses covariance and approximation. |
| time_inconsistency | Does not formulate a subgame equilibrium in the inspected derivation. |
| known_benchmark | BSM hedge in frictionless limit; not a solved frictional optimum. |
| project_relation | Closest raw-reward baseline. We isolate policy mismatch in a different allocation benchmark; do not infer failure of their hedger. Published κ/2=.05 is a units-sensitive diagnostic only. |

## jiang2017

| Field | Extraction |
|---|---|
| locator | §§2.2–2.4, §4.2 Eqs. (21)–(22), §4.3; Tables 1–2; §6. |
| problem | Long-only cryptocurrency allocation with costs. |
| objective | Portfolio growth. |
| reward | Average log portfolio growth including transaction-cost factor. |
| algorithm | Direct gradient ascent; EIIE CNN/RNN/LSTM policies and portfolio-vector memory. |
| market | Poloniex, 11 noncash assets plus Bitcoin cash, 30-minute decisions; three 2016–2017 backtests. |
| metric | Final accumulated value, Sharpe, maximum drawdown. |
| result | EIIE variants report leading accumulated values in all three tests (Table 2). |
| studies_reward_objective | Yes: log reward corresponds to multiplicative growth. |
| time_inconsistency | No terminal mean–variance equilibrium objective. |
| known_benchmark | Trading comparators, no known true market optimum. |
| project_relation | Adapt log growth on an identical bounded action set. Different target preferences explain disagreement; their own growth objective is not mis-specified. |

## yang2020

| Field | Extraction |
|---|---|
| locator | §3.3 Eq. (4); §5 ensemble selection; §6.1 and Fig. 4; §6.2.4 and Table 2. |
| problem | Automated constrained stock trading. |
| objective | Portfolio value growth with costs and turbulence control. |
| reward | Change in portfolio value net of transaction costs. |
| algorithm | PPO, A2C, DDPG; rolling Sharpe-based ensemble selection. |
| market | Dow 30 daily WRDS data; training 2009–2015, testing Jan. 2016–8 May 2020. |
| metric | Return, volatility, drawdown, Sharpe. |
| result | Table 2: ensemble Sharpe 1.30, DJIA .47, minimum variance .45. |
| studies_reward_objective | Defines value-change objective; no identity with terminal MV. |
| time_inconsistency | No equilibrium mean–variance treatment. |
| known_benchmark | DJIA and minimum-variance comparator, no true dynamic optimum. |
| project_relation | Adapt value increments with zero costs and undiscounted finite horizon. Measures preference alignment; does not reproduce PPO/DDPG or the historical result. |

## moody2001

| Field | Extraction |
|---|---|
| locator | §II-D, Eqs. (12)–(17), PDF pp. 3–4; §III-A Eq. (31); §IV-A, Fig. 5; §IV-C.2, Fig. 8. |
| problem | Trading and stock/T-bill allocation. |
| objective | Risk-adjusted trading performance. |
| reward | Differential Sharpe Eq. (14), EWMA updates Eq. (15); also differential downside-deviation reward. |
| algorithm | Recurrent reinforcement learning; Q-learning/advantage updating comparisons. |
| market | Synthetic prices; USD/GBP; monthly S&P500/T-bills with 1970–1994 test period. |
| metric | Profit and Sharpe; downside risk in FX example. |
| result | §IV-C.2 reports annualised Sharpe .83 for RRL, .63 for Q-trader, .34 buy-and-hold. |
| studies_reward_objective | Yes: derives DSR as first-order Sharpe change. |
| time_inconsistency | No terminal MV equilibrium equivalence. |
| known_benchmark | Simple market examples; no known optimal real-market policy. |
| project_relation | Adapt unscaled DSR on an augmented (wealth,A,B) tree. Original online gradient update is not identical to maximising an undiscounted sum of DSR signals. |

## bisi2020

| Field | Extraction |
|---|---|
| locator | §3 Eqs. (3)–(6); §§4–5, Algorithm 1; §7.1–7.2, Fig. 1(a)–(d). |
| problem | Trading with short-term risk control. |
| objective | Expected reward minus occupancy-weighted per-step reward variance. |
| reward | Trading P&L minus turnover costs; policy-dependent centred quadratic transformation. |
| algorithm | Trust Region Volatility Optimization (TRVO), extending TRPO. |
| market | Daily S&P500 through 2019; minute USD/EUR and USD/JPY, train 2017/test 2018. |
| metric | Mean-volatility and mean-variance frontiers. |
| result | Fig. 1 reports broader/frontier improvements over exponential rewards; S&P results are in-sample. |
| studies_reward_objective | Yes: reward-volatility Bellman/gradient theory and return-variance bound. |
| time_inconsistency | Distinguishes risk measures; does not target the terminal-MV subgame equilibrium here. |
| known_benchmark | No closed-form optimum for historical tasks. |
| project_relation | Direct prior art against broad reward-analysis novelty. We compare its per-step criterion with an independently specified terminal equilibrium; do not call its chosen short-term objective wrong. |

## zhang2021

| Field | Extraction |
|---|---|
| locator | “Mean-Variance RL”, Eq. (2); “Mean-Variance Policy Iteration”, Eqs. (3)–(4), Algorithm 1, Propositions 1–2; “Experiments”, Table 1. |
| problem | Scalable risk-averse RL. |
| objective | Discounted-occupancy per-step mean–variance. |
| reward | Transformed reward r − λr² + 2λry; y updated by policy evaluation. |
| algorithm | MVPI, instantiated with TD3; offline density-ratio variant. |
| market | Eight noisy-action MuJoCo tasks and an offline benchmark; not financial prices. |
| metric | Risk-aware score, mean, variance, Sharpe-like ratio. |
| result | Reports strong risk-aware results versus TD3 and risk-averse baselines; not universal dominance on every metric. |
| studies_reward_objective | Yes, explicitly distinguishes per-step and total-return variance. |
| time_inconsistency | No financial subgame-equilibrium target. |
| known_benchmark | Small illustrative MDP; no closed-form MuJoCo optimum. |
| project_relation | Finite-horizon uniform-time adaptation added. At zero interest its iid fixed point equals our scalar calibration: that formula alone is not a defensible novelty claim. |

## wang2020

| Field | Extraction |
|---|---|
| locator | §2 Eq. (11); §3 Theorems 1 and 3; §4; §5.1 Table 1, §§5.2–5.3. |
| problem | Learn continuous-time mean–variance allocation. |
| objective | Precommitted terminal MV via a mean constraint and quadratic embedding. |
| reward | Terminal squared deviation plus entropy regularisation. |
| algorithm | Exploratory mean–variance (EMV), policy evaluation/improvement. |
| market | Simulated GBM parameter grid and nonstationary simulations. |
| metric | Terminal return, variance, Sharpe; algorithm comparisons. |
| result | §5.1 reports EMV best Sharpe in 23 of 28 tested cases. |
| studies_reward_objective | Yes: objective and optimal exploratory control derived. |
| time_inconsistency | Uses precommitment; not an equilibrium solver. |
| known_benchmark | Closed-form Gaussian exploratory policy and classical limit. |
| project_relation | Essential positive control: objective-faithful RL already exists. Our discrete reward-family audit asks a different question; no EMV replication claimed. |

## dai2023

| Field | Extraction |
|---|---|
| locator | Working version §§2–3, §4.2 Theorem 2; §5 Algorithm 1; §6.1–6.2, Fig. 1. |
| problem | Learn equilibrium allocation under stochastic investment opportunities. |
| objective | Mean–variance of log returns plus entropy. |
| reward | Objective-specific equilibrium TD/policy updates, not arbitrary additive wealth increments. |
| algorithm | Exploratory equilibrium policy iteration and parameterised learning. |
| market | Simulated Gaussian mean-return model; perfect/noisy factor observations. |
| metric | Policy deviation from theoretical solution and convergence. |
| result | Fig. 1 shows learned policies close to the analytic target, with increased error under observation noise. |
| studies_reward_objective | Yes. |
| time_inconsistency | Yes, explicitly central. |
| known_benchmark | Semi-analytic equilibrium; closed form in Gaussian factor model. |
| project_relation | Refutes any first-equilibrium-RL claim. Our target is discrete terminal wealth MV and an audit of common rewards, not their log-MV learning problem. |

## ling2000

| Field | Extraction |
|---|---|
| locator | §§3–4, Theorems 1–2 (embedding); §5 riskless-asset case. |
| problem | Multiperiod portfolio selection. |
| objective | Terminal mean–variance at the initial date. |
| reward | No RL reward; auxiliary quadratic terminal objective. |
| algorithm | Embedding and stochastic linear-quadratic control. |
| market | Independent, potentially time-varying return moments. |
| metric | Efficient frontier and terminal mean/variance. |
| result | Analytic optimal policies/frontiers via embedding. |
| studies_reward_objective | Analyses the objective transformation, not additive RL rewards. |
| time_inconsistency | Supplies precommitted optimum, not subgame equilibrium. |
| known_benchmark | Yes, core exact reference. |
| project_relation | Our precommitment reference is established theory. Reward-design comparisons must specify whether this or equilibrium is the intended target. |

## basak2010

| Field | Extraction |
|---|---|
| locator | Thesis chapter 2 §2.2.2, Proposition 2.1, Eqs. (148)–(149); §2.2.2 Remark 1; §2.2.4; discrete-time extension in §2.4. |
| problem | Dynamic allocation under stochastic opportunities. |
| objective | Time-consistent terminal wealth mean–variance. |
| reward | No RL reward; equilibrium control and associated utility interpretation. |
| algorithm | Recursive equilibrium analysis and analytic specialisations. |
| market | Continuous-time incomplete-market models; discrete-time extensions. |
| metric | Policy, hedging demand, terminal moments. |
| result | Decomposes risky demand into myopic and intertemporal hedging components. |
| studies_reward_objective | Discusses objectives giving the same policy (Remark 1). |
| time_inconsistency | Yes. |
| known_benchmark | Analytic equilibria in tractable market models. |
| project_relation | Foundational benchmark and hedge precedent. Our finite-regime correction is a discrete audit construction, not the discovery of intertemporal hedging or inverse objectives. |

## ng1999

| Field | Extraction |
|---|---|
| locator | §3 Theorem 1, Eq. (2), Corollary 2; §4 Figures 1–2; Appendix A. |
| problem | Reward shaping without changing optimal policies. |
| objective | Expected discounted reward. |
| reward | Potential difference γΦ(s′)−Φ(s). |
| algorithm | Policy-invariance theorem; SARSA gridworld examples. |
| market | Synthetic gridworlds, not markets. |
| metric | Policy invariance and learning steps. |
| result | Potential shaping preserves optimal policies under stated conditions and can accelerate learning. |
| studies_reward_objective | Yes. |
| time_inconsistency | Not a mean–variance equilibrium treatment. |
| known_benchmark | Known small MDPs. |
| project_relation | Our redesign deliberately changes the raw reward optimum. Policy-invariant shaping cannot by itself correct a mismatched target. |

## bjork2014

| Field | Extraction |
|---|---|
| locator | Publisher abstract only; no theorem number or detailed comparison asserted. |
| problem | Markovian time-inconsistent control. |
| objective | General time-inconsistent criteria. |
| reward | Not extracted from full text. |
| algorithm | Game-theoretic extended dynamic programming (abstract). |
| market | General control setting (abstract). |
| metric | Equilibrium policies and values (abstract). |
| result | Abstract states an associated time-consistent problem can reproduce equilibrium control and value. |
| studies_reward_objective | Abstract supports existence of an equivalent control problem. |
| time_inconsistency | Yes. |
| known_benchmark | Not independently extracted. |
| project_relation | Requires conservative novelty: existence of an equivalent reward problem is prior art. Exact theorem-level comparison remains open. |

## czichowsky2013

| Field | Extraction |
|---|---|
| locator | §3 Definition 3.1 and Lemma 3.2, Eq. (3.3), manuscript pp. 8–9; §2 defines the criterion and numeraire. |
| problem | Time-consistent mean–variance portfolio choice. |
| objective | Conditional mean minus gamma/2 times variance of terminal wealth. |
| reward | No RL reward; local mean–variance criterion. |
| algorithm | Backward local optimisation; semimartingale analysis. |
| market | General price models; scalar discrete-time derivation. |
| metric | Equilibrium conditions and policy characterisation. |
| result | Eq. (3.3) gives myopic demand minus covariance with future gains divided by conditional variance. |
| studies_reward_objective | Analyses financial objective; not RL reward misspecification. |
| time_inconsistency | Yes: local mean–variance efficiency. |
| known_benchmark | Explicit discrete recursion. |
| project_relation | Our scalar observed-regime hedge is a specialisation, with gamma=2phi and terminal-unit increments. Local perturbation and feedback concepts agree here because continuation is wealth-independent; no general equivalence claimed. |

## bkm2016

| Field | Extraction |
|---|---|
| locator | §8 Proposition 8.1, Eq. (32), p. 23; §10.1 Propositions 10.1–10.2, pp. 32–33. |
| problem | Time-inconsistent stochastic control. |
| objective | General equilibrium objectives; terminal wealth mean–variance in §10.1. |
| reward | Equivalent objective E[X_T − gamma*sigma²/2 times integral of exp(2r(T−s))*u_s² ds]. |
| algorithm | Extended HJB and verification; no RL algorithm. |
| market | Continuous-time diffusion and other theoretical models. |
| metric | Equilibrium control and value. |
| result | Proposition 8.1 constructs an associated standard control problem; Proposition 10.2 supplies terminal-unit variance penalisation for MV. |
| studies_reward_objective | Yes: explicit objective equivalence. |
| time_inconsistency | Yes. |
| known_benchmark | Analytic scalar MV equilibrium. |
| project_relation | Existence of a reward implementing equilibrium and terminal-unit variance penalisation are prior ideas. Our sampled second-moment design is a finite-step implementation with a rank-one correction, not a new general principle. Oracle dependence is acknowledged in their §8 too. |

## chaouki2020

| Field | Extraction |
|---|---|
| locator | §1.1 Eqs. (1)–(5); §1.2; §2.1.1 Eqs. (9)–(12); §3 Fig. 2, Figs. 3–5 and Tables 1–3. |
| problem | Test DDPG on trading problems with known or near-optimal controls. |
| objective | Additive expected P&L minus trading costs and position risk. |
| reward | Quadratic case: position*predictor − Gamma*trade² − lambda*position², Eq. (9). |
| algorithm | DDPG with replay and target networks. |
| market | Simulated autoregressive predictor; quadratic/linear costs; quadratic risk or position bound; noisy and noiseless rewards. |
| metric | Reward, P&L, l1 position difference from reference, variability across 16 seeds. |
| result | Near-reference policies/rewards; noise worsens performance; some bounded-position agents fail. Fig. 2 explicitly excludes failed agents in that setting. |
| studies_reward_objective | Derives additive control model and compares learned policy to its reward optimum; does not audit equivalence to our terminal-MV equilibrium. |
| time_inconsistency | No terminal-MV equilibrium comparison in the inspected formulation. |
| known_benchmark | Yes; LQR and other exact/approximate controls. |
| project_relation | Known-policy financial-RL benchmarks and action-distance evaluation are not new. Our additional comparison is reward optimum versus separately specified equilibrium, before learning; no DDPG reproduction is claimed. |

## dixon2020

| Field | Extraction |
|---|---|
| locator | §3 Eqs. (19)–(23); §4 Eqs. (30)–(40); §5 Eqs. (41)–(46); §6 Table 1 and Fig. 2. |
| problem | Goal-based wealth management and reward inference from investor behaviour. |
| objective | Periodic wealth targets, contributions and costs, with entropy regularisation. |
| reward | Eq. (21): negative cash contribution, expected squared target shortfall and quadratic transaction cost; Eq. (22) defines target. |
| algorithm | G-learning (entropy-regularised LQR); GIRL inverse RL via trajectory likelihood. |
| market | Simulated 99 stocks plus bond, 30 quarterly periods, 1000 paths. |
| metric | Reward-parameter recovery, return paths and Sharpe versus unrebalanced allocation. |
| result | Table 1 and Fig. 2 report inferred parameters and imitation of the G-learner; parameter recovery is approximate. |
| studies_reward_objective | Yes: quadratic approximation and reward inference are explicit. |
| time_inconsistency | No terminal-MV subgame equilibrium analysis. |
| known_benchmark | Semi-analytic Gaussian policy for specified quadratic model. |
| project_relation | Inferring/designing rewards from target behaviour and quadratic portfolio reward analysis predate us. Our declared equilibrium target and exact raw-family mismatch differ from imitation; no new general inverse-RL method is claimed. |

## simon2026

| Field | Extraction |
|---|---|
| locator | §2.1 Eqs. (1)–(4); §3.4.2 Table 2; §4.1 Eq. (17), Table 4; §3.6 Eqs. (14)–(16), Table 3. |
| problem | Flexible direct portfolio choice. |
| objective | Investor utility; CRRA, mean–variance, loss aversion. |
| reward | MV Eq. (17) centres portfolio returns by their sample mean. |
| algorithm | Feed-forward deep parametric portfolio policy. |
| market | US equities, Open Source Asset Pricing characteristics; 1971–2020. |
| metric | Certainty-equivalent returns, Sharpe, turnover, drawdown. |
| result | Reports utility gains over linear policies and objective-specific comparisons. |
| studies_reward_objective | Yes: direct utility and risk preferences. |
| time_inconsistency | One-period utility framework; not our terminal-MV equilibrium. |
| known_benchmark | Linear policies and empirical comparators. |
| project_relation | Strong positive prior: objective-faithful learning already exists. Our covariance-MV reference implements its MV preference in a different common market, not the full DPPP architecture or stock dataset. |

## jiang2025

| Field | Extraction |
|---|---|
| locator | §2 Eqs. (5)–(9); §3.3.1 Eq. (19); §4.1; §4.3 Fig. 3/Table 2. |
| problem | Multi-period allocation with risk and trading constraints. |
| objective | Discounted sum of log-return minus variance and constraint penalties. |
| reward | Eq. (8): net log return minus lambda*sigma²; Eq. (19) adds soft turnover/weight violations. |
| algorithm | DPG with CNN/WaveNet cross-asset representation. |
| market | S&P100, DJIA, S&P/TSX; 2010–2023, test 2019–July2023. |
| metric | Accumulated value, Sharpe, maximum drawdown. |
| result | Table 2: horizon affects return/volatility; best Sharpe horizon varies by universe. |
| studies_reward_objective | Defines additive utility explicitly; not an identity with terminal MV. |
| time_inconsistency | Discounted additive objective, not terminal equilibrium. |
| known_benchmark | Competing learned/myopic strategies. |
| project_relation | Adapt log-minus-variance preference with common monthly data and hard simplex; first-order costs replace their log cost factor. No architecture or performance replication claimed. |

## jiang2024

| Field | Extraction |
|---|---|
| locator | §3 Eq. (4); §4.1 Fig. 2/Table 2; §4.2. |
| problem | Risk- and cost-sensitive trading. |
| objective | Additive portfolio-value reward with variance and trading penalties. |
| reward | Eq. (4): p_t transpose m_t minus beta*sigma² minus xi*p_t transpose |k_t|. |
| algorithm | CNN/LSTM with TD3; PPO/DDPG comparators. |
| market | DJIA30 and S&P100 stocks. |
| metric | Return, Sharpe, maximum drawdown, Calmar. |
| result | Reports strong CNN-TD3 performance in the stated backtests. |
| studies_reward_objective | Defines objective; no induced-terminal-equilibrium proof. |
| time_inconsistency | Not treated as a terminal-MV game. |
| known_benchmark | Minimum variance and max-Sharpe; no true market optimum. |
| project_relation | Motivates separate risk/cost coefficients. Do not silently reinterpret the printed portfolio-value term as our excess-return increment or call our code a replication. |

## gollart2025

| Field | Extraction |
|---|---|
| locator | §4.2.1 Table 1; §4.2.2 Algorithm 2; §5 numerical experiments. |
| problem | Dynamic expected-utility portfolio choice. |
| objective | Expected utility of terminal wealth. |
| reward | Zero intermediate rewards; terminal U(V_T). |
| algorithm | Modified DDPG. |
| market | Simulated Heston–Nandi GARCH market. |
| metric | Deviation from theoretical strategy and expected utility. |
| result | Learns approximately optimal policies against the analytical reference. |
| studies_reward_objective | Yes: explicitly maps financial problem to RL. |
| time_inconsistency | Expected utility is the target; no terminal-MV equilibrium claim. |
| known_benchmark | Analytical control benchmark. |
| project_relation | Recent positive control for objective-first RL and known-policy validation; our task audits a different reward family. |

## cong2026

| Field | Extraction |
|---|---|
| locator | §3 pathwise-gradient Eqs. (19)–(20), printed pp. 20–21; empirical sample discussion and baseline results. |
| problem | Direct goal-oriented allocation with path-dependent objectives. |
| objective | Trajectory objectives including window Sharpe and terminal utility. |
| reward | Differentiable whole-trajectory score; baseline 12-month Sharpe. |
| algorithm | Transformer representation, cross-asset attention, deterministic pathwise policy gradients. |
| market | US stocks; main OOS1990–2016. |
| metric | Sharpe, alpha, costs and economic restrictions. |
| result | Reports Sharpe above two in main and restricted universes. |
| studies_reward_objective | Yes; explicitly accommodates non-additive objectives. |
| time_inconsistency | Distinguishes additive Bellman from path objectives, not our equilibrium target. |
| known_benchmark | Empirical benchmark portfolios; no known true market policy. |
| project_relation | Refutes broad claims that financial RL only uses additive rewards. Our exact audit is complementary; no AlphaPortfolio reproduction. |

## finrobot2024

| Field | Extraction |
|---|---|
| locator | Section 3.1, Figure 2; Section 5; Section 6 future work. |
| problem | LLM financial workflows. |
| objective | Task-specific forecasting and reporting; no single terminal-MV objective. |
| reward | No portfolio-reward benchmark used here. |
| algorithm | LLM agents, tools, FinGPT forecasting. |
| market | US/Chinese-stock forecasting and report demonstrations. |
| metric | Illustrative outputs in the cited sections. |
| result | Platform demonstrations; allocation listed as future work. |
| studies_reward_objective | No portfolio reward-to-MV identity in the cited sections. |
| time_inconsistency | Not treated in the cited sections. |
| known_benchmark | Not a closed-form allocation control comparison. |
| project_relation | Motivates tool-boundary validation only; not implemented, evaluated or claimed to fail. |

## markowitz1952

| Field | Extraction |
|---|---|
| locator | pp. 77, 81–83 and 89–91; Figures 1–7. |
| problem | Portfolio choice given return beliefs. |
| objective | Efficient mean–variance combinations. |
| reward | Not RL; portfolio mean and covariance-based variance. |
| algorithm | Geometric efficient-set construction. |
| market | Stylised securities; no historical backtest. |
| metric | Expected return and variance. |
| result | Characterises efficient portfolios and the role of covariance in diversification. |
| studies_reward_objective | Direct objective formulation; no reward-surrogate experiment. |
| time_inconsistency | Static model. |
| known_benchmark | Known efficient frontier conditional on beliefs. |
| project_relation | Supplies target/control foundation, not a claimed new objective or empirical algorithm reproduction. |

## demiguel2009

| Field | Extraction |
|---|---|
| locator | Table 1 methods; Table 2 and Appendix A.2 industry data; Section 2, Eqs. (12)–(17); Tables 3–6; Proposition 1, Figure 1 and Appendix B; Section 6.1. |
| problem | Allocation under estimation error. |
| objective | Mean–variance utility and out-of-sample certainty equivalent. |
| reward | No RL reward; mean minus gamma/2 times variance. |
| algorithm | 14 plug-in, Bayesian, constrained, combination and robust models versus rebalanced 1/N. |
| market | Seven monthly datasets, including ten industries plus market; simulated N=10,25,50. |
| metric | Sharpe, CEQ, turnover and transaction-cost return loss. |
| result | No method consistently beats 1/N across datasets and metrics; required estimation length depends on N and true investment opportunities. |
| studies_reward_objective | Studies utility loss from estimation; not additive reward distortion. |
| time_inconsistency | No equilibrium time-inconsistent control. |
| known_benchmark | Known population optimum in Gaussian analysis/simulation; 1/N empirical hurdle. |
| project_relation | Retain 1/N, add N=30/49 checks at fixed L=120; distinguish estimation from reward mismatch. Not a reproduction of their dates, 14 methods, 50bp costs or normalised tangency portfolios. |

## ledoit2017

| Field | Extraction |
|---|---|
| locator | Sections 1–3 (portfolio loss and nonlinear shrinkage); Section 4.1 data; Section 4.3, Eqs. (17)–(20), Table 1. |
| problem | Covariance estimation in large portfolios. |
| objective | Minimise variance or portfolio-specific estimation loss. |
| reward | No RL reward. |
| algorithm | Rotation-equivariant nonlinear covariance eigenvalue shrinkage, with a factor-preconditioned extension. |
| market | CRSP daily stocks; 1973–2011 out-of-sample; N=30,50,100,250,500; 250-day covariance windows. |
| metric | Out-of-sample standard deviation primarily; excess return and Sharpe also. |
| result | Nonlinear shrinkage improves on linear shrinkage in Table 1; gains stronger at larger N. |
| studies_reward_objective | Matches evaluation loss to objective; not RL surrogate calibration. |
| time_inconsistency | Static estimated allocation. |
| known_benchmark | Population GMV formula; empirical competitors including 1/N. |
| project_relation | Motivates objective-specific evaluation and estimation controls. Our 10% diagonal shrinkage is NOT this estimator; no replication or performance superiority claimed. |

## garleanu2013

| Field | Extraction |
|---|---|
| locator | Section II Eqs. (3)–(5); Section III Propositions 2–3; Section VI and Tables I–II. |
| problem | Optimal trading with predictable returns and costly rebalancing. |
| objective | Discounted expected excess gains minus per-period variance and quadratic trading costs. |
| reward | The additive control objective is explicitly defined; not an RL reward approximation to terminal MV. |
| algorithm | Closed-form dynamic programming, partial adjustment toward an aim portfolio. |
| market | 15 commodity futures, daily, January 1996–January 2009. |
| metric | Gross and net Sharpe; comparison with frictionless Markowitz and static-cost controls. |
| result | Table II: dynamic net Sharpe .58/.53 versus static alternatives under two cost settings. |
| studies_reward_objective | Direct economic objective; no reward mismatch audit. |
| time_inconsistency | Time-consistent discounted stage objective, not terminal-MV equilibrium. |
| known_benchmark | Closed-form optimal policy under the model. |
| project_relation | Explains why continuation/cost-aware benchmarks matter. Our rolling one-period L1-cost target is neither their dynamic optimum nor a reproduction. |

## demiguel2024

| Field | Extraction |
|---|---|
| locator | Sections I.A–C; Eqs. (3), (6), (10); Tables II–III. |
| problem | Multifactor volatility timing. |
| objective | Mean–variance net of costs. |
| reward | No RL reward. |
| algorithm | Nonnegative factor weights affine in inverse market volatility. |
| market | Nine equity factors; CRSP/Compustat; out-of-sample 1977–2020. |
| metric | Net Sharpe, alpha, costs. |
| result | Table II: conditional/unconditional Sharpe 1.062/.940; p=.006. |
| studies_reward_objective | Direct objective; no surrogate audit. |
| time_inconsistency | No terminal equilibrium. |
| known_benchmark | Unconditional portfolio comparator. |
| project_relation | Positive cost-aware finance example; motivates preserving cost preferences. Not reproduced. |

## kolm2025

| Field | Extraction |
|---|---|
| locator | p.82 scope; Exhibit2 p.84; Portfolio Allocation pp.87–88; Learning Investor Preferences p.88; Practical Challenges pp.89–90; Takeaways pp.90–91; Exhibit3 p.92. |
| problem | Explain applications and practical adoption of RL in sequential financial decision-making. |
| objective | Multiple investor mandates: performance, risk, hedging, costs and preference-sensitive allocation; no single new objective. |
| reward | Discusses PnL, risk-adjusted returns, variance reduction, cost penalties and investor preferences. No operational reward equation or calibration values supplied. |
| algorithm | Educational discussion of RL/DRL, PPO/actor–critic, recurrent methods and inverse RL; no original algorithm experiment. |
| market | No original dataset; discusses historical-data and simulated applications from other papers. |
| metric | No original quantitative evaluation; discusses performance/risk/cost criteria in cited applications. |
| result | Recommends mandate-aligned rewards, strong forecasts, realistic validated simulators, sequential use cases and hybrid classical/RL approaches (pp.90–92). |
| studies_reward_objective | Yes, qualitatively and explicitly (pp.90–91); no reward-induced-policy identity, exact mismatch bound or numerical calibration test. |
| time_inconsistency | Discusses intertemporal decisions, but no formal terminal-MV precommitment/equilibrium or time-inconsistency analysis. |
| known_benchmark | Discusses existing known-optimal-policy comparisons (p.87) and hedging benchmarks (p.86); supplies no new quantitative benchmark. |
| project_relation | Full-text motivation for a quantitative mandate-alignment check between reward specification and training (Exhibit2). Separates forecast quality from reward fidelity, and given-mandate validation from inverse preference inference. No invented 2025 performance row; 2019 raw-reward adaptation remains distinct. |

## habibnia2024

| Field | Extraction |
|---|---|
| locator | Section 3.4 Eqs.2–8; Tables 2–4; Section 4.1. |
| problem | Two-sided crypto allocation with lending. |
| objective | Profit with asymmetric loss/cost penalties. |
| reward | Eq.8: (sum Profit − penalty*(sum Loss + sum Cost/5))/deployed capital; penalty=25. |
| algorithm | SAC with CNN and multi-head attention. |
| market | 12 Binance perpetual crypto futures; two 16-month periods, each 12 training/4 testing; four-hour rebalancing. |
| metric | Return, Sharpe, Sortino, drawdown, Calmar. |
| result | Table4 reports total returns 575.585% and 145.627%; not reproduced here. |
| studies_reward_objective | Defines reward and empirical comparison; no equivalence to our MV reference established. |
| time_inconsistency | No terminal-MV equilibrium analysis identified. |
| known_benchmark | Return-RL/MV/MAD/CVaR controls, not a known dynamic optimum. |
| project_relation | Explicit long-only unit-capital assetwise reward restriction; no SAC, loans or crypto replication. Separate convex-financing theorem/test is not their environment. |

## ledoit2004identity

| Field | Extraction |
|---|---|
| locator | Section 3.3, Lemmas 3.2–3.4 and Theorem 3.2; Section 4 simulations. |
| problem | Ill-conditioned high-dimensional sample covariance. |
| objective | Quadratic covariance estimation loss. |
| reward | Not RL. |
| algorithm | Data-driven linear shrinkage toward scaled identity. |
| market | Monte Carlo covariance models. |
| metric | Covariance quadratic loss and conditioning. |
| result | Asymptotic optimality within linear shrinkage class; finite-sample simulation support. |
| studies_reward_objective | No RL reward analysis. |
| time_inconsistency | Not applicable. |
| known_benchmark | Known population covariance in simulation. |
| project_relation | Implemented centred estimator; final covariance multiplied by L/(L−1); checked independently against scikit-learn. No guarantee of realised MV superiority. |

## ledoit2004correlation

| Field | Extraction |
|---|---|
| locator | Working paper Section 3, Appendix A Eq.3, Appendix B Eq.5; Section 4 Tables 1–3. |
| problem | Noisy covariance inputs in active portfolio management. |
| objective | Covariance quadratic loss; active portfolio risk. |
| reward | Not RL. |
| algorithm | Sample covariance shrunk toward constant correlation with estimated intensity. |
| market | Monthly US stocks, 1983–2002 evaluation in inspected working paper. |
| metric | Realised information ratio and tracking error. |
| result | Reports improved information ratios relative to sample covariance. |
| studies_reward_objective | No RL surrogate audit. |
| time_inconsistency | Not applicable. |
| known_benchmark | Index-relative portfolio comparators. |
| project_relation | Implemented target and fourth-moment intensity; unbiased-unit rescaling; direct elementwise formula test. Different long-only monthly industry environment. |

## fan2008

| Field | Extraction |
|---|---|
| locator | Final Section 2 Eqs.2–5; Section 4 portfolio allocation; Section 5 simulation. |
| problem | Covariance estimation with observed factors and growing dimension. |
| objective | Covariance estimation and portfolio risk. |
| reward | Not RL. |
| algorithm | OLS factor loadings, factor covariance and diagonal residual covariance. |
| market | Simulation with observed factor structure. |
| metric | Covariance error, inverse error, portfolio risk. |
| result | Convergence results describe when factor structure provides substantial or limited benefits. |
| studies_reward_objective | No reward calibration. |
| time_inconsistency | Not applicable. |
| known_benchmark | Known covariance and population portfolios in simulations. |
| project_relation | Market and three-factor adaptations use intercept and residual dof L−K−1, unlike their no-intercept ML residual convention. Correlated-residual simulation tests misspecification. |

## halperin2025chapter

| Field | Extraction |
|---|---|
| locator | Risk-Aware RL: Beyond Expected Returns, printed pp.99–100; policy and validation discussion. |
| problem | Practical financial RL/IRL introduction. |
| objective | Multiple risk-sensitive financial objectives. |
| reward | Includes expected return minus variance penalty. |
| algorithm | Tutorial; no single empirical comparator. |
| market | Illustrative applications. |
| metric | Multiple application-specific measures. |
| result | Emphasises risk objectives and validation. |
| studies_reward_objective | Discusses risk-sensitive objective formulation. |
| time_inconsistency | No terminal-equilibrium claim used here. |
| known_benchmark | Not used as numerical benchmark. |
| project_relation | Accessible primary background; not silently substituted for the paywalled JPM article and not needed for its unverified details. |

## lesmana2025

| Field | Extraction |
|---|---|
| locator | Read preprint §§3.2.2,4.1–4.4,5.4–6; Algorithm 5 (p.47), Theorems 26–27 (pp.21–22); Figs.1–4 discussed in §5.4. |
| problem | Time-inconsistent sequential decisions. |
| objective | Subgame-perfect equilibrium; illustrative terminal mean–variance. |
| reward | Adjusted action values and auxiliary moment functions. |
| algorithm | BPI; tabular Q-learning and deterministic actor–critic. Final abstract calls it EBPI. |
| market | Preprint: simulated risky/riskless market, annual mean ±20%, volatility30%, 100 steps. |
| metric | Policy/critic convergence and terminal mean/standard deviation. |
| result | Preprint §5.4 reports policy approach to the known benchmark; critics initialised near true parameters. |
| studies_reward_objective | Yes. |
| time_inconsistency | Explicitly. |
| known_benchmark | Analytical policy in preprint §5.4.2. |
| project_relation | Backward equilibrium learning is prior art. Our learner is a structured adaptation, not a published-algorithm reproduction. Candidate addition is a finite-iterate deviation certificate; final-version overlap still needs checking. |

## guo2026

| Field | Extraction |
|---|---|
| locator | Read §§1–2, Theorem4.2 statement and proof opening, §5 Algorithms1–3, §6.1 including Eqs.(6.1)–(6.6) and Figs.1–4 discussion. |
| problem | Continuous-time time-inconsistent control. |
| objective | Deterministic equilibrium; terminal MV and non-exponential tracking. |
| reward | Auxiliary-function-dependent modified running reward. |
| algorithm | DPG with inner fixed-point iterations and martingale critic learning. |
| market | Synthetic financial diffusions; MV example uses one risky asset. |
| metric | Relative policy/value error and learning stability. |
| result | Inner fixed-point convergence theorem; reported MV learning comparisons with entropy-regularised q-learning. |
| studies_reward_objective | Yes: two-stage reward reformulation. |
| time_inconsistency | Explicitly. |
| known_benchmark | Analytical MV equilibrium, Proposition6.1. |
| project_relation | Rules out novelty in merely learning auxiliary rewards or using DPG for equilibrium. Our proposed audit concerns finite-iterate discrete-state deviation gains, not their general continuous-time method. |

## sangadi2025

| Field | Extraction |
|---|---|
| locator | Read abstract, §§3–5 theorem statements, Algorithm2, Eq.(15), Theorem4.3 and Assumption8; detailed appendix proofs not fully checked. |
| problem | Risk-sensitive discounted MDP learning. |
| objective | Mean minus penalised variance of discounted return from an initial state. |
| reward | MDP rewards with a return-level variance objective. |
| algorithm | Tail-averaged linear TD critic, SPSA actor. |
| market | Theoretical finite-state/action discounted MDP; no financial dataset in the inspected analysis. |
| metric | Critic estimation bounds and expected squared policy-gradient norm. |
| result | Theorem4.3 gives O(n^(-1/4)) actor-iteration stationarity bound under stated assumptions. |
| studies_reward_objective | Yes: distinguishes return variance from reward volatility. |
| time_inconsistency | Not a subgame-equilibrium target. |
| known_benchmark | Theoretical stationarity reference; not a portfolio benchmark. |
| project_relation | Finite-sample MV actor–critic guarantees already exist. Our audit seeks per-state one-step equilibrium deviation, a different certificate, not a better general convergence rate. |

## chen2025seminorm

| Field | Extraction |
|---|---|
| locator | §2.1 Proposition2.1 and Lemma2.1, §2.2 Theorem2.1, §5.2 Eq.(17). |
| problem | Seminorm-contractive stochastic approximation and average-reward RL. |
| objective | General fixed points and average reward, not financial MV. |
| reward | Generic average-reward MDP. |
| algorithm | Seminorm stability theory, TD and Q-learning applications. |
| market | Theoretical models. |
| metric | Seminorm error and finite-sample convergence. |
| result | Establishes fixed-point/convergence results allowing irrelevant kernel components. |
| studies_reward_objective | Analyses value-learning geometry. |
| time_inconsistency | Not the financial subgame-equilibrium problem. |
| known_benchmark | Fixed-point solution classes. |
| project_relation | Constant-shift invariance, quotient critics and seminorm learning are prior art. Candidate contribution is their specific link to MV deviation gain; no claim to invent centring. |

## maurer2009

| Field | Extraction |
|---|---|
| locator | §1.1 Theorem4, PDF p.2. |
| problem | Data-dependent concentration and learning. |
| objective | Statistical risk estimation/variance penalisation. |
| reward | Not an RL reward. |
| algorithm | Empirical Bernstein bounds and sample variance penalisation. |
| market | General bounded independent data. |
| metric | Confidence bounds and excess risk. |
| result | Theorem4 provides a sample-variance-dependent confidence radius. |
| studies_reward_objective | Not applicable. |
| time_inconsistency | Not applicable. |
| known_benchmark | Known population expectation in theoretical analysis. |
| project_relation | We use Theorem4, p.2, on both tails of fixed-policy audit quantities; the concentration inequality is not ours. |

## schulman2017

| Field | Extraction |
|---|---|
| locator | Eq. (7), Section 5 / Algorithm 1 (p.5), Section 6.1 / Table 1 (p.6). |
| problem | Stable policy improvement with repeated minibatch updates. |
| objective | Expected cumulative task reward; not a portfolio objective. |
| reward | Environment rewards; clipped likelihood-ratio surrogate for policy optimisation. |
| algorithm | PPO with clipped objective, actor–critic and GAE. |
| market | MuJoCo continuous-control tasks and Atari; no financial data. |
| metric | Normalised cumulative task reward and learning curves. |
| result | Section 6.1 Table 1: clipping at 0.2 scores 0.82 versus -0.39 without clipping or penalty on its normalised benchmark; these are external reported values, not our results. |
| studies_reward_objective | Studies policy-optimisation surrogates, not whether a financial reward implements terminal MV. |
| time_inconsistency | No financial equilibrium analysis. |
| known_benchmark | Task/environment baselines, not closed-form portfolio policies. |
| project_relation | A standard optimiser used in a matched reward intervention. SB3 implementation and sample-only continuation refresh are disclosed. We do not replicate the original nonfinancial tasks, claim to improve PPO generally, or equate its compute budget with the direct-gradient learner. |
