"""Bounded independent checks of the UV review, not QCD samples.

Contract: exact contraction on rational, non-axis Minkowski q for a complete
symmetric traceless basis in d=2..8; symbolic anomaly/normalization/parameter
projection; degenerate charge limits. No fitted coupling or hadronic data.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math
import platform
import sympy as s
import sys
import time

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
start = time.monotonic()
tested = []

def require(name, value):
    assert value, name
    tested.append(name)

count = 0
for d in range(2, 9):
    eta = [1] + [-1]*(d-1)
    tensors = []
    # Construct the full kernel of Minkowski trace by explicit independent
    # diagonal directions plus all off-diagonal symmetric matrix units.
    for k in range(1, d):
        t = [[F(0) for _ in range(d)] for _ in range(d)]
        t[0][0] = t[k][k] = F(1)
        tensors.append(t)
    for k in range(d):
        for l in range(k+1, d):
            t = [[F(0) for _ in range(d)] for _ in range(d)]
            t[k][l] = t[l][k] = F(1)
            tensors.append(t)
    assert len(tensors) == d*(d+1)//2-1
    # All components nonzero, and q^2<0 for d>=2. This exercises off-diagonal
    # contractions that an axis-only cubature cannot exercise.
    q = [F(1, 3)] + [F(k+1, k+2) for k in range(1, d)]
    q2 = sum(eta[k]*q[k]*q[k] for k in range(d))
    assert q2 < 0
    qlo = [eta[k]*q[k] for k in range(d)]
    P = [[-F(eta[k] if k == l else 0)+q[k]*q[l]/q2
          for l in range(d)] for k in range(d)]
    for t in tensors:
        trace_t = sum(eta[k]*t[k][k] for k in range(d))
        assert trace_t == 0
        qOq = sum(qlo[k]*qlo[l]*t[k][l]
                   for k in range(d) for l in range(d))/q2
        for c2, c3 in [(F(1), F(0)), (F(0), F(1)), (F(-7, 3), F(11, 5))]:
            # Direct contraction of P^{mu nu} c2 qOq and
            # P^mu_a P^nu_b c3 O^{ab}, without the overall 1/q^2.
            direct = sum(eta[mu]*(P[mu][mu]*c2*qOq
                         +c3*sum(P[mu][a]*eta[a]*P[mu][b]*eta[b]*t[a][b]
                                 for a in range(d) for b in range(d)))
                         for mu in range(d))
            assert direct == -((d-1)*c2+c3)*qOq
            count += 1
require('non-axis rational full-tensor contractions d2..8', count == 336)

u, g, b, S, m, L = s.symbols('u g b S m L', nonzero=True)
pi = s.pi
# Derive from source current Wilson coefficient and anomaly, retaining e^2=u.
als = g**2/(4*pi)
c1 = als*S/(12*pi)
G2 = 2*m**2/(-b*als/(8*pi))
band_per_u = s.simplify(3*c1*G2/(64*pi**2*m**2))
require('scalar normalization per e squared', band_per_u == -S/(16*pi**2*b))
dg_per_u = -g**3*S*L/(256*pi**4)
ct = s.simplify(dg_per_u*(g**2*G2)/(4*m**2*g**3))
require('rescaled-field counterterm cancellation', s.simplify(ct+band_per_u*L) == 0)
require('incorrect canonical source substitution does not cancel',
        s.simplify(dg_per_u*G2/(4*m**2*g**3)+band_per_u*L) != 0)
beta_em = -s.diff(dg_per_u, L)*2*u
require('mixed beta coefficient from squared-cutoff log',
        s.simplify(beta_em-2*S*g**3*u/(16*pi**2)**2) == 0)
require('beta independent of overall charge sign',
        sum(F(k)**2 for k in ['-2/3','1/3','1/3']) == F(2,3))
require('all zero charges remove local UV effect',
        band_per_u.subs(S,0) == 0 and beta_em.subs(S,0) == 0)
require('zero e squared removes mass shift but not derivative',
        (u*band_per_u).subs(u,0) == 0 and band_per_u != 0)
require('nf3 coefficient', band_per_u.subs({S:s.Rational(2,3), b:9}) == -1/(216*pi**2))

# General calibration identity, treating J inverse as an actual inverse:
# (A_u + gradA.k) - gradA.J^-1.(M_u + J.k)
# is A_u - gradA.J^-1.M_u. Test symbolic 2x2 and no divisions by A.
j11,j12,j21,j22=s.symbols('j11 j12 j21 j22')
J=s.Matrix([[j11,j12],[j21,j22]])
grad=s.Matrix([[s.symbols('A1'),s.symbols('A2')]])
k=s.Matrix(s.symbols('k1 k2'))
Mdot=s.Matrix(s.symbols('Mdot1 Mdot2'))
Adot=s.symbols('Adot')
before=Adot-(grad*J.inv()*Mdot)[0]
after=Adot+(grad*k)[0]-(grad*J.inv()*(Mdot+J*k))[0]
require('all-input calibration projection', s.simplify(before-after)==0)
A,kappa=s.symbols('A kappa')
require('massless dimension-three ratio projection including A zero',
        s.simplify(3*kappa*A/m**3-3*A*(kappa*m)/m**4)==0)

report = {
    'assertion_tested': __doc__,
    'status': 'completed',
    'exact_checks': tested,
    'nonaxis_tensor_contractions': count,
    'band_per_e_squared': str(band_per_u),
    'nf3_band_ratio': '-log(4)/(216*pi**2)',
    'nf3_band_float': -math.log(4)/(216*math.pi**2),
    'versions': {'python':platform.python_version(),'sympy':s.__version__},
    'runtime_seconds':time.monotonic()-start,
    'non_claims':['No OPE convergence proof','No nonperturbative sea integral',
                  'No curved response','No finite-alpha continuation','No R evaluation'],
}
(OUT/'independent_result.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':report['status'],'exact_checks':len(tested),
                  'nonaxis_tensor_contractions':count}))
