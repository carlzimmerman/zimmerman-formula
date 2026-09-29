#!/usr/bin/env python3
"""B1 -- Multiple Point Principle (Bennett-Nielsen) confronted with lane Y1's validated Planck-scale couplings.  Pre-registered in B1_PREREGISTRATION.md (incl. Amendment 1).

Sources (all read in the primary text; see B1_SOURCE_LEDGER.md):
  [BN93]  D.L. Bennett, H.B. Nielsen, hep-ph/9311321   (SU(2), SU(3): triple points, formulae, Tables 3-4)
  [BT96]  D.L. Bennett, thesis, hep-ph/9607341          (all three couplings: Tables 4,5,12,13,14; eqs 345-351)
  [BN96]  D.L. Bennett, H.B. Nielsen, hep-ph/9607278    (journal paper; abstract quotes 1/alpha_1(M_P) = 56 +- 5; same Tables 7,8,9)

Run:    python3 b1_mpp_confrontation.py            (exit 0 iff all declared internal checks pass; the verdict is REPORTED, not asserted)
MUTATE: python3 b1_mpp_confrontation.py MUTATE     (the U(1) weakening factor ~6.5 is replaced by the naive N_gen = 3 in the conversion; the U(1) status and the
                                                    route verdict MUST change: exit 1 if the control fires, exit 3 if it does not)
"""
import sys
sys.dont_write_bytecode = True
import os
import math

HERE = os.path.dirname(os.path.abspath(__file__))
for sub in ("Y1_running_precision", "B_rg_asymptotic_safety", "N1_joint_couplings", "U3_invented_uv_boundary", "D_calibration_bar"):
    sys.path.insert(0, os.path.join(HERE, "..", sub))
import y1_lib as L

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
FAILED = []
PI = math.pi
MP = 1.22089e19
NGEN = 3
NSIG_PASS = 2.0          # criterion 2
INFORMATIVE_FRAC = 0.05  # criterion 3
Y1_EXPECTED = (55.234, 49.203, 52.971)
Y1_REL = (0.0023, 0.00021, 0.0012)


def chk(tag, ok, detail=""):
    if not ok:
        FAILED.append(tag)
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}")


# ---------------------------------------------------------------- transcribed primary-source data
# Lattice triple points (graphical extraction by the authors from published figures) [BN93 sec.5; BT96 sec.6.7]
TRIPLE = {"SU2": dict(N=2, b_adj=2.4, s_adj=0.05, b_f=0.54, s_f=0.10), "SU3": dict(N=3, b_adj=5.4, s_adj=0.05, b_f=0.8, s_f=0.20)}
# Printed per-group results [BN93 Tables 3,4; BT96 Tables 4,5]: 1/alpha_crit,cont (not exponentiated, exponentiated), '+-1' stated
PRINTED_PER_GROUP = {"SU2": (15.7, 16.5), "SU3": (17.7, 18.9)}
# Printed Planck-scale predictions [BT96 Table 13 / BN96 Table 8, 'continuum corrected continuum limit'] and stated absolute uncertainties [BT96/BN96 Table 14 first & second set]
PRINTED_PLANCK = {"SU2": 49.5, "SU3": 56.7}
STATED_SIG = {"SU2": (6.0, 3.5), "SU3": (6.0, 6.0)}
# Papers' own 'experimental' values extrapolated with a one-loop-type desert (Table 13): 1/alpha_Y, 1/alpha_2, 1/alpha_3 at M_Planck
PAPER_EXPT = {"Y": 54.8, "SU2": 49.2, "SU3": 53.6}
# U(1) Table 12 of [BT96] = Table 7 of [BN96]: (label, action, dgamma_eff_corr, alpha_cont, 1/alpha_cont, enh(tau=0.79), enh(tau=1), pred(tau=0.79), pred(tau=1), starred)
U1_ROWS = [
    ("Z2 only", "Wilson", 0.0600, 0.1220, 8.196, 6.677, 6.535, 54.7, 53.6, False),
    ("Z2+Z3", "Wilson", 0.1094, 0.1031, 9.697, 6.826, 6.653, 66.2, 64.5, False),
    ("(Z2+Z3)/2", "Wilson", 0.05615, 0.1239, 8.072, 6.662, 6.523, 53.8, 52.7, True),
    ("Z2/2+Z3", "Wilson", 0.08108, 0.1129, 8.854, 6.748, 6.591, 59.7, 58.4, True),
    ("Z2 only", "Villain", 0.04318, 0.1217, 8.219, 6.441, 6.348, 52.9, 52.2, False),
    ("Z2+Z3", "Villain", 0.08119, 0.09424, 10.61, 6.529, 6.418, 69.3, 68.1, False),
    ("(Z2+Z3)/2", "Villain", 0.04044, 0.1241, 8.055, 6.432, 6.341, 51.8, 51.1, True),
    ("Z2/2+Z3", "Villain", 0.05941, 0.1087, 9.204, 6.483, 6.382, 59.7, 58.7, True),
]
U1_SIG_A, U1_SIG_B = 4.5, 3.5        # stated absolute Planck-scale uncertainties, viewpoint a (8%) and b (6.4%)  [BT96 sec.9; BN96 sec.6]
U1_B_CENTRE = 59.7                    # viewpoint b: the '1/2 Z2 + Z3' row (102.8 at M_Z minus the 43.1 running)
LOW = dict(a_MZ_U1=99.4, a_MZ_SU2=29.2, delta=8.2, delta_sig=0.3, total=136.8, total_sig=9.0)
ALPHA0_INV = 137.035999177


def per_group(N, b_adj, b_f, expo):
    """1/alpha_crit,cont per SU(N) group from the printed formulae: 1/alpha = 4 pi sum_r C_r/(N^2-1) beta_r (1 - pi C_r alpha_full)   [BN93 eqs (4),(34),(35),(38),(39); BT96 (219)-(222)]"""
    C_adj, C_f = N, (N * N - 1) / (2.0 * N)
    full = 4 * PI * (C_adj * b_adj + C_f * b_f) / (N * N - 1)
    a_full = 1.0 / full
    if expo:
        fa, ff = math.exp(-PI * C_adj * a_full), math.exp(-PI * C_f * a_full)
    else:
        fa, ff = 1 - PI * C_adj * a_full, 1 - PI * C_f * a_full
    return 4 * PI * (C_adj * b_adj * fa + C_f * b_f * ff) / (N * N - 1), full


def derived_sigma(key):
    """SECONDARY uncertainty: quote the printed Monte Carlo errors on the two triple-point betas, propagate through the exponentiated formula,
    add the exponentiated-minus-not spread as one sigma, multiply by N_gen."""
    t = TRIPLE[key]
    base, _ = per_group(t["N"], t["b_adj"], t["b_f"], True)
    d_adj = per_group(t["N"], t["b_adj"] * (1 + t["s_adj"]), t["b_f"], True)[0] - base
    d_f = per_group(t["N"], t["b_adj"], t["b_f"] * (1 + t["s_f"]), True)[0] - base
    non = per_group(t["N"], t["b_adj"], t["b_f"], False)[0]
    spread = base - non
    return NGEN * math.sqrt(d_adj ** 2 + d_f ** 2 + spread ** 2), (NGEN * abs(d_adj), NGEN * abs(d_f), NGEN * abs(spread))


def status(pred, sig, target, sig_t):
    z = (pred - target) / math.sqrt(sig ** 2 + sig_t ** 2)
    frac = sig / pred
    if abs(z) <= NSIG_PASS:
        return ("PASS-INFORMATIVE" if frac <= INFORMATIVE_FRAC else "PASS-WEAK"), z, frac
    return "FAIL", z, frac


def analyse(targets, sig_t, mut):
    """Returns the result dict for either the real conversion or the mutated one."""
    out = {}
    enh_used = lambda e: (3.0 if mut else e)          # MUTATE: U(1) weakening factor replaced by the naive N_gen = 3
    # U(1) central under viewpoint a: mean of the four starred rows (tau = 0.79); real run uses the PRINTED predictions (Amendment 1), mutated run rebuilds them with enh -> 3
    star = [r for r in U1_ROWS if r[9]]
    if mut:
        pa = sum(r[4] * enh_used(r[5]) for r in star) / len(star)
        pb = [r for r in star if r[0] == "Z2/2+Z3" and r[1] == "Wilson"][0][4] * enh_used(6.748)
    else:
        pa = sum(r[7] for r in star) / len(star)
        pb = U1_B_CENTRE
    cent = {"Y": pa, "SU2": PRINTED_PLANCK["SU2"], "SU3": PRINTED_PLANCK["SU3"]}
    prim = {"Y": U1_SIG_A, "SU2": math.hypot(*STATED_SIG["SU2"]), "SU3": math.hypot(*STATED_SIG["SU3"])}
    sec = {"Y": U1_SIG_B, "SU2": derived_sigma("SU2")[0], "SU3": derived_sigma("SU3")[0]}
    cent_sec = dict(cent)
    cent_sec["Y"] = pb
    for i, k in enumerate(("Y", "SU2", "SU3")):
        s1, z1, f1 = status(cent[k], prim[k], targets[i], sig_t[i])
        s2, z2, f2 = status(cent_sec[k], sec[k], targets[i], sig_t[i])
        robust = (s1 != "FAIL" and s2 != "FAIL")
        out[k] = dict(pred=cent[k], sig=prim[k], z=z1, status=s1, frac=f1, pred2=cent_sec[k], sig2=sec[k], z2=z2, status2=s2, frac2=f2, robust=robust)
    nfail = sum(out[k]["status"] == "FAIL" for k in out)
    npass = 3 - nfail
    if nfail >= 2:
        route = "ROUTE FAILS"
    elif nfail == 0:
        route = "ROUTE PASSES (all three couplings within 2 sigma of the stated MPP uncertainty)" + (" -- every pass is WEAK" if all(out[k]["status"] == "PASS-WEAK" for k in out) else "")
    else:
        route = "ROUTE MIXED (one coupling fails)"
    out["route"] = route
    out["sig_low"] = math.sqrt(prim["Y"] ** 2 + prim["SU2"] ** 2)
    out["shift_low"] = (cent["Y"] - targets[0]) + (cent["SU2"] - targets[1])
    return out


# ================================================================================ main
print(f"B1: Multiple Point Principle vs lane Y1 Planck-scale couplings   (MUTATE={MUT})")
tr = L.run_central(mu_max=1e21)
tY, t2, t3 = tr.A(MP)
targets = (tY, t2, t3)
sig_t = tuple(t * r for t, r in zip(targets, Y1_REL))
print(f"  Y1 targets at M_P = {MP:.5e} GeV: 1/alpha = ({tY:.3f}, {t2:.3f}, {t3:.3f}) (Y, SU(2), SU(3)), 1-sigma ({sig_t[0]:.3f}, {sig_t[1]:.3f}, {sig_t[2]:.3f})")

print("\nInternal checks (transcription and arithmetic; these do not decide the physics):")
chk("C1 Y1 targets equal the pre-registered ones to 0.01", all(abs(a - b) < 0.01 for a, b in zip(targets, Y1_EXPECTED)))
# C2 recompute the non-Abelian per-group values from the printed triple points
for key in ("SU2", "SU3"):
    t = TRIPLE[key]
    ex, full = per_group(t["N"], t["b_adj"], t["b_f"], True)
    ne, _ = per_group(t["N"], t["b_adj"], t["b_f"], False)
    pn, pe = PRINTED_PER_GROUP[key]
    print(f"    {key}: full(no cont.) = {full:.2f}   not exponentiated {ne:.2f} (printed {pn})   exponentiated {ex:.2f} (printed {pe})   x{NGEN}: {NGEN * ne:.2f} / {NGEN * ex:.2f} (printed Planck value {PRINTED_PLANCK[key]})")
    if key == "SU2":
        chk(f"C2 {key} recomputed per-group values match the printed ones within 0.2", abs(ne - pn) < 0.2 and abs(ex - pe) < 0.2)
    else:
        # AMENDMENT 2 (after the FIRSTRUN, where this check failed for SU(3): recomputed 18.02/19.41 vs printed 17.7/18.9): the check is split.  The unrounded discrepancy is REPORTED
        # (and its effect on the verdict shown below); the hard check is that the paper's own rounded intermediates (25, 1.7, 0.65, 0.84, 0.70, 0.85) reproduce its printed values.
        print(f"    REPORTED discrepancy {key}: unrounded recomputation minus printed = {ne - pn:+.2f} (not exponentiated), {ex - pe:+.2f} (exponentiated); x{NGEN} = {NGEN * (ex - pe):+.2f} at the Planck scale")
        r_ne = 0.65 * 25 + 0.84 * 1.7
        r_ex = 0.70 * 25 + 0.85 * 1.7
        chk(f"C2r {key} printed rounded intermediates (25, 1.7, factors 0.65/0.84 and 0.70/0.85) reproduce the printed per-group values within 0.05 (the paper rounded 4 pi (3/8) 5.4 = {4 * PI * 3 / 8 * 5.4:.2f} to 25)", abs(r_ne - pn) < 0.05 and abs(r_ex - pe) < 0.05, f"({r_ne:.2f}, {r_ex:.2f})")
    chk(f"C2b {key} 3 x printed exponentiated per-group value equals printed Planck value within 0.15", abs(NGEN * pe - PRINTED_PLANCK[key]) < 0.15)
# C3 U(1) row arithmetic
bad = [(r[0], r[1]) for r in U1_ROWS if abs(r[4] * r[5] - r[7]) > 0.15 or abs(r[4] * r[6] - r[8]) > 0.15 or abs(1 / r[3] - r[4]) > 0.02]
chk("C3 U(1) Table 12 rows: (1/alpha_cont) x (enhancement) = printed prediction (both tau) and 1/alpha_cont = 1/alpha_cont within rounding", not bad, f"(bad rows: {bad})")
star_mean = sum(r[7] for r in U1_ROWS if r[9]) / 4
chk("C4 mean of the four starred rows = 56.25, consistent with the abstract's 56 +- 5 and with 99.4 at M_Z (56.25 + 43.1)", abs(star_mean - 56.25) < 1e-9 and abs(round(star_mean) - 56) < 1 and abs(star_mean + 43.1 - 99.4) < 0.1, f"(mean {star_mean:.3f}; 43.1 = 109.3 - 66.2 from Table 13)")
tot = LOW["a_MZ_U1"] + LOW["a_MZ_SU2"] + LOW["delta"]
tsig = math.sqrt(5.0 ** 2 + 6.0 ** 2 + 3.5 ** 2)
chk("C5 the paper's own sum 99.4 + 29.2 + 8.2 = 136.8 and its quadrature 5, 6, 3.5 gives ~9", abs(tot - LOW["total"]) < 0.05 and abs(tsig - 9.0) < 0.6, f"(sum {tot:.2f}, quadrature {tsig:.2f})")
chk("C6 the paper's SU(5)-normalised 32.9 = (3/5) x 54.8: Y-normalised couplings are the ones compared", abs(0.6 * PAPER_EXPT["Y"] - 32.9) < 0.05)
chk("C7 the paper's own 'experimental' values agree with Y1 to the paper's accuracy (< 1.5 in 1/alpha)", all(abs(PAPER_EXPT[k] - t) < 1.5 for k, t in zip(("Y", "SU2", "SU3"), targets)),
    f"(paper {PAPER_EXPT['Y']}, {PAPER_EXPT['SU2']}, {PAPER_EXPT['SU3']}  vs Y1 {tY:.2f}, {t2:.2f}, {t3:.2f})")

# scale ambiguity of the target (the papers say only 'the Planck scale')
print("\nScale ambiguity of the target (papers do not give a number for M_Planck):")
for f in (1 / 3, 1.0, 3.0):
    a = tr.A(MP * f)
    print(f"    M = {f:.3g} M_P : ({a[0]:.3f}, {a[1]:.3f}, {a[2]:.3f})   shift from M_P: ({a[0] - tY:+.3f}, {a[1] - t2:+.3f}, {a[2] - t3:+.3f})")

# real and mutated analyses
R = analyse(targets, sig_t, False)
M = analyse(targets, sig_t, True)
ACT = M if MUT else R


def show(res, title):
    print(f"\n{title}")
    print("  coupling |   MPP prediction (primary)   | Y1 target | z (primary) | status (primary)   | alt prediction (secondary)   | z (alt) | status (alt)   | robust")
    for i, k in enumerate(("Y", "SU2", "SU3")):
        r = res[k]
        print(f"  {k:8s} | {r['pred']:6.2f} +- {r['sig']:4.2f} ({100 * r['frac']:4.1f}%) | {targets[i]:8.3f}  | {r['z']:+6.2f}      | {r['status']:16s} | {r['pred2']:6.2f} +- {r['sig2']:4.2f} ({100 * r['frac2']:4.1f}%) | {r['z2']:+6.2f}  | {r['status2']:16s} | {r['robust']}")
    print(f"  {res['route']}")


show(R, "REAL conversion (papers' own factors: U(1) weakening ~6.5, non-Abelian N_gen = 3):")
print(f"  (secondary column: SU(2), SU(3) with uncertainty propagated from the printed Monte Carlo errors: see below; U(1) = the authors' viewpoint b, 59.7 +- 3.5)")
for key in ("SU2", "SU3"):
    s, parts = derived_sigma(key)
    print(f"    derived sigma {key}: {s:.2f}  (from beta_adj {parts[0]:.2f}, beta_f {parts[1]:.2f}, exp-vs-not spread {parts[2]:.2f}); paper's stated Planck-scale sigma {math.hypot(*STATED_SIG[key]):.2f}")
# AMENDMENT 3 (context only, does not enter any verdict): how easily would a prediction of this width pass by chance?  Declared broad prior: each 1/alpha_i(M_P) independent and uniform on [20, 100]
# (a generous range for an asymptotically free or weakly running coupling); the chance that a claimed value with the stated primary sigma lies within 2 sigma of the target = window / range.
print("\nChance-pass context (Amendment 3; prior 1/alpha_i(M_P) ~ U[20,100], independent; not a criterion):")
p_all = 1.0
for i, key in enumerate(("Y", "SU2", "SU3")):
    w = 2 * NSIG_PASS * math.hypot(R[key]["sig"], sig_t[i])
    p = min(1.0, w / 80.0)
    p_all *= p
    print(f"    {key}: window +-{NSIG_PASS * math.hypot(R[key]['sig'], sig_t[i]):.1f} -> chance of a pass {p:.2f}")
print(f"    all three by chance ~ {p_all:.3f}  (the three targets lie within 49-55, so a flat 'about 52 +- 8' claim for all three would also pass: the test has little power)")
# AMENDMENT 2 sensitivity: statuses if the unrounded recomputed centrals are used for SU(2), SU(3) instead of the printed ones
print("\nSensitivity to the paper's rounding (Amendment 2): unrounded recomputed centrals, primary sigma:")
for key, i in (("SU2", 1), ("SU3", 2)):
    t = TRIPLE[key]
    c = NGEN * per_group(t["N"], t["b_adj"], t["b_f"], True)[0]
    st, z, fr = status(c, R[key]["sig"], targets[i], sig_t[i])
    print(f"    {key}: central {c:.2f} (printed {PRINTED_PLANCK[key]}), z = {z:+.2f}, {st}")
if MUT:
    show(M, "MUTATED conversion (U(1) weakening factor -> 3):")

# variant spread for U(1): how many of the authors' own variants would a 2-sigma test accept?
print("\nU(1) variants printed by the authors (tau = 0.79), tested with the primary sigma = 4.5 against Y1:")
acc = 0
for r in U1_ROWS:
    z = (r[7] - tY) / math.hypot(U1_SIG_A, sig_t[0])
    acc += abs(z) <= NSIG_PASS
    print(f"    {r[1]:8s} {r[0]:10s} pred {r[7]:5.1f}  z = {z:+5.2f} {'starred' if r[9] else ''}")
print(f"    {acc} of {len(U1_ROWS)} variants within 2 sigma; range {min(r[7] for r in U1_ROWS):.1f} to {max(r[7] for r in U1_ROWS):.1f} (the choice among them is a knob unless the authors' starred set is taken as fixed)")

# Optional: low-energy alpha through the paper's own mechanism (alpha^-1(0) = 1/aY(MZ) + 1/a2(MZ) + measured running constant), boundary shift additive
print("\nOptional step: what MPP implies for the low-energy alpha through Y1's running (boundary shift is additive at one loop; two-loop boundary dependence neglected and NOT checked here):")
sh, sl = R["shift_low"], R["sig_low"]
pred0 = ALPHA0_INV + sh
sg = sl
dig = math.log10(ALPHA0_INV / sg)
print(f"    1/alpha(0) = {ALPHA0_INV} + [(56.25 - {tY:.3f}) + (49.5 - {t2:.3f})] = {pred0:.2f} +- {sg:.2f}  ({100 * sg / ALPHA0_INV:.1f}%);  the paper's own value is {LOW['total']} +- {LOW['total_sig']:.0f}")
print(f"    digits supported: log10(137/sigma) = {dig:.2f}  -> the first digit and a fraction of the second; the measured value has ~11 digits.  The 'measured running constant' is measured input (hadronic vacuum polarisation, charged masses), so this is NOT a derivation of alpha.")
print(f"    hypothetical: to reach the 5e-10 bar, the Planck-scale couplings would need to be known to ~1e-8 absolute; the MPP stated uncertainty is ~{sg:.1f}, i.e. ~{sg / 1e-8:.1e} times too large")

print("\nVERDICT (against the declared criteria):")
if not MUT:
    for k in ("Y", "SU2", "SU3"):
        r = R[k]
        print(f"  {k}: {r['status']} (z = {r['z']:+.2f}; sigma/pred = {100 * r['frac']:.1f}%); alt-uncertainty status {r['status2']} (z = {r['z2']:+.2f}); robust = {r['robust']}")
    print(f"  {R['route']}")
    print("  Zero-knob: only in the sense that the authors' choices are fixed by their papers; SU(2)/SU(3) triple points are graphical extractions with 5-20% MC errors; the U(1) result is the paper's own number (not recomputable here) and depends on a choice among printed variants.")
    print("  Ceiling: even a full pass leaves 1/alpha(0) uncertain at the ~6% level; alpha stays an INPUT; kappa = 1/2 FITTED.")
if MUT:
    changed = (M["Y"]["status"] != R["Y"]["status"]) and (M["route"] != R["route"])
    print(f"\nMUTATE CONTROL: U(1) weakening factor 6.5 -> 3.  Real: U(1) {R['Y']['status']}, route '{R['route'][:30]}...'.  Mutated: U(1) {M['Y']['status']}, route '{M['route'][:30]}...'  ->",
          "the control fires (exit 1)" if changed else "CONTROL BROKEN (exit 3): the verdict did not change")
    sys.exit(1 if changed else 3)
sys.exit(0 if not FAILED else 1)
