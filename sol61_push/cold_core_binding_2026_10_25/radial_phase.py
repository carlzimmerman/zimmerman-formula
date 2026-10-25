import numpy as np
from phase_support import profile

def radial_phase(s,u,a=None,b=None):
 total=0.;pp=np.r_[0.,s.p,0.]
 for e in range(s.ne):
  ix=np.arange(3*e,3*e+4);ok=(ix>0)&(ix<3*s.ne);ii=ix[ok]-1;v=np.zeros((4,s.nt,s.nf),complex);v[ok]=u[ii]/np.sqrt(s.w[ii,None,None])/s.sa[None,:,:];xx=(e+(s.z+1)/2)/s.ne;rr=s.R*np.sinh(s.alpha*xx)/np.sinh(s.alpha);J=s.R*s.alpha*np.cosh(s.alpha*xx)/np.sinh(s.alpha);dv=(s.Dr@v.reshape(4,-1)).reshape(v.shape)*(2*s.ne/J)[:,None,None]+1j*pp[ix,None,None]/s.eta*v;rho=abs(v)**2;q=np.imag(v.conj()*dv);part=np.divide(q*q,rho,out=np.zeros_like(rho),where=rho>0);wg=np.array([1,5,5,1])*J/(12*s.ne)*profile(rr,a,b)**2;total+=.5*s.eta**2*np.sum(wg[:,None,None]*s.aw[None,:,:]*part)
 return float(total)
