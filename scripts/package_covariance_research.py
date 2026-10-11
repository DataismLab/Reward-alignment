"""Private reproducibility archive; excludes downloaded third-party papers."""
from pathlib import Path
import hashlib
import json
import zipfile

root = Path(__file__).resolve().parents[1]
destination = root.parent / 'mvrl-covariance-research-code.zip'
paths = set()
for directory in ('mvrl', 'tests', 'scripts', 'notes', 'data', 'results'):
    for path in (root / directory).rglob('*'):
        if path.is_file() and '__pycache__' not in path.parts and path.suffix in {
            '.py', '.md', '.json', '.csv', '.txt', '.log', '.zip', '.npz'
        }:
            paths.add(path)
for name in ('README.md', 'FINDINGS.md', 'WORKLOG.md', 'COVARIANCE_RESEARCH_REPORT.md',
             'requirements.txt', 'requirements-dev.txt', 'pytest.ini'):
    path = root / name
    if path.exists():
        paths.add(path)
for path in (root / 'literature').rglob('*'):
    if path.is_file() and (path.suffix in {'.json', '.md'}):
        paths.add(path)
paper = root / 'submissions/iafm'
for name in ('paper.tex', 'paper.pdf', 'paper.bbl', 'references.bib', 'results_table.tex',
             'covariance_table.tex', 'acmart.cls', 'ACM-Reference-Format.bst'):
    paths.add(paper / name)
for name in ('theory.pdf', 'covariance.pdf', 'covariance_simulation.pdf'):
    paths.add(paper / 'figures' / name)
# The new source builder explicitly reads this preserved input.
paths.add(root / 'archive/2026-10-07-before-covariance-revision/iafm/paper.tex')
manifest = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(paths)}
with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as archive:
    archive.writestr('START_HERE.txt',
        '9 October 2026 covariance/reward extension. Private research package, not an anonymous submission.\n'
        'Read mvrl-surrogate-gap/COVARIANCE_RESEARCH_REPORT.md for results, scope and commands.\n'
        'Includes current code, tests, cached results, raw public data, and IAFM source/PDF.\n'
        'Third-party literature PDFs and optional learned-model binaries are not included.\n'
        'Current runners preserve existing outputs; use a separate copy for fresh reruns.\n'
        'Install requirements-dev.txt in a virtual environment; optional learning runs need torch.\n')
    archive.writestr('SHA256.json', json.dumps(manifest, indent=2))
    for path in sorted(paths):
        archive.write(path, 'mvrl-surrogate-gap/' + str(path.relative_to(root)))
with zipfile.ZipFile(destination) as archive:
    assert archive.testzip() is None
print(f'{len(paths)} files, {destination.stat().st_size / 1e6:.1f} MB: {destination.name}')
