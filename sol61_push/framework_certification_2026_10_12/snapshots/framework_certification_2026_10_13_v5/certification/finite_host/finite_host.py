import os
for n in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'): os.environ[n]='1'
import ast,json,sys,time
from pathlib import Path
import numpy as np
from scipy.optimize import brentq,minimize
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]
SRC=ROOT/'campaign_fresh_gravity/CFG596_lean_pm_1024/cfg596_pm.py'
N=int(sys.argv[1]); DEST=Path(sys.argv[2]); box=64.; L=16.; dx=box/N; shape=(N,)*3
# Whitelist only interpolation functions/assignments; no cosmological imports/engine.
names={'Y_P','H_P','DELTA','LYG','YG','DH_MONO','H_MONO'}
nodes=[n for n in ast.parse(SRC.read_text()).body if (isinstance(n,ast.FunctionDef) and n.name in {'h_rar','dh_rar','nu_mono'}) or (isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in names for t in n.targets))]
env={'np':np,'brentq':brentq};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(SRC),'exec'),env)
gtable=np.r_[0.,env['YG']+env['H_MONO']];ptable=np.r_[0.,env['H_MONO']]
slope=np.diff(ptable)/np.diff(gtable);integ=np.r_[0.,np.cumsum(.5*(ptable[1:]+ptable[:-1])*np.diff(gtable))]
def ec(g):
 j=np.clip(np.searchsorted(gtable,g)-1,0,len(gtable)-2); z=g-gtable[j]
 return -(integ[j]+ptable[j]*z+.5*slope[j]*z*z)
x=(np.arange(N)-N/2)*dx;X=np.meshgrid(x,x,x,indexing='ij');r=np.sqrt(sum(v*v for v in X)); center=(N//2,)*3
k=2*np.pi*np.fft.fftfreq(N,dx); k[N//2]=0
K=np.meshgrid(k,k,k,indexing='ij');k2=sum(v*v for v in K);H=-np.expm1(-k2*L*L/2)
inv=np.zeros(shape);np.divide(1,np.sqrt(k2),out=inv,where=k2>0)
def invD(a):return np.fft.ifftn(np.fft.fftn(a)*inv).real
def grad(phi):
 ft=np.fft.fftn(phi); return np.array([np.fft.ifftn(1j*kk*ft).real for kk in K])
def div(v):return np.fft.ifftn(sum(1j*kk*np.fft.fftn(a) for kk,a in zip(K,v))).real
def proj(v):return np.fft.ifftn(np.fft.fftn(v,axes=(-3,-2,-1))*H,axes=(-3,-2,-1)).real
checks=[]
def check(name,value,tol):checks.append({'name':name,'value':float(value),'tolerance':float(tol),'passed':bool(np.isfinite(value) and abs(value)<=tol)})
def source(c,width,mass):
 delta=[(xi-ci+box/2)%box-box/2 for xi,ci in zip(X,c)]
 rho=np.exp(-sum(v*v for v in delta)/(2*width*width));rho*=mass/(rho.sum()*dx**3)
 check('positive source mass '+str(c),rho.sum()*dx**3/mass-1,1e-12)
 return rho-rho.mean()
sat=source((0,0,0),2.,4*np.pi);host=source((16,0,0),4.,400*np.pi)
rng=np.random.default_rng(359);direction=rng.normal(size=shape);direction/=np.linalg.norm(direction)
rows=[];fields={};eff={};newton={};starts=time.monotonic()
for name,rho in [('satellite',sat),('host',host),('combined',sat+host)]:
 def evaluate(u,external=None,detail=False):
  phi=invD(u.reshape(shape));q=grad(phi)
  if external is not None:q=q+np.asarray(external).reshape(3,1,1,1)
  z=proj(q);g=np.sqrt(np.sum(z*z,axis=0));p=np.interp(g,gtable,ptable)
  coeff=np.zeros(shape);np.divide(-p,g,out=coeff,where=g>0)
  response=coeff*z;flux=q+proj(response);res=-div(flux)+rho
  energy=float(np.sum(.5*np.sum(q*q,axis=0)+ec(g)+rho*phi))*dx**3
  gu=invD(res)*dx**3
  return (energy,gu.ravel(),res,q,-div(proj(response))) if detail else (energy,gu.ravel())
 u0=-invD(rho);newton[name]=grad(invD(u0))
 E,gu=evaluate(u0);eps=1e-4
 fd=(evaluate(u0+eps*direction)[0]-evaluate(u0-eps*direction)[0])/(2*eps)
 exact=float(gu@direction.ravel());check(name+' functional gradient',(fd-exact)/max(abs(fd),abs(exact),1e-10),1e-4)
 opt=minimize(evaluate,u0.ravel(),jac=True,method='L-BFGS-B',options={'maxiter':500,'gtol':1e-9,'ftol':1e-14,'maxcor':8})
 E,gu,res,q,rhoeff=evaluate(opt.x,detail=True)
 represented=np.fft.ifftn(np.fft.fftn(rho)*(k2>0)).real
 residual=float(np.linalg.norm(np.fft.ifftn(np.fft.fftn(res)*(k2>0)).real)/np.linalg.norm(represented))
 check(name+' represented residual',residual,.001)
 uniform=np.array([.123,.231,-.117])
 check(name+' uniform-gradient residual invariance',np.max(np.abs(evaluate(opt.x,external=uniform)[1]-gu)),1e-9)
 source_null=float(np.linalg.norm(rho-represented)/np.linalg.norm(rho))
 pos=float(np.maximum(rhoeff,0).sum()*dx**3);neg=float(-np.minimum(rhoeff,0).sum()*dx**3)
 check(name+' effective-source integral',abs(float(rhoeff.sum()*dx**3))/max(pos+neg,1e-30),1e-12)
 rows.append({'name':name,'iterations':int(opt.nit),'optimizer_success':bool(opt.success),'message':str(opt.message),'represented_residual':residual,'source_null_fraction':source_null,'energy_with_volume':E,'rho_eff_min':float(rhoeff.min()),'rho_eff_max':float(rhoeff.max()),'rho_eff_positive_integral':pos,'rho_eff_negative_integral':neg,'minimum_hypothetical_positive_background':max(0.,-float(rhoeff.min()))})
 fields[name]=q;eff[name]=rhoeff
 print(name,'iterations',opt.nit,'residual',residual,flush=True)
sel=(r>=4)&(r<=8)
def centered(q):return q-q[(slice(None),)+center].reshape(3,1,1,1)
baseline=centered(fields['satellite']);incremental=centered(fields['combined']-fields['host']);difference=incremental-baseline
norm=float(np.linalg.norm(baseline[:,sel]));primary=float(np.linalg.norm(difference[:,sel])/norm)
rad=lambda q:sum(qi*xi for qi,xi in zip(q,X))/np.maximum(r,1e-20)
rad_primary=float(np.linalg.norm(rad(difference)[sel])/np.linalg.norm(rad(baseline)[sel]))
linbase=centered(newton['satellite']);lininc=centered(newton['combined']-newton['host'])
check('linear source-subtraction with actual finite host tides',np.linalg.norm((lininc-linbase)[:,sel])/np.linalg.norm(linbase[:,sel]),1e-10)
hq=fields['host'];hc=hq[(slice(None),)+center];ht=centered(hq)
# Actual host-center vector, after solve: control does not alter the frozen physical inputs.
# P annihilates constants exactly up to FFT roundoff; qhost-hcenter retains tidal modes.
check('host-center uniform filtered amplitude',np.max(np.abs(proj(np.broadcast_to(hc.reshape(3,1,1,1),hq.shape)))),1e-9)
jac=np.array([[(hq[i,center[0]+(j==0),center[1]+(j==1),center[2]+(j==2)]-hq[i,center[0]-(j==0),center[1]-(j==1),center[2]-(j==2)])/(2*dx) for j in range(3)] for i in range(3)])
out={'N':N,'box':box,'L':L,'rows':rows,'primary_vector_nonadditivity':primary,'radial_nonadditivity':rad_primary,'primary_gate_tolerance':.05,'finite_host_gate_survives':primary<=.05,'sampled_cells':int(sel.sum()),'host_center_gradient':hc.tolist(),'host_tidal_L2_over_satellite_internal_L2':float(np.linalg.norm(ht[:,sel])/norm),'host_filtered_L2_over_satellite_internal_L2':float(np.linalg.norm(proj(hq)[:,sel])/norm),'host_center_gradient_jacobian':jac.tolist(),'checks':checks,'numerical_checks_pass':all(c['passed'] for c in checks),'runtime_child_seconds':time.monotonic()-starts,'kernel_status':'inverse-designed target-in premise; no independent microphysical derivation','interpretation':'Finite-host nonadditive internal response after subtracting actual host force; signed effective density contrast only.'}
np.savez_compressed(DEST/'fields.npz',satellite=fields['satellite'],host=fields['host'],combined=fields['combined'],rho_eff_satellite=eff['satellite'],rho_eff_host=eff['host'],rho_eff_combined=eff['combined'],sat_source=sat,host_source=host)
(DEST/'results.json').write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2));assert out['numerical_checks_pass']
