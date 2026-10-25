"""Import the captured public website without executing its legacy scripts."""
from pathlib import Path
from urllib.parse import urljoin,urlparse,unquote
from lxml import html,etree
import json,re,copy
ROOT=Path(__file__).resolve().parent.parent
BASE='https://www.hearttoheartlifecoaching.com/'
rows=json.loads((ROOT/'docs/migration-inventory.json').read_text())
known={r['path'] for r in rows}
ALLOWED={'div','p','br','strong','em','b','i','u','s','span','a','ul','ol','li','h2','h3','h4','blockquote','img','table','tbody','thead','tr','td','th','hr','form','label','input','select','option','textarea','fieldset','legend','iframe','video','source'}
DROP={'script','style','noscript','object','embed','button'}
def local_url(value,page):
 if not value:return ''
 u=urlparse(urljoin(BASE+page,value))
 if u.scheme not in ['http','https','mailto','tel']:return ''
 if u.hostname in ['www.hearttoheartlifecoaching.com','hearttoheartlifecoaching.com']:
  p=u.path.lstrip('/') or 'index.html'
  if p in known or p.startswith('uploads/'):
   # Build rewrites these absolute-local paths relative to each output page.
   return '/'+p+('?' +u.query if u.query and not p.startswith('uploads/') else '')+('#'+u.fragment if u.fragment else '')
 return u.geturl()
def clean(el,page):
 tag=el.tag.lower() if isinstance(el.tag,str) else ''
 if el.get('id') in ['wsite-com-product-price-area','wsite-com-product-sku','wsite-com-product-social-sharing','wsite-com-product-inventory','wsite-com-product-buy','wsite-com-product-quantity-limit-custom-message','wsite-com-product-fulfillment-options-container']:
  el.drop_tree();return
 if tag=='a' and not el.get('href') and el.text_content().strip().lower()=='submit':
  el.drop_tree();return
 if tag in DROP:
  el.drop_tree();return
 if el.get('style') and re.search(r'display\s*:\s*none|visibility\s*:\s*hidden',el.get('style'),re.I):
  el.drop_tree();return
 if tag=='input' and el.get('type') in ['hidden','submit','image']:
  el.drop_tree();return
 if tag=='form' and not el.get('action'):
  el.drop_tree();return
 if tag=='iframe':
  src=local_url(el.get('src'),page)
  if 'timetap.com' in src:
   a=html.Element('a',href='https://hearttoheart.timetap.com/',attrib={'class':'button external-booking'});a.text='Open appointment scheduler';el.getparent().replace(el,a);return
  if 'youtube.com/embed/' in src:
   el.set('src',src.replace('www.youtube.com','www.youtube-nocookie.com'))
   el.set('title','Video about becoming a Christian');el.set('loading','lazy');el.set('allowfullscreen','');el.set('referrerpolicy','strict-origin-when-cross-origin')
  else:el.drop_tree();return
 if tag=='form':
  action=el.get('action','')
  if 'paypal.com' in action:
   # Retain the existing hosted PayPal destination without an active preview payment form.
   ids=el.xpath('.//input[@name="hosted_button_id"]/@value')
   a=html.Element('a',href='https://www.paypal.com/donate/?hosted_button_id='+ids[0] if ids else 'https://www.paypal.com/',attrib={'class':'button'});a.text='Donate with PayPal';a.set('target','_blank');a.set('rel','noopener noreferrer');el.getparent().replace(el,a);return
  el.set('data-local-form','');el.set('method','post');el.set('class','form-card migrated-form');el.attrib.pop('action',None)
 for ch in list(el):clean(ch,page)
 if tag=='font':
  el.drop_tag();return
 if tag not in ALLOWED:
  if tag=='h1':el.tag='h2';tag='h2'
  else:el.drop_tag();return
 old_class=el.get('class','')
 keep={}
 if tag=='a':
  href=local_url(el.get('href'),page)
  if href:keep['href']=href
  if 'wsite-button' in old_class:keep['class']='button'
  if el.get('target')=='_blank':keep.update(target='_blank',rel='noopener noreferrer')
 if tag=='img':
  src=local_url(el.get('src'),page)
  if not src or 'pixel.gif' in src:el.drop_tree();return
  keep={'src':src,'alt':el.get('alt',''),'loading':'lazy','decoding':'async'}
  if keep['alt'] in ['Picture','Image']:keep['alt']=''
 if tag=='iframe':keep={k:v for k,v in el.attrib.items() if k in ['src','title','loading','allowfullscreen','referrerpolicy']}
 if tag in ['label','input','select','option','textarea']:
  for k in ['id','for','type','name','value','placeholder','rows','cols','checked','selected','multiple','aria-required','autocomplete']:
   if el.get(k) is not None:keep[k]=el.get(k)
  if keep.get('aria-required')=='true' and keep.get('type')!='checkbox':keep['required']=''
  if tag=='input' and 'email' in (el.get('name','')+' '+el.get('id','')).lower():keep['type']='email'
 if tag=='form':keep={'data-local-form':'','method':'post','class':'form-card migrated-form'}
 if tag in ['td','th']:
  for k in ['colspan','rowspan']:
   if el.get(k):keep[k]=el.get(k)
 if tag=='div':
  if 'paragraph' in old_class:keep['class']='source-paragraph'
  elif 'wsite-image' in old_class:keep['class']='source-image'
  elif 'wsite-multicol'==old_class:keep['class']='source-columns'
  elif 'wsite-form-field' in old_class:keep['class']='source-field'
 if el.get('id') and not el.get('id').isdigit() and not el.get('id').startswith(('wsite','form-','instructions-')):keep['id']=el.get('id')
 el.attrib.clear();el.attrib.update(keep)
 if tag=='form':
  note=html.Element('p',attrib={'class':'form-note'});note.text='Local review only. Do not enter private client information. Submissions are not sent or saved.';el.insert(0,note)
  btn=html.Element('button',type='button',attrib={'class':'button','data-preview-submit':''});btn.text='Review form';el.append(btn)
  status=html.Element('p',attrib={'class':'form-status','role':'status'});el.append(status)
  # Ensure every control has a programmatic name, including legacy grouped fields.
  for index,field in enumerate(el.xpath('.//input|.//textarea|.//select')):
   fid=field.get('id') or f'field-{index}';field.set('id',fid)
   labels=el.xpath('.//label[@for=$fid]',fid=fid)
   if not labels:
    parents=field.xpath('ancestor::div[contains(concat(" ",@class," ")," source-field ")]')
    legends=parents[-1].xpath('.//label') if parents else []
    label=' '.join(legends[0].text_content().split()) if legends else field.get('placeholder') or 'Response'
    if field.get('type') in ['radio','checkbox']:label+=': '+field.get('value','Option')
    field.set('aria-label',label)
   if field.tag=='input' and any('email' in l.text_content().lower() for l in labels):field.set('type','email');field.set('autocomplete','email')
   if field.get('placeholder')=='First':field.set('autocomplete','given-name')
   if field.get('placeholder')=='Last':field.set('autocomplete','family-name')
   if any('phone number' in l.text_content().lower() for l in labels):field.set('type','tel');field.set('autocomplete','tel')
  for group in el.xpath('.//div[contains(concat(" ",@class," ")," source-field ")]'):
   if not group.xpath('.//input[@type="checkbox" or @type="radio"]'):continue
   direct_labels=group.xpath('./label')
   if direct_labels:
    group.tag='fieldset';direct_labels[0].tag='legend'
    if '*' in direct_labels[0].text_content() and group.xpath('.//input[@type="checkbox"]'):
     group.set('data-checkbox-required','')
 return el
pages=[]
for row in rows:
 path=row['path'];d=html.fromstring((ROOT/'work/source'/path).read_bytes());content=copy.deepcopy(d.xpath('//*[@id="wsite-content"]')[0]);clean(content,path)
 # Ignore historical catalog prices and redundant product machinery.
 if path.startswith('store/'):
  for el in list(content.xpath('//*[@id="wsite-com-product-price-area"]|//*[@id="wsite-com-product-sku"]')):
   if el.getparent() is not None:el.drop_tree()
  raw=html.tostring(content,encoding='unicode')
  for price in ['$75.00','$85.00','$100.00']:
   raw=raw.replace(price,'')
  # Product descriptions may repeat prices; main pricing is the sole authority.
  raw=re.sub(r'\$\s*\d+(?:\.\d{2})?(?:\s*/\s*(?:hour|hr))?','',raw)
  content=html.fromstring(raw)
 if path=='invest-in-yourself.html':
  for el in content.iter():
   if el.text:el.text=re.sub(r'(IN-PERSON\s+APPOINTMENTS:\s*)\$150\s*/\s*hour',r'\1',el.text,flags=re.I)
   if el.tail:el.tail=re.sub(r'(IN-PERSON\s+APPOINTMENTS:\s*)\$150\s*/\s*hour',r'\1',el.tail,flags=re.I)
 text=' '.join(content.text_content().split())
 title=row['title'].strip().replace('****','').strip()
 if path=='motavation.html':title='Motivation'
 if path=='index.html':title='Empowerment Coaching'
 if path=='______________________.html':title='Additional Page'
 if path.startswith('store/'):category='Appointments'
 elif any(s in path for s in ['coaching','appointments','consultation','invest-in','schedule','assessments','training','retreat','bring-us']):category='Coaching'
 elif any(s in path for s in ['coach-','about-us','about-your','calling','mission','therapy-dog','testimonials']):category='About'
 elif any(s in path for s in ['policy','privacy','disclaimer','ethics']):category='Policies'
 elif any(s in path for s in ['intake','getting-to','report','session-form','connect','testimonial-form']):category='Client resources'
 else:category='Resources'
 pages.append({'path':path,'title':title,'category':category,'source':row['url'],'description':text[:155].rsplit(' ',1)[0]+'…' if text else title+' — Heart to Heart Life Coaching.','html':html.tostring(content,encoding='unicode'),'has_form':bool(content.xpath('.//form')),'source_chars':len(text)})
(ROOT/'content/pages.json').write_text(json.dumps(pages,ensure_ascii=False,indent=2)+'\n')
print(f'Imported {len(pages)} pages into content/pages.json')
