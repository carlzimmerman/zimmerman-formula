"""Periodic electrostatic action solver, D0=1, Heaviside field units.

Minimize integral ell(|grad phi|)-rho*phi with spectral derivatives.
Its Euler equation is div D=rho, E=-grad phi, D=E/(1+|E|).
No particle deposition, spherical averaging or prescribed curl D=0.
"""
import numpy as np
from scipy.optimize import minimize


def lagrangian(e):
    e=np.asarray(e)
    return np.where(e<1e-4,e**2/2-e**3/3+e**4/4-e**5/5,e-np.log1p(e))


def energy_density(d):
    d=np.abs(np.asarray(d))
    if np.any(d>=1):raise ValueError('saturated displacement')
    return np.where(d<1e-4,d**2/2+d**3/3+d**4/4+d**5/5,-np.log1p(-d)-d)


def displacement(E):
    return E/(1+np.linalg.norm(E,axis=-1,keepdims=True))


class Field:
    def __init__(self,N=25,L=24.,sigma=1.5):
        if N%2!=1:raise ValueError('odd N avoids Nyquist derivative ambiguity')
        self.N=N;self.L=L;self.sigma=sigma;self.dv=(L/N)**3
        axis=np.arange(N)*L/N-L/2
        self.xyz=np.stack(np.meshgrid(axis,axis,axis,indexing='ij'),axis=-1)
        k=2*np.pi*np.fft.fftfreq(N,d=L/N)
        self.k=np.stack(np.meshgrid(k,k,k,indexing='ij'),axis=-1)
        k2=np.sum(self.k**2,axis=-1)
        self.inv=np.zeros_like(k2);self.inv[k2>0]=1/np.sqrt(k2[k2>0])

    def precondition(self,a):
        return np.fft.ifftn(np.fft.fftn(a)*self.inv).real

    def grad(self,a):
        ak=np.fft.fftn(a)
        return np.stack([np.fft.ifftn(1j*self.k[...,i]*ak).real for i in range(3)],axis=-1)

    def div(self,a):
        return sum(np.fft.ifftn(1j*self.k[...,i]*np.fft.fftn(a[...,i])).real for i in range(3))

    def sources(self,positions,charges,background):
        if abs(sum(charges))>1e-12 and not background:raise ValueError('periodic sources must be neutral')
        rho=np.zeros((self.N,)*3);derivatives=[]
        for pos,q in zip(positions,charges):
            dx=(self.xyz-np.array(pos)+self.L/2)%self.L-self.L/2
            w=np.exp(-np.sum(dx*dx,axis=-1)/(2*self.sigma**2))
            w/=w.sum()*self.dv
            d=dx/self.sigma**2
            d-=np.sum(w[...,None]*d,axis=(0,1,2))*self.dv
            rho+=q*w;derivatives.append(q*w[...,None]*d)
        rho-=rho.mean()  # exact periodic zero mode; background only when authorized
        return rho,derivatives

    def solve(self,positions,charges,background=False):
        rho,derivatives=self.sources(positions,charges,background)
        shape=rho.shape
        def objective(flat):
            phi=self.precondition(flat.reshape(shape));E=-self.grad(phi)
            D=displacement(E)
            val=np.sum(lagrangian(np.linalg.norm(E,axis=-1))-rho*phi)
            gradient=self.precondition(self.div(D)-rho)
            return val,gradient.ravel()
        initial=self.precondition(rho).ravel()
        sol=minimize(objective,initial,jac=True,method='L-BFGS-B',
                     options={'gtol':1e-10,'ftol':1e-15,'maxiter':500,'maxls':40})
        phi=self.precondition(sol.x.reshape(shape));E=-self.grad(phi);D=displacement(E)
        residual=np.linalg.norm(self.div(D)-rho)/np.linalg.norm(rho)
        if residual>2e-6:raise RuntimeError(f'Gauss residual {residual}: {sol.message}')
        H=float(np.sum(energy_density(np.linalg.norm(D,axis=-1)))*self.dv)
        dual=float(np.sum(rho*phi-lagrangian(np.linalg.norm(E,axis=-1)))*self.dv)
        forces=[(-np.sum(phi[...,None]*der,axis=(0,1,2))*self.dv).tolist() for der in derivatives]
        curlD=np.stack([self.grad(D[...,2])[...,1]-self.grad(D[...,1])[...,2],
                        self.grad(D[...,0])[...,2]-self.grad(D[...,2])[...,0],
                        self.grad(D[...,1])[...,0]-self.grad(D[...,0])[...,1]],axis=-1)
        return dict(N=self.N,energy=H,dual_energy=dual,duality_relative=abs(H-dual)/max(H,1e-30),
                    gauss_relative=float(residual),total_charge=float(rho.sum()*self.dv),
                    max_displacement=float(np.max(np.linalg.norm(D,axis=-1))),forces=forces,
                    curlD_rms=float(np.sqrt(np.mean(curlD**2))),iterations=sol.nit,
                    optimizer_success=bool(sol.success),message=str(sol.message))
