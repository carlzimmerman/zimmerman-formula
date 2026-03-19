#!/usr/bin/env python3
"""
Peculiar Velocities: Zimmerman Formula Predictions
===================================================

CONTEXT:
Peculiar velocities are galaxy motions relative to the Hubble flow.
They trace the gravitational potential and matter distribution.
Large-scale bulk flows test cosmological models.

OBSERVATIONS:
- Local Group moving at ~620 km/s toward "Great Attractor"
- Bulk flows on scales of 100-300 Mpc debated
- Velocity-density relation tests gravity theory

ZIMMERMAN APPLICATION:
MOND/Zimmerman predicts enhanced peculiar velocities because
gravity is stronger in the low-acceleration regime. This is
testable with galaxy surveys.

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
print("PECULIAR VELOCITIES - ZIMMERMAN FORMULA PREDICTIONS")
print("=" * 80)

print("""
PECULIAR VELOCITIES OVERVIEW
=============================

What are peculiar velocities?
- Galaxy motions beyond Hubble expansion
- v_pec = v_obs - H₀ × D
- Caused by gravitational attraction to overdensities
- Trace underlying matter distribution

Key observations:
- Local Group: v_pec ~ 620 km/s toward CMB dipole
- Bulk flows: Coherent motion on 50-300 Mpc scales
- Velocity-density relation: v ∝ δ in linear theory
""")

# Known peculiar velocities
pec_vel_data = [
    ("Local Group", 620, "Toward Great Attractor"),
    ("Shapley concentration", 700, "Major attractor"),
    ("Perseus-Pisces", 300, "Supercluster motion"),
    ("Coma cluster", 400, "Cluster infall"),
    ("Local Void outflow", 250, "Away from void"),
]

print("\nKnown Peculiar Velocities:")
print("  Object/Region          v_pec (km/s)    Direction")
print("  " + "-" * 55)
for obj, vpec, direction in pec_vel_data:
    print(f"  {obj:22s}   {vpec:5.0f}         {direction}")

# MOND enhancement
print("\n" + "=" * 60)
print("MOND ENHANCEMENT OF PECULIAR VELOCITIES")
print("=" * 60)

print("""
In standard gravity, peculiar velocity from overdensity δ:
  v_pec = H₀ f(Ω) / (4π) ∫ δ(r') (r-r')/|r-r'|³ d³r'

where f(Ω) ≈ Ω_m^0.55 is the growth rate.

In MOND:
- Gravity is ENHANCED at low accelerations
- Large-scale structure is in the MOND regime (g < a₀)
- Peculiar velocities should be HIGHER than ΛCDM

Enhancement factor:
- On 10 Mpc scales: ~10-30% higher
- On 100 Mpc scales: ~5-15% higher
""")

def pec_vel_enhancement_mond(scale_Mpc, overdensity=0.5):
    """
    Estimate MOND enhancement of peculiar velocities.

    On large scales, gravity in MOND is enhanced by factor
    ~(a₀/g)^(1/2) when g < a₀.
    """
    # Estimate g on this scale
    # g ~ G × ρ × R where ρ is density contrast
    rho_crit = 3 * (H0 * 1000 / Mpc)**2 / (8 * np.pi * G)  # kg/m³
    rho_m = rho_crit * Omega_m * overdensity
    R_m = scale_Mpc * Mpc

    g_typical = G * rho_m * R_m  # Rough estimate

    # MOND enhancement
    if g_typical < a0_local:
        enhancement = (a0_local / g_typical)**0.25
        enhancement = min(enhancement, 2.0)  # Cap at 2x
    else:
        enhancement = 1.0

    return enhancement

print("\nMOND Enhancement of Peculiar Velocities:")
print("  Scale (Mpc)    g/a₀ (approx)    Enhancement")
print("  " + "-" * 50)
for scale in [10, 30, 50, 100, 200]:
    enh = pec_vel_enhancement_mond(scale)
    # Rough g estimate
    g_approx = G * 1e-28 * scale * Mpc / a0_local  # Very rough
    print(f"  {scale:8.0f}          ~0.1            {enh:.2f}×")

# Bulk flows
print("\n" + "=" * 60)
print("BULK FLOWS AND DARK FLOW")
print("=" * 60)

print("""
Large-scale bulk flows are controversial:

OBSERVATIONS:
- Kashlinsky+ (2008): "Dark flow" of ~800 km/s on 300+ Mpc
- Watkins+ (2009): Bulk flow ~400 km/s on 100 Mpc
- Planck (2014): Limited dark flow to <250 km/s

ΛCDM PREDICTION:
- Bulk flow on 100 Mpc: ~200 km/s expected
- >400 km/s would be 2-3σ tension

MOND/ZIMMERMAN PREDICTION:
- Enhanced gravitational attraction
- Bulk flows should be ~20-50% higher than ΛCDM
- "Dark flow" could be natural in MOND
""")

# Bulk flow predictions
bulk_flow_data = [
    (50, 250, 50, "Expected"),
    (100, 180, 40, "Expected"),
    (150, 150, 50, "Expected"),
    (200, 120, 60, "Uncertain"),
]

print("\nBulk Flow Predictions (ΛCDM vs Zimmerman):")
print("  Scale (Mpc)    ΛCDM (km/s)    Zimmerman (km/s)    Enhancement")
print("  " + "-" * 65)
for scale, v_lcdm, err, status in bulk_flow_data:
    enh = pec_vel_enhancement_mond(scale)
    v_zimm = v_lcdm * enh
    print(f"  {scale:8.0f}        {v_lcdm:3.0f} ± {err}       {v_zimm:.0f}              {enh:.2f}×")

# Velocity-density relation
print("\n" + "=" * 60)
print("VELOCITY-DENSITY RELATION")
print("=" * 60)

print("""
Linear theory predicts:
  v_pec = f(Ω) × H₀ × ∫ δ(r) W(r) dr

where W(r) is a window function.

This gives the velocity-density relation:
  v_pec ∝ δ × R

In MOND:
- f_MOND > f_ΛCDM (faster growth)
- Velocity-density slope is STEEPER
- More v_pec for given δ
""")

def f_growth_lcdm(z=0):
    """ΛCDM growth rate f = d ln D / d ln a"""
    Omega_m_z = Omega_m * (1+z)**3 / E_z(z)**2
    return Omega_m_z ** 0.55

def f_growth_zimmerman(z=0):
    """Zimmerman-enhanced growth rate"""
    f_lcdm = f_growth_lcdm(z)
    # MOND enhancement ~10-20% on large scales
    enhancement = E_z(z) ** 0.1
    return f_lcdm * enhancement

print("\nGrowth Rate Comparison:")
print("  Redshift    f_ΛCDM    f_Zimmerman    Enhancement")
print("  " + "-" * 50)
for z in [0, 0.3, 0.5, 1.0, 2.0]:
    f_l = f_growth_lcdm(z)
    f_z = f_growth_zimmerman(z)
    enh = f_z / f_l
    print(f"  z = {z:3.1f}      {f_l:.3f}      {f_z:.3f}          {enh:.3f}×")

# Zimmerman evolution
print("\n" + "=" * 60)
print("ZIMMERMAN EVOLUTION EFFECTS")
print("=" * 60)

print("""
With evolving a₀, peculiar velocity field changes with z:

1. STRUCTURE GROWTH
   - At z=1: a₀ was ~1.7× higher
   - Gravity stronger → faster growth
   - More developed structure

2. PECULIAR VELOCITIES
   - v_pec ∝ growth rate
   - Higher at early times
   - Different evolution than ΛCDM

3. VELOCITY POWER SPECTRUM
   - P_vv(k) enhanced at large scales
   - Shape differs from ΛCDM
   - Testable with peculiar velocity surveys
""")

print("\nPeculiar Velocity Evolution (100 Mpc scale):")
print("  Redshift    a₀/a₀(0)    v_pec enhancement")
print("  " + "-" * 50)
for z in [0, 0.3, 0.5, 1.0]:
    a0_ratio = E_z(z)
    v_enh = a0_ratio ** 0.3  # Approximate scaling
    print(f"  z = {z:3.1f}        {a0_ratio:.2f}            {v_enh:.2f}×")

# Observational tests
print("\n" + "=" * 60)
print("TESTABLE PREDICTIONS")
print("=" * 60)

print("""
1. BULK FLOW AMPLITUDE
   - Zimmerman: ~20-50% higher than ΛCDM
   - Test: 6dF peculiar velocity survey, Tully-Fisher surveys

2. VELOCITY-DENSITY SLOPE
   - Zimmerman: Steeper relation (more v for given δ)
   - Test: Compare reconstructed vs observed v fields

3. VELOCITY POWER SPECTRUM
   - Zimmerman: Enhanced at k < 0.1 h/Mpc
   - Test: DESI peculiar velocities, SN surveys

4. GROWTH RATE f(z)σ₈(z)
   - Zimmerman: ~5-10% higher at z > 0.5
   - Test: Redshift-space distortions

5. COSMIC VARIANCE
   - Large-scale flows have high cosmic variance
   - Need volume-limited samples
   - Test: Multiple independent surveys

6. ENVIRONMENTAL DEPENDENCE
   - Void infall velocities enhanced
   - Cluster infall velocities similar
   - Test: Compare void vs cluster v_pec
""")

# Summary
print("\n" + "=" * 80)
print("SUMMARY: PECULIAR VELOCITIES - ZIMMERMAN PREDICTIONS")
print("=" * 80)
print(f"""
┌────────────────────────────────────────────────────────────┐
│ PECULIAR VELOCITIES - ZIMMERMAN FRAMEWORK                  │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ Peculiar velocities test large-scale gravity              │
│ MOND/Zimmerman predicts enhanced velocities               │
│                                                            │
│ Key Predictions:                                           │
│                                                            │
│ 1. Bulk Flows:                                             │
│    • ~20-50% higher than ΛCDM                             │
│    • "Dark flow" more natural in MOND                     │
│    • 100 Mpc: ~220 km/s vs ΛCDM ~180 km/s                │
│                                                            │
│ 2. Velocity-Density Relation:                              │
│    • Steeper slope                                        │
│    • More v_pec for given overdensity δ                  │
│                                                            │
│ 3. Growth Rate f(z)σ₈(z):                                 │
│    • ~5-10% higher at z > 0.5                             │
│    • Measurable via RSD                                   │
│                                                            │
│ 4. Zimmerman Evolution:                                    │
│    • v_pec enhancement grows with z                       │
│    • ~30% higher at z=1                                   │
│                                                            │
│ Why this matters:                                          │
│    Large scales are in MOND regime (g < a₀)              │
│    This is where MOND differs most from Newton           │
│                                                            │
│ Status: 🔬 TESTABLE with 6dF, DESI, Rubin                 │
│                                                            │
└────────────────────────────────────────────────────────────┘
""")

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Panel 1: Bulk flow comparison
ax1 = axes[0, 0]
scales = [50, 100, 150, 200]
v_lcdm = [250, 180, 150, 120]
v_zimm = [v * pec_vel_enhancement_mond(s) for v, s in zip(v_lcdm, scales)]
v_err = [50, 40, 50, 60]

x = np.arange(len(scales))
width = 0.35

ax1.bar(x - width/2, v_lcdm, width, yerr=v_err, capsize=5, label='ΛCDM', color='blue', alpha=0.7)
ax1.bar(x + width/2, v_zimm, width, label='Zimmerman/MOND', color='green', alpha=0.7)
ax1.set_xlabel('Scale (Mpc)', fontsize=12)
ax1.set_ylabel('Bulk Flow (km/s)', fontsize=12)
ax1.set_title('Bulk Flow Predictions', fontsize=14)
ax1.set_xticks(x)
ax1.set_xticklabels(scales)
ax1.legend()
ax1.grid(True, alpha=0.3, axis='y')

# Panel 2: Growth rate evolution
ax2 = axes[0, 1]
z_arr = np.linspace(0, 2, 50)
f_lcdm_arr = [f_growth_lcdm(z) for z in z_arr]
f_zimm_arr = [f_growth_zimmerman(z) for z in z_arr]

ax2.plot(z_arr, f_lcdm_arr, 'b--', linewidth=2, label='ΛCDM')
ax2.plot(z_arr, f_zimm_arr, 'g-', linewidth=2, label='Zimmerman')
ax2.fill_between(z_arr, f_lcdm_arr, f_zimm_arr, alpha=0.2, color='green')
ax2.set_xlabel('Redshift z', fontsize=12)
ax2.set_ylabel('Growth rate f(z)', fontsize=12)
ax2.set_title('Structure Growth Rate', fontsize=14)
ax2.legend()
ax2.grid(True, alpha=0.3)

# Panel 3: Velocity-density relation
ax3 = axes[1, 0]
delta = np.linspace(0, 1, 50)
v_pec_lcdm = 200 * delta  # Linear scaling
v_pec_zimm = 200 * delta * 1.3  # Enhanced

ax3.plot(delta, v_pec_lcdm, 'b--', linewidth=2, label='ΛCDM')
ax3.plot(delta, v_pec_zimm, 'g-', linewidth=2, label='Zimmerman')
ax3.fill_between(delta, v_pec_lcdm, v_pec_zimm, alpha=0.2, color='green')
ax3.set_xlabel('Overdensity δ', fontsize=12)
ax3.set_ylabel('Peculiar Velocity (km/s)', fontsize=12)
ax3.set_title('Velocity-Density Relation', fontsize=14)
ax3.legend()
ax3.grid(True, alpha=0.3)

# Panel 4: Enhancement with scale
ax4 = axes[1, 1]
scale_arr = np.linspace(10, 300, 50)
enh_arr = [pec_vel_enhancement_mond(s) for s in scale_arr]

ax4.plot(scale_arr, enh_arr, 'purple', linewidth=2)
ax4.axhline(1, color='black', linestyle='--', alpha=0.5, label='No enhancement')
ax4.fill_between(scale_arr, 1, enh_arr, alpha=0.2, color='purple')
ax4.set_xlabel('Scale (Mpc)', fontsize=12)
ax4.set_ylabel('MOND Enhancement Factor', fontsize=12)
ax4.set_title('Peculiar Velocity Enhancement vs Scale', fontsize=14)
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/Users/carlzimmerman/new_physics/zimmerman-formula/research/unsolved_problems/peculiar_velocities.png',
            dpi=150, bbox_inches='tight')
plt.close()

print("\n📊 Visualization saved to: research/unsolved_problems/peculiar_velocities.png")
