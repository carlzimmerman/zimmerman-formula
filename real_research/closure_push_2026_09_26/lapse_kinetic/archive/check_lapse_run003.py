#!/usr/bin/env python3
"""Exact frozen scalar trace/lapse degeneracy and conserved-source response."""
import argparse
import json
from pathlib import Path
import sympy as S

ap = argparse.ArgumentParser()
ap.add_argument('--output', required=True)
args = ap.parse_args()
checks = {}

def exact(name, expression):
    value = S.factor(S.cancel(expression))
    checks[name] = {'residual': str(value), 'passed': value == 0}
    assert value == 0, (name, value)
    print('PASS '+name, flush=True)

E, z, r, s, B, q, w, R = S.symbols('E zeta r s B q omega R', real=True)
p, f, u, be, dp, df, du, dR = S.symbols('psi phi U beta dpsi dphi dU dR', real=True)
T = 2 + 3*B
kap = 2*T/B
W = r*du+s*df
K = 3*dp-be
L = (-6*dp**2+4*be*dp-B*K**2-2*T*K*W-3*T*W**2
     +2*p**2-4*f*p+E*f**2-z*(u+f)**2)
a = S.Matrix([1,s,r])
A = S.Matrix([[2,-2,0],[-2,E-z,-z],[0,-z,-z]])
Ai = A.inv()
ep = S.Matrix([1,0,0])
ef = S.Matrix([0,1,0])
h = S.factor((a.T*Ai*a)[0])
D = E*(z-2*r*r)+2*r*r*z+4*r*r-4*r*(s+1)*z+2*z*s*s+4*z*s
exact('inverse_static_matrix', (A*Ai-S.eye(3)).norm()**2)
exact('trace_shift_reduction', L.subs(be,kap*(dp+W)/2)-kap*(dp+W)**2-(S.Matrix([p,f,u]).T*A*S.Matrix([p,f,u]))[0])
exact('source_shift_reduction',
      (L+be*dR).subs(be,kap*(dp+W)/2+dR/(2*B))
      -(kap*(dp+W)**2+kap*(dp+W)*dR/2+dR**2/(4*B)
        +(S.Matrix([p,f,u]).T*A*S.Matrix([p,f,u]))[0]))
exact('static_schur_denominator', h-D/(2*z*(E-2)))
exact('scalar_speed', -1/(kap*h)-2*z*(2-E)/(kap*D))
exact('old_r_denominator', D.subs(s,0)-(E*(z-2*r*r)+2*r*r*z+4*r*r-4*r*z))

# Fourier convention d/dt=-i omega, k=1, q=omega^2; homogeneous k restored in report.
src = kap*q*a/2-q*ep-ef
ax = S.factor((a.T*Ai*src)[0])
x = (-R*(Ai*src-kap*q*Ai*a*ax/(1+kap*q*h))/2).applyfunc(lambda value:S.factor(S.cancel(value)))
beta = -S.I*w*(kap*(a.T*x)[0]/2+R/(2*B))
xw = x.subs(q,w*w)
betaw = beta.subs(q,w*w)
derivative = -S.I*w
eom = [S.diff(L,p)-derivative*S.diff(L,dp)-w*w*R,
       S.diff(L,f)-derivative*S.diff(L,df)-R,
       S.diff(L,u)-derivative*S.diff(L,du),
       S.diff(L,be)+derivative*R]
fields = S.Matrix([p,f,u])
beta_fields = derivative*(kap*(a.T*fields)[0]/2+R/(2*B))
subs = {be:beta_fields,dp:derivative*p,df:derivative*f,du:derivative*u}
reduced_eom = 2*(A+kap*w*w*a*a.T)*fields+R*src.subs(q,w*w)
for idx, equation in enumerate(eom):
    exact('original_four_field_eom_'+str(idx), equation.subs(subs)-(reduced_eom[idx] if idx<3 else 0))
for idx in range(3):
    exact('explicit_source_solution_'+str(idx), (2*(A+kap*q*a*a.T)*x+R*src)[idx])
transfer = S.factor(-((src.T*Ai*src)[0]-kap*q*ax**2/(1+kap*q*h))/2+q/(2*B))
exact('tidal_observable_from_physical_metric',
      (-xw[1]-derivative*betaw-w*w*xw[0])/R-transfer.subs(q,w*w))
exact('single_reduced_pole', (A+kap*q*a*a.T).det()-A.det()*(1+kap*q*h))
# Divide by the known linear pole denominator explicitly.  Generic polynomial
# long division over five symbolic coefficients exceeded the prior CPU cap.
den = 1+kap*q*h
num = S.expand(den*(-(src.T*Ai*src)[0]/2+q/(2*B))+kap*q*ax**2/2)
coeffs = [S.factor(num.coeff(q,idx)) for idx in range(4)]
c2 = S.factor(coeffs[3]/(kap*h))
c1 = S.factor((coeffs[2]-c2)/(kap*h))
c0 = S.factor((coeffs[1]-c1)/(kap*h))
remainder = S.factor(coeffs[0]-c0)
quotient=c2*q*q+c1*q+c0
exact('contact_polynomial_division', num-den*quotient-remainder)
exact('dangerous_contact_coefficient', c2-(E*r*r-z*(r-s)**2)/(2*D))
exact('static_physical_gain', x[1].subs(q,0)/(-R/4)-2/(2-E))
exact('static_no_slip', (x[0]-x[1]).subs(q,0))
exact('static_auxiliary', (x[2]+x[1]).subs(q,0))
exact('contact_cancellation_locus', D.subs(z,E*r*r/(r-s)**2)-r*r*(E-2*(r-s))**2/(r-s)**2)
exact('contact_free_speed', (2*z*(2-E)/(kap*D)).subs(z,E*r*r/(r-s)**2)-2*E*(2-E)/(kap*(E-2*(r-s))**2))
exact('positive_candidate_speed', (2*z*(2-E)/(kap*D)).subs({r:1,s:2,z:E,B:1})-E*(2-E)/(5*(E+2)**2))
exact('positive_candidate_bound_identity', S.Rational(1,40)-E*(2-E)/(5*(E+2)**2)-(3*E-2)**2/(40*(E+2)**2))
exact('positive_candidate_static_mode', (a.T*x)[0].subs({q:0,r:1,s:2})-2*x[1].subs(q,0))
wrong = S.factor(c2.subs({E:-1,z:S.Rational(1,4),r:1,s:2}))
assert wrong != 0
checks['negative_control_uncancelled_contact'] = {'value':str(wrong),'passed':True}
result = {
    'result':'Exact general r,s trace-lapse source transfer and one-pole regular branch',
    'checks':checks,
    'D':str(D),
    'h':str(h),
    'speed_squared':str(2*z*(2-E)/(kap*D)),
    'transfer':str(transfer),
    'polynomial_coefficients':{'c2':str(c2),'c1':str(c1),'c0':str(c0)},
    'pole_remainder':str(S.factor(remainder/den)),
    'negative_E_conclusion':'For E<0, kappa>0, zeta*D!=0, c2=0 implies negative speed squared; algebraic case split in REPORT.md.',
    'positive_E_candidate':'0<E<2, r=1, s=2, zeta=E, B=1: static v=2phi and 0<cs2<=1/40; only planar conserved generator contact test.',
    'non_claims':['No nonlinear constraint count or full background solution',
                  'No general 3D source causal-support theorem or PPN pass',
                  'No isotropic coefficient realization of direction-dependent E_i',
                  'No covariance claim after omitting shift/background-gradient terms']}
Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
