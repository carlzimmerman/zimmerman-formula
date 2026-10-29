"""Exact algebra for the separately stated VR28 protection discriminators."""
import json
import sys
from pathlib import Path
import sympy as sp

s,C=sp.symbols('s C',real=True)
d,a,F,V,B,q,mu=sp.symbols('d a F V B q mu',positive=True)
U=a*sp.exp(3*s)+a/d*sp.exp(-3*d*s)
m2=sp.diff(U,s,2)/F**2
expected=81*a*a/F**4*(sp.exp(6*s)+2*d*sp.exp(3*(1-d)*s)+d*d*sp.exp(-6*d*s))
def L(f):
    f1=sp.diff(f,s)-3*f
    return sp.diff(f1,s)+3*d*f1
epsilon=sp.Function('epsilon')(q)
Veq=epsilon-q*sp.diff(epsilon,q)
loop=m2**2/(64*sp.pi**2)*(sp.log(m2/mu**2)-sp.Rational(3,2))
expressions={
 'one_loop_mass_fourth_expansion':m2*m2-expected,
 'classical_scaling_operator':L(U),
 'new_operator_nonzero_coefficient':L(sp.exp(6*s))/sp.exp(6*s)-9*(2+d),
 'subtraction_scale_local_response':mu*sp.diff(loop,mu)+m2*m2/(32*sp.pi**2),
 'vacuum_offset_ratio_derivative':sp.diff(B/(V+C),C)+B/(V+C)**2,
 'general_medium_response':-q*sp.diff(Veq,q)-q*q*sp.diff(epsilon,q,2),
 'constant_breaks_shape_relation':L(C)+9*d*C,
}
checks={k:bool(sp.simplify(v)==0) for k,v in expressions.items()}
checks['new_exponent_coefficient_strictly_positive']=bool((9*(2+d)).is_positive)
out={'claim_id':'VR28_PROTECTION','checks':checks,'domain':'Symbolic d,a,F,V,B,q,mu>0; s,C real; V+C>0 for physical offset comparison.','non_claims':['No quantization of the full PN28 stream action','No cancellation theorem for additional fields','No large-loop extrapolation','No derivation of a UV spectrum or beta function'],'software':{'Python':sys.version.split()[0],'SymPy':sp.__version__}}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(checks,indent=2))
assert all(checks.values()), checks
