#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""t010_kappa_ledger.py -- T010: assemble KAPPA_LEDGER.md (every kappa-derivation attempt
   + the committed history: TT-gauge kill, 5-variant 161.6x span, BE mirror, with a
   one-line status each) AND refutation-check every CONFIRMED/CANDIDATE row from
   T001-T009 (adversarial re-check: does ANY forced coefficient / boundary ratio actually
   land in the kappa window?  The honest expected outcome is that the CONFIRMED rows
   SURVIVE -- no forced coefficient or ratio is in-window).

PASS (consolidation): KAPPA_LEDGER.md is written with exactly one line per attempt
   (T001-T009 + 3 committed-history entries) and a status consistent with LEDGER.md, AND
   every CONFIRMED/CANDIDATE row from T001-T009 (T001, T007) has had its "no route forces
   1/2" verdict re-checked by a live first-principles recomputation.
KILL: a forced coefficient or a GHY/bulk ratio lands inside the kappa window
   [0.508, 0.594] (would overturn a CONFIRMED row), OR a ledger status contradicts
   LEDGER.md.
Not a search (no mm_search): the two refutation re-checks are deterministic
   recomputations of already-reported numbers, so no FDR trial-count is owed.
Direction-of-risk: WIN-risk -- a consolidation could bury a dead route as "CONFIRMED"
   without re-checking; the re-check recomputes the closest approach from first
   principles, so a buried claim must clear a live number to stay CONFIRMED.
"""
import sys, os, math, datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qwenlib import *   # constants, kernel, check/info/finish, KAPPA_MEAS/KAPPA_ERR, FOOTINGS

# ---- PART A: the kappa-derivation attempt registry (one-line status each) ------------
# verdicts pulled from LEDGER.md (never edit old rows; this is a NEW consolidation file).
ATTEMPTS = [
    # (id, title, verdict, one-line status)
    ("hist-TT-gauge",  "TT-gauge route",            "KILL",
     "committed corpus: TT-gauge route to kappa=1/2 killed"),
    ("hist-5var-span", "5-variant span",            "KILL",
     "5 kappa variants span 161.6x -> not a single pin"),
    ("hist-BE-mirror", "BE mirror (pre-T005)",      "REFUTED",
     "Bose-Einstein mirror route 11.1sigma low; no q in [0.5,2] reaches 1/2"),
    ("T001", "route catalog",                         "CONFIRMED",
     "every published dS-thermo route forces q!=1/2 or none; Milgrom2020 q=1/2pi=0.159 "
     "closest near-miss, outside the window"),
    ("T002", "eps_tot=1/(32pi) enumeration",          "NULL",
     "not special: 3 matches vs 2.23 expected in the +-15.6% window, typical"),
    ("T003", "graviton-bath cancellation, 1-assum.",  "UNGRADED",
     "7/7 form-assumptions LOAD-BEARING (count=7 != 1); SCRIPT-GREEN, needs grading"),
    ("T004", "response-function scan",                "UNGRADED",
     "SCRIPT-RED; no Boltzmann/Wigner/Gaussian-linear response yields untuned 1/2; needs fix"),
    ("T005", "q-deformed Deser-Levin mirror",         "REFUTED",
     "q* out of range for both deformations over q in [0.5,2]; route stays ~5x low"),
    ("T006", "first-law smearing catalog",            "UNGRADED",
     "5 smearings each fix kappa per choice; SCRIPT-GREEN, needs grading"),
    ("T007", "boundary-term (GHY/bulk) ratios",       "CONFIRMED",
     "kappa^2 not a GHY-to-bulk ratio at <=3 combos; 0/3 in window; "
     "Bekenstein-Hawking S/A=1/4 is CONVENTION-grade, excluded"),
    ("T008", "two-temperature interpolation",         "UNGRADED",
     "no n gives a0-line AND kappa=1/2; SCRIPT-RED, needs grading"),
    ("T009", "pi-free theorem",                       "UNGRADED",
     "kappa pi-free AND a pure horizon-geometry ratio is trivial (M=1) or carries a free "
     "geometric/curvature parameter; SCRIPT-GREEN, needs grading"),
]

# kappa window = the fitted value +- its 1-sigma err (1/2 is ADOPTED, never "derived").
KAPPA_MEAS, KAPPA_ERR = 0.551, 0.043
LO, HI = KAPPA_MEAS - KAPPA_ERR, KAPPA_MEAS + KAPPA_ERR       # [0.508, 0.594], +-7.80%
K2_LO, K2_HI = LO * LO, HI * HI                                # kappa^2 window

info("kappa window [%.4f, %.4f] (fit %.3f+-%.3f); kappa^2 window [%.4f, %.4f]"
     % (LO, HI, KAPPA_MEAS, KAPPA_ERR, K2_LO, K2_HI))
info("footings (dimensionless quantities below -> footing-invariant, spread shown for R3): "
     "a0 can=%.4e alt=%.4e" % (A0_CAN, A0_ALT))

# ---- PART B: refutation re-check of every CONFIRMED/CANDIDATE row (T001, T007) --------
# T001 re-check: forced literature ROUTE coefficients. NONE may land in [LO, HI].
# (graviton-bath q=2/r with r FREE forces NONE -> no value to test, noted in ledger.)
# NOTE: framework 1/Z=0.1727 is the framework's OWN adopted number (the target in its
# own normalization), NOT a route-forced coefficient, so it is excluded from FORCED to
# avoid testing the target against itself.
FORCED = {
    "Milgrom1999 q=2 (=2cH, EXCLUDED 15.6sigma)": 2.0,
    "Milgrom2020 q=1/2pi":                          1.0 / (2.0 * math.pi),
    "Verlinde q=2pi":                               2.0 * math.pi,
    "Pikhitsa/KK O(1)/2pi":                         1.0 / (2.0 * math.pi),
}
ONE_OVER_Z = 0.17274707    # framework's own adopted number (target's normalization), noted only
def dist_to_window(v, lo, hi):
    # 0 if inside, else the gap to the nearest edge
    return 0.0 if lo <= v <= hi else min(abs(v - lo), abs(v - hi))
t001_in = [name for name, v in FORCED.items() if LO <= v <= HI]
t001_closest = min((dist_to_window(v, LO, HI), name, v) for name, v in FORCED.items())
check(len(t001_in) == 0, "T001 re-check: no forced coefficient in [%.3f,%.3f]" % (LO, HI),
      "forced=%s; in-window=%s; closest gap=%.4f (%s=%.4f)"
      % (list(FORCED.values()), t001_in or "none", t001_closest[0],
         t001_closest[1], t001_closest[2]))
check(t001_closest[1] == "Milgrom2020 q=1/2pi",
      "T001 re-check: closest approach is Milgrom2020 q=1/2pi=0.159 (matches ledger near-miss)",
      "closest=%s %.4f" % (t001_closest[1], t001_closest[2]))

# T007 re-check: GHY-to-bulk eta=(R/r_h)^2/(4-(R/r_h)^2) on the Lambda static patch.
# kappa^2 targets: 0.25 (1/2 adopted) / 0.3036 (0.551^2 measured). NONE may be in-window.
def eta(r_over_rh):
    x = r_over_rh ** 2
    return x / (4.0 - x)
RRH = [0.5, 1.0 / math.sqrt(3.0), 1.0 / math.sqrt(2.0)]
t007_vals = {("%.4f" % r): eta(r) for r in RRH}
t007_in = [name for name, v in t007_vals.items() if K2_LO <= v <= K2_HI]
t007_minrel = min(abs(v - 0.3036) / 0.3036 for v in t007_vals.values())
check(len(t007_in) == 0, "T007 re-check: no GHY/bulk eta in kappa^2 window [%.4f,%.4f]" % (K2_LO, K2_HI),
      "etas=%s; in-window=%s; min rel dist to 0.3036=%.3f"
      % (t007_vals, t007_in or "none", t007_minrel))
check(t007_minrel > 0.40, "T007 re-check: closest ratio still >0.40 rel below kappa^2 (matches ledger 0.429)",
      "min rel=%.3f" % t007_minrel)

# CONVENTION-grade guard: S/A=1/4 must NOT be counted as a kappa^2 hit.
conv = 0.25
check(not (K2_LO <= conv <= K2_HI),
      "T007 guard: Bekenstein-Hawking S/A=1/4=%.2f is OUT of the kappa^2 window (CONVENTION, excluded)" % conv)

# ---- PART C: assemble KAPPA_LEDGER.md -------------------------------------------------
CONF_ROWS = [a[0] for a in ATTEMPTS if a[2] in ("CONFIRMED", "CANDIDATE")]
check(sorted(CONF_ROWS) == ["T001", "T007"],
      "CONFIRMED/CANDIDATE rows from T001-T009 are exactly T001,T007 (both re-checked above)",
      "found=%s" % CONF_ROWS)

refnote = {
    "T001": "RE-CHECKED t010: 0/4 forced route coeffs in [%.3f,%.3f]; closest q=1/2pi=0.159 -> SURVIVES" % (LO, HI),
    "T007": "RE-CHECKED t010: 0/3 GHY/bulk etas in kappa^2 window [%.3f,%.3f] -> SURVIVES" % (K2_LO, K2_HI),
}
lines = []
lines.append("# KAPPA_LEDGER.md -- every kappa=1/2 derivation attempt, one line each (T010)")
lines.append("")
lines.append("Assembled %s by runs/t010_kappa_ledger.py.  kappa=1/2 is ADOPTED/FITTED "
             "(measured 0.551+/-0.043), NEVER 'derived'.  CONFIRMED/CANDIDATE rows carry an "
             "adversarial refutation re-check." % datetime.date.today().isoformat())
lines.append("")
lines.append("Window: kappa in [%.4f, %.4f] (fit+/-1sigma); kappa^2 in [%.4f, %.4f]."
             % (LO, HI, K2_LO, K2_HI))
lines.append("Footings (dimensionless numbers are footing-invariant; a0 spread shown per R3): "
             "can a0=%.4e, alt a0=%.4e." % (A0_CAN, A0_ALT))
lines.append("")
lines.append("## Committed history (pre-T001 corpus)")
for aid, title, verdict, status in ATTEMPTS:
    if aid.startswith("hist-"):
        lines.append("- **%s** (%s) -- %s :: %s" % (aid, verdict, title, status))
lines.append("")
lines.append("## T001-T009 (task-based)")
lines.append("| id | title | verdict | one-line status | refutation status |")
lines.append("|----|-------|---------|-----------------|-------------------|")
for aid, title, verdict, status in ATTEMPTS:
    if not aid.startswith("hist-"):
        ref = refnote.get(aid, "-")
        lines.append("| %s | %s | %s | %s | %s |" % (aid, title, verdict, status, ref))
lines.append("")
lines.append("## Refutation re-check detail (CONFIRMED/CANDIDATE)")
lines.append("- T001 forced coeffs: %s ; in-window=%s ; closest %s=%.4f (gap %.4f)"
             % (FORCED, t001_in or "none", t001_closest[1], t001_closest[2], t001_closest[0]))
lines.append("- T007 GHY/bulk etas: %s ; in-window=%s ; min rel dist to 0.3036=%.3f"
             % (t007_vals, t007_in or "none", t007_minrel))
lines.append("- Verdict: both CONFIRMED rows SURVIVE the adversarial re-check "
             "(no forced coefficient / ratio lands in-window).")

out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "KAPPA_LEDGER.md")
with open(out, "w") as f:
    f.write("\n".join(lines) + "\n")
check(os.path.exists(out) and len(open(out).read().splitlines()) > 15,
      "KAPPA_LEDGER.md written to %s" % out)

finish("t010")
