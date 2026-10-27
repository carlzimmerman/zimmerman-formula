from pathlib import Path
import json,math,hashlib,subprocess
R=Path('/Users/carlzimmerman/new_physics/zimmerman-formula');S=R/'campaign_fresh_gravity/CFG856_universal_extra_speed';B=R/'sol61_push/cold_final_mile_2026_10_13';paths=[S/n for n in ['cfg856.py','FROZEN_CRITERIA.md','README.md','cfg856_results.json','cfg856_results_MUTATE.json']]+[B/'run_084/results.json',B/'run_077/results.json',B/'binary_budget_arrival_2026_10_19/receipt.json'];hashes={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths};src=json.loads(paths[3].read_text());sfh=json.loads(paths[-3].read_text());old=json.loads(paths[-2].read_text());binary=json.loads(paths[-1].read_text());checks=[]
def ck(n,v):
 checks.append({'name':n,'pass':bool(v)})
 if not v:raise AssertionError(n)
for foot in ['canonical','alt']:
 a=src[foot];ck(foot+' amplitude log',abs(math.log10(a['Vx0_kms'])-a['lV0'])<1e-12);ck(foot+' P3 gate',bool(a['P3'])==(abs(a['D'])<.05 and abs(a['D'])<=2*a['sD']));ck(foot+' M31 failure',abs(a['z_m31'])>2 and not a['P1']);ck(foot+' source class',a['cls']=='SPARC-COMPATIBLE ONLY')
V=src['canonical']['Vx0_kms'];rows=[]
for name in ['Draco','Sextans','Fornax','Leo I']:
 if name=='Sextans':
  a=next(x for x in old['dwarfs'] if x['name']==name);s0=a['footings']['canonical']['optimistic_no_free_sigma_kms'];obs=a['sigma_obs_kms'];rad=a['r12_pc']
 else:
  a=next(x for x in sfh['dwarf_cases'] if x['name']==name)['cases']['primary'];s0=a['baseline_sigma'];obs=a['obs'];rad=next(x for x in old['dwarfs'] if x['name']==name)['r12_pc']
 obs_shift=next(x for x in binary['rows'] if x['name']==name)['catalogue_sigma_if_fractional_shift_transfers'];pred=math.sqrt(s0*s0+V*V/3);need=math.sqrt(3*(obs*obs-s0*s0));need_shift=math.sqrt(3*(obs_shift*obs_shift-s0*s0));ck(name+' estimator identity',abs((pred*pred-s0*s0)*3/V**2-1)<1e-12)
 rows.append({'name':name,'retained_baseline_sigma':s0,'predicted_sigma_with_flat_Vx':pred,'catalogue_observed_sigma':obs,'required_Vx':need,'required_Vx_IF_binary_shift_transfers':need_shift,'radius_pc':rad,'flat_component_enclosed_mass_Msun':V*V*rad/4.30071e-3})
# Specific cored isothermal density rho=Vinf²/[4piG(rc²+r²)]:
# Vc²/Vinf²=1-atan(x)/x, 0<factor<1. Core cannot increase this family's boost.
for x in [.001,.01,.1,1,10,100]:ck('specified cored family upper bound '+str(x),0<1-math.atan(x)/x<1)
ck('Draco still requires larger amplitude after conditional binary shift',next(x for x in rows if x['name']=='Draco')['required_Vx_IF_binary_shift_transfers']>V)
ck('inputs unchanged',all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in hashes.items()))
res={'record':'CE856-CORE-CHECK-2026-10-19','source_commit':'79f873430','n_checks':len(checks),'checks':checks,'source_hashes':hashes,'Vx_canonical':V,'rows':rows,'scope':'Saved class/amplitude arithmetic and conditional aperture-estimator consequences against prior SFH/capped-retained budgets. No raw SPARC/bootstrap/calibration sample reconstruction or observational uncertainty fit.','non_claims':['Source uses full exponential-law baseline, our comparison uses capped rational retained baseline: this is a separate exploratory bridge, not a regrade','Finite-core upper bound applies only to explicitly stated density family or Vc<=Vflat, not all possible cores','Binary-shift branch is conditional, not new global measured dispersions','9.4km/s is fitted; neither temperature, core size, E/J export nor finite truncation is derived','No physical formation mechanism or all-dwarf fit established']};res['receipt_format']='custom bounded stdlib audit; not a v2 experiment manifest';res['committed_source_hash_matches']={p:hashlib.sha256(subprocess.check_output(['git','-C',str(R),'show','79f873430:'+p])).hexdigest()==h for p,h in hashes.items() if p.startswith('campaign_fresh_gravity/')};assert all(res['committed_source_hash_matches'].values());Path('/private/tmp/ce856_core_check.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'checks':len(checks),'Vx':V,'rows':rows},indent=1))
