from pathlib import Path
import json,hashlib,difflib,subprocess
h=Path(__file__).resolve().parent;root=h.parents[2];p='sol61_push/kinetic_receiver_lift_2026_10_12/RESULT.txt';current=(root/p).read_text();old=current
old=old.replace('local coupling, microscopic origin, action and selector remain open. The distinct\ntwo-local-field spatial continuation in LOCAL_RESULT.txt now supplies explicit\nflat-space prototype stress and actual streaming, with the same physical gaps.\n','local stress, causal coupling, microscopic origin, action and selector remain open.\n')
old=old.replace('and outputs are in INPUTS.json and version-2 manifests. The third pre-run criteria\ncommit d7e7b0dbc6afd3a73232ed70ab03ef773cb51cc9 freezes local_run. Its changed\nfield assumption and supplemental exact omission control are recorded separately.\n','and outputs are in INPUTS.json and the two version-2 manifests.\n')
old=old.split('\nLOCAL CONTINUATION\n')[0]+'\n'
inv=json.loads((h/'INPUTS.json').read_text());expected=next(x for x in inv['source_snapshots'] if x['path']==p)['sha256'];actual=hashlib.sha256(old.encode()).hexdigest()
# Exact trailing newline reconstruction is constrained by the recorded historical hash.
if actual!=expected:
 for text in [old.rstrip()+'\n',old.rstrip()+'\n\n']:
  if hashlib.sha256(text.encode()).hexdigest()==expected:old=text;actual=expected;break
assert actual==expected,(actual,expected,len(old.encode()))
(h/'context_historical_hash_matched.txt').write_text(old);(h/'context_current_snapshot.txt').write_text(current)
(h/'context_delta.patch').write_text(''.join(difflib.unified_diff(old.splitlines(True),current.splitlines(True),fromfile='historical RESULT.txt sha256 '+expected,tofile='current RESULT.txt sha256 '+hashlib.sha256(current.encode()).hexdigest())))
d={'context_path':p,'historical_sha256':expected,'current_sha256':hashlib.sha256(current.encode()).hexdigest(),'historical_bytes':len(old.encode()),'current_bytes':len(current.encode()),'historical_recovery':'Reverse the three explicit producer additions visible against original full tool-read text; exact SHA256 matches historical INPUTS and original manifest, not merely line similarity','current_publication_git':'208e62e10e','source_compute_dependence':'checks.py does not open/read/import producer RESULT.txt; it is contextual claim/interpretation provenance only','disposition':'Original run remains historical-context evidence; original manifest is not current-source fresh. Preserve it and rerun unchanged checks with explicit current snapshot/context contract.','original_run_manifest_sha256':hashlib.sha256((h/'run/manifest.json').read_bytes()).hexdigest(),'actual_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()};(h/'CONTEXT_RECONCILIATION.json').write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d))
