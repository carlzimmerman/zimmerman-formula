#!/usr/bin/env python3
"""Pressure-enabled inverse of the SAME KGB action as ticking_kgb_inverse_2026.

P(X)=k*(X-1/2) is shared across masses; G(X) is reconstructed and compared.
This is a local mathematical search, not an empirical fit or full certificate.
"""
import argparse
from functools import lru_cache
import importlib.util
import json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp,quad
import sympy as s

SOURCE=Path(__file__).resolve().parent.parent/'ticking_kgb_inverse_2026/kgb_inverse.py'
spec=importlib.util.spec_from_file_location('kgb_source',SOURCE)
model=importlib.util.module_from_spec(spec);spec.loader.exec_module(model)


def symbolic_reduction():
    r,g,gp,P,PX,X,Xp,m,U,p=s.symbols('r g gp P PX X Xp m U p',nonzero=True)
    T=1+2*r*g;B=T/(1+r*r*P/m)
    Br=s.diff(B,r)+s.diff(B,g)*gp+s.diff(B,P)*PX*Xp
    rho=m*((1-1/B)/r**2+Br/(B**2*r))
    pressure=m*((1/B-1)/r**2+2*g/(B*r))
    E0=s.factor((rho+P).subs(Xp,0))
    Z=U/X-r*g
    dX=s.factor(Z*E0/(r*PX*(1+Z/T)))
    GX=PX*p*r/(2*X*Z)
    current=PX*p/B+2*GX*X*g/B-2*GX*p*p/(B*B*r)
    current=s.factor(current*B/p).subs(p*p,B*U)
    scalar_rho=2*X*GX*dX/p-P
    M=s.Symbol('M',positive=True)
    gs=M/(r*(r-2*M));Bs=1/(1-2*M/r)
    return dict(B=B,E0=E0,Xprime=dX,GX=GX,
                Einstein_residuals=[s.factor(pressure-P),s.factor(rho+P-E0+r*PX*Xp/T)],
                scalar_residuals=[s.factor(current),s.factor(scalar_rho-rho.subs(Xp,dX))],
                Schwarzschild_density=s.factor(m*((1-1/Bs)/r**2+s.diff(Bs,r)/(Bs**2*r))),
                exclusions='P_X=0, X=0, p=0, Z=0, T+Z=0 and metric singularities require separate branches')


def geometry(epsilon,y,u,z,k,pressure=None):
    eps=float(epsilon);mu=-np.expm1(-y);lam=mu+y*np.exp(-y)
    r=eps/np.sqrt(y*mu);ry=-r*lam/(2*y*mu)
    yr=1/ry;c=r*y;cr=y+r*yr
    T=1/(1-2*c);Tr=2*cr*T*T
    g=y*T;gr=yr*T+y*Tr
    invA=np.exp(-eps*u);X=(.5-eps*z)*invA;U=2*eps*z*invA
    P=k*(.5*np.expm1(-eps*u)-eps*z*invA) if pressure is None else pressure
    PX=k;B=T/(1+r*r*P)
    Z=U/X-r*g
    rho0=4*y*y*np.exp(-y)/(r*lam)
    E0=rho0+P*(1-3/T+r*Tr/(T*T))
    Xr=Z*E0/(r*PX*(1+Z/T))
    return dict(eps=eps,y=y,r=r,ry=ry,g=g,gr=gr,T=T,Tr=Tr,X=X,U=U,
                P=P,PX=PX,B=B,Z=Z,E0=E0,Xr=Xr,invA=invA)


@lru_cache(None)
def evaluator():
    a=model.principal_template()
    args=[a['m'],a['G1'],a['G2'],a['P'],a['P1'],a['P2']]+list(a['v'])+[a['H'][i,j] for i in range(4) for j in range(i,4)]
    return s.lambdify(args,(a['M'],a['T']),'numpy',cse=True)


def local(epsilon,y,u,z,k,pressure=None,pxx=0):
    """Optional P,P_XX are local jets, NOT the global linear action used in scan."""
    a=geometry(epsilon,y,u,z,k,pressure)
    r,g,gr,T,Tr,X,U,P,PX,B,Z,Xr,invA=[a[x] for x in
        ('r','g','gr','T','Tr','X','U','P','PX','B','Z','Xr','invA')]
    if min(X,U,B)<=0 or Z==0 or Xr==0:raise ValueError('outside regular ticking inverse branch')
    p=np.sqrt(B*U)
    BrB=Tr/T-(2*r*P+r*r*PX*Xr)/(1+r*r*P)
    Ur=-2*g*invA-2*Xr
    Lp=(BrB+Ur/U)/2
    Zr=-(invA/X)*(2*g+Xr/X)-g-r*gr
    GX=PX*p*r/(2*X*Z)
    GXX=GX*((Lp+1/r-Xr/X-Zr/Z)/Xr+pxx/PX)
    H=np.array([[-g*p/B,g*np.sqrt(invA/B),0,0],
                [g*np.sqrt(invA/B),p*(Lp-BrB/2)/B,0,0],
                [0,0,p/(B*r),0],[0,0,0,p/(B*r)]])
    v=np.array([-np.sqrt(invA),p/np.sqrt(B),0,0])
    C,stress=evaluator()(1,GX,GXX,P,PX,pxx,*v,*[H[i,j] for i in range(4) for j in range(i,4)])
    rho=(1-1/B)/r**2+BrB/(B*r)
    pt=P+r*(PX*Xr+g*(rho+P))/2
    scale=max(abs(rho),abs(P),abs(pt),1e-200)
    error=max(abs(stress[0,0]-rho),abs(stress[1,1]-P),abs(stress[2,2]-pt),abs(stress[0,1]))/scale
    Jr=PX*p/B+2*GX*X*g/B-2*GX*p*p/(B*B*r)
    jscale=abs(PX*p/B)+abs(2*GX*X*g/B)+abs(2*GX*p*p/(B*B*r))
    disc=C[0,1]**2-C[0,0]*C[1,1]
    healthy=bool(C[0,0]>0 and disc>0 and C[2,2]<0)
    speed=None
    if healthy:
        cosines=np.linspace(-1,1,181)
        rad=(C[0,1]*cosines)**2-C[0,0]*(C[1,1]*cosines**2+C[2,2]*(1-cosines**2))
        speed=float(np.max((np.abs(C[0,1]*cosines)+np.sqrt(rad))/C[0,0]))
    beta=U/(2*X)
    return dict(y=float(y),X=float(X),GX=float(GX),GXX=float(GXX),P=float(P),
                rho=float(rho),enthalpy_stable=float(a['E0']-r*PX*Xr/T),
                pr_over_rho=float(P/rho),z=float(z),u=float(u),
                relative_stress_error=float(error),relative_current_error=float(abs(Jr)/max(jscale,1e-200)),
                kinetic=float(C[0,0]),radial_discriminant=float(disc),angular=float(C[2,2]),
                cross=float(C[0,1]),radial=float(C[1,1]),beta=float(beta),
                health_invariant=float(C[0,0]-C[2,2]/beta),
                healthy=healthy,max_sampled_speed=speed)


def integrate(epsilon,k,bscale,direction='outward',rtol=2e-9):
    eps=float(epsilon);low=.02;high=20.
    def ur(y):
        a=geometry(eps,y,0,.1,k)
        return 2*a['g']*a['ry']/eps
    y0,y1=(high,low) if direction=='outward' else (low,high)
    u0=quad(ur,low,y0,epsabs=1e-10,epsrel=1e-11)[0]
    a=geometry(eps,y0,u0,.1,k);W=a['r']*a['g']
    z0=bscale*W/(2*eps*(2+bscale*W))
    def rhs(y,state):
        u,z=state;a=geometry(eps,y,u,z,k)
        return [2*a['g']*a['ry']/eps,
                -(a['Xr']/a['invA']+2*a['g']*(.5-eps*z))*a['ry']/eps]
    def boundary(y,state):
        a=geometry(eps,y,*state,k)
        return min(state[1],.5/eps-state[1],1+a['r']**2*a['P'])
    boundary.terminal=True;boundary.direction=-1
    ys=np.geomspace(y0,y1,101)
    sol=solve_ivp(rhs,(y0,y1),[u0,z0],method='Radau',rtol=rtol,atol=rtol/50,
                  t_eval=ys,events=boundary,max_step=1,dense_output=True)
    rows=[]
    for y,(u,z) in zip(sol.t,sol.y.T):
        try:rows.append(local(eps,y,u,z,k))
        except ValueError:break
    return dict(epsilon=eps,k=k,bscale=bscale,direction=direction,rtol=rtol,
                solver_success=bool(sol.success),reached_end=bool(abs(sol.t[-1]-y1)<1e-8),
                message=sol.message,endpoint=float(sol.t[-1]),rows=rows,nfev=sol.nfev)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--scan',action='store_true')
    args=parser.parse_args()
    print(json.dumps({k:str(v) for k,v in symbolic_reduction().items()},indent=2))
    if args.scan:
        for k in (1e4,1e6,1e8):
            for b in (.25,.75,1.25):
                for eps in (1e-6,2e-6):
                    a=integrate(eps,k,b);rows=a.pop('rows')
                    a.update(samples=len(rows),healthy_samples=sum(x['healthy'] for x in rows),
                        max_stress_error=max((x['relative_stress_error'] for x in rows),default=None),
                        max_pressure_ratio=max((abs(x['pr_over_rho']) for x in rows),default=None),
                        first=rows[0] if rows else None,last=rows[-1] if rows else None)
                    print('SCAN='+json.dumps(a),flush=True)
    return 0


if __name__=='__main__':raise SystemExit(main())
