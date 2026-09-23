import sympy as s,json,pathlib
root=pathlib.Path(__file__).resolve().parent
a,alpha,b,eps,t,k,H,Q=s.symbols('a alpha b eps t k H Q',real=True);v,u,psi,sig=s.symbols('v u psi sig',real=True); r=3*b+2
raw=a**3*(-3*r*(v+H*psi)**2-2*r*(v+H*psi)*sig-b*sig**2+alpha*(k/a)**2*psi**2+t/(2*eps)*(u-Q*psi)**2)
sigsol=-r*(v+H*psi)/b
shift=s.factor(raw.subs(sig,sigsol))
expected=a**3*(2*r/b*(v+H*psi)**2+t/(2*eps)*(u-Q*psi)**2+alpha*(k/a)**2*psi**2)
assert s.factor(shift-expected)==0
psisol=s.solve(s.diff(shift,psi),psi)[0]
red=s.factor(shift.subs(psi,psisol)); K=s.hessian(red,[v,u]).applyfunc(s.factor)
D=4*H**2*a**2*eps*r+a**2*b*t*Q**2+2*alpha*b*eps*k**2
want=s.Matrix([[4*a**3*r*(a**2*t*Q**2+2*alpha*eps*k**2)/D,4*H*a**5*t*Q*r/D],[4*H*a**5*t*Q*r/D,2*a**3*t*(2*H**2*a**2*r+alpha*b*k**2)/D]])
assert all(s.factor(x)==0 for x in K-want)
assert s.factor(K.det()-8*a**6*alpha*t*k**2*r/D)==0
print('PASS independent kinetic-block Schur complement equals every Lean matrix entry and determinant')
record=json.loads((root/'run_general/reduced.json').read_text()); M=s.sympify(record['mass'])
lookup={str(x):x for x in M.free_symbols}
subs={lookup['av']:a,lookup['clock_alpha']:alpha,lookup['clock_c2']:b,lookup['ep']:eps,lookup['j']:-t,lookup['k']:k,lookup['H']:H,lookup['q']:Q}
assert all(s.factor(x)==0 for x in -M.subs(subs)-K)
print('PASS saved general reduced kinetic matrix equals independent Schur result')
print('Scope: k>0, a>0, alpha>0, b>0, eps>0, t=-F1>0; homogeneous flat FRW; outside-kernel scalar healing; no gradient-stability assertion')
