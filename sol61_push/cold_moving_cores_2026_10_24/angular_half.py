"""Separable, finite Galerkin angular Hamiltonian for CCT-009."""
import numpy as np
from scipy.special import sph_harm,jv
from numpy.polynomial.legendre import leggauss
class SHT:
    def __init__(self,L,M,nt=None,nphi=None):
        self.L=L;self.M=M;self.mu,self.w=leggauss(nt or 2*L+2);self.nphi=nphi or 2*M+2
        self.lm=[(l,m) for l in range(L+1) for m in range(-min(l,M),min(l,M)+1) if m%2==0]
        self.blocks=[]
        for m in range(-M,M+1,2):
            ix=np.array([j for j,(l,mm) in enumerate(self.lm) if mm==m],int)
            if not len(ix):continue
            T=np.array([sph_harm(m,self.lm[j][0],0,np.arccos(self.mu)).real for j in ix]).T
            self.blocks.append((m,ix,T))
        self.nm=len(self.lm)
    def forward(self,c):
        ft=np.zeros((len(c),len(self.mu),self.nphi),complex)
        for m,ix,T in self.blocks:ft[:,:,(m//2)%self.nphi]=c[:,ix]@T.T
        return np.fft.ifft(ft,axis=-1)*self.nphi
    def back(self,f):
        ft=np.fft.fft(f,axis=-1)/self.nphi
        c=np.empty((len(f),self.nm),complex)
        for m,ix,T in self.blocks:c[:,ix]=(ft[:,:,(m//2)%self.nphi]*self.w)@T*(2*np.pi)
        return c
    def integral(self,f):return (2*np.pi/self.nphi)*np.sum(f*self.w[None,:,None],axis=(1,2))
class Angular:
    def __init__(self,L,M,r,w):
        self.field=SHT(L,M);self.density=SHT(2*L,2*M,len(self.field.mu),self.field.nphi)
        self.r=r;self.w=w;self.ell=np.array([l for l,m in self.density.lm]);self.m=np.array([m for l,m in self.field.lm])
    def green(self,rho):
        r=self.r;ell=self.ell;shell=(self.w*r*r)[:,None]*rho
        inner=np.empty_like(shell);outer=np.zeros_like(shell)
        inner[0]=shell[0]/r[0]
        for i in range(1,len(r)):inner[i]=(r[i-1]/r[i])**(ell+1)*inner[i-1]+shell[i]/r[i]
        for i in range(len(r)-2,-1,-1):outer[i]=(r[i]/r[i+1])**ell*(outer[i+1]+shell[i+1]/r[i+1])
        return -4*np.pi/(2*ell+1)*(inner+outer)
    def potential(self,v):
        vang=self.field.forward(v)
        rho=abs(vang)**2/(self.w*self.r*self.r)[:,None,None]
        coeff=self.green(self.density.back(rho))
        pang=self.density.forward(coeff)
        if np.max(abs(pang.imag))>1e-8*max(1,np.max(abs(pang.real))):raise ArithmeticError('nonreal Phi')
        pang=pang.real;W=.5*float(sum(self.field.integral(abs(vang)**2*pang)))
        return pang,coeff,W
    def self_energy(self,v):
        va=self.field.forward(v);rho=abs(va)**2/(self.w*self.r*self.r)[:,None,None]
        cr=self.density.back(rho);co=self.green(cr)
        return .5*float(np.real(np.sum((self.w*self.r*self.r)[:,None]*cr.conj()*co)))
    def multiply(self,v,pang):return self.field.back(self.field.forward(v)*pang)
    def exp(self,v,pang,ds,eta):
        # P V P is Hermitian; its spectrum is inside the sampled real V interval.
        lo=np.min(pang,axis=(1,2));hi=np.max(pang,axis=(1,2));cen=((lo+hi)/2)[:,None];rad=((hi-lo)/2)[:,None]
        rad=np.maximum(rad,1e-14)
        x=ds*rad/eta
        def B(z):return (self.multiply(z,pang)-cen*z)/rad
        prev=v;cur=B(v);out=jv(0,x)*prev+2*(-1j)*jv(1,x)*cur
        quiet=0
        for k in range(2,200):
            nxt=2*B(cur)-prev;coef=2*(-1j)**k*jv(k,x);out+=coef*nxt
            quiet=quiet+1 if k>float(np.max(abs(x)))+3 and float(np.max(abs(coef)))<1e-14 else 0
            prev,cur=cur,nxt
            if quiet>=3:break
        else:raise ArithmeticError('Chebyshev degree cap')
        return out*np.exp(-1j*ds*cen/eta)
