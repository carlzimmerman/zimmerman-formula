"""Necessary-condition audit of baryon heating and a density-screened scalar."""
import json,math
from pathlib import Path
import sympy as s
p=Path(__file__).parent
n,g,a,k=s.symbols('n g a k',positive=True)
# V=a |chi|^3/3 + g n chi, negative branch chi=-sqrt(g n/a).
chi=-s.sqrt(g*n/a)
e=s.simplify(a*(-chi)**3/3+g*n*chi+k*n*n)
compress=s.simplify(s.diff(e,n,2))
expected=2*k-g**s.Rational(3,2)/(2*s.sqrt(a*n))
assert s.simplify(compress-expected)==0
nc=g**3/(16*a*k*k)
assert s.simplify(compress.subs(n,nc))==0
# The mediator mass^2 is 2a |chi|, so contact sigma ~ mass^-4 ~ n^-1.
mass2=2*a*(-chi)
assert s.simplify(s.diff(s.log(mass2**-2),n)*n+1)==0
G=6.67430e-11;kpc=3.085677581491367e19;Gyr=365.25*86400*1e9;a0=9.3603e-11
rows=[]
for Vkm in [50,100,200,300]:
 V=Vkm*1000;v=V/math.sqrt(2)
 for C in [.01,.1]:
  rows.append(dict(V_kms=Vkm,C=C,baryon_energy_depletion_time_Gyr=(V*V/2)/(C*a0*v)/Gyr))
relax=[]
for Rkpc in [1,10,50]:
 R=Rkpc*kpc;V=200e3;rho=V*V/(4*math.pi*G*R*R);mean=4*(V/math.sqrt(2))/math.sqrt(math.pi)
 for S in [.1,.3,4.]:
  tc=1/(rho*S*.1*mean);td=R/V
  relax.append(dict(radius_kpc=Rkpc,S_cm2_g=S,collision_time_Gyr=tc/Gyr,crossing_time_Gyr=td/Gyr,collision_to_crossing=tc/td))
R=dict(scalar_energy=str(e),inverse_compressibility=str(compress),unstable_below_density=str(nc),baryon_budget=rows,self_collision_relaxation=relax,checks={'scalar_stationary_energy':True,'compressibility_root':True,'density_cross_section_exponent':True},non_claims=['Scalar is a trial extension, not established particle model','Contact limit and dark-source-dominated screening required','Baryon budget assumes heating without replenishment; not exclusion','SIS example and self collisions only; not a full transport coefficient','No derived a0 or universal profile'])
(p/'run'/'results.json').write_text(json.dumps(R,indent=2)+'\n');print(json.dumps(R,indent=2))
