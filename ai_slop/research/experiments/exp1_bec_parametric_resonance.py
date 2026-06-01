#!/usr/bin/env python3
"""
EXPERIMENT 1: BEC PARAMETRIC RESONANCE ANALOGUE
================================================

Tests the Mathieu instability dynamics that govern radion excitation,
using a Bose-Einstein Condensate as an accessible analogue system.

THEORETICAL BASIS:
-----------------
The radion field satisfies the damped Mathieu equation:
    d²φ/dτ² + 2μ dφ/dτ + [a - 2q cos(2τ)] φ = 0

Key prediction from Z² framework:
    q_crit = 1/Q = Γ_r/ω_r

A BEC with modulated trap frequency exhibits IDENTICAL dynamics:
    d²δn/dτ² + 2γ dδn/dτ + [a - 2q cos(2τ)] δn = 0

where δn is the density fluctuation (phonon mode).

WHAT THIS TESTS:
---------------
1. The mathematical structure of parametric instability
2. Threshold behavior: q_crit = 1/Q
3. Growth rate scaling: μ ≈ (q/4) × ω_d
4. Mode selection in multi-mode systems

This validates that the Planck-scale seed mechanism has the correct
dynamical behavior, even though we cannot access radion frequencies.

Author: Carl Zimmerman
Date: April 2026
Framework: Z² = 32π/3
"""

import numpy as np
import json
from scipy.integrate import odeint
from scipy.signal import find_peaks

# Physical constants
hbar = 1.054571817e-34  # J·s
k_B = 1.380649e-23      # J/K
m_Rb = 1.443e-25        # kg (Rb-87)
a_s = 5.3e-9            # m (scattering length)

print("="*80)
print("EXPERIMENT 1: BEC PARAMETRIC RESONANCE ANALOGUE")
print("Testing Mathieu Instability Dynamics at Accessible Frequencies")
print("="*80)

# =============================================================================
# SECTION 1: EXPERIMENTAL DESIGN
# =============================================================================

print("\n" + "="*80)
print("SECTION 1: EXPERIMENTAL DESIGN")
print("="*80)

design = """
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  BEC PARAMETRIC RESONANCE EXPERIMENT                                        │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                                                                       │ │
│  │     ╔═══════════════════════════════════════════════════════════╗    │ │
│  │     ║                    MAGNETIC TRAP                          ║    │ │
│  │     ║                                                           ║    │ │
│  │     ║    ┌─────────────────────────────────────────────────┐   ║    │ │
│  │     ║    │              ⬤ ⬤ ⬤ ⬤ ⬤ ⬤ ⬤ ⬤                │   ║    │ │
│  │     ║    │           ⬤ ⬤ ⬤ ⬤ ⬤ ⬤ ⬤ ⬤ ⬤ ⬤             │   ║    │ │
│  │     ║    │              BEC (10⁶ Rb-87 atoms)              │   ║    │ │
│  │     ║    │           ⬤ ⬤ ⬤ ⬤ ⬤ ⬤ ⬤ ⬤ ⬤ ⬤             │   ║    │ │
│  │     ║    │              ⬤ ⬤ ⬤ ⬤ ⬤ ⬤ ⬤ ⬤                │   ║    │ │
│  │     ║    └─────────────────────────────────────────────────┘   ║    │ │
│  │     ║                                                           ║    │ │
│  │     ║    ω_trap(t) = ω₀ [1 + ε cos(ω_d t)]                     ║    │ │
│  │     ║                                                           ║    │ │
│  │     ╚═══════════════════════════════════════════════════════════╝    │ │
│  │                              ↓                                        │ │
│  │                       Modulation coils                                │ │
│  │                    (ω_d = 2ω_phonon)                                  │ │
│  │                                                                       │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  MEASUREMENT: Time-of-flight imaging to detect phonon amplification       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
"""
print(design)

# =============================================================================
# SECTION 2: BEC PARAMETERS
# =============================================================================

print("\n" + "="*80)
print("SECTION 2: BEC PARAMETERS")
print("="*80)

# Typical BEC parameters
N_atoms = 1e6                    # Number of atoms
T_BEC = 100e-9                   # Temperature (100 nK)
omega_trap = 2 * np.pi * 100     # Trap frequency (100 Hz)
omega_phonon = 2 * np.pi * 1000  # Phonon frequency (1 kHz)

# BEC properties
n_0 = 1e14 * 1e6  # Peak density (10¹⁴ cm⁻³ = 10²⁰ m⁻³)
xi = hbar / np.sqrt(2 * m_Rb * n_0 * 4 * np.pi * hbar**2 * a_s / m_Rb)  # Healing length
c_s = np.sqrt(4 * np.pi * hbar**2 * a_s * n_0 / m_Rb**2)  # Speed of sound

# Phonon damping (Landau damping + thermal)
gamma_phonon = 2 * np.pi * 10  # ~10 Hz damping rate
Q_phonon = omega_phonon / (2 * gamma_phonon)

print(f"""
    BEC Parameters (Rb-87):

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                         │
    │   Number of atoms:     N = {N_atoms:.0e}                                │
    │   Temperature:         T = {T_BEC*1e9:.0f} nK                                       │
    │   Trap frequency:      ω_trap = 2π × {omega_trap/(2*np.pi):.0f} Hz                        │
    │   Phonon frequency:    ω_phonon = 2π × {omega_phonon/(2*np.pi):.0f} Hz                     │
    │                                                                         │
    │   Peak density:        n₀ = {n_0:.1e} m⁻³                        │
    │   Healing length:      ξ = {xi*1e6:.2f} μm                               │
    │   Speed of sound:      c_s = {c_s*1e3:.2f} mm/s                              │
    │                                                                         │
    │   Phonon damping:      γ = 2π × {gamma_phonon/(2*np.pi):.0f} Hz                           │
    │   Quality factor:      Q = ω/2γ = {Q_phonon:.1f}                               │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
""")

# =============================================================================
# SECTION 3: MATHIEU EQUATION MAPPING
# =============================================================================

print("="*80)
print("SECTION 3: MATHIEU EQUATION MAPPING")
print("="*80)

# Driving frequency (principal resonance)
omega_drive = 2 * omega_phonon

# Critical modulation depth
q_crit_theory = 1 / Q_phonon

# Modulation depth range to test
epsilon_range = np.linspace(0.001, 0.1, 50)
q_range = epsilon_range  # For small modulation, q ≈ ε

print(f"""
    Mathieu Equation Mapping:

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                         │
    │   RADION EQUATION:                                                      │
    │     d²φ/dτ² + (Γ_r/ω_r) dφ/dτ + [1 - 2q cos(2τ)] φ = 0                │
    │                                                                         │
    │   BEC ANALOGUE:                                                         │
    │     d²δn/dτ² + (γ/ω) dδn/dτ + [1 - 2ε cos(2τ)] δn = 0                 │
    │                                                                         │
    │   MAPPING:                                                              │
    │     τ = ω_d t / 2                                                       │
    │     q ↔ ε  (modulation depth)                                          │
    │     Γ_r/ω_r ↔ γ/ω  (inverse quality factor)                           │
    │                                                                         │
    │   KEY PREDICTION:                                                       │
    │     q_crit = 1/Q = {q_crit_theory:.4f}                                       │
    │                                                                         │
    │   For ε > ε_crit, phonon amplitude grows exponentially:                │
    │     δn(t) ∝ exp(μt) where μ ≈ (ε/4) × ω_d                             │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
""")

# =============================================================================
# SECTION 4: NUMERICAL SIMULATION
# =============================================================================

print("="*80)
print("SECTION 4: NUMERICAL SIMULATION")
print("="*80)

def mathieu_damped(y, t, a, q, mu):
    """Damped Mathieu equation: y'' + 2μy' + (a - 2q cos(2t))y = 0"""
    phi, dphi = y
    ddphi = -2*mu*dphi - (a - 2*q*np.cos(2*t))*phi
    return [dphi, ddphi]

# Time array (in units of τ = ω_d t / 2)
tau_max = 100  # ~100 oscillation periods
t_eval = np.linspace(0, tau_max, 10000)

# Initial conditions (small perturbation)
y0 = [0.01, 0]

# Mathieu parameter (principal resonance)
a = 1.0

# Damping parameter
mu_damp = gamma_phonon / omega_drive

print(f"    Simulating Mathieu dynamics for various modulation depths...")
print(f"    Damping parameter: μ = γ/ω_d = {mu_damp:.4f}")
print(f"    Predicted critical: q_crit = {q_crit_theory:.4f}")
print()

# Test different q values
q_test_values = [0.01, 0.02, 0.03, 0.05, 0.08, 0.10]
growth_rates = []

print("    q value    |  Final amplitude  |  Growth rate  |  Status")
print("    " + "-"*60)

for q in q_test_values:
    sol = odeint(mathieu_damped, y0, t_eval, args=(a, q, mu_damp))
    final_amp = np.abs(sol[-1, 0])

    # Estimate growth rate from envelope
    if final_amp > y0[0]:
        mu_growth = np.log(final_amp / y0[0]) / tau_max
    else:
        mu_growth = 0

    growth_rates.append(mu_growth)

    if q > q_crit_theory and final_amp > 1:
        status = "UNSTABLE ⚠️"
    elif q > q_crit_theory:
        status = "Growing"
    else:
        status = "Stable"

    print(f"    {q:.3f}      |  {final_amp:.4e}      |  {mu_growth:.4f}        |  {status}")

# =============================================================================
# SECTION 5: EXPERIMENTAL PROTOCOL
# =============================================================================

print("\n" + "="*80)
print("SECTION 5: EXPERIMENTAL PROTOCOL")
print("="*80)

protocol = """
    STEP-BY-STEP EXPERIMENTAL PROTOCOL:

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                         │
    │  1. PREPARE BEC                                                         │
    │     • Laser cool Rb-87 to ~100 nK                                      │
    │     • Load ~10⁶ atoms into magnetic trap                               │
    │     • Verify condensate fraction > 90%                                  │
    │     • Measure trap frequency ω_trap = 2π × 100 Hz                       │
    │                                                                         │
    │  2. CHARACTERIZE PHONON MODES                                           │
    │     • Apply brief impulse to excite collective modes                   │
    │     • Measure phonon frequency ω_phonon via density oscillations       │
    │     • Extract damping rate γ from decay envelope                       │
    │     • Calculate Q = ω_phonon / 2γ                                       │
    │                                                                         │
    │  3. APPLY PARAMETRIC DRIVE                                              │
    │     • Set ω_d = 2ω_phonon (principal resonance)                        │
    │     • Scan modulation depth ε from 0.5% to 10%                         │
    │     • Drive for fixed time T_drive = 100 / ω_phonon                    │
    │     • Record density distribution via absorption imaging               │
    │                                                                         │
    │  4. MEASURE THRESHOLD                                                   │
    │     • Plot final phonon amplitude vs. ε                                │
    │     • Identify critical ε_crit where amplitude diverges               │
    │     • Compare to prediction: ε_crit = 1/Q                              │
    │                                                                         │
    │  5. MEASURE GROWTH RATE                                                 │
    │     • For ε > ε_crit, measure amplitude at multiple times             │
    │     • Extract exponential growth rate μ                                │
    │     • Compare to prediction: μ ≈ (ε/4) × ω_d                          │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
"""
print(protocol)

# =============================================================================
# SECTION 6: PREDICTED RESULTS
# =============================================================================

print("="*80)
print("SECTION 6: PREDICTED RESULTS")
print("="*80)

print(f"""
    EXPECTED EXPERIMENTAL OUTCOMES:

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                         │
    │   1. THRESHOLD MEASUREMENT                                              │
    │                                                                         │
    │      Z² Framework Prediction: ε_crit = 1/Q = {q_crit_theory:.4f}              │
    │                                                                         │
    │      For Q = {Q_phonon:.1f}:                                                   │
    │        ε_crit = {q_crit_theory*100:.2f}% modulation depth                          │
    │                                                                         │
    │      If measured ε_crit matches 1/Q to within 10%:                     │
    │        → Validates Mathieu instability threshold formula              │
    │        → Confirms radion seed mechanism has correct dynamics           │
    │                                                                         │
    │   2. GROWTH RATE MEASUREMENT                                            │
    │                                                                         │
    │      Prediction: μ = (q/4) × ω_d = (ε/4) × 2ω_phonon                  │
    │                                                                         │
    │      For ε = 5%:                                                       │
    │        μ_predicted = 0.05/4 × 2 × 2π × 1000 = {0.05/4 * 2 * 2*np.pi*1000:.1f} rad/s         │
    │        Doubling time: τ_2 = ln(2)/μ = {np.log(2)/(0.05/4 * 2 * 2*np.pi*1000)*1e3:.2f} ms                        │
    │                                                                         │
    │   3. MODE SELECTION                                                     │
    │                                                                         │
    │      Only modes satisfying ω_d = 2ω_mode should be amplified          │
    │      Higher harmonics should remain stable                              │
    │      This tests the narrow-band nature of parametric resonance         │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
""")

# =============================================================================
# SECTION 7: EQUIPMENT AND BUDGET
# =============================================================================

print("="*80)
print("SECTION 7: EQUIPMENT AND BUDGET")
print("="*80)

equipment = """
    REQUIRED EQUIPMENT:

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                         │
    │   ITEM                                    COST (USD)    STATUS          │
    │   ─────────────────────────────────────────────────────────────────    │
    │                                                                         │
    │   BEC apparatus (existing)                    $0        Available       │
    │   Rb-87 source                            $2,000        Consumable      │
    │   Magnetic coil driver (modulation)       $5,000        Custom build    │
    │   Function generator (2 kHz, <0.1%)         $500        Off-the-shelf   │
    │   High-speed camera (>10 kfps)            $8,000        Rental          │
    │   Data acquisition system                 $3,000        Available       │
    │   Optical components (imaging)            $2,000        Partial         │
    │                                                                         │
    │   ─────────────────────────────────────────────────────────────────    │
    │   TOTAL ADDITIONAL COST:                 ~$20,000                       │
    │                                                                         │
    │   TIMELINE:                                                             │
    │     Setup: 2-3 months                                                   │
    │     Data collection: 1-2 months                                         │
    │     Analysis: 1 month                                                   │
    │     Total: 4-6 months                                                   │
    │                                                                         │
    │   PERSONNEL:                                                            │
    │     1 graduate student (existing)                                       │
    │     1 postdoc supervisor (existing)                                     │
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
    VALIDATION CRITERIA:

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                         │
    │   ✓ PRIMARY SUCCESS CRITERION:                                         │
    │     Measured ε_crit within 10% of predicted 1/Q                        │
    │                                                                         │
    │   ✓ SECONDARY CRITERIA:                                                │
    │     • Growth rate μ scales linearly with (ε - ε_crit)                 │
    │     • Mode selectivity: only ω_d = 2ω_mode modes amplified            │
    │     • Instability suppressed for ε < ε_crit                           │
    │                                                                         │
    │   WHAT THIS PROVES:                                                     │
    │     • The Mathieu equation correctly describes parametric instability │
    │     • The threshold formula q_crit = 1/Q is valid                      │
    │     • The Planck-scale seed mechanism has correct dynamical structure  │
    │                                                                         │
    │   WHAT THIS DOES NOT PROVE:                                            │
    │     • That radions actually exist                                       │
    │     • That the Z² framework is the correct theory of nature            │
    │     • That Planck-scale seeds can be created                           │
    │                                                                         │
    │   INTERPRETATION:                                                       │
    │     This experiment validates the MATHEMATICAL STRUCTURE of the        │
    │     radion excitation mechanism. If the math works at kHz frequencies, │
    │     there is no reason to doubt it at 10²⁵ Hz frequencies.            │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
"""
print(criteria)

# =============================================================================
# SAVE RESULTS
# =============================================================================

results = {
    "experiment": "BEC Parametric Resonance Analogue",
    "framework": "Z² = 32π/3",
    "tests": "Mathieu instability threshold and growth rate",
    "bec_parameters": {
        "N_atoms": N_atoms,
        "T_BEC_nK": T_BEC * 1e9,
        "omega_trap_Hz": omega_trap / (2 * np.pi),
        "omega_phonon_Hz": omega_phonon / (2 * np.pi),
        "Q_phonon": Q_phonon
    },
    "predictions": {
        "epsilon_crit": q_crit_theory,
        "epsilon_crit_percent": q_crit_theory * 100,
        "growth_rate_at_5_percent": 0.05/4 * 2 * omega_phonon
    },
    "budget_usd": 20000,
    "timeline_months": "4-6",
    "success_criterion": "Measured epsilon_crit within 10% of 1/Q"
}

output_file = "research/experiments/exp1_bec_results.json"
with open(output_file, 'w') as f:
    json.dump(results, f, indent=2)

print(f"\nResults saved to: {output_file}")
print("\n" + "="*80)
print("EXPERIMENT 1 DESIGN COMPLETE")
print("="*80)
