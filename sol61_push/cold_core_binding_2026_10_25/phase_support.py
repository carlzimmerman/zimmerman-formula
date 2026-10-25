"""Streaming weak-SEM phase kinetic; optional real radial density weight."""
import numpy as np

def profile(r,a=None,b=None):
 if a is None:return np.ones_like(r)
 t=np.clip((r-a)/(b-a),0,1);w=np.cos(np.pi*t/2)**2;return np.where(r>=b,0.,w)

def phase_kinetic(s,u,a=None,b=None):
 total=0.;pp=np.r_[0.,s.p,0.]
 for e in range(s.ne):
  ix=np.arange(3*e,3*e+4);ok=(ix>0)&(ix<3*s.ne);ii=ix[ok]-1;v=np.zeros((4,s.nt,s.nf),complex);v[ok]=u[ii]/np.sqrt(s.w[ii,None,None])/s.sa[None,:,:];xx=(e+(s.z+1)/2)/s.ne;rr=s.R*np.sinh(s.alpha*xx)/np.sinh(s.alpha);J=s.R*s.alpha*np.cosh(s.alpha*xx)/np.sinh(s.alpha);dv=(s.Dr@v.reshape(4,-1)).reshape(v.shape)*(2*s.ne/J)[:,None,None]+1j*pp[ix,None,None]/s.eta*v
  rho=abs(v)**2;q=np.imag(v.conj()*dv);part=np.divide(q*q,rho,out=np.zeros_like(rho),where=rho>0);wg=np.array([1,5,5,1])*J/(12*s.ne)*profile(rr,a,b)**2;total+=.5*s.eta**2*np.sum(wg[:,None,None]*s.aw[None,:,:]*part)
 x=s.mu;bw=np.array([1/np.prod(x[i]-np.delete(x,i)) for i in range(s.nt)]);D=np.zeros((s.nt,s.nt))
 for i in range(s.nt):
  for j in range(s.nt):
   if i!=j:D[i,j]=bw[j]/bw[i]/(x[i]-x[j])
  D[i,i]=-D[i].sum()
 Dw=np.sqrt(s.wmu)[:,None]*D/np.sqrt(s.wmu)[None,:]
 for lo in range(0,len(s.r),32):
  sl=slice(lo,lo+32);v=u[sl];rho=abs(v)**2;dm=np.einsum('ij,rjk->rik',Dw,v);dp=np.fft.ifft(np.fft.fft(v,axis=2)*(1j*s.m)[None,None,:],axis=2);qm=np.imag(v.conj()*dm);qp=np.imag(v.conj()*dp);pm=np.divide(qm*qm,rho,out=np.zeros_like(rho),where=rho>0);pphi=np.divide(qp*qp,rho,out=np.zeros_like(rho),where=rho>0);total+=.5*s.eta**2*np.sum(profile(s.r[sl],a,b)[:,None,None]**2/s.r[sl,None,None]**2*((1-x*x)[None,:,None]*pm+pphi/(1-x*x)[None,:,None]))
 return float(total)
