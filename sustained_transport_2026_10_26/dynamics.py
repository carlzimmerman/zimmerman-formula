"""Independent continuous full Hamiltonian vector field and charge-safe probe."""
import sys
sys.path.insert(0,'infall_pump_2026_10_25')
import numpy as np
from scipy.optimize import root_scalar
from quiet_model_checked import QuietFull

def model():
 m=QuietFull(eta=.01,material_h_kpc=.125,wave_R_kpc=10000.);m.support=np.zeros(m.n);return m

def load(path):
 s=np.load(path);return tuple(s[k].copy() for k in ['a','alpha','carrier_p','chi','pi'])

def field(m,z):
 a,x,p,c,v=z
 extra,S,bulk,conv,U,G=m.transfer(a,x,c);mu=m.pot(a,x,True)[1];u=m.enclosed(abs(a[0])**2);xd=p/m.Z(a)
 mu[0]-=(2/np.pi)**2*m.ell2/m.c**2*m.transpose(.5*m.vol*xd**2*m.f(u)[3]);mu[0]+=extra
 H=(m.kd+mu)*a+m.J*m.alignment(a,x,c)
 H[0,:-1]+=m.ko*U*a[0,1:];H[0,1:]+=m.ko*np.conj(U)*a[0,:-1]
 H[1,:-1]+=m.ko*a[1,1:];H[1,1:]+=m.ko*a[1,:-1]
 ad=-1j*H/m.sigma;pd=-m.carrier_force(x,m.vacuum_parts(a,c))[0]
 lap=-m.wdiag*c;lap[:-1]+=m.ww*c[1:];lap[1:]+=m.ww*c[:-1]
 dep=np.bincount(m.ids,weights=(1-m.frac)*S,minlength=len(c))+np.bincount(m.ids+1,weights=m.frac*S,minlength=len(c))
 vd=m.c**2*lap/m.wvol-dep/m.wvol-m.gamma*v
 return (ad,xd,pd,v,vd)

def radius(m,a):
 q=abs(a[0])**2/np.sum(abs(a)**2,axis=0);i=np.flatnonzero((q[:-1]-.5)*(q[1:]-.5)<0)[-1]
 return float((m.r[i]+(.5-q[i])*(m.r[i+1]-m.r[i])/(q[i+1]-q[i]))*m.rm)

def Rdot(m,z):
 a=z[0];ad=field(m,z)[0];mass=abs(a)**2;md=2*np.real(np.conj(a)*ad);q=mass[0]/np.sum(mass,axis=0);qd=(md[0]-q*np.sum(md,axis=0))/np.sum(mass,axis=0)
 i=np.flatnonzero((q[:-1]-.5)*(q[1:]-.5)<0)[-1];dr=(m.r[i+1]-m.r[i])*m.rm;dq=q[i+1]-q[i]
 g=np.array([dr*(.5-q[i+1])/dq**2,-dr*(.5-q[i])/dq**2])
 return float(g@qd[i:i+2]/m.tdyn)

def Rddot(m,z,eps):
 f=field(m,z)
 return (Rdot(m,tuple(y+eps*d for y,d in zip(z,f)))-Rdot(m,tuple(y-eps*d for y,d in zip(z,f))))/(2*eps*m.tdyn)

def perturb(m,z,displacement):
 # Material-only diagnostic. No scalar or material phase packet is supplied.
 a,x,p,c,v=z;mass=np.sum(abs(a)**2,axis=0);theta=np.arctan2(abs(a[0]),abs(a[1]));R=radius(m,a);rr=m.r*m.rm
 gate=np.exp(-((rr-R)/3)**8);vt=-np.gradient(theta,rr)*gate;vx=-np.gradient(x,rr)*gate
 # One interior transition bump enforces exact global Noether charge without
 # changing total density in any cell or adding scalar momentum.
 w=np.exp(-((rr-(R-1.5))/.7)**2)*gate
 target=m.charge(a,v);phase=np.exp(1j*np.angle(a))
 def make(A,B):
  th=theta+A*vt+B*w
  aa=np.sqrt(mass)[None,:]*np.array([np.sin(th),np.cos(th)])*phase
  return aa
 def correction(A):
  def f(B):return m.charge(make(A,B),v)-target
  B=root_scalar(f,x0=0.,x1=1e-5,method='secant',xtol=1e-13,maxiter=60).root
  return B
 def residual(A):return radius(m,make(A,correction(A)))-R-displacement
 A=root_scalar(residual,x0=displacement,x1=displacement*1.01+1e-6,method='secant',xtol=1e-11,maxiter=60).root;B=correction(A)
 aa=make(A,B);xx=x+A*vx
 zz=(aa,xx,p.copy(),c.copy(),v.copy())
 assert np.max(abs(np.sum(abs(aa)**2,axis=0)-mass))<1e-14
 assert abs(m.charge(aa,v)-target)<1e-9
 assert abs(radius(m,aa)-R-displacement)<1e-8
 return zz,{'requested_displacement_kpc':displacement,'actual_displacement_kpc':radius(m,aa)-R,'A':float(A),'charge_compensating_theta_amplitude':float(B),'charge_error':m.charge(aa,v)-target,'max_cell_total_mass_error':float(np.max(abs(np.sum(abs(aa)**2,axis=0)-mass))),'wave_fields_identical':bool(np.array_equal(c,zz[3]) and np.array_equal(v,zz[4]))}
