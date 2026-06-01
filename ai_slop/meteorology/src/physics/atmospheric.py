"""
Atmospheric Physics from First Principles

This module implements fundamental atmospheric thermodynamic relationships
derived from first principles of physics.

Key Relationships:
==================

1. IDEAL GAS LAW:
   p = ρRT

   where:
   - p: pressure [Pa]
   - ρ: density [kg/m³]
   - R: specific gas constant [J/(kg·K)]
   - T: temperature [K]

2. HYDROSTATIC BALANCE:
   ∂p/∂z = -ρg

   Combining with ideal gas:
   ∂p/p = -g/(RT) · dz
   → Barometric formula: p(z) = p₀ · exp(-gz/(RT))

3. POTENTIAL TEMPERATURE:
   θ = T · (p₀/p)^(R/c_p)

   The temperature a parcel would have if brought adiabatically
   to reference pressure p₀ = 1000 hPa.

   Key property: θ is conserved for adiabatic processes.

4. VIRTUAL TEMPERATURE:
   T_v = T · (1 + r/ε) / (1 + r)

   where r = q/(1-q) is mixing ratio, ε = R_d/R_v ≈ 0.622

   T_v is the temperature dry air would need to have the same
   density as moist air at temperature T.

5. CLAUSIUS-CLAPEYRON EQUATION:
   de_s/dT = L_v · e_s / (R_v · T²)

   Governs saturation vapor pressure as function of temperature.
   Integrated: e_s(T) ≈ 610.78 · exp(17.27·(T-273.15)/(T-35.86))
"""

import torch
import torch.nn.functional as F
from typing import Tuple, Optional
import numpy as np


# ============================================================================
# PHYSICAL CONSTANTS (SI units)
# ============================================================================

# Thermodynamic constants
R_DRY = 287.058       # Gas constant for dry air [J/(kg·K)]
R_VAPOR = 461.5       # Gas constant for water vapor [J/(kg·K)]
EPSILON = R_DRY / R_VAPOR  # ≈ 0.622, ratio of molecular weights

C_P_DRY = 1004.0      # Specific heat of dry air at constant pressure [J/(kg·K)]
C_V_DRY = 717.0       # Specific heat of dry air at constant volume [J/(kg·K)]
C_P_VAPOR = 1850.0    # Specific heat of water vapor [J/(kg·K)]

L_V = 2.501e6         # Latent heat of vaporization at 0°C [J/kg]
L_S = 2.834e6         # Latent heat of sublimation at 0°C [J/kg]
L_F = 0.334e6         # Latent heat of fusion [J/kg]

# Standard atmosphere
P_REFERENCE = 100000.0  # Reference pressure [Pa] (1000 hPa)
T_REFERENCE = 288.15    # Standard temperature at sea level [K]

# Gravitational acceleration
GRAVITY = 9.80665     # Standard gravity [m/s²]


# ============================================================================
# THERMODYNAMIC FUNCTIONS
# ============================================================================

def compute_potential_temperature(
    T: torch.Tensor,
    p: torch.Tensor,
    p_ref: float = P_REFERENCE,
) -> torch.Tensor:
    """
    Compute potential temperature θ.

    From first principles:
    For adiabatic process: T·p^(-R/c_p) = constant

    Therefore: θ = T · (p_ref/p)^(R/c_p)

    Physical interpretation:
    θ is the temperature a parcel would have if compressed/expanded
    adiabatically to reference pressure. It's conserved for adiabatic
    (reversible, no heat exchange) processes.

    θ is the fundamental variable for:
    - Determining static stability (∂θ/∂z > 0 → stable)
    - Tracking air mass origins
    - Potential vorticity calculations

    Args:
        T: Temperature [K]
        p: Pressure [Pa]
        p_ref: Reference pressure [Pa], default 100000 Pa (1000 hPa)

    Returns:
        Potential temperature θ [K]
    """
    kappa = R_DRY / C_P_DRY  # ≈ 0.286
    return T * (p_ref / p) ** kappa


def compute_temperature_from_theta(
    theta: torch.Tensor,
    p: torch.Tensor,
    p_ref: float = P_REFERENCE,
) -> torch.Tensor:
    """
    Compute temperature from potential temperature.

    Inverse of compute_potential_temperature:
    T = θ · (p/p_ref)^(R/c_p)
    """
    kappa = R_DRY / C_P_DRY
    return theta * (p / p_ref) ** kappa


def compute_virtual_temperature(
    T: torch.Tensor,
    q: torch.Tensor,
) -> torch.Tensor:
    """
    Compute virtual temperature T_v.

    From first principles:
    Moist air is less dense than dry air at the same T and p because
    water vapor (M=18) is lighter than N₂ (M=28) and O₂ (M=32).

    The ideal gas law for moist air:
    p = ρ·R_d·T_v

    where T_v is the temperature dry air would need to have the same
    density as the moist air.

    Derivation:
    T_v = T · (1 + r/ε) / (1 + r)
        ≈ T · (1 + 0.608·q)  for q << 1

    where:
    - r = q/(1-q) is the mixing ratio
    - ε = R_d/R_v ≈ 0.622
    - q is specific humidity

    Args:
        T: Temperature [K]
        q: Specific humidity [kg/kg]

    Returns:
        Virtual temperature T_v [K]
    """
    # Mixing ratio
    q_safe = torch.clamp(q, min=0, max=0.1)  # Physical bounds
    r = q_safe / (1 - q_safe)

    # Virtual temperature factor
    factor = (1 + r / EPSILON) / (1 + r)

    return T * factor


def compute_saturation_vapor_pressure(
    T: torch.Tensor,
    over_ice: bool = False,
) -> torch.Tensor:
    """
    Compute saturation vapor pressure e_s(T).

    From first principles (Clausius-Clapeyron equation):
    de_s/dT = L·e_s / (R_v·T²)

    Integrated assuming L is constant:
    e_s(T) = e_s(T_0) · exp(L/R_v · (1/T_0 - 1/T))

    In practice, we use empirical formulas that are more accurate
    because L varies with temperature.

    Tetens formula (for liquid water):
    e_s = 610.78 · exp(17.27·T_c / (T_c + 237.3))  [Pa]

    For ice (T < 273.15 K):
    e_s = 610.78 · exp(21.875·T_c / (T_c + 265.5))  [Pa]

    where T_c = T - 273.15 is temperature in Celsius.

    Args:
        T: Temperature [K]
        over_ice: If True, compute saturation over ice surface

    Returns:
        Saturation vapor pressure [Pa]
    """
    T_celsius = T - 273.15

    if over_ice:
        # Saturation over ice (valid for T < 0°C)
        e_s = 610.78 * torch.exp(21.875 * T_celsius / (T_celsius + 265.5))
    else:
        # Saturation over liquid water
        e_s = 610.78 * torch.exp(17.27 * T_celsius / (T_celsius + 237.3))

    return e_s


def compute_saturation_specific_humidity(
    T: torch.Tensor,
    p: torch.Tensor,
    over_ice: bool = False,
) -> torch.Tensor:
    """
    Compute saturation specific humidity q_s(T, p).

    From first principles:
    q_s = ε·e_s / (p - (1-ε)·e_s)

    where ε = R_d/R_v ≈ 0.622

    For p >> e_s (typical atmospheric conditions):
    q_s ≈ ε·e_s / p

    Args:
        T: Temperature [K]
        p: Pressure [Pa]
        over_ice: Compute saturation over ice

    Returns:
        Saturation specific humidity [kg/kg]
    """
    e_s = compute_saturation_vapor_pressure(T, over_ice=over_ice)

    # Ensure p > e_s to avoid negative denominator
    denominator = p - (1 - EPSILON) * e_s
    denominator = torch.clamp(denominator, min=100.0)  # Min 1 Pa

    q_s = EPSILON * e_s / denominator

    return q_s


def compute_relative_humidity(
    T: torch.Tensor,
    q: torch.Tensor,
    p: torch.Tensor,
) -> torch.Tensor:
    """
    Compute relative humidity RH = q/q_s.

    From first principles:
    Relative humidity is the ratio of actual water vapor content
    to the maximum possible at the given temperature.

    RH = e/e_s = q/q_s (approximately)

    where e is the actual vapor pressure and e_s is saturation.

    Args:
        T: Temperature [K]
        q: Specific humidity [kg/kg]
        p: Pressure [Pa]

    Returns:
        Relative humidity [0-1, can exceed 1 for supersaturation]
    """
    q_s = compute_saturation_specific_humidity(T, p)
    q_s = torch.clamp(q_s, min=1e-10)  # Avoid division by zero

    return q / q_s


def compute_geopotential_height(
    T_v: torch.Tensor,         # Virtual temperature profile (batch, lat, lon, levels)
    p_levels: torch.Tensor,    # Pressure levels [Pa] (levels,)
    z_surface: Optional[torch.Tensor] = None,  # Surface geopotential height [m]
) -> torch.Tensor:
    """
    Compute geopotential height from virtual temperature.

    From first principles (hypsometric equation):
    Integrating hydrostatic equation with ideal gas law:

    Φ₂ - Φ₁ = R_d · ∫[p₁ to p₂] T_v · d(ln p)

    Discretized (for layer between pressure levels p₁ and p₂):
    Z₂ - Z₁ = (R_d/g) · T̄_v · ln(p₁/p₂)

    where T̄_v is the mean virtual temperature in the layer.

    Args:
        T_v: Virtual temperature at each pressure level
        p_levels: Pressure levels (from surface to top, decreasing)
        z_surface: Surface geopotential height (optional)

    Returns:
        Geopotential height at each level [m]
    """
    n_levels = len(p_levels)
    batch_shape = T_v.shape[:-1]

    # Initialize
    if z_surface is None:
        z_surface = torch.zeros(batch_shape, device=T_v.device, dtype=T_v.dtype)

    z = torch.zeros_like(T_v)

    # Assume levels are ordered from surface (highest p) to top (lowest p)
    z[..., 0] = z_surface

    # Integrate upward
    for k in range(1, n_levels):
        # Mean virtual temperature in layer
        T_v_mean = 0.5 * (T_v[..., k-1] + T_v[..., k])

        # Pressure ratio
        p_ratio = p_levels[k-1] / p_levels[k]

        # Thickness
        dz = (R_DRY / GRAVITY) * T_v_mean * torch.log(p_ratio)

        z[..., k] = z[..., k-1] + dz

    return z


def compute_density(
    T: torch.Tensor,
    p: torch.Tensor,
    q: Optional[torch.Tensor] = None,
) -> torch.Tensor:
    """
    Compute air density from temperature and pressure.

    From first principles (ideal gas law):
    ρ = p / (R·T)

    For moist air, use virtual temperature:
    ρ = p / (R_d·T_v)

    Args:
        T: Temperature [K]
        p: Pressure [Pa]
        q: Specific humidity [kg/kg] (optional, for moist air)

    Returns:
        Density [kg/m³]
    """
    if q is not None:
        T_v = compute_virtual_temperature(T, q)
    else:
        T_v = T

    return p / (R_DRY * T_v)


def compute_brunt_vaisala_frequency(
    theta: torch.Tensor,
    z: torch.Tensor,
) -> torch.Tensor:
    """
    Compute Brunt-Väisälä (buoyancy) frequency N².

    From first principles:
    For a displaced parcel in a stratified atmosphere:
    N² = (g/θ) · ∂θ/∂z

    Physical interpretation:
    - N² > 0: Stable stratification (oscillation frequency N)
    - N² = 0: Neutral stratification
    - N² < 0: Unstable (convection onset)

    Typical values: N ≈ 0.01 s⁻¹ (period ~10 minutes)

    Args:
        theta: Potential temperature (batch, lat, lon, levels)
        z: Geopotential height (batch, lat, lon, levels)

    Returns:
        N² [s⁻²]
    """
    # ∂θ/∂z using central differences
    dtheta = torch.diff(theta, dim=-1)
    dz = torch.diff(z, dim=-1)

    # Avoid division by zero
    dz = torch.clamp(torch.abs(dz), min=10.0) * torch.sign(dz + 1e-10)

    dtheta_dz = dtheta / dz

    # Mean theta in each layer
    theta_mean = 0.5 * (theta[..., :-1] + theta[..., 1:])

    N_squared = (GRAVITY / theta_mean) * dtheta_dz

    return N_squared


def compute_moist_adiabatic_lapse_rate(
    T: torch.Tensor,
    p: torch.Tensor,
) -> torch.Tensor:
    """
    Compute moist (saturated) adiabatic lapse rate.

    From first principles:
    For saturated air, latent heat release during condensation
    reduces the cooling rate during ascent.

    Γ_m = Γ_d · [1 + L_v·r_s/(R_d·T)] / [1 + L_v²·r_s/(c_p·R_v·T²)]

    where:
    - Γ_d = g/c_p ≈ 9.8 K/km (dry adiabatic lapse rate)
    - r_s is saturation mixing ratio

    Typical values: Γ_m ≈ 6 K/km (varies with T and p)

    Args:
        T: Temperature [K]
        p: Pressure [Pa]

    Returns:
        Moist adiabatic lapse rate [K/m]
    """
    # Dry adiabatic lapse rate
    gamma_dry = GRAVITY / C_P_DRY

    # Saturation specific humidity
    q_s = compute_saturation_specific_humidity(T, p)

    # Saturation mixing ratio
    r_s = q_s / (1 - q_s)

    # Numerator and denominator factors
    numerator = 1 + L_V * r_s / (R_DRY * T)
    denominator = 1 + L_V**2 * r_s / (C_P_DRY * R_VAPOR * T**2)

    gamma_moist = gamma_dry * numerator / denominator

    return gamma_moist
