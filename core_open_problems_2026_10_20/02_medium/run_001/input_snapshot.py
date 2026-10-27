#!/usr/bin/env python3
"""Self-contained exact/finite checks for medium checkpoint MEDIUM-2026-10-20-A.

Run from repository root; pass the fresh runner output directory as argv[1].
No existing repository script, result, dataset, or untracked file is imported.
"""
import csv
import json
import math
from pathlib import Path
import sys

import numpy as np
import scipy
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq
import sympy as s

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
checks = []


def check(name, value, detail=None):
    value = bool(value)
    checks.append(dict(name=name, passed=value, detail=detail))
    if not value:
        raise AssertionError((name, detail))


def exact(name, expr):
    residual = s.simplify(expr)
    check(name, residual == 0, str(residual))


u, a, n, K, b, m, z, y = s.symbols('u a n K b m z y', positive=True)
W = a**2 / (K*n**3) * (-s.log(1-n*u/a)-n*u/a-(n*u/a)**2/2)
f = u**2/(a-n*u)
exact('target antiderivative', K*s.diff(W, u)-f)
exact('target zero energy', W.subs(u, 0))
exact('target zero force', f.subs(u, 0))
exact('target zero remainder Hessian', s.diff(f, u).subs(u, 0))
exact('positive radial Hessian formula', s.diff(f,u)-u*(2*a-n*u)/(a-n*u)**2)
exact('positive transverse Hessian formula', f/u-u/(a-n*u))
exact('target cubic coefficient', s.limit(K*W/u**3,u,0)-1/(3*a))
exact('target quartic coefficient', s.limit((K*W-u**3/(3*a))/u**4,u,0)-n/(4*a**2))
exact('target pole residue', s.limit((a/n-u)*f,u,a/n,dir='-')-a**2/n**3)
check('target endpoint energy diverges', s.limit(W,u,a/n,dir='-') == s.oo)
root = (s.sqrt(n**2*y**2+4*y)-n*y)/2
exact('capacity family root', root**2+n*y*root-y)
g1 = (y+s.sqrt(y*y+4*y))/2
g2 = s.sqrt(y*y+y)
exact('n1 law', g1**2-y*(g1+1))
exact('n2 law', g2**2-y*y-y)
ratio_z = (z+1)/s.sqrt(z*z+3)
exact('maximum ratio derivative', s.diff(ratio_z,z)-(3-z)/(z*z+3)**s.Rational(3,2))
exact('maximum at y=1/2', (g1/g2).subs(y,s.Rational(1,2))-2/s.sqrt(3))

# Independent integration of force versus the closed-form potential.
for nn in (1, 2):
    for mm in (0.001, 0.1, 0.5, 0.9, 0.99):
        uu = mm/nn
        numeric, err = quad(lambda v: v*v/(1-nn*v), 0, uu, epsabs=1e-14, epsrel=1e-12)
        analytic = (-math.log1p(-mm)-mm-mm*mm/2)/nn**3
        check(f'potential quadrature n={nn} m={mm}', abs(numeric-analytic)<2e-12,
              dict(numeric=numeric, analytic=analytic, quad_error=err))

# Three different microscopic/constitutive candidates, all normalized to
# K W_full''(0)=1. These are favorable matching assumptions, not predictions.
Lseries = z/3-z**3/45+2*z**5/945
Linvseries = 3*m+s.Rational(9,5)*m**3+s.Rational(297,175)*m**5
exact('inverse Langevin series through m^5', s.series(Lseries.subs(z,Linvseries)-m,m,0,7).removeO())
F_bi = b*b*(1-s.sqrt(1-u*u/(b*b)))  # K W_full
f_bi = s.diff(F_bi,u)-u
exact('BI leading remainder force', s.limit(f_bi/u**3,u,0)-1/(2*b*b))
exact('BI saturation exponent', s.limit(s.sqrt(b-u)*f_bi,u,b,dir='-')-b**s.Rational(3,2)/s.sqrt(2))
check('BI endpoint energy finite', s.limit(F_bi,u,b,dir='-') == b*b)
F_site = b*b*((1+u/b)*s.log(1+u/b)+(1-u/b)*s.log(1-u/b))/2
f_site = b*s.atanh(u/b)-u
exact('two-state derivative', s.diff(F_site,u)-u-f_site)
exact('two-state leading remainder force', s.limit(f_site/u**3,u,0)-1/(3*b*b))
exact('two-state finite endpoint energy', s.limit(F_site,u,b,dir='-')-b*b*s.log(2))
F_log = -b*b*s.log(1-u*u/(b*b))/2
f_log = s.diff(F_log,u)-u
exact('symmetric logarithmic remainder force', f_log-u**3/(b*b-u*u))
exact('symmetric logarithmic leading force', s.limit(f_log/u**3,u,0)-1/(b*b))

def langevin(h):
    if abs(h) < 1e-3:
        return h/3-h**3/45+2*h**5/945-h**7/4725
    return 1/math.tanh(h)-1/h


for hh in (0.01, 0.1, 1.0, 3.0, 10.0):
    den = quad(lambda t: math.exp(hh*t), -1, 1, epsabs=1e-12)[0]
    num = quad(lambda t: t*math.exp(hh*t), -1, 1, epsabs=1e-12)[0]
    check(f'orientation partition integral h={hh}', abs(num/den-langevin(hh))<2e-13)
    # Exact finite-state sums and genuine quantum 2x2 ground-state expectation.
    prob = np.exp(np.array([-hh,hh])); prob /= prob.sum()
    check(f'binary partition h={hh}', abs(float(prob[1]-prob[0])-math.tanh(hh))<1e-14)
    H = np.array([[-hh,-1.],[-1.,hh]])
    vals, vecs = np.linalg.eigh(H)
    pol = vecs[0,0]**2-vecs[1,0]**2
    check(f'quantum two-level ground state h={hh}', abs(pol-hh/math.sqrt(1+hh*hh))<1e-14)

force_rows = []
for mm in (0.001,0.01,0.1,0.5,0.9,0.99):
    invL = brentq(lambda h: langevin(h)-mm, 1e-10, max(10.,2/(1-mm)),xtol=1e-12)
    row = dict(m=mm, target_n1=mm*mm/(1-mm), target_n2=mm*mm/(2*(1-mm)),
               langevin=invL/3-mm, BI=mm/math.sqrt(1-mm*mm)-mm,
               binary=math.atanh(mm)-mm, symmetric_log=mm**3/(1-mm*mm))
    # Here all forces are divided by b and each model shares u_max=b.
    # The n=2 target therefore has a0=2b, n=1 a0=b.
    force_rows.append(row)
    check(f'Langevin inverse reconstruction m={mm}',abs(langevin(invL)-mm)<5e-13)

# Finite-capacity kinetics in dimensionless a0=Gamma=1 units.
def ustar(nn, yy):
    if yy == 0:
        return 0.0
    return 2*yy/(math.sqrt(nn*nn*yy*yy+4*yy)+nn*yy)


def exact_trajectory(t, nn, yy, initial):
    D = math.sqrt(nn*nn*yy*yy+4*yy)
    up = ustar(nn,yy)
    um = (-nn*yy-D)/2
    ratio = (initial-up)/(initial-um)*math.exp(-D*t)
    return (up-ratio*um)/(1-ratio)


for nn in (1,2):
    for yy in (0.01,0.5,10.):
        for fraction in (0.,0.2,0.9):
            initial=fraction/nn
            tend=10/math.sqrt(nn*nn*yy*yy+4*yy)
            times=np.linspace(0,tend,41)
            sol=solve_ivp(lambda t,w: [yy*(1-nn*w[0])-w[0]**2], [0,tend], [initial],
                          t_eval=times,rtol=2e-11,atol=2e-13)
            exact_values=np.array([exact_trajectory(t,nn,yy,initial) for t in times])
            error=float(np.max(np.abs(sol.y[0]-exact_values)))
            check(f'kinetic trajectory n={nn} y={yy} init={fraction}',
                  sol.success and error<1e-10 and np.all(sol.y[0]>=-1e-13) and np.all(sol.y[0]<=1/nn+1e-13),error)
for nn in (1,2):
    initial=0.7/nn
    sol=solve_ivp(lambda t,w:[-w[0]**2],[0,10],[initial],rtol=2e-11,atol=2e-13)
    check(f'zero-source algebraic decay n={nn}',abs(sol.y[0,-1]-initial/(1+10*initial))<1e-11)

# Conditional dynamics and geometry discriminators: same fixed source and a0.
G=6.674e-11
Msun=1.98892e30
pc=3.0856775814913673e16
footings={'canonical':9.3603e-11,'alternative':1.1312e-10}
footing_rows=[]
x=s.symbols('x',positive=True)
for label,a0 in footings.items():
    rM=math.sqrt(G*1e10*Msun/a0)
    for nn in (1,2):
        radius=math.sqrt(2)*rM
        u_at=ustar(nn,0.5)*a0
        g_at=0.5*a0+u_at
        q=2/(nn+s.sqrt(nn*nn+4*x*x))
        lap=s.diff(q,x,2)+2*s.diff(q,x)/x-2*q/(x*x)
        residual_coeff=float(abs((x*x*lap/2).subs(x,s.sqrt(2))))
        footing_rows.append(dict(footing=label,n=nn,a0_m_s2=a0,u_max_m_s2=a0/nn,
            r_at_max_kpc=radius/(1000*pc),g_at_max_m_s2=g_at,v_at_max_km_s=math.sqrt(g_at*radius)/1000,
            spherical_enclosed_mean_cap_Msun_pc2=a0/(nn*math.pi*G)/(Msun/pc**2),
            planar_sheet_cap_Msun_pc2=a0/(2*nn*math.pi*G)/(Msun/pc**2),
            stiffness_residual_coeff=residual_coeff,
            stiffness_residual_Lstar_5p75pc=residual_coeff*(5.75*pc/rM)**2))

comparison_rows=[]
for yy in (1e-4,0.01,0.1,0.5,1.,10.,100.):
    gg1=yy+ustar(1,yy); gg2=yy+ustar(2,yy)
    comparison_rows.append(dict(y=yy,u1_over_a0=ustar(1,yy),u2_over_a0=ustar(2,yy),
        g1_over_a0=gg1,g2_over_a0=gg2,velocity_ratio=math.sqrt(gg1/gg2)))

for name, rows in [('forces.csv',force_rows),('footings.csv',footing_rows),('discriminator.csv',comparison_rows)]:
    with (OUT/name).open('w',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0])); writer.writeheader();writer.writerows(rows)

result=dict(checkpoint='MEDIUM-2026-10-20-A',checks=checks,check_count=len(checks),
    all_passed=all(c['passed'] for c in checks),force_rows=force_rows,footings=footing_rows,
    comparison_rows=comparison_rows,maximum=dict(y=0.5,acceleration_ratio=2/math.sqrt(3),
    velocity_ratio=math.sqrt(2/math.sqrt(3)),kinetic_rate_n2_over_n1=2/math.sqrt(3)),
    software=dict(python=sys.version.split()[0],numpy=np.__version__,scipy=scipy.__version__,sympy=s.__version__))
(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(check_count=len(checks),all_passed=result['all_passed'],maximum=result['maximum'],footings=footing_rows),indent=2))
