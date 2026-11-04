"""Full scalar/fermion + polarized massive-vector physical-number operator.

Vector channels use positive Gauss quadrature separately on each pair of
linear daughter-energy stencils. The frozen S/F channels use exact exponential
moments. Every represented event conserves the same background energy, obeys
quantum detailed balance, and has nonnegative entropy production.
"""
import sys,math,json
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).parent;OLD=ROOT/'reviews/collision_completion_2026_11_04'
sys.path.insert(0,str(OLD/'cascades'));sys.path.insert(0,str(HERE))
from angular_fast import exact_events_fast
from angular_exact import AngularExact
from rates import channels,matrix_element,VertexTable

class Combined:
 def __init__(self,parts,weights=None):
  self.parts=parts;self.weights=np.ones(len(parts)) if weights is None else np.asarray(weights);first=parts[0]
  for key in ('measure','eta','groups','by','q','W','t','masses','energies','energy'):setattr(self,key,getattr(first,key))
  self.energy_average=self.energy;self.energy_residual=max(p.energy_residual for p in parts);self.local_energy_residual=self.energy_residual;self.omitted_by_parent=sum(w*p.omitted_by_parent for w,p in zip(self.weights,parts));self.included_by_parent=sum(w*p.included_by_parent for w,p in zip(self.weights,parts));self.segment_count=sum(len(p.coefficient) for p in parts)
 def number_rhs(self,f,availability=None):return sum(w*p.number_rhs(f,availability) for w,p in zip(self.weights,self.parts))
 def number_gross(self,f,availability=None):return sum(w*p.number_gross(f,availability) for w,p in zip(self.weights,self.parts))
 def number_jacobian(self,f,availability=None):
  value=csr_matrix((len(self.measure),len(self.measure)))
  for w,p in zip(self.weights,self.parts):value=value+w*p.number_jacobian(f,availability)
  return value.tocsr()

class VectorFactory:
 def __init__(self,path):
  data=json.loads(Path(path).read_text());self.table=VertexTable(data['cases']);self.path=str(path)
 def full_events(self,data,t,q,W,angle_order=2,source=None):return full_events(data,t,q,W,self.table,angle_order,source)
 def averaged_events(self,background,xs,weights,t,q,W,angle_order=2):return averaged_events(background,xs,weights,t,q,W,self.table,angle_order)

def full_events(data,t,q,W,table,angle_order=2,source=None):
 q=np.asarray(q,float);W=np.asarray(W,float);n=len(q);groups=data['groups'];ng=len(groups);source=data.get('current_source') if source is None else source
 if ng!=30:raise ValueError('CC11 full factory expects common30 canonical groups')
 sf=exact_events_fast(data,t,q,W,source=source);sf.eta=np.repeat([1 if g['kind'] in ('S','V') else -1 for g in groups],n)
 mass=np.array([g['mass'] for g in groups]);energy=np.sqrt(mass[:,None]**2+(t*q[None,:])**2);measure=np.repeat([g['degeneracy'] for g in groups],n)*np.tile(W,ng)/(2*math.pi**2)
 if np.max(abs(sf.energy-energy.ravel()))>1e-14:raise ValueError('common SF/vector energies differ')
 record=table.at(data['x']) if hasattr(table,'at') else table;cc=channels(record,groups);zgl,wgl=np.polynomial.legendre.leggauss(angle_order);ind=[];ww=[];coef=[];omitted=np.zeros(ng*n);included=np.zeros(ng*n);vacuum_channels=[]
 for c in cc:
  p,j,k=c['p'],c['j'],c['k'];M,m1,m2=mass[[p,j,k]];ps=math.sqrt(max(0,(M-m1-m2)*(M+m1+m2)*(M-m1+m2)*(M+m1-m2)))/(2*M);beta=2*ps/M;Ep=energy[p];star=(M*M+m1*m1-m2*m2)/(2*M);offset=Ep*star/M;slope=t*q*ps/M
  with np.errstate(divide='ignore',invalid='ignore'):
   z1=(energy[j,None,:]-offset[:,None])/slope[:,None];z2=(energy[k,None,:]-(Ep-offset)[:,None])/(-slope[:,None])
  cuts=np.c_[z1,z2];cuts=np.where((cuts>-1+1e-14)&(cuts<1-1e-14)&np.isfinite(cuts),cuts,np.inf);cuts=np.sort(np.c_[np.full(n,-1.),np.full(n,1.),cuts],axis=1);l=cuts[:,:-1];r=cuts[:,1:];rows,cols=np.where(np.isfinite(r)&(r>l));left=l[rows,cols];right=r[rows,cols];half=(right-left)/2;mid=(left+right)/2
  rr=np.repeat(rows,angle_order);z=(mid[:,None]+half[:,None]*zgl).ravel();weight=(half[:,None]*wgl).ravel();E1=offset[rr]+slope[rr]*z;E2=Ep[rr]-E1
  amps=matrix_element(c,M,m1,m2,t*q[rr],z,groups);vac=measure[p*n+rr]*(M/Ep[rr])*beta/(32*math.pi*M)*amps*weight
  keep=(E1>=energy[j,0]-1e-13)&(E1<=energy[j,-1]+1e-13)&(E2>=energy[k,0]-1e-13)&(E2<=energy[k,-1]+1e-13)
  omitted+=np.bincount(p*n+rr[~keep],weights=vac[~keep],minlength=ng*n);rr=rr[keep];E1=E1[keep];E2=E2[keep];vac=vac[keep]
  def bracket(E,target):
   lo=np.clip(np.searchsorted(E,target)-1,0,n-2);hi=lo+1
   if np.any(E[hi]<=E[lo]):raise ValueError('grid energies not distinct at retained bracket')
   u=(target-E[lo])/(E[hi]-E[lo]);return lo,hi,np.clip(u,0,1)
  jl,jh,fj=bracket(energy[j],E1);kl,kh,fk=bracket(energy[k],E2);ind.append(np.c_[p*n+rr,j*n+jl,j*n+jh,k*n+kl,k*n+kh]);ww.append(np.c_[np.ones(len(rr)),1-fj,fj,1-fk,fk]);coef.append(vac/2);included+=np.bincount(p*n+rr,weights=vac,minlength=ng*n)
  # Independent total rest-width quadrature includes every polarization; no grid cut.
  zz,wz=np.polynomial.legendre.leggauss(32);width=float(beta/(32*math.pi*M)*np.dot(wz,matrix_element(c,M,m1,m2,np.zeros_like(zz),zz,groups)));vacuum_channels.append(dict(c,width=width))
 index=np.concatenate(ind) if ind else np.empty((0,5),int);a=np.concatenate(ww) if ww else np.empty((0,5));coefficient=np.concatenate(coef) if coef else np.empty(0)
 v=AngularExact(index,a,np.zeros_like(a),coefficient,measure,energy.ravel(),sf.eta,groups);v.q=q;v.W=W;v.t=t;v.masses=mass;v.energies=energy;v.omitted_by_parent=omitted;v.included_by_parent=included
 out=Combined([sf,v]);out.x=data['x'];out.channels=vacuum_channels;out.vector_operator=v;out.scalar_fermion_operator=sf;out.angle_order=angle_order;return out

def averaged_events(background,xs,weights,t,q,W,table,angle_order=2):
 weights=np.asarray(weights,float);weights/=weights.sum();parts=[full_events(background.at(float(x)),t,q,W,table,angle_order) for x in xs];out=Combined.__new__(Combined);out.parts=parts;out.weights=weights;out.localops=parts;out.local_events=parts;out.phase_weights=weights;out.xs=np.asarray(xs)
 first=parts[0]
 for key in ('measure','eta','groups','by','q','W','t','masses','energies'):setattr(out,key,getattr(first,key))
 out.energy=sum(w*p.energy for w,p in zip(weights,parts));out.energy_average=out.energy;out.energy_residual=max(p.energy_residual for p in parts);out.local_energy_residual=out.energy_residual;out.omitted_by_parent=sum(w*p.omitted_by_parent for w,p in zip(weights,parts));out.included_by_parent=sum(w*p.included_by_parent for w,p in zip(weights,parts));out.segment_count=sum(p.segment_count for p in parts);return out
