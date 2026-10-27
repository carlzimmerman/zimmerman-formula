"""Prepare the new exact complex-edge static benchmark, not a cooling run."""
import argparse,json,time
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from live import Live
from initial import initial

def prepare():
 m=Live();a,x,ch,pi,meta=initial(m,'prepared');mass=np.sum(abs(a)**2,axis=0);theta=np.arctan2(abs(a[0]),abs(a[1]));v=np.r_[np.log(np.maximum(mass,1e-300)),theta];last=x.copy();maxres=0
 def fg(v):
  nonlocal last,maxres
  z=v[:m.n];mass=np.exp(z-max(z));mass*=m.M/sum(mass);th=v[m.n:];a=np.array([np.sqrt(mass)*np.sin(th),np.sqrt(mass)*np.cos(th)],complex);last,res,it=m.minimize_alpha(a,ch,last,maxit=100);maxres=max(maxres,res);E,mu=m.pot(a,last,True)
  ka=m.kd*a;ka[:,:-1]+=m.ko*a[:,1:];ka[:,1:]+=m.ko*a[:,:-1];grad=2*np.real(mu*a+ka+m.J*m.alignment(a,last,ch));mum=np.sum(grad*np.real(a),axis=0)/(2*np.maximum(mass,1e-300));gz=mass*(mum-(mass@mum)/m.M);gth=np.sqrt(mass)*(grad[0]*np.cos(th)-grad[1]*np.sin(th));return m.energy(a,last,ch,pi),np.r_[gz,gth]
 E0=fg(v)[0];start=time.monotonic();opt=minimize(fg,v,jac=True,method='L-BFGS-B',bounds=[(-700,50)]*m.n+[(0,np.pi/2)]*m.n,options={'maxiter':3000,'gtol':1e-10,'ftol':1e-15,'maxls':30,'maxcor':30});E,g=fg(opt.x);z=opt.x[:m.n];mass=np.exp(z-max(z));mass*=m.M/sum(mass);th=opt.x[m.n:];a=np.array([np.sqrt(mass)*np.sin(th),np.sqrt(mass)*np.cos(th)],complex);return m,a,last,ch,pi,{'optimizer_success':bool(opt.success),'message':str(opt.message),'iterations':int(opt.nit),'gradient_max':float(max(abs(g))),'max_carrier_residual':maxres,'initial_energy':E0,'energy':E,'runtime_seconds':time.monotonic()-start,'diagnostics':m.diagnostics(a,last,ch,pi)}

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);arg=ap.parse_args();m,a,x,ch,pi,res=prepare();p=Path(arg.output).with_name('state.npz');np.savez_compressed(p,a=a,alpha=x,chi=ch,pi=pi);res['state_file']=str(p);Path(arg.output).write_text(json.dumps(res,indent=2)+'\n');print(res,flush=True)
