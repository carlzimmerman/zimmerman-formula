"""Continuous exact-law 1h and independently controlled finite-band 2h.
All radii supplied to public functions are physical Mpc, h70=1.
"""
import json, math
from functools import lru_cache
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.special import ellipk, ellipe, ellipkinc, jv
from scipy.integrate import simpson, quad
from scipy.interpolate import CubicSpline, PchipInterpolator
from scipy.fft import dst
from scipy.linalg import solve_triangular
from scipy.optimize import nnls, minimize, least_squares
from scipy.stats import chi2

BASE=Path(__file__).resolve().parent
H=.6736; SUP=5.364; FB=1/(1+SUP)
GPC=4.30091e-3; A0=9.3603e-11*3.0857e16/1e6
J=json.loads((BASE/'inputs/cfg650_m1m2m3_RES_canonical_N1024_L100_ns1024_lean.json').read_text())
SNAP=J['snap']['x0.2562']; A=1/(1+SNAP['z'])
KS=np.array(SNAP['k']); PS=np.array(SNAP['P_grav'])
RHO=(.02237+.1200)/H**2*2.775e11
CONVERT=H/A**2/1e12
GL=lru_cache(None)(leggauss)

def data():
    d=[np.loadtxt(BASE/'inputs'/f'Fig-3_Lensing-rotation-curves_Massbin-{b}.txt') for b in range(1,5)]
    r=np.array([v[:,0] for v in d]); y=np.array([v[:,1]/v[:,4] for v in d])
    rows=np.loadtxt(BASE/'inputs/Fig-3_Lensing-rotation-curves_Massbins_covmatrix.txt')
    mins=sorted(set(rows[:,0])); c=np.zeros((60,60))
    for v in rows:
        b=mins.index(v[0]); d=mins.index(v[1]);i=np.argmin(abs(r[b]-v[2])); j=np.argmin(abs(r[d]-v[3]))
        c[b*15+i,d*15+j]=v[4]/v[6]
    return r,y,c

def fret(lm):
    lm=np.asarray(lm)
    return np.where(lm<12.5,.1,np.where(lm<13.5,.1+.45*(lm-12.5),np.minimum(.55+.30*(lm-13.5),.9)))

def retention(lmb,convention='native_h'):
    offset=math.log10(H) if convention=='native_h' else 0.
    # Monotone scalar fixed point solved by bracket; no slow unstable iteration.
    lo=.1;hi=.9
    for _ in range(48):
        f=(lo+hi)/2
        arg=lmb-math.log10(FB*f)+offset
        target=.1 if arg<12.5 else (.1+.45*(arg-12.5) if arg<13.5 else min(.55+.30*(arg-13.5),.9))
        if f>target:hi=f
        else:lo=f
    f=(lo+hi)/2
    return 1/f,lmb-math.log10(FB*f)

def edge(lmb,convention='native_h'):
    n,lmta=retention(lmb,convention);e=math.sqrt(((2*SUP*n+1)**2-1)/4)
    rm=math.sqrt(GPC*10**lmb/A0)
    return rm*e/1e6,n,lmta,e,rm

def profile(x,e=None,order=64):
    x=np.asarray(x);v=np.sqrt(1+4*x*x);m=1/v**2
    if e is None:
        return (v*ellipe(m)+1)/(2*np.pi*x*x)-ellipk(m)/(np.pi*v)
    out=(1+(math.sqrt(1+4*e*e)-1)/2)/(np.pi*x*x)
    inside=x<e
    if np.any(inside):
        xx=x[inside]; vv=v[inside]; mm=m[inside]
        phi=np.arccos(xx/e)
        sig=ellipkinc(phi,mm)/(np.pi*vv)
        nodes,weights=GL(order)
        umax=np.arccosh(e/xx);u=(nodes[None,:]+1)*umax[:,None]/2
        shell=2*xx[:,None]**2*np.sinh(u)**2/np.sqrt(1+4*xx[:,None]**2*np.cosh(u)**2)
        caps=np.sum(shell*weights,axis=1)*umax/2
        mcyl=(math.sqrt(1+4*e*e)-1)/2-caps
        out[inside]=(1+mcyl)/(np.pi*xx**2)-sig
    return out

def onehalo(lmb,r,finite,convention='native_h',order=64):
    ex,n,lmta,e,rm=edge(lmb,convention)
    return 10**lmb/rm**2*profile(np.asarray(r)*1e6/rm,e if finite else None,order)

def smooth_power(k):
    return np.interp(k,KS,PS,left=0,right=0)*np.exp(-(.05*k)**2)

def hankel(r,nk=65537):
    k=np.linspace(KS[0],KS[-1],nk);p=smooth_power(k)
    rc=np.asarray(r)*H/A
    return RHO/(2*np.pi)*simpson(k[None,:]*p[None,:]*jv(2,rc[:,None]*k[None,:]),x=k,axis=1)*CONVERT

class Environment:
    def __init__(self,power_points=65536,padding=32):
        # Uniform k samples with zero extension are transformed by DST-I.
        # Endpoint/bin discontinuity is tested against direct Hankel quadrature.
        dk=KS[-1]/power_points;size=power_points*padding-1
        q=np.zeros(size);k=dk*np.arange(1,power_points+1)
        q[:power_points]=k*smooth_power(k)
        transformed=dst(q,type=1,overwrite_x=True)
        r=np.arange(1,size+1)*np.pi/((size+1)*dk)
        # Only r<=500 is retained. Uniform fine spacing controls interpolation.
        take=r<=500;r=r[take];values=transformed[take]*dk/(4*np.pi**2*r)
        k0=np.linspace(KS[0],KS[-1],power_points+1)
        xi0=simpson(k0*k0*smooth_power(k0),x=k0)/(2*np.pi**2)
        self.r=np.r_[0.,r];self.xi=np.r_[xi0,values]
        self.spline=CubicSpline(self.r,self.xi)
        self.mass=CubicSpline(self.r,self.r**2*self.xi).antiderivative()
        self.dk=dk;self.dr=r[0]

    def los(self,r,ex=0.,order=512,rmax=300.):
        rc=np.asarray(r)*H/A;ec=np.broadcast_to(np.asarray(ex)*H/A,rc.shape)
        # Exact shell geometry combines Sigma_bar-Sigma before integration:
        # D/rho=4/R² int_0^R r²xi dr -2 int_0^inf xi(sqrt(R²+t²))
        #                       [R/(sqrt(R²+t²)+t)]² dt.
        inner=4/rc**2*np.maximum(0,self.mass(rc)-self.mass(np.minimum(ec,rc)))
        # Do not clip signed xi mass: exclusion can extend past sign changes.
        inner=np.where(ec<rc,4/rc**2*(self.mass(rc)-self.mass(ec)),0.)
        nodes,w=GL(order)
        low=np.where(ec>rc,np.arccosh(np.maximum(ec/rc,1)),0.)
        high=np.arccosh(rmax/rc)
        u=low[:,None]+(nodes+1)[None,:]*(high-low)[:,None]/2
        rr=rc[:,None]*np.cosh(u)
        vals=self.spline(rr)*np.exp(-2*u)*rr
        outer=np.sum(vals*w,axis=1)*(high-low)/2
        return (inner-2*outer)*RHO*CONVERT

    def table(self,r,nedge=1201,order=256):
        eg=np.linspace(0,1.2,nedge)
        rr=np.repeat(r,nedge);ee=np.tile(eg,len(r))
        vals=self.los(rr,ee,order=order).reshape(len(r),nedge)
        return eg,vals

def floor_relative(x,y):
    return float(np.max(abs(np.asarray(x)-y)/np.maximum(abs(np.asarray(y)),.01*np.max(abs(np.asarray(y))))))

def covariance_diagnostics(c):
    eig=np.linalg.eigvalsh(c);diag=np.sqrt(np.diag(c));corr=c/diag[:,None]/diag[None,:]
    cross=corr.copy()
    for b in range(4):cross[b*15:(b+1)*15,b*15:(b+1)*15]=0
    return dict(symmetry_max=float(abs(c-c.T).max()),min_eigenvalue=float(eig[0]),max_eigenvalue=float(eig[-1]),condition_number=float(eig[-1]/eig[0]),max_cross_bin_correlation=float(abs(cross).max()))

class Fitter:
    def __init__(self,eg,table,finite,convention='native_h',primary=False,excluded=True,zero_bias=False):
        self.r,self.y,self.c=data();self.eg=eg
        # PCHIP removes grid jumps, preserving each continuous mass-dependent edge.
        self.interp=[PchipInterpolator(eg,v,extrapolate=False) for v in table]
        self.finite=finite;self.convention=convention;self.excluded=excluded;self.zero_bias=zero_bias
        idx=np.flatnonzero(self.r[0]<=.31) if primary else np.arange(15)
        self.sel=np.concatenate([idx+15*b for b in range(4)])
        self.cs=self.c[np.ix_(self.sel,self.sel)];self.chol=np.linalg.cholesky(self.cs)
        self.ys=self.y.ravel()[self.sel]
        self.wy=solve_triangular(self.chol,self.ys,lower=True)

    def predict(self,lms):
        ones=[];twos=[];edges=[]
        for b,lm in enumerate(lms):
            ex,n,lmta,e,rm=edge(float(lm),self.convention)
            ones.append(onehalo(float(lm),self.r[b],self.finite,self.convention))
            twos.append(np.array([self.interp[i](ex if self.excluded else 0.) for i in range(15)]))
            edges.append(dict(logMb=float(lm),N=n,logMta_physical=lmta,edge_physical_Mpc=ex,edge_in_rM=e))
        ov=np.array(ones).ravel();tv=np.zeros((60,4))
        for b,t in enumerate(twos):tv[b*15:(b+1)*15,b]=t
        wo=solve_triangular(self.chol,ov[self.sel],lower=True)
        wt=solve_triangular(self.chol,tv[self.sel],lower=True)
        biases=np.zeros(4) if self.zero_bias else nnls(wt,self.wy-wo)[0]
        residual=self.wy-wo-wt@biases
        return residual,ov,tv,biases,edges

    def objective(self,lms):
        rr,*_=self.predict(lms)
        return float(rr@rr)

    def fit(self,starts=None):
        if starts is None:starts=[[10.14,10.46,10.70,10.89],[10.4,10.8,11.,11.2],[9.7,10.2,10.7,11.4],[11.2,11.2,11.2,11.2]]
        runs=[];best=None
        for st in starts:
            opt=minimize(self.objective,st,method='L-BFGS-B',bounds=[(9.5,12)]*4,options={'maxiter':140,'ftol':1e-11,'gtol':1e-6,'maxls':30})
            runs.append(dict(start=st,chi2=float(opt.fun),logMb=opt.x.tolist(),success=bool(opt.success),message=str(opt.message),nfev=int(opt.nfev)))
            if best is None or opt.fun<best.fun:best=opt
        # Independent bounded least-squares algorithm checks the profiled minimum.
        alt=least_squares(lambda v:self.predict(v)[0],best.x,bounds=(9.5,12.),ftol=1e-11,xtol=1e-11,gtol=1e-8,max_nfev=140)
        altchi=float(alt.fun@alt.fun)
        if altchi<best.fun:best.x=alt.x;best.fun=altchi
        res,ov,tv,biases,edges=self.predict(best.x)
        pred=ov+tv@biases;raw=self.y.ravel()-pred
        rs=raw[self.sel];precision=np.linalg.solve(self.cs,rs)
        signed=[];conditional=[];pulls=[]
        for b in range(4):
            take=np.flatnonzero((self.sel//15)==b);rest=np.setdiff1d(np.arange(len(self.sel)),take)
            signed.append(float(rs[take]@precision[take]))
            conditional.append(float(rs@precision-rs[rest]@np.linalg.solve(self.cs[np.ix_(rest,rest)],rs[rest])))
        # Individual conditional pulls use covariance precision, independent of ordering.
        inv=np.linalg.inv(self.cs);conditional_pulls=precision/np.sqrt(np.diag(inv))
        dof=len(self.sel)-(4 if self.zero_bias else 8)
        successful=sorted(v['chi2'] for v in runs if v['success'])
        return dict(chi2=float(rs@precision),nominal_dof=dof,nominal_p=float(chi2.sf(rs@precision,dof)),logMb=best.x.tolist(),biases=biases.tolist(),edges=edges,starts=runs,independent_least_squares=dict(chi2=altchi,success=bool(alt.success),nfev=int(alt.nfev)),optimizer_agreement=(len(successful)>=2 and successful[1]-successful[0]<.05 and abs(altchi-float(rs@precision))<.5),predictions=pred.reshape(4,15).tolist(),onehalo=ov.reshape(4,15).tolist(),environment_b1=tv.T.reshape(4,4,15).diagonal(axis1=0,axis2=1).T.tolist() if False else [tv[15*b:15*(b+1),b].tolist() for b in range(4)],residuals=raw.reshape(4,15).tolist(),selected_indices=self.sel.tolist(),whitened_residuals=res.tolist(),precision_residuals=precision.tolist(),conditional_pulls=conditional_pulls.tolist(),signed_additive_bin_chi2=signed,nonadditive_conditional_bin_chi2=conditional)
