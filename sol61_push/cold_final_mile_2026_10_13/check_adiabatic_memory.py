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
for label in [1.,2.,5.]:
 for T in [500.,2000.]:
  ri=math.sqrt(label+label*label/qi);rf=math.sqrt(label+label*label)
  oi=math.sqrt(2*qi*qi/(ri*label*label));of=math.sqrt(2/(rf*label*label))
  def rhs(t,y):
   r,v=y[:2];q,_=source(t,T)
   acc=-q/r**2+label**2/(r**2*(r*r-label))
   ar=2*q/r**3-2*label**2*(2*r*r-label)/(r**3*(r*r-label)**2)
   A=np.array([[0.,1.],[ar,0.]])
   return np.r_[v,acc,(A@y[2:].reshape(2,2)).ravel()]
  sol=solve_ivp(rhs,[0,T],np.r_[ri,0.,np.eye(2).ravel()],method='DOP853',rtol=1e-10,atol=1e-12)
  check('variational solver s%g T%g'%(label,T),sol.success)
  M=sol.y[2:,-1].reshape(2,2);det=float(np.linalg.det(M))
  check('Hamiltonian area s%g T%g'%(label,T),abs(det-1)<1e-7,det)
  B=np.diag([math.sqrt(of),1/math.sqrt(of)])@M@np.diag([1/math.sqrt(oi),math.sqrt(oi)])
  ratios=[]
  for phase in [0.,math.pi/2,math.pi,3*math.pi/2]:
   v=np.array([math.cos(phase),math.sin(phase)]);ratios.append(float(np.dot(B@v,B@v)))
  average=float(np.mean(ratios));trace=float(np.sum(B*B)/2)
  check('phase average equals trace s%g T%g'%(label,T),abs(average-trace)<1e-12)
  check('no phase average action contraction s%g T%g'%(label,T),average>=1-1e-7,average)
  rows.append(dict(label=label,T=T,determinant=det,phase_action_ratios=ratios,mean_action_ratio=average,
   maximum_singular_value=float(max(np.linalg.svd(B,compute_uv=False))),final_reference_deviation=sol.y[0,-1]/rf-1))
out=dict(checks=checks,controls=rows,scope='Linearized homogeneous radial perturbations of actual driven trajectory, canonical area preserved. Quadratic reference action, not general nonlinear thermal DF or observer-fit theorem.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(checks=len(checks),controls=rows),indent=2))
