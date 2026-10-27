from pathlib import Path
import json,hashlib,subprocess,math,datetime
root=Path('/Users/carlzimmerman/new_physics/zimmerman-formula');base='campaign_fresh_gravity/CFG650_theory_v2_combined_pm/';names=['cfg650_native_results.json','cfg650_native_results_MUTATE.json','FROZEN_CRITERIA.md','cfg650_native.py','README.md'];paths=[base+n for n in names];hashes={p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in paths};d=json.loads((root/paths[0]).read_text());m=json.loads((root/paths[1]).read_text());checks=[];rows=[]
def ck(n,v):
 checks.append({'name':n,'pass':bool(v)})
 if not v:raise AssertionError(n)
for name,r in d['runs'].items():
 for survey,s in r['surveys'].items():
  for mode,a in s['fits'].items():ck(name+survey+mode+' chi2 difference',abs(a['F']['chi2']-a['S0']['chi2']-a['dchi2'])<1e-10)
  ck(name+survey+' dropped fraction',abs(1-s['N_kept']/s['N_published']-s['frac_lost'])<1e-12)
  town=m['T_OWN'][name][survey]
  if survey=='KiDS':ck(name+' KiDS gate',s['dchi2']<4 and max(s['robust'].values())<9 and town and s['class']=='CONSISTENT')
  else:ck(name+' DES nondiagnostic',not town and s['class']=='NOT DIAGNOSTIC')
  rows.append({'run':name,'survey':survey,'dchi2':s['dchi2'],'N_kept':s['N_kept'],'N_published':s['N_published'],'T_OWN':town,'class':s['class'],'chi2_F':s['fits']['IA']['F']['chi2'],'p_F_reported_not_recomputed':s['p_F']})
ck('NZ1 all bite',m['NZ1_all_bite']);ck('both footings present',{r['foot'] for r in d['runs'].values()}=={'canonical','alt'})
commit='0576674906';matches={}
for p in paths:
 q=subprocess.run(['git','show',commit+':'+p],cwd=root,capture_output=True);matches[p]=q.returncode==0 and hashlib.sha256(q.stdout).hexdigest()==hashes[p]
ck('source inputs match result revision',all(matches.values()));ck('inputs unchanged',all(hashlib.sha256((root/p).read_bytes()).hexdigest()==h for p,h in hashes.items()))
r={'record':'CE-SHEAR-ARRIVAL-2026-10-19','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_commit':commit,'source_hashes':hashes,'source_matches_commit':matches,'checks':checks,'n_checks':len(checks),'rows':rows,'scope':'Saved-score arithmetic and declared classification audit only; not raw survey/covariance/projection/cache or full initial-condition/run identity reproduction. No scorer or simulation run.','non_claims':['Not a solution to dwarf capture or microscopic gravity','DES not diagnostic; CMB gate not evaluated','Only104/225 KiDS points kept; reported absolute p~.03 remains a separate limitation','Inherited IC/background and nuisance priors; native-input reruns pending per README','Embedded JSON date2026-10-12 is inherited metadata; commit pins this arrival'],'command':'python3 /private/tmp/ce_shear_arrival_audit.py'};Path('/private/tmp/ce_shear_arrival_audit.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'checks':len(checks),'rows':rows},indent=1))
