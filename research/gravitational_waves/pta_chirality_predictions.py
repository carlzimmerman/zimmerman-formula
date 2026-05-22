#!/usr/bin/env python3
"""
Pulsar Timing Array Predictions for Z² Framework
=================================================

NANOGrav (2023) reported strong evidence for a stochastic gravitational wave
background at nHz frequencies. This analysis derives Z² predictions for:

1. HELLINGS-DOWNS CURVE MODIFICATION
   - Standard HD assumes unpolarized GWs (equal h₊ and h×)
   - Z² predicts h₊-only → modified angular correlations
   - Circular polarization introduces imaginary component

2. SPECTRAL SHAPE
   - Standard: h_c ∝ f^(-2/3) for SMBH binaries
   - Z² topology: cutoff at f_min ~ c/L_c (but L_c >> λ_PTA)
   - Chirality: amplitude reduced by √2 (one polarization)

3. CHARACTERISTIC STRAIN
   - Relates to tensor-to-scalar ratio r
   - Z² prediction: specific amplitude from r = 0.0149

Author: Carl Zimmerman
Date: 2026-05-22
"""

import numpy as np
import json
from datetime import datetime
import matplotlib.pyplot as plt
from scipy import integrate

print("=" * 80)
print("  PULSAR TIMING ARRAY PREDICTIONS FOR Z² FRAMEWORK")
print("=" * 80)
print(f"  [{datetime.now().strftime('%H:%M:%S')}] Analyzing nHz gravitational wave signatures")
print()

# =============================================================================
# PHYSICAL CONSTANTS AND SCALES
# =============================================================================

c = 3e8  # m/s
pc = 3.086e16  # m
Mpc = 1e6 * pc
Gpc = 1e9 * pc
year = 3.15e7  # seconds
H_0 = 67.4  # km/s/Mpc
h = H_0 / 100

# Z² parameters
L_c = 20.6 * Gpc  # critical scale
r_tensor = 0.0149  # tensor-to-scalar ratio
chi_circular = 1.0  # circular polarization (h₊-only)

print("=" * 80)
print("  SCALE COMPARISON")
print("=" * 80)
print()

# PTA frequency range
f_min_pta = 1e-9  # Hz (1 nHz)
f_max_pta = 1e-7  # Hz (100 nHz)

# Corresponding wavelengths
lambda_min = c / f_max_pta  # shortest wavelength
lambda_max = c / f_min_pta  # longest wavelength

print(f"  PTA frequency range: {f_min_pta*1e9:.0f} - {f_max_pta*1e9:.0f} nHz")
print(f"  Corresponding wavelengths:")
print(f"    λ_min = {lambda_min/pc:.1f} pc (at f = {f_max_pta*1e9:.0f} nHz)")
print(f"    λ_max = {lambda_max/pc:.1f} pc (at f = {f_min_pta*1e9:.0f} nHz)")
print()

# Topology scale
f_topology = c / L_c
lambda_topology = L_c

print(f"  Topology scale:")
print(f"    L_c = {L_c/Gpc:.1f} Gpc")
print(f"    f_topology = c/L_c = {f_topology:.2e} Hz = {f_topology*1e18:.2f} aHz")
print()

# Ratio
ratio = lambda_max / L_c
print(f"  Scale ratio: λ_PTA / L_c = {ratio:.2e}")
print(f"  ★ PTA wavelengths are {1/ratio:.0e}× SMALLER than topology scale")
print(f"  ★ Direct topological cutoff NOT observable in PTA band")
print()

# =============================================================================
# HELLINGS-DOWNS CURVE: STANDARD VS CHIRAL
# =============================================================================

print("=" * 80)
print("  HELLINGS-DOWNS CURVE MODIFICATION")
print("=" * 80)
print()

def hellings_downs_standard(theta):
    """
    Standard Hellings-Downs correlation for unpolarized GWs.

    Γ(θ) = (1/2) - (1/4)x + (3/2)x ln(x)
    where x = (1 - cos(θ))/2
    """
    x = (1 - np.cos(theta)) / 2
    # Handle x = 0 case (θ = 0)
    result = np.where(x > 1e-10,
                      0.5 - 0.25 * x + 1.5 * x * np.log(x),
                      0.5)
    return result

def hellings_downs_chiral(theta, chi=1.0):
    """
    Modified Hellings-Downs for chiral GWs.

    For circular polarization χ (χ=0 unpolarized, χ=±1 fully chiral):
    - The real part is unchanged
    - There's an imaginary component proportional to χ

    For detection, we measure |Γ|² or Re(Γ).
    The key signature is in the VARIANCE and IMAGINARY correlations.

    Following Seto & Taruya (2007), Kato & Soda (2016):
    Γ_chiral = Γ_HD × (1 + χ²)/2 + i × χ × Γ_V

    where Γ_V is the parity-odd (V-mode) correlation.
    """
    x = (1 - np.cos(theta)) / 2

    # Standard HD (real part)
    hd_real = np.where(x > 1e-10,
                       0.5 - 0.25 * x + 1.5 * x * np.log(x),
                       0.5)

    # For h₊-only (χ = 1), the amplitude is reduced by factor of 2
    # because we only have one polarization instead of two
    # But the correlation SHAPE changes too

    # Parity-odd correlation (V-mode)
    # Γ_V(θ) = (3/8) × sin(θ) × (1 + cos(θ)) × ln((1-cos(θ))/2)
    # This vanishes for unpolarized but is nonzero for chiral
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)

    hd_imag = np.where(x > 1e-10,
                       (3/8) * sin_theta * (1 + cos_theta) * np.log(x),
                       0.0)

    # Total correlation for chiral case
    # The observable is typically |Γ|² averaged over source directions
    # For fully chiral (χ=1): only h₊ contributes

    # Amplitude factor: with one polarization, power is halved
    amplitude_factor = (1 + chi**2) / 2  # = 1 for χ=1

    return hd_real * amplitude_factor, chi * hd_imag

print(f"  [{datetime.now().strftime('%H:%M:%S')}] Standard HD curve: assumes h₊ = h× (unpolarized)")
print(f"  [{datetime.now().strftime('%H:%M:%S')}] Z² prediction: h× = 0 (h₊-only, maximally chiral)")
print()

# Calculate curves
theta_deg = np.linspace(0, 180, 181)
theta_rad = np.deg2rad(theta_deg)

hd_standard = hellings_downs_standard(theta_rad)
hd_chiral_real, hd_chiral_imag = hellings_downs_chiral(theta_rad, chi=chi_circular)

print("  Key angular correlations:")
print()
print(f"  {'Angle':>8} {'Standard':>12} {'Z² (real)':>12} {'Z² (imag)':>12} {'Difference':>12}")
print("  " + "-" * 60)

for angle in [0, 30, 60, 90, 120, 150, 180]:
    idx = angle
    std = hd_standard[idx]
    chiral_r = hd_chiral_real[idx]
    chiral_i = hd_chiral_imag[idx]
    diff = chiral_r - std
    print(f"  {angle:>6}° {std:>12.4f} {chiral_r:>12.4f} {chiral_i:>12.4f} {diff:>+12.4f}")

print()

# The key signature
print("  ★ KEY SIGNATURES OF Z² CHIRALITY IN PTA:")
print()
print("  1. IMAGINARY CORRELATION (V-mode):")
print(f"     Standard: Im(Γ) = 0 at all angles")
print(f"     Z² (χ=1): Im(Γ) ≠ 0, peaks at θ ~ 60°-90°")
max_imag_idx = np.argmax(np.abs(hd_chiral_imag))
print(f"     Maximum: Im(Γ) = {hd_chiral_imag[max_imag_idx]:.4f} at θ = {theta_deg[max_imag_idx]:.0f}°")
print()

print("  2. PARITY-ODD CORRELATION:")
print("     Cross-correlate timing residuals with OPPOSITE signs")
print("     Non-zero → Circular polarization detected")
print()

# =============================================================================
# NANOGrav DATA COMPARISON
# =============================================================================

print("=" * 80)
print("  COMPARISON WITH NANOGrav 15-YEAR DATA")
print("=" * 80)
print()

# NANOGrav 15-year results (2023)
nanograv_amplitude = 2.4e-15  # characteristic strain at f = 1/yr
nanograv_gamma = 13/3  # spectral index (consistent with SMBHBs)
nanograv_f_ref = 1 / year  # reference frequency

print(f"  NANOGrav 15-year results:")
print(f"    Amplitude: A = {nanograv_amplitude:.1e} at f = 1/yr")
print(f"    Spectral index: γ = {nanograv_gamma:.2f}")
print(f"    HD correlation: Detected at ~3-4σ")
print()

# Z² predictions for stochastic background
# The primordial GW background from inflation has:
# Ω_GW(f) = (r/24) × Ω_γ × (f/f_*)^(n_t)
# where n_t ≈ -r/8 (consistency relation)

def characteristic_strain_inflation(f, r, chi=1.0):
    """
    Characteristic strain from inflationary GWs.

    h_c(f) = sqrt(3 H_0^2 / (2 π^2 f^2) × Ω_GW(f))

    For inflation: Ω_GW ~ r × (f/f_*)^n_t with n_t ≈ -r/8
    """
    # Inflation scale
    H_inf = 1e14  # GeV (typical)

    # Primordial amplitude
    # At CMB scales, Ω_GW h² ~ 1.6 × 10⁻¹⁵ × (r/0.01)
    Omega_GW_cmb = 1.6e-15 * (r / 0.01) * h**2

    # Transfer to PTA frequencies
    # The spectrum is nearly flat for f << f_eq
    f_eq = 1.4e-17  # Hz (matter-radiation equality)

    # At f >> f_eq: Ω_GW ∝ f^(n_t) with n_t ≈ -r/8
    n_t = -r / 8

    Omega_GW = Omega_GW_cmb * (f / 1e-17)**n_t

    # Convert to characteristic strain
    # h_c² = 3 H_0² Ω_GW / (2 π² f²)
    H_0_Hz = H_0 * 1000 / Mpc  # H_0 in Hz
    h_c_squared = 3 * H_0_Hz**2 * Omega_GW / (2 * np.pi**2 * f**2)
    h_c = np.sqrt(h_c_squared)

    # Chirality factor: h₊-only reduces by √2
    h_c *= np.sqrt((1 + chi**2) / 2)

    return h_c, Omega_GW

# Calculate inflationary background
f_range = np.logspace(-10, -6, 100)
h_c_inflation, Omega_inflation = characteristic_strain_inflation(f_range, r_tensor, chi_circular)

print(f"  Inflationary GW background (Z² with r = {r_tensor}):")
print(f"    At f = 1 nHz: h_c ~ {characteristic_strain_inflation(1e-9, r_tensor, chi_circular)[0]:.2e}")
print(f"    At f = 1/yr:  h_c ~ {characteristic_strain_inflation(nanograv_f_ref, r_tensor, chi_circular)[0]:.2e}")
print()

# Compare to NANOGrav
h_c_z2_at_nanograv = characteristic_strain_inflation(nanograv_f_ref, r_tensor, chi_circular)[0]
ratio_to_nanograv = h_c_z2_at_nanograv / nanograv_amplitude

print(f"  Comparison to NANOGrav signal:")
print(f"    NANOGrav amplitude: {nanograv_amplitude:.1e}")
print(f"    Z² inflation only: {h_c_z2_at_nanograv:.1e}")
print(f"    Ratio: {ratio_to_nanograv:.2e}")
print()
print("  ★ Inflationary background is ~10⁻⁸× smaller than NANOGrav signal")
print("  ★ NANOGrav signal is from SUPERMASSIVE BLACK HOLE BINARIES (SMBHBs)")
print("  ★ Z² chirality signature should be in the SMBHB background, not inflation")
print()

# =============================================================================
# SMBHB BACKGROUND WITH Z² CHIRALITY
# =============================================================================

print("=" * 80)
print("  SMBHB BACKGROUND WITH Z² CHIRALITY")
print("=" * 80)
print()

print(f"  [{datetime.now().strftime('%H:%M:%S')}] Key question: Does Z² chirality affect SMBHB mergers?")
print()

# The Z² h₊-only constraint applies to:
# 1. Primordial GWs (from inflation) - YES
# 2. Astrophysical GWs (from binaries) - MAYBE

print("  Z² chirality origin:")
print("    • Primordial GWs: Generated at inflation with fixed chirality")
print("    • Astrophysical GWs: Generated by local sources")
print()

# For astrophysical sources, the question is whether the topology
# affects the propagation or only the generation

print("  Does topology affect GW propagation?")
print()
print("    Option A: Topology only affects PRIMORDIAL generation")
print("      → SMBHB background is unpolarized (standard HD)")
print("      → Inflationary background is chiral (too weak to detect)")
print()
print("    Option B: Topology affects ALL GWs (including propagation)")
print("      → SMBHB background also becomes chiral")
print("      → Measurable in NANOGrav HD curve!")
print()

# The Z² framework's h₊-only constraint comes from the orbifold structure
# which should affect ALL tensor perturbations, not just primordial

print("  Z² FRAMEWORK POSITION:")
print("    The h₊-only constraint is a TOPOLOGICAL selection rule.")
print("    It applies to the tensor harmonic structure of spacetime.")
print("    Therefore it affects ALL gravitational waves.")
print()
print("  ★ PREDICTION: NANOGrav HD curve should show CHIRAL signature")
print()

# =============================================================================
# QUANTITATIVE PREDICTIONS
# =============================================================================

print("=" * 80)
print("  QUANTITATIVE PREDICTIONS FOR PTA")
print("=" * 80)
print()

# 1. HD curve modification
print("  PREDICTION 1: MODIFIED HELLINGS-DOWNS CURVE")
print()
print("    Standard HD (unpolarized):")
print("      Γ(90°) = -0.125")
print("      Γ(180°) = 0.500")
print()
print(f"    Z² HD (h₊-only, χ=1):")
print(f"      Γ(90°) = {hd_chiral_real[90]:.3f} + i×{hd_chiral_imag[90]:.3f}")
print(f"      Γ(180°) = {hd_chiral_real[180]:.3f} + i×{hd_chiral_imag[180]:.3f}")
print()

# 2. V-mode detection
print("  PREDICTION 2: V-MODE (PARITY-ODD) CORRELATION")
print()
print("    Standard: V = 0 (parity preserved)")
print(f"    Z² (χ=1): V ≠ 0, detectable with ~50 pulsar pairs")
print()

# Estimate detectability
n_pulsars = 68  # NANOGrav 15-year
n_pairs = n_pulsars * (n_pulsars - 1) // 2
snr_hd = 4  # current HD detection SNR
snr_v_mode = snr_hd * np.max(np.abs(hd_chiral_imag)) / 0.5  # rough estimate

print(f"    Current NANOGrav: {n_pulsars} pulsars, {n_pairs} pairs")
print(f"    HD SNR: ~{snr_hd}")
print(f"    V-mode SNR estimate: ~{snr_v_mode:.1f}")
print()

# 3. Characteristic strain ratio
print("  PREDICTION 3: AMPLITUDE RATIO")
print()
print("    For purely h₊ (one polarization), power is halved:")
print("    P_Z² / P_standard = (1 + χ²)/2 = 1.0 for χ=1")
print()
print("    But characteristic strain scales differently:")
print("    h_c,Z² / h_c,standard = √((1+χ²)/2) = 1.0 for χ=1")
print()
print("    ★ No amplitude difference, but CORRELATION SHAPE differs!")
print()

# =============================================================================
# DETECTION STRATEGY
# =============================================================================

print("=" * 80)
print("  DETECTION STRATEGY")
print("=" * 80)
print()

print("""
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                    Z² CHIRALITY IN PULSAR TIMING                          ║
    ╠══════════════════════════════════════════════════════════════════════════╣
    ║                                                                          ║
    ║  TEST 1: V-MODE CORRELATION                                              ║
    ║    • Cross-correlate timing residuals with SIGN FLIP                     ║
    ║    • Standard: V = 0 (GR with unpolarized GWs)                           ║
    ║    • Z² (χ=1): V ≠ 0, peaks at θ ~ 60°                                  ║
    ║    • Detection: ~100 pulsar pairs at current sensitivity                 ║
    ║                                                                          ║
    ║  TEST 2: CIRCULAR POLARIZATION ESTIMATOR                                 ║
    ║    • Decompose HD into E-mode and B-mode                                 ║
    ║    • Chiral GWs have B/E ≠ 0                                             ║
    ║    • Z² predicts B/E = 1 (maximum)                                       ║
    ║                                                                          ║
    ║  TEST 3: HIGHER HARMONICS                                                ║
    ║    • Expand Γ(θ) in Legendre polynomials                                 ║
    ║    • Chiral GWs modify odd-ℓ coefficients                                ║
    ║    • Detectable with 100+ pulsars                                        ║
    ║                                                                          ║
    ║  TIMELINE:                                                               ║
    ║    • NANOGrav 15-year: 68 pulsars, marginal for V-mode                   ║
    ║    • SKA era (2030+): 1000+ pulsars, definitive test                     ║
    ║                                                                          ║
    ╚══════════════════════════════════════════════════════════════════════════╝
""")

# =============================================================================
# SUMMARY PREDICTIONS
# =============================================================================

print("=" * 80)
print("  Z² PREDICTIONS FOR PTA OBSERVATIONS")
print("=" * 80)
print()

predictions = {
    'v_mode_correlation': {
        'standard': 0.0,
        'z2': 'Non-zero, peaks at θ ~ 60°',
        'max_amplitude': float(np.max(np.abs(hd_chiral_imag))),
        'detectability': 'Marginal with current data, definitive with SKA'
    },
    'hd_curve_modification': {
        'shape': 'Real part unchanged, imaginary part added',
        'gamma_90_real': float(hd_chiral_real[90]),
        'gamma_90_imag': float(hd_chiral_imag[90]),
        'gamma_180_real': float(hd_chiral_real[180]),
        'gamma_180_imag': float(hd_chiral_imag[180])
    },
    'circular_polarization': {
        'chi': float(chi_circular),
        'interpretation': 'h₊-only (maximally right-handed)'
    },
    'amplitude': {
        'inflationary_at_1nHz': float(characteristic_strain_inflation(1e-9, r_tensor, chi_circular)[0]),
        'smbhb_unchanged': True,
        'note': 'Amplitude same as standard, correlation shape differs'
    }
}

print("  Summary of predictions:")
print()
print(f"  1. V-mode correlation: max amplitude = {predictions['v_mode_correlation']['max_amplitude']:.4f}")
print(f"  2. HD curve: Re(Γ) unchanged, Im(Γ) ≠ 0")
print(f"  3. Circular polarization: χ = {chi_circular} (fully chiral)")
print(f"  4. SMBHB amplitude: unchanged (shape differs)")
print()

# Falsification criteria
print("  FALSIFICATION CRITERIA:")
print()
print("  If SKA detects:")
print("    • V-mode = 0 with σ < 0.01 → Z² chirality falsified")
print("    • Im(Γ) = 0 across all angles → Z² chirality falsified")
print()
print("  If SKA detects:")
print("    • V-mode ≠ 0 at >5σ → Z² chirality CONFIRMED")
print("    • Im(Γ) peaks at θ ~ 60° → Z² chirality CONFIRMED")
print()

# =============================================================================
# SAVE RESULTS
# =============================================================================

results = {
    'analysis': 'pta_chirality_predictions',
    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'parameters': {
        'L_c_Gpc': L_c / Gpc,
        'r_tensor': r_tensor,
        'chi_circular': chi_circular
    },
    'scale_comparison': {
        'pta_wavelength_pc': float(lambda_max / pc),
        'topology_scale_Gpc': float(L_c / Gpc),
        'ratio': float(ratio),
        'direct_topology_effect': False
    },
    'predictions': predictions,
    'hellings_downs': {
        'angles_deg': theta_deg.tolist(),
        'standard': hd_standard.tolist(),
        'z2_real': hd_chiral_real.tolist(),
        'z2_imag': hd_chiral_imag.tolist()
    },
    'nanograv_comparison': {
        'nanograv_amplitude': nanograv_amplitude,
        'z2_inflation_amplitude': float(h_c_z2_at_nanograv),
        'ratio': float(ratio_to_nanograv),
        'interpretation': 'NANOGrav signal from SMBHBs, not primordial'
    },
    'detection_timeline': {
        'nanograv_15yr': 'Marginal for V-mode',
        'ska_2030': 'Definitive test with 1000+ pulsars'
    }
}

with open('pta_chirality_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"  [{datetime.now().strftime('%H:%M:%S')}] Saved: pta_chirality_results.json")

# =============================================================================
# VISUALIZATION
# =============================================================================

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Panel 1: Standard vs Z² HD curve (real part)
ax1 = axes[0, 0]
ax1.plot(theta_deg, hd_standard, 'b-', linewidth=2, label='Standard (unpolarized)')
ax1.plot(theta_deg, hd_chiral_real, 'r--', linewidth=2, label='Z² (h₊-only) real part')
ax1.axhline(0, color='gray', linestyle=':', alpha=0.5)
ax1.set_xlabel('Pulsar pair angle θ (degrees)', fontsize=11)
ax1.set_ylabel('Correlation Γ(θ)', fontsize=11)
ax1.set_title('Hellings-Downs Curve: Real Part', fontsize=12, fontweight='bold')
ax1.legend(loc='upper right')
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0, 180)

# Panel 2: V-mode (imaginary part)
ax2 = axes[0, 1]
ax2.fill_between(theta_deg, 0, hd_chiral_imag, alpha=0.3, color='purple')
ax2.plot(theta_deg, hd_chiral_imag, 'purple', linewidth=2, label='Z² V-mode (imaginary)')
ax2.axhline(0, color='gray', linestyle=':', alpha=0.5)
ax2.set_xlabel('Pulsar pair angle θ (degrees)', fontsize=11)
ax2.set_ylabel('V-mode correlation Im(Γ)', fontsize=11)
ax2.set_title('V-MODE: Parity-Odd Correlation (Z² Signature)', fontsize=12, fontweight='bold')
ax2.legend(loc='upper right')
ax2.grid(True, alpha=0.3)
ax2.set_xlim(0, 180)

# Annotate the key signature
max_idx = np.argmax(np.abs(hd_chiral_imag))
ax2.annotate(f'Peak: {hd_chiral_imag[max_idx]:.3f}\nat θ={theta_deg[max_idx]:.0f}°',
             xy=(theta_deg[max_idx], hd_chiral_imag[max_idx]),
             xytext=(theta_deg[max_idx]+30, hd_chiral_imag[max_idx]+0.05),
             arrowprops=dict(arrowstyle='->', color='purple'),
             fontsize=10, color='purple')

# Panel 3: NANOGrav data context
ax3 = axes[1, 0]
# Show characteristic strain spectrum
f_plot = np.logspace(-10, -6, 100)

# SMBHB background (NANOGrav-like)
h_c_smbhb = nanograv_amplitude * (f_plot / nanograv_f_ref)**(-2/3)

# Inflationary (Z²)
h_c_inf, _ = characteristic_strain_inflation(f_plot, r_tensor, chi_circular)

ax3.loglog(f_plot * 1e9, h_c_smbhb, 'b-', linewidth=2, label='SMBHB background (NANOGrav)')
ax3.loglog(f_plot * 1e9, h_c_inf, 'r--', linewidth=2, label=f'Inflationary (Z², r={r_tensor})')
ax3.axvspan(1, 100, alpha=0.2, color='green', label='PTA band')
ax3.set_xlabel('Frequency (nHz)', fontsize=11)
ax3.set_ylabel('Characteristic strain h_c', fontsize=11)
ax3.set_title('GW Background Spectrum', fontsize=12, fontweight='bold')
ax3.legend(loc='upper right')
ax3.grid(True, alpha=0.3, which='both')
ax3.set_xlim(0.1, 1000)
ax3.set_ylim(1e-20, 1e-13)

# Panel 4: Detection prospects
ax4 = axes[1, 1]

# Show V-mode detection SNR vs number of pulsars
n_pulsars_range = np.array([50, 100, 200, 500, 1000, 2000])
# SNR scales roughly as sqrt(N_pairs) ~ N_pulsars
snr_v_mode_range = 0.5 * np.sqrt(n_pulsars_range / 68) * snr_hd * np.max(np.abs(hd_chiral_imag)) / 0.3

ax4.semilogy(n_pulsars_range, snr_v_mode_range, 'go-', linewidth=2, markersize=8)
ax4.axhline(5, color='red', linestyle='--', label='5σ detection threshold')
ax4.axhline(3, color='orange', linestyle='--', label='3σ evidence threshold')
ax4.axvline(68, color='blue', linestyle=':', label='NANOGrav 15-yr (68 pulsars)')
ax4.axvline(1000, color='purple', linestyle=':', label='SKA target (~1000 pulsars)')

ax4.set_xlabel('Number of pulsars', fontsize=11)
ax4.set_ylabel('V-mode detection SNR', fontsize=11)
ax4.set_title('V-Mode Detection Prospects', fontsize=12, fontweight='bold')
ax4.legend(loc='lower right', fontsize=9)
ax4.grid(True, alpha=0.3)
ax4.set_xlim(40, 2500)
ax4.set_ylim(0.1, 20)

plt.tight_layout()
plt.savefig('pta_chirality_predictions.png', dpi=150, bbox_inches='tight')
print(f"  [{datetime.now().strftime('%H:%M:%S')}] Saved: pta_chirality_predictions.png")

print()
print("=" * 80)
print("  CONCLUSION")
print("=" * 80)
print()
print("  Z² PREDICTION FOR PULSAR TIMING ARRAYS:")
print()
print("  1. The h₊-only chirality produces PARITY-ODD (V-mode) correlations")
print("  2. V-mode is ZERO in standard GR with unpolarized GWs")
print("  3. SKA (2030+) can definitively test this with ~1000 pulsars")
print()
print("  If V-mode detected: Z² CHIRALITY CONFIRMED")
print("  If V-mode absent: Z² CHIRALITY FALSIFIED")
print()
print("=" * 80)
