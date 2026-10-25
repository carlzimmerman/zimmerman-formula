"""Two-stage Gauss kinetic map, with exact quadratic-invariant stage currents."""
import numpy as np
from scipy.linalg.lapack import zgbtrf,zgbtrs
from lean import Sphere as Lean

class Sphere(Lean):
 def kinetic(self,u,tau):
  b=self.transform(u);n=len(self.r);g=np.sqrt(3)/6;A=np.array([[.25,.25-g],[.25+g,.25]]);vals,V=np.linalg.eig(A);ones=np.linalg.solve(V,np.ones(2));templates=[]
  for val in vals:
   ab=np.zeros((10,n),complex);c=1j*tau*val/self.eta
   for d in range(-3,4):
    js=np.arange(max(d,0),min(n,n+d));ii=js-d;ab[6-d,js]=(1 if d==0 else 0)+c*self.H[ii,js]
   templates.append(ab)
  for m in np.unique(abs(self.m)):
   ks=np.flatnonzero(abs(self.m)==m);k=int(ks[0])
   for l in range(self.nt):
    old=b[:,l,ks].copy();diag=self.eta**2*self.lam[l,k]/(2*self.r*self.r);ww=[]
    for j in range(2):
     ab=templates[j].copy();ab[6]+=1j*tau*vals[j]/self.eta*diag;lu,piv,info=zgbtrf(ab,3,3);assert info==0;x,info=zgbtrs(lu,3,3,np.asfortranarray(ones[j]*old),piv);assert info==0;ww.append(x)
    yy=[V[j,0]*ww[0]+V[j,1]*ww[1] for j in range(2)];mid=.5*(yy[0]+yy[1]);hm=(self.H.diagonal()+diag)[:,None]*mid
    for d in (1,2,3):
     h=np.diag(self.H,d);hm[:-d]+=h[:,None]*mid[d:];hm[d:]+=h.conj()[:,None]*mid[:-d]
    b[:,l,ks]=old-1j*tau/self.eta*hm
    for stage in yy:
     for d in (1,2,3):
      edge=-tau/self.eta*np.imag(stage[:-d].conj()*np.diag(self.H,d)[:,None]*stage[d:]);fm=np.sum(edge,axis=1);fj=self.eta*np.sum(edge*self.m[ks][None,:],axis=1)
      for offset in range(d):self.transport_mass[offset:n-d+offset]+=fm;self.transport_Jz[offset:n-d+offset]+=fj
  return self.transform(b,True)
