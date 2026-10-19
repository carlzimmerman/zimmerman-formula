"""Independent physical stress/ODE/integral checks on saved collocation polynomials."""
import json,math
from pathlib import Path
import numpy as np
from scipy.interpolate import PPoly
from numpy.polynomial.legendre import leggauss

def verify(path):
 d=np.load(path);G=float(d['G']);w=float(d['omega']);g=float(d['g']);M=float(d['M']);lam=float(d['lambda_total']);z=d['collocation_z'];poly=PPoly(d['collocation_c'],z)
 nodes,weights=leggauss(8);mid=(z[1:]+z[:-1])/2;half=(z[1:]-z[:-1])/2
 zz=(mid[:,None]+half[:,None]*nodes).reshape(-1);ww=(half[:,None]*np.broadcast_to(weights,(len(half),8))).reshape(-1)
 y=poly(zz).T;dy=poly(zz,nu=1).T
 f,fz,h,hz,v,b=y;fp,fzz,hp,hzz,vp,bp=dy
 N=1-2*v/zz;Nz=-2*vp/zz+2*v/zz**2;S=f*f+4*h*h;grad=fz*fz+hz*hz;al2=np.exp(2*b)
 V=f*f+M*M*h*h-2*g*h*f*f+lam*f**4;time=w*w*S/al2
 rho=time+G*N*grad+V;pr=time+G*N*grad-V;pt=time-G*N*grad-V
 massrhs=4*math.pi*zz*zz*rho;lapserhs=(v/zz**2+4*math.pi*zz*pr)/N
 B=2/zz+bp+Nz/(2*N)
 fs=((1-w*w/al2)*f-2*g*h*f+2*lam*f**3)/(G*N)
 hs=((M*M-4*w*w/al2)*h-g*f*f)/(G*N)
 eqf=fzz+B*fz-fs;eqh=hzz+B*hz-hs
 active=(np.abs(f)>1e-8*np.max(np.abs(f)))|(np.abs(h)>1e-8*np.max(np.abs(h)))
 # Normalization remains dimensionless and finite at source cancellations.
 res=dict(mass=float(np.max(np.abs(vp-massrhs)/(1+np.abs(massrhs)))),lapse=float(np.max(np.abs(bp-lapserhs)/(1+np.abs(lapserhs)))),
 f_KG=float(np.max(np.abs(eqf[active])/(1+np.abs(fzz[active])+np.abs(B[active]*fz[active])+np.abs(fs[active])))),
 h_KG=float(np.max(np.abs(eqh[active])/(1+np.abs(hzz[active])+np.abs(B[active]*hz[active])+np.abs(hs[active])))))
 Sz=2*f*fz+8*h*hz;Vz=2*f*fz+2*M*M*h*hz-2*g*(hz*f*f+2*h*f*fz)+4*lam*f**3*fz
 prz=w*w/al2*(Sz-2*bp*S)+G*Nz*grad+2*G*N*(fz*fzz+hz*hzz)-Vz
 cons=prz+(rho+pr)*bp+4*G*N*grad/zz
 res['stress_conservation']=float(np.max(np.abs(cons)/(1+np.abs(prz)+np.abs((rho+pr)*bp)+np.abs(4*G*N*grad/zz))))
 mass_gauss=float(np.sum(ww*massrhs)/G**1.5);q=2*w*S/np.sqrt(al2);Q_gauss=float(np.sum(ww*4*math.pi*zz*zz*q/np.sqrt(N))/G**1.5)
 mass=float(d['v'][-1])/G**1.5;Q=float(d['Q'][-1]);tailmask=d['r']>.8*float(d['r'][-1]);tailmass=(d['v'][-1]-np.interp(.8*d['r'][-1],d['r'],d['v']))/d['v'][-1]
 record=dict(ODE_residuals=res,ADM_integral_relative_error=abs(mass_gauss/mass-1),charge_gauss=Q_gauss,charge_saved=Q,charge_integral_relative_error=abs(Q_gauss/Q-1),mass_over_mQ_gauss=mass/Q_gauss,min_N=float(N.min()),tail_mass_fraction=float(tailmass),
 f_negative_relative=float(min(0.,f.min())/np.max(np.abs(f))),h_negative_relative=float(min(0.,h.min())/np.max(np.abs(h))),
 omega_local_center=float(w/d['alpha'][0]),omega_cap=float(math.sqrt(1+.02**2*2/3)))
 return record
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('profile');a=p.parse_args();print(json.dumps(verify(a.profile),indent=2))
