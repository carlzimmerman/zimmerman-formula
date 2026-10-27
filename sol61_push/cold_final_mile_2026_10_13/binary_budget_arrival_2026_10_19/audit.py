from pathlib import Path
import json,math,statistics,hashlib,subprocess,sys
R=Path('/Users/carlzimmerman/new_physics/zimmerman-formula');P=R/'campaign_fresh_gravity/CFG861_classical_dsph_binaries';B=R/'sol61_push/cold_final_mile_2026_10_13';paths=[P/n for n in ['cfg861.py','FROZEN_CRITERIA.md','README.md','cfg861_results.json','cfg861_results_MUTATE.json']]+[B/'run_084/results.json',B/'run_077/results.json'];hashes={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths};src=json.loads(paths[3].read_text());sfh=json.loads(paths[-2].read_text());old=json.loads(paths[-1].read_text());checks=[]
def ck(n,v):
 checks.append({'name':n,'pass':bool(v)})
 if not v:raise AssertionError(n)
for q in src['systems']:
 if q.get('delta') is not None:
  ck(q['name']+' velocity-ratio Delta',abs(q['delta']-2*math.log10(q['sig_clean_M']['sig']/q['sig_single_M']['sig']))<1e-12)
graded=[q for q in src['systems'] if q['name'] in src['graded']['systems']];vals=[q['D_can']+q['delta'] for q in graded];ck('graded mean',abs(statistics.mean(vals)-src['graded']['m'])<1e-12);ck('graded SEM',abs(statistics.stdev(vals)/math.sqrt(len(vals))-src['graded']['s'])<1e-12);ck('mean cleaning shift',abs(statistics.mean(q['delta'] for q in graded)-src['graded']['mean_delta'])<1e-12);ck('source PARTIAL preserved',src['cls']=='PARTIAL')
rows=[]
for name in ['Draco','Sextans','Fornax','Leo I']:
 q=next(q for q in src['systems'] if q['name']==name)
 if name=='Sextans':
  a=next(q for q in old['dwarfs'] if q['name']==name);D=a['Mdyn_in_r12_over_Mb'];settled=a['footings']['canonical']['retained_settled_over_Mb'];f0=a['footings']['canonical']['free_fraction_needed_inside_r12']
 else:
  a=next(q for q in sfh['dwarf_cases'] if q['name']==name)['cases']['primary'];settled=a['settled_over_Mstars'];D=a['additional_cold_over_Mstars']+settled+.512;f0=a['additional_fraction_remaining']
 fnew=(D*10**q['delta']-.512-settled)/(53.64-settled);sig=q['sig_lvd']*10**(q['delta']/2);tau0=-math.log1p(-f0);tau1=-math.log1p(-fnew)
 ck(name+' velocity transfer ratio',abs((sig/q['sig_lvd'])**2-10**q['delta'])<1e-12);ck(name+' positive stock-feasible shifted target',0<fnew<1)
 rows.append({'name':name,'repeat_coverage':q['frac_multi'],'delta_from_same_star_subset':q['delta'],'subset_sigma_single':q['sig_single_M']['sig'],'subset_sigma_clean':q['sig_clean_M']['sig'],'catalogue_sigma_old':q['sig_lvd'],'catalogue_sigma_if_fractional_shift_transfers':sig,'old_remaining_cold_target':f0,'new_remaining_cold_target_IF_shift_transfers':fnew,'max_other_loss_IF_perfect_assembly_and_aperture':1-fnew,'density_requirement_ratio_in_old_constant_kernel_Ndyn_model':(tau1/tau0)**1.5})
ck('sources unchanged',all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in hashes.items()))
res={'record':'CE861-BUDGET-SENSITIVITY-2026-10-19','source_commit':'42b43a572','checks':checks,'n_checks':len(checks),'source_hashes':hashes,'rows':rows,'scope':'Saved like-for-like velocity-ratio and graded-statistic replay; conditional propagation to previous fixed-aperture mass budgets. NOT original spectral/member/epoch reduction or a new global dispersion measurement.','limitations':['Repeated-observation subset footprints and member selection may not represent the global aperture; source itself transfers fractional delta to catalogue','Sextans subset clean7.95 is almost catalogue7.9, but subset single9.56 is higher: applying a multiplicative correction globally is an assumption','Fornax/LeoI repeated fractions only18%/13%; no new radial Jeans fit','Older frozen controls and uncorrected budget records are preserved, not silently replaced','No evidence microscopic transport or cooling mechanism has been solved']};Path('/private/tmp/ce861_budget_audit.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'checks':len(checks),'rows':rows},indent=1))
