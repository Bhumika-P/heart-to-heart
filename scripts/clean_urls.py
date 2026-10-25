"""Generate static directory routes usable on GitHub Pages and Live Server."""
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, unquote
import os,json,posixpath
from lxml import html
SITE='https://www.hearttoheartlifecoaching.com/'
def clean_route(path):
 if path=='index.html':return ''
 return path[:-5]+'/' if path.endswith('.html') else path

def clean_file(path):
 if path=='404.html':return '404.html'
 return clean_route(path)+'index.html'

def generate(root,paths,redirects):
 paths=list(dict.fromkeys(paths))
 known={unquote(path) for path in paths}|{unquote(path) for path in redirects}
 normalized_redirects={unquote(k):unquote(v) for k,v in redirects.items()}
 def destination(path):
  path=unquote(path)
  return clean_route(normalized_redirects.get(path,path))
 def canonical(url):
  if isinstance(url,str) and url.startswith(SITE):
   rest=url[len(SITE):];u=urlsplit(rest)
   return SITE+urlunsplit(('', '', destination(u.path) if unquote(u.path) in known else u.path,u.query,u.fragment))
  if isinstance(url,list):return [canonical(v) for v in url]
  if isinstance(url,dict):return {k:canonical(v) for k,v in url.items()}
  return url
 def local_url(value,source,outfile):
  u=urlsplit(value)
  if u.scheme or u.netloc:return canonical(value)
  if not u.path:return value
  old=posixpath.normpath(posixpath.join(posixpath.dirname(source),unquote(u.path))) if not u.path.startswith('/') else u.path.lstrip('/')
  target=destination(old) if old in known else old
  relative=os.path.relpath(root/target,(root/outfile).parent).replace(os.sep,'/')
  if (old in known or u.path.endswith('/')) and not relative.endswith('/'):relative+='/'
  return urlunsplit(('', '',relative,u.query,u.fragment))
 originals={path:(root/unquote(path)).read_text() for path in paths}
 for path,source in originals.items():
  out=clean_file(path);doc=html.document_fromstring(source)
  for node in doc.xpath('//*[@href or @src or @action]'):
   for attr in ['href','src','action']:
    value=node.get(attr)
    if value:node.set(attr,local_url(value,path,out))
  for node in doc.xpath('//meta[@property="og:url"]'):
   node.set('content',canonical(node.get('content','')))
  for node in doc.xpath('//script[@type="application/ld+json"]'):
   node.text=json.dumps(canonical(json.loads(node.text)),ensure_ascii=False).replace('</','<\\/')
  target=root/unquote(out);target.parent.mkdir(parents=True,exist_ok=True)
  target.write_text('<!doctype html>\n'+html.tostring(doc,encoding='unicode')+'\n')
 # Retired clean routes also redirect, in addition to every legacy .html address.
 def alias(old,out,new):
  target=destination(new);href=os.path.relpath(root/target,(root/out).parent).replace(os.sep,'/')+'/'
  doc=html.document_fromstring('<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Page moved</title></head><body><p>This page has moved to <a>its updated address</a>.</p></body></html>')
  head=doc.find('head');node=html.Element('meta',{'http-equiv':'refresh','content':'0;url='+href});head.append(node);head.append(html.Element('link',{'rel':'canonical','href':SITE+target}));doc.xpath('//a')[0].set('href',href)
  file=root/unquote(out);file.parent.mkdir(parents=True,exist_ok=True);file.write_text('<!doctype html>\n'+html.tostring(doc,encoding='unicode')+'\n')
 for path in paths:
  if path not in ['index.html','404.html']:alias(path,path,path)
 for old,new in redirects.items():
  alias(old,old,new);alias(old,clean_file(old),new)
 # Canonicals and sitemap contain only clean page addresses.
 sitemap=root/'sitemap.xml';sitemap.write_text(sitemap.read_text().replace('.html</loc>','/</loc>'))
