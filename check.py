"""Verify generated internal destinations, anchors, PDF signatures and key content."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json
root=Path(__file__).resolve().parent/'dist'
class Page(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set();self.h1=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  if tag=='h1':self.h1+=1
  if tag in ('a','img','link'):
   u=a.get('href',a.get('src'))
   if u:self.links.append(u)
pages={}
for f in root.rglob('*.html'):
 p=Page();p.feed(f.read_text());pages[f.resolve()]=p;assert p.h1==1,f
checked=0
for f,p in pages.items():
 for u in p.links:
  s=urlsplit(u)
  if s.scheme or s.netloc:continue
  target=(f.parent/unquote(s.path)).resolve() if s.path else f
  if target.is_dir():target=target/'index.html'
  assert target.exists(),f'{f}: missing {u}'
  if s.fragment and target in pages:assert s.fragment in pages[target].ids,f'{f}: missing anchor {u}'
  checked+=1
pdfs=list(root.rglob('*.pdf'))
for f in pdfs:assert f.read_bytes().startswith(b'%PDF-'),f
papers=json.loads((root.parent/'papers.json').read_text())
research=(root/'research/index.html').read_text()
for p in papers:assert f'id="{p["id"]}"' in research
assert len(papers)==11
print(f'PASS: {len(pages)} pages, {checked} internal links/assets, {len(pdfs)} PDFs, all 11 research entries.')
