import argparse,json,sys
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--control',choices=['none','force','cutoff','derivative'],default='none');args=ap.parse_args();checks=[]
def ck(name,value,detail=''):checks.append(dict(name=name,passed=bool(value),detail=str(detail)))
def eq(name,ex):
 ex=s.factor(s.simplify(ex));ck(name,ex==0,ex)
y,T=s.symbols('y T',positive=True);ss=s.sqrt(1+1/y);ee=(ss-1)/(1+(y/T)**2);xx=y*(1+2*ee)
xp=s.diff(xx,y)
eq('actual_source_derivative',xp-(1+T*T*(ss-1)**2/(ss*(T*T+y*y))-4*T*T*y*y*(ss-1)/(T*T+y*y)**2))
z,t,u=s.symbols('z t u',positive=True);A=z*z-z+1;B=-3*z*z+4*z+1
P=A*u*u+B*u+z
# Substitute independent z after clearing the source positive denominator.
yz=1/(z*z-1)
expr=1+t*(z-1)**2/(z*(t+yz*yz))-4*t*yz*yz*(z-1)/(t+yz*yz)**2
eq('cleared_quadratic',expr*z*(t+yz*yz)**2/yz**4-P.subs(u,t/yz**2))
disc=(z-1)*(9*z**3-19*z**2-5*z-1)
eq('discriminant',B*B-4*z*A-disc)
Pfull=P.subs(u,t*(z*z-1)**2)
R=45*z**8-132*z**7+62*z**6-24*z**5+12*z**4-20*z**3-6*z*z-1
res=s.resultant(Pfull,s.diff(Pfull,z),t)
eq('critical_resultant',res+4*(z-1)**7*(z+1)**6*R)
ck('critical_root_unique_above_one',s.Poly(R,z).count_roots(1,s.oo)==1)
C=9*z**3-19*z*z-5*z-1
ck('discriminant_birth_unique_above_one',s.Poly(C,z).count_roots(1,s.oo)==1)
roots=s.polys.polytools.intervals(R,eps=s.Rational(1,10**25));positive=[(a,b) for (a,b),mult in roots if a>1]
ck('exact_critical_root_interval',len(positive)==1,positive)
star=s.nroots(R,n=45,maxsteps=100);star=next(s.re(r) for r in star if abs(s.im(r))<s.Float('1e-35') and s.re(r)>1)
Aa=A.subs(z,star);Bb=B.subs(z,star);up=(-Bb+s.sqrt(Bb*Bb-4*star*Aa))/(2*Aa)
crit=s.sqrt(up)/(star*star-1);ystar=1/(star*star-1)
ck('critical_on_real_upper_branch',disc.subs(z,star)>0)
ck('critical_cutoff_bound',s.Float('.2086368432975')<crit<s.Float('.2086368432977'))
ck('critical_zero_xprime',abs(expr.subs({z:star,t:crit**2}).evalf(35))<s.Float('1e-30'))
ck('critical_stationarity',abs(s.diff(expr,z).subs({z:star,t:crit**2}).evalf(35))<s.Float('1e-29'))
F=(3*z+1)/((z-1)**3*(z+1)**2)
eq('crossing_derivative',s.diff(F,z)+4*(3*z*z+z+1)/((z-1)**4*(z+1)**3))
eq('crossing_zero_boost_derivative',(expr-1).subs(t,F))
x,slope,b=s.symbols('x slope b',positive=True)
eq('actual_relative_principal',(1-1/slope)/2-(slope-1)/(2*slope))
eq('positive_transverse', (1-y/(y+b))/2-b/(2*(y+b)))
Tp=s.Rational(128915,1000)
poly=s.together(F-Tp**2).as_numer_denom()[0]
root=s.nroots(poly,n=40,maxsteps=150);cross=next(s.re(r) for r in root if abs(s.im(r))<s.Float('1e-30') and s.re(r)>1)
ycross=1/(cross*cross-1)
ck('crossing_unique',s.Poly(poly,z).count_roots(1,s.oo)==1)
ck('p57_global_source_regular',Tp>crit)
numbers={}
for tag,yn in [('below',ycross/2),('cross',ycross),('above',ycross*2)]:
 xv=xx.subs({T:Tp,y:yn}).evalf(35);xpval=xp.subs({T:Tp,y:yn}).evalf(35);mu=yn/xv;m=(1-mu)/2;rad=(xpval-1)/(2*xpval)
 numbers[tag]=dict(y=str(yn.evalf(35)),x=str(xv),source_derivative=str(xpval),m=str(m.evalf(35)),relative_radial=str(rad.evalf(35)))
 ck(tag+'_source_elliptic',xpval>0);ck(tag+'_transverse_positive',m>0)
 if tag=='cross':ck('cross_radial_zero',abs(rad)<s.Float('1e-28'))
 else:ck(tag+'_radial_sign',rad>0 if tag=='below' else rad<0)
eq('UV_integrable_boost',s.limit(2*y*ee*y*y,y,s.oo)-T*T)
eq('deep_integrable_boost',s.limit(2*y*ee/s.sqrt(y),y,0)-2)
if args.control=='force':ck('false_force_implies_relative_elliptic',s.sympify(numbers['above']['relative_radial'])>0)
if args.control=='cutoff':eq('false_cutoff_selected_by_global_regularity',Tp-crit)
if args.control=='derivative':eq('false_radial_equals_transverse',s.sympify(numbers['above']['relative_radial'])-s.sympify(numbers['above']['m']))
result=dict(passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,control=args.control,Tcrit=str(crit.evalf(35)),ystar=str(ystar.evalf(35)),p57_radial_cross_y=str(ycross.evalf(35)),p57_cases=numbers)
f=Path(args.output);f.parent.mkdir(parents=True,exist_ok=True);f.write_text(json.dumps(result,indent=2));print(json.dumps({'passed':result['passed'],'total':result['total'],'failed':[c for c in checks if not c['passed']],'Tcrit':result['Tcrit'],'cross_y':result['p57_radial_cross_y']}));sys.exit(result['passed']!=result['total'])
