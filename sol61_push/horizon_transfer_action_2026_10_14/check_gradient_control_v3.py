import json,sys,math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_bvp,quad
out=Path(sys.argv[1]);out.mkdir(exist_ok=True)
checks=[]
def ck(n,v):
 checks.append({'name':n,'ok':bool(v)})
 if not bool(v):raise AssertionError(n)
# sigma=ln(V/Vbackground), phi=M sigma; fixed smooth Plummer source.
# This is a quasistatic perturbation after subtracting the homogeneous scalar
# equation, not an isolated stationary exponential-vacuum solution.
G=6.67430e-11;c=299792458.;Mass=6e10*1.98847e30;a0=9.360324825027975e-11;HL=1.807421796171574e-18
R=math.sqrt(G*Mass/a0);eps0=3*(HL*R/c)**2;core=.03;outer=10.
def eta_at(rr,sigma):
 y=rr/(rr*rr+core*core)**1.5*np.exp(-sigma/2)
 xx=np.divide(2*y,np.sqrt(y*y+4*y)+y,out=np.zeros_like(y),where=y>0)
 raw=xx+2*np.log1p(-xx)+xx/(1-xx)
 small=xx<.01
 raw[small]=sum((n-2)/n*xx[small]**n for n in range(3,13))
 return raw/(32*math.pi),xx
def one(scale,tol):
 eps=eps0/(scale*scale)
 mesh=np.unique(np.r_[0,np.geomspace(1e-5,1,220),np.linspace(1,outer,120)])
 def fun(rr,z,param):
  sigma=eps*(z[0]+param[0]);eta,xx=eta_at(rr,sigma)
  return np.vstack((z[1],np.expm1(sigma)-np.exp(sigma)*eta))
 def jac(rr,z,param):
  sigma=eps*(z[0]+param[0]);eta,xx=eta_at(rr,sigma)
  eta_sigma=-xx**3/(64*math.pi*(1-xx)*(2-xx))
  mat=np.zeros((2,2,len(rr)));mat[0,1]=1;mat[1,0]=eps*np.exp(sigma)*(1-eta-eta_sigma)
  jacp=np.zeros((2,1,len(rr)));jacp[1,0]=mat[1,0]
  return mat,jacp
 sol=solve_bvp(fun,lambda za,zb,param:np.array([za[0],za[1],zb[0]+param[0]]),mesh,np.zeros((2,len(mesh))),p=[.025],S=np.array([[0.,0.],[0.,-2.]]),tol=tol,max_nodes=8000,fun_jac=jac)
 ck('BVP converged '+str((scale,tol)),sol.success)
 rr=np.unique(np.r_[0,np.geomspace(1e-5,outer,1800)])
 zz=sol.sol(rr);zz[0]+=sol.p[0];sig=eps*zz[0];eta,xx=eta_at(rr,sig)
 yy=rr/(rr*rr+core*core)**1.5
 # u/a_background = e^(sigma/2) x; gtotal/a_background = y + that.
 oldeta,oldx=eta_at(rr,np.zeros_like(rr));gnew=yy+np.exp(sig/2)*xx;gold=yy+oldx
 du=np.divide(2*yy*np.expm1(sig/2),np.sqrt(yy*yy+4*np.exp(sig/2)*yy)+np.sqrt(yy*yy+4*yy),out=np.zeros_like(yy),where=yy>0)
 dev=np.divide(du,gold,out=np.zeros_like(gold),where=gold>0)
 # Independent linear Green-function center value, no BVP solve.
 chi0=quad(lambda rad:(rad-rad*rad/outer)*float(eta_at(np.array([rad]),np.array([0.]))[0][0]),0,outer,points=[core,.1,1],epsabs=1e-12,epsrel=1e-10)[0]
 ck('small perturbation domain '+str((scale,tol)),np.max(np.abs(sig))<1e-4)
 ck('Green function agreement '+str((scale,tol)),abs(zz[0,0]/chi0-1)<1e-4)
 ck('boundary and central regularity '+str((scale,tol)),abs(sol.sol(0)[1])<1e-10 and abs(sol.sol(outer)[0]+sol.p[0])<1e-10)
 return {'M_over_Mpl':scale,'tolerance':tol,'epsilon_gradient':eps,'sigma_center':float(sig[0]),'max_fractional_a0_change':float(np.expm1(sig/2).max()),'max_fractional_total_force_change':float(np.abs(dev).max()),'linear_center_Green':chi0,'BVP_center':float(zz[0,0]),'nodes':len(sol.x),'max_reported_residual':float(max(sol.rms_residuals))}
rows=[one(1.,1e-7),one(.01,1e-7),one(.001,1e-7)]
fine=one(1.,1e-9)
ck('mesh tolerance convergence',abs(rows[0]['sigma_center']/fine['sigma_center']-1)<1e-6)
ck('Planck scale gradient controls local a0',rows[0]['max_fractional_a0_change']<1e-10)
j={'passed':len(checks),'checks':checks,'rows':rows,'refined':fine,'assigned_core_kpc':core*R/3.0856775814913673e19,'assigned_R_kpc':R/3.0856775814913673e19,'interpretation':'Finite-domain quasistatic scalar/tether response with positive canonical gradient, actual residual-energy vacuum derivative and solved algebraic carrier response. Boundary sigma=0 at10rM and fixed Plummer baryons. No cold mass portal or GB source included in this local comparison; no cosmological boundary selection or full dynamical stability proved.'}
(out/'results.json').write_text(json.dumps(j,indent=2)+'\n');print(json.dumps(j,indent=2))
