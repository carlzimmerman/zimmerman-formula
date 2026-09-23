"""Audit the polynomial transport generator, not a novelty claim."""
import json
from pathlib import Path
import sympy as S

s,z,k=S.symbols('s z k', real=True)
q=S.Rational
def angular(g):
    p=S.Poly(S.expand(g),z)
    assert p.degree()<=2
    return S.expand(p.nth(0)+p.nth(2)*(q(3,10)*s+q(1,10)*z*z))
def L(g):
    return S.expand(2*z*S.diff(g,s)+S.diff(g,z)+k*(angular(g)-g))
m=k*(1-s)/2-z
w_bad=s-2*z/k  # Qwen's C=2/k,F=-2/k,D=E=0, I=k*s/2
res=S.expand(L(w_bad)+2*m)
boundary=S.expand(w_bad.subs(s,1)-z*z)
checks={
 'constant_annihilated': L(S.Integer(1))==0,
 'radius_square_streaming': S.expand(L(s)-2*z)==0,
 'directional_projection': S.expand(L(z)-(1-k*z))==0,
 'directional_square': S.expand(L(z*z)-(2*z+k*(q(3,10)*s-q(9,10)*z*z)))==0,
 'mean_equation': S.expand(L(m)+1)==0,
 'mean_boundary': S.expand(m.subs(s,1)+z)==0,
 'vacuum_raw_second': S.expand((L(z*z)+2*m).subs(k,0))==0,
 'vacuum_boundary': S.expand((z*z).subs(s,1)-z*z)==0,
 'qwen_interior_counterexample': res.subs({k:1,s:q(1,4),z:0})!=0,
 'qwen_boundary_counterexample': boundary.subs({k:1,z:1})!=0,
}
out={'scope':'Exact generator calibration and refutation of Qwen 7376a647fa2c4a9dba52909aeb4d4068',
 'residual':str(res),'boundary_residual':str(boundary),
 'interior_witness':str(res.subs({k:1,s:q(1,4),z:0})),
 'boundary_witness':str(boundary.subs({k:1,z:1})),
 'checks':{key:bool(v) for key,v in checks.items()}}
Path('real_research/reviews/jwst_martingale_audit_2026_09_22/generator/certified/result.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
assert all(checks.values())
