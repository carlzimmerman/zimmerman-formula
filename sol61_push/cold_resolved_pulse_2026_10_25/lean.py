"""Same Hermitian CN kinetic map, paired azimuth RHS and no persistent LU cache."""
import pathlib,sys,numpy as np
from scipy.linalg.lapack import zgbtrf,zgbtrs
OLD=pathlib.Path(__file__).resolve().parents[1]/'cold_fourth_flux_2026_10_25'
sys.path.insert(0,str(OLD))
from sphere_v3 import Sphere as Original

class Sphere(Original):
 def kinetic(self,u,tau):
  b=self.transform(u);old=b.copy();hb=self.radial_apply(b)+self.eta**2*self.lam[None,:,:]/(2*self.r[:,None,None]**2)*b
  rhs=b-1j*tau/(2*self.eta)*hb;del hb
  n=len(self.r);c=1j*tau/(2*self.eta);template=np.zeros((10,n),complex)
  for d in range(-3,4):
   js=np.arange(max(d,0),min(n,n+d));ii=js-d;template[6-d,js]=(1 if d==0 else 0)+c*self.H[ii,js]
  for m in np.unique(abs(self.m)):
   ks=np.flatnonzero(abs(self.m)==m);k=int(ks[0])
   for l in range(self.nt):
    ab=template.copy();ab[6]+=c*self.eta**2*self.lam[l,k]/(2*self.r**2)
    lu,piv,info=zgbtrf(ab,3,3);assert info==0
    x,info=zgbtrs(lu,3,3,np.asfortranarray(rhs[:,l,ks]),piv);assert info==0
    b[:,l,ks]=x
  del rhs
  mid=.5*(old+b);del old
  for d in (1,2,3):
   edge=-2*tau/self.eta*np.imag(mid[:-d].conj()*np.diag(self.H,d)[:,None,None]*mid[d:])
   fm=np.sum(edge,axis=(1,2));fj=self.eta*np.sum(edge*self.m[None,None,:],axis=(1,2))
   for offset in range(d):
    self.transport_mass[offset:n-d+offset]+=fm
    self.transport_Jz[offset:n-d+offset]+=fj
  return self.transform(b,True)
