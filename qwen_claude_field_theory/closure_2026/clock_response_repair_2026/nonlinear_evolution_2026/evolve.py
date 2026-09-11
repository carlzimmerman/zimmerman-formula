#!/usr/bin/env python3
"""Fourth-order radial jets, second-order lapse solve, RK4 time stepping.

State rows: A, R/r, Kr, Ko, Q, chi_r, theta_r, D, dust-shell positions.
D=A(R/r)^2 rho U_d is the conserved dust coordinate density per r².
The same explicit action supplies all continuum equations through equations.py.
Finite outer lapse N=1 is a boundary assumption, not cosmological matching proof.
This is an experimental solver; convergence gates must pass before its forces
can be interpreted physically. Radial projection also requires a time-consistency
check, provided independently in diagnose.py.
"""
import argparse
import importlib.util
import json
import math
from pathlib import Path
import time

import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.linalg import solve_banded
from scipy.special import gammainc

from constitutive import Model
from equations import evaluate
from center import evaluate_center
from project import project_state


def derivatives(f,spacing,odd=False):
    # Parity supplies actual negative-radius jets; the origin is not an
    # artificial one-sided boundary. Outer rows differentiate a degree-4
    # interpolant and remain outside the reported interior error norms.
    if len(f)<5:raise ValueError("five radial points required")
    extended=np.r_[(-1 if odd else 1)*f[2:0:-1],f]
    first=np.empty_like(f);second=np.empty_like(f)
    first[:-2]=(extended[:-4]-8*extended[1:-3]+8*extended[3:-1]-extended[4:])/(12*spacing)
    second[:-2]=(-extended[:-4]+16*extended[1:-3]-30*extended[2:-2]+16*extended[3:-1]-extended[4:])/(12*spacing**2)
    for index in (-2,-1):
        coordinates=np.arange(-4,1,dtype=float)-(index+1)
        polynomial=np.polynomial.polynomial.polyfit(coordinates,f[-5:]-f[index],4)
        first[index]=polynomial[1]/spacing;second[index]=2*polynomial[2]/spacing**2
    if odd:second[0]=0.
    else:first[0]=0.
    return first,second


class Evolution:
    def __init__(self,amplitude,width,points,outer,tend,gamma,constraint_addition=1.,constrained=True):
        self.amplitude,self.width=amplitude,width
        self.constraint_addition=constraint_addition
        self.constrained=constrained
        self.r=np.linspace(0,outer,points);self.dr=self.r[1]
        self.faces=np.r_[0,(self.r[1:]+self.r[:-1])/2,outer]
        self.volumes=np.diff(self.faces**3)/3
        self.model=Model(tend,gamma)
        rho=amplitude*np.exp(-(self.r/width)**2)
        mass=amplitude*width**3*math.sqrt(math.pi)/4*gammainc(1.5,(self.r/width)**2)
        uniform=1-amplitude*width**2*max(1/3,math.sqrt(math.pi)/4)
        if uniform<=0:raise ValueError("initial uniform f>0 certificate failed")
        f=1-np.divide(mass,self.r,out=np.zeros_like(self.r),where=self.r!=0)
        A=1/np.sqrt(f);bg=self.model.background(0)
        self.initial=np.array([A,np.ones(points),np.full(points,bg["H"]),
                               np.full(points,bg["H"]),np.full(points,bg["q"]),
                               np.zeros(points),np.zeros(points),A*rho,self.r.copy()])
        self.initial_mass=4*math.pi*np.dot(self.volumes,self.initial[7])

    def fields(self,t,state):
        if not np.all(np.isfinite(state)) or np.min(state[7])<0:
            raise ValueError("nonfinite state or negative dust density")
        if self.constrained:
            state=project_state(t,state,self.r,self.model)
        A,b,k,h,Q,u,w,D,_=state;r=self.r
        if not np.all(np.isfinite(state)) or np.min(D)<0:
            raise ValueError("nonfinite state or negative dust density")
        if min(np.min(A),np.min(b))<=0:raise ValueError("metric patch became singular")
        Ar,Arr=derivatives(A,self.dr);br,brr=derivatives(b,self.dr)
        kr,_=derivatives(k,self.dr);hr,_=derivatives(h,self.dr)
        Qr,Qrr=derivatives(Q,self.dr);ur,_=derivatives(u,self.dr,odd=True)
        R=r*b;Rr=b+r*br;Rrr=2*br+r*brr
        Ud=np.sqrt(1+w*w/A**2);rho=D/(A*b*b*Ud)
        Y=u*u/A**2;X=Q*Q-Y
        vals=self.model.jets(t,X,Y)
        vals.update(A=A,Ar=Ar,R=R,Rr=Rr,Rrr=Rrr,k=k,h=h,kr=kr,hr=hr,Q=Q,
                    Qr=Qr,Qrr=Qrr,cr=u,crr=ur,rho=rho,w=w,constraint_addition=self.constraint_addition)
        # The raw spherical chart excludes R=0. Evaluate a duplicate first
        # positive-radius jet at index zero, then impose regular center limits.
        evalvals={key:(np.r_[value[1],value[1:]] if isinstance(value,np.ndarray)
                       and value.shape==r.shape else value) for key,value in vals.items()}
        matrix,forcing,constraints=evaluate(evalvals)
        solved=np.linalg.solve(matrix,forcing)
        center_vals={key:(value[0] if isinstance(value,np.ndarray) and value.shape==r.shape else value)
                     for key,value in vals.items()}
        center_vals.update(a_c=A[0],A2=Arr[0],b2=brr[0],K_c=(k[0]+2*h[0])/3,
                           Q_c=Q[0],Q2=Qrr[0],u1=ur[0])
        center_matrix,center_forcing=evaluate_center(center_vals)
        center_solved=np.linalg.solve(center_matrix,center_forcing)
        acoef,bcoef,c=solved[:,3,0].copy(),solved[:,3,1].copy(),solved[:,3,2].copy()
        bcoef[0]=(4*bcoef[1]-bcoef[2])/3;c[0]=(4*c[1]-c[2])/3
        dx=self.dr
        low=1/dx**2+acoef/(2*dx);diag=-2/dx**2-bcoef;up=1/dx**2-acoef/(2*dx)
        # Exact action-derived regular-origin equation for N_rr, not a
        # coefficient extrapolation from the coordinate-singular equations.
        diag[0]=-2/dx**2-center_solved[2,0];up[0]=2/dx**2;c[0]=center_solved[2,1]
        diag[-1]=1.;low[-1]=0.;c[-1]=1.
        band=np.zeros((3,len(r)));band[0,1:]=up[:-1];band[1]=diag;band[2,:-1]=low[1:]
        N=solve_banded((1,1),band,c)
        if not np.all(np.isfinite(N)) or np.min(N)<=0:raise ValueError("positive lapse lost")
        Nr,Nrr_fd=derivatives(N,dx)
        rate=np.einsum("nij,nj->ni",solved,np.stack([Nr,N,np.ones_like(N)],axis=-1))
        center_rate=center_solved@np.array([N[0],1.])
        rate[0]=[center_rate[0],center_rate[0],center_rate[1],center_rate[2]]
        # Actual Schur principal coefficient, not an expected elliptic sign.
        kinetic=matrix[:,:3,:3]
        schur=matrix[:,3,3]-np.einsum("ni,ni->n",matrix[:,3,:3],
                                      np.linalg.solve(kinetic,matrix[:,:3,3]))
        if np.min(schur[1:])<=0:raise ValueError("preserved lapse principal sign changed")
        return dict(A=A,b=b,k=k,h=h,Q=Q,u=u,w=w,D=D,R=R,Rr=Rr,Rrr=Rrr,Ar=Ar,hr=hr,
                    Qr=Qr,Ud=Ud,rho=rho,N=N,Nr=Nr,rate=rate,constraints=constraints,
                    lapse_residual=Nrr_fd-acoef*Nr-bcoef*N-solved[:,3,2],
                    schur=schur,domain_denominator=vals["domain_denominator"])

    def rhs(self,t,state):
        f=self.fields(t,state);A,b,N=f["A"],f["b"],f["N"]
        out=np.zeros_like(state)
        out[0]=N*A*f["k"];out[1]=N*b*f["h"]
        out[2:5]=f["rate"][:,:3].T
        out[5]=f["Nr"]*f["Q"]+N*f["Qr"]
        out[6]=derivatives(N*f["Ud"],self.dr)[0]
        out[5,0]=out[6,0]=0.
        velocity=-N*f["w"]/(A*A*f["Ud"])
        flux_no_r2=f["D"]*velocity
        flux=self.faces**2*np.r_[0,(flux_no_r2[1:]+flux_no_r2[:-1])/2,flux_no_r2[-1]]
        out[7]=-np.diff(flux)/self.volumes
        out[8]=np.interp(state[8],self.r,velocity)
        if np.min(np.diff(state[8])/self.dr)<.05:
            raise ValueError("approaching sampled dust shell crossing")
        return out,4*math.pi*flux[-1]

    def snapshot(self,t,state,flux_integral):
        f=self.fields(t,state);r=self.r;mask=(r>2*self.dr)&(r<r[-1]-2*self.dr)
        bg=self.model.background(t);A,R,h,k,N,w,Ud=(f[x] for x in ("A","R","h","k","N","w","Ud"))
        angular_rate=f["rate"][:,1]
        areal=Ud**2*(R*(angular_rate/N+h*h)-f["Nr"]*f["Rr"]/(N*A*A))
        areal-=2*Ud*w/A**2*((h-k)*f["Rr"]+R*f["hr"])
        areal+=w*w/A**4*(f["Rrr"]-A*A*k*h*R-f["Ar"]*f["Rr"]/A)
        inward=R*(bg["Hdot"]+bg["H"]**2)-areal
        baryon_integral=cumulative_trapezoid(f["rho"]*R*R*f["Rr"],r,initial=0)
        gN=np.divide(baryon_integral,2*R*R,out=np.zeros_like(r),where=R!=0)
        at=3*self.width;force=float(np.interp(at,r,inward));newton=float(np.interp(at,r,gN))
        a0=math.sqrt(.7/(32*math.pi));mass=4*math.pi*np.dot(self.volumes,state[7])
        return dict(t=t,max_hamiltonian_constraint=float(np.max(abs(f["constraints"][mask,0]))),
                    max_momentum_constraint=float(np.max(abs(f["constraints"][mask,1]))),
                    max_clock_constraint=float(np.max(abs(f["constraints"][mask,2]))),
                    max_lapse_fd_residual=float(np.max(abs(f["lapse_residual"][mask]))),
                    lapse_min=float(np.min(N)),clock_principal_min=float(np.min(f["schur"][1:])),
                    constitutive_margin=float(np.min(f["domain_denominator"])),
                    shell_jacobian_min=float(np.min(np.diff(state[8])/self.dr)),
                    dust_mass=mass,mass_balance_relative_error=(mass+flux_integral-self.initial_mass)/max(self.initial_mass,1e-30),
                    clock_gradient_max=float(np.max(abs(state[5]))),dust_gradient_max=float(np.max(abs(state[6]))),
                    sampled_coordinate_radius=at,areal_inward_acceleration=force,newton_bare=newton,
                    force_ratio=force/newton if newton else None,
                    mond_balance_ratio=-math.expm1(-force/a0)*force/newton if newton and force>=0 else None)


def evolve(amplitude,width,*,tend=.02,dt=.0005,points=129,outer=3.,gamma=1e-6,constraint_addition=1.,constrained=True):
    started=time.monotonic();system=Evolution(amplitude,width,points,outer,tend,gamma,constraint_addition,constrained)
    state=system.initial.copy();snapshots=[system.snapshot(0,state,0.)]
    steps=max(1,math.ceil(tend/dt));step=tend/steps;flux_integral=0.
    for i in range(steps):
        t=i*step
        k1,f1=system.rhs(t,state);k2,f2=system.rhs(t+step/2,state+step*k1/2)
        k3,f3=system.rhs(t+step/2,state+step*k2/2);k4,f4=system.rhs(t+step,state+step*k3)
        state+=step*(k1+2*k2+2*k3+k4)/6
        if constrained:state=project_state((i+1)*step,state,system.r,system.model)
        flux_integral+=step*(f1+2*f2+2*f3+f4)/6
        if not np.all(np.isfinite(state)):raise ValueError("nonfinite evolved state")
        if i==steps-1 or (i+1)%max(1,steps//4)==0:
            snapshots.append(system.snapshot((i+1)*step,state,flux_integral))
    return dict(state=state,r=system.r,model=system.model,snapshots=snapshots,
                configuration=dict(amplitude=amplitude,width=width,tend=tend,dt=step,points=points,
                                   outer=outer,gamma=gamma,constraint_addition=constraint_addition,
                                   constrained=constrained),seconds=time.monotonic()-started)


if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--tend",type=float,default=.02)
    parser.add_argument("--dt",type=float,default=.0005);parser.add_argument("--points",type=int,default=129)
    parser.add_argument("--amplitude",type=float,default=.02);parser.add_argument("--outer",type=float,default=3.)
    args=parser.parse_args();run=evolve(args.amplitude,.3,tend=args.tend,dt=args.dt,points=args.points,outer=args.outer)
    print(json.dumps({k:run[k] for k in ("configuration","snapshots","seconds")},indent=2))
