"""Continuum shell budgets; include gravitational boundary energy, not half-W alone."""
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.special import sph_harm
from scipy.integrate import cumulative_trapezoid
def derivative(s,a,potential=False):
 # Regular one-sided polynomial origin limit; the reporting balls end well before the outer element.
 x=s.r[:4];weights=np.array([np.prod(-np.delete(x,i))/np.prod(x[i]-np.delete(x,i)) for i in range(4)])
 left=np.einsum('i,ijk->jk',weights,a[:4])[None,:,:]
 right=a[-1:]*s.r[-1]/s.R if potential else np.zeros_like(a[-1:])
 full=np.concatenate([left,a,right]);out=np.zeros_like(full);count=np.zeros(len(full))
 for e in range(s.ne):
  ix=np.arange(3*e,3*e+4);xx=(e+(s.z+1)/2)/s.ne;J=s.R*s.alpha*np.cosh(s.alpha*xx)/np.sinh(s.alpha)
  out[ix]+=(s.Dr@full[ix].reshape(4,-1)).reshape(full[ix].shape)*(2*s.ne/J)[:,None,None];count[ix]+=1
 return out[1:-1]/count[1:-1,None,None]

def initial(s,f):
 r,w,lm,v=[f[k] for k in ['r','w','lm','initial']];j=next(j for j,x in enumerate(lm) if tuple(x)==(0,0));valid=(r<21.8)&(abs(v[:,j])>1e-20);rv=r[valid];sp=CubicSpline(rv,s.eta*np.unwrap(np.angle(v[valid,j])))
 def phase(x):return np.where(x<=rv[-1],sp(x),sp(rv[-1])+sp(rv[-1],1)*(x-rv[-1]))
 amp=v/(np.sqrt(w)*r)[:,None]*np.exp(-1j*phase(r)/s.eta)[:,None];active=np.flatnonzero(np.max(abs(amp),axis=0)>1e-14);av=CubicSpline(r,amp[:,active],axis=0)(s.r);av[s.r>=r[-1]]=0
 Y=np.array([sph_harm(lm[k,1],lm[k,0],s.phi[None,:],np.arccos(s.mu)[:,None]) for k in active]);return np.einsum('rk,kij->rij',av,Y)*s.sr[:,None,None]*s.sa[None,:,:]

def shells(s,u,pot,radii):
 A=u/s.sr[:,None,None]/s.sa[None,:,:];Dr=derivative(s,A)+1j*s.p[:,None,None]/s.eta*A;pr=derivative(s,pot,True)
 # Barycentric derivative on Gauss-Legendre nodes.
 x=s.mu;bw=np.array([1/np.prod(x[i]-np.delete(x,i)) for i in range(len(x))]);D=np.zeros((len(x),len(x)))
 for i in range(len(x)):
  for j in range(len(x)):
   if i!=j:D[i,j]=bw[j]/bw[i]/(x[i]-x[j])
  D[i,i]=-D[i].sum()
 dmu=np.einsum('ij,rjk->rik',D,A);dph=np.fft.ifft(np.fft.fft(A,axis=2)*(1j*s.m)[None,None,:],axis=2)
 kin=.5*s.eta**2*(abs(Dr)**2+((1-x*x)[None,:,None]*abs(dmu)**2+abs(dph)**2/(1-x*x)[None,:,None])/s.r[:,None,None]**2)
 rho=abs(A)**2;jz=s.eta*np.imag(A.conj()*dph)
 # canonical energy in ball = integral(K+half rhoPhi)+surface(Phi DrPhi)/(8pi).
 density=[rho,jz,kin+.5*rho*pot];out={}
 for name,d in zip(['M','Jz','E_half'],density):
  radial=s.r*s.r*np.sum(s.aw[None,:,:]*d,axis=(1,2));cdf=cumulative_trapezoid(np.r_[0,radial],np.r_[0,s.r],initial=0)[1:];out[name]=np.interp(radii,s.r,cdf)
 surface=s.r*s.r*np.sum(s.aw[None,:,:]*pot*pr,axis=(1,2))/(8*np.pi);out['E_canonical']=out['E_half']+np.interp(radii,s.r,surface)
 return {k:v.tolist() for k,v in out.items()}
