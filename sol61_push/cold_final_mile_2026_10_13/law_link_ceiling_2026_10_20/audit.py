from pathlib import Path
import json,hashlib,subprocess,math
R=Path('/Users/carlzimmerman/new_physics/zimmerman-formula');hs={}
for prefix in ['CFG870','CFG871','CFG872']:
 S=next((R/'campaign_fresh_gravity').glob(prefix+'*'))
 for n in ['README.md','FROZEN_CRITERIA.md',prefix.lower()+'.py',prefix.lower()+'_results.json']:
  p=S/n;hs[str(p.relative_to(R))]=hashlib.sha256(p.read_bytes()).hexdigest()
matches={p:hashlib.sha256(subprocess.check_output(['git','-C',str(R),'show','bcba9fc59:'+p])).hexdigest()==h for p,h in hs.items()};assert all(matches.values())
b=R/'sol61_push/cold_final_mile_2026_10_13';p=b/'extra_speed_arrival_2026_10_19/receipt.json';old=json.loads(p.read_text());bp=b/'binary_budget_arrival_2026_10_19/receipt.json';binary=json.loads(bp.read_text());checks=[];rows=[];a=9.3603e-11*3.0857e16/1e6
for r in old['rows']:
 rad=r['radius_pc'];cap=a*rad/13.5;need=r['catalogue_observed_sigma']**2-r['retained_baseline_sigma']**2;shift=next(t for t in binary['rows'] if t['name']==r['name'])['catalogue_sigma_if_fractional_shift_transfers'];needb=shift**2-r['retained_baseline_sigma']**2
 # f=x/(1+x^2) <=1/2 for x>=0 follows (x-1)^2>=0.
 for t in [.01,.1,1,10,100]:
  ok=t/(1+t*t)<=.5;checks.append({'name':r['name']+' dimensionless ceiling '+str(t),'pass':ok});assert ok
 rows.append({'name':r['name'],'ceiling_extra_sigma2_kms2':cap,'needed_extra_sigma2_kms2':need,'needed_IF_binary_transfer':needb,'no_root_current_central':need>cap,'no_root_IF_binary_transfer':needb>cap})
S=next((R/'campaign_fresh_gravity').glob('CFG872*'));d=json.loads((S/'cfg872_results.json').read_text())
for f in ['canonical','alt']:
 x=d[f];checks.append({'name':f+' Draco skipped','pass':'Draco' in x['skipped']});assert checks[-1]['pass']
res={'record':'H-LINK-ceiling-2026-10-20','source_commit':'bcba9fc59','hashes':hs,'committed_matches':matches,'inputs':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest(),str(bp.relative_to(R)):hashlib.sha256(bp.read_bytes()).hexdigest()},'checks':checks,'n_checks':len(checks),'rows':rows,'scope':'Exact algebraic ceiling of declared H-LINK core ansatz, separate prior capped-retained baseline; no observational uncertainty fit, no source bootstrap or likelihood replay'};Path('/private/tmp/ce872_receipt.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'checks':len(checks),'rows':rows}))
