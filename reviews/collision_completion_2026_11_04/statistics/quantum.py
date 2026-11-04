"""CC10 positive, energy-conserving entropic projection of quantum 1<->2.

Occupations are per physical spin state. Number coordinates use comoving
measure g*(q_hi^3-q_lo^3)/(6*pi^2). Rates/time use mu units. This is a finite
entropy-variable projection, NOT linear interpolation of continuum f.
"""
import os,sys
sys.dont_write_bytecode=True
for _key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):
 os.environ[_key]='1'
from pathlib import Path
import math
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.sparse import coo_matrix,diags,eye
from scipy.sparse.linalg import spsolve

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'reviews/coupled_trapping_2026_11_04/photino'))
from source import atx

NAMES=('F','C','U1','SU2','SU3')
DEGENERACIES=np.array([24.,12.,2.,6.,16.])
STATISTICS=np.array([-1.,1.,-1.,-1.,-1.])

def make_grid(bulk=24,qmax=80.,soft=.0001):
 """First node at zero; last at qmax. W are positive shell volumes."""
 q=np.unique(np.r_[0.,np.geomspace(soft,.3,8),np.linspace(.5,20.,bulk),30.,50.,qmax])
 edges=np.r_[0.,(q[:-1]+q[1:])/2,q[-1]+(q[-1]-q[-2])/2]
 return q,(edges[1:]**3-edges[:-1]**3)/3

def background(x):
 """Actual full-component projected widths, no interpolation in x."""
 row=atx(float(x))
 # The source sums all open physical charged scalar branches. In this
 # three-lowest-species truncation every open branch must be the C block.
 for daughter in row['charged_scalar_daughters']:
  if abs(daughter['mass_over_mu']-row['lightest_scalar_over_mu'])>1e-8:
   raise ValueError('heavier charged scalar open: add that population explicitly')
 return row

def energy_split(nodes,target):
 """Positive barycentric weights in ENERGY, or None outside finite support."""
 tol=2e-13*max(1.,abs(target))
 if target<nodes[0]-tol or target>nodes[-1]+tol:return None
 pos=int(np.searchsorted(nodes,target));lo=min(max(pos-1,0),len(nodes)-2)
 b=float(np.clip((target-nodes[lo])/(nodes[lo+1]-nodes[lo]),0.,1.))
 return lo,lo+1,1-b,b

class ReactionEvents:
 """Public generic event container. columns=(parent,d1lo,d1hi,d2lo,d2hi).

 `weights` are positive magnitudes with parent=1 and each child summing 1.
 `coefficient` is the integrated empty-final-state forward reaction measure.
 `measure` and `energy` are per-state-node. Additional channels can be
 concatenated by constructing this object from the arrays directly.
 """
 def __init__(self,index,weights,coefficient,measure,energy,eta,labels=None):
  self.index=np.asarray(index,dtype=int).reshape((-1,5));self.weights=np.asarray(weights,float).reshape((-1,5));self.coefficient=np.asarray(coefficient,float)
  self.measure=np.asarray(measure,float);self.energy=np.asarray(energy,float);self.eta=np.asarray(eta,float);self.labels=labels or []
  self.stoich=self.weights*np.array([-1.,1.,1.,1.,1.])[None,:]
  m=len(self.measure);r=len(self.coefficient)
  self.S=coo_matrix((self.stoich.ravel(),(self.index.ravel(),np.repeat(np.arange(r),5))),shape=(m,r)).tocsr()
  self.energy_residual=np.max(abs(np.sum(self.stoich*self.energy[self.index],axis=1)),initial=0.)
 def products(self,f):
  f=np.maximum(np.asarray(f,float),0.);f=np.where(self.eta<0,np.minimum(f,1.),f)
  vals=f[self.index];av=1+self.eta[self.index]*vals
  with np.errstate(divide='ignore',invalid='ignore'):
   lf=np.log(vals);la=np.log(av)
   fwd=np.exp(lf[:,0]+np.sum(np.where(self.weights[:,1:]>0,self.weights[:,1:]*la[:,1:],0.),axis=1))
   rev=np.exp(la[:,0]+np.sum(np.where(self.weights[:,1:]>0,self.weights[:,1:]*lf[:,1:],0.),axis=1))
  return fwd,rev,vals,av
 def flux(self,f):
  a,b,_,_=self.products(f);return self.coefficient*(a-b)
 def rhs(self,f):return np.asarray(self.S@self.flux(f)).ravel()/self.measure
 def rhs_jacobian(self,f):
  a,b,v,av=self.products(f);eps=1e-30
  deriv=np.empty_like(v)
  deriv[:,0]=a/np.maximum(v[:,0],eps)-b*self.eta[self.index[:,0]]/np.maximum(av[:,0],eps)
  deriv[:,1:]=self.weights[:,1:]*(a[:,None]*self.eta[self.index[:,1:]]/np.maximum(av[:,1:],eps)-b[:,None]/np.maximum(v[:,1:],eps))
  D=coo_matrix(((self.coefficient[:,None]*deriv).ravel(),(np.repeat(np.arange(len(a)),5),self.index.ravel())),shape=(len(a),len(f))).tocsr()
  return diags(1/self.measure)@self.S@D
 def affinity(self,f):
  v=np.asarray(f)[self.index];av=1+self.eta[self.index]*v
  with np.errstate(divide='ignore',invalid='ignore'):
   odds=np.log(v/av)
  return odds[:,0]-np.sum(self.weights[:,1:]*odds[:,1:],axis=1)
 def audit(self,f):
  a,b,_,_=self.products(f);flux=self.coefficient*(a-b);rhs=self.rhs(f)
  scale=max(float(np.sum(self.coefficient*(a+b))),1e-300)
  return dict(events=len(a),energy_residual=float(self.energy_residual),energy_rhs_relative=float(abs(np.dot(self.measure*self.energy,rhs))/max(scale*max(self.energy),1e-300)),detailed_balance_relative=float(np.sum(self.coefficient*abs(a-b))/scale),entropy_production=float(np.nansum(flux*self.affinity(f))),coefficient_sum=float(sum(self.coefficient)))

def conversion_events(x,t,q,W,angles=6,row=None):
 """All U1/SU2/SU3 group widths, unpolarized and gauge-factorized populations.

 Component production is proportional to its actual projected group width;
 no 1/12 or spin-degeneracy production split is inserted. Degeneracies enter
 only parent measure and occupation normalization. Equal charge sectors are
 represented together; each event copies its parent's signed charge.
 """
 row=background(x) if row is None else row;n=len(q)
 masses=np.array([row['light_fermion_over_mu'],row['lightest_scalar_over_mu']]+[row['gauginos_over_mu'][g] for g in NAMES[2:]])
 energies=np.sqrt(masses[:,None]**2+(t*q[None,:])**2)
 measure=(DEGENERACIES[:,None]*W[None,:]/(2*math.pi**2)).ravel();eta=np.repeat(STATISTICS,n)
 az,aw=leggauss(angles);indices=[];weights=[];coef=[];labels=[];dropped=0.;total=0.
 for parent,child,channel in ((0,1,'widths_over_mu'),(1,0,'reverse_lightest_scalar_widths_over_mu')):
  ma=masses[parent];mb=masses[child]
  for group,gname in enumerate(NAMES[2:],2):
   mc=masses[group];gamma=row[channel][gname]
   if gamma<=0 or ma<=mb+mc:continue
   star=(ma*ma+mb*mb-mc*mc)/(2*ma);pstar=math.sqrt(max(0,(ma-mb-mc)*(ma+mb+mc)*(ma-mb+mc)*(ma+mb-mc)))/(2*ma)
   for i in range(n):
    ep=energies[parent,i];p=t*q[i]
    for z,w in zip(az,aw):
     eb=(ep*star+p*pstar*z)/ma;ec=ep-eb
     rate=measure[parent*n+i]*gamma*ma/ep*w/2;total+=rate
     b=energy_split(energies[child],eb);c=energy_split(energies[group],ec)
     if b is None or c is None:dropped+=rate;continue
     indices.append([parent*n+i,child*n+b[0],child*n+b[1],group*n+c[0],group*n+c[1]])
     weights.append([1.,b[2],b[3],c[2],c[3]]);coef.append(rate);labels.append((parent,child,group))
 out=ReactionEvents(indices,weights,coef,measure,energies.ravel(),eta,labels)
 out.masses=masses;out.energies=energies;out.q=np.asarray(q);out.W=np.asarray(W);out.x=x;out.t=t;out.dropped_vacuum_measure=dropped;out.total_vacuum_measure=total;out.row=row
 return out

def equilibrium(events,temperature,chemical=None):
 chemical=np.zeros(5) if chemical is None else np.asarray(chemical)
 arg=(events.energies-chemical[:,None])/temperature
 return (1/(np.exp(np.minimum(arg,700))-STATISTICS[:,None])).ravel()

def entropy(f,measure,eta):
 f=np.asarray(f);avail=1+eta*f
 with np.errstate(divide='ignore',invalid='ignore'):
  val=-np.where(f>0,f*np.log(f),0)+np.where(avail>0,avail*np.log(avail)/eta,0)
 return float(measure@val)

def implicit_step(events,f,dt,tol=2e-9,maxiter=24):
 """Backward Euler, analytic sparse Newton, line search inside quantum bounds.

 No clipping of the accepted state or post-step energy/number correction.
 Failure requests a smaller time step; zero initial populations are allowed.
 """
 old=np.asarray(f,float);new=old.copy();ferm=events.eta<0
 for it in range(maxiter):
  rhs=events.rhs(new);res=new-old-dt*rhs
  norm=float(np.max(abs(res)/(1e-12+np.maximum(abs(old),abs(new)))))
  if norm<tol:return new,dict(iterations=it,residual=norm)
  A=eye(len(old),format='csr')-dt*events.rhs_jacobian(new)
  delta=spsolve(A,-res)
  if not np.all(np.isfinite(delta)):raise RuntimeError('nonfinite Newton correction')
  alpha=1.
  ids=delta<0
  if np.any(ids):alpha=min(alpha,float(np.min(-.995*new[ids]/delta[ids])))
  ids=ferm&(delta>0)
  if np.any(ids):alpha=min(alpha,float(np.min(.995*(1-new[ids])/delta[ids])))
  # Exact boundary nodes with a zero correction are harmless. A negative
  # correction at zero is not a realizable Newton step.
  if alpha<=1e-15:raise RuntimeError('Newton direction blocked at quantum boundary')
  base=float(np.linalg.norm(res))
  for ls in range(18):
   trial=new+alpha*delta
   rtrial=trial-old-dt*events.rhs(trial)
   if np.linalg.norm(rtrial)<base*(1-1e-5*alpha)+1e-20:break
   alpha*=.5
  else:raise RuntimeError('Newton line search failed')
  new=trial
 raise RuntimeError('Newton iteration budget')

def observables(events,f,mu=2e6,xi=.02):
 n=len(events.q);ff=np.asarray(f).reshape((5,n));w=events.measure.reshape((5,n));counts=np.sum(w*ff,axis=1);energy=np.sum(w*ff*events.energies,axis=1)*events.t**4 # corrected below: energies already physical mu
 energy=np.sum(w*ff*events.energies,axis=1)*events.t**3
 sm_entropy=2*math.pi**2/45*106.75*(events.t/xi)**3
 yield_s=counts*events.t**3/sm_entropy
 rho=energy.sum();sh=entropy(f,events.measure,events.eta)*events.t**3
 pmean=[];p2=[]
 for g in range(5):
  den=counts[g]
  pmean.append(float(w[g]@(ff[g]*(events.t*events.q))/den) if den else 0.)
  p2.append(float(w[g]@(ff[g]*(events.t*events.q)**2)/den) if den else 0.)
 return dict(number_comoving=counts.tolist(),yields=yield_s.tolist(),energy_mu4=energy.tolist(),hidden_entropy_mu3=sh,total_energy_mu4=float(rho),mean_p_over_mu=pmean,mean_p2_over_mu2=p2,min_f=float(min(f)),max_fermion_f=float(max(np.asarray(f)[events.eta<0])),max_scalar_f=float(max(ff[1])))
