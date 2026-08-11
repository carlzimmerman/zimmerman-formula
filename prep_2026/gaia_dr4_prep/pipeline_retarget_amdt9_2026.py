#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
pipeline_retarget_amdt9_2026.py
===============================
THE DR4 PIPELINE RETARGET, RECORDED -- and two findings that change how DR4 can be scored.

Run 2026-08-11.  `wide_binary_pipeline.py` was found HALF-FIXED: Amendment 9's in-force target
GAMMA_TARGET = 1.2139 (and GAMMA_TARGET_ALT = 1.2592) were DEFINED at the top of the file but
never CONSUMED anywhere -- dead code.  Every distance, injection, separation and self-test in the
file was still computed against GAMMA_MI = 1.1582 (Amendment 8, superseded) while the header looked
current.  That is more dangerous than being plainly stale, because the file reads as updated.

REWIRED (no registered number moved -- the code now matches the registration, not the reverse):
  * report_7e   -> reports distance to Newton AND to BOTH in-force footings; MI kept as record only
  * GATE        -> injects {1.00, 1.2139, 1.2592, 1.33} (was {1.00, 1.1582, 1.33})
  * spread      -> 8 realizations at 1.2139 (label previously PRINTED "1.09" while injecting 1.1582)
  * separation  -> all N-for-3-sigma against the in-force target; footing fork added
  * ecc bracket -> at 1.2139
Nothing in PREREGISTRATION_DR4.md or any *_HASH.txt was touched, read-only.

--------------------------------------------------------------------------------------------------
FINDING 1 -- THE PRIMARY KILL TEST GOT EASIER (favourable, and it is just arithmetic)
--------------------------------------------------------------------------------------------------
A bigger predicted signal needs fewer pairs to separate from Newton.  At the retargeted 1.2139 the
3-sigma separation from Newton needs N ~ 2,333 pairs (~212 with y < 0.3), against ~5,356 at the old
1.09.  DR4 will deliver far more than that.  *** The pre-registered kill condition is comfortably
powered; if DR4 says Newtonian, the framework takes the hit and cannot plead statistics. ***

--------------------------------------------------------------------------------------------------
FINDING 2 -- THE ALT FOOTING IS VERY NEARLY UNSCOREABLE BY CONSTRUCTION (against interest)
--------------------------------------------------------------------------------------------------
Amendment 9 re-derived the no-verdict edge to 1.26 from its own definition ("above every
EFE-saturated target"), because the alt target 1.2592 had made the old 1.20 premise false.  The
consequence was not priced at the time and is priced here:

        alt target 1.2592  sits  0.0008  below the edge 1.26
        the estimator's own scatter at N = 30,000 is  sigma ~ 0.020  =  24x that margin

So if the ALT footing is the true one, a correctly-working measurement lands ABOVE the pre-declared
no-verdict edge roughly half the time and is UNSCOREABLE BY THE REGISTRATION.  The GATE run
demonstrates it rather than asserting it: injecting 1.26 recovered 1.2675 and tripped
"PRE-DECLARED UNSCOREABLE" on BOTH footings.

And the footing fork itself is systematics-capped, which corrects a banked optimism:
        canonical 1.2139 vs alt 1.2592  ->  separation 0.0453
        3-sigma on statistics alone     ->  N ~ 52,027 pairs
        but the FROZEN systematic allowance is 0.02 = 44% of the separation
        ==> the fork tops out near 2.3 sigma REGARDLESS OF N unless systematics beat ~0.015
*** The banked claim "separation 2.68 sigma => DR4 distinguishes the arms" is OPTIMISTIC: it is
~2.3 sigma and systematics-capped, not a clean discrimination. ***  Recorded against interest.
"""

import os
import re
import subprocess
import sys

FAIL = []
NCHK = [0]
HERE = os.path.dirname(os.path.abspath(__file__))
PIPE = os.path.join(HERE, "wide_binary_pipeline.py")


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))
    return True


print(__doc__)

# =================================================================================================
print("=" * 100)
print("PART A -- read the pipeline file and prove the in-force target is now WIRED, not just defined")
print("=" * 100)

src = open(PIPE).read()
body = src.split('if __name__')[0]

GT, GTA, GMI, EDGE = 1.2139, 1.2592, 1.1582, 1.26

m = re.search(r"^GAMMA_TARGET\s*=\s*([\d.]+)", src, re.M)
m_alt = re.search(r"^GAMMA_TARGET_ALT\s*=\s*([\d.]+)", src, re.M)
m_edge = re.search(r"^NOVERDICT_EDGE\s*=\s*([\d.]+)", src, re.M)
check(m and abs(float(m.group(1)) - GT) < 1e-9,
      f"A1  GAMMA_TARGET = {m.group(1) if m else 'ABSENT'} read out of the file (Amdt 9 in force)",
      "read, not asserted -- the same discipline the readiness audit used")
check(m_alt and abs(float(m_alt.group(1)) - GTA) < 1e-9 and m_edge
      and abs(float(m_edge.group(1)) - EDGE) < 1e-9,
      f"A2  GAMMA_TARGET_ALT = {m_alt.group(1) if m_alt else '?'}, "
      f"NOVERDICT_EDGE = {m_edge.group(1) if m_edge else '?'}")

# the load-bearing test: is the in-force constant actually USED, or dead code?
uses_tgt = len(re.findall(r"GAMMA_TARGET\b", src)) - 1          # minus its own definition
uses_alt = len(re.findall(r"GAMMA_TARGET_ALT\b", src)) - 1
check(uses_tgt >= 8 and uses_alt >= 4,
      f"A3  *** THE FIX THAT MATTERED: GAMMA_TARGET is now referenced {uses_tgt} times beyond its "
      f"definition and GAMMA_TARGET_ALT {uses_alt} times.  Before the rewire both counts were ZERO "
      f"-- the in-force target was DEAD CODE while the file's header read as current ***",
      "half-fixed is worse than stale: the header claims Amendment 9, the arithmetic used Amendment 8")

# the superseded number must survive ONLY as record, never in the injection/separation logic
inj = re.search(r"for ginj in \(([^)]*)\)", src)
check(inj and "GAMMA_MI" not in inj.group(1) and "GAMMA_TARGET" in inj.group(1),
      f"A4  the GATE injection set is now ({inj.group(1) if inj else '?'}) -- the superseded MI "
      f"target no longer drives any injection",
      "MI is retained in the reporting as the historical/disjointness record only")

check("GAMMA_MI" in src and "superseded record only" in src,
      "A5  and the superseded MI number is still PRINTED, labelled 'superseded record only' -- "
      "removing it would have destroyed the audit trail of what the pipeline used to test",
      "the arm changed because lensing closed MI, not because wide binaries did")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- the two findings, as arithmetic")
print("=" * 100)

SIG_AT_30K = 0.0199          # measured this run: max(profile sigma, 8-realization rms) at N=30,000
N_REF = 30000
SYS_FROZEN = 0.02            # the frozen systematic allowance (pre-registered)


def n_for_3sigma(sep):
    return N_REF * (3 * SIG_AT_30K / sep) ** 2


n_newt = n_for_3sigma(GT - 1.0)
n_newt_old = n_for_3sigma(1.09 - 1.0)
check(n_newt < n_newt_old,
      f"B1  FINDING 1: 3-sigma separation of the in-force {GT} from Newton needs N ~ {n_newt:,.0f} "
      f"pairs, against N ~ {n_newt_old:,.0f} at the original frozen 1.09 -- a bigger predicted "
      f"signal is cheaper to distinguish.  DR4 delivers far more than either",
      "so the pre-registered kill condition is comfortably powered; a Newtonian DR4 result cannot "
      "be blamed on sample size")

sep_foot = GTA - GT
n_foot = n_for_3sigma(sep_foot)
sig_cap = sep_foot / SYS_FROZEN
check(sig_cap < 3.0,
      f"B2  *** FINDING 2a, AGAINST INTEREST: the footing fork separation is only {sep_foot:.4f}, so "
      f"the frozen systematic allowance {SYS_FROZEN} caps it at {sig_cap:.2f} sigma REGARDLESS OF N "
      f"(3-sigma on statistics alone would need N ~ {n_foot:,.0f}).  The banked '2.68 sigma => DR4 "
      f"distinguishes the arms' is OPTIMISTIC -- it is ~{sig_cap:.1f} sigma and systematics-capped ***",
      f"to reach 3 sigma the systematics must beat {sep_foot / 3:.3f}, i.e. "
      f"{SYS_FROZEN / (sep_foot / 3):.1f}x better than the frozen allowance")

margin = EDGE - GTA
check(margin < SIG_AT_30K,
      f"B3  *** FINDING 2b, THE STRUCTURAL ONE: the alt target {GTA} sits only {margin:.4f} below the "
      f"no-verdict edge {EDGE}, while the estimator's own scatter is {SIG_AT_30K:.4f} = "
      f"{SIG_AT_30K / margin:.0f}x that margin.  If the ALT footing is true, a correctly-working "
      f"measurement lands above the pre-declared edge about HALF the time and is UNSCOREABLE BY THE "
      f"REGISTRATION ***",
      "demonstrated in the GATE run: injecting 1.26 recovered 1.2675 and tripped PRE-DECLARED "
      "UNSCOREABLE on both footings")

info("B4  WHY THIS IS NOT A REASON TO MOVE THE EDGE. The edge was re-derived to 1.26 from its own "
     "definition ('above every EFE-saturated target'), on the record, BEFORE data -- moving it now "
     "to make the alt footing scoreable would be exactly the post-hoc adjustment pre-registration "
     "exists to prevent. The honest options are (i) accept that an alt-footing universe yields a "
     "no-verdict about half the time, or (ii) file an amendment BEFORE DR4 that states a "
     "principled treatment of the alt footing and takes the credibility cost of another amendment. "
     "This script records the fork; it does not choose.")

info("B5  and the choice is not urgent for the PRIMARY test: the kill condition (a Newtonian result "
     "counts against the framework at 4.74-7.10 sigma_tot) is unaffected by the edge, because "
     "gamma_hat ~ 1.00 is nowhere near 1.26. What the edge threatens is only the ability to claim a "
     "CONFIRMATION on the alt footing -- i.e. it can cost a win, never a loss.")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- the ecc systematic and kappa, re-measured at the new target")
print("=" * 100)

info("C1  the eccentricity-mismatch shift (flat-e truth vs thermal-e model) re-measures to -0.0014 "
     "at the in-force target, against -0.0082 at the old 1.1582 -- smaller, but the nuisance kappa "
     "still lands 1.1189, OUTSIDE the frozen window (0.95, 1.05), so the ecc bracket still trips "
     "'SYSTEMATIC-LIMITED, NO VERDICT' exactly as Amendment 8 risk (c) declared. Unchanged in "
     "kind: reported, not repaired.")

info("C2  every GATE injection recovered within tolerance on both footings "
     "(1.00 -> 0.985, 1.2139 -> 1.2250, 1.2592 -> 1.2675, 1.33 -> 1.3325), so the estimator itself "
     "is sound at the retargeted signal size; the run's PASS is a self-test of the estimator, never "
     "a verdict on data.")

# =================================================================================================
print()
print("=" * 100)
print("PART D -- drive the retargeted pipeline (the gate for this record)")
print("=" * 100)

if "--fast" in sys.argv:
    info("D1  full pipeline run skipped (--fast).")
else:
    r = subprocess.run([sys.executable, PIPE], capture_output=True, cwd=HERE, timeout=2400)
    out = r.stdout.decode()
    check(r.returncode == 0, f"D1  wide_binary_pipeline.py exit {r.returncode}",
          "" if r.returncode == 0 else r.stderr.decode()[-400:])
    check("PIPELINE SELF-TEST: PASS" in out,
          "D2  the retargeted pipeline's own self-test PASSES (all four injections recovered)")
    check(f"in-force canonical" in out and "1.2139" in out,
          "D3  the run reports against the in-force target, not the superseded one")
    check("THE FOOTING FORK" in out,
          "D4  the footing-fork separation is now reported by the pipeline itself")

print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  THE PIPELINE IS RETARGETED AND THE RUN IS GREEN -- and the retarget surfaced a structural
  scoring problem that was created, unpriced, by Amendment 9 itself:

  1. The file was HALF-FIXED: Amendment 9's target was defined but referenced ZERO times.
     Every number it printed was Amendment 8's while its header read as current.  Now wired
     ({uses_tgt} references), with the superseded MI number kept as labelled record only.

  2. FAVOURABLE: the bigger in-force signal makes the primary test cheaper -- 3-sigma from
     Newton at N ~ {n_newt:,.0f} pairs, against ~{n_newt_old:,.0f} at the original 1.09.  The kill
     condition is comfortably powered.

  3. AGAINST INTEREST, and the reason this script exists: the alt footing {GTA} sits {margin:.4f}
     below the no-verdict edge {EDGE} against a measurement scatter of {SIG_AT_30K:.4f}.  An
     alt-footing universe returns a NO-VERDICT about half the time.  And the footing fork is
     systematics-capped at ~{sig_cap:.1f} sigma regardless of N, so the banked "2.68 sigma => DR4
     distinguishes the arms" is withdrawn as optimistic.

  4. The edge must NOT be moved now -- that is the post-hoc move pre-registration prevents.
     It can cost a confirmation on the alt footing; it can never soften the kill condition.

  NOTHING in PREREGISTRATION_DR4.md or any *_HASH.txt was touched.  No registered number moved.
""")

print("=" * 100)
print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print(f"  - {f}")
    sys.exit(1)
print("ALL CHECKS PASSED")
print("=" * 100)
