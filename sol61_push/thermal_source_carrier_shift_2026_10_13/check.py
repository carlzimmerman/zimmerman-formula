"""Real one-loop thermal-R contribution at the vacuum pair threshold."""
import json,sys,math
from pathlib import Path
import sympy as s
from scipy.integrate import quad
from scipy.special import kv
prior=json.loads(Path('sol61_push/ordinary_lepton_source_2026_10_13/run/results.json').read_text())['reduced_muon_case']
mu=prior['equal_width_mu_R_phi_eV'];m=1e6;MR=2*m
checks=[]
def ck(n,v):checks.append({'name':n,'passed':bool(v)});assert v,n
k,M,u=s.symbols('k M u',positive=True)
E=s.sqrt(4*M*M+k*k)
amp=-u*u*(1/(4*M*M+2*M*E)+1/(4*M*M-2*M*E))
ck('threshold crossed amplitude',s.simplify(amp-2*u*u/k**2)==0)
rows=[]
for T in [.1e6,.5e6,1e6,2e6,3e6]:
 x=MR/T
 def h(q):
  e=math.sqrt(q*q+x*x);z=math.exp(-e)
  return z/((1-z)*e)
 i0=quad(h,0,100,epsabs=1e-13,epsrel=1e-11)[0]
 i2=T*T*quad(lambda q:q*q*h(q),0,100,epsabs=1e-13,epsrel=1e-11)[0]
 series=sum(kv(0,n*x) for n in range(1,401))
 ck('thermal integral Bessel '+str(T),math.isclose(i0,series,rel_tol=1e-9,abs_tol=1e-18))
 Pi=-mu*mu/(2*math.pi**2)*i0
 shift=Pi/(math.sqrt(m*m+Pi)+m)
 ck('small mass expansion '+str(T),math.isclose(shift,Pi/(2*m),rel_tol=1e-9))
 contact=i2/(4*math.pi**2)
 lam=-Pi/contact
 ck('contact cancellation '+str(T),abs((Pi+lam*contact)/Pi)<1e-14)
 rows.append({'T_MeV':T/1e6,'I0_dimensionless':i0,'thermal_Pi_phi_eV2':Pi,
 'carrier_mass_shift_eV':shift,'pair_threshold_shift_eV':2*shift,
 'shift_over_weak_wall_retuned_excess':abs(2*shift)/2.6625713955157683e-16,
 'contact_coefficient_Pi_per_lambda_eV2':contact,'lambda_R2_phi2_cancel_at_this_T':lam})
result={'all_pass':all(c['passed'] for c in checks),'checks':checks,'rows':rows,
 'conventions':'L=-mu R|phi|^2; forward amplitude Mcal; Pi=-integral d^3k/(2pi)^3 nB Mcal/(2ER); MR=2m threshold limit',
 'assumptions':['Prescribed equilibrium free R bath, initially negligible phi bath',
 'Only real on-shell thermal-R self-energy contribution at leading mu^2',
 'Independent R^2|phi|^2 coefficient zero for main result, sensitivity supplied separately'],
 'non_claims':['Not a self-consistent thermal pole, total width or production rate',
 'No proof that the vacuum near-threshold mass assignment persists in a thermal bath',
 'No full cosmological exclusion or laboratory creation protocol']}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
