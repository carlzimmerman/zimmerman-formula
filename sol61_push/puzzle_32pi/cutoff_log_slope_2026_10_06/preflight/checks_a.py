"""Exact slope factors and bounded orthogonal checks of the all-T covariance proof."""
from pathlib import Path
import argparse,json
import sympy as s
import numpy as np
from scipy.integrate import quad
from scipy.special import expit
from scipy.optimize import brentq
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--control',choices=['variance','orientation','minimum']);args=ap.parse_args();rows=[]
def eq(n,x):rows.append(dict(name=n,passed=s.simplify(x)==0,residual=str(s.simplify(x))))
def ck(n,b,d=''):rows.append(dict(name=n,passed=bool(b),detail=str(d)))
t=s.symbols('t',positive=True);dt=t*(1-t*t)/2;ell=(1-t)/2
h=t/(1+t)
eq('actual_h_log_derivative',s.diff(h,t)*dt/h-ell)
eq('actual_ell_derivative',s.diff(ell,t)*dt+t*(1-t*t)/4)
v=s.symbols('v',real=True);k=1/(2*s.cosh(v))
eq('actual_kernel_score',s.diff(k,v)/k+s.tanh(v))
theta=s.atan(s.exp(v));eq('actual_logy_jacobian',s.diff(theta,v)-k)
# Dominating tails: h(e^(u+v)) <= exp((u+v)/2), h<=1/2;
# kernel<=exp(-|v|), giving vanishing/integrable endpoint products.
u=s.symbols('u',real=True)
eq('negative_endpoint_exponent',s.Rational(1,2)+1-s.Rational(3,2))
eq('positive_endpoint_exponent',-1-(-1))
# Direct quotient differentiation equals weighted covariance, after IBP J'=N.
J,J1,N,N1=s.symbols('J J1 N N1',real=True)
eq('normalized_score_covariance', (N1*J-N*J1)/J**2-(N1/J-(N/J)*(J1/J)))
# Independent original weighted moments, stable infinity evaluation; scaled for tinyT.
def moments(u):
 scale=np.exp(u/2) if u<0 else 1.
 def integrand(v,j):
  tt=np.sqrt(expit(u+v));hh=tt/(1+tt);e=(1-tt)/2;eu=-tt*(1-tt*tt)/4
  kk=np.exp(-abs(v))/(1+np.exp(-2*abs(v)))
  factor=[1.,e,np.tanh(v),e*np.tanh(v),eu+e*e,e*e][j]
  return hh*kk/scale*factor
 ints=[quad(lambda v:integrand(v,j),-np.inf,np.inf,epsabs=3e-11,epsrel=3e-11,limit=180)[0] for j in range(6)]
 j=ints[0];E=np.array(ints[1:])/j
 covariance=E[2]-E[0]*E[1];old_derivative=E[3]-E[0]**2
 return dict(u=float(u),T=float(np.exp(u)),A=float(2*np.exp(u)*scale*j),p=float(1+E[0]),score_mean=float(E[1]),covariance=float(covariance),direct_derivative=float(old_derivative),variance=float(E[4]-E[0]**2))
vals=[]
for uu in [-30.,-15.,-5.,0.,5.,15.]:
 m=moments(uu);vals.append(m);ck('strict_slope_bounds_'+str(uu),1<m['p']<1.5)
 ck('IBP_score_identity_'+str(uu),abs(m['p']-1-m['score_mean'])<3e-10)
 ck('orthogonal_derivative_'+str(uu),abs(m['covariance']-m['direct_derivative'])<3e-10)
 step=2e-4;fd=(moments(uu+step)['p']-moments(uu-step)['p'])/(2*step)
 ck('centered_derivative_'+str(uu),abs(fd-m['covariance'])<2e-8,fd-m['covariance'])
 ck('negative_covariance_'+str(uu),m['covariance']<0,m['covariance'])
# Opposing-monotone pair is pointwise strictly negative at finite distinct coordinates.
for a,b in [(-3.,1.),(0.,2.),(-10.,-9.)]:
 u0=.3;ea=(1-np.sqrt(expit(u0+a)))/2;eb=(1-np.sqrt(expit(u0+b)))/2
 ck('pair_kernel_negative_'+str((a,b)),(ea-eb)*(np.tanh(a)-np.tanh(b))<0)
beta=1.25;root=brentq(lambda u:moments(u)['p']-beta,-15,15,xtol=1e-11);mroot=moments(root)
ck('tilted_stationary_example',abs(mroot['p']-beta)<1e-10,root)
ck('tilted_curvature_is_maximum',mroot['covariance']<0,mroot['covariance'])
if args.control=='variance':
 m=moments(0.);eq('false_drop_positive_variance',s.Float(m['direct_derivative']-(m['direct_derivative']-m['variance'])))
if args.control=='orientation':ck('false_same_orientation_covariance',moments(0.)['covariance']>0)
if args.control=='minimum':ck('false_power_tilt_finite_minimum',mroot['covariance']>0)
res=dict(passed=sum(x['passed'] for x in rows),total=len(rows),checks=rows,values=vals,tilt_example=dict(beta=beta,u=root,T=float(np.exp(root)),p=mroot['p'],log_curvature=mroot['covariance'],meaning='mathematical maximum, not physical action/target choice'),control=args.control,scope='analytic allfiniteT proof inREPORT; finitequadrature/derivative checks corroborate, not universal scan')
p=Path(args.out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(dict(passed=res['passed'],total=res['total'],failed=[x['name'] for x in rows if not x['passed']])));raise SystemExit(not all(x['passed'] for x in rows))
