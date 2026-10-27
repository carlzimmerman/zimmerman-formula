from pathlib import Path
import json,hashlib,subprocess,math
R=Path('/Users/carlzimmerman/new_physics/zimmerman-formula');S=R/'campaign_fresh_gravity/CFG857_extra_speed_size';B=R/'sol61_push/cold_final_mile_2026_10_13';names=['cfg857.py','FROZEN_CRITERIA.md','README.md','cfg857_results.json','cfg857_results_MUTATE.json'];hashes={str((S/n).relative_to(R)):hashlib.sha256((S/n).read_bytes()).hexdigest() for n in names};matches={p:hashlib.sha256(subprocess.check_output(['git','-C',str(R),'show','18a81657e:'+p])).hexdigest()==h for p,h in hashes.items()};assert all(matches.values())
a=json.loads((S/'cfg857_results.json').read_text());m=json.loads((S/'cfg857_results_MUTATE.json').read_text());p=B/'extra_speed_arrival_2026_10_19/receipt.json';old=json.loads(p.read_text());checks=[]
def ck(n,v):
 checks.append({'name':n,'pass':bool(v)});assert v,n
for foot in ['canonical','alt']:
 x=a[foot];ck(foot+' slope below two sigma',abs(x['beta'])<2*x['sbeta']);ck(foot+' offset remains',abs(x['host_offset'])>=2*x['s_host']);ck(foot+' SPARC gate',abs(x['sparc_D'])<.05 and abs(x['sparc_D'])<=2*x['sparc_sD']);ck(foot+' saved class',x['cls']=='NO SIZE DEPENDENCE')
ck('canonical shuffle control passes',abs(m['canonical']['beta'])<2*m['canonical']['sbeta']);ck('alt shuffle control fails',abs(m['alt']['beta'])>=2*m['alt']['sbeta'])
rows=[];x=a['canonical']
for r in old['rows']:
 v=x['V0']*(r['radius_pc']/300)**x['beta'];s=math.sqrt(r['retained_baseline_sigma']**2+v*v/3);rows.append({'name':r['name'],'radius_pc':r['radius_pc'],'fitted_Vx_kms':v,'predicted_sigma_kms':s,'catalogue_sigma_kms':r['catalogue_observed_sigma']})
D,F=[next(r for r in rows if r['name']==n) for n in ['Draco','Fornax']];ck('size fit gives Draco smaller extra speed than Fornax',D['fitted_Vx_kms']<F['fitted_Vx_kms'])
res={'record':'CFG857-arrival-audit-2026-10-19','source_commit':'18a81657e','criteria_commit':'588cea002','format':'custom stdlib audit, not v2 manifest','source_hashes':hashes,'committed_matches':matches,'prior_receipt_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'checks':checks,'n_checks':len(checks),'rows':rows,'scope':'Saved gates and conditional capped-retained aperture bridge only; no raw regression/bootstrap/SPARC reconstruction, no uncertainty/Jeans fit. Source full exponential baseline differs from bridge. No formation mechanism.'};Path('/private/tmp/ce857_receipt.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
