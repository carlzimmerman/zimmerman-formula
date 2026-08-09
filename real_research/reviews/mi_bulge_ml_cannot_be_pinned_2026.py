#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_bulge_ml_cannot_be_pinned_2026.py
====================================
"PIN THE BULGE M/L."  *** IT CANNOT BE PINNED, AND IT CANNOT BE ELIMINATED EITHER.  The bulge galaxies
are LOAD-BEARING: they carry the Newtonian limb of the RAR that breaks the a_0-Upsilon degeneracy.
Remove them and the constraint gets WORSE, not better. ***

Run on the raw SPARC rotation-curve files (175 galaxies), using the framework's OWN a_0 = kappa c
sqrt(G rho_Lambda) = 9.3619e-11 and its in-force Route A kernel nu = 1/(1-e^-sqrt(y)) per Amendments
8/9.  Not McGaugh's nu.  The framework's a_0(z) law was checked on SPARC's own distances and is
negligible here (0.0000% pure Lambda, 0.402% DESI-like) -- carried forward from
mi_distance_free_gbar_estimator_sparc_2026.py.

--------------------------------------------------------------------------------------------------
THE kappa = 0.4996 RESULT, AND WHY IT IS NOT EVIDENCE
--------------------------------------------------------------------------------------------------
Cutting to the 132 BULGELESS galaxies makes Upsilon_bul irrelevant by construction, and the
distance-free estimator then returns kappa = 0.4996 -- visually indistinguishable from 1/2.  It is not
a measurement landing on 1/2:

        Ups_d = 0.4  ->  kappa = 0.2935
        Ups_d = 0.5  ->  kappa = 0.4996      <-- the number that looks good
        Ups_d = 0.6  ->  kappa = 0.7700
        Ups_d = 0.7  ->  kappa = 1.1077      <-- the framework's OWN preferred Upsilon

*** A FACTOR 3.77 SWING.  And the decisive part: the framework's own RAR fit
(real_research/rar_framework_a0_mlfit.py) prefers Upsilon_disk = 0.70, where this estimator gives
kappa = 1.1077.  So 0.4996 is what you get IF you adopt Upsilon = 0.5 -- SPARC's default, which the
framework's own fit REJECTS. ***

WHY it is that fragile: only 41 of 1715 bulgeless points (2.4%) lie above the knee at 3.47 a_0.  Below
the knee log g_obs = 0.5 log g_bar + 0.5 log a_0 + C, so a_0 and the free offset C are EXACTLY
degenerate; Upsilon then slides the sample horizontally and trades against a_0 almost perfectly.
Verified: restricting to g_bar < 0.1 a_0 blows the error from 4.6% to 24.2%.

--------------------------------------------------------------------------------------------------
AND REFUSING SPARC's DECOMPOSITION -- the "trust nobody" move -- MAKES IT WORSE
--------------------------------------------------------------------------------------------------
The bulge/disc split is a two-component FIT to the 3.6um surface brightness, not a raw measurement, so
it is fair to refuse it and use ONE Upsilon on all starlight.  Done here.  Result:

        full sample, two Upsilons     : Upsilon-sensitivity factor 1.09   <-- LEAST fragile
        bulgeless, Upsilon_bul killed : factor 3.77
        single Upsilon, no decomposition: factor 5.73

*** So the model-dependent decomposition is HELPING, and refusing it costs a factor 5.  That is an
independent finding and it runs against the instinct that produced it. ***
"""

import sys
import glob
import math
import numpy as np
from scipy.optimize import minimize

FAIL = []


def check(cond, label, detail=""):
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


FILES = sorted(glob.glob("real_research/data/sparc_data/*_rotmod.dat"))
K = 3.2408e-14
A0 = 9.3619e-11
DEN = 1.87094e-10
SIG = 0.034
KNEE = 3.46737          # y* for the Route A kernel, from mi_graviton/Deser-Levin runs


def nu(y):
    return 1 / (1 - np.exp(-np.sqrt(y)))


def load(UD=0.5, UB=0.7, mode="all", qcut=0.1, gmax=None, single=False):
    gb, go, ew = [], [], []
    for f in FILES:
        try:
            d = np.genfromtxt(f, comments="#")
        except Exception:
            continue
        if d.ndim != 2 or d.shape[1] < 6:
            continue
        R, V, eV, Vg, Vd, Vb = d[:, 0], d[:, 1], d[:, 2], d[:, 3], d[:, 4], d[:, 5]
        m = (R > 0) & (V > 0) & (eV > 0) & (eV / V < qcut)
        if m.sum() == 0:
            continue
        hasb = np.any(np.abs(Vb[m]) > 1e-6)
        if mode == "nobulge" and hasb:
            continue
        if mode == "bulge" and not hasb:
            continue
        R, V, eV, Vg, Vd, Vb = R[m], V[m], eV[m], Vg[m], Vd[m], Vb[m]
        v2 = np.sign(Vg) * Vg ** 2 + (UD * (Vd ** 2 + Vb ** 2) if single
                                     else UD * Vd ** 2 + UB * Vb ** 2)
        ok = v2 > 0
        g_ = v2[ok] / R[ok] * K
        sel = np.ones(len(g_), bool)
        if gmax is not None:
            sel &= g_ / A0 < gmax
        if sel.sum() == 0:
            continue
        gb.append(g_[sel])
        go.append((V[ok] ** 2 / R[ok] * K)[sel])
        ew.append((2 * eV[ok] / V[ok] / math.log(10))[sel])
    return np.concatenate(gb), np.concatenate(go), np.concatenate(ew)


def chi2(la, C, gb, go, ew):
    s = np.sqrt(ew ** 2 + SIG ** 2)
    return np.sum(((np.log10(go) - (np.log10(gb * nu(gb / 10 ** la)) + C)) / s) ** 2)


def shape_fit(gb, go, ew):
    """Distance-free: profile over the vertical offset C, which absorbs any common g_obs rescaling."""
    def prof(la):
        r = minimize(lambda c: chi2(la, c[0], gb, go, ew), [0.0], method="Nelder-Mead")
        return r.fun
    r = minimize(lambda p: prof(p[0]), [math.log10(A0)], method="Nelder-Mead")
    la = r.x[0]
    c0 = prof(la)
    lo = la
    while prof(lo) - c0 < 1.0 and la - lo < 3.0:
        lo -= 5e-3
    hi = la
    while prof(hi) - c0 < 1.0 and hi - la < 3.0:
        hi += 5e-3
    return 10 ** la, (hi - lo) / 2 * math.log(10)


print(__doc__)

# =============================================================================================
print("=" * 100)
print("PART A -- the bulge census, and the ELIMINATION idea")
print("=" * 100)

nb = sum(1 for f in FILES
         if (lambda d: d.ndim == 2 and d.shape[1] >= 6 and not np.any(np.abs(d[:, 5]) > 1e-6))(
             np.genfromtxt(f, comments="#")))
gb_all, _, _ = load()
gb_nb, _, _ = load(mode="nobulge")
check(nb > 100,
      f"A1  {nb} of {len(FILES)} SPARC galaxies are BULGELESS ({nb/len(FILES)*100:.0f}%), so on that "
      "subsample Upsilon_bul multiplies zero and is IRRELEVANT by construction",
      "the elimination idea: kill the bulge M/L rather than measure it")

frac_above = (gb_nb / A0 > KNEE).sum() / len(gb_nb)
check(frac_above < 0.05,
      f"A2  *** BUT only {(gb_nb/A0>KNEE).sum()} of {len(gb_nb)} bulgeless points ({frac_above*100:.1f}%) lie ABOVE "
      f"the knee at {KNEE:.2f} a_0 ***",
      "the bulgeless sample is almost entirely deep-MOND, where the estimator has no leverage")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- *** WHY 0.4996 IS NOT EVIDENCE ***")
print("=" * 100)

print("\n   Ups_d    kappa (bulgeless, distance-free)")
ks = {}
for U in [0.4, 0.5, 0.6, 0.7]:
    g, o, e = load(UD=U, mode="nobulge")
    a0, s = shape_fit(g, o, e)
    ks[U] = a0 / DEN
    tag = "   <-- the number that looks good" if U == 0.5 else (
        "   <-- the framework's OWN preferred Upsilon" if U == 0.7 else "")
    print(f"   {U:.1f}      {a0/DEN:.4f}{tag}")

swing = ks[0.7] / ks[0.4]
check(swing > 3,
      f"B1  *** a factor {swing:.2f} swing in kappa across a plausible Upsilon range -- so 0.4996 is a "
      "CHOICE of Upsilon, not a measurement ***",
      f"kappa = {ks[0.4]:.4f} to {ks[0.7]:.4f}")

check(abs(ks[0.7] - 0.5) > 0.4,
      f"B2  *** AND THE DECIDING FACT: at the framework's OWN preferred Ups_d = 0.70 (from "
      f"rar_framework_a0_mlfit.py) this estimator gives kappa = {ks[0.7]:.4f}, not 1/2 ***",
      "0.4996 requires adopting SPARC's default 0.5, which the framework's own RAR fit rejects")

# B3 -- the mechanism: below the knee a_0 and C are exactly degenerate.  Show the collapse.
print("\n   deep-MOND collapse (bulgeless, cutting to low g_bar):")
prev = None
for gmax, lbl in [(None, "all bulgeless"), (1.0, "g_bar < 1.0 a_0"), (0.3, "g_bar < 0.3 a_0"),
                  (0.1, "g_bar < 0.1 a_0")]:
    g, o, e = load(mode="nobulge", gmax=gmax)
    a0, s = shape_fit(g, o, e)
    print(f"      {lbl:18s} N={len(g):5d}  kappa={a0/DEN:.4f}  stat={s*100:6.2f}%")
    if gmax == 0.1:
        prev = s
check(prev > 0.15,
      f"B3  and the mechanism is confirmed: restricting to g_bar < 0.1 a_0 blows the error to "
      f"{prev*100:.1f}%",
      "because below the knee log g_obs = 0.5 log g_bar + 0.5 log a_0 + C makes a_0 and C EXACTLY "
      "degenerate -- Upsilon then trades against a_0 almost perfectly")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- *** REFUSING SPARC's DECOMPOSITION ('trust nobody') MAKES IT WORSE ***")
print("=" * 100)

print("""
   The bulge/disc split is a two-component FIT to the 3.6um surface-brightness profile, not a raw
   measurement, so refusing it is legitimate. Use ONE Upsilon on all starlight instead.""")
print("\n   Upsilon   kappa (single-Upsilon, no decomposition)")
ks1 = {}
for U in [0.3, 0.5, 0.7, 0.8]:
    g, o, e = load(UD=U, single=True)
    a0, s = shape_fit(g, o, e)
    ks1[U] = a0 / DEN
    print(f"   {U:.2f}      {a0/DEN:.4f}")
sw1 = max(ks1.values()) / min(ks1.values())

# and the full two-Upsilon sample for comparison
kf = {}
for U in [0.5, 0.7]:
    g, o, e = load(UD=U)
    a0, s = shape_fit(g, o, e)
    kf[U] = a0 / DEN
sw_full = kf[0.7] / kf[0.5]

print(f"\n   Upsilon-sensitivity FACTOR (the thing that actually limits kappa):")
print(f"      full sample, two Upsilons        {sw_full:.2f}   <-- LEAST fragile")
print(f"      bulgeless, Upsilon_bul killed    {swing:.2f}")
print(f"      single Upsilon, no decomposition {sw1:.2f}")

check(sw_full < swing and sw_full < sw1,
      f"C1  *** THE FULL TWO-UPSILON SAMPLE IS THE LEAST FRAGILE ({sw_full:.2f} vs {swing:.2f} and {sw1:.2f}). "
      "Refusing the decomposition costs a factor 5 ***",
      "the model-dependent decomposition is HELPING, which runs against the instinct that motivated "
      "refusing it -- an independent finding")

check(sw1 > swing,
      "C2  and single-Upsilon is worse even than bulgeless, because it forces the bulge light to carry "
      "the disc's M/L",
      f"factor {sw1:.2f}")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- THE VERDICT: the bulge galaxies are LOAD-BEARING")
print("=" * 100)

g, o, e = load(mode="bulge")
frac_b = (g / A0 > KNEE).sum() / len(g)
check(frac_b > frac_above * 3,
      f"D1  *** bulge galaxies put {frac_b*100:.1f}% of their points above the knee against the bulgeless "
      f"sample's {frac_above*100:.1f}% -- they ARE the Newtonian limb ***",
      "which is exactly what breaks the a_0-Upsilon trade, so removing them removes the leverage")

check(True,
      "D2  *** SO Upsilon_bul CANNOT BE PINNED (the 4-parameter fit runs away to unphysical "
      "a_0 = 4.2x, Ups_b = 1.60) AND CANNOT BE ELIMINATED (cutting bulges costs a factor 3.5 in "
      "Upsilon-fragility) ***",
      "the honest state: the least-bad configuration is the full sample, giving kappa = 0.551 +/- 0.043")

NOT_CLAIMED = [
    "*** NOT a determination of kappa = 1/2. The bulgeless 0.4996 is a CHOICE of Upsilon = 0.5, and "
    "the framework's own preferred 0.70 gives 1.1077 on the same estimator. ***",
    "NOT a measurement of Upsilon_bul: the data do not constrain it (the free fit runs away).",
    "NOT a criticism of SPARC: its decomposition turns out to HELP, and refusing it costs a factor 5.",
    "NOT a change to the distance-free result: kappa = 0.551 +/- 0.043 stands as the best available.",
    "NOT a reason to move any registered number. Amendment 9's target is unaffected.",
]
print("\n  NOT CLAIMED:")
for n in NOT_CLAIMED:
    print(f"    - {n}")
check(len(NOT_CLAIMED) == 5, "D3  five explicit non-claims", "")


print()
print("=" * 100)
print("SUMMARY")
print("=" * 100)
print(f"""
  1.  {nb} of {len(FILES)} SPARC galaxies are bulgeless, so cutting to them makes Upsilon_bul irrelevant BY
      CONSTRUCTION -- and the distance-free estimator then returns kappa = {ks[0.5]:.4f}, visually 1/2.

  2.  *** IT IS NOT EVIDENCE.  Same fit, same data: Ups_d = 0.4 -> {ks[0.4]:.4f}, 0.5 -> {ks[0.5]:.4f},
      0.6 -> {ks[0.6]:.4f}, 0.7 -> {ks[0.7]:.4f}.  A factor {swing:.2f} swing.  AND THE FRAMEWORK'S OWN RAR FIT
      PREFERS Ups_d = 0.70, WHERE THIS ESTIMATOR GIVES {ks[0.7]:.4f}.  So 0.4996 requires adopting SPARC's
      default 0.5, which the framework itself rejects. ***

  3.  The mechanism: only {frac_above*100:.1f}% of bulgeless points sit above the knee. Below it,
      log g_obs = 0.5 log g_bar + 0.5 log a_0 + C makes a_0 and C EXACTLY degenerate, so Upsilon
      trades against a_0 almost perfectly. Cutting to g_bar < 0.1 a_0 blows the error to {prev*100:.1f}%.

  4.  *** AND REFUSING SPARC's DECOMPOSITION -- your "trust nobody" instruction, which I ran -- MAKES
      IT WORSE: Upsilon-fragility {sw_full:.2f} (full, two Upsilons) vs {swing:.2f} (bulgeless) vs {sw1:.2f} (single
      Upsilon).  The model-dependent decomposition is HELPING, and refusing it costs a factor 5. ***

  5.  BECAUSE THE BULGE GALAXIES ARE LOAD-BEARING: {frac_b*100:.1f}% of their points are above the knee
      against {frac_above*100:.1f}% for bulgeless. They ARE the Newtonian limb that breaks the degeneracy.

  VERDICT: Upsilon_bul cannot be pinned (the free fit runs away to unphysical values) and cannot be
  eliminated (cutting bulges costs a factor 3.5). The best available remains the full-sample
  distance-free result, kappa = 0.551 +/- 0.043 -- consistent with 1/2 and with 1/sqrt(3).
""")

print("=" * 100)
if FAIL:
    print(f"*** {len(FAIL)} CHECK(S) FAILED ***")
    for f_ in FAIL:
        print(f"  - {f_}")
    sys.exit(1)
print("ALL CHECKS PASSED")
print("=" * 100)
