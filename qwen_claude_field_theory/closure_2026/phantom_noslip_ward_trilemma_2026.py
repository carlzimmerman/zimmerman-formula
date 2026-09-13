#!/usr/bin/env python3
"""No-slip/Ward trilemma for an Einstein-curvature phantom source.

Scope: one physical metric, weak static linearized Einstein curvature on the
left-hand side, pressureless minimally coupled baryons, and an auxiliary
effective stress U_{mu nu} on the right.  Assume the auxiliary is separately
conserved and has no trace-free spatial stress (the condition needed to keep
Phi=Psi).  The calculation shows that these assumptions force its density to
vanish wherever the gravitational field is nonzero, while the MOND Poisson
rewrite requires a nonzero phantom density.
"""

from __future__ import annotations

import sympy as sp


def main() -> int:
    G, a0, b, x = sp.symbols("G a0 b x", positive=True)
    rho_aux, p_aux, grad_phi = sp.symbols("rho_aux p_aux grad_phi", real=True)
    # Linearized Einstein identities for the metric convention used in the
    # repository: G_00=2 Delta Psi and delta^{ij}G_ij=2 Delta(Phi-Psi).
    lap_slip = sp.symbols("lap_slip", real=True)
    trace_equation = sp.Eq(2 * lap_slip, 8 * sp.pi * G * 3 * p_aux)
    p_from_noslip = sp.solve(trace_equation.subs(lap_slip, 0), p_aux)[0]
    # Static separately-conserved isotropic auxiliary stress reduces at weak
    # field to dp + (rho+p) dPhi = 0.
    ward = sp.Eq(sp.Symbol("dp", real=True) + (rho_aux + p_aux) * grad_phi, 0)
    rho_from_noslip_ward = sp.solve(
        ward.subs({sp.Symbol("dp", real=True): 0, p_aux: p_from_noslip}), rho_aux
    )[0]
    # Exact exponential MOND rewrite in one spatial dimension, Phi'=b*x>0:
    # rho_aux = (4 pi G)^-1 d_x[(1-mu) Phi'].
    g = b * x
    mu = 1 - sp.exp(-g / a0)
    rho_phantom = sp.simplify(sp.diff((1 - mu) * g, x) / (4 * sp.pi * G))
    witness = sp.simplify(rho_phantom.subs({a0: 1, b: 1, x: 2}))
    # Spherical-vacuum strengthening.  If the Ward identity forces the
    # phantom density to vanish, its flux has an integration constant C:
    # r^2 (1-mu) g = C.  The baryonic MOND flux is r^2 mu g = G M, so
    # r^2 g = G M + C.  For a nonzero total flux this makes g vary as r^-2,
    # while mu(g/a0) is strictly varying because dmu/dg=exp(-g/a0)/a0>0.
    r, M, C = sp.symbols("r M C", positive=True)
    total_flux = G * M + C
    g_spherical = total_flux / r**2
    dmu_dg = sp.exp(-g_spherical / a0) / a0
    dg_dr = sp.simplify(sp.diff(g_spherical, r))
    dmu_dr = sp.simplify(dmu_dg * dg_dr)
    ratio_mu = sp.simplify((G * M) / total_flux)
    checks = {
        "no_slip_forces_zero_auxiliary_pressure": sp.simplify(p_from_noslip) == 0,
        "separate_ward_with_static_pressure_forces_zero_density": sp.simplify(
            rho_from_noslip_ward
        ) == 0,
        "exponential_mond_requires_nonzero_phantom_density": witness != 0,
        "spherical_flux_sum_forces_newtonian_r2_field": sp.simplify(
            r**2 * g_spherical - total_flux
        ) == 0,
        "exponential_mu_varies_on_nonzero_spherical_field": dmu_dr != 0,
        "mond_plus_phantom_flux_would_require_constant_mu": ratio_mu.free_symbols
        == {G, M, C},
    }
    for name, ok in checks.items():
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print("  linearized spatial trace equation:", trace_equation)
    print("  no-slip => p_aux =", p_from_noslip)
    print("  Ward identity dp+(rho_aux+p_aux) dPhi=0")
    print("  no-slip + static dp=0 + dPhi!=0 => rho_aux =", rho_from_noslip_ward)
    print("  required MOND phantom density =", rho_phantom)
    print("  explicit witness (a0=b=1,x=2) =", witness)
    print("  spherical flux sum r^2*g =", sp.factor(r**2 * g_spherical))
    print("  d mu(g(r)/a0)/dr =", dmu_dr)
    print("  MOND flux ratio mu = GM/(GM+C) =", ratio_mu)
    print()
    print("TRILEMMA:")
    print("  exact MOND needs rho_aux != 0; no-slip + no-TF stress forces p_aux=0;")
    print("  separate static Ward conservation then forces rho_aux=0 wherever grad Phi!=0.")
    print("  At least one of MOND, Phi=Psi, separate matter/auxiliary conservation, or")
    print("  ordinary Einstein curvature equations must therefore be abandoned.")
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
