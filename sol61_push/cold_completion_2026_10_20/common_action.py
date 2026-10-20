"""Exploratory three-field stationary branch and exact positivity certificate.

Not a galaxy fit, time evolution, ground-state proof or quantum completion.
Write results only to the runner-owned fresh directory given in argv[1].
"""
from pathlib import Path
import json
import math
import resource
import sys
import time

import numpy as np
import sympy as sp
from scipy.integrate import simpson, solve_bvp

M = 100.0
a = 200.0
g = 0.002168
MX2 = 4.0016
lam = 1.99 + g*g/MX2
checks = []
rows = []

def check(name, value):
    checks.append({"name": name, "pass": bool(value)})

# Rational coefficients make the field-amplitude positivity check exact.
x = sp.Symbol('x')
mu = sp.Rational(17,20)
gg = sp.Rational(271,125000)
mx2 = sp.Rational(2501,625)
ll = sp.Rational(199,100) + gg**2/mx2
AA = ll - gg**2/(mx2 - 4*mu**2)
dd = 1 - mu**2
cut = dd/200
poly = sp.Poly(AA*x**4 + AA*50*x**3 + (20000*AA-40000)*x**2
               + 400*dd*x-dd**2, x)
sturm = sp.sturm(poly.as_expr(), x)
def variation(signs):
    signs = [int(s) for s in signs if s]
    return sum(s != t for s,t in zip(signs,signs[1:]))
at_cut = [sp.sign(p.subs(x,cut)) for p in sturm]
at_inf = [sp.sign(sp.Poly(p,x).LC()) for p in sturm]
root_count = variation(at_cut)-variation(at_inf)
check('positive charged-X quadratic at mu=17/20', mx2-4*mu**2 > 0)
check('positive effective quartic at mu=17/20', AA > 0)
check('positive daughter residual mass at mu=17/20', dd > 0)
check('positive discriminant polynomial at cut', poly.eval(cut) > 0)
check('exact Sturm no roots on cut..infinity', root_count == 0)
check('original repulsive remainder remains positive', ll-gg**2/(mx2-4) > 0)
certificate = {
    'mu': str(mu), 'X_denominator': str(mx2-4*mu**2),
    'A_mu': str(AA), 'delta': str(dd), 'cut': str(cut),
    'polynomial_coefficients_descending': [str(c) for c in poly.all_coeffs()],
    'sturm_signs_at_cut': [int(s) for s in at_cut],
    'sturm_signs_at_positive_infinity': [int(s) for s in at_inf],
    'sturm_root_count_above_cut': root_count,
    'polynomial_at_cut': str(poly.eval(cut)),
    'interpretation': 'Together with the analytic square completion, proves V >= (17/20)^2 (|Psi|^2+4|X|^2) for all classical fields; then E >= (17/20)|Q| in flat isolated or periodic space. Not the old E>=|Q|.'
}

def solve(Q, L, N, tol, seed=None):
    r = np.linspace(1e-4,L,N)
    if seed is None:
        om = .94
        I = 50.
        r0 = (3*Q/(8*math.pi*om*I))**(1/3)
        z = np.exp((r-r0)/1.2)
        f = math.sqrt(I)/(1+z)
        fp = -math.sqrt(I)*z/(1.2*(1+z)**2)
        h = -.02*f*f
        hp = -.04*f*fp
        b = -g*f*f/(MX2-4*om*om)
        bp = -2*g*f*fp/(MX2-4*om*om)
        integrand = 8*math.pi*om*r*r*(f*f+4*b*b)/Q
        q = np.concatenate([[0.],np.cumsum((integrand[1:]+integrand[:-1])/2*np.diff(r))])
        q /= q[-1]
        y = np.array([f,fp,b,bp,h,hp,q])
    else:
        om = seed.p[0]
        y = seed.sol(np.minimum(r,seed.x[-1]))
        y[:6,r>seed.x[-1]] = 0.
        y[6,r>seed.x[-1]] = 1.
    def fun(r,y,p):
        f,u,b,w,h,v,q = y
        om = p[0]
        return np.vstack([u,(1-om*om+2*lam*f*f+a*h+2*g*b)*f-2*u/r,
                          w,(MX2-4*om*om)*b+g*f*f-2*w/r,
                          v,M*M*h-3*M*h*h/8+h**3+a*f*f-2*v/r,
                          8*math.pi*om*r*r*(f*f+4*b*b)/Q])
    def bc(ya,yb,p):
        return np.array([ya[1],ya[3],ya[5],ya[6],yb[0],yb[2],yb[4],yb[6]-1])
    start = time.monotonic()
    sol = solve_bvp(fun,bc,r,y,p=[om],tol=tol,max_nodes=8000)
    rr = np.linspace(1e-4,L,24001)
    f,u,b,w,h,v,q = sol.sol(rr)
    om = float(sol.p[0])
    wt = 4*math.pi*rr*rr
    U = M*M*h*h/2-M*h**3/8+h**4/4
    V = f*f+MX2*b*b+2*g*b*f*f+lam*f**4+a*h*f*f+U
    ed_rot = om*om*(f*f+4*b*b)
    ed_grad = u*u+w*w+.5*v*v
    rot = float(simpson(wt*ed_rot,x=rr))
    grad = float(simpson(wt*ed_grad,x=rr))
    pot = float(simpson(wt*V,x=rr))
    E = rot+grad+pot
    Qint = float(simpson(wt*2*om*(f*f+4*b*b),x=rr))
    QX = float(simpson(wt*8*om*b*b,x=rr))
    tailmask = rr > .8*L
    tail = float(simpson((wt*(ed_rot+ed_grad+V))[tailmask],x=rr[tailmask]))/E
    row = {'Q':Q,'L':L,'tol':tol,'status':int(sol.status),'nodes':len(sol.x),
           'omega':om,'E':E,'Q_integrated':Qint,'E_over_Q':E/Qint,
           'X_charge_fraction':QX/Qint,'gradient':grad,'rotation':rot,'potential':pot,
           'virial_relative':(grad+3*pot-3*rot)/E,'tail_energy_fraction_outer20percent':tail,
           'f_min':float(f.min()),'f_max':float(f.max()),'b_min':float(b.min()),
           'chi_min':float(h.min()),'rms_residual_max':float(max(sol.rms_residuals)),
           'runtime_seconds':time.monotonic()-start}
    rows.append(row)
    tag = f'Q{int(Q)} L{L} tol{tol}'
    check(tag+' converged', sol.status==0)
    check(tag+' charge', abs(Qint/Q-1)<1e-7)
    check(tag+' virial', abs(row['virial_relative'])<1e-6)
    check(tag+' positive nodeless subthreshold branch', 0<om<1 and f.min()>-1e-7 and .85<E/Qint<1)
    check(tag+' tail', abs(tail)<1e-9)
    print(json.dumps(row),flush=True)
    return sol,row

s80,r80 = solve(80000.,40.,800,1e-5)
s160,r160 = solve(160000.,40.,900,1e-5)
t80,v80 = solve(80000.,60.,1000,1e-7,s80)
t160,v160 = solve(160000.,60.,1100,1e-7,s160)
_,rlo = solve(79200.,60.,1000,1e-7,t80)
_,rhi = solve(80800.,60.,1000,1e-7,t80)
for lo,hi in [(r80,v80),(r160,v160)]:
    check(f'Q{int(lo["Q"])} box/tolerance convergence', abs(lo['E']/hi['E']-1)<1e-6)
dEdQ = (rhi['E']-rlo['E'])/1600
check('dE/dQ chemical-potential normalization', abs(dEdQ/v80['omega']-1)<1e-5)
gap = 2*v80['E']-v160['E']
check('positive candidate branch merger gap', gap>0)
check('mu bound consistent with all stationary profiles', all(r['E']>.85*r['Q_integrated'] for r in rows))

# The same classical potential has a field configuration violating the OLD
# rest floor at m=1. This does not assert a stationary solution at that point.
ii=1.;hh=-.02;bb=-g/(MX2-4)
vp=ii+MX2*bb*bb+2*g*bb*ii+lam*ii*ii+a*hh*ii+M*M*hh*hh/2-M*hh**3/8+hh**4/4
check('old unit-mass potential floor is not retained', vp < ii+4*bb*bb)

rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
check('measured RSS below 1 GB', rss<1_000_000_000)
result = {'scope':'Explicit alternative common classical matter action, not adopted canonical theory; stationary finite numerical evidence only.',
          'parameters':{'m':1.,'MX2':MX2,'g':g,'lambda':lam,'M_chi':M,'a':a,'mu_certificate':.85,
                        'lambda_rep_original_limit':lam-g*g/(MX2-4)},
          'exact_positivity_certificate':certificate,'rows':rows,
          'gap':gap,'gap_fraction':gap/(2*v80['E']),'dE_dQ':dEdQ,
          'old_floor_counterexample':{'I':ii,'chi':hh,'X':bb,'V':vp,'weighted_amplitude':ii+4*bb*bb},
          'checks':checks,'n_checks':len(checks),'all_checks_pass':all(c['pass'] for c in checks),
          'peak_rss_bytes_macos':rss,
          'non_claims':['No global minimum or nonlinear stability proof','No emitted energy, charge, or angular-momentum rate',
                        'No near-threshold production yield or abundance in the added mediator',
                        'No force-law normalization, lensing or four-dwarf fit','No quantum UV completion or radiative naturalness']}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(0 if result['all_checks_pass'] else 1)
