"""Prepare AI4F's single-blind allocation-tool validation manuscript."""
from pathlib import Path
import shutil,re
r=Path(__file__).resolve().parents[1];src=r/'submissions/raiops4fin';w=r/'submissions/ai4f';w.mkdir(exist_ok=True)
for name in ['acmart.cls','ACM-Reference-Format.bst','results_table.tex']:shutil.copy2(src/name,w/name)
shutil.copytree(src/'figures',w/'figures',dirs_exist_ok=True)
s=(src/'paper.tex').read_text().replace(r'\setcopyright{none}',r'\setcopyright{none}'+'\n'+r'\setlength{\emergencystretch}{2em}')
s=re.sub(r'\\acmConference[^\n]*',lambda _:r"\acmConference[AI4F '26]{The 3rd Workshop on LLMs and Generative AI for Finance}{November 14, 2026}{Milan, Italy}",s)
s=re.sub(r'\\title\{[^\n]*',lambda _:r'\title{Checking Financial Objectives in Portfolio Tools: A Reward-Alignment Benchmark}',s)
abstract=r'''A financial assistant that calls a portfolio optimiser needs more than a valid tool response: the allocation must reflect the intended financial preference. We study this numerical component through a reward-alignment benchmark. On common pre-trade states, the benchmark separates the financial reference, the optimum induced by a proposed reward, and finite-budget optimisation error. For constrained mean--variance allocation with turnover costs, the established mean auxiliary shows why risk and cost coefficients must be calibrated together. A historical study of ten US industry portfolios over 432 months verifies fitted-policy recovery across 17 settings and compares adaptations of published reward designs. Realised performance differences remain inconclusive, and finite-budget optimisation error can exceed the primary reward-design gap. The result is a reproducible check on allocation-tool semantics that could support tool-using financial workflows. The experiments evaluate the numerical allocation component; they do not evaluate an LLM, instruction interpretation or an end-to-end agent.'''
s=re.sub(r'\\begin\{abstract\}.*?\\end\{abstract\}',lambda _:r'\begin{abstract}'+'\n'+abstract+'\n'+r'\end{abstract}',s,flags=re.S)
intro=r'''\section{Introduction}
A financial assistant may translate an investment request into a call to a portfolio tool. The call can execute successfully, return feasible weights and report an attractive backtest, yet still optimise a different preference from the one intended. Return, variance, squared return and turnover penalties are not interchangeable terms. Checking syntax and numerical convergence alone does not settle their economic meaning.

Tool-using financial platforms make this boundary concrete. FinRobot\ \cite{finrobot2024}, Section 3.1 and Figure 2, describes natural-language-to-parameter and code-generation routes to financial tools. Its Section 5 presents forecasting and document-analysis demonstrations, while Section 6 identifies portfolio allocation as future work. This motivates a component-level question: once a financial objective has been specified mathematically, how can the allocation tool be checked against it? We do not evaluate or claim a failure of FinRobot.

Our benchmark starts after that specification step. It stores the financial reference, reward-induced allocation, numerical certificates and realised returns. Comparing rewards on identical pre-trade states prevents differences accumulated along earlier trading paths from being mistaken for a local reward effect. The resulting record separates economic specification, numerical solution and investment outcome.

The case study is constrained mean--variance allocation with proportional turnover costs. The mean auxiliary in MVPI\ \cite{zhang2021} shows that rescaling a squared-return penalty also changes the effective turnover preference unless the cost coefficient is adjusted. Joint calibration recovers the fitted reference across 17 historical settings, but the principal realised-performance intervals include zero. We contribute an implemented numerical benchmark and an explicit risk--cost diagnostic. A proposed use in an LLM workflow is described separately from the completed experiments; there are no LLM-generated allocations or end-to-end agent results in this study.

'''
a=s.index(r'\section{Introduction}');b=s.index(r'\section{Portfolio objectives and validation}');s=s[:a]+intro+s[b:]
s=s.replace('preference coefficients, pre-trade allocation, chosen weights, realised return and numerical certificate','preference coefficients, chosen weights, realised return and numerical certificate; pre-trade holdings are reconstructed from the preceding allocation and asset returns')
s=s.replace('A statistically visible allocation difference','A measurable allocation difference')
s=s.replace('Thus finite-budget error can dominate the reward discrepancy.', r'In common target units, the raw policy has mean total gap $5.66\times10^{-6}=1.48\times10^{-6}+4.18\times10^{-6}$ at this budget, separating design from the signed finite-budget term. Thus finite-budget error can dominate the reward discrepancy.')
s=s.replace(r'\subsection{Which comparison can establish improvement?}',r'\subsection{Alignment and investment performance}')
s=s.replace(r'\subsection{What the robustness grid tests}',r'\subsection{Sensitivity to risk, costs and estimation}')
integration=r'''\section{Using the benchmark at a financial-tool boundary}
The completed benchmark accepts numerical preferences and portfolio states. An LLM application would introduce an earlier step that translates an investor's request into those inputs. Keeping that step separate makes the scope of a successful numerical check clear: it can establish that a tool follows the supplied objective without establishing that the objective correctly represents the user's request.

A proposed interface would record four items before invoking the allocator: the return definition and horizon, the risk and cost coefficients with their units, the feasible set, and the dated information and holdings available to the decision. For example, monthly decimal excess returns with $\varphi=5$ and a 10-basis-point charge per unit of L1 turnover specify the primary benchmark state. A request for terminal wealth, annual risk or one-way trading costs would require a different explicit specification. An assistant should not silently map those alternatives to the same numerical inputs.

The allocator can then be checked in layers. First, verify data dates and feasibility. Second, establish the accuracy of each numerical solve with an appropriate certificate. Third, compare the reward-optimal allocation with the fitted reference on a common state. Finally, report realised path metrics with their uncertainty, preserving the distinction between target fidelity and investment success. The historical implementation carries out these numerical comparisons; the interface and its use by a language model remain a proposed integration.

The example also illustrates why a calibration step should return an explanation in financial units. Risk-only calibration retains the nominal cost coefficient but adds the effective cost term in Eq.\ \eqref{eq:costdistortion}. Joint calibration rescales both coefficients, or the existing MVPI auxiliary can solve the reference directly. The record should identify which construction was used. A reference-dependent certificate is not evidence of a faster optimisation method, and a successful certificate is not approval to execute a trade.

An end-to-end assessment would require additional evidence: prompts and their intended mathematical specifications, a fixed model and version, recorded tool calls, an independent check of translated units and constraints, and comparisons with and without the numerical check. It would measure instruction fidelity and erroneous tool use as well as portfolio outcomes. None of those agent-level measurements is inferred from the 432-month numerical study. The present benchmark supplies the allocation component and reference values for such an evaluation.

'''
s=s.replace(r'\section{Discussion}',integration+r'\section{Discussion}')
s=s.replace('The procedure is suitable for a model-development validation record.','The procedure is suitable for a model-development validation record and as a numerical component in a proposed financial-tool evaluation.')
s=s.replace(r'\author{Matin Tavakoli}',r'\author{Matin Tavakoli}'+ '\n' + r'\affiliation{\institution{Amirkabir University of Technology}\city{Tehran}\country{Iran}}'+'\n'+r'\email{matin.tavakoli@aut.ac.ir}')
s=s.replace(r'\section{Discussion}',r'\balance'+'\n'+r'\section{Discussion}')
s=s.replace(r'\begin{document}',r'\hypersetup{pdfauthor={Matin Tavakoli}}'+'\n'+r'\begin{document}')
s=s.replace(r'\clearpage'+'\n'+r'\bibliographystyle',r'\bibliographystyle')
(w/'paper.tex').write_text(s)
bib=(src/'references.bib').read_text()+r'''
@misc{finrobot2024,
 author={Hongyang Yang and Boyu Zhang and Neng Wang and Cheng Guo and Xiaoli Zhang and Likun Lin and Junlin Wang and Tianyu Zhou and Mao Guan and Runjia Zhang and Christina Dan Wang},
 title={{FinRobot: An Open-Source AI Agent Platform for Financial Applications using Large Language Models}},
 year={2024},
 howpublished={arXiv:2405.14767v2, revised 27 May 2024},
 url={https://arxiv.org/abs/2405.14767v2}
}
'''
(w/'references.bib').write_text(bib)
(w/'OPENREVIEW_FIELDS.txt').write_text('Title: Checking Financial Objectives in Portfolio Tools: A Reward-Alignment Benchmark\nAuthor: Matin Tavakoli\nAffiliation: Amirkabir University of Technology\nEmail: matin.tavakoli@aut.ac.ir\n\nAbstract:\n'+abstract.replace('--','–')+'\n\nKeywords: portfolio allocation; reward alignment; financial tool evaluation; mean–variance; transaction costs\n\nSubmission: https://openreview.net/group?id=ACM.org/ICAIF/2026/Workshop/AI4F\nSingle-blind; use the named PDF. Deadline 7 October 2026 AoE. Author profile/email must be entered in OpenReview; reviewer agreement must be completed by the author.\n')
