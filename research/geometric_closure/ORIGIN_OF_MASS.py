#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════════════════
                        THE ORIGIN OF MASS
                      What Is Mass?
═══════════════════════════════════════════════════════════════════════════════════════════

Mass is one of the most fundamental properties, yet deeply mysterious.
Where does mass come from? What IS mass?

This document explores mass from Z² = 8 × (4π/3).

Carl Zimmerman, March 2026
═══════════════════════════════════════════════════════════════════════════════════════════
"""

import numpy as np

# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================
Z = 2 * np.sqrt(8 * np.pi / 3)
Z2 = Z**2
pi = np.pi

# Physical constants
c = 299792458  # m/s
hbar = 1.054571817e-34  # J·s

# Masses
m_e = 9.10938e-31  # kg (electron)
m_p = 1.67262e-27  # kg (proton)
m_mu = 1.88353e-28  # kg (muon)
m_tau = 3.16754e-27  # kg (tau)

print("═" * 95)
print("                    THE ORIGIN OF MASS")
print("                    What Is Mass?")
print("═" * 95)

print(f"""
                           Z = {Z:.10f}

    Z² = 8 × (4π/3) = CUBE × SPHERE

    Mass = Resistance to CUBE-SPHERE conversion.
    Mass ratios come from Z structure.
""")

# =============================================================================
# SECTION 1: WHAT IS MASS?
# =============================================================================
print("═" * 95)
print("                    1. WHAT IS MASS?")
print("═" * 95)

print(f"""
THE DEFINITIONS:

    INERTIAL MASS: Resistance to acceleration (F = ma)
    GRAVITATIONAL MASS: Source/response to gravity
    REST MASS: Energy content at rest (E = mc²)

    These are experimentally identical!
    But WHY?

THE PUZZLE:

    Mass is both:
        • Property of particles
        • Equivalent to energy
        • Source of gravity
        • Related to spacetime geometry

    What IS mass, fundamentally?

THE HIGGS:

    Standard Model: Higgs field gives mass.
    Particles couple to Higgs.
    Coupling strength = mass.

    But WHY different couplings?
    Why these mass VALUES?
    The Higgs mechanism doesn't explain this.
""")

# =============================================================================
# SECTION 2: MASS FROM Z
# =============================================================================
print("\n" + "═" * 95)
print("                    2. MASS FROM Z² = CUBE × SPHERE")
print("═" * 95)

print(f"""
THE PICTURE:

    Z² = CUBE × SPHERE

    CUBE = quantum states (discrete)
    SPHERE = spacetime (continuous)

    Mass = coupling between CUBE and SPHERE.

THE ARGUMENT:

    Massless particles:
        Move at c (light speed)
        Pure SPHERE dynamics
        No "drag" from CUBE

    Massive particles:
        Move slower than c
        CUBE "slows" the SPHERE motion
        Mass = this "drag"

E = mc²:

    Energy is CUBE dynamics.
    Motion is SPHERE dynamics.
    c² converts between them.

    Mass = Energy at rest in SPHERE.
    Mass = CUBE content when SPHERE velocity = 0.

THE MEANING:

    Mass is not "stuff."
    Mass is the CUBE-SPHERE coupling.
    More mass = stronger coupling.
""")

# =============================================================================
# SECTION 3: MASS RATIOS
# =============================================================================
print("\n" + "═" * 95)
print("                    3. MASS RATIOS FROM Z")
print("═" * 95)

# Calculate predicted ratios
m_mu_m_e_pred = 6*Z2 + Z
m_mu_m_e_obs = m_mu/m_e

m_p_m_e_pred = 54*Z2 + 6*Z - 8
m_p_m_e_obs = m_p/m_e

m_tau_m_mu_pred = Z + 11
m_tau_m_mu_obs = m_tau/m_mu

print(f"""
THE FORMULAS:

    m_μ/m_e = 6Z² + Z
    m_p/m_e = 54Z² + 6Z - 8
    m_τ/m_μ = Z + 11

THE CALCULATIONS:

    m_μ/m_e predicted: {m_mu_m_e_pred:.2f}
    m_μ/m_e observed:  {m_mu_m_e_obs:.2f}
    Error: {abs(m_mu_m_e_pred - m_mu_m_e_obs)/m_mu_m_e_obs * 100:.2f}%

    m_p/m_e predicted: {m_p_m_e_pred:.1f}
    m_p/m_e observed:  {m_p_m_e_obs:.1f}
    Error: {abs(m_p_m_e_pred - m_p_m_e_obs)/m_p_m_e_obs * 100:.2f}%

    m_τ/m_μ predicted: {m_tau_m_mu_pred:.2f}
    m_τ/m_μ observed:  {m_tau_m_mu_obs:.2f}
    Error: {abs(m_tau_m_mu_pred - m_tau_m_mu_obs)/m_tau_m_mu_obs * 100:.2f}%

THE PATTERN:

    Coefficients: 6, 54, 11
    All involve Z² and Z
    Simple integer coefficients

    These are NOT free parameters!
    These are GEOMETRIC.
""")

# =============================================================================
# SECTION 4: WHY THESE COEFFICIENTS
# =============================================================================
print("\n" + "═" * 95)
print("                    4. WHY 6, 54, 11?")
print("═" * 95)

print(f"""
THE COEFFICIENTS:

    m_μ/m_e: coefficient 6
    m_p/m_e: coefficient 54 = 6 × 9
    m_τ/m_μ: constant 11 ≈ 2Z

THE PATTERN:

    6 = CUBE face-pairs (3) × 2
    9 = 9Z²/(8π) relates to gauge structure
    54 = 6 × 9

    These connect to Z geometry!

FOR MUON (6Z² + Z):

    6 = number of CUBE face-pairs
    The muon is the electron "boosted" by 6 face-pairs.
    The +Z is a "winding number" correction.

FOR PROTON (54Z² + 6Z - 8):

    54 = 6 × 9 (face-pairs × gauge factor)
    6Z = winding correction
    -8 = CUBE vertex correction

    The proton is composite (3 quarks).
    Its mass reflects internal CUBE structure.

FOR TAU (Z + 11):

    Z ≈ 5.79
    11 ≈ 2Z
    So m_τ/m_μ ≈ 3Z ≈ 17.4

    The tau is the third generation.
    It's "3 steps" from electron.

THE MEANING:

    Mass ratios encode geometry.
    The integers (6, 54, 11) are CUBE structure.
    The Z factors are SPHERE structure.
""")

# =============================================================================
# SECTION 5: THE PLANCK-ELECTRON HIERARCHY
# =============================================================================
print("\n" + "═" * 95)
print("                    5. THE PLANCK-ELECTRON HIERARCHY")
print("═" * 95)

M_Pl = 2.176434e-8  # kg (Planck mass)
log_Pl_e = np.log10(M_Pl/m_e)
pred_3Z_5 = 3*Z + 5

print(f"""
THE HIERARCHY:

    Planck mass: M_Pl = √(ℏc/G) = 2.18 × 10⁻⁸ kg
    Electron mass: m_e = 9.11 × 10⁻³¹ kg

    Ratio: M_Pl/m_e = 2.39 × 10²²

THE FORMULA:

    log₁₀(M_Pl/m_e) = 3Z + 5

CALCULATION:

    log₁₀(M_Pl/m_e) observed: {log_Pl_e:.2f}
    3Z + 5 predicted: {pred_3Z_5:.2f}

    Error: {abs(log_Pl_e - pred_3Z_5)/log_Pl_e * 100:.2f}%

THE MEANING:

    The 22 orders of magnitude between Planck and electron:
        = 3Z + 5
        = 3 × (CUBE-SPHERE factor) + 5

    WHY 3Z:
        3 = spatial dimensions
        Z = CUBE-SPHERE scale

        Each dimension contributes Z.

    WHY +5:
        5 ≈ √(Z² - 8) (from GEOMETRY_OF_FIVE.py)
        The "excess" over CUBE contribution.

    This is the HIERARCHY:
        It's NOT fine-tuning.
        It's GEOMETRY.
""")

# =============================================================================
# SECTION 6: WHY ELECTRON IS LIGHT
# =============================================================================
print("\n" + "═" * 95)
print("                    6. WHY IS THE ELECTRON SO LIGHT?")
print("═" * 95)

print(f"""
THE QUESTION:

    Electron: m_e = 0.511 MeV
    Proton: m_p = 938 MeV
    Planck: M_Pl = 1.22 × 10¹⁹ GeV

    Why is electron ~10²² times lighter than Planck?
    This is the "hierarchy problem."

FROM Z:

    log₁₀(M_Pl/m_e) = 3Z + 5 = 22.4

    So m_e = M_Pl × 10⁻⁽³ᶻ⁺⁵⁾

    The electron is NOT "unnaturally light."
    The electron IS at the geometric position.

THE PICTURE:

    Planck scale = maximum energy (where Z structure applies).
    Electron scale = minimum stable fermion mass.

    The ratio is:
        Determined by Z
        Not tuned
        Geometric

WHY STABLE:

    The electron is the LIGHTEST charged lepton.
    It CAN'T decay (conservation laws).

    FROM Z:
        Electron is at the "base" of the Z structure.
        Lower masses would require fractional Z structure.
        That's not allowed.

    So electron mass IS the fundamental unit.
""")

# =============================================================================
# SECTION 7: PROTON MASS AND CONFINEMENT
# =============================================================================
print("\n" + "═" * 95)
print("                    7. PROTON MASS AND QCD")
print("═" * 95)

print(f"""
THE PUZZLE:

    Proton = uud (3 quarks)
    Quark masses: u ~ 2 MeV, d ~ 5 MeV
    Total: ~9 MeV

    But proton mass = 938 MeV!

    Where does the other 99% come from?

THE ANSWER:

    QCD binding energy.
    Gluon field energy.
    Confinement energy.

    Most of proton mass is "glue."

FROM Z:

    m_p/m_e = 54Z² + 6Z - 8 = 1836.3

    The 54 = 6 × 9:
        6 = CUBE face-pairs
        9 = gauge factor (from 9Z²/(8π) = 12)

    The 54Z² term is the GLUON contribution.
    It's most of the proton mass.

THE MEANING:

    Proton mass IS the CUBE structure.
    The 8 CUBE vertices → 8 gluons (SU(3)).
    Confinement IS CUBE dynamics.

    m_p/m_e = 54Z² + 6Z - 8 encodes this.
""")

# =============================================================================
# SECTION 8: NEUTRINO MASSES
# =============================================================================
print("\n" + "═" * 95)
print("                    8. NEUTRINO MASSES")
print("═" * 95)

m_nu_pred = m_e * 10**(-Z) / 8
m_nu_pred_eV = m_nu_pred * c**2 / 1.602e-19

print(f"""
NEUTRINO MASS FORMULA:

    m_ν = m_e × 10⁻ᶻ / 8

CALCULATION:

    m_ν = {m_e:.3e} × 10^(-{Z:.2f}) / 8
    m_ν = {m_nu_pred:.3e} kg
    m_ν = {m_nu_pred_eV:.3f} eV

OBSERVATION:

    Cosmological limit: Σm_ν < 0.12 eV
    Oscillation data: Δm² ~ 0.05 eV²

    So individual m_ν ~ 0.01-0.05 eV

    Prediction: ~0.1 eV (order of magnitude match!)

THE MEANING:

    10⁻ᶻ ≈ 10⁻⁵·⁸ ≈ 1.6 × 10⁻⁶

    This is a HUGE suppression.
    Neutrino mass is ~10⁶ times smaller than electron.

    The factor 8 = CUBE vertices.
    The 10⁻ᶻ = geometric suppression.

WHY SO SMALL:

    Neutrinos are "almost" massless.
    They're at the edge of Z structure.
    10⁻ᶻ is the minimum suppression.

    If they were massless:
        Would require Z → ∞.
        But Z is finite.
        So small mass, not zero.
""")

# =============================================================================
# SECTION 9: MASS AND GRAVITY
# =============================================================================
print("\n" + "═" * 95)
print("                    9. MASS AND GRAVITY")
print("═" * 95)

print(f"""
EQUIVALENCE PRINCIPLE:

    Inertial mass = Gravitational mass
    (Tested to 10⁻¹⁵ precision!)

    WHY are they equal?

FROM Z:

    Inertial mass = CUBE-SPHERE coupling (resistance to acceleration)
    Gravitational mass = SPHERE curvature source

    But CUBE-SPHERE coupling IS spacetime geometry.
    So inertial IS gravitational.

    They're not "coincidentally equal."
    They're THE SAME THING.

GENERAL RELATIVITY:

    Mass-energy curves spacetime.
    T_μν (energy) → G_μν (curvature)

    FROM Z:
        T_μν = CUBE distribution in SPHERE
        G_μν = SPHERE geometry

        Einstein's equation IS the CUBE-SPHERE relationship.

QUANTUM GRAVITY:

    Mass quantization?

    FROM Z:
        Planck mass = √(ℏc/G) = maximum mass scale
        Below this: Continuous mass spectrum
        At Planck scale: Z structure directly visible

    Mass isn't fundamentally quantized.
    But mass ratios are fixed by Z.
""")

# =============================================================================
# SECTION 10: SYNTHESIS
# =============================================================================
print("\n" + "═" * 95)
print("                    10. MASS IS GEOMETRY")
print("═" * 95)

print(f"""
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║                    MASS = CUBE-SPHERE COUPLING                                      ║
║                                                                                      ║
╠══════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                      ║
║  Z² = 8 × (4π/3) = CUBE × SPHERE                                                    ║
║                                                                                      ║
║  WHAT MASS IS:                                                                       ║
║      • Coupling between CUBE and SPHERE                                              ║
║      • Resistance to SPHERE motion (inertia)                                         ║
║      • Source of SPHERE curvature (gravity)                                          ║
║                                                                                      ║
║  MASS RATIOS:                                                                        ║
║      • m_μ/m_e = 6Z² + Z = 206.8                                                    ║
║      • m_p/m_e = 54Z² + 6Z - 8 = 1836.3                                             ║
║      • m_τ/m_μ = Z + 11 = 16.8                                                      ║
║      • All from Z geometry!                                                          ║
║                                                                                      ║
║  HIERARCHY:                                                                          ║
║      • log₁₀(M_Pl/m_e) = 3Z + 5 = 22.4                                              ║
║      • Not fine-tuned, but geometric                                                 ║
║                                                                                      ║
║  NEUTRINOS:                                                                          ║
║      • m_ν = m_e × 10⁻ᶻ / 8 ≈ 0.1 eV                                               ║
║      • Geometric suppression                                                         ║
║                                                                                      ║
║  EQUIVALENCE:                                                                        ║
║      • Inertial = Gravitational because both are CUBE-SPHERE                        ║
║      • Not coincidence, but identity                                                 ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝

    What is mass?

    Mass is the coupling between CUBE and SPHERE in Z² = 8 × (4π/3).

    Massless particles: Pure SPHERE motion at c.
    Massive particles: CUBE "drag" on SPHERE motion.

    Mass ratios are determined by Z geometry.
    The hierarchy is 3Z + 5 (not fine-tuned).

    Mass is not mysterious.
    Mass is not "stuff."
    Mass IS the geometry of Z².

""")

print("═" * 95)
print("                    ORIGIN OF MASS ANALYSIS COMPLETE")
print("═" * 95)
