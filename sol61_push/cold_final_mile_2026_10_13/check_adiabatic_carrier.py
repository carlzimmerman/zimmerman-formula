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
rows=[]
for T in [20.,100.,500.,2000.]:
 for warm in [False,True]:
  r0=req(qi)*(1.02 if warm else 1.);v0=np.zeros(4);initial=np.r_[r0,v0,np.zeros(4)]
  e0=U(r0,qi);min0=U(req(qi),qi);minf=U(req(qf),qf)
  def rhs(t,y):
   r=y[:4];v=y[4:8];q,qd=source(t,T)
   if np.any(r*r<=s):raise ValueError('saturationwall')
   a=-q/(r*r)+s*s/(r*r*(r*r-s))
   return np.r_[v,a,-qd/r]
  hold=2*math.pi/min(omega(qf));ts=np.unique(np.r_[np.linspace(0,T,501),np.linspace(T,T+hold,301)])
  sol=solve_ivp(rhs,[0,T+hold],initial,method='DOP853',rtol=1e-10,atol=1e-12,t_eval=ts)
  check('solver T%g warm%s'%(T,warm),sol.success,str(sol.message))
  rruns=sol.y[:4];vruns=sol.y[4:8];work=sol.y[8:12]
  check('laminar ordering T%g warm%s'%(T,warm),np.all(np.diff(rruns,axis=0)>0))
  check('domain T%g warm%s'%(T,warm),np.all(rruns*rruns>s[:,None]))
  errors=[]
  for j,t in enumerate(sol.t):
   q,_=source(t,T);errors.append(np.max(abs(U(rruns[:,j],q)+vruns[:,j]**2/2-e0-work[:,j])))
  err=float(max(errors));check('reciprocal prescribed sourcework T%g warm%s'%(T,warm),err<1e-8,err)
  finalex=U(rruns[:,-1],qf)+vruns[:,-1]**2/2-minf
  check('final energy above minimum T%g warm%s'%(T,warm),np.min(finalex)>-1e-10)
  row=dict(T=T,warm=warm,labels=s.tolist(),final_excess=finalex.tolist(),initial_excess=(e0-min0).tolist(),
   max_work_error=err,sourcework=work[:,-1].tolist(),nfev=int(sol.nfev),
   final_radius=rruns[:,-1].tolist(),equilibrium_final=req(qf).tolist(),
   approximate_action_ratio=(finalex/omega(qf)/np.maximum((e0-min0)/omega(qi),1e-300)).tolist() if warm else None)
  rows.append(row)
G=6.67430e-11;MS=1.98847e30;GYR=3.15576e16;physical=[]
for foot,a0 in [('canonical',9.3603e-11),('alt',1.1312e-10)]:
 for mb in [1e9,1e10,1e11,1e12]:
  rm=math.sqrt(G*MS*mb/a0);vf=(G*MS*mb*a0)**.25;tunit=rm/vf/GYR
  physical.append(dict(footing=foot,Mb_Msun=mb,timeunit_Gyr=tunit,T20_Gyr=20*tunit,T100_Gyr=100*tunit,T500_Gyr=500*tunit,T2000_Gyr=2000*tunit))
out=dict(checks=checks,cases=rows,physical_dictionary=physical,
 scope='Laminar inertial carrier with prepared cold/warm initial equilibrium and prescribed source growth. Not arbitrary formation or baryonic backreaction.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(checks=len(checks),summary=[dict(T=x['T'],warm=x['warm'],final_excess=x['final_excess'],action_ratio=x['approximate_action_ratio']) for x in rows]),indent=2))
