"""Exact continuum lens coordinates, conservative phase-fitted FV discretization."""
import pathlib,sys,numpy as np
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent.parent/'cold_conservative_phase_2026_10_24'))
from solver import Grid,Axis

class VariableAxis(Axis):
    def set_tau(self,tau):
        self.tau=tau;c=1j*tau/(2*self.eta)
        self.upper[:]=c*self.h;self.lower[:]=c*self.h.conj()
        self.lu[:]=1+c*self.diag
        for i in range(len(self.lu)-1):
            self.mul[i]=self.lower[i]/self.lu[i]
            self.lu[i+1]-=self.mul[i]*self.upper[i]

class Lens:
    def __init__(self,g,eta,p,beta=.1,acceleration=0.,gravity=True,omit_compensation=False):
        self.g=g;self.eta=eta;self.p=p;self.beta=beta;self.acceleration=acceleration
        self.gravity=gravity;self.omit=omit_compensation;self.p2=sum(v*v for v in p)/2
        self.ops=[VariableAxis(g,eta,p[k],k,.01) for k in range(3)]
    def scale(self,t):return 1-self.beta*t+self.acceleration*t*t/2,-self.beta+self.acceleration*t,self.acceleration
    def potential(self,u):return self.g.poisson(abs(u)**2) if self.gravity else np.zeros_like(self.g.r)
    def step(self,u,q,phi,t,dt):
        a,ad,add=self.scale(t+dt/2)
        potential=phi/a+(0 if self.omit else .5*a*add*self.g.r**2)+self.p2/a**2
        u=u*np.exp(-1j*dt/(2*self.eta)*potential);err=0.
        for k in (0,1,2,1,0):
            op=self.ops[k];op.set_tau(dt/a**2*(1 if k==2 else .5));u,q,e=op.apply(u,q);err=max(err,e)
        phi=self.potential(u)
        potential=phi/a+(0 if self.omit else .5*a*add*self.g.r**2)+self.p2/a**2
        u*=np.exp(-1j*dt/(2*self.eta)*potential)
        return u,q,phi,err
    def moments(self,u,phi,t):
        g=self.g;a,ad,add=self.scale(t);m=abs(u)**2
        current=[]
        for k in range(3):
            v=np.moveaxis(u,k,0);den=(2*np.sqrt(g.w[:-1]*g.w[1:])).reshape((-1,1,1))
            derivative=np.zeros_like(v);derivative[:-1]+=v[1:]/den;derivative[1:]-=v[:-1]/den
            j=self.eta*np.imag(v.conj()*derivative);current.append(np.moveaxis(j,0,k)+m*self.p[k])
        D=float(sum(np.sum(g.xyz[k]*current[k]) for k in range(3)));I=float(np.sum(m*g.r**2))
        T=sum(op.expectation(u) for op in self.ops)+float(np.sum(m*self.p2))
        K=T/a**2+ad/a*D+.5*ad**2*I;W=float(.5*np.sum(m*phi)/a)
        P=[float(np.sum(current[k])/a+ad*np.sum(m*g.xyz[k])) for k in range(3)]
        J=[float(np.sum(g.xyz[(k+1)%3]*current[(k+2)%3]-g.xyz[(k+2)%3]*current[(k+1)%3])) for k in range(3)]
        return dict(M=float(m.sum()),E=K+W,K=K,W=W,D_chi=D,I_chi=I,P=P,J=J,a=a,adot=ad)
