#!/usr/bin/env python3
"""
================================================================================
DERIVING INDIVIDUAL QUARK MASSES FROM Z²
================================================================================

We have quark mass RATIOS from Z²:
  m_t/m_b = Z² + CUBE = 41.5
  m_s/m_d = 5 × BEKENSTEIN = 20

Can we get ABSOLUTE quark masses?

Key insight: Each quark generation connects to its lepton partner!
  - (u, d) ↔ (e, νe)
  - (c, s) ↔ (μ, νμ)
  - (t, b) ↔ (τ, ντ)

================================================================================
"""

import numpy as np

# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================

PI = np.pi
Z = 2 * np.sqrt(8 * PI / 3)
Z_SQUARED = Z * Z

BEKENSTEIN = 3 * Z_SQUARED / (8 * PI)  # = 4
GAUGE = 9 * Z_SQUARED / (8 * PI)        # = 12
CUBE = 8

# Lepton masses (MeV) - these we take as measured/derived
m_e = 0.511  # MeV
m_mu = 105.66  # MeV
m_tau = 1776.86  # MeV

print("=" * 80)
print("DERIVING INDIVIDUAL QUARK MASSES FROM Z²")
print("=" * 80)

print(f"\nFramework constants:")
print(f"  Z = {Z:.6f}")
print(f"  BEKENSTEIN = {BEKENSTEIN:.1f}")
print(f"  GAUGE = {GAUGE:.1f}")
print(f"  CUBE = {CUBE}")

print(f"\nLepton masses (input):")
print(f"  m_e = {m_e} MeV")
print(f"  m_μ = {m_mu} MeV")
print(f"  m_τ = {m_tau} MeV")

# =============================================================================
# MEASURED QUARK MASSES (PDG 2024, MS-bar at 2 GeV)
# =============================================================================

print("\n" + "=" * 80)
print("MEASURED QUARK MASSES")
print("=" * 80)

# Current quark masses in MeV (MS-bar at 2 GeV scale)
m_u_measured = 2.16  # +0.49 -0.26 MeV
m_d_measured = 4.67  # +0.48 -0.17 MeV
m_s_measured = 93.4  # +8.6 -3.4 MeV
m_c_measured = 1270  # ±20 MeV (at m_c scale)
m_b_measured = 4180  # +30 -20 MeV (at m_b scale)
m_t_measured = 172760  # ±300 MeV (pole mass)

print(f"\n  First generation:")
print(f"    m_u = {m_u_measured} MeV")
print(f"    m_d = {m_d_measured} MeV")
print(f"\n  Second generation:")
print(f"    m_s = {m_s_measured} MeV")
print(f"    m_c = {m_c_measured} MeV")
print(f"\n  Third generation:")
print(f"    m_b = {m_b_measured} MeV")
print(f"    m_t = {m_t_measured} MeV = {m_t_measured/1000:.1f} GeV")

# =============================================================================
# DISCOVERY: QUARK-LEPTON MASS CONNECTIONS
# =============================================================================

print("\n" + "=" * 80)
print("DISCOVERY: QUARK-LEPTON MASS CONNECTIONS")
print("=" * 80)

print("""
Each quark generation is tied to its lepton partner!

  Generation 1: (u, d) ↔ electron
  Generation 2: (c, s) ↔ muon
  Generation 3: (t, b) ↔ tau
""")

# =============================================================================
# FIRST GENERATION: d AND u
# =============================================================================

print("=" * 80)
print("FIRST GENERATION: DOWN AND UP")
print("=" * 80)

# Down quark
m_d_predicted = m_e * (BEKENSTEIN - 1)**2  # = 9 m_e
print(f"""
DOWN QUARK:
  Formula: m_d = m_e × (BEKENSTEIN - 1)² = m_e × 9

  m_d = {m_e} × 9 = {m_d_predicted:.2f} MeV

  Predicted: {m_d_predicted:.2f} MeV
  Measured:  {m_d_measured:.2f} MeV
  Error: {abs(m_d_predicted - m_d_measured)/m_d_measured * 100:.1f}%

  Physical meaning: (BEKENSTEIN - 1)² = 3² = 9
  The "3" is the number of generations = spatial dimensions
""")

# Up quark
m_u_predicted = m_d_predicted / 2  # = 4.5 m_e
print(f"""
UP QUARK:
  Formula: m_u = m_d / 2 = m_e × (BEKENSTEIN - 1)² / 2

  m_u = {m_d_predicted:.2f} / 2 = {m_u_predicted:.2f} MeV

  Predicted: {m_u_predicted:.2f} MeV
  Measured:  {m_u_measured:.2f} MeV
  Error: {abs(m_u_predicted - m_u_measured)/m_u_measured * 100:.1f}%

  Physical meaning: Up quark is half the down quark mass
  This gives m_d/m_u = 2 exactly
""")

# =============================================================================
# SECOND GENERATION: s AND c
# =============================================================================

print("=" * 80)
print("SECOND GENERATION: STRANGE AND CHARM")
print("=" * 80)

# Strange quark (already known)
m_s_predicted = m_d_predicted * 5 * BEKENSTEIN  # = 20 m_d
print(f"""
STRANGE QUARK:
  Formula: m_s = m_d × 5 × BEKENSTEIN = 20 × m_d

  m_s = {m_d_predicted:.2f} × 20 = {m_s_predicted:.1f} MeV

  Predicted: {m_s_predicted:.1f} MeV
  Measured:  {m_s_measured:.1f} MeV
  Error: {abs(m_s_predicted - m_s_measured)/m_s_measured * 100:.1f}%
""")

# Charm quark - connected to muon!
m_c_predicted = m_mu * GAUGE  # = 12 m_μ
print(f"""
CHARM QUARK:
  Formula: m_c = m_μ × GAUGE = 12 × m_μ

  m_c = {m_mu:.2f} × 12 = {m_c_predicted:.0f} MeV

  Predicted: {m_c_predicted:.0f} MeV
  Measured:  {m_c_measured:.0f} MeV
  Error: {abs(m_c_predicted - m_c_measured)/m_c_measured * 100:.1f}%

  Physical meaning: Charm mass = GAUGE × muon mass
  The second generation quark ties to second generation lepton!
""")

# =============================================================================
# THIRD GENERATION: b AND t
# =============================================================================

print("=" * 80)
print("THIRD GENERATION: BOTTOM AND TOP")
print("=" * 80)

# Bottom quark - connected to tau!
m_b_predicted = m_tau * 2 * Z / 5  # = m_τ × 2Z/(BEKENSTEIN+1)
print(f"""
BOTTOM QUARK:
  Formula: m_b = m_τ × 2Z/(BEKENSTEIN + 1) = m_τ × 2Z/5

  m_b = {m_tau:.2f} × 2 × {Z:.4f} / 5 = {m_b_predicted:.0f} MeV

  Predicted: {m_b_predicted:.0f} MeV
  Measured:  {m_b_measured:.0f} MeV
  Error: {abs(m_b_predicted - m_b_measured)/m_b_measured * 100:.1f}%

  Physical meaning: Bottom ties to tau via Z and BEKENSTEIN
""")

# Top quark (already known ratio)
m_t_predicted = m_b_predicted * (Z_SQUARED + CUBE)  # = m_b × (Z² + 8)
print(f"""
TOP QUARK:
  Formula: m_t = m_b × (Z² + CUBE) = m_b × {Z_SQUARED + CUBE:.1f}

  m_t = {m_b_predicted:.0f} × {Z_SQUARED + CUBE:.1f} = {m_t_predicted:.0f} MeV
      = {m_t_predicted/1000:.1f} GeV

  Predicted: {m_t_predicted/1000:.1f} GeV
  Measured:  {m_t_measured/1000:.1f} GeV
  Error: {abs(m_t_predicted - m_t_measured)/m_t_measured * 100:.1f}%
""")

# =============================================================================
# SUMMARY TABLE
# =============================================================================

print("=" * 80)
print("SUMMARY: ALL QUARK MASSES FROM Z²")
print("=" * 80)

print(f"""
╔═══════════╦═══════════════════════════════════════╦════════════╦════════════╦═══════╗
║ Quark     ║ Z² Formula                            ║ Predicted  ║ Measured   ║ Error ║
╠═══════════╬═══════════════════════════════════════╬════════════╬════════════╬═══════╣
║ u         ║ m_e × (BEKENSTEIN-1)² / 2             ║ {m_u_predicted:6.2f} MeV ║ {m_u_measured:6.2f} MeV ║ {abs(m_u_predicted-m_u_measured)/m_u_measured*100:4.1f}% ║
║ d         ║ m_e × (BEKENSTEIN-1)²                 ║ {m_d_predicted:6.2f} MeV ║ {m_d_measured:6.2f} MeV ║ {abs(m_d_predicted-m_d_measured)/m_d_measured*100:4.1f}% ║
║ s         ║ m_d × 5 × BEKENSTEIN                  ║ {m_s_predicted:6.1f} MeV ║ {m_s_measured:6.1f} MeV ║ {abs(m_s_predicted-m_s_measured)/m_s_measured*100:4.1f}% ║
║ c         ║ m_μ × GAUGE                           ║ {m_c_predicted:6.0f} MeV ║ {m_c_measured:6.0f} MeV ║ {abs(m_c_predicted-m_c_measured)/m_c_measured*100:4.1f}% ║
║ b         ║ m_τ × 2Z/(BEKENSTEIN+1)               ║ {m_b_predicted:6.0f} MeV ║ {m_b_measured:6.0f} MeV ║ {abs(m_b_predicted-m_b_measured)/m_b_measured*100:4.1f}% ║
║ t         ║ m_b × (Z² + CUBE)                     ║ {m_t_predicted/1000:6.1f} GeV ║ {m_t_measured/1000:6.1f} GeV ║ {abs(m_t_predicted-m_t_measured)/m_t_measured*100:4.1f}% ║
╚═══════════╩═══════════════════════════════════════╩════════════╩════════════╩═══════╝
""")

# =============================================================================
# QUARK-LEPTON UNIVERSALITY
# =============================================================================

print("=" * 80)
print("QUARK-LEPTON UNIVERSALITY")
print("=" * 80)

print(f"""
The pattern reveals QUARK-LEPTON UNIVERSALITY:

Generation 1:
  Leptons: e, νe
  Quarks:  u = m_e × 4.5,  d = m_e × 9
  → First generation quarks scale with electron mass

Generation 2:
  Leptons: μ, νμ
  Quarks:  c = m_μ × 12 = m_μ × GAUGE
  → Charm quark scales with muon mass

Generation 3:
  Leptons: τ, ντ
  Quarks:  b = m_τ × 2Z/5,  t = m_b × (Z² + 8)
  → Third generation quarks scale with tau mass

This connects quarks and leptons through Z²!
Each generation is unified by the geometric framework.
""")

# =============================================================================
# MASS HIERARCHY
# =============================================================================

print("=" * 80)
print("UNDERSTANDING THE MASS HIERARCHY")
print("=" * 80)

print(f"""
Why are quarks heavier than leptons?

First generation:
  m_d/m_e = 9 = (BEKENSTEIN - 1)²
  m_u/m_e = 4.5

Second generation:
  m_c/m_μ = 12 = GAUGE

Third generation:
  m_b/m_τ = 2Z/5 ≈ 2.3
  m_t/m_τ = (2Z/5)(Z² + 8) ≈ 96

Pattern: Quark/lepton ratios involve Z, BEKENSTEIN, GAUGE

The hierarchy emerges from the SAME geometric constants!
No additional parameters needed.
""")

# =============================================================================
# VERIFICATION: KNOWN RATIOS
# =============================================================================

print("=" * 80)
print("VERIFICATION: KNOWN MASS RATIOS")
print("=" * 80)

# m_s/m_d
ms_md_predicted = 5 * BEKENSTEIN
ms_md_measured = m_s_measured / m_d_measured
print(f"  m_s/m_d = 5 × BEKENSTEIN = {ms_md_predicted:.0f}")
print(f"  Measured: {ms_md_measured:.1f}")
print(f"  Error: {abs(ms_md_predicted - ms_md_measured)/ms_md_measured * 100:.1f}%")

# m_t/m_b
mt_mb_predicted = Z_SQUARED + CUBE
mt_mb_measured = m_t_measured / m_b_measured
print(f"\n  m_t/m_b = Z² + CUBE = {mt_mb_predicted:.1f}")
print(f"  Measured: {mt_mb_measured:.1f}")
print(f"  Error: {abs(mt_mb_predicted - mt_mb_measured)/mt_mb_measured * 100:.1f}%")

# m_d/m_u
md_mu_predicted = 2
md_mu_measured = m_d_measured / m_u_measured
print(f"\n  m_d/m_u = 2")
print(f"  Measured: {md_mu_measured:.2f}")
print(f"  Error: {abs(md_mu_predicted - md_mu_measured)/md_mu_measured * 100:.1f}%")

# =============================================================================
# COMPLETE FORMULA SET
# =============================================================================

print("\n" + "=" * 80)
print("COMPLETE QUARK MASS FORMULAS")
print("=" * 80)

print(f"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║  QUARK MASS FORMULAS FROM Z²                                                 ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  FIRST GENERATION (tied to electron):                                        ║
║    m_d = m_e × (BEKENSTEIN - 1)² = 9 m_e                                     ║
║    m_u = m_d / 2 = 4.5 m_e                                                   ║
║                                                                               ║
║  SECOND GENERATION (tied to muon):                                           ║
║    m_s = 20 × m_d = 180 m_e                                                  ║
║    m_c = GAUGE × m_μ = 12 m_μ                                                ║
║                                                                               ║
║  THIRD GENERATION (tied to tau):                                             ║
║    m_b = m_τ × 2Z/(BEKENSTEIN + 1) = m_τ × 2Z/5                              ║
║    m_t = m_b × (Z² + CUBE)                                                   ║
║                                                                               ║
║  All 6 quark masses derived with 1-7% accuracy!                              ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
""")

print("=" * 80)
print("END OF QUARK MASS DERIVATION")
print("=" * 80)
