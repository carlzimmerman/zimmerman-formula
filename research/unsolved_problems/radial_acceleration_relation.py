#!/usr/bin/env python3
"""
Radial Acceleration Relation (RAR): Zimmerman Formula Predictions
==================================================================

CONTEXT:
The Radial Acceleration Relation (McGaugh+ 2016) is one of the tightest
empirical relations in extragalactic astronomy. It shows that the observed
acceleration g_obs correlates with the baryonic acceleration g_bar with
remarkably small scatter.

OBSERVATION:
g_obs = g_bar / (1 - exp(-√(g_bar/g†)))

where g† ≈ 1.2 × 10⁻¹⁰ m/s² ≈ a₀

THIS IS MOND! The RAR is exactly what MOND predicts.

ZIMMERMAN APPLICATION:
The Zimmerman formula derives a₀ = cH₀/5.79 from first principles.
With evolving a₀, the RAR should EVOLVE with redshift. This is a
key testable prediction.

Author: Carl Zimmerman
"""

import numpy as np
import matplotlib.pyplot as plt

# Constants
c = 2.998e8  # m/s
G = 6.674e-11  # m³/kg/s²
H0 = 71.5  # km/s/Mpc
a0_local = 1.2e-10  # m/s²
Omega_m = 0.315
Omega_Lambda = 0.685

def E_z(z):
    """Dimensionless Hubble parameter"""
    return np.sqrt(Omega_m * (1+z)**3 + Omega_Lambda)

def a0_z(z):
    """MOND acceleration scale at redshift z"""
    return a0_local * E_z(z)

print("=" * 80)
print("RADIAL ACCELERATION RELATION - ZIMMERMAN FORMULA PREDICTIONS")
print("=" * 80)

print("""
THE RADIAL ACCELERATION RELATION (RAR)
======================================

Discovery (McGaugh, Lelli, Schombert 2016):
- Analyzed 153 SPARC galaxies with rotation curves
- Found tight correlation between g_obs and g_bar
- Scatter: only 0.13 dex (intrinsic ~0.06 dex!)

The RAR:
  g_obs = ν(g_bar/g†) × g_bar

where the interpolating function is:
  ν(x) = 1 / (1 - exp(-√x))

and g† = (1.20 ± 0.02) × 10⁻¹⁰ m/s²

THIS IS EXACTLY a₀ FROM MOND!
""")

# RAR parameters
g_dagger = 1.20e-10  # m/s² (observed)
g_dagger_err = 0.02e-10

print(f"Observed g† = ({g_dagger:.2e} ± {g_dagger_err:.2e}) m/s²")
print(f"MOND a₀     = {a0_local:.2e} m/s²")
print(f"Difference  = {abs(g_dagger - a0_local)/a0_local * 100:.1f}%")
print(f"\nThis is MOND! The RAR is the empirical form of MOND.")

# RAR function
def rar_function(g_bar, g_dag):
    """
    The Radial Acceleration Relation.
    Returns g_obs given g_bar and the acceleration scale.
    """
    x = g_bar / g_dag
    nu = 1 / (1 - np.exp(-np.sqrt(x)))
    return g_bar * nu

def mond_simple(g_bar, a0):
    """Simple MOND interpolation for comparison"""
    x = g_bar / a0
    # Standard MOND interpolation
    return g_bar * (1 + np.sqrt(1 + 4/x)) / 2

print("""
ZIMMERMAN FORMULA CONNECTION
============================

The Zimmerman formula derives:
  a₀ = cH₀/5.79 = c√(Gρc)/2

where 5.79 = 2√(8π/3)

This EXPLAINS why g† ≈ 1.2 × 10⁻¹⁰ m/s²:
- It's not a free parameter
- It's derived from cosmological constants
- It MUST equal cH₀/5.79
""")

# Calculate Zimmerman prediction
H0_SI = H0 * 1000 / 3.086e22  # Convert to SI (s⁻¹)
a0_zimmerman = c * H0_SI / 5.79

print(f"\nZimmerman Prediction:")
print(f"  H₀ = {H0} km/s/Mpc")
print(f"  a₀ = cH₀/5.79 = {a0_zimmerman:.3e} m/s²")
print(f"  Observed g† = {g_dagger:.3e} m/s²")
print(f"  Agreement: {100 - abs(a0_zimmerman - g_dagger)/g_dagger * 100:.1f}%")

print("""
KEY INSIGHT:
The Zimmerman formula predicts the RAR scale g† from first principles!
This is not a fit - it's a DERIVATION.
""")

# Redshift evolution
print("\n" + "=" * 60)
print("RAR EVOLUTION WITH REDSHIFT")
print("=" * 60)

print("""
CRITICAL PREDICTION:

If a₀ evolves as a₀(z) = a₀(0) × E(z), then the RAR should change!

At higher z:
- g†(z) = g†(0) × E(z)
- The transition acceleration INCREASES
- Galaxies appear "more Newtonian" at high-z

This is TESTABLE with JWST + IFU spectroscopy!
""")

print("\nRAR Scale Evolution:")
print("  Redshift    E(z)    g†(z) [m/s²]    Change")
print("  " + "-" * 55)
for z in [0, 0.5, 1.0, 1.5, 2.0, 3.0]:
    Ez = E_z(z)
    g_dag_z = g_dagger * Ez
    change = (Ez - 1) * 100
    print(f"  z = {z:3.1f}      {Ez:.2f}    {g_dag_z:.2e}      {change:+.0f}%")

# Comparison at different z
print("\n" + "=" * 60)
print("RAR AT DIFFERENT REDSHIFTS")
print("=" * 60)

g_bar_arr = np.logspace(-13, -8, 100)  # m/s²

print("""
At fixed g_bar, the observed acceleration changes with z:
- Higher z → higher g† → LOWER g_obs/g_bar ratio
- Galaxies look "less boosted" at high-z

This is the opposite of what dark matter would predict!
""")

def g_obs_at_z(g_bar, z):
    """Observed acceleration at redshift z"""
    g_dag_z = g_dagger * E_z(z)
    return rar_function(g_bar, g_dag_z)

print("\nFor g_bar = 10⁻¹¹ m/s² (typical outer disk):")
print("  Redshift    g_obs/g_bar    Interpretation")
print("  " + "-" * 50)
g_bar_test = 1e-11
for z in [0, 1, 2, 3]:
    g_obs = g_obs_at_z(g_bar_test, z)
    ratio = g_obs / g_bar_test
    if ratio > 5:
        interp = "Deep MOND boost"
    elif ratio > 2:
        interp = "Moderate MOND"
    else:
        interp = "Near Newtonian"
    print(f"  z = {z:3.0f}         {ratio:.2f}          {interp}")

# SPARC comparison
print("\n" + "=" * 60)
print("SPARC DATA VALIDATION")
print("=" * 60)

print("""
The SPARC database (Lelli+ 2016) provides:
- 175 disk galaxies with rotation curves
- Accurate baryonic mass models
- High-quality kinematic data

The RAR scatter is REMARKABLY small:
- Total scatter: 0.13 dex
- Intrinsic scatter: 0.057 dex (just 14%!)
- This is TIGHTER than Tully-Fisher!

ΛCDM struggles to explain this tightness because:
- Dark matter halos have scatter in concentration
- Baryonic physics should add more scatter
- Yet the relation is nearly universal
""")

# Scatter comparison
scatter_data = [
    ("RAR (g_obs vs g_bar)", 0.13, 0.057, "McGaugh+ 2016"),
    ("Tully-Fisher", 0.20, 0.10, "Multiple"),
    ("Mass-Size", 0.25, 0.15, "van der Wel+ 2014"),
    ("Faber-Jackson", 0.30, 0.20, "Multiple"),
]

print("\nScaling Relation Scatter Comparison:")
print("  Relation                    Total    Intrinsic    Source")
print("  " + "-" * 65)
for name, total, intrinsic, source in scatter_data:
    print(f"  {name:28s}  {total:.2f}     {intrinsic:.3f}       {source}")

print("\nThe RAR is the TIGHTEST scaling relation known!")

# Testable predictions
print("\n" + "=" * 60)
print("TESTABLE PREDICTIONS")
print("=" * 60)

print("""
1. RAR SCALE EVOLUTION
   - Zimmerman: g†(z) = g†(0) × E(z)
   - At z=2: g† should be ~3× higher
   - Test: JWST IFU rotation curves at z > 1

2. RAR SCATTER EVOLUTION
   - Zimmerman: Scatter should remain small at all z
   - ΛCDM: Scatter should increase at high-z
   - Test: Compare RAR scatter at z=0 vs z=2

3. RAR SHAPE PRESERVATION
   - The functional form should be IDENTICAL at all z
   - Only the scale g† changes
   - Test: Fit RAR at different z, compare shapes

4. RAR FOR DIFFERENT GALAXY TYPES
   - Should hold for: disks, ellipticals, dwarfs, LSBs
   - Same g† for all types at same z
   - Test: Multi-type samples at fixed z

5. EXTERNAL FIELD EFFECT
   - EFE breaks RAR for satellites
   - Predictable deviation from isolated RAR
   - Test: Satellite galaxy rotation curves

6. RAR AT EXTREMELY LOW g_bar
   - Ultra-faint dwarfs probe g_bar < 10⁻¹² m/s²
   - Deep MOND regime: g_obs → √(g_bar × g†)
   - Test: Crater II, Antlia II dynamics
""")

# Summary
print("\n" + "=" * 80)
print("SUMMARY: RAR - ZIMMERMAN PREDICTIONS")
print("=" * 80)
print(f"""
┌────────────────────────────────────────────────────────────┐
│ RADIAL ACCELERATION RELATION - ZIMMERMAN FRAMEWORK         │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ The RAR is the empirical manifestation of MOND:           │
│   g_obs = g_bar / (1 - exp(-√(g_bar/g†)))                 │
│   where g† = 1.20 × 10⁻¹⁰ m/s² = a₀                       │
│                                                            │
│ Zimmerman Contribution:                                    │
│                                                            │
│ 1. DERIVES g† = a₀ = cH₀/5.79:                            │
│    • Not a free parameter                                 │
│    • Predicted from cosmology                             │
│    • Matches observation to ~0.5%                         │
│                                                            │
│ 2. PREDICTS EVOLUTION:                                     │
│    • g†(z) = g†(0) × E(z)                                 │
│    • At z=2: g† is 3× higher                              │
│    • Galaxies "less boosted" at high-z                    │
│                                                            │
│ 3. EXPLAINS TIGHT SCATTER:                                 │
│    • Only 0.057 dex intrinsic scatter                     │
│    • Natural in MOND (single scale a₀)                    │
│    • Hard to explain in ΛCDM                              │
│                                                            │
│ Status: ✅ RAR IS MOND - Zimmerman explains WHY            │
│         🔬 Evolution testable with JWST                    │
│                                                            │
└────────────────────────────────────────────────────────────┘
""")

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Panel 1: RAR at z=0
ax1 = axes[0, 0]
g_bar = np.logspace(-13, -8, 100)
g_obs_z0 = rar_function(g_bar, g_dagger)

ax1.loglog(g_bar, g_obs_z0, 'b-', linewidth=2, label='RAR (MOND)')
ax1.loglog(g_bar, g_bar, 'k--', linewidth=1, label='g_obs = g_bar (Newton)')
ax1.fill_between(g_bar, g_bar, g_obs_z0, alpha=0.2, color='blue', label='MOND boost')
ax1.axvline(g_dagger, color='red', linestyle=':', label=f'g† = a₀')
ax1.set_xlabel('g_bar (m/s²)', fontsize=12)
ax1.set_ylabel('g_obs (m/s²)', fontsize=12)
ax1.set_title('Radial Acceleration Relation (z=0)', fontsize=14)
ax1.legend(fontsize=9)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(1e-13, 1e-8)
ax1.set_ylim(1e-12, 1e-8)

# Panel 2: RAR at different redshifts
ax2 = axes[0, 1]
colors = ['blue', 'green', 'orange', 'red']
for z, color in zip([0, 1, 2, 3], colors):
    g_obs = g_obs_at_z(g_bar, z)
    ax2.loglog(g_bar, g_obs, color=color, linewidth=2, label=f'z = {z}')
ax2.loglog(g_bar, g_bar, 'k--', linewidth=1, alpha=0.5)
ax2.set_xlabel('g_bar (m/s²)', fontsize=12)
ax2.set_ylabel('g_obs (m/s²)', fontsize=12)
ax2.set_title('RAR Evolution with Redshift (Zimmerman)', fontsize=14)
ax2.legend()
ax2.grid(True, alpha=0.3)
ax2.set_xlim(1e-13, 1e-8)
ax2.set_ylim(1e-12, 1e-8)

# Panel 3: MOND boost factor
ax3 = axes[1, 0]
boost_z0 = g_obs_z0 / g_bar
boost_z1 = g_obs_at_z(g_bar, 1) / g_bar
boost_z2 = g_obs_at_z(g_bar, 2) / g_bar

ax3.semilogx(g_bar, boost_z0, 'b-', linewidth=2, label='z = 0')
ax3.semilogx(g_bar, boost_z1, 'g-', linewidth=2, label='z = 1')
ax3.semilogx(g_bar, boost_z2, 'r-', linewidth=2, label='z = 2')
ax3.axhline(1, color='black', linestyle='--', alpha=0.5)
ax3.axvline(g_dagger, color='gray', linestyle=':', alpha=0.5)
ax3.set_xlabel('g_bar (m/s²)', fontsize=12)
ax3.set_ylabel('g_obs / g_bar (MOND boost)', fontsize=12)
ax3.set_title('MOND Boost Factor vs Redshift', fontsize=14)
ax3.legend()
ax3.grid(True, alpha=0.3)
ax3.set_xlim(1e-13, 1e-8)
ax3.set_ylim(0.9, 20)

# Panel 4: g† evolution
ax4 = axes[1, 1]
z_arr = np.linspace(0, 4, 50)
g_dag_arr = [g_dagger * E_z(z) for z in z_arr]

ax4.plot(z_arr, np.array(g_dag_arr) / 1e-10, 'purple', linewidth=2)
ax4.fill_between(z_arr, g_dagger/1e-10, np.array(g_dag_arr)/1e-10, alpha=0.3, color='purple')
ax4.axhline(g_dagger/1e-10, color='blue', linestyle='--', label='g†(z=0)')
ax4.set_xlabel('Redshift z', fontsize=12)
ax4.set_ylabel('g† (10⁻¹⁰ m/s²)', fontsize=12)
ax4.set_title('RAR Scale Evolution (Zimmerman Prediction)', fontsize=14)
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/Users/carlzimmerman/new_physics/zimmerman-formula/research/unsolved_problems/radial_acceleration_relation.png',
            dpi=150, bbox_inches='tight')
plt.close()

print("\n📊 Visualization saved to: research/unsolved_problems/radial_acceleration_relation.png")
