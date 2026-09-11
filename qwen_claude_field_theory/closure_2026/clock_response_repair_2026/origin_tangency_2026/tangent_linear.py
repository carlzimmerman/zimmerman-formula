#!/usr/bin/env python3
"""Differentiate the radial constraint ODE, not two independent projections.

Complex-step differentiation applies only to smooth algebraic coefficients.
The shape-preserving density interpolation and center startup are differentiated
by explicit centered differences with a separately varied step. No PDE or
global-error certificate is inferred from this bounded diagnostic.
"""
import json
import argparse
from pathlib import Path
import sys
import time
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import PchipInterpolator

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'nonlinear_evolution_2026'))
from evolve import Evolution
from equations import compiled_constraints
from project import project_state,regular_center,radial_profiles


def tangent(system,state,t,difference_step,startup_divisor=16):
    r=system.r;model=system.model;rate,_=system.rhs(t,state)
    profiles=radial_profiles(r,*state[[1,4,5,6,7]])
    velocities=radial_profiles(r,*rate[[1,4,5,6,7]])
    eps=difference_step
    density_plus=PchipInterpolator(r*r,state[7]+eps*rate[7])
    density_minus=PchipInterpolator(r*r,state[7]-eps*rate[7])
    c=regular_center(t,state,r,model)
    cp=regular_center(t+eps,state+eps*rate,r,model)
    cm=regular_center(t-eps,state-eps*rate,r,model)
    cd={key:(cp[key]-cm[key])/(2*eps) for key in c}
    ac,hc=c['a_c'],c['K_c'];acd,hcd=cd['a_c'],cd['K_c']
    raw=model.background(t)['raw']
    # Constraints need constitutive jets through first explicit time derivative.
    # Their directional rates therefore use at most the supplied second jets.
    rawdot=np.r_[raw[5:15],np.zeros(5)]
    names,func=compiled_constraints()
    forbidden={'P_tt','W_YYt','W_YYY','V_tt','P_XX','P_Xt'}
    if forbidden.intersection(names):raise ValueError('extend background derivatives')
    tiny=1e-25

    def dual_profile(index,x,order=0):
        if index==4:
            return profiles[4](x)+1j*tiny*(density_plus(x*x)-density_minus(x*x))/(2*eps)
        return profiles[index](x,order)+1j*tiny*velocities[index](x,order)

    def algebra(x,y):
        A=ac+y[0]+1j*tiny*(acd+y[2])
        h=hc+y[1]+1j*tiny*(hcd+y[3])
        b=dual_profile(0,x);bp=dual_profile(0,x,1);bpp=dual_profile(0,x,2)
        q=dual_profile(1,x);u=dual_profile(2,x);w=dual_profile(3,x);D=dual_profile(4,x)
        Y=u*u/A**2;X=q*q-Y
        jets=dict(zip(model.names,model.jetfunc(*(raw+1j*tiny*rawdot),X,Y,model.gamma)))
        jets.update(M2=1.,Lambda=.7,gamma=model.gamma,A=A,R=x*b,
                    Rr=b+x*bp,Rrr=2*bp+x*bpp,h=h,Q=q,Qr=dual_profile(1,x,1),
                    cr=u,crr=dual_profile(2,x,1),w=w,
                    rho=D/(A*b*b*np.sqrt(1+w*w/A**2)))
        out=np.asarray(func(*(jets[name] for name in names)),dtype=complex)
        solved=np.linalg.solve(out[:9].reshape(3,3),out[9:])
        return solved.real,solved.imag/tiny

    start=r[1]/startup_divisor
    initial=[c['A2']*start**2/2,0.,cd['A2']*start**2/2,0.]
    def rhs(x,y):
        value,derivative=algebra(x,y)
        return np.r_[value[:2],derivative[:2]]
    solution=solve_ivp(rhs,(start,r[-1]),initial,method='DOP853',
                       rtol=2e-11,atol=2e-13,dense_output=True)
    if not solution.success:raise RuntimeError(solution.message)
    ys=solution.sol(r[1:]);derived=np.zeros((3,len(r)))
    projected=np.zeros((3,len(r)))
    derived[:,0]=[acd,hcd,hcd];projected[:,0]=[ac,hc,hc]
    for i,x in enumerate(r[1:],1):
        value,derivative=algebra(x,ys[:,i-1])
        projected[:,i]=[ac+ys[0,i-1],hc+ys[1,i-1],value[2]]
        derived[:,i]=[acd+ys[2,i-1],hcd+ys[3,i-1],derivative[2]]
    error=derived-rate[[0,3,2]]
    masks={str(cut):(r>=cut)&(r<2.8) for cut in (0.,.1,.3)}
    differences={}
    for cut,mask in masks.items():
        indices=np.flatnonzero(mask)
        differences[cut]={key:dict(error=float(max(abs(error[j,mask]))),
            radius=float(r[indices[np.argmax(abs(error[j,mask]))]])) for j,key in enumerate(('A','h','k'))}
    return dict(points=len(r),difference_step=eps,startup_divisor=startup_divisor,
                complex_step=tiny,nfev=solution.nfev,
                differences=differences,
                base_projection_difference=np.max(abs(projected-state[[0,3,2]]),axis=1).tolist())


def run():
    with np.load(HERE.parent/'convergence_repair_2026/run_002/states.npz') as saved:
        for index in (1,2):
            r=saved['r_'+str(index)];raw=saved['state_'+str(index)]
            system=Evolution(.02,.3,len(r),3.,.022,1e-6)
            state=project_state(.02,raw,r,system.model)
            for step in (1e-4,1e-5):
                started=time.monotonic();row=tangent(system,state,.02,step)
                row['seconds']=time.monotonic()-started
                print(json.dumps(row),flush=True)
            if index==2:
                for divisor in (32,64):
                    row=tangent(system,state,.02,1e-5,divisor)
                    row['scope']='Startup sensitivity on the same fixed input; not a re-evolved solution'
                    print(json.dumps(row),flush=True)


def manufactured():
    """Distinguish an operator defect from roughness of previously evolved data."""
    for n in (65,129,257,513):
        system=Evolution(.02,.3,n,3.,.022,1e-6);r=system.r
        state=system.initial.copy();bg=system.model.background(.02)
        gaussian=np.exp(-(r/.3)**2)
        state[1]=bg['a'];state[4]=bg['q']+1e-6*gaussian
        state[5]=1e-5*r*gaussian;state[7]=bg['a']**3*.02*gaussian
        state=project_state(.02,state,r,system.model)
        row=tangent(system,state,.02,1e-5)
        row['scope']='Common smooth analytic free data, separately constraint-projected; not time evolved'
        print(json.dumps(row),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--manufactured',action='store_true')
    args=parser.parse_args()
    manufactured() if args.manufactured else run()
