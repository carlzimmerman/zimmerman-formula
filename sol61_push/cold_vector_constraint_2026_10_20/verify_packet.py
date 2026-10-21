"""Read-only integrity check; no model evolution or imported model code."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path);ap.add_argument('--index',action='store_true');a=ap.parse_args();r=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest();checks=[]
def ck(name,value):checks.append({'check':name,'passed':bool(value)})
def read(p):return json.loads((r/p).read_text())
for folder in ['vector_review','vector_independent']:
 j=read(folder+'/sources_vector.json');o=j.get('derivation',j.get('output'));p=r/folder/Path(o['path']).name;ck(folder+' analytic output binding',sha(p.read_bytes())==o['sha256'])
j=read('vector_review/final_review_receipt.json');ck('focused review exact bytes',sha((r/'vector_review/FINAL_REVIEW.md').read_bytes())==j['review_sha256']);ck('exact peer-reviewed report retained',sha((r/'vector_review/RESULT_reviewed.md').read_bytes())==j['reviewed_report_sha256'])
j=read('REVIEW_RESOLUTION.json');ck('review correction final report binding',sha((r/'RESULT.md').read_bytes())==j['final_report_sha256'])
for e in read('vector_root/sources.json'):
 ck('source snapshot '+e['snapshot_path'],sha((r/'vector_root'/e['snapshot_path']).read_bytes())==e['sha256'])
 if a.repo and e['source_revision']:
  b=subprocess.check_output(['git','show',e['source_revision']+':'+e['original_path']],cwd=a.repo);ck('source blob '+e['original_path'],sha(b)==e['sha256'])
if a.repo:
 for e in read('formation/sources_clock_triage.json')['artifacts']:
  b=subprocess.check_output(['git','show',e['commit']+':'+e['path']],cwd=a.repo);ck('clock exact blob '+e['path'],sha(b)==e['sha256'])
 j=read('shell/sources_late_a2.json');b=subprocess.check_output(['git','show',j['commit']+':'+j['source_path']],cwd=a.repo);ck('late A2 exact committed blob',sha(b)==j['sha256'])
m=read('vector_root/run_001/manifest.json')
for k in ['input_artifacts','outputs']:
 for e in m[k]:ck('vector manifest '+e['path'],sha((r/'vector_root'/e['path']).read_bytes())==e['sha256'])
z=read('vector_root/run_001/results.json');ck('completed vector run',m['run']['status']=='completed' and m['run']['exit_status']==0);ck('28 exact finite controls passed',len(z['checks'])==28 and z['passed'] and all(x['passed'] for x in z['checks']));ck('measured RSS below 1GB',z['maximum_measured_RSS_bytes']<1000000000)
if a.index:
 for e in read('packet_index.json')['artifacts']:ck('payload '+e['path'],sha((r/e['path']).read_bytes())==e['sha256'])
result={'scope':'Integrity and completed finite-run metadata; not a whole-theory certificate','passed':all(c['passed'] for c in checks),'checks':checks,'count':len(checks),'repo_source_check':bool(a.repo),'packet_index_check':a.index};print(json.dumps(result,indent=2));sys.exit(0 if result['passed'] else 1)
