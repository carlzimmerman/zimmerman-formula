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
     argument does not cover;
  F. Alcock's own Table 1 (digitised bins, MNRAS 551 L1, read from the published PDF 10-08)
     refitted: frozen, E(z), (1+z)^1.5, (1+z)^gamma, bars as 1 sigma (c68) and as 95% (c95);
  G. the z-dependent mass drift (dex per unit z) that would bring gamma to 0 or to E(z),
     with the a0-per-M* response read off the survey's own App. C numbers.
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

# F. Alcock Table 1 refit
TAB1 = [(0.503, 1.990, 0.085, 0.086), (0.825, 2.200, 0.105, 0.105),
        (1.047, 2.571, 0.114, 0.110), (1.276, 2.710, 0.134, 0.138)]
OM_A = 0.307                                      # Alcock's background
EA = lambda z: math.sqrt(OM_A * (1 + z) ** 3 + 1 - OM_A)
def fit_shape(shape, sig):                        # one-amplitude weighted LS, a0 = A * shape(z)
    w = [1 / s_ ** 2 for s_ in sig]
    f = [shape(z) for z, *_ in TAB1]
    A = sum(wi * fi * a for wi, fi, (z, a, *_) in zip(w, f, TAB1)) / sum(wi * fi * fi for wi, fi in zip(w, f))
    chi = sum(wi * (a - A * fi) ** 2 for wi, fi, (z, a, *_) in zip(w, f, TAB1))
    return A, chi
def fit_gamma(sig):                               # grid over gamma, amplitude profiled
    best = min(((fit_shape(lambda z, g=g: (1 + z) ** g, sig)[1], g) for g in [i / 1000 for i in range(-500, 2501)]))
    chi0, g0 = best
    lo = min(g for g in [i / 1000 for i in range(-500, 2501)] if fit_shape(lambda z, g=g: (1 + z) ** g, sig)[1] <= chi0 + 1)
    hi = max(g for g in [i / 1000 for i in range(-500, 2501)] if fit_shape(lambda z, g=g: (1 + z) ** g, sig)[1] <= chi0 + 1)
    return g0, (hi - lo) / 2, chi0
print("\nF. Alcock Table 1 (four digitised bins) refitted")
res["F_alcock_refit"] = {}
for conv, k in (("c68", 1.0), ("c95", 1.96)):
    sig = [(lo_ + hi_) / 2 / k for _, _, lo_, hi_ in TAB1]
    out = {}
    for name, shp in (("frozen", lambda z: 1.0), ("E(z)", EA), ("(1+z)^1.5", lambda z: (1 + z) ** 1.5)):
        A, chi = fit_shape(shp, sig); out[name] = {"A": A, "chi2": chi}
    g, ge, chig = fit_gamma(sig)
    out["gamma"] = {"gamma": g, "err": ge, "chi2": chig, "z_vs_0": g / ge, "z_vs_E": (1.10 - g) / ge, "z_vs_1.5": (1.5 - g) / ge}
    res["F_alcock_refit"][conv] = out
    print(f"   {conv}: frozen chi2 {out['frozen']['chi2']:.1f}/3 | E(z) A={out['E(z)']['A']:.2f} chi2 {out['E(z)']['chi2']:.1f}/3"
          f" | (1+z)^1.5 chi2 {out['(1+z)^1.5']['chi2']:.1f}/3 | gamma {g:.2f} +- {ge:.2f}"
          f" (from 0: {g/ge:.1f}s, from E(z) 1.10: {(1.10-g)/ge:.1f}s)")
print("   Alcock Table 2 (c68): frozen 28.8/3, E(z) 5.2/3 A=1.40, (1+z)^1.5 23.2/3, gamma 0.78 +- 0.15")

# G. z-dependent mass drift that moves gamma
zb = [r[0] for r in TAB1]
resp = [math.log10(1.99 / 1.2) / s_lo, math.log10(2.71 / 1.2) / s_hi]   # dlog a0 / dlog M*, App. C
sig68 = [(r[2] + r[3]) / 2 for r in TAB1]
def gamma_with_drift(dd, R):                     # masses raised by dd*(z - z_first) dex, a0 falls by R*that
    keep = list(TAB1)
    TAB1[:] = [(z, a * 10 ** (-R * dd * (z - zb[0])), lo_, hi_) for z, a, lo_, hi_ in keep]
    g = fit_gamma(sig68)[0]
    TAB1[:] = keep
    return g
res["G_drift"] = {"response_dloga0_dlogM": resp}
print(f"\nG. a0 response to M* from App. C: {resp[0]:.2f} (low z) / {resp[1]:.2f} (high z)")
for R in resp:
    need0 = next(dd / 100 for dd in range(0, 101) if gamma_with_drift(dd / 100, R) <= 0)
    needE = next(dd / 100 for dd in range(-100, 1) [::-1] if gamma_with_drift(dd / 100, R) >= 1.10)
    res["G_drift"][f"R{R:.2f}"] = {"dex_per_z_to_gamma0": need0, "dex_per_z_to_E": needE}
    print(f"   response {R:.2f}: drift to reach gamma=0: +{need0:.2f} dex per unit z "
          f"(+{need0*(zb[-1]-zb[0]):.2f} dex across the bins); to reach E(z): {needE:+.2f} dex per unit z")
print(f"   survey's own App. C differential: +{s_hi - s_lo:.2f} dex between its lowest and highest bins")

json.dump(res, open(OUT, "w"), indent=1)
print(f"\nwrote {os.path.relpath(OUT, ROOT)}")
