"""Compatibility gates for a known sequestering equation and the a0 ansatz.

Exact algebra only; no new gravity completion, flux solution or cosmology.
"""
import json
import sys
from pathlib import Path
import sympy as s

out=Path(sys.argv[1]);assert out.is_dir();checks=[]
def check(name,b):
    checks.append(dict(name=name,passed=bool(b)));assert b,name
T=s.symbols('T0:4');average,C=s.symbols('average C')
for j,t in enumerate(T):
    before=t-average/4;after=t+C-(average+4*C)/4
    check('constant-stress projector cancellation component'+str(j),s.simplify(before-after)==0)

B,G,kappa,gacc,x=s.symbols('B G kappa g x',positive=True)
a0=kappa*s.sqrt(G*B)
W=gacc**3/(12*s.pi*G*a0)
derivative=s.diff(W,B)
check('force-energy vacuum-parameter derivative',s.simplify(derivative+W/(2*B))==0)
ratio=s.simplify((W/B).subs(gacc,x*a0))
check('dimensionless force-vacuum feedback',s.simplify(ratio-kappa*kappa*x**3/(12*s.pi))==0)
check('bare-parameter acceleration changes under additive shift',s.diff(a0*a0,B)==kappa*kappa*G)
rows=[]
for value in (s.Rational(1,100),s.Rational(1,10),s.Integer(1)):
    correction=s.simplify((W/(2*B)).subs({gacc:value*a0,kappa:s.Rational(1,2)}))
    rows.append(dict(g_over_a0=float(value),magnitude_of_extra_constraint_term=float(correction),
        scope='deep regime comparison' if value<1 else 'formal edge comparison, not deep-limit prediction'))
result=dict(rows=rows,checks=checks,
    conventions='Source gravity convention: P[T]=T-<trT>delta/4; spacetime average normalized so <constant>=constant. Toy deep-force energy W=g^3/(12pi G a0), a0=kappa sqrt(G B), natural units.',
    non_claims=['No source action or flux/history solution reproduced by the finite algebra','No proof that adding a B-dependent matter force leaves sequestering intact','Known mechanism only cancels matter vacuum constants under its hypotheses; not scalar tadpoles or masses','No prediction of positive residual vacuum magnitude, kappa, physical a0, galaxy response or novelty'])
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
