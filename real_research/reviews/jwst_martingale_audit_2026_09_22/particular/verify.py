"""Exact counterexample to Qwen's claimed polynomial nonexistence."""
import json
from pathlib import Path
import sympy as S

s,z=S.symbols('s z',real=True)
k=S.symbols('k',positive=True)
a0,a1,a2,b0,b1,c=S.symbols('a0 a1 a2 b0 b1 c')
unknowns=(a0,a1,a2,b0,b1,c)
def K(g):
    p=S.Poly(S.expand(g),z)
    assert p.degree()<=2
    return p.nth(0)+p.nth(2)*(S.Rational(3,10)*s+z*z/10)
def L(g):
    return S.expand(2*z*S.diff(g,s)+S.diff(g,z)+k*(K(g)-g))
m=k*(1-s)/2-z
ansatz=a0+a1*s+a2*s*s+(b0+b1*s)*z+c*z*z
residual=S.Poly(L(ansatz)+2*m,s,z)
equations=residual.coeffs()+[ansatz.subs({s:1,z:0})]
solutions=S.solve(equations,unknowns,dict=True)
assert len(solutions)==1
P=S.expand(ansatz.subs(solutions[0]))
h=S.factor(P.subs(s,1)-z*z)
bad=(S.Rational(7,3)+k*k/8+3*k/8)+(-S.Rational(7,3)-k*k/2)*s+(3*k*k/8-3*k/8)*s*s+(-k+3*k*s/2)*z+S.Rational(10,3)*z*z
bad_residual=S.factor(L(bad)+2*m)
checks={
 'coefficient_system_solved':all(S.simplify(e.subs(solutions[0]))==0 for e in equations),
 'interior_main':S.simplify(L(P)+2*m)==0,
 'interior_positive_constant_shift':S.simplify(L(P+1)+2*m)==0,
 'interior_negative_spatial_shift_fails':S.simplify(L(P+s)+2*m)!=0,
 'negative_residual_exact':S.simplify(L(P+s)+2*m-2*z)==0,
 'boundary_gauge':P.subs({s:1,z:0})==0,
 'boundary_correction_retained':h!=0,
 'qwen_bad_coefficient_residual':S.simplify(bad_residual-S.Rational(3,2)*k*s*(1-z))==0,
 'qwen_physical_witness':bad_residual.subs({k:1,s:S.Rational(1,4),z:0})!=0,
}
out={'scope':'Polynomial interior solution refutes the stated nonexistence claim; boundary still requires correction',
 'coefficient_equations':{str(monomial):str(coeff) for monomial,coeff in residual.terms()},
 'solution':{str(key):str(value) for key,value in solutions[0].items()},
 'P':str(P),'h':str(h),'P_at_centre':str(P.subs({s:0,z:0})),
 'qwen_bad_residual':str(bad_residual),
 'checks':{key:bool(value) for key,value in checks.items()}}
Path('real_research/reviews/jwst_martingale_audit_2026_09_22/particular/certified/result.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
assert all(checks.values())
