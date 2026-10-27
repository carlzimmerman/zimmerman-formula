import numpy as np
from radial_base import Radial
class Hydro(Radial):
 def __init__(self,n=256,amp=.05,zi=1100,size=1,ratio=1,xe=2e-4):
  super().__init__(n,amp,zi,size);self.gamma=5/3;self.xe=xe;self.ratio=ratio;self.area=(np.arange(n+1)*self.dx)**2
  self.vunit=self.ell*3.085677581491367e19/(self.t0*1e9*365.25*86400);self.kT=1.380649e-23/(1.22*1.67262192369e-27*self.vunit**2)
 def initial_gas(self):
  xb=self.r+self.ratio*self.disp;rho,ids,_=self.dep(xb,self.mb)
  # Same deposition for mass and momentum; recover TSC weights from a unit-mass deposition algebra.
  u=xb/self.dx-.5;j=np.floor(u+.5).astype(int);dist=u[:,None]-(j[:,None]+np.array([-1,0,1]));ad=abs(dist);w=np.where(ad<.5,.75-dist*dist,.5*(1.5-ad)**2)
  momentum=np.bincount(ids.ravel(),weights=(self.mb[:,None]*w*(self.Hi*self.ratio*self.disp)[:,None]).ravel(),minlength=self.n)/self.vol
  E=rho*self.kT*(2.725*(1+self.zi))/(self.gamma-1)+.5*momentum**2/rho
  return np.array([rho,momentum,E])
 def primitive(self,U):
  rho,j,E=U
  if min(rho)<=0:raise ValueError('gas_density')
  v=j/rho;p=(self.gamma-1)*(E-.5*j*v)
  if min(p)<=0:raise ValueError('gas_pressure')
  return rho,v,p,np.sqrt(self.gamma*p/rho)
 def gravity(self,xc,U,A):
  rc,ic,dc=self.dep(xc,self.mc);dr=(rc+U[0]-(self.mc.sum()+self.mb.sum())/self.vol.sum())/A**3
  g=A*A*np.cumsum(dr*self.vol)[:-1]/self.edge**2;phi=np.r_[-np.cumsum((g*self.dx)[::-1])[::-1],0.];phi-=np.sum(phi*self.vol)/sum(self.vol)
  return rc,ic,dc,dr,g,phi
 def gas_rhs(self,U,A,H,gradphi):
  rho,v,p,cs=self.primitive(U);left=np.column_stack((U[:,0]*np.array([1,-1,1]),U));right=np.column_stack((U,U[:,-1]*np.array([1,-1,1])))
  rl,vl,pl,cl=self.primitive(left);rr,vr,pr,cr=self.primitive(right)
  fl=np.array([rl*vl,rl*vl*vl+pl,(left[2]+pl)*vl]);fr=np.array([rr*vr,rr*vr*vr+pr,(right[2]+pr)*vr]);speed=np.maximum(abs(vl)+cl,abs(vr)+cr)
  flux=.5*(fl+fr)-.5*speed*(right-left)
  rhs=-np.diff(self.area*flux,axis=1)/(A*self.vol)
  rhs[1]+=p*np.diff(self.area)/(A*self.vol)-H*U[1]
  g=np.r_[0,gradphi,0.];gc=.5*(g[:-1]+g[1:]);rhs[1]-=rho*gc/A
  # Face mass-flux work matches the finite-volume variation of gravitational potential energy.
  gw=self.area*flux[0]*g*self.dx/A;rhs[2]-=.5*(gw[:-1]+gw[1:])/self.vol
  rhs[2]-=H*(rho*v*v+3*p)
  zp=(1+self.zi)/A;rate=8.55e-13*self.xe*zp**4*1e9*self.t0;T=p/(rho*self.kT);heat=rho*self.kT/(self.gamma-1)*rate*(2.725*zp-T);rhs[2]+=heat
  return rhs,float(np.sum(self.vol*heat))
 def gas_step(self,U,xc,t,dt):
  # SSP RK2 at actual substep endpoints.
  A=(t/self.ti)**(2/3);g=self.gravity(xc,U,A)[4];f,h0=self.gas_rhs(U,A,2/(3*t),g);trial=U+dt*f;self.primitive(trial)
  tn=t+dt;An=(tn/self.ti)**(2/3);gn=self.gravity(xc,trial,An)[4];fn,h1=self.gas_rhs(trial,An,2/(3*tn),gn);out=.5*(U+trial+dt*fn);self.primitive(out)
  return out,dt*(h0+h1)/2
 def fields(self,xc,U,P,c,A,pc,Q,V):
  rc,ic,dc,dr,g,phi=self.gravity(xc,U,A);rc=(rc-self.mc.sum()/sum(self.vol))/A**3;div=self.div(P)/A;e=rc-div;h=e/c;p=abs(P)
  if max(p)>=.985 or min(c)<=.1:raise ValueError('field_domain')
  fc=-np.sum((phi+h)[ic]*dc,axis=1);fP=-A**3*(P/(1-p)+self.grad(h)/A)/self.eta;fchi=A**3*(.5*h*h-self.alpha*(c-1)+self.d*self.div(self.grad(c))/A**2)/self.b
  Tc=.5*np.sum(self.mc*pc**2)/A**2;Tf=.5*(self.eta*np.sum(self.ev*Q**2)+self.b*np.sum(self.vol*V**2))/A**3;Ug=.5*A**3*np.sum(self.vol*dr*phi);UW=A**3*np.sum(self.ev*(-p-np.log1p(-p)));Uchi=.5*self.alpha*A**3*np.sum(self.vol*(c-1)**2);Ugrad=.5*self.d*A*np.sum(self.ev*self.grad(c)**2);Um=.5*A**3*np.sum(self.vol*e*h);gasE=np.sum(self.vol*U[2])
  energy=Tc+Tf+Ug+UW+Uchi+Ugrad+Um+gasE
  work=-2*(Tc+gasE)-3*Tf-Ug+3*(UW+Uchi+Um)+Ugrad+A**3*np.sum(self.vol*h*(-3*rc+div))
  rho,v,pr,cs=self.primitive(U);T=pr/(rho*self.kT);mean=self.mb.sum()/sum(self.vol)
  diag=dict(peak_delta_c=float(max(rc)/(self.fc*self.J/A**3)),peak_delta_b=float(max(rho/mean-1)),Tmin_K=float(min(T)),Tmax_K=float(max(T)),Pmax=float(max(p)),chi_min=float(min(c)),cell_kpc=self.dx*A*self.ell,energy=float(energy),scale=float(Tc+Tf+abs(Ug)+UW+Uchi+Ugrad+Um+gasE),gas_mass_error=float(abs(np.sum(rho*self.vol)/sum(self.mb)-1)))
  return fc,fP,fchi,energy,work,diag
 def diagnostics(self,xc,U,A):
  rc=self.dep(xc,self.mc)[0];edge=np.arange(self.n+1)*self.dx;out={}
  for rk in [.16,.3214846542759978,.64,1.28]:
   cut=rk/(A*self.ell);w=np.maximum(0,np.minimum(edge[1:],cut)**3-np.minimum(edge[:-1],cut)**3)/3;out[str(rk)]={'cold':float(np.sum(rc*w)*self.M0),'baryon':float(np.sum(U[0]*w)*self.M0)}
  return dict(aperture_mass_Msun=out,cold_shell_inversions=int(sum(np.diff(xc)<0)),cold_rmin_kpc=float(min(xc)*A*self.ell))

def evolve(n=256,amp=.05,zend=10,ratio=1,xe=2e-4,cfl=.6):
 m=Hydro(n,amp,ratio=ratio,xe=xe);xc=m.x0.copy();pc=m.Hi*m.disp.copy();U=m.initial_gas();P,c,res=m.static(xc);eps=1e-4;pp,cp,rp=m.static(xc+eps*m.disp,np.exp(eps));pm,cm,rm=m.static(xc-eps*m.disp,np.exp(-eps));Q=m.Hi*(pp-pm)/(2*eps);V=m.Hi*(cp-cm)/(2*eps)
 t=m.ti;end=t*(1101/(1+zend))**1.5;A=1;state=m.fields(xc,U,P,c,A,pc,Q,V);E0=state[3];work=heat=0.;maxscale=state[5]['scale'];maxerr=0.;rows=[];nextN=0.;steps=0;reason='endpoint'
 try:
  while t<end*(1-1e-12):
   A=(t/m.ti)**(2/3);H=2/(3*t);rho,v,p,cs=m.primitive(U);rate=8.55e-13*xe*(1101/A)**4*1e9*m.t0
   err=abs(state[3]-E0-work-heat)/max(maxscale,1e-30);maxerr=max(maxerr,err)
   if np.log(A)>=nextN:rows.append(dict(z=1101/A-1,step=steps,work_heat_error=err,**state[5],**m.diagnostics(xc,U,A)));nextN+=.15
   dt=min(cfl*np.sqrt(m.eta)/np.sqrt(1+6/(A*m.dx)**2),.3*A*m.dx/max(abs(v)+cs),.1/max(rate,1e-30),.01/H,end-t)
   # Commit only a complete successful split step; old state remains valid if a trial fails.
   Um,h1=m.gas_step(U,xc,t,dt/2);s=m.fields(xc,Um,P,c,A,pc,Q,V);pcn=pc+dt*s[0]/2;Qn=Q+dt*s[1]/2;Vn=V+dt*s[2]/2;tn=t+dt;An=(tn/m.ti)**(2/3);I2=3*m.ti**(4/3)*(t**(-1/3)-tn**(-1/3));I3=m.ti**2*(1/t-1/tn)
   xn=xc+pcn*I2;neg=xn<0;xn[neg]*=-1;pcn[neg]*=-1
   if max(xn)>m.R:raise ValueError('cold_boundary')
   Pn=P+Qn*I3;cn=c+Vn*I3;s=m.fields(xn,Um,Pn,cn,An,pcn,Qn,Vn);pcn+=dt*s[0]/2;Qn+=dt*s[1]/2;Vn+=dt*s[2]/2
   Un,h2=m.gas_step(Um,xn,t+dt/2,dt/2);sn=m.fields(xn,Un,Pn,cn,An,pcn,Qn,Vn)
   work+=.5*(state[4]+sn[4])*np.log(An/A);heat+=h1+h2;xc,pc,P,c,Q,V,U=xn,pcn,Pn,cn,Qn,Vn,Un;t=tn;state=sn;maxscale=max(maxscale,state[5]['scale']);steps+=1
 except ValueError as e:reason=str(e)
 A=(t/m.ti)**(2/3);err=abs(state[3]-E0-work-heat)/max(maxscale,1e-30);maxerr=max(maxerr,err);rows.append(dict(z=1101/A-1,step=steps,work_heat_error=err,**state[5],**m.diagnostics(xc,U,A)))
 return dict(parameters=dict(n=n,amp=amp,zend=zend,ratio=ratio,xe=xe,cfl=cfl),reason=reason,initial_residuals=[res,rp,rm],max_work_heat_error=maxerr,energy0=E0,expansion_work=work,compton_heat=heat,rows=rows,final=dict(xc=xc.tolist(),pc=pc.tolist(),U=U.tolist(),P=P.tolist(),chi=c.tolist(),Q=Q.tolist(),V=V.tolist(),time=t))
