"""Cubic radial SEM, square spherical DVR and symmetric one-source Green map."""
import numpy as np
from scipy.linalg import eigh
from scipy.linalg.lapack import zgbtrf,zgbtrs
from scipy.special import eval_legendre
from numpy.polynomial.legendre import leggauss

class Sphere:
 def __init__(self,ne=128,nt=24,nf=32,R=28,alpha=6,eta=.05,phase=None):
  self.ne=ne;self.nt=nt;self.nf=nf;self.R=R;self.alpha=alpha;self.eta=eta
  z=np.array([-1,-1/np.sqrt(5),1/np.sqrt(5),1.]);wg=np.array([1,5,5,1.])/6
  bary=np.array([1/np.prod(z[i]-np.delete(z,i)) for i in range(4)]);D=np.zeros((4,4))
  for i in range(4):
   for j in range(4):
    if i!=j:D[i,j]=bary[j]/bary[i]/(z[i]-z[j])
   D[i,i]=-D[i].sum()
  n=3*ne+1;xi=np.zeros(n);wr=np.zeros(n);st=np.zeros((n,n));adv=np.zeros((n,n),complex)
  for e in range(ne):
   ix=np.arange(3*e,3*e+4);xx=(e+(z+1)/2)/ne;xi[ix]=xx;J=R*alpha*np.cosh(alpha*xx)/np.sinh(alpha);w=wg/(2*ne)*J;wr[ix]+=w
   st[np.ix_(ix,ix)]+=D.T@np.diag(wg*(2*ne)/J)@D
  rr=R*np.sinh(alpha*xi)/np.sinh(alpha);self.r=rr[1:-1];self.w=wr[1:-1];self.sr=self.r*np.sqrt(self.w)
  self.phase=np.zeros_like(self.r) if phase is None else phase(self.r)
  pp=np.zeros(n) if phase is None else phase(rr,1)
  for e in range(ne):
   ix=np.arange(3*e,3*e+4);a=(wg*pp[ix])[:,None]*D
   adv[np.ix_(ix,ix)]+=-1j*eta/2*(a-a.T)
  norm=np.sqrt(wr[1:-1]);self.H=(eta**2/2*st[1:-1,1:-1]+adv[1:-1,1:-1])/norm[:,None]/norm[None,:]+np.diag(pp[1:-1]**2/2)
  self.p=pp[1:-1];self.mu,self.wmu=leggauss(nt);self.phi=np.arange(nf)*np.pi/nf;self.aw=self.wmu[:,None]*np.full((1,nf),2*np.pi/nf);self.sa=np.sqrt(self.aw)
  ll=np.arange(nt);Q=np.sqrt(self.wmu)[:,None]*np.array([eval_legendre(l,self.mu) for l in ll]).T*np.sqrt((2*ll+1)/2)[None,:];L0=(Q*(ll*(ll+1))[None,:])@Q.T
  self.m=np.rint(np.fft.fftfreq(nf)*nf*2).astype(int);self.Q=[];self.lam=[]
  for m in self.m:
   if m==0:vals=ll*(ll+1);vec=Q
   else:vals,vec=eigh(L0+np.diag(m*m/(1-self.mu*self.mu)))
   self.Q.append(vec);self.lam.append(vals)
  self.lam=np.array(self.lam).T;self.ell=(np.sqrt(1+4*self.lam)-1)/2
  self.cache={};self.Dr=D;self.z=z;self.xyz=self.angular_vectors()
 def angular_vectors(self):
  mu=self.mu[:,None];ph=self.phi[None,:];ss=np.sqrt(1-mu*mu)
  return np.array([ss*np.cos(ph),ss*np.sin(ph),np.broadcast_to(mu,(self.nt,self.nf))])
 def transform(self,a,inverse=False):
  if not inverse:
   b=np.fft.fft(a,axis=2,norm='ortho')
   for k,Q in enumerate(self.Q):b[:,:,k]=b[:,:,k]@Q
  else:
   b=a.copy()
   for k,Q in enumerate(self.Q):b[:,:,k]=b[:,:,k]@Q.T
   b=np.fft.ifft(b,axis=2,norm='ortho')
  return b
 def angular(self,u,tau,apply=False):
  b=self.transform(u);freq=self.eta*self.lam[None,:,:]/(2*self.r[:,None,None]**2)
  b*=self.eta*freq if apply else np.exp(-1j*tau*freq)
  return self.transform(b,True)
 def poisson_mass(self,m):
  src=m/(self.w*self.r*self.r)[:,None,None]/self.sa[None,:,:];coef=self.transform(src);out=np.empty_like(coef);A=np.zeros_like(coef[0]);r=self.r;ell=self.ell
  for i in range(len(r)):
   if i:A*=np.exp(ell*np.log(r[i-1]/r[i]))
   A+=self.w[i]*r[i]**2*coef[i];out[i]=A/r[i]
  B=np.zeros_like(A)
  for i in range(len(r)-1,-1,-1):
   if i+1<len(r):B*=np.exp(ell*np.log(r[i]/r[i+1]))
   f=self.w[i]*r[i]*coef[i];B+=f;out[i]+=B-f
  out*=-4*np.pi/(2*ell[None,:,:]+1);pot=self.transform(out,True)/self.sa[None,:,:]
  assert np.max(abs(pot.imag))<1e-8*max(1,np.max(abs(pot.real)))
  return pot.real
 def poisson(self,u):return self.poisson_mass(abs(u)**2)
 def radial_apply(self,u):
  out=self.H.diagonal()[:,None,None]*u
  for d in (1,2,3):
   h=np.diag(self.H,d);out[:-d]+=h[:,None,None]*u[d:];out[d:]+=h.conj()[:,None,None]*u[:-d]
  return out
 def radial(self,u,tau):
  key=float(tau)
  if key not in self.cache:
   n=len(self.r);ab=np.zeros((10,n),complex);c=1j*tau/(2*self.eta)
   for d in range(-3,4):
    js=np.arange(max(d,0),min(n,n+d));ii=js-d;ab[6-d,js]=(1 if d==0 else 0)+c*self.H[ii,js]
   lu,piv,info=zgbtrf(ab,3,3);assert info==0;self.cache[key]=(lu,piv)
  rhs=u-1j*tau/(2*self.eta)*self.radial_apply(u);sh=rhs.shape;v,info=zgbtrs(*self.cache[key][:1],3,3,np.asfortranarray(rhs.reshape(sh[0],-1)),self.cache[key][1]);assert info==0
  return v.reshape(sh)
 def step2(self,u,pot,dt):
  u=u*np.exp(-1j*dt/(2*self.eta)*pot);u=self.radial(u,dt/2);u=self.angular(u,dt);u=self.radial(u,dt/2);pot=self.poisson(u);u*=np.exp(-1j*dt/(2*self.eta)*pot);return u,pot
 def step(self,u,pot,dt):
  c=1/(2-2**(1/3))
  for a in (c,1-2*c,c):u,pot=self.step2(u,pot,dt*a)
  return u,pot
 def moments(self,u,pot):
  b=self.transform(u);mass=abs(u)**2;K=float(np.real(np.vdot(u,self.radial_apply(u)))+np.sum(abs(b)**2*self.eta**2*self.lam[None,:,:]/(2*self.r[:,None,None]**2)));W=float(.5*np.sum(mass*pot));ang=float(np.sum(abs(b)**2*(self.ell[None,:,:]>.75*(self.nt-1))))
  return dict(M=float(mass.sum()),K=K,W=W,E=K+W,Jz=float(self.eta*np.sum(abs(b)**2*self.m[None,None,:])),angular_edge_fraction=ang/max(float(mass.sum()),1e-30),boundary_fraction=float(mass[self.r>.85*self.R].sum()/max(mass.sum(),1e-30)),M_inner=float(mass[self.r<1].sum()),COM=[0.,0.,float(np.sum(mass*self.r[:,None,None]*self.mu[None,:,None])/mass.sum())])
