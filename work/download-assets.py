from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin,urlparse,unquote
from urllib.request import Request,urlopen
import json,hashlib,re
ROOT=Path(__file__).resolve().parent.parent
rows=json.loads((ROOT/'work/inventory.json').read_text());base='https://www.hearttoheartlifecoaching.com/'
urls=set()
for row in rows:
 for u in row['images']+row['links']:
  u=urljoin(base,u)
  if urlparse(u).hostname in ['www.hearttoheartlifecoaching.com','hearttoheartlifecoaching.com'] and '/uploads/' in urlparse(u).path:urls.add(u)
def download(u):
 path=urlparse(u).path; dest=ROOT/path.lstrip('/')
 try:
  dest.parent.mkdir(parents=True,exist_ok=True)
  if not dest.exists():
   with urlopen(Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=35) as r:data=r.read()
   dest.write_bytes(data)
  return {'url':u,'path':path.lstrip('/'),'bytes':dest.stat().st_size}
 except Exception as e:return {'url':u,'error':str(e)}
with ThreadPoolExecutor(max_workers=6) as pool:results=list(pool.map(download,sorted(urls)))
(ROOT/'docs/asset-inventory.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({'downloaded':sum('path'in r for r in results),'bytes':sum(r.get('bytes',0) for r in results),'errors':[r for r in results if 'error'in r]},indent=2))
