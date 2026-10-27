import sympy as s
import json
R, Q, T, H, w, t, A, e = s.symbols('R Q T H w t A e', real=True)
checks=[]
def ck(name, expr):
    assert s.simplify(expr)==0, name
    checks.append(name)
Euler=T-4*Q+R**2
Weyl=T-2*Q+R**2/3
ck('curvature decomposition', Euler-Weyl-(2*R**2/3-2*Q))
ck('Einstein curvature', (Euler-Weyl).subs(Q,R**2/4)-R**2/6)
ck('de Sitter normalization', (R**2/6).subs(R,12*H**2)-24*H**4)
ck('mass source cancellation', (24*H**4+w)-Weyl.subs(T,w+2*Q-R**2/3)-24*H**4)
ck('mismatch source', (24*H**4+w)-t*w-(24*H**4+(1-t)*w))
# Algebraic pieces of constant-coefficient curvature variations on Einstein metrics.
ck('R squared metric residual', 2*R*(R/4)-R**2/2)
ck('Ricci squared metric residual', 2*(R/4)**2-(R**2/4)/2)
beta=A/(16*s.pi**2)
ck('conditional anomaly ratio', 3/(4*beta*e)-12*s.pi**2/(A*e))
ck('target still needs normalization', (12*s.pi**2/(A*e)).subs(e,3*s.pi/(8*A))-32*s.pi)
print(json.dumps({'exact_checks':checks,'count':len(checks),'scope':'Curvature scalar algebra and conditional coupling identities; not tensor variation or perturbation proof'},indent=2))
