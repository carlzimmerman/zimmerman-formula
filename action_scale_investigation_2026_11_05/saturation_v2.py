"""Exact d=0 radial saturation obstruction, not a physical-source fit."""
import argparse,json
from pathlib import Path
import sympy as s
import mpmath as mp
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--mutate',action='store_true');args=ap.parse_args()
z,X,rho,b,K,gam,N,B,r,m2=s.symbols('s X rho b K gamma N B r M2',positive=True)
h=z+z/(1+z)-2*s.log(1+z)
A=2*X+1/gam;BB=b*X/K;E=b*X*X/(K*rho)
D=A+BB*h-E*z**3/(1+z);num=2*X+BB*h
used=A+BB*h if args.mutate else D
checks={}
def check(name,ok):
 checks[name]=bool(ok);print(('PASS ' if ok else 'FAIL ')+name,flush=True)
check('positive h derivative',s.simplify(s.diff(h,z)-z*z/(1+z)**2)==0 and h.subs(z,0)==0)
check('strict upper bound h less than s',s.simplify(s.diff(z-h,z)-(1+2*z)/(1+z)**2)==0 and (z-h).subs(z,0)==0)
check('saturation power lower bound for s at least one',s.simplify(z**3/(1+z)-z*z/2-z*z*(z-1)/(2*(z+1)))==0)
upper=A+BB*z-E*z*z/2
check('quadratic upper bound certificate',s.simplify(upper-D-BB*(z-h)-E*z*z*(z-1)/(2*(z+1)))==0)
s1=4*rho/X;s2=2*s.sqrt(A/E)
check('linear threshold certificate',s.simplify((E*z*z/4-BB*z).subs(z,s1))==0)
check('constant threshold certificate',s.simplify((E*z*z/4-A).subs(z,s2))==0)
check('negative asymptotic denominator',s.simplify(s.limit(used/z**2,z,s.oo)+E)==0)
check('positive asymptotic numerator',s.simplify(s.limit(num/z,z,s.oo)-BB)==0)
check('negative speed asymptotic',s.simplify(s.limit(z*num/D,z,s.oo)+rho/X)==0)
bg=B**3*r*num/(2*m2)
check('positive radial kinetic formula',s.simplify(2*m2*r/(N*bg)-4*m2*m2/(N*B**3*num))==0)
fixture=[]
for precision in [40,80]:
 with mp.workdps(precision):
  zz=mp.mpf(100);hh=zz+zz/(1+zz)-2*mp.log1p(zz)
  nn=2+mp.mpf(1)/5*hh
  dd=6+mp.mpf(1)/5*hh-(0 if args.mutate else mp.mpf(1)/10*zz**3/(1+zz))
  fixture.append({'precision':precision,'D0':mp.nstr(dd,precision),'Num':mp.nstr(nn,precision),'speed2':mp.nstr(nn/dd,precision)})
check('fixture negative gradient with positive kinetic',all(mp.mpf(f['D0'])<0 and mp.mpf(f['Num'])>0 for f in fixture))
with mp.workdps(90):
 agreement=max(abs(mp.mpf(fixture[0][k])-mp.mpf(fixture[1][k]))/max(1,abs(mp.mpf(fixture[1][k]))) for k in ['D0','Num','speed2'])
check('40 and80 digit arithmetic agreement',agreement<mp.mpf('1e-30'))
out={'passed':all(checks.values()),'mode':'omit_negative_portal' if args.mutate else 'main','checks':checks,'fixtures':fixture,
 'sufficient_threshold':str(s.Max(1,s1,s2)),
 'scope':'Formal classical local radial symbol near saturation; no cutoff-valid physical-galaxy instability claim.'}
Path(args.out).parent.mkdir(parents=True,exist_ok=True);Path(args.out).write_text(json.dumps(out,indent=2)+'\n')
raise SystemExit(0 if out['passed'] else 1)
