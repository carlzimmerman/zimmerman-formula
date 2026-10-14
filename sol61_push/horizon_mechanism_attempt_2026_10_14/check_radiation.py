import json, sys, math
from pathlib import Path
import sympy as s
out=Path(sys.argv[1]);out.mkdir(exist_ok=True)
checks=[]
def ck(n,v):
 checks.append({'name':n,'ok':bool(v)})
 if not bool(v):raise AssertionError(n)
def ze(n,e):ck(n,s.simplify(e)==0)
K,c,tau,rho,pi,grad,zdot=s.symbols('K c tau rho pi grad zdot',positive=True)
lb=zdot**2/(2*K*c*c)-grad**2/(2*K)+tau*rho*zdot
mom=s.diff(lb,zdot); Hamilton=s.expand(pi*zdot-lb).subs(zdot,K*c*c*(pi-tau*rho))
ze('positive bath Hamiltonian',Hamilton-K*c*c*(pi-tau*rho)**2/2-grad**2/(2*K))
ze('bath conjugate momentum',mom-zdot/(K*c*c)-tau*rho)
M,R,omega,eps,G,z=s.symbols('M R omega eps G z',positive=True)
k=s.symbols('k',positive=True)
FT=M*s.exp(-k*k*R*R/2)
delta=eps*R*s.diff(FT,R)
ze('number conserving radial Gaussian source',delta+eps*M*k*k*R*R*s.exp(-k*k*R*R/2))
ze('zero monopole source',delta.subs(k,0))
P=G*tau*tau*omega**4*delta**2/(2*c)
P=s.simplify(P.subs(k,omega/c))
ze('spherical radiated power',P-G*tau*tau*omega**4*eps*eps*M*M*(omega*R/c)**4*s.exp(-(omega*R/c)**2)/(2*c))
E_mode=s.Rational(3,2)*M*eps*eps*omega**2*R*R
dimensionless=s.simplify((E_mode/P)*omega)
dimensionless=dimensionless.subs(G,omega**2*R**3/M).subs(c,omega*R/z)
ze('energy loss time in orbital units',dimensionless-3*s.exp(z*z)/((tau*omega)**2*z**5))
ze('radiation speed optimum',s.diff(s.exp(z*z)/z**5,z).subs(z,s.sqrt(s.Rational(5,2))))

base=json.loads(Path('sol61_push/cold_horizon_connection_2026_10_14/run_v1/results.json').read_text())['constants']
g=base['G'];cs=base['c'];ms=base['Msun_kg'];a0=base['a0'];H=base['H_per_s']
galM=6e10*ms; RR=math.sqrt(g*galM/a0); V=(g*galM*a0)**.25; om=V/RR
tauH=1/H; secGyr=365.25*86400*1e9
cases=[]
for label,cc,tt in [('metric speed, horizon time',cs,tauH),('medium speed, horizon time',V,tauH),('medium speed, weak coupling',V,.1/om)]:
 zz=om*RR/cc; tOm=3*math.exp(zz*zz)/((tt*om)**2*zz**5)
 cases.append({'label':label,'speed_m_s':cc,'tau_s':tt,'omega_tau':om*tt,'kR':zz,'energy_loss_time_Gyr':tOm/om/secGyr,'loss_rate_over_omega':1/tOm,'weak_backreaction':1/tOm<.01,'wind_speed_300km_s_over_wave_speed':300000/cc})
ck('metric-speed horizon coupling slow',cases[0]['energy_loss_time_Gyr']>1e8)
ck('slow-wave horizon coupling violates weak-radiation estimate',not cases[1]['weak_backreaction'])
ck('weak-coupling example perturbative',cases[2]['weak_backreaction'])
result={'passed':len(checks),'checks':checks,'assigned_galaxy':{'M_solar':6e10,'R_kpc':RR/3.0856775814913673e19,'V_km_s':V/1000,'omega_per_s':om,'one_over_omega_Myr':1/om/secGyr*1000},'cases':cases,'interpretation':'Explicit positive-energy bath exchange operator; fixed smooth Gaussian harmonic-mode power only. No natural fast causal horizon-scale settling established. Medium-speed horizon-time case is outside weak-backreaction validity; moving-source Cherenkov channel requires audit.'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
