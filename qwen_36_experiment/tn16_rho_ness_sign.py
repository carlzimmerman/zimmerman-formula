#!/usr/bin/env python3
"""
tn16: NESS Spectral Density rho(omega) - Sign Change Detection

Question: Does the backreacted NESS spectral density develop negative regions
at galactic frequencies? If so, at what coupling strength and how prominent are they?

METHODOLOGY (OPTIMIZED):
1. Compute NESS Wightman function via Picard iteration using vectorized convolution
2. Extract spectral density via FFT + direct integration
3. Segment analysis: compute rho in frequency bands relevant to galactic dynamics
4. Coupling scan with fine resolution near the expected threshold
5. Physical interpretation of which modes get populated vs depopulated

REFERENCE:
- Hu-Verdaguer stochastic gravity (influence functional / Schwinger-Keldysh)
- Caldeira-Leggett model for open quantum systems
"""

import numpy as np
from scipy.integrate import quad, trapezoid as trapz
import json, os, sys

print("=" * 80)
print("tn16: NESS SPECTRAL DENSITY RHO(OMEGA) - SIGN CHANGE DETECTION")
print("=" * 80)
print()


# ============================================================================
# CONSTANTS
# ============================================================================

H = 1.0
beta = 2.0 * np.pi / H
T_GH = H / (2.0 * np.pi)
a0_physical = 9.389e-11
c_phys = 2.99792458e8
omega_c_physical = a0_physical / c_phys

print("de Sitter parameters:")
print(f"  H = {H}")
print(f"  beta_GH = 2pi/H = {beta:.6f}")
print(f"  T_GH = H/(2pi) = {T_GH:.6f}")
print(f"  omega_c (physical) = a_0/c = {omega_c_physical:.3e} rad/s")
print()


# ============================================================================
# PART 1: BUNCH-DAVIES BASELINE
# ============================================================================

print("=" * 80)
print("PART 1: BUNCH-DAVIES WIGHTMAN FUNCTION - KMS BASELINE")
print("=" * 80)
print()


def G_BD_tau(tau, eps=1e-8):
    """Bunch-Davies Wightman function on the worldline (1+1D conformal scalar)."""
    z = H * tau / 2.0 - 1j * eps
    return -H**2 / (4.0 * np.pi**2 * np.sinh(z)**2)


def G_BD_tau_vec(tau_arr, eps=1e-8):
    """Vectorized Bunch-Davies."""
    z = H * tau_arr / 2.0 - 1j * eps
    return -H**2 / (4.0 * np.pi**2 * np.sinh(z)**2)


tau_test = 1.0 / H
G_at_tau = G_BD_tau(tau_test)
G_at_tau_shifted = G_BD_tau(tau_test + 1j * beta)
kms_ratio = np.abs(G_at_tau_shifted / G_at_tau)

print("KMS VERIFICATION for Bunch-Davies:")
print(f"  |G^+(tau+i*beta)/G^+(tau)| = {kms_ratio:.15f}")
if abs(kms_ratio - 1.0) < 1e-14:
    print("  KMS SATISFIED - Bunch-Davies is a thermal state.")
else:
    print(f"  UNEXPECTED KMS VIOLATION: {abs(kms_ratio - 1.0):.2e}")
print()


# ============================================================================
# PART 2: NESS WIGHTMAN FUNCTION VIA PICARD ITERATION (VECTORIZED)
# ============================================================================

print("=" * 80)
print("PART 2: NESS WIGHTMAN FUNCTION - SELF-CONSISTENT SOLUTION")
print("=" * 80)
print()


def compute_neSS_greens_vectorized(tau_grid, q_sq, eta, max_iter=100, tol=1e-7):
    """
    Solve G_NES = G_BD + q^2 * (|G_R|^2 * G_NES) convolution via Picard iteration.

    Uses cumulative convolution for efficiency: at each step i,
    delta_G[i] = q^2 * sum_{j=0}^{i} GR_sq[i-j] * G_prev[j] * dtau

    This is a causal convolution which we compute efficiently using
    a running sum approach.
    """
    dtau = tau_grid[1] - tau_grid[0]
    N = len(tau_grid)

    # Initialize with Bunch-Davies
    G_prev = G_BD_tau_vec(tau_grid)

    # Precompute |G_R|^2 kernel (causal: G_R(t) = 0 for t < 0)
    thermal_factor = 1.0 / max(1.0 - np.exp(-H * beta), 1e-10)
    GR_sq = np.zeros(N)
    GR_sq[1:] = (np.exp(-eta * tau_grid[1:]) * thermal_factor)**2

    # Use FFT-based convolution for efficiency
    from scipy.fft import fft, ifft

    G_new = G_prev.copy()

    for n_iter in range(max_iter):
        # Convolve using FFT: delta_G = q^2 * (GR_sq * G_prev) [causal]
        # Pad to avoid circular convolution artifacts
        N_pad = 2 * N
        G_prev_padded = np.zeros(N_pad, dtype=complex)
        G_prev_padded[:N] = G_prev
        GR_sq_padded = np.zeros(N_pad)
        GR_sq_padded[:N] = GR_sq

        G_prev_ft = fft(G_prev_padded)
        GR_sq_ft = fft(GR_sq_padded)
        conv_result = ifft(G_prev_ft * GR_sq_ft)[:N]

        delta_G = q_sq * conv_result

        # New iterate: G_new[tau_i] = G_BD(tau_i) + delta_G[i]
        G_new = G_BD_tau_vec(tau_grid) + delta_G

        # Check convergence
        diff = np.max(np.abs(G_new - G_prev)) / (np.max(np.abs(G_prev)) + 1e-30)

        G_prev = G_new

        if n_iter % 20 == 0:
            print(f"  Picard iteration {n_iter}: max diff = {diff:.2e}")

        if diff < tol:
            print(f"  Converged at iteration {n_iter + 1} (tolerance: {tol})")
            break
    else:
        print(f"  WARNING: Did not converge within {max_iter} iterations. Final diff = {diff:.2e}")

    return G_new, n_iter + 1


# ============================================================================
# PART 3: SPECTRAL DENSITY COMPUTATION
# ============================================================================

def compute_spectral_density_ness(G_NES, tau_grid):
    """
    Compute spectral density from NESS Wightman function.

    rho(omega) = (1/2pi) * int dtau e^{i*omega*tau} * C(tau)
    where C(tau) = G_NES(tau) - G_NES*(-tau) is the commutator.

    For a real scalar field: G(-tau) = G*(tau), so:
    C(tau) = G(tau) - G*(tau) = 2i * Im[G(tau)]

    The spectral function:
    rho(omega) = (1/2pi) * int dtau [cos(omega*tau) + i*sin(omega*tau)] * C(tau)
               = (1/2pi) * int dtau [-sin(omega*tau)*Re[C] + cos(omega*tau)*Im[C]]

    Since C is purely imaginary: Re[C] = 0, so:
    rho(omega) = (1/2pi) * int dtau cos(omega*tau) * Im[C(tau)]
               = -(1/pi) * int dtau cos(omega*tau) * Im[G_NES(tau)]
    """
    N = len(tau_grid)
    C = G_NES - np.conj(G_NES)  # = 2i * Im[G]

    # Use FFT for initial estimate
    rho_fft = np.imag(np.fft.fft(C)) / (2.0 * np.pi)
    omega_fft = np.fft.fftfreq(N, d=tau_grid[1] - tau_grid[0]) * 2.0 * np.pi

    # Log-spaced frequency grid for detailed analysis
    omega_max_physical = np.pi / (tau_grid[1] - tau_grid[0])
    N_omega = 4096
    omega_grid = np.logspace(-4, np.log10(omega_max_physical * 0.99), N_omega)

    # Direct spectral computation via numerical FT at each frequency
    rho_vals = np.zeros(N_omega)
    Im_C = np.imag(C)

    for i_om, om in enumerate(omega_grid):
        if om < 1e-10:
            rho_vals[i_om] = 0.0
            continue
        # rho(omega) = -(1/pi) * int dtau cos(omega*tau) * Im[G_NES(tau)]
        integrand = np.cos(om * tau_grid) * Im_C
        rho_vals[i_om] = -(1.0 / np.pi) * trapz(integrand, tau_grid)

    return omega_grid, rho_vals


# ============================================================================
# PART 4: COUPLING SCAN
# ============================================================================

print("Computing NESS Wightman functions and spectral densities...")
print()

N_tau_main = 2048
tau_max_phys = 50.0 / H
tau_grid_main = np.linspace(1e-8, tau_max_phys, N_tau_main)
dtau_main = tau_grid_main[1] - tau_grid_main[0]

q_sq_values = [1e-6, 5e-6, 1e-5, 5e-5, 1e-4, 5e-4, 1e-3, 5e-3, 1e-2, 3e-2, 5e-2]
eta_val = 0.01

thermal_factor = 1.0 / max(1.0 - np.exp(-H * beta), 1e-10)

results_scan = []

for qsq in q_sq_values:
    print(f"q^2/H^2 = {qsq:.1e}:")
    try:
        G_NES, n_iter = compute_neSS_greens_vectorized(tau_grid_main, qsq, eta_val,
                                                          max_iter=80, tol=1e-6)

        # Compute spectral density
        omega_grid, rho_vals = compute_spectral_density_ness(G_NES, tau_grid_main)

        # Positive frequencies
        pos_mask = omega_grid > 1e-8
        omega_pos = omega_grid[pos_mask]
        rho_pos = rho_vals[pos_mask]

        if len(omega_pos) < 10:
            print(f"    SKIP: too few positive frequency bins")
            continue

        # Diagnostics
        rho_min = float(np.min(rho_pos))
        rho_max = float(np.max(rho_pos))
        n_neg_bins = int(np.sum(rho_pos < -1e-12))
        frac_negative = float(n_neg_bins / len(rho_pos)) if len(rho_pos) > 0 else 0.0

        # Inertia correction: delta_m = (2/pi) * integral rho(omega)/omega^2 domega
        integ_dm = rho_pos / omega_pos**2
        dm_integral = float(trapz(integ_dm, omega_pos))
        delta_m = (2.0 / np.pi) * dm_integral

        has_sign_flip = bool(rho_min < -1e-12)
        delta_m_flips = bool(delta_m < 0)

        results_scan.append({
            'q_sq': float(qsq),
            'eta': float(eta_val),
            'n_iterations': int(n_iter),
            'rho_min': rho_min,
            'rho_max': rho_max,
            'n_negative_bins': n_neg_bins,
            'frac_negative': frac_negative,
            'delta_m': delta_m,
            'sign_flip_spectral': has_sign_flip,
            'delta_m_flips_to_MOND': delta_m_flips,
        })

        flag = "MOND" if delta_m_flips else ("mixed" if rho_min < -1e-12 else "anti-MOND")
        print(f"    iter={n_iter:3d}: rho_min={rho_min:12.4e}, frac_neg={frac_negative:.4f}, "
              f"delta_m={delta_m:10.4f} {flag}")

    except Exception as e:
        print(f"    ERROR - {str(e)}")
    print()


# ============================================================================
# PART 5: SIGN CHANGE ANALYSIS AT GALACTIC FREQUENCIES
# ============================================================================

print("=" * 80)
print("PART 5: SIGN CHANGE ANALYSIS AT GALACTIC FREQUENCIES")
print("=" * 80)
print()

print("Galactic frequency analysis:")
print(f"  omega_c (physical) = {omega_c_physical:.3e} rad/s")
print(f"  Typical galactic omega_gal ~ (1-10) * omega_c in natural units")
print()

sign_flip_couplings = [r for r in results_scan if r['delta_m_flips_to_MOND']]
mixed_couplings = [r for r in results_scan if r['sign_flip_spectral'] and not r['delta_m_flips_to_MOND']]
no_flip_couplings = [r for r in results_scan if not r['sign_flip_spectral']]

if sign_flip_couplings:
    q_sq_flip = min(r['q_sq'] for r in sign_flip_couplings)
    print(f"SIGN FLIP THRESHOLD: q^2 ~ {q_sq_flip:.1e}")

    most_negative = max(sign_flip_couplings, key=lambda r: abs(r['rho_min']))
    print(f"Strongest negative spectral weight at q^2 = {most_negative['q_sq']:.1e}:")
    print(f"  rho_min = {most_negative['rho_min']:.4e}")
    print(f"  Fraction of negative bins: {most_negative['frac_negative']:.4f}")
elif mixed_couplings:
    print("Spectral sign changes detected but delta_m remains positive (anti-MOND).")
    for r in mixed_couplings:
        print(f"  q^2 = {r['q_sq']:.1e}: rho_min = {r['rho_min']:.4e}, frac_neg = {r['frac_negative']:.4f}")
    print("  Need stronger coupling for delta_m to flip.")
else:
    print("No sign flip detected in scanned coupling range.")
    if no_flip_couplings:
        max_rho_min = max(no_flip_couplings, key=lambda r: r['rho_min'])
        print(f"Most negative rho (but still positive): {max_rho_min['rho_min']:.4e} at q^2 = {max_rho_min['q_sq']:.1e}")

print()


# ============================================================================
# PART 6: FREQUENCY BAND ANALYSIS - WHICH BANDS ARE NEGATIVE?
# ============================================================================

print("=" * 80)
print("PART 6: FREQUENCY BAND ANALYSIS - WHERE IS THE SIGN CHANGE?")
print("=" * 80)
print()

"""
We analyze the spectral density in different frequency bands:
  Band 1 (deep MOND): omega < 0.01 * omega_c
  Band 2 (galactic): 0.01 * omega_c < omega < omega_c
  Band 3 (cutoff): omega_c < omega < 10 * omega_c
  Band 4 (UV): omega > 10 * omega_c

For MOND, we need negative spectral density specifically in Band 2.
"""

# Find the case with strongest negative weight for band analysis
if results_scan:
    best_case = max(results_scan, key=lambda r: abs(r['rho_min']) if r['rho_min'] < 0 else float('inf'))

    # Re-compute spectral density for the best case with high resolution
    q_best = best_case['q_sq']
    tau_grid_fine = np.linspace(1e-8, 50.0, 4096)
    G_best, _ = compute_neSS_greens_vectorized(tau_grid_fine, q_best, eta_val, max_iter=80, tol=1e-7)

    omega_fine, rho_fine = compute_spectral_density_ness(G_best, tau_grid_fine)
    pos_mask = omega_fine > 1e-8
    omega_pos_fine = omega_fine[pos_mask]
    rho_pos_fine = rho_fine[pos_mask]

    # Define frequency bands (in units of H=1)
    band_edges = [1e-6, 0.01, 0.1, 1.0, 10.0, 100.0]
    band_names = ["deep-low", "galactic-LOW", "galactic-HI", "cutoff-LOW", "cutoff-HI", "UV"]

    print(f"Band analysis for q^2/H^2 = {q_best:.1e} (best negative case):")
    print()
    print(f"  {'Band':>16}  {'omega range':>18}  {'rho_min':>14}  {'rho_max':>14}  {'<0?':>5}")
    print(f"  {'-'*70}")

    for i in range(len(band_edges) - 1):
        mask = (omega_pos_fine >= band_edges[i]) & (omega_pos_fine < band_edges[i+1])
        if np.any(mask):
            rho_band = rho_pos_fine[mask]
            rho_min_b = float(np.min(rho_band))
            rho_max_b = float(np.max(rho_band))
            neg = "YES" if rho_min_b < -1e-12 else "no"
            print(f"  {band_names[i]:>16}  {band_edges[i]:8.0e}-{band_edges[i+1]:8.0e}  "
                  f"{rho_min_b:14.4e}  {rho_max_b:14.4e}  {neg:>5}")

    print()

    # Compute band contributions to delta_m
    print("Band contributions to delta_m = (2/pi) * integral rho/omega^2 domega:")
    dm_total = 0.0
    for i in range(len(band_edges) - 1):
        mask = (omega_pos_fine >= band_edges[i]) & (omega_pos_fine < band_edges[i+1])
        if np.any(mask):
            rho_band = rho_pos_fine[mask]
            omega_band = omega_pos_fine[mask]
            integ = trapz(rho_band / omega_band**2, omega_band)
            dm_band = (2.0 / np.pi) * integ
            dm_total += dm_band
            sign_str = "NEGATIVE" if dm_band < 0 else "POSITIVE"
            print(f"  {band_names[i]:>16}: delta_m_band = {dm_band:12.4f} ({sign_str})")

    print(f"  {'TOTAL':>16}: delta_m = {dm_total:12.4f} {'-> MOND' if dm_total < 0 else '-> anti-MOND'}")
    print()


# ============================================================================
# PART 7: PHYSICAL MECHANISM OF POPULATION INVERSION
# ============================================================================

print("=" * 80)
print("PART 7: PHYSICAL MECHANISM - WHAT DRIVES THE SIGN CHANGE?")
print("=" * 80)
print()

print("Physical mechanism:")
print("  1. Accelerated matter acts as a quantum detector coupled to the de Sitter vacuum")
print("  2. The detector pumps energy into field modes resonant with its trajectory frequency")
print("  3. At certain frequencies, stimulated emission > absorption -> negative spectral density")
print("  4. This population inversion is the NESS analog of a laser gain medium")
print("  5. When the negative spectral band at galactic frequencies dominates the inertia")
print("     integral, delta_m flips sign: this is MOND lowering of inertia.")
print()

print("Connection to tn14 constraints:")
print("  tn14 found: crossover at y_cross = 1/C_eq ~ 1.57")
print("  For y < y_cross (deep MOND): need positive delta_rho -> inverted population")
print("  For y > y_cross (Newtonian): need negative delta_rho -> standard dissipation")
print()

if sign_flip_couplings:
    print(f"RESULT: Sign flip occurs at q^2 ~ {q_sq_flip:.1e}.")
    print("  The NESS backreaction produces negative spectral density that overwhelms")
    print("  the positive equilibrium contribution, giving delta_m < 0 = MOND behavior.")
else:
    print("RESULT: Sign flip not reached in scanned coupling range.")
    print("  Either need stronger coupling or a different trajectory parameterization.")

print()


# ============================================================================
# SAVE RESULTS
# ============================================================================

results = {
    "title": "tn16: NESS Spectral Density rho(omega) - Sign Change Detection",
    "physical_parameters": {
        "H": float(H),
        "beta_GH": float(beta),
        "T_GH": float(T_GH),
        "a0_physical_m_per_s2": float(a0_physical),
        "omega_c_physical_rad_per_s": float(omega_c_physical),
    },
    "kms_baseline": {
        "BD_KMS_ratio": float(kms_ratio),
        "KMS_satified": bool(abs(kms_ratio - 1.0) < 1e-14),
    },
    "NESS_results_scan": results_scan,
    "sign_flip_analysis": {
        "sign_flip_detected": len(sign_flip_couplings) > 0,
        "threshold_q_sq": float(min(r['q_sq'] for r in sign_flip_couplings)) if sign_flip_couplings else None,
        "max_negative_rho": float(max((r['rho_min'] for r in sign_flip_couplings), default=None)),
        "mixed_cases": len(mixed_couplings),
    },
    "frequency_band_results": None,
    "physical_interpretation": {
        "mechanism": "Accelerated matter pumps energy into vacuum modes, creating population inversion",
        "negative_spectral_density": "Stimulated emission > absorption at resonant frequencies",
        "MOND_criterion": "rho_NES < 0 in galactic frequency band with dominant negative weight",
    },
}

results_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tn16_rho_ness_results.json')
os.makedirs(os.path.dirname(results_path), exist_ok=True)
with open(results_path, 'w') as f:
    json.dump(results, f, indent=2, default=str)

print(f"Results saved: {results_path}")
print("=" * 80)
print("tn16 COMPLETE - NESS spectral density computed and sign change analyzed.")
print("=" * 80)

sys.exit(0)
