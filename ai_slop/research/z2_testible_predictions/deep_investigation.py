#!/usr/bin/env python3
"""
Deep Investigation of CMB Matched Circles Candidates

This script performs a thorough investigation of the elevated correlations
found in the Planck data, examining:
1. Best candidate circle pairs in detail
2. Temperature profile visualization
3. Spatial distribution of candidates
4. Systematic effects investigation
5. Finer radius search
6. Higher resolution analysis

Carl Zimmerman | May 2026
"""

import numpy as np
import healpy as hp
from scipy import stats
import matplotlib.pyplot as plt
from typing import Tuple, List
import os

# Configuration
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
CMB_FILE = os.path.join(DATA_DIR, "COM_CMB_IQU-smica_2048_R3.00_full.fits")
MASK_FILE = os.path.join(DATA_DIR, "COM_Mask_CMB-common-Mask-Int_2048_R3.00.fits")

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def load_planck_data(target_nside=512):
    """Load Planck CMB map and mask."""
    print(f"Loading Planck data at NSIDE={target_nside}...")

    cmb = hp.read_map(CMB_FILE, field=0, verbose=False)
    mask = hp.read_map(MASK_FILE, field=0, verbose=False)

    # Convert to μK if needed
    if np.std(cmb) < 1e-3:
        cmb = cmb * 1e6

    # Downsample
    native_nside = hp.get_nside(cmb)
    if target_nside < native_nside:
        cmb = hp.ud_grade(cmb, target_nside)
        mask = hp.ud_grade(mask, target_nside)
        mask = (mask > 0.5).astype(float)

    print(f"  Loaded: {len(cmb)} pixels, {np.mean(mask)*100:.1f}% unmasked")
    return cmb, mask


def get_circle_pixels(theta_c, phi_c, radius, nside, n_points=360):
    """Get pixel indices and angles for a circle."""
    psi = np.linspace(0, 2*np.pi, n_points, endpoint=False)

    cos_r = np.cos(radius)
    sin_r = np.sin(radius)
    cos_c = np.cos(theta_c)
    sin_c = np.sin(theta_c)

    theta_pts = np.arccos(cos_c * cos_r - sin_c * sin_r * np.cos(psi))
    phi_pts = phi_c + np.arctan2(sin_r * np.sin(psi),
                                  sin_c * cos_r + cos_c * sin_r * np.cos(psi))
    phi_pts = phi_pts % (2 * np.pi)

    pixels = hp.ang2pix(nside, theta_pts, phi_pts)
    return pixels, psi


def extract_circle(cmb, mask, theta_c, phi_c, radius, nside, n_points=360):
    """Extract temperature profile along a circle."""
    pixels, psi = get_circle_pixels(theta_c, phi_c, radius, nside, n_points)
    T = cmb[pixels]
    M = mask[pixels] if mask is not None else np.ones(n_points)
    good_frac = np.mean(M > 0.5)
    return T, psi, M, good_frac


def correlation_with_reversal(T1, T2, M1=None, M2=None):
    """Compute T³/Z₂ correlation with reversal."""
    n = len(T1)
    T2_rev = T2[::-1]

    # Handle masks
    if M1 is not None and M2 is not None:
        M2_rev = M2[::-1]
        valid = (M1 > 0.5) & (M2_rev > 0.5)
        if np.sum(valid) < n * 0.5:
            return 0.0, 0.0, 0
    else:
        valid = np.ones(n, dtype=bool)

    # Interpolate over gaps
    T1_clean = np.interp(np.arange(n), np.where(valid)[0], T1[valid]) if not np.all(valid) else T1
    T2_rev_clean = np.interp(np.arange(n), np.where(valid)[0], T2_rev[valid]) if not np.all(valid) else T2_rev

    # FFT cross-correlation
    std1, std2 = np.std(T1_clean), np.std(T2_rev_clean)
    if std1 < 1e-10 or std2 < 1e-10:
        return 0.0, 0.0, 0

    T1_norm = (T1_clean - np.mean(T1_clean)) / std1
    T2_norm = (T2_rev_clean - np.mean(T2_rev_clean)) / std2

    cross = np.fft.ifft(np.fft.fft(T1_norm) * np.conj(np.fft.fft(T2_norm))).real / n
    max_idx = np.argmax(cross)

    return cross[max_idx], 2*np.pi*max_idx/n, np.sum(valid)


def antipodal(theta, phi):
    """Get antipodal point."""
    return np.pi - theta, (phi + np.pi) % (2*np.pi)


# =============================================================================
# INVESTIGATION 1: EXAMINE BEST CANDIDATES
# =============================================================================

def investigate_best_candidates(cmb, mask, nside, n_centers=10000, top_n=20):
    """Find and examine the best candidate matches."""
    print("\n" + "="*70)
    print("INVESTIGATION 1: EXAMINING BEST CANDIDATES")
    print("="*70)

    # Search across radii
    all_candidates = []
    radii = [15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75]

    np.random.seed(42)
    theta_centers = np.arccos(1 - 2*np.random.rand(n_centers))
    phi_centers = 2*np.pi*np.random.rand(n_centers)

    for radius_deg in radii:
        radius = np.radians(radius_deg)
        print(f"  Scanning radius {radius_deg}°...", end=" ", flush=True)

        for i, (theta, phi) in enumerate(zip(theta_centers, phi_centers)):
            theta_anti, phi_anti = antipodal(theta, phi)

            T1, psi1, M1, f1 = extract_circle(cmb, mask, theta, phi, radius, nside)
            T2, psi2, M2, f2 = extract_circle(cmb, mask, theta_anti, phi_anti, radius, nside)

            if f1 < 0.7 or f2 < 0.7:
                continue

            corr, phase, n_valid = correlation_with_reversal(T1, T2, M1, M2)

            all_candidates.append({
                'radius_deg': radius_deg,
                'theta1': theta, 'phi1': phi,
                'theta2': theta_anti, 'phi2': phi_anti,
                'correlation': corr,
                'phase': phase,
                'good_frac': min(f1, f2),
                'n_valid': n_valid,
                'T1': T1, 'T2': T2, 'M1': M1, 'M2': M2
            })

        print(f"done")

    # Sort by correlation
    all_candidates.sort(key=lambda x: x['correlation'], reverse=True)

    print(f"\n  Total candidates evaluated: {len(all_candidates)}")
    print(f"\n  TOP {top_n} CANDIDATES:")
    print("-"*70)

    for i, c in enumerate(all_candidates[:top_n]):
        print(f"  {i+1:2d}. r={c['radius_deg']:2d}°  corr={c['correlation']:.4f}  "
              f"center=({np.degrees(c['theta1']):6.1f}°, {np.degrees(c['phi1']):6.1f}°)  "
              f"good={c['good_frac']*100:.0f}%")

    return all_candidates[:top_n]


# =============================================================================
# INVESTIGATION 2: VISUALIZE TOP CANDIDATES
# =============================================================================

def visualize_candidates(candidates, output_dir):
    """Create visualizations of top candidates."""
    print("\n" + "="*70)
    print("INVESTIGATION 2: VISUALIZING TOP CANDIDATES")
    print("="*70)

    n_show = min(6, len(candidates))
    fig, axes = plt.subplots(n_show, 2, figsize=(14, 3*n_show))

    for i, c in enumerate(candidates[:n_show]):
        # Left: Temperature profiles
        ax1 = axes[i, 0]
        psi = np.linspace(0, 360, len(c['T1']))

        # Apply mask
        T1_plot = np.where(c['M1'] > 0.5, c['T1'], np.nan)
        T2_plot = np.where(c['M2'] > 0.5, c['T2'], np.nan)
        T2_rev = T2_plot[::-1]

        # Apply phase shift
        phase_idx = int(c['phase'] * len(c['T1']) / (2*np.pi))
        T2_shifted = np.roll(T2_rev, phase_idx)

        ax1.plot(psi, T1_plot, 'b-', alpha=0.7, label='Circle 1')
        ax1.plot(psi, T2_shifted, 'r--', alpha=0.7, label='Circle 2 (reversed + shifted)')
        ax1.set_xlabel('Angle around circle (°)')
        ax1.set_ylabel('Temperature (μK)')
        ax1.set_title(f'Candidate {i+1}: r={c["radius_deg"]}°, corr={c["correlation"]:.3f}')
        ax1.legend(fontsize=8)
        ax1.grid(True, alpha=0.3)

        # Right: Cross-correlation function
        ax2 = axes[i, 1]
        T1_clean = np.nan_to_num(T1_plot - np.nanmean(T1_plot))
        T2_clean = np.nan_to_num(T2_plot[::-1] - np.nanmean(T2_plot))
        std1, std2 = np.nanstd(T1_plot), np.nanstd(T2_plot)
        if std1 > 0 and std2 > 0:
            T1_norm = T1_clean / std1
            T2_norm = T2_clean / std2
            xcorr = np.fft.ifft(np.fft.fft(T1_norm) * np.conj(np.fft.fft(T2_norm))).real / len(T1_norm)
            phases = np.linspace(0, 360, len(xcorr))
            ax2.plot(phases, xcorr, 'g-', linewidth=1.5)
            ax2.axvline(np.degrees(c['phase']), color='r', linestyle='--', label=f'Best phase: {np.degrees(c["phase"]):.1f}°')
            ax2.axhline(c['correlation'], color='orange', linestyle=':', label=f'Max corr: {c["correlation"]:.3f}')
        ax2.set_xlabel('Phase offset (°)')
        ax2.set_ylabel('Correlation')
        ax2.set_title('Cross-correlation function')
        ax2.legend(fontsize=8)
        ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    outfile = os.path.join(output_dir, 'candidate_profiles.png')
    plt.savefig(outfile, dpi=150, bbox_inches='tight')
    print(f"  Saved: {outfile}")
    plt.close()


# =============================================================================
# INVESTIGATION 3: SPATIAL DISTRIBUTION
# =============================================================================

def analyze_spatial_distribution(candidates, output_dir):
    """Analyze where high-correlation candidates are located."""
    print("\n" + "="*70)
    print("INVESTIGATION 3: SPATIAL DISTRIBUTION OF CANDIDATES")
    print("="*70)

    # Extract positions
    thetas = [c['theta1'] for c in candidates]
    phis = [c['phi1'] for c in candidates]
    corrs = [c['correlation'] for c in candidates]
    radii = [c['radius_deg'] for c in candidates]

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Panel 1: Sky map of candidates
    ax1 = axes[0]
    theta_deg = np.degrees(thetas)
    phi_deg = np.degrees(phis)
    sc = ax1.scatter(phi_deg, theta_deg, c=corrs, cmap='hot', s=50, alpha=0.7)
    plt.colorbar(sc, ax=ax1, label='Correlation')
    ax1.set_xlabel('Longitude (°)')
    ax1.set_ylabel('Colatitude (°)')
    ax1.set_title('Sky Location of Top Candidates')
    ax1.set_xlim(0, 360)
    ax1.set_ylim(180, 0)

    # Panel 2: Correlation vs galactic latitude
    ax2 = axes[1]
    gal_lat = 90 - np.array(theta_deg)  # Approximate
    ax2.scatter(gal_lat, corrs, c=radii, cmap='viridis', s=50, alpha=0.7)
    ax2.set_xlabel('Approximate Galactic Latitude (°)')
    ax2.set_ylabel('Correlation')
    ax2.set_title('Correlation vs Position\n(colored by radius)')
    ax2.grid(True, alpha=0.3)

    # Panel 3: Histogram of correlations by radius
    ax3 = axes[2]
    for r in sorted(set(radii)):
        r_corrs = [c['correlation'] for c in candidates if c['radius_deg'] == r]
        if r_corrs:
            ax3.hist(r_corrs, bins=20, alpha=0.5, label=f'{r}°')
    ax3.set_xlabel('Correlation')
    ax3.set_ylabel('Count')
    ax3.set_title('Correlation Distribution by Radius')
    ax3.legend(fontsize=8)

    plt.tight_layout()
    outfile = os.path.join(output_dir, 'spatial_distribution.png')
    plt.savefig(outfile, dpi=150, bbox_inches='tight')
    print(f"  Saved: {outfile}")
    plt.close()

    # Check for clustering
    print("\n  Checking for spatial clustering...")
    mean_theta = np.mean(thetas)
    mean_phi = np.mean(phis)
    print(f"  Mean position: ({np.degrees(mean_theta):.1f}°, {np.degrees(mean_phi):.1f}°)")

    # Angular separation between candidates
    separations = []
    for i in range(len(candidates)):
        for j in range(i+1, min(i+5, len(candidates))):
            t1, p1 = thetas[i], phis[i]
            t2, p2 = thetas[j], phis[j]
            sep = np.arccos(np.sin(t1)*np.sin(t2)*np.cos(p1-p2) + np.cos(t1)*np.cos(t2))
            separations.append(np.degrees(sep))

    print(f"  Angular separations between top candidates: {np.mean(separations):.1f}° ± {np.std(separations):.1f}°")


# =============================================================================
# INVESTIGATION 4: FINE RADIUS SEARCH
# =============================================================================

def fine_radius_search(cmb, mask, nside, n_centers=5000):
    """Search with finer radius steps around promising regions."""
    print("\n" + "="*70)
    print("INVESTIGATION 4: FINE RADIUS SEARCH (1° steps)")
    print("="*70)

    # Finer radius grid
    radii_fine = np.arange(10, 80, 1)  # 1° steps
    max_corrs = []

    np.random.seed(12345)
    theta_centers = np.arccos(1 - 2*np.random.rand(n_centers))
    phi_centers = 2*np.pi*np.random.rand(n_centers)

    for radius_deg in radii_fine:
        radius = np.radians(radius_deg)
        best_corr = 0

        for theta, phi in zip(theta_centers, phi_centers):
            theta_anti, phi_anti = antipodal(theta, phi)

            T1, _, M1, f1 = extract_circle(cmb, mask, theta, phi, radius, nside)
            T2, _, M2, f2 = extract_circle(cmb, mask, theta_anti, phi_anti, radius, nside)

            if f1 < 0.7 or f2 < 0.7:
                continue

            corr, _, _ = correlation_with_reversal(T1, T2, M1, M2)
            best_corr = max(best_corr, corr)

        max_corrs.append(best_corr)
        print(f"  r={radius_deg:2d}°: max_corr={best_corr:.4f}")

    # Plot
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(radii_fine, max_corrs, 'b.-', markersize=4)
    ax.axhline(0.5, color='r', linestyle='--', label='Threshold')
    ax.axhline(np.mean(max_corrs), color='g', linestyle=':', label=f'Mean: {np.mean(max_corrs):.3f}')

    # Mark peaks
    peaks = np.where(np.array(max_corrs) > 0.45)[0]
    if len(peaks) > 0:
        ax.scatter(radii_fine[peaks], np.array(max_corrs)[peaks], color='red', s=100, zorder=5)

    ax.set_xlabel('Circle Radius (°)', fontsize=12)
    ax.set_ylabel('Max Correlation', fontsize=12)
    ax.set_title('Fine Radius Search (1° steps)', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)

    outfile = os.path.join(DATA_DIR, 'fine_radius_search.png')
    plt.savefig(outfile, dpi=150, bbox_inches='tight')
    print(f"\n  Saved: {outfile}")
    plt.close()

    # Identify peaks
    peak_radii = radii_fine[np.array(max_corrs) > 0.45]
    print(f"\n  Radii with correlation > 0.45: {list(peak_radii)}")

    return radii_fine, max_corrs


# =============================================================================
# INVESTIGATION 5: COMPARE WITH GAUSSIAN SIMULATIONS
# =============================================================================

def compare_with_simulations(cmb, mask, nside, n_sims=10, n_centers=2000):
    """Compare Planck correlations with Gaussian simulations."""
    print("\n" + "="*70)
    print("INVESTIGATION 5: COMPARISON WITH GAUSSIAN SIMULATIONS")
    print("="*70)

    radii = [15, 30, 45, 60, 75]

    # Planck correlations
    print("  Computing Planck correlations...")
    planck_corrs = {r: [] for r in radii}

    np.random.seed(99)
    theta_centers = np.arccos(1 - 2*np.random.rand(n_centers))
    phi_centers = 2*np.pi*np.random.rand(n_centers)

    for radius_deg in radii:
        radius = np.radians(radius_deg)
        for theta, phi in zip(theta_centers, phi_centers):
            theta_anti, phi_anti = antipodal(theta, phi)
            T1, _, M1, f1 = extract_circle(cmb, mask, theta, phi, radius, nside)
            T2, _, M2, f2 = extract_circle(cmb, mask, theta_anti, phi_anti, radius, nside)
            if f1 >= 0.7 and f2 >= 0.7:
                corr, _, _ = correlation_with_reversal(T1, T2, M1, M2)
                planck_corrs[radius_deg].append(corr)

    # Simulated correlations
    print(f"  Running {n_sims} Gaussian simulations...")
    sim_corrs = {r: [] for r in radii}

    for sim_idx in range(n_sims):
        # Generate Gaussian CMB
        lmax = 3 * nside - 1
        ell = np.arange(lmax + 1)
        Cl = np.zeros(lmax + 1)
        Cl[2:] = 1e-10 / (ell[2:] * (ell[2:] + 1))
        for peak_l in [220, 530, 810]:
            Cl += 5e-11 * np.exp(-(ell - peak_l)**2 / 50**2)

        sim_cmb = hp.synfast(Cl, nside, lmax=lmax, verbose=False)
        sim_cmb = sim_cmb / np.std(sim_cmb) * np.std(cmb)  # Match Planck variance

        for radius_deg in radii:
            radius = np.radians(radius_deg)
            for theta, phi in zip(theta_centers[:500], phi_centers[:500]):  # Subset for speed
                theta_anti, phi_anti = antipodal(theta, phi)
                T1, _, M1, f1 = extract_circle(sim_cmb, mask, theta, phi, radius, nside)
                T2, _, M2, f2 = extract_circle(sim_cmb, mask, theta_anti, phi_anti, radius, nside)
                if f1 >= 0.7 and f2 >= 0.7:
                    corr, _, _ = correlation_with_reversal(T1, T2, M1, M2)
                    sim_corrs[radius_deg].append(corr)

        print(f"    Simulation {sim_idx+1}/{n_sims} done")

    # Compare distributions
    fig, axes = plt.subplots(1, len(radii), figsize=(4*len(radii), 4))

    for i, r in enumerate(radii):
        ax = axes[i]
        ax.hist(sim_corrs[r], bins=30, alpha=0.5, density=True, label='Gaussian sims', color='blue')
        ax.hist(planck_corrs[r], bins=30, alpha=0.5, density=True, label='Planck', color='red')
        ax.axvline(np.mean(sim_corrs[r]), color='blue', linestyle='--')
        ax.axvline(np.mean(planck_corrs[r]), color='red', linestyle='--')
        ax.set_xlabel('Correlation')
        ax.set_ylabel('Density')
        ax.set_title(f'r = {r}°')
        ax.legend(fontsize=8)

    plt.tight_layout()
    outfile = os.path.join(DATA_DIR, 'planck_vs_simulations.png')
    plt.savefig(outfile, dpi=150, bbox_inches='tight')
    print(f"\n  Saved: {outfile}")
    plt.close()

    # Statistical comparison
    print("\n  STATISTICAL COMPARISON:")
    print("  " + "-"*50)
    for r in radii:
        p_mean = np.mean(planck_corrs[r])
        s_mean = np.mean(sim_corrs[r])
        s_std = np.std(sim_corrs[r])
        z = (p_mean - s_mean) / s_std if s_std > 0 else 0
        print(f"  r={r:2d}°: Planck={p_mean:.4f}, Sim={s_mean:.4f}±{s_std:.4f}, z={z:.1f}σ")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("DEEP INVESTIGATION OF CMB MATCHED CIRCLES")
    print("="*70)

    # Load data
    cmb, mask = load_planck_data(target_nside=512)
    nside = hp.get_nside(cmb)

    # Investigation 1: Best candidates
    candidates = investigate_best_candidates(cmb, mask, nside, n_centers=10000, top_n=50)

    # Investigation 2: Visualize
    visualize_candidates(candidates, DATA_DIR)

    # Investigation 3: Spatial distribution
    analyze_spatial_distribution(candidates, DATA_DIR)

    # Investigation 4: Fine radius search
    radii_fine, max_corrs_fine = fine_radius_search(cmb, mask, nside, n_centers=3000)

    # Investigation 5: Compare with simulations
    compare_with_simulations(cmb, mask, nside, n_sims=5, n_centers=1000)

    print("\n" + "="*70)
    print("INVESTIGATION COMPLETE")
    print("="*70)
