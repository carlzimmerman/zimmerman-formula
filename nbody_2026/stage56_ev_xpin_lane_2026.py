#!/usr/bin/env python3
# STAGE 56 EVIDENCE: the X-pin adversarial lane's own script (committed 2026-08-13 late).
# Verdict: PIN CONFIRMED as an order-of-magnitude CLASS, range corrected to X = 140-670
# core / 70-1340 defensible (stage 54's 316-1000 SUPERSEDED); the named escape CLOSED on
# three legs; stage 54's V_FF=300 relabelled (NOT committed) and its radius pairing fixed.
# -*- coding: utf-8 -*-
r"""
XPIN_adversarial_lane_2026.py -- the dedicated adversarial lane for THE X-PIN (stage54 B2).

CLAIM UNDER TRIAL: X := Q0 c^2/a0(0) is PINNED ~316-1000 by the equality
  v_s = sqrt(y_static) c / X  =  committed drain free-fall ~300 km/s,  y_static ~ 0.1-1.

Attacks, in the brief's order:
  P1  the NAMED ESCAPE (aether spatial profile splitting static from flow) -- priced.
  P2  is the A1 identity the right object in a static halo (shift-current statics).
  P3  the inputs: y_static provenance, the 300 km/s provenance, radius-consistent pairing,
      Qbar vs Q0.
  P4  consequences over the corrected band (y_rec, clean window, fork a).
  P5  independent corpus bounds (forest, solar system) at the pinned X.
"""
import numpy as np

C_KMS = 2.99792458e5
C = 2.99792458e8
G = 6.67430e-11
MPC = 3.0856775814913673e22
KPC = MPC / 1e3
H0 = 67.4e3 / MPC
OM_M, OM_L, OM_DM = 0.315, 0.685, 0.265
R_DM = OM_DM / OM_L
A0_CAN = 9.3619e-11
KAPPA = 0.5
NU0F, NU0C = 2.14e-5, 1.77e-4
ZREC = 1090.0
RREC = (1 + ZREC) ** 3
CH2 = 1.08e4                      # (km/s)^2 committed (stage53:180): c_h^2 = G M / R_halt
V_RMS_REC, V_MODE_REC = 23.1, 12.6   # km/s (laneY B2, referee-confirmed 19-28 / 12.6)
AMP_FLOOR, AMP_CEIL = 2.78e4, 2.30e5
LAM = 3 * OM_L * H0 ** 2 / C ** 2
A0T = A0_CAN / C ** 2             # a0-tilde 1/m
RHO_CRIT = 3 * H0 ** 2 / (8 * np.pi * G)
RHO_DM0 = OM_DM * RHO_CRIT

print("=" * 100)
print("P3 FIRST (the inputs) -- because the pin's range is built from them")
print("=" * 100)

# P3a: y_static at the committed radii, recomputed (X-free).  stage54 A2's own numbers.
print("\n  y_static = g_N/a0 at committed radii (CH2 = 1.08e4 (km/s)^2 committed stage53:180):")
for r_kpc in (3.74, 13.5, 60.0):
    gN = CH2 * 1e6 / (r_kpc * KPC)        # m/s^2
    print(f"    r = {r_kpc:6.2f} kpc: y_static = {gN/A0_CAN:.3f}")
# the y=1 radius:
r_y1 = CH2 * 1e6 / A0_CAN / KPC
print(f"    y = 1 occurs at r = {r_y1:.2f} kpc (interior to the halt radii)")
# NOTE: stage51:62 committed the PROSE 'order 0.1-1'; stage54 A2 COMPUTES 0.06-0.28 at the
# halt radii.  B2's use of y = 0.1-1 therefore pairs y-values with radii where they do not occur.

# P3b: the 300 km/s.  git -S: first appears in commit e0b8d360 (stage54 itself).
# Committed neighbours: stage17 drain arithmetic 2.0e5 m/s = 200 km/s (LOAD-BEARING: it set
# the nu0 ceiling); stage2 V_C = 200; V_H = sqrt(CH2) = 103.9; stage52's 609 (an INCOHERENCE
# marker, not a physical speed).  Defensible free-fall from the committed calibration:
# deep-MOND flat speed v_flat^2 = sqrt(G M a0) with G M = CH2 * R_halt:
print("\n  free-fall through RAR radii from the committed calibration itself:")
vff = {}
for r_kpc, rh_kpc in ((3.74, 13.5), (13.5, 13.5), (60.0, 60.0)):
    GM = CH2 * (rh_kpc * KPC / 1e3)                     # km^3/s^2 * km ... (km/s)^2 * km
    vflat2 = np.sqrt(GM * (A0_CAN / 1e3))               # (km/s)^2, deep-MOND flat speed
    for rta_mpc in (0.5, 1.0, 2.0):
        v2 = 2 * vflat2 * np.log(rta_mpc * 1e3 / r_kpc)
        vff.setdefault(r_kpc, []).append(np.sqrt(v2))
    print(f"    r = {r_kpc:6.2f} kpc (R_halt {rh_kpc}): v_flat = {np.sqrt(vflat2):.0f} km/s, "
          f"v_ff(r_ta 0.5-2 Mpc) = {min(vff[r_kpc]):.0f}-{max(vff[r_kpc]):.0f} km/s")

# P3c: radius-CONSISTENT pin X(r) = sqrt(y(r)) c / v_ff(r):
print("\n  the radius-consistent pin X(r) = sqrt(y(r)) c / v_ff(r):")
Xvals = []
for r_kpc in (3.74, 13.5, 60.0):
    y = CH2 * 1e6 / (r_kpc * KPC) / A0_CAN
    for v in vff[r_kpc]:
        Xvals.append(np.sqrt(min(y, 1.0)) * C_KMS / v)
    y_ = min(y, 1.0)
    print(f"    r = {r_kpc:6.2f} kpc: y = {y_:.3f}, X = "
          f"{np.sqrt(y_)*C_KMS/max(vff[r_kpc]):.0f}-{np.sqrt(y_)*C_KMS/min(vff[r_kpc]):.0f}")
X_LO_C, X_HI_C = min(Xvals), max(Xvals)
print(f"    => radius-consistent core band X = {X_LO_C:.0f}-{X_HI_C:.0f}")

# P3d: the SHAPE MISMATCH (why the pin cannot be an exact equality at any single X):
# RAR forces v_cong(r) = sqrt(y(r)) c/X  ~ r^(-1/2);  free-fall v_ff(r) ~ sqrt(ln), near-flat.
print("\n  shape mismatch (v_cong/v_ff normalised to 1 at 13.5 kpc):")
v0 = None
for r_kpc in (3.74, 13.5, 60.0):
    y = min(CH2 * 1e6 / (r_kpc * KPC) / A0_CAN, 1.0)
    vf = np.mean(vff[r_kpc])
    ratio = np.sqrt(y) / vf
    if r_kpc == 13.5:
        v0 = ratio
for r_kpc in (3.74, 13.5, 60.0):
    y = min(CH2 * 1e6 / (r_kpc * KPC) / A0_CAN, 1.0)
    vf = np.mean(vff[r_kpc])
    print(f"    r = {r_kpc:6.2f} kpc: (v_cong/v_ff)/(ratio at 13.5) = {np.sqrt(y)/vf/v0:.2f}")
print("    => the equality holds at ONE radius; across 4-60 kpc it drifts x~2-3.")
print("       The pin is an ORDER-OF-MAGNITUDE consistency condition, not an exact equality.")

# P3e: Qbar vs Q0 at z=0: Qbar = Q0 + I0/a^3, I0/Q0 = 8 pi R_dm/(kappa^2 X^2):
print("\n  Qbar/Q0 - 1 = 8 pi R_dm/(kappa X)^2:")
for X in (120.0, 316.0, 500.0, 1000.0):
    print(f"    X = {X:6.0f}: {8*np.pi*R_DM/(KAPPA*X)**2:.2e}")
print("    => sub-1e-3 across the band; the Qbar/Q0 distinction never moves the pin.")

print()
print("=" * 100)
print("P1 -- THE NAMED ESCAPE, priced: an aether profile splitting static from flow")
print("=" * 100)
print(r"""
  (a) THE KINEMATIC LEG IS AETHER-FREE.  v_i = -c d_i(phi)/(dphi/dt) is the phi-congruence
      velocity for ANY timelike-gradient configuration (u_mu = -d_mu phi/s, exact; stages 5/6
      use it nonlinearly: 'irrotational potential flow').  No aether profile enters it.
      Whatever the tilt does, |grad phi_s| = Qbar v_flow/c is FORCED by the dust's motion.

  (b) THE STRESS LEG IS TILT-BLIND.  T_ij from -(2-K_B)Y and -F(Y,Q) contains
      (2-K_B + 2F_Y) d_i(phi) d_j(phi) with d(phi) DIRECTLY (delta Y/delta g^munu|_A =
      d_mu phi d_nu phi; the A-dependence of q sits in Q^2, no explicit metric).  The metric --
      hence the RAR and lensing -- sees the FULL |grad phi_s|^2 stress no matter how the tilt
      re-partitions Y.  So a large-X drain (|grad phi_s| = Qbar v_ff/c >> sqrt(y) a0-tilde)
      cannot be hidden by a comoving aether:""")
for X in (1.8e5, 2.2e4, 1000.0, 500.0):
    excess = (X * 300.0 / C_KMS) ** 2 / 0.28
    print(f"      X = {X:9.3g}: stress excess over the RAR-required y at 13.5 kpc = "
          f"{excess:9.3g}x" + ("   <-- RAR destroyed" if excess > 3 else "   <-- RAR-compatible"))
print(r"""
  (c) THE TILT RESPONSE IS WEAK-FIELD SUPPRESSED (m/s, not km/s).  Every coupling in the
      aether's EOM is inside the 1/16 pi G-tilde action; the stationary halo-sourced tilt
      balances K_B grad^2 w against the streaming-charge source (2 F_Y Q + F_Q) Qbar v_rel:""")
rho_loc = 1654.0 * RHO_DM0
L = 100 * KPC
w_FQ = 8 * np.pi * G * rho_loc * L ** 2 / C ** 2 * 1e-3 / 0.10       # F_Q piece, K_B = 0.10
Qb2 = (500.0 * A0T) ** 2                                             # Qbar^2 at X = 500, 1/m^2
w_FY = Qb2 * 0.5 * L ** 2 * 1e-3 / 0.10                              # F_Y ~ sqrt(y) piece
print(f"      F_Q-sourced tilt:  w ~ {w_FQ:.1e} c = {w_FQ*C_KMS:.1e} km/s")
print(f"      F_Y-sourced tilt:  w ~ {w_FY:.1e} c = {w_FY*C_KMS:.1e} km/s  (X = 500)")
print(f"      vs the ~300 km/s comoving the escape needs: short by ~{1e-3/max(w_FQ,w_FY):.0e}x.")
print(r"""
  (d) THE OTHER SPLITS ARE SLAVED.  SZ21 Eq 12 in the static limit is an algebraic
      CONSTRAINT (K_B(Edot+HE) -> 0), not a new function; the Helmholtz phase freedom
      {C1,C2} alters galaxy-interior gradients only at (mu r)^2 ~ 1e-4 (mu^-1 >~ 1 Mpc,
      r ~ kpc) -- the SETUP doc's own geometric protection, now working AGAINST the escape.

  VERDICT P1: the static/flow split is FORCED, not free.  The named escape is CLOSED at the
  order-of-magnitude level: no aether profile can decouple the RAR gradient from the flow.""")

print()
print("=" * 100)
print("P2 -- is A1 the right object in a STATIC halo?  The shift-current statics")
print("=" * 100)
print(r"""
  In a STRICTLY static halo the scalar EOM is grad . J_shift = 0 with
    J_shift ~ -(2-K_B)(grad phi - grad Phi) - 2 F_Y grad phi + (J-term flux)
  and regularity at r = 0 forces the TOTAL radial flux to vanish POINTWISE.  The Cell-3
  J-term counter-flux (outward, ~grad Phi) cancels the congruence convection (inward,
  ~grad phi) EXACTLY -- 'the balance IS the MOND field equation' (c3 lane F1, confirmed).
  So a static halo does NOT drain: the congruence speed sqrt(y) c/X is real phase
  kinematics but carries ZERO net charge.  The naive drain reading of a static halo is
  WRONG -- and this is what KILLS the pin's original phrasing as a static statement.

  WHAT RESCUES THE PIN (on the framework's own commitments): the halo is NOT static.
  Smooth accretion is committed (the 1-Mpc confrontation: xi(halo) -> 1); stage17's
  nu0 CEILING is BUILT on condensate streaming through 15 kpc at 200 km/s (committed,
  load-bearing); the condensate is pressureless (c_s ~ 1.4 km/s committed) so the stream
  is geodesic ~ free-fall; and the congruence has ONE velocity per point (potential flow,
  no multi-streaming).  So at RAR radii the ONE gradient must simultaneously be
    Qbar v_ff/c   (kinematics of the committed, ongoing accretion stream)  and
    sqrt(y) a0-t  (the RAR force, which lives in F(Y) and nowhere else) --
  the pin equality, now derived through the DYNAMIC drain, not the static halo.
  Order-of-magnitude only (P3d): exact simultaneity is impossible at any single X, which
  is the dust problem itself surfacing in the RAR region.""")

print()
print("=" * 100)
print("P4 -- consequences over the CORRECTED band")
print("=" * 100)
# corrected band: the radius-consistent core from P3c, x2 slack each way for the
# non-stationarity (P3d) and the committed-speed spread (stage17's 200 pulls X up;
# the bulk-flow leg pulls X down):
X_CORE = (X_LO_C, X_HI_C)
X_BAND = (X_LO_C / 2, X_HI_C * 2)
print(f"\n  corrected pin: CORE X = {X_CORE[0]:.0f}-{X_CORE[1]:.0f} (radius-consistent, committed"
      f" calibration), DEFENSIBLE band X = {X_BAND[0]:.0f}-{X_BAND[1]:.0f} (x2 slack each way)."
      f"\n  vs stage54's 316-1000: OVERLAP at 316-{X_CORE[1]:.0f}; the committed band's top"
      f" third (670-1000) fails the radius-consistent pairing (y=1 occurs at 3.7 kpc where"
      f" v_ff = 450-510, not 300), and its bottom is a shade high (the 60-kpc anchor gives 136).")
print("\n  y_rec across the band (rms 23.1 km/s; floor amp 2.78e4 / ceiling 2.30e5):")
for X in (X_BAND[0], X_CORE[0], 316.0, 500.0, X_CORE[1], 1000.0, X_BAND[1]):
    yf = (X * V_RMS_REC / C_KMS) ** 2 * AMP_FLOOR
    yc = (X * V_RMS_REC / C_KMS) ** 2 * AMP_CEIL
    print(f"    X = {X:6.0f}: y_rec = {yf:8.1f} (floor) / {yc:9.0f} (ceiling)"
          + ("   marginal" if yf < 4 else "   saturated"))
y_bot_f = (X_BAND[0] * V_RMS_REC / C_KMS) ** 2 * AMP_FLOOR
y_bot_c = (X_BAND[0] * V_RMS_REC / C_KMS) ** 2 * AMP_CEIL
y_core_f = (X_CORE[0] * V_RMS_REC / C_KMS) ** 2 * AMP_FLOOR
print(f"\n  fork (a): at the CORE bottom y_rec(floor) = {y_core_f:.1f} > 1 -- realized across"
      f" the full core band.  At the extreme slack corner X = {X_BAND[0]:.0f}: floor amp gives"
      f" {y_bot_f:.2f} (MARGINAL, not saturated) but ceiling amp gives {y_bot_c:.1f} > 1 --"
      f" fork (a) survives, with the one honest marginal corner named.")
print(f"  CLASS-clean window (X < 78 rms-floor / 27 rms-ceiling): EMPTY across the CORE band;")
print(f"  the extreme slack corner X ~ 68 GRAZES the floor-amp window (0.76 < 1) but stays")
print(f"  saturated at ceiling amp (6.3) -- the dilemma's first horn stands at every")
print(f"  defensible X, grading from 'active Y-sector' to 'marginally active' at the corner.")

print()
print("=" * 100)
print("P5 -- independent corpus bounds at the pinned X")
print("=" * 100)
def Arat(r, nu0):
    return np.sqrt(1 + nu0 ** 2) / np.sqrt(1 + (nu0 * r) ** 2)
# forest (z ~ 2.5, v ~ 30-60 km/s, A ~ flat there):
for X, v in ((500.0, 30.0), (1000.0, 60.0)):
    amp = 1 / Arat(3.5 ** 3, NU0C)
    y = (X * v / C_KMS) ** 2 * amp
    print(f"  forest z=2.5: X = {X:5.0f}, v = {v:.0f} km/s: y_flow = {y:.3f} "
          f"(needs << 1 for deep-MOND forest scales: {'OK' if y < 0.1 else 'MARGINAL' if y < 1 else 'BROKEN'})")
# solar system: flow-y from the Sun's 370 km/s CMB motion vs the static gradient at 1 AU:
gN_1AU = 5.9e-3
y_qs_ss = gN_1AU / A0_CAN
for X in (500.0, 1000.0):
    y_fl = (X * 370.0 / C_KMS) ** 2
    print(f"  solar system: X = {X:5.0f}: flow-y = {y_fl:.2f} vs static y = {y_qs_ss:.1e} "
        f"-- flow is {y_fl/y_qs_ss:.1e} of static: no new solar-system effect (static dominates)")
# the bulk-flow leg (named, open): if the aether does NOT track LSS flows, galaxies' peculiar
# motion 300-600 km/s adds to the RAR-radius misalignment: X <= sqrt(y) c/v_total pushes the
# pin DOWN (never up), and RAR scatter would correlate with v_pec -- unobserved at 0.108 dex:
for v_pec in (300.0, 600.0):
    print(f"  bulk-flow leg: v_pec = {v_pec:.0f} km/s => X <= {np.sqrt(0.28)*C_KMS/v_pec:.0f} "
          f"(13.5 kpc anchor) -- inside/below the core band; the leg TIGHTENS, never dissolves")
print("\n  NOTE: whether the linear-regime aether tilt tracks LSS bulk flows is the ONE open")
print("  aether question (needs SZ21's linear vector solution = owed item (2) of stage54).")
print("  Either answer keeps the pin: tracking => comparator = internal drain (as used);")
print("  not tracking => comparator larger => X smaller, fork (a) still realized (P4).")
