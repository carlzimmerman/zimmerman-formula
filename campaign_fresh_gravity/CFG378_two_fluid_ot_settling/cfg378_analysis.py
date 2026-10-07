#!/usr/bin/env python3
"""CFG378 analysis: frozen decision (CFG361 cuts) per rate and footing, vs CFG359 S0 256^3 (read-only); realised fraction of the ON-region
target (R, Q; R0 from the g = 0 run at the same resolution); overdraw; settling speeds; DEV 128^3 table vs the 128^3 S0 DEV run.
Frozen: FROZEN_CRITERIA.md (18bfc1a98; Amendment 1, corrected k_J)."""
import os, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); W = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg378_work"))
W9 = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg359_work"))
LOG, OUT = [], {"lane": "CFG378", "frozen": "18bfc1a98", "runs": {}, "dev": {}}
def P(s=""): print(s); LOG.append(s)
def load(t):
    p = os.path.join(W, f"cfg378_{t}.json"); return json.load(open(p)) if os.path.exists(p) else None
def ratios(s, r0, zn, key="P"):
    k, p = np.array(s[zn]["k"]), np.array(s[zn][key]); k0, p0 = np.array(r0[zn]["k"]), np.array(r0[zn]["P"]); m = k <= 1
    pr = p[m] / np.interp(k[m], k0, p0)
    return dict(s8=s[zn]["sigma8"] / r0[zn]["sigma8"], pdev=float(np.max(np.abs(pr - 1))), P=[float(np.interp(x, k[m], pr)) for x in (0.1, 0.3, 1.0)])
def cat(r):
    ds = abs(r["s8"] - 1)
    if ds > 0.20: return "FAIL"
    if ds <= 0.05 and r["pdev"] <= 0.10: return "GROWTH OK"
    return "TENSION"
def settle_stats(r):
    lg = r.get("settle_log", [])
    if not lg: return {}
    return dict(v_rms_kms_max=max(x["v_rms_kms"] for x in lg), v_max_kms=max(x["v_max_kms"] for x in lg), clip_frac_max=max(x["clip_frac"] for x in lg),
                lam_on_late=float(np.mean([x["lam_mean_on"] for x in lg[-16:]])))
def realised(r, rb):
    out = {}
    for zn in ("z1", "z0.5", "z0"):
        s = r["snap"][zn]; R, Q = s.get("R"), s.get("Q")
        R0 = rb["snap"][zn].get("R") if rb else None; Q0 = rb["snap"][zn].get("Q") if rb else None
        out[zn] = dict(R=R, Q=Q, R0=R0, Q0=Q0, share=((R - R0) / (1 - R0)) if (R is not None and R0 is not None and R0 < 1) else None,
                       cold_above=s.get("mass_on_cold_above_target"))
    return out
def fmt(x, f=".3f"): return "n/a" if x is None else format(x, f)
r0 = json.load(open(os.path.join(W9, "cfg359_S0_FLAT_canonical_N256.json")))["snap"]
P("CFG378 -- two species, Newtonian gravity, cold particles settled toward the MIX-A baryon phantom (declared scheme); ratios to S0 (CFG359 256^3) at z = 0")
verd = {}
for g in (1, 0.1, 0):
    for f in ("canonical", "alt"):
        r = load(f"TWO_g{g:g}_FLAT_{f}_N256")
        if r is None:
            P(f"  g={g:g} {f}: MISSING"); continue
        s = r["snap"]; z0 = ratios(s, r0, "z0"); c = cat(z0)
        if g > 0: verd[(g, f)] = c
        rb = load(f"TWO_g0_FLAT_{f}_N256"); base = "256^3"
        if rb is None: rb = load(f"TWO_g0_FLAT_{f}_N128_DEV"); base = "128^3 DEV (resolution-mismatched)"
        rl = realised(r, rb); ss = settle_stats(r)
        OUT["runs"][f"g{g:g}|{f}"] = dict(z0=z0, z05=ratios(s, r0, "z0.5"), z1=ratios(s, r0, "z1"), verdict=c, realised=rl, R0_base=base, settle=ss,
                                         sigma8_cold=s["z0"].get("sigma8_cold"), sigma8_bar=s["z0"].get("sigma8_bar"),
                                         mass_err_max=max(x["cold_mass_total_rel_err"] for x in s.values()), cold_min=min(x["cold_min_cic"] for x in s.values()))
        lab = "" if g > 0 else "  [g = 0 control: should equal S0]"
        P(f"  g={g:<4g}{f:9s}: s8 {z0['s8']:.4f}  max|P-1| k<=1 {z0['pdev']:.3f}  P@0.1/0.3/1 {z0['P'][0]:.3f}/{z0['P'][1]:.3f}/{z0['P'][2]:.3f} -> {c}{lab}")
        if g > 0:
            z = rl["z0"]
            P(f"        realised z0: R {fmt(z['R'])} (R0 {fmt(z['R0'])}, {base}) share of deficit {fmt(z['share'])}; Q {fmt(z['Q'])} (Q0 {fmt(z['Q0'])}); "
              f"ON mass with cold > target {fmt(z['cold_above'])}")
            P(f"        settling: v_rms max {ss['v_rms_kms_max']:.1f} km/s, v_max {ss['v_max_kms']:.0f} km/s, clipped max {ss['clip_frac_max']:.2e}, "
              f"late lambda/step {ss['lam_on_late']:.3f}; cold mass rel err max {OUT['runs'][f'g{g:g}|{f}']['mass_err_max']:.1e}, min cold CIC {OUT['runs'][f'g{g:g}|{f}']['cold_min']:.3g}")
for g, lab in ((1, "LANE VERDICT (Gamma = 1/t_dyn)"), (0.1, "Gamma = 1/(10 t_dyn)")):
    vs = [verd.get((g, f)) for f in ("canonical", "alt")]
    v = "INCOMPLETE" if None in vs else "FAIL" if "FAIL" in vs else "GROWTH OK" if all(x == "GROWTH OK" for x in vs) else "TENSION"
    OUT[f"verdict_g{g:g}"] = v; P(f"  g={g:g}: {v}  [{lab}]")
P("  compare CFG374 (bookkeeping RES R_c=3 + MIX-A, BUGGY k_J filter): s8 1.015/1.019, P(k=1) 1.124/1.156 (TENSION); CFG361 T5 1.205/1.257 (FAIL)")
P("\nDEV 128^3 (not scored; ratios to the 128^3 S0 DEV run of this engine)")
s0d = load("S0_g0_FLAT_canonical_N128_DEV")
for t in ("TWO_g0_FLAT_canonical_N128_DEV", "TWO_g0_FLAT_alt_N128_DEV", "TWO_g1_FLAT_canonical_N128_DEV", "TWO_g1_FLAT_alt_N128_DEV",
          "TWO_g0.1_FLAT_canonical_N128_DEV", "TWO_g1_FLAT_canonical_N128_DEV_MUTATE"):
    r = load(t)
    if r is None or s0d is None:
        P(f"  {t}: MISSING"); continue
    z0 = ratios(r["snap"], s0d["snap"], "z0"); s = r["snap"]["z0"]
    OUT["dev"][t] = dict(z0=z0, R=s.get("R"), Q=s.get("Q"), settle=settle_stats(r))
    P(f"  {t:40s} s8 {z0['s8']:.4f} max|P-1| {z0['pdev']:.3f} P@1 {z0['P'][2]:.3f}  R {fmt(s.get('R'))} Q {fmt(s.get('Q'))}  ({cat(z0)}, DEV)")
open(os.path.join(HERE, "cfg378_analysis.out"), "w").write("\n".join(LOG) + "\n")
json.dump(OUT, open(os.path.join(HERE, "cfg378_results.json"), "w"), indent=1)
