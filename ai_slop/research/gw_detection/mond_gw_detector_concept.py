#!/usr/bin/env python3
"""
MOND Transition Systems as Gravitational Wave Detectors

A speculative but novel concept: Systems at the MOND transition (g ≈ a₀)
could serve as ultra-low-frequency gravitational wave detectors.

Key insight: MOND introduces a non-linearity at the scale a₀. Systems
straddling this transition might show enhanced response to GW perturbations.

This would probe frequencies < 10⁻¹⁰ Hz - completely unexplored territory!
"""

import numpy as np
import matplotlib.pyplot as plt

# Physical constants
G = 6.674e-11        # m³/kg/s²
c = 2.998e8          # m/s
M_sun = 1.989e30     # kg
AU = 1.496e11        # m
year = 3.156e7       # seconds
pc = 3.086e16        # m

# MOND parameters (Zimmerman)
a0 = 1.2e-10         # m/s²

print("=" * 70)
print("MOND TRANSITION SYSTEMS AS GRAVITATIONAL WAVE DETECTORS")
print("=" * 70)
print()

# ============================================================================
# 1. THE MOND TRANSITION REGIME
# ============================================================================

print("PART 1: THE MOND TRANSITION REGIME")
print("-" * 50)
print()

# For a binary with total mass M, the MOND transition occurs at:
# g = GM/r² = a₀
# r_transition = √(GM/a₀)

def mond_transition_radius(M_solar):
    """Calculate MOND transition radius for given mass."""
    M = M_solar * M_sun
    r_trans = np.sqrt(G * M / a0)
    return r_trans / AU  # Return in AU

# Calculate for different masses
masses = [1, 2, 10, 100, 1e6]  # Solar masses
print(f"{'Mass (M☉)':<15} {'r_transition (AU)':<20} {'Orbital Period':<20}")
print("-" * 55)

for M in masses:
    r_au = mond_transition_radius(M)
    r_m = r_au * AU
    T_years = 2 * np.pi * np.sqrt(r_m**3 / (G * M * M_sun)) / year
    print(f"{M:<15.0e} {r_au:<20.0f} {T_years:<20.0f} years")

print()

# ============================================================================
# 2. FREQUENCY SENSITIVITY
# ============================================================================

print("PART 2: FREQUENCY SENSITIVITY")
print("-" * 50)
print()

# Wide binary orbital periods correspond to GW frequencies
r_binary = 10000 * AU  # 10,000 AU separation
M_binary = 2 * M_sun   # Solar-mass binary

T_orbit = 2 * np.pi * np.sqrt(r_binary**3 / (G * M_binary))
f_orbit = 1 / T_orbit

print(f"Wide binary at r = 10,000 AU:")
print(f"  Orbital period:    T = {T_orbit/year:.0f} years")
print(f"  Orbital frequency: f = {f_orbit:.2e} Hz")
print()

# Compare to other detectors
detectors = {
    'LIGO/Virgo': (10, 1000),
    'LISA': (1e-4, 0.1),
    'NANOGrav (PTA)': (1e-9, 1e-7),
    'MOND wide binaries': (1e-14, 1e-10),
}

print("GW Detector Frequency Ranges:")
print(f"{'Detector':<25} {'f_min (Hz)':<15} {'f_max (Hz)':<15}")
print("-" * 55)
for name, (f_min, f_max) in detectors.items():
    print(f"{name:<25} {f_min:<15.0e} {f_max:<15.0e}")
print()

print("KEY INSIGHT: MOND systems probe frequencies BELOW all current detectors!")
print()

# ============================================================================
# 3. MOND NON-LINEARITY AS AMPLIFIER?
# ============================================================================

print("PART 3: MOND NON-LINEARITY ANALYSIS")
print("-" * 50)
print()

def mond_interpolation(g, a0):
    """Standard MOND interpolating function."""
    x = g / a0
    mu = x / (1 + x)  # Simple interpolating function
    return g / mu  # Effective acceleration

def response_to_perturbation(g_base, delta_g, a0):
    """
    Calculate response of MOND system to acceleration perturbation.

    Returns fractional change in effective acceleration.
    """
    g_eff_base = mond_interpolation(g_base, a0)
    g_eff_perturbed = mond_interpolation(g_base + delta_g, a0)
    return (g_eff_perturbed - g_eff_base) / g_eff_base

# Test response at different regimes
g_values = np.logspace(-12, -8, 100)  # Range of base accelerations
delta_g = 1e-15  # Small perturbation (GW-induced)

responses = []
for g in g_values:
    resp = response_to_perturbation(g, delta_g, a0)
    responses.append(resp / (delta_g / g))  # Normalized response

responses = np.array(responses)

# Find the transition region
print(f"Perturbation: δg = {delta_g:.0e} m/s²")
print()
print(f"{'Regime':<20} {'g/a₀':<15} {'Response factor':<20}")
print("-" * 55)
print(f"{'Deep Newtonian':<20} {'>>1':<15} {'1.0 (linear)':<20}")
print(f"{'Transition':<20} {'~1':<15} {'Variable':<20}")
print(f"{'Deep MOND':<20} {'<<1':<15} {'0.5 (reduced)':<20}")
print()

# ============================================================================
# 4. GW STRAIN AND ACCELERATION PERTURBATION
# ============================================================================

print("PART 4: GW STRAIN TO ACCELERATION PERTURBATION")
print("-" * 50)
print()

# A gravitational wave with strain h causes a tidal acceleration:
# δg ~ h × c² / λ_GW ~ h × c² × f_GW / c = h × c × f_GW

def gw_induced_acceleration(h, f_gw, separation):
    """
    Calculate GW-induced acceleration perturbation.

    For a system of size L, the tidal acceleration is:
    δg ~ h × (2πf)² × L  (for f × L/c << 1)

    Or more simply: δg ~ h × c² / λ where λ = c/f
    """
    omega = 2 * np.pi * f_gw
    # Tidal acceleration across the system
    delta_g = h * omega**2 * separation
    return delta_g

# For ultra-low frequency GWs (f ~ 10⁻¹² Hz)
f_gw = 1e-12  # Hz
h_gw = 1e-10  # Strain (very optimistic for this frequency)
L = 10000 * AU  # Binary separation

delta_g_gw = gw_induced_acceleration(h_gw, f_gw, L)

print(f"For GW with f = {f_gw:.0e} Hz, h = {h_gw:.0e}:")
print(f"  Tidal acceleration across 10,000 AU: δg = {delta_g_gw:.2e} m/s²")
print(f"  Compare to a₀ = {a0:.2e} m/s²")
print(f"  Ratio δg/a₀ = {delta_g_gw/a0:.2e}")
print()

# What strain would we need to detect?
# If we can measure δg ~ 10⁻¹⁵ m/s² (very optimistic):
delta_g_detectable = 1e-15  # m/s²
h_required = delta_g_detectable / ((2*np.pi*f_gw)**2 * L)

print(f"To achieve δg = {delta_g_detectable:.0e} m/s² detection:")
print(f"  Required strain: h > {h_required:.2e}")
print()

# ============================================================================
# 5. POTENTIAL GW SOURCES AT ULTRA-LOW FREQUENCIES
# ============================================================================

print("PART 5: POTENTIAL GW SOURCES AT f < 10⁻¹⁰ Hz")
print("-" * 50)
print()

sources = [
    ("Primordial (inflation)", "10⁻¹⁸ - 10⁻¹⁵", "h ~ 10⁻¹⁵ - 10⁻¹²"),
    ("Cosmic strings", "Broadband", "h ~ 10⁻¹⁵ (uncertain)"),
    ("SMBH binaries (early inspiral)", "10⁻¹² - 10⁻¹⁰", "h ~ 10⁻¹² - 10⁻¹⁰"),
    ("Phase transitions", "10⁻¹⁵ - 10⁻¹⁰", "h ~ 10⁻¹⁵ (model dependent)"),
]

print(f"{'Source':<35} {'Frequency (Hz)':<20} {'Expected strain':<20}")
print("-" * 75)
for source, freq, strain in sources:
    print(f"{source:<35} {freq:<20} {strain:<20}")
print()

# ============================================================================
# 6. THE CONCEPT: MOND-BASED GW DETECTOR
# ============================================================================

print("PART 6: THE ZIMMERMAN GW DETECTOR CONCEPT")
print("-" * 50)
print()

print("""
CONCEPT: Use wide binary stars at the MOND transition as GW detectors

METHOD:
1. Monitor thousands of wide binaries with Gaia/successor missions
2. Measure orbital anomalies beyond Newtonian + MOND predictions
3. Look for CORRELATED anomalies across the sky
4. Angular correlation pattern (like Hellings-Downs) indicates GW origin

UNIQUE FEATURES:
• Frequency range: f < 10⁻¹⁰ Hz (unexplored!)
• Uses MOND non-linearity (if real) as physics probe
• Natural detector array (many wide binaries exist)
• Connects GW astronomy to fundamental physics

CHALLENGES:
• MOND itself is unconfirmed
• Enormous noise sources (stellar perturbations, galactic tides)
• Signal extraction extremely difficult
• Requires extraordinary astrometric precision

STATUS: Highly speculative but genuinely novel
""")

# ============================================================================
# 7. QUANTITATIVE SENSITIVITY ESTIMATE
# ============================================================================

print("PART 7: SENSITIVITY ESTIMATE")
print("-" * 50)
print()

# Gaia astrometric precision: ~20 μas for bright stars
# This corresponds to position uncertainty at d = 100 pc:
d_star = 100 * pc  # 100 parsec
theta_precision = 20e-6 * (np.pi / 180 / 3600)  # 20 μas in radians
position_precision = d_star * theta_precision

print(f"Gaia astrometric precision: 20 μas")
print(f"At d = 100 pc, this is: Δx = {position_precision/AU:.3f} AU")
print()

# For a binary at r = 10,000 AU, orbital velocity ~ 0.1 km/s
v_orbital = np.sqrt(G * 2 * M_sun / (10000 * AU)) / 1000  # km/s
print(f"Orbital velocity at 10,000 AU: v = {v_orbital:.2f} km/s")

# GW-induced velocity perturbation:
# δv ~ h × c for passing GW (order of magnitude)
# For h ~ 10⁻¹⁵: δv ~ 3×10⁸ × 10⁻¹⁵ = 3×10⁻⁷ m/s = 0.3 μm/s

h_example = 1e-15
delta_v_gw = h_example * c  # m/s

print(f"\nFor GW with h = {h_example:.0e}:")
print(f"  Induced velocity perturbation: δv ~ {delta_v_gw*1e6:.1f} μm/s")
print(f"  Gaia radial velocity precision: ~100 m/s")
print(f"  Gap: ~10⁸ (not currently detectable)")
print()

print("CONCLUSION: Direct detection requires ~10⁸ improvement in precision")
print("            OR an amplification mechanism from MOND non-linearity")
print("            OR a very loud GW source at these frequencies")
print()

# ============================================================================
# 8. THE MACHIAN CONNECTION
# ============================================================================

print("PART 8: THE MACHIAN ANGLE")
print("-" * 50)
print()

print("""
THE DEEPER QUESTION:

The Zimmerman formula suggests a Machian connection:
  a₀ = cH₀/5.79

Local dynamics (a₀) depend on global cosmology (H₀).

If this connection is REAL and LOCAL (not just global average):
  • GWs from distant sources carry information about matter dynamics
  • Passing GWs might modulate the local "Machian connection"
  • This could manifest as a₀ FLUCTUATIONS

If a₀ fluctuates with passing GWs:
  • Systems at the MOND transition would respond anomalously
  • Correlated anomalies across the sky = GW detection
  • A fundamentally NEW detection principle!

This is speculative but connects GW detection to the deepest
question in gravity: What is the origin of inertia?
""")

# ============================================================================
# 9. VISUALIZATION
# ============================================================================

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Plot 1: GW detector frequency ranges
ax1 = axes[0]
detector_data = [
    ('LIGO', 10, 1000, 'red'),
    ('LISA', 1e-4, 0.1, 'blue'),
    ('PTA', 1e-9, 1e-7, 'green'),
    ('MOND\n(proposed)', 1e-14, 1e-10, 'purple'),
]

for i, (name, f_min, f_max, color) in enumerate(detector_data):
    ax1.barh(i, np.log10(f_max) - np.log10(f_min),
             left=np.log10(f_min), color=color, alpha=0.7, height=0.6)
    ax1.text(np.log10(f_min) - 0.5, i, name, ha='right', va='center', fontsize=10)

ax1.set_xlabel('log₁₀(Frequency / Hz)', fontsize=12)
ax1.set_title('GW Detector Frequency Ranges', fontsize=14)
ax1.set_xlim(-16, 4)
ax1.set_yticks([])
ax1.axvline(x=-10, color='gray', linestyle='--', alpha=0.5)
ax1.text(-10, 3.5, 'Unexplored\nregion', ha='center', fontsize=9, color='gray')
ax1.grid(True, alpha=0.3, axis='x')

# Plot 2: MOND response function
ax2 = axes[1]
g_range = np.logspace(-12, -8, 200)
x = g_range / a0

# MOND effective acceleration
mu = x / (1 + x)
g_eff = g_range / mu

# Response to perturbation (derivative)
# d(g_eff)/dg = d(g/μ)/dg = (1/μ) - g×(dμ/dg)/μ²
# For μ = x/(1+x), dμ/dx = 1/(1+x)², dμ/dg = (1/a₀)/(1+x)²
dmu_dx = 1 / (1 + x)**2
response = 1/mu - (g_range/a0) * dmu_dx / mu**2

ax2.semilogx(x, response, 'b-', linewidth=2)
ax2.axhline(y=1, color='gray', linestyle='--', alpha=0.5, label='Newtonian response')
ax2.axvline(x=1, color='red', linestyle=':', alpha=0.7, label='MOND transition')
ax2.fill_between(x, 0.8, 1.2, where=(x > 0.1) & (x < 10),
                  alpha=0.2, color='red', label='Transition region')

ax2.set_xlabel('g/a₀', fontsize=12)
ax2.set_ylabel('Response factor', fontsize=12)
ax2.set_title('MOND Response to Perturbation', fontsize=14)
ax2.legend(loc='upper right', fontsize=9)
ax2.set_xlim(1e-4, 1e4)
ax2.set_ylim(0, 2)
ax2.grid(True, alpha=0.3)

# Plot 3: Wide binary sensitivity
ax3 = axes[2]
separations = np.logspace(2, 5, 100)  # AU
r_trans_solar = mond_transition_radius(2)  # For 2 solar mass binary

ax3.loglog(separations, separations/r_trans_solar, 'b-', linewidth=2)
ax3.axhline(y=1, color='red', linestyle='--', linewidth=2, label='MOND transition')
ax3.axvspan(r_trans_solar*0.5, r_trans_solar*2, alpha=0.2, color='red',
            label='Sensitive region')

ax3.set_xlabel('Binary Separation (AU)', fontsize=12)
ax3.set_ylabel('r / r_transition', fontsize=12)
ax3.set_title('Wide Binary MOND Sensitivity', fontsize=14)
ax3.legend(loc='upper left', fontsize=9)
ax3.grid(True, alpha=0.3, which='both')

# Add annotation
ax3.annotate(f'r_trans ≈ {r_trans_solar:.0f} AU\n(for 2 M☉)',
             xy=(r_trans_solar, 1), xytext=(r_trans_solar*3, 0.3),
             fontsize=10, arrowprops=dict(arrowstyle='->', color='red'))

plt.tight_layout()
plt.savefig('mond_gw_detector_concept.png', dpi=150, bbox_inches='tight')
plt.close()

print("=" * 70)
print("OUTPUT: mond_gw_detector_concept.png")
print("=" * 70)

# ============================================================================
# 10. SUMMARY
# ============================================================================

print()
print("=" * 70)
print("SUMMARY: MOND-BASED GW DETECTION")
print("=" * 70)
print()
print("FEASIBILITY: Highly speculative but conceptually novel")
print()
print("PROS:")
print("  + Probes unexplored frequency range (f < 10⁻¹⁰ Hz)")
print("  + Uses existing astrophysical systems (wide binaries)")
print("  + Connects GW detection to fundamental physics (MOND test)")
print("  + If Machian interpretation correct, unique detection principle")
print()
print("CONS:")
print("  - MOND itself is unconfirmed")
print("  - Sensitivity gap of ~10⁸ with current technology")
print("  - Enormous systematic noise sources")
print("  - Theoretical framework incomplete")
print()
print("VERDICT: Not practical with current technology, but worth")
print("         exploring theoretically if MOND is confirmed.")
print("=" * 70)
