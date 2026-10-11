> Current-state notice (22 September 2026): this is a historical diary. The latest dated entry and FINDINGS.md supersede earlier proof, novelty, numeric and completion claims.

# Work log

Everything done from the start of implementation, in order, including the
mistakes. Written so that a reader can reconstruct why each piece exists and
which claims have been checked against what.

---

## Stage 1 — Ground truth

**Goal.** Nothing downstream can be measured until the reference optimum exists
and is known to be correct.

**Built.**

- `market.py` — i.i.d. multi-period market with specified first two moments.
  Exposes `nu = m^T M^-1 m`, the invariant everything later depends on.
- `policies.py` — the Li–Ng pre-committed optimum. The embedding multiplier
  satisfies `lambda = 1 + 2 phi E[x_T]`; since `E[x_T]` is affine in `lambda`,
  this fixed point is solved exactly from two evaluations rather than iterated.
- `evaluate.py` — two evaluators for `J = E[x_T] - phi Var(x_T)`: exact moment
  propagation for affine policies, and Monte Carlo for anything. Having both
  matters, because the Monte Carlo one is validated against the exact one before
  being trusted on learned policies.
- `verify.py` — the check suite.

**Mistake caught here.** The first version of the "is the closed form optimal?"
check used Nelder–Mead, which failed to converge in 24 dimensions and therefore
passed *vacuously*: it only confirmed the optimiser did not **beat** the closed
form. Replaced with eight L-BFGS-B restarts requiring agreement in **both**
directions. They now converge to 2.6e-12 with spread 7e-12, and the gradient of
`J` vanishes at the closed-form policy (1.7e-9).

**Finding, unplanned.** `inconsistency.py` compares the committed plan at `t=0`
against a fresh re-solve at `t=1`. The disagreement is affine in wealth and
vanishes at exactly one point — `E[x_1]`, the wealth the earlier self expected,
to 1.8e-15 across markets, horizons, risk aversions and asset counts. Mechanism:
`lambda` is pinned by `E[x_T]`, so when realised wealth matches expectation the
re-solve recovers the same `lambda`.

**Mistake caught here.** The first write-up of that finding claimed the reversal
was "present on the expected path, not only in the tails". The opposite is true.
Corrected before it went anywhere.

---

## Stage 2 — The second reference policy

**Built.** `equilibrium.py` — the consistent-planning (Björk–Murgoci) policy by
backward recursion. The moment functions `f = E[x_T]` and `g = E[x_T^2]` under
the equilibrium continuation are affine and quadratic, which closes a recursion
in five coefficients.

**Verified against the definition directly**: at a range of times and wealth
levels, L-BFGS-B is asked to beat the equilibrium action with the continuation
held fixed. Best improvement found: 0.

**Structural result.** `alpha_t = 0` identically, equivalently `A_t^2 = B_t`.
The equilibrium control holds a constant *amount*, not a constant fraction.
This reproduces the known structure (Basak & Chabakauri) and is the main
independent evidence the recursion is right.

**Result.** `eps_incons = J(pi_pre) - J(pi_eq) = 0.102155409` for the demo
market, 7.2% of `J(pi_pre)`. Also: `eps_incons` scales exactly as `1/phi` and is
independent of `x0` (9e-13, 5e-15). Practically useful — it means the
time-consistency price can be dialled small relative to the other terms.

---

## Stage 3 — Is the research gap real?

**The question that forced this.** Everything to this point reproduced known
results. The proposal's contribution rested on `eps_surr != 0`, which had not
been shown.

**Built.** `surrogate.py`, `gap.py`. The key realisation: in this setting the
maximiser of an additive quadratic reward can be computed **exactly**, with no
reinforcement learning. Any gap found is therefore a property of the reward, not
of a learning algorithm — which is precisely the separation the decomposition
claims can be made.

**Three results.**

1. **The plain-return reward has no optimum.** No risk term means unbounded
   leverage: 0.88, 8.1, 80, 801, 8010, 80098 along a ray. The mean-variance
   problem it stands in for is bounded. Bai et al. report this as the most
   common reward in the surveyed literature.
2. **With a risk term, `pi_r` is a third policy.** Distance 0.19 from the
   equilibrium at the best `kappa`, 3.23 from the pre-committed.
3. **The Sharpe ratio ranks policies in the wrong order.** The `kappa = phi`
   surrogate has Sharpe 1.1955 against the equilibrium's 1.1501 and objective
   1.3166 against 1.3236.

**Correction forced on the proposal.** `eps_surr` is **not sign-definite** — at
`kappa* = 0.808` it is `-0.0025`, the surrogate beating the equilibrium. So
"eps_surr = 0 if and only if" is false, and Theorem 1 had to be restated for the
policy distance.

---

## Stage 4 — Reinforcement learning, and the complete decomposition

**Built.** `agent.py` — affine-Gaussian policy trained by REINFORCE on the
additive reward. The policy class *contains* `pi_r` deliberately; otherwise
`eps_learn` would confound optimisation with approximation error. The agent
never sees `J`.

**Mistake caught here.** The first version peaked at iteration 500 then
degraded. Cause: the Gaussian score carries `1/sigma^2`, so gradient variance
diverges as exploration anneals. Fixed by absorbing that factor into the
learning rate, which is the Fisher preconditioning for this policy class.

**Result.** `phase1.py`, the complete decomposition:

    J(pi_pre) = 1.425799294   J(pi_eq) = 1.323643886
    J(pi_r)   = 1.316579788   J(pi_hat) = 1.307875869  (5 seeds, sd 0.0032)

    eps_incons = +0.102155409
    eps_surr   = +0.007064097
    eps_learn  = +0.008703920
    sum        = +0.117923426  = J(pi_pre) - J(pi_hat), closes to 0.0e+00

**Research result.** Which term dominates depends on `phi`, with a crossover:
`eps_incons` decays as `1/phi` while `eps_surr` grows. So "is reward design the
problem?" has no configuration-free answer, and two studies disagreeing may sit
on opposite sides of the crossover.

---

## Stage 5 — Lambda

**The actual research.** Theorem 1 of the proposal needed a functional `Lambda`;
it had none.

**Method.** Symbolic derivation with sympy, verified numerically at every step.

**R1. The surrogate optimum satisfies a backward recursion.** The observation
that unlocked everything: the additive objective is a *sum*, hence
time-consistent, hence subject to dynamic programming. With `d = M^-1 m`,
`g_t = kappa(s-1) - p_{t+1} s`:

    alpha_t = -d g_t / (kappa - p_{t+1})
    p_t     = [kappa p_{t+1} - (1-nu) g_t^2] / (kappa - p_{t+1})
    1 + q_t = (1 + q_{t+1})(s - nu g_t / (kappa - p_{t+1}))

Verified against the independent optimiser to 5e-14. **The multi-asset case
reduces exactly to the scalar one** — asset-specific quantities enter only
through `nu` and the direction `d`.

**R0. Concavity is automatic** (found during the final audit). `p_t <= 0` by
backward induction, so `kappa - p_{t+1} >= kappa > 0` always. No hypothesis
needed. 4000 random configurations, never violated.

**R2. At `s = 1`, `kappa* = phi(1 - nu)` recovers the equilibrium exactly.**
`alpha_t = 0` needs `g_t = 0`, and `p_T = 0` forces `kappa(s-1) = 0`. Proved in
full. Verified to 1e-16, any horizon, any asset count, `nu` from 0.001 to 0.98,
`phi` from 0.1 to 50.

This explains the earlier unexplained numerical value `kappa* = 0.808` in the
demo market: `phi(1 - nu) = 1 x (1 - 0.1916) = 0.8084`.

**R3. For `T = 1` the gap vanishes at every `s`.** The alpha mismatch multiplies
a deterministic `x_0` and merges with beta, so one `kappa` absorbs it. The
surrogate gap is genuinely multi-period.

**R4. For `s != 1`, `T >= 2`, the gap is irreducible and linear in `(s-1)`.**
Exponent 1.0000 everywhere tested. Reason, visible in R1: to first order
`alpha_t = -d(s-1)`, independent of `kappa`, so it cannot be tuned away.

**Mistake caught here.** The first scaling fit used `min_kappa eps_surr` and
returned exponent 0.52 with residual 0.48. Cause: `eps_surr` changes sign, so
minimising it finds the surrogate *beating* the equilibrium, and it crosses zero
where the policies still differ. Switched to the **policy distance**, which gave
a clean power law. This is the same error that forced the Theorem 1 restatement.

**R5. For `T = 2` the constant is closed form:**

    c = ||d|| sqrt((2 - nu)(1 + nu)) / (2 phi (1 - nu))

Verified to 0.11% worst case, exponent 1.0000, single- and multi-asset.

**Result.** `Lambda(kappa) = |kappa - phi(1-nu)| + c_T |s - 1|`, `gamma = 1`.

---

## Stage 6 — Paper, and the second audit

Wrote the paper. Then, before finalising, searched the literature and re-checked
every claim. Both steps changed the paper.

**Priority search.** The distinction between summing per-period mean-variance
tradeoffs and Li & Ng's terminal criterion is **standard** in portfolio choice —
Gârleanu & Pedersen (2013) and DeMiguel et al. (2015) do exactly the former. So
"these objectives differ" is not a contribution and the paper does not claim it
as one. What the search did *not* turn up is the quantitative map
`kappa* = phi(1-nu)`. That may be new; the search was not systematic and this is
flagged as the single largest risk.

**Audit, six checks. Three claims changed.**

1. **The Sharpe misranking is not cherry-picked.** 519 random (market, phi)
   pairs; Sharpe and `J` disagree on the ordering in **93.1%**. The paper had
   shown one table and implied nothing; it now reports the sweep. This is a much
   stronger result than was originally claimed.
2. **The crossover exists generally**, but its location is market-specific
   (phi between 4 and 10 across random markets, against 12 in the demo market).
   The paper said "near 12" without qualification.
3. **Negative `eps_learn` is structural.** It is measured in `J` while the agent
   optimises `J_r`; a worse maximiser of `J_r` can sit closer to the `J`-optimum,
   and such perturbations of `pi_r` were exhibited directly. The paper's earlier
   explanation — "the optimiser lands either side" — was wrong.
4. **`c_T` is superlinear in the horizon, not a power law**: log-log exponent
   1.16 with max residual 0.08 over `T = 2..10`. Earlier notes said "close to
   linear".
5. Theorem 4 survives extreme parameters (worst 1.1e-10 at `nu = 0.98`).
6. Concavity never failed, which produced R0.

---

## Stage 7 — Third pass: the continuous-time limit

Ran the priority search properly rather than shallowly. It did not turn up
`kappa* = phi(1-nu)`, but it turned up something better: a reason why.

**The correction is `O(Delta)`.** With rebalancing interval `Delta`,
`nu = SR^2 * Delta + O(Delta^2)`, verified numerically. So `kappa* -> phi` in
continuous time. The equilibrium mean-variance literature works in continuous
time, where the factor is identically zero — so its absence there is expected
rather than surprising. This is an argument for novelty, not a proof of it, and
the paper says so.

It also gives the practical boundary: 11% correction at annual rebalancing,
2.7% quarterly, under 0.25% weekly. A practitioner rebalancing daily may set
`kappa = phi` safely; one rebalancing annually should not.

**External validation.** The equilibrium recursion was derived here rather than
quoted, so it needed a check against something outside this work. Discretising a
year into `n` steps and comparing against Basak & Chabakauri's continuous-time
formula gives relative differences 0.76%, 0.25%, 0.06%, 0.01%, 0.00% for
`n = 4, 12, 52, 252, 2520`. The convergence rate is itself a check on the `nu ~
SR^2 Delta` scaling.

Both added to the paper as Section 4.2 and to the verification subsection.

---

## What is not done

- **The priority search.** Now done across the equilibrium mean-variance and
  dynamic-trading literatures; `kappa* = phi(1-nu)` did not appear, and
  Section 4.2 of the paper explains why it would not. Still not *systematic* —
  a formal search including the operations-research and stochastic-control
  literatures remains outstanding. If the result is known, the contribution
  reduces to the decomposition, the transfer to RL, and the numerical section.
- **Theorem 8's error terms** are confirmed numerically, not bounded. It is a
  series expansion, not yet a proof.
- **`c_T` for `T >= 3`** — open.
- **The differential Sharpe ratio** — not covered. It needs the state
  augmentation `z = (x, A, B)`, which is set up in the paper but not analysed.
- **Non-i.i.d. returns** — Proposition 1 extends to time-varying moments;
  Theorem 4 does not, since one `kappa` cannot satisfy `kappa = phi(1-nu_t)` for
  all `t`. The gap is expected to be strictly positive even at `s = 1` under
  time-varying moments, but this is untested.
- **Reading the sources.** The author has not yet read Hambly §4.3, Li & Ng
  (2000), or Basak & Chabakauri (2010) in full. These underpin Sections 2–4 and
  must be read before the paper is defended.

---

## Errors caught, collected

Recorded together because the pattern is the useful part: every one was found by
a check, not by inspection.

| # | Error | How it surfaced |
|---|---|---|
| 1 | Optimality check passed vacuously (Nelder–Mead didn't converge) | Comparing the optimiser's value against the closed form in both directions |
| 2 | Claimed the reversal is present on the mean path; it vanishes there | Computing the crossing point instead of asserting |
| 3 | REINFORCE peaked then degraded | Plotting the training curve rather than reading the final value |
| 4 | `eps_surr` treated as sign-definite | Scaling fit returning exponent 0.52 with a huge residual |
| 5 | Predicted constant `c` wrong by 12–59% | Comparing prediction against measurement across configurations |
| 6 | Figure 1 contradicted Table 2 (different `kappa`) | Reading the rendered page |
| 7 | Wrong explanation of negative `eps_learn` | Auditing rather than accepting the plausible story |
| 8 | "`c` grows linearly in `T`" | Fitting rather than eyeballing |
| 9 | Concavity stated as a hypothesis when it is automatic | Testing when it fails, and finding it never does |

## 21 September 2026 — Complete input audit
Read the whole delivered project and ZIP before changes; see notes/INITIAL_AUDIT.md for coverage and contradictions. Original documents, figures, and newer standalone files preserved under archive/2026-09-21-before-audit. No separate implementation report or raw experiment records were delivered. Current source of truth will be this package; parent duplicates will point here. Dependency installation is isolated in /private/tmp/mvrl-env. Research first: general-horizon proof, reward redesign, dependent benchmark, DSR correction; proposal comes after verified results.

## 21–22 September 2026 — Research completed at a stated scope; proposal rebuilt

**PROVED:** general fixed-horizon small-interest coefficient and remainder, including global penalty minimisation near zero interest. c_T grows as T^(3/2), not linearly. A terminal-unit excess-gain reward with date-specific second-moment correction exactly recovers the independent-return equilibrium. Common raw-penalty failure under varying moments has a weighted-dispersion lower bound, with equal-nu exceptions. Corrected positivity/zero-mean/one-period qualifications; withdrew the global Lambda inequality.

**PROVED:** observed scalar regime equilibrium includes a continuation covariance hedge. Added exact joint return/next-regime backward recursions, precommitment embedding, target occupancy evaluation and an equilibrium-informed reward correction. A new independent recovery test caught an erroneous (1−nu) factor in the linear hedge correction. It was removed from both proof and implementation before reporting; final coefficient is −2phi H u Cov(P,a_next|z).

**PROVED / NUMERICALLY VERIFIED:** DSR local algebra, positive augmented variance propagation, bounded finite-horizon well-posedness; fixed-eta EWMA inconsistency. Exhaustive finite trees demonstrate dynamic continuation and sensitivity to initial A,B and eta. No fixed-kappa dynamic equivalence, constant implied risk aversion or infinite-horizon fixed point is claimed.

**NUMERICALLY VERIFIED:** 120 independent parameter configurations (720 policy records), 27 mean/volatility/correlation configurations (81 records), 30 scaling cases, time-varying and four observed-regime markets, 64 bounded reward/grid/risk-aversion comparisons, 12 DSR initialisation/decay cases, four MVPI adaptations. Closed-form policies checked with independent optimisation, enumeration and one-step deviations.

**PRELIMINARY:** 15 matched-budget training runs (five seeds, three rewards, 4,000 iterations, batch512), 360 moment-estimation records and 160 frozen-policy stress records. Redesign gives exact alignment but no learned-J advantage at current budget; AR(1) stress reverses its J advantage over raw. Included these negative findings prominently.

**Literature:** inspected primary versions of Kolm–Ritter, Jiang–Xu–Liang, Yang et al., Moody–Saffell, Bisi et al., Zhang–Liu–Whiteson, Wang–Zhou, Dai–Dong–Jia, Li–Ng, Basak–Chabakauri (thesis chapter), and Ng–Harada–Russell. Exact metadata/locators and limitations in ledger. Björk–Murgoci remains abstract-only, Ritter2017 inaccessible. Some author versions differ from final publications; no journal section numbers invented. Moody/Ng PDFs were visually inspected because extraction was corrupt. Broad absence-of-objective-analysis and first-equilibrium-RL claims are false. The adapted MVPI fixed point gives the same zero-interest calibration, proved algebraically and verified numerically. Publication priority of the quantitative results remains OPEN.

**Implementation:** stable wealth-variance propagation, corrected excess Sharpe subtraction, integrated/rewrote standalone DSR and stress scripts, replaced stale module claims, retained archival originals. Saved all outputs, histories, protocols, environment and builders. New pytest suite: 25 passed; original verifier: 10 passed. Generated ten scientific figure pairs. Proposal now centres the problem/method/result and includes comparisons, established results, limitations and proposed extensions. Paper carries the full proof appendix. Both use shared content and saved data; PDFs rendered for visual verification. README/FINDINGS/implementation report and root copies reconciled.

**Still OPEN:** unrestricted/infinite-horizon DSR, constrained/cost/dependent multi-asset exact designs, estimated continuation hedges, systematic priority verification and full published algorithm/historical replications. A completed audit/revision is not completion of every possible research extension. Old diary statements below/above are historical; current FINDINGS.md governs.


## 22 September 2026 — Restore the original LaTeX presentation

User requested that both revised documents retain the original proposal/paper format and font. Inspected the archived original sources and title pages: 11pt A4 `article`, one-inch margins, UTF-8/T1 Computer Modern, original titles and Matin Tavakoli author blocks, standard numbered headings and centred page numbers. Preserved the report-style revision in `archive/2026-09-22-report-layout/`. Replaced the ReportLab renderer with genuine LaTeX source generation and compilation; converted display mathematics and proof appendix to native LaTeX, retained all ten figures as vector PDFs, kept updated evidence labels and literature limitations. The revised research data and experiments are unchanged. The paper's proof material is now in a conventional appendix. Compilation and visual QA are recorded after the build below.

Final presentation verification: compiled both documents with pdfLaTeX (TeX Live 2026), three passes each. Proposal: 12 pages; paper: 17 pages. Both retain the original 11pt A4 article, one-inch margins, Computer Modern body/math fonts, original title/author styling, and standard page numbering. Each has ten vector figures and twelve resolved source records. No overfull boxes, missing glyph warnings, or unresolved citations/references. Rendered and inspected all pages; corrected orphan headings and awkward final-section placement. Research-output SHA256 is unchanged. Saved `results/latex_verification.txt` and compiler logs; refreshed complete delivery and added a compact standalone `latex-original-format.zip` source bundle.


## 22 September 2026 — Targeted novelty audit

Downloaded and inspected the relevant full-text sections of Czichowsky (2013), Björk–Khapko–Murgoci (2016 long preprint), Chaouki et al. (2020) and Dixon–Halperin (2020). Verified publication metadata separately and kept preprint proposition numbers separate from the shortened 2017 journal version. The dependent hedge is a specialisation of prior theory; terminal-unit variance penalisation, inverse reward inference and known-policy financial-RL benchmarks are prior art. The exact best-in-family mismatch coefficient is the remaining candidate increment, not certified novel. Access failures and screened leads are retained in literature/NOVELTY_AUDIT.md. No user input is needed to perform this audit; inaccessible papers remain explicit limits. Proposal and paper positioning are being updated without altering saved experiment results.

**User-requested stop:** paused during novelty-audit document integration to conserve usage. Full compact resume state saved in parent `CONTINUE_HERE.md`. Four-source ledger generated; document writer failed due to missing PYTHONPATH; compilation may therefore use old content. New two-case mapping test is not yet run. Updated PDFs/ZIPs are NOT final or delivered. Resume only on user request.

## Presentation edit after the user-requested pause

At the user's explicit request, revised the **pre-novelty-audit proposal** for presentation. New independent edition in `presentation/proposal.tex`, delivered as parent `proposal-presentation.pdf` and standalone LaTeX ZIP. Natural headings and connected prose; old section9 removed; five figures instead of ten; seven pages instead of twelve. Internal status/access/correction diary removed from the proposal while substantive assumptions and quantitative comparisons remain. Original format/font preserved. Three successful pdfLaTeX passes, clean warnings check and all-page visual QA. No research code, experiment results, paper, or paused novelty builders changed in this editorial turn. `CONTINUE_HERE.md` remains the checkpoint for that separate paused task.

## 26 September 2026 — Resume toward ICAIF real-data paper
User authorised finishing the checkpoint, stronger novelty search/newer journal references, historical implementation and a workshop-format paper. Selected IAFM'26 provisionally after inspecting official CFP: alignment/interpretability fit, deadline October1, anonymous ACM sigconf, non-archival. Public French industry/factor ZIPs downloaded and hashed. Real-data protocol saved before outcome inspection. New cost-coupling derivation is a corollary of the known auxiliary-variable identity and will not be advertised as a new general reward transformation. Runtime from earlier session was removed; restoring a temporary environment. Presentation proposal remains preserved separately.

## 26–27 September 2026 — Historical research completed; workshop build

Finished the checkpoint's two algebraic mapping tests; full suite now31passing and original10verificationchecks pass. Added constrained risk/cost identity with explicit attribution to existing MVPI. Downloaded French industry/factor data, froze historical protocol before inspecting outcomes, completed432monthlywalk-forwarddecisions per10methods and17prespecified robustness settings. Added paired moving-block uncertainty, common-state audit versus own-state realised paths, independent QPcertificates and full saved paths. Added5seedsoftmax optimisation diagnostic; learning error is larger than design gap at the finite budget. This is not an architecture reproduction or predictive historical RL agent.

Read and integrated five newer primary papers, bringing ledger to21. Simon et al.2026ManagementScience and Cong et al.2026NBER are positive prior objective-aware methods; broad novelty claims narrowed. The exact scalar mismatch coefficient remains the candidate increment; cost calibration is a known-identity consequence. Historical alignment confirmed; realised superiority not established. Updated FINDINGS/README/implementation status; original presentation proposal preserved. Anonymous IAFMpaper written in official acmart v2.20 sigconf. Final PDF/build QA and delivery packaging underway.

Final workshop verification: sixpages, fourfigures, one results table,13cited references selected from the21-paperledger. Officialacmart2.20,sigconf/anonymous/review; metadata author empty; no unresolved citations, missing glyphs or overfull boxes. Allpages rendered withPoppler and visually inspected; corrected smallfigurelabels, columnoverflow and floatordering. Remainingclasswarning is intentionally suppressed ACMproceedingsreferenceblock for this non-archivalworkshop. Historicalreconstructioncheckpasses; rawdatahashesverified. Currentcontinuationfile rewritten. PortableLaTeX and completeprivatecodeZIPs are generated by scripts/package_workshop.py; originalarchives/presentationproposal untouched.

## 27 September 2026 — Final workshop alternatives

Verified individual IAFM, RAIOps4Fin and AI-Driven Market Microstructure calls. Prepared audience-specific anonymous ACM versions: 6/5/5 total pages and 4/3/3 figures. IAFM is the strongest fit; RAIOps is a close alternative; monthly allocation makes Market Microstructure a secondary fit. Revised titles, abstracts, argument flow and conclusions without changing algorithms or numerical results. Preserved prior-art attribution, fitted-target scope and inconclusive realised-performance comparisons. Included accurate substantive-AI assistance acknowledgment.

All final pages visually inspected; automated checks confirm anonymous metadata, visible disclosure, page limits, resolved citations and no overflowing boxes. Sources and packaging scripts are in submissions/ and scripts/. SUBMISSION_GUIDE.md records verified deadlines, formats, archival distinctions and overlap uncertainty. These are alternatives of one study; no concurrent-submission permission or submission is claimed. Historical proposal editions preserved.

Delivery verification: all three independent LaTeX ZIPs compiled successfully after extraction to temporary folders; every page’s extracted text matches its delivered PDF. All ZIP integrity checks passed.

## 27 September 2026 — Expanded named papers and implementation report v2

At the user’s request, expanded IAFM to 8 total pages, RAIOps4Fin to 6 content + 1 reference page, and Market Microstructure to 8 total pages. Main PDFs name Matin Tavakoli; separate anonymous copies meet blind-review requirements. No affiliation/email invented. Added detailed implementation, published baseline definitions, certificate and uncertainty interpretation, robustness scope; Market Microstructure adds effective-preference algebra and saved turnover/subperiod tables. Research modules and numerical outputs unchanged. Historical reconstruction rerun: 4,320 decisions, 17 settings, 60 learning records PASS.

Created IMPLEMENTATION_REPORT_V2.tex/.pdf as an eight-page standalone explanation of the historical implementation. Previous report retained. Verified compiled paper lengths, named/anonymous identity, citations and overflow; all named paper/report pages visually inspected. Short editions preserved in archive/2026-09-27-short-workshop-editions/. Current preparation script rebuilds expanded sources from that archive and submissions/expansion/*.tex.

Final expanded delivery: all six named/anonymous portable LaTeX archives compiled independently and matched every page of their delivered PDFs. Report v2 compiled successfully in the desktop editor as well as the delivery compiler; final layout checked. Named 8/7/8 pages, anonymous 8/7/8 pages, report 8 pages. No research implementation or saved numerical experiment changed.


## AI4F addition — 28 September 2026
AI4F manuscript: 7 pages, 3 figures, ACM sigconf, single-blind; Matin Tavakoli, Amirkabir University of Technology, matin.tavakoli@aut.ac.ir. Official https://ai4f.org/ deadline 7 October 2026 23:59 AoE; no length limit; OpenReview, not CMT. Author reviewer commitment required. Source submissions/ai4f/paper.tex; root paper-ai4f-2026.pdf and ai4f-2026-submission-kit.zip. FinRobot 2024 primary-paper comparison added (ledger now 22), no replication claim. Scientific audit reran: 31 tests, 10 original checks, 4320 decisions, 17 settings; joint and risk-only identities residual <9e-18. No investment algorithm/data/results changed; added preparation/audit/package scripts. Research contribution is reward alignment, NOT real-data outperformance of recent algorithms. AI4F fit remains conditional: no LLM/end-to-end agent experiment; proposed integration is explicitly separate. IAFM/RAIOps remain stronger fits. Read AI4F_SUBMISSION_READINESS.md before submission. No submission, contact, public release or reviewer/licence acceptance made. Existing other workshop papers and Implementation Report v2 preserved.


## Final editorial revision — 29 September 2026
AI-assistance acknowledgments removed from AI4F, IAFM and RAIOps4Fin at the author's explicit request. Research-topic mentions remain. All three now have appendices: IAFM includes numerical verification and the full 17-setting table inside its eight-page limit; AI4F and RAIOps include the table and the previously completed independent calibration-identity check. No experiment, algorithm or result changed. Named copies contain Matin Tavakoli, Amirkabir University of Technology and matin.tavakoli@aut.ac.ir. AI4F is single-blind; IAFM and RAIOps have separate anonymous review files. Previous editions preserved under archive/2026-09-29-before-final-edits. Rebuild final sources with scripts/finalise_three_papers.py; older prepare scripts alone restore superseded prose.

Policy correction: ACM's 14 May 2026 authorship policy no longer requires disclosure for writing assistance alone, but requires detailed methods disclosure for AI used to conduct research, including code/analysis. Prior advice relying on older blanket acknowledgment wording was stale. The specific applicability of ACM publication policy to these non-archival/optional-CEUR workshop submissions is not established by using the ACM template. Removing the acknowledgment is an editorial action, not confirmation that disclosure obligations are satisfied. See https://prod-www.acm.bloomreach.cloud/publications/policies/new-acm-policy-on-authorship . No false human-only claim added and no submission made.

29 September author instruction: final-three-papers and both final-three ZIPs now contain NAMED copies for ALL three workshops, with Matin Tavakoli / Amirkabir University of Technology / matin.tavakoli@aut.ac.ir. No AI-assistance disclosure remains in these manuscripts. The author will add disclosures personally. Earlier anonymous variants remain separate; do not substitute them into the final-three package. Scientific content and appendices unchanged.

Latest instruction, 29 September: ALL THREE final PDFs and paper.tex sources are anonymous; author/institution/email removed, including PDF author setup. This supersedes the named-delivery instruction. Primary comparison now labels adapted Jiang et al. (2025) and MVPI/Zhang et al. (2021) rows explicitly; joint calibration (ours) row is bold, with caption clarifying that bold is identification, not best investment performance. Appendix joint-calibration column is bold. No new benchmarks or experiments claimed. Apply scripts/anonymise_highlight_final.py after any earlier source generator.

Final comparison layout: separate Method and Source / role columns; ours is last and bold. Standard controls are labelled as controls, not falsely attributed to papers. Appendix explicitly titled, lettered A/B retained, robustness rows grouped by window and values typeset in scientific notation. Three anonymous PDFs remain 8/8/7 pages. Tables and appendix pages compiled and visually checked; numerical values unchanged.

## IAFM finance and dimension revision — 1 October 2026 (in progress)
User requested IAFM-only revision. Preserved incoming manuscript in archive/2026-10-01-before-finance-revision/iafm. Read final primary papers for DeMiguel–Garlappi–Uppal (2009 RFS), Markowitz (1952 JF), Ledoit–Wolf (2017 RFS), Gârleanu–Pedersen (2013 JF), and publisher full text of DeMiguel–Martín-Utrera–Uppal (2024 JF); targeted locators and comparison roles being added to ledger. The requested diversification paper's main issue is estimation error, not a requirement for more assets; Table 2 includes ten industries plus market, Proposition 1/Figure 1 examine N and estimation length. No claim that 3000/6000 months is universal.

Added notes/DIMENSION_PROTOCOL.md before inspecting new outcomes. Downloaded 30/49 French industries (same August 2026 vintage), extended parser with date-bounded sentinel validation and complete-month checks, generalised data/run with backward-compatible n_assets=10. Added run_dimensions.py and independent verify_dimensions.py, plus four parametrised tests. All 35 tests passed. Added 6048 saved decisions; original ten-industry results preserved. New joint mean distances ~7.33e-8/1.29e-7; scalar worsens alignment in both larger universes. Joint–raw realised monthly MV −5.216/−5.670 bp with unadjusted path-bootstrap intervals wholly negative. No superiority claim; minimum variance has best realised MV among seven dimension comparators in all three universes. MVPI/log comparators were not rerun at 30/49.

Rewrote Introduction/Related Work and Section 7 around financial semantics, controlled reward interventions, faithful evaluation and model validation. Archived Sep29 official IAFM page was read; live site unreachable on Oct1, so no claim of fresh live rule confirmation. Reordered Table 1 with financial controls first, ours last. Expanded to 18 actually cited references, including five finance additions. Native proof results unchanged; joint calibration credited to MVPI identity and explicitly reference-dependent.

IMPORTANT: earlier finalise_three_papers.py/anonymise_highlight_final.py/refine_comparison_layout.py regenerate old sources and MUST NOT be run on this revision without updating them. Canonical IAFM source is submissions/iafm/paper.tex; compile this file directly.

IAFM revision completed: 8 pages including 18 references and appendix; 4 figures, 3 tables. Added independent dimension verification to appendix. All 35 tests passed and all 9072 dimension-comparison records independently reconstructed (including 6048 new records). Final PDF has resolved citations and no overflow; all eight pages visually inspected. The native editor compiler cannot access separate figure files, so the complete project was compiled with Tectonic. Current root `paper-iafm-2026.pdf` and `iafm-2026-latex.zip` updated, anonymous aliases synchronised; final-three package's IAFM entry updated while the other papers are unchanged. Five finance sources added to authoritative ledger (27 total); legacy generators protected against overwriting new IAFM text. No submission made. See notes/IAFM_REVISION_2026-10-01.md for changes, scientific interpretation and reproduction.

2 October 2026 final continuation: portable IAFM LaTeX archive independently compiled; all eight rendered pages are pixel-identical to the delivered PDF. Archive source files match canonical source; final-pass citations resolved, anonymity verified. Final hashes saved in submissions/iafm/qa-oct1/verification.json. User-edited abstract block 71843 was preserved; its ten-industry description predates the new 30/49-industry extension. No submission made.

3 October 2026: Table 1 source entries standardised to Author (Year). Removed citation numbers and mixed role suffixes from paper-attributed cells; source citations moved to a short note below the table grid. Method/role separation and last bold ours row retained. No data, numerical results or research code changed. Full-project compilation passes, remains eight pages; revised table visually checked; current PDF and source archives refreshed. Native preview still cannot resolve separate figure assets.

3 October 2026 final table request: every Table 1 row now has a year, ordered 1952, 1952, 2009, 2021, 2025, then 2026 controls/calibrations. Note explains 2026 means the present implementation, not invention date. Ours remains last and bold, citations below grid. Eight-page PDF compiled and table visually verified; delivery archives updated. No numerical or research-code changes.


## Research revision explanation — 5 October 2026
Created RESEARCH_REVISION_EXPLAINED.md at the user’s request: a detailed substantive comparison of the current IAFM revision with its pre-October finance-revision state. Covers the DGU reading, dimension rationale/protocol/results, five finance additions and retained learning comparisons, exact contribution and prior-art boundaries, Section 7/IAFM fit, code verification and open extensions. Excludes table and formatting edits. Numbers checked against saved dimension summaries; local evidence links checked. No manuscript, experiment, data or research-code changes; tests were not rerun for this documentation-only task.


## Covariance and reward extension — 7 October 2026 (in progress)
User requested linear shrinkage and factor covariance comparisons, Kolm/Ritter and Habibnia/Soltanzadeh references, stronger research and rewritten IAFM Section 7. Preserved incoming IAFM manuscript in archive/2026-10-07-before-covariance-revision. Fixed notes/COVARIANCE_PROTOCOL.md before inspecting new outcomes. Reading primary estimator/reward papers; Kolm/Ritter JPM full text not yet accessible, so no unverified section-specific claims. New analysis will separate estimator-specific fitted references from reward mismatch.


## Covariance extension completed — 7 October 2026
Read primary Ledoit–Wolf (2004 JMA and 2003 working paper for 2004 JPM), Fan–Fan–Lv (2008 final), Habibnia–Soltanzadeh (2024 v1), and separate accessible Halperin/Kolm/Ritter CFA chapter. Requested Kolm–Ritter 2025 JPM metadata/abstract verified; paywalled full text not claimed read. Six new ledger records (33 total); manuscript 24 citations, including reintroduced 2019 Kolm–Ritter raw-reward context.

Added covariance.py/financing.py, independent estimator tests, protocol-fixed 18 historical cases, 2160 known-covariance fitted problems and 50 financing states. Subsequently added an explicitly exploratory single MVPI update without a supplied target, preserving primary outputs. Main runner now includes it; old-cache extension script retained. All 50 tests pass; all 58320 historical decisions and all synthetic outcomes independently reconstructed; 144 anchor-bound checks pass. Historical raw data/vintage unchanged. New exact deterministic-cost/anchor and covariance sensitivity arguments are corollaries, not claimed inventions of MVPI. Full result and interpretation detail: COVARIANCE_RESEARCH_REPORT.md.

Joint mean alignment <1.60e-7 throughout; scalar worsens distance and fitted regret in all 12 larger cases; one-step mean-distance reduction 97.8–98.6%. No realised investment-superiority claim. Factor model helps the correctly specified simulation but not every residual design. Financing charges must scale with turnover. Restricted downside comparator is not a SAC/crypto replication.

Rewrote IAFM abstract, related work, experiments, Section 7 and appendices; regenerated two new figures and both tables. Three figures total (retained exact-theory figure). The earlier seventeen-setting and learning experiments are still discussed and preserved in results, but their old figures/table were replaced to fit the covariance evidence. Font, margins, anonymous template and title retained. Built-in compiler still cannot resolve multi-file figure assets; full-project Tectonic compiles eight pages with 24 references and no overflow or unresolved citations. No submission/contact performed. Portable packaging and final rendered QA are recorded in submissions/iafm/qa-oct7/verification.json.


## Kolm–Ritter full-text integration — 9 October 2026
User supplied final journal PDF 10.3905_jpm.2025.1.782_6ip4.pdf. Read all 15 pages (printed81–95), all three exhibits, conclusion and references; rendered/inspected every page. Exact source hash and coverage recorded in literature/covariance-update/kolm2025-fulltext-manifest.json. The earlier full-text access limitation is resolved. No journal PDF added to delivery archives.

Updated manuscript Introduction/Related Work/Section7 with exact full-text pages/exhibits: reward/mandate alignment90–91, workflowExhibit2p84, known-policy precedents87, inverse-RL88, scalability88/90, static-optimisation guidance90 and forecast-quality distinction91. Paper is explicitly an equation-free overview with no new numerical comparator; did not relabel 2019 baseline as2025 or invent results. Tightened abstract's “only when” to a sufficient joint-scaling statement; no universal necessity theorem was proved. Preserved title, font, anonymity, all numerical results and figures. Updated current source builder to retain changes.

New detailed note: notes/KOLM_RITTER_2025_FULLTEXT_REVIEW.md. Ledger remains33 records, now full-text entry forkolm2025; manuscript24 references. Updated README/FINDINGS/novelty audit/report/checkpoint. 128 research code/test/data/result files verified byte-identical to prior code archive; no research tests rerun for this literature-only revision. Full-project compilation:8pages,no unresolved citations or overflow. Native compiler still cannot resolve external figure assets. Preserved incoming manuscript/ledger under archive/2026-10-09-before-kolm-fulltext. Portable source and research delivery archives refreshed; final visual/portable QA under submissions/iafm/qa-oct9. No submission/contact performed.


## RL extension started — 9 October 2026
Reread canonical IAFM and underlying dependent/theory/learning code. Identified oracle continuation in existing regime correction and absence of shared neural sequential learning. Read primary algorithm/theory/experiment sections of Guo–Huang–Yu2026 arXiv2606.11798v1, Lesmana–Pun2021 arXiv2110.14295v1 (2025 SIAM metadata verified; final full text not obtained), Sangadi et al.2406.07892v2. No first-equilibrium-RL or first-modified-reward claim is viable. Candidate new direction is an a posteriori one-step-deviation certificate decomposing reward, actor, and continuation-critic errors; priority still open.

Protocol fixed in notes/rl-extension/PROTOCOL.md; derivation in RESIDUAL_CERTIFICATE.md. Added equilibrium_audit.py, equilibrium_learning.py, neural_equilibrium.py and tests. 14 new tests pass, including independent terminal-moment deviations, vector covariance inequality, terminal critic errors, constant-offset invariance and observable holdout certificate. Initial tabular grid complete:2160 method/seed/configuration records,20 seeds,9 markets,4 sample sizes. Neural pilot running; no neural conclusions yet. Existing IAFM/source/builders/finance results unchanged; manuscript rewrite deferred until evidence stabilises.

RL extension results: derived the mean–variance one-step deviation identity, constant-shift-invariant residual-span bound, actor/reward/critic split, and fixed-convex-action corollary. These are proved within the stated exogenous-regime/wealth-independent policy assumptions; publication priority remains open. Added observable held-out Hoeffding certificate, then exploratory Maurer–Pontil empirical Bernstein and confidence-bounded mixing refinements; 20/20 covered per construction, not proof from coverage. Mean bound .036141→.004911 versus true mean maximum .000902; audit needs786432 observations/policy.

Completed2160tabular records (9markets×4budgets×20seeds×3methods) and135shared-neural training runs/405checkpoints. At3000updates averagedover9markets×5seeds, centred-critic continuation-aware policy D=.238264 vsmyopic .610208 (61.0% lower); deviation .000559 vs.003042 (81.6% lower). Ordinary continuationcritic D=.241841: centring adds only1.48% distance improvement, not a new broadly dominant RL algorithm. Primary algorithms are structured adaptations; no claimed published SPERL/DPG-FPI reproduction. No new real-data RL outcome. Existing paper/financecode unchanged. All2565records reconstructed, error<4.45e-16,zero testedboundviolations. Two new figures visually checked; report RL_EXTENSION_REPORT.md.

Five primary-paper records added (38total); targeted full-text reading coverage explicit. Final Lesmana2025text not obtained: read2021preprint, never silently treatedasfinal. Guo2026DPG-FPI and Chen2025seminorm work narrow priority; no first-equilibrium-RL/firstcentredcritic claims. Saved exactStageAprotocolhash; neuralpilot fixed before its outcomes. Runtime /private/tmp/mvrl-rl-oct9/bin/python.

Final verification for this RL phase: **74 tests pass** (50existing+24new), 3.67seconds; savedresults/rl-extension/test_status.json. All2565records reconstructed again after constrained-audit extension; residual4.44e-16,zero violations,originalresearchfilesunchanged. Regenerated/visuallychecked finalplots after fixingcrowdedneuralx-axis labels. No pending processes. ReadRL_EXTENSION_REPORT.md forscope andnextsteps.


## Final IAFM delivery — 9 October 2026

Completed unchanged-protocol neural extension (20 seeds, 9 markets, 540 runs / 1620 checkpoints) and matched PPO reward intervention (10 seeds, 2 markets, 40 runs). All final records reconstructed; max error 4.44e-16; zero certificate violations. 78 tests pass, including four new PPO checks. Neural distance/deviation improvements 59.2%/81.4%; PPO 33.3%/49.8%. Centring adds 0.57% policy improvement over ordinary continuation and reduces the model-based bound 27.1%. Saved paired seed-bootstrap intervals; no run/checkpoint selection. Tracked finance code/results unchanged.

Rewrote canonical IAFM around the deviation certificate, with full proof, convex constraints, independent-data appendix, new neural/PPO table and three evidence figures. Eight total pages, 29 cited references; ledger39. Preserved prior paper. Guarded historical covariance generator. Added FINAL_RESEARCH_REPORT.md, refreshed submission package and continuation checkpoint. No real-data RL backtest or first-ever novelty claim invented. Official extended IAFM deadline 12 October2026 23:59AoE verified; no submission/contact. Author supplies submission declarations.

Final delivery QA complete: all eight pages visually reviewed; independently rebuilt LaTeX archive pixel-identical on all eight pages; no overflow/unresolved citations; anonymous text and metadata. PDF/source aliases refreshed; private code/results ZIP verified (966 files, 58.5 MB).

9 October 2026: added RESEARCH_EVOLUTION_REPORT.md at user request. Compared the pre-covariance, completed finance, and final RL manuscripts; explains the substantive pivot, preserved/compressed material, estimator/financing results, RL theory and experiments, exact comparison scope, code changes and open historical-RL extensions. Report only; no manuscript, code or numerical results changed.

Expanded evolution report with an explicit assessment and defence of the pivot: stronger RL validation capability, weaker simplicity, unchanged historical performance evidence, novelty/conditional-data qualifications, reviewer objections, and conditions that would reverse the assessment. No research results altered.


## GitHub repository update — 11 October 2026

Compared the clean public main branch at b9372ef (23 September 2026) with the completed research workspace. Synced the historical/dimension study, covariance/factor/financing extension, RL learners and certification evidence, final IAFM manuscript, literature records and substantive reports in separate commits. Preserved previous overview in archive/2026-09-23-repository. Rewrote the public README around the current paper and reproduction commands; added CI and a current-manuscript checker. Strengthened five historical source-builder guards (four updated, one existing) and allowed the intentional final-paper replacement in the older pilot preservation checker while retaining all code/result checks.

Verification: 78 tests pass; 4,320 primary, 9,072 dimensional and 58,320 covariance-study decisions reconstructed; 2,160 covariance simulation problems and 50 financing states verified. Final 1,660 neural/PPO records reproduce to 4.44e-16 with zero tested certificate violations. Re-generated final numbers and figures are byte-identical to the research workspace. Current PDF checks: eight pages, 29 references, three figures, two tables, anonymous text and metadata. All Python sources parse; five legacy source guards exercised successfully. Exact audit record: results/repository-sync-20261011.json. No new training or financial claims added. New downloaded external full texts, scratch/build products and optional PPO binary checkpoints are excluded; source data and saved actions/critics remain reproducible.
