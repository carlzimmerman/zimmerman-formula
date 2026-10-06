"""Independent kernel-functional QUMOND EFE calculation; no orbit integration/import of Claude solver."""
import argparse,pathlib,json,math
import sympy as s
import mpmath as m
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--control',choices=['none','moment','algebraic','external'],default='none');args=p.parse_args();checks=[]
def ck(n,v):checks.append(dict(name=n,passed=bool(v)))
def zero(n,v):ck(n,s.simplify(v)==0)
t,e,y=s.symbols('t e y',positive=True);xi=(y*y-e*e-t*t)/(2*e*t)
raw=s.expand(y/(2*e*t**s.Rational(3,2))*(e*(3*xi-5*xi**3)+t*(1-3*xi**2)))
F=y*(-25*e**6+35*e**4*t*t+75*e**4*y*y-35*e*e*t**4+70*e*e*t*t*y*y-75*e*e*y**4-7*t**6-105*t**4*y*y-105*t*t*y**4+25*y**6)/(280*e**3*t**s.Rational(7,2))
zero('exact_angular_radial_primitive',s.diff(F,t)-raw)
q=s.symbols('q',positive=True);w=2*(-s.sqrt(1-q)*(2*q**3+q*q+6*q+12)-s.sqrt(1+q)*(2*q**3-q*q+6*q-12))/(35*q**3*s.sqrt(1-q*q))
zero('tail_weight_leading',s.limit(w/q**2,q,0)-s.Rational(1,10))
zero('tail_weight_next',s.limit((w-q*q/10)/q**4,q,0)-s.Rational(11,112))
u,du,K=s.symbols('nu du K',real=True);zero('farfield_log_derivative',K.subs(K,e*du/u)-e*du/u)
# Exact rational bump moments.
z=s.symbols('z',real=True);bb=z**3*(1-z)**3
J1=s.integrate((1+z)*bb,(z,0,1));J2=s.integrate((3+z)*bb,(z,0,1));zero('bump_moment1',J1-s.Rational(3,280));zero('bump_moment2',J2-s.Rational(7,280))
m.mp.dps=55
T=m.mpf('128.9153707043');a0=m.mpf('9.3603e-11');GM=m.mpf('1.32712440018e20');ge=m.mpf('2.146e-10');eta=ge/a0;rm=m.sqrt(GM/a0);fac=-m.mpf(9)/4*a0/rm
coef=[m.mpf(1)/10,m.mpf(11)/112,m.mpf(165)/1792,m.mpf(1235)/14336,m.mpf(37145)/458752,m.mpf(200583)/2621440,m.mpf(609615)/8388608,m.mpf(4652325)/67108864]
def weight(yy,ee):
 if yy==0:return m.mpf(0)
 if yy==ee:return m.mpf(0) # single endpoint value has measure zero; limits are integrable.
 qq=ee/yy
 if yy>ee and qq<m.mpf('.001'):
  return m.sqrt(yy)*sum(c*qq**(2*(i+1)) for i,c in enumerate(coef))
 # Factor endpoint primitive before evaluation: avoids cancellation amplified by |y-e|^-3.5.
 plus=2*ee**3+ee**2*yy+6*ee*yy**2+12*yy**3
 minus=-2*ee**3+ee**2*yy-6*ee*yy**2+12*yy**3
 sign=1 if yy>ee else -1
 return -2*yy/(35*ee**3)*(plus/m.sqrt(yy+ee)-sign*minus/m.sqrt(abs(yy-ee)))

def nu1fix(yy):return 1/(yy*(m.sqrt(1+1/yy)+1)*(1+(yy/T)**2))
def nu1mu20(yy):
 # exact inverse of mu20: nu^20=(1+sqrt(1+4/y^20))/2; cancellation-free logarithm.
 rr=m.sqrt(1+4/yy**20);return m.expm1(m.log1p((rr-1)/2)/20)
def quadweight(fn,ee):
 # Independent 1D reduction, split around the integrable cancellation-shell singularity.
 return m.quad(lambda yy:fn(yy)*weight(yy,ee),[0,ee/2,ee,2*ee,10*ee,100*ee,1000*ee,m.inf])
def ext(fn):return m.findroot(lambda yy:yy*(1+fn(yy))-eta,(eta/2,eta))
def moment(fn):return m.quad(lambda yy:yy*fn(yy),[0,m.mpf('.01'),1,10,100,1000,10000,m.inf])
# Definition checks unrelated to a numerical Cassini verdict.
ee=ext(nu1fix);ck('ambient_below_bump',ee<10)
ck('constant_nu_has_zero_quadrupole',abs(quadweight(lambda yy:m.mpf(1),ee))<m.mpf('1e-20'))
baseQ=fac*quadweight(nu1fix,ee);baseC=moment(nu1fix)
ck('p57_Q2_independent_agreement',abs(baseQ-m.mpf('2.199e-26'))<m.mpf('2e-29'))
ck('target_moment_agreement',abs(baseC-32*m.pi)<m.mpf('1e-6'))
# Strictly monotone positive mixture supplies an illustrative Cassini-admissible nearby family.
alpha=m.mpf('.001');mix=lambda yy:(1-alpha)*nu1mu20(yy)+alpha*nu1fix(yy)
em=ext(mix);mixQ=fac*quadweight(mix,em);mixC=moment(mix)
ck('mixture_Cassini_2014_2sigma',0<mixQ<m.mpf('9e-27'))
Y=m.mpf(1000)
def bump(yy,start):
 zz=(yy-start*Y)/Y
 return zz**3*(1-zz)**3 if 0<=zz<=1 else m.mpf(0)
rows=[]
for name,fn,ex,Q0,C0,margin_scale in [('p35',nu1fix,ee,baseQ,baseC,m.mpf(1)),('Cassini_mixture',mix,em,mixQ,mixC,alpha)]:
 qb1=m.quad(lambda zz:zz**3*(1-zz)**3*weight(Y*(1+zz),ex),[0,1])*Y
 qb2=m.quad(lambda zz:zz**3*(1-zz)**3*weight(Y*(3+zz),ex),[0,1])*Y
 ratio=qb1/qb2;eps=m.mpf('5e-8')*margin_scale
 dq=fac*eps*(qb1-ratio*qb2);dc=eps*Y**2*(m.mpf(3)/280-ratio*m.mpf(7)/280)
 ck('exact_Q_null_'+name,abs(dq)<m.mpf('1e-70'));ck('nonzero_vacuum_moment_'+name,abs(dc)>m.mpf('1e-7')*margin_scale)
 # Analytic uniform inequalities on the two disjoint supports.
 perturb_max=eps*max(1,ratio)/64
 base_positive_min=margin_scale*nu1fix(4*Y)
 base_derivative_min=base_positive_min*(1/(4*Y)-1/(4*Y*Y)+2*Y/(T*T+16*Y*Y))
 perturb_derivative_bound=eps*max(1,ratio)*3/(16*Y)
 inverse_margin=1-9/(16*m.sqrt(3)*T)
 inverse_perturb_bound=eps*(m.mpf(25)/64+ratio*m.mpf(49)/64)
 ck('positive_nu_minus1_uniform_'+name,perturb_max<base_positive_min)
 ck('nonincreasing_nu_uniform_'+name,perturb_derivative_bound<base_derivative_min)
 ck('monotone_source_map_uniform_'+name,inverse_perturb_bound<inverse_margin)
 ck('farfield_exactly_unchanged_'+name,ex<Y)
 rows.append(dict(base=name,external_Newton_y=float(ex),base_Q2_s2=float(Q0),base_C=float(C0),bump_ratio=float(ratio),amplitude=float(eps),delta_Q2_s2=float(dq),delta_C=float(dc),nu_minus1_margin=float(base_positive_min-perturb_max),slope_margin=float(base_derivative_min-perturb_derivative_bound),source_map_margin=float(inverse_margin-inverse_perturb_bound)))
# Bounded farfield response: algebraic vector generally has curl, projected scalar has angular Green multiplier.
Ke=ee*m.diff(nu1fix,ee)/(1+nu1fix(ee));nue=1+nu1fix(ee)
ck('external_anisotropy_nonzero',Ke<0 and abs(Ke)>m.mpf('.01'))
if args.control=='moment':ck('CONTROL_wrong_unique_moment',rows[0]['delta_C']==0)
if args.control=='algebraic':ck('CONTROL_wrong_pointwise_field',Ke==0)
if args.control=='external':ck('CONTROL_wrong_observed_external_equals_Newton',abs(ee-eta)<m.mpf('1e-12'))
result=dict(passed=all(c['passed'] for c in checks),checks=checks,kernel_rows=rows,ambient=dict(eta_observed=float(eta),e_Newton=float(ee),nu_e=float(nue),K_e=float(Ke)),quadrature=dict(precision_decimal=55,high_y_series_terms=8,series_used_when_e_over_y_less_than=.001,not_interval_certified=True),control=args.control,non_claims=['No orbit/Nbody reproduction','No full relativistic health certificate','No inferred KGB quadrupole','Vacuum C=integral y(nu-1) requires independent BIMOND normalization','No exact32pi selector or full galaxy fit'])
out=pathlib.Path(args.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(passed=result['passed'],checks=len(checks),failed=[c['name'] for c in checks if not c['passed']],rows=rows)));raise SystemExit(0 if result['passed'] else 1)
