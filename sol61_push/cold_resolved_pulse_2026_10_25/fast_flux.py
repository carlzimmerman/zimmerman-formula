"""Same nodal physical currents as CCT015 flux, without full-field derivative arrays."""
import numpy as np

def local_derivative(s,a,rows,wave=False):
 out=np.zeros((len(rows),s.nt,s.nf),complex if wave else float)
 for k,row in enumerate(rows):
  f=int(row)+1;elements=[f//3]
  if f%3==0:elements.append(f//3-1)
  count=0
  for e in elements:
   if e<0 or e>=s.ne:continue
   ix=np.arange(3*e,3*e+4);values=np.zeros((4,s.nt,s.nf),out.dtype);inside=(ix>0)&(ix<3*s.ne);ii=ix[inside]-1;values[inside]=a[ii]/s.sr[ii,None,None]/s.sa[None,:,:] if wave else a[ii]
   loc=f-3*e;xx=(e+(s.z[loc]+1)/2)/s.ne;J=s.R*s.alpha*np.cosh(s.alpha*xx)/np.sinh(s.alpha);out[k]+=np.einsum('i,ijk->jk',s.Dr[loc],values)*(2*s.ne/J);count+=1
  out[k]/=count
 return out

def flux(s,u,pot,radii=(1,2,4,8,12,16)):
 lo=np.clip(np.searchsorted(s.r,radii)-1,0,len(s.r)-2);rows=np.unique(np.r_[lo,lo+1]);H=s.radial_apply(u)+s.angular(u,0,True)+pot*u;At=-1j/s.eta*H[rows]/s.sr[rows,None,None]/s.sa[None,:,:];mt=2/s.eta*np.imag(u.conj()*H);del H;pt=s.poisson_mass(mt)[rows];del mt
 A=u[rows]/s.sr[rows,None,None]/s.sa[None,:,:];Dr=local_derivative(s,u,rows,True)+1j*s.p[rows,None,None]/s.eta*A;pr=local_derivative(s,pot,rows);Aph=np.fft.ifft(np.fft.fft(A,axis=2)*(1j*s.m)[None,None,:],axis=2);pph=np.fft.ifft(np.fft.fft(pot[rows],axis=2)*(1j*s.m)[None,None,:],axis=2).real
 rr=s.r[rows]**2;fm=rr*np.sum(s.aw[None,:,:]*s.eta*np.imag(A.conj()*Dr),axis=(1,2));fe=rr*np.sum(s.aw[None,:,:]*(-s.eta**2*np.real(At*Dr.conj())-pt*pr/(4*np.pi)),axis=(1,2));fj=rr*np.sum(s.aw[None,:,:]*(s.eta**2*np.real(Aph.conj()*Dr)+pph*pr/(4*np.pi)),axis=(1,2))
 return dict(r=list(radii),mass=np.interp(radii,s.r[rows],fm).tolist(),energy=np.interp(radii,s.r[rows],fe).tolist(),Jz=np.interp(radii,s.r[rows],fj).tolist())
