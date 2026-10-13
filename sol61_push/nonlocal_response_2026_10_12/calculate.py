import os
for n in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[n]='1'
import ast,json
from pathlib import Path
import numpy as np
from scipy.optimize import brentq,minimize
HERE=Path(__file__).resolve().parent;SRC=HERE.parents[1]/'campaign_fresh_gravity/CFG596_lean_pm_1024/cfg596_pm.py'
names={'Y_P','H_P','DELTA','LYG','YG','DH_MONO','H_MONO'}
nodes=[n for n in ast.parse(SRC.read_text()).body if (isinstance(n,ast.FunctionDef) and n.name in {'h_rar','dh_rar','nu_mono'}) or (isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in names for t in n.targets))]
env={'np':np,'brentq':brentq};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(SRC),'exec'),env)
gtable=np.r_[0.,env['YG']+env['H_MONO']];ptable=np.r_[0.,env['H_MONO']]
slope=np.diff(ptable)/np.diff(gtable);integ=np.r_[0.,np.cumsum(.5*(ptable[1:]+ptable[:-1])*np.diff(gtable))]
def ec(g):
 j=np.clip(np.searchsorted(gtable,g)-1,0,len(gtable)-2);z=g-gtable[j]
 return -(integ[j]+ptable[j]*z+.5*slope[j]*z*z)
N=32;box=64.;dx=box/N;shape=(N,)*3
x=(np.arange(N)-N/2)*dx;X=np.meshgrid(x,x,x,indexing='ij');r=np.sqrt(sum(v*v for v in X))
k=2*np.pi*np.fft.fftfreq(N,dx);k[N//2]=0
K=np.meshgrid(k,k,k,indexing='ij');k2=sum(v*v for v in K)
inv=np.zeros(shape);np.divide(1,np.sqrt(k2),out=inv,where=k2>0)
rho=np.exp(-r*r/8);rho*=4*np.pi/(rho.sum()*dx**3);rho-=rho.mean()
def invD(a):return np.fft.ifftn(np.fft.fftn(a)*inv).real
def grad(phi):
 ft=np.fft.fftn(phi);return np.array([np.fft.ifftn(1j*kk*ft).real for kk in K])
def div(v):return np.fft.ifftn(sum(1j*kk*np.fft.fftn(a) for kk,a in zip(K,v))).real
u0=-invD(rho);rng=np.random.default_rng(359);direction=rng.normal(size=shape);direction/=np.linalg.norm(direction)
checks=[];rows=[];profiles={}
def check(name,v,tol):checks.append(dict(name=name,value=float(v),tolerance=tol,passed=bool(abs(v)<=tol)))
for L in (4,8,16,'local'):
 H=np.where(k2>0,1.,0.) if L=='local' else -np.expm1(-k2*L*L/2)
 def project(v):return np.fft.ifftn(np.fft.fftn(v,axes=(-3,-2,-1))*H,axes=(-3,-2,-1)).real
 def evaluate(u,external=0.,details=False):
  phi=invD(u.reshape(shape));q=grad(phi);q[0]+=external
  z=project(q);g=np.sqrt(np.sum(z*z,axis=0));p=np.interp(g,gtable,ptable)
  coeff=np.zeros(shape);np.divide(-p,g,out=coeff,where=g>0)
  response=coeff*z;flux=q+project(response);res=-div(flux)+rho
  energy=float(np.sum(.5*np.sum(q*q,axis=0)+ec(g)+rho*phi))
  gu=invD(res)
  return (energy,gu.ravel(),res,q) if details else (energy,gu.ravel())
 E,gu=evaluate(u0);eps=1e-4
 fd=(evaluate(u0+eps*direction)[0]-evaluate(u0-eps*direction)[0])/(2*eps)
 exact=float(gu@direction.ravel());check('variational derivative '+str(L),(fd-exact)/max(abs(fd),abs(exact),1e-10),1e-4)
 opt=minimize(evaluate,u0.ravel(),jac=True,method='L-BFGS-B',options={'maxiter':500,'gtol':1e-9,'ftol':1e-14,'maxcor':8})
 E,gu,res,q=evaluate(opt.x,details=True)
 # The Nyquist derivative has null modes. Audit only represented source modes.
 represented=np.fft.ifftn(np.fft.fftn(rho)*(k2>0)).real
 residual=float(np.linalg.norm(np.fft.ifftn(np.fft.fftn(res)*(k2>0)).real)/np.linalg.norm(represented))
 check('stationary residual '+str(L),residual,.001)
 check('uniform external invariance '+str(L),np.max(abs(evaluate(opt.x,external=.1)[1]-gu)),1e-9)
 sel=(r>=4)&(r<=12);rad=sum(qi*xi for qi,xi in zip(q,X))/np.maximum(r,1e-20)
 profiles[str(L)]=rad[sel]
 rows.append(dict(L=L,iterations=int(opt.nit),optimizer_success=bool(opt.success),message=str(opt.message),residual=residual,energy=E,mean_radial_force=float(rad[sel].mean())))
reference=profiles['local']
for row in rows:row['relative_force_L2_vs_local']=float(np.linalg.norm(profiles[str(row['L'])]-reference)/np.linalg.norm(reference))
out=dict(rows=rows,checks=checks,all_checks_pass=all(c['passed'] for c in checks),source_null_fraction=float(np.linalg.norm(rho-represented)/np.linalg.norm(rho)))
(HERE/'run/results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert out['all_checks_pass']
