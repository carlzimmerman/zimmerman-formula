#!/usr/bin/env python3
import argparse,json,platform
from pathlib import Path
import sympy as S
import mpmath as mp
HERE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,required=True);ap.add_argument('--drop-large-q',action='store_true');args=ap.parse_args();out=args.output_dir.resolve();out.relative_to(HERE);out.mkdir(parents=True,exist_ok=True)
checks=[]
def ck(n,v,d):checks.append(dict(name=n,passed=bool(v),detail=d));print(('PASS ' if v else 'FAIL ')+n,flush=True)
x,v,ss,u,y,q=S.symbols('x v s u y q',positive=True);A=lambda q:2*q**3+q*q+6*q+12;B=lambda q:-2*q**3+q*q-6*q+12
Fsmall=-2/(35*q**3)*(A(q)/S.sqrt(1+q)-B(q)/S.sqrt(1-q));Flarge=-2/(35*q**3)*(A(q)/S.sqrt(1+q)+B(q)/S.sqrt(q-1))
xi=S.symbols('xi');poly=1+3*xi-3*xi*xi-5*xi**3
ck('geometric_symmetrized_polynomial',S.expand(poly-(3*xi-5*xi**3+1-3*xi*xi))==0,'e,t symmetry is on triangle domain, not a branch extrapolation')
xi_geom=(2*y*y-ss*ss-v*v)/(ss*ss-v*v)
ck('geometric_inverse_radius',S.simplify(xi_geom.subs(ss*ss,v*v+1/u**2)-(2*(y*y-v*v)*u*u-1))==0,'u=(s²-v²)^-1/2')
ck('arcsine_separation',S.simplify((2*(y*y-v*v)*u*u-1).subs(u,x/S.sqrt(y*y-v*v))-(2*x*x-1))==0,'x=u sqrt(y²-v²) in[0,1]')
mean=S.integrate(poly.subs(xi,2*x*x-1),(x,0,1))
ck('exact_Mellin_constant',mean==-S.Rational(4,35),'K=pi mean=−4pi/35, nonzero')
ck('arcsine_angular_factor',S.integrate(1/S.sqrt(1-v*v),(v,-1,1))==S.pi,'v/y angular factor, no missing solidangle')
low=S.series(Fsmall,q,0,18).removeO().expand();r=S.symbols('r',positive=True)
H=2/(35*r**3)*((2+r+6*r*r+12*r**3)/S.sqrt(1+r)+(-2+r-6*r*r+12*r**3)/S.sqrt(1-r))
high=S.series(H,r,0,16).removeO().expand()
ck('small_q_convergence',low.coeff(q,2)==S.Rational(1,10),'q^-1/2F~q3/2')
ck('large_q_convergence',high.coeff(r,0)==1 and high.coeff(r,2)==S.Rational(11,40),'F=−q^-7/2(1+11/(40q²)+...), integrandq^-4')
ck('cancellation_shell_signs',S.limit(Fsmall*S.sqrt(1-q),q,1,dir='-')==S.Rational(2,7) and S.limit(Flarge*S.sqrt(q-1),q,1,dir='+')==-S.Rational(2,7),'Both sides integrable, opposite signed limits')
mp.mp.dps=45;lc=[mp.mpf(str(low.coeff(q,2*j))) for j in range(1,9)];hc=[mp.mpf(str(high.coeff(r,2*j))) for j in range(8)]
# trigonometric variable removes q=1 singularity separately on the true branches.
def inner(theta,power,upper=False):
 sn=mp.sin(theta);co=mp.cos(theta)
 if upper:
  if theta==0:return -mp.mpf(4)/7
  if co==0:return mp.mpf(0)
  qq=1/(co*co);tn=sn/co
  if qq>1000:ff=-qq**(-mp.mpf(7)/2)*sum(c*qq**(-2*j) for j,c in enumerate(hc));return 2*qq*tn*qq**power*ff
  aa=2*qq**3+qq*qq+6*qq+12;bb=-2*qq**3+qq*qq-6*qq+12
  return -mp.mpf(4)/35*qq**(power-2)*(tn*aa/mp.sqrt(1+qq)+bb)
 else:
  if theta==0:return mp.mpf('.2') if power==-mp.mpf(5)/2 else mp.mpf(0)
  if co==0:return mp.mpf(4)/7
  qq=sn*sn
  if qq<mp.mpf('.001'):ff=sum(c*qq**(2*(j+1)) for j,c in enumerate(lc));return 2*sn*co*qq**power*ff
  aa=2*qq**3+qq*qq+6*qq+12;bb=-2*qq**3+qq*qq-6*qq+12
  return -mp.mpf(4)/35*sn*qq**(power-3)*(co*aa/mp.sqrt(1+qq)-bb)
rows=[]
for power,want,name in [(-mp.mpf(1)/2,-4*mp.pi/35,'vacuum_moment'),(-mp.mpf(5)/2,mp.mpf(0),'constant_kernel_control')]:
 lo=mp.quad(lambda th:inner(th,power),[0,mp.mpf('.03'),mp.pi/4,mp.pi/2]);hi=mp.quad(lambda th:inner(th,power,True),[0,mp.pi/4,mp.pi/2-mp.mpf('.03'),mp.pi/2]);used=lo+(0 if args.drop_large_q else hi)
 ck('whole_domain_numeric_'+name,abs(used-want)<mp.mpf('1e-28'),'45digits, independent truebranches; series8terms onlyq<.001 orq>1000, notintervalcertified')
 rows.append(dict(moment=name,power=str(power),below_q1=str(lo),above_q1=str(hi),total=str(used),expected=str(want)))
result=dict(checks=checks,numerical=rows,small_coefficients=[str(c) for c in lc],large_coefficients=[str(c) for c in hc],software=dict(python=platform.python_version(),sympy=S.__version__,mpmath=mp.__version__),mutation=args.drop_large_q,scope='Whole continuumMellin identity, no finiteEFE observation/injectivity or relativisticvacuumdictionaryclaim')
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
