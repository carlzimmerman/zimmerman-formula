#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
footing_fork_and_edge_math_2026.py
==================================
THE FOOTING-FORK AND NO-VERDICT-EDGE MATH, RUN PROPERLY -- and it substantially WALKS BACK the
pessimistic framing I attached to the same two numbers on 2026-08-11.

WHAT I GOT RIGHT AND WHAT I GOT WRONG, up front:
  RIGHT (arithmetic): the ceiling formula is |delta gamma| / sigma_sym -- verified against the
    framework's OWN committed formalism in amendment3_systematics.py, which computes 4.50 sigma for
    Newton-vs-MI (0.090/0.02) and 2.35 for MI-vs-MG (0.047/0.02).  The footing fork's
    0.0453/0.02 = 2.27 sigma is therefore the correct ceiling AT THE FROZEN ALLOWANCE.
  WRONG (physics, twice):
    (1) I treated sigma_sym = 0.02 as if it were a MEASURED systematic.  It is a pre-registered
        ALLOWANCE whose stated dominant component is the Banik-vs-Chae CONTAMINATION disagreement
        -- precisely the component DR4's NSS/RV screening is built to remove.  The pipeline's own
        measured dominant systematic (eccentricity mismatch) is 0.0014, fourteen times smaller.
        Quoting a ceiling only at the allowance, and calling it "regardless of N", presented the
        most pessimistic point on a curve as if it were the whole curve.
    (2) I called the edge collision a structural threat without computing WHICH WORLDS it fires in.
        It fires only in worlds where gamma_hat > 1.26 -- i.e. where Newton is dead by >12 sigma and
        a MOND-class boost is confirmed.  *** The edge cannot cost a kill-survival; it can only
        blur which footing won, inside a world where the framework's core claim has already won. ***
        That is a bookkeeping annoyance in a winning scenario, not a structural problem, and my
        framing inverted the stakes.

Nothing registered is touched; PREREGISTRATION_DR4.md and every *_HASH.txt are read-only here.
"""

import sys
import numpy as np
from math import erf, sqrt

FAIL = []
NCHK = [0]


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


def Phi(z):
    return 0.5 * (1.0 + erf(z / sqrt(2.0)))


# in-force numbers (Amendment 9) and the measured pipeline behaviour (2026-08-11 run)
G_CAN, G_ALT, EDGE, G_NEWT = 1.2139, 1.2592, 1.26, 1.000
SIG_SYM_FROZEN = 0.02
SIG_FIT_30K = 0.0199
BIAS_OBS = 0.0083            # recovered 1.2675 when 1.2592 injected (GATE, canonical fit)
SEP_FOOT = G_ALT - G_CAN
ECC_SYS_MEASURED = 0.0014    # |shift| measured this run at the in-force target

print(__doc__)

# =================================================================================================
print("=" * 100)
print("PART A -- the ceiling formalism, reproduced from the framework's own committed script")
print("=" * 100)

G_OLD = {"Newton": 1.000, "MI": 1.090, "MG": 1.137}
c_nm = (G_OLD["MI"] - G_OLD["Newton"]) / SIG_SYM_FROZEN
c_mm = (G_OLD["MG"] - G_OLD["MI"]) / SIG_SYM_FROZEN
check(abs(c_nm - 4.50) < 0.01 and abs(c_mm - 2.35) < 0.01,
      f"A1  ceiling = |delta gamma|/sigma_sym reproduced exactly: Newton-vs-MI {c_nm:.2f} sigma, "
      f"MI-vs-MG {c_mm:.2f} sigma -- matching amendment3_systematics.py's committed 4.50 and 2.35",
      "so the formula I used was the framework's own, and the 2.27 arithmetic was not invented")

check(abs(SEP_FOOT / SIG_SYM_FROZEN - 2.27) < 0.02,
      f"A2  and the footing fork at the frozen allowance: {SEP_FOOT:.4f}/{SIG_SYM_FROZEN} = "
      f"{SEP_FOOT / SIG_SYM_FROZEN:.2f} sigma.  THAT NUMBER STANDS",
      "what does not stand is presenting it as the only number -- see Part B")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- the ceiling is a CURVE, not a number: run it")
print("=" * 100)

print(f"\n   sigma_sym      footing-fork ceiling      what that sigma_sym corresponds to")
rows = [
    (0.0014, "the ecc systematic THIS RUN measured at the in-force target"),
    (0.005, "measured-systematics scale if contamination is screened out"),
    (0.010, "half the frozen allowance (the audit's own 'systematics beat ~0.01')"),
    (0.020, "THE FROZEN ALLOWANCE -- dominated by the Banik-vs-Chae contamination gap"),
    (0.050, "if DR4 screening underperforms"),
    (0.100, "the audit's pessimistic contamination fork (delta_up = 0.10)"),
]
ceil_at = {}
for s, what in rows:
    c = SEP_FOOT / s
    ceil_at[s] = c
    mark = "  <-- what I quoted as if it were the whole story" if s == 0.020 else ""
    print(f"   {s:<9.4f}      {c:>6.2f} sigma            {what}{mark}")

check(ceil_at[0.005] > 3.0 and ceil_at[0.0014] > 3.0,
      f"B1  *** THE FOOTING FORK IS DECIDABLE IF THE SYSTEMATIC IS ANYWHERE NEAR THE MEASURED SCALE: "
      f"{ceil_at[0.005]:.1f} sigma at sigma_sym = 0.005, {ceil_at[0.0014]:.0f} sigma at the 0.0014 this "
      f"run actually measured.  It ceilings below 3 sigma ONLY at the frozen allowance and worse ***",
      "the allowance is a conservative pre-registered budget, not a measurement -- and its dominant "
      "component is exactly what DR4's NSS/RV screening exists to remove")

check(SIG_SYM_FROZEN / ECC_SYS_MEASURED > 10,
      f"B2  the gap between allowance and measurement is a factor "
      f"{SIG_SYM_FROZEN / ECC_SYS_MEASURED:.0f}: the frozen 0.02 vs the {ECC_SYS_MEASURED} "
      f"eccentricity-mismatch shift the pipeline measured at the in-force target",
      "the ecc term is the one systematic the pipeline can actually quantify end-to-end; the rest of "
      "the 0.02 is contamination, i.e. a data-quality question DR4 answers")

info("B3  AND THE HONEST OTHER SIDE, because the rule cuts both ways: the framework's own audit "
     "argues the frozen 0.02 is OPTIMISTIC, not conservative -- it is 13x smaller than the 0.26 "
     "published gamma_v disagreement between Banik+24 (Newtonian at 19 sigma) and Chae (1.43 +- 0.06, "
     "7 sigma from Newton), and it does not itemise undetected companions.  So sigma_sym could land "
     "ABOVE 0.02 as easily as below.  The defensible statement is a RANGE, not either endpoint: "
     "*** the footing fork ceilings anywhere from ~0.5 sigma (if contamination is as bad as the "
     "published disagreement) to ~30 sigma (if it screens down to the measured ecc scale), and DR4's "
     "screening quality -- not its sample size -- decides which. ***")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- the no-verdict edge: WHICH WORLDS does it fire in?")
print("=" * 100)

sig = SIG_FIT_30K
p_unbiased = 1.0 - Phi((EDGE - G_ALT) / sig)
p_biased = 1.0 - Phi((EDGE - (G_ALT + BIAS_OBS)) / sig)
print(f"\n   if the ALT footing is true (gamma = {G_ALT}):")
print(f"     P(gamma_hat > edge {EDGE}) = {100 * p_unbiased:.0f}%  (unbiased estimator, sigma = {sig})")
print(f"     P(gamma_hat > edge {EDGE}) = {100 * p_biased:.0f}%  (with the +{BIAS_OBS:.4f} shape bias "
      f"this run measured)")
check(0.4 < p_unbiased < 0.75,
      f"C1  the frequency claim holds quantitatively: an alt-footing universe returns a result above "
      f"the pre-declared edge {100 * p_unbiased:.0f}-{100 * p_biased:.0f}% of the time",
      "so the collision is real -- Part C2 is about what it COSTS, which is where I was wrong")

# the reframe: what does gamma_hat > 1.26 imply about Newton?
z_newt_at_edge = (EDGE - G_NEWT) / np.hypot(sig, SIG_SYM_FROZEN)
check(z_newt_at_edge > 9.0,
      f"C2  *** THE REFRAME I OWED AND DID NOT GIVE: a result at the edge is "
      f"{z_newt_at_edge:.1f} sigma from Newton even with the FULL frozen systematic in quadrature. "
      f"The 'unscoreable' flag therefore fires ONLY in worlds where Newton is dead by >9 sigma and a "
      f"MOND-class boost in wide binaries is confirmed.  It cannot cost a kill-survival; it can only "
      f"blur WHICH FOOTING won, inside a world the framework has already won ***",
      "I presented a bookkeeping annoyance in a winning scenario as a structural threat, and that "
      "inverted the stakes")

# and what it costs in the losing direction: nothing
z_kill = (G_CAN - G_NEWT) / np.hypot(sig, SIG_SYM_FROZEN)
info(f"C3  symmetrically, the edge is irrelevant to the kill condition: a Newtonian result sits at "
     f"gamma_hat ~ 1.00, which is {z_kill:.1f} sigma below the in-force canonical target and nowhere "
     f"near 1.26.  The pre-registered 4.74-7.10 sigma_tot evidence-against is untouched by anything "
     f"in this script -- the framework remains exactly as falsifiable as it was this morning.")

info("C4  what the collision DOES cost, stated plainly so it is not lost in the reframe: if the alt "
     "footing is true, the registration as written will more often than not decline to certify the "
     "confirmation. That is a real forfeited win, and the two honest responses remain (i) accept it, "
     "or (ii) file a principled alt-footing amendment BEFORE data. What is NOT available is moving "
     "the edge after seeing DR4 -- and note the edge's own definition ('above every EFE-saturated "
     "target') is what generated the collision, so an amendment would have to re-derive it from a "
     "better principle, not merely raise it.")

# =================================================================================================
print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  BOTH OF YESTERDAY'S "FINDINGS" SURVIVE AS ARITHMETIC AND ARE DOWNGRADED AS CONCLUSIONS.

  1. THE CEILING FORMULA WAS RIGHT (it is the framework's own: |delta gamma|/sigma_sym, verified
     against the committed 4.50 and 2.35).  The footing fork does ceiling at
     {SEP_FOOT / SIG_SYM_FROZEN:.2f} sigma AT the frozen allowance.

  2. BUT THE ALLOWANCE IS NOT A MEASUREMENT, and quoting only its value was manufacturing a
     deficit.  The ceiling is a curve: {ceil_at[0.0014]:.0f} sigma at the 0.0014 eccentricity systematic this
     run measured, {ceil_at[0.005]:.1f} sigma at 0.005, {ceil_at[0.01]:.1f} sigma at 0.01, {ceil_at[0.02]:.2f} at the allowance,
     {ceil_at[0.1]:.2f} at the pessimistic contamination fork.  *** DR4's SCREENING QUALITY, NOT ITS SAMPLE
     SIZE, DECIDES THE FOOTING FORK -- and the dominant term in the allowance is precisely the
     contamination gap DR4's NSS/RV screen is built to close. ***  Range, not endpoint: ~0.5 to
     ~30 sigma.  "Systematics-capped at 2.3 sigma regardless of N" is WITHDRAWN as a conclusion.

  3. THE EDGE COLLISION IS REAL ({100 * p_unbiased:.0f}-{100 * p_biased:.0f}% of alt-footing universes land above it) BUT I
     INVERTED ITS STAKES.  A result at the edge is {z_newt_at_edge:.1f} sigma from Newton with the full
     systematic included, so the flag fires only where Newton is already dead and a MOND-class
     boost is confirmed.  It can forfeit a footing certification; it can never soften the kill
     condition.  "Structural scoring problem" is DOWNGRADED to "a forfeited win in a winning
     world."

  4. UNCHANGED AND FAVOURABLE: the primary test needs only ~2,337 pairs for 3 sigma from Newton,
     and the kill condition stands at 4.74-7.10 sigma_tot.  The framework is not less falsifiable
     and not less powered than it was before either script ran.
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
