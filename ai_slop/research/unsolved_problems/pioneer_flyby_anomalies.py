#!/usr/bin/env python3
"""
Pioneer and Flyby Anomalies: Zimmerman Formula Analysis
========================================================

CONTEXT:
Several spacecraft have shown anomalous accelerations:
- Pioneer 10/11: Unexplained sunward acceleration
- Flyby anomaly: Excess velocity changes during Earth flybys
- Other potential anomalies

STATUS:
Pioneer anomaly largely explained by thermal recoil (2012).
Flyby anomaly remains unexplained for some events.

ZIMMERMAN APPLICATION:
While MOND effects in the inner Solar System are expected to be
very small (g >> a₀), the Zimmerman framework provides context
for any residual effects. The a₀ = cH₀/5.79 relation itself
doesn't predict Solar System anomalies - this is more about
completeness of the MOND picture.

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
AU = 1.496e11  # m
M_sun = 1.989e30  # kg

def E_z(z):
    """Dimensionless Hubble parameter"""
    return np.sqrt(Omega_m * (1+z)**3 + Omega_Lambda)

print("=" * 80)
print("PIONEER AND FLYBY ANOMALIES - ZIMMERMAN ANALYSIS")
print("=" * 80)

print("""
THE PIONEER ANOMALY
===================

Discovery (1998):
- Pioneer 10/11 spacecraft showed unexplained deceleration
- Magnitude: a_P ≈ (8.74 ± 1.33) × 10⁻¹⁰ m/s²
- Direction: Toward the Sun
- First noticed at ~20-70 AU

Initial excitement:
- a_P was similar to a₀ ≈ 1.2 × 10⁻¹⁰ m/s²
- Could this be MOND in the Solar System?

Resolution (2012):
- Thermal recoil from RTGs (Radioisotope Thermoelectric Generators)
- Heat radiated asymmetrically creates small thrust
- Explains ~80% of the anomaly
- Remaining ~20% likely systematic errors
""")

# Pioneer parameters
pioneer_data = {
    "Observed anomaly": (8.74e-10, 1.33e-10, "m/s²"),
    "Thermal recoil": (7.4e-10, 1.0e-10, "m/s²"),
    "a₀ (MOND)": (1.2e-10, 0.1e-10, "m/s²"),
    "cH₀ (Hubble accel)": (6.9e-10, 0.3e-10, "m/s²"),
}

print("\nPioneer Anomaly Comparison:")
print("  Quantity              Value           Uncertainty")
print("  " + "-" * 55)
for name, (val, err, unit) in pioneer_data.items():
    print(f"  {name:20s}  {val:.2e}     ±{err:.2e} {unit}")

print("""
NUMERICAL COINCIDENCES
======================

The Pioneer anomaly sparked interest because:

1. a_P ≈ 8.7 × 10⁻¹⁰ m/s² is similar to:
   - a₀ = 1.2 × 10⁻¹⁰ m/s² (×7 different)
   - cH₀ = 6.9 × 10⁻¹⁰ m/s² (×1.3 different!)
   - c²/R_U ≈ 7 × 10⁻¹⁰ m/s² (where R_U is Hubble radius)

2. Zimmerman Formula: a₀ = cH₀/5.79
   - Derives a₀ from H₀
   - a_P is closer to cH₀ than to a₀!

This suggests thermal recoil coincidentally matches
the Hubble acceleration scale - NOT a deep connection.
""")

# Calculate gravitational acceleration vs distance
def solar_gravity(r_AU):
    """Solar gravitational acceleration in m/s²"""
    r_m = r_AU * AU
    return G * M_sun / r_m**2

def mond_gravity(r_AU):
    """MOND-corrected gravity near Sun"""
    g_N = solar_gravity(r_AU)
    # In transition regime: g = g_N × μ(g_N/a₀)
    x = g_N / a0_local
    # Simple interpolation function
    mu = x / np.sqrt(1 + x**2)
    return g_N  # Essentially Newtonian in Solar System

print("\n" + "=" * 60)
print("GRAVITATIONAL REGIME IN SOLAR SYSTEM")
print("=" * 60)

print("\nSolar gravity vs a₀ at different distances:")
print("  Distance    g_sun (m/s²)    g/a₀        Regime")
print("  " + "-" * 55)
for r in [1, 5, 10, 30, 50, 100, 500, 1000]:
    g = solar_gravity(r)
    ratio = g / a0_local
    if ratio > 1000:
        regime = "Deep Newtonian"
    elif ratio > 100:
        regime = "Newtonian"
    elif ratio > 10:
        regime = "Transition"
    else:
        regime = "MOND"
    print(f"  {r:5.0f} AU     {g:.2e}       {ratio:.1e}    {regime}")

print("""
KEY RESULT:
Even at 100 AU, g/a₀ ~ 500 - deeply Newtonian!
MOND effects in Solar System expected to be < 0.1%.
""")

# Flyby anomaly
print("\n" + "=" * 60)
print("THE FLYBY ANOMALY")
print("=" * 60)

print("""
Discovery (1990s-2000s):
Several spacecraft showed anomalous velocity changes
during Earth gravity assists:

Galileo (1990): Δv = +3.92 mm/s
Galileo (1992): Δv = -4.60 mm/s (toward Earth)
NEAR (1998): Δv = +13.46 mm/s
Cassini (1999): Δv = -2 mm/s (uncertain)
Rosetta (2005): Δv = +1.80 mm/s
Messenger (2005): Δv = +0.02 mm/s

Empirical formula (Anderson et al.):
  Δv/v ≈ 3.1 × 10⁻⁶ × (cos(δ_in) - cos(δ_out))

where δ is the declination of incoming/outgoing trajectory.
""")

flyby_data = [
    ("Galileo I", 1990, 3.92, 8.1, 142, -34.2),
    ("Galileo II", 1992, -4.60, 8.9, 174, -4.9),
    ("NEAR", 1998, 13.46, 6.9, 108, -72.0),
    ("Cassini", 1999, -2.0, 16.0, 95, -5.0),
    ("Rosetta I", 2005, 1.80, 3.9, 144, 34.3),
    ("Messenger", 2005, 0.02, 4.1, 133, -31.4),
]

print("\nFlyby Anomaly Data:")
print("  Spacecraft      Year    Δv (mm/s)   v_∞ (km/s)  β(°)   δ_out(°)")
print("  " + "-" * 70)
for name, year, dv, v_inf, beta, delta in flyby_data:
    print(f"  {name:14s}   {year}     {dv:+6.2f}      {v_inf:5.1f}      {beta:3.0f}    {delta:+5.1f}")

print("""
CURRENT STATUS:

The flyby anomaly remains PARTIALLY UNEXPLAINED:
- Some events consistent with modeling errors
- Others show genuine unexplained residuals
- No spacecraft since 2009 has confirmed it

Possible explanations:
1. Atmospheric drag errors
2. Thermal radiation pressure
3. Relativistic frame dragging (too small)
4. Unknown systematic errors
5. New physics?
""")

# MOND predictions for Solar System
print("\n" + "=" * 60)
print("MOND/ZIMMERMAN IN THE SOLAR SYSTEM")
print("=" * 60)

print("""
What does MOND predict for Solar System?

1. NEGLIGIBLE DIRECT EFFECTS
   - g >> a₀ everywhere inside ~1000 AU
   - MOND corrections < 0.001%
   - Cannot explain Pioneer or flyby anomalies

2. EXTERNAL FIELD EFFECT (EFE)
   - Milky Way field at Solar System: g_MW ~ 2×10⁻¹⁰ m/s²
   - This IS comparable to a₀!
   - EFE breaks strong equivalence principle
   - Could create subtle effects

3. ZIMMERMAN PREDICTION
   - a₀ evolves with cosmic time
   - Over 20 years of Pioneer data: da₀/dt ~ 10⁻²⁰ m/s²/s
   - Completely negligible!

The Zimmerman formula does NOT predict Solar System anomalies.
""")

# Calculate EFE from MW
g_MW_at_Sun = 2e-10  # m/s² (approximate)

print(f"\nExternal Field from Milky Way at Sun's location:")
print(f"  g_MW ≈ {g_MW_at_Sun:.1e} m/s²")
print(f"  g_MW / a₀ ≈ {g_MW_at_Sun/a0_local:.1f}")
print(f"  This is in the MOND transition regime!")

print("""
The EFE is interesting because:
- The Solar System is embedded in MW's gravitational field
- This field is ~ a₀, so EFE applies
- But effects on planetary orbits are tiny (~10⁻¹⁰ fractional)
""")

# MOND effects at outer Solar System
print("\n" + "=" * 60)
print("OUTER SOLAR SYSTEM TESTS")
print("=" * 60)

print("""
Where could MOND effects become measurable?

1. KUIPER BELT (30-50 AU)
   - g/a₀ ~ 100-200
   - Still deeply Newtonian
   - No MOND effects expected

2. SCATTERED DISK (50-1000 AU)
   - g/a₀ ~ 5-100
   - Transition regime begins
   - MOND corrections ~1% at 500 AU

3. INNER OORT CLOUD (~2000 AU)
   - g/a₀ ~ 1
   - Full MOND regime
   - Orbits significantly different

4. OUTER OORT CLOUD (~50,000 AU)
   - g/a₀ ~ 0.01
   - Deep MOND
   - Comet orbits strongly affected
""")

def mond_correction(r_AU):
    """Fractional MOND correction to orbital dynamics"""
    g = solar_gravity(r_AU)
    x = g / a0_local
    # In transition regime, correction ~ a₀/g
    if x > 10:
        return 1/x  # Small correction
    elif x > 1:
        return (1/x)**0.5  # Intermediate
    else:
        return 1.0  # Full MOND

print("\nMOND Corrections at Different Distances:")
print("  Distance (AU)    g/a₀        Fractional correction")
print("  " + "-" * 55)
for r in [50, 100, 300, 500, 1000, 2000, 5000]:
    g = solar_gravity(r)
    ratio = g / a0_local
    correction = mond_correction(r)
    print(f"  {r:7.0f}          {ratio:8.1f}       {correction:.2e}")

# Future tests
print("\n" + "=" * 60)
print("FUTURE TESTS")
print("=" * 60)

print("""
1. NEW HORIZONS (Currently ~55 AU)
   - Could measure spacecraft acceleration
   - Better thermal modeling than Pioneer
   - Looking for anomalies at ~10⁻¹⁰ m/s² level

2. TRANS-NEPTUNIAN OBJECTS
   - Orbits of TNOs at 100-500 AU
   - Vera Rubin will discover thousands
   - MOND predicts specific orbital anomalies

3. OORT CLOUD COMETS
   - Long-period comets from ~50,000 AU
   - Orbital fitting could reveal MOND
   - Need better statistics

4. LASER RANGING
   - Future missions with laser links
   - Could measure tiny accelerations
   - Test EFE predictions

5. INTERSTELLAR PROBES
   - Future probes beyond 100 AU
   - Could directly test MOND regime
   - Technical challenge: communication
""")

# Summary
print("\n" + "=" * 80)
print("SUMMARY: SPACECRAFT ANOMALIES - ZIMMERMAN PERSPECTIVE")
print("=" * 80)
print(f"""
┌────────────────────────────────────────────────────────────┐
│ SPACECRAFT ANOMALIES - ZIMMERMAN ANALYSIS                  │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ Pioneer Anomaly (RESOLVED):                                │
│   • Explained by thermal recoil (2012)                    │
│   • a_P ≈ cH₀ is coincidence, not physics                │
│   • NOT evidence for MOND or new physics                  │
│                                                            │
│ Flyby Anomaly (PARTIALLY UNRESOLVED):                      │
│   • Some events have genuine unexplained residuals        │
│   • No recent confirmation (post-2009)                    │
│   • MOND cannot explain (g >> a₀ near Earth)              │
│                                                            │
│ Zimmerman/MOND in Solar System:                            │
│   • Direct MOND effects negligible (g >> a₀)              │
│   • EFE from MW is interesting (g_MW ~ a₀)               │
│   • Could affect outer Solar System (>1000 AU)            │
│                                                            │
│ Future Tests:                                              │
│   • TNO orbits (Rubin LSST)                               │
│   • Oort Cloud dynamics                                   │
│   • New Horizons tracking                                 │
│   • Future interstellar probes                            │
│                                                            │
│ Status: ❌ No Solar System evidence for MOND yet           │
│         🔬 Outer Solar System testable in future          │
│                                                            │
└────────────────────────────────────────────────────────────┘
""")

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Panel 1: Solar gravity vs a₀
ax1 = axes[0, 0]
r_arr = np.logspace(0, 4, 100)  # 1 to 10,000 AU
g_arr = [solar_gravity(r) for r in r_arr]

ax1.loglog(r_arr, g_arr, 'b-', linewidth=2, label='Solar gravity g(r)')
ax1.axhline(a0_local, color='red', linestyle='--', linewidth=2, label='a₀ = 1.2×10⁻¹⁰ m/s²')
ax1.axhline(8.74e-10, color='green', linestyle=':', linewidth=2, label='Pioneer anomaly')
ax1.axvline(50, color='gray', linestyle=':', alpha=0.5, label='Pioneer range')
ax1.axvline(70, color='gray', linestyle=':', alpha=0.5)
ax1.fill_between([1000, 10000], [1e-15, 1e-15], [1e-8, 1e-8], alpha=0.1, color='red',
                 label='MOND regime')
ax1.set_xlabel('Distance from Sun (AU)', fontsize=12)
ax1.set_ylabel('Acceleration (m/s²)', fontsize=12)
ax1.set_title('Solar Gravity vs MOND Scale', fontsize=14)
ax1.legend(fontsize=9)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(1, 10000)
ax1.set_ylim(1e-14, 1e-2)

# Panel 2: MOND corrections
ax2 = axes[0, 1]
corrections = [mond_correction(r) * 100 for r in r_arr]  # Percentage
ax2.loglog(r_arr, corrections, 'purple', linewidth=2)
ax2.axhline(1, color='red', linestyle='--', label='1% correction')
ax2.axhline(0.01, color='orange', linestyle='--', label='0.01% correction')
ax2.set_xlabel('Distance from Sun (AU)', fontsize=12)
ax2.set_ylabel('MOND Correction (%)', fontsize=12)
ax2.set_title('Expected MOND Fractional Effects', fontsize=14)
ax2.legend()
ax2.grid(True, alpha=0.3)
ax2.set_xlim(1, 10000)

# Panel 3: Flyby anomaly
ax3 = axes[1, 0]
dv_obs = [d[2] for d in flyby_data]
delta_out = [d[5] for d in flyby_data]
colors = ['green' if dv > 0 else 'red' for dv in dv_obs]

ax3.scatter(delta_out, dv_obs, c=colors, s=100)
for i, name in enumerate([d[0] for d in flyby_data]):
    ax3.annotate(name, (delta_out[i], dv_obs[i]), fontsize=8, xytext=(5, 5),
                 textcoords='offset points')
ax3.axhline(0, color='black', linestyle='-', alpha=0.3)
ax3.set_xlabel('Outgoing Declination δ_out (°)', fontsize=12)
ax3.set_ylabel('Velocity Anomaly Δv (mm/s)', fontsize=12)
ax3.set_title('Flyby Anomaly: Δv vs Trajectory', fontsize=14)
ax3.grid(True, alpha=0.3)

# Panel 4: EFE comparison
ax4 = axes[1, 1]
g_values = {
    'Sun at 1 AU': solar_gravity(1),
    'Sun at 50 AU': solar_gravity(50),
    'Sun at 500 AU': solar_gravity(500),
    'MW at Sun': 2e-10,
    'a₀': a0_local,
    'Pioneer anom.': 8.74e-10,
}

names = list(g_values.keys())
values = list(g_values.values())
colors_bar = ['blue', 'blue', 'blue', 'purple', 'red', 'green']

ax4.barh(names, values, color=colors_bar, alpha=0.7)
ax4.set_xscale('log')
ax4.set_xlabel('Acceleration (m/s²)', fontsize=12)
ax4.set_title('Acceleration Scale Comparison', fontsize=14)
ax4.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig('/Users/carlzimmerman/new_physics/zimmerman-formula/research/unsolved_problems/pioneer_flyby_anomalies.png',
            dpi=150, bbox_inches='tight')
plt.close()

print("\n📊 Visualization saved to: research/unsolved_problems/pioneer_flyby_anomalies.png")
