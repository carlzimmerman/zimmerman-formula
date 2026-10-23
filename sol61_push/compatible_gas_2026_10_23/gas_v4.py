"""Spherical moving-volume gas; variational mesh gravity, compatible pressure work.
Time integration is RK4, NOT exactly energy conserving. Residual is measured.
"""
import numpy as np
from radial_base import Radial

def rates(T,n):
 T=np.maximum(T,10.);x=np.log10(T);t=T/1000
 low=10**(-103+97.59*x-48.05*x*x+10.80*x**3-.9032*x**4)
 lte=9.5e-22*t**3.76/(1+.12*t**2.1)*np.exp(-(.13/t)**3)+3e-24*np.exp(-.51/t)+6.7e-19*np.exp(-5.86/t)+1.6e-18*np.exp(-11.7/t)
 return low,lte,(n*low)*lte/(n*low+lte+1e-300)

class Gas(Radial):
 def __init__(self,n=128,amp=.05,size=1,ratio=1,fmol=.001,xe=2e-4,visc=2.):
  super().__init__(n,amp,size=size);self.gamma=5/3;self.ratio=ratio;self.fmol=fmol;self.xe=xe;self.visc=visc
  self.edges=np.arange(n+1)*self.dx;self.ygrid=self.edges**3/3
  self.mgas=self.fb*self.J*self.vol;self.mnode=.5*(self.mgas[:-1]+self.mgas[1:]);self.cumm=np.r_[0,np.cumsum(self.mgas)]
  self.vunit=self.ell*3.085677581491367e19/(self.t0*1e9*365.25*86400);self.kT=1.380649e-23/(1.22*1.67262192369e-27*self.vunit**2)
  self.runit=self.M0*1.98847e30/(4*np.pi*(self.ell*3.085677581491367e19)**3);self.seconds=self.t0*1e9*365.25*86400
  lens=[n,n,n-1,n-1,n-1,n-1,n,n,n,1,1];c=np.r_[0,np.cumsum(lens)];self.sl=[slice(c[i],c[i+1]) for i in range(len(lens))]
 def unpack(self,y):return [y[s] for s in self.sl]
 def initial(self):
  disp=-self.amp*np.sin(np.pi*self.edge/self.R)/(3*np.pi/self.R)*self.ratio
  P,c,r=self.static(self.x0);eps=1e-4;pp,cp,rp=self.static(self.x0+eps*self.disp,np.exp(eps));pm,cm,rm=self.static(self.x0-eps*self.disp,np.exp(-eps))
  self.initial_residuals=[r,rp,rm]
  return np.concatenate([self.x0,self.Hi*self.disp,self.edge+disp,self.Hi*disp,P,self.Hi*(pp-pm)/(2*eps),c,self.Hi*(cp-cm)/(2*eps),np.full(self.n,self.kT*2.725*1101/(self.gamma-1)),[0],[0]])
 def gasgrid(self,b):
  faces=np.r_[0,b,self.R];vol=np.diff(faces**3)/3
  if min(vol)<=0:raise ValueError('gas_crossing')
  rb=np.diff(np.interp(self.ygrid,faces**3/3,self.cumm))/self.vol
  return faces,vol,rb
 def eval(self,t,y,frozen=False):
  xc,pc,b,pb,P,Q,c,V,u,work,heat=self.unpack(y);A=1. if frozen else (t/self.ti)**(2/3);H=0. if frozen else 2/(3*t)
  if max(abs(xc))>self.R:raise ValueError('cold_boundary')
  if min(u)<=0:raise ValueError('thermal_positivity')
  faces,vol,rb=self.gasgrid(b);rc,ic,dc=self.dep(xc,self.mc);dr=(rc+rb-self.J)/A**3
  g=A*A*np.cumsum(dr*self.vol)[:-1]/self.edge**2;phi=np.r_[-np.cumsum((g*self.dx)[::-1])[::-1],0.];phi-=np.sum(phi*self.vol)/np.sum(self.vol)
  primitive=np.r_[0,np.cumsum(phi*self.vol)];avg=np.diff(np.interp(faces**3/3,self.ygrid,primitive))/vol
  at=phi[np.minimum(np.searchsorted(self.edges,b,side='right')-1,self.n-1)];rho=self.mgas/vol
  gb=-b*b*(rho[:-1]*(at-avg[:-1])+rho[1:]*(avg[1:]-at))/self.mnode
  vel=np.r_[0,pb/A**2,0];vdot=np.diff(faces**2*vel);theta=3*H+vdot/vol;cs=np.sqrt(self.gamma*(self.gamma-1)*u)
  dv=np.diff(H*A*faces+A*vel);comp=np.where(theta<0,np.maximum(-dv,0),0)
  q=rho/A**3*self.visc*comp**2
  pressure=(self.gamma-1)*rho/A**3*u
  fp=A**3*b*b*np.diff(-(pressure+q))/self.mnode
  # Identical pressure and viscosity in force and thermal work.
  du=-(self.gamma-1)*u*theta-q/(rho/A**3)*theta
  T=(self.gamma-1)*u/self.kT;nh=.76*rho/A**3*self.runit/1.67262192369e-27/1e6
  z=1101/A-1;comp_rate=8.55e-13*self.xe*(1+z)**4*1e9*self.t0
  source=self.kT/(self.gamma-1)*comp_rate*(2.725*(1+z)-T)
  if self.fmol and z<=100:
   if max(T)>1e4 or max(nh)>1e7:raise ValueError('cooling_model_domain')
   cool=self.fmol*nh*np.maximum(rates(T,nh)[2]-rates(np.full(self.n,2.725*(1+z)),nh)[2],0)*.1 # erg/cm3/s -> J/m3/s
   source-=cool/(rho/A**3*self.runit)*self.seconds/self.vunit**2
  du+=source
  rcp=(rc-self.fc*self.J)/A**3;div=self.div(P)/A;e=rcp-div;h=e/c;p=abs(P)
  if max(p)>=.985 or min(c)<=.1:raise ValueError('field_domain')
  fc=-np.sum((phi+h)[ic]*dc,axis=1);fP=-A**3*(P/(1-p)+self.grad(h)/A)/self.eta;fV=A**3*(.5*h*h-self.alpha*(c-1)+self.d*self.div(self.grad(c))/A**2)/self.b
  Tc=.5*np.sum(self.mc*pc**2)/A**2;Tb=.5*np.sum(self.mnode*pb**2)/A**2;U=np.sum(self.mgas*u)
  Tf=.5*(self.eta*np.sum(self.ev*Q**2)+self.b*np.sum(self.vol*V**2))/A**3;Ug=.5*A**3*np.sum(self.vol*dr*phi)
  UW=A**3*np.sum(self.ev*(-p-np.log1p(-p)));Uc=.5*self.alpha*A**3*np.sum(self.vol*(c-1)**2);Ugrad=.5*self.d*A*np.sum(self.ev*self.grad(c)**2);Um=.5*A**3*np.sum(self.vol*e*h)
  E=Tc+Tb+U+Tf+Ug+UW+Uc+Ugrad+Um;scale=Tc+Tb+U+Tf+abs(Ug)+UW+Uc+Ugrad+Um
  W=-2*(Tc+Tb+U)-3*Tf-Ug+3*(UW+Uc+Um)+Ugrad+A**3*np.sum(self.vol*h*(-3*rcp+div))
  # Bulk viscosity does work against background expansion as well as peculiar flow.
  W-=3*A**3*np.sum(vol*q)
  dh=np.sum(self.mgas*source)
  dy=np.concatenate([pc/A**2,fc,pb/A**2,gb+fp,Q/A**3,fP,V/A**3,fV,du,[W*H],[dh]])
  diag=dict(z=z,energy=E,scale=scale,work=float(work[0]),heat=float(heat[0]),nHmax=float(max(nh)),Tmax=float(max(T)),Tmin=float(min(T)),Pmax=float(max(p)),chi_min=float(min(c)),field_cell_kpc=A*self.ell*self.dx,gas_min_width_kpc=float(min(np.diff(faces))*A*self.ell),cold_rmin_kpc=float(min(abs(xc))*A*self.ell),cold_inversions=int(np.sum(np.diff(abs(xc))<0)),peak_c=float(max(rc/(self.fc*self.J)-1)),peak_b=float(max(rho/(self.fb*self.J)-1)),positive_field_energy=Tf+UW+Uc+Ugrad+Um)
  for rad in [.16,.3214846542759978,.64,1.28]:
   cut=rad/(A*self.ell);weights=np.diff(np.minimum(self.edges,cut)**3)/3
   diag['mass_'+str(rad)]={'cold':float(np.sum(rc*weights)*self.M0),'gas':float(np.interp(cut**3/3,faces**3/3,self.cumm)*self.M0)}
  # Gas/cold core radii here are fixed enclosed mass fractions, not identified remnants.
  diag['gas_r001_kpc']=float(np.interp(.001*self.cumm[-1],self.cumm,faces)*A*self.ell)
  dtgas=.15*min(A*np.diff(faces)/(cs+comp+1e-30));dtthermal=.1*min(u/(abs(source)+1e-30))
  return dy,diag,min(dtgas,dtthermal)

def run(n=128,zend=10,amp=.05,size=1,ratio=1,fmol=.001,cfl=.5,visc=2.,maxsteps=250000,resume=None):
 m=Gas(n,amp,size,ratio,fmol,visc=visc);y=m.initial();t=m.ti;end=t*(1101/(1+zend))**1.5;prior=None
 if resume:
  import json
  prior=json.load(open(resume))
  for key,val in dict(n=n,amp=amp,size=size,ratio=ratio,fmol=fmol,visc=visc).items():
   if prior['parameters'][key]!=val:raise ValueError('resume_parameter_mismatch_'+key)
  y=np.array(prior['final']['state']);t=prior['final']['time']
 k,d,dtg=m.eval(t,y);E0=d['energy'] if prior is None else prior['energy0'];scale=d['scale'] if prior is None else max(r['scale'] for r in prior['rows']);rows=[] if prior is None else prior['rows'][:];nextN=np.log((t/m.ti)**(2/3));steps=0 if prior is None else prior['rows'][-1]['step'];reason='endpoint';maxerr=0 if prior is None else prior['max_absolute_defect']
 try:
  while t<end*(1-1e-12):
   A=(t/m.ti)**(2/3);err=d['energy']-E0-d['work']-d['heat'];scale=max(scale,d['scale']);maxerr=max(maxerr,abs(err));d.update(defect=err,relative_defect=abs(err)/scale,step=steps)
   if np.log(A)>=nextN:rows.append(d.copy());nextN+=.12
   dt=min(cfl*np.sqrt(m.eta)/np.sqrt(1+6/(A*m.dx)**2),dtg*cfl/.5,.01*t,end-t)
   k2=m.eval(t+dt/2,y+dt*k/2)[0];k3=m.eval(t+dt/2,y+dt*k2/2)[0];k4=m.eval(t+dt,y+dt*k3)[0];yn=y+dt*(k+2*k2+2*k3+k4)/6
   kn,dn,dtgn=m.eval(t+dt,yn);y=yn;t+=dt;k,d,dtg=kn,dn,dtgn;steps+=1
   if steps>=maxsteps:reason='step_budget';break
 except ValueError as exc:reason=str(exc)
 err=d['energy']-E0-d['work']-d['heat'];scale=max(scale,d['scale']);d.update(defect=err,relative_defect=abs(err)/scale,step=steps);rows.append(d)
 return dict(parameters=dict(n=n,zend=zend,amp=amp,size=size,ratio=ratio,fmol=fmol,cfl=cfl,visc=visc),reason=reason,initial_residuals=m.initial_residuals,energy0=E0,max_absolute_defect=max(maxerr,abs(err)),rows=rows,final=dict(time=t,state=y.tolist()))
if __name__=='__main__':
 import argparse,json
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--n',type=int,default=128);p.add_argument('--zend',type=float,default=10);p.add_argument('--fmol',type=float,default=.001);p.add_argument('--cfl',type=float,default=.5);p.add_argument('--ratio',type=float,default=1);p.add_argument('--amp',type=float,default=.05);p.add_argument('--size',type=float,default=1);p.add_argument('--visc',type=float,default=2.);p.add_argument('--resume')
 a=vars(p.parse_args());out=a.pop('output');r=run(**a);open(out,'w').write(json.dumps(r,indent=2,default=lambda x:x.item()));print(r['reason'],r['rows'][-1])
