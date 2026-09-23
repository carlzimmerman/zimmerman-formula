#!/usr/bin/env python3
"""Exact, independent PD normalization audit. Only writes its supplied result path.

Contract: the scalar static ansatz, rational OR response, its local variational
primitive, and a coefficient-level symmetry test. This is not a construction
of a covariant cosmology or a test against cosmological observations.
"""
import ast
import json
from pathlib import Path
import sys

import sympy as sp

ROOT = Path(__file__).resolve().parents[4]
Y, lam, d, LP, LS = sp.symbols("Y lambda d lap_Phi lap_Psi", positive=True)
checks = []


def equal(name, left, right):
    residual = sp.simplify(left - right)
    assert residual == 0, (name, residual)
    checks.append({"name": name, "residual": str(residual)})


# Reconstruct traces directly from h00=-2Phi, hij=-2Psi deltaij.
# Trace Rij = (d-2) lapPsi + d lapPsi - lapPhi.
R00 = LP
Rtrace = (2 * d - 2) * LS - LP
Rscalar = -R00 + Rtrace
G00 = R00 + Rscalar / 2
Gtrace = Rtrace - d * Rscalar / 2
equal("all-d 00 component", G00, (d - 1) * LS)
equal("all-d spatial trace", Gtrace, (d - 1) * (LP - (d - 2) * LS))
matrix = sp.Matrix([[d - 1, 0], [(d - 1) * (3 - d), d - 1]])
equal("scalar symbol determinant", matrix.det(), (d - 1)**2)
assert matrix.subs(d, 1).rank() == 0
assert all(matrix.subs(d, dim).rank() == 2 for dim in range(2, 7))

# Saturation does not select the channel-combination operation.
p_unit = Y / (1 + Y)
mean_response = (p_unit + p_unit) / 2
or_unit = 1 - (1 - p_unit)**2
equal("mean saturation", sp.limit(mean_response, Y, sp.oo), 1)
equal("OR saturation", sp.limit(or_unit, Y, sp.oo), 1)
equal("mean slope", sp.diff(mean_response, Y).subs(Y, 0), 1)
equal("OR slope", sp.diff(or_unit, Y).subs(Y, 0), 2)

# Even after granting OR and two identical channels, their common slope is free.
p = lam * Y / (1 + lam * Y)
mu = 1 - (1 - p)**2
equal("general OR response", mu, 1 - (1 + lam * Y)**-2)
equal("channel slope", sp.diff(p, Y).subs(Y, 0), lam)
equal("general OR slope", sp.diff(mu, Y).subs(Y, 0), 2 * lam)
equal("general OR saturation", sp.limit(mu, Y, sp.oo), 1)
kappa = 1 / (2 * lam)
assert [kappa.subs(lam, q) for q in [sp.Rational(1, 2), 1, 2]] == [1, sp.Rational(1, 2), sp.Rational(1, 4)]

# A variational completion with Newtonian normalization exists for every lam>0.
# I[Phi] = integral [-s^2/(8pi G) F(|gradPhi|^2/s^2) - rho_b Phi] d^3x.
# Its Euler equation is div(mu gradPhi)=4pi G rho_b if F_X=mu.
F_of_Y2 = Y**2 - 2 / lam**2 * (sp.log(1 + lam * Y) + 1 / (1 + lam * Y) - 1)
equal("action primitive F_X=mu", sp.diff(F_of_Y2, Y) / (2 * Y), mu)
equal("vacuum subtraction F(0)=0", F_of_Y2.subs(Y, 0), 0)
equal("action cubic coefficient", sp.limit(F_of_Y2 / Y**3, Y, 0, dir="+"), 4 * lam / 3)
equal("Newtonian action coefficient", sp.limit(F_of_Y2 / Y**2, Y, sp.oo), 1)
transverse = sp.factor(mu)
longitudinal = sp.factor(mu + Y * sp.diff(mu, Y))
equal("positive transverse eigenvalue", transverse,
      lam * Y * (lam * Y + 2) / (lam * Y + 1)**2)
equal("positive longitudinal eigenvalue", longitudinal,
      lam * Y * ((lam * Y)**2 + 3 * lam * Y + 4) / (lam * Y + 1)**3)
assert transverse.is_positive and longitudinal.is_positive

# Parity acts trivially on the two scalar potentials, so it cannot equate weights.
scalar_parity = sp.eye(2)
unequal_weights = sp.diag(1, 4)
assert scalar_parity.T * unequal_weights * scalar_parity == unequal_weights
# Even channel-exchange symmetry allows a free common normalization.
A, B = sp.symbols("A B", real=True)
exchange = sp.Matrix([[0, 1], [1, 0]])
K = sp.Matrix([[A, B], [B, A]])
assert exchange.T * K * exchange == K

# General-d counterexample to the stale PD02 header, at the first dimension d=2.
header_G00 = (d + 1) * LS / 2
header_Gtrace = (d - 1) * (LP - LS) + d * (2 - d) * LS / 2
header_residuals = {
    "G00_d2": str(sp.expand((G00 - header_G00).subs(d, 2))),
    "Gtrace_d2": str(sp.expand((Gtrace - header_Gtrace).subs(d, 2))),
}
assert all(sp.sympify(v) != 0 for v in header_residuals.values())

# PD03 is a reformulation of the normalization once s^2=G*u is fixed.
k, u, G, s, f, chi, eta = sp.symbols("kappa u G s f chi eta", positive=True)
equal("general energy matching residual", (eta * (k * s)**2 / G - f * chi * u).subs(s**2, G * u),
      u * (eta * k**2 - f * chi))
equal("quarter matching residual", ((k * s)**2 / G - u / 4).subs(s**2, G * u),
      u * (k**2 - sp.Rational(1, 4)))
equal("PD01 squared vs PD03 for generic count",
      sp.factor(1/d**2 - 1/(2*d)), (2 - d)/(2*d**2))

# No invocation of source scripts: their output-writing behavior stays untouched.
source_checks = {}
for filename in ["PD01_polarization_count.py", "PD02_polarization_count.py", "PD03_two_halves.py"]:
    tree = ast.parse((ROOT / "deepseek_push" / filename).read_text())
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)
             and isinstance(n.func, ast.Name) and n.func.id == "check"]
    literal_true = [n.lineno for n in calls if len(n.args) >= 3
                    and isinstance(n.args[2], ast.Constant) and n.args[2].value is True]
    source_checks[filename] = {"check_calls": len(calls), "literal_true_lines": literal_true}

result = {
    "status": "exact identities verified; normalization counterfamily constructed",
    "coefficient_domain": "real symbolic expressions; rational coefficients and exact log",
    "bounds": {"lambda": "every positive real", "Y": "nonnegative real (strict ellipticity only Y>0)",
               "dimension": "integer d>=2, scalar two-potential ansatz, nonzero Fourier frequency"},
    "checks": checks,
    "channel_matrix": str(matrix), "determinant": str(sp.factor(matrix.det())),
    "mu_lambda": str(sp.factor(mu)), "kappa_lambda": str(kappa),
    "F_lambda_Y_squared": str(F_of_Y2),
    "transverse_eigenvalue": str(transverse), "longitudinal_eigenvalue": str(longitudinal),
    "minimum_counterexample": {"lambda": 2, "channel_count": 2, "kappa": "1/4",
                               "mu_infinity": 1, "per_channel_slope": 2},
    "PD02_stale_header_residuals_at_d2": header_residuals,
    "source_checks": source_checks,
    "non_claims": ["No full relativistic carrier or cosmology is constructed.",
                   "No field stress tensor, vacuum energy split, or physical OR mechanism is established.",
                   "No observational parameter is fitted or imported; no LCDM assumption is used.",
                   "Strict ellipticity excludes the degenerate MOND origin g=0."]
}
output = Path(sys.argv[1])
output.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"status": result["status"], "exact_identity_checks": len(checks),
                  "kappa_lambda": str(kappa), "counterexample": result["minimum_counterexample"],
                  "source_checks": source_checks}, indent=2))
