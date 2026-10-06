"""Exact evolving de Sitter TT screen, with bounded asymptotic numerical controls."""
import argparse,json,sys
from pathlib import Path
import sympy as s
from scipy.special import yv
import numpy as np
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--mutation',choices=['drop_curvature_mass','freeze_physical_momentum']);args=ap.parse_args();rows=[]
def eq(name,e):
 e=s.factor(s.cancel(e));rows.append({'name':name,'passed':e==0,'detail':str(e)})
def ck(name,b,e=''):rows.append({'name':name,'passed':bool(b),'detail':str(e)})
x,n,m,nu,K,H=s.symbols('x n m nu K H',positive=True)
alpha=4*m*n/(1-2*m);Y=s.Function('Y')(x);D=x**(n/2)*Y
alpha_used=0 if args.mutation=='drop_curvature_mass' else alpha
op=x*x*s.diff(D,x,2)+(1-n)*x*s.diff(D,x)+(x*x-alpha_used)*D
expected=x**(n/2)*(x*x*s.diff(Y,x,2)+x*s.diff(Y,x)+(x*x-n*n/4-alpha)*Y)
eq('exact_nonautonomous_Bessel_reduction',s.simplify(op-expected))
r=-n/2+nu
eq('late_characteristic_root',s.expand(r*r+n*r-alpha).subs(nu**2,n*n/4+alpha))
B=s.symbols('B',positive=True);mm=(B-1)/(2*B-1)
eq('source_enhancement_inversion',(1-mm)/(1-2*mm)-B)
eq('enhancement_growth_relation',alpha.subs(m,mm)-4*n*(B-1))
eq('enhancement_kinetic_cost',K*(1-2*mm)/8-K/(8*(2*B-1)))
eq('kinetic_zero_critical', (K*(1-2*m)/8).subs(m,s.Rational(1,2)))
# Raw curvature action Euler matches the time-evolving equation.
t=s.symbols('t');d=s.Function('d')(t);a=s.exp(H*t);q=K*(1-2*m)/8;k=s.symbols('k',positive=True)
L=a**n*(q*(s.diff(d,t)**2-k*k*d*d/a**2)+K*m*n*H*H*d*d/2)
EL=s.diff(s.diff(L,s.diff(d,t)),t)-s.diff(L,d)
eq('action_to_full_comoving_EOM',s.simplify(EL/(2*q*a**n)-(s.diff(d,t,2)+n*H*s.diff(d,t)+(k*k/a**2-alpha*H*H)*d)))
# Frobenius decaying branch y=x^nu sum a_j x^(2j), proved recurrence.
coeff=s.S(1);pol=s.S(1)
for j in range(1,7):coeff=-coeff/(4*j*(j+nu));pol+=coeff*x**(2*j)
f=x**nu*pol;res=s.expand(x*x*s.diff(f,x,2)+x*s.diff(f,x)+(x*x-nu*nu)*f)
eq('Frobenius_exact_six_coefficients',s.simplify(res-(coeff*x**(nu+14))))
# Reduction of order yields the growing root from the decaying branch.
rr=-n/2-nu;integrand=s.exp(-n*H*t)/s.exp(2*rr*H*t)
eq('reduction_order_integrand_exponent',s.simplify(integrand-s.exp(2*nu*H*t)))
eq('growing_root_from_reduction',rr+2*nu-(-n/2+nu))
for N in [3,4,8]:
 for M in [s.Rational(1,20),s.Rational(1,8),s.Rational(1,4),s.Rational(49,100)]:
  al=alpha.subs({n:N,m:M});v=s.sqrt(s.Rational(N*N,4)+al);rate=v-s.Rational(N,2)
  ck('positive_slope_grows_n%d_m%s'%(N,M),rate>0,rate)
 for M in [-s.Rational(1,4),s.S(0),-s.S(10)]:
  al=alpha.subs({n:N,m:M});v2=s.Rational(N*N,4)+al
  ck('nonpositive_slope_no_positive_root_n%d_m%s'%(N,M),al<=0 and v2<=s.Rational(N*N,4),v2)
 ck('supercritical_TT_negative_kinetic_n%d'%N,(1-2*s.Rational(3,4))<0)
# Bounded exact-Bessel transfer, not a nonlinear trajectory.
examples=[]
for M in [.05,.125,.25,.49]:
 N=3;v=np.sqrt(N*N/4+4*M*N/(1-2*M));rate=v-N/2;Nend=4.;x0=.01;xf=x0*np.exp(-Nend)
 xf_used=x0 if args.mutation=='freeze_physical_momentum' else xf
 transfer=np.exp(-N*Nend/2)*yv(v,xf_used)/yv(v,x0);reference=np.exp(rate*Nend)
 rel=transfer/reference-1
 ck('evolving_transfer_growth_m'+str(M),abs(rel)<1e-4,rel)
 examples.append({'n':N,'m':M,'nu':float(v),'growth_rate_over_H':float(rate),'initial_p_over_H':x0,'delta_lna':Nend,'normalized_Ybranch_transfer':float(transfer),'leading_late_growth':float(reference),'relative_asymptotic_error':float(rel),'source_enhancement':(1-M)/(1-2*M)})
args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps({'passed':sum(r['passed'] for r in rows),'total':len(rows),'checks':rows,'examples':examples,'mutation':args.mutation,'scope':'exact conditional TT action plus bounded linear-mode asymptotic check'},indent=2)+'\n');print(json.dumps({'passed':sum(r['passed'] for r in rows),'total':len(rows),'failed':[r for r in rows if not r['passed']]}));sys.exit(0 if all(r['passed'] for r in rows) else 1)
