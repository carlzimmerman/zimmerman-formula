"""Variational radial discretization of the explicitly specified matter action.

The background is relaxed on each grid, so its discrete phase identity is
tested at a stationary point of that same discrete action, not repaired by
altering the fluctuation potential. Dirichlet background at0,L, w=r field.
"""
from pathlib import Path
import json,math
import numpy as np
from scipy.interpolate import CubicHermiteSpline
from scipy.sparse import diags,bmat,eye,csr_matrix,csc_matrix
from scipy.sparse.linalg import spsolve

BASE=Path(__file__).resolve().parents[2]
P=json.loads((BASE/'sol61_push/cold_completion_2026_10_20/run_001/results.json').read_text())['parameters']

def initial(profile,r):
    z=np.load(profile);rr=z['r'];yy=z['y']
    fs=CubicHermiteSpline(rr,yy[0],yy[1]);bs=CubicHermiteSpline(rr,yy[2],yy[3]);hs=CubicHermiteSpline(rr,yy[4],yy[5])
    return np.array([r*fs(r),r*bs(r),r*hs(r)]),float(z['omega'])

def background(profile,Q,L,N):
    dr=L/(N+1);r=np.arange(1,N+1)*dr
    H=diags([-np.ones(N-1),2*np.ones(N),-np.ones(N-1)],[-1,0,1],format='csc')/(dr*dr)
    w,om=initial(profile,r);xx=np.r_[w.reshape(-1),om]
    g,a,M,MX2,lam=P['g'],P['a'],P['M_chi'],P['MX2'],P['lambda']
    zero=csr_matrix((N,N))
    def evaluate(x,jac=False):
        u,b,h=x[:-1].reshape(3,N);om=x[-1];f=u/r;bb=b/r;hh=h/r
        D=MX2-4*om*om
        Up=M*M*hh-3*M*hh**2/8+hh**3
        residual=np.r_[H@u+(1-om*om+2*lam*f*f+a*hh+2*g*bb)*u,
                       H@b+D*b+g*f*f*r,
                       H@h+Up*r+a*f*f*r,
                       (8*math.pi*om*dr*np.sum(u*u+4*b*b)-Q)/Q]
        if not jac:return residual
        Vu=1-om*om+6*lam*f*f+a*hh+2*g*bb
        B=M*M-.75*M*hh+3*hh*hh
        A=bmat([[H+diags(Vu),diags(2*g*f),diags(a*f)],
                [diags(2*g*f),H+D*eye(N),zero],
                [diags(2*a*f),zero,H+diags(B)]],format='csc')
        omega_col=csc_matrix(np.r_[-2*om*u,-8*om*b,np.zeros(N)][:,None])
        qrow=csc_matrix((8*math.pi*om*dr/Q)*np.r_[2*u,8*b,np.zeros(N)][None,:])
        qq=csc_matrix([[8*math.pi*dr*np.sum(u*u+4*b*b)/Q]])
        J=bmat([[A,omega_col],[qrow,qq]],format='csc')
        return residual,J
    history=[]
    for it in range(15):
        F,J=evaluate(xx,True);field_res=np.max(np.abs(F[:-1]))/max(1,np.max(np.abs(xx[:-1])))
        history.append({'iteration':it,'field_residual_scaled':float(field_res),'charge_residual_relative':float(F[-1])})
        if field_res<1e-9 and abs(F[-1])<1e-11:break
        dx=spsolve(J,-F);base=np.linalg.norm(F)
        step=1.
        for ls in range(15):
            trial=xx+step*dx
            if 0<trial[-1]<1 and np.linalg.norm(evaluate(trial))<base:
                xx=trial;break
            step*=.5
        else:raise RuntimeError('discrete stationary line search failed')
    else:raise RuntimeError('discrete stationary Newton limit')
    wf,wb,wh=xx[:-1].reshape(3,N);om=xx[-1]
    f,b,h=wf/r,wb/r,wh/r
    U=M*M*h*h/2-M*h**3/8+h**4/4
    V=f*f+MX2*b*b+2*g*b*f*f+lam*f**4+a*h*f*f+U
    grad=4*math.pi*dr*(wf@(H@wf)+wb@(H@wb)+.5*wh@(H@wh))
    rot=4*math.pi*dr*om*om*np.sum(wf*wf+4*wb*wb)
    pot=4*math.pi*dr*np.sum(r*r*V)
    q=8*math.pi*om*dr*np.sum(wf*wf+4*wb*wb)
    rec={'Q_target':Q,'Q':float(q),'L':L,'N':N,'dr':dr,'omega':float(om),'E':float(grad+rot+pot),
         'newton_history':history,'field_residual_scaled':history[-1]['field_residual_scaled'],
         'charge_residual_relative':history[-1]['charge_residual_relative']}
    return r,dr,H,(f,b,h),rec

def operators(profile,Q,L,N,ell):
    r,dr,H,(f,b,h),rec=background(profile,Q,L,N)
    H=H+diags(ell*(ell+1)/r**2)
    om=rec['omega'];a,g,M=P['a'],P['g'],P['M_chi'];D=P['MX2']-4*om*om
    Vu=1-om*om+6*P['lambda']*f*f+a*h+2*g*b
    Vv=1-om*om+2*P['lambda']*f*f+a*h-2*g*b
    B=M*M-.75*M*h+3*h*h
    z=csr_matrix((N,N));C=diags(2*g*f);A=diags(np.sqrt(2)*a*f)
    amp=bmat([[H+diags(Vu),C,A],[C,H+D*eye(N),z],[A,z,H+diags(B)]],format='csc')
    phase=bmat([[H+diags(Vv),C],[C,H+D*eye(N)]],format='csc')
    zz=csr_matrix((3*N,2*N))
    W=bmat([[amp,zz],[zz.T,phase]],format='csc')
    Crot=bmat([[2*om*eye(N),z],[z,4*om*eye(N)],[z,z]],format='csc')
    G=bmat([[csr_matrix((3*N,3*N)),-Crot],[Crot.T,csr_matrix((2*N,2*N))]],format='csc')
    p=np.r_[np.zeros(3*N),np.sqrt(2)*r*f,2*np.sqrt(2)*r*b]
    aa=-G@p
    rec['phase_zero_relative_residual']=float(np.linalg.norm(W@p)/np.linalg.norm(p)) if ell==0 else None
    return {'r':r,'dr':dr,'N':N,'ell':ell,'amp':amp,'phase':phase,'W':W,'G':G,'p':p,'a':aa,
            'fields':(f,b,h),'record':rec}
