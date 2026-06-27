#!/usr/bin/env python3
"""
FRESH ARENA the four-script sweep did NOT point at:
  the SECULAR ABERRATION DRIFT = Gaia/VLBI direct measurement of the Solar System
  barycenter's GALACTOCENTRIC acceleration, magnitude a_sun ~ 2.3e-10 m/s^2.

WHY this is a candidate the GW/BH/PTA/lab scripts MISSED:
  - It is NOT the s^TX preferred-frame dipole (that is a Lorentz-violation COEFFICIENT,
    boost-suppressed by beta_cmb, set at high-a bodies). This is the *magnitude of a real
    acceleration*, measured KINEMATICALLY (proper-motion pattern of quasars), and it sits
    at a_sun/a0 ~ 2.5 -- i.e. INSIDE the MOND transition regime, NOT deep-Newtonian.
  - The four banked scripts cover GW-prop, BH/ringdown, PTA, ground-lab. None tests the
    Sun's own a~a0 galactocentric acceleration as measured by astrometric aberration.

THE TWO-WAY QUESTION:
  Does the framework (modified INERTIA, dS-Unruh interp g_obs=sqrt(g_bar^2+g_bar*a0))
  predict a DISTINCTIVE, ABOVE-FLOOR, NEAR-TERM deviation in this measured acceleration?
  Both ways: if it is degenerate with the (unknown) baryonic potential, or below the
  Gaia floor, or MOND-shared -> say so plainly.

Footing: a0 = 9.36e-11 m/s^2 (canonical pure-Lambda cH_Lambda/Z). c_T=1, CPT-even, apex=CMB.
All numbers below are computed here; sources cited inline. exit 0.
"""
import numpy as np

a0 = 9.36e-11        # m/s^2  canonical, INPUT (quarantine held)

# ---------------------------------------------------------------------------
# MEASURED quantity (Gaia EDR3, Klioner et al. 2021 A&A 649 A9, arXiv:2012.02036)
# ---------------------------------------------------------------------------
a_meas   = 2.32e-10  # m/s^2  magnitude of SS-barycenter acceleration
a_err    = 0.16e-10  # m/s^2  1-sigma (~6.9%)
# direction alpha=269.1 dec=-31.6 -> points to GALACTIC CENTER (centripetal), NOT CMB apex.
# proper-motion amplitude 5.05 +- 0.35 uas/yr.
# Gaia DR4 (full mission, ~2026) forecast ~2-3x tighter; DR5 ~5x -> floor ~3e-12..6e-12 m/s^2.
a_err_DR4 = a_err/2.5   # optimistic DR4 (longer baseline; error ~ T^-1.5)
a_err_DR5 = a_err/5.0

print("="*78)
print("FRESH ARENA: secular aberration drift = direct kinematic measure of a_sun")
print("="*78)
print(f"  Gaia EDR3 measured |a_sun| = {a_meas:.3e} +/- {a_err:.2e} m/s^2  ({a_err/a_meas*100:.1f}%)")
print(f"  a_sun / a0                 = {a_meas/a0:.3f}   <-- INSIDE the MOND transition (~2.5 a0)")
print(f"  (direction = Galactic center, centripetal; NOT the CMB apex -> distinct from s^TX)")
print()

# ---------------------------------------------------------------------------
# THE PHYSICS: what does each theory PREDICT for this measured number?
#
# CRUCIAL POINT (the both-ways crux): aberration measures the *true kinematic*
# acceleration of the barycenter directly (d(line-of-sight)/dt of distant quasars).
# It is a GEOMETRIC/KINEMATIC observable -- it does NOT assume any force law.
# So ALL theories (GR+DM, MOND, framework) predict the SAME measured a_sun = the
# actual centripetal acceleration v_c^2/R_0 of the Sun on its galactic orbit.
#
# The measured a_sun is therefore NOT, by itself, a discriminator: every theory that
# reproduces the rotation curve (v_c ~ 233 km/s at R0 ~ 8.2 kpc) predicts the SAME
# kinematic a_sun. The aberration value 2.3e-10 is in fact ~v_c^2/R0:
# ---------------------------------------------------------------------------
v_c = 233e3          # m/s  local circular speed (Gaia/Sgr A* proper motion)
R0  = 8.178 * 3.086e19  # m   (8.178 kpc, GRAVITY 2019)
a_kin = v_c**2 / R0
print(f"  cross-check: v_c^2/R0 = {a_kin:.3e} m/s^2 (v_c=233 km/s, R0=8.178 kpc)")
print(f"     -> matches measured {a_meas:.2e} to {abs(a_kin-a_meas)/a_meas*100:.0f}% (it IS the centripetal accel)")
print()

# ---------------------------------------------------------------------------
# So the discriminating question must be sharper. The framework (modified inertia)
# vs GR+DM vs MOND all agree on the KINEMATIC a_sun. The ONLY way aberration becomes
# a test is the SECOND-ORDER / DIRECTIONAL content:
#
# (1) MISSING-MASS reading: compare measured a_sun to the BARYONIC Newtonian
#     prediction a_bar (from counted stars+gas in the inner Galaxy). If a_meas >> a_bar,
#     that excess is the usual "dark matter / MOND boost." Framework predicts a boost
#     g_obs = sqrt(g_bar^2 + g_bar a0). BUT a_bar at R0 is NOT independently known to
#     better than tens of percent (baryonic M/L, bulge, gas), so this is M/L-DEGENERATE,
#     exactly like the RAR -- non-diagnostic of a0=9.36e-11. (Same wall as SPARC.)
#
# (2) The framework-DISTINCTIVE piece: modified INERTIA referred to u^mu (CMB) predicts
#     the a~a0 CMB-APEX DIPOLE in the inertial response. Could aberration see a dipole
#     anisotropy in a_sun? -> the aberration measures ONE vector (the Sun's accel), it
#     has no dipole-over-sky handle on the *response*; the apex-dipole lives in an
#     ENSEMBLE of low-a systems (the banked weak-lensing RAR dipole), not in the single
#     solar acceleration vector. So aberration does NOT probe the apex dipole.
# ---------------------------------------------------------------------------

# (1) quantify the missing-mass / boost reading and its degeneracy
# deep-MOND/transition boost factor at x=a_meas/a0 (framework's OWN interp, INVERTED:
# given OBSERVED g_obs, the implied g_bar is g_bar = g_obs^2/(g_obs+a0)... but we want:
# given baryonic g_bar, predicted g_obs). Take a representative baryonic guess.
x = a_meas/a0
# framework nu (simple form consistent w/ g_obs=sqrt(g_bar^2+g_bar a0)):
# solve g_obs given g_bar: g_obs = 0.5*(g_bar + sqrt(g_bar^2+4 g_bar a0))? No --
# the framework interp is g_obs = sqrt(g_bar^2 + g_bar a0). Invert for g_bar from g_obs=a_meas:
g_obs = a_meas
g_bar_implied = ( -a0 + np.sqrt(a0**2 + 4*g_obs**2) ) / 2.0
boost = g_obs/g_bar_implied
print("-"*78)
print("(1) MISSING-MASS / boost reading (framework interp g_obs=sqrt(g_bar^2+g_bar a0)):")
print(f"    implied baryonic g_bar = {g_bar_implied:.3e} m/s^2  -> boost g_obs/g_bar = {boost:.3f}")
print(f"    i.e. framework attributes ~{(1-1/boost)*100:.0f}% of a_sun to the inertial boost.")
print(f"    BUT a_bar at R0 (counted baryons) is uncertain at the tens-of-% level (M/L, bulge,")
print(f"    gas) -> this is M/L-DEGENERATE, the SAME wall as the SPARC RAR. NON-DIAGNOSTIC of a0.")
print()
print("    Both-ways: a {:.0f}% boost is 'predicted', but it is INDISTINGUISHABLE from".format((1-1/boost)*100))
print("    GR+DM (just call the excess 'the local DM density') AND from standard MOND (same nu).")
print("    -> MOND-SHARED + baryon-degenerate. NOT distinctive.")
print()

# floor check: even IF a_bar were known perfectly, is the boost above the Gaia floor?
# framework boost vs pure-Newton (no DM) would be a {boost:.2f}x effect = HUGE (factor ~1.4),
# trivially above floor -- BUT that is the generic missing-mass statement, shared by DM & MOND.
# The DISTINCTIVE framework-vs-MOND difference at x=2.5 (its own nu vs Milgrom's) is tiny:
nu_fw = g_obs/g_bar_implied
# standard simple-mu MOND at same g_bar:
gb = g_bar_implied
g_mond_simple = 0.5*gb + np.sqrt(0.25*gb**2 + gb*a0)   # simple interpolating nu
diff_fw_mond = abs(g_obs - g_mond_simple)/g_obs
print(f"    framework vs standard-MOND(simple) at same g_bar: fractional diff = {diff_fw_mond*100:.2f}%")
print(f"    Gaia EDR3 precision on a_sun = {a_err/a_meas*100:.1f}%; DR4 ~{a_err_DR4/a_meas*100:.1f}%; DR5 ~{a_err_DR5/a_meas*100:.1f}%")
if diff_fw_mond < a_err_DR5/a_meas:
    print(f"    -> framework-vs-MOND gap ({diff_fw_mond*100:.2f}%) is BELOW even the DR5 floor")
    print(f"       AND swamped by the a_bar baryon uncertainty -> NOT a discriminator.")
print()

# (2) apex-dipole: not accessible (single vector), formally
print("-"*78)
print("(2) framework-UNIQUE apex dipole: NOT accessible via aberration.")
print("    Aberration yields ONE acceleration vector (the Sun's), pointing at the Galactic")
print("    center. The framework's distinctive cos(psi) CMB-APEX dipole lives in the inertial")
print("    RESPONSE across an ENSEMBLE of a<a0 systems (the banked weak-lensing RAR dipole),")
print("    not in a single body's measured accel. No dipole handle here -> already-covered by")
print("    the banked apex-dipole front (below-floor this decade).")
print()

print("="*78)
print("VERDICT -- secular aberration drift arena")
print("="*78)
print("""  DOOR STATUS: MOND-SHARED + baryon-degenerate (NOT a fresh distinctive door).

  (i) The measured a_sun = 2.3e-10 m/s^2 IS a real number at ~2.5 a0 (transition regime,
      not high-a) -- so unlike GW/BH/lab, the MOND sector is NOT negligible here. Good catch
      that the four banked scripts skipped it.
  (ii) BUT aberration measures the TRUE KINEMATIC acceleration directly; every theory that
      fits the rotation curve predicts the SAME a_sun (= v_c^2/R0). It is not, by itself, a
      discriminator.
  (iii) Read as a missing-mass test, the framework predicts a ~22% inertial boost over the
      counted baryons -- but that is (a) MOND-SHARED (same nu family) and (b) degenerate with
      the tens-of-% baryonic M/L at R0 (the SAME SPARC-RAR wall). The framework-vs-MOND nu gap
      is ~{:.1f}% (above the DR5 ~1.4% STATISTICAL floor), BUT it is swamped by the >20-30%
      baryonic-a_bar SYSTEMATIC uncertainty -> NOT separable. Systematic-limited, not stat-limited.
  (iv) The one framework-UNIQUE signature (CMB-apex dipole) is NOT accessible from a single
      acceleration vector; it is the banked weak-lensing RAR-dipole front (below-floor).

  => NOT a new above-floor distinctive door. A genuinely a~a0 arena, but MOND-shared and
     baryon-degenerate -- it adds NO discriminating power beyond the RAR, which is already
     banked as convention-compatible / non-diagnostic of 9.36e-11. Both-ways: the framework
     is fully CONSISTENT with the Gaia aberration value (predicts a_sun at 2.5 a0 fine), it
     just is not distinctively TESTED by it.
""".format(diff_fw_mond*100))
print("exit 0")
