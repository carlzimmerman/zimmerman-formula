"""Full non-Gaussian coordinate wavefunction for one spatial cell, four fields.
A validation model, NOT a cosmological source or a momentum-resolved bath.
Dimensionless mPhi=1, hbar=1, cell volume in mPhi^-3. The original un-normal-
ordered polynomial potential is retained; no independent rates are appended.
FFT is in FIELD-CONFIGURATION coordinates, not physical spatial momentum.
"""
import numpy as np
from scipy.fft import fftn,ifftn
class CellWavefunction:
 def __init__(self,n=32,length=12.,volume=1.,g=.002168,lam=.00881292):
  self.n=n;self.length=length;self.volume=volume;self.g=g;self.lam=lam
  self.mass=np.array([1.,1.,2*np.sqrt(1+.02**2),2*np.sqrt(1+.02**2)])
  x=(np.arange(n)-n//2)*length/n
  self.fields=np.meshgrid(x,x,x,x,indexing='ij',sparse=True)
  p=2*np.pi*np.fft.fftfreq(n,d=length/n)
  self.T=sum(pp*pp for pp in np.meshgrid(p,p,p,p,indexing='ij',sparse=True))/(2*volume)
 def potential(self,a=1.):
  f,h,x,y=self.fields;r=f*f+h*h
  return self.volume*(.5*a*a*(r+self.mass[2]**2*(x*x+y*y))+self.lam*r*r/4+self.g*a/np.sqrt(2)*(x*(f*f-h*h)+2*y*f*h))
 def initial_x_excitation(self):
  # One real X oscillator excitation above a free Gaussian product vacuum.
  # Explicit benchmark state, unrelated to the high-H source density matrix.
  psi=np.exp(-.5*self.volume*sum(m*q*q for m,q in zip(self.mass,self.fields)))*self.fields[2]
  return (psi/np.linalg.norm(psi)).astype(complex)
 def evolve(self,psi,dt,steps,start=0.,scale_factor=None):
  # Carry the entire complex amplitude between steps. No Gaussian projection,
  # occupation ceiling, dephasing, stochastic resampling, or normalization reset.
  psi=psi.copy();kinetic=np.exp(-1j*dt*self.T)
  kick=np.exp(-.5j*dt*self.potential()) if scale_factor is None else None
  for j in range(steps):
   if scale_factor is not None:kick=np.exp(-.5j*dt*self.potential(scale_factor(start+(j+.5)*dt)))
   psi*=kick;psi=ifftn(fftn(psi,norm='ortho',workers=1)*kinetic,norm='ortho',workers=1);psi*=kick
  return psi
 def diagnostics(self,psi):
  prob=abs(psi)**2;ft=fftn(psi,norm='ortho',workers=1);p=2*np.pi*np.fft.fftfreq(self.n,d=self.length/self.n)
  ps=np.meshgrid(p,p,p,p,indexing='ij',sparse=True)
  q2=np.array([np.sum(prob*q*q) for q in self.fields]);p2=np.array([np.sum(abs(ft)**2*pp*pp) for pp in ps])
  occ=(p2/self.volume+self.volume*self.mass**2*q2)/(2*self.mass)-.5
  fourth=np.sum(prob*self.fields[0]**4)-3*q2[0]**2
  cross=np.sum(prob*self.fields[0]**2*self.fields[2]**2)-q2[0]*q2[2]
  boundary=np.zeros(prob.shape,dtype=bool)
  for ax in range(4):
   sl=[slice(None)]*4;sl[ax]=0;boundary[tuple(sl)]=True;sl[ax]=-1;boundary[tuple(sl)]=True
  return dict(norm=float(prob.sum()),energy=float(np.sum(abs(ft)**2*self.T)+np.sum(prob*self.potential())),bare_occupations=occ.tolist(),phi_fourth_connected=float(fourth),phi_X_squared_connected=float(cross),boundary_probability=float(prob[boundary].sum()))
