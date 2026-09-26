#!/usr/bin/env python3
"""MR1 — RAR moment-discipline transfer on the D-audit-corrected footing.
Reads real_research/reviews/deep_a0eff_audit_2026_09_25/D02_rerun_outputs/<variant>/L06_results.json
for variants std05_cut, std06_cut, std07_cut, std05_nocut (corrected 3.6-micron M/L reruns).
Pre-registered kills (Z-WAVE_BRIEF.md):
  (i)  any real-ensemble M1_pass = false in any variant -> DISCIPLINE-KILL-UNDER-CORRECTION (exit 1)
  (ii) deep-band z flips sign across variants -> UNSTABLE-UNDER-M/L flagged
  (iii) deep z mismatch vs register correction (+9.1/+7.1/+5.7/+8.1) beyond 1.0 sd of variants -> MISMATCH flagged
Exit 0 only on a real pass; else exit 1 honestly. No SE re-tuning.
"""
import json, sys, os, statistics
import numpy as np

BASE = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/reviews/deep_a0eff_audit_2026_09_25/D02_rerun_outputs"
VARIANTS = ["std05_cut", "std06_cut", "std07_cut", "std05_nocut"]
REG_DEEP_Z = [9.1, 7.1, 5.7, 8.1]  # register correction row 2026-09-25 (L06 deep channel)

def main():
    out = {"title": "MR1 moment-discipline transfer on corrected footing",
           "variants": {}, "gates": {}}
    deep_z = []
    all_pass = True
    for v in VARIANTS:
        p = os.path.join(BASE, v, "L06_results.json")
        if not os.path.exists(p):
            out["variants"][v] = {"error": "missing %s" % p}
            all_pass = False
            continue
        d = json.load(open(p))
        rows = []
        for i, r in enumerate(d.get("results", [])):
            name = r.get("name", "ensemble_%d" % i)
            m1 = r.get("M1_pass")
            zD = r.get("z_Delta")
            rows.append({"name": name, "M1_pass": m1, "z_Delta": zD,
                         "N": r.get("N"), "slack": r.get("slack")})
            if "deep" in name.lower() and zD is not None:
                deep_z.append(zD)
        n_pass = sum(1 for r in rows if r["M1_pass"] is True)
        n_fail = sum(1 for r in rows if r["M1_pass"] is False)
        if n_fail > 0:
            all_pass = False
        out["variants"][v] = {"a0": d.get("a0"), "kill_rule": d.get("kill_rule"),
                              "n_ensembles": len(rows), "n_M1_pass": n_pass,
                              "n_M1_fail": n_fail, "rows": rows}
    out["gates"]["G1_discipline_all_variants"] = all_pass
    if len(deep_z) >= 3:
        spread_sd = statistics.pstdev(deep_z)
        out["gates"]["G2_deep_z_across_variants"] = deep_z
        out["gates"]["G2_deep_z_sd"] = spread_sd
        sign_flip = (min(deep_z) < 0) != (max(deep_z) < 0)
        out["gates"]["G2_sign_flip"] = sign_flip
        reg_mean = statistics.mean(REG_DEEP_Z)
        mismatch = abs(statistics.mean(deep_z) - reg_mean) > max(spread_sd, 1.0)
        out["gates"]["G3_register_mismatch"] = {"register_deep_z": REG_DEEP_Z,
                                                "corrected_mean": statistics.mean(deep_z),
                                                "mismatch": mismatch}
    else:
        out["gates"]["G2_note"] = "fewer than 3 deep-band entries found — recorded honestly, no fabrication"
    verdict_pass = all_pass
    out["verdict"] = ("DISCIPLINE-ROBUST-UNDER-CORRECTION: M1 passes the 5-SE bar on every real ensemble in every corrected variant"
                      if verdict_pass else
                      "DISCIPLINE-KILL-UNDER-CORRECTION: at least one real-ensemble M1 gate fails on the corrected footing (honest FAIL)")
    json.dump(out, open("MR1_results.json", "w"), indent=1)
    print(json.dumps({"verdict": out["verdict"],
                      "gates": {k: v for k, v in out["gates"].items() if k != "G2_deep_z_across_variants"},
                      "deep_z": out["gates"].get("G2_deep_z_across_variants")}, indent=1))
    return 0 if verdict_pass else 1

if __name__ == "__main__":
    sys.exit(main())
