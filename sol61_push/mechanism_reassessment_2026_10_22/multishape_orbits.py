import json,sys
from pathlib import Path
import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.optimize import brentq
from scipy.special import roots_legendre
from scipy.stats import qmc
from scipy.linalg import eigh
p=Path(__file__).parent
source=(p/'kinetic_weight.py').read_text().split(' grid=np.linspace')[0]
ns={'__file__':str(p/'kinetic_weight.py'),'__name__':'background_only'};exec(source,ns)
r=ns['rr'];rho=ns['rho'];drho=ns['drho'];q=ns['q'];R=ns['R'];sol=ns['sol'];r0=ns['r0'];M=float(sol.y[0,-1]);power=int(sys.argv[2]);N=2**power
phis=[];dens=[];ss=[]
for k in range(8):
 P=np.polynomial.Legendre.basis(k);x=2*(r/R)**2-1;f=P(x);fp=P.deriv()(x)*4*r/R**2
 s=r**3*rho*f;d=-(3*rho+r*drho)*f-r*rho*fp
 integ=cumulative_trapezoid(q*(2-q)/(1-q)**2*s/r**2,r,initial=0);phi=-(integ[-1]-integ)+.01*d;norm=max(abs(phi))
 phis.append(phi/norm);dens.append(d/norm);ss.append(s/norm)
phi=np.array(phis);dens=np.array(dens);s=np.array(ss)
S=np.array([[np.trapz(r*r*dens[i]*phi[j],r) for j in range(8)] for i in range(8)]);Ssym=(S+S.T)/2
H=np.array([[np.trapz(q*(2-q)/(1-q)**2*s[i]*s[j]/r**2+.01*r*r*dens[i]*dens[j],r) for j in range(8)] for i in range(8)])
grad=np.gradient(phi,r,axis=1);moment=np.array([[np.trapz(r*r*rho*grad[i]*grad[j],r) for j in range(8)] for i in range(8)])
high={str(k):np.sqrt(eigh(moment[:k,:k],Ssym[:k,:k],eigvals_only=True)).tolist() for k in [1,2,4,8]}
cdf=cumulative_trapezoid(r*r*rho,r,initial=0);cdf/=cdf[-1];u=qmc.Sobol(3,scramble=False).random_base2(power);u=(u*(N-1)+.5)/N
rad=np.interp(u[:,0],cdf,r);pp=sol.sol(rad)[1];vv=np.linspace(0,1,30001);speed=np.sqrt(2*pp)*np.interp(u[:,1],(5*vv**3-3*vv**5)/2,vv)
vr=speed*u[:,2];vt=speed*np.sqrt(1-u[:,2]**2)/np.sqrt(1+rad*rad);L=rad*vt;E=.5*(vr*vr+vt*vt)-pp;Q=-E-L*L/2
coeff=[];freq=[];error=[]
for radius,l,e in zip(rad,L,E):
 def v2(x):return 2*(e+sol.sol(x)[1])-l*l/x**2
 rp=brentq(v2,r0,radius,xtol=1e-13);ra=brentq(v2,radius,R,xtol=1e-13);cc=[];oo=[]
 for count in [1024,2048]:
  theta=(np.arange(count)+.5)*np.pi/(2*count);xx=rp+(ra-rp)*np.sin(theta)**2;weights=(ra-rp)*np.sin(2*theta)/np.sqrt(v2(xx));phase=np.pi*(np.cumsum(weights)-weights/2)/weights.sum()
  potentials=np.array([np.interp(xx,r,f) for f in phi]);cos=np.cos(np.arange(1,17)[:,None]*phase)
  cc.append((cos*weights)@potentials.T/weights.sum());oo.append(np.pi/(weights.sum()*np.pi/(2*count)))
 coeff.append(cc[-1]);freq.append(oo[-1]);error.append(float(max(abs(cc[-1]-cc[0]).ravel())))
coeff=np.array(coeff);freq=np.array(freq);a=2*M/N*(freq[:,None]*np.arange(1,17))**2/Q[:,None]
measured=np.einsum('nh,nhi,nhj->ij',a,coeff,coeff)
checks=dict(stiffness=bool(min(np.linalg.eigvalsh(Ssym))>0),hessian=bool(np.max(abs(S-H))<1e-7),fourier=max(error)<1e-4,positive_Q=bool(min(Q)>0))
np.savez_compressed(sys.argv[1]+'.npz',S=Ssym,moment=moment,measured_moment=measured,coeff=coeff,omega=freq,Q=Q,mass=M)
out=dict(checks=checks,all_pass=all(checks.values()),samples=N,high_frequency_trial_omega=high,stiffness_condition=float(np.linalg.cond(Ssym)),hessian_error=float(np.max(abs(S-H))),max_fourier_error=max(error),moment_relative_frobenius_error=float(np.linalg.norm(measured-moment)/np.linalg.norm(moment)),scope='eight trial field shapes and finite orbit sample; high-frequency eigenvalues are not full kinetic modes')
Path(sys.argv[1]+'.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
