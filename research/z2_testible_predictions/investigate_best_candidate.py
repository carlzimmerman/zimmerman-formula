#!/usr/bin/env python3
"""
Focused investigation of the best candidate matched circles.

We found r=18° has the highest correlation (0.6645).
This script investigates:
1. Exact location and whether it's near foregrounds
2. Temperature profile visualization
3. Statistical significance via bootstrap
4. Consistency across different CMB maps (if available)

Carl Zimmerman | May 2026
"""

import numpy as np
import healpy as hp
from scipy import stats
import matplotlib.pyplot as plt
import os

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
CMB_FILE = os.path.join(DATA_DIR, "COM_CMB_IQU-smica_2048_R3.00_full.fits")
MASK_FILE = os.path.join(DATA_DIR, "COM_Mask_CMB-common-Mask-Int_2048_R3.00.fits")


def load_data(nside=512):
    """Load and prepare data."""
    cmb = hp.read_map(CMB_FILE, field=0, verbose=False)
    mask = hp.read_map(MASK_FILE, field=0, verbose=False)

    if np.std(cmb) < 1e-3:
        cmb = cmb * 1e6

    native_nside = hp.get_nside(cmb)
    if nside < native_nside:
        cmb = hp.ud_grade(cmb, nside)
        mask = hp.ud_grade(mask, nside)
        mask = (mask > 0.5).astype(float)

    return cmb, mask, nside


def get_circle(cmb, mask, theta_c, phi_c, radius, nside, n_points=720):
    """Extract circle with high resolution."""
    psi = np.linspace(0, 2*np.pi, n_points, endpoint=False)

    cos_r, sin_r = np.cos(radius), np.sin(radius)
    cos_c, sin_c = np.cos(theta_c), np.sin(theta_c)

    theta_pts = np.arccos(cos_c * cos_r - sin_c * sin_r * np.cos(psi))
    phi_pts = phi_c + np.arctan2(sin_r * np.sin(psi),
                                  sin_c * cos_r + cos_c * sin_r * np.cos(psi))
    phi_pts = phi_pts % (2 * np.pi)

    pixels = hp.ang2pix(nside, theta_pts, phi_pts)
    T = cmb[pixels]
    M = mask[pixels]

    return T, psi, M, np.mean(M > 0.5)


def correlation_with_reversal(T1, T2):
    """Compute reversed correlation."""
    n = len(T1)
    T2_rev = T2[::-1]

    std1, std2 = np.std(T1), np.std(T2_rev)
    if std1 < 1e-10 or std2 < 1e-10:
        return 0.0, 0.0

    T1_norm = (T1 - np.mean(T1)) / std1
    T2_norm = (T2_rev - np.mean(T2_rev)) / std2

    cross = np.fft.ifft(np.fft.fft(T1_norm) * np.conj(np.fft.fft(T2_norm))).real / n
    max_idx = np.argmax(cross)

    return cross[max_idx], 2*np.pi*max_idx/n


def find_best_at_radius(cmb, mask, nside, radius_deg, n_centers=20000):
    """Find the best matching circles at a specific radius."""
    radius = np.radians(radius_deg)

    print(f"Searching {n_centers} centers at r={radius_deg}°...")

    np.random.seed(42)
    theta_centers = np.arccos(1 - 2*np.random.rand(n_centers))
    phi_centers = 2*np.pi*np.random.rand(n_centers)

    best_corr = 0
    best_candidate = None
    all_corrs = []

    for theta, phi in zip(theta_centers, phi_centers):
        theta_anti = np.pi - theta
        phi_anti = (phi + np.pi) % (2*np.pi)

        T1, psi1, M1, f1 = get_circle(cmb, mask, theta, phi, radius, nside)
        T2, psi2, M2, f2 = get_circle(cmb, mask, theta_anti, phi_anti, radius, nside)

        if f1 < 0.7 or f2 < 0.7:
            continue

        corr, phase = correlation_with_reversal(T1, T2)
        all_corrs.append(corr)

        if corr > best_corr:
            best_corr = corr
            best_candidate = {
                'theta1': theta, 'phi1': phi,
                'theta2': theta_anti, 'phi2': phi_anti,
                'radius': radius_deg,
                'correlation': corr,
                'phase': phase,
                'T1': T1, 'T2': T2, 'M1': M1, 'M2': M2, 'psi': psi1
            }

    print(f"  Best correlation: {best_corr:.4f}")
    print(f"  Center: ({np.degrees(best_candidate['theta1']):.2f}°, {np.degrees(best_candidate['phi1']):.2f}°)")

    return best_candidate, np.array(all_corrs)


def bootstrap_significance(cmb, mask, nside, candidate, n_bootstrap=1000):
    """Compute significance via bootstrap resampling."""
    print(f"\nBootstrap significance test ({n_bootstrap} iterations)...")

    radius = np.radians(candidate['radius'])
    observed_corr = candidate['correlation']

    bootstrap_corrs = []

    np.random.seed(999)
    for i in range(n_bootstrap):
        # Random non-antipodal pair
        theta1 = np.arccos(1 - 2*np.random.rand())
        phi1 = 2*np.pi*np.random.rand()
        theta2 = np.arccos(1 - 2*np.random.rand())
        phi2 = 2*np.pi*np.random.rand()

        # Ensure not antipodal
        sep = np.arccos(np.sin(theta1)*np.sin(theta2)*np.cos(phi1-phi2) +
                       np.cos(theta1)*np.cos(theta2))
        if np.abs(sep - np.pi) < 0.2:
            continue

        T1, _, M1, f1 = get_circle(cmb, mask, theta1, phi1, radius, nside)
        T2, _, M2, f2 = get_circle(cmb, mask, theta2, phi2, radius, nside)

        if f1 < 0.7 or f2 < 0.7:
            continue

        corr, _ = correlation_with_reversal(T1, T2)
        bootstrap_corrs.append(corr)

        if (i+1) % 200 == 0:
            print(f"    {i+1}/{n_bootstrap} done...")

    bootstrap_corrs = np.array(bootstrap_corrs)

    mean_null = np.mean(bootstrap_corrs)
    std_null = np.std(bootstrap_corrs)
    z_score = (observed_corr - mean_null) / std_null

    # Empirical p-value
    p_value = np.mean(bootstrap_corrs >= observed_corr)

    print(f"\n  Null distribution: {mean_null:.4f} ± {std_null:.4f}")
    print(f"  Observed: {observed_corr:.4f}")
    print(f"  Z-score: {z_score:.2f}σ")
    print(f"  Empirical p-value: {p_value:.4f}")

    return z_score, p_value, bootstrap_corrs


def check_foreground_contamination(candidate, nside):
    """Check if candidate is near known foreground regions."""
    theta1 = candidate['theta1']
    phi1 = candidate['phi1']

    # Convert to galactic coordinates
    # Rough approximation - proper conversion would use healpy.Rotator
    gal_lat = 90 - np.degrees(theta1)  # Colatitude to latitude approx
    gal_lon = np.degrees(phi1)

    print(f"\nForeground contamination check:")
    print(f"  Approximate position: (gal_lat={gal_lat:.1f}°, gal_lon={gal_lon:.1f}°)")

    # Check distance from galactic plane
    if abs(gal_lat) < 20:
        print(f"  ⚠️  WARNING: Close to galactic plane!")
    else:
        print(f"  ✓ Away from galactic plane")

    # Known foreground regions (rough)
    foreground_regions = [
        ("Galactic Center", 0, 0, 20),
        ("Magellanic Clouds", -33, 280, 15),
        ("North Polar Spur", 60, 30, 30),
    ]

    for name, lat, lon, radius in foreground_regions:
        sep = np.sqrt((gal_lat - lat)**2 + ((gal_lon - lon + 180) % 360 - 180)**2)
        if sep < radius:
            print(f"  ⚠️  WARNING: Near {name}!")
        else:
            print(f"  ✓ Away from {name}")


def visualize_best_candidate(candidate, output_dir):
    """Create detailed visualization of the best candidate."""
    fig = plt.figure(figsize=(16, 12))

    # Panel 1: Temperature profiles
    ax1 = fig.add_subplot(2, 2, 1)
    psi_deg = np.degrees(candidate['psi'])
    T1 = np.where(candidate['M1'] > 0.5, candidate['T1'], np.nan)
    T2 = np.where(candidate['M2'] > 0.5, candidate['T2'], np.nan)
    T2_rev = T2[::-1]

    # Apply phase shift
    phase_idx = int(candidate['phase'] * len(candidate['T1']) / (2*np.pi))
    T2_shifted = np.roll(T2_rev, phase_idx)

    ax1.plot(psi_deg, T1, 'b-', linewidth=1, alpha=0.8, label='Circle 1')
    ax1.plot(psi_deg, T2_shifted, 'r--', linewidth=1, alpha=0.8, label='Circle 2 (reversed+shifted)')
    ax1.set_xlabel('Angle around circle (°)', fontsize=12)
    ax1.set_ylabel('Temperature (μK)', fontsize=12)
    ax1.set_title(f'Temperature Profiles (r={candidate["radius"]}°, corr={candidate["correlation"]:.4f})', fontsize=14)
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Panel 2: Difference
    ax2 = fig.add_subplot(2, 2, 2)
    diff = T1 - T2_shifted
    ax2.plot(psi_deg, diff, 'g-', linewidth=1)
    ax2.axhline(0, color='k', linestyle='--', alpha=0.5)
    ax2.fill_between(psi_deg, diff, 0, alpha=0.3, color='green')
    ax2.set_xlabel('Angle around circle (°)', fontsize=12)
    ax2.set_ylabel('Temperature difference (μK)', fontsize=12)
    ax2.set_title('Residual (Circle 1 - Circle 2 shifted)', fontsize=14)
    ax2.grid(True, alpha=0.3)

    # Panel 3: Cross-correlation
    ax3 = fig.add_subplot(2, 2, 3)
    T1_clean = np.nan_to_num(T1 - np.nanmean(T1))
    T2_clean = np.nan_to_num(T2[::-1] - np.nanmean(T2))
    std1, std2 = np.nanstd(T1), np.nanstd(T2)
    if std1 > 0 and std2 > 0:
        T1_norm = T1_clean / std1
        T2_norm = T2_clean / std2
        xcorr = np.fft.ifft(np.fft.fft(T1_norm) * np.conj(np.fft.fft(T2_norm))).real / len(T1_norm)
        phases = np.linspace(0, 360, len(xcorr))
        ax3.plot(phases, xcorr, 'purple', linewidth=1.5)
        ax3.axvline(np.degrees(candidate['phase']), color='r', linestyle='--',
                   label=f'Best phase: {np.degrees(candidate["phase"]):.1f}°')
        ax3.axhline(candidate['correlation'], color='orange', linestyle=':',
                   label=f'Max corr: {candidate["correlation"]:.4f}')
    ax3.set_xlabel('Phase offset (°)', fontsize=12)
    ax3.set_ylabel('Correlation', fontsize=12)
    ax3.set_title('Cross-correlation function', fontsize=14)
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # Panel 4: Power spectra
    ax4 = fig.add_subplot(2, 2, 4)
    freqs = np.fft.fftfreq(len(T1_clean), d=360/len(T1_clean))
    ps1 = np.abs(np.fft.fft(T1_clean))**2
    ps2 = np.abs(np.fft.fft(T2_clean))**2
    ax4.semilogy(freqs[:len(freqs)//2], ps1[:len(freqs)//2], 'b-', alpha=0.7, label='Circle 1')
    ax4.semilogy(freqs[:len(freqs)//2], ps2[:len(freqs)//2], 'r-', alpha=0.7, label='Circle 2')
    ax4.set_xlabel('Frequency (cycles/360°)', fontsize=12)
    ax4.set_ylabel('Power', fontsize=12)
    ax4.set_title('Power spectra', fontsize=14)
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    outfile = os.path.join(output_dir, 'best_candidate_detailed.png')
    plt.savefig(outfile, dpi=150, bbox_inches='tight')
    print(f"\nSaved: {outfile}")
    plt.close()


def search_multiple_radii_intensively(cmb, mask, nside, n_centers=30000):
    """Intensive search at multiple radii to find THE best candidate."""
    print("\n" + "="*70)
    print("INTENSIVE MULTI-RADIUS SEARCH")
    print("="*70)

    # Focus on radii that showed promise
    radii = [16, 17, 18, 19, 20, 25, 29, 35, 38, 45, 47, 50, 51]

    best_overall = None
    best_corr_overall = 0

    for r in radii:
        candidate, corrs = find_best_at_radius(cmb, mask, nside, r, n_centers=n_centers)
        if candidate['correlation'] > best_corr_overall:
            best_corr_overall = candidate['correlation']
            best_overall = candidate

    print(f"\n*** BEST OVERALL CANDIDATE ***")
    print(f"  Radius: {best_overall['radius']}°")
    print(f"  Correlation: {best_overall['correlation']:.4f}")
    print(f"  Center: ({np.degrees(best_overall['theta1']):.2f}°, {np.degrees(best_overall['phi1']):.2f}°)")

    return best_overall


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("INVESTIGATION OF BEST MATCHED CIRCLE CANDIDATES")
    print("="*70)

    # Load data at higher resolution
    cmb, mask, nside = load_data(nside=512)
    print(f"Loaded data at NSIDE={nside}")

    # Intensive search
    best = search_multiple_radii_intensively(cmb, mask, nside, n_centers=15000)

    # Check foreground contamination
    check_foreground_contamination(best, nside)

    # Bootstrap significance
    z_score, p_value, null_dist = bootstrap_significance(cmb, mask, nside, best, n_bootstrap=500)

    # Detailed visualization
    visualize_best_candidate(best, DATA_DIR)

    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"""
Best matched circle candidate:
  Radius: {best['radius']}°
  Correlation: {best['correlation']:.4f}
  Center: ({np.degrees(best['theta1']):.2f}°, {np.degrees(best['phi1']):.2f}°)
  Z-score: {z_score:.2f}σ
  P-value: {p_value:.4f}

Physical interpretation:
  If r={best['radius']}°, then fundamental domain L ≈ {best['radius']/90 * 14:.1f} Gpc
  (Using L ≈ 2 * d_LSS * sin(r/2) where d_LSS ≈ 14 Gpc)
""")

    print("="*70)
