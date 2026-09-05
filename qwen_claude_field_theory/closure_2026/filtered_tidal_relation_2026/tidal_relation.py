#!/usr/bin/env python3
"""Central phantom Hessian from the existing action's linear external-field response."""
import hashlib
import json
import math
from pathlib import Path
import platform
import subprocess
import sys
import time
from datetime import datetime,timezone
from functools import lru_cache

import numpy as np
import scipy
from scipy.integrate import quad
from scipy.optimize import brentq
import sympy as sp

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
PARENT=HERE.parent/'smoothed_onset_action_2026'
sys.path.insert(0,str(PARENT))
from onset_action_gate import phantom


def coefficients(y):
    if not math.isfinite(y) or y<=0:
        raise ValueError('nonzero finite background y required')
    E=math.exp(-y); mu=-math.expm1(-y); lam=mu+y*E
    return E/mu, -y*E/(mu*lam)


def symbolic_checks():
    z,A,B,y=sp.symbols('z A B y',real=True)
    par=sp.integrate(z*z*(A+B*z*z)/2,(z,-1,1))
    perp=sp.integrate((1-z*z)*(A+B*z*z)/4,(z,-1,1))
    Q=perp-par; D=2*perp+par
    mu=1-sp.exp(-y); s=y*mu; lam=sp.diff(s,y); nu=1/mu
    exact_B=sp.simplify(s*sp.diff(nu,y)/lam)
    return {
        'angular_parallel':str(sp.simplify(par-(5*A+3*B)/15)),
        'angular_perpendicular':str(sp.simplify(perp-(5*A+B)/15)),
        'division_free_identity':str(sp.simplify((15*A+5*B)*Q+2*B*D)),
        'exact_B':str(sp.simplify(exact_B+y*sp.exp(-y)/(mu*lam))),
        'kernel_ratio':str(sp.simplify((-2*exact_B/(15*(nu-1)+5*exact_B))
                                       -2*y/(5*(3*lam-y)))),
        'deep_ratio':str(sp.simplify(sp.limit(2*y/(5*(3*lam-y)),y,0,dir='+')-sp.Rational(2,25))),
    }


def tangent_error(y):
    se=y*(-math.expm1(-y)); p=np.array([0.,0.,se]); h=se*2e-5
    def f(v):
        norm=np.linalg.norm(v)
        return phantom(norm)*v/norm
    numeric=np.column_stack([(f(p+h*e)-f(p-h*e))/(2*h) for e in np.eye(3)])
    A,B=coefficients(y)
    expected=np.diag([A,A,A+B])
    return float(np.linalg.norm(numeric-expected)/np.linalg.norm(expected))


@lru_cache(maxsize=None)
def radial_factor(kernel,xi,radius):
    if xi<=0 or radius<0:
        raise ValueError('positive xi and nonnegative source radius required')
    def sigma(q):
        if kernel=='gaussian': return math.exp(-q*q/2)
        if kernel=='helmholtz': return 1/(1+q*q)
        if kernel=='quartic': return 1/(1+q**4)
        raise ValueError(kernel)
    integral,error=quad(lambda q:q*q*sigma(q)**2*math.exp(-0.5*(radius/xi*q)**2),
                         0,np.inf,epsabs=1e-12,epsrel=3e-12,limit=180)
    if error>max(1e-11,1e-10*abs(integral)):
        raise ArithmeticError('radial quadrature error too large')
    return integral/(2*np.pi**2*xi**3)


def hessian_numeric(y,kernel,xi,radius,axis=None,nz=24):
    """Direct directional integral, G=M=1; no precomputed angular moments."""
    axis=np.array([0.,0.,1.]) if axis is None else np.asarray(axis,float)
    axis=axis/np.linalg.norm(axis)
    z,w=np.polynomial.legendre.leggauss(nz)
    phi=(np.arange(2*nz)+0.5)*2*np.pi/(2*nz)
    zz,pp=np.meshgrid(z,phi,indexing='ij')
    nodes=np.stack([np.sqrt(1-zz**2)*np.cos(pp),np.sqrt(1-zz**2)*np.sin(pp),zz],axis=-1)
    A,B=coefficients(y)
    weight=(w[:,None]/(2*len(phi)))*(A+B*(nodes@axis)**2)
    angular=np.einsum('ab,abi,abj->ij',weight,nodes,nodes)
    return 4*np.pi*radial_factor(kernel,xi,radius)*angular


def hessian_formula(y,kernel,xi,radius,axis=None):
    axis=np.array([0.,0.,1.]) if axis is None else np.asarray(axis,float)
    axis=axis/np.linalg.norm(axis)
    A,B=coefficients(y)
    return 4*np.pi*radial_factor(kernel,xi,radius)/15*((5*A+B)*np.eye(3)+2*B*np.outer(axis,axis))


def observables(H,axis=None):
    e=np.array([0.,0.,1.]) if axis is None else np.asarray(axis,float)
    e=e/np.linalg.norm(e)
    parallel=float(e@H@e); trace=float(np.trace(H)); perpendicular=(trace-parallel)/2
    return perpendicular-parallel,trace,parallel,perpendicular


def identity_error(H,y,axis=None):
    A,B=coefficients(y); Q,D,_,_=observables(H,axis)
    return abs((15*A+5*B)*Q+2*B*D)/((abs(15*A+5*B)+2*abs(B))*np.linalg.norm(H))


def thresholds():
    lam=lambda y:-math.expm1(-y)+y*math.exp(-y)
    return {'parallel_zero_y':brentq(lambda y:3*y-5*lam(y),1,3),
            'trace_zero_y':brentq(lambda y:y-3*lam(y),2,5),
            'perpendicular_zero_y':brentq(lambda y:y-5*lam(y),4,7)}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    started=datetime.now(timezone.utc).isoformat(); clock=time.monotonic()
    rows=[]
    directions=[np.array([0.,0.,1.]),np.array([1.,2.,3.])/np.sqrt(14)]
    for y in [0.03,0.3,1.,2.5,4.,6.]:
        for kernel in ['gaussian','helmholtz','quartic']:
            for xi in [0.4,1.,2.5]:
                for radius in [0.,0.3,2.]:
                    for axis in directions:
                        H=hessian_numeric(y,kernel,xi,radius,axis)
                        F=hessian_formula(y,kernel,xi,radius,axis)
                        Q,D,par,perp=observables(H,axis)
                        rows.append({'y':y,'filter':kernel,'xi':xi,'source_radius':radius,
                                     'axis':axis.tolist(),'Q2':Q,'trace_H':D,
                                     'H_parallel':par,'H_perp':perp,'Q2_over_trace':Q/D,
                                     'identity_error':identity_error(H,y,axis),
                                     'formula_error':float(np.linalg.norm(H-F)/np.linalg.norm(F))})
    sym=symbolic_checks()
    fd={str(y):tangent_error(y) for y in [0.03,0.5,1.,2.5,5.]}
    refinement=[]
    for y in [0.03,1.,4.]:
        H=hessian_numeric(y,'gaussian',1.,0.3,directions[1],nz=24)
        F=hessian_numeric(y,'gaussian',1.,0.3,directions[1],nz=40)
        refinement.append(float(np.linalg.norm(H-F)/np.linalg.norm(F)))
    # Deliberate outside-assumption control: anisotropic spectral weighting.
    z,w=np.polynomial.legendre.leggauss(64); A,B=coefficients(1.)
    weight=1+0.8*z*z
    par=np.dot(w,z*z*(A+B*z*z)*weight)/2
    perp=np.dot(w,(1-z*z)*(A+B*z*z)*weight)/4
    negative_control=identity_error(np.diag([perp,perp,par]),1.)
    checks={'symbolic_identities':all(v=='0' for v in sym.values()),
            'nonlinear_tangent':max(fd.values())<2e-7,
            'angular_formula':max(r['formula_error'] for r in rows)<2e-12,
            'filter_independent_identity':max(r['identity_error'] for r in rows)<2e-12,
            'angular_refinement':max(refinement)<2e-12,
            'anisotropy_breaks_identity':negative_control>1e-3}
    checks={name:bool(value) for name,value in checks.items()}
    status=0 if all(checks.values()) else 1
    results={'scope':'linear external-field central phantom Hessian, no data or covariant closure',
             'symbolic':sym,'tangent_errors':fd,'angular_refinement_errors':refinement,
             'anisotropic_control_identity_error':negative_control,'thresholds':thresholds(),
             'rows':rows,'checks':checks,'exit_status':status}
    out=HERE/'results.json'; out.write_text(json.dumps(results,indent=2)+'\n')
    inputs=[HERE/'tidal_relation.py',HERE/'test_tidal_relation.py',HERE/'CONTRACT.md',PARENT/'onset_action_gate.py']
    manifest={'schema_version':1,'claim_id':'filtered-central-tidal-consistency-relation',
              'repository':{'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                            'dirty':bool(subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True))},
              'command':'python3 '+str((HERE/'tidal_relation.py').relative_to(ROOT)),
              'environment':{'software':[f'Python {platform.python_version()}',f'NumPy {np.__version__}',
                                         f'SciPy {scipy.__version__}',f'SymPy {sp.__version__}'],
                             'hardware':platform.platform()},
              'mathematics':{'assertion_tested':'isotropic-filter-independent central tidal identity in linear response',
                             'coefficient_domain':'SymPy exact; float64 quadrature',
                             'conventions':'G=M=1, Q2=Hperp-Hparallel, H=phantom potential Hessian',
                             'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p)} for p in inputs],
                             'bounds':{'cases':len(rows),'y':[0.03,0.3,1.,2.5,4.,6.],
                                       'xi':[0.4,1.,2.5],'source_radius':[0.,0.3,2.],
                                       'angular_resolutions':[24,40],'filters':['gaussian','helmholtz','quartic']},
                             'non_claims':['nonlinear source solution','physical external-field calibration',
                                           'novelty priority','empirical agreement','relativistic completion']},
              'randomness':{'used':False,'generator':'','seed':None},
              'run':{'started_at':started,'runtime_seconds':time.monotonic()-clock,'exit_status':status},
              'outputs':[{'path':str(out.relative_to(ROOT)),'sha256':sha(out)}],
              'checks':[{'name':k,'passed':v} for k,v in checks.items()],
              'result':'finite checks verified' if status==0 else 'finite check failed',
              'residual_risks':['Linearization only','Isotropy and constant background required',
                                'Float64 quadrature, not interval bounds','No data tested']}
    (HERE/'computation_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'cases':len(rows),'checks':checks,'thresholds':thresholds(),
                      'max_identity_error':max(r['identity_error'] for r in rows),
                      'max_formula_error':max(r['formula_error'] for r in rows),
                      'anisotropic_control_error':negative_control,
                      'runtime_seconds':manifest['run']['runtime_seconds'],'exit_status':status},indent=2))
    return status


if __name__=='__main__':
    sys.exit(main())
