import json,math,sys
from pathlib import Path
import numpy as np
import sympy as sy
from scipy.integrate import solve_ivp
ss,rr,qq=sy.symbols('s r Q',positive=True)
re=sy.sqrt(ss+ss*ss/qq)
force=-qq/rr**2+ss**2/(rr**2*(rr**2-ss))
pot=-(qq+ss)/rr+sy.sqrt(ss)/2*sy.log((rr+sy.sqrt(ss))/(rr-sy.sqrt(ss)))
checks=[]
def check(name,c,detail=''):
 checks.append(dict(name=name,passed=bool(c),detail=detail))
 if not c:raise AssertionError(name)
check('shell potential force',sy.simplify(-sy.diff(pot,rr)-force)==0)
check('instant equilibrium',sy.simplify(force.subs(rr,re))==0)
freq=sy.simplify(-sy.diff(force,rr).subs(rr,re))
check('radial restoring frequency',sy.simplify(freq-2*qq*qq/(re*ss*ss))==0)
check('source work derivative',sy.diff(pot,qq)==-1/rr)
check('equilibrium contraction derivative',sy.simplify(sy.diff(re,qq)+ss*ss/(2*qq*qq*re))==0)
s=np.array([1.,2.,5.,10.]);qi=.25;qf=1.
def req(q):return np.sqrt(s+s*s/q)
def omega(q):return np.sqrt(2*q*q/(req(q)*s*s))
def U(r,q):return -(q+s)/r+np.sqrt(s)*np.arctanh(np.sqrt(s)/r)
def source(t,T):
 x=min(1.,max(0.,t/T));h=x*x*x*(10+x*(-15+6*x));hp=30*x*x*(1-x)**2
 return qi+(qf-qi)*h,(qf-qi)*hp/T if 0<t<T else 0.
sgrid=np.geomspace(1.,5.,48);rows=[]
for T in [20.,100.,500.,2000.]:
 for warm in [False,True]:
  initial_r=np.sqrt(sgrid+sgrid*sgrid/qi)*(1.02 if warm else 1.)
  initial_z=(1+2*sgrid/qi)/(2*np.sqrt(sgrid+sgrid*sgrid/qi))*(1.02 if warm else 1.)
  init=np.r_[initial_r,np.zeros(48),initial_z,np.zeros(48)]
  def rhs(t,y):
   r=y[:48];v=y[48:96];zeta=y[96:144];zetad=y[144:192];q,_=source(t,T)
   acc=-q/r**2+sgrid*sgrid/(r**2*(r*r-sgrid))
   ar=2*q/r**3-2*sgrid*sgrid*(2*r*r-sgrid)/(r**3*(r*r-sgrid)**2)
   ass=sgrid*(2*r*r-sgrid)/(r*r*(r*r-sgrid)**2)
   return np.r_[v,acc,zetad,ar*zeta+ass]
  def fold(t,y):return min(y[96:144])
  fold.terminal=True;fold.direction=-1
  hold=2*math.pi/math.sqrt(2/(math.sqrt(30)*25))
  sol=solve_ivp(rhs,[0,T+hold],init,method='DOP853',rtol=1e-10,atol=1e-12,max_step=.25,events=fold)
  check('label Jacobian solver T%g warm%s'%(T,warm),sol.success,str(sol.message))
  last=sol.y[:,-1];check('domain before fold T%g warm%s'%(T,warm),np.all(last[:48]**2>sgrid))
  if len(sol.t_events[0]):
   time=float(sol.t_events[0][0]);i=int(np.argmin(last[96:144]));first=dict(t=time,label=float(sgrid[i]),during_ramp=time<T)
  else:first=None
  rows.append(dict(T=T,warm=warm,first_sampled_label_fold=first,minimum_jacobian_final=float(min(last[96:144])),last_observed_time=float(sol.t[-1]),nfev=int(sol.nfev)))
out=dict(checks=checks,cases=rows,scope='48-label Jacobian audit of conditional rank-preserving carrier; terminate at sampled derivative fold. Does not exclude folds at other labels or replace crossing dynamics.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(checks=len(checks),cases=rows),indent=2))
