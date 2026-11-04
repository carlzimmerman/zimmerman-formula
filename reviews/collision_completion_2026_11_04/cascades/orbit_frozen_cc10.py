"""Common all-species gas/field orbit, no neutral radiation replacement."""
import sys,os
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import json,math
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq
from numpy.polynomial.legendre import leggauss
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reviews/coupled_trapping_2026_11_04/kinetics'))
from accurate import LocalPotential
MASS=62.;T0=.004657258204883617;MU=2e6;XI=.02

class GenericOrbit:
 def __init__(self,background,q,W,phase_nodes=12,neutral_force=True):
  self.bg=background;self.q=np.asarray(q);self.W=np.asarray(W);self.n=len(q)
  self.groups=background.groups;self.ns=len(self.groups);self.by=background.by
  self.deg=np.array([g['degeneracy'] for g in self.groups]);self.measure=(self.deg[:,None]*self.W[None,:]/(2*math.pi**2)).ravel()
  self.charged=np.array([g['charged'] for g in self.groups]);self.eta=np.repeat([1 if g['kind']=='S' else -1 for g in self.groups],self.n)
  packet=json.loads((ROOT/'reviews/coupled_trapping_2026_11_04/gravity_resonance/run_leading001/result.json').read_text())['packet'];p=packet['global_profile']
  self.v=LocalPotential(CubicSpline(p['grid'],p['V0_origin_subtracted_mu4'],bc_type=((1,p['origin_force']),(2,0))),packet['local_profile'])
  self.xlo=max(float(background.xs[0]),.1);self.xhi=min(float(background.xs[-1]),40.)
  self.grid=np.unique(np.r_[self.xlo,np.linspace(self.xlo,10,321),np.linspace(10,self.xhi,161)])
  z,w=leggauss(phase_nodes);self.theta=(z+1)*math.pi/2;self.tw=w*math.pi/2
  self.last_x=None;self.neutral_force=neutral_force;self.J0=None
 def hubble(self,N):return math.sqrt(math.pi**2*106.75/90)*(T0*math.exp(-N))**2*MU/(2.435e18*XI**2)
 def gas(self,x,N,Y):
  xx=np.atleast_1d(x);t=T0*math.exp(-N);m2=np.maximum(self.bg.mass2(xx),0);slopes=self.bg.mass2(xx,1)
  p2=(t*self.q)**2;en=np.sqrt(m2[:,:,None]+p2[None,None,:]);u=np.asarray(Y).reshape(self.ns,self.n)
  rho=t**3*np.einsum('ksq,sq->k',en,u);pressure=t**3*np.einsum('ksq,sq->k',p2[None,None,:]/(3*np.maximum(en,1e-300)),u)
  force_by=t**3*np.einsum('ksq,sq->ks',slopes[:,:,None]/(2*np.maximum(en,1e-300)),u)
  force=force_by.sum(axis=1) if self.neutral_force else force_by@self.charged
  return dict(rho=rho,pressure=pressure,force=force,force_by=force_by,energy=en.reshape(len(xx),-1))
 def potential(self,x,N,Y):return self.v(x)+self.gas(x,N,Y)['rho']
 def force(self,x,N,Y):return float(self.v(x,1))+float(self.gas(x,N,Y)['force'][0])
 def well(self,N,Y):
  vg=self.potential(self.grid,N,Y);mins=np.where((vg[1:-1]<vg[:-2])&(vg[1:-1]<vg[2:]))[0]+1
  if not len(mins):raise RuntimeError('No minimum in retained background support')
  i=int(mins[0] if self.last_x is None else min(mins,key=lambda j:abs(self.grid[j]-self.last_x)))
  xm=brentq(lambda x:self.force(x,N,Y),self.grid[i-1],self.grid[i+1],xtol=1e-12)
  emin=float(self.potential(xm,N,Y)[0]);maxima=np.where((vg[1:-1]>vg[:-2])&(vg[1:-1]>vg[2:]))[0]+1
  left=maxima[maxima<i];right=maxima[maxima>i]
  xl=self.grid[int(left[-1])] if len(left) else self.xlo;xr=self.grid[int(right[0])] if len(right) else self.xhi
  limit=min(float(self.potential(xl,N,Y)[0]),float(self.potential(xr,N,Y)[0]))
  if limit<=emin:raise RuntimeError('No retained closed well; continuation required')
  return xm,emin,xl,xr,limit
 def orbit(self,N,Y,E=None,J=None,commit=False):
  xm,emin,left,right,limit=self.well(N,Y)
  h=max(1e-5,abs(xm)*1e-6);curv=(self.force(xm+h,N,Y)-self.force(xm-h,N,Y))/(2*h)
  if curv<=0:raise RuntimeError('Nonpositive local curvature')
  omega=math.sqrt(curv/MASS)
  def at_energy(en,full=False):
   if en<=emin:return 0. if not full else None
   xL=brentq(lambda x:float(self.potential(x,N,Y)[0])-en,left,xm,xtol=1e-12)
   xR=brentq(lambda x:float(self.potential(x,N,Y)[0])-en,xm,right,xtol=1e-12)
   mid=(xL+xR)/2;half=(xR-xL)/2;xx=mid-half*np.cos(self.theta);dx=half*np.sin(self.theta)
   gg=self.gas(xx,N,Y);dd=np.maximum(en-self.v(xx)-gg['rho'],1e-34)
   action=math.sqrt(2*MASS)/math.pi*float(self.tw@(dx*np.sqrt(dd)))
   if not full:return action
   ww=self.tw*dx/np.sqrt(dd);period=math.sqrt(2*MASS)*sum(ww);ww/=sum(ww)
   return dict(E=en,J=action,xmid=xm,x_inner=xL,x_outer=xR,period=period,omega=2*math.pi/period,xs=xx,weights=ww,kin2=2*dd,gas=gg,minimum=emin,harmonic=False)
  if J is not None and self.J0 is not None and J<self.J0*1e-7:
   amp=math.sqrt(2*J*omega/curv);xx=xm-amp*np.cos(self.theta);ww=self.tw/math.pi;gg=self.gas(xx,N,Y)
   result=dict(E=emin+omega*J,J=J,xmid=xm,x_inner=xm-amp,x_outer=xm+amp,period=2*math.pi/omega,omega=omega,xs=xx,weights=ww,kin2=2*omega*J*np.sin(self.theta)**2,gas=gg,minimum=emin,harmonic=True)
  else:
   eps=max(abs(limit-emin)*1e-12,1e-30)
   if E is None:
    if at_energy(limit-eps)<=J:raise RuntimeError('Retained-well separatrix; direct continuation required')
    E=brentq(lambda en:at_energy(en)-J,emin+eps,limit-eps,xtol=1e-24,rtol=1e-12)
   if not emin<E<limit:raise RuntimeError('Total energy outside retained closed well')
   result=at_energy(E,True)
  if commit:self.last_x=xm
  return result
 def initial(self,seed=0.):
  N=0.;x0=.18444259422092926;f=np.full(self.ns*self.n,float(seed));i=self.by['Fc_0'];f[i*self.n:(i+1)*self.n]=1/(np.exp(self.q)+1)
  Y=self.measure*f;E=float(self.potential(x0,N,Y)[0]);orb=self.orbit(N,Y,E=E,commit=True);self.J0=orb['J']
  return Y,orb
 def summary(self,N,Y,orb):
  t=T0*math.exp(-N);w=orb['weights'];gas=orb['gas'];num=np.asarray(Y).reshape(self.ns,self.n).sum(axis=1)
  sSM=2*math.pi**2/45*106.75*(t/XI)**3;physical=num*t**3
  forces=w@gas['force_by'];energies=w@gas['energy'];occ=Y/self.measure
  return dict(N=N,Tc_over_mu=t,x_inner=orb['x_inner'],x_outer=orb['x_outer'],x_minimum=orb['xmid'],energy=orb['E'],action=orb['J'],omega=orb['omega'],H_over_omega=self.hubble(N)/orb['omega'],Y_charged=float(physical@self.charged/sSM),charged_force=float(forces@self.charged),neutral_force=float(forces@(~self.charged)),particle_energy=t**3*float(energies@Y),comoving_number_by_group=num.tolist(),min_f=float(occ.min()),max_fermion_f=float(occ[self.eta<0].max()))
