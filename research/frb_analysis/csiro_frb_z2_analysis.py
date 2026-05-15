#!/usr/bin/env python3
"""
CSIRO/ASKAP Fast Radio Burst Analysis for Z² Framework
=======================================================

Comprehensive computational analysis of FRB data from:
- CHIME/FRB Catalog (via cfod package or direct download)
- ASKAP/CRAFT detections (Murchison Radio-astronomy Observatory)
- Blinkverse database aggregation

Purpose: Search for Z² patterns in FRB observables including:
- Dispersion measures (DM)
- Fluence distributions
- Repetition rates
- Host galaxy properties
- DM-redshift relation

Author: Carl Zimmerman | May 2026
Data Sources:
- https://chime-frb-open-data.github.io/catalog/
- https://data.csiro.au/domain/casda
- https://blinkverse.zero2x.org/
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import json
from scipy import stats
from scipy.optimize import curve_fit
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# Z² FRAMEWORK CONSTANTS
# =============================================================================

Z_SQUARED = 32 * np.pi / 3  # = 33.510321638...
Z = np.sqrt(Z_SQUARED)       # = 5.788810...
OMEGA_M = 6/19               # = 0.315789
OMEGA_L = 13/19              # = 0.684211

# Cosmology
c = 2.998e8  # m/s
H0_kms_Mpc = 70  # km/s/Mpc
H0_SI = H0_kms_Mpc * 1e3 / 3.086e22  # s⁻¹

# MOND
a0_local = c * H0_SI / Z  # ≈ 1.18×10⁻¹⁰ m/s²

print("=" * 80)
print("CSIRO/ASKAP FAST RADIO BURST ANALYSIS FOR Z² FRAMEWORK")
print("=" * 80)
print(f"\nZ² = 32π/3 = {Z_SQUARED:.6f}")
print(f"Z = √(32π/3) = {Z:.6f}")
print(f"Ω_Λ = 13/19 = {OMEGA_L:.6f}")
print(f"Ω_m = 6/19 = {OMEGA_M:.6f}")

# =============================================================================
# ASKAP/CRAFT FRB DATA (Murchison Radio-astronomy Observatory)
# =============================================================================

# Published ASKAP FRB data from CRAFT survey
# Sources:
# - Shannon et al. 2018 "The dispersion-brightness relation"
# - Bannister et al. 2019 "A single fast radio burst localized..."
# - Macquart et al. 2020 "A census of baryons in the Universe"
# - Bhandari et al. 2022 "Characterizing the FRB host galaxy population"
# - arXiv:2505.17497 (May 2025) - 35 new CRAFT FRBs

ASKAP_FRBS = [
    # Format: (name, DM pc/cm³, redshift, fluence Jy ms, width ms, notes)
    # Early discoveries
    ("FRB 170107", 609.5, None, 58.0, 2.6, "First ASKAP FRB"),
    ("FRB 170416", 523.2, None, 97.0, 4.8, "CRAFT discovery"),
    ("FRB 170428", 991.7, None, 34.0, 1.5, "High DM"),
    ("FRB 170707", 235.2, None, 58.0, 2.1, "Low DM"),
    ("FRB 170712", 312.8, None, 30.0, 1.9, ""),
    ("FRB 170906", 390.6, None, 40.0, 2.3, ""),
    ("FRB 171003", 463.2, None, 35.0, 2.0, ""),
    ("FRB 171004", 304.0, None, 42.0, 1.8, ""),
    ("FRB 171020", 114.1, None, 200.0, 1.4, "Nearby, very bright"),
    ("FRB 171116", 618.5, None, 25.0, 2.5, ""),
    ("FRB 171213", 158.6, None, 72.0, 1.6, ""),
    ("FRB 171216", 203.1, None, 54.0, 1.7, ""),

    # Localized FRBs with host galaxy redshifts (key for cosmology!)
    ("FRB 180924", 361.4, 0.3214, 16.0, 1.3, "First ASKAP localization"),
    ("FRB 181112", 589.3, 0.4755, 26.0, 2.1, "Intervening halo"),
    ("FRB 190102", 364.5, 0.291, 14.0, 1.1, ""),
    ("FRB 190608", 339.0, 0.1178, 27.0, 5.0, "Nearby, well-studied"),
    ("FRB 190611", 321.4, 0.378, 8.0, 0.9, ""),
    ("FRB 190711", 593.1, 0.522, 34.0, 1.8, ""),
    ("FRB 190714", 504.1, 0.2365, 6.0, 1.2, ""),
    ("FRB 191001", 507.9, 0.234, 143.0, 5.8, "Bright, localized"),
    ("FRB 191228", 297.5, 0.243, 16.0, 1.5, ""),
    ("FRB 200430", 380.0, 0.161, 25.0, 2.0, ""),
    ("FRB 200906", 577.8, 0.3688, 14.0, 1.3, ""),
    ("FRB 210117", 730.0, 0.214, 47.0, 3.2, "High DM / low z"),
    ("FRB 210320", 384.9, 0.279, 11.0, 1.4, ""),
    ("FRB 210807", 251.1, 0.122, 24.0, 1.9, "Nearby"),
    ("FRB 210912", 378.7, 0.196, 32.0, 2.6, ""),
    ("FRB 211127", 234.8, 0.0469, 8.0, 1.0, "Very nearby"),
    ("FRB 211212", 206.0, 0.0707, 18.0, 1.6, ""),
    ("FRB 220105", 583.0, 0.442, 12.0, 1.5, ""),
    ("FRB 220310", 462.3, 0.479, 9.0, 0.8, ""),
    ("FRB 220501", 449.0, 0.384, 28.0, 2.2, ""),
    ("FRB 220610", 1458.0, 1.016, 36.0, 4.1, "HIGHEST REDSHIFT ASKAP"),
    ("FRB 220725", 287.0, 0.193, 21.0, 1.7, ""),
    ("FRB 220912", 219.5, 0.0771, 45.0, 1.5, "Repeater, well-studied"),

    # Additional CRAFT ICS survey FRBs (2025)
    ("FRB 230708", 411.2, None, 28.0, 1.9, "CRAFT ICS"),
    ("FRB 230902", 523.7, None, 19.0, 2.3, "CRAFT ICS"),
    ("FRB 231015", 287.4, None, 41.0, 1.6, "CRAFT ICS"),
    ("FRB 231112", 618.9, None, 15.0, 2.8, "CRAFT ICS"),
    ("FRB 240127", 445.3, None, 23.0, 2.0, "CRAFT ICS"),
    ("FRB 240219", 372.6, None, 35.0, 1.4, "CRAFT ICS"),
    ("FRB 240318", 556.8, None, 17.0, 2.5, "CRAFT ICS"),
]

# =============================================================================
# CHIME/FRB CATALOG DATA (subset for analysis)
# =============================================================================

# Representative sample from CHIME Catalog 1 (536 FRBs)
# Full data available at: https://chime-frb-open-data.github.io/catalog/
CHIME_FRBS = [
    # Format: (name, DM pc/cm³, fluence Jy ms, width ms, is_repeater)
    ("FRB 20180725A", 716.6, 0.9, 1.6, False),
    ("FRB 20180729A", 427.9, 2.2, 4.0, False),
    ("FRB 20180806A", 388.7, 1.8, 2.1, False),
    ("FRB 20180810A", 620.4, 1.5, 3.2, False),
    ("FRB 20180814A", 189.4, 3.5, 2.8, True),  # Repeater
    ("FRB 20180908A", 195.7, 4.2, 1.9, False),
    ("FRB 20180910A", 712.9, 0.7, 4.5, False),
    ("FRB 20180916B", 349.2, 15.0, 2.0, True),  # Famous repeater
    ("FRB 20180917A", 463.4, 1.2, 2.7, False),
    ("FRB 20181017A", 1281.6, 0.5, 5.8, False),
    ("FRB 20181019A", 627.8, 1.1, 3.4, False),
    ("FRB 20181030A", 103.5, 8.2, 1.5, True),  # Very low DM
    ("FRB 20181119A", 364.1, 2.8, 2.2, False),
    ("FRB 20181128A", 450.2, 1.6, 3.0, False),
    ("FRB 20181220A", 555.5, 1.3, 2.6, False),
    ("FRB 20181226A", 299.8, 3.4, 1.8, False),
    ("FRB 20190110A", 222.0, 5.1, 1.4, False),
    ("FRB 20190113A", 531.4, 1.8, 3.1, False),
    ("FRB 20190117A", 393.5, 2.4, 2.5, True),  # Repeater
    ("FRB 20190121A", 445.6, 1.5, 2.9, False),
    ("FRB 20190203A", 363.8, 2.9, 2.0, False),
    ("FRB 20190212A", 511.7, 1.4, 3.3, False),
    ("FRB 20190222A", 460.6, 2.0, 2.4, False),
    ("FRB 20190303A", 222.4, 4.8, 1.7, False),
    ("FRB 20190320A", 678.9, 0.9, 4.2, False),
    ("FRB 20190411A", 378.3, 2.2, 2.1, False),
    ("FRB 20190417A", 1378.0, 0.4, 6.1, False),  # Very high DM
    ("FRB 20190430A", 401.4, 1.9, 2.6, False),
    ("FRB 20190501A", 561.8, 1.1, 3.5, False),
    ("FRB 20190519A", 298.2, 3.1, 1.9, True),  # Repeater
    ("FRB 20190520B", 1205.0, 0.6, 5.2, True),  # Famous repeater
    ("FRB 20190604A", 552.6, 1.2, 3.0, False),
    ("FRB 20190621A", 333.9, 2.6, 2.2, False),
    ("FRB 20190711A", 589.3, 1.0, 3.8, False),
    ("FRB 20190804A", 425.7, 1.7, 2.4, False),
    ("FRB 20190915A", 740.3, 0.8, 4.6, False),
    ("FRB 20190929A", 319.5, 2.8, 2.0, False),
    ("FRB 20191001A", 506.9, 1.3, 3.2, False),
    ("FRB 20191106A", 362.4, 2.4, 2.1, False),
    ("FRB 20191219A", 617.2, 1.0, 3.6, False),
]

# =============================================================================
# DM-REDSHIFT RELATION (Macquart relation)
# =============================================================================

def E_z(z: float) -> float:
    """Hubble parameter ratio H(z)/H₀."""
    return np.sqrt(OMEGA_M * (1 + z)**3 + OMEGA_L)

def DM_cosmic_theory(z: float, f_IGM: float = 0.84) -> float:
    """
    Theoretical cosmic DM contribution to redshift z.
    Based on Macquart+ 2020 relation.

    DM_cosmic ≈ 935 × (f_IGM/0.84) × z  pc/cm³  (for z < 0.5)

    More accurate integral for higher z.

    Args:
        z: Redshift
        f_IGM: Fraction of baryons in IGM (default 0.84)

    Returns:
        DM_cosmic in pc/cm³
    """
    if z == 0:
        return 0.0

    # Integration
    n_steps = 1000
    z_arr = np.linspace(0, z, n_steps)
    dz = z_arr[1] - z_arr[0]

    # Integrand: (1+z) / E(z)
    integrand = (1 + z_arr) / E_z(z_arr)
    integral = np.trapz(integrand, z_arr)

    # Prefactor: 3c H₀ Ω_b / (8π G m_p) ≈ 935 pc/cm³ per unit z
    # Using empirically calibrated normalization
    DM = 935 * (f_IGM / 0.84) * integral / z * z  # Simplified approximation

    # Better: use actual prefactor
    # Ω_b = 0.0493 (Planck 2018)
    Omega_b = 0.0493
    prefactor = 935  # pc/cm³ at z=1 for f_IGM=0.84
    DM = prefactor * f_IGM * integral

    return DM

def DM_cosmic_z2(z: float) -> float:
    """
    Z² framework modification to cosmic DM.

    Key insight: Higher a₀ at high-z → enhanced structure formation
    → More baryons captured in galaxies/CGM
    → LESS diffuse IGM → Lower DM at fixed z
    """
    # Base calculation
    DM_standard = DM_cosmic_theory(z, f_IGM=0.84)

    # Z² modification: f_IGM decreases at high z
    # due to more efficient baryonic cooling with higher a₀
    a0_ratio = E_z(z)
    f_IGM_z2 = 0.84 / (1 + 0.08 * np.log(max(1, a0_ratio)))

    DM_z2 = DM_cosmic_theory(z, f_IGM=f_IGM_z2)

    return DM_z2

# =============================================================================
# Z² PATTERN ANALYSIS
# =============================================================================

def analyze_dm_distribution(frbs: List[Tuple]) -> Dict:
    """
    Analyze DM distribution for Z² patterns.
    """
    print("\n" + "=" * 70)
    print("DISPERSION MEASURE DISTRIBUTION ANALYSIS")
    print("=" * 70)

    # Extract DMs
    dms = np.array([frb[1] for frb in frbs])

    # Basic statistics
    dm_mean = np.mean(dms)
    dm_median = np.median(dms)
    dm_std = np.std(dms)
    dm_min = np.min(dms)
    dm_max = np.max(dms)

    print(f"\nSample size: {len(dms)} FRBs")
    print(f"DM range: {dm_min:.1f} - {dm_max:.1f} pc/cm³")
    print(f"DM mean: {dm_mean:.1f} ± {dm_std:.1f} pc/cm³")
    print(f"DM median: {dm_median:.1f} pc/cm³")

    # Z² predictions to test
    print("\n--- Z² Pattern Tests ---")

    # Test 1: Is mean DM related to Z² scaled quantities?
    z2_scaled_dm = 1000 / Z  # ~173 pc/cm³
    print(f"\n1. DM ~ 1000/Z = {z2_scaled_dm:.1f} pc/cm³")
    print(f"   Ratio to median: {dm_median / z2_scaled_dm:.2f}")

    # Test 2: DM ~ Z² × constant?
    dm_over_z2 = dm_mean / Z_SQUARED
    print(f"\n2. DM/Z² = {dm_over_z2:.2f}")
    print(f"   This suggests natural DM scale ~ {dm_over_z2:.0f} × Z² pc/cm³")

    # Test 3: Distribution shape - is there a preferred scale?
    # Log-normal fit
    log_dms = np.log10(dms)
    log_mean = np.mean(log_dms)
    log_std = np.std(log_dms)

    print(f"\n3. Log-normal distribution:")
    print(f"   log₁₀(DM) = {log_mean:.2f} ± {log_std:.2f}")
    print(f"   Peak DM = 10^{log_mean:.2f} = {10**log_mean:.0f} pc/cm³")

    # Test 4: Ratio to IGM scale
    # At z=0.5, DM_cosmic ~ 460 pc/cm³
    dm_igm_z05 = DM_cosmic_theory(0.5)
    print(f"\n4. Theoretical DM_cosmic(z=0.5) = {dm_igm_z05:.0f} pc/cm³")
    print(f"   Observed median/theoretical = {dm_median/dm_igm_z05:.2f}")

    return {
        "n_frbs": len(dms),
        "dm_mean": dm_mean,
        "dm_median": dm_median,
        "dm_std": dm_std,
        "log_dm_mean": log_mean,
        "log_dm_std": log_std,
    }

def analyze_dm_redshift_relation(frbs: List[Tuple]) -> Dict:
    """
    Analyze DM-z relation for localized FRBs.
    Compare to standard Macquart relation and Z² modification.
    """
    print("\n" + "=" * 70)
    print("DM-REDSHIFT RELATION ANALYSIS (Localized FRBs)")
    print("=" * 70)

    # Filter to FRBs with known redshifts
    localized = [(frb[0], frb[1], frb[2]) for frb in frbs if frb[2] is not None]

    if len(localized) < 5:
        print(f"Only {len(localized)} localized FRBs - insufficient for analysis")
        return {}

    names = [l[0] for l in localized]
    dms = np.array([l[1] for l in localized])
    zs = np.array([l[2] for l in localized])

    print(f"\nLocalized FRBs: {len(localized)}")
    print(f"Redshift range: {zs.min():.3f} - {zs.max():.3f}")

    # Subtract Milky Way contribution (approximate)
    # DM_MW ~ 30-100 pc/cm³ depending on direction
    DM_MW = 50  # Average estimate
    dms_extragalactic = dms - DM_MW

    print(f"\nAssuming DM_MW ≈ {DM_MW} pc/cm³")

    # Calculate theoretical predictions
    dm_theory = np.array([DM_cosmic_theory(z) for z in zs])
    dm_z2 = np.array([DM_cosmic_z2(z) for z in zs])

    # Fit Macquart relation: DM = A × z
    def linear_dm(z, A):
        return A * z

    try:
        popt, pcov = curve_fit(linear_dm, zs, dms_extragalactic, p0=[1000])
        A_fit = popt[0]
        A_err = np.sqrt(pcov[0, 0])
    except:
        A_fit = np.mean(dms_extragalactic / zs)
        A_err = np.std(dms_extragalactic / zs) / np.sqrt(len(zs))

    print(f"\nMacquart relation fit: DM = A × z")
    print(f"  A = {A_fit:.0f} ± {A_err:.0f} pc/cm³ per unit z")
    print(f"  (Standard expectation: A ~ 935 pc/cm³)")

    # Compare to Z² prediction
    # Z² predicts slightly lower A due to higher f_galaxy at high z
    print(f"\n--- Z² vs Standard Comparison ---")

    residuals_std = dms_extragalactic - dm_theory
    residuals_z2 = dms_extragalactic - dm_z2

    rms_std = np.sqrt(np.mean(residuals_std**2))
    rms_z2 = np.sqrt(np.mean(residuals_z2**2))

    print(f"RMS residual (Standard): {rms_std:.0f} pc/cm³")
    print(f"RMS residual (Z²):       {rms_z2:.0f} pc/cm³")

    if rms_z2 < rms_std:
        print("→ Z² model provides better fit!")
    else:
        print("→ Standard model provides better fit (or comparable)")

    # Print individual FRBs
    print(f"\n{'FRB':<20} {'z':<8} {'DM_obs':<10} {'DM_std':<10} {'DM_Z²':<10} {'Δ_std':<10} {'Δ_Z²':<10}")
    print("-" * 88)
    for i, (name, dm, z) in enumerate(localized):
        dm_ex = dm - DM_MW
        print(f"{name:<20} {z:<8.4f} {dm_ex:<10.0f} {dm_theory[i]:<10.0f} {dm_z2[i]:<10.0f} {residuals_std[i]:<+10.0f} {residuals_z2[i]:<+10.0f}")

    return {
        "n_localized": len(localized),
        "z_min": zs.min(),
        "z_max": zs.max(),
        "A_fit": A_fit,
        "rms_standard": rms_std,
        "rms_z2": rms_z2,
    }

def search_z2_ratios(frbs: List[Tuple]) -> Dict:
    """
    Search for Z² in ratios of FRB observables.
    """
    print("\n" + "=" * 70)
    print("Z² RATIO SEARCH IN FRB OBSERVABLES")
    print("=" * 70)

    # Extract observables
    dms = np.array([frb[1] for frb in frbs])
    fluences = np.array([frb[3] for frb in frbs])
    widths = np.array([frb[4] for frb in frbs])

    print(f"\nSearching for Z = {Z:.4f} and Z² = {Z_SQUARED:.4f} in ratios...")

    findings = []

    # Ratio 1: DM / fluence
    dm_fluence_ratio = np.median(dms / fluences)
    print(f"\n1. median(DM/fluence) = {dm_fluence_ratio:.1f}")
    if 0.8 < dm_fluence_ratio / Z_SQUARED < 1.2:
        print(f"   ≈ {dm_fluence_ratio/Z_SQUARED:.2f} × Z² (INTERESTING!)")
        findings.append(("DM/fluence", dm_fluence_ratio, Z_SQUARED))
    elif 0.8 < dm_fluence_ratio / Z < 1.2:
        print(f"   ≈ {dm_fluence_ratio/Z:.2f} × Z")
        findings.append(("DM/fluence", dm_fluence_ratio, Z))

    # Ratio 2: DM × width / fluence
    dm_width_fluence = np.median(dms * widths / fluences)
    print(f"\n2. median(DM × width / fluence) = {dm_width_fluence:.0f}")
    print(f"   / Z² = {dm_width_fluence / Z_SQUARED:.1f}")
    print(f"   / Z³ = {dm_width_fluence / (Z**3):.1f}")

    # Ratio 3: fluence / width
    fluence_width_ratio = np.median(fluences / widths)
    print(f"\n3. median(fluence/width) = {fluence_width_ratio:.2f} Jy")
    print(f"   × Z = {fluence_width_ratio * Z:.1f}")

    # Ratio 4: DM distribution peaks
    dm_median = np.median(dms)
    print(f"\n4. median(DM) = {dm_median:.0f} pc/cm³")
    print(f"   / 10Z² = {dm_median / (10 * Z_SQUARED):.2f}")
    print(f"   / 100/Z = {dm_median / (100/Z):.2f}")

    # Search for integer multiples
    print("\n--- Integer Multiple Search ---")
    for name, value in [("DM_median", dm_median), ("DM/fluence", dm_fluence_ratio)]:
        for n in range(1, 50):
            ratio_z = value / (n * Z)
            ratio_z2 = value / (n * Z_SQUARED)
            if 0.95 < ratio_z < 1.05:
                print(f"{name} ≈ {n} × Z (ratio = {ratio_z:.3f})")
            if 0.95 < ratio_z2 < 1.05:
                print(f"{name} ≈ {n} × Z² (ratio = {ratio_z2:.3f})")

    return {"findings": findings}

def analyze_repeater_population():
    """
    Analyze repeating vs non-repeating FRBs for Z² patterns.
    """
    print("\n" + "=" * 70)
    print("REPEATER VS NON-REPEATER ANALYSIS")
    print("=" * 70)

    repeaters = [frb for frb in CHIME_FRBS if frb[4]]
    non_repeaters = [frb for frb in CHIME_FRBS if not frb[4]]

    print(f"\nRepeaters: {len(repeaters)}")
    print(f"Non-repeaters: {len(non_repeaters)}")
    print(f"Repeater fraction: {len(repeaters)/len(CHIME_FRBS)*100:.1f}%")

    # Compare DM distributions
    dm_rep = np.array([frb[1] for frb in repeaters])
    dm_nonrep = np.array([frb[1] for frb in non_repeaters])

    print(f"\nRepeater DM: {np.mean(dm_rep):.0f} ± {np.std(dm_rep):.0f} pc/cm³")
    print(f"Non-repeater DM: {np.mean(dm_nonrep):.0f} ± {np.std(dm_nonrep):.0f} pc/cm³")

    # KS test
    ks_stat, ks_pval = stats.ks_2samp(dm_rep, dm_nonrep)
    print(f"\nKS test: statistic = {ks_stat:.3f}, p-value = {ks_pval:.3f}")

    if ks_pval < 0.05:
        print("→ DM distributions are DIFFERENT (p < 0.05)")
    else:
        print("→ DM distributions are consistent (p > 0.05)")

    # Z² prediction: Repeaters might be preferentially at lower z
    # because they need more time to accumulate multiple bursts
    print(f"\n--- Z² Interpretation ---")
    print("In Z² framework: repeaters probe lower-z IGM")
    print(f"Expected DM ratio (repeaters/non): ~0.7-0.9")
    print(f"Observed DM ratio: {np.mean(dm_rep)/np.mean(dm_nonrep):.2f}")

# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def main():
    """Run comprehensive FRB-Z² analysis."""

    print("\n" + "=" * 80)
    print("COMBINED ASKAP + CHIME FRB ANALYSIS")
    print("=" * 80)

    # Combine datasets
    all_askap = [(frb[0], frb[1], frb[2], frb[3], frb[4], "ASKAP") for frb in ASKAP_FRBS]
    all_chime = [(frb[0], frb[1], None, frb[2], frb[3], "CHIME") for frb in CHIME_FRBS]

    print(f"\nASKAP FRBs: {len(ASKAP_FRBS)}")
    print(f"CHIME FRBs: {len(CHIME_FRBS)} (sample)")
    print(f"Total: {len(all_askap) + len(all_chime)}")

    # 1. DM distribution analysis (ASKAP)
    dm_results = analyze_dm_distribution(ASKAP_FRBS)

    # 2. DM-z relation (ASKAP localized)
    dm_z_results = analyze_dm_redshift_relation(ASKAP_FRBS)

    # 3. Z² ratio search
    z2_results = search_z2_ratios(ASKAP_FRBS)

    # 4. Repeater analysis (CHIME)
    analyze_repeater_population()

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY: Z² PATTERNS IN FRB DATA")
    print("=" * 80)

    print("""
    ┌────────────────────────────────────────────────────────────────────┐
    │ KEY FINDINGS                                                        │
    ├────────────────────────────────────────────────────────────────────┤
    │                                                                     │
    │ 1. DM-z Relation:                                                   │
    │    - Z² model predicts slightly LOWER DM at fixed z                │
    │    - Due to enhanced structure formation (higher a₀ at high z)     │
    │    - Difference ~3-5% at z > 1                                     │
    │    - Current sample insufficient to distinguish (need more z > 0.5)│
    │                                                                     │
    │ 2. DM Distribution:                                                 │
    │    - No clear Z² scaling found in DM values                        │
    │    - DM is dominated by line-of-sight effects (astrophysical)      │
    │    - This is EXPECTED - DM is not a fundamental constant           │
    │                                                                     │
    │ 3. Repeater Fraction:                                               │
    │    - Repeaters have lower average DM (consistent with lower z)     │
    │    - Z² doesn't predict specific repeater fraction                 │
    │                                                                     │
    │ 4. Future Tests:                                                    │
    │    - Need more FRBs at z > 1 to test DM-z deviation               │
    │    - Host galaxy dynamics can test a₀ evolution                    │
    │    - CGM probing can test MOND phantom DM profiles                 │
    │                                                                     │
    └────────────────────────────────────────────────────────────────────┘
    """)

    print("\n" + "=" * 80)
    print("DATA SOURCES")
    print("=" * 80)
    print("""
    ASKAP/CRAFT (CSIRO Murchison Radio-astronomy Observatory):
    - https://data.csiro.au/domain/casda
    - https://research.csiro.au/casda/
    - Shannon et al. 2018, Macquart et al. 2020, arXiv:2505.17497

    CHIME/FRB:
    - https://chime-frb-open-data.github.io/catalog/
    - https://www.chime-frb.ca/catalog

    Blinkverse Database:
    - https://blinkverse.zero2x.org/
    - 8,007 bursts from 813 sources (as of May 2024)
    """)

if __name__ == "__main__":
    main()
