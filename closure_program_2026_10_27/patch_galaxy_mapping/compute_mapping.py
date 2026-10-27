#!/usr/bin/env python3
"""Conditional patch-to-galaxy ancestry accounting; no formation efficiency fit."""
import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def mass_budget(patch_fraction, patch_mass, descendant_mass, rho_b):
    if not (0 <= patch_fraction <= 1 and 0 < descendant_mass <= patch_mass and rho_b > 0):
        raise ValueError("Closed-reservoir masses and fraction required")
    epsilon = descendant_mass / patch_mass
    number_density = patch_fraction * rho_b / patch_mass
    return dict(epsilon=epsilon, patch_number_density_Mpc_minus3=number_density,
                descendant_mass_density_Msun_Mpc3=number_density * descendant_mass,
                descendant_fraction_of_cosmic_baryons=epsilon * patch_fraction)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    if a.output.exists():
        raise FileExistsError(a.output)
    capacity = json.loads((ROOT / "closure_program_2026_10_27/capacity_run/results.json").read_text())
    population = json.loads((ROOT / "closure_program_2026_10_27/population/run/results.json").read_text())
    x22 = json.loads((ROOT / "rebuild_2026_10_22/X22_cosmic_dust_window/x22_cosmic_dust_window_results.json").read_text())
    rho_b = capacity["native"]["rho_b_Msun_Mpc3"]
    census = population["census"]
    # X22's declared Om/Ob ratio, also explicitly used by X57 for this median.
    original_total_to_baryon = 6.364
    known = mass_budget(.06, 5., 1., 100.)
    checks = {"known_reservoir_case": math.isclose(known["descendant_fraction_of_cosmic_baryons"], .012),
              "census_rhob_matches": math.isclose(rho_b, population["native"]["rho_b_Msun_Mpc3"], rel_tol=1e-13)}
    result = dict(status="CONDITIONAL_ANCESTRY_ACCOUNTING_NOT_POPULATION_OR_FOREST_CLOSURE",
                  inherited_forest_budget_is_not_calibrated=True, footings={}, checks=checks,
                  actual_template="P1D1/P1D2 use one fixed representative comoving patch radius; no mass-dependent population is simulated",
                  conditions=["One disjoint patch produces one descendant; mergers, fragmentation and external accretion require new ancestry bookkeeping",
                              "X22's law-inferred effective baryon mass is a dynamical proxy; equating it to census stars+cold gas is an extra assumption",
                              "The implied efficiency is conditional on matching this descendant mass to this patch, not an observed formation efficiency",
                              "Representative mass fractions relative to the entire census are inventory ratios, not coverage of a measured mass function",
                              "The separate native mass-scaled identity changes the patch-size model; its forest response must be recalculated"])
    for f, row in capacity["footings"].items():
        galaxy_mass = x22["step2"]["per_footing"][f]["M_L_Msun"][2] / original_total_to_baryon
        patch_mass = row["baryon_mass_per_patch_Msun"]
        b = mass_budget(row["exact_two_phase_fraction"], patch_mass, galaxy_mass, rho_b)
        b.update(descendant_effective_baryon_mass_Msun=galaxy_mass, initial_patch_baryon_mass_Msun=patch_mass,
                 fraction_of_all_stars_coldgas_inventory=b["descendant_fraction_of_cosmic_baryons"] / census["F_cold_baseline"],
                 fraction_of_stars_HI_He_inventory=b["descendant_fraction_of_cosmic_baryons"] / census["F_stars_plus_HI_He"],
                 census_normalization_is_not_a_measured_population_fraction=True)
        checks[f + "_ancestry_mass_conserved"] = math.isclose(b["descendant_mass_density_Msun_Mpc3"] / rho_b,
                  b["descendant_fraction_of_cosmic_baryons"], rel_tol=1e-13)
        checks[f + "_count_matches_capacity"] = math.isclose(b["patch_number_density_Mpc_minus3"],
                  row["patch_number_density_Mpc_minus3"], rel_tol=1e-13)
        d = row["delta_b_in"]
        scaled = dict(epsilon_if_native_volume_equals_Mgal_over_rhob=1/(1+d),
                      descendant_baryon_fraction_if_same_point_variance_budget=row["exact_two_phase_fraction"]/(1+d),
                      physical_forest_budget_for_new_size_distribution="NOT ESTABLISHED")
        # A three-bin exact identity tests the mass-scaled bookkeeping without
        # assuming a real galaxy mass function or borrowing its halo abundance.
        masses = [1e8, 1e9, 1e10]
        numbers = [.01, .005, .001]
        galaxy_density = sum(m*n for m,n in zip(masses,numbers))
        patch_density = sum((1+d)*m*n for m,n in zip(masses,numbers))
        checks[f + "_mass_scaled_integral_identity"] = math.isclose(patch_density/galaxy_density, 1+d, rel_tol=1e-13)
        result["footings"][f] = dict(literal_representative_patch=b, separate_native_mass_scaled_accounting_identity=scaled)
    if not all(checks.values()):
        raise AssertionError(checks)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
