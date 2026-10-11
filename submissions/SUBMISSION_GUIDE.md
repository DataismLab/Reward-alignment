# Current submission: IAFM only — 9 October 2026

Use `iafm/paper.pdf`: **Certifying Reward Alignment in Portfolio Reinforcement Learning**, anonymous, eight total pages, 29 references, three figures, two tables. See `iafm/SUBMISSION_READY.md`. The [official workshop deadline](https://icaif2026.org/workshop.html) was extended to **12 October 2026, 23:59 AoE**; notification 16 October. No submission has been made. The older multi-workshop options and dates below are preserved history, not current delivery instructions.

---

# Final workshop submission options

Rules checked against the official workshop sites and calls on 27 September 2026. These are alternative versions of the same research. **Recommended order: IAFM, RAIOps4Fin, then Market Microstructure.** No paper has been submitted.

| Workshop | Deadline | Core subject | Prepared paper | Submission format and limit | Fit |
|---|---|---|---|---|---|
| [IAFM: Interpretability and Alignment of Financial Models](https://iafm-icaif.netlify.app/) | 1 October 2026, 23:59 AoE | Interpretation, alignment, faithful evaluation and model risk in financial AI | **When Portfolio Rewards Miss the Target: Exact Mismatch and Policy Alignment**; iafm/paper.pdf | Anonymous ACM sigconf; maximum 8 pages total. Prepared: 8 pages, 4 figures. | Best fit for the exact mismatch result and economic interpretation of rewards. |
| [RAIOps4Fin: Applied Responsible AI Operations for Finance](https://raiops4fin2026.github.io/ICAIF/) | 1 October 2026, 23:59 AoE | Practical validation, auditability, monitoring and responsible-AI operations | **Validating Portfolio Rewards: Preference Drift, Optimisation Error and Historical Performance**; raiops4fin/paper.pdf | Anonymous ACM/host format; maximum 6 content pages excluding references and appendices. The final edition includes a robustness and verification appendix. | Strong fit for the implemented validation procedure and reproducible historical records. |
| [AI-Driven Market Microstructure in Centralized and Decentralized Finance](https://icaif-ai-driven.github.io/) | 1 October 2026, 23:59 AoE | AI trading, liquidity, execution, market design and model robustness | **Risk and Turnover Preferences in Learned Portfolio Rebalancing**; market-microstructure/paper.pdf | Double-blind PDF; only first 8 pages including references reviewed. ACM sigconf used as the host format; no distinct class named in the workshop call. Prepared: 8 pages, 3 figures. | Secondary option under the call's model-robustness theme. Monthly allocation is not an order-book or execution study. |

## What changed for each audience

IAFM retains the full exact horizon-mismatch theorem and proof, links rewards to their induced preferences, and uses the historical study to separate alignment from financial performance.

RAIOps focuses on the constrained calibration identity and a practical validation record: lagged data windows, common states, numerical certificates, independent accounting checks and separately interpreted error measures. It makes no claim of production deployment or regulatory certification.

Market Microstructure focuses on the interaction of risk and turnover penalties and the resulting rebalancing incentives. It explicitly bounds the proportional-cost setting and does not claim evidence about impact, liquidity, fills or order books. It is the weakest of the three topical fits.

The prose has been edited for direct arguments, natural headings and less repetition. Results, assumptions and source attribution remain intact. The versions share substantial data, derivations and results; changing titles and emphasis does not make them independent studies.

## Rules that matter before submitting

- The central [ICAIF workshop page](https://icaif2026.org/workshop/) specifies 23:59 Anywhere on Earth for the 1 October deadline. The workshop-specific pages agree for these three options.
- IAFM's current site states 8 pages total. Its older call suggested at least 4 pages plus up to 2 for references; the expanded version follows the current 8-page rule. Notification is 15 October, camera-ready 31 October. The saved call describes IAFM as non-archival.
- RAIOps' own site and call state notification on **14 October**, rather than the central page's 15 October. Camera-ready is 31 October. Accepted papers of at least 5 pages may be considered for CEUR proceedings with author consent; do not treat this as automatic publication or silently opt in. The current submission uses ACM, not an assumed future CEUR camera-ready template.
- The [Market Microstructure call](https://icaif2026.org/calls/workshops/AI-Driven-Market-Microstructure-2026-Call-for-Papers.pdf) states 15 October notification and double-blind review. It does not establish an archival-publication status. No publication outcome is assumed.
- Explicit permission for simultaneous submission of substantially overlapping work to these three workshops was not found. **Choose one version, or obtain clarification from the organisers before concurrent submissions.** The main-track archival policy should not be presented as verified workshop permission. RL4LLM-Agents explicitly prohibits work under review elsewhere; it was not selected because this project does not evaluate LLM agents.
- The main papers name **Matin Tavakoli**, as requested. Separate **paper-anonymous.pdf** copies preserve double-blind review. Use those anonymous PDFs for blind-review submission. Affiliation and contact information have not been invented; enter the correct details in CMT. Check the chosen track name against the central workshop page. No portal action or organiser message has been sent.
- The three revised manuscripts omit AI-assistance acknowledgments at the author’s request. ACM’s updated May 2026 policy distinguishes optional writing-assistance disclosure from required methods disclosure for research use. Workshop-specific applicability remains to be confirmed; these edits do not establish policy compliance.


## Files

Each folder contains the final PDF, editable paper.tex, references.bib, results_table.tex, official acmart class/style and vector figures. The combined submission ZIP contains named and anonymous PDF/source variants, the real-data Implementation Report v2, and separate self-contained LaTeX ZIPs, plus this guide and CMT_FIELDS.txt. It is separate from the full private code archive, which includes older author-bearing documents. Submit the selected PDF, not the private archive.

The historical data, algorithms and results did not change during this editorial adaptation. Earlier tests remain applicable: 31 pytest tests, 10 original checks and independent verification of 4,320 primary strategy decisions. No claim of realised outperformance or full historical PPO/DDPG replication has been added.

## Expanded edition and Implementation Report v2

The 27 September expanded edition uses 8 pages for IAFM, 6 content pages plus one reference page for RAIOps4Fin, and 8 pages for Market Microstructure. Added material explains lagged estimation, common-state auditing, published reward adaptations, optimisation certificates, the robustness grid and learning-error interpretation. Market Microstructure additionally reports turnover and chronological outcomes from the existing saved experiment. No new investment-performance claim or algorithmic result was introduced.

IMPLEMENTATION_REPORT_V2.pdf is the eight-page real-data implementation report; its standalone LaTeX source is included. It explains the difference from synthetic v1, source data and vintage, objectives, solvers, costs, evaluation, uncertainty, learning diagnostic, tests and reproduction. The earlier implementation report is preserved.


## AI4F addition — 28 September 2026
AI4F manuscript: 7 pages, 3 figures, ACM sigconf, single-blind; Matin Tavakoli, Amirkabir University of Technology, matin.tavakoli@aut.ac.ir. Official https://ai4f.org/ deadline 7 October 2026 23:59 AoE; no length limit; OpenReview, not CMT. Author reviewer commitment required. Source submissions/ai4f/paper.tex; root paper-ai4f-2026.pdf and ai4f-2026-submission-kit.zip. FinRobot 2024 primary-paper comparison added (ledger now 22), no replication claim. Scientific audit reran: 31 tests, 10 original checks, 4320 decisions, 17 settings; joint and risk-only identities residual <9e-18. No investment algorithm/data/results changed; added preparation/audit/package scripts. Research contribution is reward alignment, NOT real-data outperformance of recent algorithms. AI4F fit remains conditional: no LLM/end-to-end agent experiment; proposed integration is explicitly separate. IAFM/RAIOps remain stronger fits. Read AI4F_SUBMISSION_READINESS.md before submission. No submission, contact, public release or reviewer/licence acceptance made. Existing other workshop papers and Implementation Report v2 preserved.


## Final editorial revision — 29 September 2026
AI-assistance acknowledgments removed from AI4F, IAFM and RAIOps4Fin at the author's explicit request. Research-topic mentions remain. All three now have appendices: IAFM includes numerical verification and the full 17-setting table inside its eight-page limit; AI4F and RAIOps include the table and the previously completed independent calibration-identity check. No experiment, algorithm or result changed. Named copies contain Matin Tavakoli, Amirkabir University of Technology and matin.tavakoli@aut.ac.ir. AI4F is single-blind; IAFM and RAIOps have separate anonymous review files. Previous editions preserved under archive/2026-09-29-before-final-edits. Rebuild final sources with scripts/finalise_three_papers.py; older prepare scripts alone restore superseded prose.

Policy correction: ACM's 14 May 2026 authorship policy no longer requires disclosure for writing assistance alone, but requires detailed methods disclosure for AI used to conduct research, including code/analysis. Prior advice relying on older blanket acknowledgment wording was stale. The specific applicability of ACM publication policy to these non-archival/optional-CEUR workshop submissions is not established by using the ACM template. Removing the acknowledgment is an editorial action, not confirmation that disclosure obligations are satisfied. See https://prod-www.acm.bloomreach.cloud/publications/policies/new-acm-policy-on-authorship . No false human-only claim added and no submission made.
