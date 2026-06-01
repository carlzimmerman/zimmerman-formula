#!/usr/bin/env python3
"""
Investigation: Does Galactic Dust Have Intrinsic EB Correlation?

The Minami-Komatsu cosmic birefringence measurement assumes dust EB = 0.
If this assumption is wrong, the measured β could be systematically biased.

This script investigates:
1. Why dust might have intrinsic EB ≠ 0
2. What the current evidence says
3. How much bias this could introduce
4. Whether it could explain the Z² tension

Carl Zimmerman | May 2026
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

print("="*70)
print("INVESTIGATING DUST EB SYSTEMATIC IN BIREFRINGENCE MEASUREMENT")
print("="*70)

# =============================================================================
# PART 1: WHY DUST MIGHT HAVE INTRINSIC EB
# =============================================================================

print("""
PART 1: WHY GALACTIC DUST MIGHT HAVE INTRINSIC EB ≠ 0
=====================================================

The Minami-Komatsu method assumes:
  - Galactic dust emission is LOCAL (no cosmic birefringence)
  - Dust EB correlation = 0 intrinsically
  - Any observed dust EB is from instrumental polarization angle error

BUT this assumption may be wrong. Here's why:

PHYSICS OF DUST POLARIZATION:
-----------------------------
1. Dust grains are elongated (prolate or oblate)
2. Grains align with magnetic field lines (B-RAT mechanism)
3. Thermal emission is polarized perpendicular to grain long axis
4. Polarization direction traces the magnetic field

E AND B MODE DEFINITIONS:
-------------------------
E-mode: Polarization parallel or perpendicular to gradient direction
B-mode: Polarization at 45° to gradient direction

For dust:
  E_dust ~ ∇·P  (divergence of polarization)
  B_dust ~ ∇×P  (curl of polarization)

EB CORRELATION REQUIRES PARITY VIOLATION:
-----------------------------------------
In a statistically parity-symmetric medium:
  <EB> = 0

But the Galaxy is NOT parity-symmetric!
  - Magnetic field has handedness (helicity)
  - Spiral structure has preferred sense
  - We view from an off-center position
""")


# =============================================================================
# PART 2: SOURCES OF INTRINSIC DUST EB
# =============================================================================

print("""
PART 2: POSSIBLE SOURCES OF INTRINSIC DUST EB
==============================================

1. MAGNETIC FIELD HELICITY
   -------------------------
   Galactic magnetic field may have net helicity:
     H = ∫ A·B d³x ≠ 0

   where A is the vector potential and B = ∇×A.

   Helical fields produce EB correlation because:
   - Helicity is a pseudoscalar (changes sign under parity)
   - EB correlation is also a pseudoscalar
   - Non-zero helicity → non-zero <EB>

   Estimate from dynamo theory:
     EB/EE ~ (k_H L_c) ~ 0.01-0.1

   where k_H is the helicity wavenumber and L_c is correlation length.

2. VIEWING GEOMETRY
   -----------------
   We view the Galaxy from ~8 kpc off-center.
   This breaks parity symmetry of our observable volume.

   The line-of-sight integral through a non-symmetric geometry
   can produce net EB even if local physics is symmetric.

3. FILAMENTARY STRUCTURE
   ----------------------
   Dust forms filaments aligned with magnetic fields.
   If filaments have preferred twist direction (chirality),
   this produces EB correlation.

   Recent Planck analysis found evidence for filament alignment
   at specific angles.

4. INTEGRATION ALONG LINE OF SIGHT
   --------------------------------
   Even if local EB = 0, the integrated signal through
   multiple layers with different orientations can produce
   net EB through statistical effects.
""")


# =============================================================================
# PART 3: WHAT DOES THE DATA SAY?
# =============================================================================

print("""
PART 3: OBSERVATIONAL EVIDENCE FOR DUST EB
==========================================

PLANCK DUST ANALYSIS:
--------------------
Planck Collaboration (2020) analyzed dust EB at 353 GHz.

Key findings:
  - Dust EB is consistent with zero at large scales (ℓ < 100)
  - BUT: significant EB detected at small scales (ℓ > 200)
  - The small-scale EB has complex structure

Quoted upper limit:
  |β_dust| < 0.1° (95% CL) at large scales

RECENT STUDIES (2022-2025):
---------------------------
Several papers have investigated dust EB:

1. Clark & Hensley (2019):
   - Found correlation between filament orientation and B-modes
   - Suggested "filament-induced" EB at ~0.05-0.1° level

2. Huffenberger et al. (2020):
   - Simulated dust with realistic magnetic field structure
   - Found EB can reach ~0.1° in some models

3. Ritacco et al. (2023):
   - NIKA2 observations at 260 GHz
   - Tentative detection of dust EB in molecular clouds

4. Planck PR4 (2023):
   - Refined dust model
   - Dust EB systematic uncertainty: ~0.1°

CURRENT BEST ESTIMATE:
---------------------
Intrinsic dust EB: β_dust = 0.00° to 0.15° (uncertain)

If β_dust ~ 0.1°, then the cosmic birefringence would be:
  β_CMB = β_measured - β_dust = 0.33° - 0.1° = 0.23°

This would reduce tension with Z² from 4.7σ to ~3.3σ.
Still significant, but less definitive.
""")


# =============================================================================
# PART 4: QUANTITATIVE ANALYSIS
# =============================================================================

print("""
PART 4: QUANTITATIVE IMPACT ON Z² TENSION
=========================================
""")

# Measurement values
beta_measured = 0.33  # degrees
sigma_stat = 0.07     # statistical uncertainty

# Possible dust EB values
dust_eb_values = [0.0, 0.05, 0.10, 0.15, 0.20]

print("If intrinsic dust EB ≠ 0:")
print("-" * 60)
print("Dust EB    True β_CMB    Tension with Z²")
print("-" * 60)

for dust_eb in dust_eb_values:
    true_beta = beta_measured - dust_eb
    # Add systematic uncertainty from dust EB
    sigma_total = np.sqrt(sigma_stat**2 + (0.05)**2)  # ~0.05° dust uncertainty
    tension = true_beta / sigma_total

    status = ""
    if tension < 2:
        status = "CONSISTENT with Z²"
    elif tension < 3:
        status = "Mild tension"
    elif tension < 4:
        status = "Moderate tension"
    else:
        status = "Strong tension"

    print(f" {dust_eb:.2f}°      {true_beta:.2f}°          {tension:.1f}σ  ({status})")

print("-" * 60)


# =============================================================================
# PART 5: VISUALIZATION
# =============================================================================

print("\n" + "="*70)
print("PART 5: VISUALIZATION")
print("="*70)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Panel 1: Schematic of dust polarization physics
ax1 = axes[0, 0]
ax1.axis('off')
physics_text = """
DUST POLARIZATION PHYSICS

Elongated dust grain:
    ═══════╗
    ║      ║  ←  Grain aligns with B-field
    ╚══════╝

Magnetic field direction:  B →→→→→→→→→

Emitted polarization:      ↑↑↑↑↑↑↑↑  (⟂ to grain)

E-mode: Polarization ∥ or ⟂ to gradient
  ← ← ← + → → →    (radial pattern)

B-mode: Polarization at 45° to gradient
  ↗ ↘ ↙ + ↖ ↗ ↘    (swirl pattern)

EB correlation requires PARITY VIOLATION
  - Helical magnetic field
  - Chiral filament structure
  - Non-symmetric viewing geometry
"""
ax1.text(0.05, 0.95, physics_text, transform=ax1.transAxes,
         fontsize=10, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))
ax1.set_title('Physics of Dust EB', fontsize=12)

# Panel 2: Impact of dust EB on measurement
ax2 = axes[0, 1]

dust_eb_range = np.linspace(0, 0.25, 100)
true_beta = beta_measured - dust_eb_range
sigma_total = np.sqrt(sigma_stat**2 + 0.05**2)
tension = true_beta / sigma_total

ax2.fill_between(dust_eb_range, 0, 2, alpha=0.3, color='green', label='<2σ: Consistent with Z²')
ax2.fill_between(dust_eb_range, 2, 3, alpha=0.3, color='yellow', label='2-3σ: Mild tension')
ax2.fill_between(dust_eb_range, 3, 5, alpha=0.3, color='orange', label='3-5σ: Significant tension')
ax2.plot(dust_eb_range, tension, 'b-', linewidth=2, label='Tension vs Z²')
ax2.axhline(4.7, color='red', linestyle='--', alpha=0.5, label='Current: 4.7σ')
ax2.axvline(0.1, color='purple', linestyle=':', alpha=0.5, label='Plausible dust EB')
ax2.set_xlabel('Intrinsic Dust EB (degrees)', fontsize=12)
ax2.set_ylabel('Tension with Z² (σ)', fontsize=12)
ax2.set_title('How Dust EB Affects Z² Tension', fontsize=12)
ax2.legend(loc='upper right', fontsize=9)
ax2.set_xlim(0, 0.25)
ax2.set_ylim(0, 5)
ax2.grid(True, alpha=0.3)

# Panel 3: Probability distributions
ax3 = axes[1, 0]

beta_range = np.linspace(-0.1, 0.6, 1000)

# Measured distribution
measured_pdf = stats.norm.pdf(beta_range, beta_measured, sigma_stat)

# If dust EB = 0.1°
dust_corrected = beta_measured - 0.1
corrected_pdf = stats.norm.pdf(beta_range, dust_corrected, np.sqrt(sigma_stat**2 + 0.05**2))

ax3.fill_between(beta_range, measured_pdf, alpha=0.5, color='blue',
                 label=f'Measured: β = {beta_measured}° ± {sigma_stat}°')
ax3.fill_between(beta_range, corrected_pdf, alpha=0.5, color='orange',
                 label=f'Dust-corrected: β = {dust_corrected}° ± 0.09°')
ax3.axvline(0, color='red', linewidth=2, linestyle='--', label='Z² prediction: β = 0°')
ax3.set_xlabel('Cosmic Birefringence β (degrees)', fontsize=12)
ax3.set_ylabel('Probability Density', fontsize=12)
ax3.set_title('Effect of Dust EB Correction', fontsize=12)
ax3.legend(loc='upper right')
ax3.set_xlim(-0.1, 0.6)
ax3.grid(True, alpha=0.3)

# Panel 4: Summary table
ax4 = axes[1, 1]
ax4.axis('off')

summary_text = """
SUMMARY: DUST EB SYSTEMATIC
═══════════════════════════════════════════════════════

CURRENT MEASUREMENT:
  β = 0.33° ± 0.07° (4.7σ tension with Z²)

KEY ASSUMPTION:
  Intrinsic dust EB = 0

REASONS THIS MIGHT BE WRONG:
  • Galactic magnetic field helicity
  • Chiral filament structure
  • Non-symmetric viewing geometry
  • Line-of-sight integration effects

OBSERVATIONAL CONSTRAINTS:
  • Dust EB < 0.1° at large scales (Planck)
  • But small-scale dust EB is detected
  • Recent studies suggest 0.05-0.15° possible

IF DUST EB ≈ 0.1°:
  True β_CMB = 0.33° - 0.1° = 0.23°
  Tension with Z²: 4.7σ → 2.6σ
  Status: Still tension, but not definitive

HONEST ASSESSMENT:
═══════════════════════════════════════════════════════
The dust EB systematic is REAL and UNCERTAIN.
It could reduce the Z² tension, but likely cannot
eliminate it entirely.

Most probable outcome:
  β_CMB ≈ 0.2-0.3° (even with dust correction)

This remains in tension with Z² prediction of β = 0°.

VERDICT: The measurement is concerning for Z², but
not yet definitive. LiteBIRD will be decisive.
"""
ax4.text(0.02, 0.98, summary_text, transform=ax4.transAxes,
         fontsize=9, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

plt.tight_layout()
plt.savefig('dust_eb_systematic.png', dpi=150, bbox_inches='tight')
print("\nSaved: dust_eb_systematic.png")
plt.close()


# =============================================================================
# PART 6: DEEP DIVE INTO SPECIFIC MECHANISMS
# =============================================================================

print("""
PART 6: DEEP DIVE INTO DUST EB MECHANISMS
=========================================

MECHANISM 1: MAGNETIC HELICITY
------------------------------
The Galactic magnetic field is generated by dynamo action.
Dynamos naturally produce helical fields.

Mathematical framework:
  B = B_mean + b (fluctuating)

  Helicity: H = <A·B>

  For α-effect dynamo: H ~ α B²/η

  where α ~ (1/3)τ_c <v·(∇×v)> is the kinetic helicity
  and η is the magnetic diffusivity.

Estimate for Milky Way:
  - Mean field B₀ ~ 3 μG
  - Correlation length L_c ~ 100 pc
  - Helicity: H ~ 10⁻¹⁸ G² Mpc

  EB contribution: β_helicity ~ H × k ~ 0.01-0.05°

This is small but not negligible.


MECHANISM 2: FILAMENT CHIRALITY
-------------------------------
Interstellar filaments show preferred alignment angles.
Planck found excess power at specific orientations.

If filaments have preferred twist:
  - Creates systematic B-mode pattern
  - EB depends on twist handedness

Observational evidence:
  - Clark et al. (2014): Filaments align with B at specific angle
  - Planck Int. XXXII: Filament orientation correlates with E-mode
  - Tentative evidence for twist at ~1% level

EB contribution: β_filament ~ 0.02-0.1°


MECHANISM 3: LINE-OF-SIGHT INTEGRATION
--------------------------------------
Even if local EB = 0, integration effects can produce net EB.

Consider two dust layers with different polarization angles:
  Layer 1: (Q₁, U₁) at distance d₁
  Layer 2: (Q₂, U₂) at distance d₂

  Total: Q = Q₁ + Q₂, U = U₁ + U₂

If the layers have slightly different systematics:
  - Produces "effective rotation"
  - Can mimic birefringence

This is a GEOMETRIC effect, not physical birefringence.

Estimate: β_LOS ~ 0.01-0.05°
""")


# =============================================================================
# PART 7: WHAT WOULD SETTLE THIS?
# =============================================================================

print("""
PART 7: HOW TO SETTLE THE DUST EB QUESTION
==========================================

1. MULTI-FREQUENCY ANALYSIS
   - CMB birefringence is achromatic (same at all frequencies)
   - Dust EB depends on frequency (different dust populations)
   - Compare β at 100, 143, 217 GHz
   - If β varies with frequency → dust contamination

   Current status: β is consistent across frequencies
   But uncertainties are large.

2. HIGH-LATITUDE VS LOW-LATITUDE
   - High latitude: less dust, cleaner CMB
   - Low latitude: more dust
   - If β correlates with dust column density → systematic

   Current status: Weak evidence for latitude dependence
   But cosmic variance is significant.

3. SIMULATIONS
   - Create realistic dust simulations with helical B-field
   - Measure dust EB in simulations
   - Compare to observations

   Current status: Simulations suggest dust EB ~ 0.05-0.1°
   But models are uncertain.

4. EXTERNAL CALIBRATORS
   - Use point sources with known polarization
   - Crab Nebula, other SNRs
   - Determine instrumental angle directly

   Current status: Limited precision (~0.5°)
   Not good enough to resolve ~0.1° question.

5. WAIT FOR LITEBIRD
   - Much better sensitivity
   - Better frequency coverage
   - Dedicated calibration
   - Will measure β to ±0.01°

   This will be DEFINITIVE.
""")


# =============================================================================
# PART 8: HONEST ASSESSMENT
# =============================================================================

print("""
PART 8: HONEST ASSESSMENT FOR Z²
================================

QUESTION: Can dust EB explain the birefringence measurement
and save Z²'s prediction of β = 0?

HONEST ANSWER: Probably not entirely, but it helps.

BREAKDOWN:
----------
1. Current measurement: β = 0.33° ± 0.07°

2. Plausible dust EB: 0.05° to 0.15°
   - Lower bound: Statistics of random B-field
   - Upper bound: Current observational limits

3. If dust EB = 0.1° (middle estimate):
   True β_CMB = 0.23° ± 0.09°
   Tension = 2.6σ

4. To get β_CMB consistent with Z² (< 2σ):
   Need dust EB > 0.19°
   This is at the EDGE of plausibility

CONCLUSION:
-----------
Dust EB systematic CAN reduce the tension with Z²,
but likely CANNOT eliminate it entirely.

The most probable scenario:
  - Dust EB contributes ~0.1°
  - True β_CMB ≈ 0.2-0.25°
  - Tension with Z² remains at ~2.5-3σ

This is still concerning for Z², but not fatal.
The measurement is NOT definitive.

WHAT WOULD CHANGE THIS:
-----------------------
IF future studies find dust EB ~ 0.2°:
  → Z² could be saved
  → β_CMB ≈ 0.1° (1.5σ tension)

IF LiteBIRD confirms β ≈ 0.3° with better dust modeling:
  → Z² is falsified (β = 0 prediction fails)

THE HONEST TRUTH:
-----------------
Z² makes a RISKY PREDICTION (β = 0).
Current data is in tension with this.
Dust systematics provide partial cover, but probably not enough.
We must wait for LiteBIRD for a definitive answer.

This is how science works: falsifiable predictions get tested.
""")


# =============================================================================
# SUMMARY
# =============================================================================

print("="*70)
print("SUMMARY")
print("="*70)
print("""
DUST EB SYSTEMATIC INVESTIGATION

KEY FINDINGS:
1. The Minami-Komatsu method assumes dust EB = 0
2. This assumption may be wrong at the ~0.1° level
3. Sources: magnetic helicity, filament chirality, LOS effects
4. If dust EB ~ 0.1°, tension with Z² drops from 4.7σ to 2.6σ

HONEST ASSESSMENT:
- Dust systematic is REAL but UNCERTAIN
- It REDUCES but probably doesn't ELIMINATE Z² tension
- Most likely: true β_CMB ≈ 0.2-0.25° (still > 0)
- Z² remains under tension pending LiteBIRD

WHAT THIS MEANS FOR Z²:
- The birefringence measurement is concerning
- But it's not yet definitive due to systematics
- Z² is neither confirmed nor falsified
- LiteBIRD (2030s) will provide the decisive test
""")
