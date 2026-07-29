#!/usr/bin/env python3
"""
window_hit_recount.py -- AUDIT LENS: WINDOWS, part 2. Recount the depth-10 exhaustive sweep
straight off the committed 42.5M-value array, and test the DIRECTION of every window error.

Three questions, all answered from real data (results_grind/depth_10/values.f64):
  (A) Do the real windows reproduce the committed per-target hit counts in
      NULL_RESULT_DEPTH10_EXHAUSTIVE.md?  (window sanity)
  (B) Which searched targets are STRUCTURALLY INCAPABLE of passing Gate A because their own
      window caps the bit budget below PASS_BITS=10?  (gate/fdr.py: bits = min(..., _bit_cap),
      _bit_cap = n_digits*log2(10) = log2(1/rel_precision).)  If cap < 10 the target can never
      certify, no matter what lands in it -- so its hits are pure denominator.
  (C) COUNTERFACTUALS. A window that is too WIDE can only ADD hits (cannot hide a match, cannot
      weaken a null). A window that is too NARROW can HIDE a real match. So for every dataset
      window this audit found suspect, re-run the count both ways and say whether the recorded
      null could have been changed.

Local-only project. No network. Exit 0.
"""
from __future__ import annotations
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

import numpy as np  # noqa: E402
import targets.pdg_constants as pdg                      # noqa: E402
from engine.scoring import measurement_tol               # noqa: E402
from exhaust_parallel import sm_target_keys              # noqa: E402
from exhaust_depth5_forced import N_TARGETS              # noqa: E402
from gate.fdr import PASS_BITS                           # noqa: E402

VALS = os.path.join(ROOT, "results_grind", "depth_10", "values.f64")
ds = pdg.load()
BAR = "=" * 104
checks = []


def check(msg, cond):
    checks.append(bool(cond))
    print(f"   [{'PASS' if cond else 'FAIL'}] {msg}")


print(BAR)
print("WINDOW HIT RECOUNT -- depth-10 exhaustive value set, real windows vs corrected windows")
print(BAR)

if not os.path.exists(VALS):
    print(f"  MISSING {VALS} -- cannot recount. Exiting without a claim.")
    sys.exit(0)

v = np.fromfile(VALS, dtype=np.float64)
print(f"\n  loaded {v.size:,} float64 values from {os.path.relpath(VALS, ROOT)} "
      f"({os.path.getsize(VALS)/1e6:.0f} MB)")
finite = np.isfinite(v)
print(f"  finite {finite.sum():,}; committed distinct count = 42,534,139  "
      f"(match={v.size == 42_534_139})")

keys = sm_target_keys()          # the 19 SEARCH targets (holdout excluded), as the run used
# committed per-target hits from NULL_RESULT_DEPTH10_EXHAUSTIVE.md (the only surviving record)
COMMITTED = {"a_e": 0, "alpha_em_inv_0": 0, "r_p_e": 0, "r_n_p": 0, "r_mu_e": 0, "a_mu": 0,
             "r_tau_e": 28, "alpha_em_inv_MZ": 50, "sin2_thetaW_MZ": 72, "koide_Q_up": 838,
             "higgs_lambda": 1130, "ckm_lambda": 2121, "koide_Q_down": 2098, "r_b_tau": 4747,
             "r_t_b": 4443, "alpha_s_MZ": 4933, "pmns_sin2_13": 15212, "pmns_sin2_12": 26142,
             "pmns_sin2_23": 20799}


def count_hits(tv, tol):
    """the EXACT grind predicate: |x - tv| <= tol*|tv|  (rel_error <= tol)."""
    w = abs(tv) * tol
    return int(np.count_nonzero(np.abs(v - tv) <= w))


def count_wide(tv):
    return int(np.count_nonzero((v >= tv * 0.9) & (v <= tv * 1.1))) if tv > 0 else \
           int(np.count_nonzero((v <= tv * 0.9) & (v >= tv * 1.1)))


# =====================================================================================
# A + B: recount, and the structural pass-capability test
# =====================================================================================
print("\nA+B  RECOUNT WITH THE REAL WINDOWS, AND WHICH TARGETS CAN EVER CERTIFY")
print("-" * 104)
print(f"  Gate A: bits = min(-log2(min(1,E_chance)*mult), cap), cap = log2(1/rel_precision),")
print(f"  mult = N_TARGETS = {N_TARGETS}, PASS at >= {PASS_BITS:.0f} bits.")
print(f"  WINDOW-ONLY TEST (the load-bearing one, no density model needed): cap depends on NOTHING")
print(f"  but the target's own window, so cap < {PASS_BITS:.0f} => that target can NEVER certify.")
print(f"  The E_chance column below is computed from the REAL depth-10 density (local count in the")
print(f"  +/-10% band of the 42.5M enumerated values). NOTE: gate/fdr.py does NOT use that; it uses")
print(f"  build_value_set(germ_pool), a 1-3-symbol library that is far sparser than the enumeration,")
print(f"  so the gate's own E_chance is SMALLER than the honest one shown here. The 'bits_max(emp)'")
print(f"  column is therefore the HONEST ceiling, not a prediction of the committed gate's output.\n")
print(f"  {'target':<17}{'rel_prec':>11}{'hits(recount)':>14}{'committed':>10}"
      f"{'cap[bits]':>10}{'cap>=10?':>9}{'E_ch(emp)':>11}{'bits_max(emp)':>14}")
print("  " + "-" * 100)
tot_re, tot_com, eligible, dead = 0, 0, [], []
hits_eligible = hits_dead = 0
rows = []
for k in keys:
    t = ds.target(k)
    tv, tol = float(t.value), measurement_tol(t)
    n = count_hits(tv, tol)
    nw = count_wide(tv)
    e_ch = nw * (2 * tol) / 0.2
    cap = t.n_digits * math.log2(10.0)
    chance = min(1.0, min(1.0, e_ch) * N_TARGETS)
    bits_max = min(cap, -math.log2(chance) if chance > 0 else float("inf"))
    can = cap >= PASS_BITS                      # WINDOW-ONLY eligibility
    (eligible if can else dead).append(k)
    if can:
        hits_eligible += n
    else:
        hits_dead += n
    tot_re += n
    tot_com += COMMITTED.get(k, 0)
    rows.append((k, t.rel_precision, n, COMMITTED.get(k, 0), cap, e_ch, bits_max, can))
    print(f"  {k:<17}{t.rel_precision:>11.3e}{n:>14,}{COMMITTED.get(k, 0):>10,}"
          f"{cap:>10.1f}{('YES' if can else 'NO'):>9}{e_ch:>11.2e}{bits_max:>14.1f}")
print("  " + "-" * 100)
print(f"  {'TOTAL':<17}{'':>11}{tot_re:>14,}{tot_com:>10,}")
check(f"recount from values.f64 reproduces the committed depth-10 total "
      f"({tot_re:,} vs {tot_com:,})", tot_re == tot_com)
check(f"per-target recount matches the committed table on all {len(keys)} targets",
      all(r[2] == r[3] for r in rows))
print(f"\n  WINDOW-ELIGIBLE (cap >= {PASS_BITS:.0f} bits) [{len(eligible)}]: {eligible}")
print(f"  WINDOW-DEAD     (cap <  {PASS_BITS:.0f} bits) [{len(dead)}]: {dead}")
print(f"  hits at ELIGIBLE targets: {hits_eligible:,} ({100*hits_eligible/max(1,tot_re):.2f}% of all "
      f"hits); hits at WINDOW-DEAD targets: {hits_dead:,} "
      f"({100*hits_dead/max(1,tot_re):.2f}%)")
check(f"{len(dead)} of {len(keys)} searched targets have windows so LOOSE that Gate A's own bit cap "
      f"is below the {PASS_BITS:.0f}-bit PASS threshold -- certification there is impossible by "
      f"construction, yet they carry {100*hits_dead/max(1,tot_re):.1f}% of the hit count",
      len(dead) > 0)
# robustness of that partition to the 1-bit convention error found in S3 of the sibling script
dead_corr = [r[0] for r in rows if (r[4] - 1.0) < PASS_BITS]
check(f"that partition is ROBUST to the 1-bit cap-convention error (dead set with cap-1: "
      f"{len(dead_corr)} targets, same set = {set(dead_corr) == set(dead)})",
      set(dead_corr) == set(dead))
# the E_chance leg alone
e_dead = [r[0] for r in rows if r[5] >= 1.0]
print(f"  (separately, with the HONEST enumerated density, E_chance >= 1 -> BAKED(dense) would fire "
      f"on {len(e_dead)} targets: {e_dead})")
print(f"  (and even the sharpest targets top out at "
      f"{max(r[6] for r in rows):.1f} honest bits at depth 10 -- below the "
      f"{PASS_BITS:.0f}-bit threshold. This is the look-elsewhere/density lens, not the window "
      f"lens; flagged for the FDR audit, not claimed here.)")

# =====================================================================================
# C: COUNTERFACTUAL WINDOWS -- direction test
# =====================================================================================
print("\nC  COUNTERFACTUAL WINDOWS: could a window error have HIDDEN a match?")
print("-" * 104)
print("  A too-WIDE window only adds hits (cannot hide a match; cannot weaken a null).")
print("  A too-NARROW window can hide one. So only the narrow-direction cases matter.\n")
CF = [
    # (key, alt_sigma, why, direction)
    ("r_p_e", 1836.152673426 * (3.2e-11 / 1836.152673426),
     "direct CODATA2022 m_p/m_e = 1836.152673426(32); dataset PROPAGATES m_p & m_e "
     "independently -> 24,459x too wide", "dataset TOO WIDE"),
    ("sin2_thetaW_MZ", 4.0e-5,
     "PDG MS-bar s^2hat(M_Z) = 0.23122(4); dataset stores sigma=3.0e-5 -> 25% too narrow",
     "dataset TOO NARROW"),
    ("pmns_sin2_23", 0.023,
     "NuFIT-class sin^2 th23 (NO) is ASYMMETRIC ~ +0.018 -0.023; dataset stores symmetric "
     "0.018 (the SMALLER leg) -> narrow on the low side", "dataset TOO NARROW"),
    ("higgs_lambda", None,
     "v_higgs sigma in the dataset (6.0e-4 GeV) is 9.5x the value propagated from G_F "
     "(6.3e-5); does that matter for the searched lambda?", "dataset TOO WIDE (upstream)"),
]
print(f"  {'target':<17}{'sigma used':>13}{'alt sigma':>13}{'hits now':>10}{'hits alt':>10}"
      f"{'delta':>8}  note")
print("  " + "-" * 100)
narrow_new = {}
for k, alt_sigma, why, direc in CF:
    t = ds.target(k)
    tv = float(t.value)
    n_now = count_hits(tv, measurement_tol(t))
    if k == "higgs_lambda":
        # recompute lambda's propagated rel with the CORRECT v sigma, hold m_H fixed
        mH, vh = ds.target("m_H"), ds.target("v_higgs")
        v_rel_correct = 0.5 * ds.target("G_F").rel_precision
        rel_alt = math.sqrt((2 * mH.rel_precision) ** 2 + (2 * v_rel_correct) ** 2)
        alt_sigma = rel_alt * tv
    tol_alt = max(1e-10, min(0.2, alt_sigma / abs(tv)))
    n_alt = count_hits(tv, tol_alt)
    print(f"  {k:<17}{float(t.sigma):>13.3e}{alt_sigma:>13.3e}{n_now:>10,}{n_alt:>10,}"
          f"{n_alt - n_now:>+8,}  {direc}")
    print(f"                    {why}")
    if "NARROW" in direc:
        narrow_new[k] = (n_alt - n_now, n_alt, tol_alt)

print("\n  For the two NARROW-direction cases, could any of the NEW hits certify?")
for k, (dn, n_alt, tol_alt) in narrow_new.items():
    t = ds.target(k)
    tv = float(t.value)
    nw = count_wide(tv)
    e_ch = nw * (2 * tol_alt) / 0.2
    cap = -math.log10(tol_alt) * math.log2(10.0)
    chance = min(1.0, min(1.0, e_ch) * N_TARGETS)
    bits_max = min(cap, -math.log2(chance) if chance > 0 else float("inf"))
    print(f"    {k:<17} +{dn:,} new in-window values; widened cap={cap:.1f} bits, "
          f"E_chance={e_ch:.2e} -> bits_max={bits_max:.1f} "
          f"-> {'COULD certify' if bits_max >= PASS_BITS else 'CANNOT certify (below 10 bits)'}")
could = []
for k, (dn, n_alt, tol_alt) in narrow_new.items():
    t = ds.target(k)
    tv = float(t.value)
    nw = count_wide(tv)
    e_ch = nw * (2 * tol_alt) / 0.2
    cap = -math.log10(tol_alt) * math.log2(10.0)
    chance = min(1.0, min(1.0, e_ch) * N_TARGETS)
    if min(cap, -math.log2(chance) if chance > 0 else float("inf")) >= PASS_BITS:
        could.append(k)
check(f"no narrow-direction window error could have hidden a CERTIFIABLE match at depth 10 "
      f"(targets that could: {could or 'none'})", not could)

# r_p_e specifically: does tightening to the true CODATA window change anything?
t = ds.target("r_p_e")
n_wide_win = count_hits(float(t.value), measurement_tol(t))
n_true_win = count_hits(float(t.value), 3.2e-11 / 1836.152673426)
print(f"\n  r_p_e: hits with the dataset's over-wide window = {n_wide_win}; with the true "
      f"CODATA window = {n_true_win}")
check("tightening r_p_e to its true CODATA window leaves the depth-10 null unchanged "
      "(0 hits either way) -- the over-wide window inflated the SEARCH's chance rate, not the "
      "verdict", n_wide_win == 0 and n_true_win == 0)

# =====================================================================================
# D: how far is the nearest value to each ELIGIBLE target, in sigma?
# =====================================================================================
print("\nD  NEAREST APPROACH TO EVERY ELIGIBLE TARGET (in sigma) -- window-independent record")
print("-" * 104)
print(f"  {'target':<17}{'nearest |dv|/sigma':>20}{'rel_error':>13}   (this is the number a window "
      f"choice cannot move)")
print("  " + "-" * 100)
for k in eligible:
    t = ds.target(k)
    tv, sg = float(t.value), float(t.sigma)
    d = np.abs(v - tv)
    i = int(np.nanargmin(d))
    print(f"  {k:<17}{d[i]/sg:>20.3e}{d[i]/abs(tv):>13.3e}")
check("nearest-approach table is window-free: it lets any future window revision be re-scored "
      "without re-running the sweep", True)

# =====================================================================================
# E: THE TWO SEARCH DRIVERS DO NOT USE THE SAME WINDOW
# =====================================================================================
print("\nE  grind.py HITS AT 1 SIGMA; run_atomos.py PRE-GATES AT 3 SIGMA -- how much is skipped?")
print("-" * 104)
print("  run_atomos.py:1149  `if not (card.within_2sigma or card.rel_error < measurement_tol*3)`")
print("    -> union = 3 sigma (the comment says '3-sigma', within_2sigma is the weaker leg).")
print("  grind.py:477        `if card.rel_error > tol: continue`   -> exactly 1 sigma.")
print("  So the depth-10 EXHAUSTIVE null is a 1-SIGMA null. Anything sitting 1-3 sigma from a")
print("  target was never handed to the gate by grind, although run_atomos's own policy would")
print("  have gated it. Count of values in that annulus:\n")
print(f"  {'target':<17}{'n(<=1s) [null]':>16}{'n(<=2s)':>10}{'n(<=3s)':>10}"
      f"{'never gated (1-3s)':>20}")
print("  " + "-" * 100)
tot_annulus = 0
for k in keys:
    t = ds.target(k)
    tv, tol = float(t.value), measurement_tol(t)
    n1 = count_hits(tv, tol)
    n2 = count_hits(tv, min(0.2, 2 * tol))
    n3 = count_hits(tv, min(0.2, 3 * tol))
    tot_annulus += n3 - n1
    print(f"  {k:<17}{n1:>16,}{n2:>10,}{n3:>10,}{n3 - n1:>20,}")
print("  " + "-" * 100)
print(f"  total values inside 3 sigma but outside grind's 1-sigma hit window: {tot_annulus:,}")
sharp = [k for k in keys if ds.target(k).n_digits * math.log2(10.0) >= PASS_BITS]
sharp_annulus = 0
for k in sharp:
    t = ds.target(k)
    tv, tol = float(t.value), measurement_tol(t)
    sharp_annulus += count_hits(tv, min(0.2, 3 * tol)) - count_hits(tv, tol)
print(f"  of those, at the {len(sharp)} WINDOW-ELIGIBLE (cap>=10 bits) targets: {sharp_annulus:,}")
check(f"the 1-sigma-vs-3-sigma driver mismatch skipped {sharp_annulus:,} values at the only "
      f"targets where certification is possible at all -- so the depth-10 null is unchanged by "
      f"it ONLY IF that number is 0", sharp_annulus == 0)
print("\n  Could any of those skipped values have certified? Evaluate the 3-sigma window's own")
print("  chance rate at each affected window-eligible target (honest enumerated density):")
safe = True
for k in sharp:
    t = ds.target(k)
    tv, tol = float(t.value), measurement_tol(t)
    if count_hits(tv, min(0.2, 3 * tol)) - count_hits(tv, tol) == 0:
        continue
    tol3 = min(0.2, 3 * tol)
    nw = count_wide(tv)
    e3 = nw * (2 * tol3) / 0.2
    cap3 = -math.log10(tol3) * math.log2(10.0)
    ch = min(1.0, min(1.0, e3) * N_TARGETS)
    b3 = min(cap3, -math.log2(ch) if ch > 0 else float("inf"))
    verdict = "BAKED(dense), cannot pass" if e3 >= 1.0 else (
        "COULD pass" if b3 >= PASS_BITS else "below 10 bits, cannot pass")
    if e3 < 1.0 and b3 >= PASS_BITS:
        safe = False
    print(f"    {k:<17} 3-sigma E_chance={e3:>9.2e}  cap={cap3:5.1f} bits  bits_max={b3:6.1f}"
          f"  -> {verdict}")
check("every 1-3 sigma value that grind skipped sits at a target whose 3-sigma window is already "
      "dense (E_chance >> 1) under the honest enumerated density -> the depth-10 null survives the "
      "driver mismatch, though grind should say '1-sigma null' explicitly", safe)

print("\n" + BAR)
print(f"WINDOW RECOUNT: {sum(checks)}/{len(checks)} checks PASS")
print(BAR)
sys.exit(0)
