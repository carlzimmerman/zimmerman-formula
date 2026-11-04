"""Conservative cold-NR Coulomb template with tested dynamic logarithm scaling.

Stoichiometry is reprojected using exact new kinetic energies, preserving N/E
and quantum detailed balance at each T. The angular shape is a leading-log
approximation, and must be compared with fresh exact-CM builders in its domain.
"""
import numpy as np
from elastic_builder_v2 import COLOUR,screening,make_events

def characteristic_log(q,W,f,T,md2):
 q=np.asarray(q);f=np.asarray(f);meanq2=np.sum(W*q*q*f)/np.sum(W*f);R=2*T*T*meanq2/np.asarray(md2);return float(np.sum(COLOUR*(np.log1p(R)-R/(1+R))))

def template_arrays(reference,T,f,extra_screening=None):
 q=reference['q'];W=reference['W'];m=reference['m'];md=screening(q,W,f,T,m)
 if extra_screening is not None:md=md+np.asarray(extra_screening)
 oldindex=reference['index'];oldw=reference['weights'];Kr=reference['kinetic_energy'];E=np.sqrt(m*m+(T*q)**2);K=(T*q)**2/(E+m);total=K[oldindex[:,0]]+K[oldindex[:,1]];oldtotal=Kr[oldindex[:,0]]+Kr[oldindex[:,1]];fraction=np.sum(oldw[:,2:4]*Kr[oldindex[:,2:4]],axis=1)/oldtotal;t1=total*fraction;t2=total-t1
 def split(v):
  i=np.clip(np.searchsorted(K,v)-1,0,len(K)-2);j=i+1;u=np.clip((v-K[i])/(K[j]-K[i]),0,1);return i,j,u
 i,j,a=split(t1);k,l,b=split(t2);index=np.c_[oldindex[:,:2],i,j,k,l];weights=np.c_[np.ones(len(i)),np.ones(len(i)),1-a,a,1-b,b];oldf=reference['reference_screening_f'];ratio=characteristic_log(q,W,f,T,md)/characteristic_log(q,W,oldf,reference['T'],reference['md2']);out=dict(reference);out.update(index=index,weights=weights,coefficient=reference['coefficient']*ratio,energy=K,kinetic_energy=K,full_energy=E,T=T,md2=md,log_scale=ratio);return out
