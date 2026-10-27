"""One-loop MS divergence, finite charged-background instability, minimal
Lorentz scalar response characteristics, and normalization degeneracies.
No formation simulation or all-sector completion.
"""
import sys,json,math
from pathlib import Path
import numpy as np
import sympy as s
from scipy.optimize import brentq
out=Path(sys.argv[1]);assert out.is_dir();base=Path(__file__).parent
previous=json.loads((base/'mediator_phase_matching_run_002/results.json').read_text())
checks=[]
def check(n,v):checks.append({'name':n,'passed':bool(v)});assert v,n
I,chi,L,a,B,mu,l,m2=s.symbols('I chi L a B mu l m2',real=True)
# B=M²; canonical Hessian of two real charged components + chi.
rad=m2+6*L*I+a*chi;gold=m2+2*L*I+a*chi;heavy=B+2*mu*chi+3*l*chi**2
trace=s.expand(rad**2+gold**2+heavy**2+4*a*a*I)
expected=40*L*L*I*I+(16*L*m2+4*a*a)*I+16*L*a*I*chi+9*l*l*chi**4+12*l*mu*chi**3+(2*a*a+6*B*l+4*mu*mu)*chi*chi+(4*m2*a+4*B*mu)*chi+2*m2*m2+B*B
check('canonical Hessian trace polynomial',s.expand(trace-expected)==0)
# BetaV=TrH²/(32pi²), no one-loop wavefunction poles for these scalar interactions.
loop=16*math.pi**2
betaL=20*L*L;betaa=8*L*a;betaB=2*a*a+6*B*l+4*mu*mu
betanet=s.expand(betaL-a/B*betaa+a*a/(2*B*B)*betaB)
MM=s.symbols('M',positive=True);selected={L:2-1/MM,a:2*MM,B:MM*MM,mu:-3*MM/8,l:1}
projected=s.simplify(betanet.subs(selected))
check('quartic running projection',s.simplify(projected-(20*(2-1/MM)**2-32*(2-1/MM)+s.Rational(233,8)))==0)
quantum=[]
for mass in (1.,10.,100.,1000.):
 ll=2-1/mass;bn=(20*ll*ll-32*ll+233/8)/loop
 quantum.append({'M_over_m':mass,'tree_net_quartic':-1/mass,'beta_net_quartic_MS':bn,'linearized_log_interval_equal_tree':1/(mass*abs(bn)),
  'beta_host_mass_squared_over_m2':(8*ll+8*mass*mass)/loop,
  'beta_tadpole_in_m3':(4*mass-.75*mass**3)/loop,
  'beta_net_quartic_following_stationary_vacuum':bn+(6/mass**2-9/8)/loop,
  'beta_host_mass_squared_following_stationary_vacuum':(8*ll-8+9.5*mass**2)/loop,
  'beta_vacuum_constant_in_m4':(2+mass**4)/(32*math.pi**2),
  'note':'MS full-theory scale diagnostic; not finite threshold, scheme-independent stability verdict or decoupled EFT running'})
# Formation: finite charged coherent backgrounds in the actual two-field model.
formation=[]
for parent in previous['rows']:
 mass=parent['M_over_m']
 if mass not in (10.,100.):continue
 ll=2-1/mass;aa=2*mass;nu=-3*mass/8
 for fraction in (.1,.5,1.,2.):
  ii=parent['phase_I_exact']*fraction
  cc=brentq(lambda z:mass*mass*z+nu*z*z+z**3+aa*ii,-4*ii/mass-1,0)
  w2=1+2*ll*ii+aa*cc;check('real frequency '+str((mass,fraction)),w2>0)
  omega=math.sqrt(w2);Ar=4*ll*ii;Bh=mass*mass+2*nu*cc+3*cc*cc;h=aa*math.sqrt(2*ii)
  Aeff=Ar-h*h/Bh;cs2=Aeff/(Aeff+4*w2)
  threshold=max(0,2*(h*h-Ar*Bh)/(math.sqrt((Ar-Bh)**2+4*h*h)+Ar+Bh))
  wave=[]
  for k in np.linspace(0,2,201):
   K=np.array([[k*k+Ar,0,h],[0,k*k,0],[h,0,k*k+Bh]])
   gyro=np.array([[0,-2*omega,0],[2*omega,0,0],[0,0,0]])
   generator=np.block([[np.zeros((3,3)),np.eye(3)],[-K,-gyro]])
   eig=np.linalg.eigvals(generator)
   growth=float(max(eig.real))
   wave.append((float(k),growth))
   if k>0 and k*k<threshold-1e-6:
    check('independent unstable band '+str((mass,fraction,float(k))),growth>1e-7)
   if k*k>threshold+1e-6:
    check('independent stable band '+str((mass,fraction,float(k))),growth<1e-7)
   check('conjugate symmetric frequency trace '+str((mass,fraction,float(k))),abs(float(sum(eig.real)))<1e-9)
  fastest=max(wave,key=lambda v:v[1])
  vv=ii+ll*ii*ii+aa*cc*ii+.5*mass*mass*cc*cc+nu*cc**3/3+cc**4/4
  energy_per_charge=(w2*ii+vv)/(2*omega*ii)
  formation.append({'M_over_m':mass,'initial_energy_per_charge':energy_per_charge,
   'bulk_binding_energy_per_charge_available':energy_per_charge-math.sqrt(parent['omega_squared_exact']),'I_fraction_of_coexistence':fraction,'I':ii,'omega':omega,'effective_grand_amplitude_curvature':Aeff,'long_wavelength_sound_squared':cs2,'unstable_band_upper_k':math.sqrt(threshold),
   'max_sampled_growth_rate':fastest[1],'fastest_sampled_k':fastest[0],
   'sampled_spinodal_growth_above_1e_minus7':bool(fastest[1]>1e-7),
   'scope':'Homogeneous charged classical condensate; not neutral thermal gas, vacuum creation, nonlinear fragmentation or Q-ball abundance'})
# Minimal Lorentz-invariant response, fixed phase interior K=0.
p,C,beta=s.symbols('p C beta',positive=True)
y=p/C+beta*p*p;D=C*beta*p*p
cone=s.simplify(y*s.diff(D,p)/(D*s.diff(y,p)))
check('minimal scalar radial characteristic',s.simplify(cone-2*(1+C*beta*p)/(1+2*C*beta*p))==0)
cones=[{'C_beta_p':z,'radial_speed_squared_over_metric_c2':2*(1+z)/(1+2*z),'tangential_speed_squared_over_metric_c2':1.} for z in (.0001,.01,1.,100.)]
# a0 with W=beta p³/3 and annular force law.
def coeff(be):return 1/(4*math.pi*be)
normalization={'same_host_and_flux_different_response':[{'beta':be,'a0_in_q_C_Glab_unit_dictionary':coeff(be)} for be in (1.,4.)],
 'same_flux_different_vacuum_history':[{'Q':1.,'residual_DeltaF_plus_trace':d,'physical_Beff':.5+d} for d in (0.,1.)],
 'counterexample_scope':'Independent couplings/history data allowed by current candidate. Not a no-go theorem against mechanisms adding new conditions.'}
result={'checks':checks,'hessian_trace_squared':str(trace),'quantum_rows':quantum,'formation_rows':formation,'gravity_characteristics':cones,'normalization_counterexamples':normalization,
 'non_claims':['Full one-loop effective potential/finite matching, quantum phase and vacuum stability not yet calculated','Linear instability of specified charged backgrounds does not derive initial charge or nonlinear formation/energy receiver','Minimal single-gradient Lorentz scalar completion only; independent-frame/multifield alternatives not excluded','No unique physical dark-energy density, kappa, observational fit, full theory closure or novelty certificate']}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'controls':len(checks),'quantum':quantum,'formation':formation,'gravity':cones,'normalization':normalization},indent=2))
