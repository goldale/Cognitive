#!/usr/bin/env python3
import hashlib, json, pathlib, subprocess, sys, tarfile, tempfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
checks=[]
def check(name, ok, detail=''):
    checks.append({'name':name,'status':'PASS' if ok else 'FAIL','detail':detail})

def load_json(p):
    try: return json.loads(p.read_text())
    except Exception as e: check(f'json:{p.name}',False,str(e)); return {}

m=load_json(ROOT/'RELEASE_MANIFEST.json')
check('manifest release',m.get('release')=='0.3.19',str(m.get('release')))
check('manifest version',m.get('version')=='0.3.19',str(m.get('version')))
check('release notes target',(ROOT/m.get('release_notes','')).is_file(),m.get('release_notes',''))
check('pyproject version','version = "0.3.19"' in (ROOT/'pyproject.toml').read_text())
for p in ['README.md','CHANGES.md','ARCHITECTURE_FREEZE.md','RELEASE_MANIFEST.json','RELEASE_NOTES_0.3.19.md','state','docs','src','tests','scripts']:
    check('required:'+p,(ROOT/p).exists())
# no packaging junk
junk=[]
for p in ROOT.rglob('*'):
    if any(x in p.parts for x in ['.git','.pytest_cache','__pycache__','dist']) or p.name.endswith(('.pyc','.pyo')):
        junk.append(str(p.relative_to(ROOT)))
check('no transient artifacts',not junk,', '.join(junk[:10]))
# stage gates
for f, token in [('STAGE3_CHECK_SUMMARY.txt','PASS'),('STAGE4_CHECK_SUMMARY.txt','PASS'),('STAGE5_CHECK_SUMMARY.txt','PASS'),('STAGE6_CHECK_SUMMARY.txt','PASS')]:
    check('gate:'+f,(ROOT/f).is_file() and token in (ROOT/f).read_text())
# build script naming/version
b=(ROOT/'scripts/build_release.sh').read_text()
check('build release version','0.3.19' in b)
# canonical docs
idx=(ROOT/'docs/index.html')
check('docs index',idx.is_file() and idx.stat().st_size>1000)
check('A-Z index',(ROOT/'docs/chapter26/index.html').is_file())
# all YAML parse
try:
 import yaml
 for p in ROOT.joinpath('state').rglob('*.yaml'): yaml.safe_load(p.read_text())
 check('all state YAML parse',True)
except Exception as e: check('all state YAML parse',False,str(e))
# previous validators
for script in ['validate_stage1_freeze.py','validate_stage3_consistency.py','validate_stage4_duplicates.py','validate_stage5_architecture.py','validate_stage6_documentation.py']:
    r=subprocess.run([sys.executable,str(ROOT/'scripts'/script)],cwd=ROOT,text=True,capture_output=True)
    check('validator:'+script,r.returncode==0,(r.stdout+r.stderr)[-500:])
failed=[x for x in checks if x['status']=='FAIL']
out={'release':'cognitive-0.3.19','stage':7,'status':'PASS' if not failed else 'FAIL','checks':checks,'summary':{'pass':len(checks)-len(failed),'fail':len(failed)}}
(ROOT/'STAGE7_RELEASE_RESULTS.json').write_text(json.dumps(out,indent=2)+"\n")
print(f"Stage 7 release validation: {out['summary']['pass']} PASS / {out['summary']['fail']} FAIL")
sys.exit(1 if failed else 0)
