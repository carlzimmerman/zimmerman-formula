#!/usr/bin/env python3
"""Exact soft-branch regularity audit and independently checked mode evolution."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import sys
import time
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key]='1'
import mpmath as mp
import numpy as np
import scipy
from scipy.linalg import expm
import sympy as s
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--mutate',action='store_true');args=ap.parse_args()
mode='mutate' if args.mutate else 'main';out=HERE/mode;out.mkdir(exist_ok=True)
started=time.monotonic();checks={}
def check(name,value):checks[name]=bool(value)
k,rho,C,gamma,theta,v0,lam=s.symbols('k rho C gamma theta v0 lam',real=True)
B=s.Matrix([[0,-s.I*k*rho],[-s.I*(C/k+gamma*theta*k),0]])
omega2=rho*(C+gamma*theta*k*k)
check('generator_square',s.simplify(B*B+omega2*s.eye(2))==s.zeros(2))
A=s.Matrix([[v0,rho],[gamma*theta,v0]])
check('characteristic_polynomial',s.expand((lam*s.eye(2)-A).det()-(lam-v0)**2+rho*gamma*theta)==0)
soft=A.subs({v0:0,rho:s.Rational(-1,2),theta:0,gamma:1})
check('soft_Jordan_nonzero_nilpotent',soft!=s.zeros(2) and soft**2==s.zeros(2))

# The characteristic solution is exact for the pressureless principal system.
a,t=s.symbols('a t',real=True)
initial=s.Integer(1) if args.mutate else -s.sin(a)
X=a+t*initial;J=s.diff(X,a);density=-s.Rational(1,2)/J
dx=lambda f:s.diff(f,a)/J
dt=lambda f:s.diff(f,t)-initial*s.diff(f,a)/J
continuity=s.simplify(dt(density)+dx(density*initial))
momentum=s.simplify(dt(initial)+initial*dx(initial))
check('characteristic_continuity',continuity==0)
check('characteristic_momentum',momentum==0)
check('compression_witness',J.subs({a:0,t:1})==0)
characteristics=dict(X=str(X),Jacobian=str(J),density=str(density),
    continuity_residual=str(continuity),momentum_residual=str(momentum),
    scope='Pressureless principal truncation only; not a full-v3s solution or a counterexample to local existence.')

def generator(wavenumber,background,stiffness,Cvalue=1.):
    return np.array([[0,-1j*wavenumber*background],[-1j*(Cvalue/wavenumber+stiffness*wavenumber),0]],complex)
def exact(mat,omega_sq):
    if omega_sq==0:return np.eye(2)+mat
    w=np.sqrt(complex(omega_sq))
    return np.cos(w)*np.eye(2)+np.sin(w)/w*mat
def rk4(mat,steps):
    # Constant-coefficient RK4 polynomial, applied at every declared time step.
    h=1/steps;I=np.eye(2,dtype=complex)
    R=I+h*mat+(h*mat)@ (h*mat)/2+np.linalg.matrix_power(h*mat,3)/6+np.linalg.matrix_power(h*mat,4)/24
    U=I.copy()
    for _ in range(steps):U=R@U
    return U
footings={'canonical':9.3603e-11,'alt':1.1312e-10};rows={}
background=.5 if args.mutate else -.5;stiffness=1. if args.mutate else 0.
for foot,a0 in footings.items():
    cases=[];weighted=[]
    for q in (8,16,32,64,128,256):
        mat=generator(q,background,stiffness)
        U=exact(mat,background*(1+stiffness*q*q));ref=expm(mat)
        with mp.workdps(50):
            m=mp.matrix([[0,-mp.j*q*mp.mpf(str(background))],[-mp.j*(mp.mpf(1)/q+mp.mpf(str(stiffness))*q),0]])
            hp=mp.expm(m)
            high=np.array([[complex(hp[i,j]) for j in range(2)] for i in range(2)])
        norm=float(np.linalg.norm(U,2));den=float(np.linalg.norm(U))
        low,fine=rk4(mat,4096),rk4(mat,8192)
        D=np.diag([1/q,1]);weighted.append(D@U@np.diag([q,1]))
        shear=generator(q,background,0.,0.)
        known=float(np.linalg.norm(expm(shear)-(np.eye(2)+shear)))
        cases.append(dict(k=q,norm=norm,norm_over_k=norm/q,
            scipy_relative=float(np.linalg.norm(U-ref)/den),mp50_relative=float(np.linalg.norm(U-high)/den),
            rk4_4096_relative=float(np.linalg.norm(low-U)/den),rk4_8192_relative=float(np.linalg.norm(fine-U)/den),
            rk4_pair_relative=float(np.linalg.norm(low-fine)/den),known_shear_absolute=known,
            positive_stiff_bound=float(np.sqrt(2+2/q**2)),omega_squared=background*(1+stiffness*q*q)))
    asymptotic=.5*np.sinh(np.sqrt(.5))/np.sqrt(.5)
    ratio=cases[-1]['norm']/cases[-2]['norm']
    dev=max(float(np.linalg.norm(w-weighted[0])) for w in weighted)
    rows[foot]=dict(a0_m_s2=a0,length_m=24*3.0856775814913673e16,
        time_unit_seconds=float(np.sqrt(24*3.0856775814913673e16/a0)),cases=cases,
        last_ratio=ratio,main_asymptotic_coefficient=float(asymptotic),
        asymptotic_relative=float(abs(cases[-1]['norm_over_k']/asymptotic-1)),
        polarization_variable_propagator_change=dev)
    check(foot+'_independent_exponentials',max(max(r['scipy_relative'],r['mp50_relative']) for r in cases)<=1e-10)
    check(foot+'_time_convergence',max(max(r['rk4_4096_relative'],r['rk4_8192_relative'],r['rk4_pair_relative']) for r in cases)<=1e-4)
    check(foot+'_shear_known',max(r['known_shear_absolute'] for r in cases)<=1e-10)
    check(foot+'_zero_time_known',np.array_equal(expm(mat*0),np.eye(2)))
    check(foot+'_linear_k_witness',1.95<=ratio<=2.05 and rows[foot]['asymptotic_relative']<=1e-3)
    if args.mutate:check(foot+'_positive_stiff_control_bound',all(r['norm']<=r['positive_stiff_bound']*(1+1e-12)<1.5 for r in cases))
    else:check(foot+'_polarization_regularity_repair',dev<=1e-10)

sources=[Path(__file__),HERE/'FROZEN_CRITERIA.md',ROOT/'rebuild_2026_10_22/X3_switched_stiffness/x3_switched_stiffness.py',
         ROOT/'rebuild_2026_10_22/H4_v3_saddle_stability/README.md',ROOT/'astra_goal_2026_11_05/AZ34_switched_relativity/STRUCTURAL_AUDIT.md']
result=dict(mode=mode,label='NO VERDICT full nonlinear well-posedness',checks=checks,footings=rows,
    generator=str(B),principal_matrix=str(A),characteristics=characteristics,
    interpretation='Soft-branch density/velocity equal-order norm has derivative loss despite bounded modal growth. Polarization/velocity variables remove this frozen-mode loss. Neither conclusion establishes nonlinear interface evolution.',
    inputs={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
    software=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,sympy=s.__version__,mpmath=mp.__version__),
    seconds=time.monotonic()-started,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024),
    statement='kappa = 1/2 FITTED; not theory closed')
tmp=out/'results.tmp';tmp.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');os.replace(tmp,out/'results.json')
print(json.dumps(dict(mode=mode,checks=checks,metrics={f:{k:r[k] for k in ('last_ratio','asymptotic_relative','polarization_variable_propagator_change')} for f,r in rows.items()}),indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
