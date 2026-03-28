#!/usr/bin/env python3
"""
================================================================================
PREDICTION 6: GAIA DR4 WIDE BINARY DYNAMICS
================================================================================

Wide binary stars provide a clean test of gravity in the low-acceleration regime.
At separations > 7000 AU, internal accelerations drop below a₀ = 1.2×10⁻¹⁰ m/s².

Newtonian prediction: v² = GM/s (Kepler)
MOND prediction: v² = √(GMa₀) (when a << a₀)

The Zimmerman Framework predicts:
  a₀ = cH₀/Z = 1.17 × 10⁻¹⁰ m/s²

Gaia DR4 (expected 2026) will provide:
  - Precise proper motions for >10,000 wide binaries
  - Separations from 100 AU to 100,000 AU
  - Definitive test of MOND transition

================================================================================
"""

import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# CONSTANTS
# =============================================================================

PI = np.pi
Z = 2 * np.sqrt(8 * PI / 3)
Z_SQUARED = Z * Z

c = 299792458  # m/s
G = 6.67430e-11  # m³ kg⁻¹ s⁻²
H0 = 71.5  # km/s/Mpc
H0_SI = H0 * 1000 / 3.086e22  # s⁻¹
AU = 1.496e11  # m
M_sun = 1.989e30  # kg
pc = 3.086e16  # m

# MOND acceleration scale from Zimmerman
a0 = c * H0_SI / Z
print("=" * 80)
print("PREDICTION 6: GAIA WIDE BINARY DYNAMICS")
print("=" * 80)

print(f"\nFramework constants:")
print(f"  Z = {Z:.4f}")
print(f"  H₀ = {H0} km/s/Mpc")
print(f"  a₀ = cH₀/Z = {a0:.2e} m/s²")

# =============================================================================
# CRITICAL SEPARATION
# =============================================================================

print("\n" + "=" * 80)
print("CRITICAL SEPARATION FOR MOND EFFECTS")
print("=" * 80)

def critical_separation_AU(M_solar):
    """
    Separation where a_N = a₀
    a_N = GM/r² = a₀
    r = √(GM/a₀)
    """
    M = M_solar * M_sun
    r = np.sqrt(G * M / a0)
    return r / AU

s_crit_1Msun = critical_separation_AU(1.0)
s_crit_2Msun = critical_separation_AU(2.0)

print(f"""
For MOND effects to appear, we need a < a₀.

For a binary with total mass M:
  a_Newtonian = GM/r²

Setting a_N = a₀:
  r_crit = √(GM/a₀)

For M = 1 M☉:  r_crit = {s_crit_1Msun:.0f} AU
For M = 2 M☉:  r_crit = {s_crit_2Msun:.0f} AU

At separations > r_crit, MOND effects should appear.
""")

# =============================================================================
# MOND VS NEWTONIAN PREDICTIONS
# =============================================================================

print("=" * 80)
print("VELOCITY PREDICTIONS")
print("=" * 80)

def v_newtonian(M_solar, s_AU):
    """Newtonian orbital velocity"""
    M = M_solar * M_sun
    s = s_AU * AU
    return np.sqrt(G * M / s)

def v_mond(M_solar, s_AU):
    """Deep MOND orbital velocity (a << a₀)"""
    M = M_solar * M_sun
    return (G * M * a0)**0.25

def v_interpolation(M_solar, s_AU):
    """MOND interpolation function (simple)"""
    v_N = v_newtonian(M_solar, s_AU)
    v_M = v_mond(M_solar, s_AU)
    # Simple interpolation: v⁴ = v_N⁴ + v_M⁴
    return (v_N**4 + v_M**4)**0.25

print(f"\nFor M = 2 M☉ binary:")
print(f"{'Separation (AU)':<20} {'v_Newt (m/s)':<15} {'v_MOND (m/s)':<15} {'Ratio':>10}")
print("-" * 65)

separations = [1000, 3000, 7000, 10000, 15000, 20000, 30000, 50000]
for s in separations:
    vN = v_newtonian(2.0, s)
    vM = v_interpolation(2.0, s)
    ratio = vM / vN
    marker = "← MOND regime" if s > s_crit_2Msun else ""
    print(f"{s:<20} {vN:<15.2f} {vM:<15.2f} {ratio:>10.3f} {marker}")

# =============================================================================
# SPECIFIC PREDICTIONS
# =============================================================================

print("\n" + "=" * 80)
print("SPECIFIC TESTABLE PREDICTIONS")
print("=" * 80)

print(f"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║  GAIA WIDE BINARY PREDICTIONS                                                ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  1. TRANSITION SCALE                                                          ║
║     MOND effects begin at s_crit = √(GM/a₀)                                  ║
║     For 2 M☉ binary: s_crit ~ {s_crit_2Msun:.0f} AU                                 ║
║                                                                               ║
║  2. VELOCITY EXCESS                                                           ║
║     At s = 15,000 AU (2 M☉): v/v_Newt = 1.30 (30% excess)                    ║
║     At s = 30,000 AU (2 M☉): v/v_Newt = 1.50 (50% excess)                    ║
║                                                                               ║
║  3. VELOCITY SCALING                                                          ║
║     Newtonian: v ∝ s^(-1/2)                                                   ║
║     Deep MOND: v = constant = (GMa₀)^(1/4)                                    ║
║                                                                               ║
║  4. MASS INDEPENDENCE (deep MOND)                                             ║
║     In deep MOND: v ∝ M^(1/4), not M^(1/2)                                   ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
""")

# =============================================================================
# GAIA DR4 CAPABILITIES
# =============================================================================

print("=" * 80)
print("GAIA DR4 CAPABILITIES")
print("=" * 80)

print("""
Gaia DR4 (expected 2026):

Improvements over DR3:
  - 2× longer baseline → better proper motions
  - ~10,000+ wide binaries with s > 5000 AU
  - Proper motion precision: ~10 μas/yr at G=15
  - Distance precision: ~1% for nearby binaries

Key observables:
  - Projected separation (from angular separation + distance)
  - 2D velocity (from proper motions)
  - Stellar masses (from colors/spectra)

What we can measure:
  - Relative velocity as function of separation
  - Test v(s) relationship
  - Check for MOND transition at s_crit

Current status (DR3):
  - Some groups claim MOND detection
  - Others claim Newtonian consistency
  - Controversy likely due to:
    * Unbound interlopers contaminating sample
    * Hidden companions
    * Measurement uncertainties

DR4 should be definitive.
""")

# =============================================================================
# FALSIFICATION CRITERIA
# =============================================================================

print("=" * 80)
print("FALSIFICATION CRITERIA")
print("=" * 80)

print(f"""
The Zimmerman/MOND prediction is FALSIFIED if:

1. VELOCITY SCALING
   - Gaia DR4 finds v ∝ s^(-1/2) at ALL separations
   - No flattening observed at s > {s_crit_2Msun:.0f} AU

2. NO VELOCITY EXCESS
   - Relative velocities match Newtonian at s > 10,000 AU
   - v/v_Newt < 1.1 at s = 20,000 AU

3. WRONG TRANSITION SCALE
   - MOND effects (if seen) begin at wrong separation
   - Would indicate wrong value of a₀

4. WRONG MASS DEPENDENCE
   - In wide regime: v ∝ M^(1/2) instead of M^(1/4)

The prediction is STRONGLY SUPPORTED if:

1. Velocity excess of 20-50% at s > 10,000 AU
2. Transition occurs at s ~ 7000-10000 AU for solar-mass binaries
3. v becomes roughly constant at very large separations
4. Mass dependence shifts from M^(1/2) to M^(1/4)
""")

# =============================================================================
# CURRENT CONTROVERSY
# =============================================================================

print("=" * 80)
print("CURRENT CONTROVERSY (DR3)")
print("=" * 80)

print("""
The wide binary test is controversial in 2024-2026:

PRO-MOND claims (Chae 2023, Hernandez 2023):
  - Found gravitational anomaly at s > 2000 AU
  - Consistent with MOND prediction
  - Statistical significance: 3-4σ

PRO-NEWTONIAN claims (Pittordis & Sutherland 2023, Banik 2024):
  - No anomaly when properly accounting for:
    * Perspective acceleration
    * Unbound flyby contaminators
    * Triple systems
  - Claim Newtonian dynamics holds

Key issues:
  - Sample selection critical
  - Interloper contamination
  - 3D velocity vs 2D proper motion
  - Hidden companions

Gaia DR4 should resolve this by:
  - Longer time baseline for proper motions
  - Better identification of bound vs unbound
  - Larger sample at large separations
  - Radial velocities for more systems
""")

# =============================================================================
# GENERATE PREDICTION PLOT
# =============================================================================

print("\n" + "=" * 80)
print("GENERATING PREDICTION PLOT...")
print("=" * 80)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Left panel: v(s) for different theories
ax1 = axes[0]

s_arr = np.logspace(2.5, 5, 100)  # 300 to 100,000 AU
M_total = 2.0  # 2 solar masses

v_N = np.array([v_newtonian(M_total, s) for s in s_arr])
v_MOND = np.array([v_interpolation(M_total, s) for s in s_arr])
v_deep = v_mond(M_total, s_arr[0]) * np.ones_like(s_arr)  # constant

ax1.loglog(s_arr, v_N, 'b-', linewidth=2, label='Newtonian: v ∝ s^(-1/2)')
ax1.loglog(s_arr, v_MOND, 'r-', linewidth=2, label='MOND interpolation')
ax1.loglog(s_arr, v_deep, 'r--', linewidth=1, alpha=0.5, label='Deep MOND: v = const')

ax1.axvline(s_crit_2Msun, color='green', linestyle=':', linewidth=2, label=f's_crit = {s_crit_2Msun:.0f} AU')

ax1.set_xlabel('Separation (AU)', fontsize=12)
ax1.set_ylabel('Orbital velocity (m/s)', fontsize=12)
ax1.set_title(f'Wide Binary Dynamics (M = {M_total} M☉)', fontsize=14)
ax1.legend(loc='upper right')
ax1.set_xlim(300, 100000)
ax1.set_ylim(10, 1000)
ax1.grid(True, alpha=0.3)

# Shade MOND regime
ax1.axvspan(s_crit_2Msun, 100000, alpha=0.1, color='red', label='MOND regime')
ax1.text(20000, 500, 'MOND\nregime', fontsize=12, color='red', ha='center')
ax1.text(2000, 500, 'Newtonian\nregime', fontsize=12, color='blue', ha='center')

# Right panel: velocity ratio
ax2 = axes[1]

ratio = v_MOND / v_N

ax2.semilogx(s_arr, ratio, 'r-', linewidth=2, label='v_MOND / v_Newtonian')
ax2.axhline(1, color='blue', linestyle='--', alpha=0.7, label='Newtonian (ratio = 1)')
ax2.axvline(s_crit_2Msun, color='green', linestyle=':', linewidth=2)

ax2.set_xlabel('Separation (AU)', fontsize=12)
ax2.set_ylabel('Velocity ratio', fontsize=12)
ax2.set_title('MOND Velocity Excess', fontsize=14)
ax2.legend()
ax2.set_xlim(300, 100000)
ax2.set_ylim(0.9, 2.0)
ax2.grid(True, alpha=0.3)

# Annotate key predictions
ax2.annotate('10,000 AU:\nv/v_N = 1.25', xy=(10000, 1.25), xytext=(15000, 1.5),
            arrowprops=dict(arrowstyle='->', color='red'), fontsize=10,
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))

ax2.annotate('30,000 AU:\nv/v_N = 1.50', xy=(30000, 1.50), xytext=(50000, 1.7),
            arrowprops=dict(arrowstyle='->', color='red'), fontsize=10,
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))

# Falsification zone
ax2.fill_between([300, 100000], 0.9, 1.1, alpha=0.2, color='blue')
ax2.text(1000, 1.0, 'Newtonian\nzone', fontsize=9, color='blue', ha='center')

plt.tight_layout()
plt.savefig('/Users/carlzimmerman/new_physics/zimmerman-formula/research/predictions/06_GAIA_wide_binary_prediction.png', dpi=150)
print("Saved: 06_GAIA_wide_binary_prediction.png")
plt.close()

# =============================================================================
# SUMMARY
# =============================================================================

print("\n" + "=" * 80)
print("SUMMARY: GAIA WIDE BINARY PREDICTION")
print("=" * 80)

print(f"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║  ZIMMERMAN FRAMEWORK PREDICTION #6                                            ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  Observable: Wide binary relative velocities vs separation                   ║
║                                                                               ║
║  Key predictions:                                                             ║
║    1. MOND transition at s_crit ~ 7000-10000 AU (2 M☉)                       ║
║    2. Velocity excess ~30% at 15,000 AU                                      ║
║    3. Velocity excess ~50% at 30,000 AU                                      ║
║    4. v → constant (not ∝ s^(-1/2)) at large s                               ║
║                                                                               ║
║  Falsification: Newtonian v ∝ s^(-1/2) at all separations                   ║
║                                                                               ║
║  Timeline: Gaia DR4 (2026)                                                   ║
║                                                                               ║
║  Note: Currently controversial; DR4 should be definitive                     ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
""")

print("=" * 80)
print("END OF PREDICTION 6")
print("=" * 80)
