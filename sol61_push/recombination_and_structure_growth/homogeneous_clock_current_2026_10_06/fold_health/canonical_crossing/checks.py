import argparse,json
from pathlib import Path
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--omit-clock-density',action='store_true');a=p.parse_args()
M,rho,theta,A,adot,pp,H=s.symbols('M rho theta A adot pp H',nonzero=True)
z,v,pi,P=s.symbols('z v pi P');d=M/theta;e=rho/(2*theta);T=2*M*pp+3*rho
S=(A-3*M)*theta**2/M**2;zd=(P-rho*A*v/M-d*T*z+d*pi)/(2*A)
nu=d*zd+e*v;R=2*S*nu+6*theta*zd+T*z-pi
pd=e*R-rho*pp*v-3*H*pi
Pd=2*M*pp*z+T*nu-3*H*P
flow=s.Matrix([zd,nu,pd,Pd]);ys=s.Matrix([z,v,pi,P]);N=s.simplify((A*flow.jacobian(ys)).applyfunc(s.cancel).subs(A,0)/adot)
c=s.Matrix([1,d,0,T*d]);r=s.Matrix([[-d*T,0,d,1]])
checks=[]
def ck(n,b):checks.append({'name':n,'passed':bool(b)})
ck('exact_full_EOM_residue',s.simplify(N-c*r/(2*adot))==s.zeros(4))
ck('nonzero_residue',N[0,3]!=0)
ck('nilpotent_rank_one',s.simplify(N*N)==s.zeros(4) and N.rank()==1)
ck('dust_density_equation_regular',s.simplify((A*pd).subs(A,0))==0)
ck('log_solution_residue',s.simplify(N*(s.eye(4)+N*s.symbols('logtau'))-N)==s.zeros(4))
used=r.copy()
if a.omit_clock_density:used[0,2]=0
ck('compatibility_includes_clock_density',used==r)
B=s.factor(S*e**2-rho*pp/2)
ck('dust_elimination_regular_at_zero',s.simplify(B.subs(A,0)+3*rho**2/(4*M)+rho*pp/2)==0)
ck('velocity_mixing_vanishes_at_zero',s.simplify(2*e*(S*d+3*theta)-rho*A/M)==0)
ck('clock_invariant_has_pole_direction',s.simplify(s.cancel(2*A*nu).subs(A,0)-d*(r*ys)[0])==0)
out={'checks':checks,'summary':{'passed':sum(c['passed'] for c in checks),'total':len(checks)},'scope':'Symbolic residue of full finite-mode linear equations at an analytic simple Kc zero; no quantum or nonlinear verdict.'}
Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out['summary']));raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
