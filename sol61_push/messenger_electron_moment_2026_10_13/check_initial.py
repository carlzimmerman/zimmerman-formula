"""Unit-charge complex scalar, leading two-loop electron vacuum-polarization contribution."""
import json,math,sys
from pathlib import Path
import numpy as np
import sympy as s
from numpy.polynomial.legendre import leggauss
from scipy.optimize import brentq
checks=[]
def test(name,x):
 checks.append(dict(name=name,passed=bool(x)))
 assert x,name
z=s.symbols('z')
test('scalar polarization small momentum weight',s.integrate((1-2*z)**2*z*(1-z),(z,0,1))==s.Rational(1,30))
test('heavy mass g2 coefficient',s.Rational(1,4)*s.Rational(1,30)*s.integrate(z*z,(z,0,1))==s.Rational(1,360))
alpha=1/137.035999;me=.51099895 # mass unit MeV; alpha precision ample for this diagnostic
cache={}
def grid(N):
 if N not in cache:
  nd,wt=leggauss(N);cache[N]=((nd+1)/2,wt/2)
 return cache[N]
def param(M,N):
 v,w=grid(N);x=v[:,None];z=v[None,:];r=(me/M)**2
 f=(1-x)*(1-2*z)**2*np.log1p(r*x*x*z*(1-z)/(1-x))
 return (alpha/math.pi)**2/4*np.sum(w[:,None]*w[None,:]*f)
def spectral(M,N):
 v,w=grid(N);x=v[:,None];t=v[None,:];r=(me/M)**2
 # t=4M^2/s; scalar spectral R(s)=(1-t)^(3/2)/4.
 f=(1-t)**1.5/t*x*x*(1-x)/(x*x+4*(1-x)/(r*t))
 return (alpha/math.pi)**2/12*np.sum(w[:,None]*w[None,:]*f)
rows=[]
for M in [10.,100.,1000.]:
 p=param(M,512);p2=param(M,256);d=spectral(M,512);d2=spectral(M,256)
 test('two integral representations '+str(M),abs(p/d-1)<2e-6)
 test('parameter refinement '+str(M),abs(p/p2-1)<2e-6)
 test('spectral refinement '+str(M),abs(d/d2-1)<2e-6)
 heavy=(alpha/math.pi)**2*(me/M)**2/360
 test('positive and below leading heavy upper bound '+str(M),0<p<=heavy)
 rows.append(dict(M_MeV=M,delta_ae=p,heavy_limit=heavy,exact_over_heavy=p/heavy,ratio_to_2023_comparison_scale=p/7e-13,ratio_to_measurement_only_sigma=p/1.3e-13))
# These scales are diagnostic choices, not confidence limits or an empirical fit.
scales=[]
for target in [7e-13,1e-12]:
 M=brentq(lambda M:param(M,512)/target-1,10,300)
 test('diagnostic scale root '+str(target),abs(param(M,512)/target-1)<1e-9)
 scales.append(dict(target_delta_ae=target,mass_MeV=M))
out=dict(checks=checks,all_pass=all(x['passed'] for x in checks),rows=rows,diagnostic_mass_scales=scales,empirical_reference=dict(source='https://arxiv.org/pdf/2209.13084',measurement_sigma=1.3e-13,authors_comparison_scale=7e-13,comparison_scale_is_not_sigma=True),non_claims=['No global exclusion or latest combined fit','No cancellations from unspecified extra sectors','No experimental allowance of heavier benchmarks','Neutralizing real messenger atoms does not remove vacuum virtual charged-scalar loops'])
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
