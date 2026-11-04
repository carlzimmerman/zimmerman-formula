"""Common S/F/vector masses, statistics and scalar gas force for CC11.

All vector phases use the same analytic mass squared and derivative. Vector
helicity multiplicity is explicit; vector populations are bosonic. No reaction
rate or polarization closure is defined by this background alone.
"""
import sys,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
OLD=ROOT/'reviews/collision_completion_2026_11_04'
sys.path.insert(0,str(OLD/'cascades'))
sys.path.insert(0,str(OLD/'integration'))
from consistent_background import ConsistentVertexBackground
from generic_orbit import GenericOrbit,T0,MU,XI
E=.003
G=math.sqrt(29/200)*E
A2=2/(31*E)
VECTOR_GROUPS=[dict(id='Vc_L',kind='V',rep='c',charged=True,degeneracy=12,polarizations=1,helicity='longitudinal',q2=5/12,casimir=25/12),dict(id='Vc_T',kind='V',rep='c',charged=True,degeneracy=24,polarizations=2,helicity='transverse',q2=5/12,casimir=25/12),dict(id='V8_T',kind='V',rep='8',charged=False,degeneracy=16,polarizations=2,helicity='transverse',q2=0.,casimir=3.),dict(id='V3_T',kind='V',rep='3',charged=False,degeneracy=6,polarizations=2,helicity='transverse',q2=0.,casimir=2.),dict(id='V1_T',kind='V',rep='1',charged=False,degeneracy=2,polarizations=2,helicity='transverse',q2=0.,casimir=0.)]

def vector_mass2(x,nu=0):
 x=np.asarray(x,float)
 if nu==0:return 25*G*G*(A2+x*x)
 if nu==1:return 50*G*G*x
 if nu==2:return np.full_like(x,50*G*G)
 return np.zeros_like(x)

class ExtendedMass2:
 def __init__(self,base):self.base=base
 def __call__(self,x,nu=0):
  x=np.asarray(x,float);v=vector_mass2(x,nu);z=np.zeros_like(v)
  return np.concatenate([self.base(x,nu),np.stack([v,v,z,z,z],axis=-1)],axis=-1)

class CommonBackground:
 def __init__(self,path=None):
  path=path or OLD/'cascades/run_vertices001/result.json'
  self.base=ConsistentVertexBackground(path);self.xs=self.base.xs
  self.groups=[dict(g) for g in self.base.groups]+[dict(g,indices=[],mass=math.sqrt(vector_mass2(self.xs[0])) if g['charged'] else 0.) for g in VECTOR_GROUPS]
  self.by={g['id']:i for i,g in enumerate(self.groups)};self.mass2=ExtendedMass2(self.base.mass2)
 def at(self,x):
  d=self.base.at(x);m2=self.mass2(x);sl=self.mass2(x,1);groups=[]
  for i,g in enumerate(self.groups):
   m=math.sqrt(max(0,float(m2[i])));groups.append(dict(g,mass=m,dm2_dx=float(sl[i]),dm_dx=float(sl[i]/(2*m)) if m>0 else 0.))
  d['groups']=groups;d['m_vector']=float(math.sqrt(vector_mass2(x)));d['vector_groups']=[g['id'] for g in VECTOR_GROUPS]
  return d

class CommonOrbit(GenericOrbit):
 def __init__(self,background,q,W,phase_nodes=16,neutral_force=True):
  super().__init__(background,q,W,phase_nodes,neutral_force)
  self.eta=np.repeat([1 if g['kind'] in ('S','V') else -1 for g in self.groups],self.n)
 def summary(self,N,Y,orb):
  h=super().summary(N,Y,orb);t=T0*math.exp(-N);nums=np.asarray(Y).reshape(self.ns,self.n).sum(axis=1);s=2*math.pi**2/45*106.75*(t/XI)**3
  masses=np.sqrt(np.maximum(self.bg.mass2(orb['xs']),0));rest=t**3*nums*(orb['weights']@masses);num=t**3*nums/s
  h.update(charged_rest_energy_over_SM_entropy_GeV=MU*float(rest@self.charged)/s,charged_rest_energy_over_10percent_DM_gate=MU*float(rest@self.charged)/s/(.1*.44e-9),vector_number_yield=float(sum(num[i] for i,g in enumerate(self.groups) if g['kind']=='V')),photino_number_yield=float(num[self.by['F1_1']]),group_number_yields=num.tolist(),groups=[g['id'] for g in self.groups])
  return h

def extend_numbers(old_numbers,old_groups,new_groups,n):
 """Embed unchanged momenta/species; new species start exactly empty."""
 old=np.asarray(old_numbers).reshape(len(old_groups),n);out=np.zeros((len(new_groups),n));lookup={g['id'] if isinstance(g,dict) else g:i for i,g in enumerate(old_groups)}
 for j,g in enumerate(new_groups):
  if g['id'] in lookup:out[j]=old[lookup[g['id']]]
 return out.ravel()
