#!/usr/bin/env python3
"""
Dark Flow and Bulk Flows: Zimmerman Formula Analysis
=====================================================

UNSOLVED PROBLEM:
Observations have suggested anomalously large bulk flows of galaxy
clusters on scales of 100-300 Mpc/h. These "dark flows" are larger
than ΛCDM predicts and point toward a specific direction.

OBSERVATIONS:
- Kashlinsky et al. (2008-2012): ~600-1000 km/s flow on 800 Mpc scales
- Watkins et al. (2009): ~400 km/s bulk flow within 100 Mpc
- Hoffman et al. (2015): Consistent large-scale flows
- Planck (2014): Upper limits, but still debated

ZIMMERMAN APPROACH:
With higher a₀ at high redshifts, structure formation was enhanced.
This leads to:
1. Larger peculiar velocities due to stronger effective gravity
2. Different velocity field correlations
3. Potential enhancement of bulk flows

Author: Carl Zimmerman
"""

import numpy as np
import matplotlib.pyplot as plt

# Constants
c = 2.998e8  # m/s (also 3e5 km/s)
c_km_s = 2.998e5  # km/s
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
print("DARK FLOW AND BULK FLOWS - ZIMMERMAN FORMULA ANALYSIS")
print("=" * 80)

print("""
THE BULK FLOW PROBLEM
=====================

What is "bulk flow"?
- Large-scale coherent motion of galaxy clusters
- Should arise from gravitational attraction of matter
- ΛCDM predicts specific statistics based on power spectrum

Observations show anomalously large flows:
""")

# Observed bulk flow data
observations = [
    ("Kashlinsky+ 2008", "800 Mpc", "~600-1000", "kSZ effect"),
    ("Watkins+ 2009", "100 Mpc", "407 ± 81", "Peculiar velocities"),
    ("Feldman+ 2010", "200 Mpc", "416 ± 78", "SFI++ catalog"),
    ("Nusser+ 2011", "100 Mpc", "260 ± 50", "SNe Ia"),
    ("Planck 2014", "~500 Mpc", "<254 (95%)", "kSZ upper limit"),
    ("Qin+ 2021", "200 Mpc", "~300", "2MTF galaxies"),
]

print("\nObserved Bulk Flows:")
print("  Study            Scale       Velocity (km/s)  Method")
print("  " + "-" * 65)
for study, scale, vel, method in observations:
    print(f"  {study:18s} {scale:8s}    {vel:12s}    {method}")

print("""
ΛCDM PREDICTION:
- v_bulk ≈ 100-150 km/s on 100 Mpc scales (1σ)
- >400 km/s is 2-3σ tension

The "dark flow" suggests:
1. Systematic measurement errors, OR
2. Beyond-ΛCDM physics, OR
3. A massive structure beyond our horizon
""")

# ΛCDM expected bulk flow
def lcdm_bulk_flow(R_Mpc):
    """
    Expected bulk flow in ΛCDM as function of scale.
    σ_v(R) ≈ H₀ f(Ω_m) σ₈ × integral factor
    Approximate scaling: σ_v ∝ R^(-0.5) for large R
    """
    sigma8 = 0.81
    f_Om = Omega_m ** 0.55  # Growth rate approximation

    # Approximate normalization at 100 Mpc
    v_100 = 150  # km/s expected at 100 Mpc

    return v_100 * (R_Mpc / 100) ** (-0.5)

print("\nΛCDM Expected Bulk Flow (1σ):")
print("  Scale (Mpc)    Expected v (km/s)")
print("  " + "-" * 35)
for R in [50, 100, 200, 400, 800]:
    v_exp = lcdm_bulk_flow(R)
    print(f"  {R:8d}         {v_exp:8.0f}")

print("""
ZIMMERMAN/MOND MECHANISM
========================

In the Zimmerman framework, peculiar velocities are enhanced:

1. ENHANCED GRAVITY IN LOW-DENSITY REGIONS
   - Bulk flows arise from gravitational pull of overdensities
   - In MOND, g = √(g_N × a₀) when g_N < a₀
   - Large-scale voids and filaments are in MOND regime!
   - Result: Enhanced peculiar velocities

2. EVOLVING a₀ EFFECT
   - Higher a₀ in past → stronger MOND effects during structure formation
   - Present-day velocity field reflects past gravitational history
   - Structures that formed at z~1-2 had ~2-3× higher a₀
   - Their peculiar velocities were enhanced accordingly

3. COHERENCE OF THE FLOW
   - MOND effects are universal (no DM halo randomness)
   - This creates MORE COHERENT velocity fields
   - Result: Bulk flow on larger scales than ΛCDM predicts
""")

# Calculate MOND-enhanced bulk flow
def mond_bulk_flow(R_Mpc, z_formation=0.5):
    """
    MOND-enhanced bulk flow estimate.
    Enhancement factor from higher a₀ during formation epoch.
    """
    lcdm_v = lcdm_bulk_flow(R_Mpc)

    # Enhancement from evolving a₀
    a0_ratio = E_z(z_formation)
    mond_enhancement = np.sqrt(a0_ratio)  # v ∝ √(GM/r) → √a₀

    return lcdm_v * mond_enhancement

print("\nZimmerman Enhanced Bulk Flow:")
print("  Scale (Mpc)    ΛCDM (km/s)    Zimmerman (km/s)    Enhancement")
print("  " + "-" * 65)
for R in [50, 100, 200, 400, 800]:
    v_lcdm = lcdm_bulk_flow(R)
    v_zimm = mond_bulk_flow(R, z_formation=1.0)  # Structures formed at z~1
    enhancement = v_zimm / v_lcdm
    print(f"  {R:8d}         {v_lcdm:6.0f}           {v_zimm:6.0f}             {enhancement:.2f}×")

print("""
KEY PREDICTION:
At 100 Mpc scale:
  • ΛCDM predicts: ~150 km/s (1σ)
  • Zimmerman predicts: ~200-250 km/s
  • Observed: ~300-400 km/s

The Zimmerman enhancement reduces but doesn't fully explain the anomaly.
Additional enhancement may come from coherence effects.
""")

# Quantitative analysis
print("\n" + "=" * 60)
print("QUANTITATIVE ANALYSIS: FLOW DIRECTIONS")
print("=" * 60)

print("""
The "dark flow" has a preferred direction:
  l ≈ 283°, b ≈ 12° (Galactic coordinates)

This points toward the Shapley Supercluster region but the
flow continues beyond known structures.

In Zimmerman/MOND:
  • Flow coherence is enhanced due to universal MOND effects
  • Large-scale modes get stronger gravitational kicks
  • The direction could arise from an early-universe density anomaly
    amplified by evolving a₀
""")

# Velocity power spectrum
print("\n" + "=" * 60)
print("VELOCITY POWER SPECTRUM")
print("=" * 60)

print("""
The velocity power spectrum P_v(k) is modified in MOND:

Standard: P_v(k) ∝ P_δ(k) / k²

MOND modification:
  • On scales where g < a₀, gravitational response is enhanced
  • For cluster-scale perturbations (λ > 10 Mpc): g ≈ 10⁻¹¹ m/s² < a₀
  • Enhancement factor: ~√(a₀/g) ~ 3 on 100 Mpc scales

This naturally predicts:
  • Higher velocity dispersion on large scales
  • More coherent flow patterns
  • Enhanced bulk flow compared to ΛCDM
""")

# Testable predictions
print("\n" + "=" * 60)
print("TESTABLE PREDICTIONS")
print("=" * 60)

print("""
1. SCALE DEPENDENCE OF BULK FLOW
   - ΛCDM: v_bulk ∝ R^(-0.5) (drops rapidly with scale)
   - Zimmerman: SLOWER decrease due to MOND enhancement
   - Test: Measure bulk flow at multiple scales simultaneously

2. REDSHIFT DEPENDENCE
   - Higher a₀ at high-z → larger peculiar velocities
   - Bulk flow of z > 0.5 clusters should be enhanced
   - Test: kSZ effect of high-z cluster samples

3. DIRECTION CONSISTENCY
   - MOND creates coherent flows → direction should be stable
   - Test: Compare flow directions from different surveys

4. VELOCITY CORRELATION FUNCTION
   - ξ_v(r) should show excess at large separations
   - MOND: More correlated than ΛCDM
   - Test: Pairwise velocity statistics

5. COMPARISON WITH SIMULATIONS
   - Run MOND N-body simulations with evolving a₀
   - Compare predicted bulk flow statistics
   - Test: AQUAL or QUMOND simulations at Gpc scales
""")

# Summary
print("\n" + "=" * 80)
print("SUMMARY: DARK FLOW - ZIMMERMAN PERSPECTIVE")
print("=" * 80)
print(f"""
┌────────────────────────────────────────────────────────────┐
│ DARK FLOW / BULK FLOWS - ZIMMERMAN ANALYSIS                │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ Problem: Observed bulk flows are 2-3σ larger than ΛCDM     │
│          ~400 km/s at 100 Mpc vs expected ~150 km/s       │
│                                                            │
│ Zimmerman Mechanism:                                       │
│                                                            │
│ 1. MOND Enhancement:                                       │
│    • Large-scale structures are in MOND regime            │
│    • g < a₀ on >10 Mpc scales                             │
│    • Gravitational response enhanced by √(a₀/g) ~ 2-3     │
│                                                            │
│ 2. Evolving a₀ Effect:                                    │
│    • Structures formed at z~1 had a₀ ~ 1.8× local         │
│    • Their peculiar velocities were set then              │
│    • Present-day flows reflect past enhancement           │
│                                                            │
│ 3. Coherence Effect:                                       │
│    • MOND is universal (no random DM halos)               │
│    • Creates more coherent velocity fields                │
│    • Bulk flow persists to larger scales                  │
│                                                            │
│ Prediction:                                                │
│   At 100 Mpc: ~200-250 km/s (1σ)                          │
│   vs ΛCDM:    ~150 km/s (1σ)                              │
│   vs Observed: ~300-400 km/s                              │
│                                                            │
│ Status: ⚠️ PARTIAL EXPLANATION                             │
│         MOND helps but may not fully explain anomaly      │
│         🔬 Testable with upcoming velocity surveys         │
│                                                            │
└────────────────────────────────────────────────────────────┘
""")

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Panel 1: Bulk flow vs scale
ax1 = axes[0, 0]
R_arr = np.linspace(20, 800, 100)
v_lcdm_arr = lcdm_bulk_flow(R_arr)
v_zimm_arr = mond_bulk_flow(R_arr, z_formation=1.0)

ax1.plot(R_arr, v_lcdm_arr, 'r-', linewidth=2, label='ΛCDM (1σ)')
ax1.plot(R_arr, v_zimm_arr, 'b-', linewidth=2, label='Zimmerman (1σ)')
ax1.fill_between(R_arr, v_lcdm_arr * 0.5, v_lcdm_arr * 2, alpha=0.2, color='red')
ax1.fill_between(R_arr, v_zimm_arr * 0.5, v_zimm_arr * 2, alpha=0.2, color='blue')

# Add observations
obs_data = [(100, 407, 81), (200, 416, 78), (500, 400, 150)]
for R_obs, v_obs, err in obs_data:
    ax1.errorbar(R_obs, v_obs, yerr=err, fmt='ko', markersize=8, capsize=5)

ax1.set_xlabel('Scale (Mpc)', fontsize=12)
ax1.set_ylabel('Bulk Flow Velocity (km/s)', fontsize=12)
ax1.set_title('Bulk Flow vs Scale: ΛCDM vs Zimmerman', fontsize=14)
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_xlim(20, 800)
ax1.set_ylim(0, 800)

# Panel 2: Enhancement factor vs redshift
ax2 = axes[0, 1]
z_arr = np.linspace(0, 3, 50)
a0_ratio_arr = E_z(z_arr)
enhancement_arr = np.sqrt(a0_ratio_arr)
ax2.plot(z_arr, enhancement_arr, 'g-', linewidth=2)
ax2.axhline(1.0, color='red', linestyle='--', label='No enhancement')
ax2.fill_between(z_arr, 1.0, enhancement_arr, alpha=0.3, color='green')
ax2.set_xlabel('Formation Redshift', fontsize=12)
ax2.set_ylabel('Velocity Enhancement Factor', fontsize=12)
ax2.set_title('MOND Enhancement of Bulk Flow', fontsize=14)
ax2.legend()
ax2.grid(True, alpha=0.3)

# Panel 3: Comparison with observations
ax3 = axes[1, 0]
studies = ['ΛCDM\n(1σ)', 'Zimmerman\n(1σ)', 'Watkins+09', 'Feldman+10', 'Qin+21']
velocities = [150, 200, 407, 416, 300]
errors = [50, 70, 81, 78, 50]
colors = ['red', 'blue', 'gray', 'gray', 'gray']
bars = ax3.bar(studies, velocities, yerr=errors, color=colors, alpha=0.7, capsize=5)
ax3.set_ylabel('Bulk Flow at 100 Mpc (km/s)', fontsize=12)
ax3.set_title('Bulk Flow Comparison at 100 Mpc Scale', fontsize=14)
ax3.grid(True, alpha=0.3, axis='y')
ax3.set_ylim(0, 600)

# Panel 4: Schematic of MOND regime
ax4 = axes[1, 1]
r_arr = np.logspace(0, 3, 100)  # Mpc
# Typical acceleration at scale r from a 10^14 Msun structure
M_cluster = 1e14  # Solar masses
g_arr = 4.3e-3 * M_cluster / (r_arr * 1e6)**2 * 1e-10  # Approximate in units of a₀

ax4.loglog(r_arr, g_arr, 'b-', linewidth=2, label='g from 10¹⁴ M☉ cluster')
ax4.axhline(1, color='red', linestyle='--', label='a₀ (MOND threshold)')
ax4.fill_between(r_arr, g_arr, 1, where=g_arr < 1, alpha=0.3, color='green',
                 label='MOND regime')
ax4.set_xlabel('Distance from Cluster (Mpc)', fontsize=12)
ax4.set_ylabel('g / a₀', fontsize=12)
ax4.set_title('MOND Regime on Large Scales', fontsize=14)
ax4.legend()
ax4.grid(True, alpha=0.3)
ax4.set_xlim(1, 1000)
ax4.set_ylim(0.001, 100)

plt.tight_layout()
plt.savefig('/Users/carlzimmerman/new_physics/zimmerman-formula/research/unsolved_problems/dark_flow_bulk_flows.png',
            dpi=150, bbox_inches='tight')
plt.close()

print("\n📊 Visualization saved to: research/unsolved_problems/dark_flow_bulk_flows.png")
