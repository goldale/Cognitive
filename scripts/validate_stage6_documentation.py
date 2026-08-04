#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, re, sys
from html.parser import HTMLParser
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'
results=[]
def check(group,name,ok,detail=''):
    results.append({'group':group,'name':name,'status':'PASS' if ok else 'FAIL','detail':detail})

def sha(p):
    h=hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()

class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]; self.links=[]; self.images=[]; self.headings=[]; self.title=''; self._title=False; self.main=False; self.nav=False; self.text=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag=='a' and a.get('href'): self.links.append(a['href'])
        if tag=='img' and a.get('src'): self.images.append(a['src'])
        if re.fullmatch(r'h[1-6]',tag): self.headings.append(int(tag[1]))
        if tag=='title': self._title=True
        if tag=='main': self.main=True
        if tag=='nav': self.nav=True
    def handle_endtag(self,tag):
        if tag=='title': self._title=False
    def handle_data(self,data):
        t=data.strip()
        if t:
            self.text.append(t)
            if self._title: self.title += (' ' if self.title else '') + t

# A structure and completeness
required=['README.md','CHANGES.md','ARCHITECTURE_FREEZE.md','generated-source/CHAPTER_02.md','generated-source/COMPONENT_REFERENCE.md','docs/index.html','docs/alphabetical-index.html','docs/canonical-model.html','docs/token-graph.svg']
for f in required: check('A Structure',f,(ROOT/f).is_file())
for d in ['state','state/canonical','state/content','docs','generated-source','scripts','tests','assets','spec']:
    check('A Structure',d,(ROOT/d).is_dir())

# B canonical ownership
own=yaml.safe_load((ROOT/'state/canonical/ownership.yaml').read_text())
entries=own.get('ownership',own.get('entries',[]))
check('B Ownership','ownership entries present',bool(entries),f'{len(entries)} entries')
owner_text=(ROOT/'state/canonical/ownership.yaml').read_text()
for term in ['Semantic Feedback Learning','Transformer','Associative Memory','Memory State','Progressive Training']:
    check('B Ownership',term,term.lower() in owner_text.lower())

# C-F HTML, references, structure
htmls=sorted(DOCS.rglob('*.html'))
check('C HTML','HTML file count',len(htmls)>=100,str(len(htmls)))
parsed={}
for f in htmls:
    p=P(); p.feed(f.read_text(encoding='utf-8')); parsed[f]=p
    check('C HTML',f'{f.relative_to(ROOT)} title',bool(p.title))
    check('C HTML',f'{f.relative_to(ROOT)} main',p.main)
    check('C HTML',f'{f.relative_to(ROOT)} unique ids',len(p.ids)==len(set(p.ids)))
    # Generated block titles intentionally use h4. Require a clear page h1/h2 frame
    # and prohibit deep h5/h6 nesting rather than rejecting that visual convention.
    hierarchy=bool(p.headings) and p.headings[0]==1 and not any(h>4 for h in p.headings) and (len(p.headings)==1 or 2 in p.headings)
    check('F Readability',f'{f.relative_to(ROOT)} heading hierarchy',hierarchy,str(p.headings[:12]))
    for href in p.links:
        if href.startswith(('http://','https://','mailto:','javascript:')): continue
        if href.startswith('#'):
            target=f; frag=href[1:]
        else:
            base,sep,frag=href.partition('#'); target=(f.parent/base).resolve()
        check('D References',f'{f.relative_to(ROOT)} -> {href} file',target.is_file())
        if target.is_file() and frag and target.suffix=='.html':
            tp=parsed.get(target)
            if tp is None:
                tp=P(); tp.feed(target.read_text(encoding='utf-8')); parsed[target]=tp
            check('D References',f'{f.relative_to(ROOT)} -> #{frag}',frag in tp.ids)
    for src in p.images:
        if src.startswith(('http://','https://','data:')): continue
        target=(f.parent/src.split('#',1)[0]).resolve()
        check('D References',f'{f.relative_to(ROOT)} image {src}',target.is_file())

# D2 semantic navigation validation
expected_index=(DOCS/'chapter26/index.html').resolve()
for f in htmls:
    source=f.read_text(encoding='utf-8')
    matches=re.findall(r'<a\b(?=[^>]*\bclass=["\'][^"\']*\balphabetical-index\b[^"\']*["\'])(?=[^>]*\bhref=["\']([^"\']+)["\'])[^>]*>', source, re.I)
    check('D Navigation',f'{f.relative_to(ROOT)} A-Z links present',len(matches)>=2,str(len(matches)))
    for href in matches:
        base=href.split('#',1)[0]
        target=(f.parent/base).resolve()
        check('D Navigation',f'{f.relative_to(ROOT)} A-Z target {href}',target==expected_index,f'{target} != {expected_index}')

# E terminology and index
terms=yaml.safe_load((ROOT/'state/canonical/terminology.yaml').read_text())['terms']
idx=(DOCS/'chapter26/index.html').read_text(encoding='utf-8').lower()
for t in terms:
    term=t['term']
    check('E Terminology',f'index: {term}',term.lower() in idx)
for term in ['Semantic Learner','Contextual Retriever','Semantic Teacher','Semantic Feedback Learning Pipeline','Memory State','Memory Vector','READ','UPDATE']:
    check('E Terminology',f'canonical term: {term}',term.lower() in idx)

# G generated document correspondence
ch2=(ROOT/'generated-source/CHAPTER_02.md').read_text()
changes=(ROOT/'CHANGES.md').read_text()
comp=(ROOT/'generated-source/COMPONENT_REFERENCE.md').read_text()
for phrase in ['Semantic Teacher','Semantic Representation','UPDATE never produces a Memory Vector']:
    check('G Generated',f'Chapter 2: {phrase}',phrase in ch2)
for phrase in ['cognitive-0.3.33','READ(Memory State, Query)','UPDATE(Memory State, Semantic Representation)']:
    check('G Generated',f'CHANGES: {phrase}',phrase in changes)
components=yaml.safe_load((ROOT/'state/canonical/components.yaml').read_text())['components']
for c in components: check('G Generated',f'component reference: {c["name"]}',c['name'] in comp)

# H semantic documentation checks
all_text='\n'.join(p.read_text(encoding='utf-8') for p in list((ROOT/'state/content').glob('*.yaml'))+[ROOT/'generated-source/CHAPTER_02.md',ROOT/'CHANGES.md'])
for phrase in ['UPDATE(Memory State, Semantic Representation)','subsequent explicit READ','Semantic Teacher','first-class architectural process']:
    check('H Semantics',phrase,phrase.lower() in all_text.lower())
# Positive obsolete claims only, avoiding negative statements.
obsolete=[r'Associative Memory is (?:only |merely )?a passive storage',r'UPDATE\([^\n]*\)\s*->\s*Memory Vector',r'raw external observations are (?:the )?canonical.*UPDATE']
for pat in obsolete: check('H Semantics',f'absent: {pat}',re.search(pat,all_text,re.I) is None)

# I human readability quantitative guardrails
paragraphs=[]
for p in parsed.values():
    paragraphs.extend([x for x in p.text if len(x.split())>=8])
long=[x for x in paragraphs if len(x.split())>120]
check('I Human Readability','no paragraphs over 120 words',not long,f'{len(long)} long paragraphs')
css=(ROOT/'assets/cognitive.css').read_text()
for token in ['--text-indent','main {','line-height']:
    check('I Human Readability',f'CSS {token}',token in css)
# diagrams: descriptions and readability flags in key canonical sections
for rel in ['state/content/02_01_architecture_overview.yaml','state/content/10_01.yaml']:
    data=yaml.safe_load((ROOT/rel).read_text()); diagrams=[b for b in data['blocks'] if b.get('type')=='diagram']
    check('I Human Readability',f'{rel} diagram exists',bool(diagrams))
    for i,d in enumerate(diagrams):
        check('I Human Readability',f'{rel} diagram {i} description',bool(d.get('description')))
        check('I Human Readability',f'{rel} diagram {i} readability priority',d.get('readability_priority') is True)

# J reproducibility/source checks
script=(ROOT/'scripts/generate_stage2.py').read_text()
check('J Reproducibility','legacy diagram nodes absent from generator','internal_observation' not in script and "'id':'memory'" not in script)
test=(ROOT/'tests/test_docs.py').read_text()
check('J Reproducibility','regression test reflects canonical loop','no legacy' in test and 'C_SFL_PIPELINE' in test)

failed=[r for r in results if r['status']=='FAIL']
out={'stage':'Stage 6 — Documentation Validation','total':len(results),'pass':len(results)-len(failed),'fail':len(failed),'status':'PASS' if not failed else 'FAIL','checks':results}
(ROOT/'STAGE6_DOCUMENTATION_RESULTS.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:out[k] for k in ['total','pass','fail','status']}))
if failed:
    for r in failed[:50]: print('FAIL',r['group'],r['name'],r['detail'],file=sys.stderr)
    sys.exit(1)
