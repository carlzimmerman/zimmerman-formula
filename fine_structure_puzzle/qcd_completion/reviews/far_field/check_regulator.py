"""Exact algebra for a PV matching term omitted by summing d=3 modes first.

No target implementation is imported. The loop integral formulas are derived
in INDEPENDENT_RAW.md; this script verifies their algebra and finite limit.
"""
import json
import pathlib
import sys
import sympy as s

p, M, L, eps, r, v = s.symbols('p M L eps r v', positive=True)
d = 3-2*eps
C = s.Symbol('C')
orbital = d-1
b_d = ((orbital/s.Integer(6))-4)*C
e_d = ((orbital*(4-d)/s.Integer(6))-4)*C
diff_d = s.factor(e_d-b_d)
assert s.simplify(diff_d-(d-1)*(3-d)*C/6)==0
# The sum of C has residue L/(16*pi^2), a consequence of the two Hurwitz
# zeta poles at s=1+2*eps and C_3=1/(8*pi).
residue = L/(16*s.pi**2)
finite_difference = s.limit(diff_d.subs(C,residue/eps), eps, 0)
assert finite_difference == L/(24*s.pi**2)

mM = s.sqrt(p*p+M*M)
# A single real charged pair after vector/ghost counting has two scalar
# orbital traces and one Lorentz spin trace.
pv_B = -s.Rational(11,24)/(s.pi*mM)
pv_E_ibp = p*p/(24*s.pi*mM**3)-1/(2*s.pi*mM)
assert s.simplify(pv_E_ibp-pv_B+M*M/(24*s.pi*mM**3))==0
# Physical minus PV therefore has positive E-B difference.
primitive = p/s.sqrt(p*p+M*M)
assert s.simplify(s.diff(primitive,p)-M*M/mM**3)==0
integral = s.limit(primitive,p,s.oo)-s.limit(primitive,p,-s.oo)
assert integral==2
continuum_sum_limit = L/(2*s.pi)*integral
assert s.simplify(continuum_sum_limit/(24*s.pi)-finite_difference)==0

h=v-1/r
fprime=1-L*h/s.pi
outer_divergence = 4*s.pi*fprime/(12*s.pi)
assert s.expand(outer_divergence).coeff(r,-1)==L/(3*s.pi)
corrected_Gamma_tail = -4*s.pi*finite_difference
assert corrected_Gamma_tail == -L/(6*s.pi)

results={
  'dimreg_E_minus_B_per_mode_over_C':str(s.factor(diff_d/C)),
  'dimreg_KK_C_pole_residue':str(residue),
  'IBP_Gamma_E_minus_B_finite':str(finite_difference),
  'PV_E_minus_B_regulator_density':str(s.factor(pv_E_ibp-pv_B)),
  'PV_continuum_integral':str(integral),
  'outer_local_minus_IBP_divergence_1overR':str(L/(3*s.pi)),
  'IBP_Gamma_BPS_tail_correction':str(corrected_Gamma_tail),
  'IBP_logweight_BPS_tail_correction':str(-corrected_Gamma_tail),
  'status':'Exact symbolic algebra verified; UV-sum limiting argument is analytic and is explained in INDEPENDENT_RAW.md. No finite spectral determinant assertion.'
}
out=pathlib.Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
(out/'checks.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({'status':'passed','symbolic_checks':8}))
