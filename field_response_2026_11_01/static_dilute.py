#!/usr/bin/env python3
"""Dilute controls with original fixed-mass solver and material-core metrics."""
import json
import math
import resource
import sys
import traceback
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
import static_response as original


def density(sol, r):
    psi, _, ss, _ = sol.sol(r)
    return np.maximum(psi, 0.0)**1.5*np.exp(3*ss)


def enclosed_mass(sol, r, edge):
    return quad(lambda x: x*x*float(density(sol, x)), 0, min(r, edge),
                epsabs=2e-9, epsrel=2e-9, limit=600)[0]


def core_diagnostics(baseline, core_mass, row, sol, mb, a):
    """Track the original core's mass separately from a moving density threshold."""
    rq0 = baseline["quarter_radius"]
    edge = row["radius"]
    inside_original_radius = enclosed_mass(sol, rq0, edge)
    rmaterial = brentq(lambda r: enclosed_mass(sol, r, edge) - core_mass,
                       0, edge, xtol=1e-12)
    material_mass = enclosed_mass(sol, rmaterial, edge)

    def slope_mass(r):
        return -r*r*float(sol.sol(r)[1]) - float(original.plummer(r, mb, a)[2])

    # rq0 is interior to all allowed numerical domains; matter may end earlier.
    mass_fixed_error = abs(slope_mass(rq0)/inside_original_radius - 1)
    mass_material_error = abs(slope_mass(rmaterial)/material_mass - 1)
    target_error = abs(material_mass/core_mass - 1)
    mass_ratio = inside_original_radius/core_mass
    radius_ratio = rmaterial/rq0
    checks = {"fixed_original_core_radius_mass": mass_fixed_error < 2e-5,
              "material_core_radius_mass": mass_material_error < 2e-5,
              "material_core_mass_target": target_error < 2e-5,
              "material_core_radius_inside_halo": 0 < rmaterial < edge}
    if mb == 0:
        checks["zero_forcing_material_core"] = max(abs(mass_ratio - 1), abs(radius_ratio - 1)) < 5e-5
    return {"original_quarter_radius": rq0, "original_core_dark_mass": core_mass,
            "dark_mass_inside_original_quarter_radius": inside_original_radius,
            "enclosed_core_mass_ratio": mass_ratio,
            "radius_containing_original_core_mass": rmaterial,
            "material_core_radius_ratio": radius_ratio,
            "fixed_original_radius_mass_relative_error": mass_fixed_error,
            "material_radius_mass_relative_error": mass_material_error,
            "material_mass_target_relative_error": target_error,
            "checks": {k: bool(v) for k, v in checks.items()},
            "passed": bool(all(checks.values()))}


def serializable(value):
    nonfinite = {}

    def clean(item, path):
        if isinstance(item, dict):
            return {key: clean(val, path + "." + str(key)) for key, val in item.items()}
        if isinstance(item, (list, tuple)):
            return [clean(val, path + "[" + str(i) + "]") for i, val in enumerate(item)]
        if isinstance(item, float) and not math.isfinite(item):
            nonfinite[path] = repr(item)
            return None
        return item
    out = clean(value, "$")
    out["nonfinite_diagnostics_replaced_by_null"] = nonfinite
    return out


def main():
    output = Path(sys.argv[1])
    frozen = original.load_baseline()
    baselines, rows, profiles = [], [], {}
    plummer_controls = original.plummer_controls()
    eps = 0.01

    def profile(label, row, sol):
        rr = np.linspace(0, row["outer_radius"], 400)
        profiles[label] = np.vstack((rr, sol.sol(rr)))

    for pc in (0.2, 0.4, 0.6):
        auxiliary, guess = frozen.local_solution(pc)
        baseline, base_sol = frozen.solve_case(pc, eps, auxiliary, guess)
        core_mass = enclosed_mass(base_sol, baseline["quarter_radius"], baseline["radius"])
        baseline["original_core_dark_mass"] = core_mass
        baselines.append(baseline)
        for family, (mass_ratio, radius_ratio) in original.FAMILIES.items():
            label = f"p{pc}_e{eps}_{family}"
            final_mb = mass_ratio*baseline["mass_dimensionless"]
            a = radius_ratio*baseline["radius"]
            previous = base_sol
            stopped = not baseline.get("passed", False)
            last_success = None
            for index in range(41):
                fraction = index/40
                meta = {"baseline_psi_c": pc, "epsilon": eps, "family": family,
                        "fraction": fraction, "continuation_index": index}
                if stopped:
                    rows.append(dict(meta, passed=False, not_attempted="previous step or baseline failed"))
                    continue
                try:
                    row, sol = original.solve_response(baseline, eps, fraction*final_mb, a, previous.sol)
                    row.update(meta)
                    if row["passed"]:
                        core = core_diagnostics(baseline, core_mass, row, sol, fraction*final_mb, a)
                        row["material_core"] = core
                        row["checks"]["material_core_checks"] = core["passed"]
                        row["passed"] = bool(row["passed"] and core["passed"])
                    if row["passed"]:
                        previous = sol
                        last_success = (row, sol)
                        if index % 10 == 0:
                            profile(label + f"_f{fraction}", row, sol)
                    else:
                        stopped = True
                except Exception as exc:
                    row = dict(meta, passed=False, exception=repr(exc), traceback=traceback.format_exc())
                    stopped = True
                rows.append(row)
                if index % 10 == 0 or not row["passed"]:
                    summary = {key: row.get(key) for key in (
                        "baseline_psi_c", "epsilon", "family", "fraction", "passed",
                        "solver_status", "psi_c", "ratios_to_baseline", "exception")}
                    if "material_core" in row:
                        summary["material_core"] = {key: row["material_core"][key] for key in (
                            "enclosed_core_mass_ratio", "material_core_radius_ratio")}
                    print(json.dumps(serializable(summary)), flush=True)
            if stopped and last_success is not None:
                profile(label + "_last_success", *last_success)
    checks = {"three_baselines": len(baselines) == 3 and all(x.get("passed", False) for x in baselines),
              "plummer_controls": plummer_controls["passed"],
              "all_246_records": len(rows) == 246,
              "all_responses_verified": all(x.get("passed", False) for x in rows),
              "all_successful_material_core_checks": all(x["material_core"]["passed"] for x in rows if x.get("passed"))}
    result = {"claim_id": "FR01_STATIC_DILUTE", "checks": checks,
              "plummer_controls": plummer_controls, "baselines": baselines, "cases": rows,
              "peak_rss_bytes_macos": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              "scope": "Dilute controls and fixed original dark-core mass response; no stability or kinetic-accessibility assertion."}
    output.write_text(json.dumps(serializable(result), indent=2, sort_keys=True, allow_nan=False) + "\n")
    np.savez_compressed(output.with_name("profiles.npz"), **profiles)
    print(json.dumps(checks, sort_keys=True), flush=True)
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
