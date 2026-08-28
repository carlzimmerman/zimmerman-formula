#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_boosted_quadrupole_lock_refute_2026.py
=========================================
ADVERSARIAL REFUTATION ATTEMPT of the "Q2<->gamma_v lock" via the ONE angle left open by
the STATIC solve typeII_direct_variation_2026.py (its R1, R7 explicitly EXCLUDE the boosted
sector):  can the BOOSTED / CURRENT sector -- the O(w) frame-dragging aether mode driven by
the solar system's velocity w relative to the aether rest frame -- supply an INDEPENDENT
quadrupole at Cassini that DECOUPLES the phantom Cassini quadrupole Q2 from the wide-binary
gamma_v?

WHAT IS ALREADY COMMITTED (this file only PRICES it, it does not re-derive the action solve):
  * The boosted O(w) sector of AeST was solved directly from arXiv:2007.00082 Eq.5 in
      real_research/reviews/alpha2_linearised_solve_2026.py   and
      real_research/reviews/ppn_verify_g0i_channel_2026.py.
    Result:  the current/frame-dragging sector generates the STANDARD PPN preferred-frame
    metric, with
        g_00 = -1 + 2U + alpha_1 w^2 U + alpha_2 w^i w^j U_ij + ...,   U_ij=(d_ij-2 n_i n_j)U
    i.e. the boosted sector's ONLY quadrupole is the alpha_2 term  alpha_2 w^i w^j U_ij,
    a quadrupole aligned with the BOOST w (NOT with the galactic external field g_ext), and
        alpha_1 = -4 K_B  (exact),   alpha_2 = O(K_B)  [coeff 1/2..5/2 across the routes].
    K_B enters LINEARLY.  This IS a genuinely independent quadrupole knob: it is set by
    (K_B, w) and is BLIND to the nu-kernel shape that sets gamma_v.  So structurally the
    decoupling the task hunts for EXISTS.  The question is whether it is ADMISSIBLE at the
    magnitude the lock's tension actually lives at.  This file answers that, both directions.

  * The lock's tension (committed route1B / FC_AEST STATUS): to pass Cassini the EFE phantom
    quadrupole q_direct2D(nu, eta_solar=2.478) must sit under the ceiling q < 0.0441; the
    exponential/RouteA kernels give q ~ 0.166..0.34 (3.8x..7.8x FAIL), the sharp mu_n pass.
    The SAME kernel then fixes gamma_v; sharp mu_n => gamma_v ~ 1.000-1.004, in conflict
    with the registered Gaia-DR4 Amendment-10 band gamma_v in [1.16, 1.23].

REFUTATION LOGIC.  For the boosted quadrupole to BREAK the lock it must do ONE of:
  (A) contribute to the Cassini quadrupole budget at a level comparable to the ceiling
      (so a failing kernel could be rescued by cancellation), OR
  (B) contribute to gamma_v (the internal-binary enhancement) at the 16-23% level
      (so gamma_v could reach the DR4 band without a kernel that fails Cassini).
Either requires an ADMISSIBLE K_B, i.e. one that also respects the measured preferred-frame
bounds |alpha_1| < 1e-4 (LLR) and |alpha_2| < 1e-7 (solar spin axis).

Exit 0 iff every numbered check passes; the VERDICT is printed regardless.
"""
import sys
import math

FAIL, NCHK = [], [0]
def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok  ' if ok else 'FAIL'}] {label}" + (f"\n         {detail}" if detail else ""))
    if not ok: FAIL.append(label)
    return ok
def info(label, detail=""):
    print(f"  [info] {label}" + (f"\n         {detail}" if detail else ""))

print(__doc__)

# ---------------------------------------------------------------------------------------------
# constants
# ---------------------------------------------------------------------------------------------
C     = 2.99792458e8
G     = 6.67430e-11
GMSUN = 1.32712440018e20
AU    = 1.495978707e11
A0    = 9.3619e-11            # canonical footing (result is footing-insensitive; alt carried)
A0ALT = 1.1279e-10

# committed Cassini gate numbers (route1B / FC_AEST STATUS)
ETA_SOLAR = 2.478            # g_ext/a0 at the Sun
Q_CEIL    = 0.0441           # Cassini ceiling on the phantom quadrupole q_direct2D
Q_EFE_EXP = 0.166            # exponential/observable mu=1-e^-y phantom quadrupole (3.76x fail @ this norm)

# boosted-sector dictionary (committed): alpha_i = coeff * K_B, both route readings carried
ALPHA2_COEFF = (("g0i/g00 route (5/2)K_B", 2.5),
                ("frozen-lambda route (1/2)K_B", 0.5))
# measured PPN preferred-frame bounds
A1_BOUND = 1e-4              # |alpha_1| < 1e-4  (lunar laser ranging)
A2_BOUND = 1e-7             # |alpha_2| < 1e-7  (solar spin-axis alignment, Nordtvedt)

# solar-system boost relative to the preferred (cosmic aether) frame -- carry CMB and galactic
W_CASES = (("CMB dipole 370 km/s", 370e3), ("galactic rotation 220 km/s", 220e3))

# Cassini is measured near Saturn
R_SAT = 9.58 * AU
gN_sat = GMSUN / R_SAT**2

print("="*100)
print("S1.  MAGNITUDE OF THE BOOSTED (alpha_2) QUADRUPOLE AT SATURN, IN THE SAME q-UNITS AS THE EFE")
print("="*100)
info("The EFE phantom quadrupole is an O(a0) anomalous acceleration: a_EFE_quad ~ q_EFE * a0.",
     f"a0={A0:.3e}, ceiling accel = q_ceil*a0 = {Q_CEIL*A0:.3e} m/s^2 at Saturn.")
info("The boosted quadrupole is a FRACTION alpha_2*(w/c)^2 of the NEWTONIAN accel at Saturn:",
     f"g_N(Saturn={R_SAT/AU:.2f} AU) = {gN_sat:.3e} m/s^2.")
# convert boosted quadrupole into the EFE q-normalisation: q_boost = a_boost_quad / a0
worst_frac_of_ceiling = 0.0
for wname, w in W_CASES:
    wc2 = (w/C)**2
    a_boost = A2_BOUND * wc2 * gN_sat          # at the alpha_2 measurement bound
    q_boost = a_boost / A0                       # same normalisation as q_direct2D (per a0)
    frac = q_boost / Q_CEIL
    worst_frac_of_ceiling = max(worst_frac_of_ceiling, frac)
    info(f"{wname}: (w/c)^2={wc2:.3e}; at |alpha_2|<{A2_BOUND:.0e} bound: "
         f"a_boost_quad={a_boost:.3e} m/s^2, q_boost={q_boost:.3e}, "
         f"= {frac:.3e} x the Cassini ceiling")
check(worst_frac_of_ceiling < 1e-3,
      "S1  at the MEASURED alpha_2 bound the boosted quadrupole is < 1e-3 of the Cassini "
      "ceiling on EVERY boost choice -- it cannot cancel an EFE quadrupole that sits at "
      "3.8x-7.8x the ceiling, and it is ADDITIVE (wrong sign to help unless tuned), and it "
      "is aligned with w not g_ext so it cannot cancel a differently-oriented quadrupole",
      f"worst = {worst_frac_of_ceiling:.2e} of ceiling")

print()
print("="*100)
print("S2.  TURN IT AROUND: what alpha_2 (hence K_B) would the boosted quadrupole NEED to matter?")
print("="*100)
for wname, w in W_CASES:
    wc2 = (w/C)**2
    a2_need = Q_CEIL * A0 / (wc2 * gN_sat)       # alpha_2 to reach the ceiling
    over_bound = a2_need / A2_BOUND
    info(f"{wname}: alpha_2 needed to reach the Cassini ceiling = {a2_need:.3e} "
         f"= {over_bound:.2e} x the measured |alpha_2|<{A2_BOUND:.0e} bound")
    for cname, coeff in ALPHA2_COEFF:
        kb_need = a2_need / coeff
        # alpha_2 bound on K_B:
        kb_ceil_a2 = A2_BOUND / coeff
        info(f"     [{cname}] K_B needed = {kb_need:.3e}; but |alpha_2| bound caps "
             f"K_B < {kb_ceil_a2:.2e}  -> over by {kb_need/kb_ceil_a2:.2e}")
check(all((Q_CEIL*A0/((w/C)**2*gN_sat))/A2_BOUND > 1e4 for _, w in W_CASES),
      "S2  reaching the Cassini ceiling needs alpha_2 >~ 1e4-1e5 x its measured bound -- "
      "i.e. a K_B that is FOUR-TO-FIVE orders above what solar-system preferred-frame tests "
      "already allow.  No admissible K_B puts the boosted quadrupole anywhere near Cassini")

print()
print("="*100)
print("S3.  THE OTHER ESCAPE (B): can the boosted sector supply gamma_v = 1.16-1.23 instead?")
print("="*100)
GV_LO, GV_HI = 1.16, 1.23
need = GV_LO - 1.0                                # required fractional internal enhancement
info("gamma_v is a 16-23% enhancement of the internal binary acceleration. The boosted "
     "sector enhances internal dynamics only through preferred-frame terms, at fractional "
     f"level ~ |alpha_1|(w/c) (vector) or |alpha_2|(w/c)^2 (quadrupole).")
worst_gv = 0.0
for wname, w in W_CASES:
    wc = w/C
    boost_vec  = A1_BOUND * wc                    # alpha_1 (w/c)
    boost_quad = A2_BOUND * wc**2                 # alpha_2 (w/c)^2
    biggest = max(boost_vec, boost_quad)
    worst_gv = max(worst_gv, biggest)
    info(f"{wname}: alpha_1(w/c) = {boost_vec:.3e}, alpha_2(w/c)^2 = {boost_quad:.3e}; "
         f"need {need:.2f} -> shortfall {need/biggest:.2e} x")
check(worst_gv < need/1e4,
      "S3  the boosted sector can move gamma_v by at most ~1e-7 at the measured alpha bounds "
      "-- SIX orders below the 0.16-0.23 the DR4 band requires. It cannot supply gamma_v, so "
      "gamma_v STILL forces the nu-kernel, which STILL sets Q2. The two observables remain "
      "welded through the kernel",
      f"largest boosted enhancement = {worst_gv:.2e} vs required {need:.2f}")

print()
print("="*100)
print("S4.  IS THE INDEPENDENT KNOB EVEN OPEN? THE alpha-BOUNDS vs THE STABILITY FLOOR ON K_B")
print("="*100)
# committed: subluminality/stability floor K_B >~ 2.1e-4 (K_2=9.5e3); alpha_1 ceiling K_B<2.5e-5
KB_FLOOR = 2.105e-4          # subluminality floor (committed, K_2 = 9.5e3)
KB_CEIL_A1 = A1_BOUND/4.0    # |alpha_1|=4 K_B  ->  K_B < 2.5e-5
info(f"subluminality/stability floor (committed): K_B >~ {KB_FLOOR:.3e}")
info(f"alpha_1 ceiling: |alpha_1|=4 K_B < 1e-4  =>  K_B < {KB_CEIL_A1:.3e}")
info(f"alpha_2 ceiling (coeff 5/2): K_B < {A2_BOUND/2.5:.3e}  (tighter still)")
check(KB_FLOOR > KB_CEIL_A1,
      "S4  the two-sided K_B window is EMPTY: the boosted sector's own preferred-frame bounds "
      "(K_B<2.5e-5) sit BELOW the stability floor (K_B>2.1e-4). So the vector/current sector "
      "is not a free rescue knob at all -- pushing K_B up to make the boosted quadrupole "
      "matter is exactly what the alpha bounds forbid, and pushing it down to satisfy them "
      "leaves the quadrupole ~1e-5 of anything. This is an INHERITED AeST liability, not a "
      "new door out of the lock",
      f"floor {KB_FLOOR:.2e} > ceiling {KB_CEIL_A1:.2e}")

print()
print("="*100)
print("VERDICT")
print("="*100)
print("""  The boosted/current sector DOES contain a structurally-independent quadrupole -- the
  PPN alpha_2 term alpha_2 w^i w^j U_ij, aligned with the boost w, set by K_B alone and
  BLIND to the nu-kernel that fixes gamma_v. So the *structural* decoupling the task asks
  about is real, and it was worth checking honestly.

  But it does NOT break the Q2<->gamma_v lock, for three independent reasons, each a measured
  number and not a budget proxy:
    * (S1/S2) at the measured |alpha_2|<1e-7 bound the boosted quadrupole is ~1e-6 of the
      Cassini ceiling; reaching the ceiling needs alpha_2 ~ 1e4-1e5x its bound. And it is
      aligned with w, not g_ext, so it cannot cancel the EFE quadrupole even in principle.
    * (S3) it moves gamma_v by <~1e-7, six orders short of the 0.16-0.23 the DR4 band needs;
      gamma_v therefore still forces the kernel, which still sets Q2.
    * (S4) the K_B window that would be needed is empty anyway -- the alpha bounds cap K_B
      four orders below the stability floor.
  DECOUPLING FOUND (structural): yes.  DECOUPLING THAT BREAKS THE LOCK (admissible): no.
  VERDICT: lock-holds.""")

print()
print("="*100)
print(f"checks: {NCHK[0]-len(FAIL)}/{NCHK[0]} passed")
if FAIL:
    print("FAILED:", *FAIL, sep="\n   - ")
    sys.exit(1)
print("ALL CHECKS PASSED")
sys.exit(0)
