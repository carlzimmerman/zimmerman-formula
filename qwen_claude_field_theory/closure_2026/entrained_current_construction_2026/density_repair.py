#!/usr/bin/env python3
"""Construct a density-curvature entrainment family and attack its finite domain.

F=-n1-n2+f R, f=D^p exp[-b (n1-n2)^2/D^2]-1/(2D), D=(n1+n2)/2.
The chosen representative p=b=1/2 is NOT a derived fundamental coefficient.
The exponential here regulates current-density contrast, not the MOND kernel.
"""
import argparse
import json
from pathlib import Path

import numpy as np
import sympy as s

from current_action import (CURRENT, TIME, SPACE, master, hessian_at, principal,
                            bernstein_quadratic, dirac)


def repaired_master():
    _, n1, n2, relative = master()
    mean = (n1+n2)/2
    contrast = n1-n2
    f = s.sqrt(mean)*s.exp(-contrast**2/(2*mean**2))-1/(2*mean)
    return -n1-n2+f*relative, f


def leading_curvature():
    """Independently differentiate the low-velocity Lagrangian before specializing."""
    r, t = s.symbols("r t", positive=True)
    j, k, v = s.symbols("j k v", real=True)
    density = s.Symbol("n", positive=True)
    p, b = s.symbols("p b", real=True)
    mean = (r+t)/2
    f = mean**p*s.exp(-b*(r-t)**2/mean**2)-1/(r+t)
    # This is the Taylor expansion of the full Lorentz-invariant master
    # through O(spatial_current^2), not a phenomenological pressure law.
    relative2 = (t*j*j/r+r*k*k/t-2*j*k)/2
    low_l = -r-t+j*j/(2*r)+k*k/(2*t)+f*relative2
    temporal = s.hessian(low_l, (r, t)).subs({r: density, t: density,
                                            j: density*v, k: -density*v})/v**2
    temporal = temporal.applyfunc(s.simplify)
    common = s.factor(temporal[0, 0]+temporal[0, 1])
    contrast = s.factor(temporal[0, 0]-temporal[0, 1])
    spatial = s.hessian(low_l, (j, k)).subs({r: density, t: density,
                                           j: 0, k: 0}).applyfunc(s.simplify)
    return {"temporal_leading_matrix": str(temporal),
            "common_density_eigenvalue": str(common),
            "relative_density_eigenvalue": str(contrast),
            "coflow_spatial_eigenvalues": [str(s.factor(spatial[0, 0]+spatial[0, 1])),
                                           str(s.factor(spatial[0, 0]-spatial[0, 1]))]}


def stress_gate():
    """Derive stress from the invariant master function, then take counterflow.

    This is the next redistribution gate: stable waves alone do not imply the
    positive isotropic pressure produced by stochastic recoil.
    """
    n, m, cross, density = s.symbols("n m s d", positive=True)
    p, b, v, radius, slope = s.symbols("p b v radius slope", real=True)
    mean = (n+m)/2
    f = mean**p*s.exp(-b*(n-m)**2/mean**2)-1/(n+m)
    relative = cross-n*m
    F = -n-m+f*relative
    fn, fm, fs = [s.diff(F, q) for q in (n, m, cross)]
    pressure = F-n*fn-m*fm-2*cross*fs
    # This follows by differentiating f; no fitted stress is entered.
    psi_identity = s.simplify(pressure+(1+p)*mean**p*s.exp(-b*(n-m)**2/mean**2)*relative)
    assert psi_identity == 0
    gamma2 = 1/(1-v*v)
    sub = {n: density, m: density, cross: density*density*(1+v*v)*gamma2}
    pressure = s.simplify(pressure.subs(sub))
    coefficient = s.simplify((-fn/n).subs(sub))
    f_here = s.simplify(fs.subs(sub))
    rho = s.factor(-pressure+2*(coefficient-f_here)*density**2*gamma2)
    parallel = s.factor(pressure+2*(coefficient+f_here)*density**2*gamma2*v*v)
    perpendicular = pressure
    limits = {"density_correction": s.simplify(s.limit((rho-2*density)/v**2, v, 0)),
              "parallel_pressure": s.simplify(s.limit(parallel/v**2, v, 0)),
              "perpendicular_pressure": s.simplify(s.limit(perpendicular/v**2, v, 0)),
              "pressure_trace": s.simplify(s.limit((parallel+2*perpendicular)/v**2, v, 0))}
    # For an equal counterflow pair oriented radially, assume n ∝ r^-slope,
    # v constant locally; ∇·P radial = dPrr/dr +2(Prr-Ptt)/r.
    pr, pt = limits["parallel_pressure"], limits["perpendicular_pressure"]
    force_coefficient = s.factor((p+2)*slope*pr-2*(pr-pt))
    return {"generalized_pressure": str(pressure), "rho": str(rho),
            "parallel_pressure": str(parallel), "perpendicular_pressure": str(perpendicular),
            "leading_coefficients_divided_by_v_squared": {k: str(x) for k, x in limits.items()},
            "radial_force_coefficient_times_radius_over_v_squared": str(force_coefficient),
            "radial_force_at_p_half_slope_two": str(s.simplify(force_coefficient.subs({p: s.Rational(1, 2), slope: 2}))),
            "scope": "Hilbert stress and local leading-order radial stress divergence; not a self-consistent halo solution or an entropy-producing kick law"}


def all_angle_certificate(h):
    inverse, polynomial, (u, t), _ = principal(h)
    A, B, C = (polynomial.coeff(u, power) for power in (2, 1, 0))
    certificates = {
        "constant": bernstein_quadratic(C, t),
        "discriminant": bernstein_quadratic(B*B-4*A*C, t),
        "null_value": bernstein_quadratic(A+B+C, t)}
    positive_coefficients = all(x > 0 for values in certificates.values() for x in values)
    linear_signs = all(B.subs(t, x) < 0 and (2*A+B).subs(t, x) > 0 for x in (0, 1))
    return {"polynomial": str(polynomial),
            "bernstein": {k: list(map(str, v)) for k, v in certificates.items()},
            "all_angle_squared_speeds_between_zero_and_one": bool(positive_coefficients and linear_signs and A > 0),
            "time_hessian_eigenvalues": {str(a): b for a, b in h.extract(TIME, TIME).eigenvals().items()},
            "space_hessian_eigenvalues": {str(a): b for a, b in h.extract(SPACE, SPACE).eigenvals().items()},
            "positive_energy": bool(all(x < 0 for x in h.extract(TIME, TIME).eigenvals())
                                    and all(x > 0 for x in h.extract(SPACE, SPACE).eigenvals()))}


def finite_domain(lagrangian):
    """Bounded float diagnostics away from the exact equal-density witnesses.

    Positive energy is tested by current Hessian blocks. Null-symbol tests in
    9 directions are supplementary necessary causal diagnostics, not proofs.
    """
    hessian_function = s.lambdify(CURRENT, s.hessian(lagrangian, CURRENT), "numpy", cse=True)
    rows = []
    for mean in (0.01, 0.1, 1.0, 10.0, 100.0):
        for ratio in (0.5, 0.8, 1.0, 1.25, 2.0):
            n1 = 2*mean*ratio/(1+ratio)
            n2 = 2*mean/(1+ratio)
            for v in (0.001, 0.01, 0.1, 0.3, 0.6):
                gamma = 1/np.sqrt(1-v*v)
                args = [n1*gamma, n1*gamma*v, 0, 0, n2*gamma, -n2*gamma*v, 0, 0]
                h = np.asarray(hessian_function(*args), dtype=float)
                ht = np.linalg.eigvalsh(h[np.ix_(TIME, TIME)])
                hs = np.linalg.eigvalsh(h[np.ix_(SPACE, SPACE)])
                # Scale the dust-like temporal block by v^2; use relative margins.
                temporal_margin = float(-max(ht)/(v*v))
                spatial_margin = float(min(hs))
                positive = temporal_margin > 1e-7 and spatial_margin > 1e-7
                null_margin = None
                if positive:
                    inverse = np.linalg.inv(h)
                    null_eigenvalues = []
                    for z in np.linspace(-1, 1, 9):
                        proj = np.zeros((2, 8))
                        proj[0, :4] = [-1, z, np.sqrt(1-z*z), 0]
                        proj[1, 4:] = proj[0, :4]
                        null_eigenvalues.append(float(max(np.linalg.eigvalsh(proj@inverse@proj.T))))
                    null_margin = -max(null_eigenvalues)
                rows.append({"mean_density": mean, "ratio_n1_n2": ratio, "v": v,
                             "temporal_margin_scaled": temporal_margin,
                             "spatial_margin": spatial_margin,
                             "positive_energy": bool(positive),
                             "sampled_null_margin": null_margin,
                             "condition_number": float(np.linalg.cond(h))})
    return rows


def calculate():
    lagrangian, f = repaired_master()
    low = leading_curvature()
    n, p, b = s.symbols("n p b", positive=True)
    # Compare derived expressions by names, using common symbolic assumptions.
    common = s.sympify(low["common_density_eigenvalue"], locals={"n": n, "p": p, "b": b})
    contrast = s.sympify(low["relative_density_eigenvalue"], locals={"n": n, "p": p, "b": b})
    assert s.simplify(common-p*(p-1)*n**p) == 0
    assert s.simplify(contrast-(2-8*b)*n**p) == 0
    exact = {}
    for v in (s.Rational(1, 1000), s.Rational(1, 10)):
        exact[str(v)] = all_angle_certificate(hessian_at(lagrangian, v))
        assert exact[str(v)]["positive_energy"]
        assert exact[str(v)]["all_angle_squared_speeds_between_zero_and_one"]
    finite = finite_domain(lagrangian)
    # The repair is not silently classified healthy over its whole state space.
    assert any(not row["positive_energy"] for row in finite)
    high_velocity = all_angle_certificate(hessian_at(lagrangian, s.Rational(3, 5)))
    return {"master": str(lagrangian), "entrainment": str(f),
            "general_family_leading_curvature": low,
            "stress_redistribution_gate": stress_gate(),
            "exact_equal_density_witnesses": exact,
            "dirac_repaired_k0": dirac(hessian_at(lagrangian, s.Rational(1, 10)), False),
            "dirac_repaired_k1": dirac(hessian_at(lagrangian, s.Rational(1, 10)), True),
            "high_velocity_test": high_velocity,
            "finite_domain": finite,
            "finite_positive_energy_count": sum(row["positive_energy"] for row in finite),
            "finite_positive_and_sampled_null_count": sum(row["positive_energy"] and row["sampled_null_margin"] > 0 for row in finite),
            "nonclaims": ["No full gravity closure, empirical prediction, CMB or PPN result",
                          "p=b=1/2 are representative choices, unrelated to fitted kappa=1/2",
                          "The reference density/energy units remain undetermined",
                          "Finite-angle scans outside exact witnesses are numerical screens only",
                          "No global nonlinear invariant health domain or caustic resolution",
                          "Exactly comoving density kinetics remain degenerate dust; no uniform strong-coupling bound",
                          "Two additional continuum matter scalar modes remain explicitly counted"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    result = calculate()
    args.result.parent.mkdir(parents=True, exist_ok=True)
    args.result.write_text(json.dumps(result, indent=2)+"\n")
    print("Leading density eigenvalues:", result["general_family_leading_curvature"])
    print("Exact positive-energy/all-angle witnesses:", list(result["exact_equal_density_witnesses"]))
    print("Finite-domain positive-energy count:", result["finite_positive_energy_count"], "/", len(result["finite_domain"]))
    print("Positive energy and sampled null cone:", result["finite_positive_and_sampled_null_count"])
    print("Full physical viability remains OPEN; inspect finite-domain and high-velocity failures.")
