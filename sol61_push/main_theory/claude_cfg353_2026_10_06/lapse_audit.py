"""Independent lapse-weighted auxiliary-action variation; never executes Claude code."""
import argparse,json
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--output-dir',required=True,type=Path);ap.add_argument('--mutation',choices=['none','drop_lapse_adjoint','unweighted_global_zero'],default='none');a=ap.parse_args();base=Path(__file__).resolve().parent;o=a.output_dir.resolve();o.relative_to(base);o.mkdir(parents=True,exist_ok=True)
x=s.symbols('x',real=True);alpha,beta,nu,k,rb=s.symbols('alpha beta nu k rhobar',real=True)
N,mu,phi,rho,LM=[s.Function(n)(x) for n in ['N','mu','phi','rho','L_M']]
f=s.exp(alpha*phi*phi+beta*s.diff(phi,x)**2)
L=N*(mu*(s.diff(phi,x,2)-k*(rho-rb))+nu*phi+LM*f)
def el(q):return s.diff(L,q)-s.diff(s.diff(L,s.diff(q,x)),x)+s.diff(s.diff(L,s.diff(q,x,2)),x,2)
checks={}
def ck(n,v):checks[n]=bool(v);print(('PASS ' if v else 'FAIL ')+n)
ck('primal_unweighted_leaf_Poisson',s.simplify(el(mu)-N*(s.diff(phi,x,2)-k*(rho-rb)))==0)
adjoint=s.diff(N*mu,x,2)+N*nu+N*LM*2*alpha*phi*f-s.diff(N*LM*2*beta*s.diff(phi,x)*f,x)
if a.mutation=='drop_lapse_adjoint':adjoint+=N*s.diff(mu,x,2)-s.diff(N*mu,x,2)
ck('full_lapse_weighted_adjoint',s.simplify(el(phi)-adjoint)==0)
epsilon=s.symbols('epsilon',positive=True);nn=1+epsilon*s.cos(x);pp=s.cos(x)
weighted=s.integrate(nn*pp,(x,0,2*s.pi));unweighted=s.integrate(pp,(x,0,2*s.pi))
ck('periodic_zero_convention_counterexample',weighted==s.pi*epsilon and unweighted==0)
shift=epsilon/2 if a.mutation!='unweighted_global_zero' else s.Integer(0)
ck('actual_global_multiplier_zero',s.simplify(s.integrate(nn*(pp-shift),(x,0,2*s.pi)))==0)
mm=s.cos(x);diff=s.diff(nn*mm,x,2)-s.diff(nn*s.diff(mm,x),x)
ck('adjoint_is_not_weighted_divergence',s.trigsimp(diff+epsilon*s.cos(2*x))==0)
# Explicit discrete density variation including the unweighted source average.
r1,r2,n1,n2,m1,m2,w1,w2=s.symbols('r1 r2 n1 n2 m1 m2 w1 w2',positive=True)
rbar=(w1*r1+w2*r2)/(w1+w2);E=-k*(w1*n1*m1*(r1-rbar)+w2*n2*m2*(r2-rbar));avg=(w1*n1*m1+w2*n2*m2)/(w1+w2)
ck('source_average_reaction',s.simplify(s.diff(E,r1)+k*w1*(n1*m1-avg))==0)
# At any positive-lapse weighted zero, a nonconstant continuous potential must cross zero.
controls=[]
for ee in [s.Rational(1,10),s.Rational(1,2),s.Rational(9,10)]:
 ph=s.cos(x)-ee/2;root=s.acos(ee/2);grad2=s.simplify(s.diff(ph,x).subs(x,root)**2)
 controls.append({'epsilon':str(ee),'constant_shift':str(ee/2),'gradient_squared_at_nodal_zero':str(grad2)})
ck('weighted_zero_does_not_remove_nodal_failure',all(s.Rational(z['gradient_squared_at_nodal_zero'])>0 for z in controls))
(o/'results.json').write_text(json.dumps({'checks':checks,'periodic_controls':controls,'mutation':a.mutation,'limitations':['No Claude execution or metrichealth audit','Flatleaf symbolic controls test variablelapse only','Doesnotauthenticate earlier galaxy or numericalscores']},indent=2)+'\n');raise SystemExit(0 if all(checks.values()) else 1)
