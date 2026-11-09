#!/usr/bin/env python3
"""Build an accessible static site with Python's standard library only."""
from pathlib import Path
from string import Template
from html import escape as e
import json, shutil, os
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'dist'
if OUT.exists():shutil.rmtree(OUT)
(OUT/'files').mkdir(parents=True)
(OUT/'assets').mkdir()
for f in ROOT.iterdir():
 if f.is_file() and f.suffix.lower() in ['.pdf','.png','.jpeg','.svg','.css']:
  shutil.copyfile(f,OUT/('files' if f.suffix.lower()=='.pdf' else 'assets')/f.name)
def load(name):return json.loads((ROOT/f'{name}.json').read_text())
p=load('profile');papers=load('papers');papers.sort(key=lambda q: ['electricity','market-opening','contestability','migration','digital-skills','classroom','dma-review','google-search','ds4ll','high-speed-rail','ai-economics'].index(q['id']));teach=load('teaching');service=load('service')
base=Template((ROOT/'base.html').read_text())
nav=[('','Home'),('research','Research'),('teaching','Teaching'),('service','Academic Service'),('contact','Contact')]
site=os.environ.get('SITE_URL','https://yanbinxu.com').rstrip('/')
def link(url,prefix):return e(url if url.startswith(('https:','mailto:','#')) else prefix+url)
def render(slug,body,description,cls='content-page'):
 prefix='../' if slug else './'; title=next(label for s,label in nav if s==slug)
 navigation=''.join(f'<a href="{prefix}{s+"/" if s else "index.html"}"'+(' aria-current="page"' if s==slug else '')+f'>{label}</a>' for s,label in nav)
 html=base.substitute(title=e(p['name']+(' | '+title if slug else ' | Economist')),description=e(description),canonical=e(site+'/'+(slug+'/' if slug else '')),prefix=prefix,navigation=navigation,body=body,pageclass=cls)
 dest=OUT/slug/'index.html';dest.parent.mkdir(exist_ok=True);dest.write_text(html)
def heading(title,desc,label='Yanbin (Tracy) Xu'):
 intro='<p class="lede">'+e(desc)+'</p>' if desc else ''
 return f'<div class="page-heading"><p class="eyebrow">{e(label)}</p><h1>{e(title)}</h1>{intro}</div>'
def summary_card(q):
 return f'<article class="selected"><span class="area">{e(q["area"])}</span><h3><a href="research/#{q["id"]}">{e(q["title"])}</a></h3><p class="meta">{e(q["citation"])}</p></article>'
home=f'''<section class="hero"><div><p class="eyebrow">Economics · Institutions · Technology</p><h1>Yanbin <span>(Tracy)</span> Xu</h1><p class="role">{e(p['role'])}<br>{e(p['institute'])}, {e(p['university'])}</p><p class="bio">{e(p['bio'])}</p><p>{e(p['methods'])}</p><div class="actions"><a class="button" href="research/">Explore research →</a><a href="{e(p['cv_path'])}" download>Download CV (PDF)</a><a href="contact/">Contact</a></div></div><aside><img class="portrait" src="assets/portrait.jpeg" alt="Portrait of Yanbin (Tracy) Xu" width="768" height="1024"><p class="portrait-note">{e(p['education'])}</p></aside></section><section class="section-row"><h2>Research interests</h2><div><ul class="interests">{''.join('<li>'+e(x)+'</li>' for x in p['interests'])}</ul><p class="small-note">{e(p['ai_note'])}</p></div></section><section class="section-row"><h2>Selected research</h2><div>{''.join(summary_card(next(q for q in papers if q['id']==pid)) for pid in ['market-opening','contestability','migration'])}<a href="research/">All papers and policy research →</a></div></section>'''
render('',home,p['bio'],'home')
groups=['Peer-Reviewed Publications','Working Papers','Policy Research and Reports','Work in Progress']
ids=['publications','working-papers','policy','work-in-progress']
research=heading('Research','','Papers & policy research')
research+='<div class="research-intro">'+''.join('<p>'+e(paragraph)+'</p>' for paragraph in p['research_intro'])+'</div>'
research+='<div class="research-layout"><aside class="section-nav" aria-label="Research sections"><p class="eyebrow">Browse by status</p>'+''.join(f'<a href="#{i}">{g}</a>' for i,g in zip(ids,groups))+'</aside><div>'
for gid,group in zip(ids,groups):
 research+=f'<section class="research-group" id="{gid}"><h2 class="group-heading">{group}</h2>'
 for q in [x for x in papers if x['category']==group]:
  research+=f'<article class="paper" id="{q["id"]}"><span class="area">{e(q["area"])}</span><h3>{e(q["title"])}</h3>'
  if q.get('authors'):research+=f'<p class="authors">{e(q["authors"])}</p>'
  research+=f'<p class="meta">{e(q["citation"].split(' · ',1)[1] if q["citation"].startswith('With ') else q["citation"])}</p>'
  if q.get('document_title'):research+=f'<p class="meta">Full report title: {e(q["document_title"])}</p>'
  research+='<div class="paper-links">'+''.join(f'<a href="{link(a["url"],"../")}">{e(a["label"])}</a>' for a in q['links'])+'</div>'
  summary=e(q['summary'])
  for phrase in q.get('summary_emphasis',[]):
   summary=summary.replace(e(phrase),'<strong>'+e(phrase)+'</strong>')
  paragraphs=''.join('<p>'+paragraph+'</p>' for paragraph in summary.split('\n\n'))
  research+='<details'+(' open' if q.get('summary_open') else '')+'><summary>Research summary</summary>'+paragraphs+'</details>'
  if q.get('highlight'):
   highlight=q['highlight'];hid=q['id']+'-highlight'
   research+=f'<details><summary>View research figure</summary><figure class="research-highlight" aria-labelledby="{hid}-title" aria-describedby="{hid}-caption"><h4 id="{hid}-title">{e(highlight["title"])}</h4>'
   if highlight['type']=='decomposition':
    research+='<div class="decomposition-scale" aria-hidden="true"><span>0%</span><span>100%</span></div><ul class="decomposition-bars">'
    for label,value in highlight['values']:
     research+=f'<li><div class="bar-label"><span>{e(label)}</span><strong>{value}%</strong></div><div class="bar-track" aria-hidden="true"><span style="width:{value}%"></span></div></li>'
    research+='</ul>'
   else:
    research+='<div class="outcome-panels">'
    for value,unit,label in highlight['values']:
     research+=f'<div class="outcome-panel"><p class="outcome-value">{e(value)}<span>{e(unit)}</span></p><p class="outcome-label">{e(label)}</p></div>'
    research+='</div>'
   research+=f'<figcaption id="{hid}-caption">{e(highlight["caption"])}</figcaption></figure></details>'
  if q.get('figure'):
   f=q['figure'];caption=(e(f['caption_intro'])+'<br><br>' if f.get('caption_intro') else '')+e(f['caption']);research+=f'<details><summary>View research figure</summary><figure><img loading="lazy" src="../{e(f["path"])}" alt="{e(f["alt"])}"><figcaption>{caption}</figcaption></figure></details>'
  research+='</article>'
 research+='</section>'
research+='</div></div>';render('research',research,'Publications, working papers, policy reports, and research in progress by Yanbin (Tracy) Xu.')
t=heading('Teaching','Economics teaching at Georgetown University, with experience across international trade, macroeconomics, microeconomics, and econometrics.')+'<div class="narrow">'
for role in ['Instructor','Teaching assistant']:
 t+=f'<section class="teaching-group"><h2>{"Instructor" if role=="Instructor" else "Teaching Assistant"}</h2>'
 for q in teach:
  if q['role']==role:t+=f'<div class="course"><span class="term">{e(q["term"])}</span><div><h3>{e(q["course"])}</h3>{('<p class="meta">'+e(q['description'])+'</p>') if q.get('description') else ''}</div></div>'
 t+='</section>'
if p.get('teaching_statement'):t+=f'<a href="{link(p["teaching_statement"],"../")}">Teaching statement (PDF)</a>'
t+='</div>';render('teaching',t,'Instructor and teaching assistant experience at Georgetown University.')
s=heading('Academic service','Conference organization and contributions to the research community.')+'<div class="narrow"><section class="service-group"><h2>Conference organization</h2>'
for q in service['organizing']:s+=f'<div class="service-entry"><h3>{e(q["event"])}</h3><p class="meta">{e(q["role"])}</p></div>'
s+='<p>'+e(service['organization_description'])+'</p><p>'+e(service['responsibilities'])+'</p>'
s+='</section><section class="service-group"><h2>Journal refereeing</h2>'+''.join('<div class="service-entry">'+e(x)+'</div>' for x in service['refereeing'])+'</section>'
if service['presentations']:
 s+='<section class="service-group"><h2>Selected conference presentations and seminars</h2>'
 migration_talks=[q for q in service['presentations'] if q['group']=='Migration paper']
 s+='<h3>'+e(migration_talks[0]['title'])+'</h3>'
 for q in migration_talks:s+=f'<div class="course"><span class="term">{e(q["date"])}</span><div>{e(q["event"])}</div></div>'
 s+='</section><section class="service-group"><h2>Other presentations</h2>'
 for q in service['presentations']:
  if q['group']=='Other presentations':s+=f'<div class="course"><span class="term">{e(q["date"])}</span><div><h3>{e(q["title"])}</h3><p class="meta">{e(q["event"])}</p></div></div>'
 s+='</section>'
s+='</div>';render('service',s,'Academic service, conference organization, and journal refereeing.')
c=heading('Contact','')+f'''<div class="contact-grid"><div><p class="eyebrow">Email</p><a class="contact-email" href="mailto:{e(p['email'])}">{e(p['email'])}</a><div class="contact-links"><a href="{e(p['scholar'])}">Google Scholar ↗</a><a href="{e(p['github'])}">GitHub ↗</a></div></div><div><h2>{e(p['role'])}</h2><p>{e(p['institute'])}<br>{e(p['university'])}<br>Washington, DC</p></div></div>'''
render('contact',c,'Contact Yanbin (Tracy) Xu at the Knight–Georgetown Institute, Georgetown University.')
# Keep existing inbound asset URLs working after the domain cutover.
for old,new in load('legacy-assets').items():
 dest=OUT/old;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(OUT/new,dest)
(OUT/'.nojekyll').touch()
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+site+'/'+(s+'/' if s else '')+'</loc></url>' for s,_ in nav)+'</urlset>')
(OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+site+'/sitemap.xml\n')
print('Built five pages in',OUT)
