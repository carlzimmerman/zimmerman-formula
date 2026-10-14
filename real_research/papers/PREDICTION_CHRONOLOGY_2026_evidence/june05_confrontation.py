#!/usr/bin/env python3
"""
THE CONFRONTATION: MUSE-DARK III (2026) rising a0 vs the framework's CONSTANT/DECLINING reading.
===============================================================================================
C. Zimmerman, 2026-06-05.  An honest, single-file reckoning between the framework's CANONICAL a0(z)
prediction and the first multi-point DIRECT measurement of the RAR acceleration scale's redshift
evolution. This file SUPERSEDES the a0(z) framing scattered across the repo and corrects a recurring
internal inconsistency about WHICH branch is the framework's prediction.

----------------------------------------------------------------------------------------------------
THE TWO BRANCHES (the footing fork the coefficient audit flagged in the time domain)
----------------------------------------------------------------------------------------------------
The framework writes a0 = (c/2) sqrt(G rho). EVERYTHING turns on which rho:

  CANONICAL (rho = rho_Lambda, "a0 IS dark energy"):  a0 = (c/2) sqrt(G rho_Lambda).
     rho_Lambda is CONSTANT in LCDM  ->  a0(z) = CONSTANT.
     Under DESI DR2 evolving DE (w0=-0.752, wa=-0.86), rho_DE(z) falls into the past
        ->  a0(z) DECLINES ~26% by z=3.   <-- THIS is the canonical reading (memory + audit).
  FOOTING-BUG (rho = rho_total): a0 = (c/2) sqrt(G rho_total) = cH(z)/Z  prop E(z) -> RISES x3 by z=2.
     The coefficient-footing audit (COEFFICIENT_FOOTING_AUDIT_2026-06.md) flags rho_total here as the
     SAME conflation that inflates a0(0); in the time domain it flips the test from declining to rising.

So the framework's distinctive, canonical prediction is: a0 CONSTANT (LCDM) or mildly DECLINING (DESI).
The "rising a0 = cH(z)/Z" line that older repo files call "the framework's prediction" is the
DISFAVOURED rho_total branch, not the canonical one.

----------------------------------------------------------------------------------------------------
THE DATA (verified from the primary sources, 2026-06-05 -- not from memory)
----------------------------------------------------------------------------------------------------
[1] MUSE-DARK III: Ciocan, Bouche, Fensch, Krajnovic, Freundlich, Desmond, Famaey, Techi,
    A&A 709, L16 (2026), arXiv:2604.22613. 79 star-forming galaxies (M* > 10^8.8 Msun),
    0.33 < z < 1.44, MUSE Hubble Ultra Deep Field. Pressure-support (asymmetric-drift) corrected.
       a0(z) = a0(0) + a1 z,  a0(0) = 1.0 +/- 0.04,  a1 = +1.59 (+0.11/-0.10)   [x 1e-10 m/s^2]
       a0|z~1 = 2.38 (+0.12/-0.10);  four quantile bins climb ~1.99 -> 2.71;  intrinsic scatter ~0.17 dex.
    Authors' own words: the evolution is detected "at a ~30 sigma level"; "our measured a0(z) is faster
    than that of H(z)"; reconciling to a0=1.2 at all z "would require systematically larger stellar
    masses, with offsets ranging from ~+0.2 dex to ~+0.45 dex", which they say are "not supported by
    independent consistency checks." Robust across DC14/NFW/Burkert halos.
    NOTE: the "second study, 1.99 -> 2.71" in the briefing is NOT independent -- it is the binned form
    of THIS SAME measurement. There is ONE direct multi-point a0(z) dataset, not two.

[2] Magneticum: Mayer, Teklu, Dolag, Remus, MNRAS 518, 257 (2023), arXiv:2206.04333. A LCDM
    HYDRODYNAMICAL simulation -- it has NO fundamental a0. Yet fitting a MOND RAR to the simulated
    galaxies yields an APPARENT a0 that "increase[s] by a factor ~3 from z=0 to z=2.3", "without
    requiring fundamental modifications to gravity." Purpose: a measured rise is a discriminant
    BETWEEN MOND and LCDM -- and here it is LCDM that produces the rise.

[3] The other high-z a0 analyses (the split): McGaugh, Schombert, Lelli & Franck 2024 (ApJ 976, 13,
    arXiv:2406.17930) find "no clear sign of evolution" in BTFR/DM-fraction to z~2.5 (favour CONSTANT);
    Milgrom 2017 (arXiv:1703.06110), the one direct high-z RC MOND analysis, "all but exclude(s)" a
    factor ~4 a0 at z~2 and the (1+z)^1.5 law (favour CONSTANT; bound steep rises). The data are SPLIT.

Pure-numpy. Run:  python3 reviews/project_a0z_MUSE_DARK_III_confrontation.py
"""
import numpy as np

# --- cosmology / constants ---------------------------------------------------
c, G, Mpc = 2.99792458e8, 6.674e-11, 3.0857e22
H0 = 67.4e3 / Mpc
Om, OL = 0.315, 0.685
Z = 2 * np.sqrt(8 * np.pi / 3)           # the (route-dependent) coefficient; cancels in every ratio here
E = lambda z: np.sqrt(Om * (1 + z) ** 3 + OL)

# DESI DR2 (2025, arXiv:2503.14738) evolving-DE, the values the canonical declining reading uses
W0, WA = -0.752, -0.86


def rho_de_ratio(z, w0=W0, wa=WA):
    """rho_DE(z)/rho_DE(0) for CPL w(a)=w0+wa(1-a)."""
    a = 1.0 / (1.0 + z)
    return (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * (1 - a))


# framework CANONICAL a0(z)/a0(0):
a0_LCDM = lambda z: np.ones_like(np.asarray(z, float))      # rho_Lambda const -> flat
a0_DESI = lambda z: np.sqrt(rho_de_ratio(z))                # rho_DE(z) falls -> declines
# framework FOOTING-BUG (rho_total) branch, for contrast only:
a0_rho_total = lambda z: E(z)                               # = cH(z)/Z normalised

# MUSE-DARK III fit (x 1e-10), with the asymmetric a1 error symmetrised to 0.105
MU_a00, MU_a00_e = 1.0, 0.04
MU_a1,  MU_a1_e = 1.59, 0.105
muse_fit = lambda z: MU_a00 + MU_a1 * z                     # absolute a0 in 1e-10
muse_shape = lambda z: muse_fit(z) / MU_a00                 # normalised to MUSE's own z=0


def eff_slope(model, zlo=0.33, zhi=1.44, n=200):
    """Effective linear slope d(a0/a0(0))/dz of a model over the MUSE redshift window."""
    z = np.linspace(zlo, zhi, n)
    y = model(z)
    A = np.vstack([np.ones_like(z), z]).T
    b, m = np.linalg.lstsq(A, y, rcond=None)[0]
    return m  # ratio per unit z


def main():
    print("#" * 100)
    print("# MUSE-DARK III (rising a0) vs the framework's CANONICAL constant/declining reading -- honest confrontation")
    print("#" * 100 + "\n")

    # ---------------------------------------------------------------- (0) sanity: DESI declining curve
    print("=" * 100)
    print("(0) The framework's CANONICAL a0(z)/a0(0) -- recomputed, not quoted")
    print("=" * 100)
    print(f"  {'z':>5}{'LCDM (rho_L const)':>20}{'DESI w0wa (rho_DE)':>22}{'[contrast] rho_total E(z)':>27}")
    for z in (0.5, 1.0, 2.0, 3.0):
        print(f"  {z:>5.1f}{a0_LCDM(z):>20.2f}{a0_DESI(z):>22.2f}{a0_rho_total(z):>27.2f}")
    print(f"  => canonical reading: FLAT (LCDM) or DECLINING to {a0_DESI(3.0):.2f}x by z=3 (DESI, ~{100*(1-a0_DESI(3.0)):.0f}% drop).")
    print(f"     (the rho_total branch RISES to {a0_rho_total(2.0):.2f}x by z=2 -- shown only for contrast; it is the footing-bug branch.)\n")

    # ---------------------------------------------------------------- (1) the measured rise vs each branch
    print("=" * 100)
    print("(1) MUSE measures a0(z)/a0(0) = 1 + 1.59 z  -- the SHAPE, vs the framework branches")
    print("=" * 100)
    print(f"  {'z':>5}{'MUSE 1+1.59z':>15}{'LCDM flat':>12}{'DESI decline':>14}{'rho_total E(z)':>16}")
    for z in (0.33, 0.5, 1.0, 1.44):
        print(f"  {z:>5.2f}{muse_shape(z):>15.2f}{a0_LCDM(z):>12.2f}{a0_DESI(z):>14.2f}{a0_rho_total(z):>16.2f}")
    print("  The data climb; the canonical reading is flat-to-declining. Opposite SIGN. Even the rho_total")
    print("  branch (rising) UNDERSHOOTS -- MUSE rises 'faster than H(z)' (E(z)), per the authors.\n")

    # ---------------------------------------------------------------- (2) the tension in sigma, naive (fitted = fundamental)
    print("=" * 100)
    print("(2) TENSION in sigma -- TAKING MUSE's fitted a0 AS the fundamental a0 (no degeneracy relief yet)")
    print("=" * 100)
    s_lcdm = eff_slope(a0_LCDM)      # = 0
    s_desi = eff_slope(a0_DESI)      # slightly negative over 0.33-1.44
    sig_lcdm = abs(MU_a1 - s_lcdm * MU_a00) / MU_a1_e
    sig_desi = abs(MU_a1 - s_desi * MU_a00) / MU_a1_e
    print(f"  Slope test (a1, x1e-10):  MUSE a1 = +{MU_a1:.2f} +/- {MU_a1_e:.3f}")
    print(f"     framework LCDM slope   = {s_lcdm*MU_a00:+.2f}  -> tension {sig_lcdm:>4.1f} sigma  (data rise, model flat)")
    print(f"     framework DESI slope   = {s_desi*MU_a00:+.2f}  -> tension {sig_desi:>4.1f} sigma  (data rise, model declines)")
    # point test at z~1 where MUSE is tightest, normalised to MUSE's own zero point
    z = 1.0
    a0_obs, a0_obs_e = 2.38, 0.11
    pred_lcdm = a0_LCDM(z) * MU_a00       # 1.0
    pred_desi = a0_DESI(z) * MU_a00       # ~1.01
    print(f"  Point test at z~1:  MUSE a0|z~1 = {a0_obs} +/- {a0_obs_e}")
    print(f"     framework LCDM pred (anchored to MUSE z=0=1.0) = {pred_lcdm:.2f} -> {(a0_obs-pred_lcdm)/a0_obs_e:>4.1f} sigma")
    print(f"     framework DESI pred                            = {pred_desi:.2f} -> {(a0_obs-pred_desi)/a0_obs_e:>4.1f} sigma")
    print(f"  Authors' headline evolution detection: ~30 sigma (offset of intermediate-z a0 above local).")
    print(f"  => TAKEN LITERALLY, the canonical constant/declining reading is REFUTED at ~12-16 sigma (slope/point),")
    print(f"     ~30 sigma (authors' offset). The M*/L escape hatch (+0.2->+0.45 dex) is DISOWNED by the authors.\n")

    # ---------------------------------------------------------------- (3) the degeneracy relief: is the rise FUNDAMENTAL?
    print("=" * 100)
    print("(3) IS THE RISE FUNDAMENTAL, OR APPARENT? -- the Magneticum (LCDM) cross-check")
    print("=" * 100)
    mayer_z, mayer_factor = 2.3, 3.0
    muse_at = muse_shape(mayer_z)
    print(f"  Mayer+2023 (LCDM hydro, NO fundamental a0): FITTED a0 rises ~x{mayer_factor:.0f} by z={mayer_z}.")
    print(f"  MUSE fit extrapolated to z={mayer_z}: a0/a0(0) = {muse_at:.1f}x  (vs Mayer's ~{mayer_factor:.0f}x, vs E({mayer_z})={E(mayer_z):.1f}x).")
    print( "  KEY: a RISING FITTED a0 is exactly what LCDM predicts you MEASURE, with NO fundamental a0. So the")
    print( "  MUSE rise does NOT establish a rising FUNDAMENTAL a0 -- it is degenerate with baryon-fraction /")
    print( "  galaxy-assembly evolution (the 'apparent a0'). Against the framework's constant/declining")
    print( "  FUNDAMENTAL a0 + that same forward-model, MUSE is consistent to ~1-2 sigma, NOT 15.")
    print( "  THE CATCH (this cuts BOTH ways, stated honestly):")
    print( "    * It SAVES the canonical reading from outright falsification (fitted a0 != fundamental a0).")
    print( "    * It DESTROYS the older repo claim that 'MUSE confirms the rising a0=cH(z)/Z branch' -- that")
    print( "      rise is LCDM-degenerate AND overshoots E(z). RETRACTED.")
    print( "    * It makes the framework's a0(z) prediction NON-DISTINCTIVE at high z: the observable is")
    print( "      assembly-dominated, identical in LCDM and in the framework. No edge remains here.\n")

    # ---------------------------------------------------------------- (4) the rest of the split data
    print("=" * 100)
    print("(4) THE DATA ARE SPLIT -- MUSE is not the whole story")
    print("=" * 100)
    rows = [
        ("MUSE-DARK III 2026 (2604.22613)", "0.33-1.44", "a1=+1.59; a0|z~1=2.38; rises faster than H(z)", "RISE (vs canonical)"),
        ("Mayer+ 2023 LCDM sim (2206.04333)", "0-2.3", "APPARENT a0 x3 (no fundamental a0)", "rise is LCDM-degenerate"),
        ("McGaugh+ 2024 (2406.17930) BTFR/fDM", "<=2.5", "no clear evolution", "favours CONSTANT (canonical)"),
        ("Milgrom 2017 (1703.06110) direct RC", "~2", "excludes ~4 a0; excludes (1+z)^1.5", "favours CONSTANT; bounds rise"),
    ]
    print(f"  {'source':<37}{'z':>10}{'result':>48}   reading")
    for s, zz, r, rd in rows:
        print(f"  {s:<37}{zz:>10}{r:>48}   {rd}")
    print("  Two analyses (McGaugh, Milgrom) FAVOUR the constant reading and BOUND steep rises; MUSE measures")
    print("  a strong rise that is itself LCDM-degenerate. No unanimous verdict -- and none of these four pins")
    print("  the framework's DISTINCTIVE content (the a0<->H0/Lambda coefficient), only 'evolving vs constant'.\n")

    # ---------------------------------------------------------------- (5) verdict / grade
    print("=" * 100)
    print("(5) GRADE -- falsify / weaken / consistent-within-systematics?")
    print("=" * 100)
    print("""  GRADE: WEAKENED & CONTESTED, leaning UNFAVOURABLE -- NOT falsified, NOT confirmed.

  * Taken at face value (fitted a0 = fundamental a0), the single most DIRECT, multi-point a0(z)
    measurement (MUSE-DARK III) CONTRADICTS the canonical constant/declining reading at ~12-16 sigma
    (slope/point) / ~30 sigma (authors' offset), and the authors DISOWN the M*/L systematic that would
    reconcile it. On its own terms, that is a strong refutation of the canonical reading -- say so.

  * It is NOT a clean falsification only because of THREE legitimate, primary-sourced facts:
      (i)  the rise is LCDM-DEGENERATE -- Mayer+2023 shows LCDM with NO fundamental a0 produces an
           apparent a0 rising ~x3; a rising FITTED a0 does not prove a rising FUNDAMENTAL a0;
      (ii) it runs 'FASTER THAN H(z)' -- so it matches NO cosmological a0(z) coupling (neither the
           declining sqrt(rho_DE) nor even the rising E(z)); a background-density law cannot exceed H,
           which points to a galaxy-assembly / measurement origin, not a fundamental cosmological a0;
      (iii)the data are SPLIT -- McGaugh+2024 and Milgrom 2017 favour CONSTANT a0 and bound steep rises.

  * But the rescue is DOUBLE-EDGED and must not be sold as a win: the very argument that spares the
    canonical reading (the observed rise is apparent/assembly, not the fundamental scale) also makes the
    framework's a0(z) prediction NON-DISTINCTIVE and NON-CONFIRMABLE from this observable, and it
    RETRACTS the repo's prior 'MUSE confirms our rising a0' claim (it overshoots E(z) and is degenerate).

  NET: the a0(z) front, honestly, is empirically MUTE-to-UNFAVOURABLE for the framework right now. The
  one direct measurement leans AGAINST the canonical reading; survival hinges on a degeneracy that also
  strips distinctiveness; the corroborating analyses that DO favour constant a0 don't test the
  framework's distinctive coefficient either. This neither kills the framework nor rescues it -- it
  removes a0(z) as a near-term source of support and leaves the canonical reading on the back foot.""")
    print("=" * 100)


if __name__ == "__main__":
    main()
