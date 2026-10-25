import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import json,numpy as np
from scipy.special import sph_harm
from sphere import Sphere
from flux import derivative
rows=[]
for ne,dt in [(32,.02),(64,.01),(128,.005)]:
 s=Sphere(ne,12,16,eta=.2);r=s.r[:,None,None];Y=sph_harm(2,2,s.phi[None,:],np.arccos(s.mu)[:,None]);initial=r*r*np.exp(-r*r/2)*Y[None,:,:];u=initial*s.sr[:,None,None]*s.sa[None,:,:];M=np.sum(abs(u)**2);T=.6;c=1/(2-2**(1/3))
 for it in range(round(T/dt)):
  for a in [c,1-2*c,c]:u=s.radial(u,a*dt/2);u=s.angular(u,a*dt);u=s.radial(u,a*dt/2)
 z=1+1j*s.eta*T;exact=r*r*Y[None,:,:]*z**(-3.5)*np.exp(-r*r/(2*z));A=u/s.sr[:,None,None]/s.sa[None,:,:];Dr=derivative(s,A);H=s.radial_apply(u)+s.angular(u,0,True);At=-1j/s.eta*H/s.sr[:,None,None]/s.sa[None,:,:];ph=np.fft.ifft(np.fft.fft(A,axis=2)*(1j*s.m)[None,None,:],axis=2)
 fm=s.r*s.r*np.sum(s.aw[None,:,:]*s.eta*np.imag(A.conj()*Dr),axis=(1,2));fj=s.r*s.r*np.sum(s.aw[None,:,:]*s.eta*s.eta*np.real(ph.conj()*Dr),axis=(1,2));fe=s.r*s.r*np.sum(s.aw[None,:,:]*(-s.eta*s.eta*np.real(At*Dr.conj())),axis=(1,2))
 Drx=exact*(2/r-r/z);Atx=exact*(-3.5j*s.eta/z+r*r*.5j*s.eta/z**2);fex=s.r*s.r*np.sum(s.aw[None,:,:]*(-s.eta*s.eta*np.real(Atx*Drx.conj())),axis=(1,2));fmx=s.r*s.r*np.sum(s.aw[None,:,:]*s.eta*np.imag(exact.conj()*Drx),axis=(1,2));mask=(s.r>.5)&(s.r<3)
 row=dict(ne=ne,dt=dt,L2_relative=float(np.sqrt(np.sum(abs((A-exact)*s.sr[:,None,None]*s.sa[None,:,:])**2)/M)),mass_residual=float(abs(np.sum(abs(u)**2)/M-1)),mass_flux_relative=float(np.linalg.norm((fm-fmx)[mask])/np.linalg.norm(fmx[mask])),energy_flux_relative=float(np.linalg.norm((fe-fex)[mask])/np.linalg.norm(fex[mask])),spin_flux_identity=float(np.max(abs(fj-2*s.eta*fm))),Jz_error=abs(s.moments(u,np.zeros_like(A.real))['Jz']/(2*s.eta*M)-1));rows.append(row)
print(json.dumps(rows,indent=2),flush=True)
assert rows[-1]['L2_relative']<rows[0]['L2_relative']/20
assert rows[-1]['L2_relative']<1e-5 and rows[-1]['energy_flux_relative']<.001
assert all(x['mass_residual']<1e-10 and x['spin_flux_identity']<1e-12 and x['Jz_error']<1e-10 for x in rows)
print(json.dumps(rows,indent=2))
