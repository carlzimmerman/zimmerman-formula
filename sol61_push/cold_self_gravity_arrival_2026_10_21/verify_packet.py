"""Read-only packet integrity check. Does not import or run any physics model."""
from pathlib import Path
import argparse,json,hashlib,subprocess,sys
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path);ap.add_argument('--index',action='store_true');a=ap.parse_args();r=Path(__file__).resolve().parent;historical=Path('/private/tmp/cold-energy-heartbeat-20261021T003805Z');checks=[]
sha=lambda b:hashlib.sha256(b).hexdigest()
def ck(k,v):checks.append({'check':k,'passed':bool(v)})
def read(p):return json.loads((r/p).read_text())
def locate(p):
 p=Path(p)
 try:return r/p.relative_to(historical)
 except ValueError:return p
if a.repo:
 j=read('final941/source/sources.json')
 for e in j['sources']:
  b=subprocess.check_output(['git','show',e['commit_tree']+':'+e['path']],cwd=a.repo);ck('final941 committed blob '+e['path'],sha(b)==e['sha256'])
 for e in read('final941/diagnostic/sources.json'):
  b=subprocess.check_output(['git','show',e['source_revision']+':'+e['source_path']],cwd=a.repo);ck('diagnostic pinned blob '+e['source_path'],sha(b)==e['sha256'])
 j=read('late_ownership_receipt.json');b=subprocess.check_output(['git','show',j['revision']+':'+j['path']],cwd=a.repo);ck('late ownership committed ledger',sha(b)==j['committed_sha256'])
for e in read('final941/diagnostic/sources.json'):ck('diagnostic snapshot '+e['snapshot_path'],sha((r/'final941/diagnostic'/e['snapshot_path']).read_bytes())==e['sha256'])
for f in ['final941/proof/sources_final941.json','final941/proof/sources_diagnostic_review.json','final941/growth/sources_growth.json']:
 j=read(f);o=j.get('review',j.get('report'));ck('review output '+f,sha(locate(o['path']).read_bytes())==o['sha256'])
j=read('final941/proof/final_report_review_receipt.json');ck('exact peer report retained',sha((r/'final941/proof/RESULT_reviewed.md').read_bytes())==j['reviewed_report_sha256']);ck('focused report review bytes',sha(locate(j['review']).read_bytes())==j['review_sha256'])
j=read('REVIEW_RESOLUTION.json');ck('final report after explicit strictness correction',sha((r/'RESULT.md').read_bytes())==j['final_report_sha256'])
m=read('final941/diagnostic/run_001/manifest.json')
for key in ['input_artifacts','outputs']:
 for e in m[key]:ck('bounded manifest '+e['path'],sha((r/'final941/diagnostic'/e['path']).read_bytes())==e['sha256'])
z=read('final941/diagnostic/run_001/results.json');ck('diagnostic completed',m['run']['status']=='completed' and m['run']['exit_status']==0);ck('16 finite diagnostic controls',len(z['checks'])==16 and z['passed'] and all(c['passed'] for c in z['checks']));ck('measured RSS below1GB',z['maximum_measured_RSS_bytes']<1000000000)
if a.index:
 for e in read('packet_index.json')['artifacts']:ck('payload '+e['path'],sha((r/e['path']).read_bytes())==e['sha256'])
o={'scope':'Evidence integrity and recorded completed finite controls, not a whole-theory certificate','passed':all(c['passed'] for c in checks),'count':len(checks),'repo_source_checks':bool(a.repo),'packet_index_checks':a.index,'checks':checks};print(json.dumps(o,indent=2));sys.exit(0 if o['passed'] else 1)
