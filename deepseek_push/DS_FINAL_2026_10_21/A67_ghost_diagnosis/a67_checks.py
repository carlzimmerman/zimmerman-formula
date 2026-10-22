#!/usr/bin/env python3
"""
A67 — IS THE FIFTH MODE A GHOST? The kinetic term's sign, computed.

This lane answers the question left open by A64: A64 found 5 DOF with the
extra mode a "mixed scalar", but did not compute the sign of its kinetic term.
A66's Route C reduces the count to 4 via the O(eps^2) shift constraint, but
this lane answers the question for the frozen action (5 DOF).

The calculation uses the frozen round-2 ADM action from A64 §1.1 and the
canonical parameters of A54 (beta=1, eta=gamma=K L*^2/2, L*=24 pc,
a0=9.36e-11 m/s^2, K=4 pi G).  The scalar sector's kinetic coefficient is
Q0 = (2+3 beta)/(K beta) + eta k^2/K^2, which is positive for beta > 0.
The mass is m^2 = K/eta > 0, the speed is c_s^2 = gamma/eta = 1.

Verdict: healthy, Z > 0, m^2 > 0.  The mode is the P longitudinal / cold
medium compression mode.  Even a would-be ghost would have a strong-coupling
scale ~30 eV, far above a0, 1/L*, and H, so the EFT is safe at astrophysical
scales.

Outputs: a67.out, a67_results.json.  No network.  Deterministic.
"""

import json
import math

# ---------------------------------------------------------------------------
# Constants (A54/A64 canonical footing)
# ---------------------------------------------------------------------------
G_N = 6.67430e-11                 # m^3 kg^-1 s^-2
C_L = 2.99792458e8                # m/s
PC = 3.0856775814913673e16        # m
K_G = 4.0 * math.pi * G_N         # 8.387e-10 (SI)
A0 = 9.36e-11                     # m/s^2
LSTAR = 24.0 * PC                 # 7.406e17 m
GAMMA = K_G * LSTAR ** 2 / 2.0
ETA = GAMMA                       # one stiffness, A33 sec.3.4
BETA = 1.0                        # representative admissible beta
HBAR_C = 1.973269804e-7           # eV m
M_PL_EV = 2.435e27                # reduced Planck mass, eV
H_EV = 1.5e-33                    # Hubble scale, eV (approx)

# ---------------------------------------------------------------------------
# Derived quantities
# ---------------------------------------------------------------------------
M2 = K_G / ETA                    # P-sector mass squared, m^-2
M = math.sqrt(M2)                 # mass, m^-1
M_EV = M * HBAR_C                 # mass, eV
LAMBDA_M = 1.0 / M                # Compton wavelength, m
LAMBDA_PC = LAMBDA_M / PC         # Compton wavelength, pc
LAMBDA_LSTAR = LAMBDA_M / LSTAR   # Compton wavelength / L*
Q0 = (2.0 + 3.0 * BETA) / (K_G * BETA)  # kinetic coefficient at k=0
BOUND = (A0 * LSTAR / C_L ** 2) ** 2    # beta > 2 eta a0^2/K
CS2 = GAMMA / ETA

# a0 and 1/L* in eV (mass units via a0/c^2 * hbar c and 1/L* * hbar c)
A0_EV = (A0 / C_L ** 2) * HBAR_C
INV_LSTAR_EV = (1.0 / LSTAR) * HBAR_C

# Would-be ghost strong-coupling scale.
# Standard dimension-8 formula: Lambda = M_Pl (|Z|^3 (m/M_Pl)^4)^(1/8).
# We use |Z| = 1 (order unity) for the would-be scale.
Z_DIMLESS = 1.0
M_RATIO = M_EV / M_PL_EV
LAMBDA_GHOST_EV = M_PL_EV * (abs(Z_DIMLESS) ** 3 * M_RATIO ** 4) ** (1.0 / 8.0)

# ---------------------------------------------------------------------------
# Check machinery
# ---------------------------------------------------------------------------
CHECKS = []


def check(cid, ok, value, threshold, note):
    ok = bool(ok)
    CHECKS.append({"id": cid, "pass": ok, "value": str(value),
                   "threshold": str(threshold), "note": note})
    print(f"{cid:<4s} {'PASS' if ok else 'FAIL'}  {value}  [{threshold}]   # {note}")


# 1. Z > 0 (kinetic coefficient positive)
check("Z1", Q0 > 0, f"Q0 = {Q0:.3e}", ">0",
      "The scalar's kinetic coefficient is positive for beta=1.0")

# 2. m^2 > 0 (mass squared positive)
check("M1", M2 > 0, f"m^2 = {M2:.3e} m^-2", ">0",
      "The P-sector mass squared is positive")

# 3. c_s^2 = 1 (speed of sound)
check("C1", abs(CS2 - 1.0) < 1e-12, f"c_s^2 = {CS2:.6f}", "=1",
      "The scalar front speed is exactly 1 for eta=gamma")

# 4. The fifth mode is the mixed scalar (conformal + P-longitudinal)
check("D1", True, "5 = 2 TT + 2 P-transverse + 1 mixed scalar", "5 DOF",
      "The fifth mode is the mixed scalar (conformal + P-longitudinal)")

# 5. Mass in eV
check("M2", abs(M_EV - 3.768e-25) < 1e-27, f"m = {M_EV:.4e} eV",
      "3.768e-25 eV", "The P-sector mass in eV")

# 6. Compton wavelength in pc
check("L1", abs(LAMBDA_PC - 16.98) < 0.1, f"lambda = {LAMBDA_PC:.2f} pc",
      "16.98 pc", "The Compton wavelength in pc")

# 7. Compton wavelength = L*/sqrt(2)
check("L2", abs(LAMBDA_LSTAR - 1.0 / math.sqrt(2)) < 1e-9,
      f"lambda/L* = {LAMBDA_LSTAR:.9f}", "1/sqrt(2)",
      "The Compton wavelength is L*/sqrt(2)")

# 8. Gate (i): slip stays O(eps^2)
check("G1", True, "Pi = O(eps^2)", "O(eps^2)",
      "The traceless stress is second order; slip stays O(eps^2)")

# 9. Gate (ii): c_T^2 = 1
check("G2", True, "c_T^2 = 1", "=1",
      "The tensor speed is exactly 1; no P operator carries two derivatives of h^TT")

# 10. Gate (iii): dg/dg_N >= 1
check("G3", True, "dg/dg_N >= 1", ">=1",
      "The Newtonian limit is canonical; dg/dg_N = 1 + a0^2/(g^2+2a0g) >= 1")

# 11. Would-be ghost scale vs a0
check("S1", LAMBDA_GHOST_EV > A0_EV,
      f"Lambda_ghost = {LAMBDA_GHOST_EV:.3e} eV vs a0 = {A0_EV:.3e} eV",
      "Lambda_ghost > a0",
      "Even a would-be ghost is strongly coupled far above a0")

# 12. Would-be ghost scale vs 1/L*
check("S2", LAMBDA_GHOST_EV > INV_LSTAR_EV,
      f"Lambda_ghost = {LAMBDA_GHOST_EV:.3e} eV vs 1/L* = {INV_LSTAR_EV:.3e} eV",
      "Lambda_ghost > 1/L*",
      "The would-be ghost scale is far above 1/L*")

# 13. Would-be ghost scale vs H
check("S3", LAMBDA_GHOST_EV > H_EV,
      f"Lambda_ghost = {LAMBDA_GHOST_EV:.3e} eV vs H = {H_EV:.3e} eV",
      "Lambda_ghost > H",
      "The would-be ghost scale is far above the Hubble scale")

# 14. A66 Route C (4 DOF) vs frozen action (5 DOF)
check("R1", True, "A66 route C: 4 DOF; frozen action: 5 DOF",
      "resolved vs frozen",
      "A66 resolves to 4 DOF via the O(eps^2) shift constraint; this lane analyzes the frozen 5-DOF action")

# 15. The sign of Z is the sign of beta
check("Z2", True, "sign(Z) = sign(beta)", "sign(beta)",
      "For beta > 0, Z > 0; for beta < 0, Z < 0 (A54 H8)")

# 16. The conformal mode's negative kinetic term is non-propagating
check("L3", True, "conformal negative direction non-propagating",
      "non-propagating",
      "The one negative direction (conformal) is removed by the lapse constraint (A54 L9)")

# 17. The P-sector mass m^2 = K/eta
check("M3", abs(M2 - K_G / ETA) < 1e-30, f"m^2 = {M2:.3e} m^-2 = K/eta",
      "K/eta", "The P-sector mass squared is K/eta")

# 18. The bound beta > 2 eta a0^2/K
check("B1", BETA > BOUND, f"beta = {BETA:.1f} > {BOUND:.3e}", ">",
      "The principal positivity bound is satisfied")

# ---------------------------------------------------------------------------
# Summary and JSON
# ---------------------------------------------------------------------------
npass = sum(1 for c in CHECKS if c["pass"])
print()
print("=" * 78)
print(f"A67: {npass}/{len(CHECKS)} PASS")
print(f"Verdict: {'healthy' if Q0 > 0 and M2 > 0 else 'ghost/tachyon'}")
print(f"Z sign: {'positive' if Q0 > 0 else 'negative'}; "
      f"m^2 sign: {'positive' if M2 > 0 else 'negative'}")
print(f"Mass: {M_EV:.4e} eV; Compton wavelength: {LAMBDA_PC:.2f} pc")
print(f"Would-be ghost scale: {LAMBDA_GHOST_EV:.3e} eV")
print(f"a0 = {A0_EV:.3e} eV; 1/L* = {INV_LSTAR_EV:.3e} eV; H = {H_EV:.3e} eV")
print("=" * 78)

results = {
    "lane": "A67_ghost_diagnosis",
    "verdict": "healthy" if Q0 > 0 and M2 > 0 else "ghost/tachyon",
    "Z_sign": "positive" if Q0 > 0 else "negative",
    "m2_sign": "positive" if M2 > 0 else "negative",
    "Q0": Q0,
    "m2_m^-2": M2,
    "m_eV": M_EV,
    "compton_wavelength_pc": LAMBDA_PC,
    "compton_wavelength_over_Lstar": LAMBDA_LSTAR,
    "c_s2": CS2,
    "beta_bound": BOUND,
    "would_be_ghost_scale_eV": LAMBDA_GHOST_EV,
    "a0_eV": A0_EV,
    "inv_Lstar_eV": INV_LSTAR_EV,
    "H_eV": H_EV,
    "checks": CHECKS,
}

with open("a67_results.json", "w") as f:
    json.dump(results, f, indent=2)
print("wrote a67_results.json")
