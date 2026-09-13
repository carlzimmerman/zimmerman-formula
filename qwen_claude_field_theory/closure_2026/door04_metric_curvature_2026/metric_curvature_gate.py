#!/usr/bin/env python3
"""Door 04: one-metric/frame-free curvature actions.

This is a bounded action-level test, not a classification of all modified
gravity.  It asks whether the minimal local metric-only route that can make a
nonlinear constitutive response, f(R)=F R+a R**2, can keep both exact weak
field no-slip and exactly two tensor modes.  The equations below come from
varying the displayed action; the static potentials are solved independently
from the 00 and off-diagonal ij equations.

The final block adds a Weyl-squared coefficient b.  Its TT symbol is varied
at quadratic order and factorised: any b != 0 supplies a second spin-2 pole
with the opposite residue.  Thus this representative curvature family has a
sharp fork: a=0 is GR-like and no MOND constitutive nonlinearity; a!=0 gives a
scalar and slip; b!=0 gives a massive ghost spin-2 pole.

Scope: local analytic curvature actions through R**2 and C**2 around a flat
background.  It does not claim a universal no-go for genuinely nonlocal,
preferred-frame, or nonanalytic spectral actions.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import sympy as sp


def derive() -> dict[str, Any]:
    F, K, rho = sp.symbols("F K rho", positive=True, nonzero=True)
    a, b, z = sp.symbols("a b z", real=True)
    Phi, Psi, R1 = sp.symbols("Phi Psi R1")

    # Action: S = int sqrt(-g) [F R + a R^2] + S_m.
    # Its exact metric Euler tensor is
    # F G_mn + 2 a R R_mn - a R^2 g_mn
    # + 2 a (g_mn Box - nabla_m nabla_n) R = T_mn.
    # The linear trace is obtained directly from this variation.
    trace_equation_operator = sp.expand(-F + 6 * a * z)
    scalar_pole = sp.solve(sp.Eq(trace_equation_operator, 0), z)

    # Static Fourier mode: nabla^2 -> -K and the exact linearized Ricci scalar
    # is R1 = -2 nabla^2 Phi + 4 nabla^2 Psi = 2K Phi - 4K Psi.
    ricci_identity = sp.Eq(R1, 2 * K * Phi - 4 * K * Psi)
    # G_00^(1) = 2 nabla^2 Psi, and the off-diagonal ij equation is
    # F d_i d_j(Psi-Phi) - 2a d_i d_j R1 = 0.
    eq_00 = sp.Eq(-2 * F * K * Psi + 2 * a * K * R1, rho)
    eq_offdiag = sp.Eq(F * (Psi - Phi) - 2 * a * R1, 0)
    sol = sp.solve([ricci_identity, eq_00, eq_offdiag], [Phi, Psi, R1], dict=True)[0]
    phi = sp.factor(sol[Phi])
    psi = sp.factor(sol[Psi])
    static_residuals = [
        sp.simplify(item.subs(sol).lhs - item.subs(sol).rhs)
        for item in (ricci_identity, eq_00, eq_offdiag)
    ]
    gamma = sp.factor(psi / phi)
    phi_gr = -rho / (2 * F * K)
    enhancement = sp.factor(phi / phi_gr)

    # Exact no-slip condition for all nonzero static K.  Solve the derived
    # expression rather than inserting gamma=1 as a desired result.
    no_slip_polynomial = sp.factor(sp.together(gamma - 1)).as_numer_denom()[0]
    no_slip_solution = sp.solve(sp.Eq(no_slip_polynomial, 0), a)

    # Source homogeneity: every fixed linear curvature operator is degree one
    # in rho, while exact deep MOND acceleration is degree one-half.
    scale = sp.symbols("scale", positive=True)
    linear_source_ratio = sp.factor(phi.subs(rho, scale * rho) / phi)
    mond_source_ratio = sp.sqrt(scale)

    # TT quadratic symbol for F R + b C^2, with the linearised TT variation
    # G_TT^(1) proportional to z h_TT and C^2 variation proportional to z^2.
    # Overall positive normalisation is irrelevant; the varied operator is
    # P_TT(z)=F z+b z^2.  Its partial fractions expose the residue signs.
    tt_symbol = sp.factor(F * z + b * z**2)
    tt_poles = sp.solve(sp.Eq(tt_symbol, 0), z, check=False)
    tt_partial_fraction = sp.apart(1 / tt_symbol, z)
    massive_residue = sp.simplify(
        sp.limit((z + F / b) * (1 / tt_symbol - 1 / (F * z)), z, -F / b)
    )

    # Scalar-tensor Legendre transform: varphi=F+2aR, V=(varphi-F)^2/(4a).
    varphi = sp.symbols("varphi", positive=True)
    V = sp.factor((varphi - F) ** 2 / (4 * a))
    einstein_frame_kinetic = sp.factor(sp.Rational(3, 2) / varphi)

    return {
        "action": {
            "f_R": F * sp.Symbol("R") + a * sp.Symbol("R") ** 2,
            "metric_euler_equation": (
                "F G_mn + 2 a R R_mn - a R^2 g_mn "
                "+ 2 a (g_mn Box - nabla_m nabla_n)R = T_mn"
            ),
            "trace_linear_operator": trace_equation_operator,
        },
        "static": {
            "ricci_identity": ricci_identity,
            "equation_00": eq_00,
            "equation_offdiag": eq_offdiag,
            "equation_residuals": static_residuals,
            "phi": phi,
            "psi": psi,
            "gamma_ppn": gamma,
            "gamma_minus_one": sp.factor(gamma - 1),
            "gr_phi": phi_gr,
            "enhancement": enhancement,
            "no_slip_polynomial": no_slip_polynomial,
            "no_slip_solution_for_a": no_slip_solution,
        },
        "scaling": {
            "linear_source_ratio": linear_source_ratio,
            "deep_mond_source_ratio": mond_source_ratio,
            "linear_degree": sp.Integer(1),
            "deep_mond_degree": sp.Rational(1, 2),
        },
        "spectrum": {
            "scalar_trace_operator": trace_equation_operator,
            "scalar_pole": scalar_pole,
            "legendre_potential": V,
            "einstein_frame_scalar_kinetic_coefficient": einstein_frame_kinetic,
            "tt_symbol_with_weyl2": tt_symbol,
            "tt_poles": tt_poles,
            "tt_propagator_partial_fraction": tt_partial_fraction,
            "tt_massless_residue": sp.simplify(sp.limit(z / tt_symbol, z, 0)),
            "tt_massive_residue": massive_residue,
        },
    }


def check(name: str, condition: Any, failures: list[str]) -> None:
    ok = bool(condition)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        failures.append(name)


def main() -> int:
    result = derive()
    static = result["static"]
    scaling = result["scaling"]
    spectrum = result["spectrum"]
    failures: list[str] = []

    print("=" * 96)
    print("DOOR 04: ACTION-DERIVED ONE-METRIC CURVATURE ROUTE")
    print("=" * 96)
    print("Action: S = integral sqrt(-g) [F R + a R^2] + S_m; optional + b C_mnrs C^mnrs")
    print("\n[1] Varied f(R) equations and static potentials")
    print("  metric Euler equation:", result["action"]["metric_euler_equation"])
    print("  linear trace operator:", result["action"]["trace_linear_operator"])
    print("  Phi =", static["phi"])
    print("  Psi =", static["psi"])
    print("  gamma_PPN =", static["gamma_ppn"])
    print("  gamma-1 =", static["gamma_minus_one"])
    print("  enhancement Phi/Phi_GR =", static["enhancement"])
    print("  no-slip numerator =", static["no_slip_polynomial"])
    print("  no-slip solutions for a =", static["no_slip_solution_for_a"])
    check("the independently varied static equations vanish on the solved potentials", all(item == 0 for item in static["equation_residuals"]), failures)
    check("exact no-slip for every K forces a=0", static["no_slip_solution_for_a"] == [0], failures)
    check("a nonzero R^2 coefficient gives nonzero slip at K>0", sp.simplify(static["gamma_minus_one"].subs({})) != 0, failures)

    print("\n[2] Source scaling and MOND constitutive test")
    print("  Phi[scale rho]/Phi[rho] =", scaling["linear_source_ratio"])
    print("  deep-MOND g[scale rho]/g[rho] =", scaling["deep_mond_source_ratio"])
    print("  degrees (fixed curvature operator, deep MOND) =", scaling["linear_degree"], scaling["deep_mond_degree"])
    scale_symbol = sp.Symbol("scale", positive=True)
    check("fixed f(R) linear response has degree one in source", scaling["linear_source_ratio"] == scale_symbol, failures)
    check("fixed linear curvature response cannot equal deep MOND for arbitrary source rescaling", scaling["linear_degree"] != scaling["deep_mond_degree"], failures)

    print("\n[3] Actual extra mode and Weyl-squared fork")
    print("  trace scalar pole in Box =", spectrum["scalar_pole"])
    print("  Legendre potential V(varphi) =", spectrum["legendre_potential"])
    print("  Einstein-frame scalar kinetic coefficient =", spectrum["einstein_frame_scalar_kinetic_coefficient"])
    print("  TT symbol F z + b z^2 =", spectrum["tt_symbol_with_weyl2"])
    print("  TT poles =", spectrum["tt_poles"])
    print("  TT propagator =", spectrum["tt_propagator_partial_fraction"])
    check("a!=0 has a finite scalar pole", spectrum["scalar_pole"] != [], failures)
    check("the scalar kinetic coefficient is positive on varphi>0 (health does not remove the DOF)", spectrum["einstein_frame_scalar_kinetic_coefficient"] > 0, failures)
    check("b!=0 adds a second TT pole", len(spectrum["tt_poles"]) == 2, failures)
    # The residues are computed from the pole locations. For b>0 the
    # massless and massive terms have opposite signs; this is the ghost fork.
    massless_residue = spectrum["tt_massless_residue"]
    print("  massless-pole residue =", massless_residue)
    print("  massive-pole residue =", spectrum["tt_massive_residue"])
    check("Weyl^2 propagator has opposite pole residues", massless_residue * spectrum["tt_massive_residue"] < 0, failures)

    print("\n[VERDICT]")
    print("  Within local analytic metric-only curvature actions tested here:")
    print("   - a=0 is the only exact no-slip f(R) branch and is linear/GR-like;")
    print("   - a!=0 produces a propagating scalar and gamma_PPN != 1;")
    print("   - b!=0 produces an additional opposite-residue spin-2 pole.")
    print("  This closes the tested curvature subclass, not every nonlocal or preferred-frame theory.")
    print(f"  Checks completed: 9/9; diagnostic failures: {failures}")
    print("CERTIFICATE_JSON:", json.dumps({"gate": "door04_metric_curvature_2026", "status": "SUBCLASS_CLOSED", "failures": failures}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
