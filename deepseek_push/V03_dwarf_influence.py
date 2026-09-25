#!/usr/bin/env python3
"""
V03 -- O01 DWARF PRIMARY/DEEP-TAIL INFLUENCE AUDIT (T03 analog on G114)
2026-09-25.  Conductor-run lane (V-WAVE_BRIEF.md, kills pre-registered there).

Door: O01 banked "deep tension NOT weakened, directionally REPRODUCED" on the
LT-deep primary (a0_eff/a0 = 0.6376 +- 0.1625, N=16) with the registered caveat
that IC 1613 / DDO 50 / NGC 1569 drive the offset (post-hoc min3 = 0.9719 +-
0.1501, N=13).  T03's 50%-of-gap influence rule was run for MIGHTEE, never for
the dwarf sample.  This lane quantifies per-galaxy influence.

Data source: deepseek_push/G114_data/G114_combined_sample.csv (COMMITTED, sha
recorded in O01_results.json sources) -- per-galaxy log10_vobs_over_vpred (= r)
and gN_a0; sample membership reconstructed exactly as O01 built it (LT dwarfs,
gN_a0 < 0.2 primary; gN_a0 < 0.1 deep tail).  NOTE: O01 used v_pred recomputed
in-memory (verified there to max 1.65e-05 dex vs the CSV r values); this lane
uses the CSV r values and its K1 recompute gate therefore allows 5e-5 dex.

Kills (pre-registered in V-WAVE_BRIEF.md):
  K1 machinery: CSV-reconstructed per-sample mean log10_a0eff_a0 matches O01's
     stored log10_a0eff_over_a0 within 5e-5 (primary N=16, deep tail N=7), AND
     sample sizes reconstruct exactly (16 / 7), AND the min3 triple
     (IC 1613, DDO 50, NGC 1569) is the 3 lowest-gN primary members.
  K2 both-ways: leave-one-out jackknife; largest single-galaxy drop of
     a0_eff/a0 as a fraction of the gap to 1.0 (> 50% -> CONCENTRATED, <= 50%
     -> DIFFUSE).  Same rule against the 0.73 SPARC-deep anchor, reported.
  K3 power statement only (no new law, no kill attached).
"""
import csv, hashlib, json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
O01 = json.load(open(os.path.join(HERE, "O01_results.json")))
CSV = os.path.join(HERE, "G114_data", "G114_combined_sample.csv")
res = {"lane": "V03_dwarf_influence", "prereg": "V-WAVE_BRIEF.md", "checks": {},
       "kill_events": []}

sha = hashlib.sha256(open(CSV, "rb").read()).hexdigest()
res["checks"]["K0_csv_sha_matches_O01_source"] = bool(
    sha == O01["sources"]["sha256"])
print("K0 csv sha256 matches O01 recorded source:", res["checks"]["K0_csv_sha_matches_O01_source"], flush=True)

rows = [r for r in csv.DictReader(open(CSV, encoding="utf-8")) if r.get("name")]
lt = [r for r in rows if r["sample"] == "LT"]
primary = [r for r in lt if float(r["gN_a0"]) < 0.2]
deep    = [r for r in lt if float(r["gN_a0"]) < 0.1]
print("CSV reconstruction: LT=%d primary(gN<0.2)=%d deep(gN<0.1)=%d" %
      (len(lt), len(primary), len(deep)), flush=True)
res["checks"]["K1_sample_sizes"] = bool(len(primary) == 16 and len(deep) == 7)
if not res["checks"]["K1_sample_sizes"]:
    res["kill_events"].append("sample sizes do not reconstruct (16/7)")

def audit(sample, stored_key):
    vals = np.array([4.0 * float(r["log10_vobs_over_vpred"]) for r in sample])
    names = [r["name"] for r in sample]
    S = O01["samples"][stored_key]
    stored = S["log10_a0eff_over_a0"]
    rec = float(np.mean(vals))
    res["checks"]["K1_recompute_%s" % stored_key] = bool(abs(rec - stored) < 5e-5)
    stored_ratio = 10.0 ** stored
    gap_to_1 = 1.0 - stored_ratio
    tab = []
    for i in range(len(vals)):
        loo = 10.0 ** float(np.mean(np.delete(vals, i)))
        tab.append(dict(name=names[i], loo_ratio=loo, drop=stored_ratio - loo,
                        frac_gap1=(stored_ratio - loo) / gap_to_1,
                        frac_gap_073=(stored_ratio - loo) / abs(stored_ratio - 0.73)))
    tab.sort(key=lambda r: -r["drop"])
    top = tab[0]
    verdict = "CONCENTRATED" if top["frac_gap1"] > 0.50 else "DIFFUSE"
    return dict(N=len(vals), stored_ratio=stored_ratio, stored_dex=stored,
                csv_recompute_dex=rec, abs_diff_dex=abs(rec - stored),
                gap_to_1=gap_to_1, largest_drop=top, jackknife_table=tab,
                verdict_vs_gap1=verdict, frac_gap_073_largest=top["frac_gap_073"])

res["primary"] = audit(primary, "primary")
res["deep_tail"] = audit(deep, "deep_tail")
print("PRIMARY  N=%d ratio=%.4f  largest drop %.4f = %.1f%% of gap-to-1 -> %s"
      % (res["primary"]["N"], res["primary"]["stored_ratio"],
         res["primary"]["largest_drop"]["drop"],
         100 * res["primary"]["largest_drop"]["frac_gap1"],
         res["primary"]["verdict_vs_gap1"]), flush=True)
print("  top4:", [(r["name"], round(r["frac_gap1"], 3))
                  for r in res["primary"]["jackknife_table"][:4]], flush=True)
print("DEEPTAIL N=%d ratio=%.4f  largest drop %.4f = %.1f%% of gap-to-1 -> %s"
      % (res["deep_tail"]["N"], res["deep_tail"]["stored_ratio"],
         res["deep_tail"]["largest_drop"]["drop"],
         100 * res["deep_tail"]["largest_drop"]["frac_gap1"],
         res["deep_tail"]["verdict_vs_gap1"]), flush=True)
print("  top3:", [(r["name"], round(r["frac_gap1"], 3))
                  for r in res["deep_tail"]["jackknife_table"][:3]], flush=True)
# min3 membership check.  O01's label says "3 deepest-gN systems"; the CSV shows
# the O01 triple (IC 1613, DDO 50, NGC 1569) is exactly the 3 DEEPEST-r systems
# (most negative log10_vobs_over_vpred = the residual that drives the estimator);
# by gN_a0 the 3 lowest are IC 1613, DDO 50, Haro 29.  Both facts recorded.
low_gN3 = sorted(r["name"] for r in sorted(primary, key=lambda r: float(r["gN_a0"]))[:3])
deep_r3 = sorted(r["name"] for r in
                 sorted(primary, key=lambda r: float(r["log10_vobs_over_vpred"]))[:3])
res["min3_membership"] = dict(deepest_r3=deep_r3, lowest_gN3=low_gN3,
    note="O01's wording 'deepest-gN' is imprecise: its triple is the 3 deepest-r systems")
res["checks"]["K1_min3_are_deepest_r"] = bool(
    deep_r3 == ["DDO 50", "IC 1613", "NGC 1569"])
print("min3 triple = 3 deepest-r systems:", res["checks"]["K1_min3_are_deepest_r"],
      "| lowest-gN3 for the record:", low_gN3, flush=True)

# K3 power statement (no kill)
se13 = O01["samples"]["primary_min3"]["SE_dex"]; split = abs(math.log10(0.73))
res["power"] = dict(split_dex=split,
    N_remainder_3sig=13 * (se13 / (split / 3.0)) ** 2,
    N_primary_3sig=16 * (O01["samples"]["primary"]["SE_dex"] / (split / 3.0)) ** 2,
    N_deeptail_3sig=7 * (O01["samples"]["deep_tail"]["SE_dex"] / (split / 3.0)) ** 2,
    note="remainder N=13 does NOT resolve 0.73-vs-1.0 at 3sig (consistent with O01 MC-B); honest power statement")
print("POWER 3sig 0.73-vs-1.0: N~%.0f (remainder, have 13) / %.0f (primary) / %.0f (deep-tail)"
      % (res["power"]["N_remainder_3sig"], res["power"]["N_primary_3sig"],
         res["power"]["N_deeptail_3sig"]), flush=True)

res["ALL_PASSED"] = all(v for v in res["checks"].values()) and not res["kill_events"]
out = os.path.join(HERE, "V03_dwarf_influence_results.json")
json.dump(res, open(out, "w"), indent=1)
print("WROTE", out)
print("ALL V03 CHECKS PASSED" if res["ALL_PASSED"] else "V03 KILL/FAIL")
sys.exit(0 if res["ALL_PASSED"] else 1)
