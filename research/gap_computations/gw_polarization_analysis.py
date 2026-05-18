#!/usr/bin/env python3
"""
Gravitational Wave Polarization Analysis for Z² Framework

╔══════════════════════════════════════════════════════════════════════════════╗
║                           ⚠️  RETRACTED ANALYSIS  ⚠️                          ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  The h_× = 0 prediction analyzed in this script has been RETRACTED.          ║
║                                                                              ║
║  REASON: The Z₂ orbifold acts on extra dimensions (y → -y), NOT on 4D       ║
║  spacetime. The metric perturbation h_μν has indices μ,ν ∈ {0,1,2,3} only — ║
║  no y-indices. Under this action:                                            ║
║                                                                              ║
║    h_+(x, y) → h_+(x, -y) = h_+(x, y)  [Z₂-EVEN]                            ║
║    h_×(x, y) → h_×(x, -y) = h_×(x, y)  [Z₂-EVEN]                            ║
║                                                                              ║
║  BOTH polarizations are Z₂-even and SURVIVE. Neither is projected out.      ║
║                                                                              ║
║  CORRECT Z² PREDICTION: Standard 2 GW polarizations (same as GR)            ║
║                                                                              ║
║  See: /research/dynamical_framework/HONEST_DERIVATION_AUDIT.md (line 549)   ║
║       /research/dynamical_framework/GW_POLARIZATION_DERIVATION.md           ║
║       /papers/latex_series/07_gravitational_waves_z2_framework.tex          ║
║                                                                              ║
║  This script is preserved for historical reference only.                     ║
╚══════════════════════════════════════════════════════════════════════════════╝

ORIGINAL PURPOSE (now invalid):
1. Statistical power to distinguish h_× = 0 from GR
2. Simulated detector responses
3. Bayesian model comparison
4. Required number of events for definitive test

Carl Zimmerman | May 2026
RETRACTION DATE: May 2026
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.special import erfc
from typing import Tuple, List, Dict
import warnings
warnings.filterwarnings('ignore')

# Z² Constants
Z_SQUARED = 32 * np.pi / 3  # = 33.510321638...
Z = np.sqrt(Z_SQUARED)       # = 5.788810...

print("=" * 70)
print("⚠️  RETRACTED ANALYSIS - FOR HISTORICAL REFERENCE ONLY  ⚠️")
print("=" * 70)
print()
print("The h_× = 0 prediction has been RETRACTED.")
print("Reason: Z₂ acts on extra dimensions (y → -y), not 4D spacetime.")
print("Both h_+ and h_× are Z₂-EVEN and survive.")
print()
print("CORRECT Z² PREDICTION: Standard 2 GW polarizations (same as GR)")
print()
print("See: HONEST_DERIVATION_AUDIT.md for details")
print("=" * 70)
print()
print("--- Original analysis below (for historical reference) ---")
print()
print("=" * 70)
print("GRAVITATIONAL WAVE POLARIZATION ANALYSIS [RETRACTED]")
print("Original claim: h_× = 0 (cross polarization projected out)")
print("=" * 70)

# =============================================================================
# 1. DETECTOR ANTENNA PATTERNS
# =============================================================================

def antenna_pattern_plus(theta: float, phi: float, psi: float) -> float:
    """
    Antenna pattern function F_+ for a GW detector.

    Parameters:
        theta: polar angle of source
        phi: azimuthal angle of source
        psi: polarization angle
    """
    F_plus = 0.5 * (1 + np.cos(theta)**2) * np.cos(2*phi) * np.cos(2*psi)
    F_plus -= np.cos(theta) * np.sin(2*phi) * np.sin(2*psi)
    return F_plus

def antenna_pattern_cross(theta: float, phi: float, psi: float) -> float:
    """
    Antenna pattern function F_× for a GW detector.
    """
    F_cross = 0.5 * (1 + np.cos(theta)**2) * np.cos(2*phi) * np.sin(2*psi)
    F_cross += np.cos(theta) * np.sin(2*phi) * np.cos(2*psi)
    return F_cross

# Average over sky and polarization
def compute_average_antenna_response():
    """Compute sky-averaged antenna response for + and × polarizations."""
    n_samples = 10000

    # Random sky positions and polarization angles
    np.random.seed(42)
    cos_theta = np.random.uniform(-1, 1, n_samples)
    theta = np.arccos(cos_theta)
    phi = np.random.uniform(0, 2*np.pi, n_samples)
    psi = np.random.uniform(0, np.pi, n_samples)

    F_plus_sq = np.array([antenna_pattern_plus(t, p, ps)**2
                          for t, p, ps in zip(theta, phi, psi)])
    F_cross_sq = np.array([antenna_pattern_cross(t, p, ps)**2
                           for t, p, ps in zip(theta, phi, psi)])

    avg_F_plus_sq = np.mean(F_plus_sq)
    avg_F_cross_sq = np.mean(F_cross_sq)

    return avg_F_plus_sq, avg_F_cross_sq

print("\n" + "=" * 70)
print("1. DETECTOR ANTENNA RESPONSE")
print("=" * 70)

avg_Fp2, avg_Fx2 = compute_average_antenna_response()
print(f"Sky-averaged <F_+²> = {avg_Fp2:.4f}")
print(f"Sky-averaged <F_×²> = {avg_Fx2:.4f}")
print(f"Ratio <F_+²>/<F_×²> = {avg_Fp2/avg_Fx2:.4f}")

# Power ratio
GR_power = avg_Fp2 + avg_Fx2
Z2_power = avg_Fp2  # h_× = 0
print(f"\nGR total power: <F_+² + F_×²> = {GR_power:.4f}")
print(f"Z² total power: <F_+²> only = {Z2_power:.4f}")
print(f"Z²/GR power ratio = {Z2_power/GR_power:.3f}")
print("\n→ Z² predicts ~50% less detected power averaged over sky")

# =============================================================================
# 2. SIMULATED GW EVENTS
# =============================================================================

def simulate_gw_event(snr: float, inclination: float, model: str = 'GR') -> Dict:
    """
    Simulate a GW event with given SNR and inclination.

    Parameters:
        snr: signal-to-noise ratio
        inclination: binary inclination angle (radians)
        model: 'GR' or 'Z2'

    Returns:
        Dictionary with h_+, h_×, measured values, uncertainties
    """
    # True amplitudes (circular binary)
    h_plus_true = (1 + np.cos(inclination)**2) / 2
    h_cross_true = np.cos(inclination) if model == 'GR' else 0.0

    # Normalize to unit total amplitude for GR
    norm = np.sqrt(h_plus_true**2 + np.cos(inclination)**2)
    h_plus_true /= norm
    if model == 'GR':
        h_cross_true /= norm

    # Measurement uncertainty scales as 1/SNR
    sigma = 1.0 / snr

    # Measured values with noise
    h_plus_meas = h_plus_true + np.random.normal(0, sigma)
    h_cross_meas = h_cross_true + np.random.normal(0, sigma)

    return {
        'h_plus_true': h_plus_true,
        'h_cross_true': h_cross_true,
        'h_plus_meas': h_plus_meas,
        'h_cross_meas': h_cross_meas,
        'sigma': sigma,
        'snr': snr,
        'inclination': inclination,
        'model': model
    }

print("\n" + "=" * 70)
print("2. SIMULATED GW EVENTS")
print("=" * 70)

# Simulate events for both models
np.random.seed(123)
n_events = 100
snr_values = np.random.uniform(10, 50, n_events)
inclinations = np.arccos(np.random.uniform(-1, 1, n_events))

events_GR = [simulate_gw_event(snr, inc, 'GR')
             for snr, inc in zip(snr_values, inclinations)]
events_Z2 = [simulate_gw_event(snr, inc, 'Z2')
             for snr, inc in zip(snr_values, inclinations)]

# Extract h_× measurements
h_cross_GR = np.array([e['h_cross_meas'] for e in events_GR])
h_cross_Z2 = np.array([e['h_cross_meas'] for e in events_Z2])
sigmas = np.array([e['sigma'] for e in events_GR])

print(f"Simulated {n_events} events with SNR ~ 10-50")
print(f"\nGR model (h_× ≠ 0):")
print(f"  Mean |h_×|: {np.mean(np.abs(h_cross_GR)):.4f}")
print(f"  Std h_×: {np.std(h_cross_GR):.4f}")

print(f"\nZ² model (h_× = 0):")
print(f"  Mean |h_×|: {np.mean(np.abs(h_cross_Z2)):.4f} (from noise only)")
print(f"  Std h_×: {np.std(h_cross_Z2):.4f}")

# =============================================================================
# 3. STATISTICAL TESTS
# =============================================================================

def compute_chi_squared(h_cross_measured: np.ndarray,
                        sigmas: np.ndarray,
                        model: str) -> float:
    """
    Compute χ² for null hypothesis h_× = 0 or alternative h_× ≠ 0.
    """
    if model == 'Z2':  # H0: h_× = 0
        chi2 = np.sum((h_cross_measured / sigmas)**2)
    else:  # H1: h_× = expected from GR
        # For GR, we expect h_× ~ O(1) for random inclinations
        expected = 0.5  # rough expectation for |h_×|
        chi2 = np.sum(((h_cross_measured - expected) / sigmas)**2)
    return chi2

print("\n" + "=" * 70)
print("3. STATISTICAL HYPOTHESIS TESTING")
print("=" * 70)

# Test 1: Is h_× = 0 consistent with data?
# Under Z² (true): h_× = 0, so h_×/σ ~ N(0,1), and Σ(h_×/σ)² ~ χ²(N)
# Under GR (true): h_× ≠ 0, so test should reject h_× = 0

chi2_Z2_data = np.sum((h_cross_Z2 / sigmas)**2)
chi2_GR_data = np.sum((h_cross_GR / sigmas)**2)

print(f"\nTest: H₀ = h_× = 0 vs H₁ = h_× ≠ 0")
print(f"χ² statistic = Σ(h_×/σ)²")
print(f"Expected under H₀: χ²({n_events}) with mean = {n_events}")

print(f"\nFor Z² model data:")
print(f"  χ² = {chi2_Z2_data:.1f}")
print(f"  p-value = {1 - stats.chi2.cdf(chi2_Z2_data, n_events):.4f}")
print(f"  → {'CONSISTENT' if chi2_Z2_data < n_events + 3*np.sqrt(2*n_events) else 'INCONSISTENT'} with h_× = 0")

print(f"\nFor GR model data:")
print(f"  χ² = {chi2_GR_data:.1f}")
print(f"  p-value = {1 - stats.chi2.cdf(chi2_GR_data, n_events):.6f}")
print(f"  → {'CONSISTENT' if chi2_GR_data < n_events + 3*np.sqrt(2*n_events) else 'REJECTS'} h_× = 0")

# =============================================================================
# 4. BAYESIAN MODEL COMPARISON
# =============================================================================

def log_likelihood_Z2(h_cross: np.ndarray, sigmas: np.ndarray) -> float:
    """Log-likelihood under Z² model (h_× = 0)."""
    return np.sum(stats.norm.logpdf(h_cross, loc=0, scale=sigmas))

def log_likelihood_GR(h_cross: np.ndarray, sigmas: np.ndarray,
                       h_cross_true: np.ndarray) -> float:
    """Log-likelihood under GR model (h_× = expected)."""
    return np.sum(stats.norm.logpdf(h_cross, loc=h_cross_true, scale=sigmas))

print("\n" + "=" * 70)
print("4. BAYESIAN MODEL COMPARISON")
print("=" * 70)

# For Z² data
ll_Z2_model_Z2data = log_likelihood_Z2(h_cross_Z2, sigmas)
ll_GR_model_Z2data = log_likelihood_GR(h_cross_Z2, sigmas,
                                        np.array([e['h_cross_true'] for e in events_GR]))
log_BF_Z2data = ll_Z2_model_Z2data - ll_GR_model_Z2data

print(f"\nUsing Z² simulated data:")
print(f"  log P(data|Z²) = {ll_Z2_model_Z2data:.1f}")
print(f"  log P(data|GR) = {ll_GR_model_Z2data:.1f}")
print(f"  log Bayes Factor = {log_BF_Z2data:.1f}")
print(f"  → {'Z² strongly favored' if log_BF_Z2data > 5 else 'Z² favored' if log_BF_Z2data > 0 else 'GR favored'}")

# For GR data
ll_Z2_model_GRdata = log_likelihood_Z2(h_cross_GR, sigmas)
h_cross_true_GR = np.array([e['h_cross_true'] for e in events_GR])
ll_GR_model_GRdata = log_likelihood_GR(h_cross_GR, sigmas, h_cross_true_GR)
log_BF_GRdata = ll_Z2_model_GRdata - ll_GR_model_GRdata

print(f"\nUsing GR simulated data:")
print(f"  log P(data|Z²) = {ll_Z2_model_GRdata:.1f}")
print(f"  log P(data|GR) = {ll_GR_model_GRdata:.1f}")
print(f"  log Bayes Factor = {log_BF_GRdata:.1f}")
print(f"  → {'Z² strongly favored' if log_BF_GRdata > 5 else 'Z² favored' if log_BF_GRdata > 0 else 'GR strongly favored'}")

# =============================================================================
# 5. POWER ANALYSIS: HOW MANY EVENTS NEEDED?
# =============================================================================

def required_events_for_detection(significance: float = 5.0,
                                   avg_snr: float = 20.0) -> int:
    """
    Calculate number of events needed to distinguish Z² from GR.

    Parameters:
        significance: required sigma level (e.g., 5 for 5σ)
        avg_snr: average SNR of events

    Returns:
        Number of events needed
    """
    # Under GR: E[h_×²] ~ 0.25 (for random inclinations)
    # Under Z²: E[h_×²] = 0
    # Measurement variance: σ² ~ 1/SNR²

    # The test statistic Σ(h_×/σ)² has:
    # Under Z²: mean = N, var = 2N
    # Under GR: mean = N + N×<h_×²>×SNR², var = 2N + O(N×SNR²)

    # For separation at `significance` sigma:
    # N + N×0.25×SNR² - N > significance × sqrt(2N)
    # N×0.25×SNR² > significance × sqrt(2N)
    # N > (significance × sqrt(2))² / (0.25 × SNR²)²

    expected_h_cross_sq = 0.25  # average for random inclinations
    delta_chi2_per_event = expected_h_cross_sq * avg_snr**2

    # Need total delta_chi2 > significance × sqrt(2N)
    # delta_chi2 = N × delta_chi2_per_event
    # N × delta_chi2_per_event > significance × sqrt(2N)
    # sqrt(N) > significance × sqrt(2) / delta_chi2_per_event
    # N > 2 × significance² / delta_chi2_per_event²

    N_required = int(np.ceil(2 * significance**2 / delta_chi2_per_event**2))

    # More accurate: solve N × Δ = sig × √(2N)
    # N = 2 sig² / Δ² where Δ = expected_h_cross_sq × SNR²

    return max(1, N_required)

print("\n" + "=" * 70)
print("5. POWER ANALYSIS: EVENTS REQUIRED FOR DETECTION")
print("=" * 70)

for sig in [3, 5]:
    for snr in [15, 20, 30, 50]:
        n_req = required_events_for_detection(sig, snr)
        # More accurate calculation
        delta_per_event = 0.25 * snr**2
        # Solving: N × delta > sig × sqrt(2N)
        # N > 2 sig² / delta² (approximate)
        n_approx = max(1, int(2 * sig**2 / delta_per_event + 0.5))
        print(f"  {sig}σ detection with SNR={snr}: ~{n_approx} events")

# More refined calculation using simulation
print("\n--- Monte Carlo power calculation ---")

def monte_carlo_power(n_events: int, avg_snr: float, n_trials: int = 1000) -> float:
    """
    Monte Carlo calculation of detection power.

    Returns probability of correctly identifying Z² vs GR.
    """
    correct_Z2 = 0
    correct_GR = 0

    for _ in range(n_trials):
        snrs = np.random.uniform(avg_snr*0.5, avg_snr*1.5, n_events)
        incs = np.arccos(np.random.uniform(-1, 1, n_events))
        sigmas = 1.0 / snrs

        # Generate Z² data
        h_cross_Z2 = np.random.normal(0, sigmas)

        # Generate GR data
        h_cross_true_GR = np.cos(incs) / np.sqrt((1+np.cos(incs)**2)**2/4 + np.cos(incs)**2)
        h_cross_GR = h_cross_true_GR + np.random.normal(0, sigmas)

        # Chi-squared test
        chi2_Z2 = np.sum((h_cross_Z2 / sigmas)**2)
        chi2_GR = np.sum((h_cross_GR / sigmas)**2)

        threshold = n_events + 3*np.sqrt(2*n_events)  # 3σ threshold

        if chi2_Z2 < threshold:
            correct_Z2 += 1
        if chi2_GR > threshold:
            correct_GR += 1

    return correct_Z2/n_trials, correct_GR/n_trials

print(f"\nMonte Carlo power analysis (1000 trials each):")
print(f"{'N events':<10} {'SNR':<8} {'P(detect Z²|Z²)':<18} {'P(detect GR|GR)':<18}")
print("-" * 54)

for n_ev in [10, 25, 50, 100]:
    for snr in [20, 30]:
        p_z2, p_gr = monte_carlo_power(n_ev, snr, 500)
        print(f"{n_ev:<10} {snr:<8} {p_z2:<18.3f} {p_gr:<18.3f}")

# =============================================================================
# 6. VISUALIZATIONS
# =============================================================================

print("\n" + "=" * 70)
print("6. GENERATING VISUALIZATIONS")
print("=" * 70)

fig, axes = plt.subplots(2, 2, figsize=(14, 12))

# Plot 1: h_× distribution comparison
ax1 = axes[0, 0]
bins = np.linspace(-0.8, 0.8, 40)
ax1.hist(h_cross_GR, bins=bins, alpha=0.6, label='GR (h_× ≠ 0)',
         density=True, color='blue')
ax1.hist(h_cross_Z2, bins=bins, alpha=0.6, label='Z² (h_× = 0)',
         density=True, color='red')
ax1.axvline(0, color='black', linestyle='--', linewidth=2, label='h_× = 0 (Z² prediction)')
ax1.set_xlabel('Measured h_×', fontsize=12)
ax1.set_ylabel('Probability Density', fontsize=12)
ax1.set_title('Distribution of Cross Polarization Measurements', fontsize=14)
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)

# Plot 2: χ² distribution
ax2 = axes[0, 1]
# Simulate many realizations
n_trials = 1000
chi2_Z2_dist = []
chi2_GR_dist = []

for _ in range(n_trials):
    h_x_z2 = np.random.normal(0, sigmas)
    h_x_gr = h_cross_true_GR + np.random.normal(0, sigmas)
    chi2_Z2_dist.append(np.sum((h_x_z2/sigmas)**2))
    chi2_GR_dist.append(np.sum((h_x_gr/sigmas)**2))

bins_chi2 = np.linspace(50, 250, 50)
ax2.hist(chi2_Z2_dist, bins=bins_chi2, alpha=0.6, label='Z² model',
         density=True, color='red')
ax2.hist(chi2_GR_dist, bins=bins_chi2, alpha=0.6, label='GR model',
         density=True, color='blue')

# Theoretical χ² distribution for Z²
x_chi2 = np.linspace(50, 250, 100)
ax2.plot(x_chi2, stats.chi2.pdf(x_chi2, n_events), 'r--', linewidth=2,
         label=f'χ²({n_events}) theory')
ax2.axvline(n_events, color='black', linestyle=':', label=f'Expected (n={n_events})')
ax2.set_xlabel('χ² = Σ(h_×/σ)²', fontsize=12)
ax2.set_ylabel('Probability Density', fontsize=12)
ax2.set_title('Test Statistic Distribution', fontsize=14)
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)

# Plot 3: Power curve
ax3 = axes[1, 0]
n_events_range = np.arange(5, 101, 5)
power_3sigma = []
power_5sigma = []

for n_ev in n_events_range:
    # Approximate power calculation
    # Under GR: chi2 ~ N + N×0.25×SNR² with variance ~ 2N + ...
    avg_snr = 25
    delta = 0.25 * avg_snr**2 * n_ev / np.sqrt(2*n_ev)
    power_3sigma.append(stats.norm.cdf(delta - 3))
    power_5sigma.append(stats.norm.cdf(delta - 5))

ax3.plot(n_events_range, power_3sigma, 'b-o', label='3σ detection', linewidth=2)
ax3.plot(n_events_range, power_5sigma, 'r-s', label='5σ detection', linewidth=2)
ax3.axhline(0.9, color='gray', linestyle='--', label='90% power')
ax3.axhline(0.99, color='gray', linestyle=':', label='99% power')
ax3.set_xlabel('Number of Events', fontsize=12)
ax3.set_ylabel('Detection Power', fontsize=12)
ax3.set_title(f'Power to Distinguish Z² from GR (avg SNR={avg_snr})', fontsize=14)
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.3)
ax3.set_ylim([0, 1.05])

# Plot 4: Antenna pattern visualization
ax4 = axes[1, 1]
theta_grid = np.linspace(0, np.pi, 100)
phi = 0
psi = 0

F_plus = np.array([antenna_pattern_plus(t, phi, psi) for t in theta_grid])
F_cross = np.array([antenna_pattern_cross(t, phi, psi) for t in theta_grid])

ax4.plot(np.degrees(theta_grid), F_plus**2, 'b-', label='F_+²', linewidth=2)
ax4.plot(np.degrees(theta_grid), F_cross**2, 'r-', label='F_×²', linewidth=2)
ax4.fill_between(np.degrees(theta_grid), 0, F_plus**2, alpha=0.3, color='blue')
ax4.fill_between(np.degrees(theta_grid), 0, F_cross**2, alpha=0.3, color='red')
ax4.set_xlabel('Source Polar Angle θ (degrees)', fontsize=12)
ax4.set_ylabel('Antenna Pattern Squared', fontsize=12)
ax4.set_title('Detector Response vs Source Direction (φ=0, ψ=0)', fontsize=14)
ax4.legend(fontsize=10)
ax4.grid(True, alpha=0.3)

plt.suptitle('Z² GW Polarization Analysis: h_× = 0 Prediction', fontsize=16, y=1.02)
plt.tight_layout()
plt.savefig('/Users/carlzimmerman/new_physics/zimmerman-formula/research/gap_computations/gw_polarization_analysis.png',
            dpi=150, bbox_inches='tight')
plt.close()
print("Saved: gw_polarization_analysis.png")

# =============================================================================
# 7. SUMMARY
# =============================================================================

print("\n" + "=" * 70)
print("SUMMARY: GW POLARIZATION TEST OF Z² FRAMEWORK")
print("=" * 70)

print("""
╔═════════════════════════════════════════════════════════════════════╗
║              ⚠️  THIS ANALYSIS HAS BEEN RETRACTED  ⚠️                ║
╠═════════════════════════════════════════════════════════════════════╣
║                                                                     ║
║  ORIGINAL CLAIM (WRONG):                                            ║
║    h_× = 0 (cross polarization projected out by Z₂)                 ║
║                                                                     ║
║  CORRECTION:                                                        ║
║    The Z₂ orbifold acts on extra dimensions (y → -y), NOT on 4D    ║
║    spacetime indices. Since h_μν has μ,ν ∈ {0,1,2,3}, BOTH         ║
║    polarizations h_+ and h_× are Z₂-EVEN and survive.              ║
║                                                                     ║
║  CORRECT Z² PREDICTION:                                             ║
║    Standard 2 GW polarizations (identical to General Relativity)    ║
║    No exotic polarization modes (KK modes too heavy)                ║
║                                                                     ║
║  WHAT Z² ACTUALLY PREDICTS FOR GWs:                                 ║
║    • r = 0.015 ± 0.002 (tensor-to-scalar ratio) [CONJECTURED]      ║
║    • n_t = -r/8 ≈ -0.002 (tensor spectral index)                   ║
║    • Both h_+ and h_× present (standard GR)                        ║
║    • No extra polarization modes                                    ║
║                                                                     ║
║  The analysis above is preserved for historical reference only.     ║
║                                                                     ║
╚═════════════════════════════════════════════════════════════════════╝
""")

print("\nRetracted analysis complete (historical reference only).")
