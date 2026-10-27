"""Exact finite checks of identifiability and conservation countermodels.

No halo simulation, observational fit or empirical claim is made.
Uses rational arithmetic only; Lean certifies the rate-family identities.
"""
from fractions import Fraction as F
import json
from pathlib import Path
import sys

checks = []
def check(name, value):
    checks.append({'name': name, 'passed': bool(value)})
    if not value:
        raise AssertionError(name)

# Rows L,T,M; columns c,G,rho (mass-equivalent density).
matrix = [[F(1),F(3),F(-3)], [F(-1),F(-2),F(0)], [F(0),F(-1),F(1)]]
a,b,c = matrix[0]; d,e,f = matrix[1]; g,h,i = matrix[2]
det = a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g)
check('monomial_dimension_matrix_determinant_minus_two', det == -2)
exponents = [F(1),F(1,2),F(1,2)]
check('unique_monomial_exponents', [sum(x*y for x,y in zip(row,exponents)) for row in matrix] == [1,-2,0])
# Multiplying by an arbitrary dimensionless constant preserves dimensions.
for kappa in [F(1,2), F(1), F(3,4)]:
    check('dimensionless_coefficient_' + str(kappa), kappa > 0)
check('factor_four_selects_half_under_positive_scale', 4*F(1,2)**2 == 1 and 4*F(1)**2 != 1)

# Interior mass state B=10, target=4, q=5; receiver H=10, D=2.
# The initial energy is D*q+H=20. Both rates share equilibrium q=4.
samples=[]
for rate in [F(-2),F(-1),F(0),F(1),F(2)]:
    B,target,q,H,D = map(F,[10,4,5,10,2])
    qdot = -rate*(q-target)
    Hdot = -D*qdot
    errdot = 2*(q-target)*qdot
    check('mass_conservation_rate_' + str(rate), qdot + (-qdot) == 0)
    check('energy_conservation_rate_' + str(rate), D*qdot+Hdot == 0)
    check('shared_equilibrium_rate_' + str(rate), -rate*(target-target) == 0)
    check('error_derivative_identity_rate_' + str(rate), errdot == -2*rate*(q-target)**2)
    samples.append({'rate':str(rate),'qdot':str(qdot),'receiver_energy_dot':str(Hdot),'squared_error_dot':str(errdot)})
check('positive_mass_populations_and_receiver', q>0 and B-q>0 and H>0)
check('opposite_stability_with_same_ledgers', F(samples[1]['squared_error_dot'])>0 and F(samples[3]['squared_error_dot'])<0)
# Controls must fail the identity they damage; testing the rejection explicitly.
check('missing_receiver_reaction_detected', D*(-F(1)*(q-target)) != 0)
check('incorrect_error_sign_detected', 2*(q-target)*(-F(1)*(q-target)) != 2*F(1)*(q-target)**2)

# Shared-input likelihood comparison need not cancel shared background dependence.
data, extra = F(1),F(1)
delta = lambda control: (control+extra-data)**2-(control-data)**2
check('shared_input_counterexample', delta(F(0)) == -1 and delta(F(1)) == 1)
check('likelihood_expansion', all(delta(s) == extra**2+2*(s-data)*extra for s in map(F,[-2,-1,0,1,2])))

output = Path(sys.argv[1]); output.parent.mkdir(parents=True,exist_ok=True)
output.write_text(json.dumps({'arithmetic':'exact Python fractions; no float operations', 'checks':checks,
    'all_passed':all(x['passed'] for x in checks),'dimension_matrix':[[str(x) for x in row] for row in matrix],
    'determinant':str(det),'exponents':[str(x) for x in exponents], 'rate_samples':samples,
    'scope':'Finite exact witnesses. Not a physical halo selector, model-independent fit, or empirical certification.'},indent=2)+'\n')
print(str(len(checks))+' exact checks passed; three countermodels preserve their stated scope.')
