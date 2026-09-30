"""z05: the decisive-test table and the allowed range of a0(2.5)/a0(0).

(1) What a measurement of Delta log10 a0 at z ~ 2.5 with 0.1 dex precision concludes for the four laws the brief names: flat (framework; also R*, 2R*), the particle-horizon law D, the H(z)
    tracking law (a0 = cH(z)/Z), and the LambdaCDM-native emergent scale (+0.33 dex).  Pairwise separations, 2-sigma bands, the precision each pair needs, and the floor from CFG52's correlated
    0.25-dex mass-scale systematic (reproduced as a control: 2.3 sigma vs H(z), 1.3 sigma vs LCDM-native).
(2) Lane reach: for each lane the record has, the D-vs-flat lever at the lane's redshift and, where a committed number exists, the sigma it delivers; the low-z weak-lensing window from the
    record's own forecast formula (real_research/a0z_lensing_forecast.py, per_bin_sigma copied; an ASSUMPTION-LADEN forecast, not data).
(3) The allowed range of a0(2.5)/a0(0): a one-parameter shape family a0(z)/a0(0) = E(z)^p (p = 0 flat, p = 1 the H(z) law, p ~ 1.36 the particle-horizon law) confronted with the honest (systematics-
    inclusive, 2-sigma) constraints from z02-z04, the union taken over the record's own nuisance cells (gas, pressure) where those are unmeasured.  A second family D^q checks that the range is not an artefact
    of the E^p shape.  A shape family is a PROXY (D and LCDM-native are only approximately in it); the range is a statement about the family, stated with that caveat.
Declared before running: the allowed range's UPPER edge sits near p ~ 1-1.5 (a0(2.5)/a0(0) ~ 4-6); the constraints do not close the FALLING side; MUSE-DARK III at face value (p ~ 1.7) is inconsistent with the other honest rows.
Run: python3 z05_decisive_tests.py   (exit 0 iff every check passes)
"""
import os, sys, csv, json, math
import numpy as np
from zcommon import *
import zkurvs
from zkurvs import LAWS, delta, S_LIST, MU_BR, KU2, KR, OM

REPO = zkurvs.REPO
ok = []


def chk(name, cond, detail=""):
    ok.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (("\n       " + detail) if detail else ""))


cos = Cosmo(**PLANCK)
L = laws(cos)
LAW = {"flat": L["flat (R*, 2R*: z-independent)"], "H(z)": L["Hubble radius c/H(z)  [a0 = cH(z)/Z]"], "D": L["particle horizon d_p (radius OR diameter)"], "LCDM-native": lambda z: lcdm_native(z)}
NM = list(LAW)
OUT = {}

# ================================================================== (1)
print("=" * 112)
print("(1) THE DECISIVE TABLE at z = 2.5: prediction of each law in Delta log10 a0, and in the BTFR mass-axis zero point at several depths y = g_bar/a0(0)")
print("=" * 112)
Z = 2.5
dexs = {n: math.log10(LAW[n](Z)) for n in NM}
print("   Delta log10 a0(2.5)/a0(0): " + ", ".join(f"{n} {v:+.3f}" for n, v in dexs.items()) + "    ratios " + ", ".join(f"{n} {LAW[n](Z):.2f}" for n in NM))
btfr = {}
for y in (0.03, 0.1, 0.3, 1.0):
    btfr[y] = {n: dlogM_P2(LAW[n](Z), y) for n in NM}
    print(f"   BTFR zero point Delta_b at y = g_bar/a0(0) = {y:4.2f}:  " + ", ".join(f"{n} {v:+.3f}" for n, v in btfr[y].items()) + f"    (gap D - flat {btfr[y]['D'] - btfr[y]['flat']:+.3f}, D - H(z) {btfr[y]['D'] - btfr[y]['H(z)']:+.3f})")
OUT["dex25"] = dexs; OUT["btfr25"] = {str(y): v for y, v in btfr.items()}
sep = {(a, b): abs(dexs[a] - dexs[b]) for i, a in enumerate(NM) for b in NM[i + 1:]}
print("\n   pairwise separations (dex) and sigma at measurement precision s = 0.05, 0.10, 0.13 (PAPER7 pre-registered), 0.25 (CFG52 correlated mass-scale floor):")
for (a, b), v in sep.items():
    print(f"      {a:12s} vs {b:12s} {v:.3f} dex :   " + "  ".join(f"{v / s:5.1f}" for s in (0.05, 0.10, 0.13, 0.25)))
chk("D0 CONTROL: CFG52's floor numbers are reproduced: at 0.25 dex the flat law is 2.3 sigma from H(z) and 1.3 sigma from LCDM-native (STANDING 4); PAPER7's 0.13 dex gives flat vs LCDM-native 2.5 sigma",
    abs(sep[("flat", "H(z)")] / 0.25 - 2.3) < 0.05 and abs(sep[("flat", "LCDM-native")] / 0.25 - 1.34) < 0.05 and abs(sep[("flat", "LCDM-native")] / 0.13 - 2.57) < 0.05)
minsep = min(sep.values())
print(f"   smallest separation: {min(sep, key=sep.get)} = {minsep:.3f} dex -> needs sigma <= {minsep / 3:.3f} dex for 3 sigma, <= {minsep / 5:.3f} for 5 sigma")
chk("D1 at 0.1 dex: flat is separated from every other law by >= 3.3 sigma; H(z) from D only 2.1 sigma and LCDM-native from H(z) 2.4 sigma; so 0.1 dex decides 'flat or rising' but NOT which rising law",
    all(sep[("flat", b)] / 0.1 >= 3.3 for b in ("H(z)", "D", "LCDM-native")) and 2.0 < sep[("H(z)", "D")] / 0.1 < 2.2 and 2.3 < sep[("H(z)", "LCDM-native")] / 0.1 < 2.5)
print("\n   OUTCOME TABLE for a measurement m +- 0.10 dex of Delta log10 a0(2.5) (2-sigma intervals |m - law| <= 0.20):")
bands = {n: (dexs[n] - 0.2, dexs[n] + 0.2) for n in NM}
edges = sorted({e for b in bands.values() for e in b} | {-0.6, 1.2})
outs = []
for lo, hi in zip(edges[:-1], edges[1:]):
    mid = 0.5 * (lo + hi)
    alive = [n for n in NM if bands[n][0] <= mid <= bands[n][1]]
    outs.append((lo, hi, alive))
merged = []
for lo, hi, al in outs:
    if merged and merged[-1][2] == al:
        merged[-1] = (merged[-1][0], hi, al)
    else:
        merged.append((lo, hi, al))
for lo, hi, al in merged:
    print(f"      m in [{lo:+.3f}, {hi:+.3f}]:  survives at 2 sigma: " + (", ".join(al) if al else "NONE (all four excluded: a0 fell, or a systematic)"))
OUT["outcomes_0p1"] = [(lo, hi, al) for lo, hi, al in merged]
uniq = {n: [(lo, hi) for lo, hi, al in merged if al == [n]] for n in NM}
print("   unique-identification intervals: " + "; ".join(f"{n}: " + ", ".join(f"[{lo:+.2f}, {hi:+.2f}]" for lo, hi in v) for n, v in uniq.items()))
chk("D2 at 0.1 dex the H(z) law has only a %.3f-dex-wide unique window (a measurement there is read as H(z) alone) while flat, LCDM-native and D each have >= 0.17-dex windows: the table is asymmetric" % (sum(hi - lo for lo, hi in uniq['H(z)'])),
    sum(hi - lo for lo, hi in uniq["H(z)"]) < 0.08 and all(sum(hi - lo for lo, hi in uniq[n]) > 0.15 for n in ("flat", "LCDM-native", "D")))
# the measurement in the OBSERVABLE (mass axis) is diluted; the required mass-axis precision for the same discrimination
for y in (0.1, 0.3, 1.0):
    gap = btfr[y]["D"] - btfr[y]["flat"]
    print(f"   at y = {y}: the D-vs-flat gap in the mass-axis zero point is {abs(gap):.3f} dex (undiluted {dexs['D']:.3f}): dilution {abs(gap) / dexs['D']:.2f}")
# FIRST RUN: my declared D3 ('at y = 1 less than half of D reaches the mass axis') was WRONG: the exact P2 map transmits 0.64 of D's shift at y = 1, 0.86 at y = 0.3, 0.95 at y = 0.1.
lin = lambda y: (1 / y) / (2 + 1 / y)          # the ledger's LOCAL linearisation x/(2+x), x = a0/g_bar
chk("D3 (computed statement; the first-pass expectation was wrong) for the LARGE shift of D the exact P2 map transmits MORE of the a0 shift to the mass axis than the ledger's local linearisation x/(2+x): y = 0.1: %.2f vs %.2f; y = 0.3: %.2f vs %.2f; y = 1: %.2f vs %.2f -- so linearised 'diluted' predictions for the steep laws (the record's ALT numbers) UNDER-state them; deep-MOND selection (y <~ 0.3) keeps > 85%%" % (abs(btfr[0.1]["D"]) / dexs["D"], lin(0.1), abs(btfr[0.3]["D"]) / dexs["D"], lin(0.3), abs(btfr[1.0]["D"]) / dexs["D"], lin(1.0)),
    all(abs(btfr[y]["D"]) / dexs["D"] > lin(y) for y in (0.1, 0.3, 1.0)) and abs(btfr[0.3]["D"]) / dexs["D"] > 0.85)
# LCDM's 'apparent a0' in RAR fits (Mayer+23) is a different observable: x3 at z=2
print(f"   NOTE: a RAR-FITTED a0 in LambdaCDM (Mayer+23, arXiv:2206.04333) rises x3 at z = 2 (+0.48 dex) with no fundamental a0; the H(z) law at z = 2 is +{math.log10(LAW['H(z)'](2.0)):.2f}, D +{math.log10(LAW['D'](2.0)):.2f}: a RAR-fit measurement (MUSE-type) cannot separate ITS OWN LambdaCDM apparent rise from H(z) at all; the deep-MOND BTFR zero point (LCDM-native +0.33 at 2.5) is the cleaner observable")

# ================================================================== (2) lanes
print("\n" + "=" * 112)
print("(2) LANE REACH: the D-vs-flat lever at each lane's redshift, and the sigma the lane delivers where a committed number exists")
print("=" * 112)
KZ = float(np.median([o["z"] for o in KU2])); RZ = float(np.median([o["z"] for o in KR]))
levers = {"KROSS (z~0.85)": RZ, "MUSE-DARK (z 0.3-1.4, median 0.86)": 0.86, "Jeanneau deep refit (z 1.06)": 1.06, "KURVS-CDFS (z~1.5)": KZ, "KMOS3D upper bin (z~2.3)": 2.3, "z~2.5 rotator (JWST NIRSpec IFU + ALMA)": 2.5}
lv = {}
for k, z in levers.items():
    lv[k] = dict(z=z, flat_vs_D_dex=math.log10(LAW["D"](z)), flat_vs_H_dex=math.log10(LAW["H(z)"](z)), D_vs_H_dex=math.log10(LAW["D"](z) / LAW["H(z)"](z)), flat_vs_LCDMn=math.log10(LAW["LCDM-native"](z)))
    print(f"   {k:44s} z {z:4.2f}: lever flat->D {lv[k]['flat_vs_D_dex']:.3f} dex; flat->H(z) {lv[k]['flat_vs_H_dex']:.3f}; H(z)->D {lv[k]['D_vs_H_dex']:.3f}; flat->LCDM-native {lv[k]['flat_vs_LCDMn']:.3f}")
OUT["levers"] = lv
# KURVS/KROSS: separation in sigma vs the spread of the flat law's own Delta' over the nuisance cells
sd = {}
for nm, samp in (("KURVS", "KURVS"), ("KROSS", "KROSS")):
    vals = {law: [delta(samp, mu, s, law)[0] for s in S_LIST for mu in MU_BR] for law in ("flat", "D")}
    sig = float(np.median([delta(samp, mu, s, "flat")[1] for s in S_LIST for mu in MU_BR]))
    sd[nm] = dict(sep=float(np.median(np.array(vals["flat"]) - np.array(vals["D"]))), sig=sig, spread_flat=float(np.ptp(vals["flat"])), spread_D=float(np.ptp(vals["D"])))
    print(f"   {nm}: D-vs-flat separation in Delta' = {sd[nm]['sep']:.3f} dex = {sd[nm]['sep'] / sig:.1f} sigma (stat, per cell {sig:.3f}); but Delta' of the SAME law moves by {sd[nm]['spread_flat']:.2f} dex across the (s, mu) nuisance cells")
OUT["kurvs_kross"] = sd
chk("L1 the nuisance spread of a single law across the record's own (s, mu) cells (KURVS %.2f dex) is %.1fx the D-vs-flat separation (%.2f dex): the lane is NON-DIAGNOSTIC for D vs flat until s and mu are MEASURED, exactly the record's reading" % (sd["KURVS"]["spread_flat"], sd["KURVS"]["spread_flat"] / sd["KURVS"]["sep"], sd["KURVS"]["sep"]),
    sd["KURVS"]["spread_flat"] > 1.5 * sd["KURVS"]["sep"] and sd["KROSS"]["spread_flat"] > 1.5 * sd["KROSS"]["sep"])
# weak lensing window, the record's own forecast formula
N_REF, SIG_REF = 259_000, 0.08


def per_bin_sigma(N_total, n_bins, sys_floor):
    N_bin = N_total / n_bins
    return math.hypot(SIG_REF * math.sqrt(N_REF / N_bin), sys_floor)


Ez = cos.Ez                                                   # same E(z) (radiation included) as the H(z) law of z01, so the p = 1 member IS the H(z) law
sigE = (Ez(0.45) / Ez(0.15) - 1)
sigD = LAW["D"](0.45) / LAW["D"](0.15) - 1
print(f"\n   z-binned weak-lensing RAR window z = 0.15 -> 0.45 (a0(0.45)/a0(0.15) - 1): H(z) {100 * sigE:.1f}%, particle horizon D {100 * sigD:.1f}%, LCDM-native {100 * (LAW['LCDM-native'](0.45) / LAW['LCDM-native'](0.15) - 1):.1f}%, flat 0")
wl = {}
for lab, N, nb, sysf in (("KiDS now (259k, 2 bins, gas 5%)", 259_000, 2, 0.05), ("DES+HSC+KiDS (1.5M, 3 bins, gas 5%)", 1_500_000, 3, 0.05), ("LSST/Euclid era (10M, 4 bins, gas 3%)", 10_000_000, 4, 0.03)):
    sb = per_bin_sigma(N, nb, sysf); sdiff = sb * math.sqrt(2)
    wl[lab] = dict(sig_diff=sdiff, H=sigE / sdiff, D=sigD / sdiff, D_vs_H=(sigD - sigE) / sdiff)
    print(f"      {lab:40s}: sigma(diff) = {100 * sdiff:4.1f}%   H(z) {sigE / sdiff:4.1f} sigma   D {sigD / sdiff:4.1f} sigma   (D - H(z) {(sigD - sigE) / sdiff:3.1f} sigma)")
OUT["lensing"] = wl
# FIRST/SECOND RUN: my guessed control value 0.155 for the H(z) signal was WRONG; the record's own script prints +18.8% (Verlinde cH, z 0.15 -> 0.45), per-bin 12.4 / 7.6 / 4.0 %, and 1.1 / 1.7 / 3.4 sigma.
chk("L2 CONTROL: reproduces the record's forecast script (real_research/a0z_lensing_forecast.py, re-run read-only): per-bin sigma 12.4%%/7.6%%/4.0%%, H(z) (Verlinde cH) signal +18.8%% (mine %.1f%%), sigma 1.1/1.7/3.4 (mine %.1f/%.1f/%.1f)" % (100 * sigE, wl["KiDS now (259k, 2 bins, gas 5%)"]["H"], wl["DES+HSC+KiDS (1.5M, 3 bins, gas 5%)"]["H"], wl["LSST/Euclid era (10M, 4 bins, gas 3%)"]["H"]),
    abs(per_bin_sigma(259_000, 2, 0.05) - 0.124) < 1e-3 and abs(per_bin_sigma(1_500_000, 3, 0.05) - 0.076) < 1e-3 and abs(per_bin_sigma(10_000_000, 4, 0.03) - 0.040) < 1e-3 and abs(sigE - 0.188) < 0.004
    and abs(wl["KiDS now (259k, 2 bins, gas 5%)"]["H"] - 1.1) < 0.1 and abs(wl["LSST/Euclid era (10M, 4 bins, gas 3%)"]["H"] - 3.4) < 0.1 and abs(wl["DES+HSC+KiDS (1.5M, 3 bins, gas 5%)"]["H"] - 1.7) < 0.15)
chk("L3 the LOW-z window separates D from flat far better than H(z) from flat: the D signal is %.0f%% vs %.0f%%, so even the record's KiDS-now forecast reads D at %.1f sigma and LSST/Euclid at %.1f sigma (an assumption-laden forecast; the record's 'gas floor' 3-5%% is the binding term)" % (100 * sigD, 100 * sigE, wl["KiDS now (259k, 2 bins, gas 5%)"]["D"], wl["LSST/Euclid era (10M, 4 bins, gas 3%)"]["D"]),
    sigD > 1.5 * sigE and wl["LSST/Euclid era (10M, 4 bins, gas 3%)"]["D"] > 3)
# today's drift: what a LOW-z observable could see in the rate of change
H0_per_Gyr = cos.H0 * GYR
print(f"\n   local drift today: d ln a0/dt = -{1 + 1 / cos.dp(0.0):.3f} H0 = -{100 * (1 + 1 / cos.dp(0.0)) * H0_per_Gyr:.1f}% per Gyr for D (flat 0; H(z) law -{1.5 * cos.Om:.3f} H0 = -{100 * 1.5 * cos.Om * H0_per_Gyr:.1f}% per Gyr); d ln a0/dz at z = 0: D {1 + 1 / cos.dp(0.0):.3f}, H(z) {1.5 * cos.Om:.3f}")
sp05 = LAW["D"](0.05) - 1
print(f"   D at z = 0.05: +{100 * sp05:.1f}% (H(z) +{100 * (LAW['H(z)'](0.05) - 1):.1f}%): the SPARC sample (z <~ 0.03) and MIGHTEE-HI (z <= 0.08; arXiv:2504.20857, 'first tentative evidence for evolution') sit inside this ~7% and cannot separate it from the 5.4% statistical error of a0(0) itself")

# ================================================================== (3) allowed range of a0(2.5)/a0(0)
print("\n" + "=" * 112)
print("(3) THE ALLOWED RANGE: the family a0(z)/a0(0) = E(z)^p against the HONEST (systematics-inclusive, 2-sigma) constraints of z02-z04; a0(2.5)/a0(0) = E(2.5)^p")
print("=" * 112)
E25 = Ez(2.5)
ps = np.round(np.arange(-1.5, 2.5001, 0.05), 3)
Ep = lambda p: (lambda z, p=p: Ez(z) ** p)
# Jeanneau deep refit
sub = list(csv.DictReader(open(os.path.join(REPO, "prep_2026", "jeanneau_refit", "subsample.csv"))))
zj = np.array([float(r["z"]) for r in sub]); yj = np.array([float(r["gbar_over_a0canon"]) for r in sub])
jd = lambda p: float(np.median([dlogM_P2(Ez(z) ** p, y) for z, y in zip(zj, yj)]))
acc = {}
acc["Jeanneau deep refit (honest 0.272)"] = np.array([abs(jd(p) - 0.140) <= 2 * 0.272 for p in ps])
led = list(csv.DictReader(open(os.path.join(REPO, "prep_2026", "highz_tfr_fork", "data_ledger.csv"))))
f_ = lambda x: float(x) if x not in ("", None) else float("nan")
rows = [(f_(r["z_eff"]), f_(r["gbar_over_a0_typ"]), f_(r["delta_b_dex_mass_axis"]), math.hypot(f_(r["stat_err_dex"]), f_(r["sys_est_dex"]))) for r in led
        if r["relation"].startswith("bTFR") and not any(math.isnan(f_(r[k])) for k in ("z_eff", "gbar_over_a0_typ", "delta_b_dex_mass_axis", "stat_err_dex", "sys_est_dex"))]
acc["ledger bTFR rows (4, honest)"] = np.array([all(abs(dlogM_P2(Ez(z) ** p, y) - db) <= 2 * e for z, y, db, e in rows) for p in ps])
# CFG198 slopes (95% CIs)
rd = list(csv.DictReader(open(os.path.join(REPO, "data_assembly", "musedark_catalogues", "musedark_numeric.csv"))))
flx = lambda r, k: (lambda v: v if np.isfinite(v) else np.nan)(float(r[k]) if r[k] not in ("", None) else np.nan)
need_ = ("z", "logMstar_phot", "DC14_logMdisk", "fDM_at_Re", "Re_kpc", "gas_density_Msun_pc2")
S = [r for r in rd if all(np.isfinite(flx(r, k)) for k in need_) and r["has_bulge"].strip() == "0" and 0 < flx(r, "fDM_at_Re") < 1]
zS = np.array([flx(r, "z") for r in S])
j198 = json.load(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG198_musedark_pergalaxy_a0z", "cfg198_musedark_a0z_results.json")))["numbers"]
ci_ii, ci_iii = j198["primary"]["ii"]["ci"], j198["primary"]["iii"]["ci"]
slp = lambda p: float(np.polyfit(zS, p * np.log10([Ez(z) for z in zS]), 1)[0])
acc["CFG198 route ii+iii slope CIs (SED masses)"] = np.array([ci_ii[0] <= slp(p) <= ci_ii[1] and ci_iii[0] <= slp(p) <= ci_iii[1] for p in ps])
# Milgrom Table I with a one-sided offset on zeta_obs
TAB = [(0.854, 7.3, 276, 0.21, 0.10, "err"), (1.500, 7.4, 310, 0.17, 0.38, "lim"), (1.613, 4.9, 257, 0.19, 0.09, "err"), (2.196, 5.5, 301, 0.00, 0.08, "lim"), (2.242, 3.3, 364, 0.00, 0.07, "lim"), (2.383, 6.0, 299, 0.12, 0.26, "lim")]
KPC_ = 3.0856775814913673e19


def chi_mil(fn, delta_, conv="U2"):
    tot = 0.0
    for z, R, V, zo, e, kind in TAB:
        x = (V * 1e3) ** 2 / (R * KPC_) / (1.2e-10 * fn(z)); zp = 1 / (1 + x)
        s_ = e if kind == "err" else (e - zo)
        p = (zp - (zo + delta_)) / s_
        tot += 0 if (kind == "lim" and zp <= zo + delta_) else p * p
    return tot


j03 = json.load(open("z03_results.json"))["results"]["zeta_a|U2|all six"]
chk("R0 CONTROL: my Milgrom-table chi2 reproduces z03's for the H(z) law (p = 1: %.2f vs %.2f) and D (%.2f vs %.2f) and flat (%.2f vs %.2f)" % (chi_mil(Ep(1.0), 0.0), j03["H(z)"]["chi2"], chi_mil(LAW["D"], 0.0), j03["D (d_p)"]["chi2"], chi_mil(LAW["flat"], 0.0), j03["flat"]["chi2"]),
    abs(chi_mil(Ep(1.0), 0.0) - j03["H(z)"]["chi2"]) < 1e-3 and abs(chi_mil(LAW["D"], 0.0) - j03["D (d_p)"]["chi2"]) < 1e-6 and abs(chi_mil(LAW["flat"], 0.0) - j03["flat"]["chi2"]) < 1e-6)
for d_ in (0.0, 0.18, 0.30):
    acc[f"Milgrom-17 Table I, offset on zeta_obs {d_:.2f}"] = np.array([chi_mil(Ep(p), d_) <= 12.59 for p in ps])
# MUSE-DARK III face value (a scenario, NOT in the honest set)
lr3 = math.log10(2.38); s3 = math.sqrt((0.1 / 2.38) ** 2 + 0.04 ** 2) / math.log(10)
acc["[scenario] MUSE-DARK III at face value"] = np.array([abs(p * math.log10(Ez(0.87)) - lr3) <= 2 * s3 for p in ps])
# KURVS / KROSS with the pipeline, union over nuisance cells
for p in ps:
    LAWS[f"Ep{p:+.2f}"] = Ep(float(p))
pub_cells = [(s, mu) for s in (1.0, 1.42, 1.62, 1.69, 3.0) for mu in (0.67, 1.0, 1.5)]
all_cells = [(s, mu) for s in S_LIST for mu in (0.25, 0.67, 1.5, 4.0)]
kv = {}
for p in ps:
    nm = f"Ep{p:+.2f}"
    kv[float(p)] = {c: (abs(delta("KURVS", c[1], c[0], nm)[0] / delta("KURVS", c[1], c[0], nm)[1]) <= 2, abs(delta("KROSS", c[1], c[0], nm)[0] / delta("KROSS", c[1], c[0], nm)[1]) <= 2) for c in set(pub_cells) | set(all_cells)}
acc["KURVS, union over ALL 24 (s, mu) cells"] = np.array([any(kv[float(p)][c][0] for c in all_cells) for p in ps])
acc["KURVS, union over published s x measured-gas mu (15 cells)"] = np.array([any(kv[float(p)][c][0] for c in pub_cells) for p in ps])
acc["KURVS AND KROSS, same cell, published s x measured-gas mu"] = np.array([any(kv[float(p)][c][0] and kv[float(p)][c][1] for c in pub_cells) for p in ps])
acc["KROSS, union over published s x measured-gas mu"] = np.array([any(kv[float(p)][c][1] for c in pub_cells) for p in ps])


def interval(mask):
    idx = np.where(mask)[0]
    if len(idx) == 0:
        return None
    # report the largest contiguous run containing p = 0 if any, else the overall min/max
    return float(ps[idx[0]]), float(ps[idx[-1]])


print(f"   {'constraint (2-sigma honest acceptance)':64s} allowed p range      a0(2.5)/a0(0) = {E25:.2f}^p")
RANGE = {}
for k, m in acc.items():
    iv = interval(m)
    RANGE[k] = iv
    if iv is None:
        print(f"   {k:64s} EMPTY")
    else:
        print(f"   {k:64s} [{iv[0]:+.2f}, {iv[1]:+.2f}]       [{E25 ** iv[0]:.2f}, {E25 ** iv[1]:.2f}]  ({iv[0] * math.log10(E25):+.2f} .. {iv[1] * math.log10(E25):+.2f} dex)")
DATA = ["Jeanneau deep refit (honest 0.272)", "ledger bTFR rows (4, honest)", "CFG198 route ii+iii slope CIs (SED masses)"]
def inter(keys):
    m = np.ones(len(ps), bool)
    for k in keys:
        m &= acc[k]
    return interval(m)
IV = {"A data only (Jeanneau deep + ledger bTFR + CFG198 SED routes)": inter(DATA),
      "B  A + Milgrom-17 Table I at FACE VALUE (zeta offset 0)": inter(DATA + ["Milgrom-17 Table I, offset on zeta_obs 0.00"]),
      "C  A + Milgrom-17 with zeta offset 0.18 (H(z)'s own acceptance offset)": inter(DATA + ["Milgrom-17 Table I, offset on zeta_obs 0.18"]),
      "D  A + Milgrom-17 with zeta offset 0.30 (D's acceptance offset)": inter(DATA + ["Milgrom-17 Table I, offset on zeta_obs 0.30"]),
      "E  C + KURVS AND KROSS in one published (s, mu) cell (fragile lean)": inter(DATA + ["Milgrom-17 Table I, offset on zeta_obs 0.18", "KURVS AND KROSS, same cell, published s x measured-gas mu"])}
print("\n   INTERSECTIONS of the honest rows (all listed must hold):")
for k, iv in IV.items():
    print(f"      {k:74s} p in [{iv[0]:+.2f}, {iv[1]:+.2f}]  ->  a0(2.5)/a0(0) in [{E25 ** iv[0]:.2f}, {E25 ** iv[1]:.2f}]  ({iv[0] * math.log10(E25):+.2f} .. {iv[1] * math.log10(E25):+.2f} dex)")
OUT["range_p"] = {k: v for k, v in RANGE.items()}; OUT["intersections"] = IV
pD, pH, pL = math.log(LAW["D"](2.5)) / math.log(E25), 1.0, math.log(LAW["LCDM-native"](2.5)) / math.log(E25)
print(f"   the named laws in this family: flat p = 0; LCDM-native p = {pL:.2f}; H(z) p = 1; particle horizon p = {pD:.2f} (D is only approximately a power of E: D/E^{pD:.2f} at z = 0.5, 1, 2.5: " + ", ".join(f"{LAW['D'](z) / Ez(z) ** pD:.2f}" for z in (0.5, 1.0, 2.5)) + ")")
IA, IB, IC, ID, IE = list(IV.values())
chk("A1 (declared, restated on the new rows) the UPPER edge of the allowed p: %.2f with the data rows alone (a0(2.5)/a0(0) <~ %.1f), %.2f with Milgrom at face value (<~ %.1f), %.2f / %.2f with a zeta offset 0.18 / 0.30; the H(z) law (p = 1) is inside A, C, D, E and outside B; the family edge of A sits at p = %.2f, essentially at D's own p = %.2f (D is accepted by the data-only rows by a hair, see A5)" % (IA[1], E25 ** IA[1], IB[1], E25 ** IB[1], IC[1], ID[1], IA[1], pD),
    IB[1] < 0.5 and 0.9 <= IC[1] <= 1.2 and 1.2 <= ID[1] <= 1.6 and abs(IA[1] - pD) < 0.1 and IA[0] < 0 < IA[1] and IB[0] < 0 < IB[1], f"A {IA}, B {IB}, C {IC}, D {ID}, E {IE}")
chk("A2 (declared expectation partly wrong, restated) the FALLING side: Jeanneau and the ledger do not bound it (p <= -1.5, grid edge) but CFG198's SED-mass slope CIs do, at p = %.2f (a0(2.5)/a0(0) >= %.2f): the record's T law (0.19 at z = 2.5, p = %.1f) lies beyond it" % (RANGE["CFG198 route ii+iii slope CIs (SED masses)"][0], E25 ** RANGE["CFG198 route ii+iii slope CIs (SED masses)"][0], math.log(LAW_T25 := tratio(2.5)) / math.log(E25)),
    RANGE["Jeanneau deep refit (honest 0.272)"][0] <= -1.45 and RANGE["ledger bTFR rows (4, honest)"][0] <= -1.45 and math.log(tratio(2.5)) / math.log(E25) < RANGE["CFG198 route ii+iii slope CIs (SED masses)"][0])
chk("A3 (declared) MUSE-DARK III at face value (p ~ 1.7) lies ABOVE the upper edge of the data-only intersection A and of C: the rise cannot be both the fundamental a0 and something the other honest rows allow", acc["[scenario] MUSE-DARK III at face value"].any() and (RANGE["[scenario] MUSE-DARK III at face value"][0] > IC[1]) and (RANGE["[scenario] MUSE-DARK III at face value"][0] > IA[1]),
    f"III p in {RANGE['[scenario] MUSE-DARK III at face value']}, rows A {IA}, C {IC}")
# ---- acceptance matrix for the NAMED laws (no shape-family proxy)
def accepts(fn):
    r = {}
    r["Jeanneau deep"] = abs(float(np.median([dlogM_P2(fn(z), y) for z, y in zip(zj, yj)])) - 0.140) <= 2 * 0.272
    r["ledger bTFR"] = all(abs(dlogM_P2(fn(z), y) - db) <= 2 * e for z, y, db, e in rows)
    sl_ = float(np.polyfit(zS, np.log10([fn(z) for z in zS]), 1)[0]); r["CFG198 ii+iii"] = ci_ii[0] <= sl_ <= ci_ii[1] and ci_iii[0] <= sl_ <= ci_iii[1]
    for d_ in (0.0, 0.18, 0.30):
        r[f"Milgrom off {d_:.2f}"] = chi_mil(fn, d_) <= 12.59
    r["MUSE-III headline"] = abs(math.log10(fn(0.87)) - lr3) <= 2 * s3
    nmv = f"tmp_{id(fn)}"
    LAWS[nmv] = fn
    r["KURVS&KROSS pub cell"] = any(abs(delta("KURVS", mu, s_, nmv)[0] / delta("KURVS", mu, s_, nmv)[1]) <= 2 and abs(delta("KROSS", mu, s_, nmv)[0] / delta("KROSS", mu, s_, nmv)[1]) <= 2 for s_ in (1.0, 1.42, 1.62, 1.69, 3.0) for mu in (0.67, 1.0, 1.5))
    return r
AM = {n: accepts(LAW[n]) for n in NM}
cols_ = list(next(iter(AM.values())).keys())
print("\n   ACCEPTANCE MATRIX (named laws, 2-sigma honest acceptance; 'Y' = not excluded):")
print("      " + f"{'law':12s}" + "".join(f"{c[:15]:>16s}" for c in cols_))
for n in NM:
    print("      " + f"{n:12s}" + "".join(f"{('Y' if AM[n][c] else 'x'):>16s}" for c in cols_))
OUT["acceptance"] = AM
# THIRD RUN (kept as z05_decisive_tests_thirdrun.out): my declared A5 said D is accepted by the KURVS&KROSS published cell; it is NOT (KURVS tolerates D at s ~ 1.6, KROSS does not at the same s, mu at 2 sigma), while H(z) and LCDM-native ARE accepted. Restated as computed.
chk("A5 (computed; one clause of the first declaration was wrong) no named law is accepted by all eight rows; MUSE-III's headline is accepted ONLY by D; the KURVS&KROSS published cell accepts H(z) and LCDM-native and rejects flat AND D; Milgrom's table rejects D at zeta offsets 0 and 0.18 (accepts it only at 0.30) and H(z) only at face value; flat is accepted by all three data-only rows and by Milgrom at offsets 0 and 0.18",
    all(not all(AM[n][c] for c in cols_) for n in NM)
    and [n for n in NM if AM[n]["MUSE-III headline"]] == ["D"]
    and AM["H(z)"]["KURVS&KROSS pub cell"] and AM["LCDM-native"]["KURVS&KROSS pub cell"] and not AM["flat"]["KURVS&KROSS pub cell"] and not AM["D"]["KURVS&KROSS pub cell"]
    and not AM["D"]["Milgrom off 0.00"] and not AM["D"]["Milgrom off 0.18"] and AM["D"]["Milgrom off 0.30"] and not AM["H(z)"]["Milgrom off 0.00"] and AM["H(z)"]["Milgrom off 0.18"]
    and all(AM["flat"][c] for c in ("Jeanneau deep", "ledger bTFR", "CFG198 ii+iii", "Milgrom off 0.00", "Milgrom off 0.18")), "")
# ---- shape-family cross-check D^q
Dq = lambda q: (lambda z, q=q: LAW["D"](z) ** q)
qs = np.round(np.arange(-1.5, 1.8001, 0.05), 3)
accq = {}
accq["Jeanneau"] = np.array([abs(float(np.median([dlogM_P2(LAW["D"](z) ** q, y) for z, y in zip(zj, yj)])) - 0.140) <= 2 * 0.272 for q in qs])
accq["ledger"] = np.array([all(abs(dlogM_P2(LAW["D"](z) ** q, y) - db) <= 2 * e for z, y, db, e in rows) for q in qs])
accq["CFG198 ii+iii"] = np.array([(lambda sl_: ci_ii[0] <= sl_ <= ci_ii[1] and ci_iii[0] <= sl_ <= ci_iii[1])(float(np.polyfit(zS, q * np.log10([LAW["D"](z) for z in zS]), 1)[0])) for q in qs])
accq["Milgrom 0.18"] = np.array([chi_mil(Dq(q), 0.18) <= 12.59 for q in qs])
mq = np.ones(len(qs), bool)
for m in accq.values(): mq &= m
idxq = np.where(mq)[0]
q_lo, q_hi = float(qs[idxq[0]]), float(qs[idxq[-1]])
print(f"\n   cross-check with the D-shaped family a0 = a0(0) D(z)^q, rows (Jeanneau, ledger, CFG198 ii+iii, Milgrom offset 0.18): q in [{q_lo:+.2f}, {q_hi:+.2f}] -> a0(2.5)/a0(0) in [{LAW['D'](2.5) ** q_lo:.2f}, {LAW['D'](2.5) ** q_hi:.2f}] ({q_lo * dexs['D']:+.2f} .. {q_hi * dexs['D']:+.2f} dex);  the E^p family with the same rows (row C): [{E25 ** IC[0]:.2f}, {E25 ** IC[1]:.2f}]")
OUT["Dq_range"] = [q_lo, q_hi]
upE = E25 ** IC[1]
upD = LAW["D"](2.5) ** q_hi
chk("A4 the UPPER edge of the allowed a0(2.5)/a0(0) agrees between the two shape families to within a factor 1.5 (E^p: %.2f, D^q: %.2f): the range is not an artefact of the shape family" % (upE, upD), max(upE, upD) / min(upE, upD) < 1.5)
# ---- mutations
print("\n--- mutations ---")
m_ok = acc["Jeanneau deep refit (honest 0.272)"].copy()
chk("M1 MUTATION (shrink the Jeanneau honest band from 0.272 to the stat 0.07): the allowed p range must SHRINK (the range is driven by the systematic budget, so the systematic is what limits the test)",
    np.array([abs(jd(p) - 0.140) <= 2 * 0.070 for p in ps]).sum() < m_ok.sum() - 4, f"{m_ok.sum()} -> {np.array([abs(jd(p) - 0.140) <= 2 * 0.070 for p in ps]).sum()} grid points")
def chi_mil_s(fn, delta_, sscale):
    tot = 0.0
    for z, R, V, zo, e, kind in TAB:
        x = (V * 1e3) ** 2 / (R * KPC_) / (1.2e-10 * fn(z)); zp = 1 / (1 + x)
        s_ = (e if kind == "err" else (e - zo)) * sscale
        p = (zp - (zo + delta_)) / s_
        tot += 0 if (kind == "lim" and zp <= zo + delta_) else p * p
    return tot
chk("M2 MUTATION (inflate every zeta_obs error x10, i.e. an unbounded model systematic): Milgrom's table then accepts every p up to 2 (the constraint switches off); at face value it does not", all(chi_mil_s(Ep(p), 0.0, 10.0) <= 12.59 for p in (0.0, 1.0, 1.36, 2.0)) and chi_mil_s(Ep(1.36), 0.0, 1.0) > 12.59)
chk("M3 MUTATION (flip the sign of the Jeanneau datum to -0.14): the allowed p range must move UP (rising laws favoured)", (lambda m: interval(m)[1] > RANGE["Jeanneau deep refit (honest 0.272)"][1])(np.array([abs(jd(p) + 0.140) <= 2 * 0.272 for p in ps])))
json.dump(dict(pass_=sum(ok), n=len(ok), **OUT), open("z05_results.json", "w"), indent=1, default=float)
print(f"\n{sum(ok)}/{len(ok)}")
sys.exit(0 if all(ok) else 1)
