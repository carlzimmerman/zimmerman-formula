"""Born collision rate of a moving dilute impurity in an ideal two-spin Fermi bath."""
import json,math,sys
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import expit
checks=[]
def test(name,x):
 checks.append(dict(name=name,passed=bool(x)))
 assert x,name
# Structure factor for either sign of bath energy gain, vectorized.
def structure(q,omega,M,mu,T):
 w=np.abs(omega);y=w/T
 emin=(M*w/q-q/2)**2/(2*M)
 a=(mu-emin-w)/T
 # The two branches avoid cancellation for degenerate filled states and y~0.
 d=np.where(a>40,y,np.logaddexp(0,a+y)-np.logaddexp(0,a))
 small=y<1e-4
 d=np.where(small,np.log1p(expit(a)*np.expm1(np.minimum(y,1e-4))),d)
 factor=np.divide(d,-np.expm1(-y),out=expit(a).copy(),where=y!=0)
 return M*M*T/(2*math.pi**2*q)*factor*np.exp(np.minimum(omega/T,0))
def rate(K,T,m,M,mu,g,N,cut=80):
 nodes,weights=leggauss(N);a=math.sqrt(K/T)
 umax=a+math.sqrt(a*a+cut);u=(nodes+1)*umax/2;uw=weights*umax/2
 q0=math.sqrt(2*m*T);q=q0*u[:,None]
 omega=T*(2*a*u[:,None]*nodes[None,:]-u[:,None]**2)
 vals=structure(q,omega,M,mu,T)
 return g*g/(2*math.pi)*q0**3*np.sum(uw[:,None]*weights[None,:]*u[:,None]**2*vals)
# T=0: independently integrate the occupied/unoccupied annular cross section.
def zero_rate(K,m,M,kF,g,N):
 nd,wt=leggauss(N);z=(nd+1)/2;zw=wt/2;v=math.sqrt(2*K/m);Q=2*m*v
 q=Q*z[:,None];costh=z[:,None]+(1-z[:,None])*z[None,:]
 w=v*q*costh-q*q/(2*m);kz=M*w/q-q/2
 upper=kF*kF-kz*kz;lower=kF*kF-(kz+q)**2
 ann=np.where(lower>0,2*M*w,upper);ann=np.where(upper>0,ann,0)
 sf=M*ann/(4*math.pi**2*q)
 return g*g/(2*math.pi)*np.sum(zw[:,None]*zw[None,:]*Q*q*q*(1-z[:,None])*sf)
for K in [1e-6,1e-4]:
 direct=zero_rate(K,1.,3.,1.,1.,48);exact=2*9*K*K/(15*math.pi**3)
 test('zero T rate '+str(K),abs(direct/exact-1)<1e-10)
for T in [.001,.01]:
 direct=rate(0,T,1.,3.,100.,1.,64)
 exact=9*T*T/(12*math.pi)
 test('resting degenerate thermal rate '+str(T),abs(direct/exact-1)<1e-10)
m=1e6;MS=1e7;M=10510986.005756367;g=1/(4*m*MS);hc=1.973269804e-7;hb=6.582119569e-16
n=5e24;kF=hc*(3*math.pi**2*n)**(1/3);EF=kF*kF/(2*M)
U=1.9208763923634617e-9/2;D=2e-9-2*U;K=D/2;rows=[]
for T in [1e-11,1e-9,1e-7,1e-5,1e-4]:
 theta=T/EF
 def number(u):
  end=max(u,0)+50*theta
  pts=sorted(set([0,end]+[max(0,min(end,u+j*theta)) for j in [-20,0,20]]))
  return 1.5*sum(quad(lambda x:math.sqrt(x)*expit((u-x)/theta),a,b,epsabs=1e-12)[0] for a,b in zip(pts,pts[1:]))
 u=brentq(lambda u:number(u)-1,.5,1.1,xtol=1e-14);mu=u*EF
 test('density '+str(T),abs(number(u)-1)<1e-10)
 r64=rate(K,T,m,M,mu,g,64);r128=rate(K,T,m,M,mu,g,128);r100=rate(K,T,m,M,mu,g,128,100)
 test('angular radial refinement '+str(T),abs(r64/r128-1)<1e-6)
 test('thermal cutoff '+str(T),abs(r100/r128-1)<1e-6)
 rows.append(dict(T_eV=T,T_kelvin=T/8.617333262e-5,collision_rate_s=r128/hb,carrier_width_eV=r128,independent_pair_width_over_D=2*r128/D,pair_width_over_vacuum_total_source_width=2*r128/(2e-12),width_over_T=r128/T))
reduced=m*M/(m+M);scattering_length=g*reduced/(2*math.pi)
zero=2*g*g*M*M*m*K*K/(15*math.pi**3)
out=dict(checks=checks,all_pass=all(v['passed'] for v in checks),parameters=dict(n_m3=n,K_eV=K,D_eV=D,EF_eV=EF,kF_times_Born_scattering_length=kF*scattering_length),zero_temperature_width_eV=zero,zero_temperature_rate_s=zero/hb,rows=rows,non_claims=['Ideal Born bath scattering only; no full retarded spectral function','No real self-energy, source resonance broadening, atom phase stability or observed carrier','Pair width is an independent-particle sum, not a calculated interacting two-particle response'])
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
