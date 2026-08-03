from __future__ import annotations
import hashlib, json, shutil, subprocess, sys
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
STATE=ROOT/'state'
CAN=STATE/'canonical'

def load(name): return yaml.safe_load((CAN/name).read_text())
def dump(path,obj): path.write_text(yaml.safe_dump(obj,sort_keys=False,allow_unicode=True,width=110),encoding='utf-8')

components=load('components.yaml')['components']
contracts=load('contracts.yaml')
invariants=load('invariants.yaml')['invariants']
terms=load('terminology.yaml')['terms']
# Canonical component roles must also be first-class indexable terminology.
_role_terms = {
    'Semantic Learner': 'The Associative Memory role that incorporates Transformer-produced Semantic Representations into Memory State through UPDATE.',
    'Contextual Retriever': 'The Associative Memory role that produces a Memory Vector through explicit READ without modifying Memory State.',
}
_existing_terms = {item['term'] for item in terms}
for _term, _definition in _role_terms.items():
    if _term not in _existing_terms:
        terms.append({'term': _term, 'definition': _definition})
dump(CAN/'terminology.yaml', {'kind': 'T_Collection', 'schema_version': '0.3.15', 'terms': terms})
principles=load('principles.yaml')['principles']

# Chapter 2: preserve old sections while inserting a generated architecture overview first.
chapters=yaml.safe_load((STATE/'chapters.yaml').read_text())
ch2=next(c for c in chapters['chapters'] if c['order']==2)
ch2['title']='Architecture Overview and Design Principles'
ch2['summary']='Presents the canonical Cognitive architecture, its semantic self-learning loop, and the design principles governing model evolution.'
old_sections=[s for s in ch2['sections'] if s['id']!='S_02_01_ARCH']
for s in old_sections:
    s['order']=int(s['order'])+1
ch2['sections']=[{
 'kind':'T_Section','id':'S_02_01_ARCH','title':'Canonical Architecture Overview','order':1,
 'content_file':'content/02_01_architecture_overview.yaml'}]+old_sections
dump(STATE/'chapters.yaml',chapters)

nodes=[]
kindmap={'external':'external','subsystem':'subsystem','state':'state','interface':'interface','data':'data','process':'control'}
for c in components:
    nodes.append({'id':c['id'],'label':c['name'],'kind':kindmap.get(c['kind'],'subsystem')})
edges=[
 {'from':'C_EXT_INPUT','to':'C_ASSOC_MEMORY','label':'query','flow':'information'},
 {'from':'C_MEMORY_STATE','to':'C_ASSOC_MEMORY','label':'READ state','flow':'context'},
 {'from':'C_ASSOC_MEMORY','to':'C_MEMORY_VECTOR','label':'READ','flow':'information'},
 {'from':'C_MEMORY_VECTOR','to':'C_TRANSFORMER','label':'conditioning','flow':'information'},
 {'from':'C_TRANSFORMER','to':'C_SEM_REP','label':'semantic teaching','flow':'learning'},
 {'from':'C_SEM_REP','to':'C_SFL_PIPELINE','label':'learning input','flow':'learning'},
 {'from':'C_SFL_PIPELINE','to':'C_ASSOC_MEMORY','label':'UPDATE','flow':'learning'},
 {'from':'C_ASSOC_MEMORY','to':'C_MEMORY_STATE','label':'updated state','flow':'learning'},
]
blocks=[
 {'type':'paragraph','text':'Cognitive separates semantic reasoning, associative retrieval, persistent memory state, and self-learning while connecting them through explicit typed interfaces.'},
 {'type':'principle','title':'Primary architectural principle','text':'The Transformer is both the Semantic Reasoning Engine and the Semantic Teacher of Associative Memory. Associative Memory learns from Transformer-produced Semantic Representations rather than raw external observations.'},
 {'type':'diagram','title':'Cognitive Architecture — Functional Overview','description':'A compact system-level view. The detailed closed learning lifecycle and operation contracts are defined canonically in Section 10.1.','direction':'LR','size':'standard','nodes':[
   {'id':'overview_external','label':'External Input','kind':'external'},
   {'id':'overview_memory','label':'Associative Memory','kind':'subsystem'},
   {'id':'overview_transformer','label':'Transformer','kind':'subsystem'},
   {'id':'overview_learning','label':'Semantic Feedback Learning Pipeline','kind':'control'},
   {'id':'overview_state','label':'Memory State','kind':'state'},
 ],'edges':[
   {'from':'overview_external','to':'overview_memory','label':'query','flow':'information'},
   {'from':'overview_memory','to':'overview_transformer','label':'retrieved context','flow':'information'},
   {'from':'overview_transformer','to':'overview_learning','label':'semantic teaching','flow':'learning'},
   {'from':'overview_learning','to':'overview_state','label':'controlled update','flow':'learning'},
   {'from':'overview_state','to':'overview_memory','label':'retrieval state','flow':'context'},
 ],'readability_priority':True,'proportionality_priority':True},
 {'type':'note','title':'Canonical detailed specification','text':'Section 10.1 owns the complete Semantic Feedback Learning lifecycle, the READ and UPDATE contracts, and the rule that UPDATE never produces a Memory Vector. This overview intentionally does not repeat that complete definition.'},
 {'type':'heading','level':3,'text':'Operation asymmetry'},
 {'type':'table','headers':['Operation','Architectural purpose','Canonical owner'], 'rows':[
   ['READ','Retrieve context without changing memory','Section 10.1'],
   ['UPDATE','Incorporate semantic learning into Memory State','Section 10.1'],
 ]},
 {'type':'paragraph','text':'The release-blocking READ/UPDATE invariants are defined canonically in Section 10.1 and in state/canonical/invariants.yaml.'},
 {'type':'heading','level':3,'text':'First-class self-learning process'},
 {'type':'paragraph','text':'The Semantic Feedback Learning Pipeline is an independent architectural object with explicit stages, contracts, invariants, and future extension points for consolidation, replay, forgetting, structural plasticity, and evaluation.'},
]
dump(STATE/'content'/'02_01_architecture_overview.yaml',{'kind':'T_Content','section':'S_02_01_ARCH','blocks':blocks})

# Canonical rewrite of Section 10.1.
ch10=next(c for c in chapters['chapters'] if c['order']==10)
sec10=next(s for s in ch10['sections'] if s['order']==1)
sec10['title']='Semantic Feedback Learning and Subsystem Separation'
dump(STATE/'chapters.yaml',chapters)
read=next(o for o in contracts['operations'] if o['name']=='READ')
update=next(o for o in contracts['operations'] if o['name']=='UPDATE')
sec_blocks=[
 {'type':'paragraph','text':'Transformer and Associative Memory are separated by responsibility but coupled by a closed semantic learning loop. The Transformer does not merely consume memory for reasoning; it teaches Associative Memory by producing the semantic objects used for learning.'},
 {'type':'definition','title':'Semantic Teacher','text':'The Transformer role that converts externally grounded processing and retrieved context into a Semantic Representation suitable for Associative Memory UPDATE.'},
 {'type':'definition','title':'Semantic Feedback Learning Pipeline','text':'A first-class architectural process coordinating explicit READ, semantic reasoning, semantic teaching, UPDATE, and the resulting evolution of Memory State.'},
 {'type':'diagram','title':'Closed Semantic Learning Loop','description':'External Input is interpreted with an explicitly retrieved Memory Vector. Transformer output becomes a Semantic Representation. UPDATE changes Memory State only; a later READ is required to obtain another Memory Vector.','direction':'TB','size':'standard','nodes':nodes,'edges':edges,'readability_priority':True,'proportionality_priority':True},
 {'type':'heading','level':3,'text':'READ contract'},
 {'type':'formula','text':'READ(Memory State, Query) -> Memory Vector'},
 {'type':'paragraph','text':'READ is a retrieval operation. It may expose context to the Transformer but never modifies Memory State.'},
 {'type':'heading','level':3,'text':'UPDATE contract'},
 {'type':'formula','text':'UPDATE(Memory State, Semantic Representation) -> Updated Memory State'},
 {'type':'paragraph','text':'UPDATE is a learning operation. Its only architectural effect is modification of Memory State. It does not generate a new Memory Vector and performs no implicit retrieval. A Memory Vector is generated exclusively by a subsequent explicit READ operation.'},
 {'type':'principle','title':'Why semantic feedback is necessary','text':'Raw external observations are not stable learning targets. Transformer-produced Semantic Representations provide interpretation, normalization, context, and abstraction before information is incorporated into Associative Memory.'},
 {'type':'heading','level':3,'text':'Lifecycle and extension boundary'},
 {'type':'list','items':['Explicit READ retrieves a Memory Vector from the current Memory State.','Transformer performs semantic reasoning using external input and retrieved context.','Transformer acts as Semantic Teacher and produces a Semantic Representation.','The Semantic Feedback Learning Pipeline submits that representation to UPDATE.','UPDATE modifies Memory State only.','Any effect of learning on retrieval is observed only by a later explicit READ.']},
 {'type':'note','title':'Deferred extensions','text':'Sleep, replay, forgetting, importance estimation, structural plasticity, and global evaluation may extend the pipeline later, but they must preserve the READ/UPDATE asymmetry unless a future architecture decision explicitly replaces it.'},
]
dump(STATE/'content'/'10_01.yaml',{'kind':'T_Content','section':'S_10_01','blocks':sec_blocks})

# Markdown derivatives generated from canonical YAML.
docs_src=ROOT/'generated-source'
docs_src.mkdir(exist_ok=True)
chapter2=['# Chapter 2 — Architecture Overview and Design Principles','',
 '## 2.1 Canonical Architecture Overview','',
 'The Transformer is both the **Semantic Reasoning Engine** and the **Semantic Teacher** of Associative Memory.','',
 '```text','External Input -> READ -> Memory Vector -> Transformer','                                  |','                                  v','                      Semantic Representation','                                  |','                                  v','                               UPDATE','                                  |','                                  v','                            Memory State','```','',
 '## Canonical operation contracts','',
 '| Operation | Inputs | Output | State effect |','|---|---|---|---|',
 '| READ | Memory State, Query | Memory Vector | None |','| UPDATE | Memory State, Semantic Representation | Updated Memory State | Modifies only Memory State |','',
 '> UPDATE never produces a Memory Vector. A new Memory Vector is generated only by a subsequent explicit READ.','']
(docs_src/'CHAPTER_02.md').write_text('\n'.join(chapter2),encoding='utf-8')

changes=['# CHANGES — cognitive 0.3.15','', 'This incremental release introduces a complete architectural refactoring around Semantic Feedback Learning.','', '## Architectural changes','']
for p in principles: changes.append(f"- **{p['title']}** — {p['statement']}")
changes += ['', '## Interface changes','', '- `READ(Memory State, Query) -> Memory Vector` is explicitly non-mutating.', '- `UPDATE(Memory State, Semantic Representation) -> Updated Memory State` modifies only Memory State.', '- UPDATE no longer has Question, Answer, hidden state, or Memory Vector as canonical outputs.', '', '## Generated documentation', '', '- Chapter 2 is regenerated from canonical YAML.', '- Section 10.1 is completely rewritten.', '- HTML navigation and the A–Z Index are regenerated.', '- Component and canonical-model references are regenerated.', '']
(ROOT/'CHANGES.md').write_text('\n'.join(changes),encoding='utf-8')

comp=['# Component Reference','']
for c in components:
    comp += [f"## {c['name']}", '', f"- ID: `{c['id']}`", f"- Kind: `{c['kind']}`", f"- Roles: {', '.join('`'+r+'`' for r in c['roles'])}", '']
(docs_src/'COMPONENT_REFERENCE.md').write_text('\n'.join(comp),encoding='utf-8')

# Update package/release version markers.
pp=ROOT/'pyproject.toml'; txt=pp.read_text(); txt=txt.replace('version = "0.3.14"','version = "0.3.15"'); pp.write_text(txt)
mk=ROOT/'Makefile'; txt=mk.read_text().replace('cognitive-systems-lab-0.3.14.tar.gz','cognitive-systems-lab-0.3.15.tar.gz'); mk.write_text(txt)
br=ROOT/'scripts'/'build_release.sh'; txt=br.read_text().replace('cognitive-systems-lab-0.3.14.tar.gz','cognitive-systems-lab-0.3.15.tar.gz'); br.write_text(txt)
manifest=yaml.safe_load((STATE/'manifest.yaml').read_text()); manifest['version']='0.3.15-stage2'; dump(STATE/'manifest.yaml',manifest)

print('Stage 2 canonical derivatives generated.')
