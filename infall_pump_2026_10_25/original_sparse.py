"""Simultaneous LOCAL residual for the existing full CC midpoint equations.

Cumulative masses and reverse potentials are extra Newton unknowns. They are
constraints, not new physical variables. Sparse numerical Jacobian with explicit
dependency overapproximation; no nested carrier/material/wave root.
"""
import sys,time
from pathlib import Path
import numpy as np
from scipy.sparse import lil_matrix,csc_matrix
from scipy.sparse.linalg import splu
from scipy.optimize._numdiff import approx_derivative,group_columns
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'nonlinear_cascade_2026_10_25'))
from fine_cc import FineCC

class Original(FineCC):
 def geometry(self,a,chi,rho=None):
  if rho is None:rho=self.rho_coupling if self.rho_coupling is not None else abs(a[0])**2/self.vol
  cm=self.chi_m(chi);h=self.g+self.g2*.5*(rho[1:]+rho[:-1]);return rho,cm,np.zeros_like(rho),np.exp(-1j*h*np.diff(cm)/self.sigma)
 def transfer(self,a,x,chi):
  rho,cm,beta,U=self.geometry(a,chi);psi=a[0]/np.sqrt(self.vol);D=self.k*self.w*np.imag(np.conj(psi[:-1])*U*psi[1:]);rate=2*self.J/self.sigma*np.imag(np.conj(a[0])*self.alignment(a,x,chi)[0]);bulk=np.zeros(self.n)
  bulk[:-1]+=D*self.g2/self.sigma*(-1.5*rho[:-1]+.5*rho[1:]);bulk[1:]+=D*self.g2/self.sigma*(1.5*rho[1:]-.5*rho[:-1]);conv=(self.g+2*self.g2*rho)*rate
  md=-self.g2*D*np.diff(cm)/(2*self.sigma);mu=np.zeros(self.n);mu[:-1]+=md/self.vol[:-1];mu[1:]+=md/self.vol[1:]
  return mu,bulk+conv,bulk,conv,U,rate
 def secant_transfer(self,am,a0,a1,x,chi,chi0,dt):
  rho,cm,beta,U=self.geometry(am,chi);psi=am[0]/np.sqrt(self.vol);D=self.k*self.w*np.imag(np.conj(psi[:-1])*U*psi[1:]);rate=2*self.J/self.sigma*np.imag(np.conj(am[0])*self.alignment(am,x,chi)[0]);qsec=self.g+2*self.g2*rho
  pm=self.true_chi_m(2/dt*(chi-chi0));mu=-qsec*pm
  md=-self.g2*D*np.diff(cm)/(2*self.sigma);mu[:-1]+=md/self.vol[:-1];mu[1:]+=md/self.vol[1:]
  grad=np.zeros(self.n);h=self.g+self.g2*.5*(rho[1:]+rho[:-1]);grad[:-1]+=h*D/self.sigma;grad[1:]-=h*D/self.sigma
  source=qsec*(abs(a1[0])**2-abs(a0[0])**2)/dt+grad;conv=qsec*rate
  return mu,source,source-conv,conv,U,rate
 def structure(self):
  n=self.n;nw=len(self.wr);N=9*n+nw
  S=lil_matrix((N,N),dtype=int)
  for i in range(n):
   inds=np.arange(max(0,i-1),min(n,i+2));cols=np.r_[np.concatenate([j*n+inds for j in range(9)]),9*n+self.ids[inds],9*n+self.ids[inds]+1]
   for j in range(9):S[j*n+i,cols]=1
  # Last response/gravity boundary depends on the terminal cumulative masses.
  for i in range(nw):S[9*n+i,9*n+max(0,i-1):9*n+min(nw,i+2)]=1
  for i in range(n):
   inds=np.arange(max(0,i-1),min(n,i+2));cols=np.r_[np.concatenate([j*n+inds for j in range(5)]),9*n+self.ids[inds],9*n+self.ids[inds]+1]
   S[9*n+self.ids[i],cols]=1;S[9*n+self.ids[i]+1,cols]=1
  self.sparsity=csc_matrix(S);self.groups=group_columns(self.sparsity);self.pattern=(self.sparsity,self.groups)

 def full_step(self,a0,x0,p0,chi0,pi0,dt):
  if not hasattr(self,'pattern'):self.structure()
  n=self.n;nw=len(self.wr);tstart=time.monotonic();calls=0
  # Scales are fixed throughout this root and do not change its equations.
  ascale=np.maximum(np.sqrt(np.sum(abs(a0)**2,axis=0)),1e-12)
  cscale=self.sigma/max(self.g+2*self.g2*np.max(abs(a0[0])**2/self.vol),1.)
  mscale=max(np.sum(abs(a0)**2),1.)
  ctscale=np.maximum(self.enclosed(abs(a0[0])**2)*self.r**2,1e-20*self.r**2)
  cgscale=np.maximum(self.enclosed(np.sum(abs(a0)**2,axis=0))*self.r**2,1e-20*self.r**2)
  pscale=1.+np.max(abs(self.pot(a0,x0,True)[1]))
  scales=np.r_[np.tile(ascale,4),np.ones(n),ctscale,cgscale,np.full(2*n,pscale),np.full(nw,cscale)]
  amp0=abs(a0[0])**2/self.vol
  def decode(y):
   z=y*scales
   a=z[:n]+1j*z[n:2*n];f=z[2*n:3*n]+1j*z[3*n:4*n]
   return np.array([a,f]),z[4*n:5*n],z[5*n:6*n],z[6*n:7*n],z[7*n:8*n],z[8*n:9*n],z[9*n:]
  def quantities(am,x,ct,cg,cm):
   mt=abs(am[0])**2;mf=abs(am[1])**2;u=ct/self.r**2;gd=cg/self.r**2
   W,F,Wp,Fp=self.f(u);uf=.5*(u[1:]+u[:-1]);_,ff,_,fp=self.f(uf);dx=np.diff(2*x/np.pi)
   Z=(2/np.pi)**2*self.vol*(self.ell2*F+self.vac)/self.c**2
   pm=2*Z/dt*(x-x0);omega=2/dt*(x-x0)
   resp=self.vol*(Wp+self.beta*np.sin(2*x)**2/np.pi**2*Fp)
   face=.25*self.ell2*self.w*fp*dx*dx;resp[:-1]+=face;resp[1:]+=face
   resp-=(2/np.pi)**2*self.ell2/self.c**2*.5*self.vol*omega**2*Fp
   gr=self.vol*(gd+self.gb)
   # Equivalent end-point totals, expressed with local terminal unknowns.
   Mt=ct[-1]+.5*mt[-1];M=cg[-1]+.5*(mt[-1]+mf[-1])
   tail=np.sum(self.tw*self.f(Mt*self.tt**2)[2]/self.tt**2)
   vr=self.transpose(resp)+tail;vg=-self.transpose(gr)-M/self.R-1/np.sqrt(self.R**2+self.b**2)
   coeff=(2/np.pi)**2*self.w*(self.ell2*ff+self.vac)
   beta=np.zeros_like(cm)
   cross=np.real(np.exp(1j*beta)*np.conj(am[1])*am[0])
   parts=(mt,mf,F,coeff,cross)
   return mt,mf,Z,pm,resp,gr,tail,M,vr,vg,parts
  def fun(y,details=False):
   nonlocal calls
   calls+=1
   a1,x,ct,cg,vr,vg,cm=decode(y);am=.5*(a0+a1)
   self.rho_coupling=(amp0+abs(a1[0])**2/self.vol)/2
   # chi override only interpolates the scalar to matter cells.
   self.chi_override=self.true_chi_m(cm)
   mt,mf,Z,pm,resp,gr,tail,M,vrex,vgex,parts=quantities(am,x,ct,cg,self.chi_override)
   mu=np.array([vg+vr-self.eps,vg+2.5*self.K*(mf/self.vol)**(2/3)])
   extra,source,bulk,conv,U,rate=self.secant_transfer(am,a0,a1,x,cm,chi0,dt);mu[0]+=extra
   Ha=(self.kd+mu)*am+self.J*self.alignment(am,x,cm)
   Ha[0,:-1]+=self.ko*U*am[0,1:];Ha[0,1:]+=self.ko*np.conj(U)*am[0,:-1]
   Ha[1,:-1]+=self.ko*am[1,1:];Ha[1,1:]+=self.ko*am[1,:-1]
   ra=(a1-a0+1j*dt/self.sigma*Ha)/ascale
   force,hh,off,scale=self.carrier_force(x,parts);add=4*Z/dt**2
   rx=(force+add*(x-x0)-2*p0/dt)/(scale+add)
   ctres=np.r_[ct[0]-.5*mt[0],np.diff(ct)-.5*(mt[1:]+mt[:-1])]/ctscale
   mass=mt+mf;cgres=np.r_[cg[0]-.5*mass[0],np.diff(cg)-.5*(mass[1:]+mass[:-1])]/cgscale
   rr=resp/self.r**2;gg=gr/self.r**2
   rvr=np.r_[vr[:-1]-vr[1:]-.5*(rr[:-1]+rr[1:]),vr[-1]-.5*rr[-1]-tail]/pscale
   rvg=np.r_[vg[:-1]-vg[1:]+.5*(gg[:-1]+gg[1:]),vg[-1]+.5*gg[-1]+M/self.R+1/np.sqrt(self.R**2+self.b**2)]/pscale
   dep=np.bincount(self.ids,weights=(1-self.frac)*source,minlength=nw)+np.bincount(self.ids+1,weights=self.frac*source,minlength=nw)
   lap=-self.wdiag*cm;lap[:-1]+=self.ww*cm[1:];lap[1:]+=self.ww*cm[:-1]
   # Multiply original wave equation by dt^2/4; diagonal normalize only.
   rc=cm-chi0-dt*pi0/2+dt*self.gamma/2*(cm-chi0)-dt**2*self.c**2/4*lap/self.wvol+dt**2/4*dep/self.wvol
   rc/=cscale*(1+dt*self.gamma/2+dt**2*self.c**2/4*self.wdiag/self.wvol)
   out=np.r_[ra[0].real,ra[0].imag,ra[1].real,ra[1].imag,rx,ctres,cgres,rvr,rvg,rc]
   if details:return a1,x,pm,cm,source,bulk,conv,out
   return out
  # Initial guess is the old state, exact cumulative/potential constraints.
  am=a0;ct=self.enclosed(abs(am[0])**2)*self.r**2;cg=self.enclosed(np.sum(abs(am)**2,axis=0))*self.r**2
  self.rho_coupling=amp0;self.chi_override=self.true_chi_m(chi0)
  q=quantities(am,x0,ct,cg,self.chi_override);vr,vg=q[8:10]
  y=np.r_[a0[0].real,a0[0].imag,a0[1].real,a0[1].imag,x0,ct,cg,vr,vg,chi0]/scales
  guess=getattr(self,'same_state_root',None)
  if guess is not None:
   ga0,gx0,gp0,gc0,gv0,ga1,gxm,gcm,gdt=guess
   if np.array_equal(a0,ga0) and np.array_equal(x0,gx0) and np.array_equal(p0,gp0) and np.array_equal(chi0,gc0) and np.array_equal(pi0,gv0):
    ratio=dt/gdt;ag=a0+ratio*(ga1-a0);xg=x0+ratio*(gxm-x0);cmg=chi0+ratio*(gcm-chi0);amg=(a0+ag)/2
    ctg=self.enclosed(abs(amg[0])**2)*self.r**2;cgg=self.enclosed(np.sum(abs(amg)**2,axis=0))*self.r**2
    self.rho_coupling=(amp0+abs(ag[0])**2/self.vol)/2;self.chi_override=self.true_chi_m(cmg)
    qg=quantities(amg,xg,ctg,cgg,self.chi_override);vrg,vgg=qg[8:10]
    y=np.r_[ag[0].real,ag[0].imag,ag[1].real,ag[1].imag,xg,ctg,cgg,vrg,vgg,cmg]/scales
  history=[];lastjac=None;jac_error=None
  if not hasattr(self,'jac_cache'):self.jac_cache={}
  solver=self.jac_cache.get(dt);refresh=solver is None;jac_builds=0
  try:
   for it in range(36):
    r=fun(y);err=float(np.max(abs(r)));history.append(err)
    if err<2e-12:break
    built=refresh
    if refresh:
     jac=approx_derivative(fun,y,method='2-point',rel_step=None,abs_step=2e-7,sparsity=self.pattern,f0=r)
     solver=splu(csc_matrix(jac));jac_builds+=1
    delta=solver.solve(-r);rate=1.;merit=np.linalg.norm(r)
    for ls in range(18):
     trial=y+rate*delta;rt=fun(trial)
     if np.all(np.isfinite(rt)) and np.linalg.norm(rt)<merit:break
     rate*=.5
    if ls==17 and np.linalg.norm(rt)>=merit:
     if not built:refresh=True;continue
     break
    refresh=(np.linalg.norm(rt)>merit*.3 or rate<.5)
    y=trial
   a1,x,pm,cm,source,bulk,conv,r=fun(y,True)
   if np.max(abs(r))<2e-12:
    self.jac_cache[dt]=solver
    self.same_state_root=(a0.copy(),x0.copy(),p0.copy(),chi0.copy(),pi0.copy(),a1.copy(),x.copy(),cm.copy(),dt)
   pi1=4/dt*(cm-chi0)-pi0;chi1=2*cm-chi0;v=(pi0+pi1)/2
   sink=float(dt*(self.wvol@(self.gamma*v*v)));qs=float(dt*(self.wvol@(self.gamma*v)))
   # Independent old wave inverse and carrier checks catch recurrence/index errors.
   cw,pw,_,_=self.wave_source(chi0,pi0,source/self.g,dt)
   self.rho_coupling=(amp0+abs(a1[0])**2/self.vol)/2;self.chi_override=self.true_chi_m(cm)
   cres=self.carrier_force(x,self.vacuum_parts((a0+a1)/2,cm))[0]+4*self.Z((a0+a1)/2)/dt**2*(x-x0)-2*p0/dt
   return a1,2*x-x0,2*pm-p0,chi1,pi1,sink,qs,{'iterations':it+1,'fixed_point_error':float(np.max(abs(r))),'carrier_root_residual':float(np.max(abs(r[4*n:5*n]))),'source_cell':source,'source_bulk':bulk,'source_conversion':conv,'residual_evaluations':calls,'root_runtime_seconds':time.monotonic()-tstart,'root_history':history,'old_wave_inverse_error':float(np.max(abs(cw-chi1))/cscale),'jacobian_colors':int(max(self.groups)+1),'jacobian_directional_relative_error':jac_error,'jacobian_builds':jac_builds}
  finally:
   self.rho_coupling=None;self.chi_override=None;self.energy_chi=locals().get('chi1',chi0)
