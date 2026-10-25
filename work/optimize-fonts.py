from pathlib import Path
from urllib.request import Request,urlopen
import re,hashlib
ROOT=Path(__file__).resolve().parent.parent
url='https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,600&family=Lato:wght@400;700&display=swap'
headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'}
with urlopen(Request(url,headers=headers),timeout=25) as r:raw=r.read().decode()
blocks=re.findall(r'/\*\s*latin(?:-ext)?\s*\*/\s*@font-face\s*\{[^}]+\}',raw)
if not blocks:raise RuntimeError('No Latin WOFF2 blocks returned; kept existing fonts')
css='\n'.join(blocks)+'\n'
for u in set(re.findall(r'url\((https://[^)]+)\)',css)):
 if not u.endswith('.woff2'):raise RuntimeError('Expected WOFF2; kept existing fonts')
 name=hashlib.sha256(u.encode()).hexdigest()[:12]+'.woff2'
 with urlopen(u,timeout=25) as r:(ROOT/'assets/fonts'/name).write_bytes(r.read())
 css=css.replace(u,'../fonts/'+name)
(ROOT/'assets/css/fonts.css').write_text(css)
# Preserve the official licenses alongside the self-hosted font assets.
for name,u in [('Cormorant-Garamond-OFL.txt','https://raw.githubusercontent.com/google/fonts/main/ofl/cormorantgaramond/OFL.txt'),('Lato-OFL.txt','https://raw.githubusercontent.com/google/fonts/main/ofl/lato/OFL.txt')]:
 with urlopen(u,timeout=25) as r:(ROOT/'assets/fonts'/name).write_bytes(r.read())
print('Downloaded Latin and Latin Extended WOFF2 fonts and their official licenses.')
