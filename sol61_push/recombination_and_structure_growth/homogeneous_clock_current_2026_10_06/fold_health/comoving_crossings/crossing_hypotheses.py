#!/usr/bin/env python3
"""Certified rational brackets link two comoving zeros to the local simple-zero theorem."""
import argparse,json,math
from pathlib import Path
from fractions import Fraction as F
import mpmath as mp
import sympy as S
HERE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,required=True);ap.add_argument('--drop-redshift',action='store_true');args=ap.parse_args();out=args.output_dir.resolve();out.relative_to(HERE);out.mkdir(parents=True,exist_ok=True)
source=json.loads((HERE/'runs/main_a/results.json').read_text());mp.mp.dps=70;e=F(1,2);kap=F(99,100);k2=F(source['kbar_squared']);checks=[]
def ck(n,v,d):checks.append(dict(name=n,passed=bool(v),detail=d));print(('PASS ' if v else 'FAIL ')+n,flush=True)
def log_series(x):
 y=(x-1)/(x+1);su=F(0);yp=y
 for j in range(80):su+=2*yp/F(2*j+1);yp*=y*y
 rem=2*yp/(F(161)*(1-y*y));return su,su+rem
ln2=log_series(F(2))
def logbounds(x):
 shift=0
 while x>=2:x/=2;shift+=1
 while x<1:x*=2;shift-=1
 low,high=log_series(x)
 return low+shift*ln2[0],high+shift*ln2[1]
def residual_interval(t,z):
 tl,tu=logbounds(t);zl,zu=logbounds(z);q=e*(t-1)**2/2
 # z-ln z-[t-ln t+q]
 return z-zu-t+tl-q,z-zl-t+tu-q
def zbracket(t):
 tm=mp.mpf(str(t.numerator))/t.denominator;em=mp.mpf('.5');zz=-mp.re(mp.lambertw(-mp.exp(-(tm-mp.log(tm)+em*(tm-1)**2/2)),-1))
 scale=10**10;floor=int(mp.floor(zz*scale));lo=F(floor-1,scale);hi=F(floor+2,scale)
 assert residual_interval(t,lo)[1]<0 and residual_interval(t,hi)[0]>0
 return lo,hi
C=3*e*e
def cube_score(t,z):return C**3*(t-1)**3-kap**3*k2**3*z*z
rows=[]
for name,lo,hi,orientation in [('late_zero',F('1.728'),F('1.729'),1),('early_zero',F('160.69'),F('160.70'),-1)]:
 zl,zlu=zbracket(lo);zhlo,zh=zbracket(hi)
 ck(name+'_authentic_branch_enclosures',residual_interval(lo,zl)[1]<0 and residual_interval(lo,zlu)[0]>0 and residual_interval(hi,zhlo)[1]<0 and residual_interval(hi,zh)[0]>0,'Exact80term rationalatanhlog bounds, argumentreduction; monotone z-lnz')
 if orientation>0:signok=cube_score(lo,zl)<0 and cube_score(hi,zh)>0
 else:signok=cube_score(lo,zlu)>0 and cube_score(hi,zhlo)<0
 ck(name+'_actual_comoving_zero_bracket',signok,'Cubedpositive S-k² comparison has exact rational signs; IVT guarantees true zero')
 scorelow=3*lo*(zl-1)-2*(hi-1)**2*(1+e*hi)
 scorehigh=3*hi*(zh-1)-2*(lo-1)**2*(1+e*lo)
 ck(name+'_simple_derivative_sign',scorelow>0 if orientation>0 else scorehigh<0,'Every root in certifiedrectangle has nonzero S_z; no numerical nearzero inference')
 ck(name+'_finite_positive_clock_and_constraint',lo>1 and zl>1 and 1+e*lo-e>0 and k2>0,'q/qstar=t exp(-eta/2)/z>0 finite,Theta/MHstar=1+eta t-eta>0;rho positive,pnonzero')
 original=next(r for r in source['crossings'] if (float(r['z'])<10)==(orientation>0));tt=mp.mpf(original['t']);zz=mp.mpf(original['z']);hh=1+mp.mpf('.5')*tt
 sp=mp.mpf('.25')*(3*tt*(zz-1)-2*(tt-1)**2*(1+mp.mpf('.5')*tt))/(mp.mpf('.99')*zz**(mp.mpf(5)/3)*(tt-1)*(1+mp.mpf('.5')*tt))
 alpha=3*hh*mp.mpf('.99')*zz**(mp.mpf(5)/3)*sp/(hh-mp.mpf('.5'))**2
 rows.append(dict(name=name,t_bracket=[str(lo),str(hi)],z_rectangle=[str(zl),str(zh)],score_lower=str(float(scorelow)),score_upper=str(float(scorehigh)),Sprime_numeric=str(sp),alpha_over_MHstar_numeric=str(alpha),q_over_qstar_numeric=str(tt*mp.exp(-mp.mpf('.25'))/zz),Theta_over_MHstar_numeric=str(hh-mp.mpf('.5'))))
# Exact time-derivative link at a zero, independent of rounded root.
z,t,eta,ka,K2=S.symbols('z t eta ka K2',positive=True);h=1+eta*t;tp=t*(z-1)/(z*(t-1)*(1+eta*t));ss=3*eta**2*(t-1)/(ka*z**S.Rational(2,3));sp=S.diff(ss,z)+S.diff(ss,t)*tp
num=ka*K2*z**S.Rational(2,3)-3*eta**2*(t-1)
dnum=(-3*eta**2*tp if args.drop_redshift else S.diff(num,z)-3*eta**2*tp)
actual=(-3*h*z*dnum/(h-eta)**2).subs(K2,ss)
want=3*h*ka*z**S.Rational(5,3)*sp/(h-eta)**2
ck('proper_time_simple_zero_link',S.simplify(actual-want)==0,'alpha/(MHstar)=3h kappa z5/3 S_z/(h-eta)², using z_dot/Hstar=-3hz')
result=dict(checks=checks,rows=rows,kbar_squared_exact_decimal=source['kbar_squared'],certification='Exact Fraction arithmetic for logbounds, branchrectangles, cubedroot signs and derivative signs;70digit values descriptive only',mutation=args.drop_redshift,scope='Links actual finite nonzero-k roots to local canonicalcrossing hypotheses; no globaluniqueness/nonlinearcontinuation')
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
