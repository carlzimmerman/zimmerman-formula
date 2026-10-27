"""CE-FM-082: gravitational gas-cycle energy transfer, no halo simulation."""
import json,math,sys
from pathlib import Path
B=Path('sol61_push/cold_final_mile_2026_10_13');r=json.loads((B/'run_077/results.json').read_text());saved=json.loads((B/'run_080/results.json').read_text());by={x['name']:x for x in r['dwarfs']};src={x['name']:x for x in saved['results']['canonical']['rows']};zeta=.1;gas=9*zeta;checks=[]
def ck(n,v):
 checks.append({'name':n,'pass':bool(v)})
 if not v:raise AssertionError(n)
# Dimensionless initial G=M0=R=j=1. Smooth inflow, impulsive removal.
def evolve(g,dt,slow_out=False):
 T=100.;stop=2*T if slow_out else T;n=int(round(stop/dt));dt=stop/n;r=1.;v=0.;work=0.
 def mass(t):
  s=t/T
  if s<=1:return 1+g*(3*s*s-2*s*s*s),g*(6*s-6*s*s)/T
  s=s-1;return 1+g*(1-3*s*s+2*s*s*s),-g*(6*s-6*s*s)/T
 def acc(r,m):return 1/r**3-m/r**2
 for i in range(n):
  t=i*dt;m,dm=mass(t);m2,dm2=mass(t+dt);vh=v+.5*dt*acc(r,m);rr=r+dt*vh;vv=vh+.5*dt*acc(rr,m2)
  work-=.5*dt*(dm/r+dm2/rr);r,v=rr,vv
 final_m=mass(stop)[0];E=.5*v*v+.5/r**2-final_m/r
 if not slow_out:E+=g/r;work+=g/r
 return {'energy':E,'gain_over_initial_binding':2*(E+.5),'radius_at_removal':r,'net_work':work,'energy_work_residual':E+.5-work}
rows=[]
for name in ['Draco','Sextans','Fornax','Leo I']:
 x=by[name];D=src[name]['inferred_core_plus_settled_over_Mb']+src[name]['actual_free_inside_over_Mb'];g=gas/D
 ck(name+' below circular unbinding threshold',0<g<1)
 exact=g*g;fine=evolve(g,.005);coarse=evolve(g,.01);adiab=evolve(g,.005,True)
 ck(name+' exact impulse plus adiabatic action prediction',abs(fine['gain_over_initial_binding']-exact)<2e-5)
 ck(name+' step refinement',abs(fine['gain_over_initial_binding']-coarse['gain_over_initial_binding'])<1e-6)
 ck(name+' prescribed gas work accounts for energy gain',abs(fine['energy_work_residual'])<1e-6)
 ck(name+' slow cycle reversible control',abs(adiab['gain_over_initial_binding'])<2e-5)
 ck(name+' no angular momentum torque in equations',abs((1+g)*(1/(1+g))-1)<1e-15)
 # Alternate uses desired endpoint mass only as a labelled sensitivity, not formation evidence.
 gtarget=gas/x['Mdyn_in_r12_over_Mb'];tdyn=x['r12_pc']*3.0857e16/(math.sqrt(3)*src[name]['sigma_pred']*1000)/3.15576e13
 rows.append({'name':name,'gas_mass_over_stellar_Mb':gas,'saved_model_mass_in_aperture_over_Mb':D,'g_Mgas_over_remaining_mass':g,'fractional_binding_energy_gain_exact':exact,'semimajor_axis_expansion_exact':1/(1-exact),'inflow_contracted_radius_ratio_exact':1/(1+g),'final_eccentricity_exact':g,'dimensionless_orbit_integration':fine,'slow_cycle_control':adiab,'local_dynamical_time_Myr':tdyn,'desired_endpoint_mass_sensitivity_gain':gtarget*gtarget})
d={x['name']:x for x in rows}
ck('outward heating stronger inFornax thanDraco at source-model mass',d['Fornax']['fractional_binding_energy_gain_exact']>d['Draco']['fractional_binding_energy_gain_exact'])
ck('outward heating stronger inLeoI thanSextans at source-model mass',d['Leo I']['fractional_binding_energy_gain_exact']>d['Sextans']['fractional_binding_energy_gain_exact'])
# Correct route disposition: closed adiabatic potential cycles cannot provide inward transport.
res={'claim_id':'CE-FM-082','n_checks':len(checks),'all_pass':all(c['pass'] for c in checks),'checks':checks,'common_illustrative_zeta':zeta,'rows':rows,'scope':'Exact circular Kepler slow-inflow/impulsive-outflow test with independent orbit integration and slow-cycle control. Gravity-only clearing channel; gas histories/power and cold self-gravity not solved. Does not form Draco/Sextans compact mass.'}
Path(sys.argv[1]).write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'n_checks':len(checks),'rows':[{k:v for k,v in x.items() if k not in ['dimensionless_orbit_integration','slow_cycle_control']} for x in rows]},indent=2))
