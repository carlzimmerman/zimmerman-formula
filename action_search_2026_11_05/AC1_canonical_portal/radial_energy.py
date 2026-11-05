"""Finite-element second variation of the frozen quasistatic radial model."""
import numpy as np
from scipy.linalg import eigh

def minimum(sol,beta,ell,epsilon,intervals,mutate=False,scalar_only=False):
    radius=20.;xx=np.linspace(0,radius,intervals+1);nd=intervals+1
    H=np.zeros((2*nd,2*nd));N=np.zeros_like(H)
    q=(1-beta)/beta;B=2*np.sqrt(3*(1-beta))/(3*beta);xi=.5/(1+beta)
    gl,gw=np.polynomial.legendre.leggauss(3);local_min=np.inf
    for e in range(intervals):
        left,right=xx[e:e+2];dx=right-left;r=(left+right)/2;nv=np.array([.5,.5]);der=np.array([-1.,1.])/dx
        Y=sol.sol(np.array([r]));u=float(Y[0,0]);d=float(Y[2,0]);y=1+epsilon*d/B
        A=(np.sinh(y)/np.sinh(1))**(-q);Ap=-q/B*A/np.tanh(y);App=A/B**2*(q*q/np.tanh(y)**2+q/np.sinh(y)**2)
        Vpp=A*A/B**2*(4*q*q/np.tanh(y)**2+2*q/np.sinh(y)**2)
        z=u/A;g=2*(-z-np.log1p(-z))-z*z/(1-z);gp=-z*z/(1-z)**2
        D=1/(1-z)**2-1;h=-z*z*Ap/(1-z)**2;M=4*np.pi/xi*Vpp+(g-z*gp)*Ap*Ap+A*g*App
        local_min=min(local_min,M-h*h/D)
        weight=dx*r*r;div=der+2*nv/r
        hp=weight*(D*np.outer(nv,nv)+ell*ell/2*np.outer(div,div))
        hs=weight*((-1 if mutate else 1)*np.outer(der,der)+epsilon*M*np.outer(nv,nv))
        cross=weight*np.sqrt(epsilon)*h*np.outer(nv,nv)
        idx=np.array([e,e+1]);jdx=idx+nd
        H[np.ix_(idx,idx)]+=hp;H[np.ix_(jdx,jdx)]+=hs
        H[np.ix_(idx,jdx)]+=cross;H[np.ix_(jdx,idx)]+=cross.T
        norm=np.zeros((2,2))
        for zeta,w in zip(gl,gw):
            rquad=(left+right)/2+dx*zeta/2;bases=np.array([(1-zeta)/2,(1+zeta)/2])
            norm+=dx/2*w*rquad*rquad*np.outer(bases,bases)
        N[np.ix_(idx,idx)]+=norm;N[np.ix_(jdx,jdx)]+=norm
    keep=list(range(1,nd-1))+list(range(nd,2*nd-1))
    if scalar_only:keep=list(range(nd,2*nd-1))
    Hv=H[np.ix_(keep,keep)];Nv=N[np.ix_(keep,keep)]
    lam=float(eigh(Hv,Nv,subset_by_index=[0,0],check_finite=True)[0][0])
    return {'minimum':lam,'dimension':len(keep),'local_schur_min':float(local_min)}

def evaluate(sol,beta,ell,epsilon,known=False):
    coarse=minimum(sol,beta,ell,epsilon,200);fine=minimum(sol,beta,ell,epsilon,400)
    out={'coarse':coarse,'fine':fine,'relative_difference':abs(coarse['minimum']-fine['minimum'])/max(abs(fine['minimum']),1e-10)}
    if known:
        scalar=minimum(sol,beta,ell,0,400,scalar_only=True)
        out['scalar_known_answer']=scalar['minimum'];out['scalar_relative_error']=abs(scalar['minimum']/(np.pi**2/400)-1)
        out['mutant']=minimum(sol,beta,ell,0,200,mutate=True)['minimum']
    return out
