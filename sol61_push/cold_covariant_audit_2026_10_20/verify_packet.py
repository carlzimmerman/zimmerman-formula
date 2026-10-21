"""Read-only evidence/source integrity check. Does not execute a physics model."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path);ap.add_argument('--index',action='store_true');args=ap.parse_args()
r=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
checks=[]
def check(label,ok):
 checks.append({'check':label,'passed':bool(ok)})
def blob(commit,path):
 return subprocess.check_output(['git','show',commit+':'+path],cwd=args.repo)
if args.repo:
 f=json.loads((r/'formation/sources_cfg938.json').read_text())
 for e in f['artifacts']:
  check('CFG938 exact commit '+e['path'],sha(blob(e['commit_resolved'],e['path']))==e['committed_sha256'])
 n=json.loads((r/'numerical/CFG938_NUMERICAL_AUDIT_v2.json').read_text())
 for e in n['inputs']:
  check('numerical source '+e['path'],sha(blob(e['revision'],e['path']))==e['git_blob_sha256'])
 sh=json.loads((r/'shell/sources_final939.json').read_text())
 for e in sh['sources']:
  rel=str(Path(e['path']).relative_to(args.repo))
  check('CFG939 exact commit '+rel,sha(blob(e['commit'],rel))==e['sha256'])
  p=r/'shell/final939_snapshot'/Path(e['path']).name
  check('CFG939 snapshot '+p.name,sha(p.read_bytes())==e['sha256'])
 t=json.loads((r/'tensor/source_snapshot.json').read_text())
 for e in t['files']:
  check('tensor snapshot '+e['snapshot_path'],sha((r/'tensor'/e['snapshot_path']).read_bytes())==e['sha256'])
  rel=str(Path(e['original_path']).relative_to(args.repo))
  check('tensor commit '+rel,sha(blob(e['source_revision'],rel))==e['sha256'])
for rel in ['formation/sources_cfg938.json','shell/sources_final939.json']:
 data=json.loads((r/rel).read_text())
 for key in ['review','tensor_adversarial_review','proposed_repair_scope','report']:
  if key in data:
   e=data[key];p=Path(e['path']);p=r/Path(rel).parent/p.name
   check('review receipt '+str(p.relative_to(r)),sha(p.read_bytes())==e['sha256'])
man=json.loads((r/'tensor/run_001/manifest.json').read_text())
for group in ['input_artifacts','outputs']:
 for e in man[group]:check('manifest '+e['path'],sha((r/'tensor'/e['path']).read_bytes())==e['sha256'])
res=json.loads((r/'tensor/run_001/results.json').read_text())
check('completed tensor runner',man['run']['status']=='completed' and man['run']['exit_status']==0)
if args.index:
 idx=json.loads((r/'packet_index.json').read_text())
 for e in idx['artifacts']:check('packet '+e['path'],sha((r/e['path']).read_bytes())==e['sha256'])
print(json.dumps({'scope':'Read-only hashes and completed run metadata, not a mathematical theorem verdict','source_receipt_checks_included':bool(args.repo),'packet_index_included':args.index,'passed':all(x['passed'] for x in checks),'count':len(checks),'checks':checks},indent=2))
sys.exit(0 if all(x['passed'] for x in checks) else 1)
