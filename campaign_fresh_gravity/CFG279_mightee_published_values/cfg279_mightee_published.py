#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG279 -- the MIGHTEE-HI / LADUMA RAR paper (arXiv:2608.03576) read against FLAT, a0 ~ H(z) and the anchored slope, with CFG258's frozen rules; PUBLISHED VALUES ONLY.

Criteria frozen and committed before this script existed: FROZEN_CRITERIA.md (99aec4107); corrected before the first execution by FROZEN_CRITERIA_ADDENDUM_1.md (committed with this script).
Run: python3 cfg279_mightee_published.py ; SELFTEST=1 python3 ... (first) ; MUTATE=1 python3 ... (after the measurement run)
kappa = 1/2 is FITTED.  No verdict words.
"""
import os, sys, json, math, time, re, csv
sys.dont_write_bytecode = True
import numpy as np

TSTART = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
REPO = os.path.dirname(CFG)
sys.path.insert(0, os.path.join(CFG, "HZQ_common"))
import hzq_core as H

MUTATE = os.environ.get("MUTATE", "0") == "1"
SELFTEST = os.environ.get("SELFTEST", "0") == "1"
assert not (MUTATE and SELFTEST)
SFX = ("_MUTATE1" if MUTATE else "") + ("_SELFTEST" if SELFTEST else "")
LOG, CHK, NUM = [], [], {}


def P(s=""):
    print(s, flush=True); LOG.append(str(s))


def check(name, detail, ok, load_bearing=True):
    CHK.append((name, bool(ok), load_bearing))
    P(f"  [{'PASS' if ok else 'FAIL'}{'' if load_bearing else ' (not load-bearing)'}] {name}\n         {detail}")


P(__doc__.split("Run:")[0].strip())
if MUTATE: P("\n*** MUTATE=1: the MIGHTEE-only slope replaced by a world on the anchored slope ***")
if SELFTEST: P("\n*** SELFTEST: the MIGHTEE-only slope replaced by a world on FLAT ***")
TEX = os.path.join(os.path.dirname(REPO), "_external_data", "arxiv_src", "2608.03576", "main.tex")
tex = open(TEX, encoding="utf-8", errors="ignore").read()
compact = re.sub(r"\s+", "", tex)
P(f"paper source {os.path.basename(os.path.dirname(TEX))}/main.tex sha256 {H.sha(TEX)}; {len(tex)} characters")

# ----------------------------------------------------------------------------- inputs (frozen in the criteria, section 1; the paper's own numbers are never modified, only the fabricated worlds)
PAPER = dict(a0_all=(1.50, 0.05), a0_mig=(1.54, 0.11), a1_mig=(-1.60, 2.33), a0_anc=(1.15, 0.02), a1_anc=(5.23, 1.05), a1_btfr_mig=(-8.1, 2.3), a1_btfr_anc=(-6.3, 0.9))
IN = dict(PAPER)
if MUTATE:
    IN["a1_mig"] = (PAPER["a1_anc"][0] * PAPER["a0_mig"][0] / PAPER["a0_anc"][0], PAPER["a1_mig"][1])    # a world on the anchored slope b = 5.23/1.15
if SELFTEST:
    IN["a1_mig"] = (0.0, PAPER["a1_mig"][1])                                                              # a world on FLAT with the published error
SY = {"F": 0.0, "A": 1.255, "B": 4.012}                                     # CFG258's declared C0 E2 systematic scatter per unit z, frozen in the criteria (F = the formal width)
THR = 3.29
A0C = H.K4.A0["canonical"]                                                  # CFG258's canonical a0 (9.360324825e-11), its own definition B3 = A1 / A0[foot]
A0C10 = A0C / 1e-10
b3 = 5.23e-10 / A0C

# ----------------------------------------------------------------------------- C1: inputs found verbatim in the paper (whitespace-insensitive)
need = {"a0_all": r"a_0=(1.50\pm0.05)", "a0_mig": r"a_0=(1.54\pm0.11)", "a1_mig": r"a_1=(-1.60\pm2.33)", "a0_anc": r"a_0=(1.15\pm0.02)", "a1_anc": r"a_1=(5.23\pm1.05)",
        "a1_btfr_mig": r"a_1=(-8.1\pm2.3)", "a1_btfr_anc": r"a_1=(-6.3\pm0.9)", "diff_2p5": r"2.5$\sigma$level", "formal_5p0": r"formal$5.0\sigma$", "on_request": "availableonrequest"}
found = {k: (p in compact) for k, p in need.items()}
tabcomm = bool(re.search(r"^%\\input\{gbar_gobs_table\}", tex, re.M)) and bool(re.search(r"^%\\section\{Sample Data Table\}", tex, re.M))
check("C1 CONTROL: every input of the criteria section 1 is found verbatim in the paper's TeX; the Data-availability sentence says 'available on request'; the per-galaxy table's include line is commented out",
      f"found {found}; table commented out {tabcomm}", all(found.values()) and tabcomm)

# ----------------------------------------------------------------------------- C1b: the reported-only table (addendum section 3) found verbatim; the authors' tensions recomputed
TAB = [("MIGHTEE+LADUMA only", "varying", "RAR", -1.60, 2.33), ("MIGHTEE+LADUMA only", "varying", "bTFR inverse", -8.10, 2.41), ("MIGHTEE+LADUMA only", "varying", "bTFR direct", -11.42, 1.31),
       ("MIGHTEE+LADUMA only", "constant 0.6", "RAR", -4.64, 1.94), ("MIGHTEE+LADUMA only", "constant 0.6", "bTFR inverse", -5.48, 2.06), ("MIGHTEE+LADUMA only", "constant 0.6", "bTFR direct", -8.39, 1.03),
       ("MIGHTEE+LADUMA+SPARC", "varying", "RAR", 5.23, 1.05), ("MIGHTEE+LADUMA+SPARC", "varying", "bTFR inverse", -6.30, 0.94), ("MIGHTEE+LADUMA+SPARC", "varying", "bTFR direct", -7.09, 0.83),
       ("MIGHTEE+LADUMA+SPARC", "constant 0.6", "RAR", -4.80, 0.76), ("MIGHTEE+LADUMA+SPARC", "constant 0.6", "bTFR inverse", -8.84, 0.71), ("MIGHTEE+LADUMA+SPARC", "constant 0.6", "bTFR direct", -9.41, 0.63)]
tab_found = [f"{a1:.2f}\\pm{e:.2f}" in compact for (_, _, _, a1, e) in TAB]
SUBS = [("whole sample, direct photometry", 130, 1.50, 0.05, r"All&Direct&130&$1.50\pm0.05$"), ("whole sample, Sersic photometry", 130, 1.48, 0.04, r"&130&$1.48\pm0.04$"),
        ("well-behaved, direct", 61, 1.80, 0.08, r"Direct&61&$1.80\pm0.08$"), ("less well-behaved, direct", 69, 1.31, 0.06, r"Direct&69&$1.31\pm0.06$"), ("COSMOS reference, Sersic", 19, 1.69, 0.13, r"&19&$1.69\pm0.13$")]
sub_found = [s[4] in compact for s in SUBS]
tens_pub = {("MIGHTEE+LADUMA only", "varying"): 2.0, ("MIGHTEE+LADUMA only", "constant 0.6"): 0.3, ("MIGHTEE+LADUMA+SPARC", "varying"): 8.2, ("MIGHTEE+LADUMA+SPARC", "constant 0.6"): 3.9}
tens_rec = {}
for key in tens_pub:
    r_ = [t for t in TAB if (t[0], t[1]) == key and t[2] == "RAR"][0]; b_ = [t for t in TAB if (t[0], t[1]) == key and t[2] == "bTFR inverse"][0]
    tens_rec[key] = abs(r_[3] - b_[3]) / math.hypot(r_[4], b_[4])
sig5 = 5.23 / 1.05; sig24 = 4.64 / 1.94
check("C1b CONTROL: the twelve table values and the five sub-sample rows are found verbatim; the authors' four RAR-bTFR tensions are reproduced by quadrature of independent errors to 0.1 sigma, their 'formal 5.0 sigma' (a1/sigma) to 0.05 and 'tentative 2.4 sigma' to 0.1",
      f"table found {sum(tab_found)}/12; sub-samples found {sum(sub_found)}/5; tensions recomputed " + ", ".join(f"{v:.2f} (published {tens_pub[k]})" for k, v in tens_rec.items()) + f"; a1/sigma {sig5:.3f} (5.0), {sig24:.3f} (2.4)",
      all(tab_found) and all(sub_found) and all(abs(tens_rec[k] - tens_pub[k]) <= 0.1 for k in tens_pub) and abs(sig5 - 5.0) <= 0.05 and abs(sig24 - 2.4) <= 0.1)

# ----------------------------------------------------------------------------- C2: arithmetic against CFG258; the kernel statement of the addendum
c258 = json.load(open(os.path.join(CFG, "CFG258_mightee_a0z_preflight", "cfg258_preflight_results.json")))
pa = c258["part_a"]["canonical"]
Ez = lambda z: math.sqrt(0.315 * (1 + z) ** 3 + 0.685)
d2 = 0.0
for zz in ("0.02", "0.055", "0.09"):
    z_ = float(zz); d2 = max(d2, abs(1 + b3 * z_ - pa[zz]["f_iii"]), abs(Ez(z_) - pa[zz]["f_rival"]))
dec = c258["decisions"]["C0"]; sd_stat, sdA, sdB = dec["E2|ANCH|A"]["sd_stat"], dec["E2|ANCH|A"]["sd_sys"], dec["E2|ANCH|B"]["sd_sys"]
Yp = H.K4.Y_PEAK_RAR
ylo = np.logspace(-3, math.log10(Yp), 20001); yhi = np.logspace(math.log10(Yp), 3, 20001)
rel_lo = float(np.max(np.abs(H.NU(ylo) / H.K4.nu_rar(ylo) - 1))); rel_hi_arr = np.abs(H.NU(yhi) / H.K4.nu_rar(yhi) - 1); rel_hi = float(np.max(rel_hi_arr)); y_hi = float(yhi[int(np.argmax(rel_hi_arr))])
check("C2 CONTROL (amended): the law arithmetic reproduces CFG258's committed f_iii and f_rival at z = 0.02, 0.055, 0.09 (1e-9, CFG258's own a0 constant); its C0 E2 systematic scatters equal the frozen 1.255 and 4.012 (5e-4); nu_mono equals the exponential RAR kernel to 1e-3 relative for y <= Y_PEAK (the as-frozen 1e-9 clause is replaced, addendum 2a)",
      f"max |difference| {d2:.1e}; sigma_sys A {sdA:.4f}, B {sdB:.4f}; sigma_stat {sd_stat:.4f}; |nu_mono/nu_rar - 1| max {rel_lo:.2e} for y <= {Yp:.3f}; above it up to {rel_hi:.2e} (at y = {y_hi:.1f}): the s column is a CONVENTION",
      d2 < 1e-9 and abs(sdA - 1.255) < 5e-4 and abs(sdB - 4.012) < 5e-4 and rel_lo <= 1e-3)

# ----------------------------------------------------------------------------- statistics
def ratio_err(num, den):
    """b = num/den with independent errors (no covariance: the paper's is unavailable)"""
    (n, en), (d, ed) = num, den
    return n / d, math.sqrt((en / d) ** 2 + (n * ed / d ** 2) ** 2)


b_E2, sb_E2 = ratio_err(IN["a1_mig"], IN["a0_mig"])
b_AN, sb_AN = ratio_err(PAPER["a1_anc"], PAPER["a0_anc"])
rng = np.random.default_rng(279)
mc = rng.normal(*IN["a1_mig"], 1_000_000) / rng.normal(*IN["a0_mig"], 1_000_000)
check("C3 CONTROL: the propagated error of b = a1/a0 equals a 10^6-draw Monte Carlo (independent normals) to 2 %", f"propagated {sb_E2:.4f}; Monte Carlo SD {float(np.std(mc)):.4f}", abs(sb_E2 / float(np.std(mc)) - 1) < 0.02)
check("M4 CONTROL: the first 18 columns of the points file equal chart_a0z_points.csv's header", f"{H.chart_header_check()}", H.chart_header_check())

LAWS = {"FLAT": 0.0, "RIVAL": 0.4725, "RIVAL (CFG258 C0 E2 slope 0.588)": float(dec["E2|RIVAL|A"]["delta"]), "ANCH (paper units)": b_AN, "ANCH (CFG258 canonical b3)": b3}
P("\nA. THE ARITHMETIC (a(z)/a(0), exact)")
for zz in (0.02, 0.055, 0.09):
    P(f"   z = {zz}: FLAT 1; RIVAL {Ez(zz):.4f}; ANCH (paper units, b = {b_AN:.3f}) {1 + b_AN * zz:.3f}; ANCH (CFG258 canonical b3 = {b3:.3f}) {1 + b3 * zz:.3f}")
P(f"\nB. THE WITHIN-SAMPLE SLOPE (MIGHTEE+LADUMA alone; the E2 analogue): a1 = {IN['a1_mig'][0]:+.3f} +- {IN['a1_mig'][1]:.2f}, a0 = {IN['a0_mig'][0]:.2f} +- {IN['a0_mig'][1]:.2f}  ->  b = a1/a0 = {b_E2:+.4f} +- {sb_E2:.4f} per unit z")
P(f"   THE ANCHORED FIT (SPARC as the z = 0 anchor; the E1 analogue): a1 = {PAPER['a1_anc'][0]:+.2f} +- {PAPER['a1_anc'][1]:.2f}, a0 = {PAPER['a0_anc'][0]:.2f} +- {PAPER['a0_anc'][1]:.2f}  ->  b = {b_AN:+.4f} +- {sb_AN:.4f} per unit z")
P("\nC. PULLS OF THE WITHIN-SAMPLE SLOPE AGAINST EACH LAW (width: F = formal sigma_b; A = sigma_b + level-A systematic; B = + level-B systematic; DISFAVOURED iff |pull| >= 3.29)")
RES = {}
for name, bl in LAWS.items():
    row = {}
    for lv, sy in SY.items():
        sig = math.hypot(sb_E2, sy); pull = (b_E2 - bl) / sig
        row[lv] = dict(sigma=sig, pull=pull, label="DISFAVOURED" if abs(pull) >= THR else "CONSISTENT")
    RES[name] = row
    P(f"   {name:34s} b_law {bl:+.4f}: " + "; ".join(f"{lv} {row[lv]['pull']:+.3f} sigma ({row[lv]['label']})" for lv in SY))
P("\nD. SEPARATIONS BETWEEN LAWS (Delta / sigma_tot; NOT POSSIBLE iff < 3.29)")
SEP = {}
for a_, b_ in (("FLAT", "RIVAL"), ("FLAT", "ANCH (paper units)"), ("RIVAL", "ANCH (paper units)")):
    SEP[f"{a_} vs {b_}"] = {lv: abs(LAWS[a_] - LAWS[b_]) / math.hypot(sb_E2, sy) for lv, sy in SY.items()}
    P(f"   {a_} vs {b_}: Delta {abs(LAWS[a_] - LAWS[b_]):.4f}; " + "; ".join(f"{lv}: {v:.3f} sigma ({'POSSIBLE' if v >= THR else 'NOT POSSIBLE'})" for lv, v in SEP[f'{a_} vs {b_}'].items()))
P("\nE. THE ANCHORED FIT'S OWN PULLS (E1 analogue; reported)")
E1P = {name: (b_AN - bl) / sb_AN for name, bl in LAWS.items() if name in ("FLAT", "RIVAL")}
for name, v in E1P.items(): P(f"   anchored slope against {name}: {v:+.3f} sigma")
off_dex, off_err = math.log10(IN["a0_mig"][0] / PAPER["a0_anc"][0]), math.sqrt((IN["a0_mig"][1] / IN["a0_mig"][0]) ** 2 + (PAPER["a0_anc"][1] / PAPER["a0_anc"][0]) ** 2) / math.log(10)
zbar = 0.055
P(f"\nF. THE SAMPLE OFFSET: a0(MIGHTEE-only intercept) / a0(SPARC-anchored z = 0 value) = {IN['a0_mig'][0] / PAPER['a0_anc'][0]:.4f} = {off_dex:+.4f} +- {off_err:.4f} dex; ANCH implies {math.log10(1 + b_AN * zbar):+.4f} dex at z = {zbar} (CFG258's canonical b3: {math.log10(1 + b3 * zbar):+.4f}); CFG258's mimic table at z = 0.055: M* scale 0.107 dex, distances 0.047 dex, velocities 0.023 dex, sample mix 0.116 dex")
P(f"   the paper's own bTFR-derived a1 (inverse fit, reported only): MIGHTEE+LADUMA {PAPER['a1_btfr_mig'][0]:+.1f} +- {PAPER['a1_btfr_mig'][1]:.1f}; with SPARC {PAPER['a1_btfr_anc'][0]:+.1f} +- {PAPER['a1_btfr_anc'][1]:.1f}; the paper states the MIGHTEE-only and anchored RAR fits differ at 2.5 sigma")
P("\nG. LEVELS FOR THE CHART (published; the authors' M/L modelling and exponential-RAR kernel; s = a0 / " + f"{A0C10:.7f}" + " is a CONVENTION, not an a0 implied through nu_mono)")
LEV = [("whole sample, z-averaged", PAPER["a0_all"], 0.055, 0.055), ("MIGHTEE+LADUMA-only fit intercept (z = 0 extrapolation)", IN["a0_mig"], 0.0, 0.004), ("SPARC-anchored z = 0 value", PAPER["a0_anc"], 0.0, 0.0)]
for nm, (v, e), z_, zs_ in LEV: P(f"   {nm}: a0 = {v:.2f} +- {e:.2f} e-10 -> s = {v / A0C10:.4f} +- {e / A0C10:.4f}")

# ----------------------------------------------------------------------------- I. reported-only block (addendum section 3); no decision attached
P("\nI. REPORTED ONLY (no decision attached): the authors' Table of a1 and their other fit numbers; arithmetic on published values")
REP = []
for (smp, ups, rel, a1, e) in TAB:
    pull0 = a1 / e; REP.append(dict(sample=smp, upsilon=ups, relation=rel, a1=a1, err=e, pull_vs_a1_zero=pull0))
    P(f"   {smp:22s} {ups:13s} {rel:13s} a1 = {a1:+7.2f} +- {e:.2f}   (a1/sigma = {pull0:+.2f})")
P("   the authors' four RAR-bTFR tensions recomputed from the table: " + "; ".join(f"{k[0]}, {k[1]}: {v:.2f} (published {tens_pub[k]})" for k, v in tens_rec.items()))
sp = {"split_dex": math.log10(1.80 / 1.31), "split_err": math.sqrt((0.08 / 1.80) ** 2 + (0.06 / 1.31) ** 2) / math.log(10)}
P("   sub-sample levels (a0, 1e-10 m/s2): " + "; ".join(f"{n} N={N} {v:.2f} +- {e:.2f}" for (n, N, v, e, _) in SUBS) + f"; well-behaved vs less well-behaved: {sp['split_dex']:+.4f} +- {sp['split_err']:.4f} dex (the same galaxies' photometric-consistency split)")
P("   the delta-family kernel fit gives a0 = 1.86 +- 0.06 (delta = 4.10): a different kernel, not comparable with the exponential-RAR levels")
d_a1 = (PAPER["a1_mig"][0] - PAPER["a1_anc"][0]) / math.hypot(PAPER["a1_mig"][1], PAPER["a1_anc"][1]); d_a0 = (PAPER["a0_mig"][0] - PAPER["a0_anc"][0]) / math.hypot(PAPER["a0_mig"][1], PAPER["a0_anc"][1])
z_cross = (PAPER["a0_mig"][0] - PAPER["a0_anc"][0]) / (PAPER["a1_anc"][0] - PAPER["a1_mig"][0])
P(f"   MIGHTEE-only minus anchored, independent-error quadrature (the authors state 2.5 sigma for the difference, method not given): a1 {d_a1:+.2f} sigma, a0 {d_a0:+.2f} sigma")
P(f"   the two fits' central values cross at z = {z_cross:.4f}: a(z) = {PAPER['a0_mig'][0]:.2f} {PAPER['a1_mig'][0]:+.2f} z  vs  {PAPER['a0_anc'][0]:.2f} {PAPER['a1_anc'][0]:+.2f} z; at z = {zbar}: {PAPER['a0_mig'][0] + PAPER['a1_mig'][0] * zbar:.3f} vs {PAPER['a0_anc'][0] + PAPER['a1_anc'][0] * zbar:.3f} (central values; errors need the paper's covariance); at z = 0: {PAPER['a0_mig'][0]:.2f} vs {PAPER['a0_anc'][0]:.2f}; at z = 0.09: {PAPER['a0_mig'][0] + PAPER['a1_mig'][0] * 0.09:.3f} vs {PAPER['a0_anc'][0] + PAPER['a1_anc'][0] * 0.09:.3f}")
NUM.update(inputs={k: list(v) for k, v in IN.items()}, b_E2=[b_E2, sb_E2], b_ANCH=[b_AN, sb_AN], b3_cfg258=b3, laws=LAWS, pulls=RES, separations=SEP, e1_pulls=E1P, offset_dex=[off_dex, off_err], levels_widths=SY,
           found=found, kernel=dict(rel_max_below_peak=rel_lo, rel_max_above_peak=rel_hi, y_at_max_above=y_hi, Y_PEAK=Yp), reported_only=dict(table=REP, tensions_recomputed={f"{k[0]}|{k[1]}": v for k, v in tens_rec.items()}, tensions_published={f"{k[0]}|{k[1]}": v for k, v in tens_pub.items()},
           subsamples=[dict(name=n, N=N, a0=v, err=e) for (n, N, v, e, _) in SUBS], well_vs_less_dex=[sp["split_dex"], sp["split_err"]], mig_minus_anch_sigma=dict(a1=d_a1, a0=d_a0), z_cross=z_cross))

# ----------------------------------------------------------------------------- points file (chart shape; published levels)
cols = H.CHART_HEADER + ["b_per_unit_z", "b_err", "pull_FLAT_formal", "pull_RIVAL_formal", "pull_ANCH_formal", "pull_FLAT_B", "pull_ANCH_B", "limit", "quality"]
rows = []
for nm, (v, e), z_, zs_ in LEV:
    s_, es = v / A0C10, e / A0C10
    ex = [f"{b_E2:.4f}", f"{sb_E2:.4f}", f"{RES['FLAT']['F']['pull']:.3f}", f"{RES['RIVAL']['F']['pull']:.3f}", f"{RES['ANCH (paper units)']['F']['pull']:.3f}", f"{RES['FLAT']['B']['pull']:.3f}", f"{RES['ANCH (paper units)']['B']['pull']:.3f}"] if "intercept" in nm else [""] * 7
    rows.append(["CFG279", f"MIGHTEE-HI paper: {nm}", "published fit (authors' M/L, exponential RAR; not our estimator)", f"{z_:.3f}", f"{zs_:.3f}", 0, f"{s_:.4f}", f"{v:.4f}", f"{s_ - es:.4f}", f"{s_ + es:.4f}", f"{s_ - 2 * es:.4f}", f"{s_ + 2 * es:.4f}", "", "", 0, "", "", 0, *ex,
                 "published level and fit result; the per-galaxy data are not public", f"s = a0 / a0_canonical is a convention (the published a0 is an exponential-RAR a0, not implied through nu_mono); z = 0.055 is CFG258's design mean, not a measured sample mean; the paper's sub-samples span a0 1.31-1.80; the within-sample slope is {b_E2:+.2f} +- {sb_E2:.2f} per unit z"])
with open(os.path.join(HERE, f"cfg279_points{SFX}.csv"), "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(cols); [w.writerow(r) for r in rows]
P(f"\n  points written: cfg279_points{SFX}.csv ({len(rows)} rows)")

# ----------------------------------------------------------------------------- reactivity / selftest (addendum 2c) and hand estimates
if MUTATE:
    pa_ = {lv: RES["ANCH (paper units)"][lv] for lv in SY}
    ok_a = all(abs(pa_[lv]["pull"]) < 1e-9 and pa_[lv]["label"] == "CONSISTENT" for lv in SY)
    ok_b = abs(RES["FLAT"]["F"]["pull"] - 2.9389) <= 0.005
    check("M2a MUTATE=1 (amended): the pull against ANCH is 0 at every width (1e-9), CONSISTENT", f"{[round(pa_[lv]['pull'], 12) for lv in SY]}", ok_a)
    check("M2b MUTATE=1 (amended): the formal-width pull against FLAT equals the frozen hand arithmetic +2.9389 (0.005); it is below 3.29", f"pull FLAT {RES['FLAT']['F']['pull']:+.4f} ({RES['FLAT']['F']['label']})", ok_b)
    rp = os.path.join(HERE, "cfg279_results.json")
    if os.path.exists(rp):
        real = json.load(open(rp))["numbers"]["pulls"]
        flipped = real["ANCH (paper units)"]["F"]["label"] == "DISFAVOURED" and RES["ANCH (paper units)"]["F"]["label"] == "CONSISTENT"
        moved = RES["FLAT"]["F"]["pull"] - real["FLAT"]["F"]["pull"]
        check("M2c MUTATE=1 (amended): against the real run the ANCH label flips DISFAVOURED -> CONSISTENT at the formal width and the FLAT pull moves by >= 3.0 sigma", f"real ANCH {real['ANCH (paper units)']['F']['label']} ({real['ANCH (paper units)']['F']['pull']:+.3f}) -> {RES['ANCH (paper units)']['F']['label']}; real FLAT pull {real['FLAT']['F']['pull']:+.3f} -> {RES['FLAT']['F']['pull']:+.3f} (moved {moved:+.3f})", flipped and moved >= 3.0)
    else:
        check("M2c MUTATE=1: the real run's results are not present (run the measurement first)", "not evaluated", False)
    check("M2-as-frozen: in a world on the anchored slope the within-sample slope is DISFAVOURED against FLAT at the formal width", f"pull FLAT {RES['FLAT']['F']['pull']:+.4f} ({RES['FLAT']['F']['label']}); expected FAIL by arithmetic (2.94 < 3.29), addendum 2c", RES["FLAT"]["F"]["label"] == "DISFAVOURED", load_bearing=False)
elif SELFTEST:
    ok_a = all(abs(RES["FLAT"][lv]["pull"]) < 1e-9 and RES["FLAT"][lv]["label"] == "CONSISTENT" for lv in SY)
    ok_b = abs(RES["ANCH (paper units)"]["F"]["pull"] - (-3.0059)) <= 0.005 and RES["ANCH (paper units)"]["F"]["label"] == "CONSISTENT"
    ok_c = abs(RES["RIVAL"]["F"]["pull"] - (-0.3123)) <= 0.005
    check("S1 SELFTEST (amended): the pull against FLAT is 0 at every width (1e-9), CONSISTENT", f"{[round(RES['FLAT'][lv]['pull'], 12) for lv in SY]}", ok_a)
    check("S2 SELFTEST (amended): the formal-width pull against ANCH equals the frozen hand arithmetic -3.0059 (0.005) and the label is CONSISTENT at 3.29", f"pull ANCH {RES['ANCH (paper units)']['F']['pull']:+.4f} ({RES['ANCH (paper units)']['F']['label']})", ok_b)
    check("S3 SELFTEST (amended): the formal-width pull against RIVAL equals the frozen hand arithmetic -0.3123 (0.005)", f"pull RIVAL {RES['RIVAL']['F']['pull']:+.4f}", ok_c)
    check("S-as-frozen: in a world on FLAT the within-sample slope is DISFAVOURED against ANCH at the formal width", f"pull ANCH {RES['ANCH (paper units)']['F']['pull']:+.4f} ({RES['ANCH (paper units)']['F']['label']}); expected FAIL by arithmetic (3.01 < 3.29), addendum 2c", RES["ANCH (paper units)"]["F"]["label"] == "DISFAVOURED", load_bearing=False)
else:
    he = {"HE1": bool(all(abs(RES[k][lv]["pull"]) < 1.0 for k in ("FLAT", "RIVAL") for lv in SY)),
          "HE2": bool(all(v < 1.0 for v in SEP["FLAT vs RIVAL"].values())),
          "HE3": bool(RES["ANCH (paper units)"]["F"]["pull"] <= -THR and all(abs(RES["ANCH (paper units)"][lv]["pull"]) < THR for lv in ("A", "B"))),
          "HE4": bool(abs(off_dex - 0.116) <= 0.02 and off_err <= 0.04)}
    P("\nHAND ESTIMATES (frozen in the criteria section 7), scored")
    P(f"   HE1: |pull| of the within-sample slope against FLAT and RIVAL < 1 at every width: {'hit' if he['HE1'] else 'MISS (kept as it falls)'} (FLAT {[round(RES['FLAT'][lv]['pull'], 3) for lv in SY]}, RIVAL {[round(RES['RIVAL'][lv]['pull'], 3) for lv in SY]})")
    P(f"   HE2: FLAT vs RIVAL separation < 1 sigma at every width: {'hit' if he['HE2'] else 'MISS (kept as it falls)'} ({[round(v, 3) for v in SEP['FLAT vs RIVAL'].values()]})")
    P(f"   HE3: ANCH disfavoured at the formal width (pull {RES['ANCH (paper units)']['F']['pull']:+.3f} <= -3.29) and not at levels A ({RES['ANCH (paper units)']['A']['pull']:+.3f}) and B ({RES['ANCH (paper units)']['B']['pull']:+.3f}): {'hit' if he['HE3'] else 'MISS (kept as it falls)'}")
    P(f"   HE4: the sample offset {off_dex:+.4f} +- {off_err:.4f} dex within 0.02 dex of CFG258's sample-mix offset 0.116 and its error <= 0.04: {'hit' if he['HE4'] else 'MISS (kept as it falls)'}")
    P("   HE5: C1-C3 pass in this run if no load-bearing FAIL is listed above; the MUTATE=1 and SELFTEST parts are scored from their own runs in the README (the as-frozen clauses fail by arithmetic: addendum 2c)")
    NUM["hand_estimates"] = he

nf = sum(1 for _, ok, lb in CHK if lb and not ok)
P(f"\n{sum(ok for _, ok, _ in CHK)}/{len(CHK)} checks pass; load-bearing failures: {nf}   ({time.time() - TSTART:.0f} s)")
open(os.path.join(HERE, f"cfg279{SFX}.out"), "w").write("\n".join(LOG).replace(REPO, "<repo>") + "\n")
json.dump(dict(mutate=MUTATE, selftest=SELFTEST, checks=[dict(name=n, ok=ok, load_bearing=lb) for n, ok, lb in CHK], numbers=H.jc(NUM)), open(os.path.join(HERE, f"cfg279{SFX}_results.json"), "w"), indent=1)
sys.exit(1 if nf else 0)
