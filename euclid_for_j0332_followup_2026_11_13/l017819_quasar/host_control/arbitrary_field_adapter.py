"""Frozen VIS host-control adapter for arbitrary PURE REDUCED deflection.
Same Gaussian priors/operator as fit_host_v4. No field theory is assumed here.
"""
import sys
from pathlib import Path
import numpy as np
B=Path(__file__).resolve().parent
sys.path.insert(0,str(B))
from fit_host_v4 import Host
class FieldAdapter(Host):
 def __init__(self,light_parameters,ns=21,step=.06,supersample=2):
  super().__init__(ns,step);self.ss=supersample
  self.startlight=np.asarray(light_parameters,float).copy()
  if self.startlight.shape!=(6,):raise ValueError('light_parameters must be [cx,cn,lnRe_major,lnn,q,phi_west_radians]')
  self.pure=None
 def rays(self,p):
  if self.pure is None:raise ValueError('evaluate requires pure reduced deflection callable')
  a=np.asarray(self.pure(*self.A),float);b=np.asarray(self.pure(*self.C),float);d=self.A-self.C;v=d-(a-b);dx,dy=d;g1=(dx*v[0]-dy*v[1])/(d@d);g2=(dy*v[0]+dx*v[1])/(d@d)
  def total(x,y):
   ax,an=self.pure(x,y);return ax+g1*x+g2*y,an+g2*x-g1*y
  self.center=tuple(self.A-np.asarray(total(*self.A)))
  return total,(g1,g2)
 def evaluate(self,deflection,log_regularization=3.,return_arrays=True):
  """deflection(Xwest,Nnorth)->(ax,an) arcsec, already Dls/Ds reduced,
  with NO external shear or kappa. Adds exact-two-point shear, rebuilds source
  center/basis, profiles proper Gaussian source+lens/A/Bflux+sky coefficients.
  score omits only fixed image-noise normalization; same data/mask required.
  """
  self.pure=deflection
  p=np.r_[self.startlight[2:6],.8,.7,1.,float(log_regularization)]
  return self.run(p,arrays=return_arrays)
