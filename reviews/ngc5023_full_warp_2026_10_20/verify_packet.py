"""Verify execution identity, independent-review pins, and prior-packet preservation."""
import argparse,datetime,hashlib,json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
VALIDATOR=Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py')
PRIOR=['final_closure_push','novel_closure_routes','attraction_from_existing','conversion_dynamics','polarization_link','collective_state_door','ugc08286_profile','ngc5023_cube']

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

def pin(p,h):return {'path':str(p.relative_to(ROOT)),'expected':h,'actual':sha(p) if p.is_file() else None,'passed':p.is_file() and sha(p)==h}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');a=ap.parse_args();runs=[]
 for p in sorted(HERE.rglob('manifest.json')):
  d=json.loads(p.read_text())
  if d.get('schema_version')!=2:continue
  q=subprocess.run([sys.executable,str(VALIDATOR),str(p),'--root',str(ROOT)],capture_output=True,text=True,timeout=45)
  runs.append({'path':str(p.relative_to(ROOT)),'status':d['run']['status'],'manifest_sha256':sha(p),'validator_exit':q.returncode,'stdout':q.stdout.strip(),'stderr':q.stderr.strip(),'current_identity_valid':q.returncode==0})
 old=[]
 for name in PRIOR:
  folder=ROOT/'reviews'/(name+'_2026_10_20');ip=folder/'PACKET_SHA256.json';d=json.loads(ip.read_text());checks=[pin(folder/n,h) for n,h in d['files'].items()]
  old.append({'inventory':str(ip.relative_to(ROOT)),'inventory_sha256':sha(ip),'checks':checks,'all_passed':all(x['passed'] for x in checks)})
 provenance=[]
 for p in sorted(x for x in HERE.rglob('*.json') if x.name.lower().endswith('provenance.json')):
  d=json.loads(p.read_text());table=d.get('artifacts',d.get('files',{}));checks=[]
  entries=table if isinstance(table,list) else [{'path':n,'sha256':h['sha256'] if isinstance(h,dict) else h} for n,h in table.items()]
  for entry in entries:
   n=entry['path'];candidates=[ROOT/n,HERE/n,p.parent/n];existing=[x for x in candidates if x.is_file()]
   x=next((x for x in existing if sha(x)==entry['sha256']),existing[0] if existing else candidates[0]);checks.append(pin(x,entry['sha256']))
  provenance.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p),'checks':checks,'all_passed':all(x['passed'] for x in checks)})
 completed=[r for r in runs if r['status']=='completed'];history=[r for r in runs if r['status']!='completed']
 archive_checks=[]
 for run,original,archive in [('audit/stats_run001','audit/stats_verify_results.py','audit/stats_verify_results_v1_failed.py'),('recovery/digitization_run001','recovery/digitize_rings.py','recovery/digitize_rings_v1_failed.py')]:
  d=json.loads((HERE/run/'manifest.json').read_text());target=str((HERE/original).relative_to(ROOT));h=next(x['sha256'] for x in d['input_artifacts'] if x['path']==target);archive_checks.append(pin(HERE/archive,h))
 passed=all(x['passed'] for x in archive_checks) and all(r['current_identity_valid'] for r in completed) and all(x['all_passed'] for x in old+provenance)
 record={'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'assessment_base':'c821a8bccc8a20e107b4c6771d31e02d05aa8b10',
  'all_current_completed_evidence_checks_passed':passed,'completed_records':len(completed),'historical_noncompleted_records':len(history),'runs':runs,
  'earlier_files_preserved':sum(len(x['checks']) for x in old),'prior_packets':old,'source_audit_pin_freshness':provenance,'historical_failed_input_archives':archive_checks,
  'scope':'Bookkeeping and currentidentity check, not a scientific rerun, model adequacy, or discovery test. Historical failedrecords are not scientific evidence. No hardmemory cap or CPUaffinity enforced.'}
 if a.write:(HERE/'VERIFICATION.json').write_text(json.dumps(record,indent=2)+'\n')
 print(json.dumps({k:record[k] for k in ['all_current_completed_evidence_checks_passed','completed_records','historical_noncompleted_records','earlier_files_preserved']},indent=2))
 for r in runs:
  if not r['current_identity_valid']:print('Non-current record',r['path'],r['status'],r['stdout'],r['stderr'])
 for group in old+provenance:
  for c in group['checks']:
   if not c['passed']:print('Bad pin',c)
 return 0 if passed else 1
if __name__=='__main__':raise SystemExit(main())
