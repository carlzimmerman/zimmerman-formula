"""Separate finite wave-current Pz and absorber ledger; not a translation invariant discretization."""
import json,numpy as np
from tracking import harmonics
class Tracker:
 def __init__(self,ang,r,w,eta):
  self.r=r;self.w=w;self.eta=eta;mu,ph=np.meshgrid(ang.field.mu,np.arange(ang.field.nphi)*np.pi/ang.field.nphi,indexing='ij');unit=np.c_[(np.sqrt(1-mu*mu)*np.cos(ph)).ravel(),(np.sqrt(1-mu*mu)*np.sin(ph)).ravel(),mu.ravel()];aw=np.repeat(ang.field.w,ang.field.nphi)*2*np.pi/ang.field.nphi;_,mu,Y,dY,*_=harmonics(ang.field.lm,unit);self.Z=Y.conj().T@((aw*mu)[:,None]*Y);self.D=Y.conj().T@((-aw*np.sqrt(1-mu*mu))[:,None]*dY);self.rows=[];self.removed=0.
 def Pz(self,v):
  q=v/(np.sqrt(self.w)*self.r)[:,None];dq=np.gradient(q,self.r,axis=0,edge_order=2);terms=np.sum((q.conj()@self.Z)*dq,axis=1)+np.sum((q.conj()@self.D)*q,axis=1)/self.r;return float(self.eta*np.imag(np.sum(self.w*self.r*self.r*terms)))
 def before_sink(self,v):self.prev=self.Pz(v)
 def after_sink(self,v):self.removed+=self.prev-self.Pz(v)
 def record(self,t,v):
  p=self.Pz(v)
  if not self.rows:self.initial=p
  self.rows.append(dict(t=t,Pz_code=p,sink_Pz_code=self.removed,remaining_plus_sink_minus_initial_code=p+self.removed-self.initial))
 def save(self,path):open(str(path)+'_momentum.json','w').write(json.dumps(dict(scope='finite wave-current Pz using radial gradient; missing translational symmetry can leave a non-absorber residual; no external source',history=self.rows),indent=2)+'\n')
