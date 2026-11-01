#!/usr/bin/env python3
"""Fixed-dark-mass static baryonic response; see CONTRACT_STATIC.md.

Scientific execution belongs to the root's bounded runner. No input is written.
"""
import importlib.util
import json
import math
import sys
import traceback
from pathlib import Path

import numpy as np
from scipy.integrate import quad, solve_bvp
from scipy.optimize import brentq


ROOT = Path(__file__).resolve().parent
FAMILIES = {"weak_diffuse": (0.05, 0.5), "strong_compact": (0.2, 0.1)}
FRACTIONS = (0.0, 0.25, 0.5, 0.75, 1.0)


def load_baseline():
    spec = importlib.util.spec_from_file_location("frozen_gradient", ROOT / "inputs/check_gradient.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def plummer(r, mb, a):
    r = np.asarray(r)
    d = r * r + a * a
    return -mb / np.sqrt(d), 3 * mb * a * a / d**2.5, mb * r**3 / d**1.5


def plummer_controls():
    """Unit-mass/unit-scale analytic checks, independent of the BVP."""
    rows = []
    for r in (0.1, 1.0, 3.0):
        h = 1e-4 * max(0.1, r)
        f = lambda x: float(plummer(x, 1.0, 1.0)[0])
        der = (f(r - 2*h) - 8*f(r - h) + 8*f(r + h) - f(r + 2*h)) / (12*h)
        der2 = (-f(r + 2*h) + 16*f(r + h) - 30*f(r) + 16*f(r - h) - f(r - 2*h)) / (12*h*h)
        _, source, mass = plummer(r, 1.0, 1.0)
        integrated = quad(lambda x: float(plummer(x, 1.0, 1.0)[1]) * x*x, 0, r,
                          epsabs=1e-12, epsrel=1e-12)[0]
        lap_error = abs((der2 + 2*der/r) / source - 1)
        mass_error = abs(integrated / mass - 1)
        rows.append({"r_over_a": r, "laplacian_relative_error": float(lap_error),
                     "mass_relative_error": float(mass_error),
                     "passed": bool(lap_error < 2e-6 and mass_error < 2e-6 and der > 0)})
    return {"cases": rows, "passed": all(row["passed"] for row in rows)}


def exterior_guess(sol, mass, mb, a, eps):
    """Extend an existing exterior solution into a longer numerical domain."""
    old_l = float(sol.x[-1])
    psi_l, _, s_l, _ = sol.sol(old_l)
    mu = float(psi_l - mass/old_l + plummer(old_l, mb, a)[0])
    lam = math.sqrt(eps/3)

    def evaluate(r):
        rr = np.asarray(r)
        y = sol.sol(np.minimum(rr, old_l))
        outside = rr > old_l
        if np.any(outside):
            ro = rr[outside]
            sb = s_l * old_l / ro * np.exp(-(ro - old_l)/lam)
            y[:, outside] = np.array([
                mu + mass/ro - plummer(ro, mb, a)[0],
                -mass/ro**2 - mb*ro/(ro**2 + a*a)**1.5,
                sb, -sb*(1/lam + 1/ro)])
        return y
    return evaluate


def solve_response(baseline, eps, mb, a, guess, refine=False, auxiliary_radius=None):
    mass = baseline["mass_dimensionless"]
    outer = baseline["outer_radius"]
    lam = math.sqrt(eps/3)
    if refine:
        outer += max(6*lam, 0.25*auxiliary_radius)
    tol = 2e-7 if refine else 1e-6
    grid = np.unique(np.concatenate(([0.0], np.geomspace(1e-6, outer, 350),
                                    np.linspace(0, min(0.5, outer), 200),
                                    np.linspace(0, outer, 450))))
    singular = np.diag([0.0, -2.0, 0.0, -2.0])

    def rhs(r, y):
        pp = np.maximum(y[0], 0.0)
        ey = np.exp(3*y[2])
        return np.array([y[1], -pp**1.5*ey - plummer(r, mb, a)[1], y[3],
                         (ey*(1 - pp**2.5) - 1)/eps])

    def jac(r, y):
        pp = np.maximum(y[0], 0.0)
        ey = np.exp(3*y[2])
        out = np.zeros((4, 4, r.size))
        out[0, 1] = 1
        out[1, 0] = -1.5*np.sqrt(pp)*ey
        out[1, 2] = -3*pp**1.5*ey
        out[2, 3] = 1
        out[3, 0] = -2.5*pp**1.5*ey/eps
        out[3, 2] = 3*ey*(1 - pp**2.5)/eps
        return out

    total_mass_at_outer = mass + float(plummer(outer, mb, a)[2])
    tail = 1/lam + 1/outer

    def bc(left, right):
        return np.array([left[1], left[3],
                         (-outer**2*right[1] - total_mass_at_outer)/mass,
                         right[3] + tail*right[2]])

    sol = solve_bvp(rhs, bc, grid, guess(grid), S=singular, fun_jac=jac,
                    tol=tol, max_nodes=20000)
    row = {"epsilon": eps, "baryon_total_mass": mb, "baryon_scale": a,
           "target_dark_mass": mass, "refinement": refine,
           "outer_radius": outer, "tolerance": tol,
           "solver_status": int(sol.status), "solver_message": sol.message,
           "iterations": int(sol.niter), "nodes": int(sol.x.size),
           "maximum_rms_residual": float(np.max(sol.rms_residuals)),
           "bc_max_residual": float(np.max(np.abs(bc(sol.y[:, 0], sol.y[:, -1])))),
           "passed": False}
    if not sol.success:
        return row, sol

    def state(r):
        psi, dp, ss, ds = sol.sol(r)
        pp = np.maximum(psi, 0.0)
        es = np.exp(3*ss)
        return psi, dp, ss, ds, pp**1.5*es, pp**2.5*es, np.expm1(3*ss) - 3*ss

    if sol.sol(0)[0] <= 0 or sol.sol(outer)[0] >= 0:
        row["failure_reason"] = "A positive finite matter edge is not enclosed."
        return row, sol
    radius = brentq(lambda r: float(sol.sol(r)[0]), 0, outer, xtol=1e-13)
    psi_c, _, sc, _, nc, _, _ = (float(x) for x in state(0))
    rq = brentq(lambda r: float(state(r)[4]) - nc/4, 0, radius, xtol=1e-13)
    column = math.sqrt(2.5)*nc*rq

    def integrate(fn, upper=outer):
        return quad(fn, 0, upper, epsabs=2e-9, epsrel=2e-9,
                    points=[radius] if upper > radius else None, limit=600)[0]

    mass_quad = integrate(lambda r: r*r*float(state(r)[4]), radius)
    total_mass_edge = -radius**2*float(sol.sol(radius)[1])
    baryon_mass_edge = float(plummer(radius, mb, a)[2])
    dark_mass_slope = total_mass_edge - baryon_mass_edge
    mass_error = abs(mass_quad/mass - 1)
    poisson_error = abs((mass_quad + baryon_mass_edge)/total_mass_edge - 1)
    wrong_sign_error = abs((mass_quad - baryon_mass_edge)/total_mass_edge - 1)
    source = lambda r: math.exp(3*float(sol.sol(r)[2])) * (
        1 - max(float(sol.sol(r)[0]), 0)**2.5) - 1
    source_integral = integrate(lambda r: r*r*source(r))
    source_abs_integral = integrate(lambda r: r*r*abs(source(r)))
    scalar_boundary = eps*outer*outer*float(sol.sol(outer)[3])
    scalar_error = abs(source_integral - scalar_boundary)/(1 + source_abs_integral)

    def stress(r):
        _, _, _, ds, _, aa, uu = state(r)
        return np.array([aa - uu + 1.5*eps*ds*ds,
                         aa - uu - 1.5*eps*ds*ds])

    rr = np.unique(np.concatenate((np.geomspace(1e-4, 0.95*radius, 220),
                                   np.linspace(0.05*radius, 0.99*outer, 250))))
    hh = 2e-5*np.maximum(0.01, rr)
    dpr = (-stress(rr + 2*hh)[0] + 8*stress(rr + hh)[0]
           - 8*stress(rr - hh)[0] + stress(rr - 2*hh)[0])/(12*hh)
    prt = stress(rr)
    force_left = dpr + 2*(prt[0] - prt[1])/rr
    sample = state(rr)
    force_right = 2.5*sample[4]*sample[1]
    force_error = float(np.max(np.abs(force_left - force_right)) /
                        max(1.0, np.max(np.abs(force_right))))

    erel = integrate(lambda r: 1.5*r*r*float(state(r)[5]))
    potential = integrate(lambda r: r*r*float(state(r)[6]))
    gradient = integrate(lambda r: 1.5*eps*r*r*float(sol.sol(r)[3])**2)
    # W_b is the external virial, not the external Plummer potential energy.
    virial_b = integrate(lambda r: -2.5*float(state(r)[4])*mb*r**4 /
                         (r*r + a*a)**1.5, radius)
    virial_total = integrate(lambda r: 2.5*r**3*float(state(r)[4]) *
                             float(sol.sol(r)[1]), radius)
    virial_dark = virial_total - virial_b
    boundary_stress = outer**3*float(stress(outer)[0])
    virial_residual = 2*erel - 3*potential - gradient + virial_total - boundary_stress
    virial_scale = 2*erel + 3*potential + gradient + abs(virial_total)
    virial_error = abs(virial_residual)/virial_scale
    mu = float(sol.sol(outer)[0]) - mass/outer + float(plummer(outer, mb, a)[0])
    self_energy = integrate(lambda r: 1.25*r*r*float(state(r)[4]) *
                            (mu - float(sol.sol(r)[0]) - float(plummer(r, mb, a)[0])), radius)
    external_energy = integrate(lambda r: 2.5*r*r*float(state(r)[4]) *
                                float(plummer(r, mb, a)[0]), radius)
    gravity_error = abs(self_energy/virial_dark - 1)
    edge_slope = -float(sol.sol(radius)[1])
    edge_offsets = radius*np.array([1e-3, 5e-4, 1e-4])
    edge_ratios = np.asarray(state(radius - edge_offsets)[4]) / (
        math.exp(3*float(sol.sol(radius)[2]))*(edge_slope*edge_offsets)**1.5)
    sampled = state(np.linspace(0, outer, 1500))
    checks = {
        "finite_positive_halo": 0 < radius < outer and nc > 0 and dark_mass_slope > 0,
        "positive_monotone_scalar": float(np.min(sampled[2])) > -1e-10 and float(np.max(sampled[3])) < 1e-8,
        "monotone_total_potential_depth": float(np.max(sampled[1])) < 1e-10,
        "regular_boundary_residual": row["bc_max_residual"] < 1e-8,
        "small_outer_scalar": abs(float(sol.sol(outer)[2])) < 1e-6,
        "fixed_dark_mass": mass_error < 2e-5,
        "poisson_mass_integral": poisson_error < 2e-5,
        "wrong_baryon_source_sign_rejected": mb == 0 or wrong_sign_error > 2e-5,
        "scalar_integral": scalar_error < 2e-5,
        "radial_force_balance": force_error < 5e-4,
        "virial_identity": virial_error < 2e-5,
        "self_gravity_energy_identity": gravity_error < 2e-5,
        "regular_matter_edge": edge_slope > 0 and np.all(np.isfinite(edge_ratios)),
    }
    ratios = {"radius": radius/baseline["radius"], "density_c": nc/baseline["density_c"],
              "quarter_radius": rq/baseline["quarter_radius"],
              "core_column_coefficient": column/baseline["core_column_coefficient"]}
    if mb == 0:
        checks["zero_forcing_recovers_baseline"] = max(abs(v - 1) for v in ratios.values()) < 5e-5
    row.update({"checks": {key: bool(value) for key, value in checks.items()},
                "passed": bool(all(checks.values())), "psi_c": psi_c, "s_c": sc,
                "density_c": nc, "radius": radius, "quarter_radius": rq,
                "core_column_coefficient": column, "ratios_to_baseline": ratios,
                "central_scalar_change": sc - baseline["s_c"],
                "dark_mass_quadrature": mass_quad, "dark_mass_from_slope": dark_mass_slope,
                "mass_relative_error": mass_error, "poisson_mass_relative_error": poisson_error,
                "wrong_source_sign_relative_error": wrong_sign_error,
                "scalar_integrated_error": scalar_error, "radial_force_scaled_error": force_error,
                "virial_scaled_error": virial_error, "self_gravity_energy_relative_error": gravity_error,
                "s_outer": float(sol.sol(outer)[2]), "s_at_matter_edge": float(sol.sol(radius)[2]),
                "edge_density_over_leading_asymptote": edge_ratios.tolist(),
                "edge_fractional_inward_offsets": [1e-3, 5e-4, 1e-4],
                "edge_asymptote_is_diagnostic_not_error_certificate": True,
                "mu_over_enthalpy_scale": mu,
                "energies_over_4pi_B_ell_cubed": {"relative": erel, "scalar_potential": potential,
                    "scalar_gradient": gradient, "self_gravity": self_energy,
                    "external_potential": external_energy, "external_virial": virial_b,
                    "self_gravity_virial": virial_dark, "outer_virial_boundary": boundary_stress}})
    return row, sol


def main():
    output = Path(sys.argv[1])
    frozen = load_baseline()
    control = plummer_controls()
    baselines, rows, refinements, profiles = [], [], [], {}
    for pc in (0.8, 0.95, 0.99):
        auxiliary, original_guess = frozen.local_solution(pc)
        for eps in (1e-4, 1e-2):
            baseline, base_sol = frozen.solve_case(pc, eps, auxiliary, original_guess)
            baselines.append(baseline)
            label = f"p{pc}_e{eps}"
            if not baseline.get("passed", False):
                for family in FAMILIES:
                    for fraction in FRACTIONS:
                        rows.append({"baseline_psi_c": pc, "epsilon": eps, "family": family,
                                     "fraction": fraction, "passed": False,
                                     "not_attempted": "baseline checks failed"})
                continue
            for family, (mass_ratio, radius_ratio) in FAMILIES.items():
                final_mb = mass_ratio*baseline["mass_dimensionless"]
                a = radius_ratio*baseline["radius"]
                previous = base_sol
                stopped = False
                endpoint = None
                for fraction in FRACTIONS:
                    meta = {"baseline_psi_c": pc, "epsilon": eps, "family": family, "fraction": fraction}
                    if stopped:
                        rows.append(dict(meta, passed=False, not_attempted="previous continuation failed"))
                        continue
                    try:
                        row, sol = solve_response(baseline, eps, fraction*final_mb, a, previous.sol)
                        row.update(meta)
                        if sol.success:
                            r = np.linspace(0, row["outer_radius"], 400)
                            profiles[f"{label}_{family}_f{fraction}"] = np.vstack((r, sol.sol(r)))
                        if row["passed"]:
                            previous = sol
                            if fraction == 1:
                                endpoint = (row, sol)
                        else:
                            stopped = True
                    except Exception as exc:
                        row = dict(meta, passed=False, exception=repr(exc), traceback=traceback.format_exc())
                        stopped = True
                    rows.append(row)
                    print(json.dumps({key: row.get(key) for key in (
                        "baseline_psi_c", "epsilon", "family", "fraction", "passed", "psi_c",
                        "ratios_to_baseline", "exception")}), flush=True)
                if pc == 0.99:
                    meta = {"baseline_psi_c": pc, "epsilon": eps, "family": family, "fraction": 1.0}
                    if endpoint is None:
                        refinements.append(dict(meta, passed=False, not_attempted="main endpoint unavailable"))
                        continue
                    try:
                        old_row, old_sol = endpoint
                        extended = exterior_guess(old_sol, baseline["mass_dimensionless"], final_mb, a, eps)
                        fine, fine_sol = solve_response(baseline, eps, final_mb, a, extended,
                                                       refine=True, auxiliary_radius=auxiliary["radius"])
                        fine.update(meta)
                        keys = ("radius", "density_c", "core_column_coefficient")
                        fine["relative_changes_from_main"] = {
                            key: abs(fine[key]/old_row[key] - 1) for key in keys} if fine["passed"] else {}
                        fine["domain_and_tolerance_check"] = bool(fine["passed"] and
                            max(fine["relative_changes_from_main"].values()) < 5e-5)
                        if fine_sol.success:
                            r = np.linspace(0, fine["outer_radius"], 400)
                            profiles[f"{label}_{family}_refined"] = np.vstack((r, fine_sol.sol(r)))
                    except Exception as exc:
                        fine = dict(meta, passed=False, domain_and_tolerance_check=False,
                                    exception=repr(exc), traceback=traceback.format_exc())
                    refinements.append(fine)
    checks = {"plummer_controls": control["passed"],
              "six_baselines": len(baselines) == 6 and all(row.get("passed", False) for row in baselines),
              "sixty_response_records": len(rows) == 60,
              "all_requested_responses_verified": all(row.get("passed", False) for row in rows),
              "four_refinement_records": len(refinements) == 4,
              "all_refinements_verified": len(refinements) == 4 and all(
                  row.get("domain_and_tolerance_check", False) for row in refinements)}
    result = {"claim_id": "FR01_STATIC", "checks": checks, "plummer_controls": control,
              "baselines": baselines, "cases": rows, "refinements": refinements,
              "scope": "Fixed-dark-mass conditional static response; diagnostic spherical baryons, no stability, formation or observational calibration."}
    output.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n")
    np.savez_compressed(output.with_name("profiles.npz"), **profiles)
    print(json.dumps(checks, sort_keys=True), flush=True)
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
