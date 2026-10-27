"""Root preconditioner from the derived positive local(1+eta) inertia."""
import time
import numpy as np
from scipy.optimize import newton_krylov
from scipy.optimize._nonlin import NoConvergence
from scipy.sparse.linalg import LinearOperator
from fine_cc import FineCC
class PhasePreconditioned(FineCC):
 def full_step(self,a0,x0,p0,chi0,pi0,dt):
  n=self.n;size=2*n;rho0=abs(a0[0])**2/self.vol;diag=np.r_[np.ones(4*n),1+self.g2*self.g2*rho0**3/self.c**2];pre=None;cm0=self.true_chi_m(chi0);scale=self.sigma/max(self.g+2*self.g2*max(abs(a0[0])**2/self.vol),1);calls=0;iterations=0;last=None;start=time.monotonic()
  def pre_apply(v):
   out=v/diag;dc=out[4*n:]*scale;corr=np.zeros((2,n),complex);corr[0]=-2j*self.g2*rho0*a0[0]*dc/self.sigma;out[:size]+=corr.real.ravel();out[size:2*size]+=corr.imag.ravel();return out
  pre=LinearOperator((5*n,5*n),matvec=pre_apply)
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
