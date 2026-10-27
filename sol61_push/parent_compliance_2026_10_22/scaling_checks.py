"""Exact scaling and declared finite examples for material compliance."""
import argparse,json
from pathlib import Path
import sympy as s
import numpy as np
from scipy.optimize import brentq

pa=argparse.ArgumentParser()
pa.add_argument('--output',required=True)
pa.add_argument('--mutate',action='store_true')
args=pa.parse_args()
checks=[]
def ck(name,ok,value):
    checks.append(dict(name=name,passed=bool(ok),value=str(value)))
    print(('PASS ' if ok else 'FAIL ')+name+': '+str(value))

aa,m,rho0,ell0,k,M,R,A0,G=s.symbols('a m rho0 ell0 k M R A0 G',positive=True)
z=(k/aa)**2*ell0**2*((rho0/aa**3)/rho0)**(-m)
ck('expansion_exponent',s.simplify(aa*s.diff(z,aa)/z-(3*m-2))==0,z)
vol=4*s.pi*R**3/3
rho=M/vol
U=A0*rho0**m*rho**(2-m)*vol/2
grav=(-1 if not args.mutate else 1)*3*G*M*M/(5*R)
ck('concentration_exponent',s.simplify(R*s.diff(U,R)/U+3*(1-m))==0,s.simplify(R*s.diff(U,R)/U))
mc=((5*A0*rho0**s.Rational(2,3)/(6*G))*(3/(4*s.pi))**s.Rational(1,3))**s.Rational(3,2)
coeff=s.simplify((R*(U+grav)).subs(m,s.Rational(2,3)))
ck('marginal_mass',s.simplify(coeff.subs(M,mc))==0,mc)
unitfactor=s.simplify(mc.subs(A0,4*s.pi*G*ell0**2)/(rho0*ell0**3))
ck('mass_coefficient',s.simplify(unitfactor-s.sqrt(250*s.pi**2/9))==0,unitfactor)

# Direct integral check for a uniform sphere gravitational energy.
r=s.symbols('r',positive=True)
enc=M*(r/R)**3
direct=s.integrate(-G*enc/r*s.diff(enc,r),(r,0,R))
ck('sphere_gravity_integral',s.simplify(direct+3*G*M*M/(5*R))==0,direct)

fb=1/6.364;fc=1-fb
def growth(z):
    lam=(fb+fc/(1+z)+np.sqrt((fb-fc/(1+z))**2+4*fb*fc))/2
    return (-1+np.sqrt(1+24*lam))/4
zmax=brentq(lambda z:growth(z)-.999,0,1)
pc=3.085677581491367e16;Msun=1.98847e30
ellmax=np.sqrt(zmax)/.1*1e6*pc
rhoref=2.26e-27
Mcrit=float(unitfactor)*rhoref*ellmax**3/Msun
examples=[]
for ratio in [.5,1.,2.,100.]:
    # At critical exponent, U/|Egrav|=(Mcrit/M)^(2/3).
    rel=ratio**(-2/3)-1
    examples.append(dict(mass_over_trial_critical=ratio,total_energy_over_abs_gravity=rel))
ck('trial_signs', examples[0]['total_energy_over_abs_gravity']>0 and examples[2]['total_energy_over_abs_gravity']<0,examples)

result=dict(status='checks_passed' if all(c['passed'] for c in checks) else 'checks_failed',
            mutation=args.mutate,checks=checks,
            benchmark=dict(rho0_kg_m3=rhoref,ell0_upper_pc=ellmax/pc,
                           uniform_sphere_trial_mass_Msun=Mcrit,coefficient=float(unitfactor),
                           note='Upper allowed length, not a selected length; trial scale not a core prediction'),
            examples=examples,non_claims=['No dynamical collapse simulation','No all-background stability theorem',
                                         'No observed mass threshold','No full relativistic completion'])
path=Path(args.output);path.parent.mkdir(parents=True,exist_ok=True)
path.write_text(json.dumps(result,indent=2)+'\n')
print(f"CHECKS {sum(c['passed'] for c in checks)}/{len(checks)}")
raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
