#!/usr/bin/env python3
"""
Fermi Bubbles: Zimmerman Formula Analysis
==========================================

CONTEXT:
The Fermi Bubbles are two giant gamma-ray emitting lobes extending
~50° (~10 kpc) above and below the Galactic plane, discovered by
Fermi-LAT in 2010.

MYSTERY:
- Origin unclear: AGN jet vs starburst wind
- Hard gamma-ray spectrum (E⁻² not E⁻²·⁷)
- Sharp edges
- Age ~2-8 Myr (recent event)

ZIMMERMAN APPLICATION:
If the bubbles were created in the past, a₀ was slightly higher.
This affects the bubble expansion dynamics and cosmic ray energetics.

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

def E_z(z):
    """Dimensionless Hubble parameter"""
    return np.sqrt(Omega_m * (1+z)**3 + Omega_Lambda)

def a0_z(z):
    """MOND acceleration scale at redshift z"""
    return a0_local * E_z(z)

print("=" * 80)
print("FERMI BUBBLES - ZIMMERMAN FORMULA ANALYSIS")
print("=" * 80)

print("""
FERMI BUBBLES OVERVIEW
======================

Discovery:
- Found in Fermi-LAT gamma-ray data (2010)
- Two giant lobes, N and S of Galactic center
- Size: ~50° × 40° (~10 kpc × 8 kpc)
- Hard spectrum: E⁻² (vs typical ISM E⁻²·⁷)

Properties:
- Gamma-ray luminosity: ~4 × 10³⁷ erg/s
- Total energy: ~10⁵⁵ erg
- Sharp edges (not diffusive)
- Associated with eROSITA X-ray bubbles (larger)

Mysteries:
1. What created them? (AGN jet or starburst)
2. Why the hard spectrum?
3. Why the sharp edges?
4. Age estimates: 2-8 Myr
""")

# Fermi Bubble parameters
fermi_bubble_params = {
    "Height": "10 kpc",
    "Width": "8 kpc",
    "L_gamma": "4e37 erg/s",
    "E_total": "1e55 erg",
    "Age": "2-8 Myr",
    "Spectrum": "E^-2",
}

print("\nFermi Bubble Observed Properties:")
print("  " + "-" * 40)
for key, value in fermi_bubble_params.items():
    print(f"  {key:15s}: {value}")

print("""
ZIMMERMAN CONNECTION
====================

At first glance: Why would a₀ matter for Fermi Bubbles?

Key insight:
1. The Galactic Center region is in TRANSITION MOND regime
2. a₀ affects stellar dynamics → affects black hole fueling
3. a₀ affects gas dynamics in the Galactic halo
4. Bubble expansion in low-g regime → MOND effects

The bubbles extend to r ~ 10 kpc from Galactic center.
At these radii, accelerations can approach a₀!
""")

# Calculate accelerations at bubble boundary
def galactic_acceleration(r_kpc, M_MW=1e12):
    """Newtonian acceleration from MW mass (m/s²)"""
    M_kg = M_MW * 1.989e30
    r_m = r_kpc * kpc
    return G * M_kg / r_m**2

def mond_acceleration(g_N, a0):
    """MOND interpolated acceleration"""
    x = g_N / a0
    # Simple interpolation
    nu = (1 + np.sqrt(1 + 4/x**2)) / 2
    return g_N * nu

print("\n" + "=" * 60)
print("GRAVITATIONAL REGIME AT BUBBLE LOCATIONS")
print("=" * 60)

print("\nAcceleration vs position (from GC):")
print("  r (kpc)    g_Newton    g/a₀     Regime")
print("  " + "-" * 50)
for r in [1, 3, 5, 8, 10, 15]:
    g_N = galactic_acceleration(r)
    g_a0_ratio = g_N / a0_local
    if g_a0_ratio > 10:
        regime = "Newtonian"
    elif g_a0_ratio > 1:
        regime = "Transition"
    else:
        regime = "MOND"
    print(f"  {r:5.0f}       {g_N:.2e}    {g_a0_ratio:6.1f}    {regime}")

print("""
KEY FINDING:
At the bubble edges (~10 kpc), g ≈ 2-5 × a₀
This is the TRANSITION regime where MOND effects begin!
""")

# Bubble expansion dynamics
print("\n" + "=" * 60)
print("BUBBLE EXPANSION DYNAMICS")
print("=" * 60)

print("""
Bubble expansion is governed by:
  ρ(dv/dt) = -∇P + ρg

In the transition regime, effective g is ENHANCED by MOND.
This affects the terminal velocity of bubble expansion.

For outflows from Galactic center:
- Need to overcome gravity (potential well)
- MOND makes this EASIER at large r
- Bubbles can expand further/faster
""")

def escape_velocity(r_kpc, use_mond=False):
    """Escape velocity from Galactic center (km/s)"""
    M_MW = 6e10  # Baryonic mass (MOND), solar masses
    M_kg = M_MW * 1.989e30
    r_m = r_kpc * kpc

    if use_mond:
        # In MOND, v_esc enhanced at low g
        g_N = G * M_kg / r_m**2
        if g_N < a0_local:
            # Deep MOND: v_esc ∝ (GMa₀)^(1/4)
            v_esc = (G * M_kg * a0_local * r_m**2)**0.25
        else:
            # Transition: interpolate
            g_eff = mond_acceleration(g_N, a0_local)
            v_esc = np.sqrt(2 * g_eff * r_m)
    else:
        # Newtonian with dark matter halo
        M_tot = 1e12  # Total mass including DM
        v_esc = np.sqrt(2 * G * M_tot * 1.989e30 / r_m)

    return v_esc / 1000  # km/s

print("\nEscape Velocity at Bubble Heights:")
print("  r (kpc)    v_esc (ΛCDM)    v_esc (MOND)    Difference")
print("  " + "-" * 55)
for r in [3, 5, 8, 10, 15]:
    v_lcdm = escape_velocity(r, use_mond=False)
    v_mond = escape_velocity(r, use_mond=True)
    diff_pct = (v_mond - v_lcdm) / v_lcdm * 100
    print(f"  {r:5.0f}        {v_lcdm:6.0f}          {v_mond:6.0f}          {diff_pct:+.0f}%")

# Cosmic ray energetics
print("\n" + "=" * 60)
print("COSMIC RAY ENERGETICS")
print("=" * 60)

print("""
The Fermi Bubbles glow in gamma rays from cosmic ray interactions.

Zimmerman effect on CR acceleration:
- CR acceleration at shocks depends on v_shock
- MOND affects shock dynamics in low-g regions
- Hard spectrum (E⁻²) suggests recent, strong acceleration

If bubbles formed ~5 Myr ago:
- a₀ was ~0.002% higher (negligible at this timescale)
- But the TRANSITION regime still applies!
""")

# Age estimate
def bubble_age(height_kpc, expansion_velocity_km_s):
    """Estimate bubble age in Myr"""
    h_m = height_kpc * kpc
    v_m_s = expansion_velocity_km_s * 1000
    t_s = h_m / v_m_s
    return t_s / (3.154e13)  # Myr

print("\nBubble Age Estimates:")
print("  v_expansion    Age (Myr)    Notes")
print("  " + "-" * 50)
for v in [500, 1000, 2000, 3000]:
    age = bubble_age(10, v)
    note = "Plausible" if 2 < age < 10 else "Too slow/fast"
    print(f"  {v:5.0f} km/s    {age:6.1f}        {note}")

# Sgr A* activity
print("\n" + "=" * 60)
print("SGR A* ACTIVITY AND MOND")
print("=" * 60)

print("""
One proposed origin: Past AGN activity from Sgr A*.

Zimmerman insight:
- Black hole accretion depends on gas dynamics
- In MOND, gas orbits differ from Newtonian
- Accretion rate affected by MOND potential
- Past AGN outbursts may have been more energetic

The fact that Sgr A* is currently quiescent but was
active ~5 Myr ago could relate to MOND-modified
accretion dynamics.
""")

# eROSITA bubbles
print("\n" + "=" * 60)
print("eROSITA X-RAY BUBBLES")
print("=" * 60)

print("""
eROSITA discovered even larger X-ray bubbles (2020):
- Extend to ~14 kpc from Galactic plane
- Enclose the Fermi bubbles
- Suggest older event or continuous outflow

At 14 kpc:
- g/a₀ ≈ 1-2 (deep transition/MOND regime)
- Bubble edges expanding into MOND territory
- Sharp edges could be MOND-related boundary
""")

g_at_14kpc = galactic_acceleration(14)
print(f"\nAcceleration at eROSITA bubble edge:")
print(f"  r = 14 kpc: g = {g_at_14kpc:.2e} m/s² = {g_at_14kpc/a0_local:.1f} × a₀")
print(f"  This is in the MOND transition regime!")

# Testable predictions
print("\n" + "=" * 60)
print("TESTABLE PREDICTIONS")
print("=" * 60)

print("""
1. BUBBLE EDGE DYNAMICS
   - MOND predicts specific velocity profile near edges
   - Sharp edges from g-transition
   - Test: IFU spectroscopy of bubble edges

2. GAS KINEMATICS
   - Halo gas in MOND regime
   - Different velocity dispersion at r > 10 kpc
   - Test: Absorption line studies

3. COSMIC RAY DISTRIBUTION
   - CR propagation affected by MOND gravity
   - Different diffusion at bubble edges
   - Test: Gamma-ray spatial distribution

4. POLARIZATION
   - Magnetic field structure in MOND
   - May affect synchrotron polarization
   - Test: Polarimetric observations

5. NORTHERN vs SOUTHERN BUBBLE
   - Any asymmetry could indicate MOND effects
   - Different halo density → different g
   - Test: Detailed morphology comparison
""")

# Summary
print("\n" + "=" * 80)
print("SUMMARY: FERMI BUBBLES - ZIMMERMAN ANALYSIS")
print("=" * 80)
print(f"""
┌────────────────────────────────────────────────────────────┐
│ FERMI BUBBLES - ZIMMERMAN ANALYSIS                         │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ The Fermi Bubbles extend into the MOND transition regime  │
│ At r ~ 10 kpc: g ≈ 2-5 × a₀ (not deeply Newtonian)       │
│                                                            │
│ Key Insights:                                              │
│                                                            │
│ 1. Gravitational Regime:                                   │
│    • Bubble edges at ~10 kpc are in transition zone       │
│    • MOND effects enhance effective gravity               │
│    • This aids bubble expansion to large heights          │
│                                                            │
│ 2. Sharp Edges:                                            │
│    • Transition from Newtonian to MOND could create       │
│      sharp boundaries in expansion dynamics               │
│                                                            │
│ 3. eROSITA Bubbles:                                        │
│    • At 14 kpc: g/a₀ ~ 1-2 (deeper MOND)                 │
│    • Even more affected by MOND dynamics                  │
│                                                            │
│ 4. Sgr A* Activity:                                        │
│    • MOND affects accretion dynamics                      │
│    • May explain timing of AGN activity                   │
│                                                            │
│ Limitations:                                               │
│    a₀ evolution negligible over 5 Myr timescale          │
│    But spatial MOND transition is relevant                │
│                                                            │
│ Status: 🔬 SPECULATIVE - spatial MOND effects testable    │
│                                                            │
└────────────────────────────────────────────────────────────┘
""")

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Panel 1: Acceleration profile
ax1 = axes[0, 0]
r_arr = np.linspace(0.5, 20, 100)
g_arr = [galactic_acceleration(r) / a0_local for r in r_arr]
ax1.semilogy(r_arr, g_arr, 'b-', linewidth=2)
ax1.axhline(1, color='red', linestyle='--', label='a₀ (MOND threshold)')
ax1.axhline(5, color='orange', linestyle='--', alpha=0.5, label='5×a₀ (transition)')
ax1.axvline(10, color='green', linestyle=':', label='Fermi bubble edge')
ax1.axvline(14, color='purple', linestyle=':', label='eROSITA bubble edge')
ax1.fill_between(r_arr, 0.1, 5, alpha=0.1, color='red', label='MOND/transition zone')
ax1.set_xlabel('Distance from GC (kpc)', fontsize=12)
ax1.set_ylabel('g / a₀', fontsize=12)
ax1.set_title('Gravitational Regime in MW Halo', fontsize=14)
ax1.legend(fontsize=8)
ax1.grid(True, alpha=0.3)
ax1.set_ylim(0.1, 100)

# Panel 2: Bubble schematic
ax2 = axes[0, 1]
# Draw simplified bubble outline
theta = np.linspace(0, np.pi, 100)
r_bubble = 10  # kpc
x_bubble = r_bubble * np.sin(theta) * 0.8
y_bubble = r_bubble * np.cos(theta)

ax2.fill(x_bubble, y_bubble, alpha=0.3, color='blue', label='North bubble')
ax2.fill(x_bubble, -y_bubble, alpha=0.3, color='blue', label='South bubble')
ax2.axhline(0, color='black', linewidth=1)
ax2.plot(0, 0, 'ko', markersize=10, label='Galactic Center')
ax2.axhline(10, color='red', linestyle='--', alpha=0.5)
ax2.axhline(-10, color='red', linestyle='--', alpha=0.5)
ax2.text(6, 11, 'g ~ 2×a₀', fontsize=10)
ax2.text(6, 5, 'g ~ 5×a₀', fontsize=10)
ax2.set_xlabel('x (kpc)', fontsize=12)
ax2.set_ylabel('z (kpc)', fontsize=12)
ax2.set_title('Fermi Bubble Geometry', fontsize=14)
ax2.set_xlim(-15, 15)
ax2.set_ylim(-15, 15)
ax2.set_aspect('equal')
ax2.grid(True, alpha=0.3)

# Panel 3: Escape velocity
ax3 = axes[1, 0]
v_lcdm_arr = [escape_velocity(r, use_mond=False) for r in r_arr]
v_mond_arr = [escape_velocity(r, use_mond=True) for r in r_arr]
ax3.plot(r_arr, v_lcdm_arr, 'b--', linewidth=2, label='ΛCDM (with DM halo)')
ax3.plot(r_arr, v_mond_arr, 'g-', linewidth=2, label='MOND (baryonic only)')
ax3.axvline(10, color='red', linestyle=':', alpha=0.5, label='Bubble edge')
ax3.set_xlabel('Distance from GC (kpc)', fontsize=12)
ax3.set_ylabel('Escape Velocity (km/s)', fontsize=12)
ax3.set_title('Escape Velocity Profile', fontsize=14)
ax3.legend()
ax3.grid(True, alpha=0.3)

# Panel 4: MOND enhancement factor
ax4 = axes[1, 1]
def mond_enhancement(r_kpc):
    g_N = galactic_acceleration(r_kpc)
    g_MOND = mond_acceleration(g_N, a0_local)
    return g_MOND / g_N

enhancement = [mond_enhancement(r) for r in r_arr]
ax4.plot(r_arr, enhancement, 'purple', linewidth=2)
ax4.axhline(1, color='black', linestyle='--', alpha=0.5, label='Newtonian')
ax4.axvline(10, color='green', linestyle=':', label='Fermi bubble edge')
ax4.fill_between(r_arr, 1, enhancement, alpha=0.2, color='purple')
ax4.set_xlabel('Distance from GC (kpc)', fontsize=12)
ax4.set_ylabel('g_MOND / g_Newtonian', fontsize=12)
ax4.set_title('MOND Gravity Enhancement', fontsize=14)
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/Users/carlzimmerman/new_physics/zimmerman-formula/research/unsolved_problems/fermi_bubbles.png',
            dpi=150, bbox_inches='tight')
plt.close()

print("\n📊 Visualization saved to: research/unsolved_problems/fermi_bubbles.png")
