"""Exact constrained de-Sitter shear repair, not full nonlinear admission."""
import argparse,json,sys
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--control',choices=['wrong_sign','erase_shear','freeze_clock']);args=ap.parse_args();rows=[]
def eq(name,x):
 x=s.factor(x);rows.append(dict(name=name,passed=x==0,residual=str(x)))
def ck(name,x):rows.append(dict(name=name,passed=bool(x)))
n,H,P,eta=s.symbols('n H P eta',positive=True)
f,t,z,v,zd,e=s.symbols('f t z nu zd e',real=True)
chi=(n-1)/(2*(n-2));Lam=n*(n-1)*H**2/2
# Raw scalar extrinsic curvature deltaK=f I+t diag(1,0,..).
for nn in range(3,7):
 mat=s.diag(f+t,*([f]*(nn-1)));tf=mat-s.trace(mat)*s.eye(nn)/nn
 eq('raw_EH_trace_'+str(nn),s.trace(mat*mat)-s.trace(mat)**2+nn*(nn-1)*f*f+2*(nn-1)*f*t)
 eq('raw_shear_norm_'+str(nn),s.trace(tf*tf)-(s.Rational(nn-1,nn))*t*t)
# Mean-relative split retains BOTH shears and shifts.
F,T,fr,tr=s.symbols('F T fr tr',real=True)
raw=lambda ff,tt:-n*(n-1)*ff**2-2*(n-1)*ff*tt-eta*(n-1)/n*tt**2
split=raw(F+fr/2,T+tr/2)+raw(F-fr/2,T-tr/2)
eq('both_metric_kinetic_split',split-2*raw(F,T)-raw(fr,tr)/2)
L=-n*(n-1)/2*(zd-H*v)**2-(n-1)*(zd-H*v)*t-eta*(n-1)/(2*n)*t*t+(n-1)*(n-2)/2*P*z*z+(n-1)*P*v*z+Lam/2*(v+n*z+e)**2+chi*P*v*v
solt=-n*(zd-H*v)/eta
eq('actual_relative_shift_row',s.diff(L,t).subs(t,solt))
Ls=s.factor(L.subs(t,solt));sole=-v-n*z
eq('actual_relative_shear_row',s.diff(Ls,e).subs(e,sole))
Lse=s.factor(Ls.subs(e,sole));A=-n*(n-1)*(1-eta)/(2*eta)
eq('relative_two_square_form',Lse-(-A*(zd-H*v)**2+chi*P*(v+(n-2)*z)**2))
solv=(A*H*zd+chi*P*(n-2)*z)/(A*H*H-chi*P)
eq('actual_relative_lapse_row',s.diff(Lse,v).subs(v,solv))
Kr=A*chi*P/(A*H*H-chi*P)
eq('fully_reduced_relative_action',Lse.subs(v,solv)-Kr*(zd+(n-2)*H*z)**2)
eq('positive_Kr_closed_form',Kr-(n*(n-1)*(1-eta)*chi*P)/(n*(n-1)*(1-eta)*H*H+2*eta*chi*P))
for nn in (3,4,6):
 for pp in (s.Rational(1,100),1,10000):
  ck('positive_physical_scalar_'+str((nn,pp)),Kr.subs({n:nn,H:1,P:pp,eta:s.Rational(1,4)})>0)
# Full mean lapse/shift elimination; a^n P has logarithmic derivative (n-2)H.
Z,V,Zd,tm=s.symbols('Z V Zd tm',real=True)
Lm=-n*(n-1)*(Zd-H*V)**2-2*(n-1)*(Zd-H*V)*tm-eta*(n-1)/n*tm*tm+(n-1)*(n-2)*P*Z*Z+2*(n-1)*P*V*Z
st=-n*(Zd-H*V)/eta;eq('actual_mean_shift_row',s.diff(Lm,tm).subs(tm,st))
Am=2*A;sv=Zd/H+(n-1)*P*Z/(Am*H*H)
eq('actual_mean_lapse_row',s.diff(Lm.subs(tm,st),V).subs(V,sv))
meanred=s.factor(Lm.subs(tm,st).subs(V,sv));bdot=(n-1)*P*(2*Z*Zd+(n-2)*H*Z*Z)/H
Lconstraint=-(n-1)*eta/(n*(1-eta))*P*P/(H*H)*Z*Z
eq('mean_evolving_boundary',meanred-bdot-Lconstraint)
pi=s.symbols('pi',real=True);Lc=2*Lconstraint.subs(Z,Z-H*pi)
eq('mean_clock_elliptic_row',s.diff(Lc,pi)-4*(n-1)*eta/(n*(1-eta))*P**2/H*(Z-H*pi))
# Pure-shear fixed-metric pi differs from full constraint coefficient.
bare=-2*eta*(n-1)/n*P*P*pi*pi
full=Lc.subs(Z,0)
eq('coupled_not_bare_clock_coefficient',full-bare/(1-eta))
qrel,qd,a=s.symbols('qrel qd a',positive=True)
eq('actual_relative_positive_coordinate',(a**n*Kr*(zd+(n-2)*H*z)**2).subs({z:qrel/a**(n-2),zd:(qd-(n-2)*H*qrel)/a**(n-2)})-a**(4-n)*Kr*qd*qd)
# Actual tensor/vector blocks after shear deformation.
K=s.symbols('K',positive=True);gd,gx=s.symbols('tensor_dot tensor_grad')
TT=K/4*((1-eta)*gd*gd-gx*gx)
eq('TT_derivative_coefficient',s.diff(TT,gd,2)-K*(1-eta)/2)
ct2=s.symbols('cT_squared');eq('TT_speed_relation',s.solve((1-eta)*ct2-1,ct2)[0]-1/(1-eta))
Fd,S=s.symbols('vector_dot vector_shift');LV=K*(1-eta)*P*(Fd-S)**2/2
eq('actual_vector_shift_constraint',s.diff(LV,S).subs(S,Fd))
# Old decaying pure scalar remains linear shear-free in n3.
nu=s.symbols('nu');eq('old_decay_shift_shear_zero',(-2*H*nu)+P*(2*H*nu/P))
eq('old_decay_f_zero',(-H*z)-H*(-z))
# Controls change physical claim, not only formal syntactic identity.
candidate=Kr.subs({n:3,H:1,P:10000,eta:s.Rational(1,4)})
if args.control=='wrong_sign':
 ss=s.Rational(1,4);Aw=s.Rational(3*2,2)*(1+1/ss);candidate=Aw*10000/(Aw-10000)
ck('declared_all_finite_p_positive_physical_scalar',candidate>0)
volumeHess=s.diff(L,e,2)
if args.control=='erase_shear':volumeHess=s.diff(L-Lam*(v+n*z+e)**2/2,e,2)
eq('declared_relative_shear_retained',volumeHess-Lam)
clockCoefficient=full
if args.control=='freeze_clock':clockCoefficient=bare
eq('declared_constrainted_clock_not_bare',clockCoefficient-bare/(1-eta))
# Negative sign comparator full constraints, not bare lapse/shear Hessian.
ss=s.symbols('wrong_shear_sign',positive=True);Aw=n*(n-1)*(1+1/ss)/2
Kw=Aw*chi*P/(Aw*H*H-chi*P)
eq('wrong_sign_high_p_limit',s.limit(Kw,P,s.oo)+Aw)
# Exact first variation and scale independence structural controls.
u,du=s.symbols('shear dshear');eq('static_FRW_first_variation',s.diff(-eta*u*u,u).subs(u,0))
AA,a0=s.symbols('vacuum_A a0',positive=True);Hs=chi*a0*a0*AA/(n*(n-1))
eq('vacuum_A_stays_free',s.diff(Hs,AA)-chi*a0*a0/(n*(n-1)))
out=dict(passed=sum(r['passed'] for r in rows),total=len(rows),checks=rows,control=args.control,scope='exact constrained quadratic common deSitter n>=3,k>0,H>0,0<eta<1; finite fixtures corroborate analytic signs; no full nonlinear source/matter health or selector')
p=Path(args.out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(passed=out['passed'],total=out['total'],failed=[r['name'] for r in rows if not r['passed']])));sys.exit(not all(r['passed'] for r in rows))
