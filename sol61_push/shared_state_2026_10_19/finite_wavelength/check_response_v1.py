#!/usr/bin/env python3
"""Finite source-specific checks in the exact common-profile n=1 fluid limit.

G=R=1, K=2/pi. A full shared-state construction and its environmental
closure are separate; this checks the common density channel and COM source.
"""
import argparse
import json
import math
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.special import spherical_jn


def integral(f):
    return quad(f, 0, 1, epsabs=2e-12, epsrel=2e-12, limit=120)[0]


pi = math.pi
K = 2 / pi
rows = []
checks = []


def check(name, error, tolerance=1e-10):
    checks.append({"name": name, "error": float(error), "tolerance": tolerance})
    assert abs(error) < tolerance, (name, error)


# Direct boundary-matched polynomial responses; no fitted modal frequency.
A1 = 2 * pi / 3
lam1 = 10 / pi**2 - 5 / 3
H1 = lambda r: A1 * spherical_jn(1, pi*r) - 10*r/pi**2
drho1 = lambda r: -H1(r)/(2*K)
U1 = lambda r: H1(r) + r**3 + lam1*r
U1p = A1*pi*spherical_jn(1, pi, derivative=True)-10/pi**2+3+lam1
check('l1 potential boundary', U1(1))
check('l1 derivative boundary', U1p)
check('l1 COM zero', integral(lambda r: r**3*drho1(r)))
chi1 = (4*pi/3)*integral(lambda r: r**5*drho1(r))
c1 = 20/(3*pi**2)-40/63
check('l1 polynomial response moment', chi1-c1)

A3 = -7*pi/3
H3 = lambda r: A3*spherical_jn(3, pi*r)
drho3 = lambda r: -H3(r)/(2*K)
B3 = H3(1)+1
check('l3 exterior derivative matching', A3*pi*spherical_jn(3, pi, derivative=True)+3+4*B3)
chi3 = (4*pi/7)*integral(lambda r: r**5*drho3(r))
c3 = (105-10*pi**2)/(3*pi**2)
check('l3 polynomial response moment', chi3-c3)
C = 2/(9*pi**2)-4/189
check('combined small-k coefficient', chi1/100+chi3/225-C)


def phi(r, k, ell):
    return (2*ell+1)*((-1)**((ell-1)//2))*spherical_jn(ell, k*r)/k


def response_one(k, ell):
    q = pi
    c = k*k/(q*q-k*k)
    if ell == 1:
        # delta U self = A*j1(qr)+(1+c)*phi+lambda*r,
        # with vanishing exterior mass dipole and zero COM.
        f1 = phi(1, k, 1)
        fp1 = 3*spherical_jn(1, k, derivative=True)
        A = -(1+c)*(fp1-f1)/(q*spherical_jn(1,q,derivative=True)-spherical_jn(1,q))
        lam = -A*spherical_jn(1,q)-(1+c)*f1
        drho = lambda r: -(A*spherical_jn(1,q*r)+c*phi(r,k,1))/(2*K)
        com = integral(lambda r: r**3*drho(r))
        boundary_error = A*q*spherical_jn(1,q,derivative=True)+(1+c)*fp1+lam
        check('finite-k l1 COM '+str(k), com, 2e-10)
        check('finite-k l1 exterior '+str(k), boundary_error, 2e-10)
    else:
        # Matching Robin condition for a decaying l multipole outside R.
        A = -(1+c)*(2*ell+1)*((-1)**((ell-1)//2))*spherical_jn(ell-1,k)/(q*spherical_jn(ell-1,q))
        drho = lambda r: -(A*spherical_jn(ell,q*r)+c*phi(r,k,ell))/(2*K)
    return 4*pi/(2*ell+1)*integral(lambda r: r*r*phi(r,k,ell)*drho(r))


for k in (.02, .05, .1, .2, .5, 1.):
    contributions = {str(ell): response_one(k,ell) for ell in (1,3,5,7)}
    total = sum(contributions.values())
    check('positive static susceptibility '+str(k), min(total,0),1e-20)
    rows.append({'kR':k,'chi_D':total,'chi_D_over_k4':total/k**4,'partial_waves':contributions})
check('small-k asymptotic coefficient', rows[0]['chi_D_over_k4']/C-1, .0003)
check('small-k partial-wave order', rows[0]['partial_waves']['5']/rows[0]['chi_D'], 1e-8)

# Orthogonal check of the l=1 cubic polynomial susceptibility by expansion
# in the Newton operator's eigenfunctions j1(n*pi*r). COM removal changes
# source coefficients; simply deleting n=1 is wrong.
z = lambda n: integral(lambda r: r**3*spherical_jn(1,n*pi*r))
f = lambda n: integral(lambda r: r**5*spherical_jn(1,n*pi*r))
norm = lambda n: integral(lambda r: r*r*spherical_jn(1,n*pi*r)**2)
modal = 0.
for n in range(2,65):
    effective = f(n)-f(1)*z(n)/z(1)
    modal += (4*pi/3)*effective**2/(norm(n)*2*K*(1-1/n**2))
check('independent COM-constrained eigenbasis sum',modal/c1-1,3e-7)

parser=argparse.ArgumentParser()
parser.add_argument('--output',required=True)
args=parser.parse_args()
out={'status':'passed','checks':checks,'check_count':len(checks),
     'coefficients':{'chi_l1_r3':c1,'chi_l3_r3':c3,'C_smallk':C,'modal_l1_64':modal},
     'finite_k_rows':rows,'scope':'Exact n1 shared-fluid common density channel; finite partial waves and quadrature checks do not prove microscopic formation or saturation.'}
Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'passed','check_count':len(checks),'C_smallk':C,'modal_l1_64':modal}))
