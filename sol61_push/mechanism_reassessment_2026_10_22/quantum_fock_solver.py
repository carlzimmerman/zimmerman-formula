"""Finite-mode nonlinear quantum Hamiltonian from the normal-ordered complex action.
Units mPhi=1. Momentum labels -1,0,1 along one axis in a 3D periodic box;
all other modes are omitted: this is a Galerkin benchmark, not a continuum bath.
"""
from collections import defaultdict
from itertools import product
import numpy as np
from scipy.sparse import coo_matrix,diags,eye
from scipy.sparse.linalg import expm_multiply

class Model:
 def __init__(self,energy_cut=10.,number_cut=8,charge=2,momentum=0,volume=100.,p=None):
  self.M=2*np.sqrt(1+.02**2);self.g=.002168;self.lam=.00881292
  self.p=np.sqrt(((self.M+2)/2)**2-1) if p is None else float(p)
  self.volume=volume;self.momenta=np.tile([-1,0,1],4);self.charges=np.repeat([1,-1,2,-2],3)
  self.energies=np.sqrt(np.repeat([1,1,self.M**2,self.M**2],3)+(self.p*self.momenta)**2)
  states=[]
  def visit(j,left,nleft,qleft,pleft,ns):
   if j==12:
    if qleft==0 and pleft==0:states.append(tuple(ns))
    return
   for n in range(min(nleft,int((left+1e-10)/self.energies[j]))+1):
    visit(j+1,left-n*self.energies[j],nleft-n,qleft-n*self.charges[j],pleft-n*self.momenta[j],ns+[n])
  visit(0,energy_cut,number_cut,charge,momentum,[])
  self.states=np.array(states,dtype=int);self.index={x:i for i,x in enumerate(states)};self.free=self.states@self.energies
  self.H0=diags(self.free,format='csr')
  self.H3=self.operator(self.vertex([('Xbar','phi','phi'),('X','phibar','phibar')]))
  self.H4=self.operator(self.vertex([('phibar','phibar','phi','phi')]))
  self.mass_phi=self.operator(self.vertex([('phibar','phi')]))
  self.mass_X=self.operator(self.vertex([('Xbar','X')]))
  self.mass_operator=self.mass_phi+self.M**2*self.mass_X
  # Vacuum c-number omitted consistently; no effect on density-matrix dynamics.
 def field(self,name):
  # tuple: mode, create(+1)/annihilate(-1), Fourier phase, coefficient.
  sectors={'phi':[(0,-1),(3,1)],'phibar':[(0,1),(3,-1)],'X':[(6,-1),(9,1)],'Xbar':[(6,1),(9,-1)]}
  return [(off+j,sgn,-sgn*self.momenta[off+j],1/np.sqrt(2*self.energies[off+j])) for off,sgn in sectors[name] for j in range(3)]
 def vertex(self,words):
  terms=defaultdict(float)
  for word in words:
   for factors in product(*(self.field(w) for w in word)):
    if sum(f[2] for f in factors):continue
    create=tuple(sorted(f[0] for f in factors if f[1]==1));ann=tuple(sorted(f[0] for f in factors if f[1]==-1))
    terms[create,ann]+=self.volume**(1-len(word)/2)*np.prod([f[3] for f in factors])
  return terms
 def operator(self,terms):
  rows=[];cols=[];data=[]
  for j,state in enumerate(self.states):
   for (create,ann),coef in terms.items():
    v=state.copy();weight=coef
    for k in ann:
     if v[k]==0:weight=0.;break
     weight*=np.sqrt(v[k]);v[k]-=1
    if weight==0:continue
    for k in create:weight*=np.sqrt(v[k]+1);v[k]+=1
    i=self.index.get(tuple(v))
    if i is not None:rows.append(i);cols.append(j);data.append(weight)
  return coo_matrix((data,(rows,cols)),shape=(len(self.states),)*2).tocsr()
 def hamiltonian(self,a=1.,g=None,lam=None):
  g=self.g if g is None else g;lam=self.lam if lam is None else lam
  return self.H0+(a*a-1)*self.mass_operator+a*g*self.H3+lam*self.H4
 def evolve(self,initial,times,scale_factor=lambda t:1.,g=None,lam=None):
  """Unitary exponential midpoint; converges with timestep, no collision switching."""
  psi=np.asarray(initial,dtype=complex).copy();history=[psi.copy()]
  for t0,t1 in zip(times[:-1],times[1:]):
   h=self.hamiltonian(scale_factor((t0+t1)/2),g,lam)
   psi=expm_multiply((-1j*(t1-t0))*h,psi);history.append(psi.copy())
  return np.array(history)
 def occupation_correlations(self,history):
  probability=abs(history)**2;mean=probability@self.states
  pair=np.einsum('ti,ij,ik->tjk',probability,self.states,self.states,optimize=True)
  return mean,pair-mean[:,:,None]*mean[:,None,:]
