"""Bounded TOM phase-space scout for the declared Hernquist/RAR target."""
import argparse
import json
import math
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.optimize import brentq

parser = argparse.ArgumentParser()
parser.add_argument('--output', required=True)
parser.add_argument('--omit-boundary', action='store_true')
args = parser.parse_args()
checks = []

def check(name, value):
    checks.append({'name': name, 'pass': bool(value)})

r, b, R = sp.symbols('r b R', positive=True)
t = r+b
s = sp.exp(-1/t)
mc = r**2/t**2*s/(1-s)
rho = sp.diff(mc, r)/(4*sp.pi*r**2)
h = (1-r**2/R**2)*rho
g = 1/(t**2*(1-s))
exprs = [mc, rho, h, g, -sp.diff(h,r)/g,
         (g*sp.diff(h,r,2)-sp.diff(g,r)*sp.diff(h,r))/g**3]
evaluate = sp.lambdify((r,b,R), exprs, 'numpy', cse=True)
norm = 1/(math.sqrt(8)*math.pi**2)

# Independent forward integral: uniform sphere has h=2*rho0*psi,
# so its entire inversion is the boundary term.
for psi in [0.001,0.1,0.4]:
    rho0 = 3/(4*math.pi)
    got = 0.0 if args.omit_boundary else 4*math.pi*math.sqrt(2)*norm*2*rho0*quad(
        lambda angle: 2*psi*math.cos(angle)**2, 0, math.pi/2)[0]
    check('uniform_sphere_forward_'+str(psi), abs(got-2*rho0*psi)<1e-12)

rows=[]
for bv in [0.03,0.1,0.3,1.0,3.0]:
    for q in [0.5364,5.364]:
        rv=brentq(lambda x: float(evaluate(x,bv,1)[0])-q, 1e-8, 100)
        logedge=math.log(math.expm1(1/(rv+bv)))
        def psi_at(x):
            return np.log(np.expm1(1/(np.asarray(x)+bv)))-logedge
        def radius_at(psi):
            return 1/np.logaddexp(0,psi+logedge)-bv
        edge=evaluate(rv,bv,rv)
        boundary=float(edge[4])
        check('edge_mass_'+str((bv,q)), abs(float(edge[0])-q)<1e-10)
        check('edge_derivative_'+str((bv,q)), abs(boundary-2*float(edge[1])/(rv*float(edge[3])))<1e-11)
        samples=[]
        for frac in np.r_[np.geomspace(1e-4,0.95,70),0.99,0.9999]:
            re=rv*frac
            Q=float(psi_at(re))
            vals=evaluate(re,bv,rv)
            check('inverse_potential_'+str((bv,q,float(frac))), abs(float(radius_at(Q))-re)<1e-10*max(1,re))
            def integrand(z):
                rr=float(radius_at(Q*(1-z*z)))
                return 2*math.sqrt(Q)*float(evaluate(rr,bv,rv)[5])
            interior,err=quad(integrand,0,1,epsabs=1e-10,epsrel=2e-9,limit=200)
            ab=quad(lambda z: abs(integrand(z)),0,1,epsabs=1e-10,epsrel=2e-8,limit=200)[0]
            bd=0 if args.omit_boundary else boundary/math.sqrt(Q)
            f=norm*(bd+interior)
            signed_fraction=(bd+interior)/(abs(bd)+ab)
            samples.append({'r_over_R':float(frac),'Q':Q,'f':f,'f_over_absolute_integral':signed_fraction,
                            'quadrature_error_estimate':norm*err,'h_psi':float(vals[4])})
        grid=rv*np.geomspace(1e-5,1,2001)
        vals=evaluate(grid,bv,rv)
        # Necessary monotonicity follows directly from the positive Abel transform.
        hprime=np.asarray(vals[4])
        failed=np.where(hprime < -1e-9*np.max(abs(hprime)))[0]
        negative=[x for x in samples if x['f_over_absolute_integral'] < -1e-6]
        row={'b_over_rM':bv,'q':q,'R_over_rM':rv,'rho_edge':float(edge[1]),
             'edge_h_psi':boundary,'min_h_psi':float(hprime.min()),
             'min_f_over_absolute_integral':min(x['f_over_absolute_integral'] for x in samples),
             'negative_f_samples':len(negative),'total_f_samples':len(samples),
             'monotonicity_violation_samples':len(failed),'samples':samples}
        rows.append(row)
        print(json.dumps({k:v for k,v in row.items() if k!='samples'}))

result={'base_commit':'baf7e3dd46582631887fa889c6e9a12ea5362210',
        'mutation_omit_boundary':args.omit_boundary,'checks':checks,'models':rows,
        'limitations':['Sampled double-precision inversion is not positivity over the continuum.',
                       'No formation, non-spherical or collective stability calculation.',
                       'The RAR law, abundance, and anisotropy ansatz are inputs.']}
out=Path(args.output)
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(result,indent=2)+'\n')
print('implementation checks:',sum(x['pass'] for x in checks),'/',len(checks))
raise SystemExit(0 if all(x['pass'] for x in checks) else 1)
