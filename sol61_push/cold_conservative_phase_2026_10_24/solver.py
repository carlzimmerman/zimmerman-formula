"""Weighted finite-volume phase-fitted CCT pilot. No tags in gravity."""
import numpy as np
from scipy.linalg import eigh_tridiagonal

def transport(m,q,F):
    """Exact chain fluxes, donor fraction including same-step through-flow."""
    Q=np.zeros_like(F)
    for i in range(len(F)):
        incoming=np.maximum(F[i-1],0) if i else 0
        tagged=np.maximum(Q[i-1],0) if i else 0
        den=m[i]+incoming
        frac=np.divide(q[i]+tagged,den,out=np.zeros_like(den),where=den>0)
        Q[i]=np.where(F[i]>0,F[i]*frac,0)
    for i in range(len(F)-1,-1,-1):
        incoming=np.maximum(-F[i+1],0) if i+1<len(F) else 0
        tagged=np.maximum(-Q[i+1],0) if i+1<len(F) else 0
        den=m[i+1]+incoming
        frac=np.divide(q[i+1]+tagged,den,out=np.zeros_like(den),where=den>0)
        Q[i]=np.where(F[i]<0,F[i]*frac,Q[i])
    ans=q.copy(); ans[:-1]-=Q; ans[1:]+=Q
    return ans

class Grid:
    def __init__(self,n=48,box=28,stretch=3.5):
        self.n=n; self.box=box
        z=np.linspace(-1,1,n+2)[1:-1]
        self.x=box*np.sinh(stretch*z)/np.sinh(stretch)
        hl=np.diff(np.r_[-box,self.x]); hr=np.diff(np.r_[self.x,box])
        self.w=(hl+hr)/2
        self.d=(1/hl+1/hr)/self.w
        self.o=-1/(hr[:-1]*np.sqrt(self.w[:-1]*self.w[1:]))
        self.lam,self.Q=eigh_tridiagonal(self.d,self.o)
        self.vol=self.w[:,None,None]*self.w[None,:,None]*self.w[None,None,:]
        self.sv=np.sqrt(self.vol)
        self.xyz=np.meshgrid(self.x,self.x,self.x,indexing='ij')
        self.r=np.sqrt(sum(a*a for a in self.xyz))
    def poisson(self,m):
        a=-4*np.pi*m/self.sv
        for axis in range(3):
            a=np.moveaxis(a,axis,0); a=np.tensordot(self.Q.T,a,axes=(1,0)); a=np.moveaxis(a,0,axis)
        a/=self.lam[:,None,None]+self.lam[None,:,None]+self.lam[None,None,:]
        for axis in range(3):
            a=np.moveaxis(a,axis,0); a=np.tensordot(self.Q,a,axes=(1,0)); a=np.moveaxis(a,0,axis)
        return a/self.sv

class Axis:
    def __init__(self,g,eta,p,axis,tau):
        self.axis=axis; self.eta=eta; self.tau=tau
        p=np.moveaxis(p,axis,0)
        s=(g.n-1,)+(1,)*(p.ndim-1)
        self.h=g.o.reshape(s)*eta**2/2-1j*eta*(p[:-1]+p[1:])/4/np.sqrt(g.w[:-1]*g.w[1:]).reshape(s)
        self.diag=(eta**2*g.d/2).reshape((g.n,)+(1,)*(p.ndim-1))
        c=1j*tau/(2*eta)
        self.upper=c*self.h; self.lower=c*self.h.conj()
        self.lu=np.broadcast_to(1+c*self.diag,p.shape).copy()
        self.mul=np.empty_like(self.h)
        for i in range(g.n-1):
            self.mul[i]=self.lower[i]/self.lu[i]
            self.lu[i+1]-=self.mul[i]*self.upper[i]
    def apply(self,u,q):
        old=np.moveaxis(u,self.axis,0)
        c=1j*self.tau/(2*self.eta)
        b=(1-c*self.diag)*old
        b[:-1]-=self.upper*old[1:]; b[1:]-=self.lower*old[:-1]
        for i in range(len(b)-1): b[i+1]-=self.mul[i]*b[i]
        b[-1]/=self.lu[-1]
        for i in range(len(b)-2,-1,-1): b[i]=(b[i]-self.upper[i]*b[i+1])/self.lu[i]
        mid=(old+b)/2
        F=-2*self.tau/self.eta*np.imag(mid[:-1].conj()*self.h*mid[1:])
        delta=np.abs(b)**2-np.abs(old)**2
        delta[:-1]+=F; delta[1:]-=F
        err=float(np.max(np.abs(delta)))
        qq=transport(np.abs(old)**2,np.moveaxis(q,self.axis,0),F)
        return np.moveaxis(b,0,self.axis),np.moveaxis(qq,0,self.axis),err
    def expectation(self,u):
        a=np.moveaxis(u,self.axis,0)
        return float(np.sum(self.diag*np.abs(a)**2)+2*np.real(np.sum(a[:-1].conj()*self.h*a[1:])))

class Evolve:
    def __init__(self,g,eta,p,dt):
        self.g=g; self.eta=eta; self.dt=dt; self.p2=sum(a*a for a in p)/2
        self.ops=[Axis(g,eta,p[a],a,dt*(1 if a==2 else .5)) for a in range(3)]
    def energy(self,u,phi):
        return sum(op.expectation(u) for op in self.ops)+float(np.sum(np.abs(u)**2*(self.p2+phi/2)))
    def step(self,u,q,phi):
        u=u*np.exp(-1j*self.dt/(2*self.eta)*(phi+self.p2)); err=0.
        for a in (0,1,2,1,0):
            u,q,e=self.ops[a].apply(u,q); err=max(err,e)
        phi=self.g.poisson(np.abs(u)**2)
        u*=np.exp(-1j*self.dt/(2*self.eta)*(phi+self.p2))
        return u,q,phi,err
