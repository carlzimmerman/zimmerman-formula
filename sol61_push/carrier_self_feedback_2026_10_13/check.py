"""Leading Hartree feedback diagnostic from the inherited repulsive quartic."""
import json,sys,math
from pathlib import Path
import sympy as s
from scipy.integrate import quad,solve_ivp
prev=json.loads(Path('sol61_push/thermal_carrier_initial_production_2026_10_13/run/results.json').read_text())
src=json.loads(Path('sol61_push/ordinary_lepton_source_2026_10_13/run/results.json').read_text())['reduced_muon_case']
mu=src['equal_width_mu_R_phi_eV'];m=1e6;MR=2*m;lam=1e-6;hb=6.582119569e-16;hc=1.973269804e-7
checks=[]
def ck(n,v):checks.append({'name':n,'passed':bool(v)});assert v,n
r1,r2,L,J=s.symbols('r1 r2 L J',real=True)
V=L*(r1*r1+r2*r2)**2/4
mass=s.expand(s.diff(V,r1,2)).subs({r1**2:J/2,r2**2:J/2})
ck('O2 quartic Hartree normalization',s.simplify(mass-2*L*J)==0)
rows=[]
for p in prev['rows']:
 T=p['T_MeV']*1e6;D0=p['effective_pair_excess_eV'];gam=p['quasiparticle_spontaneous_partial_width_eV']
 mi=m+p['one_step_carrier_mass_shift_eV'];beta=math.sqrt(D0*(MR+2*mi))/MR
 x=MR/T
 def components(q):
  E=math.sqrt(x*x+q*q);f=math.exp(-E)/(1-math.exp(-E));r=q/E*beta
  angular=math.atanh(r)/r if r else 1.
  return q*q*f/E,4*q*q*f/(E*E)*angular
 In=quad(lambda q:components(q)[0],0,100,epsabs=1e-12,epsrel=1e-11)[0]
 IJ=quad(lambda q:components(q)[1],0,100,epsabs=1e-12,epsrel=1e-11)[0]
 ndot=2*gam*MR*T*T/(2*math.pi**2)*In
 Jdot=gam*MR*T/(2*math.pi**2)*IJ
 ck('initial total source cross-check '+str(T),math.isclose(ndot,p['initial_number_source_eV4'],rel_tol=1e-9))
 # Check exact isotropic decay-angle average for one representative parent.
 ER=math.sqrt(MR*MR+T*T)
 angle=quad(lambda z:1/(ER/2+T*beta*z/2)+1/(ER/2-T*beta*z/2),-1,1)[0]/2
 ratio=T*beta/ER
 analytic=4/ER*math.atanh(ratio)/ratio
 ck('decay-angle inverse-energy average '+str(T),math.isclose(angle,analytic,rel_tol=1e-12))
 Jstar=m*D0/(2*lam)
 tstop=2*Jstar/Jdot*hb
 nstar=Jstar*ndot/Jdot
 fzero=p['initial_rest_mode_df_dt_per_s']*tstop/2
 nR=p['assumed_R_number_density_eV3']
 rows.append({'T_MeV':p['T_MeV'],'initial_J_source_eV3':Jdot,'threshold_feedback_J_eV2':Jstar,
 'on_shell_closure_time_toy_s':tstop,'daughter_number_at_closure_eV3':nstar,
 'daughter_number_at_closure_per_m3':nstar/hc**3,'parent_depletion_fraction_estimate':nstar/(2*nR),
 'rest_mode_occupation_at_closure_estimate':fzero})
# Universal leading source-feedback equation: u=J/Jstar, s=t/tstop.
# Valid before closure; do not numerically extrapolate a zero-width closure.
sol=solve_ivp(lambda t,y:[2*math.sqrt(max(0,1-y[0]))],(0,.99),[0.],rtol=1e-10,atol=1e-12,dense_output=True)
ck('feedback solver success',sol.success)
err=max(abs(sol.sol(t)[0]-(2*t-t*t)) for t in [0,.1,.5,.9,.99])
ck('feedback solution analytic agreement',err<1e-8)
result={'all_pass':all(c['passed'] for c in checks),'checks':checks,'rows':rows,'lambda_rep':lam,
 'tree_square_completion_minimum_lambda':mu**2/(2*MR**2),
 'direct_source_tadpole_over_repulsive_Hartree_magnitude':mu**2/(4*lam*MR**2),
 'feedback_solution_max_error':err,
 'non_claims':['Truncated moment diagnostic, not full conserved source-carrier kinetic evolution',
 'On-shell closure is not zero production with finite widths and off-shell processes',
 'No final equilibrium, relic abundance or cold laboratory inventory']}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
