#!/usr/bin/env python3
"""Exact two-phase mass accounting for the specified M6 patch model.

This does not turn the X57 variance prescription into a measured flux bound.
Run from the repository root with --output PATH (fresh result path).
"""
import argparse
import json
import math
from pathlib import Path


def phase_state(delta, volume_fraction):
    if delta <= 0 or not 0 <= volume_fraction <= 1 / (1 + delta):
        raise ValueError("positive overdensity and nonnegative outside density required")
    f = volume_fraction
    outside = -f * delta / (1 - f)
    return {"baryon_fraction": f * (1 + delta),
            "outside_delta": outside,
            "mean_density": f * (1 + delta) + (1 - f) * (1 + outside),
            "point_variance": f * delta * delta / (1 - f)}


def exact_fraction_at_variance(delta, variance):
    if delta <= 0 or variance < 0:
        raise ValueError("invalid density or variance")
    # V = delta^2 F / (1 + delta - F); enforce outside positivity as well.
    return min(1.0, variance * (1 + delta) / (delta * delta + variance))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    p1 = json.loads(Path("rebuild_2026_10_22/P1D1_m6_boera_high_z_forest/p1d1_m6_boera_results.json").read_text())
    x57 = json.loads(Path("rebuild_2026_10_22/X57_exclusion_mechanism/x57_exclusion_results.json").read_text())
    native = p1["backgrounds"]["native"]
    h = native["h"]
    omega_b = native["OB"] * h * h
    # Critical density per h^2 in solar masses / Mpc^3; fixed conversion,
    # not an observational matter-density input.
    rho_b = 2.77536627e11 * omega_b
    radius_mpc = x57["step0"]["X22_R_L_med"] / h
    volume_mpc3 = 4 * math.pi * radius_mpc ** 3 / 3
    checks = {}
    simple = phase_state(1.0, 0.25)
    checks["two_phase_known_case"] = (abs(simple["baryon_fraction"] - .5) < 1e-14
        and abs(simple["outside_delta"] + 1/3) < 1e-14
        and abs(simple["point_variance"] - 1/3) < 1e-14
        and abs(simple["mean_density"] - 1) < 1e-14)
    checks["zero_patch_limit"] = phase_state(1, 0)["point_variance"] == 0
    checks["all_baryons_limit"] = abs(phase_state(4, .2)["outside_delta"] + 1) < 1e-14
    checks["known_variance_inverse"] = abs(exact_fraction_at_variance(1, .5) - 2/3) < 1e-14
    result = {"claim": "Exact accounting and conditional capacity of the specified two-phase M6 population",
              "status": "conditional_on_X57_variance_prescription_not_a_flux_likelihood",
              "native": {"h": h, "omega_b": omega_b, "rho_b_Msun_Mpc3": rho_b,
                         "patch_radius_comoving_Mpc": radius_mpc,
                         "patch_volume_comoving_Mpc3": volume_mpc3},
              "footings": {}, "checks": checks,
              "non_claims": ["No physical forest confidence bound is established",
                             "No galaxy formation efficiency or isolated-population fraction is measured",
                             "No nonlinear patch evolution or mass-profile closure is established"]}
    for footing, row in native["m6"].items():
        delta = row["delta_b_in"]
        F_old = row["Fb_max_z3"]
        B = F_old * delta ** 2 / (1 + delta)
        F_exact = exact_fraction_at_variance(delta, B)
        state = phase_state(delta, F_exact / (1 + delta))
        Mpatch = rho_b * volume_mpc3 * (1 + delta)
        npatch = state["baryon_fraction"] * rho_b / Mpatch
        checks[footing + "_variance_inversion"] = abs(state["point_variance"] / B - 1) < 1e-12
        checks[footing + "_mass_normalization"] = abs(npatch * Mpatch / rho_b / F_exact - 1) < 1e-12
        checks[footing + "_mean_conservation"] = abs(state["mean_density"] - 1) < 1e-12
        result["footings"][footing] = {
            "delta_b_in": delta, "original_dilute_variance_fraction": F_old,
            "variance_budget": B, "exact_two_phase_fraction": F_exact,
            "state_at_exact_variance_ceiling": state,
            "baryon_mass_per_patch_Msun": Mpatch,
            "patch_number_density_Mpc_minus3": npatch,
            "baryon_density_in_patches_Msun_Mpc3": F_exact * rho_b,
            "capacity_by_retained_efficiency": [
                {"epsilon": e, "max_observed_galaxy_baryon_density_Msun_Mpc3": e * F_exact * rho_b}
                for e in (.25, .5, .75, 1.0)],
            "necessary_population_condition": "rho_baryons_required_in_galaxies <= epsilon * F_allowed * rho_b",
            "population_mapping_conditions": [
                "Count each baryon and each Lagrangian patch once",
                "epsilon is retained galaxy baryons divided by initial patch baryons, at most one",
                "If external baryons enter, include their provenance and associated cold accretion; the simple closed-reservoir bound then needs extension",
                "Identify the required isolated/law population independently of the M6 budget"]}
    if not all(checks.values()):
        raise AssertionError(checks)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"native": result["native"], "footings": result["footings"], "checks": checks}, indent=2))


if __name__ == "__main__":
    main()
