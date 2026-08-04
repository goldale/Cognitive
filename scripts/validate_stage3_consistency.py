#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, re, sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote
import yaml

ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'
checks=[]
def check(group,name,ok,detail=''):
    checks.append({'group':group,'name':name,'status':'PASS' if ok else 'FAIL','detail':detail})

def load_yaml(name):
    return yaml.safe_load((ROOT/'state/canonical'/name).read_text())

class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]; self.links=[]; self.text=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if 'id' in d:self.ids.append(d['id'])
        if tag=='a' and 'href' in d:self.links.append(d['href'])
    def handle_data(self,data): self.text.append(data)

# A canonical YAML
files=['principles.yaml','components.yaml','contracts.yaml','invariants.yaml','terminology.yaml','ownership.yaml','generation.yaml']
parsed={}
for f in files:
    try: parsed[f]=load_yaml(f); check('A','parse '+f,True)
    except Exception as e: check('A','parse '+f,False,str(e))

comp=parsed.get('components.yaml',{}); con=parsed.get('contracts.yaml',{}); term=parsed.get('terminology.yaml',{})
components={x['name']:x for x in comp.get('components',[])}
ops={x['name']:x for x in con.get('operations',[])}
for name in ['Transformer','Associative Memory','Memory State','Memory Vector','Semantic Representation','Semantic Feedback Learning Pipeline']:
    check('B','component '+name,name in components)
check('B','Transformer semantic_teacher','semantic_teacher' in components.get('Transformer',{}).get('roles',[]))
check('B','Associative Memory semantic_learner','semantic_learner' in components.get('Associative Memory',{}).get('roles',[]))
read=ops.get('READ',{}); update=ops.get('UPDATE',{})
check('C','READ output Memory Vector',read.get('outputs')==['Memory Vector'],str(read.get('outputs')))
check('C','READ no effects',read.get('effects')==[],str(read.get('effects')))
check('C','UPDATE output Updated Memory State',update.get('outputs')==['Updated Memory State'],str(update.get('outputs')))
check('C','UPDATE forbids Memory Vector','Memory Vector' in update.get('forbidden_outputs',[]))
check('C','UPDATE forbids implicit READ','READ' in update.get('implicit_operations_forbidden',[]))
check('C','UPDATE input Semantic Representation','Semantic Representation' in update.get('inputs',[]))

# HTML parse and refs
html_files=sorted(DOCS.rglob('*.html')); parsers={}
all_ids={}
for f in html_files:
    p=P(); p.feed(f.read_text(errors='replace')); parsers[f]=p; all_ids[f]=set(p.ids)
    dup=[x for x,c in Counter(p.ids).items() if c>1]
    check('D','unique ids '+str(f.relative_to(ROOT)),not dup,', '.join(dup))

broken=[]
for f,p in parsers.items():
    for href in p.links:
        if not href or href.startswith(('http:','https:','mailto:','javascript:')): continue
        target,_,frag=href.partition('#')
        target=unquote(target)
        tf=(f.parent/target).resolve() if target else f.resolve()
        try: tf.relative_to(ROOT.resolve())
        except ValueError: broken.append(f'{f.relative_to(ROOT)} -> {href} (outside root)'); continue
        if not tf.exists(): broken.append(f'{f.relative_to(ROOT)} -> {href} (missing file)'); continue
        if frag and tf.suffix.lower()=='.html' and frag not in all_ids.get(tf,set()):
            broken.append(f'{f.relative_to(ROOT)} -> {href} (missing id)')
check('D','all internal HTML links resolve',not broken,'; '.join(broken[:20]))

# A-Z coverage
idx=(DOCS/'chapter24/index.html').read_text(errors='replace')
for t in [x['term'] for x in term.get('terms',[])]: check('E','A-Z term '+t,t in idx)
for role in ['Semantic Teacher','Semantic Learner']:
    normalized=role.lower().replace(' ','_')
    present=role in idx or normalized in idx
    check('E','A-Z role '+role,present)

# Core artifact coverage
artifact_paths={'Chapter 2':DOCS/'chapter02','Section 10.1':DOCS/'chapter10/10_01.html','Canonical model':DOCS/'canonical-model.html','CHANGES':ROOT/'CHANGES.md'}
phrases=['Semantic Teacher','Semantic Feedback Learning Pipeline','Semantic Representation','Memory State','Memory Vector','READ','UPDATE']
for label,path in artifact_paths.items():
    text=('\n'.join(x.read_text(errors='replace') for x in sorted(path.rglob('*.html'))) if path.is_dir() else path.read_text(errors='replace')) if path.exists() else ''
    check('F',label+' exists',path.exists())
    for phrase in phrases: check('F',label+' contains '+phrase,phrase in text)

# semantic regression patterns: positive obsolete assertions only
corpus='\n'.join(p.read_text(errors='replace') for p in list((ROOT/'state').rglob('*.yaml'))+list(DOCS.rglob('*.html')))
patterns={
 'passive storage assertion':r'Associative Memory\s+(?:is|acts as)\s+(?:a\s+)?passive storage',
 'raw observation direct update':r'(?:raw|external) observations?\s+(?:are|is)\s+(?:the\s+)?(?:canonical\s+)?input\s+(?:to|of|for)\s+UPDATE',
 'UPDATE positively produces Memory Vector':r'UPDATE(?!(?:[^\n<]{0,40})(?:never|not|does not|no ))[^\n<]{0,100}(?:produce|return|generate)s?[^\n<]{0,40}Memory Vector',
}
for name,pat in patterns.items():
    hits=re.findall(pat,corpus,re.I)
    check('G','no '+name,not hits,str(hits[:3]))

# Stage 2 provenance manifest remains as an immutable input record. Stage 3 writes a new current manifest.
check('H','Stage 2 provenance manifest exists',(ROOT/'STAGE2_MANIFEST.json').exists())

# project tests represented separately by runner
failed=[c for c in checks if c['status']=='FAIL']
out={'version':'0.3.17-stage3','summary':{'total':len(checks),'pass':len(checks)-len(failed),'fail':len(failed),'status':'PASS' if not failed else 'FAIL'},'checks':checks}
(ROOT/'STAGE3_CONSISTENCY_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out['summary']))
sys.exit(1 if failed else 0)
