import numpy as np

def derivative(s,a):
 full=np.concatenate([np.zeros_like(a[:1]),a,np.zeros_like(a[:1])]);out=np.zeros_like(full);count=np.zeros(len(full))
 xi=np.arange(s.ne+1)/s.ne
 for e in range(s.ne):
  ix=np.arange(3*e,3*e+4);xx=(e+(s.z+1)/2)/s.ne;J=s.R*s.alpha*np.cosh(s.alpha*xx)/np.sinh(s.alpha)
  out[ix]+=(s.Dr@full[ix].reshape(4,-1)).reshape(full[ix].shape)*(2*s.ne/J)[:,None,None];count[ix]+=1
 return out[1:-1]/count[1:-1,None,None]

def flux(s,u,pot,radii=(1,2,4,8,12,16)):
 A=u/s.sr[:,None,None]/s.sa[None,:,:];Dr=derivative(s,A)+1j*s.p[:,None,None]/s.eta*A
 H=s.radial_apply(u)+s.angular(u,0,True)+pot*u
 At=-1j/s.eta*H/s.sr[:,None,None]/s.sa[None,:,:]
 mt=2/s.eta*np.imag(u.conj()*H);pt=s.poisson_mass(mt);pr=derivative(s,pot)
 Aph=np.fft.ifft(np.fft.fft(A,axis=2)*(1j*s.m)[None,None,:],axis=2);pph=np.fft.ifft(np.fft.fft(pot,axis=2)*(1j*s.m)[None,None,:],axis=2).real
 # radial surface Jz: x cross T.n -> eta^2 Re(d_phi psi* d_r psi), plus gravity stress.
 fm=s.r**2*np.sum(s.aw[None,:,:]*s.eta*np.imag(A.conj()*Dr),axis=(1,2))
 fe=s.r**2*np.sum(s.aw[None,:,:]*(-s.eta**2*np.real(At*Dr.conj())-pt*pr/(4*np.pi)),axis=(1,2))
 fj=s.r**2*np.sum(s.aw[None,:,:]*(s.eta**2*np.real(Aph.conj()*Dr)+pph*pr/(4*np.pi)),axis=(1,2))
 return dict(r=list(radii),mass=np.interp(radii,s.r,fm).tolist(),energy=np.interp(radii,s.r,fe).tolist(),Jz=np.interp(radii,s.r,fj).tolist())
