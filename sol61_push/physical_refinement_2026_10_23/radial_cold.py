import numpy as np
from scipy.optimize import minimize
from scipy.sparse import diags,bmat
from scipy.sparse.linalg import factorized,spsolve
class Radial:
 def __init__(self,n=256,amp=.03,zi=1100,size=1):
  self.n=n;self.eta=.005;self.alpha=.005;self.b=self.d=.125;self.amp=amp;self.zi=zi;self.size=size;self.ell=.4404221297174536;self.t0=.012074272908402984;self.M0=130257985.45037776
  H0=67.4*1000/3.085677581491367e22*365.25*86400*1e9;self.Hi=H0*np.sqrt(.315)*(1+zi)**1.5*self.t0;self.ti=2/(3*self.Hi);self.J=1.5*self.Hi**2;self.fb=0.;self.fc=1.
  self.RL=.04037934389859046;self.R=1000*np.pi*self.RL*size/(1+zi)/self.ell;self.dx=self.R/n;edge=np.arange(n+1)*self.dx;self.r=(edge[:-1]+edge[1:])/2;self.vol=(edge[1:]**3-edge[:-1]**3)/3;self.edge=edge[1:-1];self.ev=self.edge**2*self.dx
  off=np.ones(n-1)*.125;diag=np.ones(n)*.75;diag[0]=diag[-1]=.875;assign=diags([off,diag,off],[-1,0,1],format='csc');mass=factorized(assign)(self.J*self.vol);assert min(mass)>0
  self.mc=mass*self.fc;self.mb=mass*self.fb;k=np.pi/self.R;self.disp=-amp*np.sin(k*self.r)/(3*k);self.x0=self.r+self.disp
  right=self.edge**2/self.dx;diagonal=np.zeros(n);diagonal[:-1]-=right/self.vol[:-1];diagonal[1:]-=right/self.vol[1:];self.lap=diags([right/self.vol[1:],diagonal,right/self.vol[:-1]],[-1,0,1],format='csc')
 def grad(self,x):return np.diff(x)/self.dx
 def div(self,x):
  f=np.zeros(self.n+1);f[1:-1]=self.edge**2*x;return np.diff(f)/self.vol
 def dep(self,x,m):
  u=x/self.dx-.5;j=np.floor(u+.5).astype(int);ids=j[:,None]+np.array([-1,0,1]);dist=u[:,None]-ids;ad=abs(dist);w=np.where(ad<.5,.75-dist*dist,.5*(1.5-ad)**2);dw=np.where(ad<.5,-2*dist,-(1.5-ad)*np.sign(dist))/self.dx
  ids=np.where(ids<0,-ids-1,ids);ids=np.where(ids>=self.n,2*self.n-ids-1,ids)
  if ids.min()<0 or ids.max()>=self.n:raise ValueError('matter_boundary')
  rho=np.bincount(ids.ravel(),weights=(m[:,None]*w).ravel(),minlength=self.n)/self.vol;return rho,ids,dw
 def static(self,x,A=1):
  rho,_,_=self.dep(x,self.mc);rho=(rho-self.mc.sum()/self.vol.sum())/A**3;I=diags(np.ones(self.n),format='csc');B=self.alpha*I-self.d*self.lap/A**2;inv=factorized(B);h=spsolve(I-self.lap/A**2,rho);chi=1+.5*inv(h*h)
  def residual(h,chi):
   g=self.grad(h)/A;return chi*h-self.div(g/(1+abs(g)))/A-rho,B@(chi-1)-.5*h*h
  norm=lambda f:np.sqrt(np.sum(self.vol*f*f))
  for it in range(30):
   f1,f2=residual(h,chi);err=max(norm(f1)/max(norm(rho),1e-30),norm(f2)/max(norm(.5*h*h),1e-30))
   if err<1e-10:break
   g=self.grad(h)/A;right=self.edge**2/(self.dx*A*A)/(1+abs(g))**2;diag=np.zeros(self.n);diag[:-1]-=right/self.vol[:-1];diag[1:]-=right/self.vol[1:];lap=diags([right/self.vol[1:],diag,right/self.vol[:-1]],[-1,0,1],format='csc');H=diags(h,format='csc');jac=bmat([[diags(chi)-lap,H],[-H,B]],format='csc');delta=spsolve(jac,-np.r_[f1,f2]);fac=1.
   old=norm(f1)+norm(f2)
   for back in range(20):
    hh=h+fac*delta[:self.n];cc=chi+fac*delta[self.n:];fnew=residual(hh,cc)
    if min(cc)>.1 and norm(fnew[0])+norm(fnew[1])<=old:break
    fac*=.5
   h=hh;chi=cc
  f1,f2=residual(h,chi);res=norm(f1)/max(norm(rho),1e-30);g=self.grad(h)/A
  return -g/(1+abs(g)),chi,float(res)
 def evaluate(self,xc,xb,P,c,A,pc,pb,Q,V):
  rc,ic,dc=self.dep(xc,self.mc);rb,ib,db=self.dep(xb,self.mb);rc=(rc-self.mc.sum()/self.vol.sum())/A**3;rb=(rb-self.mb.sum()/self.vol.sum())/A**3
  gradphi=A*A*np.cumsum((rc+rb)*self.vol)[:-1]/self.edge**2;phi=np.r_[-np.cumsum((gradphi*self.dx)[::-1])[::-1],0.];phi-=np.sum(phi*self.vol)/np.sum(self.vol)
  div=self.div(P)/A;e=rc-div;h=e/c;p=abs(P)
  if p.max()>=.985 or c.min()<=.1:raise ValueError('field_domain')
  W=-p-np.log1p(-p);gc=self.grad(c)/A;fc=-np.sum((phi+h)[ic]*dc,axis=1);fb=-np.sum(phi[ib]*db,axis=1);fP=-A**3*(P/(1-p)+self.grad(h)/A)/self.eta;fchi=A**3*(.5*h*h-self.alpha*(c-1)+self.d*self.div(gc)/A)/self.b
  Tm=.5*(np.sum(self.mc*pc*pc)+np.sum(self.mb*pb*pb))/A**2;Tf=.5*(self.eta*np.sum(self.ev*Q*Q)+self.b*np.sum(self.vol*V*V))/A**3;Ug=.5*A**3*np.sum(self.vol*(rc+rb)*phi);UW=A**3*np.sum(self.ev*W);Uc=.5*self.alpha*A**3*np.sum(self.vol*(c-1)**2);Ugchi=.5*self.d*A**3*np.sum(self.ev*gc*gc);Um=.5*A**3*np.sum(self.vol*e*h)
  energy=Tm+Tf+Ug+UW+Uc+Ugchi+Um;work=-2*Tm-3*Tf-Ug+3*(UW+Uc+Um)+Ugchi+A**3*np.sum(self.vol*h*(-3*rc+div))
  return (fc,fb,fP,fchi,energy,work,dict(peak_delta_c=float(max(rc)/(self.fc*self.J/A**3)),peak_delta_b=float(max(rb)/(self.fb*self.J/A**3)),Pmax=float(max(p)),chi_min=float(min(c)),chi_max=float(max(c)),energy=float(energy),scale=float(Tm+Tf+abs(Ug)+UW+Uc+Ugchi+Um),cell_kpc=self.dx*A*self.ell))
 def mass_diagnostics(self,x,A):
  R=x*A*self.ell;res={}
  for rad in [.16,.3214846542759978,.64,1.28]:res[str(rad)]=float(np.sum(self.mc[R<rad])*self.M0)
  return dict(cold_mass_apertures_Msun=res,rmin_kpc=float(min(R)),shell_crossings=int(np.sum(np.diff(x)<0)))

def evolve(n=256,amp=.03,zi=1100,zend=10,size=1,cfl=.6):
 m=Radial(n,amp,zi,size);xc=m.x0.copy();xb=xc.copy();pc=m.Hi*m.disp.copy();pb=pc.copy();P,c,res=m.static(xc);eps=1e-4;Pp,cp,rp=m.static(xc+eps*m.disp,np.exp(eps));Pm,cm,rm=m.static(xc-eps*m.disp,np.exp(-eps));Q=m.Hi*(Pp-Pm)/(2*eps);V=m.Hi*(cp-cm)/(2*eps)
 t=m.ti;end=t*((1+zi)/(1+zend))**1.5;A=1;state=m.evaluate(xc,xb,P,c,A,pc,pb,Q,V);E0=state[4];work=0.;rows=[];step=0;nextN=0;maxscale=state[6]['scale'];maxerr=0;reason='endpoint';reflections=0
 try:
  while t<end*(1-1e-12):
   A=(t/m.ti)**(2/3);H=2/(3*t);fc,fb,fP,fchi,E,W,d=state;maxscale=max(maxscale,d['scale']);err=abs(E-E0-work)/max(maxscale,1e-30);maxerr=max(maxerr,err)
   if np.log(A)>=nextN:
    rows.append(dict(z=(1+zi)/A-1,step=step,work_error=err,**d,**m.mass_diagnostics(xc,A)));nextN+=.15
   dt=min(cfl*np.sqrt(m.eta)/np.sqrt(1+6/(A*m.dx)**2),.01/H,end-t);pc+=dt*fc/2;pb+=dt*fb/2;Q+=dt*fP/2;V+=dt*fchi/2;tn=t+dt;An=(tn/m.ti)**(2/3);I2=3*m.ti**(4/3)*(t**(-1/3)-tn**(-1/3));I3=m.ti**2*(1/t-1/tn)
   xc+=pc*I2;xb+=pb*I2
   for x,v in [(xc,pc),(xb,pb)]:
    neg=x<0;reflections+=int(sum(neg));x[neg]*=-1;v[neg]*=-1
    if max(x)>m.R:raise ValueError('matter_outer_boundary')
   P+=Q*I3;c+=V*I3;mid=m.evaluate(xc,xb,P,c,An,pc,pb,Q,V);pc+=dt*mid[0]/2;pb+=dt*mid[1]/2;Q+=dt*mid[2]/2;V+=dt*mid[3]/2;state=m.evaluate(xc,xb,P,c,An,pc,pb,Q,V);work+=.5*(W+state[5])*np.log(An/A);t=tn;step+=1
 except ValueError as e:reason=str(e)
 A=(t/m.ti)**(2/3);d=state[6];err=abs(state[4]-E0-work)/max(maxscale,d['scale'],1e-30);maxerr=max(maxerr,err);rows.append(dict(z=(1+zi)/A-1,step=step,work_error=err,**d,**m.mass_diagnostics(xc,A)))
 return dict(parameters=dict(n=n,amp=amp,zi=zi,zend=zend,size=size,cfl=cfl,cold_mass_Msun=float(m.mc.sum()*m.M0)),reason=reason,initial_residuals=[res,rp,rm],rows=rows,max_work_error=float(maxerr),reflections=reflections,final=dict(xc=xc.tolist(),xb=xb.tolist(),pc=pc.tolist(),pb=pb.tolist(),P=P.tolist(),chi=c.tolist(),Q=Q.tolist(),V=V.tolist(),time=t))
