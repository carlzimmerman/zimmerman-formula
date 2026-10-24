"""Symbolic constant-X self-tuning selector checks; no observed inputs."""
import argparse,json
from pathlib import Path
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--mutate',action='store_true');args=p.parse_args()
X,h,M2,A,Xr,B0=s.symbols('X h M2 A Xref B0',positive=True)
H,V,n=s.symbols('H V n',real=True)
K=s.Function('K')(X);B=s.Function('B')(X)
kx=s.diff(K,X);kxx=s.diff(K,X,2)
gx=(-1 if not args.mutate else 1)*kx/(3*h*s.sqrt(2*X));gxx=s.diff(gx,X)
J=s.sqrt(2*X)*kx+6*H*X*gx
rho_phi=2*X*kx-K+6*H*s.sqrt(2*X)*X*gx
F=kx+4*h*s.sqrt(2*X)*gx-2*X**2*gx**2/M2
Q=kx+2*X*kxx+6*h*s.sqrt(2*X)*gx+6*X**2*gx**2/M2+6*h*X*s.sqrt(2*X)*gxx
checks=[]
def ck(name,expr):
 r=s.factor(s.simplify(expr));checks.append({'name':name,'residual':str(r),'passed':r==0})
ck('current_factorization',J-s.sqrt(2*X)*kx*(1-H/h))
ck('vacuum_energy_cancellation',rho_phi.subs(H,h)+K)
ck('gradient_coefficient',F+kx/3+X*kx**2/(9*M2*h*h))
ck('kinetic_coefficient',Q-X*kx**2/(3*M2*h*h))
logK=-A*s.log(X/Xr)
logsubs={s.diff(K,X,2):s.diff(logK,X,2),s.diff(K,X):s.diff(logK,X)}
Fl=A/(3*X)*(1-A/(3*M2*h*h));Ql=A*A/(3*M2*h*h*X)
ck('log_gradient',F.subs(logsubs)-Fl)
ck('log_kinetic',Q.subs(logsubs)-Ql)
ck('log_sound_speed',Fl/Ql-(M2*h*h/A-s.Rational(1,3)))
Xs=Xr*s.exp((3*M2*h*h-V)/A)
ck('constant_X_background',logK.subs(X,Xs)-(V-3*M2*h*h))
ck('vacuum_adjustment_sensitivity',s.diff(Xs,V)+Xs/A)
# Response here is a conditional bare static coefficient with fixed source conversion.
a0=1/B
dX_dV=1/kx
sensitivity=(-1 if not args.mutate else 1)*s.diff(B,X)/(B*kx)
ck('response_chain_rule',s.diff(s.log(a0),X)*dX_dV-sensitivity)
Bp=B0*(X/Xr)**n
ln_a0_on_branch=-s.log(B0)-n*(3*M2*h*h-V)/A
ck('power_response_sensitivity',s.diff(ln_a0_on_branch,V)-n/A)
ck('power_chain_rule',(-s.diff(Bp,X)/(Bp*s.diff(logK,X))).subs(X,Xs)-n/A)
# Vacuum-insensitive normalization: |acceleration|^3 has a zero second jet.
z,b,theta,Omega,I=s.symbols('z b Theta Omega integral_O',positive=True)
for j in range(3): ck('cubic_vacuum_jet_'+str(j),s.diff(b*z**3/theta,z,j).subs(z,0))
W=s.Function('W')(b)
S=-b*I-Omega*W
ck('promoted_coefficient_equation',s.diff(S,b)+I+Omega*s.diff(W,b))
ck('no_potential_equation',s.diff(-b*I,b)+I)
result={'mutated':args.mutate,'checks':checks,'passed':sum(c['passed'] for c in checks),'total':len(checks),'scope':'four-dimensional KGB vacuum health; conditional bare response sensitivity; no full halo matching or microscopic completion'}
Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
