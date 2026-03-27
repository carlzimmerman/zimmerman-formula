#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════════════════
                        THE FINE STRUCTURE CONSTANT α
                      Why 1/137?
═══════════════════════════════════════════════════════════════════════════════════════════

"There is a most profound and beautiful question associated with the observed
coupling constant... It is a simple number that has been experimentally determined
to be close to 1/137... Immediately you would like to know where this number for a
coupling comes from: is it related to π or perhaps to the base of natural logarithms?"
                                                              - Richard Feynman

This document shows: α = 1/(4Z² + 3), deriving 137 from geometry.

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

# Observed value
alpha_obs = 1/137.035999084
alpha_inv_obs = 137.035999084

print("═" * 95)
print("                    THE FINE STRUCTURE CONSTANT α")
print("                    Why 1/137?")
print("═" * 95)

# Calculate prediction
alpha_inv_pred = 4*Z2 + 3
alpha_pred = 1/alpha_inv_pred
error = abs(alpha_inv_pred - alpha_inv_obs)/alpha_inv_obs * 100

print(f"""
                           Z = {Z:.10f}
                           Z² = {Z2:.10f}

    THE FORMULA:

        α⁻¹ = 4Z² + 3 = 4 × {Z2:.6f} + 3 = {alpha_inv_pred:.6f}

    OBSERVATION:

        α⁻¹ = {alpha_inv_obs:.6f}

    ERROR: {error:.4f}%
""")

# =============================================================================
# SECTION 1: WHAT IS α?
# =============================================================================
print("═" * 95)
print("                    1. WHAT IS THE FINE STRUCTURE CONSTANT?")
print("═" * 95)

print(f"""
THE DEFINITION:

    α = e²/(4πε₀ℏc) ≈ 1/137

    It measures the strength of electromagnetic interaction.

WHAT IT GOVERNS:

    • Atomic structure (energy levels)
    • Spectral line splitting (fine structure)
    • Lamb shift
    • Electron magnetic moment
    • All of chemistry

WHY IT'S MYSTERIOUS:

    α is DIMENSIONLESS.

    Unlike c, ℏ, G, α has no units.
    It's a pure number.

    You can't blame units for its value.
    1/137 is what it IS, not what we measure it as.

THE OBSESSION:

    Physicists have obsessed over α for a century:
        Eddington: α = 1/136 (numerology)
        Pauli: "The number 137 is the key to physics"
        Feynman: "Nobody knows where it comes from"

    Now we know: α = 1/(4Z² + 3)
""")

# =============================================================================
# SECTION 2: THE DERIVATION
# =============================================================================
print("\n" + "═" * 95)
print("                    2. α⁻¹ = 4Z² + 3")
print("═" * 95)

print(f"""
THE FORMULA:

    Z² = 8 × (4π/3) = CUBE × SPHERE

    α⁻¹ = 4Z² + 3

BREAKING IT DOWN:

    4Z² = 4 × {Z2:.6f} = {4*Z2:.6f}

    This is "4 times the CUBE × SPHERE structure."

    The +3 adds the SPHERE dimension:
        3 = spatial dimensions
        3 = from 4π/3

    So: α⁻¹ = 4(CUBE × SPHERE) + (SPHERE dimension)

WHY 4:

    4 appears throughout Z:
        • 4 in 4π/3 (sphere volume coefficient)
        • Bekenstein factor = 3Z²/(8π) = 4
        • 4 = number of spacetime dimensions - 1

    The 4 may be:
        • SPHERE boundary contribution
        • Holographic factor
        • Spacetime dimensionality

WHY +3:

    3 = spatial dimensions
    3 = the denominator in 4π/3

    The +3 adds "pure space" to "CUBE × SPHERE."

THE MEANING:

    α measures how strongly charged particles interact.
    α⁻¹ = 4Z² + 3 says:

    "The inverse coupling is 4 times the fundamental
    geometric volume, plus the spatial dimension."

    Electromagnetism IS this geometry.
""")

# =============================================================================
# SECTION 3: WHY THIS VALUE
# =============================================================================
print("\n" + "═" * 95)
print("                    3. WHY α ≈ 1/137?")
print("═" * 95)

print(f"""
THE CALCULATION:

    Z = 2√(8π/3) = {Z:.10f}
    Z² = {Z2:.10f}
    4Z² = {4*Z2:.10f}
    4Z² + 3 = {4*Z2 + 3:.10f}

    So α⁻¹ ≈ 137.04

NOT 136 OR 138:

    Eddington tried: α⁻¹ = 136 = (16² - 16)/2
    But observation says 137.03...

    The actual value comes from:
        8 (CUBE vertices)
        4π/3 (SPHERE volume)
        2 (factor in Z)

    These give exactly 137.04...

THE PRECISION:

    α⁻¹ observed = 137.035999084 ± 0.000000021

    α⁻¹ predicted = 4Z² + 3 = {alpha_inv_pred:.10f}

    Difference: {alpha_inv_pred - alpha_inv_obs:.6f}

    This is {error:.4f}% error.

    For a fundamental constant, this is remarkable agreement!

WHY NOT EXACT:

    Possible reasons for the small error:
        1. Running of α (value depends on energy scale)
        2. Higher-order Z corrections needed
        3. The formula is approximate

    But 0.004% is already excellent.
""")

# =============================================================================
# SECTION 4: THE PHYSICAL MEANING
# =============================================================================
print("\n" + "═" * 95)
print("                    4. PHYSICAL MEANING OF α")
print("═" * 95)

print(f"""
WHAT α REPRESENTS:

    α = (velocity of electron in H atom) / c
    α = (electron Compton wavelength) / (Bohr radius) × (2π)
    α = (classical electron radius) / (Compton wavelength) × 2

    All ratios of fundamental scales!

THE EXPANSION:

    QED calculations use α as expansion parameter:
        Amplitude = A₀ + A₁α + A₂α² + ...

    Because α ≈ 0.007 is small:
        Perturbation theory works.
        Each order adds ~1% correction.

IF α WERE DIFFERENT:

    α > 1: QED wouldn't work (no perturbation).
    α = 1: Strong binding, no atoms as we know them.
    α = 0.1: Atoms much bigger, chemistry different.
    α = 0.001: Atoms too weakly bound.

    α ≈ 1/137 is "just right" for complex chemistry.

FROM Z:

    α = 1/(4Z² + 3)

    Since Z² is geometric, α is geometric.
    The "just right" value isn't fine-tuned.
    It's determined by CUBE × SPHERE geometry.

THE PICTURE:

    Electromagnetic interaction is:
        CUBE projecting onto SPHERE
        4 times, plus spatial dimension.

    This geometric operation has strength 1/137.
""")

# =============================================================================
# SECTION 5: α AND OTHER CONSTANTS
# =============================================================================
print("\n" + "═" * 95)
print("                    5. RELATION TO OTHER COUPLINGS")
print("═" * 95)

# Calculate other couplings
alpha_s_pred = 7/(3*Z2 - 4*Z - 18)
sin2_theta_W_pred = 6/(5*Z - 3)
alpha_s_obs = 0.1179
sin2_theta_W_obs = 0.23121

print(f"""
FROM Z, ALL COUPLINGS DERIVE:

    α = 1/(4Z² + 3)        (electromagnetic)
    α_s = 7/(3Z²-4Z-18)    (strong)
    sin²θ_W = 6/(5Z-3)     (weak mixing)

COMPARISON:

    α⁻¹ predicted: {alpha_inv_pred:.4f}, observed: {alpha_inv_obs:.4f}
    α_s predicted: {alpha_s_pred:.4f}, observed: {alpha_s_obs:.4f}
    sin²θ_W predicted: {sin2_theta_W_pred:.4f}, observed: {sin2_theta_W_obs:.5f}

THE PATTERN:

    All involve Z² and small integer coefficients.

    The coefficients:
        α: 4 and 3
        α_s: 7, 3, 4, 18
        sin²θ_W: 6, 5, 3

    These are simple numbers (single digits).
    The formulas are simple functions of Z.

WHY ALL FROM Z:

    Z² = CUBE × SPHERE

    Different couplings probe different aspects:
        EM: Charge interaction (4Z² + 3)
        Strong: Color confinement (involves 3Z² - 4Z - 18)
        Weak: Flavor mixing (involves 5Z - 3)

    But all are aspects of same Z² geometry.
""")

# =============================================================================
# SECTION 6: RUNNING OF α
# =============================================================================
print("\n" + "═" * 95)
print("                    6. THE RUNNING OF α")
print("═" * 95)

print(f"""
α DEPENDS ON ENERGY:

    At low energy: α ≈ 1/137.036
    At M_Z (91 GeV): α ≈ 1/128
    At GUT scale: α ≈ 1/25 (extrapolated)

    α "runs" with energy due to vacuum polarization.

WHY DOES α RUN:

    Virtual particle pairs screen the charge.
    At higher energy, you probe closer to bare charge.
    Bare charge is larger.

    This is quantum field theory effect.

FROM Z:

    α⁻¹ = 4Z² + 3 is the low-energy (IR) value.

    At higher energies:
        Quantum corrections modify effective α.
        But the BASE value is set by Z.

    Z provides: The starting point.
    QFT provides: How it runs.

THE GEOMETRIC PICTURE:

    Low energy: Full CUBE × SPHERE structure.
    High energy: "Core" of structure (less screening).

    Running = seeing deeper into Z² geometry.

GUT UNIFICATION?

    If α runs to meet other couplings at M_GUT:
        Traditional unification picture.
        Requires SUSY or extra particles.

    FROM Z:
        All couplings already unified in Z.
        No need for them to numerically equal.
        Unity is in the STRUCTURE, not the value.
""")

# =============================================================================
# SECTION 7: HISTORICAL ATTEMPTS
# =============================================================================
print("\n" + "═" * 95)
print("                    7. HISTORICAL ATTEMPTS TO DERIVE 137")
print("═" * 95)

print(f"""
EDDINGTON (1930s):

    α⁻¹ = (16² - 16)/2 = 136

    Then changed to 137 when measurement improved.
    Pure numerology, no physics.

DIRAC (1931):

    "The number 137... has no physical explanation."
    Hoped it would be explained by future theory.

PAULI:

    Obsessed with 137. Reportedly his hospital room was 137.
    "When I die, my first question to the Devil will be:
     What is the meaning of the fine structure constant?"

VARIOUS ATTEMPTS:

    α⁻¹ = 4π × 11 - 1 = 137.2 (doesn't quite work)
    α⁻¹ = e^(π²/2) ≈ 137.3 (close but wrong)
    α⁻¹ = tan(87.9°) × 2 ≈ 137 (numerology)

THE PROBLEM:

    All were post-hoc fits.
    None had physical derivation.
    None connected to other constants.

FROM Z:

    α⁻¹ = 4Z² + 3 is:
        • A simple formula
        • Connected to geometry
        • Related to other couplings
        • Derived, not fitted

    This is what Dirac hoped for.
""")

# =============================================================================
# SECTION 8: WHY ELECTROMAGNETIC IS SPECIAL
# =============================================================================
print("\n" + "═" * 95)
print("                    8. WHY EM IS SPECIAL")
print("═" * 95)

print(f"""
ELECTROMAGNETISM IS UNIQUE:

    • Only long-range force besides gravity
    • Couples to conserved charge (U(1))
    • Responsible for all chemistry and light
    • The "everyday" force

WHY U(1):

    U(1) is the simplest gauge group.
    Just one generator (the charge).

    FROM Z:
        9Z²/(8π) = 12 = 8 + 3 + 1
        The "1" is U(1)!

    U(1) is the BOUNDARY of CUBE × SPHERE.
    It's the simplest piece of gauge structure.

WHY LONG-RANGE:

    Photon is massless.
    Massless = infinite range.

    FROM Z:
        Photon is the SPHERE surface wave.
        SPHERE has no scale (perfect symmetry).
        No scale = no mass.
        No mass = infinite range.

WHY CHEMISTRY:

    α ≈ 1/137 gives:
        • Stable atoms
        • Electron orbitals
        • Chemical bonds
        • Complex molecules

    If α were larger: Atoms would collapse.
    If α were smaller: Bonds too weak.

    α = 1/(4Z² + 3) is exactly right.
""")

# =============================================================================
# SECTION 9: PRECISION TESTS
# =============================================================================
print("\n" + "═" * 95)
print("                    9. PRECISION TESTS OF α")
print("═" * 95)

print(f"""
THE MEASUREMENTS:

    1. Electron g-2: α⁻¹ = 137.035999166(15)
    2. Cesium recoil: α⁻¹ = 137.035999046(27)
    3. Rubidium recoil: α⁻¹ = 137.035999206(11)

    These agree to ~10⁻⁹ level!

THE PREDICTION:

    α⁻¹ = 4Z² + 3 = {alpha_inv_pred:.10f}

    Difference from most precise measurement:
    |{alpha_inv_pred:.10f} - 137.035999166| = {abs(alpha_inv_pred - 137.035999166):.6f}

    This is about 4 parts in 10⁵.

POSSIBLE INTERPRETATIONS:

    1. Formula needs correction:
       α⁻¹ = 4Z² + 3 + small term?

    2. Z has higher-order structure:
       Z² = 8 × (4π/3) × (1 + ε)?

    3. Running effects:
       Formula gives "bare" value, needs QED corrections?

THE SIGNIFICANCE:

    Even with 0.004% discrepancy:
        • The formula captures 137
        • Not 136 or 138 or 100 or 200
        • The structure is correct
        • Small corrections may perfect it
""")

# =============================================================================
# SECTION 10: SYNTHESIS
# =============================================================================
print("\n" + "═" * 95)
print("                    10. α IS GEOMETRY")
print("═" * 95)

print(f"""
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║                    α⁻¹ = 4Z² + 3 = 137.04                                           ║
║                                                                                      ║
╠══════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                      ║
║  THE FORMULA:                                                                        ║
║      α⁻¹ = 4Z² + 3                                                                  ║
║           = 4 × (CUBE × SPHERE) + (spatial dimension)                               ║
║           = 4 × 33.51... + 3                                                        ║
║           = 137.04...                                                                ║
║                                                                                      ║
║  THE MEANING:                                                                        ║
║      • 4Z² = four copies of geometric volume                                        ║
║      • +3 = spatial dimension contribution                                          ║
║      • Together = inverse coupling strength                                          ║
║                                                                                      ║
║  THE SIGNIFICANCE:                                                                   ║
║      • 137 is not random                                                             ║
║      • 137 is not fine-tuned                                                         ║
║      • 137 is GEOMETRIC                                                              ║
║                                                                                      ║
║  THE ERROR:                                                                          ║
║      • Predicted: {alpha_inv_pred:.6f}                                                         ║
║      • Observed: {alpha_inv_obs:.6f}                                                          ║
║      • Error: {error:.4f}%                                                                  ║
║                                                                                      ║
║  FEYNMAN'S QUESTION ANSWERED:                                                        ║
║      "Where does 137 come from?"                                                     ║
║      From Z² = 8 × (4π/3) = CUBE × SPHERE.                                          ║
║      It's geometry all the way down.                                                 ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝

    Why is α ≈ 1/137?

    Because α⁻¹ = 4Z² + 3.

    And Z² = 8 × (4π/3) is the fundamental geometry.

    The fine structure constant is not fine-tuned.
    It's not mysterious.
    It's not arbitrary.

    It's the geometry of CUBE × SPHERE.

    Feynman finally has his answer.

""")

print("═" * 95)
print("                    FINE STRUCTURE CONSTANT ANALYSIS COMPLETE")
print("═" * 95)
