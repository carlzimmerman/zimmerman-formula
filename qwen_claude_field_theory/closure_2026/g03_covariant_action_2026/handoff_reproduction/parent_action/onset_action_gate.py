#!/usr/bin/env python3
"""Static variational gate and Gaussian onset curve; no relativistic claims.

Run this file for results.json and computation_manifest.json, or run its tests.
The action, boundary assumptions and continuum argument are in REPORT.md.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone

import numpy as np
import scipy
from scipy.integrate import quad
from scipy.linalg import expm
from scipy.optimize import brentq
from scipy.special import gammainc
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def inverse_y(s):
    """Solve s=y(1-exp(-y)); scale the root to retain relative precision."""
    s = float(s)
    if not math.isfinite(s) or s < 0:
        raise ValueError('s must be finite and nonnegative')
    if s == 0:
        return 0.0
    scale = math.sqrt(s) + s
    z = brentq(lambda z: (scale*z/s)*(-math.expm1(-scale*z))-1,
               0, 2, xtol=5e-15, rtol=1e-14)
    return scale*z


def phantom(s):
    """Exact y-s = y exp(-y), evaluated without high-field cancellation."""
    y = inverse_y(s)
    return y * math.exp(-y)


def dual_q(s):
    """q(s²)=2sy-G(y)-s²; used away from cancellation in lattice tests."""
    y = inverse_y(s)
    primitive = y*y + 2*(1+y)*math.exp(-y)-2
    return 2*s*y-primitive-s*s


def symbolic_checks():
    y = sp.symbols('y', positive=True)
    mu = 1-sp.exp(-y)
    s = y*mu
    primitive = y*y+2*(1+y)*sp.exp(-y)-2
    q = 2*s*y-primitive-s*s
    flux = sp.simplify(sp.diff(q, y)/(2*s*sp.diff(s, y)))
    F = sp.symbols('F', positive=True)
    coefficient = sp.integrate(sp.sqrt(F)/3, (F, 0, 1))
    # An exact graph-Laplacian illustration, not a claim of a continuum proof.
    L = sp.Matrix([[1,-1,0],[-1,2,-1],[0,-1,1]])
    S = (sp.eye(3)+L).inv()
    A = -sp.Matrix([[1,-1,0],[-1,3,-2],[0,-2,2]])
    commutator = A*S-S*A
    return {
        'primitive_residual': str(sp.simplify(sp.diff(primitive,y)/(2*y)-mu)),
        'dual_flux_residual': str(sp.simplify(flux-(y/s-1))),
        'exact_onset_residual': str(sp.simplify(
            (1-sp.exp(-sp.log(1+F)))-F/(1+F))),
        'gaussian_central_coefficient': str(coefficient),
        'graph_commutator': str(commutator),
        'graph_commutator_rank': int(commutator.rank()),
        'graph_constant_mode_residual': str((commutator*sp.ones(3,1)).norm()),
    }


def lattice(kind, n=12):
    D = np.roll(np.eye(n), -1, axis=1)-np.eye(n)
    L = -D.T@D
    width = 0.8
    if kind == 'gaussian':
        S = expm(width**2*L/2)
    elif kind == 'helmholtz':
        S = np.linalg.inv(np.eye(n)-width**2*L)
    else:
        raise ValueError(kind)
    T = np.linalg.pinv(L, rcond=1e-12)
    theta = 2*np.pi*np.arange(n)/n
    u = np.sin(theta)+0.31*np.cos(2*theta)+0.17*np.sin(3*theta+0.2)
    return D, L, S, T, u


def flux_vector(g):
    return np.array([np.sign(v)*phantom(abs(v)) for v in g])


def variation_check(kind):
    D, L, S, _, u = lattice(kind)
    phi = 0.7*u+np.cos(np.arange(len(u)))
    rho = L@u
    f = flux_vector(D@S@u)
    analytic_u = L@phi-L@u+S@D.T@f
    missing_u = L@phi-L@u+D.T@f
    analytic_phi = L@u-rho

    def action(u_arg, phi_arg):
        return (-np.dot(D@phi_arg, D@u_arg)+0.5*np.dot(D@u_arg,D@u_arg)
                +0.5*sum(dual_q(abs(v)) for v in D@S@u_arg)-rho@phi_arg)

    h = 2e-5
    basis = np.eye(len(u))
    numeric_u = np.array([(action(u+h*v,phi)-action(u-h*v,phi))/(2*h) for v in basis])
    numeric_phi = np.array([(action(u,phi+h*v)-action(u,phi-h*v))/(2*h) for v in basis])
    norm = np.linalg.norm(analytic_u)
    return {
        'finite_difference_relative_error': float(max(np.linalg.norm(numeric_u-analytic_u),
                                                       np.linalg.norm(numeric_phi-analytic_phi))/norm),
        'missing_adjoint_relative_error': float(np.linalg.norm(numeric_u-missing_u)/norm),
        'minimum_filtered_gradient': float(min(abs(D@S@u))),
    }


def reciprocity_check(kind, n=12):
    D,L,S,T,u = lattice(kind,n)
    grad = D@S@u
    y = np.array([inverse_y(abs(v)) for v in grad])
    tangent = 1/(-np.expm1(-y)+y*np.exp(-y))-1
    A = -D.T@np.diag(tangent)@D
    one = T+T@A@S@T
    corrected = T+T@S@A@S@T
    P = np.eye(n)-np.ones((n,n))/n
    rho = L@u

    def response(source):
        potential = T@source
        return potential-T@D.T@flux_vector(D@S@potential)

    h = 1e-6
    fd = np.column_stack([(response(rho+h*v)-response(rho-h*v))/(2*h) for v in P])
    return {
        'n': n,
        'one_filter_relative_antisymmetry': float(np.linalg.norm(one-one.T)/np.linalg.norm(one)),
        'action_relative_antisymmetry': float(np.linalg.norm(corrected-corrected.T)/np.linalg.norm(corrected)),
        'finite_difference_response_error': float(np.linalg.norm(fd-one)/np.linalg.norm(one)),
        'laplacian_nullity': int(n-np.linalg.matrix_rank(L,tol=1e-11)),
        'minimum_filtered_gradient': float(min(abs(grad))),
    }


def mass_fraction(x, kind='gaussian'):
    if x < 0:
        raise ValueError('radius must be nonnegative')
    if kind == 'gaussian':
        return float(gammainc(1.5, x*x/2))
    if kind == 'helmholtz':
        return float(gammainc(2, x))
    raise ValueError(kind)


def one_filter_onset(eps, kind):
    if eps <= 0:
        raise ValueError('epsilon must be positive')
    def residual(logx):
        x = math.exp(logx)
        F = mass_fraction(x,kind)
        return x*x*math.log1p(F)/(1+F)/eps-1
    return math.exp(brentq(residual,-40,math.log(10+10*math.sqrt(eps)),xtol=1e-13))


def angular_kernel(x, t):
    """exp[-(x²+t²)/2] int_-1^1 z exp(xtz) dz, stably."""
    a = x*t
    if abs(a) < 0.1:
        series = sum(2*a**(2*j+1)/(math.factorial(2*j+1)*(2*j+3)) for j in range(5))
        return math.exp(-(x*x+t*t)/2)*series
    return ((a-1)*math.exp(-(x-t)**2/2)+(a+1)*math.exp(-(x+t)**2/2))/(a*a)


def filtered_phantom(x, eps, cutoff=10):
    """Radial component of Gaussian convolution of the inner phantom vector."""
    if x == 0:
        return 0.0
    if x < 0 or eps <= 0:
        raise ValueError('x must be nonnegative and epsilon positive')
    def integrand(t):
        if t == 0:
            return 0.0
        f = phantom(eps*mass_fraction(t)/t**2)
        return t*t*f*angular_kernel(x,t)/math.sqrt(2*math.pi)
    value,error = quad(integrand,0,x+cutoff,points=[x],epsabs=math.sqrt(eps)*min(x,1)*1e-12,
                       epsrel=2e-10,limit=180)
    if error > max(abs(value)*2e-8,math.sqrt(eps)*min(x,1)*2e-12):
        raise ArithmeticError(f'quadrature error estimate {error} for value {value}')
    return value


def filtered_phantom_angular(x, eps):
    """Independent angular Gauss-Legendre integral, no analytic kernel formula."""
    nodes, weights = np.polynomial.legendre.leggauss(96)
    def integrand(t):
        if t == 0:
            return 0.0
        angles = np.dot(weights,nodes*np.exp(-(x*x+t*t-2*x*t*nodes)/2))
        return t*t*phantom(eps*mass_fraction(t)/t**2)*angles/math.sqrt(2*math.pi)
    return quad(integrand,0,x+12,points=[x],epsabs=math.sqrt(eps)*min(x,1)*1e-12,
                epsrel=2e-10,limit=180)[0]


def action_onset(eps):
    if eps <= 0:
        raise ValueError('epsilon must be positive')
    # Wide physical bracket independent of the proposed sixth-power coefficient.
    def residual(logx):
        x = math.exp(logx)
        return filtered_phantom(x,eps)*x*x/eps-1
    return math.exp(brentq(residual,-30,math.log(10+10*math.sqrt(eps)),xtol=2e-12))


def central_slope(eps):
    value = quad(lambda t: math.sqrt(2/math.pi)/3*t**3*math.exp(-t*t/2)
                 *phantom(eps*mass_fraction(t)/t**2) if t else 0,
                 0,12,epsabs=math.sqrt(eps)*1e-12,epsrel=2e-11)[0]
    return value


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    start = time.monotonic()
    timestamp = datetime.now(timezone.utc).isoformat()
    rows = []
    for eps in np.logspace(-12,-4,9):
        x = action_onset(eps)
        one = one_filter_onset(eps,'gaussian')
        helm = one_filter_onset(eps,'helmholtz')
        rows.append({'epsilon':float(eps),'action_gaussian_onset':x,
                     'sixth_power_ratio':x**6/((81/4)*eps),
                     'one_filter_gaussian_onset':one,'one_filter_helmholtz_onset':helm,
                     'central_slope_over_sqrt_epsilon':central_slope(eps)/math.sqrt(eps),
                     'onset_force_residual':filtered_phantom(x,eps)*x*x/eps-1})
    slopes = {}
    for key in ['action_gaussian_onset','one_filter_gaussian_onset','one_filter_helmholtz_onset']:
        slopes[key] = float(np.polyfit(np.log([r['epsilon'] for r in rows[:4]]),
                                      np.log([r[key] for r in rows[:4]]),1)[0])
    symmetry = {f'{k}_{n}':reciprocity_check(k,n) for k in ['gaussian','helmholtz'] for n in [8,12,20]}
    variation = {k:variation_check(k) for k in ['gaussian','helmholtz']}
    independent = []
    for x,eps in [(0.04,1e-8),(0.6,1e-4),(3,0.02)]:
        a = filtered_phantom(x,eps)
        independent.append({'x':x,'epsilon':eps,'angular_relative_difference':
                            a/filtered_phantom_angular(x,eps)-1,'cutoff_relative_difference':
                            a/filtered_phantom(x,eps,cutoff=12)-1})
    symbolic = symbolic_checks()
    checks = {
        'symbolic_identities': all(v=='0' for k,v in symbolic.items() if k.endswith('_residual')),
        'finite_variation': all(v['finite_difference_relative_error']<2e-7 for v in variation.values()),
        'missing_adjoint_detected': all(v['missing_adjoint_relative_error']>1e-3 for v in variation.values()),
        'nonreciprocal_one_filter': all(v['one_filter_relative_antisymmetry']>1e-3 for v in symmetry.values()),
        'reciprocal_action': all(v['action_relative_antisymmetry']<1e-12 for v in symmetry.values()),
        'sixth_power_asymptote': abs(rows[0]['sixth_power_ratio']-1)<0.001,
        'independent_convolution': all(abs(v['angular_relative_difference'])<2e-7 and
                                       abs(v['cutoff_relative_difference'])<2e-8 for v in independent),
        'onset_force_balance': max(abs(r['onset_force_residual']) for r in rows)<2e-9,
    }
    checks = {name: bool(passed) for name, passed in checks.items()}
    status = 0 if all(checks.values()) else 1
    result = {'scope':'Static construction and finite checks, not relativistic or empirical closure',
              'symbolic':symbolic,'variation':variation,'reciprocity':symmetry,
              'onset_rows':rows,'measured_log_slopes_first_four_masses':slopes,
              'independent_convolution':independent,'checks':checks,'exit_status':status}
    path = HERE/'results.json'
    path.write_text(json.dumps(result,indent=2)+'\n')
    commit = subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    dirty = subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True)
    source_paths = [HERE/'onset_action_gate.py',HERE/'test_onset_action_gate.py',HERE/'CONTRACT.md',
                    ROOT/'hunt_2026/f29_coherence_length_law.py',ROOT/'hunt_2026/f30_ppn_screening_door.py']
    manifest = {'schema_version':1,'claim_id':'smoothed-phantom-variational-sixth-power-onset',
                'repository':{'commit':commit,'dirty':bool(dirty)},
                'command':'python3 '+str(HERE.relative_to(ROOT)/'onset_action_gate.py'),
                'environment':{'software':[f'Python {platform.python_version()}',f'NumPy {np.__version__}',
                                           f'SciPy {scipy.__version__}',f'SymPy {sp.__version__}'],
                               'hardware':platform.platform()},
                'mathematics':{'assertion_tested':'Adjoint variation, reciprocity and isolated spherical onset asymptote',
                    'coefficient_domain':'SymPy exact expressions; float64 numerical checks',
                    'conventions':'outward potential gradient; Gaussian width xi; epsilon=GM/(a0 xi²)',
                    'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p)} for p in source_paths],
                    'bounds':{'epsilon_min':1e-12,'epsilon_max':1e-4,'masses':9,'lattice_sizes':[8,12,20],
                              'quadrature_cutoffs':[10,12],'angular_nodes':96},
                    'non_claims':['relativistic completion','empirical agreement','novelty priority','PPN/DOF/FLRW/stability']},
                'randomness':{'used':False,'generator':'','seed':None},
                'run':{'started_at':timestamp,'runtime_seconds':time.monotonic()-start,'exit_status':status},
                'outputs':[{'path':str(path.relative_to(ROOT)),'sha256':sha(path)}],
                'checks':[{'name':k,'passed':bool(v)} for k,v in checks.items()],
                'result':'finite assertions verified' if status==0 else 'one or more finite assertions failed',
                'residual_risks':['No data tested','No relativistic action','No external field or finite source extent',
                                  'Float64 quadrature checks are not certified interval bounds']}
    (HERE/'computation_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'checks':checks,'slopes':slopes,'first_onset':rows[0],
                      'runtime_seconds':manifest['run']['runtime_seconds'],'exit_status':status},indent=2))
    return status


if __name__ == '__main__':
    sys.exit(main())
