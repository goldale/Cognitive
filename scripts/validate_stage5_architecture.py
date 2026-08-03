#!/usr/bin/env python3
from __future__ import annotations
import json, re, sys
from collections import defaultdict, deque
from html.parser import HTMLParser
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
checks=[]
def ck(group,name,ok,detail=''):
    checks.append({'group':group,'name':name,'status':'PASS' if ok else 'FAIL','detail':detail})
def y(path): return yaml.safe_load((ROOT/path).read_text())

# A principles
pr=y('state/canonical/principles.yaml')['principles']
byid={p['id']:p for p in pr}
for pid in ['P_021','P_022','P_023','P_024','P_025']:
    ck('A','principle '+pid,pid in byid)
    if pid in byid: ck('A',pid+' accepted',byid[pid].get('status')=='T_Accepted')
ck('A','Transformer semantic teacher principle','Semantic Teacher' in byid['P_021']['statement'])
ck('A','semantic representations learning principle','Semantic Representations' in byid['P_022']['statement'])
ck('A','pipeline first-class principle','first-class architectural object' in byid['P_023']['statement'])
ck('A','READ UPDATE asymmetry principle','never produces a Memory Vector' in byid['P_024']['statement'])
ck('A','explicit READ after learning principle','explicit READ' in byid['P_025']['statement'])

# B components and roles
comps=y('state/canonical/components.yaml')['components']; C={c['name']:c for c in comps}
required=['External Input','Transformer','Associative Memory','Memory State','Memory Vector','Semantic Representation','Semantic Feedback Learning Pipeline']
for n in required: ck('B','component '+n,n in C)
role_reqs={
 'Transformer':['semantic_reasoning_engine','semantic_teacher'],
 'Associative Memory':['contextual_retriever','semantic_learner'],
 'Memory Vector':['read_result','transformer_conditioning'],
 'Semantic Representation':['canonical_update_input'],
 'Semantic Feedback Learning Pipeline':['self_learning','learning_coordination'],
}
for n,roles in role_reqs.items():
    for r in roles: ck('B',f'{n} role {r}',r in C.get(n,{}).get('roles',[]))
ids=[c['id'] for c in comps]; ck('B','component ids unique',len(ids)==len(set(ids)))

# C contracts
contracts=y('state/canonical/contracts.yaml'); O={o['name']:o for o in contracts['operations']}
ck('C','only READ and UPDATE operations',set(O)=={'READ','UPDATE'},str(sorted(O)))
R=O.get('READ',{}); U=O.get('UPDATE',{})
for item in ['Memory State','Query']: ck('C','READ input '+item,item in R.get('inputs',[]))
ck('C','READ output exactly Memory Vector',R.get('outputs')==['Memory Vector'],str(R.get('outputs')))
ck('C','READ has no effects',R.get('effects')==[],str(R.get('effects')))
ck('C','READ forbids Updated Memory State','Updated Memory State' in R.get('forbidden_outputs',[]))
for item in ['Memory State','Semantic Representation']: ck('C','UPDATE input '+item,item in U.get('inputs',[]))
ck('C','UPDATE output exactly Updated Memory State',U.get('outputs')==['Updated Memory State'],str(U.get('outputs')))
ck('C','UPDATE modifies Memory State',U.get('effects')==['modifies Memory State'],str(U.get('effects')))
ck('C','UPDATE forbids Memory Vector','Memory Vector' in U.get('forbidden_outputs',[]))
ck('C','UPDATE forbids implicit READ','READ' in U.get('implicit_operations_forbidden',[]))

# D invariants
invs=y('state/canonical/invariants.yaml')['invariants']; I={i['id']:i for i in invs}
for n in range(1,8):
    iid=f'INV_{n:03d}'; ck('D','invariant '+iid,iid in I)
    if iid in I: ck('D',iid+' release blocking',I[iid].get('severity')=='release_blocking')
expected={
 'INV_001':'READ never modifies Memory State.',
 'INV_002':'UPDATE modifies only Memory State.',
 'INV_003':'UPDATE never produces a Memory Vector.',
 'INV_004':'UPDATE never performs an implicit READ.',
 'INV_005':'A new Memory Vector is produced only by an explicit READ.',
 'INV_006':'Raw external observations are not canonical UPDATE inputs.',
 'INV_007':'The canonical UPDATE input is a Semantic Representation produced by the Transformer.',
}
for iid,s in expected.items(): ck('D',iid+' exact statement',I.get(iid,{}).get('statement')==s,I.get(iid,{}).get('statement',''))

# E pipeline canonical sequence
stages=contracts['pipeline']['stages']
expected_stages=['External Input','Associative Memory READ','Memory Vector','Transformer semantic reasoning','Transformer semantic teaching','Semantic Representation','Associative Memory UPDATE','Updated Memory State']
ck('E','pipeline sequence exact',stages==expected_stages,str(stages))
for a,b in zip(expected_stages,expected_stages[1:]):
    ck('E',f'pipeline ordering {a} before {b}',stages.index(a)<stages.index(b))
ck('E','no direct External Input to UPDATE',not ('External Input' in stages and stages.index('External Input')+1<len(stages) and stages[stages.index('External Input')+1]=='Associative Memory UPDATE'))

# F detailed diagram graph
content=y('state/content/10_01.yaml')
diagrams=[b for b in content['blocks'] if b.get('type')=='diagram']
ck('F','Section 10.1 has one detailed diagram',len(diagrams)==1,str(len(diagrams)))
if diagrams:
    d=diagrams[0]; nodes={n['id']:n for n in d['nodes']}; edges=d['edges']
    ck('F','diagram title canonical',d.get('title')=='Closed Semantic Learning Loop')
    ck('F','diagram node ids unique',len(nodes)==len(d['nodes']))
    required_ids=['C_EXT_INPUT','C_TRANSFORMER','C_ASSOC_MEMORY','C_MEMORY_STATE','C_MEMORY_VECTOR','C_SEM_REP','C_SFL_PIPELINE']
    for nid in required_ids: ck('F','diagram node '+nid,nid in nodes)
    endpoint_ok=all(e['from'] in nodes and e['to'] in nodes for e in edges)
    ck('F','all diagram edge endpoints exist',endpoint_ok)
    deg=defaultdict(int); adj=defaultdict(list)
    for e in edges:
        deg[e['from']]+=1;deg[e['to']]+=1;adj[e['from']].append(e['to'])
    orphan=[n for n in nodes if deg[n]==0]
    ck('F','no orphan diagram nodes',not orphan,', '.join(orphan))
    def edge(fr,to,label=None):
        return any(e['from']==fr and e['to']==to and (label is None or e.get('label')==label) for e in edges)
    for fr,to,label in [
      ('C_EXT_INPUT','C_ASSOC_MEMORY','query'),('C_MEMORY_STATE','C_ASSOC_MEMORY','READ state'),
      ('C_ASSOC_MEMORY','C_MEMORY_VECTOR','READ'),('C_MEMORY_VECTOR','C_TRANSFORMER','conditioning'),
      ('C_TRANSFORMER','C_SEM_REP','semantic teaching'),('C_SEM_REP','C_SFL_PIPELINE','learning input'),
      ('C_SFL_PIPELINE','C_ASSOC_MEMORY','UPDATE'),('C_ASSOC_MEMORY','C_MEMORY_STATE','updated state')]:
        ck('F',f'diagram edge {fr}->{to} [{label}]',edge(fr,to,label))
    bad=[e for e in edges if e['from'] in {'C_SFL_PIPELINE','C_ASSOC_MEMORY'} and e['to']=='C_MEMORY_VECTOR' and e.get('label')=='UPDATE']
    ck('F','diagram has no UPDATE to Memory Vector',not bad,str(bad))

# G semantic source validation
files=list((ROOT/'state').rglob('*.yaml'))+list((ROOT/'docs').rglob('*.html'))+[ROOT/'CHANGES.md']
corpus='\n'.join(p.read_text(errors='replace') for p in files if p.exists())
patterns={
 'passive storage assertion':r'Associative Memory\s+(?:is|acts as)\s+(?:a\s+)?passive (?:storage|store)',
 'raw observation canonical update':r'(?:raw|external) observations?\s+(?:are|is)\s+(?:the\s+)?(?:canonical\s+)?(?:input|training signal)\s+(?:to|for)\s+UPDATE',
 'implicit read assertion':r'UPDATE[^\n<]{0,100}(?:automatically|implicitly)\s+(?:performs?|triggers?|runs?)\s+(?:an?\s+)?READ',
}
for n,p in patterns.items():
    hits=re.findall(p,corpus,re.I)
    ck('G','no '+n,not hits,str(hits[:3]))
# Sentence-level check avoids treating explicit negative invariants as obsolete positive claims.
sentences=re.split(r'(?<=[.!?])\s+|[\n<]+',corpus)
bad=[]
for sentence in sentences:
    low=sentence.lower()
    if 'update' not in low: continue
    tail=low[low.find('update'):]
    if 'memory vector' in tail and re.search(r'\b(produce|produces|return|returns|generate|generates)\b',tail):
        if not re.search(r'\b(never|not|does not|doesn\'t|no)\b',tail):
            bad.append(sentence.strip())
ck('G','no UPDATE produces vector',not bad,str(bad[:3]))
for phrase in ['Transformer is both the Semantic Reasoning Engine and the Semantic Teacher','Semantic Feedback Learning Pipeline','UPDATE never produces a Memory Vector','subsequent explicit READ']:
    ck('G','canonical phrase present: '+phrase,phrase in corpus)

# H terminology and ownership
terms=y('state/canonical/terminology.yaml')['terms']; names=[t['term'] for t in terms]
for n in ['Semantic Teacher','Semantic Feedback Learning','Semantic Feedback Learning Pipeline','Semantic Representation','Memory State','Memory Vector','READ','UPDATE','Semantic Learner','Contextual Retriever']:
    ck('H','term '+n,n in names)
ck('H','terminology unique',len(names)==len(set(names)))
own=y('state/canonical/ownership.yaml'); owners={x['concept']:x['canonical_location'] for x in own['ownership']}
for c,loc in [('Architecture Overview','Chapter 2'),('Semantic Feedback Learning','Section 10.1'),('Memory State','Memory State chapter'),('Progressive Training','Progressive Training chapter')]:
    ck('H',f'ownership {c}',owners.get(c)==loc,str(owners.get(c)))
ck('H','ownership anti-duplication rule present','summarize and link' in own.get('rule',''))

# I generated docs semantic parity
paths=[ROOT/'docs/chapter02/02_01.html',ROOT/'docs/chapter10/10_01.html',ROOT/'docs/canonical-model.html',ROOT/'CHANGES.md']
for p in paths:
    ck('I','artifact exists '+str(p.relative_to(ROOT)),p.exists())
    txt=p.read_text(errors='replace') if p.exists() else ''
    for phrase in ['Semantic Teacher','Semantic Feedback Learning Pipeline','Memory State','Memory Vector','READ','UPDATE']:
        ck('I',f'{p.name} contains {phrase}',phrase in txt)
section=(ROOT/'docs/chapter10/10_01.html').read_text(errors='replace')
ck('I','HTML Section 10.1 explicit UPDATE invariant','UPDATE never produces a Memory Vector' in section or 'does not generate a new Memory Vector' in section)
ck('I','HTML Section 10.1 explicit later READ','subsequent explicit READ' in section)

# J generation policy
G=y('state/canonical/generation.yaml')
ck('J','incremental release model preserved',G.get('incremental_release_model') is True)
ck('J','canonical yaml source included','state/canonical/*.yaml' in G.get('source_of_truth',[]))
ck('J','HTML manual editing forbidden','docs/**/*.html' in G.get('manual_editing_forbidden',[]))
for a in ['Chapter 2 rendering','CHANGES.md','A-Z Index','architecture diagrams']:
    ck('J','generated artifact '+a,a in G.get('generated_artifacts',[]))

failed=[c for c in checks if c['status']=='FAIL']
out={'version':'0.3.15-stage5','summary':{'total':len(checks),'pass':len(checks)-len(failed),'fail':len(failed),'status':'PASS' if not failed else 'FAIL'},'checks':checks}
(ROOT/'STAGE5_ARCHITECTURAL_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out['summary']))
sys.exit(1 if failed else 0)
