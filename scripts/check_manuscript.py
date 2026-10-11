"""Check the research manuscript and its generated numerical inputs."""
from pathlib import Path
import json
import re
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
paper=ROOT/'manuscript'
source=(paper/'paper.tex').read_text()
pdf=PdfReader(paper/'paper.pdf')
text='\n'.join(page.extract_text() for page in pdf.pages)
assert len(pdf.pages)==8, 'Expected final eight-page manuscript'
assert not pdf.metadata.get('/Author'), 'Author metadata must be empty for anonymous review'
assert not re.search(r'\b(?:Matin|Tavakoli|Amirkabir)\b', text, re.I)
assert all(token not in text for token in ('??','\ufffd','/Users/'))
for kind,count in [('Figure',3),('Table',2)]:
    assert len(re.findall(r'\b'+kind+r'\s+\d+:',text))==count,kind
assert 'sigconf,anonymous,review' in source
assert 'Certifying Reward Alignment' in source
assert (paper/'paper.bbl').read_text().count('\\bibitem')==29
for name in re.findall(r'\\input\{([^}]+)\}', source):
    assert (paper/name).is_file(),name
for name in re.findall(r'\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}', source):
    assert (paper/name).is_file(),name
summary=json.loads((ROOT/'results/rl-extension/final_summary.json').read_text())
n=summary['neural_means'];m=(paper/'rl_numbers.tex').read_text()
expected={
    'DistanceReduction':100*(1-n['paired_centered']['D']/n['myopic']['D']),
    'DeviationReduction':100*(1-n['paired_centered']['max_deviation']/n['myopic']['max_deviation']),
}
for key,value in expected.items():
    actual=re.search(r'\\newcommand\{\\'+key+r'\}\{([^}]+)\}',m)
    assert actual and actual.group(1)==f'{value:.1f}',key
log=paper/'paper.log'
if log.exists():
    for token in ('Overfull','undefined','Missing character','LaTeX Error'):
        assert token not in log.read_text(),token
print('PASS: eight pages; anonymous text/metadata; 29 references; three figures; two tables; inputs and final reduction macros agree.')
