#!/usr/bin/env python3
"""X76: apply the frozen verdict (FROZEN_CRITERIA.md, 5775b7d6b3) to the committed JSONs; writes x76_summary.json.
kappa = 1/2 FITTED; c_f EXTERNAL; not theory closed.      python3 -I x76_summary.py
"""
import os, json
H = os.path.dirname(os.path.abspath(__file__)); J = lambda f: json.load(open(os.path.join(H, f)))
L, S, P = J("x76_lensing_grade_fair.json"), J("x76_sat_results.json"), J("x76_lens_profile_results.json")
K1 = J("x76_lensing_grade_sparc.json")["K1"]
out = {"criteria": "5775b7d6b3", "K1_sparc_identity": K1, "K2_rta": S["x76"]["K2"], "K3_mass": S["x76"]["K3"], "mutate_lens_m1_up": P["mutate_m1_up"], "footings": {}}
for f in ("canonical", "alt"):
    s = S["footings"][f]; lab = L[f"{f}|all"]
    sat_ok = abs(s["D"]) < 2 * max(s["sD"], 1e-3); lens_ok = lab["dchi2"] < lab["sparc"]
    m_lens = P["footings"][f]["truncated"]["all"]["common_shift"]
    v = "FAIR SHARE SUPPLIES THE MASS" if (sat_ok and lens_ok) else f"FAIR SHARE FALLS SHORT: needs m = {s['D']:+.2f} (satellites), {m_lens:+.2f} (lensing, all radii)"
    out["footings"][f] = dict(verdict=v, sat_m=s["D"], sat_range=[s["lo"], s["hi"]], sat_chi2_m0=s["chi2_H0"], sat_chi2_best=s["chi2_min"],
                              lens_dchi2_fair=lab["dchi2"], lens_dchi2_sparc=lab["sparc"], lens_m_all=m_lens,
                              lens_m_primary=P["footings"][f]["truncated"]["primary"]["common_shift"])
    print(f"[{f}] {v}; satellites chi2 at m=0 {s['chi2_H0']:.1f}; lensing dchi2 {lab['dchi2']:+.1f} vs SPARC {lab['sparc']:+.1f}")
ok = K1 <= 1e-9 and out["K2_rta"] < 1e-12 and out["K3_mass"] < 1e-8 and out["mutate_lens_m1_up"]
out["checks_pass"] = ok; json.dump(out, open(os.path.join(H, "x76_summary.json"), "w"), indent=1)
raise SystemExit(0 if ok else 1)
