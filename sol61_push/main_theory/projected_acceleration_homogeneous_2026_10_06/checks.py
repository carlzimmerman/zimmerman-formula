import argparse, json, sys
from pathlib import Path
import sympy as s

ap=argparse.ArgumentParser()
ap.add_argument('--output',required=True)
ap.add_argument('--control',choices=['none','frozen_lapse','free_offset'],default='none')
args=ap.parse_args(); checks=[]
def ck(name,value,detail=''):checks.append(dict(name=name,passed=bool(value),detail=str(detail)))
def eq(name,expr):
    expr=s.simplify(expr);ck(name,expr==0,expr)
B,V,U,t,ratio,ell=s.symbols('B V U t ratio ell',positive=True)
v=s.symbols('v',real=True)
# ratio=exp[(n zeta-r)/2], a useful exact independent variable.
kin=-B*V/ell*(ratio*(t+v/2)**2+(t-v/2)**2/ratio)
rr=(t-v/2)/(t+v/2)
eq('relative_lapse_stationarity',s.diff(kin,ratio).subs(ratio,rr))
red=s.factor(kin.subs(ratio,rr))
eq('reduced_kinetic',red+2*B*V/ell*(t*t-v*v/4))
eq('relative_lapse_nonzero_curvature',s.diff(kin,ratio,2).subs(ratio,rr)+2*B*V*(t+v/2)**3/(ell*(t-v/2)))
L=red-ell*U
pt=s.diff(L,t);pz=s.diff(L,v)
eq('tau_momentum',pt+4*B*V*t/ell)
eq('zeta_momentum',pz-B*V*v/ell)
P,Q=s.symbols('P Q',real=True)
repl={t:-ell*P/(4*B*V),v:ell*Q/(B*V)}
ham=s.simplify((pt*t+pz*v-L).subs(repl))
C=-P*P/(8*B*V)+Q*Q/(2*B*V)+U
eq('canonical_hamiltonian',ham-ell*C)
eq('common_constraint_from_ell',(-s.diff(L,ell)).subs(repl)-C)
eq('constraint_velocity_equivalence',C.subs({P:pt,Q:pz})+2*B*V/ell**2*(t*t-v*v/4)-U)
M=s.symbols('M',positive=True)
eq('expanding_constraint_solution',C.subs({P:-2*s.sqrt(Q*Q+M*M),U:M*M/(2*B*V)}))
H=2*s.sqrt(Q*Q+M*M)
eq('relative_velocity',s.diff(H,Q)-2*Q/s.sqrt(Q*Q+M*M))
eq('positive_relational_Hessian',s.diff(H,Q,2)-2*M*M/(Q*Q+M*M)**s.Rational(3,2))
ck('Hamiltonian_Hessian_positive',s.diff(H,Q,2).simplify().is_positive)
w=s.symbols('w',real=True)
Lj=-2*M*s.sqrt(1-w*w/4)
eq('relational_momentum',s.diff(Lj,w)-M*w/(2*s.sqrt(1-w*w/4)))
eq('relational_Lagrangian_Hessian',s.diff(Lj,w,2)-M/(2*(1-w*w/4)**s.Rational(3,2)))
ww=2*Q/s.sqrt(Q*Q+M*M)
eq('inverse_relational_momentum',s.diff(Lj,w).subs(w,ww)-Q)
eq('velocity_inside_expanding_patch',1-ww*ww/4-M*M/(Q*Q+M*M))
n,tau,m0,Z=s.symbols('n tau m0 Z',positive=True)
mass=m0*s.exp(n*tau)
q=s.asinh(Q/mass)
zeta=Z-2*q/n
eq('exact_relative_solution',s.diff(zeta,tau)-2*Q/s.sqrt(Q*Q+mass*mass))
# log-ratio formula is checked algebraically through exponentials on |w|<2.
q0=s.symbols('q0',real=True)
eq('reconstructed_lapse_ratio',(s.exp(2*q0)*(1-s.tanh(q0))-(1+s.tanh(q0))).rewrite(s.exp))
eq('late_relative_velocity',s.limit(s.diff(zeta,tau),tau,s.oo))
eq('coincident_relative_metric_kinetic',s.diff(Lj,w,2).subs(w,0)-M/2)
K,a0,A,chi=s.symbols('K a0 A chi',positive=True)
bb=K*n*(n-1)
H2=chi*a0*a0*A/(n*(n-1))
eq('common_deSitter_constraint',-2*bb*H2+2*K*chi*a0*a0*A)
eq('vacuum_dictionary',n*(n-1)*H2/2-chi*a0*a0*A/2)
ck('vacuum_offset_remains_free',s.diff(H2,A)!=0)
X,Y,r=s.symbols('X Y r',positive=True)
Cr=-X*s.exp(r/2)-Y*s.exp(-r/2)
eq('relative_lapse_secondary_stationarity',s.diff(Cr,r).subs(r,s.log(Y/X)))
eq('relative_lapse_constraint_bracket',s.diff(Cr,r,2).subs(r,s.log(Y/X))+s.sqrt(X*Y)/2)
ck('second_class_relative_pair',(-s.sqrt(X*Y)/2).is_negative)
if args.control=='frozen_lapse':
    frozen=kin.subs(ratio,1)
    ck('false_positive_relative_kinetic_at_frozen_lapse',s.diff(frozen,v,2).is_positive)
if args.control=='free_offset':
    eq('false_selected_offset',s.diff(H2,A))
out=dict(passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,control=args.control,scope='exact homogeneous both-expanding metric sector; no finite-k or clock degree count')
p=Path(args.output);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2))
print(json.dumps(dict(passed=out['passed'],total=out['total'],failures=[c for c in checks if not c['passed']])))
sys.exit(out['passed']!=out['total'])
