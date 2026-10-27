"""Conservation gates for mergers; no field collision kernel is assumed."""
from pathlib import Path
from fractions import Fraction
import json,math,sys,resource
from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar
R=Path(__file__).resolve().parents[2]
d=json.loads((R/'campaign_fresh_gravity/CFG918_dwarf_receiver_capacity/cfg918_results.json').read_text())
p=json.loads((R/'sol61_push/cold_collision_outflow_2026_10_20/run_001/results.json').read_text())
proj=json.loads((R/'sol61_push/cold_endpoint_projection_2026_10_20/run_002/results.json').read_text())
arg=json.loads((R/'argon_push/ARGON11_nonlinear_fragmentation_2026-10-17/argon11_results.json').read_text())
G=d['constants']['G'];c=299792.458;checks=[];rows=[]
def ck(name,cond):
 checks.append({'name':name,'pass':bool(cond)});assert cond,name

def relK(m,P):
 return P*P/(math.sqrt(m*m+(P/c)**2)+m)

def Jcap(r,m,K):
 return r*math.sqrt(2*m*K+K*K/(c*c))

# Six unpolarized photons, zero momentum and intrinsic J in their COM, boosted in x.
for beta in [0.,1e-5,1e-3]:
 gamma=1/math.sqrt(1-beta*beta);Elab=0.;px=0.;py=0.;pz=0.
 for nx,ny,nz in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
  E=1/6;Elab+=gamma*E*(1+beta*nx);px+=gamma*E*(nx+beta);py+=E*ny;pz+=E*nz
 ck('isotropic COM radiation boost '+str(beta),abs(px-beta*Elab)<1e-14 and abs(py)+abs(pz)<1e-14)
ck('bound E/Q need not yield merger fuel',Fraction(95,100)*123+Fraction(95,100)*456-Fraction(95,100)*(123+456)==0)
ck('surface correction can yield positive incremental release',2-2**(2/3)>0)
# Independent two-particle saturation of the nonrel orbital Cauchy inequality.
for rr,vel,m in [(1.,1.,2.),(10.,20.,3.),(648.,128.,291027.)]:
 J=sum((m/2)*rr*vel for _ in range(2));K=sum(.5*(m/2)*vel*vel for _ in range(2))
 ck('orbital Cauchy saturation '+str(rr),abs(J/(rr*math.sqrt(2*m*K))-1)<1e-14)

frag=arg['R1'].get('At_tA') or next(s for s in arg['R1']['series'] if s['Nl']>=3 and math.isfinite(s['R_med']))
rad_dim=frag['R_med'];rad_pc=rad_dim*197.3269804e-15/3.0857e16 # illustrative mh=1MeV, source radius in mh^-1
for t in p['targets']:
 n=t['name'];b=d['results']['canonical']['B0'][n]['base'];s=next(r for r in proj['rows'] if r['name']==n)
 M=t['initial_mass_Msun'];m0=t['wind_mass_Msun'];K0=M*t['required_energy_per_mass'];J=M*t['required_J_per_mass'];Rc=b['R'];rA=s['endpoint_rA_pc'];rB=s['endpoint_rB_pc'];mA=t['bound_receiver_mass_Msun']
 def phi(r):
  return -G*b['Ms']/math.sqrt(r*r+b['a']**2)-G*(b['s']*b['Ms']+b['Mx'])/r-G*mA/max(r,rA)
 def gravacc(r):
  mpl=b['Ms']*r**3/(r*r+b['a']**2)**1.5
  return G*(mpl+b['s']*b['Ms']+b['Mx']+(mA if r>rA else 0))/r**2
 # Total wind orbital energy, excluding rest energy, conserved in this static thin-shell model.
 Eorb=K0+m0*phi(rB)-G*m0*m0/(2*rB)
 def Kr(r):return Eorb-m0*phi(r)+G*m0*m0/(2*r)
 Kc=Kr(Rc);Jc=Jcap(Rc,m0,Kc)
 cuts=sorted(set([Rc,rB]+([rA] if Rc<rA<rB else [])))
 work=sum(quad(gravacc,l,h,epsabs=1e-9,epsrel=1e-10)[0] for l,h in zip(cuts,cuts[1:]))
 ck(n+' static potential work checked by enclosed-mass quadrature',abs((phi(rB)-phi(Rc))-work)<1e-8*max(1,abs(work)))
 ck(n+' positive asymptotic shell orbital energy',Eorb>0)
 for r in [Rc,math.sqrt(Rc*rB),rB]:
  E=Kr(r)+m0*phi(r)-G*m0*m0/(2*r)
  ck(n+' static shell energy invariant '+str(round(r,3)),abs(E-Eorb)<1e-12*max(abs(Eorb),K0))
 ck(n+' source last-radius orbital capacity passes',Jcap(rB,m0,K0)>=J)
 ck(n+' compact core orbital capacity fails',Jc<J)
 rmin=brentq(lambda r:Jcap(r,m0,Kr(r))-J,Rc,rB,xtol=1e-8,rtol=1e-13)
 ck(n+' first last-torque root',abs(Jcap(rmin,m0,Kr(rmin))/J-1)<1e-10)
 # For this positive-energy static spherical model r^2 K(r) is increasing:
 # each fixed positive mass element's contribution is monotone, plus Eorb r^2.
 grid=[Rc*(rB/Rc)**(i/128) for i in range(129)];caps=[Jcap(r,m0,Kr(r)) for r in grid]
 ck(n+' last-torque capacity monotone sampled check',all(x<y for x,y in zip(caps,caps[1:])))
 # Extra binding energy changes rest mass and the ledger: final cold rest mass m=m0-delta.
 # Fixed core+A; all other released energy (1-eta)delta*c^2 must leave separately, never retained heat here.
 def Kgrav_new(m):return Eorb-m*phi(Rc)+G*m*m/(2*Rc)
 def deficit(delta,eta):
  mass=m0-delta
  return Kgrav_new(mass)+eta*delta*c*c-relK(mass,J/Rc)
 delta=brentq(lambda x:deficit(x,1.),0,m0/2,xtol=1e-9,rtol=1e-13)
 mnew=m0-delta;extra=delta*c*c;launch_new=Kgrav_new(mnew)+extra
 ck(n+' extended rest-mass ledger',abs((b['Mx']+mA+mnew+delta)/M-1)<1e-12)
 ck(n+' extended orbital energy and J equality',abs(Jcap(Rc,mnew,launch_new)/J-1)<1e-10)
 ck(n+' new rest defect below allowed wind budget',0<delta<m0)
 def eta_needed(z):
  delta_=z*m0;mass=m0-delta_
  return max(0.,(relK(mass,J/Rc)-Kgrav_new(mass))/(delta_*c*c))
 opt=minimize_scalar(eta_needed,bounds=(1e-8,1-1e-8),method='bounded',options={'xatol':1e-13})
 eta_min=opt.fun;z=opt.x
 ck(n+' finite mass-budget efficiency threshold equality',abs(deficit(z*m0,eta_min))<1e-8*max(relK(m0*(1-z),J/Rc),1.))
 Erad_min=J*c/Rc;dmrad=Erad_min/(c*c)
 # Cold escaper intrinsic spin bound uses positive-energy/causal size condition S <= E a/c.
 amin_spin=J/(m0*c)
 # Advected radiation only: COM momentum AND intrinsic-J-free emission, bulk<=2sigma.
 Vmax=2*t['sigma_kms'];advected_max_fraction=m0*Rc*Vmax/J
 # Endpoint-specific stellar kinetic margin, no re-equilibration or uncertainty likelihood.
 sigglobal=s['apertures']['global']['sigma_stars_kms'];margin=max(0.,1.5*b['Ms']*(b['sig']**2-sigglobal**2))
 rows.append({'name':n,'core_R_pc':Rc,'wind_mass_original_Msun':m0,'original_wind_K_Msun_kms2':K0,'residual_J_Msun_pc_kms':J,'reference_wind_speed_kms':math.sqrt(2*K0/m0),'core_required_tangential_speed_kms':J/(m0*Rc),'fixed_K_min_radius_pc':J/math.sqrt(2*m0*K0),'static_K_at_core_over_endpoint_K':Kc/K0,'static_core_orbital_J_cap_over_required':Jc/J,'static_min_last_torque_radius_pc':rmin,'last_torque_radius_over_core':rmin/Rc,'minimum_core_orbital_K_rel_Msun_kms2':relK(m0,J/Rc),'core_orbital_K_min_over_reference_K':relK(m0,J/Rc)/K0,'binding_defect_ideal_wind_branch':{'delta_rest_mass_Msun':delta,'new_wind_rest_mass_Msun':mnew,'released_energy_over_original_wind_K':extra/K0,'released_energy_over_initial_free_rest_energy':delta/M,'fraction_of_allowed_noncore_rest_budget_consumed':delta/m0,'ideal_orbital_efficiency_threshold_if_any_rest_defect_allowed':eta_min,'rest_defect_fraction_of_noncore_budget_at_threshold':z,'scope':'Optimistic new ledger, not measured merger release or Q flux. Core and A held fixed; rest defect taken from noncore allocation. Inefficiency must escape through a separately accounted channel, not heat stars.'},'directed_radiation_J_branch':{'minimum_energy_over_reference_wind_K':Erad_min/K0,'equivalent_rest_mass_Msun':dmrad,'fraction_of_allowed_noncore_rest_budget':dmrad/m0,'scope':'Optimally directed positive-energy freely propagating radiation at Rc. No measured radiation spectrum, Q, or global chirality/torque. Not an exact extended endpoint solution.'},'advected_only_radiation_branch':{'assumed_emitter_bulk_speed_max_kms':Vmax,'J_fraction_even_if_entire_noncore_rest_budget_radiated':advected_max_fraction,'scope':'Radiation has zero net momentum and intrinsic J in emitter COM. Emission from within Rc; excludes intrinsic/multipole radiation J and anisotropic recoil.'},'intrinsic_spin_branch':{'minimum_escaper_radius_pc':amin_spin,'ARGON_R1_reference_radius_dimensionless':rad_dim,'ARGON_illustrative_radius_at_1MeV_pc':rad_pc,'size_requirement_over_illustrative_radius':amin_spin/rad_pc,'scope':'Positive-energy causal compact-object spin bound; cold escapers. Illustrative mh1MeV mapping only, not a derived carrier mass or exclusion of all spectra.'},'fixed_global_stellar_snapshot_margin':{'additional_stellar_K_before_catalogue_central_value_Msun_kms2':margin,'direct_stellar_kinetic_fraction_of_ideal_binding_release_max':margin/extra,'scope':'Selected old endpoint and fixed tracer profile only. Guard near saturation by construction, not universal heating bound. Re aperture and actual observational weighting unresolved.'}})
ck('measured peak RSS below1GB',resource.getrusage(resource.RUSAGE_SELF).ru_maxrss<1_000_000_000)
out={'claim':'Conservation requirements for orbital merger outflow, conditional extended binding/rest ledger, radiation and intrinsic-spin alternatives','targets':'Same fixed reference endpoints as prior collision packet; no observed aperture refit','checks':checks,'n_checks':len(checks),'rows':rows,'peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'scope':'Necessary kinematic/ledger gates, not an actual merger kernel, phase-averaged flux, charge closure, rate, or four-dwarf physical formation result.'}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'checks':len(checks),'rows':[{'name':x['name'],'last_torque_kpc':x['static_min_last_torque_radius_pc']/1000,'core_J_fraction':x['static_core_orbital_J_cap_over_required'],'ideal_binding_rest_defect_Msun':x['binding_defect_ideal_wind_branch']['delta_rest_mass_Msun'],'rad_J_rest_equivalent_Msun':x['directed_radiation_J_branch']['equivalent_rest_mass_Msun']} for x in rows]},indent=2))
