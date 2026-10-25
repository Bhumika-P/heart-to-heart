"""Generate a buildless review site; open root index.html with VS Code Live Server."""
from pathlib import Path
from urllib.parse import urlparse,unquote
import json,html,re,os
from lxml import html as dom
from PIL import Image
ROOT=Path(__file__).resolve().parent.parent
e=html.escape
pages=json.loads((ROOT/'content/pages.json').read_text())
REDIRECTS=json.loads((ROOT/'content/redirects.json').read_text())
lookup={p['path']:p for p in pages}
PRICING=json.loads((ROOT/'content/pricing.json').read_text())
IMAGE_DESCRIPTIONS=json.loads((ROOT/'content/image-descriptions.json').read_text())
def rel(path,page):return os.path.relpath(ROOT/path, (ROOT/page).parent).replace(os.sep,'/')
def asset(path,page):return e(rel(path,page),quote=True)
nav=[('index.html','Home'),('coach-shereacutee.html','About'),('why-coaching.html','Coaching'),('resources.html','Resources'),('invest-in-yourself.html','Pricing'),('connect-with-us.html','Contact')]
heart='<svg class="icon" viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 35C-5 18 3 1 15 8L20 13L25 8C37 1 45 18 20 35Z"/></svg>'
def link(path,label,page,cls=''):
 path=REDIRECTS.get(path,path)
 return f'<a href="{asset(path,page)}"'+(f' class="{cls}"' if cls else '')+(' aria-current="page"' if path==page else '')+f'>{e(label)}</a>'
def brand(page,include_heart=True):return f'<a class="brand" href="{asset("index.html",page)}" aria-label="Heart to Heart Life Coaching home">{heart if include_heart else ""}<span>HEART <i>to</i> HEART<small>LIFE COACHING</small></span></a>'
def pricing_cards(page):
 info_pages={"discovery-call":"free-consultation.html","phone-virtual":"phone-appointments.html","emergency-phone-virtual":"emergency-phone-virtual-coaching.html"}
 return '<div class="pricing-grid">'+''.join(f'<article class="price-card"><p class="eyebrow">{s["duration_minutes"]}-minute session</p><h2>{e(s["label"])}</h2><p class="price">'+('Complimentary' if s['price']==0 else f'${s["price"]}<span> / hour</span>')+f'</p><p>'+('For established clients with an urgent coaching appointment request.' if s['id'].startswith('emergency') else 'An initial conversation, with no cost or obligation.' if s['price']==0 else 'Connect by phone, Zoom, or FaceTime.')+f'</p><a class="button" href="{asset(info_pages[s["id"]].split("#")[0],page)}{('#'+info_pages[s['id']].split('#')[1]) if '#' in info_pages[s['id']] else ''}" aria-label="More information about {e(s["label"],quote=True)}">More info</a><a class="button" href="https://hearttoheart.timetap.com/#/" target="_blank" rel="noopener noreferrer">View availability<span class="sr-only"> (opens a new tab)</span></a></article>' for s in PRICING['services'])+'</div>'
HOME_QUESTIONS = [
 'Are you having a hard time holding it together when everything seems to be falling apart?',
 'Are you frustrated with yourself and your choices?',
 'Are you in a toxic relationship?',
 'Are you doing things that may be sabotaging your future?',
 "Is your heart so hurt that it's hard to move forward?",
]

def source_body(p):
 page=p['path'];d=dom.fromstring(p['html'])
 if page=='index.html':
  # Move the existing questions to the new prominent section rather than repeating them.
  for paragraph in d.xpath('.//div[@class="source-paragraph"]'):
   text=' '.join(paragraph.text_content().replace('\u200b','').split())
   if all(question in text for question in HOME_QUESTIONS):paragraph.drop_tree()
  for span in d.xpath('.//span'):
   if span.text_content().strip()=='Empowerment Coaching may be just what you need!':span.drop_tree()
 headings=d.xpath('.//h2')
 if headings and ' '.join(headings[0].text_content().split()).casefold()==' '.join(p['title'].split()).casefold():
  headings[0].drop_tree()
 for node in d.iter():
  for attr in ['href','src']:
   value=node.get(attr)
   if value and value.startswith('/'):
    u=urlparse(value);node.set(attr,rel(u.path.lstrip('/'),page)+('?' +u.query if u.query else '')+('#'+u.fragment if u.fragment else ''))
  if node.tag=='img':
   src=node.get('src','')
   if 'weebly/images/file_icons/pdf.png' in src:
    replacement=dom.Element('span',attrib={'class':'pdf-icon','aria-hidden':'true'});replacement.text='PDF';replacement.tail=node.tail;node.getparent().replace(node,replacement);continue
   f=(ROOT/page).parent/src
   original_path=os.path.relpath(f,ROOT).replace(os.sep,'/')
   description=IMAGE_DESCRIPTIONS.get(original_path,{})
   if description.get('text'):
    replacement=dom.Element('p',attrib={'class':'image-text-transcript'});replacement.text=description['text'];replacement.tail=node.tail;node.getparent().replace(node,replacement);continue
   if description.get('alt'):node.set('alt',description['alt'])
   try:
    with Image.open(f) as im:
     node.set('width',str(im.width));node.set('height',str(im.height))
     if im.width>400 and im.format not in ['GIF','SVG']:
      out=f.with_suffix('.webp')
      if not out.exists():
       pic=im.copy();pic.thumbnail((1600,1600));pic.save(out,'WEBP',quality=82,method=6)
      node.set('src',str(Path(src).with_suffix('.webp')))
   except (OSError,ValueError):pass
  if node.tag=='a' and node.get('href','').startswith('https://www.hearttoheartlifecoaching.com/uploads'):
   node.set('href',rel(urlparse(node.get('href')).path.lstrip('/'),page))
 # Give image-only links a meaningful name even for decorative image exceptions.
 for a in d.xpath('.//a[@href]'):
  if not a.text_content().strip() and not any(i.get('alt') for i in a.xpath('.//img')):
   target=lookup.get(a.get('href','').split('#')[0].split('?')[0].split('/')[-1])
   a.set('aria-label',target['title'] if target else 'View linked resource')
 # Fix the source site's .con typo without changing the contact address otherwise.
 for a in d.xpath('.//a[starts-with(@href,"mailto:")]'):
  a.set('href',a.get('href').replace('.con','.com'))
 body=dom.tostring(d,encoding='unicode')
 if not p['source_chars'] and not p.get('intentional_blank',False):
  body='<p class="empty-page-note">This page has no published content on the current website.</p>'
 return body

def template(page,title,description,body,category='Life Coaching',schema_extra=None):
 canonical='https://www.hearttoheartlifecoaching.com/'+('' if page=='index.html' else page)
 business_id='https://www.hearttoheartlifecoaching.com/#organization'
 graph=[{'@type':'Organization','@id':business_id,'name':'Heart to Heart Life Coaching LLC','url':'https://www.hearttoheartlifecoaching.com/','telephone':'+1-224-225-9494'}, {'@type':'WebSite','@id':'https://www.hearttoheartlifecoaching.com/#website','url':'https://www.hearttoheartlifecoaching.com/','name':'Heart to Heart Life Coaching','publisher':{'@id':business_id}}, {'@type':'WebPage','@id':canonical+'#webpage','url':canonical,'name':title,'description':description,'isPartOf':{'@id':'https://www.hearttoheartlifecoaching.com/#website'},'about':{'@id':business_id}}]
 if page!='index.html':graph.append({'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':'https://www.hearttoheartlifecoaching.com/'},{'@type':'ListItem','position':2,'name':title,'item':canonical}]})
 if page=='invest-in-yourself.html':
  graph.extend({'@type':'Service','name':service['label'],'provider':{'@id':business_id},'offers':{'@type':'Offer','price':service['price'],'priceCurrency':'USD','url':canonical}} for service in PRICING['services'])
 if page=='coach-shereacutee.html':
  graph.append({'@type':'Person','@id':'https://www.hearttoheartlifecoaching.com/#sheree-bergman','name':'Sherée Bergman','jobTitle':'Empowerment Coach','worksFor':{'@id':business_id},'url':canonical})
 if schema_extra:graph.extend(schema_extra)
 navhtml=''.join(link(u,l,page) for u,l in nav)
 if page!='index.html':
  body='<nav class="breadcrumbs container" aria-label="Breadcrumb"><ol><li>'+link('index.html','Home',page)+'</li><li aria-current="page">'+e(title)+'</li></ol></nav>'+body
 contact_scripts=(f'<script defer src="{asset("assets/js/contact-config.js",page)}?v=live1"></script><script defer src="{asset("assets/js/contact.js",page)}"></script>') if page=='connect-with-us.html' else ''
 fonts=''
 hero_preload=f'<link rel="preload" as="image" href="{asset("assets/img/scenery/mountain-sunrise.webp",page)}" fetchpriority="high">' if page=='index.html' else ''
 font_css=ROOT/'assets/css/fonts.css'
 if font_css.exists():fonts=f'<link rel="stylesheet" href="{asset("assets/css/fonts.css",page)}">'
 return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} | Heart to Heart Life Coaching</title><meta name="description" content="{e(description,quote=True)}"><meta name="robots" content="noindex,nofollow"><link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#650d29"><meta property="og:type" content="website"><meta property="og:title" content="{e(title,quote=True)}"><meta property="og:description" content="{e(description,quote=True)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="https://www.hearttoheartlifecoaching.com/assets/img/Logo/main-logo-burgundy.png">
<link rel="icon" href="{asset("assets/img/Logo/favicon-concept.png",page)}">{hero_preload}{fonts}<link rel="stylesheet" href="{asset("assets/css/theme.css",page)}"><link rel="stylesheet" href="{asset("assets/css/main.css",page)}"><script defer src="{asset("assets/js/site.js",page)}"></script><script defer src="{asset("assets/js/review.js",page)}"></script>{contact_scripts}
<script type="application/ld+json">{json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('</','<\\/')}</script></head>
<body><a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="container header-inner">{brand(page)}<button class="menu-toggle" aria-controls="navigation" aria-expanded="false" aria-label="Open menu"><span></span><span></span><span></span></button><nav id="navigation" aria-label="Main navigation">{navhtml}</nav><div class="header-actions">{link('schedule-appointment.html','Book a discovery call',page,'button header-join')}</div></div></header>
<main id="main">{body}</main>
<section class="closing-cta"><div class="container"><p class="eyebrow">Hope · Healing · Empowerment</p><h2>Take your next step with Heart to Heart</h2><p>Start with a complimentary 20-minute discovery phone call.</p>{link('free-consultation.html','Arrange a discovery call',page,'button light')}</div></section>
<footer class="site-footer"><div class="container"><div class="footer-top">{brand(page,include_heart=page!="index.html")}<nav aria-label="Footer navigation">{link('become-a-christian.html','Become a Christian',page)}{link('f-a-q.html','F.A.Q.',page)}{link('testimonials.html','Testimonials',page)}<a href="https://support.hearttoheartlifecoaching.com/">Support group</a></nav></div><div class="footer-contact"><a href="tel:+12242259494" class="{'home-phone' if page=='index.html' else ''}">224-225-9494</a><span>Algonquin, Illinois · Chicago Northwest Suburbs and beyond</span></div><div class="footer-bottom"><small>© <span data-year>2026</span> Heart to Heart Life Coaching LLC.</small><div>{link('privacy--confidentiality.html','Privacy & confidentiality',page)}{link('cancellation-policy.html','Cancellation policy',page)}{link('disclaimer.html','Disclaimer',page)}{link('standards--ethics.html','Standards & ethics',page)}</div></div></div></footer></body></html>'''

def write(page,title,desc,body,category='Life Coaching',schema_extra=None):
 out=ROOT/unquote(page);out.parent.mkdir(parents=True,exist_ok=True);out.write_text('\n'.join(line.rstrip() for line in template(page,title,desc,body,category,schema_extra).splitlines())+'\n')
def intro(p):
 eyebrow=f'<p class="eyebrow">{e(p["category"])}</p>' if p.get('show_eyebrow',True) else ''
 return f'<section class="page-intro{" discovery-centered" if p["path"]=="free-consultation.html" else ""}"><div class="container">{eyebrow}<h1>{e(p["title"])}</h1>{p.get("intro_statement_html", "")}</div></section>'
for p in pages:
 path=p['path'];body=source_body(p)
 if path=='free-consultation.html':body='<div class="discovery-centered">'+body+'</div>'
 before=''
 if path=='invest-in-yourself.html':before='<section class="container section-space pricing-options"><div class="section-heading"><h2>Coaching options</h2></div>'+pricing_cards(path)+'</section>'
 if path.startswith('store/'):
  before='<section class="container narrow section-space"><p>Appointments are arranged through our existing booking service. See current pricing before booking.</p>'+link('invest-in-yourself.html','Current appointment prices',path,'button')+'</section>'
 if path=='invest-in-yourself.html':
  before='<section class="container narrow booking-intro section-space"><p>Check availability or arrange your appointment with Heart to Heart through our existing TimeTap scheduler.</p><a class="button" href="https://hearttoheart.timetap.com/" target="_blank" rel="noopener noreferrer">Open the appointment scheduler <span class="sr-only">(opens a new tab)</span></a><p class="form-note">Booking continues on TimeTap. Review appointment details and fees there before confirming.</p><hr></section>'+before
 content=intro(p)+before+f'<article class="container narrow prose source-content section-space" aria-label="{e(p["title"],quote=True)} details">{body}</article>'
 if path=='index.html':
  title='Christian Life Coaching with Sherée Bergman'
  path_forward = '''<section class="container section-space home-path-forward"><div class="section-heading"><h2>Your path forward</h2></div><div class="feature-grid">'''+''.join(f'<a class="feature-card" href="{u}"><h3>{t}</h3><p>{desc}</p><span>Explore →</span></a>' for u,t,desc in [('why-coaching.html','Why coaching?','Learn what coaching can offer and whether it is right for you.'),('resources.html','Resources','Explore some transformative resources for healing and growth.'),('invest-in-yourself.html','Invest in yourself','See current coaching prices and arrange a discovery call.')])+'</div></section>'
  founder = f'''<section class="container section-space home-founder"><img src="assets/img/Profile/sheree-portrait-burgundy.webp" alt="Sherée Bergman, founder of Heart to Heart Life Coaching" width="700" height="700" loading="lazy"><div><p class="eyebrow">Meet your coach</p><h2>Meet Sherée</h2><p>Sherée is the founder of Heart to Heart Life Coaching LLC in the Chicagoland area. Her coaching focuses on emotional healing, healthier relationships, and marriage and family restoration.</p>{link('coach-shereacutee.html','About Sherée',path,'button')}</div><blockquote><p>“The purposes of a person’s heart are deep waters, but one who has insight draws them out.”</p><cite>Proverbs 20:5</cite></blockquote></section>'''
  content=f'''<section class="hero main-hero"><div class="container"><a class="button outline hero-support" href="https://support.hearttoheartlifecoaching.com/index.html">GO TO SUPPORT GROUP WEBSITE</a><div class="hero-copy"><p class="eyebrow">Heart to Heart Life Coaching</p><h1>Get to the heart<br>of what matters</h1><p class="hero-subtitle"><strong>EMPOWERMENT COACHING</strong></p><p class="hero-description">Compassionate, faith-centered coaching for emotional healing, healthier relationships, and lasting restoration.</p><div class="actions">{link('free-consultation.html','Your free discovery call',path,'button')}{link('donate.html','Donate',path,'button outline')}</div></div></div></section>
<section class="tinted home-questions" aria-label="Questions you may be asking"><div class="container section-space support-feature"><ul>'''+''.join(f'<li>{e(question)}</li>' for question in HOME_QUESTIONS)+'''</ul><div class="coaching-message"><p class="fading-message"><strong><em>Empowerment Coaching may be just what you need!</em></strong></p></div></div></section>'''+path_forward+founder+'''
<section class="home-coaching-cards" id="coaching-options"><div class="container feature-grid">'''+''.join(f'<a class="feature-card coaching-card" href="{href}"><h2>{e(title)}</h2><p>'+(('Open-Heart Coaching<br>'+e(description)) if title=='Heal' else e(description))+f'</p><span>{e(label)} →</span></a>' for title,description,href,label in [('Heal','for Emotional Healing','open-heart-emotional-healing.html','Explore Healing'),('Relationships','Support for healthier relationships and restoration.','relationship-coaching.html','Explore connect'),('Abuse Recovery','Rebuild self-trust and move toward healing after abuse.','coaching-for-abuse.html','Explore abuse recovery')])+f'''</div></section>
<section class="tinted home-support"><div class="container section-space support-feature"><div><p class="eyebrow">A place for understanding, hope & healing</p><h2>You are not alone.</h2><p>Explore our faith-centered support group for those who have experienced narcissistic and emotional abuse, unhealthy relationship patterns, and attachment wounds.</p></div><a class="button" href="https://support.hearttoheartlifecoaching.com/">Visit the support group</a></div></section>
<section class="container narrow prose source-content section-space home-more-coaching" aria-label="More about coaching">{body}</section>'''
  write(path,title,'Christian life coaching with Sherée Bergman in Algonquin and the Chicago Northwest Suburbs. Emotional healing, relationships, productivity and life purpose.',content)
 else:write(path,p['title'],p['description'],content,p['category'])

for path,title,selected in [('all-pages.html','Explore every page',pages),('extra-links.html','Extra Links',[p for p in pages if p['category'] in ['Resources','Client resources','Policies']])]:
 categories=sorted(set(p['category'] for p in selected))
 body=f'<section class="page-intro"><div class="container"><p class="eyebrow">Heart to Heart</p><h1>{title}</h1><p>Explore coaching, stories, client resources, and practical guidance.</p></div></section><div class="container section-space page-directory">'
 for cat in categories:
  body+=f'<section><h2>{e(cat)}</h2><ul>'+''.join(f'<li>{link(p["path"],p["title"],path)}</li>' for p in selected if p['category']==cat)+'</ul></section>'
 body+='</div>'
 if path=='all-pages.html':body='<section class="container narrow section-space prose"><h1>Explore every page</h1><p>This directory is currently unavailable.</p></section>'
 if path=='extra-links.html':body='<section class="container narrow section-space prose"><h1>Extra Links</h1><p>Additional resources are being updated. Please check back later.</p></section>'
 write(path,title,'Additional resources are being updated.' if path=='extra-links.html' else 'Browse Heart to Heart Life Coaching pages, services, educational articles, client downloads, and policies.',body)
resources_record=json.loads((ROOT/'content/resources.json').read_text())
resources_body='<section class="page-intro"><div class="container"><h1>Resources for your journey</h1></div></section>'+source_body(resources_record)
write('resources.html','Resources for your journey','Explore books and resources for healing and growth from Heart to Heart.',resources_body)
write('404.html','Page not found','Find your way back to Heart to Heart Life Coaching.','<section class="container narrow section-space prose"><h1>Let’s help you find your way.</h1><p>This address does not match a page in the local review site.</p><a class="button" href="index.html">Go home</a></section>')
(ROOT/'robots.txt').write_text('User-agent: *\nDisallow: /\n# Local/staging review only. Review indexing settings before production.\n')
urls=['https://www.hearttoheartlifecoaching.com/'+('' if p['path']=='index.html' else p['path']) for p in pages]+['https://www.hearttoheartlifecoaching.com/resources.html']
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{e(u)}</loc></url>\n' for u in urls)+'</urlset>\n')
# Local static aliases preserve old bookmarks without retaining duplicate content.
# Translate content/redirects.json to permanent HTTP redirects when hosting is configured.
for old,new in REDIRECTS.items():
 target=rel(new,old)
 label=lookup[new]['title'] if new in lookup else 'Resources for your journey'
 canonical='https://www.hearttoheartlifecoaching.com/'+new
 (ROOT/old).write_text(f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><meta http-equiv="refresh" content="0;url={e(target,quote=True)}"><link rel="canonical" href="{e(canonical,quote=True)}"><title>{e(label)} — page moved</title></head><body><p>This page has moved to <a href="{e(target,quote=True)}">{e(label)}</a>.</p></body></html>\n')
from clean_urls import generate
generate(ROOT,[p['path'] for p in pages]+['resources.html','extra-links.html','all-pages.html','404.html'],REDIRECTS)
print(f'Built {len(pages)} active source pages + resources, Extra Links, directory, 404, and {len(REDIRECTS)} redirects. Local review indexing protections enabled.')
