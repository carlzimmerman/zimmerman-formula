"""Exact symbolic change of variables only; no galaxy simulation."""
import pathlib,json,sympy as s
x,t=s.symbols('x t',real=True);eta=s.symbols('eta',positive=True,real=True);A=s.Function('A')(x,t);S=s.Function('S',real=True)(x,t);Phi=s.Function('Phi',real=True)(x,t);psi=A*s.exp(s.I*S/eta)
original=s.exp(-s.I*S/eta)*(s.I*eta*s.diff(psi,t)+eta**2*s.diff(psi,x,2)/2-Phi*psi)
transformed=s.I*eta*s.diff(A,t)+eta**2*s.diff(A,x,2)/2+s.I*eta*(s.diff(S,x)*s.diff(A,x)+s.diff(S,x,2)*A/2)-(Phi+s.diff(S,t)+s.diff(S,x)**2/2)*A
res=s.simplify(original-transformed);assert res==0
p=pathlib.Path(__file__).resolve().parent;(p/'phase_identity_check.json').write_text(json.dumps(dict(SymPy=s.__version__,symbolic_residual=str(res),scope='one spatial dimension; independent Cartesian directions add; exact variable change, not a solved assembly mechanism'),indent=2)+'\n');print('exact residual',res)
