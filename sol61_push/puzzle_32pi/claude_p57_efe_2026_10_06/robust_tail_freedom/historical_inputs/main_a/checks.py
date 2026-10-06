import argparse,json,pathlib
import sympy as s
import mpmath as mp
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--control',action='store_true');args=ap.parse_args();checks=[]
def ck(n,b,d=None):checks.append(dict(name=n,passed=bool(b),detail=d))
def zero(n,e):e=s.factor(e);ck(n,e==0,str(e))
y,Y,L,sy,sp,ft,fp=s.symbols('y Y L sy sp ft fp',positive=True)
T=y-(1-1/L)*sy;Tp=1-(1-1/L)*sp
zero('convex_map_difference',T-y*Tp-(1-1/L)*(y*sp-sy))
alpha=y*Tp/T
zero('inverse_source_convex_blend',1+ft+y*fp*Tp-((1-alpha)*(1+ft)+alpha*(1+ft+T*fp)))
t=s.symbols('t',real=True);ramp=t**3-t**4/2;step=3*t*t-2*t**3
zero('polynomial_ramp_derivative',s.diff(ramp,t)-step)
zero('polynomial_ramp_convexity',s.diff(step,t)-6*t*(1-t))
zero('affine_tail_join_value',ramp.subs(t,1)-s.Rational(1,2))
f=y**(-s.Rational(1,2))*(1+y)**(-s.Rational(5,2))
zero('baseline_log_slope',y*s.diff(f,y)/f+s.Rational(1,2)+s.Rational(5,2)*y/(1+y))
zero('baseline_exact_moment',s.beta(s.Rational(3,2),s.Rational(3,2)).rewrite(s.gamma)-s.pi/8)
neg2=4*y/(1+y)**7
zero('source_negative_bound_extremum',s.diff(neg2,y).subs(y,s.Rational(1,6)))
ck('strict_source_lower_bound',s.Rational(2,3)*(s.Rational(6,7))**7<1)
zero('uniform_weight_integral',2/s.sqrt(Y)-s.integrate(y**(-s.Rational(3,2)),(y,Y,s.oo)))
mp.mp.dps=40;yy=mp.mpf(10)
def base(z):return 1/mp.sqrt(z)/(1+z)**mp.mpf('2.5')
def S(z):
 if z<=yy:return mp.mpf(0)
 if z>=2*yy:return z-mp.mpf('1.5')*yy
 tt=(z-yy)/yy;return yy*(tt**3-tt**4/2)
rows=[]
for ll in [1,10,100,1000]:
 def ff(z):return base(z-(1-mp.mpf(1)/ll)*S(z))
 offset=(1-mp.mpf(1)/ll)*mp.mpf('1.5')*yy
 tmin=2*yy/ll+offset
 moment=mp.quad(lambda z:z*ff(z),[0,yy,2*yy])+ll**2*mp.quad(lambda z:(z-offset)*base(z),[tmin,mp.inf])
 weight=mp.quad(lambda z:(ff(z)-base(z))/z**mp.mpf('1.5'),[yy,2*yy,mp.inf])
 bound=2*base(yy)/mp.sqrt(yy)
 rows.append(dict(L=ll,moment=str(moment),weighted_EFE_tail_proxy=str(weight),uniform_bound=str(bound)))
 ck('finite_stretch_moment_upper_'+str(ll),moment<=ll**2*mp.pi/8+mp.mpf('1e-30'))
 ck('uniform_weight_bound_'+str(ll),0<=weight<bound)
ck('large_moment_example',mp.mpf(rows[-1]['moment'])>10000*mp.pi/8)
if args.control:ck('CONTROL_bounded_EFE_weight_bounds_moment',mp.mpf(rows[-1]['moment'])<10*mp.pi/8)
out=dict(passed=all(c['passed'] for c in checks),checks=checks,examples=rows,scope='Universal theorem analytic; finite control baseline/ramp not astronomical fit; EFE proxy bound not full orbit likelihood')
pathlib.Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(passed=out['passed'],checks=len(checks))));raise SystemExit(0 if out['passed'] else 1)
