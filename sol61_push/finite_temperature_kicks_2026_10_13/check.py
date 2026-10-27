"""Finite-T ideal two-spin Fermi bath; resting, dilute impurity only."""
import json, math, sys
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import expit, zeta
checks=[]
def test(name, ok):
 checks.append(dict(name=name,passed=bool(ok)))
 assert ok,name
# Stable log(1+exp(a+y))-log(1+exp(a)), y positive.
def logs(a,y):
 if a>40:return y
 return float(np.logaddexp(0,a+y)-np.logaddexp(0,a))
def sf(q,w,M,mu,T):
 if w<0:return math.exp(w/T)*sf(q,-w,M,mu,T)
 emin=(M*w/q-q/2)**2/(2*M)
 d=logs((mu-emin-w)/T,w/T)
 return M*M*T/(2*math.pi**2*q)*d/(-math.expm1(-w/T))
# Independent radial Fermi occupation integral after the angular delta function.
for q,w in [(.1,.01),(.4,.03),(.2,-.02),(.8,-.05)]:
 M=2.;mu=.3;T=.02;emin=(M*w/q-q/2)**2/(2*M)
 integral=quad(lambda e:expit((mu-e)/T)*expit((e+w-mu)/T),emin,max(emin,mu+abs(w))+50*T,epsabs=1e-13)[0]
 direct=M*M/(2*math.pi**2*q)*integral
 test('occupation integral '+str((q,w)),abs(sf(q,w,M,mu,T)/direct-1)<1e-9)
# Detailed balance is checked against the independent occupation integral above,
# not counted separately since sf implements that identity.
hc=1.973269804e-7;hb=6.582119569e-16;m=1e6;MS=1e7;MA=10510986.005756367
n=1e25;g=1/(4*m*MS);kF=hc*(3*math.pi**2*n)**(1/3);EF=kF*kF/(2*MA)
barrier=1.92087639236e-9
rows=[]
for T in [1e-9,1e-7,1e-5,1e-4]:
 theta=T/EF
 def number(u):
  end=max(u,0)+50*theta
  pts=sorted(set([0,end]+[max(0,min(end,u+j*theta)) for j in [-20,0,20]]))
  return 1.5*sum(quad(lambda x:math.sqrt(x)*expit((u-x)/theta),a,b,epsabs=1e-12)[0] for a,b in zip(pts,pts[1:]))
 u=brentq(lambda u:number(u)-1,.5,1.1,xtol=1e-14);mu=u*EF
 test('fixed density '+str(T),abs(number(u)-1)<1e-10)
 def delta(y):
  E=y*T;q=math.sqrt(2*m*E)
  emin=(MA*E/q+q/2)**2/(2*MA)
  return logs((mu-emin)/T,y)
 def integrand(y,p):
  if y==0:return 0. if p else expit(mu/T)
  return y**p*delta(y)/math.expm1(y)
 def calc(p,lo,cut):return quad(lambda y:integrand(y,p),lo,cut,epsabs=1e-11,epsrel=1e-10)[0]
 coeff=g*g*MA*MA*m/(2*math.pi**3*hb)
 power=coeff*T**3*calc(1,0,100)
 rate=coeff*T*T*calc(0,barrier/T,100)
 test('power cutoff '+str(T),abs(calc(1,0,80)/calc(1,0,100)-1)<1e-9)
 test('kick cutoff '+str(T),abs(calc(0,barrier/T,80)/calc(0,barrier/T,100)-1)<1e-9)
 asympower=coeff*T**3*2*float(zeta(3,1))
 asymrate=coeff*T*T*quad(lambda y:y/math.expm1(y),barrier/T,100)[0]
 test('phase space upper bound '+str(T),power<=asympower*(1+1e-10) and rate<=asymrate*(1+1e-10))
 rows.append(dict(T_eV=T,T_kelvin=T/8.617333262e-5,mu_over_EF=u,upward_power_eV_s=power,single_kick_above_wall_s_inverse=rate,waiting_scale_years=1/rate/(365.25*86400),power_over_degenerate_limit=power/asympower,rate_over_degenerate_limit=rate/asymrate))
out=dict(checks=checks,all_pass=all(c['passed'] for c in checks),EF_eV=EF,barrier_eV=barrier,rows=rows,non_claims=['Resting impurity only, no cavity evaporation lifetime','Hypothetical ideal unpaired neutral atoms, no empirical evidence','No moving-distribution evolution or preparation protocol'])
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
