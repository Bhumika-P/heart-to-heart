from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request, urllib.parse, json, hashlib
from lxml import etree, html
ROOT=Path(__file__).resolve().parent
BASE='https://www.hearttoheartlifecoaching.com'
OUT=ROOT/'source'; OUT.mkdir(exist_ok=True)
def fetch(url):
 req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (website migration inventory)'})
 with urllib.request.urlopen(req,timeout=35) as r:return r.read()
sitemap=fetch(BASE+'/sitemap.xml');(OUT/'sitemap.xml').write_bytes(sitemap)
urls=etree.fromstring(sitemap).xpath('//*[local-name()="loc"]/text()')
def read(url):
 path=urllib.parse.urlparse(url).path.lstrip('/') or 'index.html'
 try:
  raw=fetch(url); dest=OUT/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
  doc=html.fromstring(raw)
  content=doc.xpath('//*[@id="wsite-content"]')
  c=content[0] if content else doc
  return {'url':url,'path':path,'title':doc.xpath('string(//title)'),'sha256':hashlib.sha256(raw).hexdigest(),'content_chars':len(c.text_content()),'forms':[{'action':f.get('action'),'method':f.get('method'),'fields':[{'name':i.get('name'),'type':i.get('type'),'label':i.get('placeholder')} for i in f.xpath('.//input|.//select|.//textarea')]} for f in c.xpath('.//form')],'links':list(dict.fromkeys(c.xpath('.//a/@href'))),'images':list(dict.fromkeys(c.xpath('.//img/@src'))),'embeds':c.xpath('.//iframe/@src'),'scripts':c.xpath('.//script/@src')}
 except Exception as e:return {'url':url,'path':path,'error':str(e)}
with ThreadPoolExecutor(max_workers=6) as pool: rows=list(pool.map(read,urls))
(ROOT/'inventory.json').write_text(json.dumps(rows,indent=2))
print(json.dumps({'sitemap_pages':len(urls),'downloaded':sum('error' not in r for r in rows),'errors':[r for r in rows if 'error' in r],'forms':[{k:r[k] for k in ['path','forms']} for r in rows if r.get('forms')],'pdfs':sorted(set(urllib.parse.urljoin(BASE+'/',u) for r in rows for u in r.get('links',[]) if '.pdf' in u.lower()))},indent=2))
