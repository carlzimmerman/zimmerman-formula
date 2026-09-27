#!/usr/bin/env python3
"""Independent response/inertia construction identities, with exact scope."""
import argparse
import json
from pathlib import Path
import sympy as s

parser = argparse.ArgumentParser()
parser.add_argument('--output', required=True)
args = parser.parse_args()
checks = {}

def exact(name, value):
    residual = s.factor(s.simplify(value))
    checks[name] = {'residual': str(residual), 'passed': residual == 0}
    assert residual == 0, (name, residual)

k, P, Q, A, B, J, H, Z = s.symbols('k P Q A B J H Z', real=True)
ps, ph, u, be, dp, du, source = s.symbols('ps ph u be dp du source', real=True)
L = (-6*dp**2 + 4*k**2*be*dp + 2*k**2*ps**2 - 4*k**2*ph*ps
     + 2*P*k**2*(u-ph)**2 + 2*Q*k**2*u**2
     - B*(3*dp-k**2*be)**2 + A*k**2*ph**2)
E = A+2*P*Q/(P+Q)
aux = s.solve([s.diff(L, z) for z in [ph, u, be]], [ph, u, be], dict=True)[0]
Kscalar = 2*(2+3*B)/B
exact('minimal_reduced_action', L.subs(aux) - (Kscalar*dp**2-2*k**2*(2-E)/E*ps**2))
Lstatic = L.subs({dp: 0, be: 0})-source*ph
static = s.solve([s.diff(Lstatic, z) for z in [ph, ps, u]], [ph, ps, u], dict=True)[0]
exact('independent_static_no_slip', static[ps]-static[ph])
exact('independent_static_gain', static[ph]/(-source/(4*k**2))-2/(2-E))
mu = s.symbols('mu', nonzero=True)
exact('matching_E', (2/(2-s.Symbol('ee'))).subs('ee', 2*(1-mu))-1/mu)
Lext = L + J*du**2 + H*dp*du + 4*Z*k**2*be*du
aux2 = s.solve([s.diff(Lext, z) for z in [ph, be]], [ph, be], dict=True)[0]
red2 = s.expand(Lext.subs(aux2))
K = s.Matrix([[s.factor(s.diff(red2, aa, bb)/2) for bb in [dp, du]] for aa in [dp, du]])
V = -s.Matrix([[s.factor(s.diff(red2, aa, bb)/(2*k**2)) for bb in [ps, u]] for aa in [ps, u]])
Kexpected = s.Matrix([[Kscalar, H/2+2*Z*(2+3*B)/B], [H/2+2*Z*(2+3*B)/B, J+4*Z**2/B]])
for i in range(2):
    for j in range(2):
        exact(f'kinetic_matrix_{i}{j}', K[i,j]-Kexpected[i,j])
direction = s.Matrix([1, -V[0,1]/V[1,1]])
exact('unchanged_negative_potential_direction', (direction.T*V*direction)[0]-2*(2-E)/E)
x, a0, r = s.symbols('x a0 r', positive=True)
F = 4*a0**2*(1-(1+x)*s.exp(-x))
Gexp = x**2+2*(1+x)*s.exp(-x)-2
exact('nonlinear_primitive_matches_AQUAL', -2*a0**2*x**2+F+2*a0**2*Gexp)
ET = s.diff(F, x)/(2*a0**2*x)
EL = s.diff(F, x, 2)/(2*a0**2)
exact('transverse_full_jet', ET-2*s.exp(-x))
exact('longitudinal_full_jet', EL-2*(1-x)*s.exp(-x))
exact('radial_integrability', EL-ET-x*s.diff(ET,x))
ee, zz = s.symbols('E zeta', real=True)
Lint = (-6*dp**2+4*k**2*be*dp+2*k**2*ps**2-4*k**2*ph*ps
        +ee*k**2*ph**2-zz*k**2*(u+ph)**2-B*(3*dp-k**2*be)**2+J*du**2)
aux3 = s.solve([s.diff(Lint,z) for z in [ph,be]], [ph,be], dict=True)[0]
red3 = s.expand(Lint.subs(aux3))
Kv = s.Matrix([[s.factor(s.diff(red3,aa,bb)/2) for bb in [dp,du]] for aa in [dp,du]])
Vv = -s.Matrix([[s.factor(s.diff(red3,aa,bb)/(2*k**2)) for bb in [ps,u]] for aa in [ps,u]])
Vwant = s.Matrix([[4/(ee-zz)-2, 2*zz/(ee-zz)], [2*zz/(ee-zz), zz*ee/(ee-zz)]])
for i in range(2):
    for j in range(2):
        exact(f'integrated_potential_{i}{j}', Vv[i,j]-Vwant[i,j])
        exact(f'constant_kinetic_witness_{i}{j}', Kv[i,j].subs({B:s.Rational(2,5),J:16})-16*(i==j))
exact('integrated_potential_determinant', Vv.det()-2*zz*(2-ee)/(ee-zz))
exact('causal_complement_determinant', (16*s.eye(2)-Vv).det().subs(zz,s.Rational(1,4))-54*(21*ee-10)/(4*ee-1))
exact('causal_complement_first_minor', (16-Vv[0,0]).subs(zz,s.Rational(1,4))-(18-16/(4*ee-1)))
negative_E = -2/s.exp(2)
negative_direction = s.simplify((2*(2-ee)/ee).subs(ee,negative_E))
assert negative_direction.is_negative
checks['high_x_negative_control'] = {'quadratic_form':str(negative_direction),'passed':True}
endpoints = {name: {'equation':'2(1-x)exp(-x)='+str(val), 'x_exact':str(1-s.LambertW(val*s.E/2)),
                    'x_approx':float(1-s.LambertW(val*s.E/2))}
             for name,val in [('unit_speed',s.Rational(10,21)),('lapse_schur',s.Rational(1,4)),('response_turnover',s.Integer(0))]}
result = {'result':'exact same-action matching, kinetic-only obstruction and integrated low-x candidate identities verified',
          'checks':checks, 'minimal':{'E':str(E),'kinetic':str(Kscalar),'gain':'2/(2-E)','speed_squared':'B*(2-E)/((2+3B)*E)'},
          'derivative_extension':{'K':str(K),'V':str(V),'negative_direction':'(1,-V12/V22)'},
          'integrated_candidate':{'F':str(F),'ET':str(ET),'EL':str(EL),'V':str(Vv),'K':'16 I','endpoints':endpoints},
          'non_claims':['Only stated frozen principal blocks, not full covariant canonical closure',
                        'Low-x candidate has two scalar modes and no PPN/full-spec pass',
                        'No global no-go for derivative changes that also alter constraints or static geometry']}
dest=Path(args.output);dest.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
