#!/usr/bin/env python3
"""
Why T³/Z₂ Predicts Zero Cosmic Birefringence

A detailed derivation of the Z² prediction β = 0 from first principles.

The key insight: Z₂ parity projection eliminates pseudoscalar modes,
which are exactly what's needed for cosmic birefringence.

Carl Zimmerman | May 2026
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

print("="*70)
print("WHY T³/Z₂ PREDICTS β = 0: DETAILED DERIVATION")
print("="*70)

# =============================================================================
# PART 1: WHAT CAUSES COSMIC BIREFRINGENCE?
# =============================================================================

print("""
PART 1: THE PHYSICS OF COSMIC BIREFRINGENCE
============================================

Cosmic birefringence arises from a coupling between photons and a
PSEUDOSCALAR FIELD φ (like an axion):

LAGRANGIAN COUPLING:
  L_int = (g_φγ/4) φ F_μν F̃^μν

where:
  g_φγ = coupling constant
  F_μν = electromagnetic field tensor
  F̃^μν = dual tensor = ½ ε^μνρσ F_ρσ

The product F·F̃ = E·B is a PSEUDOSCALAR (odd under parity).

For photons traveling through a region where φ varies:
  - Left-circular and right-circular polarization propagate differently
  - Linear polarization rotates by angle:

    β = (g_φγ/2) × ∫ (dφ/dt) dt = (g_φγ/2) × Δφ

where Δφ = φ(today) - φ(at last scattering)

KEY REQUIREMENT: There must be a LARGE-SCALE pseudoscalar field
that has different values at z=0 and z=1100.
""")


# =============================================================================
# PART 2: THE T³/Z₂ ORBIFOLD STRUCTURE
# =============================================================================

print("""
PART 2: THE T³/Z₂ ORBIFOLD STRUCTURE
=====================================

T³/Z₂ is constructed as:
  - Start with T³ (3-torus): identify opposite faces of a cube
  - Apply Z₂: identify points x with -x

This creates a quotient manifold with:
  - 8 FIXED POINTS at (n₁π, n₂π, n₃π) where n_i ∈ {0,1}
  - These fixed points are WHERE you cannot move without hitting yourself
  - Fields must satisfy: φ(-x) = ±φ(x)

PARITY CLASSIFICATION:
  EVEN (scalar): φ(-x) = +φ(x)   → survives Z₂ projection
  ODD (pseudoscalar): φ(-x) = -φ(x) → ELIMINATED by Z₂ projection

At the fixed points, an odd field must satisfy:
  φ(x) = φ(-x) = -φ(x)  →  φ = 0

Odd fields VANISH at fixed points and are projected out globally!
""")


# =============================================================================
# PART 3: MODE DECOMPOSITION ON T³/Z₂
# =============================================================================

print("""
PART 3: MODE DECOMPOSITION ON T³/Z₂
====================================

On the torus T³ with size L, fields expand in Fourier modes:
  φ(x) = Σ_k φ_k exp(ik·x)

where k = (2π/L)(n₁, n₂, n₃) with n_i integers.

Under Z₂ (x → -x):
  exp(ik·(-x)) = exp(-ik·x)

For the field to be well-defined on T³/Z₂:

EVEN MODES (scalar):
  φ_k = φ_{-k}  →  cos(k·x) survives

ODD MODES (pseudoscalar):
  φ_k = -φ_{-k}  →  sin(k·x) survives

BUT the sin modes vanish at all fixed points!

For a PSEUDOSCALAR field (like axion):
  Under parity, φ → -φ
  Combined with Z₂: φ(-x) = -φ(x)

  This means φ must use sin modes

  φ_pseudo(x) = Σ_k a_k sin(k·x)

At fixed points (x = 0, πL/2π, etc.):
  sin(k·x) = sin(0) = 0 or sin(nπ) = 0

  φ_pseudo(fixed points) = 0

The pseudoscalar is CONSTRAINED to vanish at 8 points!
""")


# =============================================================================
# PART 4: THE KEY CONSTRAINT
# =============================================================================

print("""
PART 4: THE KEY CONSTRAINT - NO LARGE-SCALE PSEUDOSCALAR
========================================================

For cosmic birefringence, we need:
  Δφ = φ(z=0) - φ(z=1100) ≠ 0

This requires φ to vary on COSMOLOGICAL scales.

In T³/Z₂:
  - Fundamental domain size L ~ Hubble scale
  - The 8 fixed points are spread across the fundamental domain
  - Any pseudoscalar field must be ZERO at all 8 fixed points

THE MATHEMATICAL CONSTRAINT:

If L is comparable to the Hubble scale (~14 Gpc), then the
cosmological volume contains only ~1 fundamental domain.

A pseudoscalar field on T³/Z₂ must satisfy:
  φ(0) = 0
  φ(πL_x/L, 0, 0) = 0
  φ(0, πL_y/L, 0) = 0
  ... (all 8 fixed points)

For a smoothly varying field over the domain, being zero at 8
spread-out points STRONGLY constrains the average value.

THE AVERAGE OF A PSEUDOSCALAR ON T³/Z₂ IS ZERO:

  <φ> = (1/V) ∫ φ(x) d³x = 0

This follows from:
  ∫ sin(k·x) d³x = 0 for any k ≠ 0

The ZERO MODE (k=0, constant field) is FORBIDDEN for pseudoscalars!
""")


# =============================================================================
# PART 5: DERIVATION OF β = 0
# =============================================================================

print("""
PART 5: DERIVATION OF β = 0
===========================

The birefringence angle is:
  β = (g_φγ/2) × [φ(z=0) - φ(z=1100)]

In T³/Z₂:

1. ZERO MODE FORBIDDEN
   A constant pseudoscalar φ = φ₀ everywhere is not allowed.
   This would violate φ(-x) = -φ(x) at x = 0.

   So there's no "background axion field" that permeates space.

2. OSCILLATING MODES AVERAGE TO ZERO
   The allowed modes are sin(k·x) with k ≠ 0.

   When we integrate along the photon path:
   ∫_path sin(k·x) ds ~ 0

   The oscillations cancel over cosmological distances.

3. NO NET ROTATION
   β = (g_φγ/2) × ∫_path (∇φ · ds)
     = (g_φγ/2) × [φ_end - φ_start]

   But φ at any point is a sum of sin modes:
     <φ(any point)> → 0 when averaged over realizations

   And more importantly, the ZERO MODE contribution is exactly zero.

THEREFORE:
  β = 0 EXACTLY in T³/Z₂

This is not a fine-tuning. It's a TOPOLOGICAL PROTECTION.
The geometry itself forbids the large-scale pseudoscalar needed
for birefringence.
""")


# =============================================================================
# PART 6: WHAT ABOUT AXION DARK MATTER?
# =============================================================================

print("""
PART 6: WHAT ABOUT AXION DARK MATTER?
=====================================

Standard cosmology often includes axion dark matter.
What happens to this in T³/Z₂?

STANDARD PICTURE:
  - Axion field φ_a has mass m_a
  - Oscillates: φ_a ~ cos(m_a t)
  - Acts as cold dark matter
  - Has cosmological average φ̄_a ≠ 0

IN T³/Z₂:
  - The homogeneous mode (k=0) is FORBIDDEN
  - Cannot have φ_a = constant across space
  - Axion-like particles are severely constrained

IMPLICATION:
  Z² framework predicts either:
  1. No axion dark matter (dark matter is something else)
  2. Axions exist but in fundamentally different configuration

This connects to the dark matter sector of Z².
In the Z² framework, dark matter comes from:
  - Extra-dimensional remnants (KK modes)
  - NOT from pseudoscalar axions

So the prediction β = 0 is CONSISTENT with the broader Z² picture:
  - No large-scale pseudoscalars
  - No axion dark matter
  - Dark matter from geometric/extra-dimensional origin
""")


# =============================================================================
# PART 7: VISUALIZATION
# =============================================================================

print("\n" + "="*70)
print("PART 7: VISUALIZATION")
print("="*70)

fig = plt.figure(figsize=(16, 12))

# Panel 1: The T³/Z₂ fundamental domain with fixed points
ax1 = fig.add_subplot(2, 2, 1, projection='3d')

# Draw cube edges
cube_vertices = np.array([
    [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
    [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]
]) * np.pi

edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

for e in edges:
    ax1.plot3D(*zip(cube_vertices[e[0]], cube_vertices[e[1]]), 'b-', alpha=0.5)

# Fixed points
fixed_points = np.array([
    [0, 0, 0], [np.pi, 0, 0], [0, np.pi, 0], [0, 0, np.pi],
    [np.pi, np.pi, 0], [np.pi, 0, np.pi], [0, np.pi, np.pi], [np.pi, np.pi, np.pi]
])

ax1.scatter(*fixed_points.T, s=200, c='red', marker='o', label='Fixed points')

# Z₂ identification arrows
for fp in fixed_points:
    if not np.allclose(fp, [0,0,0]):
        mid = fp / 2
        ax1.quiver(mid[0], mid[1], mid[2], -mid[0]*0.3, -mid[1]*0.3, -mid[2]*0.3,
                   color='green', alpha=0.5, arrow_length_ratio=0.3)

ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_zlabel('z')
ax1.set_title('T³/Z₂: 8 Fixed Points', fontsize=12)
ax1.legend()

# Panel 2: Even vs Odd modes
ax2 = fig.add_subplot(2, 2, 2)
x = np.linspace(0, np.pi, 100)

# Even mode (cosine)
y_even = np.cos(2*x)
# Odd mode (sine)
y_odd = np.sin(2*x)

ax2.plot(x, y_even, 'b-', linewidth=2, label='Even (cos): survives Z₂')
ax2.plot(x, y_odd, 'r--', linewidth=2, label='Odd (sin): pseudoscalar')
ax2.axhline(0, color='gray', linewidth=0.5)
ax2.axvline(0, color='green', linewidth=2, alpha=0.5)
ax2.axvline(np.pi, color='green', linewidth=2, alpha=0.5)
ax2.scatter([0, np.pi], [0, 0], s=100, c='red', zorder=5)
ax2.annotate('Fixed\npoints', xy=(0.05, 0.1), fontsize=10)
ax2.set_xlabel('x', fontsize=12)
ax2.set_ylabel('φ(x)', fontsize=12)
ax2.set_title('Mode Structure on T³/Z₂', fontsize=12)
ax2.legend()
ax2.grid(True, alpha=0.3)
ax2.set_xlim(-0.1, np.pi+0.1)

# Panel 3: Why zero mode is forbidden
ax3 = fig.add_subplot(2, 2, 3)
ax3.axis('off')

derivation_text = """
WHY β = 0 IN T³/Z₂: MATHEMATICAL SUMMARY

1. Birefringence requires: φ F·F̃ coupling
   - F·F̃ = E·B is a PSEUDOSCALAR
   - φ must be PSEUDOSCALAR (odd under parity)

2. On T³/Z₂, pseudoscalars must satisfy:
   φ(-x) = -φ(x)   (Z₂ identification)

3. At fixed points (x = -x mod L):
   φ(x) = φ(-x) = -φ(x)
   → φ(fixed point) = 0

4. Mode expansion:
   Pseudoscalar φ = Σ_k a_k sin(k·x)

   The k=0 (constant) mode is FORBIDDEN
   because sin(0) = 0 ≠ constant.

5. Birefringence angle:
   β ∝ Δφ = φ(z=0) - φ(z=1100)

   For oscillating sin modes:
   <Δφ> = 0

6. CONCLUSION:
   ┌─────────────────────────────┐
   │  β = 0 EXACTLY in T³/Z₂    │
   │                             │
   │  TOPOLOGICAL PROTECTION    │
   │  NOT FINE-TUNING!          │
   └─────────────────────────────┘
"""
ax3.text(0.05, 0.95, derivation_text, transform=ax3.transAxes,
         fontsize=10, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

# Panel 4: Comparison with observation
ax4 = fig.add_subplot(2, 2, 4)

# Show probability distributions
beta = np.linspace(-0.2, 0.7, 1000)

# Observed distribution
from scipy.stats import norm
obs_pdf = norm.pdf(beta, 0.33, 0.07)

# Z² prediction (delta function at 0)
z2_pdf = np.zeros_like(beta)
z2_pdf[np.abs(beta) < 0.005] = 50

ax4.fill_between(beta, obs_pdf, alpha=0.5, color='blue', label='Observed: β = 0.33° ± 0.07°')
ax4.axvline(0, color='red', linewidth=3, linestyle='-', label='Z² prediction: β = 0 exactly')
ax4.fill_between(beta[np.abs(beta) < 0.02], 0, 50, alpha=0.3, color='red')

# Calculate tension
tension = 0.33 / 0.07
ax4.annotate(f'Tension: {tension:.1f}σ', xy=(0.45, 4), fontsize=14,
             bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))

ax4.set_xlabel('Cosmic Birefringence β (degrees)', fontsize=12)
ax4.set_ylabel('Probability Density', fontsize=12)
ax4.set_title('Z² Prediction vs Observation', fontsize=12)
ax4.legend(loc='upper right')
ax4.set_xlim(-0.2, 0.7)
ax4.set_ylim(0, 7)
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('birefringence_in_t3z2.png', dpi=150, bbox_inches='tight')
print("\nSaved: birefringence_in_t3z2.png")
plt.close()


# =============================================================================
# PART 8: THE TENSION AND POSSIBLE RESOLUTIONS
# =============================================================================

print("""
PART 8: THE TENSION AND POSSIBLE RESOLUTIONS
=============================================

THE PROBLEM:
  Z² predicts:  β = 0° exactly
  Observed:     β = 0.33° ± 0.07°
  Tension:      4.7σ

IF THE OBSERVATION IS CORRECT:
  T³/Z₂ as currently formulated is FALSIFIED.

POSSIBLE RESOLUTIONS:

1. SYSTEMATIC ERROR IN MEASUREMENT
   - Intrinsic dust EB ≠ 0
   - Foreground contamination
   - Instrumental effects

   Status: Under investigation. Some hints that dust EB ~ 0.1-0.2°
   would reduce tension.

2. ANISOTROPIC BIREFRINGENCE
   - The measurement assumes uniform β across sky
   - If β varies spatially, interpretation changes
   - T³/Z₂ could allow position-dependent effects

   Status: Some evidence for anisotropy at ~2σ level.

3. MODIFIED T³/Z₂ STRUCTURE
   - Perhaps the Z₂ action is not exactly x → -x
   - A slightly different orbifold might allow small β

   Status: Would require reworking the framework.

4. ADDITIONAL PHYSICS BEYOND T³/Z₂
   - Some other source of birefringence
   - Not from axions but from modified gravity

   Status: Would need to be compatible with Z² otherwise.

VERDICT:
  This is the MOST SERIOUS TEST of Z².

  If LiteBIRD confirms β ≈ 0.3° → Z² is falsified
  If LiteBIRD finds β → 0° → Z² gains strong support

  We must wait for better data.
""")


# =============================================================================
# PART 9: WHAT CAN WE DO NOW?
# =============================================================================

print("""
PART 9: WHAT CAN WE DO NOW?
===========================

1. ANALYZE EXISTING DATA FOR SYSTEMATICS
   - Look at dust EB correlations
   - Check for spatial variations
   - Compare different foreground models

2. COMPUTE THEORETICAL PREDICTIONS MORE PRECISELY
   - What exactly does T³/Z₂ allow?
   - Are there any loopholes?
   - Can oscillating modes produce any net effect?

3. WAIT FOR NEW EXPERIMENTS
   - LiteBIRD (2030s): β to ±0.01°
   - Simons Observatory: Near-term constraints
   - CLASS: Independent measurement

4. PREPARE FOR BOTH OUTCOMES
   - If β = 0: Celebrate Z² confirmation
   - If β ≠ 0: Understand what modification is needed
""")


# =============================================================================
# SUMMARY
# =============================================================================

print("="*70)
print("SUMMARY: WHY T³/Z₂ PREDICTS β = 0")
print("="*70)
print("""
THE CHAIN OF LOGIC:

1. Cosmic birefringence requires pseudoscalar coupling φ F·F̃
2. Pseudoscalars are ODD under parity: φ(-x) = -φ(x)
3. T³/Z₂ identifies x with -x (the Z₂ projection)
4. At 8 fixed points, odd fields must vanish: φ = 0
5. The constant (k=0) mode is FORBIDDEN for pseudoscalars
6. Only oscillating sin(k·x) modes are allowed
7. These average to zero over cosmological distances
8. Therefore: β = ∫ ∇φ · ds = 0

THIS IS TOPOLOGICAL PROTECTION - NOT FINE-TUNING.

The 4.7σ tension with observation is the MOST SERIOUS
challenge to the Z² framework. Resolution requires either:
  - Systematic error in the birefringence measurement
  - Modification of the T³/Z₂ structure
  - Additional physics not in current Z² formulation

Awaiting LiteBIRD (2030s) for definitive test.
""")
