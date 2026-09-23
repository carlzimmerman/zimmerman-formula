#!/usr/bin/env python3
"""Exact checks of three existing normalization routes; no data fitting.

Units c=1. This audits stated action sectors, not a completed covariant theory.
Run from repository root with --output PATH. All scientific checks are exact.
"""
import argparse
import json
from pathlib import Path
import sympy as sp

parser = argparse.ArgumentParser()
parser.add_argument("--output", required=True)
args = parser.parse_args()
checks = []
results = {}

def equal(name, actual, expected):
    residual = sp.simplify(actual - expected)
    checks.append({"name": name, "residual": str(residual), "pass": residual == 0})
    assert residual == 0, (name, residual)

# 1. L236's explicitly uncomputed U(tau) loophole, keeping lapse N(t).
# Future monotone clock: dot(tau)>0 and N>0. sqrt(X)=dot(tau)/N.
t = sp.symbols("t", real=True)
a, N, tau = [sp.Function(n)(t) for n in ("a", "N", "tau")]
U, V = sp.Function("U"), sp.Function("V")
Lclock = a**3 * U(tau) * sp.diff(tau, t) - N * a**3 * V(tau)
Eclock = sp.simplify(sp.diff(sp.diff(Lclock, sp.diff(tau, t)), t) - sp.diff(Lclock, tau))
expected_clock = 3*a**2*sp.diff(a, t)*U(tau) + N*a**3*sp.diff(V(tau), tau)
equal("variable_U_derivatives_cancel_in_clock_equation", Eclock, expected_clock)
rho_clock = sp.simplify(-sp.diff(Lclock, N)/a**3)
equal("clock_energy_is_potential_only", rho_clock, V(tau))
results["clock_equation_divided_by_N_a3"] = str(sp.simplify(Eclock/(N*a**3)))
results["clock_energy"] = str(rho_clock)

# 2. One AQUAL function: Newtonian normalization pins its overall coefficient,
# not the additive primitive constant. The lapse term is explicitly specified.
z, y, s, G, n, F0 = sp.symbols("z y s G n F0", positive=True)
aa, NN = sp.symbols("a N", positive=True)
F2 = z - 2*sp.log(1+sp.sqrt(z)) - 2/(1+sp.sqrt(z)) + 2 + F0
mu2 = 1-(1+sp.sqrt(z))**-2
equal("n2_primitive_has_exact_required_derivative", sp.diff(F2,z), mu2)
equal("n2_primitive_at_zero", sp.limit(F2,z,0,dir="+"), F0)
equal("n2_deep_slope", sp.limit((1-(1+y)**-2)/y,y,0),2)
equal("n2_newtonian_limit", sp.limit(mu2,z,sp.oo),1)
Lvac = -NN*aa**3*s**2*F0/(8*sp.pi*G)
rho_vac = sp.simplify(-sp.diff(Lvac,NN)/aa**3)
a0 = s/n
kappa_sq = sp.simplify(a0**2/(G*rho_vac))
equal("one_function_kappa_squared", kappa_sq, 8*sp.pi/(n**2*F0))
equal("L230_scale_identification_requires_F0_8pi", kappa_sq.subs(F0,8*sp.pi), 1/n**2)
equal("same_n2_force_different_vacuum_kappa_half", kappa_sq.subs({n:2,F0:8*sp.pi}),sp.Rational(1,4))
equal("same_n2_force_different_vacuum_kappa_one", kappa_sq.subs({n:2,F0:2*sp.pi}),1)
results["n2_primitive"] = str(F2)
results["vacuum_density_in_declared_lapse_completion"] = str(rho_vac)
results["kappa_squared"] = str(kappa_sq)

# 3. Test whether empty Newtonian vacuum fixes F0 without a new coefficient.
# F'(z)=mu_n(sqrt(z)); F(z)-z -> 0 implies F0=int_0^infinity (1-mu) dz.
R, ell = sp.symbols("R ell", positive=True)
I2 = 2*sp.log(1+R)+2/(1+R)-2
equal("n2_cutoff_integral_by_antiderivative", sp.diff(I2,R),2*R/(1+R)**2)
equal("n2_cutoff_integral_lower_limit",I2.subs(R,0),0)
assert sp.limit(I2,R,sp.oo) == sp.oo
checks.append({"name":"n2_empty_Newtonian_vacuum_diverges", "value":"+infinity", "pass":True})
finite2 = sp.limit(I2-2*sp.log(R/ell),R,sp.oo)
equal("n2_renormalized_finite_part",finite2,2*sp.log(ell)-2)
equal("finite_part_keeps_subtraction_scale",ell*sp.diff(finite2,ell),2)

# For all real n>2 the elementary antiderivative tends to zero at infinity.
# Establish the antiderivative identically, then use exponents 2-n<0,1-n<0.
primitive_n = 2*((1+y)**(2-n)/(2-n)-(1+y)**(1-n)/(1-n))
equal("general_residual_antiderivative",sp.diff(primitive_n,y),2*y*(1+y)**-n)
Fn0 = sp.simplify(-primitive_n.subs(y,0))
equal("n_gt_2_empty_vacuum_value",Fn0,2/((n-1)*(n-2)))
kap_empty_sq = sp.factor(kappa_sq.subs(F0,Fn0))
equal("n_gt_2_kappa_squared",kap_empty_sq,4*sp.pi*(n-1)*(n-2)/n**2)
equal("integer_n_ge_3_monotonicity",sp.diff(kap_empty_sq,n),4*sp.pi*(3*n-4)/n**3)
equal("integer_n_ge_3_minimum_at_3",kap_empty_sq.subs(n,3),8*sp.pi/9)
results["n2_cutoff_integral_R_in_y_units"] = str(I2)
results["n2_finite_part_with_subtraction_scale_ell"] = str(finite2)
results["n_gt_2_empty_Newtonian_F0"] = str(Fn0)
results["n_gt_2_empty_Newtonian_kappa_squared"] = str(kap_empty_sq)
results["integer_n_ge_3_minimum_kappa_squared"] = str(8*sp.pi/9)

# 4. Four-form normalization: independently reproduce its lapse variation.
f, q, Z, beta, b = sp.symbols("f q Z beta b",positive=True)
P = Z*q**2/2+b*beta**2*q**2
L4 = NN*aa**3*P.subs(q,f/(NN*aa**3))
rho4 = sp.simplify((-sp.diff(L4,NN)/aa**3).subs(f,q*NN*aa**3))
equal("four_form_legendre_energy_from_lapse",rho4,q*sp.diff(P,q)-P)
kap4_sq = sp.simplify(beta**2*q**2/rho4)
equal("four_form_remaining_ratio",kap4_sq,2/(Z/beta**2+2*b))
equal("four_form_half_condition",kap4_sq.subs(Z,(8-2*b)*beta**2),sp.Rational(1,4))
equal("four_form_flux_amplitude_cancels",sp.diff(kap4_sq,q),0)
results["four_form_kappa_squared"] = str(kap4_sq)

payload = {"status":"all_exact_checks_passed", "checks":checks, "results":results,
    "non_claims":["No complete covariant gravitational action is constructed.",
    "No proof that all possible normalization principles fail.",
    "The AQUAL vacuum result assumes the explicitly written standard lapse coupling.",
    "The empty Newtonian vacuum prescription is a tested extra boundary condition, not a derived physical law."]}
Path(args.output).write_text(json.dumps(payload,indent=2)+"\n")
print(json.dumps({"checks_passed":len(checks),"results":results},indent=2))
