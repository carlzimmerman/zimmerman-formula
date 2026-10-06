import argparse,json,pathlib
import sympy as s
import mpmath as mp
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--control',action='store_true');args=ap.parse_args()
checks=[]
def ck(n,v,detail=None):checks.append(dict(name=n,passed=bool(v),detail=detail))
def zero(n,e):e=s.factor(e);ck(n,e==0,str(e))
A,C,D,d,b,v,u,a=s.symbols('A C D d b v u a',real=True)
L=A*v*v+C*u*u+D*(d*v+b*u)**2
schur=s.diff(L,v,2)/2-(s.diff(L,v,u)/2)**2/(s.diff(L,u,2)/2)
expected=A+D*d*d*C/(C+D*b*b)
zero('exact_radiation_velocity_Schur',schur-expected)
zero('finite_saturation',s.limit(expected-A,D,s.oo)-d*d*C/b**2)
zero('finite_threshold_numerator',s.factor((expected.subs(A,-a))*(C+D*b*b))-(D*(d*d*C-a*b*b)-a*C))
zero('monotone_square_gain',s.diff(expected,D)-d*d*C*C/(C+D*b*b)**2)
M,H,eta,h,r=s.symbols('M H eta h r',positive=True)
ac=3*M*eta*(h-1-eta)/(h-eta)**2
dd=1/(H*H*(h-eta)**2);cc=12*M*H*H*eta*r
zero('background_capacity_dictionary',(dd*cc-ac*b*b)*(h-eta)**2/(3*M*eta)-(4*r-(h-1-eta)*b*b))
mp.mp.dps=70
rows=[]
for rf in [mp.mpf(1)/10000,mp.mpf(1)/4]:
 et=mp.mpf(1)/2;x=mp.mpf(1)/2;df=1-4*rf/3;rad=rf/x**4
 rhs=df*(x**-3-1)+rf*(x**-4-1)+3*mp.log(x)
 def f(y):return (y*y-(1+et)**2)/(2*et)-(y-1-et)-mp.log((y-1)/et)-rhs
 lo=1+et;hi=mp.mpf(20)
 for _ in range(260):
  mid=(lo+hi)/2
  if f(mid)>0:hi=mid
  else:lo=mid
 hh=(lo+hi)/2;hp=(-3*df/x**3-4*rad+3)/(hh/et-1-1/(hh-1));bb=-(3+hp/(hh-1))
 ratio=4*rad/((hh-1-et)*bb*bb)
 rows.append(dict(eta=str(et),r_fold=str(rf),x=str(x),h=str(hh),b_r=str(bb),capacity_ratio=str(ratio),implicit_residual=str(f(hh))))
 ck('implicit_background_residual_'+str(rf),abs(f(hh))<mp.mpf('1e-60'))
ck('finite_epoch_insufficient_capacity',mp.mpf(rows[0]['capacity_ratio'])<1,rows[0]['capacity_ratio'])
ck('finite_epoch_capacity_example',mp.mpf(rows[1]['capacity_ratio'])>1,rows[1]['capacity_ratio'])
if args.control:ck('CONTROL_every_positive_radiation_history_repaired',mp.mpf(rows[0]['capacity_ratio'])>1)
result=dict(passed=all(c['passed'] for c in checks),checks=checks,examples=rows,scope='Exact Schur criterion and analytic small-radiation family obstruction; numerical examples are not interval certificates; full gradients untested')
pathlib.Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(passed=result['passed'],checks=len(checks))));raise SystemExit(0 if result['passed'] else 1)
