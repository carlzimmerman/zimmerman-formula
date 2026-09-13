"""Homogeneous equations on the trace-degenerate ADM branch D=0.

This is a necessary-condition calculation, not a full perturbation or Dirac
analysis. It keeps K(Q) general and varies before imposing D=0.
"""
import json
import sympy as s
a,F,kappa,C,Q,H=s.symbols('a F kappa C Q H',positive=True,real=True)
K=s.Function('K')(Q);Kp=s.diff(K,Q);Kpp=s.diff(K,Q,2)
rho=s.simplify(6*F*kappa/a**2-C-K+Q*Kp)
p=s.simplify(C+K-2*F*kappa/a**2)
rho_plus_p=s.simplify(rho+p)
Qdot=s.simplify(-3*H*Kp/Kpp)
adot=H*a
drho=s.simplify(s.diff(rho,a)*adot+s.diff(rho,Q)*Qdot)
dp=s.simplify(s.diff(p,Q)*Qdot)
continuity=s.simplify(drho+3*H*rho_plus_p)
adiabatic=s.simplify(dp/drho)
assert s.simplify(rho_plus_p-(4*F*kappa/a**2+Q*Kp))==0
assert continuity==0
# For kappa=0 this reduces to K'/(Q K''); the curvature term changes the
# background density derivative and must not be silently dropped.
assert s.simplify(adiabatic.subs(kappa,0)-Kp/(Q*Kpp))==0
ell=s.symbols('ell',real=True)
affine_scalar=s.simplify(3*ell*a**2*adot)
assert affine_scalar==3*ell*a**3*H
witness={Q:1,H:1,F:1,kappa:0,a:1}
Ktest=Q-(Q-1)**2/s.Integer(2)
witness_values={K:Ktest,Kp:s.diff(Ktest,Q),Kpp:s.diff(Ktest,Q,2)}
witness_expr={**witness_values}
def witness_eval(expr):
    # Replace the function jet first, then evaluate the remaining symbols.
    return s.simplify(expr.xreplace(witness_expr).subs(witness))
assert witness_eval(rho_plus_p)==1
assert witness_eval(adiabatic)==-1
print(json.dumps(dict(full_theory='OPEN',scope=__doc__,
    rho=str(rho),pressure=str(p),rho_plus_p=str(rho_plus_p),
    clock_charge_equation='a^3 K_prime(Q)=constant',Qdot=str(Qdot),
    continuity_residual=str(continuity),adiabatic_slope=str(adiabatic),
    affine_scalar_equation=str(affine_scalar),
    witness={'QKprime':1,'Kpp':-1,'rho_plus_p':1,'dp_drho':-1},
    interpretation='On flat expanding solutions with Q*Kprime>0, Kpp<0 implies dp/drho<0. This is a necessary instability warning for the degenerate branch, not a universal no-go.'),indent=2))
