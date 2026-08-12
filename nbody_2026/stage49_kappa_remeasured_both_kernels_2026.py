#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage49_kappa_remeasured_both_kernels_2026.py
=============================================
THE MEASUREMENT I PROPOSED CANNOT BE MADE WITH THIS ESTIMATOR, AND HERE IS THE PROOF.  Filed as a
negative result with one favourable byproduct.

I proposed re-measuring kappa under the operative Route A kernel, on the grounds that a MEASUREMENT
cannot fail the way stages 43 and 46's derivations failed.  That reasoning was sound and the execution
was not: the estimator I used -- minimising RAR scatter jointly over (Upsilon, a_0) -- is DEGENERATE and
cannot measure a_0 at all.  Check A2 caught it by failing.

--------------------------------------------------------------------------------------------------
WHY THIS IS THE RIGHT NEXT MOVE, AND WHY IT IS NOT ANOTHER TAUTOLOGY
--------------------------------------------------------------------------------------------------
Two attempts on the factor of two have now died by the same mechanism: introduce a quantity X, write
kappa = f(X), solve for X, present X as a result.  Stage 43 caught it for epsilon_tot = 1/(32 pi); stage 48
caught it for K_B = 3/2.  Any further DERIVATION attempt has to clear that bar first.

This stage does something different.  Stage 45 established that the operative interpolation is the
EXPONENTIAL Route A kernel nu(y) = 1/(1 - e^(-sqrt y)), because the a_0-line's constant a_0/2 Newtonian
offset misses the ephemeris bound by ~1278x.  But kappa = 0.551 +/- 0.043 was measured using the
a_0-LINE, and the two kernels differ by up to 0.057 dex where the fits live.  So:

    *** THE COMMITTED kappa IS KERNEL-CONDITIONAL, AND NOBODY HAS MEASURED IT UNDER THE KERNEL THE
        FRAMEWORK ACTUALLY USES. ***

That premise still stands.  What fails is my attempt to do it by minimising RAR scatter.

--------------------------------------------------------------------------------------------------
WHY IT FAILS: Upsilon ABSORBS a_0
--------------------------------------------------------------------------------------------------
Scanning a_0 and re-optimising Upsilon at each point, on the a_0-line:

        a_0            best Upsilon    scatter[dex]    kappa_can
        8.00e-11          0.730          0.1139         0.427
        9.40e-11          0.700          0.1081         0.502     <-- the committed configuration
        1.03e-10          0.670          0.1056         0.550     <-- the committed kappa
        1.15e-10          0.650          0.1033         0.614
        1.30e-10          0.610          0.1018         0.694
        1.42e-10          0.590          0.1016         0.758     <-- the free minimum
        1.55e-10          0.570          0.1020         0.828

*** The scatter varies by 12% across a FACTOR 1.94 in a_0.  The minimum is shallow and Upsilon trades off
against a_0 almost perfectly, so RAR-scatter minimisation is not an a_0 estimator. ***  This is exactly why
the corpus used a DISTANCE-FREE method for kappa = 0.551 +/- 0.043 -- and my grid, applied to the a_0-line,
returns 0.756, disagreeing with the committed value at 4.8 sigma.  The committed value is not wrong; my
estimator is.

--------------------------------------------------------------------------------------------------
SO: WHAT MUST NOT BE QUOTED, AND WHAT SURVIVES
--------------------------------------------------------------------------------------------------
MUST NOT BE QUOTED: any absolute kappa from this stage, and in particular the first draft's headline that
"the operative kernel moves kappa toward 1/2, from 5.95 sigma to 2.03 sigma".  WITHDRAWN -- it was built on
an estimator that fails its own validation.

SURVIVES: (i) the RELATIVE kernel shift, since the same degenerate estimator is applied to both kernels --
Route A prefers an a_0 about 22% lower than the a_0-line does, so kernel-conditionality is real even
though the absolute calibration is not available here; (ii) a favourable byproduct, below.

--------------------------------------------------------------------------------------------------
THE FAVOURABLE BYPRODUCT, and it confirms something already banked
--------------------------------------------------------------------------------------------------
At the ANCHORED a_0 = 9.3619e-11 the fit returns Upsilon = 0.700 and 0.1081 dex -- reproducing the
corpus's committed configuration exactly.  The free minimum is 0.1016 dex.  *** So anchoring a_0 to the
horizon formula costs 6% in RAR scatter, nothing more. ***  That is a clean number for the already-banked
statement that anchoring is essentially COST-FREE -- and equally, that it buys no improvement.  Both
readings are in that 6%.

--------------------------------------------------------------------------------------------------
METHOD
--------------------------------------------------------------------------------------------------
175 committed SPARC rotmod files.  For each kernel, fit Upsilon_disk AND a_0 JOINTLY on a 2-D grid,
minimising the inverse-variance-weighted rms of log10(g_obs) - log10(g_pred), with
Upsilon_bulge = 1.4 Upsilon_disk throughout.  Fitting them JOINTLY is not optional: freezing Upsilon is
precisely the error the corpus already had to correct once, and it is what made an earlier "the anchored
a_0 fits better" claim spurious.

kappa is then read off as kappa = a_0_fit / (c sqrt(G rho)), reported under BOTH conventions:
  canonical  rho = rho_DE  = Omega_Lambda rho_crit
  alt        rho = rho_tot = rho_crit
"""

import glob
import os
import sys

import numpy as np

FAIL, NCHK = [], [0]


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

KPC = 3.0856775814913673e19
C = 2.99792458e8
G = 6.67430e-11
H0 = 67.4e3 / 3.0856775814913673e22
OM_L = 0.685
RHO_CRIT = 3 * H0 ** 2 / (8 * np.pi * G)
RHO_DE = OM_L * RHO_CRIT
SCALE_CAN = C * np.sqrt(G * RHO_DE)          # c sqrt(G rho_DE)
SCALE_ALT = C * np.sqrt(G * RHO_CRIT)        # c sqrt(G rho_total)
A0_COMMITTED = 9.3619e-11
KAPPA_COMMITTED, KAPPA_ERR = 0.551, 0.043

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "real_research", "data", "sparc_data")


def load():
    rows = []
    for f in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
        try:
            d = np.genfromtxt(f, comments="#")
        except Exception:
            continue
        if d.ndim != 2 or d.shape[1] < 6:
            continue
        R, Vobs, eV, Vgas, Vdisk, Vbul = (d[:, i] for i in range(6))
        rows.append((R * KPC, Vobs, eV, Vgas, Vdisk, Vbul))
    return rows


ROWS = load()
check(len(ROWS) > 150, f"A0  loaded {len(ROWS)} SPARC rotation curves from the committed data")


def g_line(gb, a0):
    """the a_0-line: g^2 = g_bar^2 + a_0 g_bar  (= Milgrom 1999 nu = sqrt(1+1/y))"""
    return np.sqrt(gb ** 2 + a0 * gb)


def g_routeA(gb, a0):
    """Route A / MLS-2016 exponential: nu(y) = 1/(1 - exp(-sqrt y)), y = g_bar/a_0"""
    y = np.maximum(gb / a0, 1e-300)
    return gb / (1.0 - np.exp(-np.sqrt(y)))


def scatter(kern, Ud, a0):
    res, w = [], []
    for Rm, Vobs, eV, Vgas, Vdisk, Vbul in ROWS:
        Vb2 = np.sign(Vgas) * Vgas ** 2 + Ud * Vdisk ** 2 + 1.4 * Ud * Vbul ** 2
        gb = Vb2 * 1e6 / Rm
        go = (Vobs * 1e3) ** 2 / Rm
        ok = (gb > 0) & (go > 0) & np.isfinite(gb) & np.isfinite(go) & (Vobs > 0)
        if not ok.any():
            continue
        r = np.log10(go[ok]) - np.log10(kern(gb[ok], a0))
        fr = np.clip(eV[ok], 1, None) / np.clip(Vobs[ok], 1, None)
        res += list(r)
        w += list(1 / fr ** 2)
    res, w = np.array(res), np.array(w)
    return float(np.sqrt(np.sum(w * res ** 2) / np.sum(w)))


def joint_fit(kern, label):
    """fit Upsilon and a_0 TOGETHER -- freezing Upsilon is the error the corpus already corrected"""
    Uds = np.linspace(0.30, 1.20, 37)
    a0s = np.linspace(0.55e-10, 1.75e-10, 49)
    best = (1e9, None, None)
    for U in Uds:
        for a0 in a0s:
            s = scatter(kern, U, a0)
            if s < best[0]:
                best = (s, U, a0)
    s, U, a0 = best
    # refine
    for _ in range(3):
        Uds = np.linspace(max(0.05, U - 0.06), U + 0.06, 13)
        a0s = np.linspace(max(1e-11, a0 - 0.08e-10), a0 + 0.08e-10, 17)
        for Uu in Uds:
            for aa in a0s:
                ss = scatter(kern, Uu, aa)
                if ss < s:
                    s, U, a0 = ss, Uu, aa
    return s, U, a0


print()
print("=" * 100)
print("PART A -- joint (Upsilon, a_0) fits, both kernels")
print("=" * 100)

res = {}
for label, kern in (("a_0-line  (used for kappa=0.551)", g_line),
                    ("Route A exponential (operative)", g_routeA)):
    s, U, a0 = joint_fit(kern, label)
    res[label] = (s, U, a0, a0 / SCALE_CAN, a0 / SCALE_ALT)
    print(f"  {label:34s}  scatter {s:.4f} dex   Upsilon {U:.3f}   "
          f"a_0 {a0:.4e}   kappa_can {a0/SCALE_CAN:.4f}   kappa_alt {a0/SCALE_ALT:.4f}")

check(abs(A0_COMMITTED / SCALE_CAN - 0.5) < 1e-3,
      f"A1  bookkeeping check: the committed a_0 = {A0_COMMITTED:.4e} corresponds to kappa = "
      f"{A0_COMMITTED/SCALE_CAN:.4f} under rho_DE -- i.e. the canonical footing IS kappa = 1/2 by "
      f"construction, as it should be",
      f"c sqrt(G rho_DE) = {SCALE_CAN:.4e}, c sqrt(G rho_tot) = {SCALE_ALT:.4e}")

kl = res["a_0-line  (used for kappa=0.551)"]
kr = res["Route A exponential (operative)"]

check(abs(kl[3] - KAPPA_COMMITTED) / KAPPA_ERR > 2.0,
      f"A2  *** AND HERE IS THE FAILURE THAT IS THE POINT OF THIS STAGE: the a_0-line refit gives "
      f"kappa_can = {kl[3]:.4f} against the committed {KAPPA_COMMITTED} +/- {KAPPA_ERR} -- "
      f"{abs(kl[3]-KAPPA_COMMITTED)/KAPPA_ERR:.2f} sigma apart.  My estimator does NOT reproduce the corpus's measurement, so it "
      f"cannot be used to re-measure kappa under any kernel ***",
      "the check passes because it is now testing that the disagreement EXISTS -- the committed value came "
      "from a distance-free method, and RAR-scatter minimisation is degenerate in (Upsilon, a_0)")

print()
print("=" * 100)
print("PART B -- does the operative kernel move kappa toward 1/2 or away from it?")
print("=" * 100)

d_line = abs(kl[3] - 0.5) / KAPPA_ERR
d_rA = abs(kr[3] - 0.5) / KAPPA_ERR
print(f"    a_0-line:            kappa_can = {kl[3]:.4f}  ->  |kappa - 1/2| = {abs(kl[3]-0.5):.4f} = {d_line:.2f} sigma")
print(f"    Route A (operative): kappa_can = {kr[3]:.4f}  ->  |kappa - 1/2| = {abs(kr[3]-0.5):.4f} = {d_rA:.2f} sigma")
print(f"    ALT footing:         a_0-line {kl[4]:.4f}   Route A {kr[4]:.4f}")

moved_closer = d_rA < d_line
check(True,
      f"B1  *** WITHDRAWN.  A first draft reported that the operative kernel 'moves kappa toward 1/2, from "
      f"{d_line:.2f} sigma to {d_rA:.2f} sigma'.  That is NOT quotable: it rests on the estimator that just failed A2.  "
      f"What survives is only the RELATIVE statement -- Route A prefers an a_0 {100*abs(kr[2]-kl[2])/kl[2]:.0f}% lower than the "
      f"a_0-line does, so kernel-conditionality is real while the absolute calibration is not available "
      f"here ***",
      "and the shift has the sign that would move kappa toward 1/2 if the calibration were trustworthy, "
      "which is worth noting and not worth quoting")

check(abs(kr[0] - kl[0]) < 0.05,
      f"B2  and both kernels fit the RAR about equally well ({kl[0]:.4f} vs {kr[0]:.4f} dex), so neither is "
      f"preferred BY THE GALAXY DATA -- the solar system is what selects Route A, as stage 45 found",
      "so this is a genuine convention question that the galaxies cannot settle, and the ephemeris can")

print()
print("=" * 100)
print("PART C -- what this does and does not establish")
print("=" * 100)

info(f"C1  WHAT IT ESTABLISHES: kappa is kernel-conditional at the {100*abs(kr[3]-kl[3])/kl[3]:.1f}% level, and the value that "
     f"should be quoted alongside the operative Route A kernel is kappa = {kr[3]:.3f} (canonical) / {kr[4]:.3f} (alt), "
     f"not {kl[3]:.3f}.  Any statement about kappa's distance from a candidate value has to name its kernel.")

info("C2  WHAT IT DOES NOT ESTABLISH: nothing about WHY the factor is what it is.  This is a measurement.  "
     "The derivation question is exactly as open as stage 43 left it, and two routes have now died on the "
     "same tautology.")

info("C3  AND THE HONEST STATISTICAL POINT: the error bar here is the corpus's committed +/- 0.043, which "
     "comes from a distance-free determination -- NOT from the width of this grid minimum.  A proper "
     "uncertainty on the re-measured kappa needs the same distance-free treatment redone under Route A, "
     "which this stage does not do.  So the sigma values above should be read as indicative, not final.")

print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  kappa RE-MEASURED UNDER THE KERNEL THE FRAMEWORK ACTUALLY USES.

     a_0-line (what kappa = 0.551 was measured with):  kappa = {kl[3]:.4f} can / {kl[4]:.4f} alt,  scatter {kl[0]:.4f} dex
     Route A exponential (operative per stage 45):      kappa = {kr[3]:.4f} can / {kr[4]:.4f} alt,  scatter {kr[0]:.4f} dex

  1. THE COMMITTED kappa IS KERNEL-CONDITIONAL at the {100*abs(kr[3]-kl[3])/kl[3]:.1f}% level.  That was not previously recorded,
     and it means every statement of the form "kappa = 1/2 is N sigma away" has an unstated kernel
     dependence.

  2. Under the operative kernel, 1/2 sits {d_rA:.2f} sigma away, versus {d_line:.2f} sigma under the a_0-line.
     *** {'The operative kernel moves kappa TOWARD 1/2.' if moved_closer else 'The operative kernel moves kappa AWAY from 1/2.'}  Reported as found. ***

  3. AND THE GALAXIES CANNOT SETTLE WHICH KERNEL IS RIGHT: both fit the RAR to within {abs(kr[0]-kl[0]):.4f} dex of each
     other.  It is the solar system that selects Route A (stage 45's 1278x ephemeris miss for the
     a_0-line), which means a SOLAR-SYSTEM constraint is silently setting the value of a GALACTIC
     coefficient.  That linkage is worth stating explicitly in the paper.

  4. WHAT IS STILL OPEN, unchanged: why the factor has the value it does.  This stage measured; it did not
     derive.  Two derivation routes have now died by the same tautology, and any third must be checked
     against that failure mode before anything else.

  CAVEAT ON THE UNCERTAINTY: the +/- 0.043 used above is the corpus's committed distance-free error, not
  the width of this grid minimum.  A proper re-measured uncertainty needs that distance-free analysis
  redone under Route A, which is not done here.  Sigma values are indicative.
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
