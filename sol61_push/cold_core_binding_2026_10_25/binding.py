"""Window energy and rigorous finite-frozen-operator spectral-weight bounds."""
import numpy as np

def negative_weight_bounds(mean,variance,lower):
 assert variance>=-1e-12*max(1,mean*mean)
 variance=max(0.,variance)
 if mean<0:
  assert lower<0 and mean>=lower-1e-10*max(1,abs(lower))
  return max(0.,min(1.,max(mean/lower,mean*mean/(variance+mean*mean)))),1.
 if mean>0:return 0.,max(0.,min(1.,variance/(variance+mean*mean)))
 return 0.,1.

def momentum_z(s,u):
 total=0.;pp=np.r_[0.,s.p,0.]
 for e in range(s.ne):
  ix=np.arange(3*e,3*e+4);ok=(ix>0)&(ix<3*s.ne);ii=ix[ok]-1;v=np.zeros((4,s.nt,s.nf),complex);v[ok]=u[ii]/np.sqrt(s.w[ii,None,None])/s.sa[None,:,:];xx=(e+(s.z+1)/2)/s.ne;J=s.R*s.alpha*np.cosh(s.alpha*xx)/np.sinh(s.alpha)
  dv=(s.Dr@v.reshape(4,-1)).reshape(v.shape)*(2*s.ne/J)[:,None,None]+1j*pp[ix,None,None]/s.eta*v
  total+=s.eta*np.sum((np.array([1,5,5,1])*J/(12*s.ne))[:,None,None]*s.aw[None,:,:]*s.mu[None,:,None]*np.imag(v.conj()*dv))
 x=s.mu;bw=np.array([1/np.prod(x[i]-np.delete(x,i)) for i in range(s.nt)]);D=np.zeros((s.nt,s.nt))
 for i in range(s.nt):
  for j in range(s.nt):
   if i!=j:D[i,j]=bw[j]/bw[i]/(x[i]-x[j])
  D[i,i]=-D[i].sum()
 Dw=np.sqrt(s.wmu)[:,None]*D/np.sqrt(s.wmu)[None,:]
 for lo in range(0,len(s.r),32):
  sl=slice(lo,lo+32);du=np.einsum('ij,rjk->rik',Dw,u[sl]);total+=s.eta*np.sum(np.imag(u[sl].conj()*du)*(1-x*x)[None,:,None]/s.r[sl,None,None])
 return float(total)

def measure(s,v,full_potential=None):
 mass=float(np.vdot(v,v).real);kin=s.angular(v,0,True);kin+=s.radial_apply(v);K=float(np.vdot(v,kin).real);pot=s.poisson(v);W=.5*float(np.sum(abs(v)**2*pot));Pz=momentum_z(s,v);rest=K-Pz*Pz/(2*mass);assert rest>=-1e-10*max(1,K)
 spectra={}
 for name,phi in [('self',pot)]+([] if full_potential is None else [('full_envelope',full_potential)]):
  hh=0.;h2=0.
  for lo in range(0,len(s.r),32):
   sl=slice(lo,lo+32);Hv=kin[sl]+phi[sl]*v[sl];hh+=float(np.vdot(v[sl],Hv).real);h2+=float(np.vdot(Hv,Hv).real)
  mean=hh/mass;var=h2/mass-mean*mean;lower=float(phi.min());pmin,pmax=negative_weight_bounds(mean,var,lower);spectra[name]=dict(mean=mean,variance=var,H_lower_bound=lower,negative_spectral_weight_lower=pmin,negative_spectral_weight_upper=pmax,negative_spectral_mass_lower=mass*pmin,negative_spectral_mass_upper=mass*pmax)
 Jz=Iz=z=Minner=0.
 for lo in range(0,len(s.r),32):
  sl=slice(lo,lo+32);u=v[sl];rho=abs(u)**2;bf=np.fft.fft(u,axis=2,norm='ortho');Jz+=float(s.eta*np.sum(abs(bf)**2*s.m[None,None,:]));Iz+=float(np.sum(rho*s.r[sl,None,None]**2*(1-s.mu*s.mu)[None,:,None]));z+=float(np.sum(rho*s.r[sl,None,None]*s.mu[None,:,None]));Minner+=float(rho[s.r[sl]<1].sum())
 return dict(M=mass,M_inside_reference=Minner,K=K,W_self=W,E_self=K+W,K_bulk_rest_diagnostic=rest,E_self_bulk_rest_diagnostic=rest+W,K_over_abs_W=K/abs(W),Pz=Pz,bulk_speed_z=Pz/mass,COMz=z/mass,Jz=Jz,Iz=Iz,spectra=spectra,external_envelope_potential_energy=None if full_potential is None else float(sum(np.sum(abs(v[lo:lo+32])**2*(full_potential[lo:lo+32]-pot[lo:lo+32])) for lo in range(0,len(s.r),32))),scope='windowed wave with cutoff kinetic cost; frozen spectral probability, not a particle count, retained core mass, or future capture')

def window(s,u,a,b):
 t=np.clip((s.r-a)/(b-a),0,1);w=np.cos(np.pi*t/2)**2;w[s.r>=b]=0.;return u*w[:,None,None]
