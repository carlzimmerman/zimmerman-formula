"""Exact free-band neutrality identities and independent occupation quadrature."""
import argparse
import json
import math
import sympy as s
from scipy.integrate import quad

checks = []
def check(name, condition):
    checks.append({'name': name, 'passed': bool(condition)})

m, z, v, nu, E = s.symbols('m z v nu E', positive=True)
vac = nu*m**3/(6*s.pi*v**2)
occupied = -nu/(2*s.pi*v**2)*s.integrate(E*(z-E), (E,m,z))
metal = -nu*z**3/(12*s.pi*v**2)+nu*z*m**2/(4*s.pi*v**2)
check('cubic cancels for m below zeta', s.simplify(vac+occupied-metal)==0)
check('potential continuous at threshold', s.simplify((metal-vac).subs(m,z))==0)
check('first mass derivative continuous', s.simplify(s.diff(metal-vac,m).subs(m,z))==0)
check('density', s.simplify(-s.diff(metal,z)-nu*(z*z-m*m)/(4*s.pi*v*v))==0)
check('deep metallic cubic derivative vanishes', s.diff(metal,m,3)==0)

I=s.eye(2)
x=s.Matrix([[0,1],[1,0]])
y=s.Matrix([[0,-s.I],[s.I,0]])
zz=s.diag(1,-1)
kron=s.kronecker_product
gx,gy=kron(x,I),kron(y,I)
mass=[kron(zz,a) for a in (x,y,zz)]
U=kron(y,y)
def theta(A): return s.simplify(U*A.conjugate()*U.H)
check('time reversal square plus one', U*U.conjugate()==s.eye(4))
check('time reversal flips kinetic matrices', all(theta(A)==-A for A in (gx,gy)))
check('time reversal preserves all polarization masses', all(theta(A)==A for A in mass))
check('time reversal excludes singlet gap', theta(kron(zz,I))==-kron(zz,I))
check('time reversal permits identity chemical potential', theta(s.eye(4))==s.eye(4))
check('central product is real minus identity', gx*gy*mass[0]*mass[1]*mass[2]==-s.eye(4))

rows=[]
for mass_value in (0.0,0.2,0.8,1.0,1.5):
    speed=0.3
    kf=math.sqrt(max(0,1-mass_value**2))/speed
    correction=quad(lambda k: -2/(2*math.pi)*k*(1-math.sqrt(speed**2*k*k+mass_value**2)),0,kf,epsabs=1e-13,epsrel=1e-13)[0]
    numerical=2*mass_value**3/(6*math.pi*speed**2)+correction
    expected=(-2/(12*math.pi*speed**2)+2*mass_value**2/(4*math.pi*speed**2)) if mass_value<1 else 2*mass_value**3/(6*math.pi*speed**2)
    residual=abs(numerical-expected)
    check('momentum occupation integral m='+str(mass_value), residual<1e-11)
    rows.append({'m':mass_value,'grand_potential':numerical,'absolute_residual':residual})

parser=argparse.ArgumentParser()
parser.add_argument('--output',required=True)
args=parser.parse_args()
with open(args.output,'w') as f:
    json.dump({'checks':checks,'passed':all(c['passed'] for c in checks),'quadrature':rows},f,indent=2)
print(str(sum(c['passed'] for c in checks))+'/'+str(len(checks))+' checks passed')
raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
