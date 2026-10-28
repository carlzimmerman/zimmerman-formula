#!/usr/bin/env python3
"""Read stored grades; independently evaluate the declared SPARC conjunction."""
import argparse
import collections
import json
import pathlib
import resource
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
REB = ROOT / "rebuild_2026_10_22"
SOURCES = {
    "CF1": "CF1_cf_window_map/cf1_window_results.json",
    "CF2": "CF2_decoupled_threshold_map/cf2_decoupled_results.json",
    "CL1": "CL1_combined_threshold_budget/cl1_combined_results.json",
    "CL2": "CL2_native_cf_slope/cl2_native_slope_results.json",
    "CL3": "CL3_one_number/cl3_one_number_results.json",
}


def read(path):
    return json.loads((REB / path).read_text())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=pathlib.Path, required=True)
    parser.add_argument("--mutate", action="store_true")
    args = parser.parse_args()
    checks, census, rows = {}, {}, []
    lee = read("LEE1_look_elsewhere/lee1_results.json")
    for lane, path in SOURCES.items():
        data = read(path)
        # Enumerate every top-level grade-bearing object, independently of LEE1's
        # lane-name predicates. Exclude metadata rather than assume grid counts.
        grades = [(k, v["grade"]) for k, v in data.items()
                  if isinstance(v, dict) and "grade" in v]
        census[lane] = {"n": len(grades)}
        for foot in ("canonical", "alt"):
            census[lane]["pass_" + foot] = sum(not g[foot]["fails"] for _, g in grades)
        checks["census_" + lane] = census[lane] == lee["census"][lane]
        if lane == "CL3":
            rows.extend((lane + ":" + key, grade) for key, grade in grades)

    bs = read("BS1_basin_switch/bs1_basin_switch_results.json")
    rows.append(("BS1:primary", bs["primary"]["grade"]))
    lo = 0.40 if args.mutate else 0.50
    sparc = []
    for label, grade in rows:
        for foot in ("canonical", "alt"):
            for bg, st in grade[foot]["sparc"].items():
                residual_ok = st["rms"] <= 0.110
                calibration_ok = lo <= st["U"] <= 0.80
                ok = residual_ok and calibration_ok
                key = label + ":" + foot + ":" + bg
                checks["gate:" + key] = ok == st["line"]
                sparc.append(dict(configuration=label, footing=foot, background=bg,
                                  rms=st["rms"], median_U=st["U"],
                                  residual_ok=residual_ok, calibration_ok=calibration_ok,
                                  recomputed_line=ok, stored_line=st["line"]))
    draws = lee["partB"]
    checks["draw_count"] = len(draws) == len(lee["draws"]) == 24
    for i, row in enumerate(draws):
        for foot in ("canonical", "alt"):
            checks["draw_flags:%s:%s" % (i, foot)] = row["pass_" + foot] == (not row["fails_" + foot])
    alt_failures = collections.Counter(f.split(" (")[0] for row in draws for f in row["fails_alt"])
    checks["alt_independent_lines_present"] = all(
        any(f == "SPARC line" for f in row["fails_alt"]) and
        any(f.startswith("dwarfs MW ultra-faint") for f in row["fails_alt"])
        for row in draws)
    combined = {
        "configuration_evaluations": sum(x["n"] for x in census.values()) + len(draws),
        "canonical_pass": sum(x["pass_canonical"] for x in census.values()) + sum(r["pass_canonical"] for r in draws),
        "alt_pass": sum(x["pass_alt"] for x in census.values()) + sum(r["pass_alt"] for r in draws),
    }
    result = dict(mutate=args.mutate, gate_lower_bound=lo, census=census,
                  combined=combined, draw_alt_failure_lines=dict(alt_failures),
                  sparc=sparc, checks=checks,
                  scope="Stored-output and gate audit; no raw-data refit; configurations are dependent.",
                  peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == "darwin" else 1024))
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    for name, ok in checks.items():
        print(name, "PASS" if ok else "FAIL")
    print("Counts:", combined)
    print("FOOTING AUDIT COMPLETE: %d/%d checks PASS." % (sum(checks.values()), len(checks)))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
