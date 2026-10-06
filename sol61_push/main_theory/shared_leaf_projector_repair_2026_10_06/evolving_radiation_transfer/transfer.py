#!/usr/bin/env python3
"""Actual Q1 radiation canonical evolution; no singular velocity auxiliary inverse in RHS."""
import numpy as np
from scipy.integrate import solve_ivp
ETA=.25;B0=3*(1-ETA)/ETA

def coefficients(y,k,op):
 a,b=y[:2];H=np.sqrt(1+a**-4);L=a**3/b**3;H2=L;ell=3*(H-H2);e=2*a**-4/H
 Pg=k*k/a/a;Ph=k*k/b/b
 A=6/a;B=B0*a**3*H*H;D=B0*a**3
 g=a**3*Pg*H;j=a**3*Ph*H2
 delta=(Pg-Ph)/(Pg+Ph)
 G=a**3*(Pg+Ph)/4 if op=='arithmetic' else a**3*Pg*Ph/(Pg+Ph)/(1+delta*delta)
 return a,b,H,L,H2,ell,e,Pg,Ph,A,B,D,g,j,G

def auxiliary(y,k,op):
 a,b,H,L,H2,ell,e,Pg,Ph,A,B,D,g,j,G=coefficients(y,k,op)
 w,ch,pw,pc=y[2:];aa=pw-pc-2*g*ch;S=g*g/B+j*j/D;Z=g*aa/B+j*pc/D-ell*pc
 u=Z/(2*S);ng=(aa-2*g*u)/(2*B);nh=(pc-2*j*u)/(2*D)
 return u,ng,nh

def rhs(y,k,op):
 a,b,H,L,H2,ell,e,Pg,Ph,A,B,D,g,j,G=coefficients(y,k,op);w,ch,pw,pc=y[2:];u,ng,nh=auxiliary(y,k,op)
 return np.array([a*H,b*H2,pw/(2*A)+ng+e*w,pc/(2*G)+ell*u-ng+nh-e*w,-e*(pw-pc)-2*g*e*w,2*g*ng])

def chart_det(y,k,op):
 a,b,H,L,H2,ell,e,Pg,Ph,A,B,D,g,j,G=coefficients(y,k,op)
 # Explicit determinant avoids subtracting a numerically scaled determinant.
 C=np.array([[A+B+G,-G,g-G*ell],[-G,D+G,j+G*ell],[g-G*ell,j+G*ell,G*ell*ell]])
 return np.linalg.det(C)

def initial(k,op):
 y=np.array([1.,2.,0.,1.,0.,0.]);a,b,H,L,H2,ell,e,Pg,Ph,A,B,D,g,j,G=coefficients(y,k,op)
 r=j/(g+j);w=-r;y[2]=w
 Tw=-e*w;Y=e*w
 C=np.array([[A+B+G,-G,g-G*ell],[-G,D+G,j+G*ell],[g-G*ell,j+G*ell,G*ell*ell]])
 ng,nh,u=np.linalg.solve(C,-np.array([-A*Tw+G*Y+g, -G*Y,-G*ell*Y]))
 y[4]=2*A*(Tw-ng);y[5]=2*G*(Y-ell*u+ng-nh)
 return y

def derivative(func,y,k,op):
 # Exact-direction complex-step derivative of analytic rational/sqrt functions.
 dy=rhs(y,k,op);h=1e-24
 return np.imag(func(y.astype(complex)+1j*h*dy,k,op))/h

def raw_geometry(y,k,op):
 a,b,H,L,H2,ell,e,Pg,Ph,A,B,D,g,j,G=coefficients(y,k,op);w,ch,pw,pc=y[2:];u,ng,nh=auxiliary(y,k,op)
 zg=H*(ch+u);zh=H2*u;v=w+ch+u
 Bg=3*H*ng/(ETA*Pg);Bh=3*H2*nh/(ETA*L*L*Ph)
 return np.array([zg,zh,v,Bg,Bh,u])

def observables(y,k,op):
 a,b,H,L,H2,ell,e,Pg,Ph,A,B,D,g,j,G=coefficients(y,k,op);w,ch,pw,pc=y[2:];u,ng,nh=auxiliary(y,k,op)
 zg,zh,v,Bg,Bh,_=raw_geometry(y,k,op);zd,zhd,vd,Bgd,Bhd,ud=derivative(raw_geometry,y,k,op)
 ngmetric=rhs(y,k,op)[3]+ud+e*w+ng;nhmetric=ud+ell*u+nh
 Phi=-zg-H*Bg;Psi=ngmetric+Bgd
 Phih=-zh-H2*Bh;Psih=nhmetric+Bhd+ell*Bh
 Wrad=4*a**-4;drho=3*Wrad*(vd-H*v-ngmetric)-3*H*Wrad*Bg
 qrad=-Wrad*(v+Bg)
 return np.array([Phi,Psi,(Phi+Psi)/2,Phih,Psih,(Phih+Psih)/2,drho,qrad,ngmetric,nhmetric])

def constraint_residual(y,k,op):
 a,b,H,L,H2,ell,e,Pg,Ph,A,B,D,g,j,G=coefficients(y,k,op);w,ch,pw,pc=y[2:];u,ng,nh=auxiliary(y,k,op);dy=rhs(y,k,op)
 Tw=dy[2]-e*w;Y=dy[3]+e*w;R=Y-ell*u+ng-nh
 return np.array([-2*B*ng+pw-pc-2*g*ch-2*g*u,-2*D*nh+pc-2*j*u,ell*pc-2*g*ng-2*j*nh,pw-2*A*(Tw-ng),pc-2*G*R])

def integrate(k,op,rtol=2e-9,cap=40000,a_end=1.5,method='DOP853'):
 y0=initial(k,op);t0=np.arcsinh(1.)/2;t1=np.arcsinh(a_end*a_end)/2;calls=[0]
 def f(t,y):
  calls[0]+=1
  if calls[0]>cap:raise RuntimeError('declared RHS cap')
  return rhs(y,k,op)
 sol=solve_ivp(f,[t0,t1],y0,method=method,rtol=rtol,atol=rtol*1e-3,dense_output=True)
 ts=np.linspace(t0,t1,401);ys=sol.sol(ts).T;obs=np.array([observables(y,k,op) for y in ys])
 Ipeak=max(2*coefficients(y,k,op)[-1]/y[0]**3*(o[8]-o[9])**2 for y,o in zip(ys,obs))
 rel=np.max(np.abs(np.array([constraint_residual(y,k,op) for y in ys]))/(1+np.abs(ys[:,4:]).max()))
 return sol,ys,obs,dict(k=k,operator=op,method=method,rtol=rtol,RHS_calls=calls[0],success=bool(sol.success),a_interval=[1.,a_end],time_interval=[t0,t1],chi_max=float(np.max(np.abs(ys[:,3]))),chi_end=float(ys[-1,3]),Weyl_max=float(np.max(np.abs(obs[:,2]))),Weyl_end=float(obs[-1,2]),radiation_delta_end=float(obs[-1,6]/(3*ys[-1,0]**-4)),constraint_relative_residual=float(rel),max_unit_lapse=float(np.max(np.abs(obs[:,8:10]))),I_peak_a0_one_amplitude_1e_minus8=float(1e-16*Ipeak),chart_det_range=[float(min(chart_det(y,k,op) for y in ys)),float(max(chart_det(y,k,op) for y in ys))])
