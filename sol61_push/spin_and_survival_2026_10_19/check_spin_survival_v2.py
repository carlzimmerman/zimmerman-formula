"""CE089: conditional angular-momentum barrier, energy receiver, and tidal survival."""
from pathlib import Path
import json,math,sys,resource
B=Path('sol61_push');early=json.loads((B/'early_dense_assembly_2026_10_19/run_001/results.json').read_text());old=json.loads((B/'cold_final_mile_2026_10_13/run_086_v2/results.json').read_text());d={r['name']:r for r in early['rows']};obs={r['name']:r for r in old['dwarfs']}
G,MS,PC,A0,YEAR=6.674e-11,1.989e30,3.0857e16,9.3603e-11,365.25*86400;U=MS/PC**3;checks=[]
def ck(n,v):
 checks.append({'name':n,'pass':bool(v)})
 if not v:raise AssertionError(n)
# Uniform virial sphere W=-3GM²/(5R), E=W/2, I=2MR²/5.
# Trot >= J²/(2I), Trot<=|W|/2 -> R>=25 J²/(6GM³).
# lambda=J sqrt(|Ei|)/(GM^(5/2)); Rmin/Ri=(125/9) lambda².
alpha=125/9;q=2; thermal_fraction=1-1/q; density_correction=thermal_fraction**(-.75);lammax=math.sqrt(9/(125*q));spin=[]
for guard_spin in [.05,.1,.18,lammax]:
 ref=next(v for v in d['Fornax']['benchmarks'] if v['sigma_cap_cm2g']==1 and v['N_dyn']==1);rhoF=ref['rho_Msun_pc3']*density_correction;rhoi=rhoF*(q*alpha*guard_spin**2)**3;td=1/math.sqrt(G*rhoi*U)/YEAR/1e6;values=[]
 for name in d:
  re=next(v for v in d[name]['benchmarks'] if v['sigma_cap_cm2g']==1 and v['N_dyn']==1);lam=guard_spin*(rhoF/(re['rho_Msun_pc3']*density_correction))**(1/6);contraction=q*alpha*lam**2;M=d[name]['remaining_stock_Msun']*MS;Ri=(3*M/(4*math.pi*rhoi*U))**(1/3);Rf=contraction*Ri
  ck(name+str(guard_spin)+' density spin match',abs(rhoi/contraction**3/(re['rho_Msun_pc3']*density_correction)-1)<1e-12)
  J=lam*G*M**2.5/math.sqrt(.3*G*M*M/Ri);I=.4*M*Rf*Rf;W=.6*G*M*M/Rf
  ck(name+str(guard_spin)+' rotational share',abs((J*J/(2*I))/(W/2)-1/q)<1e-12)
  values.append({'name':name,'lambda_required':lam,'initial_radius_pc':Ri/PC,'final_cloud_radius_pc':Rf/PC,'rotational_floor_pc':Rf/(q*PC),'rho_final_Msun_pc3':re['rho_Msun_pc3']*density_correction,'random_kinetic_fraction':thermal_fraction})
 spin.append({'lambda_Fornax':guard_spin,'common_initial_density_Msun_pc3':rhoi,'initial_dynamical_time_Myr':td,'values':values})
# Isolated energy endpoint: initial uniform virial cloud at5 present apertures;
# final uniform virial core fM at benchmark Rc. Remaining mass energy at infinity
# assigned to eps M ejecta; this is an existence budget, not a collision history.
energy=[]
for name in ['Draco','Sextans']:
 x=d[name];M=x['remaining_stock_Msun']*MS;f=x['target_fraction'];Ri=5*obs[name]['R_pc']*PC;Rc=next(v for v in x['benchmarks'] if v['sigma_cap_cm2g']==1 and v['N_dyn']==1)['R_cloud_pc']*PC;Ei=-.3*G*M*M/Ri;Ef=-.3*G*(f*M)**2/Rc;release=Ei-Ef
 for eps in [.001,.005,.01,1-f]:
  if eps>1-f+1e-14:continue
  speed=math.sqrt(2*release/(eps*M)) if release>0 else None
  if speed is not None:ck(name+str(eps)+' energy endpoint',abs((Ef+.5*eps*M*speed**2-Ei)/Ei)<1e-12)
  energy.append({'name':name,'initial_radius_pc':Ri/PC,'core_mass_fraction':f,'core_radius_pc':Rc/PC,'ejected_fraction_of_initial_stock':eps,'remaining_noncore_fraction_assigned_zero_energy_at_infinity':1-f-eps,'energy_export_J':release,'ejecta_speed_at_infinity_kms_if_only_receiver':speed/1000 if speed is not None else None})
# Cold-only Plummer truncated at circularized Jacobi radius in prescribed host.
# Host uses exponential isolated law; internal compact cold self-gravity Newtonian.
# T=Omega²-Phi''=(g/Rp)[3-s/(exp(s)-1)], s=sqrt(G Mb/a0)/Rp.
# Mbound=M F(rt), rt³=G Mbound/T -> rt=sqrt[(GM/T)^(2/3)-b²].
x=d['Sextans'];M=x['remaining_stock_Msun']*MS;R=obs['Sextans']['R_pc']*PC;target=x['target_fraction'];tidal=[]
def F(r,b):return r**3/(r*r+b*b)**1.5 if r>0 else 0.
for host in [6e10,8e10]:
 for peri in [5,10,20,50,100]:
  rp=peri*1000*PC;s=math.sqrt(G*host*MS/A0)/rp;gn=G*host*MS/rp**2;g=gn/(-math.expm1(-s));T=g/rp*(3-s/math.expm1(s));rj=(G*M/T)**(1/3)
  for bpc in [10,20,25,40,56.898628039976664]:
   b=bpc*PC;rt=math.sqrt(max(0,rj*rj-b*b));surv=F(rt,b);inner=F(min(R,rt),b);postA=inner/surv if surv else 0.
   ck(str((host,peri,bpc))+' truncation mass partition',abs(surv*postA-inner)<1e-14)
   if rt>0:ck(str((host,peri,bpc))+' implicit Jacobi mass',abs(rt**3*T/(G*M*surv)-1)<1e-12)
   tidal.append({'host_Msun':host,'peri_kpc_assumed_not_measured':peri,'b_pc':bpc,'rj_point_pc':rj/PC,'rt_pc':rt/PC,'survival':surv,'post_truncation_aperture_fraction':postA,'stock_fraction_left_inside_R':inner,'enough_inner_mass':inner>=target-1e-12})
# For rt>R, removing ONLY outer material leaves inner mass unchanged.
ck('outer stripping does not remove interior mass',all(abs(t['stock_fraction_left_inside_R']-F(R,t['b_pc']*PC))<1e-13 for t in tidal if t['rt_pc']>R/PC))
# Same initial spin/density gives the same final density -> does not select dwarfs.
ratios={name:(next(z for z in d[name]['benchmarks'] if z['sigma_cap_cm2g']==1 and z['N_dyn']==1)['rho_Msun_pc3']/next(z for z in d['Fornax']['benchmarks'] if z['sigma_cap_cm2g']==1 and z['N_dyn']==1)['rho_Msun_pc3'])**(1/6) for name in ['Draco','Sextans','Leo I']}
out={'claim_id':'CE-FM-089','n_checks':len(checks),'all_pass':all(x['pass'] for x in checks),'checks':checks,'lambda_Fornax_over_lambda_dwarf':ratios,'q_Rfinal_over_Rrotation_floor':q,'capture_density_correction_for_random_speed':density_correction,'spin_scenarios':spin,'energy_receiver':energy,'tidal_scenarios':tidal,'peak_rss_raw':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'assertion_tested':'Uniform rotating virial-sphere with half rotational and half random kinetic energy, adjusted ideal capture density; isolated energy-endpoint ejection budgets, and static self-consistent Plummer Jacobi truncation for Sextans in prescribed host fields.','non_claims':['No prediction or measurement of original cold-spin or initial density','Rotation floor is necessary, not sufficient: shape, pressure, differential rotation and instability omitted','No demonstrated cooling/torque or gravothermal capture rate; energy endpoint not dynamical trajectory','Jacobi circular-orbit tidal approximation at assumed pericentres, not actual Sextans orbit or time-dependent shocks','No stellar kinematic profile fit or full framework internal force law','All inherited stellar/cold inventories remain conditional']}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'checks':len(checks),'spin_ratios':ratios,'spin_scenarios':spin,'energy_Sextans':[z for z in energy if z['name']=='Sextans'],'tidal_b25':[z for z in tidal if z['b_pc']==25 and z['host_Msun']==6e10]},indent=1))
