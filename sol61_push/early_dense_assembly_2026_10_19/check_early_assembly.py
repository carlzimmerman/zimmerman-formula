"""CE088: ideal cold-cloud assembly exposure, survival, and aperture benchmarks."""
import csv,json,math,sys,resource,platform
from pathlib import Path
B=Path('sol61_push/cold_final_mile_2026_10_13');data=json.loads((B/'run_086_v2/results.json').read_text());cat={r['name']:r for r in csv.DictReader(Path('real_research/data/dsph/lvd_dwarf_mw.csv').open())}
G,MS,PC,YEAR,C=6.674e-11,1.989e30,3.0857e16,365.25*86400,299792458.;unitrho=MS/PC**3;checks=[]
def ck(n,v):
 checks.append({'name':n,'pass':bool(v)})
 if not v:raise AssertionError(n)
rows=[];ref=.1*unitrho
for d in data['dwarfs']:
 name=d['name'];R=d['R_pc']*PC;target=d['target_remaining_cold_fraction'];old=d['cases'][0];M=old['density_Msun_pc3']*unitrho*4*math.pi*(5*R)**3/3
 tau=-math.log1p(-target)
 def cloud(rho):
  re=(3*M/(4*math.pi*rho))**(1/3);s=math.sqrt(G*M/(5*re));td=1/math.sqrt(G*rho);return re,s,td,rho*math.sqrt(6)*s*td
 re,s,td,ex=cloud(ref);bench=[]
 for scm in [.1,1,10]:
  for nd in [1,3,10]:
   req=ref*(tau/(ex*(scm/10)*nd))**1.5;rr,ss,tt,xx=cloud(req);got=-math.expm1(-xx*(scm/10)*nd)
   ck(name+str((scm,nd))+' inversion',abs(got-target)<1e-12)
   ck(name+str((scm,nd))+' virial',abs(5*ss*ss*rr/(G*M)-1)<1e-12)
   bench.append({'sigma_cap_cm2g':scm,'N_dyn':nd,'rho_Msun_pc3':req/unitrho,'R_cloud_pc':rr/PC,'sigma_cloud_kms':ss/1000,'duration_Myr':nd*tt/YEAR/1e6,'cloud_radius_over_present_aperture':rr/R,'virial_binding_fraction_rest':3*G*M/(10*rr*C*C)})
 surv=[]
 for survival in [1,.995,.99,.98,.95]:
  for aperture in [1,.99,.95]:
   product=survival*aperture;f=target/product;feasible=f<1
   ck(name+str((survival,aperture))+' budget ceiling',(f<=1)==(product>=target))
   surv.append({'survival':survival,'aperture_fraction':aperture,'required_assembly_fraction':f,'finite_tau_possible':feasible,'tau_if_possible':-math.log1p(-f) if feasible else None})
 bmax=R*math.sqrt(target**(-2/3)-1)
 ck(name+' Plummer target',abs(R**3/(R*R+bmax*bmax)**1.5-target)<1e-12)
 rows.append({'name':name,'remaining_stock_Msun':M/MS,'target_mass_inside_R_Msun':M/MS*target,'target_fraction':target,'tau_ideal':tau,'max_loss_if_all_other_efficiencies_one':1-target,'reference_rho_Msun_pc3':.1,'reference_N1_sigma1_tau':ex*.1,'benchmarks':bench,'survival_aperture':surv,'maximum_Plummer_scale_pc_if_full_assembly_and_no_loss':bmax/PC})
d={r['name']:r for r in rows};ratios=[]
for name in ['Draco','Sextans']:
 for other in ['Fornax','Leo I']:
  tau_ratio=d[name]['tau_ideal']/d[other]['tau_ideal'];mratio=d[name]['remaining_stock_Msun']/d[other]['remaining_stock_Msun'];required_density_ratio=(tau_ratio/mratio**(1/3))**1.5
  nratio=tau_ratio/mratio**(1/3)
  ck(name+other+' no common density/clock',required_density_ratio>1)
  ratios.append({'target':name,'guard':other,'minimum_density_ratio_for_equal_N_and_constant_sigma_cap':required_density_ratio,'required_N_ratio_at_equal_density_constant_sigma_cap':nratio,'conditional_formation_1plusz_ratio_at_equal_overdensity':required_density_ratio**(1/3)})
# Uniform sphere: vrel~M^(1/3)rho^(1/6), rho*vrel*N/sqrt(G rho)~N M^(1/3)rho^(2/3).
# Independent kernel bound at COMMON density/clock: Maxwellian s~M^(1/3), td same.
# For Msmall<Mlarge, rate_small/rate_large <=(slarge/ssmall)^3=Mlarge/Msmall.
# This can evade the constant-kernel ordering but not necessarily all target ratios.
kernels=[]
for name in ['Draco','Sextans']:
 for other in ['Fornax','Leo I']:
  limit=d[other]['remaining_stock_Msun']/d[name]['remaining_stock_Msun'];req=d[name]['tau_ideal']/d[other]['tau_ideal']
  kernels.append({'target':name,'guard':other,'common_density_Maxwellian_any_shared_velocity_kernel_upper_rate_ratio':limit,'required_rate_ratio':req,'excluded_by_this_bound':req>limit})
# Same-density common constant kernel normalized to capture Sextans' target.
fref=[]
for name in d:
 t=d['Sextans']['tau_ideal']*(d[name]['remaining_stock_Msun']/d['Sextans']['remaining_stock_Msun'])**(1/3)
 fref.append({'name':name,'fraction_if_common_density_clock_constant_kernel_matches_Sextans':-math.expm1(-t)})
ck('matching Sextans overfills both guards',all(x['fraction_if_common_density_clock_constant_kernel_matches_Sextans']>d[x['name']]['target_fraction'] for x in fref if x['name'] in ['Fornax','Leo I']))
res={'claim_id':'CE-FM-088','n_checks':len(checks),'checks':checks,'all_pass':all(c['pass'] for c in checks),'rows':rows,'density_clock_ratios':ratios,'common_density_velocity_kernel_bounds':kernels,'common_density_matching_Sextans':fref,'observed_peak_rss':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'rss_units':'bytes on Darwin; KiB on Linux','platform':platform.system(),'assertion_tested':'Conditional uniform self-gravitating cold sphere: virial s²=GM/(5R), tdyn=(G rho)^-1/2, constant rho during N tdyn, effective one-hit irreversible capture with Poisson probability, no initial protected seed; finite stock survival and Plummer aperture ceilings.','non_claims':['No fragment dissipation/radiation rate derived: sigma_capture is an assumed successful capture cross section, not geometric area','A dense initial cloud already assumes assembly of the full finite stock, not its physical production or delivery','Cold self-gravity and initial virialization are assumptions, baryons/tides/expansion omitted','Early densities, durations, redshifts and velocity distributions are not measured','No full evolving halo solution, observational uncertainty fit or frozen criterion repair','Sextans Upsilon2 and unchanged inventory remain conditional']}
Path(sys.argv[1]).write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'checks':len(checks),'density_ratios':ratios,'kernel_bounds':kernels,'sigma1_N1':[dict(name=x['name'],**next(v for v in x['benchmarks'] if v['sigma_cap_cm2g']==1 and v['N_dyn']==1)) for x in rows],'matching_Sextans':fref},indent=2))
