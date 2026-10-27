"""Re-minimize the inherited static energy with the finite mediator retained."""
import argparse,json,time
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from matched import Matched

ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
rows=[];states={};start=time.monotonic()
for length in [1e-6,.001,.01,.1]:
 obj=Matched(length_kpc=length);m=obj.m;old=obj.reference;mass0=np.sum(abs(old['a'])**2,axis=0);total=np.sum(mass0)
 y0=np.r_[np.log(mass0),np.arctan2(abs(old['a'][0]),abs(old['a'][1])),old['alpha']]
 def decode(y):
  z=y[:m.n];ex=np.exp(z-np.max(z));mass=total*ex/np.sum(ex);th=y[m.n:2*m.n];xx=y[2*m.n:]
  aa=np.sqrt(mass)[None,:]*np.array([np.sin(th),np.cos(th)])
  return aa.astype(complex),xx,mass,th
 def fun(y):
  aa,xx,mass,th=decode(y);state=obj.static(aa,xx);E=obj.energy(state);ga,gx,*_=obj.gradient(state)
  mu=np.sum(np.real(np.conj(ga)*aa),axis=0)/mass
  gz=mass*(mu-np.sum(mass*mu)/total)
  gt=2*np.sqrt(mass)*(ga[0].real*np.cos(th)-ga[1].real*np.sin(th))
  return E,np.r_[gz,gt,gx]
 E0,g0=fun(y0)
 # Fixed bounds/iteration budget; optimizer loss is not physical cooling.
 res=minimize(fun,y0,jac=True,method='L-BFGS-B',bounds=[(None,None)]*m.n+[(0,np.pi/2)]*(2*m.n),
              options={'maxiter':1200,'ftol':2e-15,'gtol':1e-9,'maxls':30,'maxcor':30})
 aa,xx,mass,th=decode(res.x);state=obj.static(aa,xx);E,grad=fun(res.x)
 projected=grad.copy()
 for j in range(m.n,3*m.n):
  if (res.x[j]<1e-10 and grad[j]>0) or (res.x[j]>np.pi/2-1e-10 and grad[j]<0):projected[j]=0
 m.energy_chi=np.zeros(len(m.wr));diag=m.diagnostics(aa,xx,np.zeros(len(m.wr)),np.zeros(len(m.wr)))
 cap=float(np.max(m.enclosed(abs(aa[0])**2)))
 rows.append({'length_kpc':length,'initial_energy':E0,'final_energy':E,'iterations':res.nit,
              'optimizer_success':bool(res.success),'optimizer_message':str(res.message),'projected_gradient_max':float(max(abs(projected))),
              'initial_gradient_max':float(max(abs(g0))),'mass_error':float(np.sum(mass)-total),'maximum_acceleration_ratio':cap,
              'diagnostics':diag,'alpha':obj.alpha,'M':obj.M,'h':obj.h,'lambda':obj.lam})
 states[f'a_{length}']=aa;states[f'carrier_{length}']=xx;states[f's_{length}']=state[5]
 assert np.isfinite(E) and cap<.9997 and abs(np.sum(mass)-total)<1e-11
 print({'length':length,'energy':E,'pg':max(abs(projected)),'success':res.success,'law':diag.get('law_error_percent')},flush=True)
np.savez_compressed(Path(args.output).with_name('states.npz'),**states)
Path(args.output).write_text(json.dumps({'rows':rows,'wall_seconds':time.monotonic()-start,
 'interpretation':'Static constrained optimization only; convergence measured by reported gradient, not optimizer flag. Finite inherited grid, no time history or continuum certificate.'},indent=2)+'\n')
