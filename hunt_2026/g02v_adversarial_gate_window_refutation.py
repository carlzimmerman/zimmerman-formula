#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""g02v_adversarial_gate_window_refutation.py
=================================================================================================
ADVERSARIAL VERIFICATION of the g02 claim:

  "The framework's OWN frequency gate G(w) = 1/(1 + i w/omega_c) cannot produce a measurable
   vertical/planar split ANYWHERE in its theory-allowed omega_c window.  Scanning omega_c over
   2e-15 to 1e-11 rad/s (the ~4-decade window whose lower edge is the galactic-survival bound),
   the largest departure of S from unity is 4.54% (at the window's bottom edge)."

WHAT IS TESTED HERE, and it is only the WINDOW and the GATE ARITHMETIC.  Every geometric input
(Omega, q = nu_z/Omega, |g_N| at the two evaluation points, sigma(S)) is taken VERBATIM from
g02's own committed stdout, so nothing below can be blamed on a different mass model.  The
question is narrow: is the omega_c interval g02 scans the one the framework actually allows, and
is 4.54% the number that interval produces?

THE SOURCE OF TRUTH is the script g02 itself cites, real_research/reviews/mi_omegac_anchor_2026.py,
whose S3 prints:
      Omega_gal,max = 6.482e-15 rad/s   (inner disk star, 100 km/s at 0.5 kpc)
      LOWER BOUND, galaxies must survive:  Re G >= 1/2 there  ->  omega_c >= 6.482e-15
      THEORY-ALLOWED WINDOW: 6.482e-15 < omega_c < 6.296e-12 rad/s -- a span of 3.0 orders
      COMMITTED WINDOW:      [1.782e-14, 2.211e-14]
and whose S2 table reports the gate's attenuation as  Re G = 1/(1 + (w/omega_c)^2),  NOT the
modulus |G| = 1/sqrt(1 + (w/omega_c)^2) that g02 uses.  The committed lower edge is defined in
mi_kernel_axis_separation_omegac_2026.py:66 as "3 x OMEGA_GAL, from Re G >= 0.90" -- i.e. by Re G.

FOUR CHARGES, each a numbered check that can fail:
  A1  g02's lower edge 2.0e-15 lies BELOW the framework's own galactic-survival bound.
  A2  the stated window is ~4 decades; the framework's is 3.0, and its COMMITTED one is x1.24.
  A3  three evaluations are not a scan: |S-1| is NON-MONOTONIC in omega_c.
  A4  the gate function used (|G|) is not the one the anchor uses (Re G), and the choice matters.
  A5  THE VERDICT ON THE CONCLUSION, computed under the CORRECTED window and the WORST-CASE
      convention: does the no-go survive being fixed?  (Charges A1-A4 are against the claim's
      numbers; A5 asks whether they are against its conclusion, and it is written so that it
      FAILS if the corrected split ever becomes measurable.)

BOTH a0 FOOTINGS on every gate evaluation.  MUTATION CONTROL at the end.
"""
from __future__ import annotations
import math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import A0, Check, P, info, nu  # noqa: E402

C = Check()
def banner(t): P("\n" + "=" * 100); P("  " + t); P("=" * 100)

# ---- inputs lifted VERBATIM from g02's committed stdout (lines 129-135, 165) ---------------------
OM      = 9.0748e-16      # Omega = V_c/R0 at the Sun
Q_ZMAX  = 1.801           # nu_z/Omega for z_max = 1.1 kpc     <- the ONLY q g02 feeds the gate
Q_MID   = 3.135           # nu_z/Omega in the midplane limit    <- computed by g02, then unused
GN_RAD  = 1.2302e-10      # |g_N|(R0, 0)
GN_VER  = 1.2349e-10      # |g_N|(R0, 1.1 kpc)
S_ERR   = 0.1208          # sigma(S) from g02's V6 Monte Carlo
S_OBS   = 0.6417

# ---- the framework's own numbers, from mi_omegac_anchor_2026.py S3 -------------------------------
OM_GAL_MAX   = 6.482e-15  # inner-disk star; Re G >= 1/2 there IS the galactic-survival bound
ANCHOR_LO    = 6.482e-15  # theory-allowed lower edge
ANCHOR_HI    = 6.296e-12  # theory-allowed upper edge at a 1e-9 monopole tolerance
COMMIT_LO    = 1.782e-14  # committed window, both footings
COMMIT_HI_C  = 2.211e-14  # canonical
COMMIT_HI_A  = 1.831e-14  # alt
G02_LO, G02_HI = 2.0e-15, 1.0e-11   # what g02 line 612 actually scans


def S_gate(oc, q, a0, mode="abs"):
    """S = nu_vert/nu_rad under the one-pole gate.  mode 'abs' = |G| (g02); 're' = Re G (anchor)."""
    nr, nv = float(nu(GN_RAD / a0)), float(nu(GN_VER / a0))
    xr, xv = OM / oc, q * OM / oc
    if mode == "abs":
        Gr, Gv = 1 / math.sqrt(1 + xr**2), 1 / math.sqrt(1 + xv**2)
    else:
        Gr, Gv = 1 / (1 + xr**2), 1 / (1 + xv**2)
    return (1 + Gv * (nv - 1)) / (1 + Gr * (nr - 1))


banner("A0  REGRESSION -- reproduce g02's own three gate points before attacking them")
for tag, oc in (("lo", G02_LO), ("committed", 1.782e-14), ("hi", G02_HI)):
    P(f"      omega_c = {oc:.3e} ({tag:<9}):  S = {S_gate(oc, Q_ZMAX, A0['canonical']):.4f}  "
      f"|S-1| = {abs(S_gate(oc, Q_ZMAX, A0['canonical']) - 1):.2%}")
rep_lo = abs(S_gate(G02_LO, Q_ZMAX, A0["canonical"]) - 1)
rep_co = abs(S_gate(1.782e-14, Q_ZMAX, A0["canonical"]) - 1)
C("A0 this file reproduces g02's published gate numbers (4.54% at its 'lo', 0.19% at the committed "
  "value), so everything below attacks the same arithmetic and not a different one",
  abs(rep_lo - 0.0454) < 5e-4 and abs(rep_co - 0.0019) < 5e-4,
  f"got {rep_lo:.2%} and {rep_co:.2%} against g02's 4.54% and 0.19%")

banner("A1  IS 2.0e-15 THE GALACTIC-SURVIVAL BOUND?  (the claim says it is)")
reG_at_g02lo = 1 / (1 + (OM_GAL_MAX / G02_LO) ** 2)
P(f"""
  mi_omegac_anchor_2026.py S3 defines the bound: the largest galactic orbital frequency in its own
  table is Omega_gal,max = {OM_GAL_MAX:.3e} rad/s, and galaxies survive only while Re G >= 1/2 there,
  i.e. omega_c >= {ANCHOR_LO:.3e} rad/s.

  g02 scans down to {G02_LO:.3e}, which is {ANCHOR_LO/G02_LO:.2f}x BELOW that bound.  At that omega_c the
  framework's own gate leaves the inner-disk star  Re G = {reG_at_g02lo:.3f}  -- galaxies keep
  {reG_at_g02lo:.0%} of their MOND boost, i.e. the RAR is destroyed.  So the headline 4.54% is
  evaluated at an omega_c the framework has already excluded.""")
C("A1 the claim's 'window bottom edge' is NOT the galactic-survival bound -- it sits a factor 3+ "
  "below it, at an omega_c where the framework's own gate switches galaxies off",
  G02_LO >= ANCHOR_LO, f"g02 lo = {G02_LO:.3e} against the anchor's {ANCHOR_LO:.3e} "
  f"({ANCHOR_LO/G02_LO:.2f}x); Re G at Omega_gal,max would be {reG_at_g02lo:.3f} -- FAILING THIS IS "
  f"THE REFUTATION OF THE CLAIM'S STATED WINDOW")

banner("A2  IS THE WINDOW ~4 DECADES?")
P(f"      claim / g02       : {G02_LO:.3e} - {G02_HI:.3e}   = {math.log10(G02_HI/G02_LO):.2f} decades")
P(f"      anchor, allowed   : {ANCHOR_LO:.3e} - {ANCHOR_HI:.3e}   = {math.log10(ANCHOR_HI/ANCHOR_LO):.2f} decades")
P(f"      anchor, COMMITTED : {COMMIT_LO:.3e} - {COMMIT_HI_C:.3e}   = a factor "
  f"{COMMIT_HI_C/COMMIT_LO:.2f} (canonical), {COMMIT_HI_A/COMMIT_LO:.2f} (alt)")
C("A2 the theory-allowed window is the anchor's 3.0 decades, not the claim's ~4, and the COMMITTED "
  "window is a factor 1.24 wide -- so 'the parameter's whole allowed window' is misdescribed by "
  "the claim", abs(math.log10(G02_HI/G02_LO) - math.log10(ANCHOR_HI/ANCHOR_LO)) < 0.3,
  f"claim {math.log10(G02_HI/G02_LO):.2f} dex vs anchor {math.log10(ANCHOR_HI/ANCHOR_LO):.2f} dex; "
  f"committed span x{COMMIT_HI_C/COMMIT_LO:.2f} -- FAILING THIS RECORDS THE MISDESCRIPTION")

banner("A3  THREE POINTS ARE NOT A SCAN -- |S-1| is non-monotonic in omega_c")
ocs = np.logspace(-17, -10, 6001)
dev = np.array([abs(S_gate(o, Q_ZMAX, A0["canonical"]) - 1) for o in ocs])
peak_oc, peak = float(ocs[dev.argmax()]), float(dev.max())
m_g02 = (ocs >= G02_LO) & (ocs <= G02_HI)
P(f"""
  |S-1| -> 0 as omega_c -> 0 (gate shuts on BOTH trajectories) and -> {abs(S_gate(1e-8, Q_ZMAX, A0['canonical'])-1):.2%} as
  omega_c -> inf (gate open on both).  It therefore PEAKS in between: the true maximum over all
  omega_c is {peak:.2%} at omega_c = {peak_oc:.3e} rad/s -- which lies BELOW g02's own 'lo', so the
  three sampled points cannot establish 'the largest departure' even inside the stated interval.
  (Inside g02's interval the max is {dev[m_g02].max():.2%}, at its bottom edge -- true, but shown
  here by a 6001-point grid, not by the three evaluations OMC = dict(lo, committed, hi).)""")
C("A3 the claim's 'exhaustive scan over the parameter's whole allowed window' is three function "
  "evaluations of a NON-MONOTONIC function whose global maximum lies outside them",
  peak_oc >= G02_LO, f"global peak {peak:.2%} at {peak_oc:.3e}, below g02's lo {G02_LO:.3e} -- "
  f"FAILING THIS RECORDS THAT 3 POINTS DID NOT ESTABLISH THE MAXIMUM")

banner("A4  THE GATE FUNCTION -- g02 uses |G|, the anchor uses Re G")
P("""      mi_omegac_anchor_2026.py S2 tabulates 'Re G (omc lo)', and the committed lower edge is
      defined in mi_kernel_axis_separation_omegac_2026.py:66 as "3 x OMEGA_GAL, from Re G >= 0.90".
      g02 line 628-630 uses |G| = 1/sqrt(1+(w/omc)^2) instead.  Re G falls faster, so it SPLITS the
      two trajectories harder -- the substitution runs AGAINST the claim, not for it.""")
P(f"\n      {'omega_c':>14}{'|G|, q=1.801':>15}{'ReG, q=1.801':>15}{'|G|, q=3.135':>15}{'ReG, q=3.135':>15}")
for oc in (ANCHOR_LO, COMMIT_LO, COMMIT_HI_C, ANCHOR_HI):
    P(f"      {oc:14.3e}" + "".join(f"{abs(S_gate(oc, q, A0['canonical'], md)-1):15.3%}"
                                    for q, md in ((Q_ZMAX,"abs"),(Q_ZMAX,"re"),(Q_MID,"abs"),(Q_MID,"re"))))
ratio = abs(S_gate(ANCHOR_LO, Q_ZMAX, A0["canonical"], "re") - 1) / \
        abs(S_gate(ANCHOR_LO, Q_ZMAX, A0["canonical"], "abs") - 1)
C("A4 the two gate conventions are NOT interchangeable at the percent level the claim trades in -- "
  "Re G roughly doubles the split at fixed omega_c, and Re G is the one the cited anchor uses",
  abs(ratio - 1) < 0.10, f"Re G / |G| split ratio = {ratio:.2f} at the survival edge -- FAILING THIS "
  f"RECORDS THAT THE FORM CHOICE IS LOAD-BEARING FOR THE HEADLINE NUMBER")
P(f"      (q = {Q_MID} is g02's own midplane value, printed at its V5b and then never fed to the "
  f"gate; it raises the split a further factor ~2.7.)")

banner("A5  DOES THE CONCLUSION SURVIVE THE CORRECTION?  worst case over EVERY defensible choice")
P("      both footings x {|G|, Re G} x {q=1.801, q=3.135}, evaluated on the CORRECTED windows:")
def worst(lo, hi):
    grid = np.logspace(math.log10(lo), math.log10(hi), 2001)
    return max(abs(S_gate(o, q, a0, md) - 1) for o in grid for q in (Q_ZMAX, Q_MID)
               for a0 in A0.values() for md in ("abs", "re"))
w_allowed = worst(ANCHOR_LO, ANCHOR_HI)
w_commit  = max(worst(COMMIT_LO, COMMIT_HI_C), worst(COMMIT_LO, COMMIT_HI_A))
P(f"\n      claim's headline, at its excluded omega_c   : 4.54%  = {0.0454/S_ERR:.2f} sigma")
P(f"      worst over the ALLOWED window (anchor S3)   : {w_allowed:.2%}  = {w_allowed/S_ERR:.2f} sigma")
P(f"      worst over the COMMITTED window             : {w_commit:.2%}  = {w_commit/S_ERR:.2f} sigma")
C("A5a THE NO-GO CONCLUSION SURVIVES, AND STRENGTHENS: with the window corrected, the gate's largest "
  "possible split over every defensible convention stays far below sigma(S) -- so the claim's "
  "CONCLUSION is not refuted, only its numbers", w_allowed < 0.5 * S_ERR,
  f"{w_allowed:.2%} worst allowed vs sigma(S) = {S_ERR:.2%}")
C("A5b and the claim's own headline number is wrong for the window it names: inside the COMMITTED "
  "window the gate reaches at most {:.2%}, not 4.54%".format(w_commit), abs(w_commit - 0.0454) < 0.005,
  f"committed-window worst {w_commit:.2%} against the claimed 4.54% -- a factor "
  f"{0.0454/w_commit:.1f} overstatement; FAILING THIS IS THE CORRECTION")
C("A5c the gate cannot rescue the common offset either: even the worst allowed split moves the MI "
  "prediction by less than half a sigma toward S_obs, so it is not hiding a fit improvement",
  w_allowed / S_ERR < 1.0, f"largest move {w_allowed/S_ERR:.2f} sigma against a {abs(S_OBS-0.9990)/S_ERR:.2f} "
  f"sigma offset")

banner("MUTATION CONTROLS")
# M1 with q -> 1 the gate factors become IDENTICAL, so S collapses onto the ungated algebraic
# ratio nu(g_v)/nu(g_r) interpolated toward 1 -- NOT onto 1.  That residual is the algebraic arm's
# own 0.10% split, which the gate can only attenuate; the correct null is therefore "S lies between
# nu_v/nu_r and 1", i.e. the gate contributes NOTHING of its own.  (Same point as g02's own M3.)
worstdev = 0.0
for a0 in A0.values():
    alg = float(nu(GN_VER / a0)) / float(nu(GN_RAD / a0))
    for md in ("abs", "re"):
        for o in np.logspace(-17, -10, 401):
            s1 = S_gate(o, 1.0, a0, md)
            worstdev = max(worstdev, max(0.0, s1 - 1.0, alg - s1))   # excursion OUTSIDE [alg, 1]
m1 = worstdev
P(f"      M1 q -> 1 (the two trajectories made identical): worst excursion of S outside the ungated "
  f"band [nu_v/nu_r, 1] over ALL omega_c = {m1:.2e}")
C("M1 with the frequency difference deleted the gate contributes NO split of its own at any omega_c "
  "-- S never leaves the band between the ungated algebraic ratio and 1 -- so every number above is "
  "the frequency dependence and not the machinery", m1 < 1e-9, f"worst excursion {m1:.2e}")
m2 = max(abs(S_gate(o, q, 1e-18, md) - 1) for o in np.logspace(-17, -10, 401)
         for q in (Q_ZMAX, Q_MID) for md in ("abs", "re"))
P(f"      M2 Newtonian limit (a0 = 1e-18, nu -> 1): worst |S-1| over ALL omega_c = {m2:.2e}")
C("M2 with the kernel switched off the gate has nothing to attenuate and S = 1 identically",
  m2 < 1e-6, f"worst {m2:.2e}")

banner("VERDICT")
P(f"""
  THE CLAIM'S CONCLUSION STANDS.  THE CLAIM'S NUMBERS AND WINDOW DO NOT.

  * '2e-15 to 1e-11, the ~4-decade window whose lower edge is the galactic-survival bound' is wrong
    on all three counts.  The script it cites, mi_omegac_anchor_2026.py, puts the galactic-survival
    bound at {ANCHOR_LO:.3e} ({ANCHOR_LO/G02_LO:.2f}x higher), the allowed window at 3.0 decades, and the
    COMMITTED window at [{COMMIT_LO:.3e}, {COMMIT_HI_C:.3e}] -- a factor {COMMIT_HI_C/COMMIT_LO:.2f}, not 4 decades.
  * '4.54% at the window's bottom edge' is therefore evaluated at an omega_c where the framework's
    own gate leaves galaxies Re G = {reG_at_g02lo:.3f}.  Inside the committed window the honest worst case
    over both footings, both gate conventions and both frequency ratios is {w_commit:.2%}.
  * The correction runs IN THE CLAIM'S FAVOUR.  {w_allowed:.2%} is the largest split the gate can produce
    anywhere the theory permits, i.e. {w_allowed/S_ERR:.2f} sigma of a measurement whose error is {S_ERR/S_OBS:.0%}.
    The one-pole gate is even more thoroughly unable to split vertical from planar than g02 says.
  * Fix to apply at g02 line 612:  OMC = dict(lo=6.482e-15, committed=1.782e-14, hi=6.296e-12),
    and either switch to Re G or state explicitly that |G| is the amplitude convention chosen.""")
P("")
sys.exit(C.done())
