"""Same 3D longitudinal functional, with every isolated Gaussian self term exact."""
import functools
import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize_scalar
from field import Field3D

class ExactSelfField(Field3D):
    @functools.lru_cache(maxsize=256)
    def self_energy(self,mass):
        # Exact maximum of a Gaussian field: independent of packet position.
        peak=minimize_scalar(lambda r:-mass*r*self.kernel(np.array([[r,0,0.]]))[0][0]/self.kappa,
                             bounds=(.01*self.sigma,8*self.sigma),method='bounded')
        if -peak.fun>=1:raise ValueError('isolated Gaussian field saturation')
        def fun(r):
            z=mass*r*self.kernel(np.array([[r,0,0.]]))[0][0]/self.kappa
            rem=sum(z**j/j for j in range(3,14)) if z<.03 else -np.log1p(-z)-z-.5*z*z
            return self.kappa**2*r*r*rem
        correction,error=quad(fun,0,np.inf,epsabs=1e-11,epsrel=1e-9,limit=200)
        return correction,float(-peak.fun),error

    def evaluate(self,x,m,force=True):
        e,grad=self.quadratic(x,m)
        if not len(m):return e,grad,dict(max_z=0.,quadratic=0.,nonlinear=0.)
        exact=[self.self_energy(float(mi)) for mi in m]
        correction=sum(v[0] for v in exact)
        if len(m)==1:
            return e+correction,grad,dict(max_z=exact[0][1],quadratic=e,nonlinear=correction)
        maxz=0.
        for start in range(0,len(self.grid),4096):
            q=self.grid[start:start+4096];d=q[:,None,:]-x[None,:,:]
            f,fp=self.kernel(d);individual=(f*m[None,:])[:,:,None]*d
            u=np.sum(individual,axis=1);z=np.linalg.norm(u,axis=1)/self.kappa
            zi=np.linalg.norm(individual,axis=2)/self.kappa
            maxz=max(maxz,float(max(z)))
            if np.any(z>=1):raise ValueError('sampled 3D field saturation')
            def rem(z):return np.where(z<.03,sum(z**j/j for j in range(3,13)),-np.log1p(-z)-z-.5*z*z)
            correction+=self.volume*self.kappa**2/(4*np.pi)*float(np.sum(rem(z)-np.sum(rem(zi),axis=1)))
            if force:
                p=self.volume/(4*np.pi)*(u[:,None,:]*(z/(1-z))[:,None,None]-individual*(zi/(1-zi))[:,:,None])
                dot=np.sum(d*p,axis=-1)
                grad-=m[:,None]*np.sum(f[:,:,None]*p+fp[:,:,None]*dot[:,:,None]*d,axis=0)
        return e+correction,grad,dict(max_z=maxz,quadratic=e,nonlinear=correction)
