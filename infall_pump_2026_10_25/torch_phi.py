"""Forward automatic differentiation of the independently written local residual.

Colors compress derivatives only; no finite differences or physical model
approximation. Compare this residual with the NumPy implementation at each use.
"""
import numpy as np
import torch
from scipy.sparse import csc_matrix

class ForwardJacobian:
 def __init__(self,m):
  self.m=m;self.n=m.n;self.N=9*m.n+len(m.wr);self.const={}
  for name in ['r','vol','w','tt','tw','gb','kd','ko','ww','wdiag','wvol','gamma','frac']:
   self.const[name]=torch.tensor(getattr(m,name),dtype=torch.float64)
  self.ids=torch.tensor(m.ids,dtype=torch.int64);self.groups=m.groups;self.coo=m.sparsity.tocoo()
  seed=torch.zeros((int(max(m.groups)+1),self.N),dtype=torch.float64);seed[torch.tensor(m.groups),torch.arange(self.N)]=1.;self.seed=seed
 def build(self,y,context,numpy_residual):
  m=self.m;n=self.n;t=self.const
  # gamma may change between a Hamiltonian root and passive absorber halves.
  t['gamma']=torch.tensor(m.gamma,dtype=torch.float64)
  a0,x0,p0,chi0,pi0,dt,scales,ascale,cts,cgs,pscale,cscale=context
  def tensor(x):return torch.tensor(x,dtype=torch.complex128 if np.iscomplexobj(x) else torch.float64)
  a0,x0,p0,chi0,pi0,scales,ascale,cts,cgs=map(tensor,[a0,x0,p0,chi0,pi0,scales,ascale,cts,cgs])
  abs2=lambda a:a.real*a.real+a.imag*a.imag
  rho0=abs2(a0[0])/t['vol'];nw=len(chi0)
  def interp(z):return (1-t['frac'])*z[self.ids]+t['frac']*z[self.ids+1]
  def deposit(z):
   return torch.zeros(nw,dtype=torch.float64).index_add(0,self.ids,(1-t['frac'])*z).index_add(0,self.ids+1,t['frac']*z)
  def add_edges(z):return torch.cat((z[:1],z[:-1]+z[1:],z[-1:]))
  def left_minus_right(z):return torch.cat((z[:1],z[1:]-z[:-1],-z[-1:]))
  def response(u):
   cap=.9999;v=torch.clamp(u,max=cap);d=u-v
   F=v*v/(1-v)+d*cap*(2-cap)/(1-cap)**2+d*d/(1-cap)**3
   Wp=v/(1-v)+d/(1-cap)**2;Fp=v*(2-v)/(1-v)**2+2*d/(1-cap)**3
   return F,Wp,Fp
  def residual(yy):
   z=yy*scales;a1=torch.stack((torch.complex(z[:n],z[n:2*n]),torch.complex(z[2*n:3*n],z[3*n:4*n])))
   x=z[4*n:5*n];ct=z[5*n:6*n];cg=z[6*n:7*n];vr=z[7*n:8*n];vg=z[8*n:9*n];cw=z[9*n:];am=(a0+a1)/2
   rho=(rho0+abs2(a1[0])/t['vol'])/2;cm=interp(cw);pim=interp(2/dt*(cw-chi0));mt=abs2(am[0]);mf=abs2(am[1]);u=ct/t['r']**2;gd=cg/t['r']**2
   F,Wp,Fp=response(u);ff,_,fp=response((u[1:]+u[:-1])/2);dx=2/np.pi*torch.diff(x)
   Z=(2/np.pi)**2*t['vol']*(m.ell2*F+m.vac)/m.c**2;omega=2/dt*(x-x0)
   resp=t['vol']*(Wp+m.beta*torch.sin(2*x)**2/np.pi**2*Fp)+add_edges(.25*m.ell2*t['w']*fp*dx**2)
   resp=resp-(2/np.pi)**2*m.ell2/m.c**2*.5*t['vol']*omega**2*Fp
   gr=t['vol']*(gd+t['gb']);Mt=ct[-1]+.5*mt[-1];M=cg[-1]+.5*(mt[-1]+mf[-1]);tail=torch.sum(t['tw']*response(Mt*t['tt']**2)[1]/t['tt']**2)
   beta=(m.g+2*m.g2*rho)*cm/m.sigma
   U=torch.exp(1j*m.g2/m.sigma*(2*rho[1:]*cm[1:]-2*rho[:-1]*cm[:-1]-(rho[1:]+rho[:-1])/2*torch.diff(cm)))
   psi=am[0]/torch.sqrt(t['vol']);D=m.k*t['w']*torch.imag(torch.conj(psi[:-1])*U*psi[1:]);qsec=m.g+2*m.g2*rho
   sc=torch.sin(x)*torch.cos(x);alT=torch.cos(x)**2*am[0]-sc*torch.exp(-1j*beta)*am[1];alF=torch.sin(x)**2*am[1]-sc*torch.exp(1j*beta)*am[0]
   rate=2*m.J/m.sigma*torch.imag(torch.conj(am[0])*alT)
   mleft=D*m.g2/m.sigma*(-.5*cm[1:]-1.5*cm[:-1]);mright=D*m.g2/m.sigma*(1.5*cm[1:]+.5*cm[:-1])
   mextra=(torch.cat((mleft,torch.zeros(1,dtype=torch.float64)))+torch.cat((torch.zeros(1,dtype=torch.float64),mright)))/t['vol']
   muT=vg+vr-m.eps+2*m.g2*cm*rate/t['vol']+mextra
   muF=vg+2.5*m.K*((mf+1e-300)/t['vol'])**(2/3)
   sc=torch.sin(x)*torch.cos(x);alT=torch.cos(x)**2*am[0]-sc*torch.exp(-1j*beta)*am[1];alF=torch.sin(x)**2*am[1]-sc*torch.exp(1j*beta)*am[0]
   eT=t['ko']*U;eF=t['ko'];HT=(t['kd']+muT)*am[0]+m.J*alT+torch.cat((eT*am[0,1:],torch.zeros(1,dtype=torch.complex128)))+torch.cat((torch.zeros(1,dtype=torch.complex128),torch.conj(eT)*am[0,:-1]))
   HF=(t['kd']+muF)*am[1]+m.J*alF+torch.cat((eF*am[1,1:],torch.zeros(1,dtype=torch.complex128)))+torch.cat((torch.zeros(1,dtype=torch.complex128),eF*am[1,:-1]))
   ra=(a1-a0+1j*dt/m.sigma*torch.stack((HT,HF)))/ascale
   coeff=(2/np.pi)**2*t['w']*(m.ell2*ff+m.vac);cross=torch.real(torch.exp(1j*beta)*torch.conj(am[1])*am[0]);force=2*m.beta*t['vol']*F*torch.sin(4*x)/np.pi**2+m.B*t['vol']*torch.sin(2*x)+m.J*((mf-mt)*torch.sin(2*x)-2*cross*torch.cos(2*x))-left_minus_right(coeff*torch.diff(x))
   scale=1e-18+add_edges(coeff)+2*m.J*(mt+mf)+2*m.B*t['vol']+8*m.beta*t['vol']*F/np.pi**2;add=4*Z/dt**2;rx=(force+add*(x-x0)-2*p0/dt)/(scale+add)
   rct=torch.cat((ct[:1]-.5*mt[:1],torch.diff(ct)-.5*(mt[1:]+mt[:-1])))/cts;mass=mt+mf;rcg=torch.cat((cg[:1]-.5*mass[:1],torch.diff(cg)-.5*(mass[1:]+mass[:-1])))/cgs
   rr=resp/t['r']**2;gg=gr/t['r']**2
   rvr=torch.cat((vr[:-1]-vr[1:]-.5*(rr[:-1]+rr[1:]),vr[-1:]-.5*rr[-1:]-tail))/pscale
   rvg=torch.cat((vg[:-1]-vg[1:]+.5*(gg[:-1]+gg[1:]),vg[-1:]+.5*gg[-1:]+M/m.R+1/np.sqrt(m.R**2+m.b**2)))/pscale
   bl=D*m.g2/m.sigma*(-1.5*rho[:-1]+.5*rho[1:]);br=D*m.g2/m.sigma*(1.5*rho[1:]-.5*rho[:-1])
   S=qsec*rate+torch.cat((bl,torch.zeros(1,dtype=torch.float64)))+torch.cat((torch.zeros(1,dtype=torch.float64),br))
   lap=-t['wdiag']*cw+torch.cat((t['ww']*cw[1:],torch.zeros(1,dtype=torch.float64)))+torch.cat((torch.zeros(1,dtype=torch.float64),t['ww']*cw[:-1]))
   rw=(cw-chi0-dt*pi0/2+dt*t['gamma']/2*(cw-chi0)-dt**2*m.c**2/4*lap/t['wvol']+dt**2/4*deposit(S)/t['wvol'])/(cscale*(1+dt*t['gamma']/2+dt**2*m.c**2/4*t['wdiag']/t['wvol']))
   return torch.cat((ra[0].real,ra[0].imag,ra[1].real,ra[1].imag,rx,rct,rcg,rvr,rvg,rw))
  yy=torch.tensor(y,dtype=torch.float64);actual=residual(yy).detach().numpy();self.residual_error=float(np.max(abs(actual-numpy_residual))/max(1.,np.max(abs(numpy_residual))))
  if self.residual_error>1e-9:raise RuntimeError('Torch/NumPy residual mismatch: '+str(self.residual_error))
  deriv=torch.vmap(lambda tangent:torch.func.jvp(residual,(yy,),(tangent,))[1])(self.seed).detach().numpy()
  vals=deriv[self.groups[self.coo.col],self.coo.row]
  return csc_matrix((vals,(self.coo.row,self.coo.col)),shape=self.coo.shape)
