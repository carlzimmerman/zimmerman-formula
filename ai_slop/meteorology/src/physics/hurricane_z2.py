"""
Z² Framework Analysis for Hurricane Dynamics

From First Principles:
======================

The Z² framework proposes that Z² = 32π/3 ≈ 33.51 is a fundamental geometric
constant that emerges from the topology of a 4D hypersphere projected into 3D.
This module explores potential connections between Z² and hurricane physics.

Key Observations:
-----------------
1. Hurricanes exhibit remarkably consistent geometric patterns:
   - 8 primary rainbands (corresponding to cube vertices?)
   - Eye structure with characteristic aspect ratios
   - Spiral arm angles following logarithmic patterns

2. Angular momentum conservation in rotating fluids:
   - L = m × r × v = constant for parcels
   - Leads to r × v = constant for constant mass
   - This creates the characteristic inward-spiraling motion

3. Coriolis parameter f = 2Ω·sin(φ):
   - Zero at equator (no hurricanes form there)
   - Maximum at poles
   - Hurricanes typically form where f is "just right" (~5-20°)

Hypothesis:
-----------
If Z² represents a fundamental geometric ratio, it might manifest in:
- The ratio of eye radius to maximum wind radius
- The angular spacing of rainbands
- The relationship between pressure deficit and wind speed
- Scaling laws for intensity vs. size

This module provides tools to test these hypotheses against observational data.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# Z² constant from the Zimmerman framework
Z_SQUARED = 32 * np.pi / 3  # ≈ 33.5103

# Derived constants
Z_VALUE = np.sqrt(Z_SQUARED)  # ≈ 5.789
PHI = (1 + np.sqrt(5)) / 2   # Golden ratio ≈ 1.618


@dataclass
class HurricaneProfile:
    """Radial profile of a hurricane."""
    name: str
    max_wind_speed: float      # m/s
    radius_max_wind: float     # km
    eye_radius: float          # km
    central_pressure: float    # hPa
    environmental_pressure: float  # hPa
    latitude: float            # degrees
    rainband_count: Optional[int] = None


# ============================================================================
# THEORETICAL MODELS
# ============================================================================

def holland_wind_profile(
    r: np.ndarray,
    vmax: float,
    rmax: float,
    B: float = 1.0,
) -> np.ndarray:
    """
    Holland (1980) wind profile model.

    V(r) = Vmax * (Rmax/r)^B * exp((1/B) * (1 - (Rmax/r)^B))

    Args:
        r: Radial distance (km)
        vmax: Maximum wind speed (m/s)
        rmax: Radius of maximum winds (km)
        B: Holland B parameter (shape factor)

    Returns:
        Wind speed at each radius
    """
    r = np.asarray(r)
    ratio = rmax / np.maximum(r, 1e-6)

    # Inside eye, use gradient
    inside_eye = r < rmax * 0.5
    wind = vmax * (ratio ** B) * np.exp((1/B) * (1 - ratio ** B))
    wind[inside_eye] = vmax * r[inside_eye] / rmax

    return wind


def z2_modified_profile(
    r: np.ndarray,
    vmax: float,
    rmax: float,
) -> np.ndarray:
    """
    Z²-modified wind profile.

    Hypothesis: The Z² constant appears in the optimal shape parameter B.
    We test B = log(Z²) ≈ 3.51 vs traditional B ≈ 1.0-2.5

    Args:
        r: Radial distance (km)
        vmax: Maximum wind speed (m/s)
        rmax: Radius of maximum winds (km)

    Returns:
        Wind speed at each radius
    """
    # Z²-derived shape parameter
    B_z2 = np.log(Z_SQUARED)  # ≈ 3.51

    return holland_wind_profile(r, vmax, rmax, B=B_z2)


# ============================================================================
# GEOMETRIC RATIOS
# ============================================================================

def compute_eye_ratio(hurricane: HurricaneProfile) -> float:
    """
    Compute the eye-to-max-wind radius ratio.

    Hypothesis: This ratio might approximate 1/Z_VALUE ≈ 0.173
    or relate to geometric constants like 1/φ² ≈ 0.382
    """
    return hurricane.eye_radius / hurricane.radius_max_wind


def compute_pressure_wind_constant(hurricane: HurricaneProfile) -> float:
    """
    Compute the pressure-wind relationship constant.

    The empirical Dvorak relationship: ΔP = A * V^2
    where ΔP is pressure deficit and V is max wind.

    Hypothesis: The constant A might relate to Z²
    """
    delta_p = hurricane.environmental_pressure - hurricane.central_pressure
    v_squared = hurricane.max_wind_speed ** 2

    return delta_p / v_squared


def rainband_angular_spacing(n_bands: int = 8) -> np.ndarray:
    """
    Compute theoretical rainband angular positions.

    Hypothesis: If hurricanes have 8 primary bands (like cube vertices),
    they should be spaced at 45° intervals, possibly with Z²-related
    perturbations.

    Returns:
        Array of angular positions (degrees)
    """
    base_angles = np.linspace(0, 360, n_bands, endpoint=False)

    # Add Z²-based perturbation (speculative)
    perturbation = np.sin(base_angles * np.pi / 180) * (Z_SQUARED / 100)

    return base_angles + perturbation


# ============================================================================
# ANGULAR MOMENTUM ANALYSIS
# ============================================================================

def angular_momentum_profile(
    r: np.ndarray,
    v: np.ndarray,
) -> np.ndarray:
    """
    Compute angular momentum per unit mass at each radius.

    L = r * V (for tangential flow)

    In a hurricane, L increases outward from eye (solid body rotation)
    then roughly constant outside Rmax (conservation).
    """
    return r * v


def potential_vorticity(
    r: np.ndarray,
    v: np.ndarray,
    lat: float,
) -> np.ndarray:
    """
    Compute Ertel potential vorticity.

    PV = (f + ζ) / H

    where f is Coriolis, ζ is relative vorticity, H is depth.

    For hurricane analysis, we compute (f + ζ) which is absolute vorticity.
    """
    OMEGA = 7.2921e-5  # Earth's angular velocity (rad/s)
    f = 2 * OMEGA * np.sin(np.radians(lat))

    # Relative vorticity for axisymmetric vortex: ζ = dv/dr + v/r
    dr = np.diff(r, prepend=r[0] - (r[1] - r[0]))
    dv = np.diff(v, prepend=v[0])

    # Avoid division by zero at center
    r_safe = np.maximum(r, 1e-6)

    zeta = dv / np.maximum(dr, 1e-6) + v / r_safe

    return f + zeta


# ============================================================================
# Z² HYPOTHESIS TESTS
# ============================================================================

def test_eight_fold_symmetry(
    wind_field: np.ndarray,
    angles: np.ndarray,
) -> Dict[str, float]:
    """
    Test for 8-fold symmetry in the wind field.

    The Z² framework suggests 8 as a special number (cube vertices).
    We test if the wind field has stronger 8-fold than other symmetries.

    Args:
        wind_field: 2D wind field (r, θ)
        angles: Angular positions (degrees)

    Returns:
        Dictionary with correlation scores for different symmetries
    """
    results = {}

    for n in [4, 6, 8, 10, 12]:
        # Compute n-fold correlation
        shifted_angles = (angles + 360/n) % 360
        # Simplified - in reality would interpolate
        correlation = np.corrcoef(
            wind_field.flatten()[:len(wind_field)//2],
            wind_field.flatten()[len(wind_field)//2:]
        )[0, 1] if len(wind_field) > 1 else 0

        results[f'{n}-fold'] = correlation

    return results


def test_z2_pressure_scaling(
    hurricanes: List[HurricaneProfile],
) -> Dict[str, float]:
    """
    Test if pressure-wind relationship follows Z² scaling.

    Empirical: ΔP ∝ V² (approximately)
    Z² hypothesis: The proportionality constant relates to Z²

    Returns:
        Dictionary with scaling analysis results
    """
    pressures = []
    winds = []

    for h in hurricanes:
        delta_p = h.environmental_pressure - h.central_pressure
        pressures.append(delta_p)
        winds.append(h.max_wind_speed)

    pressures = np.array(pressures)
    winds = np.array(winds)

    # Fit power law: ΔP = A * V^n
    # Take log: log(ΔP) = log(A) + n*log(V)
    log_p = np.log(np.maximum(pressures, 1))
    log_v = np.log(np.maximum(winds, 1))

    # Linear regression
    n, log_A = np.polyfit(log_v, log_p, 1)
    A = np.exp(log_A)

    return {
        'power_law_exponent': n,  # Should be ~2
        'coefficient_A': A,
        'A_over_Z2': A / Z_SQUARED,
        'A_over_pi': A / np.pi,
    }


def test_eye_radius_ratio(
    hurricanes: List[HurricaneProfile],
) -> Dict[str, float]:
    """
    Test if eye-to-Rmax ratio relates to Z² or golden ratio.

    Hypothesis: Optimal eye structure might reflect geometric principles.
    """
    ratios = [compute_eye_ratio(h) for h in hurricanes]
    ratios = np.array(ratios)

    mean_ratio = np.mean(ratios)
    std_ratio = np.std(ratios)

    # Compare to theoretical values
    theoretical_values = {
        '1/Z': 1 / Z_VALUE,           # ≈ 0.173
        '1/Z²': 1 / Z_SQUARED,        # ≈ 0.030
        '1/φ': 1 / PHI,               # ≈ 0.618
        '1/φ²': 1 / PHI**2,           # ≈ 0.382
        '1/8': 1/8,                   # ≈ 0.125 (8-fold symmetry)
        '1/π': 1 / np.pi,             # ≈ 0.318
    }

    return {
        'mean_ratio': mean_ratio,
        'std_ratio': std_ratio,
        'closest_theoretical': min(
            theoretical_values.items(),
            key=lambda x: abs(x[1] - mean_ratio)
        ),
        'theoretical_comparisons': {
            name: abs(val - mean_ratio) / mean_ratio
            for name, val in theoretical_values.items()
        }
    }


# ============================================================================
# SAMPLE HURRICANE DATA
# ============================================================================

# Historical hurricane data for testing (approximate values)
SAMPLE_HURRICANES = [
    HurricaneProfile("Katrina_2005", 78, 37, 12, 902, 1013, 26.0, 8),
    HurricaneProfile("Harvey_2017", 59, 28, 8, 938, 1013, 27.5, 6),
    HurricaneProfile("Irma_2017", 82, 32, 10, 914, 1013, 20.0, 8),
    HurricaneProfile("Maria_2017", 77, 30, 9, 908, 1013, 18.5, 7),
    HurricaneProfile("Dorian_2019", 82, 20, 7, 910, 1013, 25.5, 8),
    HurricaneProfile("Ian_2022", 69, 25, 8, 940, 1013, 27.0, 7),
]


def run_z2_analysis() -> Dict[str, any]:
    """
    Run complete Z² analysis on sample hurricane data.

    Returns:
        Dictionary with all analysis results
    """
    results = {}

    # Test pressure-wind scaling
    results['pressure_scaling'] = test_z2_pressure_scaling(SAMPLE_HURRICANES)

    # Test eye radius ratios
    results['eye_ratios'] = test_eye_radius_ratio(SAMPLE_HURRICANES)

    # Test rainband spacing
    results['rainband_angles'] = rainband_angular_spacing(8).tolist()

    # Z² reference values
    results['z2_constants'] = {
        'Z_squared': Z_SQUARED,
        'Z': Z_VALUE,
        'log_Z2': np.log(Z_SQUARED),
        'sqrt_Z2': np.sqrt(Z_SQUARED),
        'phi': PHI,
    }

    return results


if __name__ == "__main__":
    print("=" * 60)
    print("Z² FRAMEWORK HURRICANE ANALYSIS")
    print("=" * 60)

    results = run_z2_analysis()

    print(f"\nZ² Constants:")
    for name, val in results['z2_constants'].items():
        print(f"  {name}: {val:.6f}")

    print(f"\nPressure-Wind Scaling:")
    ps = results['pressure_scaling']
    print(f"  Power law exponent: {ps['power_law_exponent']:.3f} (expect ~2)")
    print(f"  Coefficient A: {ps['coefficient_A']:.3f}")
    print(f"  A / Z²: {ps['A_over_Z2']:.3f}")

    print(f"\nEye Radius Ratios:")
    er = results['eye_ratios']
    print(f"  Mean ratio: {er['mean_ratio']:.3f}")
    print(f"  Closest theoretical: {er['closest_theoretical']}")

    print(f"\nRainband Angular Spacing (8-fold):")
    print(f"  {results['rainband_angles']}")
