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
s=np.array([1.,2.,5.]);qi=.25;qf=1.
def req(q):return np.sqrt(s+s*s/q)
def omega(q):return np.sqrt(2*q*q/(req(q)*s*s))
def U(r,q):return -(q+s)/r+np.sqrt(s)*np.arctanh(np.sqrt(s)/r)
def source(t,T):
 x=min(1.,max(0.,t/T));h=x*x*x*(10+x*(-15+6*x));hp=30*x*x*(1-x)**2
 return qi+(qf-qi)*h,(qf-qi)*hp/T if 0<t<T else 0.
from scipy.optimize import brentq
G=6.67430e-11;MS=1.98847e30;GYR=3.15576e16
rows=[]
for foot,a0 in [('canonical',9.3603e-11),('alt',1.1312e-10)]:
 for mb in [1e9,1e10,1e11,1e12]:
  unit=math.sqrt(G*MS*mb/a0)/(G*MS*mb*a0)**.25/GYR
  for duration in [1.,5.,13.8]:
   T=duration/unit;r0=req(qi);e0=U(r0,qi)
   def rhs(t,y):
    r=y[:3];v=y[3:6];q,qd=source(t,T)
    if np.any(r*r<=s):raise ValueError('saturationwall')
    return np.r_[v,-q/r**2+s*s/(r**2*(r**2-s)),-qd/r]
   sol=solve_ivp(rhs,[0,T],np.r_[r0,np.zeros(6)],method='DOP853',rtol=1e-10,atol=1e-12,t_eval=np.linspace(0,T,301))
   check('physical solver %s %g %g'%(foot,mb,duration),sol.success)
   check('physical ordering %s %g %g'%(foot,mb,duration),np.all(np.diff(sol.y[:3],axis=0)>0))
   errors=[]
   for j,t in enumerate(sol.t):
    q,_=source(t,T);errors.append(np.max(abs(U(sol.y[:3,j],q)+sol.y[3:6,j]**2/2-e0-sol.y[6:9,j])))
   err=float(max(errors));check('physical work ledger %s %g %g'%(foot,mb,duration),err<1e-8,err)
   finalE=U(sol.y[:3,-1],1.)+sol.y[3:6,-1]**2/2
   turns=[]
   for i,label in enumerate(s):
    center=float(req(1.)[i]);value=float(finalE[i]);floor=float(U(req(1.),1.)[i]);gap=max(0.,value-floor)
    def pot_scalar(rad):return -(1+label)/rad+math.sqrt(label)*math.atanh(math.sqrt(label)/rad)
    if gap<1e-12:lo=hi=center;bounded_error=True
    else:
     lo=brentq(lambda rad:pot_scalar(rad)-value,math.sqrt(label)*(1+1e-12),center,xtol=1e-12)
     hi=2*center
     while pot_scalar(hi)<value:hi*=2
     hi=brentq(lambda rad:pot_scalar(rad)-value,center,hi,xtol=1e-12);bounded_error=False
    deviation=max(1-lo/center,hi/center-1)
    turns.append(dict(label=float(label),minimum_radius=lo,maximum_radius=hi,equilibrium_radius=center,
                      fractional_radius_excursion=deviation,excitation_energy=gap,beyond_energy_resolution=not bounded_error))
   rows.append(dict(footing=foot,Mb_Msun=mb,growth_Gyr=duration,T=T,max_work_error=err,turning_controls=turns))
out=dict(checks=checks,physical_cases=rows,scope='Specified point-baryon .25to1 quintic growth from prepared cold shell equilibrium; exact final turning points. Durations are stipulated controls, not measured assembly histories or observational verdicts.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(checks=len(checks),outer_s5=[dict(footing=x['footing'],mass=x['Mb_Msun'],growth_Gyr=x['growth_Gyr'],fractional_excursion=x['turning_controls'][-1]['fractional_radius_excursion']) for x in rows]),indent=2))
