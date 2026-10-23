"""Independent thermal detailed balance and free-X envelope controls."""
import json,sys
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.special import kv,jv,jvp,gamma
m=.001;u=.02;M=2*m*np.sqrt(1+u*u);g=2.168e-6
width=g*g/(8*np.pi*M)*np.sqrt(1-4*m*m/M**2)
C=1+2*u*u;D=np.sqrt(C*C-1);ratios=[]
for theta in [.05,.2,1.]:
 def integrand(e):
  q=np.sqrt(e*e-1)
  return np.exp(-e/theta)*theta*(np.exp(-(C*e-D*q)/theta)-np.exp(-(C*e+D*q)/theta))
 I=quad(integrand,1,1+100*theta,epsabs=1e-80,epsrel=1e-10)[0]
 rate=g*g*m*m/(8*np.pi**3)*I
 exact=width*M*M*m*theta/np.pi**2*kv(1,M/(m*theta))
 ratios.append(float(rate/exact))
x=np.linspace(1000,1100,10001);A=2**.25*gamma(1.25)
field=A*x**(-.25)*jv(.25,x)
derivative=A*(x**(-.25)*jvp(.25,x)-.25*x**(-1.25)*jv(.25,x))
B2=8*gamma(1.25)**2/np.pi
envelope_ratio=(field**2+derivative**2)*(2*x)**1.5/B2
checks=dict(thermal_detailed_balance=max(abs(r-1) for r in ratios)<1e-9,
 free_X_envelope=float(np.max(np.abs(envelope_ratio-1)))<.002)
out=dict(checks=checks,all_pass=all(checks.values()),thermal_rate_ratios=ratios,
 free_X_envelope_max_relative_error=float(np.max(np.abs(envelope_ratio-1))),
 scope='Independent normalization and asymptotic checks, not complete collision-network validation.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
sys.exit(0 if out['all_pass'] else 1)
