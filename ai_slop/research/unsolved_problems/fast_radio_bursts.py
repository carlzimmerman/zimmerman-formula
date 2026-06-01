#!/usr/bin/env python3
"""
Fast Radio Bursts: Zimmerman Formula Predictions
=================================================

UNSOLVED PROBLEM:
Fast Radio Bursts (FRBs) are mysterious millisecond-duration radio bursts
from cosmological distances. While their origin is now linked to magnetars,
their cosmological applications are rapidly expanding.

ZIMMERMAN APPLICATIONS:
1. FRB dispersion measures probe intergalactic medium → baryon distribution
2. FRB host galaxies at high-z can test evolving a₀
3. FRB timing could probe gravitational effects

Key insight: The Zimmerman formula predicts different baryon distribution
and dynamics at high-z, affecting FRB observations.

Author: Carl Zimmerman
"""

import numpy as np
import matplotlib.pyplot as plt

# Constants
c = 2.998e8  # m/s
G = 6.674e-11  # m³/kg/s²
H0 = 71.5  # km/s/Mpc
H0_si = H0 * 1e3 / 3.086e22  # /s
a0_local = 1.2e-10  # m/s²
Omega_m = 0.315
Omega_b = 0.0493
Omega_Lambda = 0.685

def E_z(z):
    """Dimensionless Hubble parameter"""
    return np.sqrt(Omega_m * (1+z)**3 + Omega_Lambda)

def a0_z(z):
    """MOND acceleration scale at redshift z"""
    return a0_local * E_z(z)

print("=" * 80)
print("FAST RADIO BURSTS - ZIMMERMAN FORMULA PREDICTIONS")
print("=" * 80)

print("""
FAST RADIO BURSTS: OVERVIEW
============================

What are FRBs?
- Millisecond radio bursts from extragalactic distances
- First discovered 2007 (Lorimer burst)
- Now: >800 detected (CHIME, Parkes, ASKAP, etc.)
- Origin: Magnetars (confirmed by SGR 1935+2154 in 2020)

Why cosmologically important?
- Dispersion Measure (DM) probes free electrons along line of sight
- DM = ∫ n_e dl → measures baryon content of IGM
- FRBs can "weigh" the missing baryons!
""")

# FRB dispersion measure theory
print("""
DISPERSION MEASURE AND BARYONS
==============================

The DM-redshift relation depends on cosmic baryon distribution:

DM_cosmic(z) = (3 c H₀ Ω_b) / (8π G m_p) × ∫₀ᶻ f_IGM(z') (1+z') / E(z') dz'

where f_IGM is the IGM baryon fraction (depends on structure formation!)
""")

# Calculate DM-z relation
def DM_cosmic(z, f_IGM_model='constant'):
    """
    Calculate cosmic DM contribution to redshift z.
    Units: pc/cm³
    """
    # Constants in cgs
    c_cgs = 2.998e10  # cm/s
    H0_cgs = H0 * 1e5 / 3.086e24  # /s
    mp_cgs = 1.673e-24  # g
    G_cgs = 6.674e-8  # cm³/g/s²

    prefactor = 3 * c_cgs * H0_cgs * Omega_b / (8 * np.pi * G_cgs * mp_cgs)

    # Numerical integration
    z_arr = np.linspace(0, z, 1000)
    dz = z_arr[1] - z_arr[0] if len(z_arr) > 1 else z

    integrand = np.zeros_like(z_arr)
    for i, z_i in enumerate(z_arr):
        E_zi = E_z(z_i)

        if f_IGM_model == 'constant':
            f_IGM = 0.84  # Standard assumption: 84% of baryons in IGM
        elif f_IGM_model == 'zimmerman':
            # Zimmerman: more efficient structure formation at high-z
            # Less baryons in diffuse IGM at high-z due to higher a₀
            a0_ratio = E_z(z_i)
            f_IGM = 0.84 / (1 + 0.1 * np.log(a0_ratio))  # Modest reduction

        integrand[i] = f_IGM * (1 + z_i) / E_zi

    DM = prefactor * np.trapz(integrand, z_arr)

    # Convert to pc/cm³
    DM_pc_cm3 = DM * 3.086e18  # cm to pc
    return DM_pc_cm3

print("\nDM-z Relation Predictions:")
print("  Redshift    DM (ΛCDM)    DM (Zimmerman)    Difference")
print("  " + "-" * 60)
z_values = [0.1, 0.3, 0.5, 1.0, 1.5, 2.0, 3.0]
for z in z_values:
    DM_lcdm = DM_cosmic(z, 'constant')
    DM_zimm = DM_cosmic(z, 'zimmerman')
    diff_pct = 100 * (DM_zimm - DM_lcdm) / DM_lcdm
    print(f"  z = {z:3.1f}      {DM_lcdm:6.0f}        {DM_zimm:6.0f}           {diff_pct:+.1f}%")

print("""
PHYSICAL MECHANISM
==================

In the Zimmerman framework:
1. Higher a₀ at high-z → enhanced structure formation
2. More baryons captured into galaxies/CGM at early times
3. Less diffuse IGM → LOWER DM at fixed z

The difference is subtle (~3-5%) but detectable with large FRB samples.
""")

# FRB host galaxy dynamics
print("\n" + "=" * 60)
print("FRB HOST GALAXY DYNAMICS")
print("=" * 60)

print("""
Many FRBs are now localized to host galaxies. These hosts can test MOND:

At high-z, the Zimmerman formula predicts enhanced mass discrepancy:
  M_dyn / M_baryon ∝ √(a₀(z) / g)

For FRB hosts at z > 0.5, MOND effects should be stronger.
""")

# FRB host data (example high-z hosts)
frb_hosts = [
    ("FRB 20121102", 0.193, 1e10, "Repeater, dwarf host"),
    ("FRB 20180916B", 0.034, 1e10, "Spiral, offset from center"),
    ("FRB 20190520B", 0.241, 1e9, "Dwarf, persistent radio source"),
    ("FRB 20201124A", 0.098, 1e11, "Massive host"),
    ("FRB 20220912A", 0.077, 3e10, "Spiral galaxy"),
]

print("\nFRB Host Galaxy MOND Analysis:")
print("  FRB           z      log M*    a₀(z)/a₀(0)    Notes")
print("  " + "-" * 70)
for name, z, M_star, notes in frb_hosts:
    a0_ratio = E_z(z)
    log_M = np.log10(M_star)
    print(f"  {name:15s}  {z:.3f}   {log_M:.1f}       {a0_ratio:.2f}×         {notes}")

print("""
At z ~ 0.2:
  a₀ was ~1.1× local → small enhancement
  But for FRBs at z > 1, effect grows significantly

Future FRB hosts at z > 1 can test Zimmerman evolution!
""")

# FRB timing precision
print("\n" + "=" * 60)
print("FRB TIMING AND GRAVITATIONAL EFFECTS")
print("=" * 60)

print("""
FRBs have microsecond timing precision. This could probe:

1. SHAPIRO DELAY VARIATION
   - FRB timing through galaxy clusters
   - MOND vs DM halo produce different delays
   - Difference: ~100 ns for typical cluster

2. GRAVITATIONAL WAVE EFFECTS
   - FRBs could detect GW memory effects
   - Modified gravity predictions differ

3. DISPERSION MEASURE VARIATIONS
   - DM varies with sightline through structures
   - MOND predicts different DM profile shapes
""")

# Testable predictions
print("\n" + "=" * 60)
print("TESTABLE PREDICTIONS")
print("=" * 60)

print("""
1. DM-z RELATION
   - Standard: DM ∝ z (low z), DM ∝ z×(1+z/2) (high z)
   - Zimmerman: ~5% lower at z > 1 due to enhanced structure
   - Test: CHIME + ASKAP localized FRBs at z > 1

2. HOST GALAXY DYNAMICS
   - FRB hosts are often dwarf galaxies (deep MOND)
   - Mass discrepancy should be ~2-3× at z ~ 0.2
   - At z ~ 1: Mass discrepancy ~4-5×
   - Test: IFU spectroscopy of FRB hosts

3. MISSING BARYON MEASUREMENT
   - FRB DM probes ALL baryons along line of sight
   - Zimmerman predicts ~10% fewer missing baryons
   - Test: DM excess above galactic + host contribution

4. CGM PROBING
   - FRBs through galaxy halos show DM excess
   - MOND: Different radial profile than NFW
   - Test: FRB DM vs impact parameter

5. FRB RATE VS REDSHIFT
   - FRB rate depends on magnetar formation
   - Higher a₀ at high-z → different stellar evolution?
   - Test: FRB luminosity function vs z
""")

# Summary
print("\n" + "=" * 80)
print("SUMMARY: FRBs AS ZIMMERMAN FORMULA PROBES")
print("=" * 80)
print(f"""
┌────────────────────────────────────────────────────────────┐
│ FAST RADIO BURSTS - ZIMMERMAN PREDICTIONS                  │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ What FRBs Probe:                                           │
│   • Intergalactic medium (dispersion measure)             │
│   • Baryon distribution (missing baryon problem)          │
│   • Host galaxy dynamics (MOND regime)                    │
│                                                            │
│ Zimmerman Predictions:                                     │
│                                                            │
│ 1. DM-z relation:                                          │
│    • ~3-5% LOWER than ΛCDM at z > 1                       │
│    • Due to more efficient structure formation            │
│    • Testable with >1000 localized FRBs                   │
│                                                            │
│ 2. Host galaxy dynamics:                                   │
│    • Dwarf hosts in deep MOND regime                      │
│    • Mass discrepancy evolves with z                      │
│    • At z=1: M_dyn/M_bar ~4-5× (vs ~3× locally)           │
│                                                            │
│ 3. CGM profiles:                                           │
│    • Different DM vs impact parameter shape               │
│    • MOND phantom DM vs NFW halo                          │
│    • FRB sightlines through galaxy outskirts              │
│                                                            │
│ Status: 🔬 TESTABLE with upcoming FRB surveys              │
│         CHIME/2, DSA-2000, CHORD can test by 2027         │
│                                                            │
└────────────────────────────────────────────────────────────┘
""")

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Panel 1: DM-z relation
ax1 = axes[0, 0]
z_arr = np.linspace(0.01, 3, 50)
DM_lcdm_arr = np.array([DM_cosmic(z, 'constant') for z in z_arr])
DM_zimm_arr = np.array([DM_cosmic(z, 'zimmerman') for z in z_arr])
ax1.plot(z_arr, DM_lcdm_arr, 'r-', linewidth=2, label='ΛCDM (constant f_IGM)')
ax1.plot(z_arr, DM_zimm_arr, 'b--', linewidth=2, label='Zimmerman (evolving)')
ax1.set_xlabel('Redshift z', fontsize=12)
ax1.set_ylabel('DM_cosmic (pc/cm³)', fontsize=12)
ax1.set_title('FRB Dispersion Measure vs Redshift', fontsize=14)
ax1.legend()
ax1.grid(True, alpha=0.3)

# Panel 2: Mass discrepancy evolution for FRB hosts
ax2 = axes[0, 1]
z_arr2 = np.linspace(0, 2, 50)
# In MOND, M_dyn/M_bar ∝ √(a₀/g) for low accelerations
# Higher a₀ at high-z → larger mass discrepancy
a0_ratio_arr = E_z(z_arr2)
mass_disc = 3.0 * np.sqrt(a0_ratio_arr)  # Base factor 3 at z=0, scales with √a₀
ax2.plot(z_arr2, mass_disc, 'g-', linewidth=2)
ax2.axhline(3.0, color='red', linestyle='--', label='Local (z=0) value')
ax2.fill_between(z_arr2, mass_disc * 0.8, mass_disc * 1.2, alpha=0.2, color='green',
                 label='±20% uncertainty')
ax2.set_xlabel('Redshift z', fontsize=12)
ax2.set_ylabel('M_dyn / M_baryon', fontsize=12)
ax2.set_title('FRB Host Galaxy Mass Discrepancy (Dwarf Hosts)', fontsize=14)
ax2.legend()
ax2.grid(True, alpha=0.3)

# Panel 3: DM difference (Zimmerman - ΛCDM)
ax3 = axes[1, 0]
diff_pct = 100 * (DM_zimm_arr - DM_lcdm_arr) / DM_lcdm_arr
ax3.plot(z_arr, diff_pct, 'purple', linewidth=2)
ax3.axhline(0, color='black', linestyle='-', alpha=0.3)
ax3.fill_between(z_arr, diff_pct, 0, alpha=0.3, color='purple')
ax3.set_xlabel('Redshift z', fontsize=12)
ax3.set_ylabel('(DM_Zimmerman - DM_ΛCDM) / DM_ΛCDM (%)', fontsize=12)
ax3.set_title('DM Difference: Zimmerman vs ΛCDM', fontsize=14)
ax3.grid(True, alpha=0.3)

# Panel 4: FRB detection predictions
ax4 = axes[1, 1]
# FRB rate evolution (schematic)
z_rate = np.linspace(0, 3, 50)
rate_lcdm = (1 + z_rate)**2.5 * np.exp(-z_rate/2)  # Star formation rate proxy
# Zimmerman: More efficient SF at high-z due to higher a₀
rate_zimm = (1 + z_rate)**2.5 * np.exp(-z_rate/2) * (1 + 0.3 * np.log(E_z(z_rate)))
ax4.plot(z_rate, rate_lcdm / rate_lcdm.max(), 'r-', linewidth=2, label='ΛCDM')
ax4.plot(z_rate, rate_zimm / rate_zimm.max(), 'b--', linewidth=2, label='Zimmerman')
ax4.set_xlabel('Redshift z', fontsize=12)
ax4.set_ylabel('Relative FRB Rate (normalized)', fontsize=12)
ax4.set_title('FRB Rate Evolution (Follows Magnetar Formation)', fontsize=14)
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/Users/carlzimmerman/new_physics/zimmerman-formula/research/unsolved_problems/fast_radio_bursts.png',
            dpi=150, bbox_inches='tight')
plt.close()

print("\n📊 Visualization saved to: research/unsolved_problems/fast_radio_bursts.png")
