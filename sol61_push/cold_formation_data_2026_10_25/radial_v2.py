"""O(N) cubic phase-fitted SEM and energy-preserving nonlinear CN."""
import numpy as np
from scipy.linalg import solve_banded

def phi_shell(r,dm):
 c=np.cumsum(dm);o=np.cumsum((dm/r)[::-1])[::-1]-dm/r
 return -c/r-o

def potential_at(q,r,dm):
 q=np.asarray(q);ix=np.searchsorted(r,q,side='right');c=np.r_[0,np.cumsum(dm)];o=np.r_[np.cumsum((dm/r)[::-1])[::-1],0.]
 return -c[ix]/np.maximum(q,1e-300)-o[ix]

def force_at(q,r,dm):
 q=np.asarray(q);ix=np.searchsorted(r,q,side='right');return np.r_[0,np.cumsum(dm)][ix]/np.maximum(q*q,1e-300)

class Radial:
 def __init__(self,ne=1024,eta=.05,vin=0.,R=40.,alpha=12.,pb=None):
  self.ne=ne;self.eta=eta;self.R=R;self.alpha=alpha
  z=np.array([-1.,-1/np.sqrt(5),1/np.sqrt(5),1.]);wg=np.array([1,5,5,1.])/6;bary=np.array([1/np.prod(z[i]-np.delete(z,i)) for i in range(4)]);D=np.zeros((4,4))
  for i in range(4):
   for j in range(4):
    if i!=j:D[i,j]=bary[j]/bary[i]/(z[i]-z[j])
   D[i,i]=-D[i].sum()
  nn=3*ne+1;rr=np.zeros(nn);ww=np.zeros(nn);locals=[]
  for e in range(ne):
   ix=np.arange(3*e,3*e+4);xi=(e+(z+1)/2)/ne;r=R*np.sinh(alpha*xi)/np.sinh(alpha);J=R*alpha*np.cosh(alpha*xi)/np.sinh(alpha);w=wg*J/(2*ne);rr[ix]=r;ww[ix]+=w;locals.append((ix,r,J,w))
  self.r=rr[1:-1];self.w=ww[1:-1];self.p=-vin*self.r/np.sqrt(self.r*self.r+.05**2);n=len(self.r);diag=np.zeros(n);upper=[np.zeros(n-d,complex) for d in [1,2,3]]
  for ix,r,J,w in locals:
   p=-vin*r/np.sqrt(r*r+.05**2);A=eta*(2*ne/J)[:,None]*D+1j*np.diag(p);K=.5*A.conj().T@(w[:,None]*A)
   for i,gi in enumerate(ix):
    if gi==0 or gi==nn-1:continue
    a=gi-1;diag[a]+=K[i,i].real/ww[gi]
    for j in range(i+1,4):
     gj=ix[j]
     if gj==nn-1:continue
     d=gj-gi;upper[d-1][a]+=K[i,j]/np.sqrt(ww[gi]*ww[gj])
  self.diag=diag;self.upper=upper;self.pb=np.zeros(n) if pb is None else pb(self.r);self.transport=np.zeros(n-1)
 def gaussian(self):return (2/np.pi**.25*self.r*np.exp(-self.r*self.r/2)*np.sqrt(self.w)).astype(complex)
 def apply(self,u):
  ans=self.diag*u
  for d,h in enumerate(self.upper,1):ans[:-d]+=h*u[d:];ans[d:]+=h.conj()*u[:-d]
  return ans
 def kinetic(self,u):return float(np.vdot(u,self.apply(u)).real)
 def energy(self,u,phi):return self.kinetic(u)+float(np.sum(abs(u)**2*(.5*phi+self.pb)))
 def inventory(self,u,phi,rc):
  m=abs(u)**2;sel=self.r<rc;Kloc=np.real(u.conj()*self.apply(u));return dict(M=float(m[sel].sum()),E=float(np.sum((Kloc+m*(.5*phi+self.pb))[sel])))
 def phase_bad(self,u):
  m=abs(u)**2;weight=.5*(m[:-1]+m[1:]);return float(np.sum(weight*(abs(np.angle(u[:-1].conj()*u[1:]))>np.pi/3))/max(weight.sum(),1e-300))
 def step(self,old,phi,dt,tag=None):
  n=len(old);c=1j*dt/(2*self.eta);guess=phi.copy();previous=old;error=float('inf');sol=old
  for iteration in range(200):
   p=self.pb+.5*(phi+guess);diag=self.diag+p;rhs=old-c*(self.apply(old)+p*old);ab=np.zeros((7,n),complex);ab[3]=1+c*diag
   for d,h in enumerate(self.upper,1):ab[3-d,d:]=c*h;ab[3+d,:-d]=c*h.conj()
   sol=solve_banded((3,3),ab,rhs,overwrite_ab=True,check_finite=False);newphi=phi_shell(self.r,abs(sol)**2)
   resid=sol-old+c*(self.apply(sol+old)+(self.pb+.5*(phi+newphi))*(sol+old));error=float(np.linalg.norm(resid)/np.linalg.norm(old))
   if error<=1e-11:break
   guess=.5*(guess+newphi);previous=sol
  if error>1e-10:return old,phi,tag,dict(converged=False,residual=error,iterations=iteration+1)
  mid=.5*(old+sol);flows=[]
  for d,h in enumerate(self.upper,1):
   flow=-2*dt/self.eta*np.imag(mid[:-d].conj()*h*mid[d:]);flows.append(flow)
   for offset in range(d):self.transport[offset:n-d+offset]+=flow
  if tag is not None:
   mass=abs(sol)**2;iv=1/np.maximum(mass,1e-280);ab=np.zeros((7,n));ab[3]=1
   for d,flow in enumerate(flows,1):
    plus=np.maximum(flow,0)*iv[:-d];minus=np.maximum(-flow,0)*iv[d:];ab[3,:-d]+=plus;ab[3,d:]+=minus;ab[3+d,:-d]-=plus;ab[3-d,d:]-=minus
   tag=solve_banded((3,3),ab,tag,overwrite_ab=True,check_finite=False)
  return sol,newphi,tag,dict(converged=True,residual=error,iterations=iteration+1)
