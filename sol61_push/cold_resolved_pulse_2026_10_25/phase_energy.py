"""Exact weak-SEM amplitude/phase kinetic partition of the resolved field."""
import numpy as np

def split(chi,d):
 rho=abs(chi)**2;z=chi.conj()*d;ka=np.divide(z.real**2,rho,out=abs(d)**2,where=rho>0);kp=np.divide(z.imag**2,rho,out=np.zeros_like(rho),where=rho>0)
 return ka,kp

def measure(s,u):
 eta=s.eta;chi=u/np.sqrt(s.w[:,None,None])/s.sa[None,:,:];full=np.concatenate([np.zeros_like(chi[:1]),chi,np.zeros_like(chi[:1])]);pp=np.r_[0.,s.p,0.];Ka=Kp=Icurrent=0.
 for e in range(s.ne):
  ix=np.arange(3*e,3*e+4);xx=(e+(s.z+1)/2)/s.ne;r=s.R*np.sinh(s.alpha*xx)/np.sinh(s.alpha);J=s.R*s.alpha*np.cosh(s.alpha*xx)/np.sinh(s.alpha);dc=(s.Dr@full[ix].reshape(4,-1)).reshape(full[ix].shape)*(2*s.ne/J)[:,None,None]+1j*pp[ix,None,None]/eta*full[ix]
  a,p=split(full[ix],dc);w=np.array([1,5,5,1])*J/(12*s.ne);Ka+=.5*eta**2*np.sum(w[:,None,None]*s.aw[None,:,:]*a);Kp+=.5*eta**2*np.sum(w[:,None,None]*s.aw[None,:,:]*p);Icurrent+=2*eta*np.sum((w*r)[:,None,None]*s.aw[None,:,:]*np.imag(full[ix].conj()*dc))
 x=s.mu;bw=np.array([1/np.prod(x[i]-np.delete(x,i)) for i in range(len(x))]);D=np.zeros((len(x),len(x)))
 for i in range(len(x)):
  for j in range(len(x)):
   if i!=j:D[i,j]=bw[j]/bw[i]/(x[i]-x[j])
  D[i,i]=-D[i].sum()
 dm=np.einsum('ij,rjk->rik',D,chi);dp=np.fft.ifft(np.fft.fft(chi,axis=2)*(1j*s.m)[None,None,:],axis=2);weight=.5*eta**2*(s.w/(s.r*s.r))[:,None,None]*s.aw[None,:,:]
 a,p=split(chi,dm);Ka+=np.sum(weight*(1-x*x)[None,:,None]*a);Kp+=np.sum(weight*(1-x*x)[None,:,None]*p)
 a,p=split(chi,dp);Ka+=np.sum(weight/(1-x*x)[None,:,None]*a);Kp+=np.sum(weight/(1-x*x)[None,:,None]*p)
 b=s.transform(u);Kop=float(np.real(np.vdot(u,s.radial_apply(u)))+np.sum(abs(b)**2*eta**2*s.lam[None,:,:]/(2*s.r[:,None,None]**2)));M=abs(u)**2;Jz=float(eta*np.sum(abs(b)**2*s.m[None,None,:]));Iz=float(np.sum(M*s.r[:,None,None]**2*(1-x*x)[None,:,None]));Idot=float(2/eta*np.imag(np.vdot(u,s.r[:,None,None]**2*s.radial_apply(u))));res=float(Ka+Kp-Kop)
 assert abs(res)<1e-10*max(1,Kop)
 return dict(K_amplitude=float(Ka),K_phase=float(Kp),K_operator=Kop,partition_residual=res,phase_fraction=float(Kp/Kop),I=float(np.sum(M*s.r[:,None,None]**2)),Iz=Iz,Jz=Jz,K_rotation_lower_bound=Jz*Jz/(2*Iz),I_dot_discrete=Idot,I_dot_continuum_current=float(Icurrent),scope='resolved full-field weak-SEM kinetic identity; not an equilibrium or stellar-survival certificate')
