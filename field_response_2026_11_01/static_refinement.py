#!/usr/bin/env python3
"""Frozen .025-step continuation using unchanged original static equations."""
import json
import math
import resource
import sys
import traceback
from pathlib import Path

import numpy as np
import static_response as original


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
    reference = json.loads((original.ROOT / "static_run_002/result.json").read_text())
    coarse = {(r["baseline_psi_c"], r["epsilon"], r["family"], r["fraction"]): r
              for r in reference["cases"]}
    frozen = original.load_baseline()
    baselines, rows, comparisons, refinements, profiles = [], [], [], [], {}
    plummer = original.plummer_controls()

    def profile(label, row, sol):
        rr = np.linspace(0, row["outer_radius"], 400)
        profiles[label] = np.vstack((rr, sol.sol(rr)))

    for pc in (0.8, 0.95, 0.99):
        auxiliary, initial_guess = frozen.local_solution(pc)
        for eps in (1e-4, 1e-2):
            base, base_sol = frozen.solve_case(pc, eps, auxiliary, initial_guess)
            baselines.append(base)
            for family, (mass_ratio, radius_ratio) in original.FAMILIES.items():
                label = f"p{pc}_e{eps}_{family}"
                final_mb = mass_ratio*base.get("mass_dimensionless", 0)
                a = radius_ratio*base.get("radius", 0)
                previous = base_sol
                stopped = not base.get("passed", False)
                endpoint = None
                last_success = None
                for index in range(41):
                    fraction = index/40
                    meta = {"baseline_psi_c": pc, "epsilon": eps, "family": family,
                            "fraction": fraction, "continuation_index": index}
                    if stopped:
                        rows.append(dict(meta, passed=False, not_attempted="previous step or baseline failed"))
                        continue
                    try:
                        row, sol = original.solve_response(base, eps, fraction*final_mb, a, previous.sol)
                        row.update(meta)
                        if row["passed"]:
                            previous = sol
                            last_success = (row, sol)
                            if index % 10 == 0:
                                profile(label + f"_f{fraction}", row, sol)
                            if index == 40:
                                endpoint = (row, sol)
                            old = coarse.get((pc, eps, family, fraction))
                            if old is not None and old.get("passed", False):
                                keys = ("radius", "density_c", "core_column_coefficient")
                                changes = {key: abs(row[key]/old[key] - 1) for key in keys}
                                comparisons.append(dict(meta, relative_differences=changes,
                                                        passed=max(changes.values()) < 5e-5))
                        else:
                            stopped = True
                    except Exception as exc:
                        row = dict(meta, passed=False, exception=repr(exc), traceback=traceback.format_exc())
                        stopped = True
                    rows.append(row)
                    if index % 10 == 0 or not row["passed"]:
                        print(json.dumps(serializable({key: row.get(key) for key in (
                            "baseline_psi_c", "epsilon", "family", "fraction", "passed",
                            "solver_status", "psi_c", "ratios_to_baseline", "exception")})), flush=True)
                if stopped and last_success is not None:
                    profile(label + "_last_success", *last_success)
                if pc == 0.99:
                    meta = {"baseline_psi_c": pc, "epsilon": eps, "family": family, "fraction": 1.0}
                    if endpoint is None:
                        refinements.append(dict(meta, passed=False, not_attempted="main endpoint unavailable"))
                        continue
                    old_row, old_sol = endpoint
                    try:
                        extended = original.exterior_guess(old_sol, base["mass_dimensionless"], final_mb, a, eps)
                        fine, fine_sol = original.solve_response(base, eps, final_mb, a, extended,
                            refine=True, auxiliary_radius=auxiliary["radius"])
                        fine.update(meta)
                        keys = ("radius", "density_c", "core_column_coefficient")
                        fine["relative_changes_from_main"] = {
                            key: abs(fine[key]/old_row[key] - 1) for key in keys} if fine["passed"] else {}
                        fine["domain_and_tolerance_check"] = bool(fine["passed"] and
                            max(fine["relative_changes_from_main"].values()) < 5e-5)
                        if fine_sol.success:
                            profile(label + "_refined", fine, fine_sol)
                    except Exception as exc:
                        fine = dict(meta, passed=False, domain_and_tolerance_check=False,
                                    exception=repr(exc), traceback=traceback.format_exc())
                    refinements.append(fine)
    checks = {
        "plummer_controls": plummer["passed"],
        "six_baselines": len(baselines) == 6 and all(x.get("passed", False) for x in baselines),
        "all_492_records": len(rows) == 492,
        "all_responses_verified": all(x.get("passed", False) for x in rows),
        "all_available_coarse_comparisons_consistent": all(x["passed"] for x in comparisons),
        "four_refinement_records": len(refinements) == 4,
        "all_refinements_verified": len(refinements) == 4 and all(
            x.get("domain_and_tolerance_check", False) for x in refinements),
    }
    result = {"claim_id": "FR01_STATIC_A2", "checks": checks, "plummer_controls": plummer,
              "baselines": baselines, "cases": rows, "coarse_comparisons": comparisons,
              "refinements": refinements,
              "peak_rss_bytes_macos": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              "scope": "Frozen smaller-step numerical continuation; no stability, formation or physical branch selection claim."}
    output.write_text(json.dumps(serializable(result), indent=2, sort_keys=True, allow_nan=False) + "\n")
    np.savez_compressed(output.with_name("profiles.npz"), **profiles)
    print(json.dumps(checks, sort_keys=True), flush=True)
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
