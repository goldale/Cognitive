from pathlib import Path
import yaml, sys
root=Path(__file__).resolve().parents[1]
required=["principles.yaml","components.yaml","contracts.yaml","invariants.yaml","terminology.yaml","ownership.yaml","generation.yaml"]
errors=[]
for f in required:
 p=root/"state"/"canonical"/f
 if not p.exists(): errors.append(f"missing {p}")
 else:
  try: yaml.safe_load(p.read_text())
  except Exception as e: errors.append(f"invalid YAML {p}: {e}")
contracts=yaml.safe_load((root/"state/canonical/contracts.yaml").read_text())
ops={o["name"]:o for o in contracts["operations"]}
if ops["UPDATE"]["outputs"] != ["Updated Memory State"]: errors.append("UPDATE output contract")
if "Memory Vector" not in ops["UPDATE"]["forbidden_outputs"]: errors.append("UPDATE must forbid Memory Vector")
if ops["READ"]["outputs"] != ["Memory Vector"]: errors.append("READ output contract")
if errors:
 print("STAGE 1 FREEZE VALIDATION: FAIL")
 print("\n".join(errors)); sys.exit(1)
print("STAGE 1 FREEZE VALIDATION: PASS")
print("7 canonical files parsed; READ/UPDATE asymmetry verified.")
