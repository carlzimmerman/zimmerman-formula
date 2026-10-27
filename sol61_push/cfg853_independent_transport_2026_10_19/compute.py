"""Small, reproducible CFG853 discriminators. See TARGET.md and contract.json.

No dynamics, raw-star reduction, posterior fit, or source-action capture rate.
"""
import csv
import itertools
import json
import math
import platform
import resource
import sys
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import quad
from scipy.optimize import linprog

BASE = Path("sol61_push/cfg853_independent_transport_2026_10_19")
G, MSUN, PC = 6.674e-11, 1.989e30, 3.0857e16
G_PC_KMS = G * MSUN / (PC * 1e6)
PSTAR, COLD_RATIO, FRET = 64 / 125, 5.364, 0.1
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
checks = []


def check(name, condition):
    checks.append({"name": name, "pass": bool(condition)})
    if not condition:
        raise AssertionError(name)


def close(name, actual, expected, rel=1e-10, absolute=1e-12):
    check(name, math.isclose(actual, expected, rel_tol=rel, abs_tol=absolute))


def mass_floor(a1, a2, sigma1, sigma2):
    """Sharp finite positive-measure mass lower bound, pc and km/s inputs."""
    if not 0 < a1 < a2 or min(sigma1, sigma2) <= 0:
        raise ValueError("ordered positive scales and positive moments required")
    h = a2 / a1
    y1 = 3 * a1 * sigma1**2 / G_PC_KMS
    y2 = 3 * a2 * sigma2**2 / G_PC_KMS
    ratio = y2 / y1
    if ratio < 1 or ratio >= h**3:
        return {"finite_positive_measure_possible": False, "h": h, "R": ratio,
                "single_tracer_floor_Msun": [y1, y2]}
    if ratio == 1:
        u, radius, mass = 1.0, 0.0, y1
    else:
        u = ((h*h / ratio**(2/3) - 1) / (h*h - 1))**1.5
        radius = a1 * math.sqrt(u**(-2/3) - 1)
        mass = y1 / u
    return {"finite_positive_measure_possible": True, "h": h, "R": ratio,
            "single_tracer_floor_Msun": [y1, y2], "sharp_floor_Msun": mass,
            "saturating_shell_radius_pc": radius, "u_at_equality": u}


def main(outpath):
    old = json.loads(Path("sol61_push/cold_final_mile_2026_10_13/run_086_v2/results.json").read_text())
    binaries = {x["name"]: x for x in json.loads(Path(
        "campaign_fresh_gravity/CFG861_classical_dsph_binaries/cfg861_results.json"
    ).read_text())["systems"]}
    catalog = {x["name"]: x for x in csv.DictReader(Path(
        "real_research/data/dsph/lvd_dwarf_mw.csv").open())}
    extraction = json.loads((BASE / "source_extraction.json").read_text())
    rows = []
    for footing, a0 in A0.items():
        for d in old["dwarfs"]:
            name = d["name"]
            ms = d["ups"] * 10**(.4 * (4.83 - float(catalog[name]["M_V"])))
            radius = d["R_pc"]
            y = G * PSTAR * ms * MSUN / ((radius * PC)**2 * a0)
            retained = min(PSTAR * (math.sqrt(.25 + 1 / y) - .5), COLD_RATIO)
            stock = (COLD_RATIO / FRET - retained) * ms
            total = (1 + COLD_RATIO / FRET) * ms
            limits = {"name": name, "footing": footing, "Mstar_Msun": ms,
                      "R_pc": radius, "ups": d["ups"],
                      "retained_cold_Msun": retained * ms,
                      "remaining_free_stock_Msun": stock,
                      "generous_total_gravitating_stock_Msun": total,
                      "catalog_sigma_reference": catalog[name]["ref_vlos"],
                      "maximum_aperture_sigma_kms_all_cold_and_pstars": math.sqrt(
                          G_PC_KMS * (COLD_RATIO/FRET + PSTAR) * ms / (3 * radius))}
            for mode in ["original", "relative_transfer_sensitivity", "paper_flag_transfer_sensitivity",
                         "absolute_clean_subset_sensitivity"]:
                b = binaries[name]
                if mode == "relative_transfer_sensitivity":
                    sigma = d["sigma_obs_kms"] * 10**(b["delta"] / 2)
                elif mode == "paper_flag_transfer_sensitivity":
                    sigma = d["sigma_obs_kms"] * 10**(b["delta_pf"] / 2)
                elif mode == "absolute_clean_subset_sensitivity":
                    sigma = b["sig_clean_M"]["sig"]
                else:
                    sigma = d["sigma_obs_kms"]
                required = 3 * sigma**2 * radius / G_PC_KMS - (PSTAR + retained) * ms
                fraction = required / stock
                row = dict(limits, mode=mode, sigma_kms=sigma,
                           required_free_mass_Msun=required, required_free_fraction=fraction,
                           tau_one_hit=(-math.log1p(-fraction) if 0 < fraction < 1 else None),
                           stock_possible=0 <= fraction <= 1)
                if footing == "canonical" and mode == "original":
                    close(name + " original normalized budget replay", fraction,
                          d["target_remaining_cold_fraction"])
                close(name + footing + mode + " stock decomposition",
                      stock + retained * ms, COLD_RATIO/FRET * ms)
                close(name + footing + mode + " aperture mass reconstructed",
                      required + (PSTAR + retained)*ms, 3*sigma**2*radius/G_PC_KMS)
                if 0 < fraction < 1:
                    close(name + footing + mode + " one-hit inversion",
                          -math.expm1(-row["tau_one_hit"]), fraction)
                rows.append(row)

    kernel_cases = []
    for mode in ["original", "relative_transfer_sensitivity", "paper_flag_transfer_sensitivity"]:
        byname = {x["name"]: x for x in rows if x["footing"] == "canonical" and x["mode"] == mode}
        for small in ["Draco", "Sextans"]:
            for guard in ["Fornax", "Leo I"]:
                d, f = byname[small], byname[guard]
                ratio = d["tau_one_hit"] / f["tau_one_hit"]
                mratio = f["remaining_free_stock_Msun"] / d["remaining_free_stock_Msun"]
                kernel_cases.append({"mode": mode, "target": small, "guard": guard,
                    "needed_optical_depth_ratio": ratio, "common_density_clock_kernel_upper_ratio": mratio,
                    "minimum_Ndyn_target_over_guard_when_target_no_hotter": ratio / mratio,
                    "same_density_and_Ndyn_common_nonnegative_velocity_kernel_excluded": ratio > mratio})
                # Different densities cancel while the virial cloud stays no hotter.
                for rho_ratio in [0.1, 1, min(10, mratio*mratio)]:
                    sratio = mratio**(-1/3) * rho_ratio**(1/6)
                    close(small+guard+mode+str(rho_ratio)+" Maxwell exposure cancellation",
                          rho_ratio**.5 / sratio**3, mratio)
    check("strong Leo I guard obstruction remains in transfer sensitivity",
          all(x["same_density_and_Ndyn_common_nonnegative_velocity_kernel_excluded"]
              for x in kernel_cases if x["guard"] == "Leo I"))
    # Orthogonal analytic kernel fixture: K(v)=v^p, integral is elementary Gamma.
    def moment(s, exponent):
        return 2**(exponent+1) * s**exponent * math.gamma((exponent+3)/2) / math.sqrt(math.pi)
    for exponent in [-2.8, -2, 0, 1, 4]:
        sd, sf = .7, 1.8
        ratio = moment(sd, exponent)/moment(sf, exponent)
        check("Maxwell moment bound " + str(exponent), ratio <= (sf/sd)**3)
        numerical = quad(lambda v: v**exponent * v*v * math.exp(-v*v/(4*sf*sf)) /
                         (2*math.sqrt(math.pi)*sf**3), 0, np.inf, epsabs=1e-9)[0]
        close("Maxwell normalization/moment " + str(exponent), numerical, moment(sf, exponent), rel=1e-8)

    # Two-tracer theorem: independent shell fixture, smooth self-Plummer benchmark.
    fixture_mass, fixture_radius, af1, af2 = 83.0, 2.7, 1.3, 4.1
    fixture_sigma = [math.sqrt(G_PC_KMS*fixture_mass/(3*a)*(1+(fixture_radius/a)**2)**-1.5)
                     for a in [af1, af2]]
    recovered = mass_floor(af1, af2, *fixture_sigma)
    close("independent shell exact mass recovery", recovered["sharp_floor_Msun"], fixture_mass)
    close("independent shell exact radius recovery", recovered["saturating_shell_radius_pc"], fixture_radius)
    apl, mpl = 1.7, 23.0
    val1 = quad(lambda r: (3/(4*math.pi*apl**3))*(1+(r/apl)**2)**-2.5 *
                (mpl*r**3/(r*r+apl*apl)**1.5)*r, 0, np.inf)[0] * (4*math.pi*G_PC_KMS/3)
    val2 = quad(lambda r: (1+(r/apl)**2)**-1.5 *
                (3*mpl*r*r/apl**3)*(1+(r/apl)**2)**-2.5, 0, np.inf)[0]*G_PC_KMS/(3*apl)
    close("projected Jeans integral self-Plummer benchmark", val1, math.pi*G_PC_KMS*mpl/(32*apl))
    close("radial mass-measure kernel self-Plummer benchmark", val2, val1)

    pops = extraction["populations"]
    radii = [1000*extraction["distance_kpc"]*math.tan(math.radians(p["Rh_deg"])) for p in pops]
    sigmas = [p["sigma_kms"] for p in pops]
    mainbound = mass_floor(*radii, *sigmas)
    # Independent optimization over radial mass bins; shell optimizer is NOT put on grid.
    grid = radii[0]*np.concatenate(([0.0], np.geomspace(1e-5, 1e5, 2000)))
    weights = np.array([(1+(grid/a)**2)**-1.5 for a in radii])
    normalized_y = np.array(mainbound["single_tracer_floor_Msun"])/mainbound["single_tracer_floor_Msun"][0]
    lp = linprog(np.ones(len(grid)), A_eq=weights, b_eq=normalized_y,
                 bounds=(0, None), method="highs")
    check("radial positive-mass LP found a feasible profile", lp.success)
    lp_mass = lp.fun * mainbound["single_tracer_floor_Msun"][0]
    check("LP does not violate analytic mass floor", lp_mass >= mainbound["sharp_floor_Msun"]*(1-1e-8))
    close("independent radial LP agrees with sharp mass floor", lp_mass,
          mainbound["sharp_floor_Msun"], rel=3e-4)
    shell = mainbound["saturating_shell_radius_pc"]
    for a, sig in zip(radii, sigmas):
        close("published conditional shell reproduces moment a="+str(a),
              G_PC_KMS*mainbound["sharp_floor_Msun"]/(3*a)*(1+(shell/a)**2)**-1.5, sig*sig)
    mainbound.update({"radii_pc": radii, "sigma_kms": sigmas,
                      "independent_LP_minimum_Msun": lp_mass,
                      "LP_equality_residual": float(np.max(np.abs(weights@lp.x-normalized_y)))})
    sx = next(r for r in rows if r["name"] == "Sextans" and r["mode"] == "original"
              and r["footing"] == "canonical")
    new_sigma = extraction["global_sigma_kms"]
    sextans_global_sensitivity = {
        "meaning": "New survey global sigma inserted at OLD catalogue aperture and stellar inputs; a sensitivity, not a matched new mass measurement",
        "sigma_kms": new_sigma,
        "required_free_fraction": (3*new_sigma**2*sx["R_pc"]/G_PC_KMS - PSTAR*sx["Mstar_Msun"] -
                                   sx["retained_cold_Msun"])/sx["remaining_free_stock_Msun"]}
    comparisons = []
    for geom in [1.0, math.sqrt(.71), .8]:
        bound = mainbound["sharp_floor_Msun"] * geom
        outer = mainbound["single_tracer_floor_Msun"][1] * geom
        comparisons.append({"common_radius_factor": geom,
            "outer_only_floor_Msun": outer, "joint_floor_Msun": bound,
            "generous_total_stock_Msun": sx["generous_total_gravitating_stock_Msun"],
            "outer_floor_over_stock": outer/sx["generous_total_gravitating_stock_Msun"],
            "joint_floor_over_stock": bound/sx["generous_total_gravitating_stock_Msun"],
            "maximum_fret_outer_if_total_stock_used": COLD_RATIO/(outer/sx["Mstar_Msun"]-1),
            "maximum_fret_joint_if_total_stock_used": COLD_RATIO/(bound/sx["Mstar_Msun"]-1)})
        check("common geometry scales mass floor "+str(geom), outer > sx["generous_total_gravitating_stock_Msun"])
    sensitivity = []
    # Rectangular endpoints only: NOT a posterior, and not an exhaustive continuous-box proof.
    ranges = [[p["Rh_deg"]-p["Rh_error_deg"], p["Rh_deg"]+p["Rh_error_deg"]] for p in pops]
    ranges += [[p["sigma_kms"]-p["sigma_error_minus_kms"], p["sigma_kms"]+p["sigma_error_plus_kms"]] for p in pops]
    for r1, r2, s1, s2 in itertools.product(*ranges):
        aa = [1000*extraction["distance_kpc"]*math.tan(math.radians(r)) for r in [r1,r2]]
        bnd = mass_floor(*aa, s1, s2)
        sensitivity.append({"Rh_deg": [r1,r2], "sigma_kms": [s1,s2], **bnd})
    check("all 16 sensitivity corners evaluated", len(sensitivity) == 16)

    # Measure-level compact profile discriminator; support refers to ALL mass.
    compact = []
    for b in [25, 56.9, 648, 1000, 1302, 2000]:
        maxR = ((1+(b/radii[0])**2)/(1+(b/radii[1])**2))**1.5
        compact.append({"outer_support_radius_pc": b, "maximum_y2_over_y1": maxR,
                        "needed_y2_over_y1": mainbound["R"],
                        "positive_mass_profile_possible_by_ratio": maxR >= mainbound["R"]})
    check("648 pc total support cannot reproduce two central moments", not compact[2]["positive_mass_profile_possible_by_ratio"])

    result = {"checkpoint": "CFG853-20261019-A", "checks": checks,
        "all_checks_pass": all(c["pass"] for c in checks), "n_checks": len(checks),
        "four_dwarf_budget_cases": rows, "common_velocity_kernel_cases": kernel_cases,
        "sextans_new_global_at_old_radius_sensitivity": sextans_global_sensitivity,
        "two_tracer_conditional_bound": mainbound, "two_tracer_stock_comparisons": comparisons,
        "two_tracer_16_corner_sensitivity": sensitivity, "compact_total_support_tests": compact,
        "software": {"Python": platform.python_version(), "NumPy": np.__version__, "SciPy": scipy.__version__},
        "peak_rss": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "rss_units": "bytes on Darwin, KiB on Linux", "platform": platform.system(),
        "non_claims": ["No action-derived capture or cooling kernel or physical formation history",
                       "Binary shift transfers and absolute subset replacement are sensitivity readings, not a revised observed dispersion",
                       "The Tolstoy selected elliptical Gaussian tracers are not authenticated full spherical virial moments",
                       "No resolved-kinematic posterior or exclusion of generic cold matter",
                       "Stock and retention are conditional model inputs; no frozen criterion modified"]}
    Path(outpath).write_text(json.dumps(result, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"n_checks": len(checks), "all_pass": result["all_checks_pass"],
                      "two_tracer": mainbound, "stock": comparisons,
                      "kernel_min_Nratios": kernel_cases}, indent=2))


if __name__ == "__main__":
    main(sys.argv[1])
