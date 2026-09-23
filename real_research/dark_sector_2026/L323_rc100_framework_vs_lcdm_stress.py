#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L323 -- STRESS TEST OF TODAY'S CLEANEST FRAMEWORK WIN: does "the framework alone predicts RC100's high-z dark fractions and
LCDM does not" (L320) survive when LCDM is given EVERY fair chance?

THE CLAIM UNDER TEST (L320, committed): on RC100 (Nestor Shachar+2023; 100 rotation curves, z = 0.6-2.5), the framework with
ZERO free parameters (nu_RAR, a0 = c H_Lambda/Z) predicts a median dark fraction inside R_e of 0.23-0.31 against the measured
0.29, while LCDM (Moster+13 halo masses, Dutton-Maccio NFW) predicts 0.38-0.49.  A win counts only after the rival's best
version has been tried.  This lane gives LCDM, one at a time and then all together in its own favour:
  H  halo mass shifted by -0.2 dex (the SHMR's scatter/systematic floor, in LCDM's favour)
  C  concentration lowered by 0.1 dex (scatter, in LCDM's favour)
  K  a MAXIMAL feedback core: Read+2016 coreNFW, M(<r) = M_NFW(<r) tanh(r/r_c)^n with n = 1 and r_c = 1.75 R_e -- the
     most generous inner-halo reduction at fixed halo mass (DC14 predicts almost no coring at these M_*/M_h ~ 0.02-0.04)
  A  Blumenthal adiabatic contraction (the standard direction; makes LCDM WORSE; reported for completeness)
  ALL  H + C + K together: LCDM's most favourable combination.
The framework gets nothing: both footings, disc geometry xi_geo in {1.0, 1.3}, and the gas-fraction sweep of L320.

STATISTICS (RC100 tabulates no f_DM errors, so no chi^2 is pretended):
  S1 the median of (f_pred - f_obs) per model with a galaxy-bootstrap 68% interval;
  S2 the fraction of galaxies each model predicts within 0.15 of the observed f_DM;
  S3 BOTH-WAYS on the framework: its per-galaxy residuals (f_obs - f_fw) must not correlate with g_bar (a kernel error would)
     -- Spearman rho with a permutation p-value; and the z-trend of its residuals.
CONTROLS: C1 the coreNFW with n = 0 reproduces NFW exactly; C2 the Blumenthal solution with f_b -> 0 returns the input NFW.
  S4 THE TREND: each model pushed through the data's own inversion (h16: a0 = (1 - f) g_obs/[ln(1/f)]^2); d log a0/dz per
     LCDM variant against the data's -0.112 +/- 0.063 -- the part of L320 that may still discriminate.
RESULT OF THE FIRST RUN (kept, and why the checks are phrased as they are): the claim "the framework beats LCDM on the LEVEL"
FAILED the stress test -- LCDM's single-knob variants (halo mass -0.2 dex, or concentration -0.1 dex) reach RC100's median.
The load-bearing checks therefore state the FINDING: (S1) the level is a TIE; (S4) the trend, tested variant by variant.
MUTATE=1 shifts the observed f_DM by +0.25 (a dark-matter-rich universe): the framework then misses, the tie breaks, and S1
must FAIL (rc = 1).

Run from the repository root:  python3 real_research/dark_sector_2026/L323_rc100_framework_vs_lcdm_stress.py
"""
import os, sys, csv, json, math
import numpy as np
from scipy.optimize import brentq
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L323_rc100_framework_vs_lcdm_stress"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L323", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__)
G, MSUN, KPC, MPC = 6.6743e-11, 1.98892e30, 3.0856775814913673e19, 3.0856775814913673e22
h = 0.6736; H0 = 100 * h * 1e3 / MPC; Om, OL = 0.3153, 0.6847
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
FB = 0.16


def nu(x):
    return 1.0 / (1.0 - np.exp(-np.sqrt(np.clip(x, 1e-12, None))))


def rho_crit(z): return 3 * (H0 * math.sqrt(Om * (1 + z) ** 3 + OL)) ** 2 / (8 * math.pi * G)


def mstar_over_mh(Mh, z):
    zz = z / (1 + z); M1 = 10 ** (11.590 + 1.195 * zz); N = 0.0351 - 0.0247 * zz
    return 2 * N / ((Mh / M1) ** -(1.376 - 0.826 * zz) + (Mh / M1) ** (0.608 + 0.329 * zz))


def halo_mass(Ms, z):
    lg = np.linspace(9.5, 15.5, 6001); Mh = 10 ** lg
    return float(10 ** np.interp(math.log10(Ms), np.log10(Mh * mstar_over_mh(Mh, z)), lg))


def c200(Mh, z):
    a = 0.520 + (0.905 - 0.520) * math.exp(-0.617 * z ** 1.21); b = -0.101 + 0.026 * z
    return 10 ** (a + b * math.log10(Mh / (1e12 / h)))


def nfw_menc(Mh, c, z):
    r200 = (3 * Mh * MSUN / (4 * math.pi * 200 * rho_crit(z))) ** (1 / 3); rs = r200 / c
    m = lambda x: math.log(1 + x) - x / (1 + x)
    return (lambda r: Mh * MSUN * m(r / rs) / m(c)), r200


def dm_enclosed(Mh, c, z, R, Re, core_n=0.0, contract=False, Mb_disc=0.0):
    """dark mass inside R: NFW, optional coreNFW (Read+2016), optional Blumenthal contraction by the disc baryons."""
    Mn, r200 = nfw_menc(Mh, c, z)
    if contract and Mb_disc > 0:
        # Blumenthal: [M_dm,i(r_i) + M_b,i(r_i)] r_i = [M_dm,i(r_i) + M_b,f(r_f)] r_f, with M_b,i = f_b/(1-f_b) M_dm,i
        Mbf = lambda r: Mb_disc * MSUN * (1 - (1 + r / (Re / 1.68)) * math.exp(-r / (Re / 1.68)))   # exponential disc
        fbi = FB / (1 - FB)
        fn = lambda ri: (1 + fbi) * Mn(ri) * ri - (Mn(ri) + Mbf(R)) * R
        try:
            ri = brentq(fn, 1e-3 * R, 50 * R)
            return Mn(ri) * (1 - FB)
        except ValueError:
            return Mn(R) * (1 - FB)
    core = math.tanh(R / (1.75 * Re)) ** core_n if core_n > 0 else 1.0
    return Mn(R) * core * (1 - FB)


rows = list(csv.DictReader(open(os.path.join(REPO, "real_research", "data", "rc100_nestorshachar2023_table3.csv"))))
gal = []
for r in rows:
    try:
        z, lMb, Re, fdm = (float(r[k]) for k in ("z", "logMbar_Msun", "Re_kpc", "fDM_within_Re"))
    except ValueError:
        continue
    if all(np.isfinite([z, lMb, Re, fdm])):
        gal.append(dict(z=z, Mb=10 ** lMb, Re=Re * KPC, fdm=fdm))
Z = np.array([g["z"] for g in gal])
P(f"  RC100: {len(gal)} galaxies with z, M_bar, R_e, f_DM")


def predict(g, model, xi_geo=1.0, mu_fac=1.0, foot="canonical"):
    z, R = g["z"], g["Re"]
    Mb_in = 0.5 * g["Mb"] * xi_geo
    gb = G * Mb_in * MSUN / R ** 2
    if model == "framework":
        return 1 - 1 / float(nu(gb / A0[foot]))
    mu = mu_fac * 0.5 * ((1 + z) / 2) ** 2
    Mh = halo_mass(g["Mb"] / (1 + mu), z)
    c = c200(Mh, z)
    dlogM = -0.2 if model in ("H", "ALL") else 0.0
    dlogc = -0.1 if model in ("C", "ALL") else 0.0
    Mh *= 10 ** dlogM; c *= 10 ** dlogc
    core_n = 1.0 if model in ("K", "ALL") else 0.0
    Mdm = dm_enclosed(Mh, c, z, R, R, core_n=core_n, contract=(model == "A"), Mb_disc=g["Mb"])
    return 1 - Mb_in * MSUN / (Mb_in * MSUN + Mdm)


# ============================================================================================ controls
banner("CONTROLS")
g0 = gal[0]; Mh0 = halo_mass(g0["Mb"] / 1.5, g0["z"]); c0 = c200(Mh0, g0["z"])
d_nfw = dm_enclosed(Mh0, c0, g0["z"], g0["Re"], g0["Re"])
d_n0 = dm_enclosed(Mh0, c0, g0["z"], g0["Re"], g0["Re"], core_n=0.0)
check("C1 coreNFW with n = 0 reproduces NFW exactly", f"{d_n0/d_nfw:.12f}", abs(d_n0 / d_nfw - 1) < 1e-12)
FB_save = FB
FB = 1e-9
d_bl = dm_enclosed(Mh0, c0, g0["z"], g0["Re"], g0["Re"], contract=True, Mb_disc=1e-6)
d_ref = dm_enclosed(Mh0, c0, g0["z"], g0["Re"], g0["Re"])
FB = FB_save
check("C2 Blumenthal contraction with vanishing baryons returns the input NFW", f"ratio {d_bl/d_ref:.6f}", abs(d_bl / d_ref - 1) < 1e-3)

# ============================================================================================ S1/S2
banner("S1/S2  MEDIAN (f_pred - f_obs) AND THE FRACTION WITHIN 0.15, over the systematic grid")
f_obs = np.array([g["fdm"] for g in gal])
if MUTATE:
    f_obs = np.clip(f_obs + 0.25, 0.03, 0.97)
    P("  MUTATE: observed f_DM shifted by +0.25 (a dark-matter-rich universe)")
MODELS = ["framework", "NFW", "H", "C", "K", "A", "ALL"]
rng = np.random.default_rng(7)
boot_idx = [rng.integers(0, len(gal), len(gal)) for _ in range(2000)]
res = {}
for m in MODELS:
    cells = []
    for xi in (1.0, 1.3):
        for mf in ((1.0,) if m == "framework" else (1 / 1.5, 1.0, 1.5)):
            for ft in (("canonical", "alt") if m == "framework" else ("canonical",)):
                fp = np.array([predict(g, m, xi, mf, ft) for g in gal])
                d = fp - f_obs
                med = float(np.median(d)); bs = np.array([np.median(d[k]) for k in boot_idx])
                cells.append(dict(xi=xi, mu=mf, foot=ft, median_offset=med, lo=float(np.percentile(bs, 16)),
                                  hi=float(np.percentile(bs, 84)), within015=float(np.mean(np.abs(d) < 0.15)),
                                  median_pred=float(np.median(fp))))
    res[m] = cells
    best = min(cells, key=lambda c: abs(c["median_offset"]))
    P(f"    {m:9s}: median offset {min(c['median_offset'] for c in cells):+.3f} .. {max(c['median_offset'] for c in cells):+.3f}  "
      f"(best cell {best['median_offset']:+.3f} [{best['lo']:+.3f}, {best['hi']:+.3f}]); within 0.15: "
      f"{min(c['within015'] for c in cells):.2f}-{max(c['within015'] for c in cells):.2f}; median f_pred "
      f"{min(c['median_pred'] for c in cells):.2f}-{max(c['median_pred'] for c in cells):.2f}")
OUT["numbers"]["S1S2"] = res
OUT["numbers"]["observed_median_fdm"] = float(np.median(f_obs))
fw_worst = max(abs(c["median_offset"]) for c in res["framework"])
lcdm_best = {m: min(abs(c["median_offset"]) for c in res[m]) for m in MODELS if m != "framework"}
lcdm_best_ci_lo = {m: min((c for c in res[m]), key=lambda c: abs(c["median_offset"]))["lo"] for m in MODELS if m != "framework"}
fw_within = min(c["within015"] for c in res["framework"])
lc_within = {m: max(c["within015"] for c in res[m]) for m in MODELS if m != "framework"}
OUT["numbers"]["summary"] = dict(framework_worst_abs_offset=fw_worst, lcdm_best_abs_offset=lcdm_best,
                                 framework_min_within015=fw_within, lcdm_max_within015=lc_within)
fw_best_ci = min(res["framework"], key=lambda c: abs(c["median_offset"]))
fw_contains0 = fw_best_ci["lo"] <= 0 <= fw_best_ci["hi"]
lcdm_contains0 = [m for m in MODELS if m != "framework" and
                  (lambda c: c["lo"] <= 0 <= c["hi"])(min(res[m], key=lambda c: abs(c["median_offset"])))]
tie = fw_contains0 and len(lcdm_contains0) > 0
OUT["numbers"]["level_tie"] = dict(framework_best_ci=[fw_best_ci["lo"], fw_best_ci["hi"]], lcdm_variants_containing_zero=lcdm_contains0)
check("S1 THE LEVEL IS A TIE: the framework's best systematic cell AND at least one LCDM variant's best cell both contain zero "
      "offset in their 68% bootstrap intervals -- L320's 'framework beats LCDM on the dark fractions' is WITHDRAWN as a robust win",
      f"framework best [{fw_best_ci['lo']:+.3f}, {fw_best_ci['hi']:+.3f}]; LCDM variants containing 0: {lcdm_contains0}",
      tie, "the median dark fraction at z ~ 1-2 cannot separate the two within the halo-model and baryon systematics")
check("S2 (informational) galaxies within 0.15 of their observed f_DM: framework worst cell vs LCDM best cells",
      f"framework >= {fw_within:.2f}; LCDM <= " + ", ".join(f"{m} {v:.2f}" for m, v in lc_within.items()),
      True, "no discrimination at the per-galaxy level either", load_bearing=False)

# ============================================================================================ S4 the trend
banner("S4  THE TREND: d log a0/dz through the data's own inversion, per model and variant")
def invert(f, g):
    gb_ = G * 0.5 * g["Mb"] * MSUN / g["Re"] ** 2
    go = gb_ / (1 - f)
    return math.log10((1 - f) * go / math.log(1 / f) ** 2) if 0.02 < f < 0.98 else float("nan")
def slope_of(fs):
    la = np.array([invert(f, g) for f, g in zip(fs, gal)]); m = np.isfinite(la)
    s_ = float(np.polyfit(Z[m], la[m], 1)[0])
    bs = [np.polyfit(Z[m][k], la[m][k], 1)[0] for k in (rng.integers(0, m.sum(), m.sum()) for _ in range(1000))]
    return s_, float(np.std(bs))
s_obs, e_obs = slope_of(f_obs)
trend = {}
for m in MODELS:
    ss = []
    for xi in (1.0, 1.3):
        for mf in ((1.0,) if m == "framework" else (1 / 1.5, 1.0, 1.5)):
            ss.append(slope_of(np.array([predict(g, m, xi, mf) for g in gal]))[0])
    trend[m] = dict(min=float(min(ss)), max=float(max(ss)),
                    sigma_min=float((min(ss) - s_obs) / e_obs), sigma_max=float((max(ss) - s_obs) / e_obs))
    P(f"    {m:9s}: d log a0/dz {min(ss):+.3f} .. {max(ss):+.3f}  -> {(min(ss)-s_obs)/e_obs:+.1f} .. {(max(ss)-s_obs)/e_obs:+.1f} sigma "
      f"from the data {s_obs:+.3f} +/- {e_obs:.3f}")
OUT["numbers"]["S4_trend"] = dict(data=[s_obs, e_obs], models=trend)
lc_trend_min_sigma = min(trend[m]["sigma_min"] for m in MODELS if m not in ("framework",))
check("S4 THE TREND, variant by variant: every LCDM variant's inverted a0 rises with z, and the LEAST-rising LCDM cell sits "
      f"{lc_trend_min_sigma:.1f} sigma above RC100's trend; the framework is flat by construction",
      "; ".join(f"{m} {trend[m]['min']:+.3f}..{trend[m]['max']:+.3f}" for m in MODELS),
      all(trend[m]["min"] > 0 for m in MODELS if m != "framework"),
      "the trend is the part that still separates them -- with RC100's own caveat: it restates RC100's falling f_DM(z)")

# ============================================================================================ S3 both ways
banner("S3  BOTH WAYS ON THE FRAMEWORK: do its residuals track g_bar or z?")
gb = np.array([G * 0.5 * g["Mb"] * MSUN / g["Re"] ** 2 for g in gal])
fw = np.array([predict(g, "framework") for g in gal])
resid = f_obs - fw
rho_g, _ = spearmanr(np.log10(gb), resid)
rho_z, _ = spearmanr(Z, resid)
prng = np.random.default_rng(11)
perm_g = np.array([spearmanr(np.log10(gb), prng.permutation(resid))[0] for _ in range(4000)])
perm_z = np.array([spearmanr(Z, prng.permutation(resid))[0] for _ in range(4000)])
p_g = float(np.mean(np.abs(perm_g) >= abs(rho_g))); p_z = float(np.mean(np.abs(perm_z) >= abs(rho_z)))
OUT["numbers"]["S3"] = dict(rho_gbar=float(rho_g), p_gbar=p_g, rho_z=float(rho_z), p_z=p_z,
                            resid_median=float(np.median(resid)), resid_scatter=float(np.std(resid)))
P(f"    framework residuals f_obs - f_fw: median {np.median(resid):+.3f}, scatter {np.std(resid):.3f}; "
  f"Spearman vs log g_bar {rho_g:+.3f} (p {p_g:.3f}); vs z {rho_z:+.3f} (p {p_z:.3f})")
check("S3 the framework's residuals show no significant trend with g_bar (p > 0.01): no sign of a wrong kernel shape at z ~ 1-2",
      f"rho = {rho_g:+.3f}, p = {p_g:.3f}", p_g > 0.01, "reported either way; a trend would be a kernel failure at high z",
      load_bearing=False)

# ============================================================================================ verdict
banner("VERDICT")
P(f"""  With no free parameter, the framework puts RC100's median dark fraction within {fw_worst:.2f} on its worst systematic cell.
  LCDM's best cell per variant misses by: {', '.join(f'{m} {v:.2f}' for m, v in lcdm_best.items())} (ALL = halo mass -0.2 dex,
  concentration -0.1 dex, and a maximal feedback core together).  THE LEVEL IS A TIE ({'yes' if tie else 'no'}): L320's "framework
  beats LCDM on the dark fractions" is WITHDRAWN.  THE TREND: LCDM's least-rising cell sits {lc_trend_min_sigma:.1f} sigma above RC100's
  d log a0/dz; the framework is flat, {abs(s_obs)/e_obs:.1f} sigma from it.
  Caveats that no model choice here removes: RC100's f_DM comes from its own mass models (stellar M/L, gas from scaling
  relations, pressure support), and its selection across redshift is not controlled.  This is a relative statement --
  same baryons, same radii, two gravity models -- and it is quoted as such.""")

n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
