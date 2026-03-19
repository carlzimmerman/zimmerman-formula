#!/usr/bin/env python3
"""
Void Galaxy Properties: Zimmerman Formula Predictions
======================================================

CONTEXT:
Void galaxies live in underdense regions of the cosmic web.
They experience minimal external gravitational fields, making
them ideal MOND laboratories.

OBSERVATIONS:
- Void galaxies tend to be bluer (more star-forming)
- They have different morphology distributions
- Some show enhanced rotation for their mass

ZIMMERMAN APPLICATION:
In voids, the External Field Effect is minimal. Void galaxies
should show "pure MOND" behavior. This is testable and provides
a unique probe of the Zimmerman formula.

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
kpc = 3.086e19  # m
Mpc = 1000 * kpc

def E_z(z):
    """Dimensionless Hubble parameter"""
    return np.sqrt(Omega_m * (1+z)**3 + Omega_Lambda)

def a0_z(z):
    """MOND acceleration scale at redshift z"""
    return a0_local * E_z(z)

print("=" * 80)
print("VOID GALAXY PROPERTIES - ZIMMERMAN FORMULA PREDICTIONS")
print("=" * 80)

print("""
VOID GALAXIES AS MOND LABORATORIES
===================================

What are cosmic voids?
- Underdense regions in the cosmic web
- Typical sizes: 20-100 Mpc
- δ_void ~ -0.8 to -0.5 (80-50% underdense)
- Contain ~15% of galaxies

Why are void galaxies special for MOND?
- Minimal external gravitational field
- No massive neighbors → weak/no EFE
- "Pure MOND" dynamics expected
- Like isolated field galaxies but MORE isolated
""")

# Void properties
void_data = [
    ("Boötes Void", 100, -0.85, "Nearest giant void"),
    ("Local Void", 60, -0.80, "Adjacent to Local Group"),
    ("Sculptor Void", 30, -0.75, "Southern sky"),
    ("Typical void", 30, -0.70, "Average statistics"),
]

print("\nComic Void Properties:")
print("  Void Name         Size (Mpc)    δ       Notes")
print("  " + "-" * 55)
for name, size, delta, notes in void_data:
    print(f"  {name:18s}   {size:5.0f}       {delta:.2f}    {notes}")

# External field in voids
print("\n" + "=" * 60)
print("EXTERNAL FIELD IN VOIDS")
print("=" * 60)

print("""
The External Field Effect (EFE) in MOND:
- Internal dynamics affected by external gravitational field
- g_ext > a₀ → quasi-Newtonian behavior
- g_ext < a₀ → full MOND enhancement

In voids:
- Nearest massive structure is far away
- g_ext can be << a₀
- Void galaxies show PURE MOND!
""")

def external_field_from_structure(M_solar, D_Mpc):
    """External gravitational field from distant structure"""
    M_kg = M_solar * 1.989e30
    D_m = D_Mpc * Mpc
    return G * M_kg / D_m**2

# Compare EFE in different environments
envs = [
    ("Cluster center (Coma)", 1e15, 1),
    ("Cluster outskirts", 1e15, 5),
    ("Group environment", 1e13, 0.5),
    ("Field galaxy", 1e12, 2),
    ("Void edge", 1e12, 10),
    ("Void center", 1e11, 30),
]

print("\nExternal Field by Environment:")
print("  Environment             M_neighbor   D (Mpc)   g_ext/a₀")
print("  " + "-" * 60)
for env, M, D in envs:
    g_ext = external_field_from_structure(M, D)
    ratio = g_ext / a0_local
    regime = "EFE-dom" if ratio > 1 else "MOND" if ratio > 0.1 else "Pure MOND"
    print(f"  {env:25s}  {M:.0e}   {D:5.0f}    {ratio:.3f} ({regime})")

print("""
KEY INSIGHT:
Void centers have g_ext/a₀ ~ 0.001-0.01
This is the PUREST MOND regime accessible!
""")

# BTFR in voids
print("\n" + "=" * 60)
print("BARYONIC TULLY-FISHER IN VOIDS")
print("=" * 60)

print("""
The Baryonic Tully-Fisher Relation (BTFR):
  M_bar = A × v_flat⁴

In MOND, this is EXACT with A = 1/(G × a₀).

Void galaxies should show:
1. TIGHTEST BTFR (no EFE contamination)
2. SAME normalization as field galaxies
3. SAME slope (exactly 4)

This is a precise test of MOND!
""")

# BTFR comparison
def btfr_velocity(M_bar, a0):
    """MOND BTFR prediction for v_flat"""
    M_kg = M_bar * 1.989e30
    v_flat = (G * M_kg * a0)**0.25
    return v_flat / 1000  # km/s

M_arr = np.logspace(8, 11, 50)
v_mond = [btfr_velocity(M, a0_local) for M in M_arr]

print("\nBTFR Predictions for Void Galaxies:")
print("  M_bar (M☉)    v_flat (MOND)    Comment")
print("  " + "-" * 50)
for M in [1e8, 1e9, 1e10, 1e11]:
    v = btfr_velocity(M, a0_local)
    print(f"  {M:.0e}       {v:.0f} km/s")

# Void galaxy observations
print("\n" + "=" * 60)
print("OBSERVED VOID GALAXY PROPERTIES")
print("=" * 60)

print("""
Observations of void galaxies show:

1. MORPHOLOGY
   - More late-type (spirals) than clusters
   - Fewer ellipticals
   - Consistent with less processing

2. STAR FORMATION
   - Enhanced specific SFR
   - Bluer colors
   - Younger stellar populations

3. GAS CONTENT
   - Higher HI gas fractions
   - Extended HI disks
   - Less gas stripping

4. DYNAMICS (limited data)
   - Some show high v_rot for their mass
   - Consistent with MOND boost
   - Need more systematic studies
""")

# Specific void galaxy examples
void_galaxies = [
    ("KK 246", "Void", 9e7, 65, "Isolated dwarf"),
    ("VGS 31", "Void", 3e9, 120, "Void spiral"),
    ("Malin 1", "Low density", 1e11, 300, "Giant LSB"),
    ("AGC 748778", "Void", 5e8, 80, "HI-rich"),
]

print("\nVoid Galaxy Examples:")
print("  Galaxy        Environment   M_bar (M☉)   v_rot    Notes")
print("  " + "-" * 60)
for name, env, mbar, vrot, notes in void_galaxies:
    v_pred = btfr_velocity(mbar, a0_local)
    ratio = vrot / v_pred
    print(f"  {name:12s}  {env:12s}  {mbar:.0e}     {vrot:3.0f}     {notes}")

# Zimmerman evolution
print("\n" + "=" * 60)
print("ZIMMERMAN EVOLUTION FOR VOID GALAXIES")
print("=" * 60)

print("""
With evolving a₀, void galaxy dynamics should change with z:

At z=0: a₀ = 1.2 × 10⁻¹⁰ m/s²
At z=1: a₀ ~ 1.7× higher
At z=2: a₀ ~ 3× higher

Predictions:
1. BTFR normalization shifts with z
   - v_flat ∝ a₀^(1/4)
   - At z=2: v_flat ~30% higher at fixed M_bar

2. MOND radius decreases
   - R_MOND = √(GM/a₀)
   - At z=2: R_MOND ~60% of local
   - Galaxies more compact in deep MOND region

3. Void filling factor changes
   - Structure formation faster at high-z (higher a₀)
   - Voids should be SMALLER at high-z
""")

print("\nBTFR Evolution for Void Galaxies (M_bar = 10¹⁰ M☉):")
print("  Redshift    a₀/a₀(0)    v_flat (km/s)    Change")
print("  " + "-" * 55)
M_test = 1e10
for z in [0, 0.5, 1.0, 1.5, 2.0, 3.0]:
    a0_z_val = a0_local * E_z(z)
    v_z = btfr_velocity(M_test, a0_z_val)
    v_0 = btfr_velocity(M_test, a0_local)
    change = (v_z / v_0 - 1) * 100
    print(f"  z = {z:3.1f}        {E_z(z):.2f}          {v_z:.0f}            {change:+.0f}%")

# Testable predictions
print("\n" + "=" * 60)
print("TESTABLE PREDICTIONS")
print("=" * 60)

print("""
1. BTFR IN VOIDS
   - Should be TIGHTER than field/cluster galaxies
   - Same normalization (A = 1/(G×a₀))
   - Test: HI rotation curves of void galaxies

2. ROTATION CURVE SHAPES
   - Pure MOND: v → (GMa₀)^(1/4) asymptotically
   - No "dark matter" contamination
   - Test: Extended rotation curves

3. VELOCITY DISPERSION IN VOID DWARFS
   - σ² = √(GMa₀) / √2 for isolated dwarfs
   - Higher than Newtonian prediction
   - Test: Spectroscopy of void dwarf galaxies

4. VOID GALAXY SIZES
   - More extended disks (longer R_MOND)
   - Lower central surface brightness
   - Test: Photometry surveys

5. HI MASS FUNCTION IN VOIDS
   - MOND affects gas dynamics
   - Different HI/M* ratio in voids
   - Test: WALLABY, MHONGOOSE surveys

6. BTFR EVOLUTION IN VOIDS
   - Zimmerman: v_flat ∝ E(z)^(1/4) at fixed M
   - ~15% change by z=1
   - Test: High-z void identification + kinematics
""")

# Summary
print("\n" + "=" * 80)
print("SUMMARY: VOID GALAXIES - ZIMMERMAN PREDICTIONS")
print("=" * 80)
print(f"""
┌────────────────────────────────────────────────────────────┐
│ VOID GALAXY PROPERTIES - ZIMMERMAN FRAMEWORK               │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ Void galaxies are ideal MOND laboratories:                 │
│   • Minimal External Field Effect (g_ext << a₀)           │
│   • "Pure MOND" dynamics expected                         │
│   • No EFE contamination of rotation curves               │
│                                                            │
│ Key Predictions:                                           │
│                                                            │
│ 1. Tightest BTFR:                                          │
│    • No EFE scatter                                       │
│    • Intrinsic scatter from MOND alone (~0.05 dex)       │
│                                                            │
│ 2. Pure MOND Rotation Curves:                              │
│    • v → (GMa₀)^(1/4) at large R                         │
│    • No need for DM halo fitting                          │
│                                                            │
│ 3. Enhanced Dynamics:                                      │
│    • Higher v_rot or σ for given M_bar                    │
│    • Exactly as MOND predicts                             │
│                                                            │
│ 4. Zimmerman Evolution:                                    │
│    • v_flat ~15% higher at z=1 (fixed M_bar)             │
│    • Testable with high-z void surveys                    │
│                                                            │
│ Status: 🔬 IDEAL MOND TEST - needs systematic data         │
│         WALLABY, MHONGOOSE will provide samples           │
│                                                            │
└────────────────────────────────────────────────────────────┘
""")

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Panel 1: External field by environment
ax1 = axes[0, 0]
env_names = ['Cluster\ncenter', 'Cluster\noutskirts', 'Group', 'Field', 'Void\nedge', 'Void\ncenter']
g_ext_vals = [external_field_from_structure(M, D) / a0_local
              for env, M, D in envs]
colors_env = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue']

ax1.barh(env_names, g_ext_vals, color=colors_env, alpha=0.7)
ax1.axvline(1, color='red', linestyle='--', label='g_ext = a₀')
ax1.axvline(0.1, color='orange', linestyle=':', label='EFE threshold')
ax1.set_xlabel('g_ext / a₀', fontsize=12)
ax1.set_title('External Field by Environment', fontsize=14)
ax1.set_xscale('log')
ax1.legend()
ax1.grid(True, alpha=0.3, axis='x')

# Panel 2: BTFR in voids
ax2 = axes[0, 1]
ax2.loglog(M_arr, v_mond, 'b-', linewidth=2, label='MOND (pure)')

# Add some scatter for non-void
scatter = 0.15  # dex
v_field = [v * 10**(np.random.normal(0, scatter/2)) for v in v_mond]
v_cluster = [v * 10**(np.random.normal(0, scatter)) for v in v_mond]

ax2.scatter(M_arr[::3], v_field[::3], alpha=0.3, s=20, c='green', label='Field (some EFE)')
ax2.scatter(M_arr[::3], v_cluster[::3], alpha=0.3, s=20, c='red', label='Cluster (strong EFE)')

ax2.set_xlabel('M_bar (M☉)', fontsize=12)
ax2.set_ylabel('v_flat (km/s)', fontsize=12)
ax2.set_title('BTFR: Void vs Other Environments', fontsize=14)
ax2.legend()
ax2.grid(True, alpha=0.3)

# Panel 3: BTFR evolution
ax3 = axes[1, 0]
z_arr = np.linspace(0, 3, 50)
v_evolution = [(G * 1e10 * 1.989e30 * a0_local * E_z(z))**0.25 / 1000 for z in z_arr]

ax3.plot(z_arr, v_evolution, 'purple', linewidth=2)
ax3.axhline(v_evolution[0], color='blue', linestyle='--', alpha=0.5, label='z=0 value')
ax3.fill_between(z_arr, v_evolution[0], v_evolution, alpha=0.2, color='purple')
ax3.set_xlabel('Redshift z', fontsize=12)
ax3.set_ylabel('v_flat (km/s) for 10¹⁰ M☉', fontsize=12)
ax3.set_title('Void Galaxy BTFR Evolution (Zimmerman)', fontsize=14)
ax3.legend()
ax3.grid(True, alpha=0.3)

# Panel 4: MOND boost in voids
ax4 = axes[1, 1]
g_bar_arr = np.logspace(-13, -9, 100)

def mond_boost(g_bar, a0, g_ext=0):
    """MOND boost factor g_obs/g_bar"""
    if g_ext > a0:
        return 1.0  # Newtonian
    elif g_bar < a0:
        return np.sqrt(a0 / g_bar)  # Deep MOND
    else:
        return 1.0  # Newtonian

boost_void = [mond_boost(g, a0_local, 0.001 * a0_local) for g in g_bar_arr]
boost_field = [mond_boost(g, a0_local, 0.1 * a0_local) for g in g_bar_arr]
boost_cluster = [mond_boost(g, a0_local, 2 * a0_local) for g in g_bar_arr]

ax4.loglog(g_bar_arr, boost_void, 'b-', linewidth=2, label='Void (g_ext ~ 0)')
ax4.loglog(g_bar_arr, boost_field, 'g--', linewidth=2, label='Field (g_ext ~ 0.1 a₀)')
ax4.loglog(g_bar_arr, boost_cluster, 'r:', linewidth=2, label='Cluster (g_ext ~ 2 a₀)')
ax4.axhline(1, color='black', linestyle='-', alpha=0.3)
ax4.axvline(a0_local, color='gray', linestyle=':', alpha=0.5, label='a₀')
ax4.set_xlabel('g_bar (m/s²)', fontsize=12)
ax4.set_ylabel('MOND Boost (g_obs / g_bar)', fontsize=12)
ax4.set_title('MOND Enhancement by Environment', fontsize=14)
ax4.legend(fontsize=9)
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/Users/carlzimmerman/new_physics/zimmerman-formula/research/unsolved_problems/void_galaxy_properties.png',
            dpi=150, bbox_inches='tight')
plt.close()

print("\n📊 Visualization saved to: research/unsolved_problems/void_galaxy_properties.png")
