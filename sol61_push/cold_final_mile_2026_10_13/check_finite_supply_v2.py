import json,math,sys
from pathlib import Path
import numpy as np
import sympy as s
r,m,Q,S=s.symbols('r m Q S',positive=True)
u=s.symbols('u',positive=True);w=-u*u/2-u-s.log(1-u);R=u*u/(1-u)
checks=[]
def check(name,cond,detail=''):
 checks.append(dict(name=name,passed=bool(cond),detail=detail))
 if not cond:raise AssertionError(name)
check('effective energy variation',s.simplify(s.diff(r*r*w.subs(u,m/r**2)-Q*m/r**2,m)-(R.subs(u,m/r**2)-Q/r**2))==0)
check('strict convexity except empty endpoint',s.simplify(s.diff(R,u)-u*(2-u)/(1-u)**2)==0)
mzero=(s.sqrt(Q*Q+4*Q*r*r)-Q)/2
check('unconstrained root',s.simplify(mzero*mzero-Q*(r*r-mzero))==0)
edge=s.sqrt(S+S*S/Q)
check('supply edge root',s.simplify((m*m-Q*(r*r-m)).subs({m:S,r:edge}))==0)
check('outside residual sign numerator',s.simplify((R.subs(u,S/r**2)-Q/r**2)*r**2*(r**2-S)-(S*S+Q*S-Q*r*r))==0)
# General Q(r) implicit derivative; positivity if Qprime>=0 and u<1.
qp,mp=s.symbols('Qprime mprime',nonnegative=True)
implicit=2*m*mp-qp*(r*r-m)-Q*(2*r-mp)
check('general root monotonicity',s.simplify(s.solve(s.Eq(implicit,0),mp)[0]-(qp*(r*r-m)+2*r*Q)/(2*m+Q))==0)
def m0(x):return 2*x*x/(np.sqrt(1+4*x*x)+1)
core=float(m0(2.));supply=2.;re=math.sqrt(6.)
def stablew(v):
 v=np.asarray(v);out=np.empty_like(v);mask=v<.05
 out[mask]=sum(v[mask]**j/j for j in range(3,28))
 out[~mask]=-v[~mask]**2/2-v[~mask]-np.log1p(-v[~mask]);return out
def profile(x,fac):return np.minimum(supply,np.maximum(core,m0(x/fac)))
def ediff(fac,n):
 breaks=sorted(set([2.,100.,re,max(2.,min(100.,fac*2.)),max(2.,min(100.,fac*re))]))
 nodes,weights=np.polynomial.legendre.leggauss(n);total=0.
 for lo,hi in zip(breaks[:-1],breaks[1:]):
  x=(hi+lo)/2+(hi-lo)/2*nodes
  ref=profile(x,1.);test=profile(x,fac)
  check('domain factor%g interval%g'%(fac,lo),bool(np.all(test/x**2<1)))
  delta=x*x*(stablew(test/x**2)-stablew(ref/x**2))-(test-ref)/x**2
  # Pointwise supporting-hyperplane condition outside the active cap.
  grad=(ref/x**2)**2/(1-ref/x**2)-1/x**2
  check('constrained first variation sign factor%g interval%g'%(fac,lo),bool(np.min(grad*(test-ref))>=-2e-13))
  check('pointwise energy minimum factor%g interval%g'%(fac,lo),bool(np.min(delta)>=-2e-13))
  total+=(hi-lo)/2*float(np.sum(weights*delta))
 return total
rows=[]
for fac in [.5,.8,1.,1.25,2.]:
 d100=ediff(fac,100);d200=ediff(fac,200)
 check('energy quadrature factor%g'%fac,abs(d100-d200)<1e-10)
 check('minimum energy factor%g'%fac,d200>=-1e-12)
 rows.append(dict(radius_dilation=fac,energy_above_minimum=d200,quadrature_difference=abs(d100-d200)))
for rv in [re,re*1.01,5.,20.,100.]:
 uv=supply/rv**2;acc=-1/rv**2+uv*uv/(1-uv)
 check('outside virtual test mass accelerated inward r%g'%rv,acc<1e-14)
out=dict(checks=checks,point_control=dict(core=core,supply=supply,edge=re),energy_controls=rows,
 scope='Constrained zero-stiffness radial carrier minimum. Independent vacuum P EL differs outside support. Formation and physical carrier bridge remain open.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(checks=len(checks),edge=re,energy_controls=rows),indent=2))
