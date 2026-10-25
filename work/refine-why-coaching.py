from pathlib import Path
from lxml import html,etree
import json
ROOT=Path(__file__).resolve().parent.parent
p=ROOT/'content/pages.json';pages=json.loads(p.read_text());page=next(p for p in pages if p['path']=='why-coaching.html');d=html.fromstring(page['html'])
old=d.xpath('.//div[@class="source-paragraph"][ul]')[0];replacement=html.Element('div',attrib={'class':'coaching-benefits'})
intro=etree.SubElement(replacement,'p');intro.text='Emotional healing coaching offers a compassionate, nonjudgmental space to explore what you’ve experienced and how it may be affecting your life today. With support and encouragement, you can begin to understand your feelings, recognize familiar patterns, and take steps toward healing at your own pace.'
lead=etree.SubElement(replacement,'p');lead.text='Through coaching, you can:'
listing=etree.SubElement(replacement,'ul')
for heading,description in [
 ('Feel heard and understood',' as you share your story without pressure to reveal more than you’re ready to.'),
 ('Recognize protective patterns',' that may have helped you through difficult experiences but now leave you feeling stuck.'),
 ('Rebuild self-trust',' by learning to recognize your feelings, needs, and personal values.'),
 ('Strengthen boundaries and communication',' so you can approach relationships with greater awareness and choice.'),
 ('Practice healthier ways of responding',' when difficult emotions or familiar challenges arise.'),
 ('Move forward with support',' through practical tools and manageable steps that reflect your needs and readiness.')]:
 item=etree.SubElement(listing,'li');bold=etree.SubElement(item,'strong');bold.text=heading;bold.tail=description
replacement.tail=old.tail;old.getparent().replace(old,replacement)
for el in list(d.xpath('.//div[@class="source-paragraph"]')):
 if "You decide where and how fast" in el.text_content():el.drop_tree()
for el in list(d.xpath('.//a[@href="/types-of-coaching.html"]')):el.drop_tree()
for el in list(d.xpath('.//h2')):
 if 'Choice, not circumstances' in el.text_content():el.drop_tree()
# Remove dividers left surrounding the retired closing content.
for el in list(d.xpath('.//hr'))[1:]:el.drop_tree()
page['html']=html.tostring(d,encoding='unicode');page['show_eyebrow']=False;page['source_chars']=len(' '.join(d.text_content().split()));p.write_text(json.dumps(pages,ensure_ascii=False,indent=2)+'\n')
p=ROOT/'scripts/build.py';s=p.read_text();old='''def intro(p):
 return f'<section class="page-intro"><div class="container"><p class="eyebrow">{e(p["category"])}</p><h1>{e(p["title"])}</h1></div></section>' '''.rstrip();new='''def intro(p):
 eyebrow=f'<p class="eyebrow">{e(p["category"])}</p>' if p.get('show_eyebrow',True) else ''
 return f'<section class="page-intro"><div class="container">{eyebrow}<h1>{e(p["title"])}</h1></div></section>' '''.rstrip();assert old in s;s=s.replace(old,new,1);p.write_text(s)
print('Replaced coaching benefits and removed requested Why Coaching elements.')
