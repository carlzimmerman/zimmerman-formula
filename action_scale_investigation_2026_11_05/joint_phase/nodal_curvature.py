"""Minimal leaf-Dirac threshold matching; no numerical parameter selection."""
import argparse
import json
from pathlib import Path
import sympy as s

ap = argparse.ArgumentParser()
ap.add_argument('--out', required=True)
ap.add_argument('--mutate', action='store_true')
args = ap.parse_args()
m, nu, ds, cutoff, h, sigma, mass, q2 = s.symbols(
    'm nu d_s Lambda h sigma M q2', positive=True)
x, y = s.symbols('x y', real=True)
checks = {}

def check(name, expr):
    ok = s.simplify(expr) == 0
    checks[name] = ok
    print(('PASS ' if ok else 'FAIL ')+name, flush=True)

pref = nu*ds/(2*(4*s.pi)**s.Rational(3, 2))
U = pref*s.gamma(-s.Rational(3, 2))*m**3
eR = -pref*s.gamma(-s.Rational(1, 2))*m/12
F = (2 if args.mutate else -2)*eR
check('finite positive cubic energy', U-nu*ds*m**3/(12*s.pi))
check('Euclidean curvature coefficient', eR-nu*ds*m/(96*s.pi))
check('Lorentz curvature sign and coefficient', F+nu*ds*m/(48*s.pi))
I1 = 2*cutoff*s.exp(-m*m/cutoff**2)-2*s.sqrt(s.pi)*m*s.erfc(m/cutoff)
I0 = 2*cutoff**3*s.exp(-m*m/cutoff**2)/3-2*m*m*I1/3
check('proper time integrals derivative relation', s.diff(I0, m)+2*m*I1)
Fcut = pref*I1/6
check('cutoff curvature response decreases with mass',
      s.diff(Fcut, m)+nu*ds*s.erfc(m/cutoff)/(48*s.pi))
Fdiv = nu*ds*cutoff/(48*s.pi**s.Rational(3, 2))
Udiv = nu*ds*(cutoff**3/24-m*m*cutoff/8)/s.pi**s.Rational(3, 2)
check('finite curvature extracted from cutoff', s.limit(Fcut-Fdiv, cutoff, s.oo)-F)
check('finite vacuum extracted from cutoff', s.limit(pref*I0-Udiv, cutoff, s.oo)-U)

# Dimensional regularization of the two-point function in three dimensions.
def loop_integral(power):
    return s.gamma(power-s.Rational(3, 2))/(
        (4*s.pi)**s.Rational(3, 2)*s.gamma(power))*mass**(3-2*power)

bubble_integrand = nu*ds*(2*mass**2*loop_integral(2)-loop_integral(1))
check('Dirac numerator and loop integral', bubble_integrand-nu*ds*mass/(2*s.pi))
bubble_q = bubble_integrand.subs(mass, s.sqrt(m*m+x*(1-x)*q2))
Pi0 = s.integrate(bubble_q.subs(q2, 0), (x, 0, 1))
Zm = s.integrate(s.diff(bubble_q, q2).subs(q2, 0), (x, 0, 1))
check('zero momentum bubble equals vacuum Hessian', Pi0-s.diff(U, m, 2))
check('induced mass kinetic coefficient', Zm-nu*ds/(24*s.pi*m))
D = s.simplify(F.subs(m, h*sigma)/sigma)
CA = s.simplify(3*U.subs(m, h*sigma)/sigma**3)
Zsigma = s.simplify(h*h*Zm.subs(m, h*sigma))
check('joint cubic curvature matching', D+CA/(12*h*h))
check('joint kinetic curvature matching', Zsigma+2*D/sigma)

# Compute R from the metric, not from the proposed warped-curvature formula.
a = s.Function('a')(y)
g = s.diag(a*a, a*a, a*a, 1)
gi = g.inv()
def partial(expr, index):
    return s.diff(expr, y) if index == 3 else s.S.Zero
Gamma = [[[s.simplify(sum(gi[i,k]*(partial(g[k,j],l)+partial(g[k,l],j)
           -partial(g[j,l],k)) for k in range(4))/2)
           for l in range(4)] for j in range(4)] for i in range(4)]
Ric = [[s.simplify(sum(partial(Gamma[k][i][j], k)-partial(Gamma[k][i][k], j)
        +sum(Gamma[k][k][l]*Gamma[l][i][j]-Gamma[k][j][l]*Gamma[l][i][k]
             for l in range(4)) for k in range(4))) for j in range(4)] for i in range(4)]
R4 = s.simplify(sum(gi[i,j]*Ric[i][j] for i in range(4) for j in range(4)))
check('warped full curvature from connection', R4+6*s.diff(a,y,2)/a+6*s.diff(a,y)**2/a**2)
check('integrated curvature modulo boundary derivative',
      a**3*R4+s.diff(6*a*a*s.diff(a,y),y)-6*a*s.diff(a,y)**2)
eps = s.symbols('epsilon', positive=True)
atest = 1+eps*s.cos(y)
periodic = s.integrate(6*atest*s.diff(atest,y)**2,(y,0,2*s.pi))
check('periodic metric nonzero Einstein action', periodic-6*s.pi*eps**2)

result = {
    'passed': all(checks.values()),
    'mode': 'reverse_curvature_Wick_sign' if args.mutate else 'main',
    'checks': checks,
    'results': {'finite_U':str(U), 'finite_F_leaf':str(F),
                'C_A':str(CA), 'D_leaf':str(D), 'Z_sigma':str(Zsigma),
                'warped_R4':str(R4)},
    'scope':'Minimal parity-even leaf Dirac determinant, small external '
            'momentum and curvature relative to positive mass. Not a four-dimensional '
            'Einstein matching or a full MOND response.'}
Path(args.out).parent.mkdir(parents=True, exist_ok=True)
Path(args.out).write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(0 if result['passed'] else 1)
