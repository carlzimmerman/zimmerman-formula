#!/usr/bin/env python3
"""
Computational Analysis of 10 Experimental Tests for Z² Framework

Carl Zimmerman | May 2026

This script computes quantitative predictions for each proposed experimental
test of the Z² framework, including statistical power analysis and comparison
to current/future experimental sensitivities.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.integrate import quad
from scipy.special import erfc
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================

Z_SQUARED = 32 * np.pi / 3  # = 33.510321638...
Z = np.sqrt(Z_SQUARED)       # = 5.788810...

# Framework integers
GAUGE = 12
BEKENSTEIN = 4
N_GEN = 3
TOTAL_MODES = 19

# Cosmological predictions
OMEGA_LAMBDA = 13 / 19  # = 0.684210526...
OMEGA_MATTER = 6 / 19   # = 0.315789474...

# Magic angle
THETA_MAGIC_RAD = np.arctan(1 / np.sqrt(2))  # = 0.6154797...
THETA_MAGIC_DEG = np.degrees(THETA_MAGIC_RAD)  # = 35.264°

# Tensor-to-scalar ratio
R_PREDICTED = 1 / (2 * Z_SQUARED)  # = 0.01492...

# Fine structure constant
ALPHA_INV = 4 * Z_SQUARED + 3  # = 137.041...

print("=" * 70)
print("Z² FRAMEWORK: EXPERIMENTAL TESTS COMPUTATIONAL ANALYSIS")
print("=" * 70)
print(f"Z² = 32π/3 = {Z_SQUARED:.10f}")
print(f"Z = √(32π/3) = {Z:.10f}")
print(f"Magic angle = {THETA_MAGIC_DEG:.4f}°")
print(f"r = 1/(2Z²) = {R_PREDICTED:.6f}")
print(f"Ω_Λ = 13/19 = {OMEGA_LAMBDA:.10f}")
print(f"α⁻¹ = 4Z² + 3 = {ALPHA_INV:.6f}")
print("=" * 70)

# =============================================================================
# TEST 1: CRYSTAL MAGIC ANGLE ALIGNMENT
# =============================================================================

def test1_crystal_magic_angle():
    """
    Calculate resistivity anomaly vs crystal orientation relative to CMB dipole.

    The framework predicts a ~1% resistivity drop when the crystal body diagonal
    aligns with the CMB dipole direction (at the magic angle to crystal faces).
    """
    print("\n" + "=" * 70)
    print("TEST 1: CRYSTAL MAGIC ANGLE ALIGNMENT")
    print("=" * 70)

    # Angle range (0 to 90 degrees)
    theta = np.linspace(0, 90, 1000)
    theta_rad = np.radians(theta)

    # Tensor coupling for phonon scattering
    # C(θ) = (9/4)sin²θ - 3/4
    # At magic angle (sin²θ = 1/3): C = 0
    C_theta = (9/4) * np.sin(theta_rad)**2 - 3/4

    # Resistivity model: ρ(θ) = ρ₀[1 + ε·C(θ)²]
    # where ε is coupling strength
    epsilon = 0.01  # 1% maximum effect

    # Normalized resistivity
    rho_normalized = 1 + epsilon * C_theta**2

    # At magic angle
    rho_at_magic = 1 + epsilon * 0**2  # C = 0 at magic angle
    rho_at_0 = 1 + epsilon * (-3/4)**2
    rho_at_90 = 1 + epsilon * (9/4 - 3/4)**2

    anomaly_percent = (rho_at_0 - rho_at_magic) / rho_at_0 * 100

    print(f"\nMagic angle: θ = {THETA_MAGIC_DEG:.4f}°")
    print(f"Tensor coupling C(θ_magic) = 0 (exact)")
    print(f"Resistivity at θ = 0°: ρ/ρ₀ = {rho_at_0:.6f}")
    print(f"Resistivity at θ = magic: ρ/ρ₀ = {rho_at_magic:.6f}")
    print(f"Predicted anomaly: {anomaly_percent:.2f}% drop at magic angle")

    # Measurement requirements
    print(f"\nMeasurement requirements:")
    print(f"  - Resistivity precision: < 0.1% (achievable)")
    print(f"  - Angular precision: < 0.1° (achievable)")
    print(f"  - Temperature stability: < 0.01 K (achievable)")

    return theta, rho_normalized, C_theta

# =============================================================================
# TEST 2: GW CROSS-POLARIZATION NULL TEST
# =============================================================================

def test2_gw_polarization():
    """
    Monte Carlo analysis of GW h_× = 0 test.

    Z² predicts h_× = 0 exactly. GR predicts h_× ≈ h_+ on average.
    Calculate events needed for definitive distinction.
    """
    print("\n" + "=" * 70)
    print("TEST 2: GW CROSS-POLARIZATION NULL TEST")
    print("=" * 70)

    np.random.seed(42)
    n_simulations = 10000

    # Event counts to test
    n_events_range = np.array([10, 25, 50, 100, 200, 500])

    # SNR distribution (typical for LIGO detections)
    snr_mean = 15
    snr_std = 8
    snr_min = 8  # Detection threshold

    detection_power_z2_true = []
    detection_power_gr_true = []

    for n_events in n_events_range:
        z2_rejects_gr = 0  # Times we correctly reject GR when Z² is true
        gr_rejects_z2 = 0  # Times we correctly reject Z² when GR is true

        for _ in range(n_simulations):
            # Generate SNRs
            snrs = np.maximum(snr_min, np.random.normal(snr_mean, snr_std, n_events))

            # Measurement uncertainty on h_×/h_+
            sigma_ratio = 1 / snrs

            # Simulate under Z² (h_× = 0)
            h_cross_z2 = np.random.normal(0, sigma_ratio)

            # Simulate under GR (h_× = h_+ on average, with variation)
            true_ratio_gr = np.random.uniform(0.5, 1.5, n_events)  # Random orientation
            h_cross_gr = np.random.normal(true_ratio_gr, sigma_ratio)

            # Test statistic: χ² for h_× = 0
            chi2_z2 = np.sum((h_cross_z2 / sigma_ratio)**2)
            chi2_gr = np.sum((h_cross_gr / sigma_ratio)**2)

            # Null hypothesis: h_× = 0 (Z² prediction)
            # Under null, χ² ~ χ²(n_events)
            p_value_z2 = 1 - stats.chi2.cdf(chi2_z2, n_events)
            p_value_gr = 1 - stats.chi2.cdf(chi2_gr, n_events)

            # Reject null (Z²) at 5σ if p < 3e-7
            alpha = 3e-7  # 5σ significance

            if p_value_z2 > alpha:  # Fail to reject Z² when Z² is true (correct)
                z2_rejects_gr += 1
            if p_value_gr < alpha:  # Reject Z² when GR is true (correct)
                gr_rejects_z2 += 1

        detection_power_z2_true.append(z2_rejects_gr / n_simulations)
        detection_power_gr_true.append(gr_rejects_z2 / n_simulations)

    print(f"\nDetection power analysis (5σ significance):")
    print(f"{'Events':<10} {'P(support Z²|Z² true)':<25} {'P(reject Z²|GR true)':<25}")
    print("-" * 60)
    for i, n in enumerate(n_events_range):
        print(f"{n:<10} {detection_power_z2_true[i]:<25.3f} {detection_power_gr_true[i]:<25.3f}")

    # Find events needed for 95% power
    for i, n in enumerate(n_events_range):
        if detection_power_gr_true[i] > 0.95:
            print(f"\n→ ~{n} events needed for 95% power to distinguish GR from Z²")
            break

    return n_events_range, detection_power_z2_true, detection_power_gr_true

# =============================================================================
# TEST 3: ULTRA-PRECISION FLATNESS TEST
# =============================================================================

def test3_flatness_precision():
    """
    Fisher matrix forecast for Ω_k constraints.

    Z² predicts Ω_k = 0.0000 exactly.
    Calculate required precision to test this.
    """
    print("\n" + "=" * 70)
    print("TEST 3: ULTRA-PRECISION FLATNESS TEST")
    print("=" * 70)

    # Current and future constraints on |Ω_k|
    experiments = {
        'Planck 2018': 0.0007,
        'Planck + BAO': 0.0004,
        'DESI Y1': 0.0025,
        'DESI Y5 (proj)': 0.001,
        'Euclid (proj)': 0.0005,
        'Combined 2030': 0.0002,
        'Combined 2035': 0.0001,
    }

    print(f"\nZ² prediction: Ω_k = 0.000000... (exactly flat)")
    print(f"\nCurrent and projected constraints on σ(Ω_k):")
    print("-" * 50)

    for exp, sigma in experiments.items():
        # Significance of detecting Ω_k = 0.001 (typical inflation prediction)
        omega_k_test = 0.001
        significance = omega_k_test / sigma
        print(f"{exp:<20}: σ(Ω_k) = {sigma:.4f}  |  {significance:.1f}σ for Ω_k=0.001")

    # Detection threshold analysis
    print(f"\nIf Ω_k = 0.0001 (some inflation models):")
    for exp, sigma in experiments.items():
        if sigma <= 0.0001:
            print(f"  {exp}: Would detect at {0.0001/sigma:.1f}σ")

    return experiments

# =============================================================================
# TEST 4: CMB TOPOLOGY SEARCH
# =============================================================================

def test4_cmb_topology():
    """
    Calculate angular scales for T³/Z₂ topology signatures.

    The topology creates matched circles and specific correlation patterns.
    """
    print("\n" + "=" * 70)
    print("TEST 4: CMB TOPOLOGY SEARCH FOR T³/Z₂ SIGNATURES")
    print("=" * 70)

    # Fundamental domain size (unknown - parameterize)
    # L_fund in units of Hubble radius
    L_fund_range = np.array([0.5, 1.0, 2.0, 3.0, 5.0])  # × c/H₀

    # Current Hubble radius
    c_H0 = 4.4e3  # Mpc (c/H₀ for H₀ = 68 km/s/Mpc)

    # Distance to last scattering surface
    D_LSS = 14000  # Mpc (comoving)

    print(f"\nT³/Z₂ topology signatures:")
    print(f"  - 8 fixed points (orbifold singularities)")
    print(f"  - Matched circles at antipodal points")
    print(f"  - Z₂ identification halves the number of matches vs T³")

    print(f"\nMatched circle angular radius vs fundamental domain size:")
    print(f"{'L_fund (c/H₀)':<15} {'L_fund (Mpc)':<15} {'θ_circle (°)':<15} {'Status':<20}")
    print("-" * 65)

    for L in L_fund_range:
        L_mpc = L * c_H0
        # Angular radius of matched circles
        # θ ≈ arccos(L / (2 * D_LSS)) for L < 2*D_LSS
        if L_mpc < 2 * D_LSS:
            theta_rad = np.arccos(L_mpc / (2 * D_LSS))
            theta_deg = np.degrees(theta_rad)
            status = "Detectable" if theta_deg > 10 else "Marginal"
        else:
            theta_deg = 0
            status = "No circles"
        print(f"{L:<15.1f} {L_mpc:<15.0f} {theta_deg:<15.1f} {status:<20}")

    # Number of matched circle pairs for T³/Z₂
    print(f"\nT³ has 6 pairs of matched circles (3 directions × 2)")
    print(f"T³/Z₂ has 3 pairs (Z₂ identifies opposite pairs)")

    return L_fund_range

# =============================================================================
# TEST 5: DARK ENERGY w(z) PRECISION TEST
# =============================================================================

def test5_dark_energy():
    """
    Calculate w(z) predictions and comparison to DESI hints.

    Z² predicts w = -1 exactly at all z.
    """
    print("\n" + "=" * 70)
    print("TEST 5: DARK ENERGY EQUATION OF STATE w(z)")
    print("=" * 70)

    # Redshift range
    z = np.linspace(0, 2.5, 100)

    # Z² prediction
    w_z2 = -1.0 * np.ones_like(z)

    # DESI Year 1 hints (w₀-wₐ parameterization)
    w0_desi = -0.55
    wa_desi = -1.30
    w_desi = w0_desi + wa_desi * z / (1 + z)

    # Standard ΛCDM
    w_lcdm = -1.0 * np.ones_like(z)

    # Quintessence example
    w_quint = -0.9 - 0.1 * z / (1 + z)

    # Current constraints
    print(f"\nZ² prediction: w(z) = -1.000 exactly at all z")
    print(f"\nDESI Year 1 (2.5σ from ΛCDM):")
    print(f"  w₀ = {w0_desi:.2f}")
    print(f"  wₐ = {wa_desi:.2f}")

    # χ² calculation for current data
    # Simplified: assume N_eff data points with given errors
    n_data = 20
    sigma_w = 0.1  # Typical current error

    chi2_z2_vs_desi = n_data * ((w0_desi - (-1))**2 + (wa_desi - 0)**2) / sigma_w**2

    print(f"\nStatistical comparison (current precision σ_w ~ {sigma_w}):")
    print(f"  χ² (Z² vs DESI best-fit): {chi2_z2_vs_desi:.1f}")
    print(f"  Significance: {np.sqrt(chi2_z2_vs_desi):.1f}σ")

    # Future projections
    print(f"\nFuture precision projections:")
    future_experiments = {
        'DESI Y5': 0.03,
        'Euclid': 0.025,
        'Roman': 0.03,
        'Combined 2030': 0.015,
        'Combined 2035': 0.008,
    }

    print(f"{'Experiment':<20} {'σ(w₀)':<10} {'σ needed for 5σ DESI-Z²':<25}")
    print("-" * 55)
    for exp, sigma in future_experiments.items():
        delta_w = abs(w0_desi - (-1))
        sigma_5sig = delta_w / 5
        achieves = "YES" if sigma < sigma_5sig else "NO"
        print(f"{exp:<20} {sigma:<10.3f} {sigma_5sig:<10.3f} → {achieves}")

    return z, w_z2, w_desi, w_quint

# =============================================================================
# TEST 6: TENSOR-TO-SCALAR RATIO PRECISION
# =============================================================================

def test6_tensor_scalar():
    """
    Calculate tensor-to-scalar ratio predictions and experimental requirements.

    Z² predicts r = 1/(2Z²) = 0.01492...
    """
    print("\n" + "=" * 70)
    print("TEST 6: TENSOR-TO-SCALAR RATIO r")
    print("=" * 70)

    r_z2 = R_PREDICTED
    r_uncertainty = 0.0005  # Framework uncertainty estimate

    print(f"\nZ² prediction: r = 1/(2Z²) = 3/(64π) = {r_z2:.6f}")
    print(f"Predicted range: r ∈ [{r_z2 - 2*r_uncertainty:.4f}, {r_z2 + 2*r_uncertainty:.4f}]")

    # Current and future constraints
    experiments = {
        'BICEP/Keck 2021': {'limit': 0.036, 'sigma': None, 'type': 'upper'},
        'Planck 2018': {'limit': 0.10, 'sigma': None, 'type': 'upper'},
        'LiteBIRD (proj)': {'limit': None, 'sigma': 0.002, 'type': 'measurement'},
        'CMB-S4 (proj)': {'limit': None, 'sigma': 0.003, 'type': 'measurement'},
        'PICO (proj)': {'limit': None, 'sigma': 0.0005, 'type': 'measurement'},
    }

    print(f"\nExperimental landscape:")
    print(f"{'Experiment':<20} {'Constraint':<20} {'Z² detectable?':<20}")
    print("-" * 60)

    for exp, data in experiments.items():
        if data['type'] == 'upper':
            constraint = f"r < {data['limit']:.3f}"
            detectable = "Below limit ✓" if r_z2 < data['limit'] else "Excluded ✗"
        else:
            constraint = f"σ(r) = {data['sigma']:.4f}"
            snr = r_z2 / data['sigma']
            detectable = f"{snr:.1f}σ detection"
        print(f"{exp:<20} {constraint:<20} {detectable:<20}")

    # Probability distribution for r measurements
    r_range = np.linspace(0, 0.04, 1000)

    # Z² prediction distribution
    pdf_z2 = stats.norm.pdf(r_range, r_z2, r_uncertainty)

    # LiteBIRD measurement distribution (if r = r_z2)
    sigma_litebird = 0.002
    pdf_litebird = stats.norm.pdf(r_range, r_z2, sigma_litebird)

    print(f"\nFalsification criteria:")
    print(f"  r < {r_z2 - 3*sigma_litebird:.4f} → Z² falsified at 3σ")
    print(f"  r > {r_z2 + 3*sigma_litebird:.4f} → Z² falsified at 3σ")

    return r_range, pdf_z2, pdf_litebird

# =============================================================================
# TEST 7: FINE STRUCTURE CONSTANT CONSTANCY
# =============================================================================

def test7_alpha_constancy():
    """
    Calculate constraints on α variation.

    Z² predicts Δα/α = 0 exactly if α is geometrically fixed.
    """
    print("\n" + "=" * 70)
    print("TEST 7: FINE STRUCTURE CONSTANT CONSTANCY")
    print("=" * 70)

    print(f"\nZ² prediction: α⁻¹ = 4Z² + 3 = {ALPHA_INV:.6f}")
    print(f"If α is geometric: Δα/α = 0 at all z and positions")

    # Current constraints
    constraints = {
        'Atomic clocks (local)': {'delta_alpha': 0, 'error': 1e-18, 'z': 0},
        'Oklo reactor (z~0)': {'delta_alpha': 0, 'error': 1e-7, 'z': 0},
        'Quasar absorption (z~1)': {'delta_alpha': -0.5e-5, 'error': 1e-5, 'z': 1},
        'Quasar absorption (z~2)': {'delta_alpha': 1e-5, 'error': 2e-5, 'z': 2},
        'Quasar absorption (z~4)': {'delta_alpha': -2e-5, 'error': 3e-5, 'z': 4},
        'CMB (z~1100)': {'delta_alpha': 0, 'error': 4e-3, 'z': 1100},
    }

    print(f"\nCurrent constraints on Δα/α:")
    print(f"{'Method':<30} {'z':<10} {'Δα/α':<15} {'σ':<15} {'Consistent w/ Z²?':<15}")
    print("-" * 85)

    for method, data in constraints.items():
        da = data['delta_alpha']
        err = data['error']
        z = data['z']
        # Z² consistent if |Δα/α| < 2σ from 0
        consistent = "YES" if abs(da) < 2*err else "TENSION"
        print(f"{method:<30} {z:<10} {da:<15.2e} {err:<15.2e} {consistent:<15}")

    # Webb et al. dipole claim
    print(f"\nControversial claim (Webb et al.):")
    print(f"  Spatial dipole: Δα/α ~ 10⁻⁵ across sky")
    print(f"  If confirmed: CHALLENGES Z² geometric origin")
    print(f"  Current status: Not independently confirmed")

    return constraints

# =============================================================================
# TEST 8: PRIMORDIAL NON-GAUSSIANITY
# =============================================================================

def test8_non_gaussianity():
    """
    Calculate f_NL predictions from T³/Z₂ perturbation theory.
    """
    print("\n" + "=" * 70)
    print("TEST 8: PRIMORDIAL NON-GAUSSIANITY f_NL")
    print("=" * 70)

    # Z² predictions (derived from topological suppression)
    f_NL_local_z2 = 5 / (12 * Z_SQUARED)
    f_NL_equil_z2 = -3 / (8 * Z_SQUARED)
    f_NL_ortho_z2 = 1 / (4 * Z_SQUARED)

    print(f"\nZ² predictions from orbifold perturbation theory:")
    print(f"  f_NL^local = 5/(12Z²) = {f_NL_local_z2:.6f}")
    print(f"  f_NL^equil = -3/(8Z²) = {f_NL_equil_z2:.6f}")
    print(f"  f_NL^ortho = 1/(4Z²) = {f_NL_ortho_z2:.6f}")

    # Current constraints
    print(f"\nPlanck 2018 constraints:")
    planck = {
        'local': {'value': -0.9, 'error': 5.1},
        'equil': {'value': -26, 'error': 47},
        'ortho': {'value': -38, 'error': 24},
    }

    for shape, data in planck.items():
        print(f"  f_NL^{shape} = {data['value']:.1f} ± {data['error']:.1f}")

    # Consistency check
    print(f"\nConsistency with Z² predictions:")
    for shape, data in planck.items():
        if shape == 'local':
            z2_pred = f_NL_local_z2
        elif shape == 'equil':
            z2_pred = f_NL_equil_z2
        else:
            z2_pred = f_NL_ortho_z2

        tension = abs(z2_pred - data['value']) / data['error']
        status = "Consistent" if tension < 2 else "Tension"
        print(f"  {shape}: Z² = {z2_pred:.4f}, Planck = {data['value']:.1f} ± {data['error']:.1f} → {tension:.2f}σ ({status})")

    # Future prospects
    print(f"\nFuture experiments:")
    future = {
        'CMB-S4': 0.5,
        'PICO': 0.3,
        'SKA (21cm)': 0.1,
        'MegaMapper': 0.2,
    }

    print(f"{'Experiment':<15} {'σ(f_NL^local)':<15} {'Z² detectable?':<20}")
    print("-" * 50)
    for exp, sigma in future.items():
        snr = abs(f_NL_local_z2) / sigma
        detectable = f"{snr:.2f}σ" if snr > 0.1 else "No"
        print(f"{exp:<15} {sigma:<15.2f} {detectable:<20}")

    print(f"\n→ Z² prediction f_NL ~ 0.01 requires σ(f_NL) ~ 0.003 for 3σ detection")
    print(f"   This may be achievable with 21cm cosmology in 2040s")

    return f_NL_local_z2, f_NL_equil_z2, f_NL_ortho_z2

# =============================================================================
# TEST 9: COSMIC BIREFRINGENCE
# =============================================================================

def test9_birefringence():
    """
    Calculate cosmic birefringence predictions.

    Z² predicts β = 0 (no axion from T³/Z₂).
    """
    print("\n" + "=" * 70)
    print("TEST 9: COSMIC BIREFRINGENCE")
    print("=" * 70)

    # Z² prediction
    beta_z2 = 0.0  # degrees

    print(f"\nZ² prediction: β = {beta_z2:.2f}° (no axion → no birefringence)")
    print(f"Mechanism: Z₂-odd B-field projected out of spectrum")

    # Current measurements
    print(f"\nCurrent measurements:")
    measurements = {
        'Minami & Komatsu 2020': {'beta': 0.35, 'error': 0.14, 'sigma': 2.4},
        'Planck PR4 + WMAP': {'beta': 0.30, 'error': 0.11, 'sigma': 2.7},
        'Diego-Palazuelos 2022': {'beta': 0.36, 'error': 0.11, 'sigma': 3.3},
    }

    for exp, data in measurements.items():
        print(f"  {exp}: β = {data['beta']:.2f}° ± {data['error']:.2f}° ({data['sigma']:.1f}σ from 0)")

    # Weighted average
    weights = [1/m['error']**2 for m in measurements.values()]
    betas = [m['beta'] for m in measurements.values()]
    beta_avg = np.average(betas, weights=weights)
    sigma_avg = 1 / np.sqrt(sum(weights))

    print(f"\nWeighted average: β = {beta_avg:.2f}° ± {sigma_avg:.2f}°")
    print(f"Tension with Z² (β = 0): {beta_avg/sigma_avg:.1f}σ")

    # Implications
    print(f"\nImplications:")
    if beta_avg / sigma_avg > 5:
        print(f"  → If confirmed at 5σ: Z² FALSIFIED (or requires modification)")
    else:
        print(f"  → Current tension: {beta_avg/sigma_avg:.1f}σ (not yet decisive)")
        print(f"  → LiteBIRD will reach σ(β) ~ 0.01° → decisive test")

    # Future projections
    print(f"\nFuture sensitivity:")
    future = {
        'LiteBIRD': 0.01,
        'CMB-S4': 0.02,
        'PICO': 0.005,
    }

    for exp, sigma in future.items():
        significance = beta_avg / sigma
        print(f"  {exp}: σ(β) = {sigma:.3f}° → {significance:.0f}σ if β = {beta_avg:.2f}°")

    return beta_z2, beta_avg, sigma_avg

# =============================================================================
# TEST 10: GW PHASE COHERENCE
# =============================================================================

def test10_gw_phase():
    """
    Calculate GW phase deviations from topological effects.
    """
    print("\n" + "=" * 70)
    print("TEST 10: GRAVITATIONAL WAVE PHASE COHERENCE")
    print("=" * 70)

    # Phase deviation from discretized tensor modes
    # Δφ = (π/Z²) × (m/M_Pl)²

    M_pl = 1.22e19  # GeV (Planck mass)

    # Different source masses (mass in solar masses, GeV equivalent)
    # 1 M_sun = 1.989e30 kg, 1 kg = 5.61e35 GeV/c²
    sources = [
        ('Stellar BH', 30, 30 * 1.989e30 * 5.61e26),  # 30 M_sun in GeV
        ('IMBH', 1000, 1000 * 1.989e30 * 5.61e26),    # 1000 M_sun in GeV
        ('SMBH', 1e6, 1e6 * 1.989e30 * 5.61e26),      # 10^6 M_sun in GeV
    ]

    print(f"\nPredicted phase deviation: Δφ = (π/Z²) × (m/M_Pl)²")
    print(f"Z² = {Z_SQUARED:.6f}")
    print(f"M_Pl = {M_pl:.2e} GeV")

    print(f"\n{'Source':<25} {'Mass (M☉)':<15} {'Δφ (rad)':<20} {'Detectable?':<20}")
    print("-" * 80)

    for source_name, mass_solar, mass_gev in sources:
        delta_phi = (np.pi / Z_SQUARED) * (mass_gev / M_pl)**2
        # Current phase measurement precision ~ 0.01 rad for high SNR
        # Future 3G detectors ~ 0.001 rad
        detectable_2g = "No" if delta_phi < 0.01 else "Yes (2G)"
        detectable_3g = "Yes (3G)" if delta_phi > 0.001 else "No"
        status = detectable_3g if delta_phi > 0.001 else detectable_2g

        print(f"{source_name:<25} {mass_solar:<15.0f} {delta_phi:<20.2e} {status:<20}")

    # Alternative signature: mode discretization
    print(f"\nAlternative signature: Tensor mode discretization")
    print(f"  On T³/Z₂, tensor modes have discrete spectrum")
    print(f"  Spacing: Δk ~ 2π/L_fund")
    print(f"  For L_fund ~ c/H₀: Δk ~ 10⁻²⁶ m⁻¹")
    print(f"  Effect on GW: Phase modulation at ~10⁻²⁶ Hz (undetectable)")

    print(f"\n→ Direct phase coherence test challenging")
    print(f"→ Better test: Statistical ensemble of h_× = 0 (Test 2)")

    return sources

# =============================================================================
# GENERATE VISUALIZATION
# =============================================================================

def create_visualization():
    """Create comprehensive 10-panel figure for all tests."""

    fig = plt.figure(figsize=(20, 24))

    # Run all tests and collect data
    theta, rho, C_theta = test1_crystal_magic_angle()
    n_events, power_z2, power_gr = test2_gw_polarization()
    flatness_exp = test3_flatness_precision()
    L_fund = test4_cmb_topology()
    z, w_z2, w_desi, w_quint = test5_dark_energy()
    r_range, pdf_z2, pdf_litebird = test6_tensor_scalar()
    alpha_constraints = test7_alpha_constancy()
    f_local, f_equil, f_ortho = test8_non_gaussianity()
    beta_z2, beta_avg, sigma_avg = test9_birefringence()
    gw_sources = test10_gw_phase()

    # Panel 1: Crystal Magic Angle
    ax1 = fig.add_subplot(5, 2, 1)
    ax1.plot(theta, rho, 'b-', linewidth=2, label='Resistivity ρ/ρ₀')
    ax1.axvline(THETA_MAGIC_DEG, color='r', linestyle='--', linewidth=2, label=f'Magic angle = {THETA_MAGIC_DEG:.2f}°')
    ax1.set_xlabel('Crystal angle θ (degrees)', fontsize=12)
    ax1.set_ylabel('Normalized resistivity', fontsize=12)
    ax1.set_title('Test 1: Crystal Magic Angle Alignment', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 90)

    # Panel 2: GW Polarization Detection Power
    ax2 = fig.add_subplot(5, 2, 2)
    ax2.plot(n_events, power_z2, 'b-o', linewidth=2, markersize=8, label='P(support Z² | Z² true)')
    ax2.plot(n_events, power_gr, 'r-s', linewidth=2, markersize=8, label='P(reject Z² | GR true)')
    ax2.axhline(0.95, color='k', linestyle='--', alpha=0.5, label='95% power')
    ax2.set_xlabel('Number of GW events', fontsize=12)
    ax2.set_ylabel('Detection power', fontsize=12)
    ax2.set_title('Test 2: GW Cross-Polarization Null Test', fontsize=14, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 1.05)

    # Panel 3: Flatness Precision
    ax3 = fig.add_subplot(5, 2, 3)
    exps = list(flatness_exp.keys())
    sigmas = list(flatness_exp.values())
    colors = ['gray', 'gray', 'blue', 'blue', 'green', 'green', 'red']
    ax3.barh(exps, sigmas, color=colors, alpha=0.7)
    ax3.axvline(0.0001, color='r', linestyle='--', linewidth=2, label='Target: σ(Ω_k) = 10⁻⁴')
    ax3.set_xlabel('σ(Ω_k)', fontsize=12)
    ax3.set_title('Test 3: Spatial Flatness Precision', fontsize=14, fontweight='bold')
    ax3.set_xscale('log')
    ax3.legend()
    ax3.grid(True, alpha=0.3, axis='x')

    # Panel 4: CMB Topology Angular Scale
    ax4 = fig.add_subplot(5, 2, 4)
    c_H0 = 4400  # Mpc
    D_LSS = 14000  # Mpc
    L_mpc = L_fund * c_H0
    theta_circle = np.degrees(np.arccos(np.minimum(L_mpc / (2 * D_LSS), 0.999)))
    ax4.plot(L_fund, theta_circle, 'b-o', linewidth=2, markersize=10)
    ax4.axhline(10, color='r', linestyle='--', label='Detection threshold ~10°')
    ax4.set_xlabel('Fundamental domain size (c/H₀)', fontsize=12)
    ax4.set_ylabel('Matched circle radius (degrees)', fontsize=12)
    ax4.set_title('Test 4: CMB Topology Circles', fontsize=14, fontweight='bold')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # Panel 5: Dark Energy w(z)
    ax5 = fig.add_subplot(5, 2, 5)
    ax5.plot(z, w_z2, 'b-', linewidth=3, label='Z²: w = -1 exactly')
    ax5.plot(z, w_desi, 'r--', linewidth=2, label='DESI Y1: w₀=-0.55, wₐ=-1.30')
    ax5.plot(z, w_quint, 'g:', linewidth=2, label='Quintessence example')
    ax5.fill_between(z, -1.05, -0.95, alpha=0.2, color='blue', label='Z² ±0.05')
    ax5.set_xlabel('Redshift z', fontsize=12)
    ax5.set_ylabel('w(z)', fontsize=12)
    ax5.set_title('Test 5: Dark Energy Equation of State', fontsize=14, fontweight='bold')
    ax5.legend(loc='lower left')
    ax5.grid(True, alpha=0.3)
    ax5.set_ylim(-2.5, 0)

    # Panel 6: Tensor-to-Scalar Ratio
    ax6 = fig.add_subplot(5, 2, 6)
    ax6.fill_between(r_range, pdf_z2 / pdf_z2.max(), alpha=0.5, color='blue', label='Z² prediction')
    ax6.fill_between(r_range, pdf_litebird / pdf_litebird.max(), alpha=0.5, color='green', label='LiteBIRD measurement')
    ax6.axvline(R_PREDICTED, color='b', linestyle='-', linewidth=2)
    ax6.axvline(0.036, color='r', linestyle='--', linewidth=2, label='BICEP/Keck limit')
    ax6.set_xlabel('Tensor-to-scalar ratio r', fontsize=12)
    ax6.set_ylabel('Probability density (normalized)', fontsize=12)
    ax6.set_title('Test 6: Tensor-to-Scalar Ratio r', fontsize=14, fontweight='bold')
    ax6.legend()
    ax6.grid(True, alpha=0.3)
    ax6.set_xlim(0, 0.04)

    # Panel 7: Fine Structure Constant
    ax7 = fig.add_subplot(5, 2, 7)
    z_vals = [0, 0, 1, 2, 4, 1100]
    da_vals = [0, 0, -0.5e-5, 1e-5, -2e-5, 0]
    err_vals = [1e-18, 1e-7, 1e-5, 2e-5, 3e-5, 4e-3]
    labels = ['Clocks', 'Oklo', 'QSO z~1', 'QSO z~2', 'QSO z~4', 'CMB']

    for i, (zv, da, err, lab) in enumerate(zip(z_vals, da_vals, err_vals, labels)):
        if zv < 10:
            ax7.errorbar(zv, da, yerr=err, fmt='o', markersize=10, capsize=5, label=lab)

    ax7.axhline(0, color='b', linewidth=2, linestyle='-', label='Z² prediction: Δα/α = 0')
    ax7.set_xlabel('Redshift z', fontsize=12)
    ax7.set_ylabel('Δα/α', fontsize=12)
    ax7.set_title('Test 7: Fine Structure Constant Constancy', fontsize=14, fontweight='bold')
    ax7.legend(loc='upper right', fontsize=8)
    ax7.grid(True, alpha=0.3)
    ax7.set_xlim(-0.5, 5)

    # Panel 8: Non-Gaussianity
    ax8 = fig.add_subplot(5, 2, 8)
    shapes = ['local', 'equilateral', 'orthogonal']
    z2_preds = [f_local, f_equil, f_ortho]
    planck_vals = [-0.9, -26, -38]
    planck_errs = [5.1, 47, 24]

    x_pos = np.arange(len(shapes))
    width = 0.35

    ax8.bar(x_pos - width/2, z2_preds, width, label='Z² prediction', color='blue', alpha=0.7)
    ax8.errorbar(x_pos + width/2, planck_vals, yerr=planck_errs, fmt='o', color='red',
                 markersize=10, capsize=5, label='Planck 2018')
    ax8.set_xticks(x_pos)
    ax8.set_xticklabels(shapes)
    ax8.set_ylabel('f_NL', fontsize=12)
    ax8.set_title('Test 8: Primordial Non-Gaussianity', fontsize=14, fontweight='bold')
    ax8.legend()
    ax8.grid(True, alpha=0.3, axis='y')

    # Panel 9: Cosmic Birefringence
    ax9 = fig.add_subplot(5, 2, 9)
    measurements = ['Minami+20', 'Planck PR4', 'Diego-P+22', 'Average']
    betas = [0.35, 0.30, 0.36, beta_avg]
    errors = [0.14, 0.11, 0.11, sigma_avg]

    ax9.errorbar(measurements, betas, yerr=errors, fmt='o', markersize=12, capsize=5, color='red')
    ax9.axhline(0, color='blue', linewidth=3, linestyle='-', label='Z² prediction: β = 0°')
    ax9.fill_between(measurements, -0.03, 0.03, alpha=0.3, color='blue', label='LiteBIRD 1σ reach')
    ax9.set_ylabel('Birefringence angle β (degrees)', fontsize=12)
    ax9.set_title('Test 9: Cosmic Birefringence', fontsize=14, fontweight='bold')
    ax9.legend()
    ax9.grid(True, alpha=0.3)

    # Panel 10: Summary Timeline
    ax10 = fig.add_subplot(5, 2, 10)
    tests = ['1. Crystal', '2. GW h_×', '3. Flatness', '4. Topology', '5. w(z)',
             '6. r', '7. α const', '8. f_NL', '9. Biref.', '10. GW phase']
    years = [2024, 2027, 2030, 2027, 2030, 2032, 2026, 2035, 2027, 2040]

    colors = ['green' if y <= 2026 else 'blue' if y <= 2030 else 'orange' for y in years]
    ax10.barh(tests, years, color=colors, alpha=0.7)
    ax10.axvline(2024, color='k', linestyle='-', linewidth=2)
    ax10.axvline(2030, color='gray', linestyle='--', linewidth=1)
    ax10.set_xlabel('Expected decisive result (year)', fontsize=12)
    ax10.set_title('Test 10: Experimental Timeline', fontsize=14, fontweight='bold')
    ax10.set_xlim(2023, 2042)
    ax10.grid(True, alpha=0.3, axis='x')

    # Add legend for timeline colors
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='green', alpha=0.7, label='Now (2024-2026)'),
                       Patch(facecolor='blue', alpha=0.7, label='Near-term (2027-2030)'),
                       Patch(facecolor='orange', alpha=0.7, label='Long-term (2030+)')]
    ax10.legend(handles=legend_elements, loc='lower right')

    plt.tight_layout()
    plt.savefig('/Users/carlzimmerman/new_physics/zimmerman-formula/research/experimental_tests/experimental_tests_analysis.png',
                dpi=150, bbox_inches='tight')
    plt.close()

    print("\n" + "=" * 70)
    print("VISUALIZATION SAVED")
    print("=" * 70)
    print("Output: experimental_tests_analysis.png")

# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    # Create output directory if needed
    import os
    os.makedirs('/Users/carlzimmerman/new_physics/zimmerman-formula/research/experimental_tests', exist_ok=True)

    # Run all analyses and create visualization
    create_visualization()

    # Print summary
    print("\n" + "=" * 70)
    print("SUMMARY: 10 EXPERIMENTAL TESTS FOR Z² FRAMEWORK")
    print("=" * 70)
    print("""
    IMMEDIATE (NOW):
    1. Crystal Magic Angle - Tabletop resistivity measurement

    NEAR-TERM (2025-2027):
    2. GW h_× = 0 Test - LIGO O4/O5 catalog analysis
    7. α Constancy - Ongoing atomic clock comparisons
    9. Birefringence - Planck/LiteBIRD polarization

    MEDIUM-TERM (2027-2032):
    4. CMB Topology - LiteBIRD pattern search
    5. Dark Energy w(z) - DESI/Euclid precision
    6. Tensor-to-Scalar r - LiteBIRD measurement

    LONG-TERM (2032+):
    3. Ultra-Precision Flatness - Combined probes
    8. Non-Gaussianity - 21cm cosmology
    10. GW Phase - Einstein Telescope

    KEY DISCRIMINATING TESTS:
    - Test 2 (h_× = 0): GR predicts h_× ≈ h_+, Z² predicts exactly 0
    - Test 5 (w = -1): DESI hints at w ≠ -1, Z² requires exactly -1
    - Test 6 (r = 0.015): Specific value, narrow range
    - Test 9 (β = 0): Current 3σ tension with Z² prediction

    MOST URGENT: Test 9 (birefringence) shows 3σ tension already!
    """)
