from pathlib import Path
import json,math,hashlib,sys,resource,subprocess
import scipy
from scipy.integrate import quad
R=Path(__file__).resolve().parents[2];P=R/'campaign_fresh_gravity/CFG918_dwarf_receiver_capacity/cfg918_results.json';Q=R/'sol61_push/cold_final_mile_2026_10_13/receiver_capacity_audit_2026_10_20/run_001/results.json';d=json.loads(P.read_text());guard=json.loads(Q.read_text());G=d['constants']['G'];checks=[]
MSUN=1.989e33;PC=3.0857e18;T=12*365.25*86400*1e9
pins={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [P,Q]}
def ck(name,v):
 assert v,name
 checks.append({'name':name,'pass':True})
ck('source mass result committed bytes',hashlib.sha256(subprocess.check_output(['git','-C',str(R),'show','bb9b20525:'+str(P.relative_to(R))])).hexdigest()==pins[str(P.relative_to(R))])
def moments(v,s):
 z=v*v/(2*s*s);e=math.exp(-z);p=math.erfc(math.sqrt(z))+2/math.sqrt(math.pi)*math.sqrt(z)*e
 return (p,math.sqrt(8/math.pi)*s*(1+z)*e,3*s*s*p+4/math.sqrt(math.pi)*s*s*z**1.5*e,8*math.sqrt(2/math.pi)*s**3*(1+z+.5*z*z)*e)
for cut in [0.,1.,3.,6.,17.5]:
 a=moments(cut,1.)
 for k in range(4):
  b=quad(lambda v: math.sqrt(2/math.pi)*v**(k+2)*math.exp(-v*v/2),cut,math.inf,epsabs=1e-95,epsrel=1e-10)[0]
  ck('analytic Maxwell moment vs independent quadrature '+str((cut,k)),abs(a[k]/b-1)<1e-8)

def flux_bound(targ,S,v):
 s=targ['sigma_kms'];a0,a1,a2,a3=moments(v,s);mean=math.sqrt(8/math.pi)*s
 pref=T*targ['rho_max_Msun_pc3']*MSUN/PC**3*S*1e5 # moments below use km/s; factor converts event speed to cm/s
 return pref*(a1+mean*a0),.5*pref*(a3+mean*a2),pref*(a2+mean*a1)*targ['Rmax_pc']

def budget(targ,S):
 f=targ['escaping_mass_fraction'];m0,e0,j0=flux_bound(targ,S,0.)
 if m0<=f:cut=0.;mass,E,J=m0,e0,j0
 else:
  lo,hi=0.,100*targ['sigma_kms']
  for _ in range(100):
   v=(lo+hi)/2
   if flux_bound(targ,S,v)[0]>f:lo=v
   else:hi=v
  cut=(lo+hi)/2;mass,E,J=flux_bound(targ,S,cut)
 return {'Smax_cm2_g':S,'optimal_cut_kms':cut,'optimistic_escaping_fraction':mass,'max_wind_energy_per_initial_mass_kms2':E,'energy_fraction_of_required':E/targ['required_energy_per_mass'],'max_wind_J_per_initial_mass_pc_kms':J,'J_fraction_of_required':J/targ['required_J_per_mass'] if targ['required_J_per_mass']>0 else None,'passes_energy_upper_bound':E>=targ['required_energy_per_mass'],'passes_J_upper_bound':J>=targ['required_J_per_mass']}

targets=[]
for n in ['Draco','Sextans','Fornax','Leo I']:
 obj=d['results']['canonical']['B0'][n];b=obj['base'];gr=obj['geoms']['G1'];cr=gr['cores']['C'];a=b['a'];rad=b['R'];rmax=gr['rmax_set'][-1];initialE=gr['E_init_corners']['lam1.0|phiK1.0'];Jreq=gr['patch']['J1']
 if n in ['Draco','Sextans']:
  key=next(k for k in gr['rb']['RE']['opt'] if k.startswith('1.0|C|'));ref=gr['rb']['RE']['opt'][key][-1];c=ref['cfg'];mA=c['mA'];mB=c['mB'];r1=c['r1'];r2=c['r2'];KB=c['KB'];KA=c['KA'];stellar_guard='source endpoint; full-population kinematics not certified'
 else:
  v=next(z for z in guard['separate_PH1_partial_guard'] if z['name']==n);c=v['full_static_snapshot_optimum'];mA=c['mA_Msun'];mB=c['mB_Msun'];r1=c['rA_pc'];r2=c['rB_pc'];stellar_guard='previous static full-Plummer upper guard only, not radial likelihood'
  Mpl=b['Ms']*r1**3/(r1*r1+a*a)**1.5;KA=.5*mA*G*(Mpl+b['s']*b['Ms']+b['Mx']+mA/2)/r1
  phi=lambda r:-G*b['Ms']/math.sqrt(r*r+a*a)-G*b['s']*b['Ms']/r
  WA=mA*phi(r1)-G*b['Mx']*mA/r1-G*mA*mA/(2*r1);WB=mB*phi(r2)-G*b['Mx']*mB/r2-G*mA*mB/r2-G*mB*mB/(2*r2)
  KB=initialE-(cr['E']+KA+WA+WB)
 JA=mA*r1*math.sqrt(2*KA/mA) if mA else 0.
 sigma=math.sqrt(2*cr['K']/(3*b['Mx']));gR=rad**3/(rad**2+104**2);rho0=3*b['Mx']/(4*math.pi*gR*104**2)
 ck(n+' receiver finite stock',abs((b['Mx']+mA+mB)/b['Mrem']-1)<1e-12)
 ck(n+' source wind kinetic positive',KB>0)
 targ={'name':n,'mass_branch':'catalogue B0','footing':'canonical','sigma_kms':sigma,'rho_max_Msun_pc3':rho0,'initial_mass_Msun':b['Mrem'],'core_mass_Msun':b['Mx'],'bound_receiver_mass_Msun':mA,'wind_mass_Msun':mB,'Rmax_pc':rmax,'escaping_mass_fraction':mB/b['Mrem'],'wind_speed_reference_kms':math.sqrt(2*KB/mB),'required_energy_per_mass':KB/b['Mrem'],'required_J_per_mass':max(0,Jreq-JA)/b['Mrem'],'stellar_guard':stellar_guard}
 targ['scan']=[budget(targ,S) for S in [.01,.1,1.,10.,100.,1e4]]
 lo,hi=-12.,100.
 if budget(targ,10**hi)['passes_energy_upper_bound']:
  for _ in range(100):
   mid=(lo+hi)/2
   if budget(targ,10**mid)['passes_energy_upper_bound']:hi=mid
   else:lo=mid
  targ['log10_formal_S_required_energy_bound']=hi
 else:targ['log10_formal_S_required_energy_bound']=None
 targ['Maxwell_speed_tail_at_reference_wind']=moments(targ['wind_speed_reference_kms'],sigma)[0]
 if n=='Sextans':
  warm=[]
  for cap in [1.,100.,1e4]:
   lo,hi=sigma,100.
   for _ in range(80):
    mid=(lo+hi)/2;test=dict(targ,sigma_kms=mid)
    if budget(test,cap)['passes_energy_upper_bound']:hi=mid
    else:lo=mid
   deltaK=1.5*b['Mx']*(hi*hi-sigma*sigma)
   warm.append({'Smax_cm2_g':cap,'sigma_required_to_pass_optimistic_energy_bound_kms':hi,'extra_random_core_K_if_entire_core_heated_Msun_kms2':deltaK,'extra_core_heating_over_reference_wind_K':deltaK/KB})
  targ['heated_phase_sensitivity_not_equilibrium']=warm
 ck(n+' selected flux mass never exceeds budget',all(z['optimistic_escaping_fraction']<=targ['escaping_mass_fraction']*(1+1e-12) for z in targ['scan']))
 ck(n+' larger cross-section cap increases energy upper bound',all(x['energy_fraction_of_required']<=y['energy_fraction_of_required'] for x,y in zip(targ['scan'],targ['scan'][1:])))
 targets.append(targ)
# Isolated equal-mass elastic collisions conserve COM momentum and kinetic energy.
for v1,v2 in [((1.,2.,3.),(-3.,4.,-1.)),((10.,0.,0.),(-10.,0.,0.)),((0.,7.,0.),(0.,7.,0.))]:
 V=tuple((x+y)/2 for x,y in zip(v1,v2));w=tuple(x-y for x,y in zip(v1,v2));w1=(-w[1],w[0],w[2]);u1=tuple(x+y/2 for x,y in zip(V,w1));u2=tuple(x-y/2 for x,y in zip(V,w1));ck('elastic energy '+str(v1),abs(sum(x*x for x in v1+v2)-sum(x*x for x in u1+u2))<1e-12);ck('elastic momentum '+str(v1),all(abs(x+y-z-q)<1e-12 for x,y,z,q in zip(v1,v2,u1,u2)))
ck('all input bytes unchanged',all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in pins.items()))
result={'claim':'Optimistic fixed-Maxwellian reversible-elastic wind energy/J upper bound with finite lost-mass budget','source_snapshot':'CFG918 bb9b20525 plus prior two-target stellar-upper-guard audit','input_hashes':pins,'checks':checks,'n_checks':len(checks),'targets':targets,'scope':'No actual microscopic collision kernel or evolution; no nonthermal or contracting hotter phase; bounds only under written hypotheses. Same cross-section cap per scan cell across four endpoints. No four-dwarf dynamics or observed-likelihood fit.','software':{'python':sys.version.split()[0],'scipy':scipy.__version__},'peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss};assert result['peak_rss_bytes_macos']<1_000_000_000;Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'checks':len(checks),'scans':[{ 'name':t['name'],'S1_energy_fraction':t['scan'][2]['energy_fraction_of_required'],'S1e4_energy_fraction':t['scan'][-1]['energy_fraction_of_required'],'S1e4_J_fraction':t['scan'][-1]['J_fraction_of_required'],'log10_formal_S_min_energy':t['log10_formal_S_required_energy_bound']} for t in targets]}))
