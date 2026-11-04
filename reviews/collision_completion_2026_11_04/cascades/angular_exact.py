"""Exact angular moments of the finite entropy-projected quantum 1<->2 operator.

Each daughter-energy stencil interval has affine weights a+b*u, -1<u<1.
Forward and reverse products are exponentials of affine functions of u.
Analytic moments integrate the number RHS and its Jacobian without global
angle quadrature. This is exact for the declared finite momentum projection,
not the continuum momentum collision integral.
"""
import math
import numpy as np
from scipy.sparse import coo_matrix
from reaction import full_events

SIGNS=np.array([-1.,1.,1.,1.,1.])

def exponential_moments(log_minus,log_plus):
 """Return integral exp(A+B*u)*(1,u,u²) du on[-1,1], from endpoint logs.

 Endpoint logs avoid cancellation in A+abs(B) when one endpoint is suppressed
 by an extremely small Pauli hole. A zero factor throughout the open segment
 gives zero moments; endpoint-only nonzero values have zero measure.
 """
 lm=np.asarray(log_minus,float);lp=np.asarray(log_plus,float);shape=lm.shape;lm=lm.ravel();lp=lp.ravel()
 ans=np.zeros((3,len(lm)));valid=np.isfinite(lm)&np.isfinite(lp)
 if not np.any(valid):return ans.reshape((3,)+shape)
 left=lm[valid];right=lp[valid];B=(right-left)/2;x=abs(B);small=x<.1;v=np.empty((3,len(x)))
 if np.any(small):
  z=B[small];z2=z*z;factor=2*np.exp((left[small]+right[small])/2)
  v[0,small]=factor*(1+z2/6+z2*z2/120+z2**3/5040+z2**4/362880)
  v[1,small]=factor*z*(1/3+z2/30+z2*z2/840+z2**3/45360+z2**4/3991680)
  v[2,small]=factor*(1/3+z2/10+z2*z2/168+z2**3/6480+z2**4/443520)
 if np.any(~small):
  z=x[~small];peak=np.maximum(left[~small],right[~small]);I0=np.exp(peak)*(-np.expm1(-2*z))/z
  tail=np.zeros(len(z));ok=z<350;tail[ok]=2/np.expm1(2*z[ok]);mean=1+tail-1/z
  v[0,~small]=I0;v[1,~small]=I0*np.sign(B[~small])*mean;v[2,~small]=I0*(1-2*mean/z)
 ans[:,valid]=v
 return ans.reshape((3,)+shape)

class AngularExact:
 """Number RHS/Jacobian in Y=measure*f coordinates; holes may be independent.

 `number_rhs(f,availability=None)` and `number_jacobian(f,availability=None)`
 accept a separately retained 1-f array, so sub-ulp holes are not reconstructed
 by subtraction. At exact zero child factors the fractional projection is
 non-Lipschitz; the Jacobian's 1e-280 denominator is a numerical one-sided
 regularization there. Interior positive-state Jacobians are analytic.
 """
 def __init__(self,index,a,b,coefficient,measure,energy,eta,groups=None):
  self.index=np.asarray(index,int).reshape(-1,5);self.a=np.asarray(a,float).reshape(-1,5);self.b=np.asarray(b,float).reshape(-1,5);self.coefficient=np.asarray(coefficient,float);self.measure=np.asarray(measure,float);self.energy=np.asarray(energy,float);self.energy_average=self.energy;self.eta=np.asarray(eta,float);self.groups=groups or [];self.by={g['id']:i for i,g in enumerate(self.groups)};r=len(self.coefficient);m=len(self.measure);cols=np.repeat(np.arange(r),5)
  self.Sa=coo_matrix(((self.a*SIGNS).ravel(),(self.index.ravel(),cols)),shape=(m,r)).tocsr();self.Sb=coo_matrix(((self.b*SIGNS).ravel(),(self.index.ravel(),cols)),shape=(m,r)).tocsr()
  self.energy_residual=float(max(np.max(abs(np.sum(self.a*SIGNS*self.energy[self.index],axis=1)),initial=0.),np.max(abs(np.sum(self.b*SIGNS*self.energy[self.index],axis=1)),initial=0.)))
 def _logs(self,f,availability=None):
  f=np.asarray(f,float);av=1+self.eta*f if availability is None else np.asarray(availability,float)
  if np.any(f<0) or np.any(av<0):raise ValueError('negative occupation or availability')
  vals=f[self.index];avail=av[self.index]
  with np.errstate(divide='ignore',invalid='ignore'):
   lf=np.log(vals);la=np.log(avail);wm=self.a[:,1:]-self.b[:,1:];wp=self.a[:,1:]+self.b[:,1:]
   def weighted(w,l):return np.sum(np.where(w>0,w*l,0.),axis=1)
   fm=weighted(wm,la[:,1:]);fp=weighted(wp,la[:,1:]);rm=weighted(wm,lf[:,1:]);rp=weighted(wp,lf[:,1:])
  F=exponential_moments(lf[:,0]+fm,lf[:,0]+fp);R=exponential_moments(la[:,0]+rm,la[:,0]+rp)
  return F,R,vals,avail,(fm,fp,rm,rp)
 def number_rhs(self,f,availability=None):
  F,R,*_=self._logs(f,availability)
  return np.asarray(self.Sa@(self.coefficient*(F[0]-R[0]))+self.Sb@(self.coefficient*(F[1]-R[1]))).ravel()
 def number_gross(self,f,availability=None):
  """Integrated absolute-stoichiometry forward+reverse measure per node."""
  F,R,*_=self._logs(f,availability)
  # Parent b=0; all daughters have positive stoichiometric sign. Therefore
  # abs(Sa) contains a while Sb already contains the unsigned b coefficients.
  value=np.asarray(abs(self.Sa)@(self.coefficient*(F[0]+R[0]))+self.Sb@(self.coefficient*(F[1]+R[1]))).ravel()
  return np.maximum(value,0.)
 def number_jacobian(self,f,availability=None):
  F,R,v,av,childlogs=self._logs(f,availability);eta=self.eta[self.index];meas=self.measure[self.index];tiny=1e-280
  df=np.empty_like(v);dr=np.empty_like(v);df[:,0]=1/(meas[:,0]*np.maximum(v[:,0],tiny));dr[:,0]=eta[:,0]/(meas[:,0]*np.maximum(av[:,0],tiny));df[:,1:]=eta[:,1:]/(meas[:,1:]*np.maximum(av[:,1:],tiny));dr[:,1:]=1/(meas[:,1:]*np.maximum(v[:,1:],tiny))
  D0=(self.a*F[0,:,None]+self.b*F[1,:,None])*df-(self.a*R[0,:,None]+self.b*R[1,:,None])*dr
  D1=(self.a*F[1,:,None]+self.b*F[2,:,None])*df-(self.a*R[1,:,None]+self.b*R[2,:,None])*dr
  # The parent derivative has a finite empty-parent limit, unlike fractional
  # child factors. Evaluate that limit without a 0/0 division.
  empty=v[:,0]<tiny;noavail=av[:,0]<tiny
  if np.any(empty):
   C=exponential_moments(childlogs[0][empty],childlogs[1][empty]);D0[empty,0]=C[0]/meas[empty,0]-(R[0,empty]*dr[empty,0]);D1[empty,0]=C[1]/meas[empty,0]-(R[1,empty]*dr[empty,0])
  if np.any(noavail):
   C=exponential_moments(childlogs[2][noavail],childlogs[3][noavail]);D0[noavail,0]=F[0,noavail]*df[noavail,0]-eta[noavail,0]*C[0]/meas[noavail,0];D1[noavail,0]=F[1,noavail]*df[noavail,0]-eta[noavail,0]*C[1]/meas[noavail,0]
  rows=np.repeat(np.arange(len(self.coefficient)),5);shape=(len(self.coefficient),len(self.measure));M0=coo_matrix(((self.coefficient[:,None]*D0).ravel(),(rows,self.index.ravel())),shape=shape).tocsr();M1=coo_matrix(((self.coefficient[:,None]*D1).ravel(),(rows,self.index.ravel())),shape=shape).tocsr()
  return (self.Sa@M0+self.Sb@M1).tocsr()
 def audit(self,f,availability=None):
  f=np.asarray(f);av=1+self.eta*f if availability is None else np.asarray(availability);F,R,*_=self._logs(f,av);rhs=self.number_rhs(f,av);scale=float(sum(self.coefficient*(F[0]+R[0])))
  with np.errstate(divide='ignore',invalid='ignore'):odds=np.log(f/av)
  return dict(segments=len(self.coefficient),energy_residual=self.energy_residual,energy_rhs_relative=float(abs(self.energy@rhs)/max(scale*max(self.energy),1e-300)),detailed_balance_RHS_relative=float(sum(abs(rhs))/max(scale,1e-300)),entropy_production=float(-odds@rhs),forward_reverse_integral_scale=scale)

def exact_events(data,t,q,W,source=None,signed=False):
 base=full_events(data,t,q,W,angles=1,signed=signed,source=source);q=np.asarray(q);n=len(q);index=[];aa=[];bb=[];coefficient=[];omitted=np.zeros(len(base.measure));included=np.zeros(len(base.measure))
 def bracket(E,target):
  lo=int(np.clip(np.searchsorted(E,target)-1,0,n-2));hi=lo+1
  while hi<n and E[hi]<=E[lo]:hi+=1
  if hi==n:
   hi=n-1;lo=hi-1
   while lo>=0 and E[lo]>=E[hi]:lo-=1
  if lo<0 or E[hi]<=E[lo]:raise ValueError('energy grid needs at least two distinct energies')
  return lo,hi
 for c in base.channels:
  p=base.by[c['parent']];j,k=[base.by[d] for d in c['daughters']];M,m1,m2=base.masses[[p,j,k]]
  if c['width']<=0 or M<=m1+m2+1e-14:continue
  star=(M*M+m1*m1-m2*m2)/(2*M);pstar=math.sqrt(max(0,(M-m1-m2)*(M+m1+m2)*(M-m1+m2)*(M+m1-m2)))/(2*M)
  for i in range(n):
   Ep=base.energies[p,i];e10=Ep*star/M;slope=t*q[i]*pstar/M;e20=Ep-e10;rate=base.measure[p*n+i]*c['width']*M/Ep/2
   cuts=[-1.,1.]
   if slope>0:
    for energies,offset,sl in ((base.energies[j],e10,slope),(base.energies[k],e20,-slope)):
     z=(energies-offset)/sl;cuts.extend(z[(z>-1+1e-14)&(z<1-1e-14)].tolist())
   cuts=np.unique(np.asarray(cuts))
   for left,right in zip(cuts[:-1],cuts[1:]):
    mid=(left+right)/2;half=(right-left)/2;target1=e10+slope*mid;target2=Ep-target1;coef=rate*half
    if target1<base.energies[j,0]-1e-13 or target1>base.energies[j,-1]+1e-13 or target2<base.energies[k,0]-1e-13 or target2>base.energies[k,-1]+1e-13:
     omitted[p*n+i]+=2*coef;continue
    jl,jh=bracket(base.energies[j],target1);kl,kh=bracket(base.energies[k],target2);fj=(target1-base.energies[j,jl])/(base.energies[j,jh]-base.energies[j,jl]);bj=slope*half/(base.energies[j,jh]-base.energies[j,jl]);fk=(target2-base.energies[k,kl])/(base.energies[k,kh]-base.energies[k,kl]);bk=-slope*half/(base.energies[k,kh]-base.energies[k,kl]);a=np.array([1.,1-fj,fj,1-fk,fk]);b=np.array([0.,-bj,bj,-bk,bk]);leftw=np.clip(a-b,0,1);rightw=np.clip(a+b,0,1);a=(leftw+rightw)/2;b=(rightw-leftw)/2
    index.append([p*n+i,j*n+jl,j*n+jh,k*n+kl,k*n+kh]);aa.append(a);bb.append(b);coefficient.append(coef);included[p*n+i]+=2*coef
 out=AngularExact(index,aa,bb,coefficient,base.measure,base.energy,base.eta,base.groups);out.by=base.by;out.q=q;out.W=np.asarray(W);out.t=t;out.x=data['x'];out.masses=base.masses;out.energies=base.energies;out.omitted_by_parent=omitted;out.included_by_parent=included;out.local_energy_residual=out.energy_residual
 return out

def averaged_exact_events(background,xs,weights,t,q,W):
 weights=np.asarray(weights,float);weights=weights/weights.sum();parts=[]
 for x in xs:
  d=background.at(float(x));parts.append(exact_events(d,t,q,W,source=d['current_source']))
 energy=sum(w*p.energy for w,p in zip(weights,parts));first=parts[0];out=AngularExact(np.concatenate([p.index for p in parts]),np.concatenate([p.a for p in parts]),np.concatenate([p.b for p in parts]),np.concatenate([w*p.coefficient for w,p in zip(weights,parts)]),first.measure,energy,first.eta,first.groups);out.q=np.asarray(q);out.W=np.asarray(W);out.t=t;out.xs=np.asarray(xs);out.phase_weights=weights;out.local_events=parts;out.local_energy_residual=max(p.energy_residual for p in parts);out.omitted_by_parent=sum(w*p.omitted_by_parent for w,p in zip(weights,parts));out.included_by_parent=sum(w*p.included_by_parent for w,p in zip(weights,parts))
 return out
