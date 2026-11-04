"""Stable-log event flux for immutable mixed hole-coordinate Newton driver.

Availability is carried explicitly. Subtracting two separately exponentiated
balanced event products loses accuracy; log1p and expm1 retain the difference.
NumPy longdouble is used where the platform supplies extended precision; its
actual mantissa must be recorded by each control. Physical number storage and
sparse Newton solves remain float64. No state clipping or portal is added.
"""
import numpy as np
from holes_v2 import QuantumState as OriginalQuantumState,implicit_step

class QuantumState(OriginalQuantumState):
 def copy(self):return QuantumState(self.measure,self.eta,Z=self.Z,holes=self.holes)
 def logarithms(self):
  z=np.asarray(self.Z,np.longdouble)/np.asarray(self.measure,np.longdouble);eta=np.asarray(self.eta,np.longdouble)
  with np.errstate(divide='ignore',invalid='ignore'):
   logz=np.log(z);logone=np.log1p(-z)
   lf=np.where(self.holes,logone,logz)
   la=np.where(self.holes,logz,np.where(eta<0,logone,np.log1p(z)))
  return lf,la
 def logproducts(self,events):
  lf,la=self.logarithms();idx=events.index;w=np.asarray(events.weights[:,1:],np.longdouble)
  with np.errstate(invalid='ignore'):
   A=lf[idx[:,0]]+np.sum(np.where(w>0,w*la[idx[:,1:]],0.),axis=1,dtype=np.longdouble)
   B=la[idx[:,0]]+np.sum(np.where(w>0,w*lf[idx[:,1:]],0.),axis=1,dtype=np.longdouble)
  return A,B
 def products(self,events):
  A,B=self.logproducts(events);f,a=self.arrays()
  return np.asarray(np.exp(A),float),np.asarray(np.exp(B),float),f[events.index],a[events.index]
 def flux(self,events):
  A,B=self.logproducts(events);forward=A>=B
  with np.errstate(invalid='ignore',over='ignore'):
   # Both-empty events have A=B=-inf and exactly zero flux.
   difference=np.where(forward,np.exp(A)*(-np.expm1(B-A)),np.exp(B)*np.expm1(A-B))
  difference=np.where(np.isneginf(A)&np.isneginf(B),0.,difference)
  return np.asarray(np.asarray(events.coefficient,np.longdouble)*difference,float)
