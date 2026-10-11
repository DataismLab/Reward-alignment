from pathlib import Path as _RevisionPath
_revision_source = _RevisionPath(__file__).resolve().parents[1] / 'submissions/iafm/paper.tex'
if any(marker in _revision_source.read_text() for marker in ('Financial semantics and model validation', 'Certifying Reward Alignment')):
 raise SystemExit('Legacy source generator blocked: preserve the current IAFM revision. Compile submissions/iafm/paper.tex directly; see notes/IAFM_REVISION_2026-10-01.md.')
"""Build expanded named manuscripts from the preserved short editions."""
from pathlib import Path
import shutil,json
r=Path(__file__).resolve().parents[1];s=r/'submissions';archive=r/'archive/2026-09-27-short-workshop-editions';archive.mkdir(exist_ok=True)
for key in ['iafm','raiops4fin','market-microstructure']:
 for name in ['paper.tex','paper.pdf']:
  target=archive/key/name;target.parent.mkdir(exist_ok=True)
  if not target.exists():shutil.copy2(s/key/name,target)
 t=(archive/key/'paper.tex').read_text().replace('sigconf,anonymous,review','sigconf,review').replace('\\author{Anonymous Author(s)}','\\author{Matin Tavakoli}')
 common=(s/'expansion/common.tex').read_text()+'\n'+(s/'expansion/sensitivity.tex').read_text()
 if key=='market-microstructure':common+='\n'+(s/'expansion/trading.tex').read_text()+'\n'+(s/'expansion/trading_results.tex').read_text()
 heading={'iafm':r'\section{Implications and scope}','raiops4fin':r'\section{Discussion}','market-microstructure':r'\section{Implications for trading models}'}[key]
 t=t.replace(heading,common+'\n'+heading)
 (s/key/'paper.tex').write_text(t)
