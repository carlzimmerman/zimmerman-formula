#!/usr/bin/env python3
"""Direct variation of the T-B binary action and spectral orbital frequencies.

G=a0=xi=1 unless stated; outputs are conditional theory checks, not data.
"""
from datetime import datetime, timezone
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import platform
import subprocess
import sys
import time

import numpy as np
import scipy
from scipy.special import gammainc
import sympy as sp

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]

def inverse_array(s):
    s=np.asarray(s,dtype=float)
    if np.any(s<0) or not np.isfinite(s).all():
        raise ValueError('finite nonnegative acceleration required')
    y=s+np.sqrt(s)
    for _ in range(12):
        mu=-np.expm1(-y)
        den=mu+y*np.exp(-y)
        y-=np.divide(y*mu-s,den,out=np.zeros_like(y),where=den!=0)
    return y

def flux(p):
    s=np.linalg.norm(p,axis=-1); y=inverse_array(s)
    fac=np.divide(y*np.exp(-y),s,out=np.zeros_like(s),where=s!=0)
    return p*fac[...,None]

@lru_cache(maxsize=1)
def q_coefficients():
    y=sp.Symbol('y')
    q=2-2*(1+y)*sp.exp(-y)-y*y*sp.exp(-2*y)
    poly=sp.series(q,y,0,18).removeO().expand()
    return np.array([float(poly.coeff(y,j)) for j in range(18)])

def dual_q_array(s):
    y=inverse_array(s)
    direct=2-2*(1+y)*np.exp(-y)-y*y*np.exp(-2*y)
    series=np.polynomial.polynomial.polyval(y,q_coefficients())
    return np.where(y<.1,series,direct)

def newton_kernel(x):
    """Gradient and Hessian of -erf(r/sqrt(2))/r, unit source/filter width."""
    x=np.asarray(x,float); r=np.linalg.norm(x,axis=-1)
    # The analytic small-r branch below is used there; keep the unused
    # direct branch finite too, since np.where evaluates both arguments.
    safe=np.maximum(r,.05); r2=r*r; c=math.sqrt(2/math.pi)
    F=gammainc(1.5,r2/2)
    gamma=np.divide(F,safe**3)
    slope=c*np.exp(-r2/2)/safe**2-3*F/safe**5
    gamma=np.where(r<.05,c*(1/3-r2/10+r2**2/56-r2**3/432),gamma)
    slope=np.where(r<.05,c*(-1/5+r2/14-r2**2/72+r2**3/528),slope)
    H=gamma[...,None,None]*np.eye(3)+slope[...,None,None]*x[..., :,None]*x[...,None,:]
    return gamma[...,None]*x,H

@lru_cache(maxsize=8)
def grid(n):
    """All-space radial map plus independent angular quadrature."""
    nodes,w=np.polynomial.legendre.leggauss(n)
    t=(nodes+1)/2; r=np.tan(np.pi*t/2)
    rw=w/2*(np.pi/2)*(1+r*r)*r*r
    phi=(np.arange(2*n)+.5)*np.pi/n
    zz,pp=np.meshgrid(nodes,phi,indexing='ij')
    directions=np.stack([np.sqrt(1-zz*zz)*np.cos(pp),
                         np.sqrt(1-zz*zz)*np.sin(pp),zz],axis=-1)
    angw=np.broadcast_to(w[:,None]*np.pi/n,(n,2*n))
    x=(r[:,None,None,None]*directions[None,...]).reshape(-1,3)
    weight=(rw[:,None,None]*angw[None,...]).ravel()
    return x,weight

def pair_fields(M,fraction,d,n,axis):
    if M<=0 or not 0<fraction<1 or d<=0:
        raise ValueError('positive mass/separation and interior mass fraction required')
    axis=np.asarray(axis,float); axis=axis/np.linalg.norm(axis)
    masses=M*np.array([fraction,1-fraction])
    positions=np.array([-(1-fraction)*d*axis,fraction*d*axis])
    x,w=grid(n)
    p1,H1=newton_kernel(x-positions[0]); p2,H2=newton_kernel(x-positions[1])
    return masses,positions,w,masses[0]*p1+masses[1]*p2,(H1,H2)

def binary_accelerations(M,fraction,d,n=42,axis=(0,0,1),external=(0,0,0)):
    """Both forces from dL_red/dx_a: no assigned total-mass force law."""
    masses,positions,w,p,Hs=pair_fields(M,fraction,d,n,axis)
    pe=np.asarray(external,float)
    f=flux(p+pe)-flux(pe)
    return np.array([-np.einsum('n,nij,nj->i',w,H,f)/(4*np.pi) for H in Hs])

def energy_difference(M,fraction,d,n=42):
    """U_ph(d)-U_ph(0), same total-mass reference and infinite-space map."""
    masses,positions,w,p,Hs=pair_fields(M,fraction,d,n,(0,0,1))
    p0=M*newton_kernel(grid(n)[0])[0]
    delta=dual_q_array(np.linalg.norm(p,axis=-1))-dual_q_array(np.linalg.norm(p0,axis=-1))
    return -float(w@delta)/(8*np.pi)

def force_check(M,fraction,d,n=42):
    a=binary_accelerations(M,fraction,d,n=n)
    reduced=M*fraction*(1-fraction)
    derivative=-(reduced*(a[1,2]-a[0,2]))
    step=d*2e-3
    fd=(energy_difference(M,fraction,d+step,n)-energy_difference(M,fraction,d-step,n))/(2*step)
    net=fraction*a[0]+(1-fraction)*a[1]
    return {'energy_derivative_error':float(abs(fd-derivative)/abs(derivative)),
            'momentum_error':float(np.linalg.norm(net)/np.linalg.norm(a[1]-a[0])),
            'force_derivative':float(derivative),'energy_derivative':float(fd)}

def symbolic_frequency():
    R,z,M,a,b,y=sp.symbols('R z M a b y',positive=True)
    V=-M/sp.sqrt(R*R+z*z)+(a*R*R+b*z*z)/2
    O=(sp.diff(V,R)/R).subs(z,0)
    K=(sp.diff(V,R,2)+3*sp.diff(V,R)/R).subs(z,0)
    Z=sp.diff(V,z,2).subs(z,0)
    A,B,C=sp.symbols('A B C',real=True)
    gap=sp.simplify((K-O)/(O-Z)).subs({a:C*(5*A+B),b:C*(5*A+3*B)})
    mu=1-sp.exp(-y); s=y*mu; lam=sp.diff(s,y); nu=1/mu
    exactB=s*sp.diff(nu,y)/lam
    target=3*(5*lam-y)/(2*y)
    return {'radial_derivative':str(sp.simplify(K-M/R**3-4*a)),
            'vertical_derivative':str(sp.simplify(Z-M/R**3-b)),
            'orbital_derivative':str(sp.simplify(O-M/R**3-a)),
            'frequency_identity':str(sp.simplify(gap.subs({A:nu-1,B:exactB})-target))}

def frequency_observables(y,R,n=42,radial_weight='gaussian'):
    """Finite-R derivatives of full Fourier pair potential, G=M=xi=1.

    R^-3 is the analytically unsmoothed Newtonian contribution. Frequency
    differences are formed from anomalous derivatives to avoid cancellation.
    """
    k,w=grid(n); radius=np.linalg.norm(k,axis=1); nhat=k/radius[:,None]
    mu=-math.expm1(-y); lam=mu+y*math.exp(-y)
    nu=1/mu; A=nu-1; B=-y*math.exp(-y)/(mu*lam)
    if radial_weight=='gaussian': sigma2=np.exp(-radius**2)
    elif radial_weight=='gaussian_mixture': sigma2=(.4*np.exp(-radius**2/2)+.6*np.exp(-2*radius**2))**2
    else: raise ValueError(radial_weight)
    weight=4*np.pi*w/(2*np.pi)**3*sigma2*(A+B*nhat[:,2]**2)
    phase=k[:,0]*R
    gradient=float(weight@(nhat[:,0]*np.sin(phase)/radius))
    Hxx=float(weight@(nhat[:,0]**2*np.cos(phase)))
    Hzz=float(weight@(nhat[:,2]**2*np.cos(phase)))
    dO=gradient/R; dK=Hxx+3*dO; dZ=Hzz
    radial_gap=dK-dO; vertical_gap=dO-dZ
    predicted=3*(5*lam-y)/(2*y)
    residual=2*y*radial_gap-3*(5*lam-y)*vertical_gap
    scale=abs(2*y*radial_gap)+abs(3*(5*lam-y)*vertical_gap)
    return {'y':y,'R_over_xi':R,'filter':radial_weight,
            'Omega2':R**-3+dO,'kappa2':R**-3+dK,'vertical2':R**-3+dZ,
            'delta_Omega2':dO,'delta_kappa2':dK,'delta_vertical2':dZ,
            'gap_ratio':radial_gap/vertical_gap,'core_prediction':predicted,
            'identity_error':abs(residual)/scale}

def main():
    started=datetime.now(timezone.utc).isoformat(); clock=time.monotonic()
    force_rows=[]
    for M in [1e-8,1e-6,1e-4]:
        for fraction in [.1,.3,.5,.9]:
            for d in [.02,.06,.2]:
                a=binary_accelerations(M,fraction,d)
                h=-(a[1,2]-a[0,2])/d
                force_rows.append({'epsilon':M,'mass_fraction':fraction,'d_over_xi':d,
                                   'h_measured':float(h),'h_leading':2/9*math.sqrt(M),
                                   'relative_asymptotic_error':float(h/(2/9*math.sqrt(M))-1)})
    freq_rows=[frequency_observables(y,R,radial_weight=kind)
               for y in [.3,1.,2.5,4.,6.] for R in [.01,.03,.1,.3,1.]
               for kind in ['gaussian','gaussian_mixture']]
    variation=force_check(.02,.3,.15,n=52)
    a42=binary_accelerations(1e-6,.3,.06,n=42)
    a58=binary_accelerations(1e-6,.3,.06,n=58)
    refinement=float(np.linalg.norm(a42-a58)/np.linalg.norm(a58))
    spectral_refinement=abs(frequency_observables(1.,.1,n=42)['gap_ratio']/
                            frequency_observables(1.,.1,n=58)['gap_ratio']-1)
    sym=symbolic_frequency()
    core=[r for r in force_rows if r['epsilon']<=1e-6 and r['d_over_xi']<=.06]
    tiny=[r for r in freq_rows if r['R_over_xi']==.01]
    checks={'symbolic_frequency_derivation':all(v=='0' for v in sym.values()),
            'action_force_variation':variation['energy_derivative_error']<2e-5,
            'momentum_conservation':variation['momentum_error']<2e-5,
            'compact_binary_coefficient':max(abs(r['relative_asymptotic_error']) for r in core)<.003,
            'force_resolution':refinement<2e-4,
            'spectral_resolution':spectral_refinement<2e-8,
            'core_frequency_identity':max(r['identity_error'] for r in tiny)<.001,
            'finite_radius_breaks_exact_core_identity':max(r['identity_error'] for r in freq_rows if r['R_over_xi']==1.)>.01}
    checks={k:bool(v) for k,v in checks.items()}; status=0 if all(checks.values()) else 1
    results={'scope':'conditional static binary forces and near-circular frequencies; no empirical or covariant verification',
             'symbolic':sym,'force_rows':force_rows,'frequency_rows':freq_rows,'variation':variation,
             'force_refinement':refinement,'spectral_refinement':spectral_refinement,
             'checks':checks,'exit_status':status}
    output=HERE/'results.json'; output.write_text(json.dumps(results,indent=2)+'\n')
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    inputs=[HERE/'binary_frequency.py',HERE/'test_binary_frequency.py',HERE/'CONTRACT.md']
    manifest={'schema_version':1,'claim_id':'filtered-mond-comparable-mass-and-frequency-law',
              'repository':{'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                            'dirty':bool(subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True))},
              'command':'python3 '+str((HERE/'binary_frequency.py').relative_to(ROOT)),
              'environment':{'software':[f'Python {platform.python_version()}',f'NumPy {np.__version__}',
                                         f'SciPy {scipy.__version__}',f'SymPy {sp.__version__}'],'hardware':platform.platform()},
              'mathematics':{'assertion_tested':results['scope'],'coefficient_domain':'float64 quadrature and exact SymPy',
                             'conventions':'G=a0=xi=1 for force; G=M=xi=1 for linear frequency coefficients',
                             'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p)} for p in inputs],
                             'bounds':{'force_cases':len(force_rows),'frequency_cases':len(freq_rows),
                                       'quadrature_orders':[42,52,58],'all_input_values_in_results':True},
                             'non_claims':['observational discovery','novelty priority','relativistic completion',
                                           'nonlinear external-field binary law','large-amplitude orbital frequencies']},
              'randomness':{'used':False,'generator':'','seed':None},
              'run':{'started_at':started,'runtime_seconds':time.monotonic()-clock,'exit_status':status},
              'outputs':[{'path':str(output.relative_to(ROOT)),'sha256':sha(output)}],
              'checks':[{'name':k,'passed':v} for k,v in checks.items()],
              'result':'bounded checks verified' if status==0 else 'check failed',
              'residual_risks':['finite quadrature','linear external-field approximation','compact-pair and small-oscillation regimes']}
    (HERE/'computation_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'checks':checks,'variation':variation,'force_refinement':refinement,
                      'spectral_refinement':spectral_refinement,
                      'max_core_force_error':max(abs(r['relative_asymptotic_error']) for r in core),
                      'max_core_frequency_error':max(r['identity_error'] for r in tiny),
                      'runtime_seconds':manifest['run']['runtime_seconds'],'exit_status':status},indent=2))
    return status

if __name__=='__main__':
    sys.exit(main())
