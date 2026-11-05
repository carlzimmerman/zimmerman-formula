"""Exact and finite structural checks; no coefficient prediction or data fit."""
import argparse
import json
from pathlib import Path
import sys

import mpmath as mp
import sympy as sp

parser = argparse.ArgumentParser()
parser.add_argument('--out', required=True)
parser.add_argument('--mutate', action='store_true')
args = parser.parse_args()
checks = []

def check(name, value):
    checks.append({'name': name, 'passed': bool(value)})
    print(('PASS ' if value else 'FAIL ') + name, flush=True)

a, p, K, b, rho, s, X, r, t, A, k = sp.symbols(
    'a p K b rho s X r t A k', positive=True)
W = a**2/K*(-p/a-sp.log(1-p/a))
Wrho = W.subs(a, sp.sqrt(b*rho))
sub = {p: sp.sqrt(b*rho)*s/(1+s)}
h = s+s/(1+s)-2*sp.log(1+s)
eps = b/(2*K)
wr = sp.simplify(sp.expand_log(sp.diff(Wrho, rho).subs(sub), force=True))
wrr = sp.simplify(sp.diff(Wrho, rho, 2).subs(sub))
check('W_rho=-eps*h at fixed p', sp.simplify(wr+eps*h)==0)
check('W_rhorho at fixed p', sp.simplify(wrr-eps*s**3/(2*rho*(1+s)))==0)
T = r-wr*r-2*X*(wrr*r**2+wr*t)
target = r+eps*h*(r+2*X*t)-eps*X*r**2/rho*s**3/(1+s)
check('general k-essence chain rule', sp.simplify(T-target)==0)
check('large-s coefficient negative', sp.simplify(sp.limit(T/s**2,s,sp.oo)+eps*X*r**2/rho)==0)
check('zero polarization recovers bare rho_X', sp.simplify(T.subs(s,0)-r)==0)
opw = sp.symbols('opw', positive=True)
canonical = target.subs({r:1,t:0,X:opw*rho/2})
check('canonical AZ40 limit', sp.simplify(canonical-(1+eps*(h-opw*s**3/(2*(1+s)))))==0)

# Independent Legendre representation: retain clock velocity before elimination.
L = b*rho/K*(A/sp.sqrt(b*rho)-sp.log(1+A/sp.sqrt(b*rho)))
at = {A:s*sp.sqrt(b*rho)}
LAA = sp.simplify(sp.diff(L,A,2).subs(at))
LAr = sp.simplify(sp.diff(L,A,rho).subs(at))
Lr = sp.simplify(sp.expand_log(sp.diff(L,rho).subs(at),force=True))
Lrr = sp.simplify(sp.diff(L,rho,2).subs(at))
Tfree = r+Lr*(r+2*X*t)+2*X*r**2*Lrr
mix2 = 2*X*r**2*LAr**2/LAA
Tlock = Tfree if args.mutate else Tfree-mix2
check('Legendre clock Schur complement equals fixed-p coefficient', sp.simplify(Tlock-T)==0)
check('mixing correction strictly positive formula', sp.simplify(mix2-eps*X*r**2/rho*s**4/(1+s)**2)==0)

# Generic PN constraint block, separate from a complete action matching.
D, B, ell, tau = sp.symbols('D B ell tau', real=True)
C = sp.Matrix([[-k**2,k],[k,-D]])
Bc = sp.Matrix([[-ell,0],[-B,-k]])
H = sp.diag(tau,0)-Bc.T*C.inv()*Bc
det = sp.factor(H.det())
check('generic PN determinant independent of polarization mixing',
      sp.simplify(det-(k**2*tau+ell**2)/(D-1))==0)
check('generic PN clock diagonal positive when D>1', sp.simplify(H[1,1]-k**2/(D-1))==0)

# Exact adopted-kernel auxiliary-scale variation; a here is geometrized.
q = sp.symbols('q', positive=True)
Jcorr = -2*a**2*(q/a-sp.log(1+q/a))
Ja = sp.simplify(sp.diff(Jcorr,a).subs(q,a*s))
check('adopted kernel scale derivative', sp.simplify(Ja+2*a*h)==0)
check('h positive proof derivative', sp.simplify(sp.diff(h,s)-s**2/(1+s)**2)==0)
check('vacuum scale derivative zero', sp.simplify(Ja.subs(s,0))==0)

# AC2: a0 first appears at cubic order in small polarization.
series = sp.series(W,p,0,5).removeO()
check('AC2 polarization expansion', sp.simplify(series-(p**2/(2*K)+p**3/(3*K*a)+p**4/(4*K*a**2)))==0)

rows = []
for n in (1,2,3):
    for V in (1,10,100):
        for bk in ('0.01','0.1'):
            for ss in (1,10,1000):
                vals = []
                for dps in (40,80):
                    with mp.workdps(dps):
                        bb, xx = mp.mpf(bk), mp.mpf(1)
                        def density(z):
                            return (2*n-1)*z**n+V
                        rr = density(xx)
                        aa = mp.sqrt(bb*rr)
                        pp = aa*ss/(1+ss)
                        def lag(z):
                            az = mp.sqrt(bb*density(z))
                            return z**n-V-az**2*(-pp/az-mp.log1p(-pp/az))
                        direct = mp.diff(lag,xx)+2*xx*mp.diff(lag,xx,2)
                        rx = n*(2*n-1)*xx**(n-1)
                        rxx = n*(n-1)*(2*n-1)*xx**(n-2)
                        hh = mp.mpf(ss)+mp.mpf(ss)/(1+ss)-2*mp.log1p(ss)
                        formula = rx+bb/2*hh*(rx+2*xx*rxx)-bb/2*xx*rx**2/rr*mp.mpf(ss)**3/(1+ss)
                        vals.append((direct,formula))
                with mp.workdps(80):
                    residual=max(abs(vals[0][0]-vals[1][0]),abs(vals[1][0]-vals[1][1]))/max(1,abs(vals[1][0]))
                    rows.append({'n':n,'V':V,'b_over_K':bk,'s':ss,
                                 'T':mp.nstr(vals[1][0],35),'normalized_error':mp.nstr(residual,8)})
check('54 finite derivative fixtures',len(rows)==54)
check('40/80 digits and independent derivative agreement', all(mp.mpf(z['normalized_error'])<mp.mpf('1e-30') for z in rows))

result={'mode':'omit_clock_mixing' if args.mutate else 'main',
        'checks':checks,'finite_rows':rows,'passed':all(z['passed'] for z in checks),
        'symbolic':{'T_fixed_p':str(sp.simplify(target)),
                    'large_s_limit':str(-eps*X*r**2/rho),
                    'PN_determinant':str(det)},
        'non_claims':['No derived kappa','No solved physical background',
                      'No complete covariant stability or exclusion theorem']}
Path(args.out).parent.mkdir(parents=True,exist_ok=True)
Path(args.out).write_text(json.dumps(result,indent=2)+'\n')
sys.exit(0 if result['passed'] else 1)
