"""Exact finite-radius functionals; synthetic data only, never QCD samples."""
import json
import sys
from pathlib import Path
import sympy as s

out = Path(sys.argv[1])
H, m, Om = s.symbols('H m Omega', positive=True)
z = s.symbols('z')
checks = []

def check(name, actual, expected=0):
    residual = s.simplify(actual-expected)
    assert residual == 0, (name, residual)
    checks.append(name)

# Derive coefficients by independent linear systems, rather than declaring
# a polynomial and checking that the same declared roots are roots.
stress_weights = s.Matrix([[-64, 84, -21, 1]])
stress_matrix = s.Matrix([[s.Integer(2)**(j*n) for j in range(4)]
                         for n in (0, 1, 2, 4)])
stress_solved = stress_matrix.inv()*s.Matrix([0, 28, 0, 0])
check('stress weights from moment system',
      (stress_solved-stress_weights.T).norm())
P = sum(stress_weights[j]*z**j for j in range(4))
check('stress factored operator', P, (z-1)*(z-4)*(z-16))

w_weights = [1, -22, 105, -148, 64]
w_matrix = s.Matrix([[s.Integer(2)**(j*n) for j in range(5)]
                     for n in (-4, -3, -2, 0)] + [[j for j in range(5)]])
w_solved = w_matrix.inv()*s.Matrix([0, -s.Rational(49,128), 0, 0, 0])
check('W weights from moment and log system',
      (w_solved-s.Matrix(w_weights)).norm())
Q64 = sum(w_weights[j]*z**j for j in range(5))
check('W factored operator', Q64,
      64*(z-1)**2*(z-s.Rational(1,4))*(z-s.Rational(1,16)))

def stress_op(expr):
    return s.expand(sum(stress_weights[j]*expr.subs(H,2**j*H)
                        for j in range(4))/(28*H*m**3))

def w_op(expr):
    return s.expand(-s.Rational(96,49)/Om*(H/m)**3*
                    sum(w_weights[j]*expr.subs(H,2**j*H) for j in range(5)))

a0,a1,a2,a4,a6,L = s.symbols('a0 a1 a2 a4 a6 L')
f = a0+a1*H+a2*H**2+a4*H**4+L*H**4*s.log(H)+a6*H**6
rho = s.expand(f-H*s.diff(f,H)/4)
W = Om*H**(-4)*f
# Derivative-derived stress and generating function are separate inputs.
check('synthetic stress coefficient and leading bias',stress_op(rho),
      s.Rational(3,4)*a1/m**3-3240*a6*H**5/m**3)
check('synthetic W coefficient and leading bias',w_op(W),
      s.Rational(3,4)*a1/m**3-s.Rational(116640,7)*a6*H**5/m**3)
for n in (0,2,4):
    check('stress kills local power '+str(n),stress_op(H**n))
for n in (-4,-2,0):
    check('W kills local power '+str(n),w_op(H**n))
check('W kills anomaly log',w_op(s.log(H)))
check('stress retains true linear term',stress_op(H),1/m**3)
check('W retains free energy linear term',w_op(Om/H**3),s.Rational(3,4)/m**3)
check('stress H6 bias',stress_op(H**6),6480*H**5/m**3)
check('stress H4 log bias',stress_op(H**4*s.log(H)),
      s.Rational(720,7)*s.log(2)*H**3/m**3)
check('common W normalization invariant',w_op(s.Integer(1)))
check('stress covariance independent equal-error weight',
      sum(x*x for x in stress_weights),11594)
check('stress remainder l1 coefficient',sum(abs(x) for x in stress_weights),170)
check('W remainder l1 coefficient',sum(abs(x) for x in w_weights),340)

u,lam,A,B,C = s.symbols('u lam A B C')
# Test matched derivative using a distinct explicit family, not the same
# formal chain rule rewritten. Flat calibration M=lam+u*lam^2; W has
# local and nonlocal pieces. Evaluate d/du at zero on lam(u)=M-uM^2+O(u^2).
M = s.symbols('M',positive=True)
wf = Om/H**4*(A*lam**4+B*u*lam**3*H+C*lam**3*H)
tangent = s.diff(wf,u)-lam**2*s.diff(wf,lam)
explicit = s.diff(wf.subs(lam,M-u*M**2),u).subs(u,0)
check('matched tangent explicit calibration',tangent.subs({u:0,lam:M}),explicit)
check('local matching term annihilated at every radius',
      w_op(explicit),s.Rational(3,4)*(B*M**3-3*C*M**4)/m**3)

result = {'assertion_tested':'Exact moment-system weights, local/log cancellations, bias and matched-tangent identities for declared analytic families; no QCD data',
          'check_count':len(checks),'checks':checks,'stress_weights':list(stress_weights),
          'partition_weights':w_weights,'status':'all exact symbolic residuals zero',
          'physical_R_computed':False,'alpha_fitted':False}
out.write_text(json.dumps(result,indent=2,default=str)+'\n')
print(json.dumps({'check_count':len(checks),'status':result['status']}))
