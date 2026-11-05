#!/usr/bin/env python3
"""Bounded symbolic construction checks, not a full G0 health verdict."""
import argparse
import json
from pathlib import Path
import sys

import mpmath as mp
import sympy as sp

parser = argparse.ArgumentParser()
parser.add_argument('--output', required=True)
parser.add_argument('--mutate', choices=['kinetic', 'tie', 'cross'])
args = parser.parse_args()
checks = []


def check(name, passed, detail=''):
    passed = bool(passed)
    checks.append(dict(name=name, passed=passed, detail=str(detail)))
    print(f"{'PASS' if passed else 'FAIL'} {name}: {detail}", flush=True)


def exact(name, expr):
    residual = sp.simplify(expr)
    check(name, residual == 0, residual)


X, phi, b, m2, alpha, G, kap = sp.symbols('X phi b m2 alpha G kappa', positive=True)
V = m2 * phi**2 / 2
Pde = b / phi * sp.sqrt(2 * X) - V
if args.mutate == 'kinetic':
    Pde += X
rho = sp.simplify(2 * X * sp.diff(Pde, X) - Pde)
exact('A1 rho_DE equals V', rho - V)
exact('A2 homogeneous time Hessian vanishes', sp.diff(Pde, X) + 2 * X * sp.diff(Pde, X, 2))
ascale = alpha * phi**(2 if args.mutate == 'tie' else 1)
exact('A3 tie slope is one half', (sp.diff(ascale, phi) / ascale) / (sp.diff(rho, phi) / rho) - sp.Rational(1, 2))
exact('A4 exact normalization', (ascale**2 - kap**2 * G * rho).subs(alpha**2, kap**2 * G * m2 / 2))

p, a, s = sp.symbols('p a s', positive=True)
W = a**2 * (-p/a - sp.log(1-p/a))  # K W in physical units
sub = {p: a*s/(1+s)}
HL = sp.simplify(sp.diff(W, p, 2).subs(sub))
HT = sp.simplify((sp.diff(W, p)/p).subs(sub))
Waa = sp.simplify(sp.diff(W, a, 2).subs(sub))
Wpa = sp.simplify(sp.diff(W, p, a).subs(sub))
exact('B1 Legendre flux', sp.diff(W, p).subs(sub) - a*s)
exact('B2 CT14 radial Hessian', HL - (1+s)**2)
exact('B3 CT14 transverse Hessian', HT - (1+s))
exact('B4 CT14 scale Hessian', Waa - (s**2 - 2*s + 2*sp.log(1+s)))
exact('B5 CT14 cross Hessian', Wpa + s**2)
g, gb = sp.symbols('g gb', positive=True)
law = (gb + sp.sqrt(gb**2 + 4*gb*a))/2
exact('B6 spherical fixed-scale law', (g - a*g/(a+g) - gb).subs(g, law))
exact('B7 zero-field scale independence through quadratic order', sp.limit(sp.diff(W, p, p, a), p, 0))

H, Hc, M2, rb = sp.symbols('H Hc M2 rho_b', positive=True)
# With dotphi<0 the scalar equation is V_phi=3 (b/phi) H.
phi2 = 3*b*H/m2
rhoH = sp.simplify(V.subs(phi**2, phi2))
exact('C1 homogeneous rho_DE', rhoH - 3*b*H/2)
exact('C2 Friedmann constraint', (3*M2*H**2-rhoH-rb).subs(b, 2*M2*Hc) - (3*M2*(H**2-Hc*H)-rb))
rbon = 3*M2*H*(H-Hc)
Hdot = -3*H**2*(H-Hc)/(2*H-Hc)
exact('C3 baryon continuity', sp.diff(rbon, H)*Hdot + 3*H*rbon)
phidot = phi*Hdot/(2*H)
enthalpy = -b*phidot/phi
exact('C4 DE continuity on decreasing branch', sp.diff(rhoH, H)*Hdot + 3*H*enthalpy)
w = sp.simplify(enthalpy/rhoH - 1)
exact('C5 equation of state', w + H/(2*H-Hc))
deceleration = sp.simplify(-1-Hdot/H**2)
exact('C6 acceleration threshold', deceleration - (H-2*Hc)/(2*H-Hc))
# H=Hc+y with y>0 makes the branch inequalities exact.
y = sp.symbols('y', positive=True)
check('C7 decreasing field and positive enthalpy', sp.simplify((-Hdot).subs(H,Hc+y)).is_positive and sp.simplify(enthalpy.subs(H,Hc+y)).is_positive)

Upp = HL - 1  # subtract the worst longitudinal Newtonian projection
cross = (2 if args.mutate == 'cross' else 1) * Wpa
det = sp.simplify(Upp*Waa - cross**2)
D = 2*s*((s+2)*sp.log(1+s)-2*s)
exact('D1 determinant of gravity-subtracted joint Hessian', det-D)
q = sp.log(1+s)-2*s/(s+2)
exact('D2 positive derivative certificate', sp.diff(q,s)-s**2/((s+1)*(s+2)**2))
exact('D3 derivative certificate starts at zero', q.subs(s,0))
exact('D4 scale Hessian monotonic derivative', sp.diff(Waa,s)-2*s**2/(1+s))
exact('D5 zero-field scale Hessian limit', Waa.subs(s,0))
exact('D6 transverse gravity-subtracted Hessian', HT-1-s)

# Fixed-metric scalar square root: examine arbitrary spatial tilt explicitly.
u,z,C = sp.symbols('u z C', positive=True)
Lkin=C*sp.sqrt(u**2-z**2)
exact('E1 velocity Hessian at spatial tilt', sp.diff(Lkin,u,2)+C*z**2/(u**2-z**2)**sp.Rational(3,2))
exact('E2 homogeneous Hessian', sp.diff(Lkin,u,2).subs(z,0))

mp.mp.dps=80
fn=sp.lambdify(s,det,'mpmath')
positive=0
worst_identity=mp.mpf(0)
minimum=None
for j in range(65):
    sv=mp.power(10,mp.mpf(-8)+mp.mpf(j)/4)
    vdet=fn(sv)
    positive += int(vdet>0)
    minimum=vdet if minimum is None else min(minimum,vdet)
    # Independent evaluation directly in u=p/a, rather than s derivatives.
    uv=sv/(1+sv)
    wp=1/(1-uv)**2 - 1
    wa=uv**2/(1-uv)**2-2*uv/(1-uv)-2*mp.log(1-uv)
    wc=-uv**2/(1-uv)**2
    direct=wp*wa-((2 if args.mutate=='cross' else 1)*wc)**2
    worst_identity=max(worst_identity,abs(direct-vdet)/max(mp.mpf(1),abs(vdet)))
check('D7 positivity on 65 declared points',positive==65,f'{positive}/65; minimum {mp.nstr(minimum,12)}')
check('D8 independent variable evaluation',worst_identity<=mp.mpf('1e-50'),mp.nstr(worst_identity,12))

result=dict(
    assertion_tested='Exact action identities and restricted joint static Hessian, plus a 65-point corroboration; not full gravitational stability.',
    mutation=args.mutate, checks=checks,
    passed=sum(c['passed'] for c in checks), total=len(checks),
    domain={'s_min':'1e-8','s_max':'1e8','points':65,'mpmath_digits':80},
    formulas={'rho_DE':str(rho),'Hdot':str(Hdot),'w_DE':str(w),'joint_determinant':str(det)},
    gate_status={'G0':'UNDECIDED: full constraints and inhomogeneous foliation health uncomputed','G1_G2_G4':'NOT GRADED','G3':'exact identity only; specified empirical histories not graded','G5_G6_G7':'NOT GRADED'},
)
Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
print(f"Checks {result['passed']}/{result['total']}; G0 UNDECIDED")
sys.exit(0 if all(c['passed'] for c in checks) else 1)
