import json
from pathlib import Path
import numpy as np,torch
from scipy.linalg import null_space
from surface_checked import solve
from joint import T,RESERVOIR

def finish(m,v,path,initial_iterations=180,newton_iterations=80):
 assert initial_iterations==0, '3n solver supports Newton initialization only'
 path=Path(path);r=solve(m,v,path.with_name(path.stem+'_initial.json'),maxiter=initial_iterations) if initial_iterations else m.report(np.r_[np.log(v[:m.n]),v[m.n:]]);initial=r.get('optimizer',{'skipped':True});n=m.n;size=len(v);y=np.r_[np.sqrt(r['mass']),r['v'][n:]];trace=[]
 def unpack(y):
  mass=RESERVOIR*y[:n]**2/sum(y[:n]**2);return np.r_[mass,y[n:]]
 def report(y):
  v=unpack(y);r=m.report(np.r_[np.log(v[:n]),v[n:]]);E,g=m.direct(v);active=v[:n]>1e-7;mu=g[:n]-np.median(g[:n][active]);mu=np.where((~active)&(mu>0),0,mu);r.update(density_KKT_max=float(max(abs(mu))),mass_constraint_error=float(abs(sum(v[:n])-RESERVOIR)),cap_slack_min=float(min(m.cap(v))),ell_kpc=float(np.sqrt(m.ell2)*m.rm));return r
 for iteration in range(newton_iterations):
  v=unpack(y);rr=report(y)
  if rr['density_KKT_max']<1e-6 and rr['gradient_max']<1e-8:break
  _,physical_g=m.direct(v);lam=np.median(physical_g[:n][v[:n]>1e-7]);im=np.where((v[:n]>4e-12)|(physical_g[:n]<lam-1e-8))[0];gx=physical_g[n:];ix=np.where(((y[n:]>1e-12)|(gx<0))&((y[n:]<1-1e-12)|(gx>0)))[0]+n;P0=null_space(y[im][None,:]);P=np.zeros((size,len(im)-1));P[im]=P0;Z=np.c_[P,np.eye(size)[:,ix]]
  def energy(aa):return m.energy(torch.log(aa[:n]**2),aa[n:])
  aa=T(y).requires_grad_(True);E=energy(aa);g=torch.autograd.grad(E,aa)[0].detach().numpy();H=torch.autograd.functional.hessian(energy,aa).detach().numpy();HH=Z.T@H@Z;gg=Z.T@g;scale=1/np.sqrt(np.maximum(abs(np.diag(HH)),1e-8));HS=scale[:,None]*HH*scale[None,:];mine=float(np.linalg.eigvalsh(HS)[0]);shift=(-mine+.01) if mine<=0 else 0;d=-Z@(scale*np.linalg.solve(HS+shift*np.eye(len(gg)),scale*gg));d[:n][(v[:n]<=4e-12)&(d[:n]<0)]=0;d[n:][(y[n:]<=1e-8)&(d[n:]<0)]=0;d[n:][(y[n:]>=1-1e-8)&(d[n:]>0)]=0;alpha=1.
  lo=np.r_[np.full(n,1e-6),np.zeros(size-n)];hi=np.r_[np.full(n,np.inf),np.ones(size-n)]
  neg=d<0;pos=d>0
  if any(neg):alpha=min(alpha,.95*float(min((y[neg]-lo[neg])/(-d[neg]))))
  if any(pos):alpha=min(alpha,.95*float(min((hi[pos]-y[pos])/d[pos])))
  accepted=False
  for attempt in range(30):
   candidate=y+alpha*d;candidate[:n]*=np.sqrt(RESERVOIR/sum(candidate[:n]**2));vv=unpack(candidate)
   if min(m.cap(vv))>0:
    EE=float(energy(T(candidate)))
    if EE<=float(E)+1e-4*alpha*float(g@d)+1e-14:accepted=True;break
   alpha*=.5
  trace.append(dict(iteration=iteration,min_scaled_H=mine,damping=shift,step=alpha,accepted=accepted,density_KKT=rr['density_KKT_max'],projected_gradient=rr['gradient_max'],energy_before=float(E)))
  if not accepted or alpha<1e-12:break
  y=candidate;rr=report(y);rr.update(status='newton_checkpoint',newton_trace=trace,initial_optimizer=initial);path.write_text(json.dumps(rr,indent=2)+'\n')
 r=report(y);r.update(initial_optimizer=initial,newton_trace=trace,optimizer=dict(success=bool(r['density_KKT_max']<1e-5 and r['gradient_max']<1e-7),message='Force-based Newton finish after bounded SLSQP; inspect residuals and active sets',iterations=len(trace)));path.write_text(json.dumps(r,indent=2)+'\n');return r
