# Contributing

Use a separate branch for each research question or maintenance change. Keep commits focused enough to review and reproduce.

## Results and tests

Run `python -m pytest -q` with the research extras installed. Add an independent numerical or analytical check when changing a mathematical result. Check reported numbers against saved outputs before changing the paper or documentation.

Experiment runners reuse cached results. Use a separate output directory or move the old cache aside before changing a protocol. Preserve seeds, data versions, estimation windows and evaluation conventions. Expensive experiments should run explicitly, never on import or as part of the default test suite.

## Claims and provenance

Distinguish proved statements, finite numerical evidence, preliminary findings and open questions. Credit the exact source of known methods. Record corrections in `FINDINGS.md` and substantive changes in `WORKLOG.md`; retain negative results and the conditions under which a result fails.

Keep reward-design error, optimisation error and investment performance separate. Update manuscript statements and generated numerical inputs together when results change. The current paper is `manuscript/paper.tex`; earlier versions are available through Git history.
