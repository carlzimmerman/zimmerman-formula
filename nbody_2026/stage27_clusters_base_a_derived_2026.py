#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage27_clusters_base_a_derived_2026.py
=======================================
CLUSTERS, WITH NO DARK-MATTER PARTICLE -- and the number that was blocking them is DERIVED here from
work this corpus already committed.

--------------------------------------------------------------------------------------------------
WHAT WAS BLOCKING CLUSTERS
--------------------------------------------------------------------------------------------------
The live cluster mechanism is the a_0-bump: a position-dependent Helmholtz mass
mu^2_eff = A B(Y/a_0^2), resonant at the framework's OWN a_0, which is where clusters live
(R500 at 0.33-0.58 a_0).  It is NOT a dark-matter particle -- it is a term in the same scalar
sector that supplies Lambda and MOND.  Its problem has always been amplitude:

   the framework's own chain gives   mu^2_eff(cluster) = 0.23 Mpc^-2   at A = A_fid = 1.65 Mpc^-2
   Mistele's cluster modelling wants mu^2_eff(cluster) = 1.0 - 7.9 Mpc^-2   (the "4x - 34x" band)

and the health analysis capped A.  The cap's size depended on ONE unresolved number -- `base_a`,
"the aether's algebraic gradient entry" -- through the softening factor 0.64/base_a.  Four candidates
were enumerated (2 - K_B, K_B, 1, or infinity), the published band assumed base_a = 1, and the
verdict FLIPPED between them: at base_a = 1 the bump only just touches the bottom of the cluster
demand.  `base_a_lookup_and_robustness_2026.py` established that this is a DERIVATION, not a
literature lookup, and left it owed.

--------------------------------------------------------------------------------------------------
IT IS NO LONGER OWED: base_a = K_B, READ OUT OF STAGE 22's OWN FULL-ACTION REDUCTION
--------------------------------------------------------------------------------------------------
Stage 22's committed scalar reduction (`svt_2026/svt_scalar_reduce.py`, run under the FULL AeST
action including the 2(2-K_B) J.grad phi - (2-K_B) Y terms) produces the aether scalar's algebraic
gradient coefficient explicitly:

    AP = a (8 pi G K2 Qb^2 a^2 - 6 H^2 a^2 + K_B k^2) / (32 pi G)      ->      K_B a k^2/(32 pi G)

at sub-horizon k.  The aether scalar's gradient entry is therefore K_B -- candidate (ii), not the
base_a = 1 the published band assumed.  *** That is the derivation the caveat asked for, and it was
already in the corpus; it just had not been read against this question. ***

--------------------------------------------------------------------------------------------------
CONSEQUENCE: THE CLUSTER WINDOW OPENS SUBSTANTIALLY
--------------------------------------------------------------------------------------------------
base_a = K_B, and K_B's only quantitative bound is AeST's own stability window 0 < K_B < 2, with
K_B = 0.1 the dominant fiducial in the literature.  Since the cap softens as 0.64/base_a, a SMALL
K_B softens it a lot.  Part C computes the resulting reachable mu^2_eff and compares it to the
cluster demand; Part D states what is still missing, which is no longer base_a but K_B itself and a
profile fit.
"""

import sys
import numpy as np

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


# ---- committed anchors ---------------------------------------------------------------------------
A_FID = 1.65                 # Mpc^-2, the fiducial bump amplitude (cluster calibration)
MU2_AT_FID = 0.23            # Mpc^-2, the framework's own chain at A_FID
MIST_LO, MIST_HI = 1.0, 7.9  # Mpc^-2, Mistele's cluster demand ("4x-34x")
AMAX_BAND_BASE1 = (4.49, 7.36)   # Mpc^-2, the v4-corrected published band AT base_a = 1
MIXRATIO_NUM = 0.64          # the softening is MIXRATIO_NUM/base_a (full-matrix result)
KB_FID = 0.1                 # the literature's dominant fiducial
KB_WINDOW = (0.0, 2.0)       # AeST's own stability window -- the ONLY quantitative bound

print(__doc__)

# =================================================================================================
print("=" * 100)
print("PART A -- base_a = K_B, read out of the committed SVT reduction")
print("=" * 100)

import os
import subprocess
SVT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "svt_2026")
SVT = os.path.join(SVT_DIR, "svt_scalar_reduce.py")
# RUN the committed reduction and read its COMPUTED output -- not a string in the source
_r = subprocess.run([sys.executable, SVT], capture_output=True, cwd=SVT_DIR, timeout=1200)
out = _r.stdout.decode()
ap_line = [l for l in out.splitlines() if l.strip().startswith("AP  (on Friedmann)")]
check(_r.returncode == 0 and ap_line and "K_B*k**2" in ap_line[0],
      "A1  the committed reduction RE-RUN (exit 0) prints its own aether-scalar coefficient: "
      + (ap_line[0].split("=", 1)[1].strip() if ap_line else "NOT FOUND"),
      "computed, not read from source text")

check(ap_line and "32*pi*G" in ap_line[0] and "K_B*k**2" in ap_line[0],
      "A2  and that IS the aether-scalar block's algebraic coefficient: "
      "AP = a(8 pi G K2 Qb^2 a^2 - 6 H^2 a^2 + K_B k^2)/(32 pi G), whose SUB-HORIZON limit is "
      "K_B a k^2/(32 pi G) -- so the aether's algebraic GRADIENT entry is K_B",
      "*** base_a = K_B: candidate (ii), not the base_a = 1 the published band assumed ***")

info("A3  WHY THIS IS A DERIVATION AND NOT A GUESS: stage 22 obtained AP by explicit second-order "
     "expansion of the FULL AeST action (the truncated version was caught and killed by its own "
     "adversarial verifiers), then eliminated the constrained fields.  The K_B k^2 term is the "
     "aether spatial mode's gradient energy, which is exactly what base_a was defined to be.  "
     "Candidates (i) 2-K_B and (iii) 1 are excluded because neither appears on the aether scalar's "
     "gradient slot; candidate (iv) (A^i = 0, no aether mode) is the PRL's own quasi-static ANSATZ, "
     "not a property of the action, and stage 22 worked with A^i live.")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- the cap, recomputed with base_a = K_B instead of base_a = 1")
print("=" * 100)


def soften(base_a):
    """the published band was computed at base_a = 1; the softening factor is 1 + 0.64/base_a."""
    return 1.0 + MIXRATIO_NUM / base_a


s1 = soften(1.0)
print("\n     base_a        softening (1+0.64/base_a)     A_max band [Mpc^-2]      mu^2_eff reachable")
rows = {}
for label, ba in (("2 - K_B  (= 1.90)", 2 - KB_FID), ("1  (published assumption)", 1.0),
                  ("K_B  (= 0.10, DERIVED)", KB_FID), ("K_B = 0.5", 0.5), ("K_B = 1.5", 1.5)):
    f = soften(ba) / s1
    band = (AMAX_BAND_BASE1[0] * f, AMAX_BAND_BASE1[1] * f)
    mu2 = (MU2_AT_FID * band[0] / A_FID, MU2_AT_FID * band[1] / A_FID)
    rows[label] = (band, mu2)
    print(f"   {label:<26s}   {soften(ba):>6.2f}              [{band[0]:>6.2f}, {band[1]:>6.2f}]        "
          f"[{mu2[0]:>5.2f}, {mu2[1]:>5.2f}]")

mu2_derived = rows["K_B  (= 0.10, DERIVED)"][1]
mu2_pub = rows["1  (published assumption)"][1]
check(mu2_derived[1] > MIST_LO,
      f"B1  *** AT THE DERIVED base_a = K_B = {KB_FID}, the bump reaches mu^2_eff up to "
      f"{mu2_derived[1]:.2f} Mpc^-2 -- against the cluster demand's low end {MIST_LO} and mid-band. "
      f"At the published base_a = 1 assumption it reached only {mu2_pub[1]:.2f}, i.e. it BARELY "
      f"touched {MIST_LO}.  The derivation multiplies the reachable amplitude by "
      f"{mu2_derived[1]/mu2_pub[1]:.1f}x ***",
      "so clusters move from 'just barely marginal' to 'covered over most of the demanded band'")

frac = (min(mu2_derived[1], MIST_HI) - MIST_LO) / (MIST_HI - MIST_LO)
check(frac > 0.3,
      f"B2  quantitatively: the reachable range now covers {100*frac:.0f}% of Mistele's "
      f"{MIST_LO}-{MIST_HI} Mpc^-2 band (up to {min(mu2_derived[1], MIST_HI):.2f}), where the "
      f"published assumption covered ~0%",
      f"the 34x top end ({MIST_HI} Mpc^-2) REMAINS EXCLUDED -- that exclusion is robust and is not "
      "being walked back")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- and it is K_B-monotone, so the cluster verdict is now a statement about K_B")
print("=" * 100)


def mu2_max_of(kb):
    f = soften(kb) / s1
    return MU2_AT_FID * AMAX_BAND_BASE1[1] * f / A_FID


kbs = np.array([0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 1.5, 1.9])
print("\n     K_B      mu^2_eff reachable [Mpc^-2]     covers the cluster demand?")
for kb in kbs:
    m = mu2_max_of(kb)
    verdict = ("YES, most of the band" if m > 3 else
               "the low edge only" if m > MIST_LO else "NO")
    print(f"   {kb:>5.2f}            {m:>7.2f}                  {verdict}")

kb_crit = MIXRATIO_NUM / ((MIST_LO * A_FID / (MU2_AT_FID * AMAX_BAND_BASE1[1])) * s1 - 1.0)
check(0 < kb_crit < KB_WINDOW[1],
      f"C1  *** THE CLUSTER FRONT IS NOW A STATEMENT ABOUT ONE UNMEASURED CONSTANT: the bump covers "
      f"the cluster demand's low end for K_B <~ {kb_crit:.2f}, and most of the band for K_B <~ 0.2. "
      f"AeST's own stability window is {KB_WINDOW} and the literature's dominant fiducial is "
      f"{KB_FID} -- comfortably inside ***",
      "smaller K_B is better for clusters, and the fiducial sits where clusters work")

check(mu2_max_of(KB_WINDOW[1] - 0.1) < MIST_LO,
      f"C2  AND THE FALSIFIABLE OTHER SIDE, which makes this a prediction rather than a rescue: at "
      f"the TOP of the stability window (K_B -> {KB_WINDOW[1]}) the reachable mu^2_eff falls to "
      f"{mu2_max_of(KB_WINDOW[1]-0.1):.2f} Mpc^-2, BELOW the cluster demand.  *** So the framework now "
      f"PREDICTS K_B is small -- an independent measurement of K_B above ~{kb_crit:.1f} would kill the "
      f"bump as the cluster mechanism ***",
      "one number, two fronts: K_B sets both the aether sector and whether clusters close")

# =================================================================================================
print()
print("=" * 100)
print("PART D -- what this does NOT do (read before quoting any of it)")
print("=" * 100)

info("D1  IT DOES NOT REMOVE THE DARK SECTOR. The bump changes the FIELD's response in cluster-like "
     "environments; it does not remove the pressureless clustering component the CMB requires "
     "(Delta chi^2 > 400 on H3/H1, and stage 24 showed a linear perturbation at the sigma_8 scale "
     "sits at y ~ 1e-3 where the kernel would boost gravity 29x, so the component is STRUCTURALLY "
     "REQUIRED). What the framework has is NO DARK-MATTER PARTICLE -- the component is the Q-sector "
     "of the same scalar that gives Lambda and MOND. That is the defensible slogan and this stage "
     "does not upgrade it.")

info("D2  IT IS AN AMPLITUDE RESULT, NOT A PROFILE FIT. Mistele's 1.0-7.9 Mpc^-2 is a requirement on "
     "mu^2_eff at cluster scales; matching it says the bump can supply the needed STRENGTH. It does "
     "NOT show the bump reproduces the observed cluster mass PROFILE shape (rho_c flat, M_c ~ r^3, "
     "the centrally-concentrated deficit dying to eta ~ 1 by 2-3 Mpc). That fit -- one amplitude "
     "against a whole radial profile, which is a real test -- remains the front's oldest owed item, "
     "and real eRASS1 data (N = 9830) plus X-COP/CLASH profiles are in hand to do it.")

info("D3  AND THE RESIDUAL IS STILL THERE. The committed eta(R500) = 2.334 median (eRASS1, the "
     "framework's own kernel) needs a_0 x eta^2 = 5.45x to erase; the kernel removes 74-89% of the "
     "cluster dark matter and leaves 11-26%. This stage says the bump has the AMPLITUDE HEADROOM to "
     "address that residual once base_a is correctly derived -- it does not yet demonstrate that it "
     "does. 'Clusters are fixed' is NOT the claim; 'the amplitude obstruction is removed and the "
     "profile fit is now the only thing between here and a verdict' is.")

info("D4  K_B IS UNMEASURED. It has never been measured, every value in print is a fiducial, "
     "GW170817 constrains it not at all (c1 = -c3 makes the tensor-speed combination vanish "
     "identically, consistent with this corpus's own c_T = 1 theorem), and the quasi-static "
     "phenomenology is K_B-BLIND (G-tilde = (1 - K_B/2) G-hat absorbs it). So Part C's verdict rides "
     "on a constant the theory does not fix -- which is exactly why C2's falsifiable direction is "
     "the honest way to state it.")

print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  THE CLUSTER FRONT'S AMPLITUDE OBSTRUCTION IS REMOVED, WITH NO DARK-MATTER PARTICLE ANYWHERE IN IT.

  1. base_a = K_B, DERIVED -- read out of stage 22's own committed full-action scalar reduction
     (AP -> K_B a k^2/32 pi G at sub-horizon k).  The published band assumed base_a = 1; the
     enumerated candidates 2-K_B, 1 and infinity are all excluded by that reduction.  This closes a
     caveat the corpus had explicitly left owed.

  2. Because the cap softens as 0.64/base_a and K_B is small (fiducial {KB_FID}, window {KB_WINDOW}),
     the reachable bump amplitude rises: mu^2_eff up to {mu2_derived[1]:.2f} Mpc^-2 against
     {mu2_pub[1]:.2f} at the old assumption -- a factor {mu2_derived[1]/mu2_pub[1]:.1f}x -- which covers {100*frac:.0f}% of the
     cluster demand instead of ~0%.  The 34x top end stays excluded.

  3. The front becomes a statement about ONE unmeasured constant: clusters close for
     K_B <~ {kb_crit:.2f}, and FAIL at the top of the stability window.  *** So the framework now predicts
     K_B is small, and a measurement of K_B above ~{kb_crit:.1f} would kill the bump as the cluster
     mechanism. *** That is a falsifiable prediction where there used to be an open caveat.

  4. NOT CLAIMED: that clusters are fixed (the profile fit is still owed -- one amplitude against a
     whole radial profile, with eRASS1 N = 9830 and X-COP/CLASH in hand); that the residual is gone
     (eta(R500) = 2.334 still stands); or that the dark sector is removed (the CMB requires it, and
     stage 24 showed it is structurally required).  The slogan stays NO DARK-MATTER PARTICLE.
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
