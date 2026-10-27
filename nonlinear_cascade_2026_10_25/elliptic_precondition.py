"""Coupled fixed-density scalar Schur inverse plus exact material CN response.
For the nonlinear solve only: physical forces and accepted residual unchanged.
"""
import time
import numpy as np
from scipy.linalg.lapack import dgttrf,dgttrs
from scipy.optimize import newton_krylov
from scipy.optimize._nonlin import NoConvergence
from scipy.sparse.linalg import LinearOperator
from fine_cc import FineCC
class EllipticPreconditioned(FineCC):
 def build_pre(self,a,x,p,chi,dt,scale):
  n=self.n;nw=len(self.wr);ni=int(np.sum(self.r*self.rm<80));rho=abs(a[0])**2/self.vol;cm0=self.true_chi_m(chi);psi=a[0]/np.sqrt(self.vol);rh,cm,beta,U=self.geometry(a,chi,rho=rho);C=np.maximum(self.k*self.w*np.real(np.conj(psi[:-1])*U*psi[1:]),0)*(self.g2/self.sigma)**2;A=1.5*rho[1:]-.5*rho[:-1];B=1.5*rho[:-1]-.5*rho[1:];kd=np.zeros(n);ko=-C*A*B;kd[:-1]+=C*B*B;kd[1:]+=C*A*A;kd+=np.maximum(self.J*np.sin(2*x)*np.real(np.exp(1j*beta)*np.conj(a[1])*a[0]),0)*((self.g+2*self.g2*rho)/self.sigma)**2;factor=dt*dt/4;dg=self.wvol+factor*self.c**2*self.wdiag+dt/2*self.gamma*self.wvol;off=-factor*self.c**2*self.ww;dg2=dg.copy();of2=off.copy();dg2[:ni]+=factor*kd[:ni];of2[:ni-1]+=factor*ko[:ni-1];lu=dgttrf(of2.copy(),dg2.copy(),of2.copy());mup=self.pot(a,x,True)[1]
  def apply(v):
   out=v.copy();f=np.zeros(nw);f[:ni]=v[4*n:4*n+ni];rhs=dg*f;rhs[:-1]+=off*f[1:];rhs[1:]+=off*f[:-1];z,info=dgttrs(*lu[:-1],np.asfortranarray(rhs[:,None]));assert info==0;dc=v[4*n:].copy();dc[:ni]=z[:ni,0];out[4*n:]=dc;direction=scale*dc;norm=max(float(np.max(abs(dc))),1.);eps=1e-3/norm;oldcm=self.chi_override;oldrho=self.rho_coupling
   try:
    self.rho_coupling=rho;self.chi_override=cm0+eps*direction;mu=mup.copy();mu[0]+=self.transfer(a,x,chi)[0];ap=self.material_cn(a,mu,x,chi,dt);self.chi_override=cm0-eps*direction;mu=mup.copy();mu[0]+=self.transfer(a,x,chi)[0];am=self.material_cn(a,mu,x,chi,dt);da=(ap-am)/(2*eps)
   finally:self.chi_override=oldcm;self.rho_coupling=oldrho
   out[:2*n]+=da.real.ravel();out[2*n:4*n]+=da.imag.ravel();return out
  return LinearOperator((5*n,5*n),matvec=apply)
 def full_step(self,a0,x0,p0,chi0,pi0,dt):
  n=self.n;size=2*n;cm0=self.true_chi_m(chi0);scale=self.sigma/max(self.g+2*self.g2*max(abs(a0[0])**2/self.vol),1);calls=0;iterations=0;last=None;start=time.monotonic()
  pre=self.build_pre(a0,x0,p0,chi0,dt,scale)
  def fun(y):
   nonlocal calls,last
   calls+=1;a1=a0+(y[:size]+1j*y[size:2*size]).reshape(2,n);cmid=y[2*size:]*scale;self.chi_override=cmid;self.rho_coupling=(abs(a0[0])**2+abs(a1[0])**2)/(2*self.vol);am=(a0+a1)/2;xm,pm,res=self.carrier_mid(am,chi0,x0,p0,dt,x0);mu=self.pot(am,xm,True)[1];u=self.enclosed(abs(am[0])**2);omega=pm/self.Z(am);mu[0]-=(2/np.pi)**2*self.ell2/self.c**2*self.transpose(.5*self.vol*omega**2*self.f(u)[3]);mu[0]+=self.transfer(am,xm,chi0)[0];an=self.material_cn(a0,mu,xm,chi0,dt);_,source,bulk,conv,U,rate=self.transfer(am,xm,chi0);cn,pn,sink,qs=self.wave_source(chi0,pi0,source/self.g,dt);ra=(a1-an).ravel();rc=(cmid-(cm0+self.true_chi_m(cn))/2)/scale;last=(an,xm,pm,cn,pn,sink,qs,res,source,bulk,conv);return np.r_[ra.real,ra.imag,rc]
  mu=self.pot(a0,x0,True)[1];self.rho_coupling=abs(a0[0])**2/self.vol;self.chi_override=cm0;mu[0]+=self.transfer(a0,x0,chi0)[0];predict=self.material_cn(a0,mu,x0,chi0,dt)-a0;y0=np.r_[predict.ravel().real,predict.ravel().imag,cm0/scale]
  def callback(y,f):
   nonlocal iterations
   iterations+=1
  failed=False
  try:y=newton_krylov(fun,y0,inner_M=pre,f_tol=3e-13,maxiter=30,inner_maxiter=60,rdiff=1e-6,callback=callback,line_search='armijo')
  except NoConvergence as exc:y=np.array(exc.args[0]);failed=True
  except (ValueError,np.linalg.LinAlgError):y=y0;failed=True
  residual=float(max(abs(fun(y))));an,xm,pm,cn,pn,sink,qs,res,S,B,C=last;self.rho_coupling=None;self.chi_override=None;self.energy_chi=cn
  return an,2*xm-x0,2*pm-p0,cn,pn,sink,qs,{'iterations':iterations,'fixed_point_error':residual,'carrier_root_residual':res,'source_cell':S,'source_bulk':B,'source_conversion':C,'residual_evaluations':calls,'root_runtime_seconds':time.monotonic()-start,'root_nonconvergence':failed}

