import importlib.util
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
source=Path(__file__).resolve().parents[1]/'fragment_radiation_2026_10_22/model.py'
spec=importlib.util.spec_from_file_location('old',source);old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
class Model(old.Model):
 def __init__(self,n=8,amp=.001,zi=1100):
  self.n=n;self.eta=.005;self.a=.005;self.b=self.d=.125;self.amp=amp;self.zi=zi
  self.t0=.012074272908402984;self.ell=.0004404221297174536;self.M0=130257985.45037776;H0=67.4*1000/3.085677581491367e22*365.25*86400*1e9
  self.Hi=H0*np.sqrt(.315)*(1+zi)**1.5*self.t0;self.ti=2/(3*self.Hi);self.J0=1.5*self.Hi**2;self.fb=1/6.364;self.fc=1-self.fb
  rhom=.315*3*(67.4*1000/3.085677581491367e22)**2/(8*np.pi*6.67430e-11)*3.085677581491367e22**3/1.98847e30
  self.RL=(3*1.0952264e7/(4*np.pi*rhom))**(1/3);self.Lcom=2*np.pi*self.RL;self.box=self.Lcom/(1+zi)/self.ell;self.dx=self.box/n;self.vol=self.dx**3/(4*np.pi)
  self.mc=self.fc*self.J0*self.box**3/(4*np.pi*n**3);self.mb=self.fb*self.J0*self.box**3/(4*np.pi*n**3)
  k=4*np.sin(np.pi*np.fft.fftfreq(n))**2/self.dx**2;self.k2=k[:,None,None]+k[None,:,None]+k[None,None,:];self.safe=self.k2.copy();self.safe[0,0,0]=1
  grid=(np.arange(n)+.5)*self.dx-self.box/2;Q=np.array(np.meshgrid(grid,grid,grid,indexing='ij')).reshape(3,-1).T;k0=2*np.pi/self.box
  self.disp=-amp/(3*k0)*np.sin(k0*Q);self.x0=Q+self.disp
 def dep(self,x,m):self.m=m;return self.deposit(x)
 def fields(self,x,A=1):
  rho,_,_=self.dep(x,self.mc);rho=(rho-rho.mean())/A**3
  inv=lambda z:np.fft.ifftn(np.fft.fftn(z)/(self.a+self.d*self.k2/A**2)).real
  def fg(y):
   h=y.reshape(rho.shape);g=self.grad(h)/A;s=np.sqrt(np.sum(g*g,axis=0));zz=inv(h*h)
   return np.sum(.5*h*h+s-np.log1p(s)-rho*h+.125*h*h*zz),(h+.5*h*zz-self.div(g/(1+s))/A-rho).ravel()
  h0=np.fft.ifftn(np.fft.fftn(rho)/(1+self.k2/A**2)).real
  if np.linalg.norm(rho)<1e-12:return np.zeros((3,)+(rho.shape)),np.ones_like(rho),0.
  op=minimize(fg,h0.ravel(),jac=True,method='L-BFGS-B',options={'ftol':1e-14,'gtol':1e-9,'maxiter':1000});h=op.x.reshape(rho.shape);g=self.grad(h)/A;s=np.sqrt(np.sum(g*g,axis=0));return -g/(1+s),1+.5*inv(h*h),float(np.linalg.norm(fg(op.x)[1])/np.linalg.norm(rho))
 def evaluate(self,xc,xb,P,c,A,pc,pb,Q,V):
  rc,ic,dc=self.dep(xc,self.mc);rb,ib,db=self.dep(xb,self.mb);rc=(rc-rc.mean())/A**3;rb=(rb-rb.mean())/A**3
  phi=np.fft.ifftn(-A*A*np.fft.fftn(rc+rb)/self.safe).real;phi-=phi.mean();div=self.div(P)/A;e=rc-div;h=e/c;p=np.sqrt(np.sum(P*P,axis=0))
  if p.max()>=.985 or c.min()<=.1:raise ValueError('field_domain_guard')
  W=-p-np.log1p(-p);gc=self.grad(c)/A
  forcec=-np.sum((phi+h).ravel()[ic][:,:,None]*dc,axis=1);forceb=-np.sum(phi.ravel()[ib][:,:,None]*db,axis=1)
  forceP=-A**3*(P/(1-p)+self.grad(h)/A)/self.eta;forcechi=A**3*(.5*h*h-self.a*(c-1)+self.d*self.div(gc)/A)/self.b
  Tm=.5*(self.mc*np.sum(pc*pc)+self.mb*np.sum(pb*pb))/A**2;Tf=.5*self.vol*(self.eta*np.sum(Q*Q)+self.b*np.sum(V*V))/A**3
  Ug=.5*A**3*self.vol*np.sum((rc+rb)*phi);UW=A**3*self.vol*np.sum(W);Uc=.5*self.a*A**3*self.vol*np.sum((c-1)**2);Ugrad=.5*self.d*A**3*self.vol*np.sum(gc*gc);Um=.5*A**3*self.vol*np.sum(e*h)
  energy=Tm+Tf+Ug+UW+Uc+Ugrad+Um
  work=-2*Tm-3*Tf-Ug+3*(UW+Uc+Um)+Ugrad+A**3*self.vol*np.sum(h*(-3*rc+div))
  diag=dict(contrast_c_max=float(rc.max()/(self.fc*self.J0/A**3)),contrast_b_max=float(rb.max()/(self.fb*self.J0/A**3)),rms_c=float(np.sqrt(np.mean(rc**2))/(self.fc*self.J0/A**3)),Pmax=float(p.max()),chi_min=float(c.min()),chi_max=float(c.max()),cell_kpc=self.dx*A*self.ell*1000,energy=float(energy),energy_scale=float(Tm+Tf+abs(Ug)+UW+Uc+Ugrad+Um))
  return forcec,forceb,forceP,forcechi,energy,work,diag
 def groups(self,x,A):
  x=(x+self.box/2)%self.box;link=.2*self.dx;pairs=cKDTree(x,boxsize=self.box).query_pairs(link,output_type='ndarray');ii=pairs[:,0] if len(pairs) else [];jj=pairs[:,1] if len(pairs) else [];graph=coo_matrix((np.ones(len(pairs)),(ii,jj)),shape=(len(x),len(x))).tocsr();num,labels=connected_components(graph,directed=False);counts=np.bincount(labels)
  return dict(max_members=int(max(counts)),groups_ge32=int(sum(counts>=32)),particle_mass_Msun=self.mc*self.M0,core_radius_cells=.3214846542759978/(self.dx*A*self.ell*1000),link_comoving=link)

def evolve(n=8,amp=.001,zi=1100,zend=10,cfl=.6):
 m=Model(n,amp,zi);xc=m.x0.copy();xb=xc.copy();pc=m.Hi*m.disp.copy();pb=pc.copy();P,c,res=m.fields(xc);eps=1e-4;Pp,cp,rp=m.fields(xc+eps*m.disp,np.exp(eps));Pm,cm,rm=m.fields(xc-eps*m.disp,np.exp(-eps));Q=m.Hi*(Pp-Pm)/(2*eps);V=m.Hi*(cp-cm)/(2*eps)
 t=m.ti;end=m.ti*((1+zi)/(1+zend))**1.5;A=1.;state=m.evaluate(xc,xb,P,c,A,pc,pb,Q,V);E0=state[4];work=0.;rows=[];step=0;reason='endpoint';nextN=0;maxerr=0;maxscale=state[6]['energy_scale'];mass=m.mc*n**3
 try:
  while t<end*(1-1e-12):
   A=(t/m.ti)**(2/3);H=2/(3*t);fc,fb,fP,fchi,E,W,diag=state;maxscale=max(maxscale,diag['energy_scale']);err=abs(E-E0-work)/max(maxscale,1e-30);maxerr=max(maxerr,err)
   if np.log(A)>=nextN:
    rows.append(dict(z=(1+zi)/A-1,step=step,work_error=err,**diag,**m.groups(xc,A)));nextN+=.15
   dt=min(cfl*np.sqrt(m.eta)/np.sqrt(1+12/(A*m.dx)**2),.015/H,end-t)
   pc+=dt*fc/2;pb+=dt*fb/2;Q+=dt*fP/2;V+=dt*fchi/2
   tn=t+dt;An=(tn/m.ti)**(2/3);I2=3*m.ti**(4/3)*(t**(-1/3)-tn**(-1/3));I3=m.ti**2*(1/t-1/tn)
   xc+=pc*I2;xb+=pb*I2;xc=(xc+m.box/2)%m.box-m.box/2;xb=(xb+m.box/2)%m.box-m.box/2;P+=Q*I3;c+=V*I3
   mid=m.evaluate(xc,xb,P,c,An,pc,pb,Q,V);pc+=dt*mid[0]/2;pb+=dt*mid[1]/2;Q+=dt*mid[2]/2;V+=dt*mid[3]/2
   state=m.evaluate(xc,xb,P,c,An,pc,pb,Q,V);work+=.5*(W+state[5])*np.log(An/A);t=tn;step+=1
 except ValueError as e:reason=str(e)
 A=(t/m.ti)**(2/3);diag=state[6];err=abs(state[4]-E0-work)/max(maxscale,diag['energy_scale'],1e-30);maxerr=max(maxerr,err);rows.append(dict(z=(1+zi)/A-1,step=step,work_error=err,**diag,**m.groups(xc,A)))
 return dict(parameters=dict(n=n,amp=amp,zi=zi,zend=zend,cfl=cfl,cold_box_mass_Msun=mass*m.M0,Lcom_Mpc=m.Lcom),initial_residuals=[res,rp,rm],reason=reason,steps=step,max_work_error=maxerr,rows=rows,final_x_c=xc.tolist(),final_pc=pc.tolist())
