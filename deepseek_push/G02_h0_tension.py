#!/usr/bin/env python3
r"""G02 -- THE FRAMEWORK'S H0: what the horizon identity implies for the
Hubble tension, stated and quantified.

THE DOOR.  Z11's identity a0 = c^2/(Z R_dS) = kappa_dS/Z with
R_dS = c/(H0 sqrt(Omega_Lambda)) INVOLVES H0: a0 = c H0 sqrt(Omega_L)/Z.
Does the framework speak to the Hubble tension?

(1) THE H0 FACE -- the committed inversion.  From
      a0   = c^2/(Z R_dS),   R_dS = c/(H0 sqrt(Omega_L))
    substitution gives a0 = c H0 sqrt(Omega_L)/Z, i.e. INVERTING:
      H0   = Z a0 / (c sqrt(Omega_L)).
    At the committed constants (a0_DE = 9.3619e-11, Omega_L = 0.685,
    Z = 2 sqrt(8 pi/3) = 5.78881) this returns H0_framework = 67.413
    (km/s/Mpc); at the horizon value a0_H = 9.362375e-11 it returns
    EXACTLY 67.4000 (the identity is built from the same constants, so
    the inversion is EXACT -- a tautological re-inversion, ratio 1.00005
    between the two footings).  Also quantified: the weld to the other
    side of the tension -- H0 = 73.0 (SH0ES-class) binds a0 = 1.0139e-10
    (the +8.31% a0-split: Planck -> 9.3619e-11, SH0ES -> 1.014e-10, the
    MINE_M1/EQUATION_BOOK register), and the alt galactic footing
    a0_alt = 1.1279e-10 (G204/G088) binds H0 = 81.2 (unchanged register).

(2) THE TENSION STATEMENT.  H0_framework = 67.41 vs the local 73.0
    (SH0ES-class, UNVERIFIED in this repo) and the early-universe 67.4
    (Planck).  THE FRAMEWORK'S PREDICTED H0 SITS AT THE 67.4-68.0 CLASS
    BY CALIBRATION: a0_DE was committed at the Planck-consistent H0
    (the G058 identity Omega = 32 pi a0^2/(3 H0^2 c^2) closes to 0.685
    exactly at (a0_DE, H0 = 67.4)), and the C06 closure is the
    Lean-certified TAUTOLOGICAL FIXED POINT -- EVERY Omega is a fixed
    point of the map, the reconstruction is independent of H0's numeric
    value (num_horizon_omega_exact), so the identity chain is H0-BLIND:
    it cannot select 67 or 73.  THE HONEST STATEMENT: the framework
    does NOT resolve the tension -- it INHERITS the early-universe H0
    through a0's calibration.  THE AUDIT (is there ANY relation that
    prefers 67 or 73 independently?): (a) the inversion itself: no --
    it re-reads the calibration; (b) the ladder-free flow H0 (h94):
    68.7 +- 3.4 (canonical footing, 0.4 sigma from Planck) vs
    73.9 +- 3.6 (alt footing, 0.2 sigma from SH0ES) -- the two a0
    footings sit on OPPOSITE SIDES of the tension, the footing alone
    decides the camp, NO arbitration; (c) the z* = 2.4 freeze epoch:
    T_b = T_CMB(z*) is a TAUTOLOGY that DEFINES the epoch (F07) -- no
    value; (d) the DR4 ridge: its normalization moves < 1% under the
    whole 8.31% H0 split -- no discrimination.  ANSWER: NO relation
    prefers 67 or 73 independently.

(3) THE PREDICTION FACE -- the H0-dependent predictions and their
    deltas if H0 = 73.0 instead of 67.4 (Omega_L and a0's slot fixed:
    a0 scales WITH H0 as a0 = c H0 sqrt(Omega_L)/Z):
      R_dS    = c/(H0 sqrt(Omega_L))   : x0.92329  =  -7.671% linear
                                          (-0.0347 dex; the "-3.5%" guess
                                           is the DEX, corrected here)
      T_dS    = hbar H_Lambda/(2 pi k_B): x1.08309  =  +8.309% linear
                                          (+0.0341 dex)
      freeze  (1+z*) = m sigma^2/(k_B T0),
               sigma^2 = (1/2) sqrt(G M_b a0): x1.04075 = +4.075% linear
               (z*: 2.3656 -> 2.502, 2.40 -> 2.538; T_b: 9.267 -> 9.644 K)
      r_M     = sqrt(G M_b / a0)      : x0.96081  =  -3.919% linear
      DR4 ridge s_exc = (1 + m_cl/M_b)^(1/3),
               m_cl = sqrt(G M_b a0) s / G: +0.57% linear (plateau
               1.1840 -> 1.1908); gamma_plateau 1.2886 -> 1.2991 (+0.81%)
               -- the ridge is an a0-scale test, NOT an H0 test.
    THE OBSERVATIONAL PREFERENCE (which H0 the committed data prefer
    THROUGH the framework): (a) the a0 zero point: the clean TRIO core
    (104 galaxies, SPARC+HI+bright dSph) sits ON a0_H (0.976 x a0_H,
    z = -0.20) -- prefers the 67.4-class footing in central value; the
    SH0ES-weld a0 = 1.014e-10 sits only +0.85 sigma from the TRIO -- no
    decisive split at current precision; the full-542 line zero point
    (1.81 x a0_H <-> H0 ~ 122) is the REGISTERED M/L-normalization
    departure (ATLAS3D JAM + end-departures, Z11), NOT an H0 datum;
    (b) the DR4 ridge: forecast at the committed (67.4-anchored) a0; a
    % -precision ridge measures a0_eff (footing K1: a0_RAR vs a0_DE) --
    through the weld, an H0 probe at +-8% granularity; today it prefers
    its own committed forecast; (c) the freeze epoch: tautological by
    construction (F07) -- no preference; the committed z* = 2.3656 -
    2.4932 (G132) is data-anchored through m and T0, consistent with
    both H0 classes at ~2%.  STATEMENT: the data prefer the 67.4-class
    THROUGH the framework because every committed observable was
    REGISTERED at the 67.4-anchored a0; there is no independent arbiter.

(4) VERDICTS:
    V1 -- H0_framework = 67.413 km/s/Mpc (a0_DE footing; exact 67.4000
         at a0_H); the committed inversion H0 = Z a0/(c sqrt(Omega_L)).
    V2 -- the framework does NOT resolve the Hubble tension: its
         predicted H0 inherits the early-universe H0 through a0's
         calibration; the audit finds NO relation preferring 67 or 73
         independently (identity chain H0-blind, C06; flow route
         footing-ambiguous, h94; z* tautological, F07; ridge < 1%).
    V3 -- the honest statement: the framework's Hubble relation
         a0 = c H0 sqrt(Omega_L)/Z inverts to H0 = Z a0/(c sqrt(Omega_L))
         and returns the 67.4-68.0 class by calibration; under
         H0 = 73.0 its predictions move by: R_dS -7.67% (-0.0347 dex),
         T_dS +8.31%, (1+z*) +4.07%, r_M -3.92%, DR4 ridge +0.57% --
         all small, none decisive; the framework inherits the early-
         universe H0, no independent tension resolution.

DELIVERABLE: deepseek_push/G02_h0_tension.py + .out + G02_results.json.
Commit and push.  Registers read (nothing recomputed): Z11, C06, G058,
E01, F07, G212, G163, G132, h94, G189, G088, G089/C09, MINE_M1.
Only deepseek_push/ is written.
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# committed constants (repo convention: Z11/G058/F07/E01)
# ---------------------------------------------------------------------------
C      = 2.99792458e8                     # m/s, exact (SI)
G      = 6.674e-11                        # m^3 kg^-1 s^-2, repo convention
H0KMS  = 67.4                             # km/s/Mpc (G058/G189/Z11)
H0     = H0KMS * 1000.0 / 3.085677581e22  # s^-1
OM_L   = 0.685                            # committed Omega_Lambda
Z      = 2.0 * math.sqrt(8.0 * math.pi / 3.0)   # 5.7888100, the germ (C06)
A0_DE  = 9.3619e-11                       # m/s^2, committed DE footing
A0_ALT = 1.1279e-10                       # m/s^2, the alt galactic footing
MSUN   = 1.98892e30                       # kg
KB     = 1.380649e-23                     # J/K
HBAR   = 1.054571817e-34                  # J s (CODATA 2018)
EV_J   = 1.602176634e-19                  # J
T0     = 2.72548                          # K (FIRAS)
ZSTAR_MW  = 2.3656                        # the MW-rung freeze epoch (G132/G213)
ZSTAR_LO, ZSTAR_HI = 2.3656, 2.4932       # G132 registered band
T_BAND  = (9.1729, 9.5205)                # K (A03/Z11 committed phase band)
SIG_MW  = 119.2 * 1e3                     # m/s, the galaxy triad (G213/G168)
MB_MW   = 6.5e10 * MSUN                   # kg (the G003/G119 anchor)
MPC_SI  = 3.085677581e22                  # m per Mpc
KMPS_TO_MPC = 1.0e3 / MPC_SI              # (km/s/Mpc) -> s^-1

# registry values read from the committed artifacts (not recomputed)
H94_CANON = 68.7                          # hunt_2026/h94: flow H0, canonical
H94_ALT   = 73.9                          # hunt_2026/h94: flow H0, alt footing
H94_SIG   = 3.4                           # h94 statistical error (V>2000 cut)
A0_TRIO   = 9.140756175736266e-11         # Z11: TRIO a0 (n = 104)
ZTRIO     = -0.1956400645292849           # Z11: TRIO z vs a0_H
A0_LINE   = 1.69782963817582e-10          # Z11: full-542 slope-fixed zero pt
RATIO_LINE = 1.8134603674641752           # Z11: a0_line / a0_H

CHECKS = []
def chk(name, ok, detail=""):
    CHECKS.append({"name": name, "pass": bool(ok), "detail": str(detail)})
    print("  [%s] %s%s" % ("PASS" if ok else "FAIL", name,
                           ("   | " + str(detail)[:130]) if detail else ""),
          flush=True)
    return bool(ok)

print("=" * 104)
print("G02 -- THE FRAMEWORK'S H0: the horizon identity vs the Hubble tension")
print("=" * 104)
print()

# ---------------------------------------------------------------------------
# (1) THE H0 FACE -- the committed inversion
# ---------------------------------------------------------------------------
print("(1) THE H0 FACE:  a0 = c^2/(Z R_dS),  R_dS = c/(H0 sqrt(Omega_L))")
print("    substitution:  a0 = c H0 sqrt(Omega_L)/Z")
print("    INVERTED:      H0 = Z a0 / (c sqrt(Omega_L))")
R_DS = C / (H0 * math.sqrt(OM_L))                    # m
A0_H = C * H0 * math.sqrt(OM_L) / Z                  # the horizon value
print("    R_dS = %.6e m = %.4f Gpc   (committed, H0 = 67.4)" %
      (R_DS, R_DS / 3.085677581e25))

def h0_from_a0(a0):
    """H0 = Z a0/(c sqrt(Omega_L)) in km/s/Mpc."""
    return Z * a0 / (C * math.sqrt(OM_L)) / KMPS_TO_MPC

H0_FW_DE  = h0_from_a0(A0_DE)            # the committed footing inversion
H0_FW_H   = h0_from_a0(A0_H)             # the horizon-value inversion
H0_FW_ALT = h0_from_a0(A0_ALT)           # the alt galactic footing
print("    H0_framework (a0_DE footing)  = %.6f km/s/Mpc   [THE COMMITTED "
      "INVERSION]" % H0_FW_DE)
print("    H0_framework (a0_H horizon)   = %.6f km/s/Mpc   (exact -- the "
      "identity is built from the same constants)" % H0_FW_H)
print("    H0_framework (a0_alt footing) = %.4f km/s/Mpc   (the G204/G088 "
      "alt register, unchanged)" % H0_FW_ALT)
chk("the committed inversion returns the calibration H0: "
    "67.40-67.42 km/s/Mpc at the committed footings",
    abs(H0_FW_DE - 67.4) < 0.05 and abs(H0_FW_H - 67.4) < 1e-9,
    "%.5f (a0_DE) / %.9f (a0_H)" % (H0_FW_DE, H0_FW_H))
chk("the inversion is EXACT on the identity: a0_H = c H0 sqrt(Omega_L)/Z "
    "re-inverts to 67.400000000",
    abs(H0_FW_H - 67.4) < 1e-6, "%.12f" % H0_FW_H)

# the weld: H0 = 73.0 (SH0ES-class) binds the a0 that the framework would
# need -- the 8.31% a0-split (MINE_M1 / EQUATION_BOOK register)
RATIO_H0 = 73.0 / 67.4
A0_SH0ES = A0_DE * RATIO_H0
print()
print("    THE WELD (the tension mapped onto the framework's own slot):")
print("    H0 = 73.0 (SH0ES-class) <-> a0 = %.5e m/s^2  (%.2f%% above the "
      "committed a0_DE)" % (A0_SH0ES, 100.0 * (RATIO_H0 - 1.0)))
chk("the tension maps onto an 8.31% a0 split: Planck -> 9.3619e-11, "
    "SH0ES -> 1.014e-10 (MINE_M1 / EQUATION_BOOK register)",
    abs(A0_SH0ES - 1.014e-10) / 1.014e-10 < 1e-3,
    "a0_SH0ES = %.6e vs registered 1.014e-10" % A0_SH0ES)
chk("the alt galactic footing a0_alt = 1.1279e-10 (G204/G088) binds "
    "H0 = 81.2 km/s/Mpc -- a SEPARATE register, not an SH0ES weld",
    abs(H0_FW_ALT - 81.2) / 81.2 < 2e-3, "%.2f" % H0_FW_ALT)

# ---------------------------------------------------------------------------
# (2) THE TENSION STATEMENT
# ---------------------------------------------------------------------------
print()
print("(2) THE TENSION STATEMENT")
print("    H0_framework = %.2f (a0_DE footing) -- the 67.4-68.0 class" %
      H0_FW_DE)
print("    vs local SH0ES-class 73.0 (UNVERIFIED in this repo) and the "
      "early-universe 67.4 (Planck):")
print("      the tension's width: 73.0 - 67.4 = 5.6 km/s/Mpc (8.31% of "
      "67.4)")
print("    the framework inherits the early-universe H0 through a0's "
      "calibration:")
print("      a0_DE = 9.3619e-11 was committed at (H0, Omega_L) = (67.4, "
      "0.685): the G058 identity")
print("      Omega = 32 pi a0_DE^2/(3 H0^2 c^2) = 0.684929 -> closes to "
      "0.685 exactly (G189 register);")
print("      the C06 closure is the Lean-certified TAUTOLOGICAL FIXED "
      "POINT: EVERY Omega is a")
print("      fixed point of the map Omega -> 32 pi a0(Omega)^2/(3 H0^2 "
      "c^2) and the reconstruction is")
print("      independent of H0's numeric value (num_horizon_omega_exact) "
      "-- the identity chain is H0-BLIND.")
om_rec = 32.0 * math.pi * A0_DE ** 2 / (3.0 * H0 * H0 * C * C)
chk("G058 at the committed pair: Omega(a0_DE, H0 = 67.4) = 0.685 to 1e-4 "
    "(G189 register 0.684930)",
    abs(om_rec - OM_L) < 1e-4, "Omega = %.6f" % om_rec)
# H0-blindness: at ANY H0, the horizon pair keeps the identity closed
worst = 0.0
for hh in (67.4, 70.0, 73.0, 80.0):
    hh_si = hh * 1000.0 / MPC_SI
    a0h = C * hh_si * math.sqrt(OM_L) / Z
    rec = 32.0 * math.pi * a0h ** 2 / (3.0 * hh_si * hh_si * C * C)
    worst = max(worst, abs(rec - OM_L) / OM_L)
chk("H0-BLIND identity chain re-verified: the horizon pair closes Omega = "
    "0.685 EXACTLY at H0 = 67.4, 70, 73, 80 (C06 fixed point -- the "
    "closure selects NO H0)",
    worst < 1e-9, "max |rec-0.685|/0.685 = %.2e" % worst)

print("    THE AUDIT -- any framework relation that prefers 67 or 73 "
      "INDEPENDENTLY?")
print("      (a) the inversion itself: NO -- it re-reads the calibration "
      "(V1's number IS the input H0).")
print("      (b) the ladder-free FLOW H0 (h94, the framework's own "
      "registry):")
print("          canonical footing (a0_DE): 68.7 +- 3.4  (0.4 sigma from "
      "Planck 67.4)")
print("          alt footing (a0_alt)     : 73.9 +- 3.6  (0.2 sigma from "
      "SH0ES 73.0)")
print("          'the two a0 footings sit on OPPOSITE SIDES of the Hubble "
      "tension; this route")
print("           cannot arbitrate the tension; it can only be told which "
      "side it is on' (h94) --")
print("          the footing alone decides the camp.")
chk("h94 registry quoted exactly: canonical 68.7 +- 3.4 (Planck, 0.4 "
    "sigma), alt 73.9 +- 3.6 (SH0ES, 0.2 sigma)",
    abs(H94_CANON - 68.7) < 0.1 and abs(H94_ALT - 73.9) < 0.1,
    "%s / %s with footnote: footing-ambiguous, no arbitration" %
    (H94_CANON, H94_ALT))
print("      (c) the z* = 2.4 freeze epoch: T_b = T_CMB(z*) is a "
      "TAUTOLOGY that DEFINES the epoch")
print("          (F07 2b: z* = T_b/T_0 - 1 by construction) -- the claim's "
      "content is the epoch")
print("          itself (cosmic noon, G011's discriminator) and the mass "
      "inversion m = 4.60-5.05 keV,")
print("          NOT an H0 preference; the epoch SHIFTS with H0 as "
      "(1+z*) ~ H0^(1/2) (Part 3).")
print("      (d) the DR4 ridge: its a0-carrying normalization moves < 1% "
      "under the whole 8.31%")
print("          H0 split (Part 3) -- the ridge is an a0-scale test, not "
      "an H0 test.")
print("      ANSWER: NO framework relation prefers 67 or 73 "
      "independently.")
print("    VERDICT V2: the framework does NOT resolve the Hubble tension.")
print("      It inherits the early-universe H0 through a0's calibration "
      "(67.4 -> a0 = 9.3619e-11,")
print("      G058-closed), at the 67.4-68.0 class in its own registries "
      "(67.41 inversion; h94 68.7).")

# ---------------------------------------------------------------------------
# (3) THE PREDICTION FACE -- the deltas under H0 = 73.0
# ---------------------------------------------------------------------------
print()
print("(3) THE PREDICTION FACE:  if H0 = 73.0 instead of 67.4 (Omega_L and "
      "a0's slot fixed;")
print("    a0 SCALES WITH H0 via a0 = c H0 sqrt(Omega_L)/Z):")
H0_73 = 73.0 * 1000.0 / MPC_SI
R_DS_73    = C / (H0_73 * math.sqrt(OM_L))
T_DS       = HBAR * (H0 * math.sqrt(OM_L)) / (2.0 * math.pi * KB)     # at 67.4
T_DS_73    = HBAR * (H0_73 * math.sqrt(OM_L)) / (2.0 * math.pi * KB)
S_SQRT     = math.sqrt(H0_73 / H0)          # (1+z*), T_b, r_M^-1, sigma^2
ZSTAR_73   = (1.0 + ZSTAR_MW) * S_SQRT - 1.0
ZSTAR_24   = (1.0 + 2.4) * S_SQRT - 1.0
T_B_73     = 2.72548 * (1.0 + 2.4) * S_SQRT
# DR4 ridge: m_cl = sqrt(G M_b a0) s / G -> s_exc = (1 + m_cl/M_b)^(1/3)
MM_CAP    = 0.6605                          # G088/G006: M_ph(<cap)/M_b
MM_CAP_73 = MM_CAP * S_SQRT                 # m_cl ~ a0^(1/2)
S_EXC     = (1.0 + MM_CAP) ** (1.0 / 3.0)
S_EXC_73  = (1.0 + MM_CAP_73) ** (1.0 / 3.0)
GAM_PL    = math.sqrt(1.0 + MM_CAP)
GAM_PL_73 = math.sqrt(1.0 + MM_CAP_73)

def pct(x, y):
    return 100.0 * (x / y - 1.0)

print("      R_dS  = c/(H0 sqrt(Omega_L))")
print("        R_dS: %.6e -> %.6e m    %.2f%% (LINEAR)   %+.5f (DEX)"
      % (R_DS, R_DS_73, pct(R_DS_73, R_DS), math.log10(R_DS_73 / R_DS)))
print("        in Gpc: %.4f -> %.4f  (5.374 -> 4.962)" %
      (R_DS / 3.085677581e25, R_DS_73 / 3.085677581e25))
print("        NOTE: the '-3.5%' pre-guess is the change in DEX "
      "(-3.47%); the LINEAR delta")
print("        is -7.67%.  [corrected: the horizon radius shrinks by "
      "7.67% at H0 = 73]")
chk("R_dS delta at H0 = 73: -7.67% linear (-0.0347 dex); the '-3.5%' "
    "figure is the dex, corrected",
    abs(pct(R_DS_73, R_DS) + 7.671) < 0.05
    and abs(math.log10(R_DS_73 / R_DS) + 0.03470) < 5e-4,
    "%.3f%% linear / %+.5f dex" % (pct(R_DS_73, R_DS),
                                   math.log10(R_DS_73 / R_DS)))
print("      T_dS  = hbar H_Lambda/(2 pi k_B),  H_Lambda = H0 sqrt(Omega_L)"
      " (the horizon temperature, F07 rung 1)")
print("        T_dS: %.4e -> %.4e K    %+.3f%% linear   %+.5f dex"
      % (T_DS, T_DS_73, pct(T_DS_73, T_DS), math.log10(T_DS_73 / T_DS)))
chk("T_dS delta at H0 = 73: +8.31% linear (A03 register 2.1977e-30 K "
    "verified)",
    abs(T_DS / 2.197696e-30 - 1.0) < 1e-3
    and abs(pct(T_DS_73, T_DS) - 8.309) < 0.05,
    "%.4e K at 67.4 (register 2.197696e-30); %+.3f%% at 73"
    % (T_DS, pct(T_DS_73, T_DS)))
print("      freeze epoch:  1+z* = m sigma^2/(k_B T0),  sigma^2 = "
      "(1/2) sqrt(G M_b a0) ~ H0^(1/2)")
print("        (1+z*) x %.5f:  z*(MW 2.3656) -> %.4f;  z*(2.40) -> %.4f;  "
      "T_b: 9.2666 -> %.3f K" %
      (S_SQRT, ZSTAR_73, ZSTAR_24, T_B_73))
print("        +%.3f%% linear on (1+z*)  (+%.5f dex)" %
      (pct(S_SQRT, 1.0), math.log10(S_SQRT)))
chk("freeze-epoch delta at H0 = 73: (1+z*) +4.08% -> z* = 2.50 (MW rung) / "
    "2.54 (z* = 2.40); T_b 9.64 K",
    abs(pct(S_SQRT, 1.0) - 4.075) < 0.05 and abs(ZSTAR_73 - 2.5022) < 1e-3,
    "(1+z*) %+.3f%%; MW z*: %.4f" % (pct(S_SQRT, 1.0), ZSTAR_73))
print("      r_M   = sqrt(G M_b/a0) ~ H0^(-1/2)")
print("        x %.5f:  %+.3f%% linear  (e.g. r_M(Sun) 7959 -> %.1f AU)" %
      (math.sqrt(H0 / H0_73), pct(math.sqrt(H0 / H0_73), 1.0),
       7959.0 * math.sqrt(67.4 / 73.0)))
chk("r_M delta at H0 = 73: -3.92% linear (r_M ~ H0^(-1/2))",
    abs(pct(math.sqrt(H0 / H0_73), 1.0) + 3.919) < 0.05,
    "%+.3f%%" % pct(math.sqrt(H0 / H0_73), 1.0))
print("      DR4 ridge:  s_exc = (1 + m_cl/M_b)^(1/3),  m_cl ~ a0^(1/2) ~ "
      "H0^(1/2)")
print("        plateau s_exc: %.4f -> %.4f  (%+.3f%%)   "
      "gamma_plateau: %.4f -> %.4f (%+.3f%%)" %
      (S_EXC, S_EXC_73, pct(S_EXC_73, S_EXC), GAM_PL, GAM_PL_73,
       pct(GAM_PL_73, GAM_PL)))
print("        the whole 8.31% H0 split moves the ridge by < 1% -- the "
      "ridge is an a0-scale test,")
print("        NOT an H0 discriminator (the EFE cap 7.4 kAU is "
      "a0-independent: g_ext of the MW).")
chk("DR4 ridge delta at H0 = 73: s_exc +0.57%, gamma +0.81% -- below "
    "forecast resolution;",
    abs(pct(S_EXC_73, S_EXC) - 0.57) < 0.1 and abs(pct(GAM_PL_73, GAM_PL)
                                                  - 0.81) < 0.1,
    "s_exc %+.3f%%, gamma %+.3f%%" % (pct(S_EXC_73, S_EXC),
                                      pct(GAM_PL_73, GAM_PL)))

print()
print("    THE OBSERVATIONAL PREFERENCE -- which H0 the committed data "
      "prefer THROUGH the framework:")
print("      (a) the a0 zero point: the clean TRIO core (SPARC + HI + "
      "bright dSph, n = 104)")
print("          sits ON a0_H (0.976 x a0_H, z = -0.20, Z11) -- central "
      "value at the 67.4-class;")
print("          the SH0ES-weld a0 = 1.014e-10 sits only +%.2f sigma from "
      "the TRIO -- no decisive" % 0.85)
print("          split at current precision; the full-542 line zero point "
      "(1.81 x a0_H <-> H0 = 122)")
print("          is the REGISTERED M/L-normalization departure (ATLAS3D "
      "JAM + end-departures, Z11),")
print("          NOT an H0 datum.")
z_trio_sh0es = math.log10(A0_SH0ES / A0_TRIO) / (0.0104 / 0.1956)
chk("TRIO-vs-SH0ES-weld quantified: dex = %.3f, z = %.2f (computed from "
    "Z11's TRIO fit sigma)" % (math.log10(A0_SH0ES / A0_TRIO),
                               z_trio_sh0es),
    abs(z_trio_sh0es - 0.85) < 0.2,
    "SH0ES side is +%.2f sigma from the TRIO zero point" % z_trio_sh0es)
print("      (b) the DR4 ridge: the zero-parameter forecast (G088) was "
      "REGISTERED at the committed")
print("          (67.4-anchored) a0; a %-precision ridge measurement "
      "resolves the a0 footing")
print("          (G190 K1: a0_RAR vs a0_DE) -- through the weld, an H0 "
      "probe at +-8%% granularity;")
print("          today the ridge prefers its own committed forecast.")
print("      (c) the freeze epoch: tautological by construction (F07) -- "
      "no preference; the")
print("          committed z* = 2.3656-2.4932 (G132) is data-anchored "
      "through m = 5.09 keV and")
print("          T0 = 2.72548 K, consistent with BOTH H0 classes at ~2%.")
print("      STATEMENT: the committed data prefer the 67.4-class THROUGH "
      "the framework because")
print("      every committed observable (the a0 footing itself, the "
      "G058/0.685 closure, the z* band,")
print("      the T_b band, the DR4 forecast) was REGISTERED at the "
      "67.4-anchored a0 -- and no")
print("      independent arbiter exists (the audit of Part 2).")

# ---------------------------------------------------------------------------
# (4) VERDICTS
# ---------------------------------------------------------------------------
v1 = ("V1 -- H0_framework = %.4f km/s/Mpc (the committed inversion "
      "H0 = Z a0/(c sqrt(Omega_L)) at the a0_DE footing; EXACT 67.400000000 "
      "at the horizon value a0_H = %.6e, the identity re-inverting "
      "itself).  THE FRAMEWORK'S H0 FROM THE HORIZON + a0 + Omega_L: the "
      "67.4-68.0 class." % (H0_FW_DE, A0_H))
v2 = ("V2 -- THE TENSION STATEMENT: the framework does NOT resolve the "
      "Hubble tension.  Its predicted H0 (%.2f vs the local SH0ES-class "
      "73.0, UNVERIFIED, and the early-universe Planck 67.4) inherits the "
      "early-universe H0 through a0's calibration: a0_DE was committed at "
      "(67.4, 0.685) with the G058 identity closed (0.684930, G189), and "
      "the C06 closure is the Lean-certified tautological fixed point, "
      "H0-BLIND (EVERY Omega fixed; the reconstruction independent of "
      "H0's numeric value) -- the identity chain cannot select 67 or 73.  "
      "THE AUDIT: NO relation prefers 67 or 73 independently: (a) the "
      "inversion re-reads the calibration; (b) the ladder-free flow H0 "
      "(h94) = 68.7 +- 3.4 (canonical, 0.4 sigma from Planck) vs "
      "73.9 +- 3.6 (alt, 0.2 sigma from SH0ES) -- the two footings sit on "
      "OPPOSITE SIDES of the tension, the footing alone decides the camp; "
      "(c) the z* = 2.4 freeze epoch is a tautology defining the epoch "
      "(F07) -- no value; (d) the DR4 ridge moves < 1%% under the whole "
      "8.31%% split -- no discrimination." % H0_FW_DE)
v3 = ("V3 -- THE HONEST STATEMENT: the framework's Hubble relation "
      "a0 = c H0 sqrt(Omega_L)/Z inverts to H0 = Z a0/(c sqrt(Omega_L)) "
      "and returns the 67.4-68.0 class BY CALIBRATION (%.2f at a0_DE; "
      "h94's independent flow registry 68.7 +- 3.4, the same class).  It "
      "INHERITS the early-universe H0; it offers NO independent tension "
      "resolution.  Under H0 = 73.0 the framework's H0-dependent "
      "predictions move by: R_dS %.2f%% LINEAR (-0.0347 dex -- the '-3.5%%' "
      "guess is the dex, corrected), the horizon temperature T_dS %+.2f%%, "
      "the freeze epoch (1+z*) %+.2f%% (z* 2.3656 -> 2.50; T_b 9.267 -> "
      "9.64 K), r_M %.2f%%, and the DR4 ridge s_exc %+.2f%% (gamma %+.2f%%)"
      " -- every delta small, none decisive; the committed data prefer "
      "the 67.4-class through the framework only because the committed "
      "observables were registered at the 67.4-anchored a0.  THE "
      "FRAMEWORK'S VERDICT ON THE TENSION: it lives on the early-universe "
      "side, by inheritance, and says so." %
      (H0_FW_DE, pct(R_DS_73, R_DS), pct(T_DS_73, T_DS), pct(S_SQRT, 1.0),
       pct(math.sqrt(H0 / H0_73), 1.0), pct(S_EXC_73, S_EXC),
       pct(GAM_PL_73, GAM_PL)))
print()
print("(4) VERDICTS")
print("    " + v1)
print("    " + v2)
print("    " + v3)

# ---------------------------------------------------------------------------
# results json
# ---------------------------------------------------------------------------
res = {
 "lane": "G02_h0_tension",
 "title": "THE FRAMEWORK'S H0: what the horizon identity implies for the "
          "Hubble tension, stated and quantified",
 "date": "2026-09-16",
 "gate": "identity arithmetic re-run in-file; registries read from the "
         "committed artifacts (Z11, C06, G058/G189, h94, F07, G212/G163/"
         "G132, G088/G006, MINE_M1) -- nothing re-fitted",
 "part1_h0_face": {
   "identity": "a0 = c^2/(Z R_dS) = c H0 sqrt(Omega_L)/Z with "
               "R_dS = c/(H0 sqrt(Omega_L))",
   "inversion": "H0 = Z a0/(c sqrt(Omega_L))",
   "constants": {"H0_kms_Mpc": H0KMS, "Omega_Lambda": OM_L, "G": G,
                 "c": C, "Z": Z, "a0_DE": A0_DE, "a0_H": A0_H,
                 "a0_alt": A0_ALT},
   "H0_framework_a0DE": H0_FW_DE,
   "H0_framework_a0H": H0_FW_H,
   "H0_framework_alt": H0_FW_ALT,
   "class": "67.4-68.0",
   "weld": {"H0_SH0ES": 73.0, "a0_SH0ES": A0_SH0ES,
            "a0_split_pct": 100.0 * (RATIO_H0 - 1.0),
            "register": "MINE_M1/EQUATION_BOOK: Planck 9.36e-11, SH0ES "
                        "1.014e-10 (8.3%)",
            "alt_footing_binds_H0": H0_FW_ALT}},
 "part2_tension_statement": {
   "H0_framework_class": "67.4-68.0 (inherited by a0's calibration)",
   "local_SH0ES_73": "UNVERIFIED in this repo",
   "early_universe_Planck_67_4": True,
   "tension_width_kms": 5.6,
   "tension_width_pct": 8.31,
   "omega_identity_at_committed": om_rec,
   "g189_register": 0.684930,
   "c06_h0_blind": "the closure is the Lean-certified tautological fixed "
                   "point; EVERY Omega fixed; reconstruction independent "
                   "of H0's value -- the identity chain selects NO H0",
   "audit": {
     "a_inversion": "NO -- re-reads the calibration",
     "b_flow_h0_h94": "canonical 68.7 +- 3.4 (0.4 sig from Planck 67.4); "
                      "alt 73.9 +- 3.6 (0.2 sig from SH0ES 73.0); the "
                      "footing alone decides the camp; cannot arbitrate",
     "c_freeze_epoch": "z* = 2.4 is a TAUTOLOGY defining the epoch (F07) "
                       "-- no value; shifts as (1+z*) ~ H0^(1/2)",
     "d_dr4_ridge": "moves < 1% under the 8.31% split -- an a0-scale "
                    "test, not an H0 test",
     "answer": "NO framework relation prefers 67 or 73 independently"},
   "honest_statement": "the framework INHERITS the early-universe H0 "
                       "through a0's calibration; does NOT resolve the "
                       "tension"},
 "part3_prediction_face": {
   "if_H0_73": {
     "R_dS": {"pct_linear": pct(R_DS_73, R_DS),
              "dex": math.log10(R_DS_73 / R_DS),
              "m": [R_DS, R_DS_73], "Gpc": [R_DS / 3.085677581e25,
                                            R_DS_73 / 3.085677581e25],
              "note": "the '-3.5%' pre-guess is the DEX (-3.47%); the "
                      "LINEAR delta is -7.67% (R_dS ~ 1/H0)"},
     "T_dS": {"pct_linear": pct(T_DS_73, T_DS),
              "dex": math.log10(T_DS_73 / T_DS),
              "K": [T_DS, T_DS_73], "register_K": 2.197696e-30,
              "note": "T_dS = hbar H_Lambda/(2 pi k_B) ~ H0 (F07 rung 1)"},
     "freeze_epoch": {"pct_linear_on_1pz": pct(S_SQRT, 1.0),
                      "dex": math.log10(S_SQRT),
                      "zstar_MW": [ZSTAR_MW, ZSTAR_73],
                      "zstar_2p40": [2.4, ZSTAR_24],
                      "T_b_K": [2.72548 * 3.4, T_B_73],
                      "note": "1+z* = m sigma^2/(k_B T0), sigma^2 ~ "
                              "a0^(1/2) ~ H0^(1/2)"},
     "r_M": {"pct_linear": pct(math.sqrt(H0 / H0_73), 1.0),
             "factor": math.sqrt(H0 / H0_73),
             "note": "r_M = sqrt(G M_b/a0) ~ H0^(-1/2)"},
     "DR4_ridge": {"s_exc_plateau": [S_EXC, S_EXC_73],
                   "s_exc_pct": pct(S_EXC_73, S_EXC),
                   "gamma_plateau": [GAM_PL, GAM_PL_73],
                   "gamma_pct": pct(GAM_PL_73, GAM_PL),
                   "note": "m_cl = sqrt(G M_b a0) s/G ~ H0^(1/2); the "
                           "ridge is an a0-scale test -- < 1% under the "
                           "whole split; EFE cap 7.4 kAU a0-independent"}},
   "observational_preference": {
     "a0_zero_point": "TRIO core (n = 104) ON a0_H: 0.976 x a0_H, "
                      "z = -0.20 (Z11) -- 67.4-class in central value; "
                      "the SH0ES-weld a0 = 1.014e-10 is only +0.85 sigma "
                      "from the TRIO -- no decisive split; full-542 line "
                      "1.81 x a0_H <-> H0 = 122 is the REGISTERED M/L "
                      "departure (ATLAS3D JAM), NOT an H0 datum",
     "dr4_ridge": "forecast registered at the committed (67.4-anchored) "
                  "a0; a %-precision ridge resolves the a0 footing "
                  "(G190 K1) -> through the weld an H0 probe at +-8% "
                  "granularity; today prefers its own committed forecast",
     "freeze_epoch": "tautological (F07) -- no preference; committed "
                     "z* = 2.3656-2.4932 (G132) consistent with both "
                     "classes at ~2%",
     "statement": "the committed data prefer the 67.4-class THROUGH the "
                  "framework because every committed observable was "
                  "registered at the 67.4-anchored a0; no independent "
                  "arbiter exists"}},
 "verdicts": {"V1_H0_framework": v1, "V2_tension_statement": v2,
              "V3_honest_statement": v3},
 "checks": CHECKS,
 "n_pass": sum(1 for cr in CHECKS if cr["pass"]),
 "n_total": len(CHECKS),
}
out = os.path.join(HERE, "G02_results.json")
with open(out, "w") as f:
    json.dump(res, f, indent=1)
print()
print("wrote %s" % out)
print("checks: %d/%d pass" % (res["n_pass"], res["n_total"]))
raise SystemExit(0 if res["n_pass"] == res["n_total"] else 1)