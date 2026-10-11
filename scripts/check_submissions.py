"""Check named and blind copies against workshop limits and render named PDFs."""
from pathlib import Path
import pymupdf,re,json
r=Path(__file__).resolve().parents[1]/'submissions';report=[]
for key,count in [('ai4f',3),('iafm',4),('raiops4fin',3),('market-microstructure',3)]:
 p=r/key;versions={}
 for stem in (['paper'] if key=='ai4f' else ['paper','paper-anonymous']):
  d=pymupdf.open(p/(stem+'.pdf'));txt='\n'.join(x.get_text() for x in d);log=(p/(stem+'.log')).read_text()
  for token in ['undefined','Missing character','LaTeX Error']:assert token not in log,(key,stem,token)
  for token in ['/Users/','??','�']:assert token not in txt,(key,stem,token)
  if stem=='paper' and key=='market-microstructure':assert 'Matin Tavakoli' in d[0].get_text()
  else:assert 'Tavakoli' not in txt and not d.metadata.get('author')
  assert len(re.findall(r'Figure \d+:',txt))==count
  assert ('OpenAI Codex' in txt)==(key=='market-microstructure')
  refs=next(i+1 for i,x in enumerate(d) if '\nReferences\n' in x.get_text())
  if key=='iafm':assert len(d)<=8
  if key in ['ai4f','iafm','raiops4fin']:assert '\\appendix' in (p/(stem+'.tex')).read_text()
  if key=='raiops4fin':assert refs<=7
  for page in d:
   for b in page.get_text('dict')['blocks']:
    for line in b.get('lines',[]):
     for span in line['spans']:
      x0,y0,x1,y1=span['bbox'];assert 15<x0<x1<page.rect.width-15 and 15<y0<y1<page.rect.height-15,(key,span['text'])
  if stem=='paper':
   (p/'qa-v2').mkdir(exist_ok=True)
   for i,page in enumerate(d):page.get_pixmap(matrix=pymupdf.Matrix(1.45,1.45)).save(p/'qa-v2'/f'page-{i+1}.png')
  versions[stem]=dict(pages=len(d),references_start_page=refs,anonymous=key!='market-microstructure' or stem.endswith('anonymous'))
 report.append(dict(workshop=key,versions=versions,figures=count,unresolved_references=False,ai_disclosure_visible=key=='market-microstructure'))
 print(key,versions,'PASS',flush=True)
(r/'verification.json').write_text(json.dumps(report,indent=2))
