#!/usr/bin/env python3
"""
Comparison with Alcock, arXiv:2609.38796 (30 Sep 2026), "Is the acceleration scale of the
radial acceleration relation tracking the cosmic expansion rate?"

Alcock fits a0(z) = A (1+z)^gamma to the MUSE-DARK III (Ciocan et al., arXiv:2604.22613,
A&A 709 L16) binned a0 values (read off the paper's Fig. 3) and reports gamma = 0.78 +- 0.15,
gamma = 0 excluded at 5.3 sigma, a0 ~ H(z) (gamma_eff ~ 1.10) preferred, and states that the
exponent is invariant under redshift-INDEPENDENT rescalings of a0 (common-mode M* systematics).

This script puts the numbers this repository already holds next to those claims. No new data,
no downloads. Inputs:
  data_assembly/arxiv_tables/musedark_II_III/musedarkIII_stated_results_NOT_A_TABLE.csv
  campaign_fresh_gravity/CFG262_musedark_zthirds_by_route/cfg262_stageB_results.json

Checks:
  A. effective exponent implied by each of MUSE-DARK III's OWN three mass routes (DC14 halo,
     per-galaxy best LCDM halo, MOND refit) over the survey range 0.33 < z < 1.44;
  B. the binned endpoints 1.99 -> 2.71 under a bracket of bin-centre assumptions (the paper
     prints neither bin edges nor middle-bin values);
  C. the H(z) effective exponent over the same range (Alcock quotes ~1.10);
  D. CFG262 (this repo, 10-01): z-thirds by baryon route, third3 - third1 against flat, the
     H(z) rival, and Alcock's gamma = 0.78 projected onto the same thirds;
  E. the survey's own z-DEPENDENT stellar-mass shift (App. C), which Alcock's invariance
     argument does not cover.
"""
import csv, json, math, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CSV = os.path.join(ROOT, "data_assembly/arxiv_tables/musedark_II_III/musedarkIII_stated_results_NOT_A_TABLE.csv")
CFG262 = os.path.join(ROOT, "campaign_fresh_gravity/CFG262_musedark_zthirds_by_route/cfg262_stageB_results.json")
OUT = os.path.join(os.path.dirname(__file__), "alcock_2609_38796_comparison_results.json")

Z_LO, Z_HI = 0.33, 1.44          # MUSE-DARK III redshift range (Alcock abstract)
OM = 0.315                       # Planck 2018 flat LCDM, for E(z)
ALCOCK_GAMMA, ALCOCK_GAMMA_E = 0.78, 0.15

rows = list(csv.DictReader(open(CSV)))
def val(quantity, framework_prefix):
    for r in rows:
        q = r["quantity"]
        if (q == quantity or q.startswith(quantity + " in a0(z)")) and r["framework"].startswith(framework_prefix):
            return float(r["value"])
    raise KeyError((quantity, framework_prefix))

def gamma_between(a_lo, a_hi, z_lo, z_hi):
    return math.log(a_hi / a_lo) / math.log((1 + z_hi) / (1 + z_lo))

E = lambda z: math.sqrt(OM * (1 + z) ** 3 + 1 - OM)
res = {}

# A. the survey's three routes, linear form a0(0) + a1 z
print("A. Effective exponent of MUSE-DARK III's own linear fits over 0.33 < z < 1.44")
routes = {"DC14 halo (headline)": "DC14", "best-evidence LCDM halo": "per-galaxy", "MOND refit": "MOND refit"}
res["A_routes"] = {}
for label, pre in routes.items():
    a00, a1 = val("a0(0)", pre), val("a1", pre)
    g = gamma_between(a00 + a1 * Z_LO, a00 + a1 * Z_HI, Z_LO, Z_HI)
    res["A_routes"][label] = {"a0_0": a00, "a1": a1, "gamma_eff": g}
    print(f"   {label:26s} a0(0)={a00:.2f} a1={a1:.2f}  -> gamma_eff = {g:.2f}")

# B. binned endpoints under bin-centre brackets
lo, hi = val("a0 in lowest of four quantile z bins", "DC14"), val("a0 in highest of four quantile z bins", "DC14")
print(f"\nB. Binned endpoints {lo:.2f} -> {hi:.2f} (x1e-10); bin centres not printed, so bracket them")
res["B_bins"] = {}
for zl, zh in [(0.45, 1.30), (0.55, 1.25), (0.65, 1.20)]:
    g = gamma_between(lo, hi, zl, zh)
    res["B_bins"][f"{zl}-{zh}"] = g
    print(f"   centres z = {zl:.2f}, {zh:.2f}  -> gamma = {g:.2f}")
print(f"   Alcock (all four bins, Fig. 3 read-off): gamma = {ALCOCK_GAMMA} +- {ALCOCK_GAMMA_E}")

# C. H(z) effective exponent
gH = gamma_between(E(Z_LO), E(Z_HI), Z_LO, Z_HI)
res["C_Hz_gamma_eff"] = gH
print(f"\nC. a0 ~ H(z) over 0.33-1.44 (Om={OM}): gamma_eff = {gH:.2f}  (Alcock quotes ~1.10)")

# D. CFG262 thirds by baryon route
d = json.load(open(CFG262))["numbers"]
zt = [d["rows"][f"z{i}-routei-bD"]["z"] for i in (1, 2, 3)]
rival = d["diff"]["bD|i"]["rival"]
alc = ALCOCK_GAMMA * math.log10((1 + zt[2]) / (1 + zt[0]))
alc_e = ALCOCK_GAMMA_E * math.log10((1 + zt[2]) / (1 + zt[0]))
print(f"\nD. CFG262 (frozen 10-01): implied-a0 change third3 - third1, z {zt[0]:.3f} -> {zt[2]:.3f} (dex)")
print(f"   expectations: flat 0.000 | H(z) {rival:+.3f} | Alcock gamma=0.78 {alc:+.3f} +- {alc_e:.3f}")
names = {"i": "fitted DC14 masses", "ii": "SED M* + H2 gas", "iii": "SED M*"}
res["D_cfg262"] = {"z_thirds": zt, "Hz_expect": rival, "alcock_expect": alc, "routes": {}}
for r in ("i", "ii", "iii"):
    x = d["diff"][f"bD|{r}"]
    zf, zh, za = x["d"] / x["sd"], (x["d"] - rival) / x["sd"], (x["d"] - alc) / math.hypot(x["sd"], alc_e)
    res["D_cfg262"]["routes"][r] = {"d": x["d"], "sd": x["sd"], "z_vs_flat": zf, "z_vs_Hz": zh, "z_vs_alcock": za}
    print(f"   route ({r:3s}) {names[r]:20s} {x['d']:+.3f} +- {x['sd']:.3f}   vs flat {zf:+.1f}s  vs H(z) {zh:+.1f}s  vs Alcock {za:+.1f}s")
lv = [d["rows"][f"z3-route{r}-bD"]["s"] for r in ("i", "ii", "iii")]
res["D_cfg262"]["z3_levels"] = lv
print(f"   top-third (z {zt[2]:.2f}) implied a0/a0_ref by route: {lv[0]:.2f} / {lv[1]:.2f} / {lv[2]:.2f}  (spread x{max(lv)/min(lv):.1f})")

# E. the survey's own z-dependent M* shift
s_lo = val("uniform M* shift needed to recover a0=1.2e-10 (lowest z bins)", "DC14")
s_hi = val("uniform M* shift needed to recover a0=1.2e-10 (highest z bin)", "DC14")
h2 = val("systematic on total disk mass from unmodelled molecular gas", "DC14")
res["E_Mstar"] = {"shift_low_z": s_lo, "shift_high_z": s_hi, "differential": s_hi - s_lo, "unmodelled_H2": h2}
print(f"\nE. MUSE-DARK III App. C: M* shift that returns a0 = 1.2e-10 is {s_lo} dex (low z) and {s_hi} dex (high z)")
print(f"   -> a z-DEPENDENT mass offset of {s_hi - s_lo:.2f} dex erases the whole rise; unmodelled H2 alone is ~{h2} dex")
print("   Alcock's invariance covers only z-independent rescalings, so it does not reach this.")

json.dump(res, open(OUT, "w"), indent=1)
print(f"\nwrote {os.path.relpath(OUT, ROOT)}")
