"""Derive the stress/slip obstruction of the normalized parent.

The lapse-neutral class has static density -sqrt(h) F(Y), Y=|D N|.
For h_ij=diag(exp(2*s_parallel),exp(2*s_perp),exp(2*s_perp)), isotropic
stress means the per-direction variations obey e_parallel=e_transverse/2.
Their difference is Y F'(Y).  Exact isotropic stress therefore imposes F'=0,
whereas exact exponential MOND requires F'=2Y(1-exp(-Y)) (up to one common
normalization).  The two demands are incompatible at every Y>0.

The second calculation expands the same covariant density to first order in
the spatial potential Psi while keeping the acceleration dependence nonlinear.
It produces the actual Psi equation and its nonzero source on Phi=Psi.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


def class_no_go():
    y = sp.symbols("y", positive=True)
    mu = 1 - sp.exp(-y)
    mup = sp.diff(mu, y)
    # Isotropy of the per-direction stress plus desired flux gives mu*y=0.
    incompatibility = sp.simplify(y * mu)
    return {
        "mu": str(mu),
        "mu_prime": str(mup),
        "isotropy_flux_consequence": str(incompatibility),
        "positive_for_y_positive": bool(incompatibility.subs(y, 1) > 0),
        "limit_y0": str(sp.limit(incompatibility, y, 0, dir="+")),
        "limit_yinf": str(sp.limit(incompatibility, y, sp.oo)),
        "not_identically_zero": bool(incompatibility != 0),
    }


def nonlinear_slip_source():
    """Vary a first-order-in-Psi static reduction of the covariant density."""

    x, a0, c2, rho = sp.symbols("x a0 c2 rho", positive=True)
    Phi = sp.Function("Phi")(x)
    Psi = sp.Function("Psi")(x)
    y = sp.diff(Phi, x) / a0
    ys = sp.symbols("ys", positive=True)
    Hs = 2 * (1 + ys) * sp.exp(-ys) - 2
    H = Hs.subs(ys, y)
    Hy = sp.diff(Hs, ys).subs(ys, y)
    # h_ij=(1-2 Psi/c2) delta_ij gives sqrt(h)=1-3 Psi/c2 and
    # Y=y*(1+Psi/c2), retained to first order in Psi/c2.
    L_aux = -2 * a0**2 * (H + (Psi / c2) * (y * Hy - 3 * H))
    L_eh = 2 * sp.diff(Psi, x) ** 2 - 4 * sp.diff(Phi, x) * sp.diff(Psi, x) + 2 * sp.diff(Phi, x) ** 2
    L = L_eh + L_aux - rho * Phi
    e_phi = sp.simplify(sp.diff(L, Phi) - sp.diff(sp.diff(L, sp.diff(Phi, x)), x))
    e_psi = sp.simplify(sp.diff(L, Psi) - sp.diff(sp.diff(L, sp.diff(Psi, x)), x))
    equal_sub = {Psi: Phi, sp.diff(Psi, x): sp.diff(Phi, x), sp.diff(Psi, x, 2): sp.diff(Phi, x, 2)}
    psi_on_equal = sp.factor(e_psi.subs(equal_sub))
    # A constant-gradient witness removes all Phi'' terms while keeping y finite.
    witness = sp.simplify(psi_on_equal.subs({sp.diff(Phi, x, 2): 0}))
    high_y_gradient = sp.simplify(sp.limit(ys * sp.diff(Hs, ys), ys, sp.oo))
    high_y_volume = sp.simplify(sp.limit(-3 * Hs, ys, sp.oo))
    return {
        "e_phi": str(e_phi),
        "e_psi": str(e_psi),
        "psi_equation_on_Phi_equals_Psi": str(psi_on_equal),
        "constant_gradient_slip_source": str(witness),
        "constant_gradient_source_at_y1": str(sp.simplify(witness.subs({sp.diff(Phi, x): a0}))),
        "high_acceleration_gradient_source": str(high_y_gradient),
        "high_acceleration_volume_offset": str(high_y_volume),
        "exact_slip_source_vanishes_identically": bool(sp.simplify(witness) == 0),
    }


def run():
    no_go = class_no_go()
    slip = nonlinear_slip_source()
    checks = {
        "scalar_norm_class_incompatible": no_go["not_identically_zero"],
        "exponential_positive_witness": no_go["positive_for_y_positive"],
        "independent_phi_psi_variations_derived": bool(slip["e_phi"] and slip["e_psi"]),
        "finite_y_slip_source_nonzero": not slip["exact_slip_source_vanishes_identically"],
        "high_acceleration_gradient_source_vanishes": slip["high_acceleration_gradient_source"] == "0",
    }
    result = {
        "candidate": "normalized_acceleration_parent_2026",
        "class_no_go": no_go,
        "nonlinear_slip": slip,
        "checks": checks,
        "status": "OPEN_WITH_SCOPED_NO_GO",
        "interpretation": "Changing only the scalar constitutive function cannot restore exact no-slip. A successful continuation needs an independent non-propagating tensor/topological compensator or must relax exact Phi=Psi.",
    }
    out = Path(__file__).parent / "run_001"
    out.mkdir(exist_ok=True)
    (out / "isotropic_stress_slip_results.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    assert all(checks.values())
    return result


if __name__ == "__main__":
    run()
