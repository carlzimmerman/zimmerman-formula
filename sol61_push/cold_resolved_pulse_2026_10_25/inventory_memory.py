"""Operator-consistent mapped-SEM finite-ball inventory; no evolution changes."""
import numpy as np
from lean import OLD
from budget import derivative

def shells(s,u,pot,radii=(1,2,4,8,12,16)):
 eta=s.eta;ne=s.ne;z=s.z;n=len(s.r)
 b=s.transform(u);ang=np.sum(abs(b)**2*s.lam[None,:,:],axis=(1,2))*eta**2/(2*s.r*s.r*s.w)
 mass=np.sum(abs(u)**2,axis=(1,2))/s.w;jz=eta*np.sum(abs(b)**2*s.m[None,None,:],axis=(1,2))/s.w;fw=.5*np.sum(abs(u)**2*pot,axis=(1,2))/s.w
 del b
 chi=u/np.sqrt(s.w[:,None,None])/s.sa[None,:,:];full=np.concatenate([np.zeros_like(chi[:1]),chi,np.zeros_like(chi[:1])]);pp=np.r_[0.,s.p,0.]
 del chi
 ang=np.r_[0.,ang,0.];mass=np.r_[0.,mass,0.];jz=np.r_[0.,jz,0.];fw=np.r_[0.,fw,0.];lp=[];ip=[]
 for i in range(4):
  q=np.poly1d([1.])
  for j in range(4):
   if i!=j:q*=np.poly1d([1.,-z[j]])/(z[i]-z[j])
  lp.append(q);ip.append(np.polyint(q))
 seg=[];K=0.;W=0.
 for e in range(ne):
  ix=np.arange(3*e,3*e+4);xx=(e+(z+1)/2)/ne;J=s.R*s.alpha*np.cosh(s.alpha*xx)/np.sinh(s.alpha)
  dc=(s.Dr@full[ix].reshape(4,-1)).reshape(full[ix].shape)*(2*ne/J)[:,None,None]+1j*pp[ix,None,None]/eta*full[ix]
  kr=.5*eta**2*np.sum(s.aw[None,:,:]*abs(dc)**2,axis=(1,2));F=np.array([mass[ix],jz[ix],kr+ang[ix]+fw[ix]])*J[None,:];seg.append(F)
  wg=np.array([1,5,5,1])/(12*ne);K+=float(wg@(J*(kr+ang[ix])));W+=float(wg@(J*fw[ix]))
 values=[]
 for R in radii:
  xi=np.arcsinh(R*np.sinh(s.alpha)/s.R)/s.alpha;ee=min(int(xi*ne),ne-1);value=np.zeros(3)
  for e in range(ee+1):
   ze=1. if e<ee else 2*(xi*ne-e)-1;weights=np.array([p(ze)-p(-1.) for p in ip])/(2*ne);value+=seg[e]@weights
  ix=np.arange(3*ee,3*ee+4);cr=np.einsum('i,ijk->jk',np.array([p(ze) for p in lp]),full[ix]);value[2]-=.5*eta**2*np.sum(s.aw*abs(cr)**2)/R;values.append(value)
 values=np.array(values).T;surf=np.interp(radii,s.r,s.r*s.r*np.sum(s.aw[None,:,:]*pot*derivative(s,pot,True),axis=(1,2))/(8*np.pi))
 return dict(r=list(radii),M=values[0].tolist(),Jz=values[1].tolist(),E_half=values[2].tolist(),E_canonical=(values[2]+surf).tolist(),K_global_SEM=K,W_global_SEM=W,scope='mapped LGL and element-local weak derivative; partial-element cardinal integration still requires refinement')
