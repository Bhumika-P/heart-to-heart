from pathlib import Path
from urllib.request import Request,urlopen
from PIL import Image
import re,hashlib
ROOT=Path(__file__).resolve().parent.parent
for p in (ROOT/'assets/img').rglob('*.png'):
 if 'scenery' in str(p) or 'Profile' in str(p):
  with Image.open(p) as im:
   im.thumbnail((1600,1600) if 'scenery' in str(p) else (700,700));im.save(p.with_suffix('.webp'),'WEBP',quality=82,method=6)
css=ROOT/'assets/css/theme.css';s=css.read_text().replace('mountain-sunrise.png','mountain-sunrise.webp').replace('mountain-boardwalk.png','mountain-boardwalk.webp');css.write_text(s)
url='https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,600&family=Lato:wght@400;700&display=swap'
req=Request(url,headers={'User-Agent':'Mozilla/5.0'})
with urlopen(req,timeout=25) as r:fonts=r.read().decode()
folder=ROOT/'assets/fonts';folder.mkdir(exist_ok=True)
for u in set(re.findall(r'url\((https://[^)]+)\)',fonts)):
 name=hashlib.sha256(u.encode()).hexdigest()[:12]+'.'+u.split('.')[-1]
 with urlopen(u,timeout=25) as r:(folder/name).write_bytes(r.read())
 fonts=fonts.replace(u,'../fonts/'+name)
(ROOT/'assets/css/fonts.css').write_text(fonts)
print('Prepared local fonts and optimized theme photographs.')
