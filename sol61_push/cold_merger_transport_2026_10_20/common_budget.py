"""Shared hypothetical binding-release budget; not a merger or evolution model."""
from pathlib import Path
import json,math,sys,resource
from scipy.integrate import quad
from scipy.optimize import brentq
R=Path(__file__).resolve().parents[2];B=Path(__file__).resolve().parent
p=json.loads((R/'sol61_push/cold_collision_outflow_2026_10_20/run_001/results.json').read_text());d=json.loads((R/'campaign_fresh_gravity/CFG918_dwarf_receiver_capacity/cfg918_results.json').read_text());proj=json.loads((R/'sol61_push/cold_endpoint_projection_2026_10_20/run_002/results.json').read_text());bind=json.loads((B/'isolated_binding/run_002/results.json').read_text());old=json.loads((B/'run_001/results.json').read_text())
G=d['constants']['G'];c=299792.458;beta_gap=bind['incremental_release_fraction_of_initial_two_profile_energy'];checks=[];rows=[]
def ck(name,cond):checks.append({'name':name,'pass':bool(cond)});assert cond,name
fac=quad(lambda t:.5*math.sin(t)**2,0,math.pi,epsabs=1e-12)[0]
ck('uniform spherical constant-momentum tangential J factor',abs(fac-math.pi/4)<1e-12)
for t in p['targets']:
 n=t['name'];b=d['results']['canonical']['B0'][n]['base'];s=next(r for r in proj['rows'] if r['name']==n);o=next(r for r in old['rows'] if r['name']==n);M=t['initial_mass_Msun'];m0=t['wind_mass_Msun'];K0=M*t['required_energy_per_mass'];J=M*t['required_J_per_mass'];Rc=b['R'];rA=s['endpoint_rA_pc'];rB=s['endpoint_rB_pc'];mA=t['bound_receiver_mass_Msun']
 phi=lambda r:-G*b['Ms']/math.sqrt(r*r+b['a']**2)-G*(b['s']*b['Ms']+b['Mx'])/r-G*mA/max(r,rA)
 Eorb=K0+m0*phi(rB)-G*m0*m0/(2*rB)
 # Independent analytic uniqueness check for the eta threshold reported by run_001.
 pp=J/Rc;qq=pp/c;gg=G/(2*Rc)
 F=lambda m:pp*pp/(math.sqrt(m*m+qq*qq)+m)
 N=lambda m:F(m)-Eorb+m*phi(Rc)-gg*m*m
 Np=lambda m:-c*c*qq*qq/(math.sqrt(m*m+qq*qq)*(math.sqrt(m*m+qq*qq)+m))+phi(Rc)-2*gg*m
 Npp_lower=c*c*qq*qq/(m0*m0+qq*qq)**1.5-2*gg
 DD=lambda m:Np(m)*(m0-m)+N(m)
 ck(n+' strict convex threshold numerator',Npp_lower>0 and N(m0)>0 and DD(0)<0<DD(m0))
 mm=brentq(DD,0,m0,xtol=1e-7,rtol=1e-13);eta=N(mm)/((m0-mm)*c*c)
 ck(n+' unique efficiency minimum agrees independent stationary root',abs(eta/o['binding_defect_ideal_wind_branch']['ideal_orbital_efficiency_threshold_if_any_rest_defect_allowed']-1)<1e-7)
 ideal=o['binding_defect_ideal_wind_branch']['delta_rest_mass_Msun'];processed=ideal/beta_gap
 out={'name':n,'branch_gap_fraction':beta_gap,'ideal_processed_fragment_mass_for_prior_lower_bound_Msun':processed,'ideal_processed_fraction_of_initial_free_mass_for_prior_lower_bound':processed/M,'shared_release_scan':[]}
 for eps in [1e-8,1e-7,1e-6,2e-6,1e-5]:
  dm=eps*M;m=m0-dm;valid=m>0
  if not valid:out['shared_release_scan'].append({'epsilon_rest_defect_per_initial_free_mass':eps,'mass_budget_pass':False});continue
  KR=Eorb-m*phi(Rc)+G*m*m/(2*Rc)+dm*c*c
  KB=Eorb-m*phi(rB)+G*m*m/(2*rB)+dm*c*c
  P=math.sqrt(2*m*KR+KR*KR/(c*c));Jmax=fac*Rc*P;need=J/Jmax
  oldglob=s['apertures']['global']['sigma_stars_kms']**2;Bvar=s['apertures']['global']['sigma2_contributions_kms2']['B'];newglob=oldglob-Bvar*dm/m0
  u=KR/(m*c*c);speed=c*math.sqrt(u*(2+u))/(1+u)
  ck(n+' common epsilon '+str(eps)+' rest/energy allocation',abs((b['Mx']+mA+m+dm)/M-1)<1e-12 and abs((KR+m*phi(Rc)-G*m*m/(2*Rc)-(Eorb+dm*c*c)))/max(KR,1)<1e-12)
  ck(n+' common epsilon '+str(eps)+' static stellar gravity does not increase',newglob<=oldglob)
  out['shared_release_scan'].append({'epsilon_rest_defect_per_initial_free_mass':eps,'rest_defect_Msun':dm,'new_wind_rest_mass_Msun':m,'mass_budget_pass':True,'orbital_J_capacity_pass_at_core':need<=1,'required_tangential_momentum_fraction_of_uniform_spherical_launch':need,'wind_speed_at_core_kms':speed,'new_outer_wind_K_over_old':KB/K0,'processed_fraction_if_stationary_gap_fully_available_and_to_wind':eps/beta_gap,'static_global_sigma_with_reduced_outer_wind_mass_kms':math.sqrt(newglob),'stellar_heat_assumed_zero':True})
 rows.append(out)
allpass=[]
for eps in [1e-8,1e-7,1e-6,2e-6,1e-5]:
 allpass.append({'epsilon':eps,'all_four_budget_and_spherical_launch_J_gates':all(next(a for a in x['shared_release_scan'] if a['epsilon_rest_defect_per_initial_free_mass']==eps).get('orbital_J_capacity_pass_at_core',False) for x in rows)})
res={'checks':checks,'n_checks':len(checks),'rows':rows,'common_scan':allpass,'peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'scope':'Post-hoc exploratory energy-budget example only. Same epsilon per initial free rest mass in all four, fixed core/A profiles, compensating rest/charge allocation assumed, full release goes to selected wind, zero stellar heating. Spherical launch moment factorpi/4; later spherical propagation/self-energy remains an assumed closure, not a trajectory. Static old aperture/stock failures unresolved. Actual merger processing, phase average, torque, Q and release branching unmeasured.'};assert res['peak_rss_bytes_macos']<1_000_000_000;Path(sys.argv[1]).write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'checks':len(checks),'common_scan':allpass,'ideal_Sextans_processed_mass_Msun':rows[1]['ideal_processed_fragment_mass_for_prior_lower_bound_Msun']},indent=2))
