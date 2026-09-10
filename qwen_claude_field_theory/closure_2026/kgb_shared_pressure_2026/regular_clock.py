#!/usr/bin/env python3
"""Regular inverse chart L=G_X/psi' crosses P_X=Z=0 without dividing by either.

The same action is integrated: P'=P_X X', G_X=pL, and L evolves according
to the curvature selected within the *derived* causal window. This is a
one-profile construction unless independently checked across different masses.
"""
import importlib.util
import json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp,quad

spec=importlib.util.spec_from_file_location('steering',Path(__file__).with_name('jet_steering.py'))
gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)


def local(eps,y,u,z,P,L,steer=False,fraction=.5):
    a=gate.source.geometry(eps,y,u,z,1.,pressure=P)
    r,g,gr,T,Tr,X,U,B,Z,invA=[a[k] for k in ('r','g','gr','T','Tr','X','U','B','Z','invA')]
    if min(X,U,B)<=0 or L==0 or T+Z==0:raise ValueError('outside regular chart')
    PX=2*X*L*Z/r;Xr=a['E0']/(2*X*L*(1+Z/T))
    if Xr==0:raise ValueError('X ceases to be a local coordinate')
    p=np.sqrt(B*U)
    BrB=Tr/T-(2*r*P+r*r*PX*Xr)/(1+r*r*P)
    Ur=-2*g*invA-2*Xr;Lp=(BrB+Ur/U)/2
    Zr=-(invA/X)*(2*g+Xr/X)-g-r*gr
    PXX0=2*L*Z/r+2*X*L/r*(Zr/Xr-Z/(r*Xr))
    GX=p*L;GXX0=p*Lp*L/Xr
    H=np.array([[-g*p/B,g*np.sqrt(invA/B),0,0],
       [g*np.sqrt(invA/B),p*(Lp-BrB/2)/B,0,0],[0,0,p/(B*r),0],[0,0,0,p/(B*r)]])
    v=[-np.sqrt(invA),p/np.sqrt(B),0,0]
    def evaluate(curvature):
        return gate.source.evaluator()(1,GX,GXX0+p*curvature,P,PX,PXX0+2*X*Z*curvature/r,
                                  *v,*[H[i,j] for i in range(4) for j in range(i,4)])
    C,stress=evaluate(0.);beta=U/(2*X)
    E=a['E0']-r*PX*Xr/T;rho=E-P
    I=C[0,0]-C[2,2]/beta
    window=gate.window(I,C[0,1],C[1,1],beta)
    curvature=0.
    if steer:
        if not window['exists']:raise ValueError(window['reason'])
        if E==0:raise ValueError('zero enthalpy chart')
        if not 0<fraction<1:raise ValueError('fraction must be strictly inside the window')
        chosen_K=window['lower']+fraction*(window['upper']-window['lower'])
        curvature=L*(chosen_K-C[0,0])/E
        C,stress=evaluate(curvature)
    pr_geo=(1/B-1)/r**2+2*g/(B*r)
    pt_geo=(gr+g*g-g*BrB/2+(g-BrB/2)/r)/B
    rho_geo=(1-1/B)/r**2+BrB/(B*r)
    err=max(abs(stress[0,0]-rho_geo),abs(stress[1,1]-pr_geo),
            abs(stress[2,2]-pt_geo),abs(stress[0,1]))/max(abs(rho),abs(P),abs(pt_geo),1e-200)
    disc=C[0,1]**2-C[0,0]*C[1,1]
    healthy=bool(C[0,0]>0 and disc>0 and C[2,2]<0)
    speed=None
    if healthy:
        t=np.linspace(-1,1,181)
        d=(C[0,1]*t)**2-C[0,0]*(C[1,1]*t*t+C[2,2]*(1-t*t))
        speed=float(np.max((np.abs(C[0,1]*t)+np.sqrt(d))/C[0,0]))
    return dict(y=float(y),u=float(u),z=float(z),P=float(P),PX=float(PX),
        PXX=float(PXX0+2*X*Z*curvature/r),L=float(L),L_X=float(curvature),
        X=float(X),Xr=float(Xr),GX=float(GX),GXX=float(GXX0+p*curvature),
        rho=float(rho),pr_over_rho=float(P/rho),kinetic=float(C[0,0]),
        angular=float(C[2,2]),cross=float(C[0,1]),radial=float(C[1,1]),beta=float(beta),
        invariant=float(I),radial_discriminant=float(disc),healthy=healthy,
        max_sampled_speed=speed,window=window,relative_stress_error=float(err),
        finite=bool(np.isfinite(C).all()))


def integrate(eps=1e-6,bscale=.75,rtol=2e-7,fraction=.5):
    hi,lo=20.,.02
    def du(y):
        a=gate.source.geometry(eps,y,0,.1,1.)
        return 2*a['g']*a['ry']/eps
    u0=quad(du,lo,hi,epsabs=1e-10)[0]
    a=gate.source.geometry(eps,hi,u0,.1,1.);W=a['r']*a['g']
    z0=bscale*W/(2*eps*(2+bscale*W))
    a=gate.source.geometry(eps,hi,u0,z0,1.,pressure=0.)
    L0=a['r']/(2*a['X']*a['Z']) # Initial P_X=1, not a global linear P.
    last={};evaluations=0
    def rhs(t,state):
        nonlocal last,evaluations
        y=np.exp(t);u,z,P,L=state
        row=local(eps,y,u,z,P,L,steer=True,fraction=fraction);last=row;evaluations+=1
        a=gate.source.geometry(eps,y,u,z,1.,pressure=P)
        dX=row['Xr']*a['ry']*y
        return [2*a['g']*a['ry']*y/eps,
            -(row['Xr']/a['invA']+2*a['g']*(.5-eps*z))*a['ry']*y/eps,
            row['PX']*dX,row['L_X']*dX]
    try:
        sol=solve_ivp(rhs,(np.log(hi),np.log(lo)),[u0,z0,0.,L0],method='Radau',
            rtol=rtol,atol=[1e-9,1e-10,1e-13,1e-10],max_step=.05,dense_output=True)
        ys=np.geomspace(hi,np.exp(sol.t[-1]),101)
        rows=[local(eps,y,*sol.sol(np.log(y)),steer=True,fraction=fraction) for y in ys]
        return dict(epsilon=eps,bscale=bscale,rtol=rtol,fraction=fraction,solver_success=bool(sol.success),
            reached_end=bool(sol.success and abs(sol.t[-1]-np.log(lo))<1e-8),
            endpoint_y=float(np.exp(sol.t[-1])),message=sol.message,evaluations=evaluations,
            min_PX=min(r['PX'] for r in rows),max_PX=max(r['PX'] for r in rows),
            all_sampled_healthy=all(r['healthy'] for r in rows),
            max_sampled_speed=max(r['max_sampled_speed'] or float('inf') for r in rows),
            max_pressure_ratio=max(abs(r['pr_over_rho']) for r in rows),
            min_density=min(r['rho'] for r in rows),rows=rows)
    except (ValueError,OverflowError,np.linalg.LinAlgError) as error:
        return dict(epsilon=eps,bscale=bscale,rtol=rtol,fraction=fraction,reached_end=False,
            message=str(error),evaluations=evaluations,last_successful_rhs_evaluation=last,
            scope='Last RHS evaluation need not be an accepted ODE endpoint; no nonexistence proof')


def main():
    cases=[(1e-6,.75,.5),(2e-6,.75,.5),(1e-6,1.25,.5)]+[(1e-6,.75,f) for f in (.01,.1,.9,.99)]
    for eps,b,fraction in cases:
        a=integrate(eps,b,fraction=fraction)
        rows=a.pop('rows',[])
        if rows:a.update(first=rows[0],last=rows[-1])
        print('REGULAR='+json.dumps(a),flush=True)
    return 0


if __name__=='__main__':raise SystemExit(main())
