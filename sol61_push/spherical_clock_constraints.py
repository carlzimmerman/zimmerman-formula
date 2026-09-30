"""Necessary stationary spherical equations for the local kappa=0 action."""
import argparse
import json
import sympy as s

r=s.symbols('r',positive=True)
M2,Z,K,A,B,ell=s.symbols('M2 Z K A B ell',positive=True)
N=s.Function('N')(r); sig=s.Function('sig')(r)
V=s.Function('V')(r); q=s.Function('q')(r); P=s.Function('P')(r)
Np=s.diff(N,r); sp=s.diff(sig,r); qp=s.diff(q,r)
lam=1+ell*q
U=A/q**2+B*q**2
F=s.diff(V,r)+V*sp; W=V/r; T=F+2*W
Qkin=F*F+2*W*W-lam*T*T
R3=2*(1-s.exp(-2*sig))/r**2+4*s.exp(-2*sig)*sp/r
Lraw=M2*r*r*s.exp(sig)*Qkin/(2*N)+M2*r*r*N*s.exp(sig)*R3/2+2*M2*r*r*P*Np-r*r*N*s.exp(sig)*(M2*P*P+K*q*P**3+U)+Z*r*r*s.exp(sig)*V*V*qp*qp/(2*N)-Z*r*r*N*s.exp(-sig)*qp*qp/2
L=M2*r*r*s.exp(sig)*Qkin/(2*N)+M2*N*(s.exp(sig)+s.exp(-sig))+2*M2*r*Np*s.exp(-sig)+2*M2*r*r*P*Np-r*r*N*s.exp(sig)*(M2*P*P+K*q*P**3+U)+Z*r*r*s.exp(sig)*V*V*qp*qp/(2*N)-Z*r*r*N*s.exp(-sig)*qp*qp/2
checks=[]
def check(name,ok): checks.append({'name':name,'passed':bool(ok)})
def zero(expr): return s.simplify(expr)==0
check('intrinsic curvature boundary integration',zero(Lraw-L+s.diff(2*M2*r*N*s.exp(-sig),r)))
def EL(field): return s.diff(L,field)-s.diff(s.diff(L,s.diff(field,r)),r)
EN=EL(N)/(r*r*s.exp(sig))
EV=EL(V)/(M2*r*r*s.exp(sig)/N)
ES=EL(sig)/(r*r*N*s.exp(sig))
EQ=EL(q)/(r*r*N*s.exp(sig))
EP=EL(P)/(r*r*N*s.exp(sig))
J=F-lam*T
momentum=s.diff(J,r)+(2/r-Np/N)*J-2*(W-lam*T)/r-Z/M2*V*qp*qp
check('shift momentum equation',zero(EV+momentum))
lapse=-M2*Qkin/(2*N*N)+M2*R3/2-2*M2*s.exp(-sig)*(s.diff(P,r)+2*P/r)-M2*P*P-K*q*P**3-U-Z*(s.exp(-2*sig)+V*V/(N*N))*qp*qp/2
check('lapse equation',zero(EN-lapse))
scalar=Z*s.diff(r*r*N*s.exp(-sig)*(1-s.exp(2*sig)*V*V/(N*N))*qp,r)/(r*r*N*s.exp(sig))-s.diff(U,q)-K*P**3-M2*ell*T*T/(2*N*N)
check('scalar advection and curvature equation',zero(EQ-scalar))
aux=2*M2*(s.exp(-sig)*Np/N-P)-3*K*q*P*P
check('polarization acceleration equation',zero(EP-aux))
combined=ES-V*EL(V)/(r*r*N*s.exp(sig))
combined_expected=-M2*Qkin/(2*N*N)+M2*(1-s.exp(-2*sig))/r**2-2*M2*s.exp(-2*sig)*Np/(N*r)-M2*P*P-K*q*P**3-U+Z*(s.exp(-2*sig)-V*V/(N*N))*qp*qp/2
check('radial metric-minus-shift equation',zero(combined-combined_expected))
identity=sp+Np/N-r*s.exp(sig)*(s.diff(P,r)+2*P/r)-Z*r*qp*qp/(2*M2)
check('exact gradient stress constraint',zero(EN-combined-2*M2*s.exp(-2*sig)*identity/r))

H,qc,m,Cshift=s.symbols('H qc m Cshift',positive=True)
Avac=s.Rational(3,2)*M2*H*H*qc*qc*(1+s.Rational(9,4)*ell*qc)
Bvac=s.Rational(3,2)*M2*H*H/(qc*qc)*(1+s.Rational(3,4)*ell*qc)
def metric_sub(expr,v,lambda_zero=False):
    out=expr.subs({N:1,sig:0,q:qc,P:0,V:v}).doit()
    out=out.subs({A:Avac,B:Bvac})
    if lambda_zero: out=out.subs(ell,0)
    return s.simplify(out)
for name,eq in [('lapse',EN),('shift',EV),('radial metric',ES),('scalar',EQ),('polarization',EP)]:
    check('de Sitter benchmark '+name,metric_sub(eq,-H*r)==0)
for name,eq in [('lapse',EN),('shift',EV),('radial metric',ES),('scalar',EQ)]:
    check('GR mass benchmark '+name,metric_sub(eq,-s.sqrt(H*H*r*r+2*m/r),True)==0)
flat_shift=metric_sub(momentum,V).subs({V:s.Function('v')(r)}).doit()
v=s.Function('v')(r)
check('flat-lapse constant-scalar shift equation',zero(flat_shift+ell*qc*(s.diff(v,r,2)+2*s.diff(v,r)/r-2*v/r**2)))
vtrial=-H*r+Cshift/r**2
check('decaying shift solves momentum',metric_sub(momentum,vtrial)==0)
check('decaying shift removed by lapse',zero(metric_sub(EN,vtrial)+3*M2*Cshift**2/r**6))
gp_res=metric_sub(momentum,-s.sqrt(H*H*r*r+2*m/r))
check('GR freefall mass fails variable-coupling momentum',gp_res!=0)

eps=s.symbols('eps',real=True)
phi=s.Function('phi')(r); psi=s.Function('psi')(r)
w=s.Function('w')(r); u=s.Function('u')(r)
weak=momentum.subs({N:1+eps*phi,sig:eps*psi,V:-H*r+eps*w,q:qc+eps*u}).doit()
linear=s.simplify(s.diff(weak,eps).subs(eps,0))
deltaK=-s.diff(w,r)-2*w/r+H*r*s.diff(psi,r)-3*H*phi
linear_expected=ell*qc*s.diff(deltaK,r)-2*H*s.diff(phi+psi,r)+3*H*ell*s.diff(u,r)
check('weak clock-metric boundary relation',zero(linear-linear_expected))
static_mass=(s.diff(U,q,2)-9*M2*H*H*ell/qc).subs(q,qc)
check('feedback mass equals vacuum mode mass floor',zero((static_mass-(2*A/qc**4+6*B)).subs({A:Avac,B:Bvac})))
# Necessary stationary-shell matter couplings; support stresses are not
# supplied by this prescribed particle distribution.
mu=s.Function('mu')(r)
Fmetric=N*N-s.exp(2*sig)*V*V
Lm=-mu*s.sqrt(Fmetric)
check('stationary shell lapse coupling',zero(s.diff(Lm,N)+mu*N/s.sqrt(Fmetric)))
check('stationary shell momentum coupling',zero(s.diff(Lm,V)-mu*s.exp(2*sig)*V/s.sqrt(Fmetric)))
check('stationary shell radial-minus-shift cancellation',zero(s.diff(Lm,sig)-V*s.diff(Lm,V)))
source_shift=s.diff(Lm,V)/(M2*r*r*s.exp(sig)/N)
check('cosmic-flow stationary source current',zero(source_shift.subs({N:1,sig:0,V:-H*r}).doit()+mu*H/(M2*r*s.sqrt(1-H*H*r*r))))
source_identity=identity-mu*N*s.exp(sig)/(2*M2*r*s.sqrt(Fmetric))
check('sourced exact gradient identity',zero(EN+s.diff(Lm,N)/(r*r*s.exp(sig))-combined-2*M2*s.exp(-2*sig)*source_identity/r))
# Measured circular-orbit scale differs from preferred-normal acceleration.
gorbit=s.diff(Fmetric,r)/(2*Fmetric)
check('orbit acceleration metric dictionary',zero(gorbit-(N*Np-s.exp(2*sig)*(V*s.diff(V,r)+sp*V*V))/Fmetric))
gp=gorbit.subs({N:1,sig:0,V:-s.sqrt(H*H*r*r+2*m/r)}).doit()
check('GR mass orbit acceleration despite zero clock acceleration',zero(gp-(m/r**2-H*H*r)/(1-H*H*r*r-2*m/r)))
check('static zero-shift orbit and clock dictionary',zero(gorbit.subs({V:0,sig:0}).doit()-Np/N))
result={'passed':all(c['passed'] for c in checks),'checks':checks,'freefall_mass_momentum_residual':str(gp_res),'exact_gradient_identity':str(identity),'weak_boundary_relation':str(linear_expected)}
parser=argparse.ArgumentParser()
parser.add_argument('--output',required=True)
args=parser.parse_args()
with open(args.output,'w') as f: json.dump(result,f,indent=2)
print(str(sum(c['passed'] for c in checks))+'/'+str(len(checks))+' checks passed')
for c in checks:
    if not c['passed']: print(c)
print('freefall-mass momentum residual:',gp_res)
raise SystemExit(0 if result['passed'] else 1)
