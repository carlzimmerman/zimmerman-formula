import sys,json
from pathlib import Path
import numpy as np,torch
from scipy.optimize import minimize
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'redistribution_2026_10_24'))
from redistribute import Capillary,transfer_species,RESERVOIR
from mixed_carrier import Mixed
class Coupled(Capillary):
 def __init__(self,*args,eta=1,**kw):super().__init__(*args,**kw);self.eta=eta
 def energy(self,z,x):
  E=Mixed.energy(self,z,x);mass=RESERVOIR*torch.softmax(z,dim=0);a=torch.sqrt(mass/self.vol);q=torch.sin(torch.pi*x/2)**2
  w=(a[1:]-a[:-1])-self.eta*(a[1:]+a[:-1])/2*(q[1:]-q[:-1])
  return E+.5*(self.L/self.rm)**3*torch.sum(self.rf**2/self.dr*w**2)
 def report(self,v):
  r=super().report(v);r['eta']=self.eta;rad=np.array(r['r']);mass=np.array(r['mass']);edges=[0.]
  for rr in rad:edges.append(2*rr-edges[-1])
  M50=float(np.interp(50**3,np.array(edges)**3,np.r_[0,np.cumsum(mass)]));r['mass50_volume']=M50;r['mass_outside50']=RESERVOIR-M50
  if r['interpolated_crossings_kpc']:
   R=r['interpolated_crossings_kpc'][-1];sel=(rad>15)&(rad<R);r['min_transition_cell_mass']=float(min(mass[sel])) if any(sel) else None
  return r

def solve(m,v,path,maxiter=1800):
 n=m.n;y=np.r_[np.sqrt(v[:n]),v[n:]];count=[0]
 def unpack(y):return np.r_[y[:n]**2,y[n:]]
 def fg(y):
  E,g=m.direct(unpack(y));return E,g*np.r_[2*y[:n],np.ones(n)]
 def report(y):
  a=unpack(y);r=m.report(np.r_[np.log(a[:n]),a[n:]]);E,g=m.direct(a);active=a[:n]>1e-7;mu=g[:n]-np.median(g[:n][active]);mu=np.where((~active)&(mu>0),0,mu);r.update(density_KKT_max=float(max(abs(mu))),mass_constraint_error=float(abs(sum(a[:n])-RESERVOIR)),cap_slack_min=float(min(m.cap(a))),ell_kpc=float(np.sqrt(m.ell2)*m.rm));return r
 def cb(y):
  count[0]+=1
  if count[0]%100==0:
   r=report(y);r['iterations']=count[0];Path(path).write_text(json.dumps(r,indent=2)+'\n')
 cons=[dict(type='eq',fun=lambda y:sum(y[:n]**2)-RESERVOIR,jac=lambda y:np.r_[2*y[:n],np.zeros(n)]),dict(type='ineq',fun=lambda y:m.cap(unpack(y)),jac=lambda y:m.capjac(unpack(y))*np.r_[2*y[:n],np.ones(n)])]
 op=minimize(fg,y,jac=True,method='SLSQP',bounds=[(1e-6,np.sqrt(RESERVOIR))]*n+[(0,1)]*n,constraints=cons,callback=cb,options=dict(ftol=1e-14,maxiter=maxiter));r=report(op.x);r['optimizer']=dict(success=bool(op.success),message=str(op.message),iterations=int(op.nit));Path(path).write_text(json.dumps(r,indent=2)+'\n');return r
