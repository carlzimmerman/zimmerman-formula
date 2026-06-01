#!/usr/bin/env python3
"""
Corrected SPARC Verification with REAL Data

This script uses the ACTUAL binned SPARC data from Lelli+ 2017
downloaded from https://astroweb.cwru.edu/SPARC/RARbins.mrt

Author: Carl Zimmerman
Date: May 2, 2026
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar

# =============================================================================
# REAL SPARC DATA from Lelli+ 2017 (Figure 2)
# Downloaded from https://astroweb.cwru.edu/SPARC/RARbins.mrt
# =============================================================================

REAL_SPARC_DATA = {
    'log_g_bar': np.array([-11.69, -11.48, -11.26, -11.05, -10.84, -10.62,
                           -10.41, -10.19, -9.98, -9.76, -9.55, -9.34, -9.12, -8.91]),
    'log_g_obs': np.array([-10.75, -10.70, -10.57, -10.43, -10.31, -10.17,
                           -10.03, -9.90, -9.76, -9.60, -9.44, -9.29, -9.11, -8.90]),
    'sd': np.array([0.18, 0.16, 0.15, 0.14, 0.13, 0.12, 0.14, 0.13,
                    0.14, 0.14, 0.14, 0.11, 0.13, 0.11]),
    'N': np.array([75, 191, 308, 323, 283, 229, 242, 229, 204, 177, 137, 104, 85, 43])
}

# Observed MOND scale
a0_observed = 1.2e-10  # m/s²

# =============================================================================
# MOND Interpolating Functions
# =============================================================================

def mu_Z2(x):
    """Z² / Simple MOND: μ(x) = x/(1+x)"""
    return x / (1 + x)

def mu_standard(x):
    """Standard MOND: μ(x) = x/√(1+x²)"""
    return x / np.sqrt(1 + x**2)

def mu_RAR(x):
    """RAR empirical: μ(x) = 1 - exp(-√x)"""
    return 1 - np.exp(-np.sqrt(np.maximum(x, 1e-10)))

# =============================================================================
# MOND Prediction
# =============================================================================

def mond_g_obs(g_bar, a0, mu_func):
    """
    Solve MOND equation: g_obs × μ(g_obs/a0) = g_bar

    Returns g_obs given g_bar
    """
    # For each g_bar, find g_obs such that g_obs * mu(g_obs/a0) = g_bar
    # This requires iteration

    g_obs = g_bar.copy()  # Initial guess

    for _ in range(100):
        x = g_obs / a0
        mu_val = mu_func(x)
        # From: g_obs * mu(g_obs/a0) = g_bar
        # We get: g_obs = g_bar / mu(g_bar/a0) approximately
        # But actually need: g_obs such that g_obs * mu(g_obs/a0) = g_bar
        # Newton iteration: g_obs_new = g_bar / mu(g_obs/a0)
        g_obs_new = g_bar / mu_val

        if np.max(np.abs(g_obs_new - g_obs) / g_obs) < 1e-8:
            break
        g_obs = g_obs_new

    return g_obs

# =============================================================================
# Chi-squared Calculation
# =============================================================================

def compute_chi2(mu_func, a0):
    """Compute chi-squared for a given interpolating function."""

    g_bar = 10**REAL_SPARC_DATA['log_g_bar']
    g_obs_measured = 10**REAL_SPARC_DATA['log_g_obs']

    # Error in log space converts to relative error
    # sigma_log = sd, so sigma_g / g = sd * ln(10)
    g_obs_err = REAL_SPARC_DATA['sd'] * g_obs_measured * np.log(10)

    # MOND prediction
    g_obs_pred = mond_g_obs(g_bar, a0, mu_func)

    # Chi-squared
    chi2 = np.sum(((g_obs_measured - g_obs_pred) / g_obs_err)**2)

    return chi2

def fit_a0(mu_func):
    """Find best-fit a0 for a given interpolating function."""

    def neg_likelihood(log_a0):
        a0 = 10**log_a0
        return compute_chi2(mu_func, a0)

    result = minimize_scalar(neg_likelihood, bounds=(-11, -9), method='bounded')

    best_a0 = 10**result.x
    best_chi2 = result.fun

    return best_a0, best_chi2

# =============================================================================
# Main Analysis
# =============================================================================

def main():
    print("=" * 70)
    print("CORRECTED SPARC VERIFICATION WITH REAL DATA")
    print("=" * 70)
    print("\nData source: Lelli+ 2017 (SPARC RARbins.mrt)")
    print(f"URL: https://astroweb.cwru.edu/SPARC/")
    print(f"Number of bins: {len(REAL_SPARC_DATA['log_g_bar'])}")
    print(f"Total data points: {np.sum(REAL_SPARC_DATA['N'])}")

    mu_funcs = {
        'Z² / Simple [x/(1+x)]': mu_Z2,
        'Standard [x/√(1+x²)]': mu_standard,
        'RAR [1-exp(-√x)]': mu_RAR,
    }

    print("\n" + "=" * 70)
    print("TEST 1: Fixed a₀ = 1.2 × 10⁻¹⁰ m/s²")
    print("=" * 70)

    dof = len(REAL_SPARC_DATA['log_g_bar']) - 1  # 13 degrees of freedom

    results_fixed = {}
    for name, mu_func in mu_funcs.items():
        chi2 = compute_chi2(mu_func, a0_observed)
        chi2_red = chi2 / dof
        results_fixed[name] = {'chi2': chi2, 'chi2_red': chi2_red}
        print(f"\n{name}:")
        print(f"  χ² = {chi2:.2f}")
        print(f"  χ²/dof = {chi2_red:.3f}")

    best_fixed = min(results_fixed.keys(), key=lambda k: results_fixed[k]['chi2_red'])
    print(f"\n>>> Best fit (fixed a₀): {best_fixed}")

    print("\n" + "=" * 70)
    print("TEST 2: Free a₀ (best fit)")
    print("=" * 70)

    results_free = {}
    for name, mu_func in mu_funcs.items():
        best_a0, best_chi2 = fit_a0(mu_func)
        chi2_red = best_chi2 / dof
        results_free[name] = {'a0': best_a0, 'chi2': best_chi2, 'chi2_red': chi2_red}
        print(f"\n{name}:")
        print(f"  Best a₀ = {best_a0:.3e} m/s²")
        print(f"  χ² = {best_chi2:.2f}")
        print(f"  χ²/dof = {chi2_red:.3f}")

    best_free = min(results_free.keys(), key=lambda k: results_free[k]['chi2_red'])
    print(f"\n>>> Best fit (free a₀): {best_free}")

    print("\n" + "=" * 70)
    print("COMPARISON SUMMARY")
    print("=" * 70)

    print(f"\n{'Function':<30} {'χ²/dof (fixed)':<15} {'χ²/dof (free)':<15} {'Best a₀':<15}")
    print("-" * 75)
    for name in mu_funcs:
        fixed = results_fixed[name]['chi2_red']
        free = results_free[name]['chi2_red']
        a0 = results_free[name]['a0']
        print(f"{name:<30} {fixed:<15.3f} {free:<15.3f} {a0:.2e}")

    print("\n" + "=" * 70)
    print("HONEST ASSESSMENT")
    print("=" * 70)

    z2_fixed = results_fixed['Z² / Simple [x/(1+x)]']['chi2_red']
    std_fixed = results_fixed['Standard [x/√(1+x²)]']['chi2_red']
    rar_fixed = results_fixed['RAR [1-exp(-√x)]']['chi2_red']

    print(f"""
With fixed a₀ = 1.2 × 10⁻¹⁰ m/s²:
  - Z² / Simple:  χ²/dof = {z2_fixed:.3f}
  - Standard:     χ²/dof = {std_fixed:.3f}
  - RAR:          χ²/dof = {rar_fixed:.3f}

Interpretation:
  - χ²/dof ≈ 1 means good fit
  - χ²/dof > 1 means poor fit or underestimated errors
  - χ²/dof < 1 means overestimated errors or overfitting
""")

    if z2_fixed < std_fixed and z2_fixed < rar_fixed:
        print("  >>> Z² / Simple provides the BEST fit")
    elif std_fixed < z2_fixed and std_fixed < rar_fixed:
        print("  >>> Standard provides the BEST fit")
    else:
        print("  >>> RAR provides the BEST fit")

    # Plot
    plot_results(results_fixed, results_free)

    return results_fixed, results_free

def plot_results(results_fixed, results_free):
    """Create visualization of the fits."""

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Data
    g_bar = 10**REAL_SPARC_DATA['log_g_bar']
    g_obs = 10**REAL_SPARC_DATA['log_g_obs']
    g_obs_err = REAL_SPARC_DATA['sd'] * g_obs * np.log(10)

    # Plot 1: RAR with different fits
    ax = axes[0]

    ax.errorbar(g_bar, g_obs, yerr=g_obs_err, fmt='ko', markersize=6,
                capsize=3, label='SPARC data (Lelli+ 2017)', zorder=5)

    # 1:1 line (Newtonian)
    g_range = np.logspace(-12, -8, 100)
    ax.loglog(g_range, g_range, 'gray', linestyle='--', alpha=0.5,
              label='g_obs = g_bar (Newtonian)')

    # Predictions
    colors = {'Z² / Simple [x/(1+x)]': 'blue',
              'Standard [x/√(1+x²)]': 'red',
              'RAR [1-exp(-√x)]': 'green'}

    mu_funcs = {
        'Z² / Simple [x/(1+x)]': mu_Z2,
        'Standard [x/√(1+x²)]': mu_standard,
        'RAR [1-exp(-√x)]': mu_RAR,
    }

    for name, mu_func in mu_funcs.items():
        g_pred = mond_g_obs(g_range, a0_observed, mu_func)
        chi2_red = results_fixed[name]['chi2_red']
        ax.loglog(g_range, g_pred, colors[name], linewidth=2,
                  label=f'{name} (χ²/dof={chi2_red:.2f})')

    ax.set_xlabel('g_bar (m/s²)', fontsize=12)
    ax.set_ylabel('g_obs (m/s²)', fontsize=12)
    ax.set_title('Radial Acceleration Relation - REAL SPARC Data', fontsize=14)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_xlim([1e-12, 3e-9])
    ax.set_ylim([1e-11, 3e-9])

    # Plot 2: Residuals
    ax = axes[1]

    for name, mu_func in mu_funcs.items():
        g_pred = mond_g_obs(g_bar, a0_observed, mu_func)
        residual = (g_obs - g_pred) / g_obs * 100  # percent
        ax.semilogx(g_bar, residual, 'o-', color=colors[name],
                    markersize=6, linewidth=1.5, label=name)

    ax.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    ax.axhspan(-10, 10, alpha=0.1, color='gray')

    ax.set_xlabel('g_bar (m/s²)', fontsize=12)
    ax.set_ylabel('Residual (%)', fontsize=12)
    ax.set_title('Fit Residuals', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim([-50, 50])

    plt.tight_layout()
    plt.savefig('corrected_sparc_verification.png', dpi=150, bbox_inches='tight')
    print("\nPlot saved to corrected_sparc_verification.png")
    plt.show()

if __name__ == "__main__":
    results_fixed, results_free = main()
