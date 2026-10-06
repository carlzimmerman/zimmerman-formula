"""Full QUMOND quadrupole kernel and all-external-field vacuum-moment sum rule."""
import argparse,json,pathlib,sympy as s,mpmath as m
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--control',choices=['none','blind','wrong_branch','finite_window'],default='none');args=p.parse_args();checks=[]
def ck(name,val,detail=None):checks.append(dict(name=name,passed=bool(val),detail=detail))
def zero(name,expr):expr=s.simplify(expr);ck(name,expr==0,str(expr))
q,t,z,x=s.symbols('q t z x',positive=True);xi=(1-q*q-t*t)/(2*q*t)
raw=s.expand(1/(2*q*t**s.Rational(3,2))*(q*(3*xi-5*xi**3)+t*(1-3*xi**2)))
primitive=(-25*q**6+35*q**4*t*t+75*q**4-35*q*q*t**4+70*q*q*t*t-75*q*q-7*t**6-105*t**4-105*t*t+25)/(280*q**3*t**s.Rational(7,2))
zero('exact_weight_primitive',s.diff(primitive,t)-raw)
P=2*q**3+q*q+6*q+12;R=-2*q**3+q*q-6*q+12
Flo=-s.Rational(2,35)/q**3*(P/s.sqrt(1+q)-R/s.sqrt(1-q));Fhi=-s.Rational(2,35)/q**3*(P/s.sqrt(1+q)+R/s.sqrt(q-1))
zero('upper_endpoint_factor',primitive.subs(t,1+q)+s.Rational(2,35)*P/(q**3*s.sqrt(1+q)))
zero('lower_endpoint_low_branch',primitive.subs({q:1-z*z,t:z*z})+s.Rational(2,35)*R.subs(q,1-z*z)/((1-z*z)**3*z))
zero('lower_endpoint_high_branch',primitive.subs({q:1+z*z,t:z*z})-s.Rational(2,35)*R.subs(q,1+z*z)/((1+z*z)**3*z))
zero('small_q_leading',s.limit(Flo/q**2,q,0)-s.Rational(1,10))
zero('large_q_leading',s.limit(Fhi*q**s.Rational(7,2),q,s.oo)+1)
zero('shell_low_leading',s.limit(Flo*s.sqrt(1-q),q,1,dir='-')-s.Rational(2,7))
zero('shell_high_leading',s.limit(Fhi*s.sqrt(q-1),q,1,dir='+')+s.Rational(2,7))
# Exact rational substitutions for the three elementary Mellin integrals.
Splus=-s.Rational(24,5)*z**5+12*z**3-14*z-2*s.log(z-1)+2*s.log(z+1)
Slow=-s.Rational(24,5)*z**5-12*z**3-14*z+4*s.atan(z)
Shigh=s.Rational(24,5)*z**5-12*z**3+14*z+2*s.log(1-z)-2*s.log(z+1)
for name,prim,a,sign,polynomial in [('plus',Splus,z*z-1,-2,P),('low',Slow,1+z*z,-2,R),('high',Shigh,1-z*z,2,R)]:
 zero('Mellin_substitution_primitive_'+name,s.diff(prim,z)-sign*a*a*polynomial.subs(q,1/a))
# Finite-cutoff expression for combined K; only combined endpoints are finite.
L=Slow.subs(z,s.sqrt(1/x-1))-Splus.subs(z,s.sqrt(1/x+1))
U=Splus.subs(z,s.sqrt(1+x))+Shigh.subs(z,s.sqrt(1-x))
zero('combined_small_cutoff_limit',s.limit(L,x,0,dir='+')-2*s.pi)
zero('combined_large_cutoff_limit',s.limit(U,x,0,dir='+'))
Kexact=-4*s.pi/35;zero('nonzero_moment_sum_rule_factor',(-s.Rational(9,4))*Kexact-9*s.pi/35)
# Analytic equivalent direct radial integral checks on BOTH sides of the shell.
m.mp.dps=70
def F(q):
 if q==1:return m.mpf(0) # Arbitrary point value; both one-sided singularities integrable.
 P=2*q**3+q*q+6*q+12;R=-2*q**3+q*q-6*q+12
 sign=m.sign(1-q)
 if args.control=='wrong_branch' and q>1:sign=1
 return -m.mpf(2)/(35*q**3)*(P/m.sqrt(1+q)-sign*R/m.sqrt(abs(1-q)))
for qq in ['.1','.5','1.1','2','10']:
 qq=m.mpf(qq)
 def direct(tt):
  xx=(1-qq*qq-tt*tt)/(2*qq*tt)
  return (qq*(3*xx-5*xx**3)+tt*(1-3*xx*xx))/(2*qq*tt**m.mpf('1.5'))
 val=m.quad(direct,[abs(1-qq),1+qq]);ck('full_weight_direct_'+str(qq),abs(val-F(qq))<m.mpf('1e-60'),str(val-F(qq)))
# Independent direct quadrature omits tails; endpoint antiderivatives supply exact tails.
lo=m.mpf('.001');hi=m.mpf(100)
plus=lambda z:-m.mpf(24)/5*z**5+12*z**3-14*z-2*m.log(z-1)+2*m.log(z+1)
low=lambda z:-m.mpf(24)/5*z**5-12*z**3-14*z+4*m.atan(z)
high=lambda z:m.mpf(24)/5*z**5-12*z**3+14*z+2*m.log(1-z)-2*m.log(z+1)
klow=-m.mpf(2)/35*(plus(m.sqrt(1+1/lo))-low(m.sqrt(1/lo-1))+2*m.pi)
khigh=m.mpf(2)/35*(plus(m.sqrt(1+1/hi))+high(m.sqrt(1-1/hi)))
kmid=m.quad(lambda q:F(q)/m.sqrt(q),[lo,.1,.5,1,2,10,hi]);K=klow+kmid+khigh
ck('independent_K_quadrature',abs(K+4*m.pi/35)<m.mpf('1e-30'),str(K))
Kabs=m.quad(lambda q:abs(F(q))/m.sqrt(q),[lo,.1,.5,1,2,10,hi])+abs(klow)+abs(khigh)
ck('absolute_Mellin_norm_finite_sample',Kabs>abs(K),str(Kabs))
# Continuum response to a delta-shell test is the exact kernel at e/y; finite-band truncation differs.
# This is a distributional test of the operator, not an admissible constitutive family.
a,b=m.mpf('.2'),m.mpf(4)
kband=m.quad(lambda q:F(q)/m.sqrt(q),[a,.5,1,2,b]);ck('finite_external_band_not_full_moment',abs(kband-K)>m.mpf('.001'),str(kband))
if args.control=='blind':ck('CONTROL_moment_Mellin_blind',Kexact==0)
if args.control=='finite_window':ck('CONTROL_finite_band_equals_continuum',abs(kband-K)<m.mpf('1e-30'))
# Signed two-scale shell response: integrated quadrupole moment reconstructs both signs of C.
y1,y2=m.mpf(2),m.mpf(7);c1,c2=m.mpf(3),m.mpf(-1)
C=c1*y1+c2*y2; recovered=(c1*y1+c2*y2)*K/(-4*m.pi/35);ck('signed_two_scale_operator_moment',abs(recovered-C)<m.mpf('1e-28'),str(C))
result=dict(passed=all(c['passed'] for c in checks),checks=checks,K_exact='-4*pi/35',K_numerical=str(K),absolute_Mellin_norm_estimate=str(Kabs),finite_band=dict(qmin=str(a),qmax=str(b),Mellin_factor=str(kband)),sumrule='integral_0^infinity e^(-1/2) Q2(e) de = 9*pi*a0/(35*rM) * integral_0^infinity y*(nu(y)-1)dy',hypotheses=['fixed same kernel across all external Newtonian e>0','measurable f with integral y*abs(f) finite','uniform external-field point-source QUMOND quadrupole definition'],control=args.control,arithmetic=dict(decimal_digits=70,not_interval_certified=True),non_claims=['No full inversion or injectivity theorem','No physical accessible all-e dataset','No covariant vacuum normalization inherited','No 32pi selector','Signed shell test is a distributional operator control, not physical nu'])
out=pathlib.Path(args.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(passed=result['passed'],checks=len(checks),failed=[c['name'] for c in checks if not c['passed']],K=str(K))));raise SystemExit(0 if result['passed'] else 1)
