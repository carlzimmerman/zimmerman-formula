#!/usr/bin/env python3
import argparse,json,platform
from pathlib import Path
import sympy as S
import mpmath as mp
HERE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,required=True);ap.add_argument('--freeze-physical-p',action='store_true');args=ap.parse_args();out=args.output_dir.resolve();out.relative_to(HERE);out.mkdir(parents=True,exist_ok=True)
checks=[]
def ck(n,v,d):checks.append(dict(name=n,passed=bool(v),detail=d));print(('PASS ' if v else 'FAIL ')+n,flush=True)
z,t,eta,kap,kbar,M=S.symbols('z t eta kap kbar M',positive=True);h=1+eta*t
Sband=3*eta**2*(t-1)/(kap*z**S.Rational(2,3));tp=t*(z-1)/(z*(t-1)*(1+eta*t))
actual=(kap*kbar*kbar*(1 if args.freeze_physical_p else z**S.Rational(2,3))-3*eta**2*(t-1))/(h-eta)**2
ck('fixed_comoving_sign_identity',S.simplify(actual-kap*z**S.Rational(2,3)*(kbar*kbar-Sband)/(h-eta)**2)==0,'p/Hstar=kbar z1/3, not constant physicalp')
Fp=S.diff(t-S.log(t)-1+eta*(t-1)**2/2,t);Gp=S.diff(z-S.log(z)-1,z)
ck('implicit_branch_derivative',S.simplify(Fp*tp-Gp)==0,'t(z)>1 monotone on earlybranch')
Dband=S.diff(Sband,z)+S.diff(Sband,t)*tp
station=3*t*(z-1)-2*(t-1)**2*(1+eta*t)
ck('exact_peak_stationarity',S.simplify(Dband-eta**2*station/(kap*z**S.Rational(5,3)*(t-1)*(1+eta*t)))==0,'Stationarityequation, no uniquenessassumption')
fold=Sband.subs(t,1+(z-1)/S.sqrt(1+eta))
ck('fold_asymptotic_coefficient',S.limit(fold/(z-1),z,1)==3*eta**2/(kap*S.sqrt(1+eta)),'Actual signedfold slope')
zz=S.symbols('zz',positive=True);tearly=S.sqrt(2*zz/eta)
ck('early_S_coefficient',S.limit(Sband.subs({z:zz,t:tearly})*zz**S.Rational(1,6),zz,S.oo)==3*S.sqrt(2)*eta**S.Rational(3,2)/kap,'Leading implicitbranch t~sqrt2z/eta')
ck('early_fixed_mode_positive',S.simplify(S.limit(actual.subs({z:zz,t:tearly})*zz**S.Rational(1,3),zz,S.oo)-kap*kbar*kbar/(2*eta))==0,'Every fixed nonzerocomovingmodepositiveasymptotic early')
# latebranch t(z)=exp(eta/2)z+o(z)
ck('late_fixed_mode_positive',S.simplify(S.limit(actual.subs(t,S.exp(eta/2)*z),z,0)-3*eta**2/(1-eta)**2)==0,'Latevacuum kinetic positive for0eta1')
a=S.symbols('a',positive=True);ac=(1+S.sqrt(1+2*eta))/eta
ck('bound_crossover',S.simplify(eta*ac**2/2-ac-1)==0,'z>max(1+a,eta a²/2) at t1+a')
ck('first_bound_piece_increases',S.simplify(S.diff(a/(1+a)**S.Rational(2,3),a)-(1+a/3)/(1+a)**S.Rational(5,3))==0,'Universalfinite bound peak at ac')
ck('second_bound_piece_decreases',S.simplify(S.diff((2/eta)**S.Rational(2,3)*a**(-S.Rational(1,3)),a)+(2/eta)**S.Rational(2,3)*a**(-S.Rational(4,3))/3)==0,'Beyond ac universalbounddecreases')
mp.mp.dps=70;ee=mp.mpf('.5');kk=mp.mpf('.99');calls=[0]
def Z(tt):
 calls[0]+=1
 if calls[0]>10000 or tt<=1:raise RuntimeError('declared range/evaluation cap')
 target=tt-mp.log(tt)+ee*(tt-1)**2/2
 return -mp.re(mp.lambertw(-mp.exp(-target),-1))
def Band(tt):return 3*ee*ee*(tt-1)/(kk*Z(tt)**(mp.mpf(2)/3))
def Peak(tt):return 3*tt*(Z(tt)-1)-2*(tt-1)**2*(1+ee*tt)
def bisect(fn,lo,hi):
 lo=mp.mpf(lo);hi=mp.mpf(hi);fl=fn(lo);fh=fn(hi)
 if fl*fh>=0:raise RuntimeError('missing bracket')
 for _ in range(240):
  mid=(lo+hi)/2;fm=fn(mid)
  if fl*fm>0:lo=mid;fl=fm
  else:hi=mid;fh=fm
 return (lo+hi)/2
pt=bisect(Peak,5,10);pz=Z(pt);ps=Band(pt);k2=ps/2;kt=mp.sqrt(k2)
roots=[bisect(lambda v:Band(v)-k2,mp.mpf('1.1'),pt),bisect(lambda v:Band(v)-k2,pt,1000)]
ck('bounded_stationary_point',abs(Peak(pt))<mp.mpf('1e-55'),'Bracket5t10, no claim globaluniqueness')
ck('bounded_local_maximum',Peak(pt-mp.mpf('.001'))>0 and Peak(pt+mp.mpf('.001'))<0,'Derivative sign at stated neighboring points')
ck('two_distinct_crossings',roots[0]<pt<roots[1] and all(abs(Band(v)-k2)<mp.mpf('1e-55') for v in roots),'Actual two roots; not exhaustive enumeration')
ck('positive_negative_positive_mode',Band(mp.mpf('1.01'))<k2 and Band(pt)>k2 and Band(mp.mpf('1e6'))<k2,'Finite mode history signs agree endpoint proof')
bound_ac=(1+mp.sqrt(1+2*ee))/ee;bound=3*ee**2/kk*bound_ac/(1+bound_ac)**(mp.mpf(2)/3)
ck('finite_bound_samples',all(Band(1+mp.exp(mp.mpf(j)/4))<bound for j in range(-24,49)),'73 boundedt samples corroborate analyticupperbound')
ck('source_branch_constraint_at_roots',all(abs((v-mp.log(v)-1+ee*(v-1)**2/2)-(Z(v)-mp.log(Z(v))-1))<mp.mpf('1e-55') for v in roots+[pt]),'Authenticupper branch, no offdomainfindroot')
rows=[dict(t=str(v),z=str(Z(v)),a_over_fold=str(Z(v)**(-mp.mpf(1)/3)),p_over_H=str(kt*Z(v)**(mp.mpf(1)/3)/(1+ee*v))) for v in roots]
result=dict(checks=checks,eta=str(ee),kappa=str(kk),peak=dict(t=str(pt),z=str(pz),S=str(ps),sqrtS=str(mp.sqrt(ps)),claim='Bracketed local maximum; global uniqueness notproved'),kbar=str(kt),kbar_squared=str(k2),crossings=rows,universal_upper_bound=str(bound),evaluation_calls=calls[0],software=dict(python=platform.python_version(),sympy=S.__version__,mpmath=mp.__version__),mutation=args.freeze_physical_p,scope='Fixedcomoving sign history in tuned background; no physicalsingularityorghost classification')
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
