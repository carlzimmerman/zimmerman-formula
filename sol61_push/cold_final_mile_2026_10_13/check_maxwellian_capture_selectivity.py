"""Exact pointwise relative-speed kernel bound plus finite arithmetic checks."""
import json,math,sys
from pathlib import Path
b=Path('sol61_push/cold_final_mile_2026_10_13');r=json.loads((b/'run_086_v2/results.json').read_text());d={x['name']:x for x in r['dwarfs']};checks=[];rows=[]
def ck(n,v):
 checks.append({'name':n,'pass':bool(v)})
 if not v:raise AssertionError(n)
for i,k in enumerate([5,10,20]):
 F=d['Fornax'];fc=F['cases'][i]
 for name in ['Draco','Sextans']:
  D=d[name];dc=D['cases'][i];sd=D['sigma_obs_kms'];sf=F['sigma_obs_kms'];ck(name+' narrower speed distribution',sd<sf)
  # p_rel(v|s)=v² exp[-v²/(4s²)]/(2 sqrt(pi) s³).
  # Multiplication by ANY shared nonnegative kernel preserves pointwise bound.
  bnd=dc['density_Msun_pc3']/fc['density_Msun_pc3']*(sf/sd)**3
  required=dc['tau_target']/fc['tau_target'];ck(name+str(k)+' universal common-kernel bound fails target',required>bnd)
  for v in [0,.1,1,5,10,20,50,100,200]:
   ratio=(sf/sd)**3*math.exp(-v*v/4*(1/sd**2-1/sf**2));ck(name+str(k)+' pointwise '+str(v),ratio<=(sf/sd)**3*(1+1e-14))
  rows.append({'name':name,'k':k,'required_encounter_rate_ratio_vs_Fornax':required,'upper_bound_for_any_shared_nonnegative_velocity_kernel':bnd,'needed_extra_density_time_or_nonshared_kernel_factor':required/bnd})
out={'claim_id':'CE-FM-086B','n_checks':len(checks),'all_pass':all(x['pass'] for x in checks),'checks':checks,'rows':rows,'proof':'p_rel(v|sd)/p_rel(v|sf)=(sf/sd)^3 exp[-v²(1/sd²-1/sf²)/4] <= (sf/sd)^3 for sd<sf. Integrate against common nonnegative sigma_cap(v)*v and multiply by rho_d/rho_f. Applies to all such kernels with finite integrals, not just the tested speeds.','hypotheses':['Isotropic centered Maxwellian velocities with cold 1D dispersion equal observed stars','Static homogeneous reservoirs with common outer radius/aperture ratio and10Gyr duration','One successful hit deposits mass; initial aperture fraction accounted for','Same velocity-only capture cross section per mass, same fragment population; no potential-dependent branching or environmental selection'],'non_claims':['Does not exclude different cold velocity DFs, time-dependent density histories, potential-dependent capture, primordial compact assembly or a different inventory','No actual microscopic radiated energy or collision solution']}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'checks':len(checks),'rows':rows},indent=2))
