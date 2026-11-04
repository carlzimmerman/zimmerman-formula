"""Vectorized exact-angle builder; frozen angular_exact.py supplies the algebra.

All channel x parent-node cuts are sorted as a matrix. No per-segment Python
loop is used. The averaged backend keeps phase operators without concatenating
and duplicating their arrays/scatters, reducing peak memory for Jacobians.
"""
import math
import numpy as np
from scipy.sparse import csr_matrix
from angular_exact import AngularExact
from reaction import full_events

def exact_events_fast(data,t,q,W,source=None,signed=False):
 base=full_events(data,t,q,W,angles=1,signed=signed,source=source);q=np.asarray(q);n=len(q);channels=[]
 for c in base.channels:
  p=base.by[c['parent']];j,k=[base.by[d] for d in c['daughters']];M,m1,m2=base.masses[[p,j,k]]
  if c['width']>0 and M>m1+m2+1e-14:
   star=(M*M+m1*m1-m2*m2)/(2*M);pstar=math.sqrt(max(0,(M-m1-m2)*(M+m1+m2)*(M-m1+m2)*(M+m1-m2)))/(2*M);channels.append((p,j,k,M,star,pstar,c['width']))
 omitted=np.zeros(len(base.measure));included=np.zeros(len(base.measure))
 if channels:
  values=np.array(channels);p=np.repeat(values[:,0].astype(int),n);j=np.repeat(values[:,1].astype(int),n);k=np.repeat(values[:,2].astype(int),n);M=np.repeat(values[:,3],n);star=np.repeat(values[:,4],n);pstar=np.repeat(values[:,5],n);width=np.repeat(values[:,6],n);i=np.tile(np.arange(n),len(channels));parent=p*n+i;Ep=base.energies[p,i];e10=Ep*star/M;slope=t*q[i]*pstar/M;e20=Ep-e10;rate=base.measure[parent]*width*M/Ep/2
  with np.errstate(divide='ignore',invalid='ignore'):
   z1=(base.energies[j]-e10[:,None])/slope[:,None];z2=(base.energies[k]-e20[:,None])/(-slope[:,None])
  z=np.c_[z1,z2];z=np.where((z>-1+1e-14)&(z<1-1e-14)&np.isfinite(z),z,np.inf);cuts=np.sort(np.c_[np.full(len(parent),-1.),np.full(len(parent),1.),z],axis=1);left=cuts[:,:-1];right=cuts[:,1:];valid=np.isfinite(right)&(right>left);rows,columns=np.where(valid);left=left[rows,columns];right=right[rows,columns];mid=(left+right)/2;half=(right-left)/2;target1=e10[rows]+slope[rows]*mid;target2=Ep[rows]-target1;coefficient=rate[rows]*half;jj=j[rows];kk=k[rows]
  support=(target1>=base.energies[jj,0]-1e-13)&(target1<=base.energies[jj,-1]+1e-13)&(target2>=base.energies[kk,0]-1e-13)&(target2<=base.energies[kk,-1]+1e-13);omitted=np.bincount(parent[rows[~support]],weights=2*coefficient[~support],minlength=len(base.measure));rows=rows[support];half=half[support];target1=target1[support];target2=target2[support];coefficient=coefficient[support];jj=jj[support];kk=kk[support]
  def brackets(group,target):
   low=np.empty(len(group),int);high=np.empty(len(group),int)
   for gid in np.unique(group):
    select=group==gid;E=base.energies[gid];lo=np.clip(np.searchsorted(E,target[select])-1,0,n-2);hi=lo+1
    bad=E[hi]<=E[lo]
    if np.any(bad):
     hh=np.searchsorted(E,E[lo[bad]],side='right');end=hh==n;hh=np.minimum(hh,n-1);ll=lo[bad].copy();ll[end]=np.searchsorted(E,E[-1],side='left')-1
     if np.any(ll<0):raise ValueError('energy grid needs two distinct energies')
     lo[bad]=ll;hi[bad]=hh
    low[select]=lo;high[select]=hi
   return low,high
  jl,jh=brackets(jj,target1);kl,kh=brackets(kk,target2);delta1=base.energies[jj,jh]-base.energies[jj,jl];delta2=base.energies[kk,kh]-base.energies[kk,kl];fj=(target1-base.energies[jj,jl])/delta1;bj=slope[rows]*half/delta1;fk=(target2-base.energies[kk,kl])/delta2;bk=-slope[rows]*half/delta2;a=np.c_[np.ones(len(rows)),1-fj,fj,1-fk,fk];b=np.c_[np.zeros(len(rows)),-bj,bj,-bk,bk];leftw=np.clip(a-b,0,1);rightw=np.clip(a+b,0,1);a=(leftw+rightw)/2;b=(rightw-leftw)/2;index=np.c_[parent[rows],jj*n+jl,jj*n+jh,kk*n+kl,kk*n+kh];included=np.bincount(parent[rows],weights=2*coefficient,minlength=len(base.measure))
 else:index=np.empty((0,5),int);a=np.empty((0,5));b=np.empty((0,5));coefficient=np.empty(0)
 out=AngularExact(index,a,b,coefficient,base.measure,base.energy,base.eta,base.groups);out.by=base.by;out.q=q;out.W=np.asarray(W);out.t=t;out.x=data['x'];out.masses=base.masses;out.energies=base.energies;out.omitted_by_parent=omitted;out.included_by_parent=included;out.local_energy_residual=out.energy_residual;out.segment_count=len(coefficient)
 return out

class AveragedExact:
 """Protocol-compatible memory-lean weighted sum of exact phase backends."""
 def __init__(self,parts,weights,xs,t,q,W):
  self.local_events=parts;self.localops=parts;self.phase_weights=np.asarray(weights,float);self.xs=np.asarray(xs);first=parts[0];self.measure=first.measure;self.eta=first.eta;self.groups=first.groups;self.by=first.by;self.q=np.asarray(q);self.W=np.asarray(W);self.t=t;self.energy_average=sum(w*p.energy for w,p in zip(weights,parts));self.energy=self.energy_average;self.local_energy_residual=max(p.energy_residual for p in parts);self.omitted_by_parent=sum(w*p.omitted_by_parent for w,p in zip(weights,parts));self.included_by_parent=sum(w*p.included_by_parent for w,p in zip(weights,parts));self.segment_count=sum(len(p.coefficient) for p in parts)
 def number_rhs(self,f,availability=None):
  value=np.zeros(len(self.measure))
  for w,p in zip(self.phase_weights,self.local_events):value+=w*p.number_rhs(f,availability)
  return value
 def number_gross(self,f,availability=None):
  value=np.zeros(len(self.measure))
  for w,p in zip(self.phase_weights,self.local_events):value+=w*p.number_gross(f,availability)
  return value
 def number_jacobian(self,f,availability=None):
  value=csr_matrix((len(self.measure),len(self.measure)))
  for w,p in zip(self.phase_weights,self.local_events):value=value+w*p.number_jacobian(f,availability)
  return value.tocsr()

def averaged_exact_fast(background,xs,weights,t,q,W):
 weights=np.asarray(weights,float);weights=weights/weights.sum();parts=[]
 for x in xs:
  d=background.at(float(x));parts.append(exact_events_fast(d,t,q,W,source=d['current_source']))
 return AveragedExact(parts,weights,xs,t,q,W)
