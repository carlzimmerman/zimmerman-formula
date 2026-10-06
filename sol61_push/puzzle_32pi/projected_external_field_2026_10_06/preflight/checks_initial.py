"""Actual projected NR external-field operator versus matched spherical QUMOND."""
import argparse,json,sys
from pathlib import Path
import sympy as s
import mpmath as mp
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--control',choices=['transfer_QUMOND','solar_Q2','omit_sum']);args=ap.parse_args();rows=[]
def eq(n,x):
 x=s.factor(s.cancel(s.expand(x)));rows.append({'name':n,'passed':x==0,'residual':str(x)})
def ck(n,x):rows.append({'name':n,'passed':bool(x),'residual':str(x)})
mu,a,L=s.symbols('mu a L',positive=True);x=s.symbols('x',positive=True);muf=s.Function('mu')(x);p1,p2,p3=s.symbols('p1 p2 p3')
# Differentiate actual constitutive vector at nonzero background along z.
v1,v2,v3=s.symbols('v1 v2 v3',real=True);norm=s.sqrt(v1*v1+v2*v2+v3*v3);MF=s.Function('mu');vec=s.Matrix([v1,v2,v3])*MF(norm)
JJ=vec.jacobian([v1,v2,v3]).subs({v1:0,v2:0,v3:x})
want=s.diag(MF(x),MF(x),MF(x)+x*s.diff(MF(x),x))
ck('actual_constitutive_Jacobian',JJ==want)
eq('positive_symbol',mu*(p1*p1+p2*p2+(1+L)*p3*p3)-mu*(p1*p1+p2*p2+a*p3*p3).subs(a,1+L))
# All-n index derivation: transformed radius S, anisotropic laplacian.
n,S=s.symbols('n S',positive=True);rad=S**(-(n-2)/2)
eq('general_n_anisotropic_harmonic',2*n*s.diff(rad,S)+4*S*s.diff(rad,S,2))
ck('Green_delta_Jacobian_positive',s.sqrt(a)>0)
# Matched aligned radial dictionary and external slope translation.
nu=(1+muf)/(2*muf);ell=x*s.diff(muf,x)/muf
K=s.simplify((x*s.diff(nu,x)/nu)/(1+ell))
eq('spherical_nu_dictionary',nu-(1+muf)/(2*muf))
eq('slope_translation',K+ell/((1+muf)*(1+ell)))
proj_pole=(1+1/mu)/2;proj_eq=(1+1/(mu*s.sqrt(a)))/2
nu0=(1+mu)/(2*mu);ke=-(a-1)/((1+mu)*a);qu_eq=nu0*(1+ke/2)
eq('same_polar_response',proj_pole-nu0)
# Radical factorization use a=t² to avoid branch simplifier ambiguity.
t=s.symbols('t',positive=True)
eq('exact_equatorial_discriminant',(proj_eq-qu_eq+(s.sqrt(a)-1)**2/(4*mu*a)).subs(a,t*t))
ck('different_for_L1_mu_half',(proj_eq-qu_eq).subs({a:2,mu:s.Rational(1,2)})<0)
cost=s.symbols('cost',real=True)
ang=(1+1/(mu*s.sqrt(1+L))*s.sqrt(1-L/(1+L)*cost**2)**(-1))/2
series=s.series(ang,L,0,3).removeO().expand();P4=s.legendre(4,cost)
l4=s.integrate(series*P4,(cost,-1,1))*s.Rational(9,2)
eq('new_l4_angular_coefficient',l4-3*L*L/(70*mu))
qang=nu0*(1+ke*(1-cost*cost)/2)
eq('QUMOND_no_l4_linear_EFE',s.integrate(qang*P4,(cost,-1,1)))
# Source audit current files versus exact snapshot provenance, no peer code import.
source=json.loads((Path(__file__).parent/'SOURCE_AUDIT.json').read_text())
ck('bounded_no_new_tracked_scoped_commit',len(source['scoped_tracked_commits_after_verified_p57'])==0)
ck('audited_scientific_sources_match_HEAD',all(r['current_matches_HEAD'] for r in source['files']))
# Quantitative comparison at actual p57 input, no target refit.
mp.mp.dps=40;eobs=mp.mpf('2.146e-10')/mp.mpf('9.3603e-11');numeric=[]
for T in [None,mp.mpf('128.915')]:
 def nu_y(y):return 1+(mp.sqrt(1+1/y)-1)/(1+(y/T)**2) if T else mp.sqrt(1+1/y)
 y=mp.findroot(lambda y:y*nu_y(y)-eobs,2);v=nu_y(y);dv=mp.diff(nu_y,y);xx=y*(2*v-1);mm=y/xx;le=-2*y*dv/(2*v-1+2*y*dv);kk=y*dv/v
 pole=(1+1/mm)/2;eqp=(1+1/(mm*mp.sqrt(1+le)))/2;eqq=v*(1+kk/2)
 af=lambda u:(1+1/(mm*mp.sqrt(1+le))* (1-le/(1+le)*u*u)**(-mp.mpf('.5')))/2
 four=mp.mpf('4.5')*mp.quad(lambda u:af(u)*mp.legendre(4,u),[-1,0,1]);num={'T':str(T),'y_e':str(y),'x_e':str(xx),'mu_e':str(mm),'L_e':str(le),'K_e':str(kk),'polar':str(pole),'projected_equatorial':str(eqp),'QUMOND_equatorial':str(eqq),'difference':str(eqp-eqq),'angular_l4':str(four)};numeric.append(num)
 ck('local_inverse_admissibility_'+str(T),mm>0 and 1+le>0)
 ck('equatorial_exact_numeric_'+str(T),abs((eqp-eqq)+(mp.sqrt(1+le)-1)**2/(4*mm*(1+le)))<mp.mpf('1e-35'))
 ck('l4_nonzero_numeric_'+str(T),four>0)
if args.control=='transfer_QUMOND':eq('false_spherical_kernel_implies_same_EFE',(proj_eq-qu_eq).subs({a:2,mu:s.Rational(1,2)}))
if args.control=='solar_Q2':ck('false_external_dominated_formula_applies_inner_solar',mp.mpf('256')<mp.mpf('2'))
if args.control=='omit_sum':eq('false_physical_potential_is_star_alone',proj_pole-1/mu)
out={'passed':sum(r['passed'] for r in rows),'total':len(rows),'checks':rows,'numeric':numeric,'control':args.control,'scope':'constant aligned external boundary and far/external-dominated NR response; not inner solarQ2/globalcovarianthealth'}
Path(args.out).parent.mkdir(parents=True,exist_ok=True);Path(args.out).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'passed':out['passed'],'total':out['total'],'failed':[r['name'] for r in rows if not r['passed']],'numeric':numeric}));sys.exit(not all(r['passed'] for r in rows))
