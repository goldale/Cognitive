#!/usr/bin/env python3
from __future__ import annotations
import json, re, sys, hashlib
from collections import defaultdict, Counter
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
CONTENT=ROOT/'state/content'
checks=[]
def add(group,name,ok,detail=''):
    checks.append({'group':group,'name':name,'status':'PASS' if ok else 'FAIL','detail':detail})

def norm(s):
    return re.sub(r'\s+',' ',re.sub(r'[`*_#>]+',' ',s)).strip().lower()

def iter_text(v, path=''):
    if isinstance(v,dict):
        for k,x in v.items():
            if k in {'text','description','statement','definition'} and isinstance(x,str):
                yield path+'/'+k,x
            else:
                yield from iter_text(x,path+'/'+str(k))
    elif isinstance(v,list):
        for i,x in enumerate(v): yield from iter_text(x,path+'/'+str(i))

# A. Exact long prose duplication across authored content.
texts=defaultdict(list)
docs={}
for p in sorted(CONTENT.glob('*.yaml')):
    d=yaml.safe_load(p.read_text()) or {}; docs[p.name]=d
    for loc,t in iter_text(d):
        n=norm(t)
        if len(n)>=100: texts[n].append(f'{p.name}{loc}')
exact={k:v for k,v in texts.items() if len(v)>1}
add('A','no exact long prose duplicates',not exact,'; '.join(f'{v}' for v in list(exact.values())[:10]))

# B. Diagram identity and ownership.
def diagram_sig(b):
    nodes=tuple(sorted((n.get('label',''),n.get('kind','')) for n in b.get('nodes',[])))
    edges=tuple(sorted((e.get('from',''),e.get('to',''),e.get('label',''),e.get('flow','')) for e in b.get('edges',[])))
    return nodes,edges
sigs=defaultdict(list)
for fn,d in docs.items():
    for i,b in enumerate(d.get('blocks',[])):
        if b.get('type')=='diagram':
            sig=diagram_sig(b)
            # Legacy placeholder diagrams without structured nodes/edges are not semantic duplicates.
            if sig != ((),()): sigs[sig].append(f'{fn}#{i}:{b.get("title","")}')
ident={k:v for k,v in sigs.items() if len(v)>1}
add('B','no identical diagrams in multiple sections',not ident,'; '.join(map(str,list(ident.values())[:10])))
ch2=docs.get('02_01_architecture_overview.yaml',{})
s10=docs.get('10_01.yaml',{})
ch2_titles=[b.get('title') for b in ch2.get('blocks',[]) if b.get('type')=='diagram']
s10_titles=[b.get('title') for b in s10.get('blocks',[]) if b.get('type')=='diagram']
add('B','Chapter 2 owns compact functional overview','Cognitive Architecture — Functional Overview' in ch2_titles,str(ch2_titles))
add('B','Section 10.1 owns detailed closed learning loop','Closed Semantic Learning Loop' in s10_titles,str(s10_titles))

# C. Canonical ownership map and cross-reference behavior.
own=yaml.safe_load((ROOT/'state/canonical/ownership.yaml').read_text())
owner={x['concept']:x['canonical_location'] for x in own['ownership']}
required={'Architecture Overview':'Chapter 2','Transformer roles':'Transformer chapter','Associative Memory operations':'Associative Memory chapter','Memory State':'Memory State chapter','Semantic Feedback Learning':'Section 10.1','Progressive Training':'Progressive Training chapter'}
for concept,location in required.items(): add('C',f'ownership {concept}',owner.get(concept)==location,str(owner.get(concept)))
ch2corpus=' '.join(norm(t) for _,t in iter_text(ch2))
add('C','Chapter 2 references Section 10.1','section 10.1' in ch2corpus)
add('C','Chapter 2 explicitly avoids full redefinition','does not repeat that complete definition' in ch2corpus)

# D. Canonical definition uniqueness for first-class new terms.
def_titles=defaultdict(list)
for fn,d in docs.items():
    for i,b in enumerate(d.get('blocks',[])):
        if b.get('type')=='definition': def_titles[b.get('title','')].append(f'{fn}#{i}')
for term,expected in [('Semantic Teacher','10_01.yaml'),('Semantic Feedback Learning Pipeline','10_01.yaml')]:
    locs=def_titles.get(term,[])
    add('D',f'one canonical definition: {term}',len(locs)==1 and locs[0].startswith(expected),str(locs))

# E. Contract canonicality: exact formulas only in owner section among chapter content.
formula_locs=defaultdict(list)
for fn,d in docs.items():
    for i,b in enumerate(d.get('blocks',[])):
        if b.get('type')=='formula': formula_locs[norm(b.get('text',''))].append(f'{fn}#{i}')
for formula in ['READ(Memory State, Query) -> Memory Vector','UPDATE(Memory State, Semantic Representation) -> Updated Memory State']:
    locs=formula_locs.get(norm(formula),[])
    add('E',f'canonical formula owned by Section 10.1: {formula.split("(")[0]}',len(locs)==1 and locs[0].startswith('10_01.yaml'),str(locs))

# F. Generated HTML duplicate identifiers and critical navigation.
html=list((ROOT/'docs').rglob('*.html'))
id_pat=re.compile(r'\bid=["\']([^"\']+)["\']')
dups=[]
for p in html:
    ids=id_pat.findall(p.read_text(errors='replace'))
    repeated=[x for x,c in Counter(ids).items() if c>1]
    if repeated: dups.append(f'{p.relative_to(ROOT)}:{repeated}')
add('F','no duplicate HTML ids',not dups,'; '.join(dups[:10]))
idx=(ROOT/'docs/chapter19/index.html').read_text(errors='replace') if (ROOT/'docs/chapter19/index.html').exists() else ''
for term in ['Semantic Teacher','Semantic Learner','Semantic Feedback Learning Pipeline','Memory Vector']:
    add('F',f'A-Z contains {term}',term in idx)

failed=[x for x in checks if x['status']=='FAIL']
result={'version':'0.3.15-stage4','summary':{'total':len(checks),'pass':len(checks)-len(failed),'fail':len(failed),'status':'PASS' if not failed else 'FAIL'},'checks':checks}
(ROOT/'STAGE4_DUPLICATE_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result['summary']))
sys.exit(1 if failed else 0)
