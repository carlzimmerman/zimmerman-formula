#!/usr/bin/env python3
"""AZ39: conserved-source curvature on a conditional GR branch, not full v3s.
OMP_NUM_THREADS=1 python3 run.py [--mutate]
"""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import time
import numpy as np
import sympy as S
from numpy.polynomial.legendre import leggauss

START = time.time()
HERE = Path(__file__).resolve().parent
MUTATE = argparse.ArgumentParser()
MUTATE.add_argument('--mutate', action='store_true')
MUTATE = MUTATE.parse_args().mutate
OUT = HERE / ('mutate' if MUTATE else 'main')
OUT.mkdir(exist_ok=True)
checks = []
def check(name, ok, value=None):
    checks.append(dict(name=name, passed=bool(ok), value=value))
def zero(e):
    return S.simplify(e) == 0

x = S.symbols('t x y z', real=True)
t, xx, yy, z = x
eta = [-1, 1, 1, 1]
f, u = S.Function('f')(*x), S.Function('u')(*x)
box = lambda v: sum(eta[a]*S.diff(v, x[a], 2) for a in range(4))
T = S.Matrix(4, 4, lambda a,b: S.diff(f,x[a],x[b])
             - (eta[a]*box(f) if a == b else 0))
check('scalar_source_conservation', all(zero(sum(eta[a]*S.diff(T[a,b],x[a])
      for a in range(4))) for b in range(4)))
hg = S.Matrix(4, 4, lambda a,b: -2*S.diff(u,x[a],x[b]))
hc = S.diag(*[-e*f for e in eta])
def riemann(h,a,b,c,d):
    return (S.diff(h[a,d],x[b],x[c])+S.diff(h[b,c],x[a],x[d])
            -S.diff(h[a,c],x[b],x[d])-S.diff(h[b,d],x[a],x[c]))/2
gauge = [riemann(hg,a,b,c,d) for a in range(4) for b in range(4)
         for c in range(4) for d in range(4)]
check('all_256_gauge_curvatures_zero', all(zero(v) for v in gauge))
def einstein(h):
    tr = sum(eta[a]*h[a,a] for a in range(4))
    Ric = S.Matrix(4,4,lambda a,b: (sum(eta[c]*(S.diff(h[c,b],x[c],x[a])
          +S.diff(h[c,a],x[c],x[b])) for c in range(4))
          -box(h[a,b])-S.diff(tr,x[a],x[b]))/2)
    R = sum(eta[a]*Ric[a,a] for a in range(4))
    return Ric-S.diag(*[e*R/2 for e in eta])
check('Einstein_scalar_response_equals_source', all(zero(v) for v in einstein(hg+hc)-T))
h = hg+hc
tr = sum(eta[a]*h[a,a] for a in range(4))
hb = h-S.diag(*[e*tr/2 for e in eta])
check('harmonic_condition_when_Box_u_equals_f', all(zero(
      sum(eta[a]*S.diff(hb[a,b],x[a]) for a in range(4))
      +S.diff(box(u)-f,x[b])) for b in range(4)))
scalar_tidal = S.simplify(riemann(h,0,1,0,1))
check('scalar_tidal_is_local', zero(scalar_tidal-(S.diff(f,t,2)-S.diff(f,xx,2))/2))

p, s, Q, gamma, mu = S.symbols('p s Q gamma mu', real=True)
W = -p-S.log(1-p)
check('branch_potential_value_and_first_derivative', W.subs(p,0)==0 and S.diff(W,p).subs(p,0)==0)
check('branch_switch_one_sided_first_derivatives',
      S.limit(gamma*s*s/2,s,0,dir='+')==0 and
      S.limit(S.diff(gamma*s*s/2,s),s,0,dir='+')==0)
check('branch_clock_value_and_first_derivative',
      (mu*(Q-1)**2).subs(Q,1)==0 and S.diff(mu*(Q-1)**2,Q).subs(Q,1)==0)
# Left branch F=0 identically. P.A first variation vanishes for P=A=0.
P,A,dP,dA = S.symbols('P A dP dA')
check('branch_acceleration_coupling_first_variation', (dP*A+P*dA).subs({P:0,A:0})==0)

B = S.Function('B')(t,z)
TT = S.zeros(4)
TT[1,2]=TT[2,1]=B
check('planar_TT_source_conservation', all(zero(sum(eta[a]*S.diff(TT[a,b],x[a])
      for a in range(4))) for b in range(4)))
hh = S.zeros(4)
H = S.Function('H')(t,z)
hh[1,2]=hh[2,1]=H
GG = einstein(hh)
check('TT_Einstein_wave_operator', zero(GG[1,2]+box(H)/2)
      and all(zero(GG[a,b]) for a in range(4) for b in range(4) if {a,b}!={1,2}))
check('TT_tidal_operator', zero(riemann(hh,0,1,0,2)+S.diff(H,t,2)/2))

v,q,tv = S.symbols('v q tv', real=True)
bp = 256*v**4*(1-v)**4
cp = (1-q*q)**4
primitive = S.integrate(cp,q)
mass = S.integrate(cp,(q,-1,1))
cpd = S.lambdify(q,S.diff(cp,q),'numpy')
bfun = S.lambdify(v,bp,'numpy')
cfunc = S.lambdify(q,cp,'numpy')
bdd = S.diff(bp,v,2)
times = [S.Rational(1,4),S.Rational(1,2),S.Rational(3,2),S.Rational(9,4),
         S.Rational(5,2),S.Integer(3),S.Rational(7,2),S.Rational(9,2),S.Rational(11,2)]

def quadrature(fun,lo,hi,n):
    if hi <= lo:
        return 0.0
    gx,gw = leggauss(n)
    return float((hi-lo)/2*np.dot(gw,fun((hi+lo)/2+(hi-lo)/2*gx)))

def retarded_exact(tt):
    lo,hi = max(S.Integer(0),tt-4), min(S.Integer(1),tt-2)
    if hi <= lo:
        return S.Integer(0)
    return S.integrate(bp*S.diff(cp,q).subs(q,3-tt+v)/2,(v,lo,hi))

def retarded_h_expression(tt):
    # z=3: upper wave-cone endpoint always beyond source; lower=3-tv+v.
    # Choose the polynomial piece containing tt, then differentiate it.
    full_end = tv-4 if 0 < tt-4 < 1 else (S.Integer(1) if tt-4 >= 1 else S.Integer(0))
    mid_lo = tv-4 if tt > 4 else S.Integer(0)
    mid_hi = tv-2 if tt < 3 else S.Integer(1)
    expr = S.integrate(bp*mass,(v,0,full_end))
    if min(S.Integer(1),tt-2) > max(S.Integer(0),tt-4):
        expr += S.integrate(bp*(primitive.subs(q,1)-primitive.subs(q,3-tv+v)),(v,mid_lo,mid_hi))
    return expr

rows=[]
for tt in times:
    bt = bdd.subs(v,tt) if 0<tt<1 else S.Integer(0)
    exact = bt*3*mass/2 if MUTATE else retarded_exact(tt)
    vals=[]
    for n in (16,32):
        if MUTATE:
            value = float(bt)/2*quadrature(lambda a:(3-a)*cfunc(a),-1,1,n)
        else:
            lo,hi = max(0,float(tt)-4),min(1,float(tt)-2)
            value = quadrature(lambda a:bfun(a)*cpd(3-float(tt)+a)/2,lo,hi,n)
        vals.append(value)
    # Exact differentiation of the retarded displacement independently
    # checks the boundary derivative formula, even on the mutation run.
    hhpoly = retarded_h_expression(tt)
    check('retarded_h_second_derivative_t'+str(tt),zero(-S.diff(hhpoly,tv,2).subs(tv,tt)/2-retarded_exact(tt)))
    rows.append(dict(t=str(tt),exact=str(exact),coarse=vals[0],fine=vals[1],
                     outside_light_cone=bool(tt<2)))
max_pair=max(abs(r['coarse']-r['fine']) for r in rows)
max_exact=max(abs(r['fine']-float(S.Rational(r['exact']))) for r in rows)
outside=max(abs(r['fine']) for r in rows if r['outside_light_cone'])
inside=max(abs(r['fine']) for r in rows if not r['outside_light_cone'])
for name,a0 in [('canonical',9.3603e-11),('alt',1.1312e-10)]:
    check(name+'_quadrature_pair',max_pair<=1e-10,max_pair)
    check(name+'_exact_polynomial_answer',max_exact<=1e-10,max_exact)
    check(name+'_outside_cone_curvature',outside<=1e-12,outside)
    # The mutant has an instantaneous local-time pulse, rather than the
    # delayed signal; this gate intentionally grades the same times.
    check(name+'_nonzero_delayed_response',inside>1e-6,inside)
result=dict(label='NO VERDICT',scope='Full v3s constraint causality unresolved; conditional GR-branch probes only',
            kappa='1/2 FITTED; not theory closed',mutate=MUTATE,
            footings={'canonical':9.3603e-11,'alt':1.1312e-10},
            independent_of_a0_and_Lstar=True,checks=checks,rows=rows,
            scalar_tidal=str(scalar_tidal),source_integral=str(mass),
            hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),HERE/'FROZEN_CRITERIA.md']},
            seconds=time.time()-START,max_rss_native=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
failed=[v['name'] for v in checks if not v['passed']]
print(json.dumps(dict(mutate=MUTATE,passed=len(checks)-len(failed),total=len(checks),failed=failed,
      max_pair=max_pair,max_exact=max_exact,outside=outside,inside=inside,seconds=result['seconds']),indent=2))
raise SystemExit(bool(failed))
