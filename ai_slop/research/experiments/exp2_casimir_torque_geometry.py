#!/usr/bin/env python3
"""
EXPERIMENT 2: CASIMIR TORQUE IN EXTRA-DIMENSIONAL GEOMETRIES
=============================================================

Tests for signatures of compactified extra dimensions in the Casimir effect
using novel plate geometries that break 4D symmetry.

THEORETICAL BASIS:
-----------------
The Casimir effect arises from vacuum fluctuations confined between boundaries.
In 4D, the force between parallel plates is:

    F/A = -π²ℏc / (240 L⁴)

In theories with extra dimensions (like Z² framework), the Casimir energy
receives ADDITIONAL contributions from Kaluza-Klein modes:

    E_Casimir^(8D) = E_Casimir^(4D) + Σ_n E_KK(m_n, L)

The KK contributions depend on the GEOMETRY of the boundaries relative to
the extra-dimensional structure.

WHAT THIS TESTS:
---------------
1. Anisotropic Casimir forces in non-parallel geometries
2. Torque on birefringent plates (broken rotational symmetry)
3. Deviations from 1/L⁴ scaling at sub-micron separations
4. Geometry-dependent corrections consistent with T³/Z₂

Author: Carl Zimmerman
Date: April 2026
Framework: Z² = 32π/3
"""

import numpy as np
import json

# Physical constants
hbar = 1.054571817e-34  # J·s
c = 299792458           # m/s
epsilon_0 = 8.854187817e-12  # F/m

print("="*80)
print("EXPERIMENT 2: CASIMIR TORQUE IN EXTRA-DIMENSIONAL GEOMETRIES")
print("Testing for KK Mode Signatures in Vacuum Fluctuations")
print("="*80)

# =============================================================================
# SECTION 1: THEORETICAL FRAMEWORK
# =============================================================================

print("\n" + "="*80)
print("SECTION 1: THEORETICAL FRAMEWORK")
print("="*80)

theory = """
    CASIMIR EFFECT IN EXTRA DIMENSIONS:

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                         │
    │   Standard 4D Casimir Energy (parallel plates, area A, separation L):  │
    │                                                                         │
    │     E_4D = -π²ℏc A / (720 L³)                                          │
    │                                                                         │
    │   Force per unit area:                                                  │
    │                                                                         │
    │     F/A = -π²ℏc / (240 L⁴) ≈ -1.3 × 10⁻²⁷ / L⁴  [N/m²]               │
    │                                                                         │
    │   ─────────────────────────────────────────────────────────────────    │
    │                                                                         │
    │   Z² Framework Correction (8D with T³/Z₂):                             │
    │                                                                         │
    │   Additional KK modes contribute:                                       │
    │                                                                         │
    │     E_KK = Σ_n ∫ d³k ½ℏ√(k² + m_n²) × (boundary factor)               │
    │                                                                         │
    │   where m_n ~ n × M_KK ~ n × TeV are KK masses.                        │
    │                                                                         │
    │   For L >> 1/M_KK (laboratory scales):                                 │
    │                                                                         │
    │     δE/E_4D ~ (L × M_KK)⁻⁴ × f(geometry)                               │
    │                                                                         │
    │   This is TINY for L ~ 1 μm, M_KK ~ TeV:                               │
    │                                                                         │
    │     δE/E ~ (10⁻⁶ × 10⁻¹⁹/ℏc)⁻⁴ ~ 10⁻⁷⁶                               │
    │                                                                         │
    │   HOWEVER: The geometry-dependent factor f(geometry) can be            │
    │   anomalously large for ANISOTROPIC boundaries!                        │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
"""
print(theory)

# =============================================================================
# SECTION 2: THE TORQUE SIGNATURE
# =============================================================================

print("\n" + "="*80)
print("SECTION 2: THE TORQUE SIGNATURE")
print("="*80)

torque_theory = """
    CASIMIR TORQUE: A UNIQUE SIGNATURE OF ANISOTROPY

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                         │
    │   When two birefringent plates (e.g., calcite) are placed at angle θ, │
    │   the Casimir energy depends on θ:                                     │
    │                                                                         │
    │     E(θ) = E₀ + E₂ cos(2θ) + E₄ cos(4θ) + ...                         │
    │                                                                         │
    │   This produces a TORQUE:                                               │
    │                                                                         │
    │     τ = -dE/dθ = 2E₂ sin(2θ) + 4E₄ sin(4θ) + ...                      │
    │                                                                         │
    │   ─────────────────────────────────────────────────────────────────    │
    │                                                                         │
    │   4D QED PREDICTION:                                                    │
    │                                                                         │
    │     τ_4D ~ (ℏc/L⁴) × A × (n_e - n_o)² × sin(2θ)                       │
    │                                                                         │
    │   where n_e, n_o are extraordinary and ordinary refractive indices.    │
    │                                                                         │
    │   ─────────────────────────────────────────────────────────────────    │
    │                                                                         │
    │   Z² FRAMEWORK PREDICTION:                                              │
    │                                                                         │
    │   Extra dimensions break 4D rotational symmetry. The T³/Z₂ torus      │
    │   has PREFERRED DIRECTIONS. If the plates are aligned with these       │
    │   directions, the torque receives corrections:                          │
    │                                                                         │
    │     τ_8D = τ_4D × [1 + ξ(L/R₅)⁴ × g(θ, orientation)]                  │
    │                                                                         │
    │   where ξ ~ O(1) is a geometric factor and R₅ ~ 1/TeV ~ 10⁻¹⁹ m.     │
    │                                                                         │
    │   For L = 100 nm: (L/R₅)⁴ ~ (10⁻⁷/10⁻¹⁹)⁴ ~ 10⁴⁸                     │
    │                                                                         │
    │   BUT: This enhancement is cancelled by the KK mass suppression!      │
    │                                                                         │
    │   Net effect: δτ/τ ~ exp(-M_KK × L) ~ exp(-10¹⁶) ≈ 0                  │
    │                                                                         │
    │   ═══════════════════════════════════════════════════════════════════  │
    │   CONCLUSION: Direct KK signatures are undetectable.                   │
    │   We must look for INDIRECT effects on vacuum structure.               │
    │   ═══════════════════════════════════════════════════════════════════  │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
"""
print(torque_theory)

# =============================================================================
# SECTION 3: ALTERNATIVE APPROACH - DYNAMICAL CASIMIR EFFECT
# =============================================================================

print("\n" + "="*80)
print("SECTION 3: ALTERNATIVE - DYNAMICAL CASIMIR EFFECT")
print("="*80)

dce_theory = """
    THE DYNAMICAL CASIMIR EFFECT (DCE):

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                         │
    │   When a boundary moves at relativistic velocities, vacuum photons    │
    │   are CREATED from the quantum vacuum:                                  │
    │                                                                         │
    │     N_photons ~ (v/c)² × (ω × T) × (A / λ²)                           │
    │                                                                         │
    │   This was demonstrated in 2011 using SQUID-modulated boundary         │
    │   conditions (no mechanical motion required).                           │
    │                                                                         │
    │   ─────────────────────────────────────────────────────────────────    │
    │                                                                         │
    │   Z² FRAMEWORK SIGNATURE:                                               │
    │                                                                         │
    │   In 8D, the DCE should also produce KK mode excitations:              │
    │                                                                         │
    │     γ_vacuum → γ + G_KK  (photon + KK graviton)                        │
    │                                                                         │
    │   The KK graviton carries energy into the bulk, appearing as           │
    │   "missing energy" in the 4D measurement.                               │
    │                                                                         │
    │   Predicted signature:                                                  │
    │     N_observed < N_4D_predicted                                         │
    │                                                                         │
    │   Deficit: δN/N ~ (ℏω / M_KK)² ~ (10⁻⁵ eV / 10¹² eV)² ~ 10⁻³⁴        │
    │                                                                         │
    │   ═══════════════════════════════════════════════════════════════════  │
    │   STILL UNDETECTABLE with current technology.                          │
    │   ═══════════════════════════════════════════════════════════════════  │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
"""
print(dce_theory)

# =============================================================================
# SECTION 4: VIABLE EXPERIMENT - PRECISION CASIMIR GEOMETRY TESTS
# =============================================================================

print("\n" + "="*80)
print("SECTION 4: VIABLE EXPERIMENT - PRECISION GEOMETRY TESTS")
print("="*80)

viable = """
    WHAT WE CAN ACTUALLY TEST:

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                         │
    │   While direct KK signatures are suppressed by ~10⁻³⁴, we can test    │
    │   PREDICTIONS of the Z² framework that affect low-energy physics:      │
    │                                                                         │
    │   1. FINE STRUCTURE CONSTANT CONSISTENCY                                │
    │      The Casimir force depends on α. If Z² correctly predicts         │
    │      α⁻¹ = 4Z² + 3 = 137.04, then precision Casimir measurements     │
    │      should be consistent with this value (not free parameter).        │
    │                                                                         │
    │   2. GEOMETRY-DEPENDENT VACUUM ENERGY                                   │
    │      Different geometries (spheres, cylinders, gratings) have          │
    │      different Casimir energies. The Z² framework makes SPECIFIC       │
    │      predictions for ratios of these energies.                          │
    │                                                                         │
    │   3. NON-ADDITIVE CASIMIR FORCES                                        │
    │      Three-body Casimir interactions are sensitive to quantum          │
    │      field structure. Z² framework predicts specific corrections.      │
    │                                                                         │
    │   ─────────────────────────────────────────────────────────────────    │
    │                                                                         │
    │   PROPOSED EXPERIMENT: Precision Sphere-Plate Casimir Measurement      │
    │                                                                         │
    │   The sphere-plate Casimir force is:                                    │
    │                                                                         │
    │     F = -π³ℏc R / (360 L³) × [1 + f(R/L) + α-corrections]             │
    │                                                                         │
    │   We measure F vs. L and extract α from the data.                      │
    │   Compare to Z² prediction: α⁻¹ = 137.04                               │
    │                                                                         │
    │   Current best Casimir α measurement: ±0.1%                            │
    │   Z² prediction error: 0.004%                                          │
    │                                                                         │
    │   If measurement precision reaches 0.01%, we can TEST the Z²          │
    │   prediction against the standard α value.                              │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
"""
print(viable)

# =============================================================================
# SECTION 5: EXPERIMENTAL DESIGN
# =============================================================================

print("\n" + "="*80)
print("SECTION 5: EXPERIMENTAL DESIGN")
print("="*80)

# Casimir force calculation
def casimir_sphere_plate(R, L, alpha=1/137.036):
    """Casimir force between sphere (radius R) and plate (gap L)"""
    # Leading order (Proximity Force Approximation)
    F_PFA = -np.pi**3 * hbar * c * R / (360 * L**3)

    # QED corrections (order α)
    F_QED = F_PFA * (1 + 2.4 * alpha / np.pi)

    return F_QED

# Typical parameters
R_sphere = 100e-6  # 100 μm radius sphere
L_gap = np.linspace(100e-9, 1e-6, 100)  # 100 nm to 1 μm

# Calculate forces
F_casimir = np.array([casimir_sphere_plate(R_sphere, L) for L in L_gap])

print(f"""
    SPHERE-PLATE CASIMIR EXPERIMENT:

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                         │
    │   ┌─────────────────────────────────────────────────────────────────┐  │
    │   │                                                                 │  │
    │   │                    ⬤  Gold-coated sphere                       │  │
    │   │                   ╱ ╲   R = 100 μm                              │  │
    │   │                  ╱   ╲                                          │  │
    │   │                 ╱     ╲                                         │  │
    │   │                │       │                                        │  │
    │   │                │   ↕   │  L = 100 nm - 1 μm                    │  │
    │   │   ════════════════════════════════════════════════════════════ │  │
    │   │                  Gold-coated plate                              │  │
    │   │                                                                 │  │
    │   │   Measurement: Atomic Force Microscope (AFM) cantilever        │  │
    │   │   Sensitivity: ~1 pN                                           │  │
    │   │                                                                 │  │
    │   └─────────────────────────────────────────────────────────────────┘  │
    │                                                                         │
    │   At L = 100 nm, R = 100 μm:                                           │
    │     F = {casimir_sphere_plate(R_sphere, 100e-9)*1e12:.2f} pN                                                │
    │                                                                         │
    │   At L = 500 nm, R = 100 μm:                                           │
    │     F = {casimir_sphere_plate(R_sphere, 500e-9)*1e12:.2f} pN                                                │
    │                                                                         │
    │   At L = 1 μm, R = 100 μm:                                             │
    │     F = {casimir_sphere_plate(R_sphere, 1e-6)*1e12:.2f} pN                                                 │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
""")

# =============================================================================
# SECTION 6: α EXTRACTION PROTOCOL
# =============================================================================

print("="*80)
print("SECTION 6: α EXTRACTION PROTOCOL")
print("="*80)

protocol = """
    EXTRACTING α FROM CASIMIR MEASUREMENTS:

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                         │
    │   1. MEASURE F(L) for L = 100 nm to 1 μm (>50 data points)            │
    │                                                                         │
    │   2. FIT to theoretical model:                                          │
    │                                                                         │
    │      F(L) = -π³ℏcR/(360L³) × [1 + 2.4α/π + f(R/L,T) + δ_rough]       │
    │                                                                         │
    │      Free parameters:                                                   │
    │        • α (fine structure constant)                                   │
    │        • R_eff (effective sphere radius, ~known)                       │
    │        • δ_rough (surface roughness correction)                        │
    │                                                                         │
    │   3. EXTRACT α from best fit                                           │
    │                                                                         │
    │   4. COMPARE to predictions:                                            │
    │                                                                         │
    │      Standard Model:  α⁻¹ = 137.035999...                              │
    │      Z² Framework:    α⁻¹ = 4Z² + 3 = 137.041                          │
    │      Difference:      0.004%                                            │
    │                                                                         │
    │   5. REQUIRED PRECISION to distinguish:                                 │
    │                                                                         │
    │      σ(α)/α < 0.002% (20 ppm)                                          │
    │                                                                         │
    │      Current best: ~0.1% (1000 ppm)                                    │
    │      Needed improvement: 50×                                            │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
"""
print(protocol)

# =============================================================================
# SECTION 7: EQUIPMENT AND BUDGET
# =============================================================================

print("\n" + "="*80)
print("SECTION 7: EQUIPMENT AND BUDGET")
print("="*80)

equipment = """
    REQUIRED EQUIPMENT:

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                         │
    │   ITEM                                    COST (USD)    STATUS          │
    │   ─────────────────────────────────────────────────────────────────    │
    │                                                                         │
    │   Ultra-high vacuum AFM                  $150,000       Purchase        │
    │   Vibration isolation table               $20,000       Available       │
    │   Gold-coated microspheres (100 μm)        $1,000       Purchase        │
    │   Gold-coated Si wafers                      $500       Purchase        │
    │   Temperature control system               $5,000       Purchase        │
    │   Piezo nanopositioners                   $15,000       Purchase        │
    │   Interferometric distance sensor         $25,000       Purchase        │
    │   Data acquisition & control              $10,000       Partial         │
    │                                                                         │
    │   ─────────────────────────────────────────────────────────────────    │
    │   TOTAL:                                ~$225,000                       │
    │                                                                         │
    │   TIMELINE:                                                             │
    │     Equipment setup: 3-4 months                                         │
    │     System calibration: 2 months                                        │
    │     Data collection: 4-6 months                                         │
    │     Analysis: 2 months                                                  │
    │     Total: 12-14 months                                                 │
    │                                                                         │
    │   PERSONNEL:                                                            │
    │     1 graduate student (full-time)                                      │
    │     1 postdoc (50% time)                                               │
    │     PI supervision                                                      │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
"""
print(equipment)

# =============================================================================
# SECTION 8: SUCCESS CRITERIA
# =============================================================================

print("="*80)
print("SECTION 8: SUCCESS CRITERIA")
print("="*80)

criteria = """
    SUCCESS CRITERIA:

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                         │
    │   ✓ TIER 1 (Achievable):                                               │
    │     • Measure F(L) with <1% precision across 100 nm - 1 μm range      │
    │     • Extract α with σ(α)/α < 0.1%                                     │
    │     • Verify consistency with standard QED predictions                  │
    │                                                                         │
    │   ✓ TIER 2 (Challenging):                                              │
    │     • Improve precision to σ(α)/α < 0.01%                              │
    │     • Begin to constrain Z² vs. standard prediction                    │
    │     • Publish precision measurement paper                               │
    │                                                                         │
    │   ✓ TIER 3 (Breakthrough):                                             │
    │     • Achieve σ(α)/α < 0.002%                                          │
    │     • Definitively test α⁻¹ = 4Z² + 3 prediction                       │
    │     • Major physics discovery                                           │
    │                                                                         │
    │   ─────────────────────────────────────────────────────────────────    │
    │                                                                         │
    │   REALISTIC ASSESSMENT:                                                 │
    │     Tier 1 is achievable with proposed setup                           │
    │     Tier 2 requires systematic improvements                             │
    │     Tier 3 requires new experimental techniques                         │
    │                                                                         │
    │   EVEN TIER 1 SUCCESS provides:                                         │
    │     • Independent α measurement                                         │
    │     • Validation of QED vacuum structure                                │
    │     • Foundation for future precision work                              │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
"""
print(criteria)

# =============================================================================
# SAVE RESULTS
# =============================================================================

results = {
    "experiment": "Casimir Torque Geometry / Precision α Measurement",
    "framework": "Z² = 32π/3",
    "tests": "Fine structure constant via precision Casimir measurement",
    "parameters": {
        "R_sphere_um": R_sphere * 1e6,
        "L_gap_range_nm": [100, 1000],
        "F_at_100nm_pN": casimir_sphere_plate(R_sphere, 100e-9) * 1e12,
        "F_at_1um_pN": casimir_sphere_plate(R_sphere, 1e-6) * 1e12
    },
    "predictions": {
        "alpha_inv_SM": 137.036,
        "alpha_inv_Z2": 137.041,
        "difference_percent": 0.004
    },
    "budget_usd": 225000,
    "timeline_months": "12-14",
    "success_criterion": "Extract α with σ(α)/α < 0.1%"
}

output_file = "research/experiments/exp2_casimir_results.json"
with open(output_file, 'w') as f:
    json.dump(results, f, indent=2)

print(f"\nResults saved to: {output_file}")
print("\n" + "="*80)
print("EXPERIMENT 2 DESIGN COMPLETE")
print("="*80)
