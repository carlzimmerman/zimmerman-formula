"""Exact identities for the frozen linear induced-coupling construction."""
import argparse
import json
from pathlib import Path
import sympy as s

parser = argparse.ArgumentParser()
parser.add_argument('--out', required=True)
parser.add_argument('--mutate', action='store_true')
args = parser.parse_args()
q, p, q0, D, A, B, Z, U0, F0, R = s.symbols(
    'sigma p sigma0 D C_A C_B Z U0 F0 R', positive=True)
r = s.sqrt(q*q+p*p)
F = D*r
U = U0+A*r**3/3+B*p**3/3
fv, uv = F.subs(p, 0), U.subs(p, 0)
checks = {}

def check(name, difference):
    ok = s.simplify(difference) == 0
    checks[name] = ok
    print(('PASS ' if ok else 'FAIL ')+name, flush=True)

def vac(expr):
    return s.simplify(expr.subs(q, q0).subs(U0, A*q0**3/6).subs(F0, D*q0))

check('homogeneous scalar Einstein stationarity',
      vac(s.diff(uv, q)-2*s.diff(fv, q)*uv/fv))
energy = vac(uv)
check('positive vacuum energy identity', energy-A*q0**3/2)
VE = F0**2*uv/fv**2
KE = F0*(Z/fv+s.Rational(3, 2)*(s.diff(fv, q)/fv)**2)
check('Einstein frame stationarity', vac(s.diff(VE, q)))
check('Einstein frame potential curvature', vac(s.diff(VE, q, 2))-A*q0)
used_kinetic = Z if args.mutate else vac(KE)
expected_kinetic = Z+3*D/(2*q0)
check('scalar metric kinetic contribution', used_kinetic-expected_kinetic)
mass = vac(s.diff(VE, q, 2))/used_kinetic
check('canonical scalar mass', mass-A*q0/expected_kinetic)
H2 = energy/(3*D*q0)
check('Hubble scale', H2-A*q0*q0/(6*D))
check('scalar cannot have a large Compton hierarchy',
      mass/H2-6*D/(Z*q0+3*D/2))
# Positive expression proves m^2/H^2<4 for positive Z; equality at Z=0.
check('exact positive gap below hierarchy bound',
      4-mass/H2-4*Z*q0/(Z*q0+3*D/2))
charge_numerator = vac(F0*s.diff(s.log(s.sqrt(F0/fv)), q)**2)
alpha2 = charge_numerator/used_kinetic
check('Jordan matter scalar charge', alpha2-D/(4*Z*q0+6*D))
check('mass and scalar charge identity', mass/H2-24*alpha2)
radial_derivative = s.diff(U-F*R/2, q)
check('fixed curvature radial stationarity',
      radial_derivative-q*(A*r-D*R/(2*r)))
rstar = s.sqrt(D*R/(2*A))
reduced = U0+A*rstar**3/3-D*R*rstar/2+B*p**3/3
check('fixed curvature quadratic response vanishes',
      s.diff(reduced, p, 2).subs(p, 0))
check('fixed curvature cubic coefficient', s.diff(reduced, p, 3)/2-B)
K = 1/(2*D*q0)
G_tensor = 1/(8*s.pi*D*q0)
a_held = 1/(K*B)
ratio = a_held**2/(G_tensor*energy)
check('condensate cancels from tensor ratio', ratio-64*s.pi*D**3/(A*B**2))
check('vacuum offset changes condensate but not tensor ratio', s.diff(ratio, q0))
result = {
    'passed': all(checks.values()),
    'mode': 'omit_conformal_kinetic' if args.mutate else 'main',
    'checks': checks,
    'results': {
        'vacuum_energy': str(energy), 'mass_squared': str(mass),
        'H_squared': str(H2), 'scalar_charge_squared': str(alpha2),
        'kappa_tensor_squared': str(s.simplify(ratio))},
    'scope': 'Homogeneous scalar-tensor vacuum and fixed-curvature response; '
             'not an operational MOND prediction or a microscopic coefficient.'}
Path(args.out).parent.mkdir(parents=True, exist_ok=True)
Path(args.out).write_text(json.dumps(result, indent=2)+'\n')
raise SystemExit(0 if result['passed'] else 1)
