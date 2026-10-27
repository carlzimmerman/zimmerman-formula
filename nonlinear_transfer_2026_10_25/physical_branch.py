"""Exact response throughout accepted physical states, trial-only continuation."""
import numpy as np
from outgoing import OutgoingFull,OutgoingBO

class ExactResponse:
 def f(self,u):
  u=np.asarray(u);c=.9999;v=np.minimum(u,c);d=u-v;poly=np.zeros_like(v)+1/16
  for n in range(15,1,-1):poly=1/n+v*poly
  W=np.where(abs(v)<.05,v*v*poly,-np.log1p(-v)-v)+d*c/(1-c)+.5*d*d/(1-c)**2
  F=v*v/(1-v)+d*c*(2-c)/(1-c)**2+d*d/(1-c)**3;Wp=v/(1-v)+d/(1-c)**2;Fp=v*(2-v)/(1-v)**2+2*d/(1-c)**3
  return W,F,Wp,Fp

class PhysicalFull(ExactResponse,OutgoingFull):pass
class PhysicalBO(ExactResponse,OutgoingBO):pass
