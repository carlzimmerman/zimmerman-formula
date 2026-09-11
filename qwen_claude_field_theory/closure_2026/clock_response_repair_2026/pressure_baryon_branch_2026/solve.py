#!/usr/bin/env python3
"""Coupled pressure-balanced INITIAL data; not a stationary galaxy spacetime.

Normal-rest P_b=lambda*(sqrt(Z)-1)^(5/2) baryons, homogeneous initial chi,
Kr=Ko=H_bg. Central enthalpy hc is prescribed. The chemical frequency omega
and geometry/lapse are solved together, with a free fluid surface and N(L)=1.
The pressure EOS is extended by zero outside h>0 only for this initial BVP;
the degenerate vacuum boundary has no time-evolution health certificate.
"""
import argparse
import json
from pathlib import Path
import sys
import time
import numpy as np
from scipy.integrate import cumulative_trapezoid, solve_bvp
from scipy.optimize import brentq

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'nonlinear_infall_2026'))
from initial import coefficients


def eos(h,lam):
    h=np.maximum(h,0.)
    pressure=lam*h**2.5
    density=.5*lam*h**1.5*(3*h+5)
    return density,pressure


def solve(hc=.01,lam=50.,outer=3.,points=500,tolerance=2e-7,seed=.2):
    start=time.monotonic();c=coefficients();S,l0,lb,M=[c[n] for n in ('S','lambda0','lambdab','M2')]
    if hc<=0 or lam<=0:raise ValueError('positive matter parameters required')
    rhoc,pc=eos(hc,lam)
    threshold=lb*(rhoc+3*pc)/(l0*hc)
    if threshold<1:
        return dict(status='excluded_by_necessary_binding_bound',hc=hc,lam=lam,
                    binding_ratio=float(threshold),scope='this homogeneous-clock initial family',
                    assumption='central enthalpy hc is the global fluid maximum')
    rmin=1e-5;mesh=np.linspace(rmin,outer,points)
    width=min(.6,max(.03,np.sqrt(hc/rhoc)))
    D0=(1+seed)/(1+hc);delta=D0*np.exp(-mesh*mesh/(2*width*width))
    Nguess=1-hc*delta
    hguess=hc*(delta-seed)/Nguess
    rguess,pguess=eos(hguess,lam)
    enclosed=cumulative_trapezoid(rguess*mesh*mesh,mesh,initial=0)+rhoc*rmin**3/3
    guess=np.array([enclosed,delta,-mesh*delta/width**2])

    def rhs(r,y,param):
        mass,D,Dp=y;W=param[0];N=1-hc*D
        f=1-mass/(M*r)
        if np.min(N)<=0 or np.min(f)<=0:raise ValueError('Newton iterate left positive metric patch')
        h=hc*(D-W)/N;rho,p=eos(h,lam)
        fp=(1-f)/r-rho*r/M
        return np.array([rho*r*r,Dp,(l0*D-lb*(rho+3*p)*N/hc)/(S*f)
                         -(2/r+fp/(2*f))*Dp])

    def bc(left,right,param):
        W=param[0];Dc=(1+W)/(1+hc);Nc=1-hc*Dc
        D2=(l0*Dc-lb*(rhoc+3*pc)*Nc/hc)/(3*S)
        return np.array([left[0]-rhoc*rmin**3/3,left[1]-Dc-D2*rmin*rmin/2,
                         left[2]-D2*rmin,right[1]])

    raw=solve_bvp(rhs,bc,mesh,guess,p=[seed],tol=tolerance,max_nodes=18000)
    if not raw.success:return dict(status='solver_failed',message=raw.message,hc=hc,lam=lam)
    r=np.linspace(rmin,outer,2501);mass,D,Dp=raw.sol(r);N=1-hc*D;f=1-mass/(M*r)
    W=float(raw.p[0]);omega=1-hc*W;h=hc*(D-W)/N;rho,p=eos(h,lam)
    active=np.flatnonzero(h>0);surface=float(r[active[-1]]) if len(active) else 0.
    if len(active) and active[-1]+1<len(r):
        index=active[-1]
        surface=brentq(lambda x:raw.sol(x)[1]-W,r[index],r[index+1],xtol=1e-12)
    probe=raw.x[:-1]+.371*np.diff(raw.x);yy=raw.sol(probe)
    residual=raw.sol(probe,1)-rhs(probe,yy,raw.p)
    scales=np.maximum(np.max(abs(rhs(probe,yy,raw.p)),axis=1),1e-8)
    offgrid=np.max(abs(residual),axis=1)/scales
    q,H,g=[c[n] for n in ('q','H','gamma')]
    # Fixed global a0, diagnostic only; no measured-G calibration is assumed.
    a0=np.sqrt(c['Lambda']/(32*np.pi));at=max(surface*1.5,.1)
    vacuum=bool(0<omega<1 and surface<outer*.8)
    force=newton=None
    if vacuum and at<=outer:
        mass_at,D_at,_=raw.sol(at);N_at=1-hc*D_at
        rho_at,p_at=eos(hc*(D_at-W)/N_at,lam)
        qdot=-(N_at*(3*c['J']*(H+g*q**3/M)+g*q*q*(rho_at+3*p_at)/M)+c['C'])/c['Bhat']
        newton=float(mass_at/(2*M*at*at))
        force=float(newton+at*p_at/(2*M)+at*(c['U']*(1-N_at)+2*g*q*q*(qdot-c['qdot']))/(2*M*N_at))
    result=dict(status='initial_bvp_solved',hc=hc,lam=lam,outer=outer,points=points,
                tolerance=tolerance,seed=seed,omega=omega,binding_ratio=float(threshold),
                surface=surface,lapse_min=float(N.min()),f_min=float(f.min()),
                total_areal_mass=float(4*np.pi*mass[-1]),max_offgrid_relative=offgrid.tolist(),
                max_boundary_residual=float(max(abs(bc(raw.y[:,0],raw.y[:,-1],raw.p)))),
                vacuum_exterior=vacuum,
                central_maximum=bool(np.max(h)<=hc*(1+2e-5)),
                force_radius=at if force is not None else None,areal_force=force,bare_newton_force=newton,
                force_ratio=force/newton if newton else None,
                mond_balance=(-np.expm1(-force/a0)*force/newton) if force is not None and force>=0 and newton>0 else None,
                seconds=time.monotonic()-start,
                non_claims=['not a static spacetime','not a galactic MOND law','not a vacuum-boundary stability proof'])
    result['expanding_density_rate_at_center']=-3*c['H']*float(N[0])*(rhoc+pc)
    if not result['vacuum_exterior'] or not result['central_maximum'] or max(offgrid)>1e-3:
        result['status']='physical_or_residual_gate_failed'
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--hc',type=float,default=.01)
    parser.add_argument('--lam',type=float,default=50.);parser.add_argument('--outer',type=float,default=3.)
    parser.add_argument('--points',type=int,default=500);parser.add_argument('--seed',type=float,default=.2)
    args=parser.parse_args()
    try:answer=solve(hc=args.hc,lam=args.lam,outer=args.outer,points=args.points,seed=args.seed)
    except ValueError as exc:answer=dict(status='solver_domain_failure',message=str(exc))
    print(json.dumps(answer,indent=2))
    sys.exit(0 if answer['status'] in ('initial_bvp_solved','excluded_by_necessary_binding_bound') else 1)
