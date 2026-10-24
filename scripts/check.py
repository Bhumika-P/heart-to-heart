"""Check migration coverage and static review-site invariants."""
from pathlib import Path
from urllib.parse import urlparse,unquote
from lxml import html,etree
import json,re
ROOT=Path(__file__).resolve().parent.parent
rows=json.loads((ROOT/'docs/migration-inventory.json').read_text())
redirects=json.loads((ROOT/'content/redirects.json').read_text())
errors=[];count=0;forms=0;images=0
additional_pages=[p['path'] for p in json.loads((ROOT/'content/pages.json').read_text()) if p['path'] not in {r['path'] for r in rows}]
for name in [r['path'] for r in rows]+additional_pages+['resources.html','extra-links.html','all-pages.html','404.html']:
 p=ROOT/unquote(name)
 if not p.exists():errors.append(f'Missing page: {name}');continue
 count+=1;d=html.fromstring(p.read_bytes())
 if name in redirects:
  destination=redirects[name]
  if not (ROOT/destination).exists():errors.append(f'{name}: redirect target missing')
  if not d.xpath('//meta[@http-equiv="refresh" and @content=$value]',value='0;url='+destination):errors.append(f'{name}: local redirect missing')
  if d.xpath('string(//link[@rel="canonical"]/@href)')!='https://www.hearttoheartlifecoaching.com/'+destination:errors.append(f'{name}: redirect canonical incorrect')
  continue
 for label,query,n in [('h1','//h1',1),('main','//main',1),('canonical','//link[@rel="canonical"]',1),('description','//meta[@name="description"]',1)]:
  if len(d.xpath(query))!=n:errors.append(f'{name}: expected {n} {label}')
 if d.get('lang')!='en':errors.append(f'{name}: missing page language')
 if not d.xpath('//meta[@name="robots" and contains(@content,"noindex")]'):errors.append(f'{name}: review indexing protection missing')
 for s in d.xpath('//script[@type="application/ld+json"]'):
  try:json.loads(s.text)
  except Exception:errors.append(f'{name}: invalid structured data JSON')
 for n in d.xpath('//a[@href]|//img[@src]|//script[@src]|//link[@href]'):
  v=n.get('href') or n.get('src');u=urlparse(v)
  if u.scheme or u.netloc:continue
  target=(p.parent/u.path) if u.path else p
  # Python's static server decodes paths, as do Live Server and production servers.
  if not target.exists() and not Path(unquote(str(target))).exists():errors.append(f'{name}: missing local target {v}')
 for img in d.xpath('//img'):
  images+=1
  if img.get('alt') is None:errors.append(f'{name}: image lacks alt')
  if not img.get('width') or not img.get('height'):errors.append(f'{name}: image dimensions missing')
 for a in d.xpath('//a[@href]'):
  if not a.text_content().strip() and not a.get('aria-label') and not any(i.get('alt') for i in a.xpath('.//img')):errors.append(f'{name}: link lacks accessible name ({a.get("href")})')
 for form in d.xpath('//form'):
  forms+=1
  if 'data-local-form' not in form.attrib or form.get('action'):errors.append(f'{name}: active external form in local review')
  if form.get('method','').lower()!='post':errors.append(f'{name}: unsafe form fallback')
  for field in form.xpath('.//input|.//textarea|.//select'):
   fid=field.get('id')
   if not field.get('aria-label') and not (fid and form.xpath('.//label[@for=$fid]',fid=fid)):errors.append(f'{name}: unlabelled field {fid}')
 if name.startswith('store/') and re.search(r'\$\s*(75|85)(?:\D|$)',d.xpath('//main')[0].text_content()):errors.append(f'{name}: legacy price remains')
 if name=='invest-in-yourself.html':
  text=' '.join(d.xpath('//main')[0].text_content().split())
  if re.search(r'IN-PERSON\s+APPOINTMENTS:\s*\$',text,re.I):errors.append('In-person price remains')
 for attr in d.xpath('//@onclick | //@onload | //@onsubmit'):errors.append(f'{name}: legacy inline event handler remains')
# Every original user-entered form field remains represented.
for r in rows:
 if r['path'] not in ['connect-with-us.html','testimonial-form.html','pre-coaching-report.html','post-coaching-report.html']:continue
 d=html.fromstring((ROOT/unquote(r['path'])).read_bytes())
 expected=[f['name'] for form in r['forms'] for f in form['fields'] if f['type'] not in ['hidden','submit','image'] and f['name']]
 if r['path']=='connect-with-us.html':
  removed={'_u166661856328742272','_u850138711910425745[Life Purpose Coaching for Direction]','_u850138711910425745[Behavioral Strength Assessment Testing]','_u850138711910425745[All of the above]','_u850138711910425745[Teaching/Training Event]'}
  expected=[name for name in expected if name not in removed]
 actual=d.xpath('//form//input/@name|//form//select/@name|//form//textarea/@name')
 if sorted(actual)!=sorted(expected):errors.append(f'{r["path"]}: migrated fields differ from source')
assets=json.loads((ROOT/'docs/asset-inventory.json').read_text())
pdfs={a['path'] for a in assets if a.get('path','').endswith('.pdf')}
archived_pdfs=json.loads((ROOT/'docs/client-resource-archive.json').read_text())
if len(pdfs)!=11 or not all((ROOT.parent/archived_pdfs[p]).exists() and not (ROOT/p).exists() for p in pdfs):errors.append('Expected 11 client PDFs safely archived outside the website folder')
# Brand palette pairings used on solid surfaces. Photo backgrounds require visual review.
def lum(h):
 rgb=[int(h[i:i+2],16)/255 for i in (1,3,5)]
 return sum(v*w for v,w in zip([v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in rgb],[.2126,.7152,.0722]))
pairs=[('body','#302c29','#fbf8f3'),('muted','#61564c','#fbf8f3'),('burgundy heading/link','#650d29','#fbf8f3'),('button','#ffffff','#650d29'),('eyebrow','#795840','#fbf8f3'),('review banner','#493b32','#eee8e0')]
contrast=[]
for label,fg,bg in pairs:
 a,b=sorted([lum(fg),lum(bg)]);ratio=(b+.05)/(a+.05);contrast.append({'label':label,'ratio':round(ratio,2)})
 if ratio<4.5:errors.append(f'Contrast fails: {label}')
report={'pages_checked':count,'source_pages':len(rows),'active_source_pages':len(rows)-len(redirects),'retired_page_redirects':len(redirects),'forms_checked':forms,'image_instances_checked':images,'preserved_pdfs':len(pdfs),'solid_color_contrast':contrast,'errors':errors,'limitations':['Static and selected browser checks are not a WCAG conformance audit.','No Lighthouse or field Core Web Vitals measurement has been performed.','Client forms are local review only; private backend and commerce migration remain outstanding.']}
(ROOT/'docs/check-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));raise SystemExit(bool(errors))
