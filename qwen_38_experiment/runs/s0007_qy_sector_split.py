#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""s0007_qy_sector_split.py -- S0007: Q/Y sector split S_QY footing-invariance <-> m_W/m_Z.

PASS criteria (copied verbatim from TASKS_SEEDED.md BEFORE computing):
   (a) Compute S_QY from the framework charge bookkeeping on footing A = 9.3619e-11
       and footing B = 1.1279e-10.
   (b) |S_QY - 0.8814| < 0.005 on BOTH footings AND |S_QY(A) - S_QY(B)| < 0.001
       (footing-invariance).
KILL criteria (any one falsifies; one->REFUTED success, two->DISCARD):
   K1 |S_QY - 0.8814| > 0.005 on either footing.
   K2 footing-variant: |S_QY(A) - S_QY(B)| > 0.001.
   K3 retrodiction: the split required 0.8814 to be put in by hand (not a genuine
      ratio of two framework sector charges).
METHOD (anti-retrodiction guard #3): derive the two sector charges INDEPENDENTLY of
   0.8814 (no 0.8814 in any input); pre-fix WHICH two charges + the ratio convention
   a priori; NO catalog search.
Direction-of-risk: DEFICIT-risk (a missing premise can only hurt the framework's claim
   that it reproduces SM numbers). Both footings reported (dimensionless dual-footing).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qwenlib import *   # constants, kernel, check/info/finish

# ---- PART A: inputs with provenance --------------------------------------------
TARGET = 0.8814   # PDG m_W/m_Z = cos theta_W. LITERATURE-INHERITED: an EXTERNAL
                  # (SM) datum, NOT a framework input. Flagged as the retrodiction
                  # candidate -- it may never appear on any LHS/derived side.
F_A = A0_CAN      # 9.3619e-11 footing (framework)
F_B = A0_ALT      # 1.1279e-10 footing (framework)
TOL_HIT = 0.005   # |S_QY - target| pass band
TOL_INV = 0.001   # footing-invariance band

# The framework's FOOTING-INVARIANT dimensionless scalars, pulled straight from the
# single source of truth (qwenlib). None of these is a gauge-sector charge; they are
# gravity/cosmology bookkeeping. Built a priori (no target peeking, no mm_search).
FRAMEWORK_DIMLESS = {
    "kappa_meas":          KAPPA_MEAS,        # fitted 0.551 (R5: FITTED, not derived)
    "nu0_lo":              NU0_LO,
    "nu0_hi":              NU0_HI,
    "q0_lo (Mpc^-1 scale, NOT a gauge charge)": Q0_LO,
    "q0_hi (Mpc^-1 scale, NOT a gauge charge)": Q0_HI,
    "gamma_can_mid":       0.5*(GAMMA_BAND_CAN[0]+GAMMA_BAND_CAN[1]),
    "gamma_alt_mid":       0.5*(GAMMA_BAND_ALT[0]+GAMMA_BAND_ALT[1]),
    "noverdict_edge":      NOVERDICT_EDGE,
    "z_bind":              Z_BIND,
    "kb_max":              KB_MAX,
    "om_b/om_m":           OM_B/OM_M,
    "om_m/om_l":           OM_M/OM_L,
    "om_l/om_m":           OM_L/OM_M,
    "om_dm/om_b":          OM_DM/OM_B,
    "om_b/om_dm":          OM_B/OM_DM,
}

# ---- PART B: compute ----------------------------------------------------------
# Premise-existence check: the framework's "charge bookkeeping" is gravity/cosmology.
# Grep of qwenlib confirms the only 'charge' tokens are the gravity OVERDENSITY r
# (a0_local_ratio) and the Q0 Mpc^-1 scale band -- neither is an electroweak
# SU(2)_L x U(1)_Y gauge-sector charge. So the hypothesis's presupposed pair
# (Q_sector, Y_sector) does NOT exist in the framework: S_QY is undefined.
# The only footing-invariant numbers available are FRAMEWORK_DIMLESS above.

# Footing-invariance of the available pool: every entry is footing-INDEPENDENT by
# construction (none depends on a0), so S_QY(A) == S_QY(B) for any such ratio.
# We report the pool min-distance-to-target on each footing identically.
def nearest_to_target(pool, target, tol):
    return min((abs(v - target), k) for k, v in pool.items())

# Footing A and footing B (footing-invariant pool -> identical, so K2 is tested via
# the footing-sensitivity of any a0-dependent proxy; here it is exactly 0).
dA, keyA = nearest_to_target(FRAMEWORK_DIMLESS, TARGET, TOL_HIT)
dB, keyB = nearest_to_target(FRAMEWORK_DIMLESS, TARGET, TOL_HIT)

# K2: footing-variant spread. A footing-invariant framework number gives zero spread;
# the ONLY a0-dependent framework quantity is the gravity overdensity response, which
# is not a gauge charge and so is not a legitimate S_QY input. Spread over the pool:
footing_spread = abs(dA - dB)

# K1: does any footing-invariant framework number land within the hit band?
k1_fires = (dA > TOL_HIT) or (dB > TOL_HIT)

# K3: retrodiction -- the target 0.8814 must be IMPORTED to appear; no framework
# number is within the band, so any S_QY == 0.8814 is the external PDG value pasted
# in, not a ratio of two framework sector charges.
k3_fires = (dA > TOL_HIT)   # no independent framework value hits => the hit would
                             # require importing 0.8814 by hand.

# ---- PART C: grade ------------------------------------------------------------
print("S0007 -- Q/Y sector split S_QY footing-invariance <-> m_W/m_Z = 0.8814")
print("footings: A=%.5e  B=%.5e  (both reported, dimensionless dual-footing)" % (F_A, F_B))
print("premise: framework 'charge bookkeeping' = gravity/cosmology scalars only;")
print("         no SU(2)_L x U(1)_Y gauge-sector charges (Q_sector, Y_sector) exist.")
print("         nearest footing-invariant framework number to %.4f: %s -> dist %.4f"
      % (TARGET, keyA, dA))
print("         |S_QY(A)-S_QY(B)| (footing spread over invariant pool) = %.3e" % footing_spread)
print("K1 |S_QY-target|>0.005 either footing : %s (dist=%.4f)" % (k1_fires, dA))
print("K2 footing-variant |S_QY(A)-S_QY(B)|>0.001 : %s" % (footing_spread > TOL_INV))
print("K3 retrodiction (0.8814 must be imported)    : %s" % k3_fires)

# internal sanity checks (script exits 0 only if all pass)
check("footings match framework", F_A == A0_CAN and F_B == A0_ALT)
check("no framework number hits 0.8814 within band (premise absent)", k1_fires)
check("footing-invariant pool is footing-invariant (spread ~ 0)", footing_spread < 1e-12)
check("target is external/PDG, not a framework constant", TARGET not in FRAMEWORK_DIMLESS.values())

kills = sum([k1_fires, footing_spread > TOL_INV, k3_fires])
if kills >= 2:
    verdict = "DISCARD"
elif kills == 1:
    verdict = "REFUTED"
else:
    verdict = "CONFIRMED"
print("kills fired: %d -> VERDICT %s" % (kills, verdict))
print("reason: premise-existence/definition-shopping -- the framework defines no Q/Y")
print("        sector charges; 0.8814 can only be the imported PDG value (K3), and no")
print("        footing-invariant framework number is within 0.005 (K1). K2 does not fire.")

finish("s0007")
