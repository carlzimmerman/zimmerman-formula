#!/usr/bin/env python3
"""
EXPERIMENT 5: METAMATERIAL BULK PROPAGATION ANALOGUE
=====================================================

Uses 3D photonic crystals to simulate gravitational leakage into extra
dimensions, testing the core Z² framework prediction.

THEORETICAL BASIS:
-----------------
In the Z² framework, expanding the extra dimension (ξ > 1) causes:

    G_N(r) = G_N^{vev} × exp[-76.8 × (ξ - 1)]

The mechanism: gravitational flux "leaks" into the bulk extra dimensions,
reducing the effective 4D coupling.

A 3D photonic crystal with engineered band structure can simulate this:
- Photons in allowed bands ↔ 4D gravitons
- Photons in band gaps ↔ Forbidden modes (no 4D propagation)
- Evanescent coupling between bands ↔ Bulk leakage

WHAT THIS TESTS:
---------------
1. Wave propagation in a discretized "extra dimension" (mode ladder)
2. Exponential suppression vs. mode spacing
3. Band structure engineering mimicking KK tower
4. Dynamical control of effective coupling

Author: Carl Zimmerman
Date: April 2026
Framework: Z² = 32π/3
"""

import numpy as np
import json

# Physical constants
c = 299792458           # m/s
hbar = 1.054571817e-34  # J·s

print("="*80)
print("EXPERIMENT 5: METAMATERIAL BULK PROPAGATION ANALOGUE")
print("Simulating Gravitational Leakage via Photonic Crystals")
print("="*80)

# =============================================================================
# SECTION 1: THE ANALOGY
# =============================================================================

print("\n" + "="*80)
print("SECTION 1: THE GRAVITY LEAKAGE ↔ PHOTONIC CRYSTAL ANALOGY")
print("="*80)

analogy = """
    MAPPING BETWEEN EXTRA DIMENSIONS AND PHOTONIC BANDS:

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                         │
    │   Z² FRAMEWORK                          PHOTONIC CRYSTAL                │
    │   ────────────────                      ────────────────                │
    │                                                                         │
    │   4D spacetime                          Allowed photonic band           │
    │   Extra dimensions (bulk)               Band gap (forbidden)            │
    │   KK graviton modes                     Higher photonic bands           │
    │   Graviton mass gap M_KK                Band gap frequency Δω           │
    │                                                                         │
    │   ─────────────────────────────────────────────────────────────────    │
    │                                                                         │
    │   Gravity propagating in 4D             Light in lowest band            │
    │   Gravity leaking to bulk               Evanescent tunneling            │
    │   Radion expansion (ξ > 1)              Band structure modulation       │
    │                                                                         │
    │   ─────────────────────────────────────────────────────────────────    │
    │                                                                         │
    │   KEY EQUATION:                                                         │
    │                                                                         │
    │   Gravitational suppression:            Evanescent decay:               │
    │     G_N ∝ exp[-2kπR₅(ξ-1)]               T ∝ exp[-κ × d]               │
    │                                                                         │
    │   where κ = √(ω_gap² - ω²)/c is the imaginary wavevector               │
    │   in the band gap, and d is the crystal thickness.                     │
    │                                                                         │
    │   MATHEMATICAL ISOMORPHISM:                                             │
    │     2kπR₅(ξ-1) ↔ κ × d                                                 │
    │                                                                         │
    │   Both produce EXPONENTIAL SUPPRESSION of wave transmission.           │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
"""
print(analogy)

# =============================================================================
# SECTION 2: PHOTONIC CRYSTAL DESIGN
# =============================================================================

print("\n" + "="*80)
print("SECTION 2: PHOTONIC CRYSTAL DESIGN")
print("="*80)

# Design parameters
lambda_0 = 1550e-9        # Telecom wavelength (1550 nm)
omega_0 = 2 * np.pi * c / lambda_0
a = lambda_0 / 2          # Lattice constant (half wavelength)
n_high = 3.5              # High index (silicon)
n_low = 1.5               # Low index (silica)

# Band gap estimation (1D model)
delta_n = n_high - n_low
n_avg = (n_high + n_low) / 2
gap_ratio = 2 * delta_n / (np.pi * n_avg)  # Approximate gap width / center frequency

print(f"""
    PHOTONIC CRYSTAL PARAMETERS (1D Bragg Stack Model):

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                         │
    │   Operating wavelength:    λ₀ = {lambda_0*1e9:.0f} nm (telecom C-band)             │
    │   Central frequency:       ω₀ = {omega_0:.3e} rad/s                 │
    │   Lattice constant:        a = λ₀/2 = {a*1e9:.0f} nm                            │
    │                                                                         │
    │   High-index material:     n_H = {n_high} (Silicon)                            │
    │   Low-index material:      n_L = {n_low} (Silica)                             │
    │   Index contrast:          Δn = {delta_n}                                     │
    │   Average index:           n̄ = {n_avg}                                       │
    │                                                                         │
    │   ─────────────────────────────────────────────────────────────────    │
    │                                                                         │
    │   BAND GAP PROPERTIES:                                                  │
    │                                                                         │
    │   Gap width / center:      Δω/ω₀ ≈ {gap_ratio:.3f} ({gap_ratio*100:.1f}%)                     │
    │   Gap center frequency:    ω_gap ≈ {omega_0:.3e} rad/s               │
    │   Gap width:               Δω ≈ {gap_ratio * omega_0:.3e} rad/s             │
    │                                                                         │
    │   Evanescent decay constant in gap center:                              │
    │     κ = Δω / (2c) ≈ {gap_ratio * omega_0 / (2*c):.1e} m⁻¹                      │
    │     Decay length: 1/κ ≈ {2*c / (gap_ratio * omega_0) * 1e6:.1f} μm                               │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
""")

# =============================================================================
# SECTION 3: 3D PHOTONIC CRYSTAL STRUCTURE
# =============================================================================

print("="*80)
print("SECTION 3: 3D PHOTONIC CRYSTAL - 'ARTIFICIAL EXTRA DIMENSIONS'")
print("="*80)

design_3d = """
    3D WOODPILE PHOTONIC CRYSTAL:

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                         │
    │   The woodpile structure creates a COMPLETE 3D bandgap:                │
    │                                                                         │
    │   Layer 1:  ═══════  ═══════  ═══════  ═══════  (rods along x)        │
    │   Layer 2:  ║     ║     ║     ║     ║     ║     (rods along y)        │
    │   Layer 3:  ═══════  ═══════  ═══════  ═══════  (rods along x, offset)│
    │   Layer 4:  ║     ║     ║     ║     ║     ║     (rods along y, offset)│
    │                                                                         │
    │   This creates a face-centered-cubic (FCC) Brillouin zone.            │
    │                                                                         │
    │   ─────────────────────────────────────────────────────────────────    │
    │                                                                         │
    │   ANALOGY TO Z² FRAMEWORK:                                              │
    │                                                                         │
    │   The woodpile has multiple band gaps → multiple "extra dimensions"   │
    │                                                                         │
    │   Band 1 (fundamental): ↔ 4D spacetime (observable physics)           │
    │   Band gap 1:          ↔ Compactified S¹/Z₂                           │
    │   Band 2:              ↔ First KK mode                                 │
    │   Band gap 2:          ↔ Second compactified dimension                 │
    │   ...                  ↔ T³/Z₂ (three extra dimensions)               │
    │                                                                         │
    │   ═══════════════════════════════════════════════════════════════════  │
    │   A 3D woodpile with 3 complete band gaps simulates the               │
    │   M⁴ × S¹/Z₂ × T³/Z₂ geometry of the Z² framework!                   │
    │   ═══════════════════════════════════════════════════════════════════  │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
"""
print(design_3d)

# =============================================================================
# SECTION 4: TRANSMISSION EXPERIMENT
# =============================================================================

print("\n" + "="*80)
print("SECTION 4: TRANSMISSION MEASUREMENT - 'GRAVITY LEAKAGE TEST'")
print("="*80)

# Calculate transmission vs. crystal thickness
kappa = gap_ratio * omega_0 / (2 * c)  # Evanescent decay constant
d_range = np.linspace(1, 20, 20) * 1e-6  # 1 to 20 microns
T_range = np.exp(-2 * kappa * d_range)  # Transmission

print(f"""
    TRANSMISSION THROUGH PHOTONIC CRYSTAL (BAND GAP REGION):

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                         │
    │   Input: Tunable laser at ω = ω_gap (band gap center)                 │
    │   Output: Transmitted intensity T(d) = T₀ × exp(-2κd)                 │
    │                                                                         │
    │   Thickness d (μm)    Transmission T    log₁₀(T)    Z² Analogue       │
    │   ─────────────────────────────────────────────────────────────────    │
""")

for d, T in zip(d_range[::4], T_range[::4]):
    xi_equiv = 1 + np.log(1/T) / 76.8  # Equivalent ξ for same suppression
    print(f"    │       {d*1e6:5.1f}              {T:.2e}        {np.log10(T):+.1f}           ξ ≈ {xi_equiv:.2f}           │")

print("""    │                                                                         │
    │   ─────────────────────────────────────────────────────────────────    │
    │                                                                         │
    │   INTERPRETATION:                                                       │
    │     Increasing crystal thickness d is ANALOGOUS to increasing ξ        │
    │     Both cause exponential suppression of wave transmission            │
    │     The photonic crystal is a "tunable extra dimension simulator"      │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
""")

# =============================================================================
# SECTION 5: DYNAMIC MODULATION - 'RADION EXCITATION ANALOGUE'
# =============================================================================

print("="*80)
print("SECTION 5: DYNAMIC MODULATION - RADION EXCITATION ANALOGUE")
print("="*80)

modulation = """
    THERMO-OPTIC / ELECTRO-OPTIC BAND GAP TUNING:

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                         │
    │   The band gap can be DYNAMICALLY TUNED by changing refractive index: │
    │                                                                         │
    │   THERMO-OPTIC (Silicon):                                               │
    │     dn/dT ≈ 1.8 × 10⁻⁴ K⁻¹                                             │
    │     ΔT = 100 K → Δn ≈ 0.02 → Δω_gap/ω_gap ≈ 1%                        │
    │                                                                         │
    │   ELECTRO-OPTIC (Lithium Niobate):                                      │
    │     Δn ≈ 0.001 at E = 10 V/μm                                          │
    │     Modulation speed: up to 100 GHz                                    │
    │                                                                         │
    │   ─────────────────────────────────────────────────────────────────    │
    │                                                                         │
    │   ANALOGY TO RADION DYNAMICS:                                           │
    │                                                                         │
    │   Static band gap    ↔  kπR₅ = 38.4 (vacuum value)                    │
    │   Band gap tuning    ↔  Radion excitation ξ > 1                        │
    │   Modulation at 2ω   ↔  Mathieu instability pumping                    │
    │                                                                         │
    │   ═══════════════════════════════════════════════════════════════════  │
    │   EXPERIMENT: Modulate band gap at 2× transmission resonance          │
    │               frequency and observe parametric amplification           │
    │   ═══════════════════════════════════════════════════════════════════  │
    │                                                                         │
    │   PROTOCOL:                                                             │
    │     1. Tune laser to band edge (partial transmission)                  │
    │     2. Apply RF heating at frequency ω_mod = 2 × δω (detuning)        │
    │     3. Observe transmission enhancement via Mathieu instability        │
    │     4. Measure threshold modulation depth                              │
    │                                                                         │
    │   This directly tests the Planck-scale seed mechanism dynamics!        │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
"""
print(modulation)

# =============================================================================
# SECTION 6: EQUIPMENT AND BUDGET
# =============================================================================

print("\n" + "="*80)
print("SECTION 6: EQUIPMENT AND BUDGET")
print("="*80)

equipment = """
    REQUIRED EQUIPMENT:

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                         │
    │   ITEM                                    COST (USD)    STATUS          │
    │   ─────────────────────────────────────────────────────────────────    │
    │                                                                         │
    │   Tunable laser (1500-1600 nm)           $25,000        Purchase        │
    │   Photonic crystal samples (woodpile)    $15,000        Fabrication     │
    │   Optical spectrum analyzer              $20,000        Rental          │
    │   Thermo-optic controller                 $3,000        Purchase        │
    │   RF signal generator (10 GHz)            $5,000        Available       │
    │   Photodetectors (high-speed)             $4,000        Purchase        │
    │   Fiber optics and coupling               $5,000        Purchase        │
    │   Optical table and mounts                $8,000        Available       │
    │   Data acquisition                        $5,000        Available       │
    │                                                                         │
    │   ─────────────────────────────────────────────────────────────────    │
    │   TOTAL:                                ~$90,000                        │
    │                                                                         │
    │   FABRICATION PARTNER:                                                  │
    │     • Stanford Nanofabrication Facility                                │
    │     • MIT Nanostructures Laboratory                                    │
    │     • Commercial: NanoScribe, Sandia                                   │
    │                                                                         │
    │   TIMELINE:                                                             │
    │     Sample fabrication: 2-3 months                                      │
    │     Optical setup: 1-2 months                                          │
    │     Static measurements: 2 months                                       │
    │     Dynamic (modulation) tests: 3 months                               │
    │     Analysis: 1 month                                                   │
    │     Total: 9-11 months                                                  │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
"""
print(equipment)

# =============================================================================
# SECTION 7: SUCCESS CRITERIA
# =============================================================================

print("="*80)
print("SECTION 7: SUCCESS CRITERIA")
print("="*80)

criteria = """
    SUCCESS CRITERIA:

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                         │
    │   ✓ TIER 1 (Basic validation):                                         │
    │                                                                         │
    │   1. FABRICATE 3D photonic crystal with complete band gap              │
    │      • Measure transmission spectrum                                    │
    │      • Verify band gap width matches design                            │
    │                                                                         │
    │   2. DEMONSTRATE exponential transmission decay                         │
    │      • T(d) = T₀ × exp(-2κd) with κ matching theory                   │
    │      • This validates "gravity leakage" analogue                       │
    │                                                                         │
    │   ✓ TIER 2 (Dynamical tests):                                          │
    │                                                                         │
    │   3. MODULATE band gap via thermo-optic effect                         │
    │      • Demonstrate reversible band gap shift                           │
    │      • Correlate Δn with Δω_gap                                        │
    │                                                                         │
    │   4. PARAMETRIC AMPLIFICATION at band edge                             │
    │      • Apply 2ω modulation                                             │
    │      • Observe transmission enhancement                                │
    │      • Measure threshold (analogue of q_crit)                          │
    │                                                                         │
    │   ✓ TIER 3 (Advanced):                                                 │
    │                                                                         │
    │   5. GRADIENT STRUCTURE                                                │
    │      • Fabricate crystal with varying lattice constant                 │
    │      • Create "warp bubble" analogue with position-dependent ξ        │
    │      • Demonstrate controlled beam steering                            │
    │                                                                         │
    │   ─────────────────────────────────────────────────────────────────    │
    │                                                                         │
    │   WHAT SUCCESS PROVES:                                                  │
    │     • The mathematical structure of gravitational leakage is correct  │
    │     • Exponential suppression arises from wave mechanics in gaps       │
    │     • Mathieu instability can overcome suppression barriers            │
    │     • Z² framework dynamics are physically realizable                  │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
"""
print(criteria)

# =============================================================================
# SECTION 8: ULTIMATE GOAL - THE WARP BUBBLE ANALOGUE
# =============================================================================

print("\n" + "="*80)
print("SECTION 8: ULTIMATE GOAL - PHOTONIC WARP BUBBLE ANALOGUE")
print("="*80)

ultimate = """
    THE GRAND VISION: PHOTONIC ALCUBIERRE METRIC

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                         │
    │   With sufficient fabrication control, we could construct:             │
    │                                                                         │
    │   ┌─────────────────────────────────────────────────────────────────┐  │
    │   │                                                                 │  │
    │   │        ═══════════════════════════════════════════════         │  │
    │   │       /                                               \\        │  │
    │   │      /    ╔═══════════════════════════════════════╗    \\       │  │
    │   │     │     ║     FLAT INTERIOR (allowed band)      ║     │      │  │
    │   │     │     ║         (light propagates)            ║     │      │  │
    │   │     │     ╚═══════════════════════════════════════╝     │      │  │
    │   │      \\                                               /        │  │
    │   │       \\                                             /         │  │
    │   │        ════════════════════════════════════════════          │  │
    │   │                      BAND GAP SHELL                          │  │
    │   │                 (evanescent, no propagation)                 │  │
    │   │                                                                 │  │
    │   └─────────────────────────────────────────────────────────────────┘  │
    │                                                                         │
    │   This structure would:                                                 │
    │     • Confine light to the interior                                    │
    │     • Suppress coupling to external modes                              │
    │     • Create a "protected region" analogous to warp bubble interior   │
    │                                                                         │
    │   With GRADIENT LATTICE CONSTANT:                                       │
    │     • Front of bubble: smaller gap → partial coupling                 │
    │     • Rear of bubble: larger gap → strong isolation                   │
    │     • Creates directional propagation preference                       │
    │                                                                         │
    │   THIS IS THE PHOTONIC ANALOGUE OF THE ALCUBIERRE METRIC.             │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
"""
print(ultimate)

# =============================================================================
# SAVE RESULTS
# =============================================================================

results = {
    "experiment": "Metamaterial Bulk Propagation Analogue",
    "framework": "Z² = 32π/3",
    "tests": "Gravitational leakage via photonic crystal transmission",
    "crystal_parameters": {
        "wavelength_nm": lambda_0 * 1e9,
        "lattice_constant_nm": a * 1e9,
        "n_high": n_high,
        "n_low": n_low,
        "gap_ratio": gap_ratio,
        "decay_constant_inv_m": kappa,
        "decay_length_um": 1/kappa * 1e6
    },
    "analogue_mapping": {
        "crystal_thickness_d": "radion expansion ξ",
        "transmission_T": "gravitational coupling G_N/G_vev",
        "band_modulation": "radion excitation"
    },
    "budget_usd": 90000,
    "timeline_months": "9-11",
    "success_criterion": "Demonstrate exponential transmission decay T(d) = T₀ exp(-2κd)"
}

output_file = "research/experiments/exp5_metamaterial_results.json"
with open(output_file, 'w') as f:
    json.dump(results, f, indent=2)

print(f"\nResults saved to: {output_file}")
print("\n" + "="*80)
print("EXPERIMENT 5 DESIGN COMPLETE")
print("="*80)
