#!/usr/bin/env python3
"""
Example 17: Radial Acceleration Relation (RAR) - MOND's Greatest Success

The RAR is a tight correlation between observed centripetal acceleration
g_obs = v²/r and baryonic gravitational acceleration g_bar = GM(<r)/r².

This is arguably MOND's most impressive success:
1. The relation exists across ALL galaxies (dwarfs to giants)
2. It has remarkably small scatter (<0.1 dex)
3. The transition occurs precisely at a₀ ~ 1.2×10⁻¹⁰ m/s²
4. In ΛCDM, this requires "conspiracy" between baryons and dark matter

Zimmerman contribution: The transition scale a₀ = cH₀/5.79 is derived,
not fitted - making the RAR a PREDICTION, not a post-hoc fit.

References:
- McGaugh et al. (2016) PRL 117, 201101 - Discovery paper
- Lelli et al. (2017) ApJ 836, 152 - SPARC database analysis
- McGaugh (2020) ApJ 891, 88 - RAR in MOND theory
"""

import numpy as np
import matplotlib.pyplot as plt
import os

# Physical constants
G = 6.674e-11        # m³/kg/s²
c = 2.998e8          # m/s
M_sun = 1.989e30     # kg
kpc_to_m = 3.086e19  # m per kpc
Mpc_to_m = 3.086e22  # m per Mpc

# Cosmological parameters
H0 = 67.4            # km/s/Mpc
H0_SI = H0 * 1000 / Mpc_to_m

# MOND parameters
a0_observed = 1.2e-10   # m/s² (from RAR fits)
a0_zimmerman = c * H0_SI / 5.79  # Zimmerman prediction

print("=" * 70)
print("EXAMPLE 17: RADIAL ACCELERATION RELATION - MOND'S GREATEST SUCCESS")
print("=" * 70)
print()

# ============================================================================
# 1. THE RAR DISCOVERY
# ============================================================================

print("PART 1: THE RAR DISCOVERY")
print("-" * 40)
print()
print("McGaugh et al. (2016) analyzed 153 galaxies from SPARC:")
print()
print("  g_obs = v²/r  (observed centripetal acceleration)")
print("  g_bar = GM_bar(<r)/r²  (Newtonian baryonic acceleration)")
print()
print("Result: These are tightly correlated with:")
print("  g_obs = g_bar / μ(g_bar/a₀)")
print()
print("where μ(x) is the MOND interpolating function and a₀ = 1.2×10⁻¹⁰ m/s²")
print()

# ============================================================================
# 2. ZIMMERMAN PREDICTION FOR a₀
# ============================================================================

print("PART 2: ZIMMERMAN PREDICTION")
print("-" * 40)
print()
print("The Zimmerman formula:")
print("  a₀ = c√(Gρc)/2 = cH₀/5.79")
print()
print(f"With H₀ = {H0} km/s/Mpc:")
print(f"  a₀(Zimmerman) = {a0_zimmerman:.3e} m/s²")
print(f"  a₀(RAR fit)   = {a0_observed:.3e} m/s²")
print(f"  Error:          {(a0_zimmerman - a0_observed)/a0_observed * 100:.1f}%")
print()
print("The RAR transition scale is DERIVED from cosmology, not fitted!")
print()

# ============================================================================
# 3. SIMULATED SPARC-LIKE DATA
# ============================================================================

# Generate realistic mock data spanning the RAR
# Based on SPARC statistics (Lelli et al. 2016)

np.random.seed(42)
n_points = 2000  # Number of data points

# g_bar spans ~4 decades
log_g_bar = np.random.uniform(-13, -9, n_points)
g_bar = 10**log_g_bar

# MOND prediction for g_obs
def mond_rar(g_bar, a0):
    """
    MOND prediction: g_obs = g_bar / μ(g_bar/a0)
    Using the 'simple' interpolating function: μ(x) = x/(1+x)
    This gives: g_obs = g_bar * (1 + a0/g_bar) = g_bar + a0
    Or more precisely with the McGaugh function:
    """
    x = g_bar / a0
    # McGaugh interpolating function
    nu = 1 / (1 - np.exp(-np.sqrt(x)))
    return g_bar * nu

g_obs_mond = mond_rar(g_bar, a0_zimmerman)

# Add realistic scatter (0.1 dex observed)
scatter = 0.1
g_obs = g_obs_mond * 10**(np.random.normal(0, scatter, n_points))

print("PART 3: SIMULATED RAR DATA (SPARC-like)")
print("-" * 40)
print()
print(f"Generated {n_points} data points spanning:")
print(f"  log(g_bar): {log_g_bar.min():.1f} to {log_g_bar.max():.1f}")
print(f"  Scatter:    {scatter} dex (matches observations)")
print()

# ============================================================================
# 4. RAR IN DIFFERENT REGIMES
# ============================================================================

print("PART 4: REGIMES OF THE RAR")
print("-" * 40)
print()

# Define regimes
newtonian_mask = g_bar > 10 * a0_zimmerman
transition_mask = (g_bar >= 0.1 * a0_zimmerman) & (g_bar <= 10 * a0_zimmerman)
deep_mond_mask = g_bar < 0.1 * a0_zimmerman

print(f"Newtonian regime (g_bar > 10 a₀):     {np.sum(newtonian_mask)} points")
print(f"Transition regime (0.1 < g_bar/a₀ < 10): {np.sum(transition_mask)} points")
print(f"Deep MOND regime (g_bar < 0.1 a₀):    {np.sum(deep_mond_mask)} points")
print()

print("Behavior in each regime:")
print("  Newtonian:   g_obs ≈ g_bar (1:1 line)")
print("  Deep MOND:   g_obs ≈ √(g_bar × a₀) (flattening)")
print("  Transition:  Smooth interpolation")
print()

# ============================================================================
# 5. WHY RAR IS A PROBLEM FOR ΛCDM
# ============================================================================

print("PART 5: THE ΛCDM CONSPIRACY PROBLEM")
print("-" * 40)
print()
print("In ΛCDM, the RAR requires a 'conspiracy':")
print()
print("  g_obs = g_bar + g_DM")
print()
print("For the RAR to hold tightly, dark matter must 'know' about baryons:")
print("  • Where baryons are dense, DM contributes less")
print("  • Where baryons are sparse, DM contributes more")
print("  • This must work across 4 decades in g_bar")
print("  • With scatter < 0.1 dex (!!)")
print()
print("This requires extreme fine-tuning of DM halo profiles")
print("to baryonic distributions - with no physical mechanism.")
print()

# ============================================================================
# 6. QUANTITATIVE TEST: SCATTER
# ============================================================================

print("PART 6: QUANTITATIVE SCATTER ANALYSIS")
print("-" * 40)
print()

# Calculate residuals from MOND prediction
residuals = np.log10(g_obs) - np.log10(g_obs_mond)

print(f"Scatter statistics:")
print(f"  Mean residual:  {np.mean(residuals):.3f} dex")
print(f"  RMS scatter:    {np.std(residuals):.3f} dex")
print(f"  Observed:       0.10 ± 0.01 dex (McGaugh et al.)")
print()
print("The scatter is dominated by measurement errors, not intrinsic!")
print("MOND predicts ZERO intrinsic scatter - all galaxies on one curve.")
print()

# ============================================================================
# 7. HIGH-Z PREDICTION
# ============================================================================

print("PART 7: ZIMMERMAN PREDICTION FOR HIGH-z RAR")
print("-" * 40)
print()

def a0_at_z(z, Om=0.315, OL=0.685):
    """Zimmerman: a₀(z) = a₀(0) × E(z)"""
    E_z = np.sqrt(Om * (1 + z)**3 + OL)
    return a0_zimmerman * E_z

redshifts = [0, 0.5, 1.0, 2.0, 3.0]
print("Evolution of RAR transition scale:")
print(f"{'z':<8} {'a₀(z)/a₀(0)':<15} {'Effect on RAR':<30}")
print("-" * 53)

for z in redshifts:
    a0_z = a0_at_z(z)
    ratio = a0_z / a0_zimmerman
    effect = "Same as local" if z == 0 else f"Transition at higher g_bar"
    print(f"{z:<8} {ratio:<15.2f} {effect:<30}")

print()
print("KEY PREDICTION: At z=2, MOND effects begin at g_bar 3× higher than local.")
print("This shifts the RAR curve - TESTABLE with JWST kinematics!")
print()

# ============================================================================
# 8. CREATE VISUALIZATIONS
# ============================================================================

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Plot 1: The RAR
ax1 = axes[0]

# Plot data points colored by regime
ax1.scatter(np.log10(g_bar[deep_mond_mask]), np.log10(g_obs[deep_mond_mask]),
            c='blue', s=5, alpha=0.3, label='Deep MOND')
ax1.scatter(np.log10(g_bar[transition_mask]), np.log10(g_obs[transition_mask]),
            c='green', s=5, alpha=0.3, label='Transition')
ax1.scatter(np.log10(g_bar[newtonian_mask]), np.log10(g_obs[newtonian_mask]),
            c='red', s=5, alpha=0.3, label='Newtonian')

# MOND prediction line
g_bar_line = np.logspace(-13, -9, 100)
g_obs_line = mond_rar(g_bar_line, a0_zimmerman)
ax1.plot(np.log10(g_bar_line), np.log10(g_obs_line), 'k-', linewidth=2,
         label='MOND (Zimmerman a₀)')

# 1:1 line (Newtonian)
ax1.plot([-13, -9], [-13, -9], 'k--', linewidth=1, alpha=0.5, label='g_obs = g_bar')

# Mark a₀
ax1.axvline(x=np.log10(a0_zimmerman), color='orange', linestyle=':',
            linewidth=2, label=f'a₀ = {a0_zimmerman:.2e}')

ax1.set_xlabel('log(g_bar) [m/s²]', fontsize=12)
ax1.set_ylabel('log(g_obs) [m/s²]', fontsize=12)
ax1.set_title('Radial Acceleration Relation', fontsize=14)
ax1.legend(loc='lower right', fontsize=8)
ax1.set_xlim(-13, -9)
ax1.set_ylim(-12, -9)
ax1.grid(True, alpha=0.3)

# Plot 2: Residuals
ax2 = axes[1]
ax2.scatter(np.log10(g_bar), residuals, c='steelblue', s=5, alpha=0.3)
ax2.axhline(y=0, color='k', linestyle='-', linewidth=1)
ax2.axhline(y=0.1, color='r', linestyle='--', linewidth=1, alpha=0.5)
ax2.axhline(y=-0.1, color='r', linestyle='--', linewidth=1, alpha=0.5)

ax2.set_xlabel('log(g_bar) [m/s²]', fontsize=12)
ax2.set_ylabel('Residual [dex]', fontsize=12)
ax2.set_title('Scatter from MOND Prediction', fontsize=14)
ax2.set_xlim(-13, -9)
ax2.set_ylim(-0.5, 0.5)
ax2.grid(True, alpha=0.3)

# Add text
ax2.text(-12.5, 0.35, f'RMS = {np.std(residuals):.3f} dex',
         fontsize=11, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Plot 3: RAR at different redshifts
ax3 = axes[2]

colors = ['black', 'blue', 'green', 'orange', 'red']
for i, z in enumerate(redshifts):
    a0_z = a0_at_z(z)
    g_obs_z = mond_rar(g_bar_line, a0_z)
    ax3.plot(np.log10(g_bar_line), np.log10(g_obs_z), '-',
             color=colors[i], linewidth=2, label=f'z = {z}')

# Mark local a₀
ax3.axvline(x=np.log10(a0_zimmerman), color='gray', linestyle=':',
            linewidth=1, alpha=0.5)

ax3.set_xlabel('log(g_bar) [m/s²]', fontsize=12)
ax3.set_ylabel('log(g_obs) [m/s²]', fontsize=12)
ax3.set_title('RAR Evolution with Redshift\n(Zimmerman Prediction)', fontsize=14)
ax3.legend(loc='lower right', fontsize=9)
ax3.set_xlim(-13, -9)
ax3.set_ylim(-12, -9)
ax3.grid(True, alpha=0.3)

# Add arrow showing evolution
ax3.annotate('Higher a₀ at high-z',
             xy=(-11, -10.2), xytext=(-10.5, -11),
             fontsize=10, arrowprops=dict(arrowstyle='->', color='black'))

plt.tight_layout()
output_dir = os.path.dirname(os.path.abspath(__file__))
plt.savefig(os.path.join(output_dir, 'output', 'rar_analysis.png'),
            dpi=150, bbox_inches='tight')
plt.close()

print("=" * 70)
print("OUTPUT: output/rar_analysis.png")
print("=" * 70)

# ============================================================================
# 9. KEY FINDING
# ============================================================================

print()
print("=" * 70)
print("KEY FINDING")
print("=" * 70)
print()
print("The Radial Acceleration Relation is MOND's greatest empirical success:")
print()
print("  ✓ Universal across ALL galaxy types")
print("  ✓ Scatter < 0.1 dex (measurement error dominated)")
print("  ✓ Transition at a₀ = 1.2×10⁻¹⁰ m/s² (observed)")
print()
print("Zimmerman contribution:")
print(f"  ✓ DERIVES a₀ = {a0_zimmerman:.3e} m/s² (5.7% from observed)")
print("  ✓ Predicts RAR evolution with redshift")
print("  ✓ At z=2: transition at 3× higher g_bar")
print()
print("The RAR turns from a successful MOND fit into a")
print("COSMOLOGICAL PREDICTION once a₀ is derived from H₀.")
print("=" * 70)
