"""Exact geometry checks; no proposed matter realization is assumed."""
import json
import math
import sys
from pathlib import Path
import sympy as s

out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=False)
checks = []

def zero(label, expr):
    value = s.simplify(expr)
    assert value == 0, (label, value)
    checks.append(label)

# Arbitrary local gradient J_ij=partial_i beta_j.
J = s.Matrix(3, 3, s.symbols('j0:9'))
K = (J + J.T) / 2
A = sum(q*q for q in J)
B = s.trace(J*J)
curl2 = (J[1,2]-J[2,1])**2 + (J[2,0]-J[0,2])**2 + (J[0,1]-J[1,0])**2
zero('curl norm identity', curl2-(A-B))
zero('divergence plus curl decomposition', s.trace(K)**2-s.trace(K*K)-(s.trace(J)**2-B-curl2/2))
fx, fy, fz, v = s.symbols('fx fy fz v', real=True)
Jz = s.Matrix([[0,0,-v*fx],[0,0,-v*fy],[0,0,-v*fz]])
Kz = (Jz+Jz.T)/2
zero('directed bubble ADM density', s.trace(Kz)**2-s.trace(Kz*Kz)+v*v*(fx*fx+fy*fy)/2)

# Independent 4D Ricci calculation for ds2=-dt2+dx2+dy2+(dz+b(x)dt)^2.
t,x,y,z = s.symbols('t x y z', real=True)
coords = (t,x,y,z)
b = s.Function('b')(x)
g = s.Matrix([[-1+b*b,0,0,b],[0,1,0,0],[0,0,1,0],[b,0,0,1]])
gi = s.simplify(g.inv())
Gamma = [[[s.simplify(sum(gi[a,d]*(s.diff(g[d,c],coords[q])+s.diff(g[d,q],coords[c])-s.diff(g[q,c],coords[d])) for d in range(4))/2) for c in range(4)] for q in range(4)] for a in range(4)]
Ric = s.zeros(4)
for a in range(4):
    for q in range(4):
        Ric[a,q] = s.simplify(sum(s.diff(Gamma[d][a][q],coords[d])-s.diff(Gamma[d][a][d],coords[q])+sum(Gamma[d][d][e]*Gamma[e][a][q]-Gamma[d][q][e]*Gamma[e][a][d] for e in range(4)) for d in range(4)))
scalar = s.simplify(sum(gi[a,q]*Ric[a,q] for a in range(4) for q in range(4)))
Ein = s.simplify(Ric-g*scalar/2)
n = s.Matrix([1,0,0,-b])
zero('normal unit timelike', (n.T*g*n)[0]+1)
zero('4D Einstein vs ADM density', (n.T*Ein*n)[0]+s.diff(b,x)**2/4)

# Exact compact C2 plateau/transition/exterior profile.
u = s.symbols('u', real=True)
f = 1-10*u**3+15*u**4-6*u**5
for endpoint, expected in [(0,1),(1,0)]:
    zero('profile value '+str(endpoint), f.subs(u,endpoint)-expected)
    for order in (1,2):
        zero('profile derivative '+str((endpoint,order)), s.diff(f,u,order).subs(u,endpoint))
IoverR = s.integrate((u+1)**2*s.diff(f,u)**2/2,(u,0,1))
p = s.Poly(s.expand((u+1)**2*s.diff(f,u)**2/2),u)
manual = sum(coef/s.Integer(power[0]+1) for power,coef in p.terms())
zero('radial integral independent monomial sum', IoverR-manual)
theta = s.symbols('theta', real=True)
zero('angular transverse gradient integral', 2*s.pi*s.integrate(s.sin(theta)**3,(theta,0,s.pi))-8*s.pi/3)
coeff = s.simplify(IoverR/12)
assert coeff > 0
checks.append('compact energy coefficient positive')

# Canonical scalar and positive vacuum cannot supply negative T(n,n).
dotphi, grad2, potential, rhovac = s.symbols('dotphi grad2 potential rhovac', nonnegative=True)
rho_scalar = (dotphi**2+grad2)/2+potential
assert rho_scalar.is_nonnegative
checks.append('canonical scalar nonnegative under stated potential hypothesis')
zero('vacuum Tnn', -rhovac*(-1)-rhovac)

c = 299792458.0
G = 6.67430e-11
rows = []
for radius in (1.0,10.0,100.0):
    for speed in (1.0,1000.0,1e6,c/2):
        energy = -float(coeff)*c**4/G*(speed/c)**2*radius
        assert energy < 0 and math.isfinite(energy)
        checks.append('negative illustrative integral R='+str(radius)+' speed='+str(speed))
        rows.append({'R_m':radius,'speed_m_s':speed,'integral_rho_J':energy,'signed_mass_equivalent_kg':energy/c**2})
result = {'claim':'CGD-001','checks_passed':len(checks),'I_over_R':str(IoverR),'compact_coefficient':str(coeff),'Einstein_Gnn':str(s.simplify((n.T*Ein*n)[0])),'illustrations':rows,'interpretation':'Slice integral of required Eulerian density, NOT ADM energy, fuel cost or universal lower bound.'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(result,indent=2))
