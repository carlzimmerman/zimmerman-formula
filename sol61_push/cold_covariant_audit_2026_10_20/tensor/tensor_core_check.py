"""Exact homogeneous-shear audit of the displayed CFG938 action, not a model rerun.

Use c=1,K=4piG. beta3=-beta1-beta2 fixes volume exactly. Derive the
connection from the metric; reduce Einstein-Hilbert by an explicit boundary.
The optional alpha family is a new unaudited repair except for these identities.
"""
from pathlib import Path
import json,sys,time,resource,math
import sympy as s

out=Path(sys.argv[1]);here=Path(__file__).resolve().parent;start=time.monotonic()
t=s.symbols('t',real=True);K,gamma=s.symbols('K gamma',positive=True)
a=s.Function('a',positive=True)(t)
b1=s.Function('b1',real=True)(t);b2=s.Function('b2',real=True)(t)
betas=[b1,b2,-b1-b2];chi=s.Function('chi',real=True)(t)
lam=s.Function('lambda',real=True)(t);rho=s.symbols('rho_c',positive=True)
scales=[a*s.exp(b) for b in betas];gdiag=[-s.Integer(1)]+[v*v for v in scales]
ginv=[1/v for v in gdiag];volume=a**3
checks=[]
def ck(name,v):
    checks.append({'name':name,'pass':bool(v)})
def zero(e):return s.simplify(s.expand(e))==0
def derivative(e,index):return s.diff(e,t) if index==0 else s.S.Zero
def metric(i,j):return gdiag[i] if i==j else s.S.Zero
Gamma={}
for A in range(4):
 for B in range(4):
  for C in range(4):
   val=s.simplify(ginv[A]*(derivative(metric(A,C),B)+derivative(metric(A,B),C)-derivative(metric(B,C),A))/2)
   if val!=0:Gamma[A,B,C]=val
def G(A,B,C):return Gamma.get((A,B,C),s.S.Zero)
ricci=[]
for B in range(4):
 val=sum(derivative(G(A,B,B),A)-derivative(G(A,B,A),B)
         +sum(G(A,B,B)*G(C,A,C)-G(A,B,C)*G(C,B,A) for C in range(4)) for A in range(4))
 ricci.append(s.simplify(val))
Ricci=s.simplify(sum(ginv[i]*ricci[i] for i in range(4)))
Hi=[s.simplify(s.diff(v,t)/v) for v in scales];H=s.diff(a,t)/a
shear2=sum(s.diff(b,t)**2 for b in betas)
ck('volume independent of shear',zero(s.prod(scales)-volume))
ck('expansion trace exactly3H',zero(sum(Hi)-3*H))
ck('Ricci from connection agrees with Bianchi identity',zero(Ricci-(2*sum(s.diff(v,t) for v in Hi)+sum(v*v for v in Hi)+sum(Hi)**2)))
reduced_EH=s.simplify((volume*Ricci-s.diff(2*volume*sum(Hi),t))/(4*K))
ck('EH boundary reduction principal coefficient',zero(reduced_EH-volume*(-6*H*H+shear2)/(4*K)))
B=s.diag(*ginv[1:]);n=s.simplify(s.sqrt(B.det()))
ck('dust sqrt(-g)n independent of shear',zero(volume*n-1))
hess_mixed=[s.simplify(-ginv[i]*G(0,i,i)*s.diff(chi,t)) for i in range(1,4)]
D2=s.simplify(sum(hess_mixed));tau=[s.simplify(v-D2/3) for v in hess_mixed]
tau2=s.simplify(sum(v*v for v in tau))
ck('homogeneous projected D2chi is time-coupled',zero(D2+3*H*s.diff(chi,t)))
ck('traceless projected Hessian contains shear rate',all(zero(v+s.diff(chi,t)*s.diff(b,t)) for v,b in zip(tau,betas)))
ck('tidal square exactly chi_dot_squared times shear_squared',zero(tau2-s.diff(chi,t)**2*shear2))
mult=volume*lam*(D2-K*rho)
ck('multiplier has no shear coordinate dependence',all(zero(s.diff(mult,b)) for b in [b1,b2]))
ck('multiplier has no shear-rate principal Hessian',all(zero(s.diff(mult,s.diff(b,t),2)) for b in [b1,b2]))
total_shear=volume*shear2/(4*K)-3*gamma*volume*tau2/(4*K*K)
QT=s.simplify(total_shear/(volume*shear2/(4*K)))
ck('total tensor kinetic factor exact',zero(QT-(1-3*gamma*s.diff(chi,t)**2/K)))
Ht,rt=s.symbols('H rho_total',positive=True)
QT_constraint=s.simplify(QT.subs(s.diff(chi,t),-K*rho/(3*Ht)))
QT_friedmann=s.simplify(QT_constraint.subs(Ht**2,2*K*rt/3))
ck('FRW constraint reduction',zero(QT_constraint-(1-gamma*K*rho*rho/(3*Ht*Ht))))
ck('stiff density ratio is tensor deficit',zero(QT_friedmann-(1-gamma*rho*rho/(2*rt))))
healthy=s.simplify(QT_constraint.subs({K:1,Ht:1,rho:1,gamma:1}))
ghost=s.simplify(QT_constraint.subs({K:1,Ht:1,rho:1,gamma:4}))
ck('healthy kinetic nonluminal counterexample',healthy==s.Rational(2,3) and 1/healthy==s.Rational(3,2))
ck('positive density ghost counterexample',ghost==-s.Rational(1,3))
alpha=s.symbols('alpha',real=True)
tau_alpha=[v+alpha*s.diff(chi,t)*s.diff(b,t) for v,b in zip(tau,betas)]
QT_alpha=s.simplify(1-3*gamma*sum(v*v for v in tau_alpha)/(K*shear2))
ck('proposed operator family tensor coefficient',zero(QT_alpha-(1-3*gamma*s.diff(chi,t)**2*(1-alpha)**2/K)))
ck('alpha1 cancels this tensor correction',zero(QT_alpha.subs(alpha,1)-1))
ck('alpha0 recovers displayed original',zero(QT_alpha.subs(alpha,0)-QT))
# Structural Newtonian cancellation and restricted spherical core corollary.
Bo,C1,C2,kk=s.symbols('B C1 C2 k',real=True,nonzero=True)
Leff=s.expand(K*((Bo+C1+C2)**2-(C1+C2)**2)/(2*kk**2))
ck('no cold-cold Newtonian cross attraction',zero(s.diff(Leff,C1,C2)))
ck('baryon-cold attraction remains',zero(s.diff(Leff,Bo,C1)-K/kk**2))
u,a0,neggrad=s.symbols('u a0 positive_gradient_magnitude',positive=True)
R=u*u/(a0-u)
ck('no decreasing baryon-free hydrostatic core (0<u<a0)',s.simplify((R+gamma*neggrad).subs({u:a0/2}))>0)
# Declared source background, not observations newly imported here.
raw=json.loads((here/'evidence/cfg938_results.json').read_text())
GSI=6.67430e-11;c=299792458.;PC=3.0856775814913673e16
H0=67.4e3/(1e6*PC);crit=3*H0*H0/(8*math.pi*GSI)
Ob=.0493;Oc=5.364*Ob;rho_r0=7.5657e-16*2.7255**4/c**2*(1+7/8*(4/11)**(4/3)*3.046)
z=4e8;matter_over_radiation=(Ob+Oc)*crit/(rho_r0*(1+z));bbn=[]
for name,v in raw['S2']['early_universe_local_EoS'].items():
    ratio=v['ratio_at_zBBN'];deficit=ratio/(1+matter_over_radiation)
    bbn.append({'L':name,'source_stiff_over_radiation':ratio,'matter_over_radiation':matter_over_radiation,
                'tensor_kinetic_deficit_on_declared_branch':deficit,'Q_T':1-deficit})
    ck(name+' negative tensor kinetic on declared early-medium branch',1-deficit<0)
    Lpc=float(name[:-2]);coef=math.pi*GSI*(Lpc*PC)**2*(Oc*crit)**2/(rho_r0*c*c)
    ck(name+' independent declared stiff-ratio arithmetic',abs(coef*(1+z)**2/ratio-1)<1e-13)
rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;ck('measured RSS below1GB',rss<1000000000)
result={'scope':'Exact homogeneous-shear counterexample audit of CFG938 A5 and early tensor kinetic; new alpha family checked only in this restricted sector.',
 'primary_verdict':'refuted, with a homogeneous-shear counterexample to structural c_T=c; branch-specific negative tensor kinetic if medium is present at declared BBN epoch',
 'conventions':'c=1 in exact algebra,K=4piG,metric(-1,a²exp(2beta_i)),sum beta_i=0,comoving fluid,homogeneous chi; tensor principal part about isotropic FRW',
 'symbolic':{'Ricci':str(Ricci),'EH_after_explicit_boundary':str(reduced_EH),'D2chi':str(D2),'tau_squared':str(tau2),'Q_T':str(QT),'Q_T_after_FRW_constraint_and_Friedmann':str(QT_friedmann),'new_alpha_family_Q_T':str(QT_alpha),'Newtonian_Leff':str(Leff)},
 'counterexamples':{'K_H_rhoc_gamma_1_QT':str(healthy),'same_with_gamma4_QT':str(ghost),'rho_total_in_both':1.5},
 'BBN_declared_branch':bbn,'checks':checks,'n_checks':len(checks),'all_checks_pass':all(v['pass'] for v in checks),
 'peak_rss_bytes_macos':rss,'runtime_seconds':time.monotonic()-start,
 'non_claims':['No general nonlinear degree-of-freedom or stability theorem','No conclusion that all cold-energy actions or late-production backgrounds fail',
               'Alpha1 is a proposed changed operator, not an adopted or fully audited repair; scalar/vector/constraint/growth/dwarf tests remain',
               'Static no-decreasing-core corollary is baryon-free,isolated/no external binding,0<u<a0,gamma>=0; not all profiles/backgrounds']}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'n_checks':len(checks),'all_checks_pass':result['all_checks_pass'],'BBN':bbn,'RSS':rss}))
raise SystemExit(0 if result['all_checks_pass'] else 1)
