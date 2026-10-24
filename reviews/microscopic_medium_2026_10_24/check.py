"""Exact first-derivative medium checks; no acceleration or target input."""
import argparse,json
from pathlib import Path
import sympy as s
p=s.symbols
cli=argparse.ArgumentParser();cli.add_argument('--output',required=True);cli.add_argument('--mutate',action='store_true');args=cli.parse_args()
mu,q,A,L,D=s.symbols('mu q A L D',positive=True)
a,b,gamma,M=s.symbols('a b gamma M',real=True)
e,pt,px,st,sx=s.symbols('e pi_t pi_x sigma_t sigma_x',real=True)
# Plane perturbations; other regular Hessians change A, L and the mixed term,
# but do not change the two coefficients at issue.
X=(mu+e*pt)**2-e**2*px**2
B=(q+e*sx)**2-e**2*st**2
C=-(mu+e*pt)*e*st+e*px*(q+e*sx)
P=a*(X-mu**2)+b*(B-q**2)+gamma*C**2
P2=s.expand(P).coeff(e,2)
K=-b+(-1 if args.mutate else 1)*gamma*mu**2
S=-a+gamma*q**2
h=2*(mu**2*a-q**2*b)
checks=[]
def ck(name,expr):
 r=s.factor(s.simplify(expr));checks.append({'name':name,'residual':str(r),'passed':r==0})
ck('solid_kinetic_from_action',P2.coeff(st,2)-K)
ck('clock_gradient_from_action',P2.coeff(px,2)-S)
ck('portal_mixed_derivative',P2.coeff(st,1).coeff(px,1)+2*gamma*mu*q)
ck('enthalpy_identity',q**2*K-mu**2*S-h/2)
ck('vacuum_opposite_energy_sign',K.subs(a,q**2*b/mu**2)-mu**2*S.subs(a,q**2*b/mu**2)/q**2)
z,k=s.symbols('omega2 k',real=True)
# The mixed entry squares to M^2 omega^2 k^2.
poly=s.expand((A*z+S*k**2)*(K*z-L*k**2)-M**2*z*k**2)
ck('frequency_root_product',poly.subs(z,0)/poly.coeff(z,2)+S*L*k**4/(A*K))
H,tau=s.symbols('enthalpy tau',positive=True)
near={mu:1,q:1,a:b+H/2,gamma:b+tau*H/2}
ck('near_vacuum_inertia',K.subs(near,simultaneous=True)-tau*H/2)
ck('near_vacuum_stiffness',S.subs(near,simultaneous=True)+(1-tau)*H/2)
# Covariant volume Jacobian has T_mu_nu=(U-J U')g_mu_nu.
J,J0,alpha,C0,E=s.symbols('J J0 alpha integration_constant epsilon',real=True)
U=-E+alpha*(J-J0)**2/2
energy=J*s.diff(U,J)-U
branch=J0+C0/alpha
ck('volume_branch_field_equation',s.diff(U,J).subs(J,branch)-C0)
ck('volume_branch_energy',energy.subs(J,branch)-(E+J0*C0+C0**2/(2*alpha)))
ck('volume_branch_memory',s.diff(energy.subs(J,branch),C0)-branch)
# Isolated clock with positive inertia and high-k stabilizing term.
Sp=s.symbols('S_positive',positive=True)
w2=(-Sp*k**2+(-1 if args.mutate else 1)*D*k**4)/A
ck('high_k_stabilization',s.expand(w2).coeff(k,4)-D/A)
ck('band_boundary',w2.subs(k**2,Sp/D))
ck('fastest_growth',w2.subs(k**2,Sp/(2*D))+Sp**2/(4*A*D))
ck('fastest_stationarity',s.diff(w2,k).subs(k,s.sqrt(Sp/(2*D))))
result={'mutated':args.mutate,'checks':checks,'passed':sum(c['passed'] for c in checks),'total':len(checks),'scope':'regular isotropic first-derivative decoupling limit; separate volume-form and unmixed higher-derivative examples; not a UV or MOND completion'}
Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
