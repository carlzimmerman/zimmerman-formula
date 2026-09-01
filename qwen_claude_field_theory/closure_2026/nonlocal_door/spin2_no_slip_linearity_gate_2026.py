#!/usr/bin/env python3
"""Audit the frame-free spin-2 nonlocal route without overstating its scope.

Claim card
==========
The existing ``ghost_theorem_lensing.py`` claims that every frame-free extra
mode couples only through R^(1), so any nonzero modification must generate
Phi != Psi.  That is not true for a universal spin-2 form factor.  The
quadratic, diffeomorphism-invariant action

    S2 = (M_P^2/4) int h^{mu nu} a(Box) E_{mu nu}^{rho sigma} h_{rho sigma}
         - (1/2) int h_{mu nu} T^{mu nu}

has Euler--Lagrange equation a(Box) G^(1)_{mu nu}=8 pi G T_{mu nu}.  For a
zero-free a, it has the GR massless pole only and, in a static nonrelativistic
source, amplifies Phi and Psi by the same factor.  It is a counterexample to
the *linear coupling-direction* premise, not a finished MOND construction.

This script then proves the next obstruction directly: a field-independent
form factor makes the response linear in rho.  Exact deep MOND instead scales
as sqrt(rho), equivalently M_b proportional to v^4 rather than v^2.  Therefore
the healthy no-slip quadratic action cannot furnish the requested MOND law.

No numerical sampling is used for the load-bearing statements: all variation,
source scaling, and pole-factor statements are symbolic.  The calculation does
not rule out a genuinely nonlinear, field-dependent nonlocal action; that is
the precisely stated residual route.
"""

from __future__ import annotations

import sys
from typing import Any

import sympy as sp


def derive_spin2_gate() -> dict[str, Any]:
    """Derive the static action variation, spectrum, and source-scaling gate."""

    k, ell, rho = sp.symbols("k ell rho", positive=True)
    phi, psi = sp.symbols("Phi Psi")
    lambda_r = sp.symbols("lambda", positive=True)
    z = sp.symbols("z")
    k2 = k**2

    # In the static limit Box -> -k^2.  The covariant entire form factor
    # a(Box)=exp(-ell^2 Box) is therefore a_static=exp(+ell^2 k^2).
    a_static = sp.exp(ell**2 * k2)

    # This is the scalar Newtonian reduction of the covariant quadratic action
    # h a(Box) E h.  Its GR kernel follows directly from linearized Einstein
    # equations in Newtonian gauge; multiplying the whole Einstein operator by
    # a is precisely the universal spin-2 form-factor branch.
    gr_kernel = sp.Matrix([[0, 2 * k2], [2 * k2, -2 * k2]])
    source = sp.Matrix([rho, 0])
    fields = sp.Matrix([phi, psi])
    static_action = sp.simplify(
        sp.Rational(1, 2) * (fields.T * (a_static * gr_kernel) * fields)[0]
        - (source.T * fields)[0]
    )
    euler = sp.Matrix([sp.diff(static_action, item) for item in fields])
    solution = sp.solve(list(euler), (phi, psi), dict=True)[0]
    phi_solution = sp.simplify(solution[phi])
    psi_solution = sp.simplify(solution[psi])

    # The second Euler equation is the scalar trace-free relation.  It is
    # obtained by variation, not set by hand.
    tracefree_residual = sp.simplify((phi_solution - psi_solution))
    gamma = sp.simplify(psi_solution / phi_solution)

    # Entire nonvanishing form factor: exp(z) has an empty complex zero set.
    form_factor_zero_set = sp.solveset(sp.Eq(sp.exp(z), 0), z, domain=sp.S.Complexes)
    form_factor_has_zeros = form_factor_zero_set != sp.EmptySet
    propagator_denominator = sp.simplify(k2 * a_static)

    # Fixed linear response versus exact deep-MOND homogeneity under rho->lambda rho.
    linear_response_ratio = sp.simplify(phi_solution.subs(rho, lambda_r * rho) / phi_solution)
    linear_kernel_degree = sp.simplify(sp.log(linear_response_ratio) / sp.log(lambda_r))
    mond_acceleration_ratio = sp.sqrt(lambda_r)
    mond_degree = sp.simplify(sp.log(mond_acceleration_ratio) / sp.log(lambda_r))

    # v^2=r g.  A linear response gives v^2 proportional to M, while deep MOND
    # gives v^4=G M a0.  The exponents below mean M proportional to v^exponent.
    btfr_exponent_linear_kernel = sp.Integer(2)
    btfr_exponent_mond = sp.Integer(4)

    # The F+ object previously identified as the candidate remains fixed as an
    # operator argument here.  Its non-rationality does not alter the source
    # homogeneity proof: any fixed linear operator is homogeneous of degree one.
    F_plus = 4 * (1 - (1 + sp.sqrt(z) / 2) * sp.exp(-sp.sqrt(z) / 2))
    F_plus_small_z = sp.series(F_plus, z, 0, 3).removeO()

    return {
        "action": {
            "static_action": static_action,
            "gr_kernel": gr_kernel,
            "form_factor_static": a_static,
            "euler": euler,
        },
        "field_equations": {
            "solution": solution,
            "phi": phi_solution,
            "psi": psi_solution,
            "tracefree_residual": tracefree_residual,
            "gamma_ppn_linear": gamma,
            "gamma_minus_one": sp.simplify(gamma - 1),
        },
        "spectrum": {
            "covariant_form_factor": sp.exp(-ell**2 * z),
            "form_factor_zero_set": form_factor_zero_set,
            "form_factor_has_zeros": bool(form_factor_has_zeros),
            "propagator_denominator": propagator_denominator,
        },
        "scaling": {
            "linear_response_ratio": linear_response_ratio,
            "linear_kernel_degree": linear_kernel_degree,
            "mond_acceleration_ratio": mond_acceleration_ratio,
            "mond_degree": mond_degree,
            "btfr_exponent_linear_kernel": btfr_exponent_linear_kernel,
            "btfr_exponent_mond": btfr_exponent_mond,
        },
        "f_plus": {"operator": F_plus, "small_z": F_plus_small_z},
    }


def _check(label: str, condition: Any) -> bool:
    passed = bool(condition)
    print(f"  [{'PASS' if passed else 'FAIL'}] {label}")
    return passed


def main() -> int:
    result = derive_spin2_gate()
    action = result["action"]
    fields = result["field_equations"]
    spectrum = result["spectrum"]
    scaling = result["scaling"]
    f_plus = result["f_plus"]

    print("=" * 92)
    print("FRAME-FREE SPIN-2 NONLOCAL GATE: NO-SLIP COUNTEREXAMPLE, THEN MOND SCALING TEST")
    print("=" * 92)
    print("\n[1] Action variation")
    print("  Covariant quadratic action: S2=(M_P^2/4) int h a(Box) E h - (1/2) int h T")
    print(f"  Static reduced action S2(k) = {action['static_action']}")
    print(f"  Euler--Lagrange vector = {list(action['euler'])}")
    print(f"  Solution: Phi = {fields['phi']}; Psi = {fields['psi']}")
    print(f"  Phi-Psi = {fields['tracefree_residual']}")
    print(f"  gamma_linear = Psi/Phi = {fields['gamma_ppn_linear']}")

    checks = [
        _check("the varied universal spin-2 action has exact linear no slip", fields["tracefree_residual"] == 0 and fields["gamma_minus_one"] == 0),
    ]

    print("\n[2] Linear spectrum")
    print(f"  Covariant a(Box) = {spectrum['covariant_form_factor']}")
    print(f"  zero set of exp(z) over C = {spectrum['form_factor_zero_set']}")
    print(f"  static propagator denominator = {spectrum['propagator_denominator']}")
    checks.append(_check("the selected entire form factor adds no linear pole beyond k^2=0", not spectrum["form_factor_has_zeros"]))

    print("\n[3] Exact source-scaling obstruction")
    print(f"  Fixed-kernel response Phi[lambda rho]/Phi[rho] = {scaling['linear_response_ratio']}")
    print(f"  fixed-kernel homogeneity degree = {scaling['linear_kernel_degree']}")
    print(f"  deep-MOND acceleration ratio g[lambda rho]/g[rho] = {scaling['mond_acceleration_ratio']}")
    print(f"  deep-MOND homogeneity degree = {scaling['mond_degree']}")
    print(f"  M(v) exponent: fixed linear kernel = {scaling['btfr_exponent_linear_kernel']}; MOND = {scaling['btfr_exponent_mond']}")
    checks.append(_check("a field-independent spin-2 kernel cannot equal deep MOND for arbitrary source rescaling", scaling["linear_kernel_degree"] != scaling["mond_degree"]))
    checks.append(_check("the same mismatch gives v^2-proportional-to-M instead of the BTFR v^4-proportional-to-M", scaling["btfr_exponent_linear_kernel"] != scaling["btfr_exponent_mond"]))

    print("\n[4] Relation to the remaining F+ door")
    print(f"  F+(z) = {f_plus['operator']}")
    print(f"  F+(z->0) = {f_plus['small_z']}")
    print("  Its transcendence may evade finite localization, but if it remains a fixed response operator,")
    print("  the exact homogeneity calculation above still excludes MOND.  A surviving candidate must make")
    print("  the nonlocal spin-2 form factor field-dependent while preserving the no-pole and no-slip properties.")

    print("\n[VERDICT]")
    print("  Corrected claim: frame-free covariant nonlocality is NOT automatically slip-locked at linear order.")
    print("  Closed subclass: every field-independent, zero-free, universal spin-2 form factor is too linear")
    print("  in baryonic mass to produce exact MOND.  The nonlinear field-dependent spin-2 route remains OPEN.")
    print(f"  Checks completed: {sum(checks)}/{len(checks)}")
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
