#!/usr/bin/env python3
"""Conditional GR branch and incoming Schwarzschild flow, with a flat-profile control."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import sys
import time
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key]='1'
import numpy as np
import scipy
from scipy.integrate import solve_ivp,quad
from scipy.optimize import brentq
import sympy as s
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--mutate',action='store_true');args=ap.parse_args()
mode='mutate' if args.mutate else 'main';out=HERE/mode;out.mkdir(exist_ok=True)
start=time.monotonic();checks={}
def check(name,val):checks[name]=bool(val)
r,M,E=s.symbols('r M E',positive=True)
f=1-2*M/r;Tp=s.sqrt(E*E-(1 if args.mutate else f))/(1 if args.mutate else f)
Q2=s.simplify(E*E/f-f*Tp*Tp);Q=s.sqrt(Q2)
nl=[-E/Q,-Tp/Q];nu=[-nl[0]/f,f*nl[1]]
Gamma={(0,0,1):s.diff(f,r)/(2*f),(0,1,0):s.diff(f,r)/(2*f),
       (1,0,0):f*s.diff(f,r)/2,(1,1,1):-s.diff(f,r)/(2*f)}
acc=[s.simplify(nu[1]*s.diff(nl[i],r)-sum(nu[j]*Gamma.get((k,j,i),0)*nl[k] for j in range(2) for k in range(2))) for i in range(2)]
check('normalized_unit_vector',s.simplify(sum(nl[i]*nu[i] for i in range(2))+1)==0)
check('Q_equals_one',s.simplify(Q2-1)==0)
check('geodesic_acceleration',all(v==0 for v in acc))
u,a,K,gamma,psi,mu2,qq=s.symbols('u a K gamma psi mu2 Q',positive=True)
W=(-a*u-a*a*s.log(1-u/a))/K
check('capped_W_value_and_first_variation',W.subs(u,0)==0 and s.diff(W,u).subs(u,0)==0)
check('switch_value_and_first_variation',all(expr.subs(psi,0)==0 and s.diff(expr,psi).subs(psi,0)==0 for expr in (gamma*psi*psi/2,s.Integer(0))))
Kq=mu2*(qq-1)**2/(2*K)
check('KQ_value_and_first_variation',Kq.subs(qq,1)==0 and s.diff(Kq,qq).subs(qq,1)==0)
known=[]
for energy in (s.Integer(1),s.Rational(13,12),s.Rational(5,3)):
    known.append(dict(E=str(energy),Q2_minus1=str(s.simplify((Q2-1).subs(E,energy))),
        acceleration_at_r10M=[str(s.N(v.subs({E:energy,M:1,r:10}),30)) for v in acc]))
eps,R,B=s.symbols('epsilon R B',positive=True)
force=-1/R**2+B**2/(1-eps)/R**3-3*eps*B**2/(1-eps)/R**4
check('Newtonian_force_limit',s.simplify(s.limit(force,eps,0)+1/R**2-B**2/R**3)==0)

GM=1.32712440018e20;c=299792458.;RSUN=6.957e8
strength=0 if args.mutate else 1
def solve(speed,impact,tight):
    e=(speed/c)**2;E2=1/(1-e);en=math.sqrt(E2);R0=math.sqrt(100**2+impact**2)
    def radial_sq(R):return E2+2*strength/R-E2*impact**2/R**2+2*strength*e*E2*impact**2/R**3
    def integrand(u):return en*impact/math.sqrt(E2+2*strength*u-E2*impact**2*u*u+2*strength*e*E2*impact**2*u**3)
    tol=1e-12 if tight else 1e-10
    angle,err=quad(integrand,0,1/R0,epsabs=tol,epsrel=tol)
    y0=[R0,-math.sqrt(radial_sq(R0)),math.pi-angle,0.]
    def rhs(t,y):
        radius,ur,theta,T=y
        return [ur,-strength/radius**2+E2*impact**2/radius**3-3*strength*e*E2*impact**2/radius**4,
                -en*impact/radius**2,en/(1-2*strength*e/radius)]
    def axis(t,y):return y[2]
    axis.direction=-1;axis.terminal=True
    def peri(t,y):return y[1]
    peri.direction=1;peri.terminal=False
    sol=solve_ivp(rhs,(0,1000),y0,method='DOP853',rtol=1e-11 if tight else 1e-9,
                  atol=1e-13 if tight else 1e-11,events=(axis,peri),dense_output=True)
    ts=np.linspace(0,sol.t[-1],1025);Y=sol.sol(ts);radius,ur,theta,T=Y
    # Evaluate the Schwarzschild invariant even for the flat-profile mutant.
    energy_scaled=ur*ur-E2-2/radius+E2*impact**2/radius**2-2*e*E2*impact**2/radius**3
    drift=float(np.max(np.abs(energy_scaled-energy_scaled[0])))
    crossing=bool(len(sol.t_events[0]));pericenter=sol.y_events[1][0,0] if len(sol.t_events[1]) else None
    # Independent turning-point root of the exact radial energy equation.
    grid=np.geomspace(max(10*e,1e-5),R0,2000)
    brackets=[(x,y) for x,y in zip(grid[:-1],grid[1:]) if radial_sq(x)*radial_sq(y)<0]
    root=brentq(radial_sq,*brackets[-1],xtol=1e-13) if brackets else None
    rc=GM/speed**2
    return dict(success=bool(sol.success),angle=angle,angle_quad_error=err,
        crossing=crossing,crossing_radius=float(sol.y_events[0][0,0]) if crossing else None,
        crossing_time=float(sol.y_events[0][0,3]) if crossing else None,
        pericenter=float(pericenter) if pericenter is not None else None,
        turning_root=float(root) if root is not None else None,
        turning_relative=abs(float(pericenter/root-1)) if pericenter is not None and root is not None else None,
        capture_radius_m=rc,pericenter_m=float(pericenter*rc) if pericenter is not None else None,
        scaled_energy_drift=drift,
        flat_ray_x_relative=float(np.max(np.abs(radius*np.sin(theta)/impact-1))),steps=len(sol.t))

footings={'canonical':9.3603e-11,'alt':1.1312e-10};rows={}
for foot,a0 in footings.items():
    rows[foot]=dict(a0_m_s2=a0,cases={})
    for speed in (220000.,369000.):
        for impact in (2.,5.,10.,20.):
            lo,hi=solve(speed,impact,False),solve(speed,impact,True)
            errors={}
            for key in ('pericenter','crossing_radius','crossing_time'):
                if hi[key] is not None and lo[key] is not None:errors[key]=abs(lo[key]/hi[key]-1)
            agreement=lo['crossing']==hi['crossing']
            name=f'{int(speed/1000)}kms_B{impact:g}'
            rows[foot]['cases'][name]=dict(coarse=lo,fine=hi,convergence_relative=errors)
            check(foot+'_'+name+'_convergence',agreement and max(errors.values())<=1e-5 and abs(lo['angle']-hi['angle'])<=1e-8)
            check(foot+'_'+name+'_integration',lo['success'] and hi['success'] and hi['turning_relative']<=1e-7)
            check(foot+'_'+name+'_vacuum_periapsis',hi['pericenter_m']>RSUN)
            check(foot+'_'+name+'_Schwarzschild_energy',hi['scaled_energy_drift']<=1e-7)
            check(foot+'_'+name+'_focusing_witness',hi['crossing'])
            if args.mutate:check(foot+'_'+name+'_flat_known',hi['flat_ray_x_relative']<=1e-7)

sources=[Path(__file__),HERE/'FROZEN_CRITERIA.md',ROOT/'rebuild_2026_10_22/AS3_ppn_and_khronon_scalar/README.md']
result=dict(mode=mode,label='NO VERDICT selected moving-Sun solution',checks=checks,footings=rows,
    exact=dict(Q2=str(Q2),acceleration=list(map(str,acc)),known=known),
    scope='Conditional extra-sector-free GR branch; incoming-flow focusing warns about caustics. No matching to Galactic polarization or actual PPN prediction.',
    inputs={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
    software=dict(sympy=s.__version__,scipy=scipy.__version__,numpy=np.__version__),
    seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024),
    statement='kappa = 1/2 FITTED; not theory closed')
tmp=out/'branch_and_flow.tmp';tmp.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');os.replace(tmp,out/'branch_and_flow.json')
print(mode,sum(checks.values()),'/',len(checks),'failed',[k for k,v in checks.items() if not v],flush=True)
raise SystemExit(0 if all(checks.values()) else 1)
