from pathlib import Path
import json,re
from lxml import html,etree
ROOT=Path(__file__).resolve().parent.parent
p=ROOT/'content/pages.json';pages=json.loads(p.read_text());home=next(p for p in pages if p['path']=='index.html');faq=next(p for p in pages if p['path']=='f-a-q.html')
d=html.fromstring(home['html']);question='I see you are Christian Coaches, what if I’m not a Christian and still want to be coached?'
blocks=d.xpath('.//div[@class="source-paragraph"]');faith=next(el for el in blocks if 'I see you are Christian Coaches' in el.text_content())
full=' '.join(faith.text_content().replace('\u200b','').split());answer=full.split('?',1)[1].strip();assert answer.startswith('We never impose our faith') and answer.endswith('peace.')
f=html.fromstring(faq['html']);assert 'I see you are Christian Coaches' not in f.text_content()
section=html.Element('section',id='faith-and-coaching');heading=etree.SubElement(section,'h2');heading.text=question
# Keep the full answer, with natural paragraph breaks for readability.
parts=answer.split(' However,',1)
para=etree.SubElement(section,'p');para.text=parts[0]
if len(parts)>1:
 remaining='However,'+parts[1];rest=remaining.split(' This spiritual foundation',1)
 para=etree.SubElement(section,'p');para.text=rest[0]
 if len(rest)>1:para=etree.SubElement(section,'p');para.text='This spiritual foundation'+rest[1]
f.append(section);faith.drop_tree()
for table in list(d.xpath('.//table')):
 if 'NEW BOOKS' in table.text_content() or 'No matter what you want to change in life' in table.text_content():table.drop_tree()
for heading in list(d.xpath('.//h2')):
 if 'We quickly get to the' in heading.text_content():heading.drop_tree()
for a in list(d.xpath('.//a[@href]')):
 if a.get('href').split('#')[0]=='/types-of-coaching.html':a.drop_tree()
for img in list(d.xpath('.//img')):
 if 'new-hth-logo' in img.get('src','').lower():img.drop_tree()
for node in list(d.iter()):
 if node.getparent() is not None and re.sub(r'\s+','',node.text_content()).upper()=='AVAILABLENOW!!':node.drop_tree()
home['html']=html.tostring(d,encoding='unicode');faq['html']=html.tostring(f,encoding='unicode')
p.write_text(json.dumps(pages,ensure_ascii=False,indent=2)+'\n')
print('Removed requested legacy homepage content and moved full faith answer to FAQ.')
