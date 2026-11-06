import sympy as S
import json,hashlib
from pathlib import Path
r,A,g,r0=S.symbols('r A gamma r0',positive=True)
H=r*r/2+(A*r-1-g*r*r)**2/(2*g)
h1=S.diff(H,r);h2=S.diff(H,r,2);h3=S.diff(H,r,3)
sub={r:r0,A:(1+g*r0*r0)/r0}
checks={
 'Hr':S.simplify(h1.subs(sub)-r0)==0,
 'Hrr':S.simplify(h2.subs(sub)-1-(1/r0-g*r0)**2/g)==0,
 'Hrrr':S.simplify(h3.subs(sub)+6*(1/r0-g*r0))==0,
}
c2=h1/(r*h2)
# 2 r c times d lambda+/dr at rest, with theta'=1/(r c).
Gdirect=2*(1-c2)+r*S.diff(c2,r)
G=3*(1-c2)-h1*h3/(h2*h2)
checks['genuine_nonlinearity_factor']=S.simplify(Gdirect-G)==0
z=S.symbols('z',positive=True)
checks['sound_homogeneous']=S.simplify(c2.subs(sub).subs(g,z/r0**2)-z/(1-z+z*z))==0
K,k=S.symbols('K k',positive=True)
Dr=(1/r0-g*r0)/g
Hrr=1+g*Dr**2
effective=Hrr-K*Dr**2/(k*k+K/g)
checks['finite_K_effective_kinetic']=S.simplify(effective-(Hrr*k*k+K/g)/(k*k+K/g))==0
checks['finite_K_sound']=S.simplify(1/effective-(k*k+K/g)/(Hrr*k*k+K/g))==0
root=Path(__file__).resolve().parents[3]
inputs=['ac2q_postfold_2026_11_06/coupled/time_layer_review/AUXILIARY_STRESS.md',
 'action_search_2026_11_05/AC7_charge_switch/README.md']
print(json.dumps({'base':'d7aba1da7f','input_sha256':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in inputs},
 'checks':checks,'all_pass':all(checks.values()),
 'scope':'Exact algebra; no nonlinear transfer or uniqueness verified.'},indent=2))
