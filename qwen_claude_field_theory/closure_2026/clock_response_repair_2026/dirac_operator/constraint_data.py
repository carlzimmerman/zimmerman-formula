#!/usr/bin/env python3
"""Solve C=T=H_x=0 before testing the lapse operator in a periodic plane sector.

Even cosine data on a 2pi cell, zero mean conformal log and shear; the chi
zero-mode momentum is solved, not silently fixed to its FLRW value.
This is a spectral nonlinear constraint solve, not a 3D/global closure proof.
"""
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.optimize import root
from scipy.special import expit
import sympy as s


def model():
    X,Y,u,d,q,m=s.symbols('X Y U d q m',real=True)
    P=-u*s.log((u-2*d*X)/(u-2*d*q*q))/2
    W=u+q*q*m*d*(s.sqrt(1+2*Y/(q*q*m))-1)
    qb=s.Rational(10,11);A=s.Rational(1,10);mb=s.Rational(1,10);H=2/s.sqrt(15)
    mn=s.Rational(109,1120);qn=-qb*mn/(1+mb);un=mn*qb*A+mb*qn*A-3*mb*qb*A
    aa=s.symbols('A');de=aa*u/(2*q*(q*aa+u));ub=mb*qb*A
    dn=(s.diff(de,aa)*(-3*aa)+s.diff(de,q)*qn+s.diff(de,u)*un).subs({aa:A,u:ub,q:qb})
    Pt=H*(s.diff(P,u)*un+s.diff(P,d)*dn+s.diff(P,q)*qn)
    sub={u:ub,d:s.Rational(1,200),q:qb,m:mb}
    fun=s.lambdify((X,Y),[f.subs(sub) for f in (P,s.diff(P,X),s.diff(P,X,2),Pt,s.diff(Pt,X),W,s.diff(W,Y),s.diff(W,Y,2))],'numpy',cse=True)
    return fun,dict(q=float(qb),U=float(ub),Vt=float(H*un),H=float(H),R0=float(ub/(2*s.Rational(1,200))),Lambda=.7)


def solve_case(amplitude,nmode,previous=None):
    fun,par=model();n=8*nmode;x=np.arange(n)*2*np.pi/n
    modes=np.arange(1,nmode+1)[:,None];cos=np.cos(modes*x);sin=np.sin(modes*x)
    wave=np.fft.fftfreq(n,1/n)
    def diff(v,order=1):return np.fft.ifft((1j*wave)**order*np.fft.fft(v)).real
    chi=amplitude*par['q']*np.cos(x);chix=diff(chi);chixx=diff(chi,2)
    def fields(v):
        conf=v[:nmode]@cos;shear=v[nmode:2*nmode]@cos
        Q=np.sqrt(par['R0']*expit(v[-1]));hxx=np.exp(-2*conf);grad=diff(conf)
        Y=hxx*chix**2;X=Q*Q-Y
        P,PX,PXX,Pt,PtX,W,WY,WYY=[np.broadcast_to(t,(n,)) for t in fun(X,Y)]
        Yx=diff(Y);J=hxx*(WY*chixx+(grad*WY+WYY*Yx)*chix)
        K=(Pt-par['Vt']+(4/3)*WY*Y*shear+2*Q*J)/(W-(2/3)*WY*Y)
        rho=2*Q*Q*PX-P+par['U']
        R=hxx*(-4*diff(conf,2)-2*grad*grad)
        C=R+(2/3)*(K*K-shear*shear)-2*rho-2*par['Lambda']
        momentum=(2/3)*(diff(shear)-diff(K))+2*grad*shear-2*Q*PX*chix
        T=par['Vt']-Pt+W*K-2*WY*Y*(K+2*shear)/3-2*Q*J
        return locals()
    def residual(v):
        f=fields(v)
        return np.r_[np.mean(f['C']),2*(cos@f['C'])/n,2*(sin@f['momentum'])/n]
    initial=np.zeros(2*nmode+1);initial[-1]=np.log(10.)
    if previous is not None:
        old=(len(previous)-1)//2
        initial[:min(old,nmode)]=previous[:min(old,nmode)]
        initial[nmode:nmode+min(old,nmode)]=previous[old:old+min(old,nmode)]
        initial[-1]=previous[-1]
    run=root(residual,initial,method='hybr',options={'xtol':1e-10})
    f=fields(run.x);projected=float(np.max(np.abs(residual(run.x))))
    if not np.all(np.isfinite(run.x)) or projected>1e-8:
        return dict(amplitude=amplitude,modes=nmode,solver_success=bool(run.success),projected_residual=projected,
                    status='constraint solve not certified',message=str(run.message)),run.x
    # Geometric form of the independently checked functional mass coefficient.
    conf,shear,K,Q,Y,X=[f[k] for k in ('conf','shear','K','Q','Y','X')]
    P,PX,PXX,Pt,PtX,W,WY,WYY=[f[k] for k in ('P','PX','PXX','Pt','PtX','W','WY','WYY')]
    hxx=f['hxx'];gx=f['grad'];R=f['R'];J=f['J'];rho=f['rho']
    kx=(K+2*shear)/3;ky=(K-shear)/3;Z=kx*Y;B=2*PX+4*Q*Q*PXX
    dy=-2*Z # Q is spatially constant in this family
    dq=(2*np.exp(-3*conf)*diff(np.exp(conf)*PX*chix)-2*Q*PX*K+2*Q*PXX*dy)/B
    dx=2*Q*dq-dy
    ham=R+K*K-(kx*kx+2*ky*ky)-2*rho-2*par['Lambda']
    dk=-R-K*K+PX*(3*Q*Q-Y)-3*P+3*par['U']+3*par['Lambda']+3*ham/4
    ric_xx=-2*diff(conf,2) # conformally flat 3-metric depending on x only
    dz=-ric_xx*hxx*Y-K*Z-2*kx*kx*Y+Y*(PX*(Q*Q+Y)-P+par['U'])+par['Lambda']*Y+Y*ham/4
    dj=np.exp(-3*conf)*diff(np.exp(conf)*(WYY*dy*chix-2*WY*kx*chix))+WY*hxx*chix*diff(K)
    t=f['T'];mass_raw=K*t-PtX*dx+WY*dy*K+W*dk-2*WYY*dy*Z-2*WY*dz-2*dq*J-2*Q*dj
    principal=W-2*Q*Q*WY-2*Y*WY-4*Q*Q*Y*WYY
    a2=np.exp(conf)*principal;a0=np.exp(3*conf)*mass_raw;dxgrid=2*np.pi/n
    edge=np.fft.ifft(np.fft.fft(a2)*np.exp(1j*wave*dxgrid/2)).real
    mat=np.diag(-a0+(edge+np.roll(edge,1))/dxgrid**2)
    for j in range(n):mat[j,(j+1)%n]-=edge[j]/dxgrid**2;mat[(j+1)%n,j]-=edge[j]/dxgrid**2
    eigen=np.linalg.eigvalsh(mat)
    return dict(amplitude=amplitude,modes=nmode,mesh=n,solver_success=bool(run.success),
        projected_residual=projected,full_C_residual=float(np.max(np.abs(f['C']))),
        full_T_residual=float(np.max(np.abs(t))),full_momentum_residual=float(np.max(np.abs(f['momentum']))),
        Q_zero_mode=float(Q),mean_charge_density=float(np.mean(np.exp(3*conf)*2*Q*PX)),
        min_principal=float(principal.min()),min_mass=float((-mass_raw).min()),
        min_X=float(X.min()),min_log_domain=float((par['R0']-X).min()),min_kinetic=float(B.min()),
        lowest_eigenvalues=eigen[:3].tolist(),max_metric_log=float(np.max(np.abs(conf))),
        status='spectral constraint solution; continuum and 3D certification still open'),run.x


def main():
    rows=[]
    for amplitude in (0.,.001,.01,.05):
        previous=None
        for modes in (8,16):
            row,previous=solve_case(amplitude,modes,previous);rows.append(row)
    return dict(cases=rows,full_theory_status='OPEN',
        scope='Nonlinear plane-symmetric periodic constraint data; no unrestricted 3D or time-evolution theorem')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--result-file',type=Path);a=p.parse_args()
    r=main()
    if a.result_file:a.result_file.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,indent=2))
