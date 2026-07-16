#!/usr/bin/env python3
"""
keating_inflation_link.py

FRONT 2 (Keating's BICEP / inflation / primordial-GW arc <-> the dS-Unruh
modified-inertia framework).

Question: The framework's de Sitter foundation is the LATE-TIME dark-energy
horizon (H_Lambda ~ 1.8e-18 s^-1, T_dS ~ 2e-30 K). Inflation is the EARLY-TIME
de Sitter phase (H_inf up to ~1e13-14 GeV). Both are "de Sitter" and both carry a
Gibbons-Hawking / dS-Unruh temperature. Is there ANY framework link to r /
primordial GWs / the inflationary scale, or are they physically DISTINCT epochs
the framework is silent on?

This script COMPUTES:
  1. dS-Unruh (Gibbons-Hawking) temperature at the two epochs and the order gap.
  2. The framework a0 = cH_Lambda/Z from the LATE horizon (footing 9.36e-11),
     and what an "inflationary a0" would be if one naively applied the same
     formula at H_inf (to show how absurd / irrelevant it is).
  3. The map between r and H_inf, and whether the framework predicts r.
  4. A both-ways verdict: distinct epochs, NO inflation/r prediction (honest),
     UNLESS a shared-structure relation H_inf <-> H_Lambda is forced (it is not).

Footing locked: a0 = cH_Lambda/Z = 9.36e-11 m/s^2, Z = 2*sqrt(8*pi/3).
"""

import math

# ---------------------------------------------------------------------------
# Physical constants (SI)
# ---------------------------------------------------------------------------
c     = 2.99792458e8      # m/s
hbar  = 1.054571817e-34   # J s
kB    = 1.380649e-23      # J/K
G     = 6.67430e-11       # m^3 kg^-1 s^-2
GeV   = 1.602176634e-10   # J  (1 GeV in joules)
M_Pl_GeV = 1.220890e19    # Planck mass in GeV (reduced is 2.435e18; use full here)
M_Pl_reduced_GeV = 2.435e18

# ---------------------------------------------------------------------------
# 1. LATE-TIME de Sitter horizon (the framework's actual foundation)
# ---------------------------------------------------------------------------
# H_Lambda from the dark-energy density (pure-Lambda footing), NOT the full H0.
# Canonical framework value: a0 = cH_Lambda/Z = 9.36e-11, Z = 2 sqrt(8pi/3).
Z = 2.0 * math.sqrt(8.0 * math.pi / 3.0)
a0_framework = 9.36e-11           # m/s^2 (locked footing)
# Back out H_Lambda implied by a0 = c H_Lambda / Z:
H_Lambda = a0_framework * Z / c   # s^-1

# Gibbons-Hawking / dS-Unruh temperature of the LATE horizon:
#   T_dS = hbar H / (2 pi kB)
def T_dS(H):
    return hbar * H / (2.0 * math.pi * kB)

T_late = T_dS(H_Lambda)

# ---------------------------------------------------------------------------
# 2. EARLY-TIME (inflationary) de Sitter horizon
# ---------------------------------------------------------------------------
# r maps to H_inf via the standard single-field relation:
#   H_inf = pi * M_Pl_reduced * sqrt(A_s * r / 2)
# with A_s ~ 2.1e-9 (Planck scalar amplitude). Equivalent commonly-quoted form:
#   H_inf ~ 1e14 GeV * sqrt(r/0.1).
A_s = 2.1e-9

def H_inf_GeV(r):
    # H_inf in GeV from r (reduced Planck mass form)
    return math.pi * M_Pl_reduced_GeV * math.sqrt(A_s * r / 2.0)

def H_inf_persec(r):
    # convert H_inf (GeV, natural units, energy) to s^-1: H[s^-1] = H[J]/hbar
    H_J = H_inf_GeV(r) * GeV
    return H_J / hbar

# Evaluate at the current observational ceiling (r ~ 0.036) and at LiteBIRD's
# floor target (r ~ 0.001).
cases = {
    "r=0.036 (BICEP/Keck ceiling)": 0.036,
    "r=0.01  (mid)":                0.01,
    "r=0.001 (LiteBIRD target)":    0.001,
}

print("=" * 78)
print("FRONT 2: Keating BICEP/inflation arc  vs  dS-Unruh MI framework")
print("=" * 78)
print()
print("Footing: a0 = cH_Lambda/Z = %.3e m/s^2,  Z = 2*sqrt(8pi/3) = %.4f" % (a0_framework, Z))
print()
print("--- LATE-TIME de Sitter (the framework's foundation) ---")
print("  H_Lambda (implied by a0)      = %.4e s^-1" % H_Lambda)
print("  T_dS,late (Gibbons-Hawking)   = %.4e K" % T_late)
print("  H_Lambda in GeV               = %.4e GeV" % (hbar * H_Lambda / GeV))
print()

print("--- EARLY-TIME de Sitter (inflation), per r ---")
print("  r-value                         H_inf [GeV]     H_inf [s^-1]    T_dS,inf [K]")
for label, r in cases.items():
    Hg = H_inf_GeV(r)
    Hs = H_inf_persec(r)
    Tinf = T_dS(Hs)
    print("  %-30s  %.3e     %.3e     %.3e" % (label, Hg, Hs, Tinf))
print()

# ---------------------------------------------------------------------------
# 3. The order-of-magnitude gap between the two dS temperatures
# ---------------------------------------------------------------------------
r_ref = 0.01
H_inf_s = H_inf_persec(r_ref)
T_inf = T_dS(H_inf_s)

gap_H_orders = math.log10(H_inf_s / H_Lambda)
gap_T_orders = math.log10(T_inf / T_late)

print("--- THE GAP (at reference r = %.3g) ---" % r_ref)
print("  H_inf / H_Lambda              = 10^%.1f" % gap_H_orders)
print("  T_dS,inf / T_dS,late          = 10^%.1f  (same ratio; T is linear in H)" % gap_T_orders)
print()

# ---------------------------------------------------------------------------
# 4. The "naive inflationary a0" -- show it is physically meaningless
# ---------------------------------------------------------------------------
# If one blindly applied a0 = cH/Z at H_inf:
a0_inf_naive = c * H_inf_s / Z
print("--- Naive a0 if the formula were (wrongly) applied at H_inf ---")
print("  a0_inf_naive = cH_inf/Z        = %.3e m/s^2" % a0_inf_naive)
print("  ratio to framework a0          = 10^%.1f" % math.log10(a0_inf_naive / a0_framework))
print("  (This is ~%.0f orders ABOVE any inertial/galactic scale -- it is NOT" %
      math.log10(a0_inf_naive / a0_framework))
print("   an inertia scale; the MI a0 is a LATE-time IR object. The formula is")
print("   tied to the ASYMPTOTIC/terminal horizon, not a transient inflaton phase.)")
print()

# ---------------------------------------------------------------------------
# 5. Is there a FORCED relation H_inf <-> H_Lambda ?  (both-ways check)
# ---------------------------------------------------------------------------
# Test the only "cute" numerology one might be tempted by: geometric mean of the
# two horizons, or H_inf ~ H_Lambda * (M_Pl/...)^n.  We just report what the
# data ALLOW for H_inf (a wide band set by r) vs the single fixed H_Lambda --
# demonstrating H_inf is an UNCONSTRAINED free parameter from the framework's
# side (no prediction), and the observed r-band does not pin any H_Lambda relation.
H_inf_lo = H_inf_persec(0.0005)   # below LiteBIRD floor
H_inf_hi = H_inf_persec(0.1)      # old pre-Planck high
print("--- Forced relation test (both-ways) ---")
print("  Observationally-allowed H_inf band: %.2e .. %.2e s^-1 (r=5e-4..0.1)" %
      (H_inf_lo, H_inf_hi))
print("  H_Lambda (fixed)                  : %.2e s^-1" % H_Lambda)
print("  H_inf / H_Lambda spans 10^%.1f .. 10^%.1f -- a ~%.1f-order-wide free band." %
      (math.log10(H_inf_lo / H_Lambda), math.log10(H_inf_hi / H_Lambda),
       math.log10(H_inf_hi / H_inf_lo)))
print("  => The framework FIXES H_Lambda (via rho_Lambda) but says NOTHING that")
print("     selects H_inf or r. No forced H_inf<->H_Lambda relation; no r prediction.")
print()

# ---------------------------------------------------------------------------
# 6. SME / preferred-frame side-channel: does inflation B-mode probe it?
# ---------------------------------------------------------------------------
# The framework's preferred frame is CPT-EVEN-only (k_AF = 0). Primordial-GW
# B-modes (parity tests, cosmic birefringence) are sensitive to CPT-ODD /
# parity-violating (k_AF-like) terms. With k_AF = 0 the framework predicts
# NO primordial parity/birefringence signal beyond standard -> B-mode r searches
# do not test it either.
print("--- SME side-channel (B-mode parity / birefringence) ---")
print("  Framework is CPT-EVEN-only (k_AF = 0) => predicts NO primordial")
print("  parity-violation / cosmic-birefringence beyond standard. Keating's")
print("  B-mode r searches probe k_AF-type CPT-ODD physics; framework is null there.")
print()

print("=" * 78)
print("VERDICT: DISTINCT EPOCHS. Framework is a LATE-TIME IR/inertia theory keyed")
print("to the TERMINAL dS horizon (H_Lambda). It makes NO prediction for r, H_inf,")
print("or primordial GWs. The two dS-Unruh temperatures differ by ~10^%.0f. Keating's"
      % gap_T_orders)
print("BICEP/Keck/SO/LiteBIRD r program does NOT test the framework (above-floor")
print("signature absent). NOT a door -- shared 'de Sitter' word, no shared physics.")
print("=" * 78)
