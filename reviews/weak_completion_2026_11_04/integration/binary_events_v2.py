"""Positive finite-projection 2<->2 number operator, chunked and cancellation-aware.

Index=(in1,in2,out1lo,out1hi,out2lo,out2hi). Incoming weights are one,
each daughter's two weights sum to one. Caller supplies the complete physical
coefficient including quadrature, densities and all pair/orientation factors.
Interior Jacobians above the 1e-280 number-coordinate denominator budget are analytic.
Sub-budget cells use that declared one-sided Jacobian regularization; the RHS
and accepted physical occupations are unchanged and are never clipped. Fractional powers at an exactly empty
outgoing cell have only a declared one-sided numerical regularization.
"""
import numpy as np
from scipy.sparse import coo_matrix,csr_matrix,diags

class _Block:
 def __init__(self,index,weights,coefficient,size):
  self.index=index;self.w=weights;self.c=coefficient;nb=len(coefficient);cols=np.repeat(np.arange(nb),6)
  vals=[];inds=[]
  for pin,lo,hi in ((0,2,3),(1,4,5)):
   p=index[:,pin];l=index[:,lo];h=index[:,hi];wl=weights[:,lo];wh=weights[:,hi]
   v=np.c_[-np.ones(nb),wl,wh];a=l==p;b=h==p
   v[a,0]=-wh[a];v[a,1]=0.;v[b,0]=-wl[b];v[b,2]=0.;v[a&b]=0.
   vals.append(v);inds.append(np.c_[p,l,h])
  val=np.concatenate(vals,axis=1);ind=np.concatenate(inds,axis=1)
  self.S=coo_matrix((val.ravel(),(ind.ravel(),cols)),shape=(size,nb)).tocsr();self.S.eliminate_zeros();self.ST=self.S.T.tocsr();self.absS=abs(self.S)
 def products(self,f,av):
  v=f[self.index];a=av[self.index]
  with np.errstate(divide='ignore',invalid='ignore'):
   lf=np.log(v);la=np.log(a);wf=self.w[:,2:]
   childA=np.sum(np.where(wf>0,wf*la[:,2:],0.),axis=1);childF=np.sum(np.where(wf>0,wf*lf[:,2:],0.),axis=1)
   logF=lf[:,0]+lf[:,1]+childA;logR=la[:,0]+la[:,1]+childF
   odds=np.log(f)-np.log(av)
  bad=~np.isfinite(odds);aff=-np.asarray(self.ST@np.where(bad,0.,odds)).ravel();rows=np.asarray(abs(self.ST)@bad.astype(float)).ravel()>0
  with np.errstate(invalid='ignore'):aff[rows]=(logF-logR)[rows]
  F=np.exp(logF);R=np.exp(logR);net=np.zeros_like(F);pos=aff>=0;neg=aff<0
  net[pos]=F[pos]*(-np.expm1(-aff[pos]));net[neg]=R[neg]*np.expm1(aff[neg])
  null=(F==0)&(R==0);net[null]=0.;aff[null]=0.
  if not np.all(np.isfinite(net)):raise FloatingPointError('nonfinite binary flux')
  return F,R,net,aff,v,a,childA,childF
 def jacobian(self,f,av,measure,eta):
  F,R,net,aff,v,a,ca,cf=self.products(f,av);nb=len(F);size=len(f);tiny=1e-280
  if np.any(v<=0) or np.any(a<=0):
   D=np.empty_like(v)
   for j in (0,1):
    k=1-j;df=np.exp(np.log(np.maximum(v[:,k],tiny))+ca);dr=eta[self.index[:,j]]*R/np.maximum(a[:,j],tiny)
    z=a[:,j]<=0
    if np.any(z):dr[z]=eta[self.index[z,j]]*np.exp(np.log(np.maximum(a[z,k],tiny))+cf[z])
    D[:,j]=df-dr
   D[:,2:]=self.w[:,2:]*(F[:,None]*eta[self.index[:,2:]]/np.maximum(a[:,2:],tiny)-R[:,None]/np.maximum(v[:,2:],tiny))
   M=coo_matrix(((self.c[:,None]*D/measure[self.index]).ravel(),(np.repeat(np.arange(nb),6),self.index.ravel())),shape=(nb,size)).tocsr()
   return self.S@M
  # dFlux=Flux*dlogF - R*nu*dlog(f/A), avoiding F-R Jacobian cancellation.
  LF=np.empty_like(v);LF[:,:2]=1/np.maximum(measure[self.index[:,:2]]*v[:,:2],tiny);LF[:,2:]=self.w[:,2:]*eta[self.index[:,2:]]/np.maximum(measure[self.index[:,2:]]*a[:,2:],tiny)
  L=coo_matrix(((self.c[:,None]*net[:,None]*LF).ravel(),(np.repeat(np.arange(nb),6),self.index.ravel())),shape=(nb,size)).tocsr()
  metric=self.S@diags(self.c*R)@self.ST
  return self.S@L-metric@diags(1/np.maximum(measure*f*av,tiny))

class BinaryEvents:
 def __init__(self,index,weights,coefficient,measure,energy,eta,groups=None,chunk=50000):
  self.index=np.asarray(index,int).reshape(-1,6);self.weights=np.asarray(weights,float).reshape(-1,6);self.coefficient=np.asarray(coefficient,float);self.measure=np.asarray(measure,float);self.energy=np.asarray(energy,float);self.energy_average=self.energy;self.eta=np.asarray(eta,float);self.groups=groups or [];self.by={g['id']:i for i,g in enumerate(self.groups)}
  if len(self.index)!=len(self.coefficient) or np.any(self.coefficient<0) or not np.all(np.isfinite(self.coefficient)):raise ValueError('invalid binary coefficients')
  if np.any(self.weights<0) or np.max(abs(self.weights[:,:2]-1),initial=0)>1e-14 or np.max(abs(self.weights[:,2:4].sum(axis=1)-1),initial=0)>5e-13 or np.max(abs(self.weights[:,4:6].sum(axis=1)-1),initial=0)>5e-13:raise ValueError('invalid binary weights')
  if np.any(self.measure<=0):raise ValueError('nonpositive number measure')
  self.blocks=[_Block(self.index[i:i+chunk],self.weights[i:i+chunk],self.coefficient[i:i+chunk],len(self.measure)) for i in range(0,len(self.coefficient),chunk)]
  self.number_residual=max([float(max(abs(b.ST@np.ones(len(self.measure))),default=0.)) for b in self.blocks]+[0.]);self.energy_residual=max([float(max(abs(b.ST@self.energy),default=0.)) for b in self.blocks]+[0.]);self.local_energy_residual=self.energy_residual
 def arrays(self,f,availability):
  f=np.asarray(f,float);a=1+self.eta*f if availability is None else np.asarray(availability,float)
  if np.any(f<0) or np.any(a<0) or not np.all(np.isfinite(f)) or not np.all(np.isfinite(a)):raise ValueError('invalid binary occupations/availability')
  return f,a
 def number_rhs(self,f,availability=None):
  f,a=self.arrays(f,availability);out=np.zeros(len(f))
  for b in self.blocks:out+=b.S@(b.c*b.products(f,a)[2])
  return out
 def number_gross(self,f,availability=None):
  f,a=self.arrays(f,availability);out=np.zeros(len(f))
  for b in self.blocks:
   F,R,*_=b.products(f,a);out+=b.absS@(b.c*(F+R))
  return np.maximum(out,0.)
 def number_jacobian(self,f,availability=None):
  f,a=self.arrays(f,availability);out=csr_matrix((len(f),len(f)))
  for b in self.blocks:out=out+b.jacobian(f,a,self.measure,self.eta)
  return out.tocsr()
 def entropy_production(self,f,availability=None):
  f,a=self.arrays(f,availability);value=0.
  for b in self.blocks:
   F,R,net,aff,*_=b.products(f,a);value+=float(np.dot(b.c*net,aff))
  return value
