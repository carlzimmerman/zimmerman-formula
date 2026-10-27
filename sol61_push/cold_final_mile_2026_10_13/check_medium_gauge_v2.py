import json,math,sys
from pathlib import Path
import sympy as s
from scipy.optimize import brentq
E,D,rho,l=s.symbols('E D rho lambda',positive=True)
ep=s.symbols('eps_parallel',positive=True)
v,B,ed=s.symbols('v B ed',real=True)
A=rho+E*D-l*E*E;C=D-l*E
L=ep*ed*ed/2+A*v*v/2+C*v*B-l*B*B/2
checks=[]
def check(name,c,detail=''):
 checks.append(dict(name=name,passed=bool(c),detail=detail))
 if not c:raise AssertionError(name)
vr=s.solve(s.Eq(s.diff(L,v),0),v)[0]
mu=s.factor(l+C*C/A)
check('varied frame wave magnetic coefficient',s.simplify(L.subs(v,vr)-(ep*ed*ed-mu*B*B)/2)==0)
delta=s.symbols('delta',real=True)
gamma=1/s.sqrt(1-delta*delta*v*v)
Eu=gamma*(E+delta*ed+delta*delta*v*B)
Bu=gamma*(delta*B+delta*v*(E+delta*ed))
check('exact boosted invariant',s.simplify(Eu*Eu-Bu*Bu-(E+delta*ed)**2+delta*delta*B*B)==0)
Eu1=s.diff(Eu,delta).subs(delta,0);Eu2=s.diff(Eu,delta,2).subs(delta,0)
Bu1=s.diff(Bu,delta).subs(delta,0)
boostquad=s.expand(D*Eu2/2+ep*Eu1*Eu1/2-l*Bu1*Bu1/2+rho*v*v/2)
check('independent boost and dust quadratic expansion',s.simplify(boostquad-L)==0)
check('coefficient grows withlambda',s.simplify(s.diff(mu,l)-rho*rho/A**2)==0)
check('minimum coefficient atlambda0',s.simplify(mu.subs(l,0)-D*D/(rho+E*D))==0)
check('causal magnetic boundary',s.simplify(s.solve(s.Eq(mu,ep),l)[0]-(ep*(rho+E*D)-D*D)/(rho-E*D+ep*E*E))==0)
p=s.symbols('p',real=True)
H=s.expand(p*v-L)
check('positive momentum square and magnetic energy',s.simplify(H.subs(v,(p-C*B)/A)-((p-C*B)**2/(2*A)+l*B*B/2-ep*ed*ed/2))==0)
# Positive field timekinetic contributes independent conjugatemomentum squared.
omega,k=s.symbols('omega k',real=True)
matrix=s.Matrix([[ep*omega**2-l*k*k,-C*omega*k],[-C*omega*k,A*omega**2]])
check('coupled determinant propagating andzero branch',s.simplify(matrix.det()-A*omega**2*(ep*omega**2-mu*k*k))==0)
t=s.symbols('t',positive=True);d=t/(1+t);el=1/(1+t)**2
threshold=s.simplify(d*d/el-t*d)
check('required density for anypositive causal magnetic response',s.simplify(threshold-t*t*t/(1+t))==0)
check('fixedframe luminal choice fails whenframe varied',s.factor((mu-ep).subs(l,ep))==s.factor((D-ep*E)**2/(rho+E*D-ep*E*E)))
rows=[]
for ee in [.01,.1,1.,9.]:
 dd=ee/(1+ee);eps=1/(1+ee)**2;epsT=1/(1+ee);minimum=ee*ee-dd*ee
 for ratio in [.1,1.,10.,1e6]:
  rr=ratio*minimum
  lower=dd*dd/(rr+ee*dd)/eps
  cap=(eps*(rr+ee*dd)-dd*dd)/(rr-ee*dd+eps*ee*ee)
  if ratio>1:
   aa=rr+ee*dd-cap*ee*ee;cc=dd-cap*ee
   speed=(cap+cc*cc/aa)/eps
   check('positive coupled inertia e%g rho%g'%(ee,ratio),aa>0 and cap>0)
   check('causalboundary identity e%g rho%g'%(ee,ratio),abs(speed-1)<1e-10)
   check('otherfield branch nofasterthanmetric e%g rho%g'%(ee,ratio),cap/epsT<=1+1e-10)
  elif ratio<1:
   check('no positive magnetic repair below density e%g rho%g'%(ee,ratio),lower>1)
  rows.append(dict(E_over_D0=ee,density_over_threshold=ratio,minimum_selected_speed_squared_over_metric=lower,
                   maximum_causal_lambda=cap,strict_positive_causal_lambda_exists=ratio>1))
G=6.67430e-11;MS=1.98847e30;c=299792458.;pc=3.0856775814913673e16
physical=[]
def shape(x):
 m=2*x*x/(math.sqrt(1+4*x*x)+1);u=m/(x*x);mp=2*x/math.sqrt(1+4*x*x)
 return x*x*u**3/(mp*(1-u)**2)
for foot,a0 in [('canonical',9.3603e-11),('alt',1.1312e-10)]:
 for mb in [1e9,1e10,1e11,1e12]:
  rm=math.sqrt(G*mb*MS/a0);vf=(G*mb*MS*a0)**.25
  root=brentq(lambda x:vf*vf/(c*c)*shape(x)-1,1e-5,1.,xtol=1e-12)
  check('pointsource density threshold root %s %g'%(foot,mb),abs(vf*vf/(c*c)*shape(root)-1)<1e-6)
  physical.append(dict(footing=foot,Mb_Msun=mb,pointsource_inner_threshold_pc=root*rm/pc,
                       threshold_r_over_rM=root,meaning='Inside this ideal pointsource radius the specified dustprofile lacks density for selectedcausal repair; no extendedgalaxy/stiffness score.'))
out=dict(checks=checks,constitutive_controls=rows,pointsource_controls=physical,
 scope='Selected locallyfrozen pressurelessfluid/gauge principal block with frame varied; not fullcovariant health or vacuum matching. Newmagnetic constitutivefunction supplied.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(checks=len(checks),pointsource_controls=physical),indent=2))
