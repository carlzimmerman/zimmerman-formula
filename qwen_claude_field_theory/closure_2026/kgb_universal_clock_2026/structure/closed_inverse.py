#!/usr/bin/env python3
"""Closed regular static inverse, analytic for real/complex-step inputs.

No projection onto a constraint surface, numerical rank, or health verdict is
inserted. Domain: finite nonzero F,w,p,Q,r,B and a regular target chart.
The coefficients wrapper additionally requires f!=0. W denotes dw/dr, not
the differently named quantity in the older unextended KGB inverse.
"""
import numpy as np


def geometry(eps,y,backend=np):
    mu=-backend.expm1(-y);lam=mu+y*backend.exp(-y)
    r=eps/backend.sqrt(y*mu);ry=-r*lam/(2*y*mu);yr=1/ry
    B=1/(1-2*r*y);Br=2*(y+r*yr)*B*B
    g=y*B;gr=yr*B+y*Br
    rho=4*y*y*backend.exp(-y)/(r*lam)
    pt=(gr+g*g-g*Br/(2*B)+(g-Br/(2*B))/r)/B
    return dict(eps=eps,y=y,r=r,ry=ry,g=g,gr=gr,B=B,Br=Br,rho=rho,pt=pt)


def normalized(eps,y,X,U,w,F,backend=np):
    """Return P, kappa=PX/f, gamma=GX/f and W=dw/dr, independent of f,j."""
    a=geometry(eps,y,backend=backend)
    r,g,B,b,rho=a['r'],a['g'],a['B'],a['Br']/(2*a['B']),a['rho']
    p=backend.sqrt(B*U);Q=2*X+U;aa=g+2/r
    P=(2*w*aa+1.5*w*w/F)/B
    L=2*F*rho+2*w*(g+b)/B+3*w*w/(F*B)
    S=2*F*aa*rho+4*w*(r*g-1)/(r*r*B)
    gamma=p*r*S/(2*Q*w)
    W=B*(L-X*r*S/Q)/2
    H=((2/r+w/F)*U-(2*g+w/F)*X)/p
    kappa=2*P/F+H*gamma
    return dict(**a,X=X,U=U,w=w,F=F,p=p,Q=Q,P=P,L=L,S=S,H=H,
                kappa=kappa,gamma=gamma,W=W,
                Rrad=aa+1.5*w/F,Dcoord=1+r*w/(2*F))


def coefficients(eps,y,X,U,w,F,f,j=0.,backend=np):
    """Reconstruct the physical action jets and radial clock derivatives."""
    a=normalized(eps,y,X,U,w,F,backend=backend);z=w/f
    return dict(**a,f=f,j=j,z=z,zr=a['W']/f-j*z*z/f,
                PX=f*a['kappa'],GX=f*a['gamma'],Dfield=2*(F-X*f))


def flow_X(eps,y,X,U,w,F,f,j,backend=np):
    """Actual X-flow; returns a dict without choosing the shared j control."""
    a=normalized(eps,y,X,U,w,F,backend=backend)
    return dict(F=f,f=j,y=f/(a['ry']*w),
                U=-2-2*f*a['g']*(2*X+U)/w,w=f*a['W']/w)
