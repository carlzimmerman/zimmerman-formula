"""CE086: conditional encounter selectivity and Kepler cooling benchmarks; no PDE evolution."""
import csv,json,math,sys,resource,platform
from pathlib import Path
B=Path('sol61_push/cold_final_mile_2026_10_13');G=6.674e-11;MS=1.989e30;PC=3.0857e16;C0=299792458.;T=10e9*365.25*86400
sfh=json.loads((B/'run_084/results.json').read_text());old=json.loads((B/'run_077/results.json').read_text());frag=json.loads(Path('argon_push/ARGON11_nonlinear_fragmentation_2026-10-17/argon11_results.json').read_text());cat={r['name']:r for r in csv.DictReader(Path('real_research/data/dsph/lvd_dwarf_mw.csv').open())};checks=[]
def ck(n,v):
 checks.append({'name':n,'pass':bool(v)})
 if not v:raise AssertionError(n)
rows=[]
for name in ['Draco','Sextans','Fornax','Leo I']:
 c=cat[name];r=4/3*float(c.get('rhalf_sph_physical') or c['rhalf_physical'])*PC
 if name=='Sextans':
  a=next(x for x in old['dwarfs'] if x['name']==name);u=2;sig=a['sigma_obs_kms'];settled=a['footings']['canonical']['retained_settled_over_Mb'];f=a['footings']['canonical']['free_fraction_needed_inside_r12']
 else:
  a=next(x for x in sfh['dwarf_cases'] if x['name']==name)['cases']['primary'];u=a['ups'];sig=a['obs'];settled=a['settled_over_Mstars'];f=a['additional_fraction_remaining']
 m=u*10**(.4*(4.83-float(c['M_V'])));reservoir=(53.64-settled)*m*MS;v=math.sqrt(6)*sig*1000;cases=[]
 for k in [5,10,20]:
  f0=k**-3; tau=math.log((1-f0)/(1-f)); ck(name+str(k)+' initial fraction below target',0<f0<f<1)
  rho=3*reservoir/(4*math.pi*(k*r)**3);exposure=rho*v*T # kg/m^2; sigma/m units m²/kg, x10 to cm²/g
  scm=10*tau/exposure
  de=1.5*(sig*1000)**2*(1-1/k);dj=1-1/math.sqrt(k)
  ck(name+str(k)+' probability inverse',abs(f0+(1-f0)*(-math.expm1(-exposure*scm/10))-f)<1e-12)
  ck(name+str(k)+' Kepler energy balance',abs((-1.5*(sig*1000)**2/k)-de-(-1.5*(sig*1000)**2))<1e-7)
  cases.append({'initial_radius_over_aperture':k,'initial_fraction_inside_aperture':f0,'tau_target':tau,'density_Msun_pc3':rho/(MS/PC**3),'target_capture_cross_section_cm2g':scm,'final_fraction_if_sigma_cap_1cm2g':f0+(1-f0)*(-math.expm1(-exposure/10)),'energy_loss_J_per_kg_to_circular_R':de,'energy_loss_fraction_rest':de/C0**2,'specific_angular_momentum_fraction_to_remove':dj,'exposure_kg_m2':exposure})
 rows.append({'name':name,'ups':u,'R_pc':r/PC,'sigma_obs_kms':sig,'target_remaining_cold_fraction':f,'cases':cases})
comparisons=[]
for kidx in range(3):
 d={x['name']:x['cases'][kidx]['target_capture_cross_section_cm2g'] for x in rows};lo=max(d[n] for n in ['Draco','Sextans']);hi=min(d[n] for n in ['Fornax','Leo I']);ck('common constant sigma infeasible '+str(kidx),lo>hi)
 comparisons.append({'k':rows[0]['cases'][kidx]['initial_radius_over_aperture'],'required_sigma_cap_lower_Draco_Sextans':lo,'allowed_sigma_cap_upper_Fornax_LeoI':hi,'required_selectivity_Sextans_over_Fornax':d['Sextans']/d['Fornax'],'required_selectivity_Draco_over_Fornax':d['Draco']/d['Fornax']})
# Radiation diagnostic scales: equal masses in their CM frame, each speed v_rel/2.
# K_rel/(total rest mass*c²)=v_rel²/(8c²); relative speed chosen RMS=sqrt(6)*sigma.
diag=[]
for x in rows:
 e=(math.sqrt(6)*x['sigma_obs_kms']*1000/C0)**2/8
 diag.append({'name':x['name'],'pair_CM_orbital_energy_over_rest':e,'global_H_drift_R1_over_pair_kinetic_fraction':frag['R1']['K1']['dE']/e})
# Momentum-conserving capture by merger into an initially stationary equal mass at escape speed ve.
# COM final speed v/2; v²=vinf²+ve² -> bound iff vinf²<3ve².
for z in [.5,1,1.7,1.8,5,10]:ck('equal mass merger capture threshold '+str(z),((math.sqrt(1+z*z)/2)<1)==(z*z<3))
# Newtonian circular-orbit contraction needs a torque in addition to energy export.
ck('five radius contraction angular loss',1-1/math.sqrt(5)>.55)
r={'claim_id':'CE-FM-086','n_checks':len(checks),'checks':checks,'all_pass':all(x['pass'] for x in checks),'dwarfs':rows,'common_sigma_comparisons':comparisons,'radiation_diagnostic':diag,'observed_peak_rss_raw':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'peak_rss_units':'bytes on Darwin; KiB on Linux','platform':platform.system(),'assertion_tested':'Ideal one-successful-hit Poisson capture in static homogeneous homologous reservoirs for k=5,10,20 over10Gyr, using cold RMS speed=sqrt(6)*stellar sigma, plus fixed-Kepler circular contraction and momentum benchmarks.','non_claims':['No measured sigma_capture, radiation kernel, physical initial radius, cold velocity distribution, density evolution or full halo solve','Target fractions from retained-only aperture budget; existing free profiles not recomputed','Encounter optical depth is not a rigorous cooling-time bound for evolving self-gravitating halos','No universal no-go for velocity-dependent collisions or different assembly histories','Geometric cross section is not capture/transport cross section','Sextans M/L=2 and total inventory53.64 are assumptions, not new measurements']}
Path(sys.argv[1]).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'checks':len(checks),'comparisons':comparisons,'diagnostic':diag,'k5_rows':[dict(name=x['name'],f=x['target_remaining_cold_fraction'],**x['cases'][0]) for x in rows]},indent=2))
