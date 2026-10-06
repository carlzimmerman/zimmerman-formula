"""Axisymmetric conservative nonlinear projected star solve in rM/a0 units."""
import numpy as np
from scipy.interpolate import PchipInterpolator
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve
from scipy.optimize import brentq
import time
T=128.915
A0=9.3603e-11
GE=2.146e-10
GM=4*np.pi**2*(1.495978707e11)**3/(3.15576e7)**2 # Claude p57 AU/yr convention

def nu_y(y):
 y=np.asarray(y);b=1/(y*(np.sqrt(1+1/y)+1));return 1+b/(1+(y/T)**2)
Y=np.exp(np.linspace(-50,50,20001));X=Y*(2*nu_y(Y)-1)
assert np.all(np.diff(X)>0)
INV=PchipInterpolator(np.log(X),np.log(Y),extrapolate=False)
def mu_x(x):
 x=np.asarray(x);safe=np.clip(x,X[0],X[-1]);y=np.exp(INV(np.log(safe)));val=y/safe
 return np.where(x<X[0],x/4,np.where(x>X[-1],1.,val))
ye=brentq(lambda y:y*nu_y(y)-GE/A0,.001,100,xtol=1e-14)
xe=ye*(2*nu_y(ye)-1);mue=1/(2*nu_y(ye)-1)
h=ye*1e-5;dv=(nu_y(ye+h)-nu_y(ye-h))/(2*h);Le=-2*ye*dv/(2*nu_y(ye)-1+2*ye*dv)

def configure_kernel(new_T):
 global T,X,INV,ye,xe,mue,Le
 T=float(new_T);X=Y*(2*nu_y(Y)-1)
 assert np.all(np.diff(X)>0)
 INV=PchipInterpolator(np.log(X),np.log(Y),extrapolate=False)
 ye=brentq(lambda y:y*nu_y(y)-GE/A0,.001,100,xtol=1e-14)
 xe=ye*(2*nu_y(ye)-1);mue=1/(2*nu_y(ye)-1)
 h=ye*1e-5;dv=(nu_y(ye+h)-nu_y(ye-h))/(2*h);Le=-2*ye*dv/(2*nu_y(ye)-1+2*ye*dv)

def solve(nr=100,nt=40,rmin=.005,rmax=20.,tol=1e-9,maxiter=100,relax=.8,linear=False,wall=35,mass=1.,kernel_T=128.915):
 tic=time.monotonic();configure_kernel(kernel_T);re=np.geomspace(rmin,rmax,nr+1);r=(re[:-1]+re[1:])/2;dr=np.diff(re);te=np.linspace(-1,1,nt+1);t=(te[:-1]+te[1:])/2;dt=2/nt;R=r[:,None];Z=t[None,:]
 # Correct external-dominated anisotropic star boundary, including Newton monopole.
 bc=xe*rmax*t-mass/(mue*np.sqrt(1+Le)*rmax*np.sqrt(1-Le/(1+Le)*t*t))
 if linear:bc=xe*rmax*t-mass/rmax
 phi=-mass/R+xe*R*Z
 flux_in=(mass+(mue if mass==0 and not linear else 1)*xe*rmin*rmin*t)*dt
 hist=[];min_mu=1.;last=None
 ids=np.arange(nr*nt).reshape(nr,nt)
 def face_coeff(f):
  grcell=np.gradient(f,r,axis=0,edge_order=2);gtcell=np.gradient(f,t,axis=1,edge_order=2)
  gr=(f[1:]-f[:-1])/(r[1:,None]-r[:-1,None]);weight=(re[1:-1]-r[:-1])/(r[1:]-r[:-1]);gt=(1-weight[:,None])*gtcell[:-1]+weight[:,None]*gtcell[1:]
  mr=mu_x(np.hypot(gr,np.sqrt(1-t*t)[None,:]*gt/re[1:-1,None]))
  gro=(bc-f[-1])/(rmax-r[-1]);gto=(np.gradient(bc,t,edge_order=2)+gtcell[-1])/2
  mo=mu_x(np.hypot(gro,np.sqrt(1-t*t)*gto/rmax))
  gt=(f[:,1:]-f[:,:-1])/dt;grt=(grcell[:,1:]+grcell[:,:-1])/2
  mt=mu_x(np.hypot(grt,np.sqrt(1-te[1:-1]**2)[None,:]*gt/R))
  if linear:mr[:]=1;mo[:]=1;mt[:]=1
  return mr,mt,mo
 def matrix(mr,mt,mo):
  cr=re[1:-1,None]**2*mr*dt/(r[1:,None]-r[:-1,None]);ct=(1-te[1:-1]**2)[None,:]*mt*dr[:,None]/dt;co=rmax*rmax*mo*dt/(rmax-r[-1]);di=np.zeros((nr,nt));di[:-1]+=cr;di[1:]+=cr;di[:,:-1]+=ct;di[:,1:]+=ct;di[-1]+=co
  aa=ids[:-1].ravel();bb=ids[1:].ravel();cc=cr.ravel();dd=ids[:,:-1].ravel();ee=ids[:,1:].ravel();ff=ct.ravel()
  row=np.concatenate([ids.ravel(),aa,bb,dd,ee]);col=np.concatenate([ids.ravel(),bb,aa,ee,dd]);data=np.concatenate([di.ravel(),-cc,-cc,-ff,-ff]);mat=coo_matrix((data,(row,col)),shape=(nr*nt,nr*nt)).tocsc();rhs=np.zeros((nr,nt));rhs[0]-=flux_in;rhs[-1]+=co*bc
  return mat,rhs.ravel(),cr,ct,co
 for it in range(maxiter):
  if time.monotonic()-tic>wall:raise RuntimeError('wall_guard')
  mr,mt,mo=face_coeff(phi);min_mu=min(min_mu,float(min(mr.min(),mt.min(),mo.min())));mat,rhs,*_=matrix(mr,mt,mo);new=spsolve(mat,rhs,permc_spec='MMD_AT_PLUS_A').reshape(nr,nt);new=relax*new+(1-relax)*phi
  update=float(np.max(np.abs(new-phi)/(1+np.abs(phi))));phi=new;hist.append(update)
  if update<tol:break
 converged=hist[-1]<tol
 mr,mt,mo=face_coeff(phi);mat,rhs,cr,ct,co=matrix(mr,mt,mo);res=mat@phi.ravel()-rhs;res_scaled=float(np.max(np.abs(res))/(1+np.max(np.abs(rhs))))
 # Discrete radial/angular flux conservation; angular end faces have sin²theta=0.
 fr=re[1:-1,None]**2*mr*(phi[1:]-phi[:-1])/(r[1:,None]-r[:-1,None]);fout=rmax*rmax*mo*(bc-phi[-1])/(rmax-r[-1]);massflux=np.sum(fr,axis=1)*dt/2;massout=float(np.sum(fout)*dt/2)
 # Piecewise constant angular projection. Exact cell integral of P2 removes radial monopole.
 w2=((te[1:]**3-te[:-1]**3)-(te[1:]-te[:-1]))/2
 v2=phi@w2*2.5
 # Source and external uniform are l0/l1 and vanish in this projection.
 fits={}
 for lo,hi in [(.01,.025),(.015,.035),(.025,.06),(.04,.09),(.06,.12)]:
  pick=(r>=lo)&(r<=hi);rr=r[pick];vv=v2[pick]
  # Harmonic interior solution contains regular r² plus inner-boundary r^-3 image.
  design=np.array([rr*rr,rr**(-3)]).T;scale=np.linalg.norm(design,axis=0);coef=np.linalg.lstsq(design/scale,vv,rcond=None)[0]/scale;relative=float(np.max(np.abs(vv-design@coef))/(max(np.max(np.abs(vv)),1e-30)));fits[str((lo,hi))]={'A2_star':float(coef[0]),'inner_image':float(coef[1]),'fit_residual':relative,'nodes':int(pick.sum())}
 # Physical Phi=(PhiN+Phistar)/2, Q2 convention PhiQ=-Q2 r²P2/3.
 A2=fits[str((.01,.025))]['A2_star'];rM=np.sqrt(GM/A0);Q2=-1.5*A2*A0/rM
 return {'nr':nr,'nt':nt,'rmin':rmin,'rmax':rmax,'iterations':len(hist),'converged':converged,'last_update':hist[-1],'nonlinear_residual_scaled':res_scaled,'min_mu_face':min_mu,'mass_flux_range':[float(massflux.min()),float(massflux.max())],'mass_flux_outer':massout,'fits':fits,'Q2_visible_SI':float(Q2),'elapsed':time.monotonic()-tic,'history':hist,'kernel':{'T':T,'ye':float(ye),'xe':float(xe),'mue':float(mue),'Le':float(Le)},'linear':linear,'mass':mass,'profile':{'r':r.tolist(),'phi_star_l2':v2.tolist()},'units':{'a0_SI':A0,'GM_SI_Claude_convention':float(GM),'rM_SI':float(rM)}}
