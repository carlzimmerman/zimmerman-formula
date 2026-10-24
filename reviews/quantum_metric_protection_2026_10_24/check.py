"""Matter-induced metric action: exact frame and vacuum diagnostics."""
import argparse,json
from pathlib import Path
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--mutate',action='store_true');args=p.parse_args()
A,d,B,P,q=s.symbols('A d B P q',positive=True)
b,v,Vd=s.symbols('b v Vd',nonzero=True,real=True)
F=B+2*b*A**d
Z=-2*b*d*(d+1)*q**2*A**d
if args.mutate: Z=-Z
D=lambda f:q*A*s.diff(f,A)
K=s.factor(P*(Z/F+(d+1)/d*(D(F)/F)**2))
Q=s.factor(q-D(F)/(d*F))
checks=[]
def ck(name,e):
    r=s.factor(s.simplify(e));checks.append(dict(name=name,passed=r==0,residual=str(r)))
ck('general_dimension_diagonal_kinetic',K+2*b*d*(d+1)*q**2*A**d*B*P/F**2)
ck('general_dimension_matter_charge',Q-q*B/F)
ck('pure_induced_kinetic',K.subs(B,0))
ck('pure_induced_charge',Q.subs(B,0))
ck('no_induced_term_kinetic',K.subs(b,0))
ck('no_induced_term_charge',Q.subs(b,0)-q)
Zct=2*b*d*(d+1)*q**2*A**d*B/F
ck('additional_cancellation_counterterm',K+P*Zct/F)
w=s.symbols('w',positive=True)
F4=B+2*b*w
U=P**2*(Vd+v*w**2)/F4**2
Dt=lambda f:2*q*w*s.diff(f,w)
ck('vacuum_stationarity_equation',Dt(U)-4*q*P**2*w*(v*B*w-2*b*Vd)/F4**3)
wstar=2*b*Vd/(v*B)
ck('stationary_point',Dt(U).subs(w,wstar))
ck('stationary_vacuum',U.subs(w,wstar)-P**2*v*Vd/(v*B**2+4*b*b*Vd))
ck('pure_induced_vacuum',U.subs({B:0,Vd:0})-P**2*v/(4*b*b))
lam=s.symbols('lam',positive=True)
ck('common_vacuum_rescaling_keeps_extremum',wstar.subs({v:lam*v,Vd:lam*Vd})-wstar)
ck('common_vacuum_rescaling_changes_energy',U.subs({v:lam*v,Vd:lam*Vd})-lam*U)
# At any nondegenerate finite stationary point, use Vd=v B w/(2 b).
K4=K.subs({d:2,A:s.sqrt(w)})
stat={Vd:v*B*w/(2*b)}
ck('stationary_canonical_mass',s.cancel(Dt(Dt(U)).subs(stat)/K4)+4*U.subs(stat)/(3*P))
r=dict(mutated=args.mutate,passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,kinetic=str(K),charge=str(Q),scope='two-derivative induced metric action; stationary mass conditional on nonzero K; no full matter or gravity loop integration')
Path(args.output).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
