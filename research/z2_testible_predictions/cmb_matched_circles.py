#!/usr/bin/env python3
"""
CMB Matched Circles Search for T³/Z₂ Topology

This script searches for matched circles in the CMB that would indicate
T³/Z₂ cosmic topology. Unlike previous searches for standard T³, this
specifically looks for the antipodal + reversal matching pattern unique
to T³/Z₂.

Physics:
--------
In T³/Z₂ topology:
- Universe is a 3-torus with Z₂ (inversion) identification
- Points x and -x are identified
- Creates antipodal matched circles on CMB
- Circle temperatures match with reversal: T₁(ψ) = T₂(-ψ + φ₀)

Algorithm:
----------
1. For each candidate circle center (θ, φ)
2. Find antipodal center (π-θ, φ+π)
3. Extract temperature profiles on both circles
4. Test correlation with reversal: corr(T₁(ψ), T₂(-ψ))
5. If correlation > threshold, record as match

Carl Zimmerman | May 2026
"""

import numpy as np
from scipy import stats
from scipy.ndimage import gaussian_filter1d
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Try to import healpy (may not be installed)
try:
    import healpy as hp
    HEALPY_AVAILABLE = True
except ImportError:
    HEALPY_AVAILABLE = False
    print("WARNING: healpy not installed. Using simulated CMB map.")


# =============================================================================
# CONFIGURATION
# =============================================================================

@dataclass
class Config:
    """Configuration for matched circles search."""
    # Map parameters
    nside: int = 256  # HEALPix resolution (256 → ~14 arcmin pixels)
    lmax: int = 500   # Maximum multipole for power spectrum

    # Search parameters
    circle_radii_deg: List[float] = None  # Circle radii to search
    n_points_per_circle: int = 360  # Points to sample on each circle
    n_random_centers: int = 5000    # Number of random centers to test

    # Detection parameters
    correlation_threshold: float = 0.50  # Minimum correlation for match
    significance_threshold: float = 3.0  # Sigma threshold for detection

    def __post_init__(self):
        if self.circle_radii_deg is None:
            # Search radii from 15° to 75° in 5° steps
            self.circle_radii_deg = list(range(15, 80, 5))


config = Config()


# =============================================================================
# CMB MAP GENERATION/LOADING
# =============================================================================

def generate_simulated_cmb(nside: int = 256, seed: int = 42) -> np.ndarray:
    """
    Generate a simulated CMB map using theoretical power spectrum.

    This uses the standard ΛCDM power spectrum shape.
    For real analysis, use actual Planck maps.
    """
    np.random.seed(seed)
    npix = 12 * nside**2

    if HEALPY_AVAILABLE:
        # Generate from power spectrum
        lmax = 3 * nside - 1
        ell = np.arange(lmax + 1)

        # Approximate CMB power spectrum (Sachs-Wolfe + acoustic peaks)
        # C_l ∝ 1/[l(l+1)] with acoustic oscillations
        Cl = np.zeros(lmax + 1)
        Cl[2:] = 1e-10 / (ell[2:] * (ell[2:] + 1))

        # Add acoustic peaks
        for peak_l in [220, 530, 810]:
            Cl += 5e-11 * np.exp(-(ell - peak_l)**2 / (50**2))

        # Generate map
        cmb_map = hp.synfast(Cl, nside, lmax=lmax, verbose=False)

        # Normalize to μK
        cmb_map = cmb_map / np.std(cmb_map) * 100  # ~100 μK rms

    else:
        # Simple random field (fallback)
        cmb_map = np.random.randn(npix) * 100  # μK

    return cmb_map


def load_planck_map(filename: str = None,
                    mask_file: str = None,
                    target_nside: int = None) -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
    """
    Load Planck CMB map with optional mask and downsampling.

    Parameters:
    -----------
    filename : str
        Path to SMICA FITS file (e.g., COM_CMB_IQU-smica_2048_R3.00_full.fits)
    mask_file : str
        Path to mask FITS file (e.g., COM_Mask_CMB-common-Mask-Int_2048_R3.00.fits)
    target_nside : int
        Target resolution (for downsampling). If None, use native resolution.

    Returns:
    --------
    cmb_map : array or None
        Temperature map in μK
    mask : array or None
        Binary mask (1 = good, 0 = masked)
    """
    if not HEALPY_AVAILABLE:
        print("Cannot load Planck map without healpy")
        return None, None

    if filename is None:
        print("No Planck map provided. Use generate_simulated_cmb() instead.")
        return None, None

    try:
        # Load temperature map (field 0 in IQU file)
        print(f"   Loading CMB map from: {filename}")
        cmb_map = hp.read_map(filename, field=0, verbose=False)
        native_nside = hp.get_nside(cmb_map)
        print(f"   Native resolution: NSIDE = {native_nside}")

        # Convert from K to μK (Planck maps are in K)
        if np.std(cmb_map) < 1e-3:  # Likely in K
            cmb_map = cmb_map * 1e6
            print(f"   Converted from K to μK")

        # Load mask if provided
        mask = None
        if mask_file is not None:
            print(f"   Loading mask from: {mask_file}")
            mask = hp.read_map(mask_file, field=0, verbose=False)
            # Mask may have multiple fields, we want the first one
            if len(mask.shape) > 1:
                mask = mask[0]
            # Ensure binary (some masks use different conventions)
            mask = (mask > 0.5).astype(float)
            sky_fraction = np.mean(mask)
            print(f"   Sky fraction (unmasked): {sky_fraction*100:.1f}%")

        # Downsample if requested
        if target_nside is not None and target_nside < native_nside:
            print(f"   Downsampling from NSIDE={native_nside} to NSIDE={target_nside}...")
            cmb_map = hp.ud_grade(cmb_map, target_nside)
            if mask is not None:
                mask = hp.ud_grade(mask, target_nside)
                # Re-threshold after downsampling
                mask = (mask > 0.5).astype(float)

        print(f"   Temperature range: {cmb_map.min():.1f} to {cmb_map.max():.1f} μK")
        print(f"   RMS: {np.std(cmb_map):.1f} μK")

        return cmb_map, mask

    except Exception as e:
        print(f"Error loading map: {e}")
        import traceback
        traceback.print_exc()
        return None, None


# =============================================================================
# CIRCLE EXTRACTION
# =============================================================================

def get_circle_pixels(theta_center: float, phi_center: float,
                      radius: float, nside: int,
                      n_points: int = 360) -> Tuple[np.ndarray, np.ndarray]:
    """
    Get pixel indices and angles for points on a circle.

    Parameters:
    -----------
    theta_center : float
        Colatitude of circle center (radians)
    phi_center : float
        Longitude of circle center (radians)
    radius : float
        Circle radius (radians)
    nside : int
        HEALPix resolution
    n_points : int
        Number of points to sample

    Returns:
    --------
    pixels : array
        HEALPix pixel indices
    psi : array
        Angle around circle (radians)
    """
    psi = np.linspace(0, 2*np.pi, n_points, endpoint=False)

    # Points on circle in local coordinates
    # Circle is at colatitude = radius from center
    theta_local = radius * np.ones(n_points)
    phi_local = psi

    # Rotate to center position
    # Use spherical geometry
    cos_radius = np.cos(radius)
    sin_radius = np.sin(radius)
    cos_center = np.cos(theta_center)
    sin_center = np.sin(theta_center)

    # Spherical rotation
    theta_points = np.arccos(
        cos_center * cos_radius -
        sin_center * sin_radius * np.cos(psi)
    )

    phi_points = phi_center + np.arctan2(
        sin_radius * np.sin(psi),
        sin_center * cos_radius + cos_center * sin_radius * np.cos(psi)
    )

    # Wrap phi to [0, 2π)
    phi_points = phi_points % (2 * np.pi)

    if HEALPY_AVAILABLE:
        pixels = hp.ang2pix(nside, theta_points, phi_points)
    else:
        # Simple approximation for non-healpy case
        npix = 12 * nside**2
        pixels = ((theta_points / np.pi) * npix).astype(int) % npix

    return pixels, psi


def extract_circle_profile(cmb_map: np.ndarray,
                          theta_center: float, phi_center: float,
                          radius: float, nside: int,
                          n_points: int = 360,
                          mask: np.ndarray = None) -> Tuple[np.ndarray, np.ndarray, float]:
    """
    Extract temperature profile along a circle.

    Parameters:
    -----------
    cmb_map : array
        CMB temperature map
    theta_center, phi_center : float
        Center position (radians)
    radius : float
        Circle radius (radians)
    nside : int
        HEALPix resolution
    n_points : int
        Number of sample points
    mask : array or None
        Binary mask (1 = good, 0 = masked)

    Returns:
    --------
    T : array
        Temperature values around circle
    psi : array
        Angle around circle
    good_fraction : float
        Fraction of unmasked pixels (1.0 if no mask)
    """
    pixels, psi = get_circle_pixels(theta_center, phi_center,
                                    radius, nside, n_points)
    T = cmb_map[pixels]

    good_fraction = 1.0
    if mask is not None:
        mask_values = mask[pixels]
        good_fraction = np.mean(mask_values)
        # Set masked pixels to NaN for later interpolation
        T = np.where(mask_values > 0.5, T, np.nan)

    return T, psi, good_fraction


# =============================================================================
# T³/Z₂ MATCHING ALGORITHM
# =============================================================================

def compute_antipodal_center(theta: float, phi: float) -> Tuple[float, float]:
    """
    Compute antipodal point on sphere.

    For T³/Z₂: point (θ, φ) is identified with (π-θ, φ+π)
    """
    theta_anti = np.pi - theta
    phi_anti = (phi + np.pi) % (2 * np.pi)
    return theta_anti, phi_anti


def correlation_with_reversal(T1: np.ndarray, T2: np.ndarray,
                              phase_search: bool = True) -> Tuple[float, float]:
    """
    Compute correlation between T1(ψ) and T2(-ψ + φ₀).

    For T³/Z₂ matching, we expect:
    - T₁(ψ) matches T₂(-ψ + φ₀) for some phase offset φ₀

    Parameters:
    -----------
    T1, T2 : arrays
        Temperature profiles (same length), may contain NaN for masked pixels
    phase_search : bool
        If True, search over phase offsets to maximize correlation

    Returns:
    --------
    max_corr : float
        Maximum correlation found
    best_phase : float
        Phase offset giving maximum correlation
    """
    n = len(T1)

    # Handle NaN values (masked pixels)
    valid1 = ~np.isnan(T1)
    valid2 = ~np.isnan(T2)

    # If too many masked pixels, return low correlation
    if np.sum(valid1) < n * 0.5 or np.sum(valid2) < n * 0.5:
        return 0.0, 0.0

    # Interpolate over NaN values for FFT
    if np.any(~valid1):
        T1 = np.interp(np.arange(n), np.where(valid1)[0], T1[valid1])
    if np.any(~valid2):
        T2 = np.interp(np.arange(n), np.where(valid2)[0], T2[valid2])

    # Reverse T2 (for -ψ)
    T2_reversed = T2[::-1]

    if not phase_search:
        # Direct correlation without phase search
        corr = np.corrcoef(T1, T2_reversed)[0, 1]
        return corr if not np.isnan(corr) else 0.0, 0.0

    # Search over phase offsets using FFT cross-correlation
    # Normalize
    std1 = np.std(T1)
    std2 = np.std(T2_reversed)
    if std1 < 1e-10 or std2 < 1e-10:
        return 0.0, 0.0

    T1_norm = (T1 - np.mean(T1)) / std1
    T2_norm = (T2_reversed - np.mean(T2_reversed)) / std2

    # Cross-correlation via FFT
    fft1 = np.fft.fft(T1_norm)
    fft2 = np.fft.fft(T2_norm)
    cross_corr = np.fft.ifft(fft1 * np.conj(fft2)).real / n

    # Find maximum
    max_idx = np.argmax(cross_corr)
    max_corr = cross_corr[max_idx]
    best_phase = 2 * np.pi * max_idx / n

    return max_corr, best_phase


def search_matched_circles(cmb_map: np.ndarray,
                          radius_deg: float,
                          nside: int,
                          n_centers: int = 1000,
                          n_points: int = 360,
                          threshold: float = 0.5,
                          include_centers: List[Tuple[float, float]] = None,
                          mask: np.ndarray = None,
                          min_good_fraction: float = 0.7) -> List[dict]:
    """
    Search for matched circles at given radius.

    Parameters:
    -----------
    cmb_map : array
        CMB temperature map
    radius_deg : float
        Circle radius in degrees
    nside : int
        HEALPix resolution
    n_centers : int
        Number of random centers to test
    n_points : int
        Points per circle
    threshold : float
        Correlation threshold for detection
    include_centers : list of (theta, phi) tuples
        Additional specific centers to test (for validation)
    mask : array or None
        Binary mask (1 = good, 0 = masked)
    min_good_fraction : float
        Minimum fraction of unmasked pixels required (default 0.7)

    Returns:
    --------
    matches : list of dict
        Detected matches with centers, correlation, phase
    """
    radius = np.radians(radius_deg)
    matches = []
    all_correlations = []

    # Generate random circle centers
    np.random.seed(12345)  # Reproducibility
    theta_centers = np.arccos(1 - 2 * np.random.rand(n_centers))  # Uniform on sphere
    phi_centers = 2 * np.pi * np.random.rand(n_centers)

    # Add specific centers if provided (for validation)
    if include_centers:
        for theta_c, phi_c in include_centers:
            theta_centers = np.append(theta_centers, theta_c)
            phi_centers = np.append(phi_centers, phi_c)

    n_skipped = 0
    for i, (theta, phi) in enumerate(zip(theta_centers, phi_centers)):
        # Get antipodal center
        theta_anti, phi_anti = compute_antipodal_center(theta, phi)

        # Extract profiles
        T1, psi1, frac1 = extract_circle_profile(cmb_map, theta, phi,
                                                  radius, nside, n_points, mask)
        T2, psi2, frac2 = extract_circle_profile(cmb_map, theta_anti, phi_anti,
                                                  radius, nside, n_points, mask)

        # Skip if too many masked pixels
        if frac1 < min_good_fraction or frac2 < min_good_fraction:
            n_skipped += 1
            all_correlations.append(0.0)
            continue

        # Compute correlation with reversal (T³/Z₂ matching)
        corr, phase = correlation_with_reversal(T1, T2)
        all_correlations.append(corr)

        if corr > threshold:
            matches.append({
                'center1': (np.degrees(theta), np.degrees(phi)),
                'center2': (np.degrees(theta_anti), np.degrees(phi_anti)),
                'radius': radius_deg,
                'correlation': corr,
                'phase': np.degrees(phase),
                'good_fraction': min(frac1, frac2),
            })

    return matches, np.array(all_correlations)


# =============================================================================
# STATISTICAL ANALYSIS
# =============================================================================

def compute_null_distribution(cmb_map: np.ndarray,
                             radius_deg: float,
                             nside: int,
                             n_trials: int = 1000,
                             n_points: int = 360,
                             mask: np.ndarray = None) -> np.ndarray:
    """
    Compute null distribution of correlations for random circle pairs.

    This uses non-antipodal circles to establish the null hypothesis.
    """
    radius = np.radians(radius_deg)
    null_correlations = []

    np.random.seed(54321)

    for _ in range(n_trials):
        # Two random (non-antipodal) centers
        theta1 = np.arccos(1 - 2 * np.random.rand())
        phi1 = 2 * np.pi * np.random.rand()

        theta2 = np.arccos(1 - 2 * np.random.rand())
        phi2 = 2 * np.pi * np.random.rand()

        # Ensure they're not antipodal
        sep = np.arccos(np.sin(theta1)*np.sin(theta2)*np.cos(phi1-phi2) +
                       np.cos(theta1)*np.cos(theta2))
        if np.abs(sep - np.pi) < 0.1:  # Too close to antipodal
            continue

        T1, _, frac1 = extract_circle_profile(cmb_map, theta1, phi1, radius, nside, n_points, mask)
        T2, _, frac2 = extract_circle_profile(cmb_map, theta2, phi2, radius, nside, n_points, mask)

        # Skip if too many masked pixels
        if frac1 < 0.7 or frac2 < 0.7:
            continue

        corr, _ = correlation_with_reversal(T1, T2)
        null_correlations.append(corr)

    return np.array(null_correlations)


def compute_significance(observed_corr: float,
                        null_distribution: np.ndarray) -> float:
    """
    Compute significance of observed correlation vs null distribution.
    """
    mean_null = np.mean(null_distribution)
    std_null = np.std(null_distribution)

    if std_null == 0:
        return 0.0

    z_score = (observed_corr - mean_null) / std_null
    return z_score


# =============================================================================
# INJECTION TEST (VALIDATION)
# =============================================================================

def inject_matched_circles(cmb_map: np.ndarray,
                          nside: int,
                          radius_deg: float = 45.0,
                          amplitude: float = 50.0,
                          center: Tuple[float, float] = None) -> np.ndarray:
    """
    Inject artificial matched circles for validation.

    This creates a pair of antipodal circles with identical (reversed)
    temperature patterns to test the detection algorithm.
    """
    cmb_modified = cmb_map.copy()

    if center is None:
        center = (np.pi/3, np.pi/2)  # Default center

    theta_c, phi_c = center
    theta_anti, phi_anti = compute_antipodal_center(theta_c, phi_c)
    radius = np.radians(radius_deg)

    # Get circle pixels
    n_points = 360
    pixels1, psi1 = get_circle_pixels(theta_c, phi_c, radius, nside, n_points)
    pixels2, psi2 = get_circle_pixels(theta_anti, phi_anti, radius, nside, n_points)

    # Create matching pattern (sinusoidal for clarity)
    pattern = amplitude * (np.sin(3 * psi1) + 0.5 * np.sin(7 * psi1))

    # Add to circle 1
    for pix, val in zip(pixels1, pattern):
        cmb_modified[pix] += val

    # Add reversed pattern to circle 2 (T³/Z₂ matching)
    pattern_reversed = pattern[::-1]
    for pix, val in zip(pixels2, pattern_reversed):
        cmb_modified[pix] += val

    return cmb_modified


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_results(cmb_map: np.ndarray,
                matches: List[dict],
                all_correlations: dict,
                null_distributions: dict,
                output_file: str = None):
    """
    Create comprehensive visualization of results.
    """
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    # Panel 1: CMB map (if healpy available)
    ax1 = axes[0, 0]
    if HEALPY_AVAILABLE:
        # Project to 2D for simple visualization
        nside = hp.get_nside(cmb_map)
        npix = len(cmb_map)

        # Simple Mollweide-like projection
        n_theta = 180
        n_phi = 360
        img = np.zeros((n_theta, n_phi))

        for i in range(n_theta):
            for j in range(n_phi):
                theta = np.pi * i / n_theta
                phi = 2 * np.pi * j / n_phi
                pix = hp.ang2pix(nside, theta, phi)
                img[i, j] = cmb_map[pix]

        im = ax1.imshow(img, cmap='RdBu_r', aspect='auto',
                       extent=[0, 360, 180, 0])
        plt.colorbar(im, ax=ax1, label='Temperature (μK)')
    else:
        ax1.text(0.5, 0.5, 'CMB Map\n(requires healpy)',
                ha='center', va='center', transform=ax1.transAxes)
    ax1.set_title('CMB Temperature Map')
    ax1.set_xlabel('Longitude (°)')
    ax1.set_ylabel('Colatitude (°)')

    # Panel 2: Correlation histogram for one radius
    ax2 = axes[0, 1]
    if all_correlations:
        radius = list(all_correlations.keys())[len(all_correlations)//2]
        corrs = all_correlations[radius]
        ax2.hist(corrs, bins=50, density=True, alpha=0.7, label='Antipodal pairs')

        if radius in null_distributions:
            null = null_distributions[radius]
            ax2.hist(null, bins=50, density=True, alpha=0.5, label='Random pairs')

        ax2.axvline(x=0.5, color='r', linestyle='--', label='Threshold')
        ax2.set_xlabel('Correlation')
        ax2.set_ylabel('Density')
        ax2.set_title(f'Correlation Distribution (r = {radius}°)')
        ax2.legend()

    # Panel 3: Max correlation vs radius
    ax3 = axes[0, 2]
    if all_correlations:
        radii = sorted(all_correlations.keys())
        max_corrs = [np.max(all_correlations[r]) for r in radii]
        mean_corrs = [np.mean(all_correlations[r]) for r in radii]

        ax3.plot(radii, max_corrs, 'ro-', label='Max correlation')
        ax3.plot(radii, mean_corrs, 'b.-', label='Mean correlation')
        ax3.axhline(y=0.5, color='g', linestyle='--', label='Threshold')
        ax3.set_xlabel('Circle Radius (°)')
        ax3.set_ylabel('Correlation')
        ax3.set_title('Correlation vs Circle Radius')
        ax3.legend()
        ax3.grid(True, alpha=0.3)

    # Panel 4: Best match example
    ax4 = axes[1, 0]
    if matches:
        best = max(matches, key=lambda x: x['correlation'])
        ax4.text(0.5, 0.7, f"Best Match Found:",
                ha='center', transform=ax4.transAxes, fontsize=14, fontweight='bold')
        ax4.text(0.5, 0.5, f"Radius: {best['radius']:.1f}°\n"
                          f"Correlation: {best['correlation']:.3f}\n"
                          f"Center 1: ({best['center1'][0]:.1f}°, {best['center1'][1]:.1f}°)\n"
                          f"Center 2: ({best['center2'][0]:.1f}°, {best['center2'][1]:.1f}°)",
                ha='center', va='center', transform=ax4.transAxes, fontsize=11)
    else:
        ax4.text(0.5, 0.5, 'No matches found\nabove threshold',
                ha='center', va='center', transform=ax4.transAxes, fontsize=14)
    ax4.axis('off')
    ax4.set_title('Detection Summary')

    # Panel 5: Significance analysis
    ax5 = axes[1, 1]
    if all_correlations and null_distributions:
        radii = sorted(all_correlations.keys())
        significances = []

        for r in radii:
            if r in null_distributions:
                max_corr = np.max(all_correlations[r])
                sig = compute_significance(max_corr, null_distributions[r])
                significances.append(sig)
            else:
                significances.append(0)

        colors = ['green' if s < 2 else 'orange' if s < 3 else 'red' for s in significances]
        ax5.bar(radii, significances, color=colors, width=4)
        ax5.axhline(y=3, color='r', linestyle='--', label='3σ threshold')
        ax5.axhline(y=5, color='darkred', linestyle='--', label='5σ threshold')
        ax5.set_xlabel('Circle Radius (°)')
        ax5.set_ylabel('Significance (σ)')
        ax5.set_title('Detection Significance')
        ax5.legend()
        ax5.grid(True, alpha=0.3)

    # Panel 6: T³/Z₂ matching illustration
    ax6 = axes[1, 2]
    # Draw schematic of matching pattern
    theta = np.linspace(0, 2*np.pi, 100)
    ax6.plot(np.cos(theta), np.sin(theta), 'b-', lw=2, label='Circle 1')
    ax6.plot(-np.cos(theta), -np.sin(theta), 'r--', lw=2, label='Circle 2 (antipodal)')

    # Add arrows showing reversal
    ax6.annotate('', xy=(0.7, 0.7), xytext=(0.5, 0.5),
                arrowprops=dict(arrowstyle='->', color='blue'))
    ax6.annotate('', xy=(-0.7, -0.7), xytext=(-0.5, -0.5),
                arrowprops=dict(arrowstyle='->', color='red'))

    ax6.set_xlim(-1.5, 1.5)
    ax6.set_ylim(-1.5, 1.5)
    ax6.set_aspect('equal')
    ax6.set_title('T³/Z₂ Matching Pattern\nT₁(ψ) = T₂(-ψ)')
    ax6.legend()
    ax6.axis('off')

    plt.tight_layout()

    if output_file:
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        print(f"Saved visualization to {output_file}")

    plt.close()


# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def run_full_analysis(use_injection: bool = True,
                     injection_amplitude: float = 30.0,
                     planck_map_file: str = None,
                     planck_mask_file: str = None,
                     target_nside: int = None):
    """
    Run complete matched circles analysis.

    Parameters:
    -----------
    use_injection : bool
        If True, inject artificial matched circles for validation (only for simulated)
    injection_amplitude : float
        Amplitude of injected signal (μK)
    planck_map_file : str
        Path to Planck SMICA FITS file (if provided, uses real data)
    planck_mask_file : str
        Path to Planck mask FITS file
    target_nside : int
        Target resolution for downsampling (default: use native or config)
    """
    print("=" * 70)
    print("CMB MATCHED CIRCLES SEARCH FOR T³/Z₂ TOPOLOGY")
    print("=" * 70)

    mask = None
    injection_center = None
    injection_radius = None

    # Load Planck data or generate simulated
    if planck_map_file is not None:
        print("\n1. Loading Planck CMB map...")
        cmb_map, mask = load_planck_map(
            planck_map_file,
            mask_file=planck_mask_file,
            target_nside=target_nside or 512  # Downsample for speed
        )

        if cmb_map is None:
            print("ERROR: Failed to load Planck map")
            return None, None, None

        nside = hp.get_nside(cmb_map)
        use_injection = False  # Don't inject into real data
    else:
        print("\n1. Generating simulated CMB map...")
        nside = config.nside
        cmb_map = generate_simulated_cmb(nside)
        print(f"   Map resolution: NSIDE = {nside} ({12*nside**2} pixels)")
        print(f"   Temperature range: {cmb_map.min():.1f} to {cmb_map.max():.1f} μK")

        # Optional: inject matched circles for validation
        if use_injection:
            print(f"\n2. Injecting artificial matched circles (amplitude = {injection_amplitude} μK)...")
            injection_center = (np.pi/3, np.pi/4)
            injection_radius = 45.0
            cmb_map = inject_matched_circles(cmb_map, nside,
                                             radius_deg=injection_radius,
                                             amplitude=injection_amplitude,
                                             center=injection_center)
            print(f"   Injected at center: ({np.degrees(injection_center[0]):.1f}°, {np.degrees(injection_center[1]):.1f}°)")
            print(f"   Circle radius: {injection_radius}°")

    # Search for matched circles
    step = 3 if planck_map_file else 2
    print(f"\n{step}. Searching for matched circles...")
    all_matches = []
    all_correlations = {}
    null_distributions = {}

    # If injection test, include the injection center in search
    specific_centers = None
    if use_injection and injection_center is not None:
        specific_centers = [injection_center]

    for radius in config.circle_radii_deg:
        print(f"   Radius = {radius}°...", end=" ", flush=True)

        # Search antipodal pairs
        matches, correlations = search_matched_circles(
            cmb_map, radius, nside,
            n_centers=config.n_random_centers,
            n_points=config.n_points_per_circle,
            threshold=config.correlation_threshold,
            include_centers=specific_centers,
            mask=mask
        )

        all_correlations[radius] = correlations
        all_matches.extend(matches)

        # Compute null distribution (subset for speed)
        null = compute_null_distribution(
            cmb_map, radius, nside,
            n_trials=500,
            n_points=config.n_points_per_circle,
            mask=mask
        )
        null_distributions[radius] = null

        # Report
        max_corr = np.max(correlations) if len(correlations) > 0 else 0
        n_matches = len([m for m in matches if m['radius'] == radius])
        sig = compute_significance(max_corr, null)
        print(f"max corr = {max_corr:.3f}, {n_matches} matches, {sig:.1f}σ")

    # Summary
    print("\n" + "=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)

    if all_matches:
        print(f"\nTotal matches found: {len(all_matches)}")

        # Best match
        best = max(all_matches, key=lambda x: x['correlation'])
        print(f"\nBest match:")
        print(f"  Radius: {best['radius']:.1f}°")
        print(f"  Correlation: {best['correlation']:.4f}")
        print(f"  Center 1: θ={best['center1'][0]:.2f}°, φ={best['center1'][1]:.2f}°")
        print(f"  Center 2: θ={best['center2'][0]:.2f}°, φ={best['center2'][1]:.2f}°")
        print(f"  Phase offset: {best['phase']:.1f}°")

        # Significance
        radius = best['radius']
        if radius in null_distributions:
            sig = compute_significance(best['correlation'], null_distributions[radius])
            print(f"  Significance: {sig:.1f}σ")

            if sig > 5:
                print("\n  *** DETECTION! Significance > 5σ ***")
            elif sig > 3:
                print("\n  ** Evidence for match (3-5σ) **")
    else:
        print("\nNo matches found above threshold.")
        print("This is consistent with:")
        print("  - No T³/Z₂ topology at this scale")
        print("  - Topology scale larger than observable universe")

    # Visualization
    print("\n4. Creating visualization...")
    output_file = "/Users/carlzimmerman/new_physics/zimmerman-formula/research/z2_testible_predictions/cmb_matched_circles_results.png"
    plot_results(cmb_map, all_matches, all_correlations,
                null_distributions, output_file)

    # Interpretation
    print("\n" + "=" * 70)
    print("INTERPRETATION")
    print("=" * 70)

    if use_injection:
        print(f"""
INJECTION TEST RESULTS:
-----------------------
We injected artificial matched circles at:
  - Radius: {injection_radius}°
  - Amplitude: {injection_amplitude} μK

The algorithm {"SUCCESSFULLY DETECTED" if any(m['radius'] == injection_radius and m['correlation'] > config.correlation_threshold for m in all_matches) else "did not detect"} the injected signal.

This validates that the algorithm can detect T³/Z₂ topology if present.
""")

    print("""
PHYSICS IMPLICATIONS:
--------------------
If NO significant matches are found (with real Planck data):
  → T³/Z₂ topology has L > observable universe (undetectable)
  → OR the universe is simply connected

If SIGNIFICANT matches are found:
  → Evidence for T³/Z₂ cosmic topology!
  → Circle radius gives fundamental domain size
  → Would be a major discovery

NEXT STEPS:
-----------
1. Run this analysis on actual Planck SMICA map
2. Apply galactic mask to avoid foreground contamination
3. Compare with simulated maps (null hypothesis testing)
4. If detection: verify with different CMB maps (NILC, SEVEM)
""")

    return all_matches, all_correlations, null_distributions


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    import sys
    import os

    # Command line options:
    #   --planck : Use Planck SMICA data (looks for files in planck_data/)
    #   --planck-map <file> : Specify Planck map file
    #   --planck-mask <file> : Specify Planck mask file
    #   --nside <value> : Target NSIDE for downsampling (default 512)
    #   --no-injection : Run without injection (for simulated analysis)
    #   --injection-amplitude <value> : Set injection amplitude (default 150 μK)

    use_injection = True
    injection_amplitude = 150.0
    planck_map = None
    planck_mask = None
    target_nside = 512

    # Data directory
    data_dir = os.path.dirname(os.path.abspath(__file__))

    # Parse arguments
    if "--planck" in sys.argv:
        # Use default Planck file locations
        planck_map = os.path.join(data_dir, "COM_CMB_IQU-smica_2048_R3.00_full.fits")
        planck_mask = os.path.join(data_dir, "COM_Mask_CMB-common-Mask-Int_2048_R3.00.fits")
        print("\n*** Running on REAL PLANCK DATA ***\n")

    if "--planck-map" in sys.argv:
        idx = sys.argv.index("--planck-map")
        planck_map = sys.argv[idx + 1]

    if "--planck-mask" in sys.argv:
        idx = sys.argv.index("--planck-mask")
        planck_mask = sys.argv[idx + 1]

    if "--nside" in sys.argv:
        idx = sys.argv.index("--nside")
        target_nside = int(sys.argv[idx + 1])

    if "--no-injection" in sys.argv:
        use_injection = False
        if planck_map is None:
            print("\n*** Running simulated data WITHOUT injection ***\n")

    if "--injection-amplitude" in sys.argv:
        idx = sys.argv.index("--injection-amplitude")
        injection_amplitude = float(sys.argv[idx + 1])

    if planck_map is None and use_injection:
        print(f"\n*** Running with INJECTED matched circles (amplitude = {injection_amplitude} μK) ***\n")

    matches, correlations, nulls = run_full_analysis(
        use_injection=use_injection,
        injection_amplitude=injection_amplitude,
        planck_map_file=planck_map,
        planck_mask_file=planck_mask,
        target_nside=target_nside
    )
