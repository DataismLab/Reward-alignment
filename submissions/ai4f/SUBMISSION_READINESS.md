# AI4F submission-readiness audit

Checked 28 September 2026. Paper: **Checking Financial Objectives in Portfolio Tools: A Reward-Alignment Benchmark**. Author: **Matin Tavakoli**, Amirkabir University of Technology, matin.tavakoli@aut.ac.ir.

## Verdict

The manuscript is a completed, correctly scoped numerical allocation-tool paper. Its calculations and references were checked against the archived implementation and source records. **It should not be described as unconditionally ready for this particular workshop:** AI4F's central subject is LLMs and generative AI, and this study has no LLM or end-to-end agent experiment. The manuscript discloses that boundary in its abstract, introduction and proposed-integration section. Rewording cannot supply missing empirical evidence.

There is no explicit requirement in the published call that every submission include an LLM experiment. A numerical benchmark may be considered under evaluation, verification or infrastructure, but that is a topical-fit judgment for the organisers/reviewers. IAFM and RAIOps remain stronger fits for the completed evidence. For a stronger AI4F submission, either establish that a standalone allocation-tool validation paper is in scope, or conduct an actual, reproducible LLM-tool experiment before claiming agent-level validation. No organiser contact has been made.

## Verified venue rules

Sources: [official AI4F site](https://ai4f.org/) and the public [OpenReview submission invitation](https://api2.openreview.net/invitations?id=ACM.org/ICAIF/2026/Workshop/AI4F/-/Submission), archived in this folder.

| Item | Verified rule / delivery |
|---|---|
| Deadline | 7 October 2026, 23:59 Anywhere on Earth; portal due date is 8 October 2026 11:59 UTC. |
| Review | Single-blind, no rebuttal. The author's name belongs on the PDF. |
| Format | PDF; no length limit or strict format; ACM sigconf recommended. |
| Publication | Non-archival; no official proceedings. |
| File upload | PDF up to 50 MB according to the public invitation. |
| Metadata | Title <=250 characters; abstract <=5000; author profile ID or email required. |
| Reviewing | At least one author must agree to review and deliver reviews on time. |
| Author list | Finalise before the initial submission; later changes are restricted. |
| Workshop | 14 November 2026, Milan. In-person participation strongly preferred. |

The portal's current submission invitation specifies a CC BY 4.0 note licence. This has not been accepted on the author's behalf. The workshop's non-archival status does not itself establish permission for simultaneous submission of overlapping manuscripts.

## Scientific checks

- **31 pytest tests passed**, plus all **10 original verification checks** on 28 September.
- Historical reconstruction passed for **4,320 decisions**, **17 robustness settings** and **60 learning records**; data hashes, dates, constraints, costs, drift and summaries checked.
- Both calibration identities re-evaluated at four random feasible portfolios on each of 432 historical states: maximum algebraic residual below **9e-18**.
- The minimum observed positive calibration factor is **1.02079575**; largest saved common-state quadratic certificate **4.2675e-9**.
- The actual raw finite-budget decomposition at 5,000 steps is approximately **5.66e-6 = 1.48e-6 + 4.18e-6** in target-objective units. This avoids substituting own-reward suboptimality for the signed target difference.
- Primary baseline table and three figures use the existing archived results. No new historical-performance or LLM-performance result was invented.
- The MVPI and Jiang 2025 implementations are adaptations. FinRobot 2024 is a contextual primary-paper comparison, not a tested baseline. The manuscript says so explicitly.
- Joint calibration is attributed to the known mean auxiliary. It is not claimed to beat exact MVPI or to guarantee better realised investment performance.
- The reference remains a fitted one-period objective, not a known historical terminal equilibrium. Data vintage, first-order costs, primary-only logarithmic/MVPI comparators and bootstrap scope are explicit.

## Corrections made during this audit

1. Added the correct AI4F title, event, single-blind author information and contact details.
2. Reframed the contribution as numerical validation of an allocation tool, with a separately labelled proposed LLM-workflow use.
3. Added and verified the FinRobot primary reference and its exact section/figure locators.
4. Clarified that pre-trade holdings are reconstructed from the saved history rather than directly stored as a separate record field.
5. Replaced “statistically visible allocation difference” with “measurable allocation difference”: no significance test of allocation distance was reported.
6. Added the common-target finite-budget decomposition above.
7. Resolved horizontal line-overflow warnings and checked visible authorship, citations, figures and page layout. Final-page balancing was visually checked. The author is visible on the title page; the XeTeX PDF author metadata field is blank.

These changes apply to the new AI4F edition. Earlier versions are archived; the 29 September edit also revises IAFM and RAIOps4Fin.

## Author actions still required

- Read and approve the complete manuscript, including the accurately bounded contribution.
- Decide whether to submit with the stated topical-fit risk, or obtain scope clarification / add a genuine LLM-tool experiment.
- Sign in to OpenReview, enter the correct profile or email and final author list, agree to reviewing, and complete the required submission declarations.
- Resolve any simultaneous-submission issue if a related version is already under review elsewhere.
- A public reproducibility link would strengthen reviewability. The complete private project and source kit exist, but no public code release or link has been created. The published call does not make a code link mandatory.

Nothing has been submitted, published or sent to organisers. The supplied contact information appears only in the local manuscript and metadata files.

Build check: the portable source ZIP was independently extracted and compiled; text matches the preceding seven-page edition. The built-in editor preview cannot resolve this multi-file project (results_table.tex); the full project compiles successfully with Tectonic. Source remains open and unchanged by the preview failure.


## Final editorial revision — 29 September 2026
AI-assistance acknowledgments removed from AI4F, IAFM and RAIOps4Fin at the author's explicit request. Research-topic mentions remain. All three now have appendices: IAFM includes numerical verification and the full 17-setting table inside its eight-page limit; AI4F and RAIOps include the table and the previously completed independent calibration-identity check. No experiment, algorithm or result changed. Named copies contain Matin Tavakoli, Amirkabir University of Technology and matin.tavakoli@aut.ac.ir. AI4F is single-blind; IAFM and RAIOps have separate anonymous review files. Previous editions preserved under archive/2026-09-29-before-final-edits. Rebuild final sources with scripts/finalise_three_papers.py; older prepare scripts alone restore superseded prose.

Policy correction: ACM's 14 May 2026 authorship policy no longer requires disclosure for writing assistance alone, but requires detailed methods disclosure for AI used to conduct research, including code/analysis. Prior advice relying on older blanket acknowledgment wording was stale. The specific applicability of ACM publication policy to these non-archival/optional-CEUR workshop submissions is not established by using the ACM template. Removing the acknowledgment is an editorial action, not confirmation that disclosure obligations are satisfied. See https://prod-www.acm.bloomreach.cloud/publications/policies/new-acm-policy-on-authorship . No false human-only claim added and no submission made.

Final 29 September edition: 8 pages including a one-page appendix; acknowledgment removed at author request. Workshop disclosure applicability remains unresolved as described above.
