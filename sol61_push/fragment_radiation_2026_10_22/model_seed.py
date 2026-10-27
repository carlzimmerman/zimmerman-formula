import numpy as np
from scipy.optimize import minimize
from scipy.special import ndtri
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

class Model:
 def __init__(self,n=32,box=8,np_side=10,mass_ratio=1,spin=.02,lam=100,seed_shift=0):
  self.n=n;self.box=box;self.dx=box/n;self.vol=self.dx**3/(4*np.pi);self.eta=.005;self.a=1/(2*lam);self.b=self.a/.2**2;self.d=self.b
  q=ndtri((np.arange(np_side)+.5)/np_side);x=np.array(np.meshgrid(q,q,q,indexing='ij')).reshape(3,-1).T*.6
  x*=np.array([1.2,.8,1]);x[:,0]+=.06*np.sin(np.pi*x[:,0]/.6);x-=x.mean(axis=0);x+=seed_shift*self.dx
  theta=np.arctan2(x[:,1],x[:,0]);x+=.03*np.column_stack([np.sin(3*theta)*np.cos(x[:,2]/.6),np.cos(2*theta)*np.sin(x[:,2]/.6),np.sin(2*theta)]);x-=x.mean(axis=0)
  self.x0=x;self.mass=.08408132497418408*mass_ratio;self.m=self.mass/len(x)
  k=4*np.sin(np.pi*np.fft.fftfreq(n))**2/self.dx**2;self.k2=k[:,None,None]+k[None,:,None]+k[None,None,:];self.safe=self.k2.copy();self.safe[0,0,0]=1
  grid=(np.arange(n)-n/2)*self.dx;xx=np.meshgrid(grid,grid,grid,indexing='ij');rad=np.sqrt(sum(t*t for t in xx));self.sg=2*np.clip((rad-2.7)/(box/2-2.7),0,1)**2
  self.mask=np.maximum.reduce([abs(t) for t in xx])<2.25
  rho,_,_=self.deposit(x);U,phi=self.gravity(rho);I=self.m*np.sum(x[:,0]**2+x[:,1]**2);om=np.sqrt(2*spin*abs(U)/I)
  self.v0=om*np.array([-x[:,1],x[:,0],np.zeros(len(x))]).T
 def grad(self,h):return np.array([(np.roll(h,-1,axis=i)-h)/self.dx for i in range(3)])
 def div(self,P):return sum((P[i]-np.roll(P[i],1,axis=i))/self.dx for i in range(3))
 def deposit(self,x):
  u=x/self.dx+self.n/2;j=np.floor(u+.5).astype(int);offs=np.array(np.meshgrid([-1,0,1],[-1,0,1],[-1,0,1],indexing='ij')).reshape(3,-1).T
  ids=j[:,None,:]+offs;dist=u[:,None,:]-ids;ad=abs(dist);w=np.where(ad<.5,.75-dist*dist,.5*(1.5-ad)**2);dw=np.where(ad<.5,-2*dist,-(1.5-ad)*np.sign(dist))/self.dx
  weight=np.prod(w,axis=2);der=np.array([dw[:,:,i]*w[:,:,(i+1)%3]*w[:,:,(i+2)%3] for i in range(3)]).transpose(1,2,0)
  ids%=self.n;flat=(ids[:,:,0]*self.n+ids[:,:,1])*self.n+ids[:,:,2];rho=np.bincount(flat.ravel(),weights=(self.m/self.vol*weight).ravel(),minlength=self.n**3).reshape((self.n,)*3)
  return rho,flat,der
 def gravity(self,rho):
  phi=np.fft.ifftn(-np.fft.fftn(rho)/self.safe).real;phi-=phi.mean();return .5*self.vol*np.sum(rho*phi),phi
 def static(self,x):
  rho,_,_=self.deposit(x);inv=lambda z:np.fft.ifftn(np.fft.fftn(z)/(self.a+self.d*self.k2)).real
  def fg(y):
   h=y.reshape(rho.shape);g=self.grad(h);s=np.sqrt(np.sum(g*g,axis=0));zz=inv(h*h)
   return np.sum(.5*h*h+s-np.log1p(s)-rho*h+.125*h*h*zz),(h+.5*h*zz-self.div(g/(1+s))-rho).ravel()
  h0=np.fft.ifftn(np.fft.fftn(rho)/(1+self.k2)).real;op=minimize(fg,h0.ravel(),jac=True,method='L-BFGS-B',options={'ftol':1e-14,'gtol':1e-8,'maxiter':1500})
  h=op.x.reshape(rho.shape);g=self.grad(h);s=np.sqrt(np.sum(g*g,axis=0));P=-g/(1+s);chi=1+.5*inv(h*h)
  return P,chi,dict(success=bool(op.success),residual=float(np.linalg.norm(fg(op.x)[1])/np.linalg.norm(rho)))
 def evaluate(self,x,P,chi):
  rho,flat,der=self.deposit(x);U,phi=self.gravity(rho);e=rho-self.div(P);h=e/chi;p=np.sqrt(np.sum(P*P,axis=0))
  if p.max()>=.985 or chi.min()<=.1:raise ValueError('field domain guard')
  W=-p-np.log1p(-p);gchi=self.grad(chi)
  E=U+self.vol*np.sum(.5*e*h+W+.5*self.a*(chi-1)**2+.5*self.d*np.sum(gchi*gchi,axis=0))
  ax=-np.sum((phi+h).ravel()[flat][:,:,None]*der,axis=1)
  aP=-(P/(1-p)+self.grad(h))/self.eta
  ac=(.5*h*h-self.a*(chi-1)+self.d*self.div(gchi))/self.b
  return E,ax,aP,ac,h,dict(max_p=float(p.max()),min_chi=float(chi.min()),max_chi=float(chi.max()),gravity=float(U))
 def kinetic(self,v,Pv,cv):return .5*self.m*np.sum(v*v)+.5*self.vol*(self.eta*np.sum(Pv*Pv)+self.b*np.sum(cv*cv))
 def damp(self,Pv,cv,dt):
  before=.5*self.vol*(self.eta*np.sum(Pv*Pv)+self.b*np.sum(cv*cv));fac=np.exp(-self.sg*dt);Pv=Pv*fac;cv=cv*fac
  after=.5*self.vol*(self.eta*np.sum(Pv*Pv)+self.b*np.sum(cv*cv));return Pv,cv,before-after
 def flux(self,Pv,cv,h,chi):
  gc=self.grad(chi);SP=np.array([np.roll(h,-1,axis=i)*Pv[i] for i in range(3)]);SC=np.array([-self.d*np.roll(cv,-1,axis=i)*gc[i] for i in range(3)])
  return np.array([self.vol*np.sum(self.mask*self.div(S)) for S in [SP,SC]])
 def partitions(self,x,v,h):
  groups=[]
  for link in [.25,.5,1.]:
   pairs=cKDTree(x).query_pairs(link,output_type='ndarray');ii=pairs[:,0] if len(pairs) else [];jj=pairs[:,1] if len(pairs) else [];graph=coo_matrix((np.ones(len(pairs)),(ii,jj)),shape=(len(x),len(x))).tocsr();num,labels=connected_components(graph,directed=False)
   count=np.bincount(labels);ix=np.argsort(count)[::-1];groups.append(dict(link=link,mass_fractions=(count[ix[:10]]/len(x)).tolist(),components_above_five_percent=int(np.sum(count>=.05*len(x)))))
  # Isolated softened Newtonian escape diagnostic, evaluated only at final state.
  phi=np.zeros(len(x))
  for start in range(0,len(x),128):
   rr=np.sqrt(np.sum((x[start:start+128,None,:]-x[None,:,:])**2,axis=2)+self.dx**2);weights=1/rr
   weights[np.arange(min(128,len(x)-start)),np.arange(start,min(start+128,len(x)))]=0;phi[start:start+128]=-self.m*np.sum(weights,axis=1)
  rad=np.linalg.norm(x,axis=1);spec=.5*np.sum(v*v,axis=1)+phi
  esc=(rad>2.5)&(np.sum(x*v,axis=1)>0)&(spec>0)
  return dict(fof=groups,candidate_newtonian_ejecta_fraction=float(np.mean(esc)),candidate_ejecta_count=int(sum(esc)),specific_energy_max=float(spec.max()))

def evolve(model,dt=.003,end=18,frozen=False):
 x=model.x0.copy();v=model.v0.copy();P,chi,init=model.static(x);Pv=np.zeros_like(P);cv=np.zeros_like(chi)
 pot,ax,aP,ac,h,diag=model.evaluate(x,P,chi);E0=pot+model.kinetic(v,Pv,cv);L0=model.m*np.sum(np.cross(x,v),axis=0);lost=0.;fluxint=np.zeros(2);lastflux=model.flux(Pv,cv,h,chi);rows=[];reason='time_limit';step=0
 try:
  for step in range(round(end/dt)+1):
   if step%max(1,round(.15/dt))==0 or step==round(end/dt):
    rad=np.linalg.norm(x,axis=1);L=model.m*np.sum(np.cross(x,v),axis=0)
    rows.append(dict(t=step*dt,energy_error=float((pot+model.kinetic(v,Pv,cv)+lost-E0)/abs(E0)),absorbed=float(lost),flux=fluxint.tolist(),mass_apertures=[float(np.mean(rad<r)) for r in [.5,1,2,2.5]],r50=float(np.median(rad)),rmax=float(max(rad)),L_relative_error=float(np.linalg.norm(L-L0)/max(np.linalg.norm(L0),1e-15)),momentum_norm=float(np.linalg.norm(model.m*v.sum(axis=0))),**diag))
   if step==round(end/dt):break
   if np.max(abs(x))>model.box/2-2*model.dx:reason='matter_boundary_guard';break
   Pv,cv,loss=model.damp(Pv,cv,dt/2);lost+=loss
   if not frozen:v+=dt*ax/2;x+=dt*v
   Pv+=dt*aP/2;cv+=dt*ac/2;P+=dt*Pv;chi+=dt*cv
   pot,ax,aP,ac,h,diag=model.evaluate(x,P,chi)
   if not frozen:v+=dt*ax/2
   Pv+=dt*aP/2;cv+=dt*ac/2;Pv,cv,loss=model.damp(Pv,cv,dt/2);lost+=loss
   now=model.flux(Pv,cv,h,chi);fluxint+=(lastflux+now)*dt/2;lastflux=now
 except ValueError as exc:reason=str(exc)
 return dict(parameters=dict(n=model.n,box=model.box,particles=len(x),mass=model.mass,dt=dt,end=end,frozen=frozen,a=model.a,b=model.b),initial=init,E0=float(E0),L0=L0.tolist(),stop_reason=reason,stop_time=step*dt,rows=rows,final_x=x.tolist(),final_v=v.tolist(),partition=model.partitions(x,v,h),max_energy_error=max(abs(r['energy_error']) for r in rows))
