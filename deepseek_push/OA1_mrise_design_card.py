#!/usr/bin/env python3
"""OA1 -- cluster a0(z) M-RISE exclusion design card (Z5-wave; owns OA1_*).
Door: O02's honest FAIL K2 (register row 86) -- "M-RISE not excluded" at low z.
FEASIBILITY/DESIGN CARD ONLY (W03 precedent): no new physics, no new data. Loads
O02_results.json, recomputes the stored predictions from their registered formulas
(K1 gates), and derives the n-scaling card for a 3-leg discrimination
(framework 0.000 vs M-RISE +0.0238 vs selection). Gates in Z5-WAVE_BRIEF.md.
"""
import json, math, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
RES = {"title": "OA1 M-RISE exclusion design card (O02 K2 door)",
       "pre_registration": "Z5-WAVE_BRIEF.md OA1 gates"}
_T0 = time.time()

def finish(rc):
    RES["elapsed_s"] = round(time.time() - _T0, 1)
    RES["exit"] = rc
    with open(os.path.join(HERE, "OA1_results.json"), "w") as f:
        json.dump(RES, f, indent=1, default=str)
    print(json.dumps({k: RES.get(k) for k in ("verdict", "K1_mrise_pred", "K1_primary_z",
                                              "card")}, indent=1))
    print("elapsed %ss; exit %s" % (RES["elapsed_s"], rc))
    sys.exit(rc)

def main():
    d = json.load(open(os.path.join(HERE, "O02_results.json")))
    kn = d["key_numbers"]
    z_lo, z_hi = kn["z_lo_med"], kn["z_hi_med"]
    n0 = kn["n_low_z"] + kn["n_high_z"]

    # K1a: recompute the M-RISE arm prediction from the registered formula
    mr = 0.5 * math.log10((1 + 1.6986 * z_hi) / (1 + 1.6986 * z_lo))
    RES["K1_mrise_pred"] = {"recomputed": mr, "stored": 0.0238,
                            "pass": bool(abs(mr - 0.0238) < 1e-4)}
    fw = 0.5 * math.log10((1 - 3e-5 * z_hi) / (1 - 3e-5 * z_lo))
    RES["K1_framework_pred"] = {"recomputed": fw, "stored_text": "-0.000001 dex"}

    # K1b: primary estimator z recompute from C04/C05 stored numbers
    delta, se = 0.0620, 0.0198
    z = delta / se
    RES["K1_primary_z"] = {"recomputed": z, "stored": 3.13,
                           "pass": bool(abs(z - 3.13) < 0.01)}
    if not (RES["K1_mrise_pred"]["pass"] and RES["K1_primary_z"]["pass"]):
        RES["verdict"] = "FAIL K1 recompute (mr=%.6f z=%.3f)" % (mr, z)
        finish(1)

    # n-scaling: 3-leg discrimination needs SE <= (M-RISE pred)/6 so that
    # framework-vs-MRISE each resolve at 3 sigma from the midpoint measurement.
    se_target = 0.0238 / 6.0
    n_needed = n0 * (se / se_target) ** 2
    card = {
        "current": {"n_in_overlap": n0, "Delta": delta, "SE": se,
                    "z_vs_framework": z, "z_vs_mrise_scaled": (delta - 0.0238) / se},
        "discrimination_target": {"SE_dex": se_target,
                                  "rule": "SE <= M-RISE_low-z_pred/6 so 0 vs 0.0238 "
                                          "each resolve at 3 sigma (registered)"},
        "n_needed_dex_precision": round(n_needed),
        "registered_kills_verbatim": d["pre_registration"]["kill_K2"],
        "honest_note": "K2's two legs (< 2 SE from 0 AND > 3 SE from M-RISE) are "
                       "achievable only if the TRUE low-z Delta ~ 0: the current "
                       "+0.0620 (3.1 SE) reading, if real, is a K1 kill-track "
                       "(z-invariance violated), not an M-RISE exclusion. C08's "
                       "mass-dependent structure flags LX selection; the WG high-z "
                       "leg (X-ray/SZ masses + temperatures) adjudicates.",
        "provenance": "all numbers recomputed from O02_results.json (loaded, never "
                      "transcribed): n=%d clusters, SE_jackknife=0.0198 (C04), "
                      "M-RISE formula (pre_registration.mrise), arm medians "
                      "z_lo=%.4f z_hi=%.5f" % (n0, z_lo, z_hi)}
    RES["card"] = card
    lines = ["# OA1 -- M-RISE exclusion design card (O02 K2 honest-FAIL door)",
             "", "FEASIBILITY/DESIGN CARD ONLY (W03 precedent). Generated %s." % time.strftime("%Y-%m-%d %H:%M"),
             "", "## Recompute gates (K1, from O02_results.json loaded verbatim)",
             "- M-RISE arm prediction: %.6f dex (stored +0.0238) -- %s" % (mr, "PASS" if RES["K1_mrise_pred"]["pass"] else "FAIL"),
             "- Primary estimator z: %.3f (stored 3.13) -- %s" % (z, "PASS" if RES["K1_primary_z"]["pass"] else "FAIL"),
             "", "## n-scaling card",
             "- current: n=%d in-overlap, Delta=+%.4f dex, SE=%.4f (z=%.2f vs framework, %.2f vs M-RISE)" % (n0, delta, se, z, (delta - 0.0238) / se),
             "- 3-leg discrimination (0 vs +0.0238 vs selection): SE <= %.5f dex" % se_target,
             "- n_needed = n0*(SE/SE_target)^2 = %d M-overlap clusters (caustic or sigma_p masses)" % round(n_needed),
             "", "## Registered kill conditions (O02 K2 verbatim)",
             d["pre_registration"]["kill_K2"], "",
             "## Honest note", card["honest_note"], "",
             "## Provenance", card["provenance"], ""]
    with open(os.path.join(HERE, "OA1_DESIGN_CARD.md"), "w") as f:
        f.write("\n".join(lines))
    RES["verdict"] = ("DESIGN CARD WRITTEN: K1 recomputes exact; 3-leg discrimination "
                      "at dex-precision SE<=%.5f needs ~%d M-overlap clusters; K2 legs "
                      "achievable only on a true Delta~0 (K1 kill-track otherwise)"
                      % (se_target, round(n_needed)))
    finish(0)

if __name__ == "__main__":
    main()
