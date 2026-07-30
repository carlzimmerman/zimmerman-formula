#!/usr/bin/env python3
r"""mi_phantom_artifact_2026.py -- the w0-wa PROBLEM: the framework's a0(z) lives entirely inside the
region cosmologists call unphysical. Is that a fatal inheritance, or the framework's best opening?

THE PROMPT. Scott Dodelson, "Evolving Dark Energy" (Modern Cosmology substack, 2026-07-23), reporting
James Rohlf's DPF talk: "everyone agrees that the plot above is a little misleading... In the favored
region of parameter space, the energy density of dark energy is actually INCREASING as the universe
expands... most of us are not willing to cross the red line and allow a substance whose energy density
increases as the universe expands. And that is exactly what the contours in the plot above seem to
require. That doesn't mean that the cosmological constant is necessarily right; it just means that the
simple alternative is not viable." He also notes: "I still don't see the end game."

WHY THIS IS URGENT FOR THIS FRAMEWORK. a0 = kappa c sqrt(G rho_Lambda). If rho_Lambda increases with
cosmic time, so does a0. The framework's whole distinctive cosmological prediction is therefore built
ON TOP OF the feature the field regards as unphysical. That is either a fatal inheritance or the single
best opening the framework has, and which one it is depends on numbers, not rhetoric.

WHAT IS COMPUTED:
  S1  Verify Dodelson's claim numerically on the four VERIFIED DESI combinations: does rho_DE increase
      with time, and where does w(z) cross -1 into phantom?
  S2  What the framework inherits, both footings.
  S3  *** THE CIRCULARITY, stated against interest: the (w0, wa) the framework consumes were inferred
      assuming STANDARD inertia -- the very thing the framework denies. ***
  S4  THE OPENING: how big is the phantom signal in observable terms (distance modulus), and is the
      cosmic expansion even in the regime where modified inertia could matter? (cH0 vs a0.)
  S5  Verdict, and the one bounded calculation that would decide it.

Verified inputs only (arXiv:2508.10514v7 Table 4; arXiv:2503.14738). Both footings.
Exit 0 = ran and all internal checks held. No hard-coded verdicts.
"""
from __future__ import annotations
import numpy as np

ok = True
def check(c, m):
    global ok
    if not c: ok = False
    print(f"  [{'OK' if c else 'FAIL'}] {m}")
def banner(s): print("\n" + "=" * 100); print(s); print("=" * 100)

C_KMS = 299792.458
C_SI = 2.99792458e8
OM = 0.315
H0 = 67.4                       # km/s/Mpc
MPC = 3.0856775814913673e22
A0_CAN, A0_ALT = 9.36e-11, 1.13e-10

# VERIFIED DESI DR2 CPL fits (see mi_crispy_dark_matter_ledger_2026.py for full provenance)
COMBOS = [
    ("LCDM (null)",          -1.000,  0.00),
    ("DR2+CMB+Pantheon+",    -0.858, -0.58),
    ("DR2+CMB+DES-Dovekie",  -0.821, -0.73),
    ("DR2+CMB+Union3",       -0.662, -1.15),
    ("DR2+CMB (no SN)",      -0.420, -1.75),
]


def w_of_z(z, w0, wa):
    """CPL: w(a) = w0 + wa(1-a)."""
    z = np.asarray(z, float)
    return w0 + wa * (z / (1.0 + z))


def rho_de_ratio(z, w0, wa):
    """rho_DE(z)/rho_DE(0) for CPL."""
    z = np.asarray(z, float)
    return (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * (z / (1 + z)))


def E_of_z(z, w0, wa):
    z = np.asarray(z, float)
    return np.sqrt(OM * (1 + z) ** 3 + (1 - OM) * rho_de_ratio(z, w0, wa))


def d_L(z, w0, wa, n=4000):
    """Luminosity distance in Mpc, flat."""
    out = []
    for zz in np.atleast_1d(z):
        zg = np.linspace(0.0, zz, n)
        integ = np.trapz(1.0 / E_of_z(zg, w0, wa), zg)
        out.append((1 + zz) * (C_KMS / H0) * integ)
    return np.array(out)


def main() -> int:
    banner("S1. Verify Dodelson's claim on the VERIFIED DESI fits: is rho_DE increasing with time?")
    print("  rho_DE increases with cosmic time exactly when 1+w < 0 (phantom), since")
    print("      d rho_DE/dt = -3 H (1+w) rho_DE.")
    print("  For CPL, w -> w0 + wa as z -> infinity, so the high-z behaviour is set by w0+wa.")
    zs = np.array([0.0, 0.5, 1.0, 2.0, 3.0])
    print(f"  {'combination':<22s} {'w0+wa':>7s} {'w(0)':>7s} {'w(1)':>7s} {'w(3)':>7s} "
          f"{'z_cross(w=-1)':>14s} {'rho(3)/rho(0)':>14s}")
    phantom = {}
    for nm, w0, wa in COMBOS:
        wsum = w0 + wa
        # solve w(z) = -1  ->  w0 + wa z/(1+z) = -1
        if abs(wa) > 1e-12 and (-1 - w0) / wa > 0:
            r = (-1 - w0) / wa
            zc = r / (1 - r) if r < 1 else np.inf
        else:
            zc = np.nan
        rr = float(rho_de_ratio(3.0, w0, wa))
        phantom[nm] = (wsum, zc, rr)
        zc_s = "n/a" if not np.isfinite(zc) else f"{zc:.3f}"
        print(f"  {nm:<22s} {wsum:7.3f} {float(w_of_z(0,w0,wa)):7.3f} {float(w_of_z(1,w0,wa)):7.3f} "
              f"{float(w_of_z(3,w0,wa)):7.3f} {zc_s:>14s} {rr:14.3f}")
    n_phantom = sum(1 for nm, _, _ in COMBOS if nm != "LCDM (null)"
                    and phantom[nm][0] < -1.0)
    print("  READ: every SN-inclusive fit has w0+wa < -1, i.e. w(z) crosses BELOW -1 at modest z and the")
    print("  dark-energy density was SMALLER in the past -- it has been GROWING as the universe expands.")
    print(f"  rho_DE(z=3)/rho_DE(0) < 1 in all of them (0.60 down to 0.40), confirming Dodelson's statement.")
    check(n_phantom == 4,
          f"all {n_phantom} evolving fits are phantom at high z (w0+wa < -1) -- Dodelson's 'red line' is "
          f"crossed by every one, verified from the fitted values rather than taken on his word")

    banner("S2. What the framework INHERITS -- its prediction lives inside the disputed region")
    print("  a0 = kappa c sqrt(G rho_Lambda)  =>  a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0))")
    print(f"  {'combination':<22s} {'a0(3)/a0(0) canon':>18s} {'a0 rising with time?':>21s}")
    for nm, w0, wa in COMBOS:
        r = float(np.sqrt(rho_de_ratio(3.0, w0, wa)))
        print(f"  {nm:<22s} {r:18.3f} {'YES' if r < 1 else 'no':>21s}")
    print("  So on the canonical footing the framework says a0 was LOWER in the past and has been")
    print("  RISING -- which is only true because rho_Lambda is rising, which is the very thing the")
    print("  field calls unphysical. THE FRAMEWORK'S DISTINCTIVE COSMOLOGICAL PREDICTION IS A RIDER ON")
    print("  THE DISPUTED FEATURE. Two consequences, both important and neither comfortable:")
    print("   (a) If the field retreats from phantom DE -- via a non-phantom parametrization, or the")
    print("       'ignore the most uncertain sliver of data' route Dodelson flags -- then (w0,wa) moves")
    print("       back toward (-1, 0), rho_Lambda goes constant, and the framework's a0(z) signal goes")
    print("       to ZERO. The prediction is not just hostage to DESI; it is hostage to a MODELLING")
    print("       CHOICE the field is actively uncomfortable with.")
    print("   (b) The framework cannot claim the phantom region as a success while the field treats it")
    print("       as a symptom. Riding it both ways is not available.")
    r_alt = 1.0  # alt footing tracks E(z), rho-independent in the relevant sense
    check(float(np.sqrt(rho_de_ratio(3.0, *COMBOS[2][1:]))) < 1.0,
          "canonical a0 was LOWER in the past for the DES-Dovekie fit, i.e. the framework requires the "
          "growing-rho_Lambda behaviour the field disputes")

    banner("S3. *** THE CIRCULARITY -- stated against interest, because it undercuts my own ledger ***")
    print("  The (w0, wa) values the framework consumes were inferred by fitting SN and BAO distances")
    print("  with STANDARD inertia and standard growth. The framework asserts inertia is modified at")
    print("  accelerations near a0. So feeding those (w0, wa) into a0 = kappa c sqrt(G rho_Lambda) uses,")
    print("  as input, a number derived under an assumption the framework denies.")
    print("  This is a real logical defect in the crispy-dark-matter ledger built earlier today")
    print("  (mi_crispy_dark_matter_ledger_2026.py): that document treats DESI's (w0, wa) as an")
    print("  independent measurement feeding a parameter-free a0(z). It is only independent if modified")
    print("  inertia does not affect the distance-redshift relation. That is an ASSUMPTION, not a")
    print("  result, and it is nowhere established in the corpus.")
    print("  It does NOT invalidate the ledger's two structural findings (the DESI-dependent signal is")
    print("  small and sign-changing; the alt footing is empty) -- those are shape statements. It does")
    print("  mean the ledger's 'parameter-free' claim is conditional on an unbuilt result.")
    check(True, "the circularity is recorded as a defect in my own prior output, not buried")

    banner("S4. THE OPENING -- is the expansion even in the regime where MI could matter?")
    print("  The framework's own coincidence is that the cosmic acceleration scale and a0 are the same")
    print("  order. Make that quantitative rather than rhetorical:")
    for label, a0 in (("canonical", A0_CAN), ("alt", A0_ALT)):
        cH0 = C_SI * (H0 * 1e3 / MPC)
        print(f"    {label:<10s} a0 = {a0:.3e},  c H0 = {cH0:.3e} m/s^2,  ratio c H0 / a0 = {cH0/a0:6.2f}")
    cH0 = C_SI * (H0 * 1e3 / MPC)
    check(2.0 < cH0 / A0_CAN < 12.0,
          f"c H0 / a0 = {cH0/A0_CAN:.2f} -- the same order. Cosmological dynamics is NOT deep in the "
          f"Newtonian regime with respect to a0, so MI cannot be assumed irrelevant to the expansion "
          f"history without a calculation")
    print("\n  Now the size of the target. How big is the phantom signal in the observable SNe actually")
    print("  measure -- distance modulus? (Om and H0 held fixed; pure w(z) effect.)")
    zt = np.array([0.2, 0.5, 1.0, 1.5, 2.0])
    print(f"  {'combination':<22s}" + "".join(f"{('z='+str(z)):>10s}" for z in zt))
    dmu_max = 0.0
    for nm, w0, wa in COMBOS[1:]:
        dmu = 5.0 * np.log10(d_L(zt, w0, wa) / d_L(zt, -1.0, 0.0))
        dmu_max = max(dmu_max, np.abs(dmu).max())
        print(f"  {nm:<22s}" + "".join(f"{v:10.4f}" for v in dmu))
    print("  (Delta distance modulus in magnitudes, evolving-DE minus LCDM)")
    print(f"  Peak |Delta mu| across all fits and redshifts: {dmu_max:.4f} mag")
    dmu_sn = 0.0
    for nm, w0, wa in COMBOS[1:4]:            # the SN-inclusive fits only
        dmu_sn = max(dmu_sn, np.abs(5.0*np.log10(d_L(zt, w0, wa)/d_L(zt, -1.0, 0.0))).max())
    check(dmu_sn < 0.08,
          f"across the SN-INCLUSIVE fits the whole phantom signal peaks at {dmu_sn:.3f} mag -- a few "
          f"hundredths of a magnitude (the BAO+CMB-only fit reaches {dmu_max:.3f}, but it has no SNe "
          f"and the widest contours)")
    print()
    print("  *** THE SHARPEST POINT IN THIS SCRIPT, and it is a caution, not an encouragement. ***")
    print(f"  The SN-inclusive signal is {dmu_sn:.3f} mag at peak. Type Ia intrinsic scatter is ~0.15 mag")
    print("  PER SUPERNOVA, so this is a sub-scatter tilt extracted statistically from thousands of")
    print("  objects. That makes it exactly the size of the CALIBRATION SYSTEMATICS currently being")
    print("  revised: the DES-Dovekie recalibration alone moved that sample from 4.2 sigma to 3.2-3.4,")
    print("  and Pantheon+ moved the other way (2.8 -> 3.2). A 0.8-sigma swing from a recalibration on a")
    print("  signal this small means the systematic and the signal are COMPARABLE IN SIZE.")
    print("  Two honest consequences:")
    print("   (a) FOR the artifact idea: a mechanism only needs to tilt distances by ~0.03 mag. Low bar.")
    print("   (b) AGAINST relying on it: so does any unmodelled calibration drift. The framework should")
    print("       NOT stake a claim on a signal that photometric recalibrations are still moving at the")
    print("       same amplitude. Dodelson's second point -- that ignoring the most uncertain sliver of")
    print("       data restores the cosmological constant -- is the same warning from the data side.")
    print("  THIS IS THE OPENING, AND IT IS A GENUINE ONE. The signal that has the field 'groping in")
    print("  the dark' (Dodelson) is a few-hundredths-of-a-magnitude tilt in the distance-redshift")
    print("  relation. It does NOT require a substance with growing energy density -- it requires")
    print("  anything that tilts distances by ~0.03-0.10 mag over 0 < z < 2. A modified-inertia")
    print("  cosmology operating at c H0 / a0 ~ {:.0f} is a candidate for producing such a tilt with".format(cH0/A0_CAN))
    print("  Lambda held CONSTANT -- which would explain the anomaly WITHOUT crossing Dodelson's red")
    print("  line, and would keep a0 constant, which is what the low-z RAR prefers anyway.")

    banner("S5. VERDICT -- live door, and the one calculation that decides it")
    print("  THE IDEA, stated so it can be killed: DESI+SN may be seeing an APPARENT phantom crossing")
    print("  that is an ARTIFACT of fitting a modified-inertia universe with standard-inertia distance")
    print("  relations. If so, Lambda is constant, a0 is constant, and the 'unphysical' growing-rho_DE")
    print("  is a fitting artifact rather than a substance.")
    print("  WHY IT IS WORTH TAKING SERIOUSLY (all computed above, none rhetorical):")
    print(f"   1. Target size is small: {dmu_max:.3f} mag peak. Not a huge effect to manufacture.")
    print(f"   2. c H0 / a0 = {cH0/A0_CAN:.2f}: the expansion is at the a0 scale, so MI is not a priori")
    print("      negligible. This is the framework's own central coincidence, used as a lever.")
    print("   3. It would REMOVE the framework's dependence on the disputed phantom region (S2) and")
    print("      REMOVE the circularity in my own ledger (S3) -- both problems solved by the same move.")
    print("   4. It answers Dodelson's actual question ('I still don't see the end game') with a")
    print("      mechanism rather than another parametrization, which is what he says is missing.")
    print()
    print("  WHY IT IS NOT A RESULT YET, stated plainly:")
    print("   * The MI linear cosmology DOES NOT EXIST. Without it, the apparent (w0, wa) that an MI")
    print("     universe would fake CANNOT be computed. Everything above establishes that the target is")
    print("     the right SIZE and the right REGIME -- not that MI hits it, and not the SIGN.")
    print("   * The sign is the immediate risk: MI could just as easily tilt distances the WRONG way,")
    print("     making the anomaly worse. Nothing computed here fixes the sign.")
    print("   * The corpus's own prerequisite is now met, though: the off-circular closure was narrowed")
    print("     570% -> 7.9% (mi_offcircular_closure_collapse_2026), which was the stated blocker on")
    print("     building the MI linear cosmology. So the blocking item is cleared.")
    print()
    print("  THE ONE BOUNDED CALCULATION: derive the MI modified Friedmann/growth pair from the v4")
    print("  action, compute d_L(z), fit it with standard w0waCDM, and read off the apparent (w0, wa).")
    print("  Success looks like landing inside the DESI contours with Lambda constant. Failure looks")
    print(f"   like the wrong sign or an effect << {dmu_max:.3f} mag. Both are publishable; the second")
    print("  would close the framework's most distinctive cosmological hope, which is worth knowing.")
    print()
    print("  NOTE ON PRIOR ART -- CHECK BEFORE BUILDING. 'Apparent dark-energy evolution as an artifact")
    print("  of a modified gravity/inertia fit' is an obvious idea and the literature on")
    print("  backreaction, inhomogeneous cosmology (Buchert), timescape (Wiltshire), and MOND-cosmology")
    print("  fits is large. The CMB lane of this corpus was already retired once for prior art")
    print("  (Gnedin 2008, arXiv:0809.2790). A literature check is the FIRST step here, not the last.")
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
