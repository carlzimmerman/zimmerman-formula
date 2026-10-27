"""Isolated longitudinal 3D Gaussian field, with a finite nonlinear quadrature."""
import numpy as np
from scipy.special import erf

class Field3D:
    def __init__(self,kappa,sigma=1.,extent=24.,spacing=1.):
        self.kappa=float(kappa);self.sigma=float(sigma);self.extent=float(extent)
        n=int(np.ceil(2*extent/spacing));self.spacing=2*extent/n
        q=-extent+(np.arange(n)+.5)*self.spacing
        self.grid=np.stack(np.meshgrid(q,q,q,indexing='ij'),axis=-1).reshape(-1,3)
        self.volume=self.spacing**3

    def kernel(self,d):
        r2=np.sum(d*d,axis=-1);r=np.sqrt(r2);s=self.sigma
        a=r/(np.sqrt(2)*s);e=np.exp(-a*a)
        enclosed=erf(a)-np.sqrt(2/np.pi)*r/s*e
        safe=np.maximum(r,1e-20)
        f=enclosed/safe**3
        fp_over_r=np.sqrt(2/np.pi)*e/(s**3*safe**2)-3*enclosed/safe**5
        small=r<1e-3*s
        f=np.where(small,np.sqrt(2/np.pi)/(3*s**3)*(1-3*r2/(10*s*s)),f)
        fp_over_r=np.where(small,-np.sqrt(2/np.pi)/(5*s**5),fp_over_r)
        return f,fp_over_r

    def quadratic(self,x,m):
        if not len(m): return 0.,np.zeros_like(x)
        d=x[:,None,:]-x[None,:,:];r=np.linalg.norm(d,axis=-1);s=self.sigma
        safe=np.maximum(r,1e-20);a=r/(2*s)
        kernel=np.where(r>1e-7*s,erf(a)/safe,1/(np.sqrt(np.pi)*s))
        e=.5*float(m@kernel@m)
        f=(erf(a)-r/(s*np.sqrt(np.pi))*np.exp(-a*a))/safe**3
        f=np.where(r>1e-3*s,f,1/(6*np.sqrt(np.pi)*s**3))
        grad=-m[:,None]*np.sum((m[None,:]*f)[:,:,None]*d,axis=1)
        return e,grad

    def evaluate(self,x,m,force=True):
        e,grad=self.quadratic(x,m)
        if not len(m): return e,grad,dict(max_z=0.,quadratic=0.,nonlinear=0.)
        nonlin=0.;maxz=0.
        # Bound memory even during mesh refinement; no all-particle tensor stored.
        for start in range(0,len(self.grid),4096):
            q=self.grid[start:start+4096];d=q[:,None,:]-x[None,:,:]
            f,fp=self.kernel(d);u=np.sum((f*m[None,:])[:,:,None]*d,axis=1)
            mag=np.linalg.norm(u,axis=1);z=mag/self.kappa;maxz=max(maxz,float(max(z)))
            if np.any(z>=1):raise ValueError('sampled 3D field saturation')
            # Stable w(z)-z²/2.
            rem=np.where(z<.03,sum(z**j/j for j in range(3,13)),-np.log1p(-z)-z-.5*z*z)
            nonlin+=self.volume*self.kappa**2/(4*np.pi)*float(np.sum(rem))
            if force:
                # dU_remainder/du = u*z/(4pi*(1-z)).
                p=u*(z/(1-z))[:,None]/(4*np.pi)*self.volume
                dot=np.sum(d*p[:,None,:],axis=-1)
                grad-=m[:,None]*np.sum(f[:,:,None]*p[:,None,:]+fp[:,:,None]*dot[:,:,None]*d,axis=0)
        return e+nonlin,grad,dict(max_z=maxz,quadratic=e,nonlinear=nonlin)
