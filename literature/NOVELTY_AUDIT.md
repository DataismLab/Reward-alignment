# Full-text update — 9 October 2026

All 15 pages of Kolm–Ritter (2025 JPM) were read from the user-provided final PDF, including Exhibits 1–3 and references. The former abstract-only limitation is resolved. Printed pp. 90–91 explicitly recognise reward-design/mandate alignment; p. 87 discusses known-policy comparisons. These are positive prior-art context, precluding first-recognition or first-benchmark-validation claims. The article is an equation-free educational overview (p. 82), not an empirical method with a reward formula or numerical result to reproduce. It does not supply a counterexample to the scoped exact mismatch coefficient, but absence from this non-exhaustive overview is not a novelty certificate. Our given-mandate audit differs from the inverse-preference applications on p. 88. Primary follow-up leads in its bibliography remain leads, not independently verified performance evidence. See `notes/KOLM_RITTER_2025_FULLTEXT_REVIEW.md` and the source-hash manifest for exact coverage.

# Claim-level novelty audit — 22 September 2026

## Decision

**Targeted audit completed, with explicit access limits. Publication priority remains OPEN.** Mathematical correctness and originality are different questions. We can substantiate the scoped proofs; we cannot certify that no earlier paper contains an equivalent result. This audit is a relevance-led primary-source comparison, not an exhaustive systematic review.

The defensible headline is: **For a specified quadratic wealth-increment reward family, we derive the exact leading policy mismatch that remains even after optimally tuning its scalar penalty. This separates a structural reward limitation from learning error and supplies a reproducible test of when calibration must be replaced by redesign.**

The exact coefficient is the candidate theoretical increment. The correction is useful, but is presented as a concrete implementation of established equilibrium-control ideas rather than a new general reward-design principle. No claim of improved Sharpe, initial mean–variance value, or learned performance follows from this positioning.

## Claim matrix

| Project claim | Mathematical/evidence status | Priority assessment and closest inspected source |
|---|---|---|
| Precommitment and mean–variance equilibrium differ | PROVED, known | Li–Ng (2000), Basak–Chabakauri (2010), Czichowsky (2013); not a contribution of this project |
| At zero interest, scalar calibration is phi(1−nu) | PROVED | Rank-one matrix identity and the adapted Zhang et al. MVPI fixed point; do not claim novelty |
| Bellman solution for raw quadratic increments | PROVED | Standard linear-quadratic recursion specialised to this reward; a benchmark component |
| Nonzero-interest exact recovery generally fails in the raw scalar family | PROVED, scoped | Immediate final-stage wealth-slope obstruction; useful diagnosis but not strong independent novelty |
| Exact optimally calibrated fixed-horizon mismatch coefficient | PROVED within model | No equivalent formula located in the inspected sources. **Candidate increment; priority OPEN**, especially against older dynamic approximation and discrete-control work |
| Common-penalty changing-moment lower bound | PROVED | Elementary weighted least-squares projection; supporting diagnostic, not claimed new theory |
| Existence of a time-consistent objective implementing equilibrium | Known prior result | Björk–Khapko–Murgoci long preprint §8 Proposition 8.1; Björk–Murgoci (2014) abstract also explicitly states this |
| Terminal-unit independent-return correction | PROVED | Related to prior terminal-unit variance penalisation, long preprint §10.1 Proposition 10.2. Finite-step second-moment conversion below; do not claim a new general principle |
| Scalar dependent continuation hedge | PROVED | Specialisation of Czichowsky §3 Lemma 3.2 Eq. (3.3), itself crediting earlier work |
| Hedge-informed additive reward | PROVED, oracle | Requires solved continuation; a scoped implementation, not a model-free solution of dependence |
| Known optimal policy as financial-RL benchmark | Existing practice | Chaouki et al. §§1.2, 2, 3; Wang–Zhou and Dai et al. already in ledger |
| Infer rewards from target behaviour | Existing practice | Dixon–Halperin §§3–5, GIRL; not a new general inverse-RL proposal |
| Separate induced optimum from intended equilibrium, with exact mismatch law and reproducible adaptations | PROVED + NUMERICALLY VERIFIED components | Project synthesis and benchmark contribution; uniqueness of the synthesis is not certified |
| Learned or financial superiority | PRELIMINARY / unsupported as a general claim | Current five-seed and stress results do not establish it |

## Exact mathematical crosswalks

### 1. Discrete continuation hedge is prior art

Czichowsky (2013), read version arXiv:1205.4748, §3 Definition 3.1 and Lemma 3.2, manuscript p. 9, Eq. (3.3), gives

    theta_k = E[Delta S_k | F_(k−1)] / (gamma Var[Delta S_k | F_(k−1)])
              − Cov(Delta S_k, future gains | F_(k−1)) / Var[Delta S_k | F_(k−1)].

Set gamma=2phi and choose terminal-unit gains Delta S_k=H_t P_t, with theta_k=u_t. In our exogenous observed scalar regime model, future equilibrium dollar holdings depend on time and regime, not wealth. Conditioning the future gains on the next regime yields a_next. The conditional covariance becomes H_t Cov(P_t,a_next|z), and the variance becomes H_t² Var(P_t|z). The result is exactly our equilibrium formula.

This is a mapping in our stated model. Local perturbations of a predictable strategy and deviations in a feedback strategy are not automatically the same notion in every model; wealth-independent continuation is essential to this comparison. The paper itself attributes the recursion to earlier Basak–Chabakauri and an unpublished thesis. We do not assert that Czichowsky originated it.

### 2. Terminal-unit variance reward precedes our construction

Björk, Khapko and Murgoci, **2016 long preprint** arXiv:1612.03650v1, §8 Proposition 8.1, p. 23, constructs an associated standard control problem with the same equilibrium control and value. The authors explicitly note that constructing it requires knowing the equilibrium. In §10.1 Proposition 10.2, p. 33, the scalar diffusion example maximises

    E[X_T − (gamma sigma²/2) integral_t^T exp(2r(T−s)) u_s² ds].

The variance penalty is already expressed in terminal units. The related **2017 journal paper has a different title and is shorter**; its §1.2 explicitly points to the longer working paper for mean–variance examples. We cite the long preprint for these proposition numbers, not the journal version.

Our finite-step expected rewards, at one date, are

    Q_var(u) = H m'u − phi H² u' Sigma u,
    Q_design(u) = H m'u − phi(1−nu) H² u'(Sigma+mm')u,
    nu = m'(Sigma+mm')^(-1)m.

Direct subtraction gives the **PROVED algebraic comparison**

    Q_design(u) − Q_var(u)
      = phi H² [nu u'Sigma u − (1−nu)(m'u)²] >= 0.

To prove the sign, write a=m'Sigma^(-1)m, so nu=a/(1+a), and apply (m'u)² <= a u'Sigma u. For nonzero m, equality holds exactly on the span of Sigma^(-1)m. Both strictly concave functions have the same maximiser Sigma^(-1)m/(2phi H) and the same maximum. With one risky asset they are identical for all actions; with zero m they are also identical. With several risky assets and nonzero m, they generally differ away from the efficient direction.

Thus the sampled correction is a finite-step, moment-based implementation of a familiar control idea. It is not literally the continuous-time functional, nor generally identical to its discrete variance counterpart for all policies. Its practical advantage is a realised quadratic signal once moments are supplied; it does not remove the need to estimate those moments. The comparison is independently covered by test_prior_variance_reward_mapping.

### 3. What is still distinctive in the inspected material

For iid returns, positive-definite covariance, nonzero m, fixed T>=2, unconstrained dollars, known moments, s near 1, and the explicitly declared occupancy distance, our derivation gives

    min_(kappa>0) D = c_T |s−1| + O((s−1)²),
    c_T = ||d|| b sqrt[T(T²−1)/3 + nu(1−nu)T(T−1)/2],
    d=(Sigma+mm')^(-1)m, b=1/[2phi(1−nu)].

The closest inspected papers provide equilibrium policies, objective transformations, reward-volatility optimisation, or learning-versus-optimum benchmarks. Their cited sections do not give this optimised local coefficient for the raw wealth-increment family. This is a source-bounded observation, not proof that the formula is unpublished. Changing distance, occupancy, units, constraints or asymptotic regime changes the question. The coefficient's large-T growth is not a uniform joint limit theorem.

### 4. Existing benchmark and inverse-reward work

Chaouki et al. (2020), arXiv:2003.06497v2, §2.1.1 Eqs. (9)–(12), formulate additive predictor-position reward with quadratic cost and position risk; §3 Fig. 2 and Tables 1–3 evaluate DDPG against reference controls across 16 seeds. Table 1 uses an l1 position difference. This already establishes known-policy financial-RL validation. Our additional axis is reward-optimal policy versus an independently selected terminal equilibrium. Their chosen additive objective is not labelled incorrect.

Dixon–Halperin (2020), arXiv:2002.10990v1, §3 Eqs. (19)–(23), explicitly replace a one-sided target penalty with a quadratic reward; §§4–5 derive Gaussian policies and reward inference from trajectories. §6 Table 1 and Fig. 2 report recovery and imitation. This is prior portfolio reward analysis/inference, though its goal-based cash-flow problem differs from terminal mean–variance equilibrium. We do not claim its parameter recovery is exact: the table itself contains finite discrepancies.

## Search protocol and screened leads

Search date: 22 September 2026. Channels: web search, arXiv, author/institution repositories, publisher metadata/full text, and references within primary papers. Inclusion: a plausible antecedent of the exact mismatch coefficient, an implementing objective, equilibrium hedge, inverse portfolio reward, or known-policy financial-RL benchmark. Exclusion from theorem comparisons: abstract-only records, surveys alone, unrelated risk objectives, or inaccessible formulas. No paywall was bypassed and no article purchased.

Query log (phrases used; relevance search, not an exhaustive database export):

- time consistent mean variance discrete time equivalent objective reward
- Bjork Murgoci 2014 full text discrete time
- time consistent mean variance Czichowsky discrete time
- portfolio reinforcement learning inverse reward design equilibrium
- Deep Deterministic Portfolio Optimization
- G-Learner and GIRL Dixon Halperin
- quadratic wealth increment reward mean variance equilibrium calibration policy mismatch
- mean variance reward small interest calibration equilibrium
- quadratic reward policy mismatch portfolio
- On the Use of Mean-Variance and Quadratic Approximations authors 1993

Four additional full-text manuscripts and their SHA256 hashes are stored in novelty-audit/download_manifest.json. The ledger now contains 16 comparison records: 15 with primary-version sections inspected and one explicitly abstract-only. This does not mean every page of each newly located source was read; inspected sections and equations are recorded precisely.

| Additional screened source | What was actually verified | Disposition |
|---|---|---|
| Huiling Wu (2013), Time-Consistent Strategies for a Multiperiod Mean-Variance Portfolio Selection Problem, Journal of Applied Mathematics, article 841627, DOI 10.1155/2013/841627 | Publisher full-text prose, assumptions A1–A4, §3.1 Theorem 2; equation rendering missing; PDF request returned 403 | Supports an additional equilibrium-priority lead; exact Eq. (16) mapping not asserted |
| Robert R. Grauer and Nils H. Hakansson (1993), On the Use of Mean-Variance and Quadratic Approximations in Implementing Dynamic Investment Strategies: A Comparison of Returns and Investment Policies, Management Science 39(7), 856–871, DOI 10.1287/mnsc.39.7.856 | Publisher metadata and abstract; institutional 1991 working-paper PDF located, not inspected in this pass | Important older approximation lead; cannot exclude theorem-level overlap without further reading; no formula attributed |
| Gordon Ritter (2017), Machine Learning for Trading, SSRN 3015609, DOI 10.2139/ssrn.3015609 | Author PDF returned 403 again | Full-text gap; use inspected Kolm–Ritter manuscript for baseline, not unverified Ritter equations |
| Björk–Murgoci (2014), DOI 10.1007/s00780-014-0234-y | Publisher abstract and institutional metadata; attempted SSRN precursor download returned 403 | Full-text gap remains; abstract already defeats broad equivalent-objective novelty |

Primary links: [Czichowsky manuscript](https://arxiv.org/abs/1205.4748), [publisher record](https://doi.org/10.1007/s00780-012-0189-9); [Björk–Khapko–Murgoci long manuscript](https://arxiv.org/abs/1612.03650), [shorter published article](https://doi.org/10.1007/s00780-017-0327-5); [Chaouki manuscript](https://arxiv.org/abs/2003.06497), [published article](https://doi.org/10.1016/j.jfds.2020.06.002); [Dixon–Halperin](https://arxiv.org/abs/2002.10990); [Wu](https://doi.org/10.1155/2013/841627); [Grauer–Hakansson](https://doi.org/10.1287/mnsc.39.7.856), [located working version](https://digicoll.lib.berkeley.edu/record/86302/files/b120984374_C044472178.pdf).

## What would close the remaining priority question?

Inspect the missing discrete-control and approximation full texts, compare equivalent notational forms of the coefficient, and obtain an independent specialist assessment of the increment. The absence of a web-search match is insufficient. Until then, use “we derive” and “in this benchmark”, not “first”, “new general framework”, or “previous literature does not analyse rewards”. The user need not supply anything for the completed audit; an authorised copy of an inaccessible paper would help the remaining checks.

## September 26 update: recent finance literature and costs

The ledger now has **21** papers, including Simon–Weibels–Zimmermann (2026, Management Science), Jiang–Olmo–Atwi (2025, International Review of Economics and Finance; 2024, Global Finance Journal), Gollart–Okhrin (2025, Annals of Operations Research), and Cong–Tang–Wang (2026, NBER35195). Exact inspected locators and version-specific authors are in recent_records.json and the generated ledger. These papers strengthen the positive prior-art comparison: direct utility, analytical benchmarks and non-additive trajectory objectives are already supported. We do not claim financial RL universally uses arbitrary additive rewards. Older Mathematical Finance and Review of Financial Studies work remains necessary for the control reference; recent dates alone do not supersede foundational results.

The constrained joint risk/cost calibration follows the MVPI auxiliary identity. Its explicit penalty-only distortion is derived in notes/CONSTRAINED_CALIBRATION.md and verified on historical estimates. Neither is billed as a new generic algorithm. The fixed-horizon coefficient remains the narrow candidate theoretical contribution, with priority bounded by the inspected sources.

Additional searches used "reward calibration mean variance transaction costs reinforcement learning", "portfolio reinforcement learning 2025 Journal of Finance", and "portfolio reinforcement learning 2026 Review of Financial Studies". No relevant new JoF/RFS primary result was verified from these queries. Do not manufacture prestigious journal citations. Additional screened leads not used for substantive claims: European Journal of Finance DOI10.1080/1351847X.2025.2558114 (end-to-end direct RL for multi-factor MV) and DOI10.1080/1351847X.2025.2605061 (bond portfolios) returned403 for full text. JFDS DOI10.1016/j.jfds.2026.100205 was search-visible with a future December2026 issue date, but full-text access failed; excluded from empirical/theorem comparisons. The older full-text access limits above remain.
