"""Inner l4 functional and exact finite-observable null-space construction."""
import argparse,pathlib,json,hashlib
import sympy as s
import mpmath as m
pa=argparse.ArgumentParser();pa.add_argument('--output',required=True);pa.add_argument('--control',choices=['none','drop_l4','unique_C','wrong_l2_normalization'],default='none');args=pa.parse_args();checks=[]
def ck(n,b,d=None):checks.append(dict(name=n,passed=bool(b),detail=d))
def zero(n,e):e=s.simplify(e);ck(n,e==0,str(e))
X,t,q,z=s.symbols('X t q z',real=True,positive=True);xi=(1-q*q-t*t)/(2*q*t)
P2=s.legendre(2,X);H2=3*(t+q*X)*P2-q*(1-X*X)*s.diff(P2,X);old=q*(3*X-5*X**3)+t*(1-3*X*X)
zero('l2_normalization_matches_Q2',H2+s.Rational(3,2)*old)
P4=s.legendre(4,X);H4=5*(t+q*xi)*P4.subs(X,xi)-q*(1-xi*xi)*s.diff(P4,X).subs(X,xi);raw=s.expand(H4/(2*q*s.sqrt(t)));primitive=s.integrate(raw,t);zero('l4_exact_primitive',s.diff(primitive,t)-raw)
Pplus=2*q**5-q**4+20*q**3-68*q*q-56*q+112;Pminus=2*q**5+q**4+20*q**3+68*q*q-56*q-112
F4=-5*(s.sqrt(1+q)*Pplus+s.sqrt(1-q)*Pminus)/(77*q**5)
# Primitive endpoint identity for0<q<1, with the positive real square-root branches.
plus=s.factor(primitive.subs(t,1+q));minus=s.factor(primitive.subs(t,1-q));minus=minus.subs((q-1)**5,-(1-q)**5)
zero('l4_factored_endpoint',s.simplify(plus-minus-F4))
series=s.series(F4,q,0,9).removeO();zero('l4_leading_and_next',series-(-s.Rational(5,112)*q**4-s.Rational(65,1408)*q**6-s.Rational(85,2048)*q**8))
B=z**3*(1-z)**3
for j in [1,3,5]:zero('exact_bump_moment_'+str(j),s.integrate((j+z)*B,(z,0,1))-s.Rational(2*j+1,280))
# General scaledweight derivative order vanishing at q0 for l2,l4 already shown;
# leadingpowers imply independent weights +vacuumy. No boundedtest is called a universalproof.
zero('independent_l4_to_l2_leading_ratio',(-s.Rational(5,112))/(-s.Rational(3,20))-s.Rational(25,84))
m.mp.dps=80;T=m.mpf('128.9153707043');Y=m.mpf(1000);amplitude=m.mpf('1e-10');a0=m.mpf('9.3603e-11');ge=m.mpf('2.146e-10')
def nu1(y):return 1/(y*(m.sqrt(1+1/y)+1)*(1+(y/T)**2))
e=m.findroot(lambda y:y*(1+nu1(y))-ge/a0,(1,3))
def w2(y):
 q=e/y;plus=2*q**3+q*q+6*q+12;minus=-2*q**3+q*q-6*q+12
 old=-2*m.sqrt(y)/(35*q**3)*(plus/m.sqrt(1+q)-minus/m.sqrt(1-q))
 return -m.mpf('1.5')*old

def w4(y):
 q=e/y;plus=2*q**5-q**4+20*q**3-68*q*q-56*q+112;minus=2*q**5+q**4+20*q**3+68*q*q-56*q-112
 return -5*y**m.mpf('1.5')/(77*q**5)*(m.sqrt(1+q)*plus+m.sqrt(1-q)*minus)
# Independent direct angular-radial weight check at three non-cancellation-heavy ratios.
for ratio in ['.01','.1','.3']:
 qq=m.mpf(ratio);yy=e/qq
 def h4(tt):
  xx=(yy*yy-e*e-tt*tt)/(2*e*tt);p=(35*xx**4-30*xx*xx+3)/8;dp=(140*xx**3-60*xx)/8
  return yy/(2*e*m.sqrt(tt))*(5*(tt+e*xx)*p-e*(1-xx*xx)*dp)
 direct=m.quad(h4,[yy-e,yy+e]);ck('l4_direct_integral_'+ratio,abs((direct-w4(yy))/direct)<m.mpf('1e-58'),str(abs((direct-w4(yy))/direct)))
ql=[];cl=[]
for j in [1,3,5]:
 ql.append([Y*m.quad(lambda z:z**3*(1-z)**3*w(Y*(j+z)),[0,1]) for w in [w2,w4]]);cl.append(Y*Y*m.mpf(2*j+1)/280)
# Fix b1 coefficient1; theother two exactlysolve both response-null equations.
A=m.matrix([[ql[1][0],ql[2][0]],[ql[1][1],ql[2][1]]]);rhs=m.matrix([-ql[0][0],-ql[0][1]]);sol=m.lu_solve(A,rhs);co=[m.mpf(1),sol[0],sol[1]]
if args.control=='drop_l4':co=[m.mpf(1),-ql[0][0]/ql[1][0],m.mpf(0)]
nulls=[]
for ell,index in [(2,0),(4,1)]:
 res=m.fsum(co[j]*ql[j][index] for j in range(3));scale=m.fsum(abs(co[j]*ql[j][index]) for j in range(3));ck('exactfunctional_null_l'+str(ell),abs(res)/scale<m.mpf('1e-65'),str(res));nulls.append(dict(ell=ell,weighted_integrals=[str(ql[j][index]) for j in range(3)],normalized_residual=str(abs(res)/scale)))
dC=amplitude*m.fsum(co[j]*cl[j] for j in range(3));ck('vacuum_moment_nonzero',abs(dC)>m.mpf('1e-6'),str(dC))
Mmax=max(abs(v) for v in co);valuebound=amplitude*Mmax/64;derivativebound=amplitude*Mmax*3/(16*Y);positivebase=nu1(6*Y);slopelower=positivebase*(1/(6*Y)-1/(4*Y*Y)+2*Y/(T*T+36*Y*Y));sourcebase=1-9/(16*m.sqrt(3)*T);sourcebound=amplitude*Mmax*m.mpf(73)/64
ck('uniform_positive_excess',valuebound<positivebase);ck('uniform_decreasing_nu',derivativebound<slopelower);ck('uniform_increasing_source_map',sourcebound<sourcebase);ck('ambient_response_exactly_preserved',e<Y)
# L4 alone supplies new information: original2bump Q2null has nonzeroL4.
oldco=-ql[0][0]/ql[1][0];oldl4=ql[0][1]+oldco*ql[1][1];ck('l4_discriminates_original_Q2_null',abs(oldl4)>m.mpf('1e-10'),str(oldl4))
# Threefunctional evaluationmatrix has nonzerorank on actualbumpfamily.
det=m.det(m.matrix([[ql[j][0] for j in range(3)],[ql[j][1] for j in range(3)],cl]));ck('functional_matrix_full_rank',abs(det)>m.mpf('1e-9'),str(det))
if args.control=='unique_C':ck('CONTROL_finite_multipoles_fix_C',dC==0)
if args.control=='wrong_l2_normalization':zero('CONTROL_wrong_Q2_A2_sign',H2-s.Rational(3,2)*old)
# Precisionrefinement of independent integrals: sharednull arithmeticalone isnot anexactcertificate.
m.mp.dps=100;qlfine=[[Y*m.quad(lambda z:z**3*(1-z)**3*w(Y*(j+z)),[0,1]) for w in [w2,w4]] for j in [1,3,5]];Afine=m.matrix([[qlfine[1][0],qlfine[2][0]],[qlfine[1][1],qlfine[2][1]]]);solfine=m.lu_solve(Afine,m.matrix([-qlfine[0][0],-qlfine[0][1]]));referror=max(abs((solfine[i]-sol[i])/solfine[i]) for i in range(2));ck('quadrature_precision_refinement',referror<m.mpf('1e-40'),str(referror))
result=dict(passed=all(v['passed'] for v in checks),checks=checks,parameters=dict(T=str(T),Y=str(Y),external_Newton_e=str(e),amplitude=str(amplitude)),bump_coefficients=[str(v) for v in co],nulls=nulls,delta_C=str(dC),old_two_bump_delta_M4_per_amplitude=str(oldl4),functional_matrix_determinant=str(det),uniform_margins=dict(nu_minus1=str(positivebase-valuebound),negative_slope=str(slopelower-derivativebound),source_map=str(sourcebase-sourcebound)),arithmetic=dict(decimal_digits=80,refinement_decimal_digits=100,coefficient_refinement_relative=str(referror),not_interval_certified=True),control=args.control,non_claims=['No fullbaseQ4 or orbitintegration','No allSolar/Galaxyobservablepreservation','Exactnull proofdefinescoefficientsbyexactintegrals, notnumericcertificate','Vacuumdictionaryrequiresseparaterelativisticnormalization','No fullcovarianthealth orarbitraryfiniteCshift'])
p=pathlib.Path(args.output);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(passed=result['passed'],checks=len(checks),failed=[v['name'] for v in checks if not v['passed']],deltaC=str(dC),coefficients=[str(v) for v in co])));raise SystemExit(0 if result['passed'] else 1)
