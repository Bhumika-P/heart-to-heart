from pathlib import Path
from lxml import html
import json
ROOT=Path(__file__).resolve().parent.parent
p=ROOT/'content/pages.json';pages=json.loads(p.read_text());page=next(p for p in pages if p['path']=='why-coaching.html');d=html.fromstring(page['html'])
old_intro=next(el for el in d.xpath('.//div[@class="source-paragraph"]') if 'horse-drawn vehicle' in el.text_content())
old_patterns=next(el for el in d.xpath('.//div[@class="source-paragraph"]') if 'Our lives and relationships often revert' in el.text_content())
paragraphs=[
'Before it described a profession, the word <strong>“coach”</strong> referred to a horse-drawn carriage that carried people from where they were to where they wanted to go. Emotional healing coaching follows a similar idea: offering support as you make sense of your experiences, recognize what is keeping you feeling stuck, and take meaningful steps toward healing.',
'Painful experiences can influence how we see ourselves, respond to challenges, and connect with others. Sometimes, patterns we developed to protect ourselves become our <strong>“default,”</strong> even when they no longer serve us. Recognizing those patterns is an opportunity to understand ourselves with compassion.',
'Coaching offers a welcoming space to explore these patterns at your own pace. Through thoughtful questions, practical tools, and encouragement, you can learn to recognize your feelings and needs, strengthen boundaries, rebuild self-trust, and practice healthier ways of responding.',
'<strong>Think of coaching as looking through the windshield while remaining aware of the rearview mirror.</strong> Your past can offer insight into the beliefs and responses shaping your life today. Understanding those connections can help you approach the road ahead with greater awareness and choice.',
'The goal is to support you in creating a <strong>new default</strong>— one grounded in emotional safety, healthier relationships, and the freedom to move forward without being controlled by your past.'
]
for text in paragraphs:old_intro.addprevious(html.fromstring('<p>'+text+'</p>'))
old_intro.drop_tree();old_patterns.drop_tree()
for image in list(d.xpath('.//img')):
 if any(name in image.get('src','') for name in ['21171251-s_10.jpg','7971140-s_14.jpg']):image.drop_tree()
page['html']=html.tostring(d,encoding='unicode');page['description']='Explore emotional healing coaching: understand familiar patterns, strengthen boundaries, rebuild self-trust, and move forward beyond your past.';page['source_chars']=len(' '.join(d.text_content().split()));p.write_text(json.dumps(pages,ensure_ascii=False,indent=2)+'\n')
print('Updated Why Coaching with all five supplied paragraphs and removed both images.')
