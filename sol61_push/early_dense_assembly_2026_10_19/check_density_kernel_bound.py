"""CE088B: independent mass reconstruction and general unequal-density kernel bound."""
import math,json,csv,sys
from pathlib import Path
b=Path('sol61_push/early_dense_assembly_2026_10_19');r=json.loads((b/'run_001/results.json').read_text());d={x['name']:x for x in r['rows']};inp=json.loads(Path('sol61_push/cold_final_mile_2026_10_13/run_086_v2/results.json').read_text());cat={x['name']:x for x in csv.DictReader(open('real_research/data/dsph/lvd_dwarf_mw.csv'))};G,MS,PC=6.674e-11,1.989e30,3.0857e16;checks=[];rows=[]
def ck(n,v):
 checks.append({'name':n,'pass':bool(v)})
 if not v:raise AssertionError(n)
for x in inp['dwarfs']:
 n=x['name'];m=x['ups']*10**(.4*(4.83-float(cat[n]['M_V'])));radius=x['R_pc']*PC;y=G*.512*m*MS/radius**2/9.3603e-11;settled=min(.512*(math.sqrt(.25+1/y)-.5),5.364);M=(53.64-settled)*m
 ck(n+' independent remaining mass',abs(M/d[n]['remaining_stock_Msun']-1)<1e-12)
for n in ['Draco','Sextans']:
 for other in ['Fornax','Leo I']:
  massratio=d[other]['remaining_stock_Msun']/d[n]['remaining_stock_Msun'];required=d[n]['tau_ideal']/d[other]['tau_ideal'];crit=massratio**2;ndmin=required/massratio
  ck(n+other+' fixed Ndyn fails when target colder',ndmin>1)
  for density_ratio in [.01,1,10,crit]:
   sratio=(1/massratio)**(1/3)*density_ratio**(1/6)
   clock_ratio=density_ratio**-.5
   prefactor=density_ratio*clock_ratio/sratio**3
   ck(n+other+str(density_ratio)+' cancellation',abs(prefactor/massratio-1)<1e-12)
   ck(n+other+str(density_ratio)+' target no hotter branch',sratio<1+1e-12)
  rows.append({'target':n,'guard':other,'density_ratio_above_which_target_becomes_hotter':crit,'necessary_N_target_over_N_guard_if_target_no_hotter_for_any_common_velocity_kernel':ndmin,'same_N_necessary_alternative':'density ratio must exceed critical value; necessary only, not sufficient'})
sx=d['Sextans'];target=sx['target_fraction'];R=next(x['R_pc'] for x in inp['dwarfs'] if x['name']=='Sextans');cap=[]
for survival in [1,.995,.99,.98]:
 if survival>target:
  a=target/survival;bmax=R*math.sqrt(a**(-2/3)-1);tau=-math.log1p(-a)
  ck('Sextans surviving Plummer '+str(survival),abs(survival*R**3/(R*R+bmax*bmax)**1.5-target)<1e-12)
  cap.append({'survival':survival,'minimum_capture_fraction_if_aperture_one':a,'required_tau_if_aperture_one':tau,'max_final_Plummer_scale_pc_if_capture_one':bmax})
 else:cap.append({'survival':survival,'impossible_even_if_full_capture_and_full_aperture':True})
out={'claim_id':'CE-FM-088B','n_checks':len(checks),'all_pass':all(x['pass'] for x in checks),'checks':checks,'kernel_bounds':rows,'Sextans_survival_aperture':cap,'proof':'For equal-mass fragments with common nonnegative velocity-only capture kernel, Maxwellian sd<=sf gives rate ratio <=(rho_d/rho_f)(sf/sd)^3. Uniform self-gravitating spheres have sd/sf=(Md/Mf)^(1/3)(rho_d/rho_f)^(1/6); durations Nd/sqrt(G rho_d) give optical-depth ratio <=(Nd/Nf)(Mf/Md). Density cancels until sd>sf, occurring at rho_d/rho_f>(Mf/Md)^2. Bound is necessary only; violating cold ordering removes this bound but does not prove capture.','non_claims':['No density or clock history derived from primordial physics','No Maxwellian cold state or common capture kernel inferred from actual ARGON action','Targets remain conditional on stellar mass, retained stock and zero other free contribution']};Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'checks':len(checks),'kernel_bounds':rows,'Sextans':cap},indent=2))
