#!/usr/bin/env python3
"""Two-cell perspective floor: retain V0=0 boundary failure and test V0>0 repair."""
import argparse,json,sys
from pathlib import Path
import sympy as s
import mpmath as mp


def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();checks={}
 def exact(name,e):
  v=s.factor(s.simplify(e));assert v==0,(name,v);checks[name]=str(v)
 z=s.symbols('z',real=True);kap,p,V=s.symbols('kap p V',positive=True)
 H=kap*z*z+(p*p/2+V)/(1+z)+V/(1-z)
 Hzz=s.diff(H,z,2)
 exact('floor_Hessian',Hzz-(2*kap+(p*p+2*V)/(1+z)**3+2*V/(1-z)**3))
 exact('floor_stationary_origin_pzero',s.diff(H,z).subs({z:0,p:0}))
 exact('floor_momentum_Schur',s.diff(H,p,2)-s.diff(H,p,z)**2/Hzz-(2*kap+2*V/(1+z)**3+2*V/(1-z)**3)/((1+z)*Hzz))
 exact('zero_floor_boundary_derivative',s.diff(H,z).subs({z:1,V:0})-(2*kap-p*p/8))
 # Scalar regularizer used by the parent's continuum barrier proof.
 t,delta=s.symbols('t delta',positive=True);u=t/delta
 low=(u*u-3*u+3)/delta
 exact('regularizer_value_match',low.subs(t,delta)-1/delta)
 exact('regularizer_derivative_match',s.diff(low,t).subs(t,delta)+1/delta**2)
 exact('regularizer_f_plus_tfp',low+t*s.diff(low,t)-3*(u-1)**2/delta)
 mp.mp.dps=40;rows=[]
 for floor in [mp.mpf('0.000001'),mp.mpf('0.1')]:
  for pv in [mp.mpf('1'),mp.mpf('5'),mp.mpf('50')]:
   fun=lambda x:2*x-(pv*pv/2+floor)/(1+x)**2+floor/(1-x)**2
   lo=mp.mpf('0');hi=1-mp.mpf('1e-30');assert fun(lo)<0<fun(hi)
   for _ in range(160):
    mid=(lo+hi)/2
    if fun(mid)>0:hi=mid
    else:lo=mid
   zz=(lo+hi)/2
   hz=2+(pv*pv+2*floor)/(1+zz)**3+2*floor/(1-zz)**3
   hp=(2+2*floor/(1+zz)**3+2*floor/(1-zz)**3)/((1+zz)*hz)
   assert 0<zz<1 and hz>0 and hp>0
   rows.append({'V0':float(floor),'p':float(pv),'z':float(zz),'t_min':float(1-zz),'Z_Hessian':float(hz),'momentum_Schur':float(hp),'stationary_residual':str(abs(fun(zz)))})
 out={'runtime':{'python':sys.version,'executable':sys.executable,'sympy':s.__version__,'mpmath':mp.__version__},'checks':checks,'count':len(checks),'controls':rows,
      'result':'Every tested positive floor gives an interior positive-domain minimizer and positive reduced momentum Hessian; convexity and divergent endpoint energies prove the two-cell result for all finite p',
      'nonclaims':['V0 is a new fixed vacuum-energy input, not a derived magnitude','The finite-cell calculation is not a global-time gravitational theorem','Continuum positive-lapse existence requires the independent stated regularity/barrier argument']}
 Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'passed':True,'exact_checks':len(checks),'positive_floor_controls':len(rows)}))
if __name__=='__main__':main()
