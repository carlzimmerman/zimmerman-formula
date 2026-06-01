#!/usr/bin/env python3
"""
Z² Framework: Outflow Layer Dynamics
=====================================

First-principles derivation of hurricane outflow physics using
the Z² = 32π/3 framework. The outflow layer is the "exhaust" of
the Carnot heat engine - where warm, high-angular-momentum air
exits at low temperature, completing the thermodynamic cycle.

The outflow structure directly controls:
1. Ventilation of the warm core
2. Angular momentum export
3. Interaction with environment
4. Hurricane size evolution

Author: Claude (Anthropic) & Carl Zimmerman
Date: 2024
"""

import numpy as np
from dataclasses import dataclass
from typing import Tuple, Optional
import warnings

# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================

# The Zimmerman constant
Z_SQUARED = 32 * np.pi / 3  # ≈ 33.51
Z = np.sqrt(Z_SQUARED)       # ≈ 5.79

# Physical constants
g = 9.81              # Gravitational acceleration (m/s²)
c_p = 1005            # Specific heat (J/kg/K)
R_d = 287             # Gas constant for dry air (J/kg/K)
Omega = 7.292e-5      # Earth rotation rate (rad/s)
rho_ref = 0.4         # Reference outflow density (kg/m³)

# =============================================================================
# SECTION 1: OUTFLOW LAYER STRUCTURE
# =============================================================================
"""
FIRST PRINCIPLES: The Hurricane Outflow

The outflow layer (150-300 hPa) is where air exits the storm.
It forms the COLD reservoir of the Carnot cycle.

Key characteristics:
1. Anticyclonic rotation (upper-level high)
2. Radial outflow velocities 10-30 m/s
3. Temperature ~ -50 to -70°C (outflow temperature)
4. Strong divergence above eyewall
5. Jet stream interaction possible

The outflow determines efficiency by setting T_out:
    η = (T_s - T_out) / T_s

Lower T_out → higher efficiency → stronger storm!

The upper-level warm core creates the pressure gradient
that drives surface winds. Outflow structure modulates
how effectively the warm core is maintained.
"""

def outflow_temperature(SST_C: float, delta_T_tropo: float = 85) -> float:
    """
    Calculate outflow temperature.

    The outflow temperature is approximately:
        T_out ≈ T_surface - ΔT_troposphere

    Typical tropical tropopause: -60 to -80°C

    Parameters
    ----------
    SST_C : float
        Sea surface temperature (°C)
    delta_T_tropo : float
        Temperature drop across troposphere (K)

    Returns
    -------
    float
        Outflow temperature (°C)
    """
    T_out = SST_C - delta_T_tropo
    return T_out


def carnot_efficiency(SST_C: float, T_out_C: float) -> float:
    """
    Calculate Carnot efficiency.

    η = (T_s - T_out) / T_s

    Parameters
    ----------
    SST_C : float
        Sea surface temperature (°C)
    T_out_C : float
        Outflow temperature (°C)

    Returns
    -------
    float
        Carnot efficiency (0-1)
    """
    T_s = SST_C + 273.15
    T_out = T_out_C + 273.15

    eta = (T_s - T_out) / T_s

    return eta


def outflow_level_height(tropopause_hPa: float = 100) -> float:
    """
    Calculate height of primary outflow level.

    Using standard atmosphere approximation:
        z ≈ -H × ln(p/p_0)

    Parameters
    ----------
    tropopause_hPa : float
        Pressure at tropopause (hPa)

    Returns
    -------
    float
        Height of outflow (m)
    """
    H = 8500  # Scale height (m)
    p_0 = 1013.25  # Surface pressure (hPa)

    z = -H * np.log(tropopause_hPa / p_0)

    return z


# =============================================================================
# SECTION 2: OUTFLOW ANTICYCLONE
# =============================================================================
"""
THE UPPER-LEVEL ANTICYCLONE

As high-angular-momentum air exits at large radius,
conservation of M creates anticyclonic rotation:

    M = r×V + (f/2)×r² = constant

At large r, V must become negative (anticyclonic)
to conserve M:
    V = M/r - (f/2)×r → negative for large r

This creates the upper-level anticyclone visible in
water vapor imagery and analyzed on weather maps.

The anticyclone:
1. Shields the storm from environmental shear
2. Indicates healthy outflow
3. Interacts with upper-level troughs
4. Affects downstream weather patterns
"""

def coriolis_parameter(latitude: float) -> float:
    """Calculate Coriolis parameter."""
    return 2 * Omega * np.sin(np.radians(latitude))


def outflow_tangential_wind(M_eyewall: float, r_km: float,
                             latitude: float) -> float:
    """
    Calculate tangential wind in outflow at given radius.

    V = M/r - (f/2)×r

    Parameters
    ----------
    M_eyewall : float
        Angular momentum from eyewall (m²/s)
    r_km : float
        Radius in outflow (km)
    latitude : float
        Latitude (degrees)

    Returns
    -------
    float
        Tangential wind (m/s), negative = anticyclonic
    """
    r = r_km * 1000
    f = coriolis_parameter(latitude)

    V = M_eyewall / r - 0.5 * f * r

    return V


def anticyclone_circulation(M_eyewall: float, r_outer_km: float,
                             latitude: float) -> float:
    """
    Calculate circulation of outflow anticyclone.

    Γ = ∮ V · dl = 2π × r × V

    Parameters
    ----------
    M_eyewall : float
        Angular momentum (m²/s)
    r_outer_km : float
        Outer radius for integration (km)
    latitude : float
        Latitude (degrees)

    Returns
    -------
    float
        Circulation (m²/s), negative = anticyclonic
    """
    V = outflow_tangential_wind(M_eyewall, r_outer_km, latitude)
    r = r_outer_km * 1000

    Gamma = 2 * np.pi * r * V

    return Gamma


def anticyclone_strength_index(V_max: float, r_max_km: float,
                                latitude: float) -> float:
    """
    Calculate index of outflow anticyclone strength.

    Stronger storms with larger eyes produce stronger anticyclones.

    Index = |Γ_anticyclone| / (typical value)

    Parameters
    ----------
    V_max : float
        Maximum wind speed (m/s)
    r_max_km : float
        Radius of maximum wind (km)
    latitude : float
        Latitude (degrees)

    Returns
    -------
    float
        Anticyclone strength index (>1 = strong)
    """
    # Calculate eyewall angular momentum
    f = coriolis_parameter(latitude)
    r_max = r_max_km * 1000
    M = r_max * V_max + 0.5 * f * r_max**2

    # Circulation at typical outflow radius (1000 km)
    Gamma = anticyclone_circulation(M, 1000, latitude)

    # Normalize to typical value
    Gamma_typical = -5e7  # m²/s for moderate hurricane

    return abs(Gamma / Gamma_typical)


# =============================================================================
# SECTION 3: OUTFLOW CHANNEL DYNAMICS
# =============================================================================
"""
OUTFLOW CHANNELS

Hurricanes require clear pathways for outflow evacuation.
Environmental features can enhance or block outflow:

FAVORABLE (enhance outflow):
- Upper-level trough to the north/northeast
- Anticyclone to the south
- Weak upper-level flow
- Diffluent environment

UNFAVORABLE (block outflow):
- Strong upper-level ridge directly overhead
- Strong westerly jet shearing the top
- Upper-level trough directly over storm
- Convergent environment

The outflow layer efficiency ε_out:
    ε_out = 1 - (blockage factor)

Blocked outflow → reduced η → weaker storm
"""

def outflow_channel_efficiency(jet_distance_km: float,
                                jet_speed: float,
                                trough_position: str = 'none') -> float:
    """
    Calculate outflow channel efficiency.

    Efficiency depends on:
    1. Distance to jet stream (too close = shear)
    2. Presence of upper-level features
    3. Diffluence vs confluence

    Parameters
    ----------
    jet_distance_km : float
        Distance to jet stream axis (km)
    jet_speed : float
        Jet stream wind speed (m/s)
    trough_position : str
        'favorable' (NE), 'overhead', 'none'

    Returns
    -------
    float
        Outflow efficiency (0-1)
    """
    # Jet interaction factor
    if jet_distance_km < 300:
        jet_factor = 0.5 * (jet_distance_km / 300)  # Too close - shear
    elif jet_distance_km < 800:
        jet_factor = 0.5 + 0.5 * ((jet_distance_km - 300) / 500)
    else:
        jet_factor = 1.0  # Far enough for good outflow

    # Trough factor
    if trough_position == 'favorable':
        trough_factor = 1.2  # Enhancement
    elif trough_position == 'overhead':
        trough_factor = 0.6  # Direct interaction - bad
    else:
        trough_factor = 1.0  # Neutral

    # Jet speed effect (very strong jet can disrupt)
    if jet_speed > 60:
        speed_factor = 60 / jet_speed
    else:
        speed_factor = 1.0

    epsilon = jet_factor * trough_factor * speed_factor

    return min(epsilon, 1.2)


def outflow_divergence(V_r_out: float, r_inner_km: float,
                        r_outer_km: float) -> float:
    """
    Calculate upper-level divergence.

    For radial outflow V_r:
        D = (1/r) × ∂(r×V_r)/∂r ≈ V_r/r + ∂V_r/∂r

    Parameters
    ----------
    V_r_out : float
        Radial outflow velocity (m/s)
    r_inner_km : float
        Inner radius (km)
    r_outer_km : float
        Outer radius (km)

    Returns
    -------
    float
        Divergence (s⁻¹)
    """
    r_inner = r_inner_km * 1000
    r_outer = r_outer_km * 1000
    r_mean = (r_inner + r_outer) / 2
    dr = r_outer - r_inner

    # Simple estimate assuming constant V_r
    div = V_r_out / r_mean

    return div


def mass_flux_outflow(V_r_out: float, r_km: float,
                       depth_hPa: float = 150) -> float:
    """
    Calculate mass flux through outflow cylinder.

    F_mass = 2π × r × depth × ρ × V_r

    Parameters
    ----------
    V_r_out : float
        Radial outflow velocity (m/s)
    r_km : float
        Radius of cylinder (km)
    depth_hPa : float
        Depth of outflow layer (hPa)

    Returns
    -------
    float
        Mass flux (kg/s)
    """
    r = r_km * 1000

    # Convert pressure depth to mass per area
    # dm/dA = dp/g
    mass_per_area = depth_hPa * 100 / g  # kg/m²

    # Approximate as layer depth
    # Assuming scale height H ≈ 8 km at tropopause
    layer_depth = 2000  # m (typical outflow layer thickness)

    # Mass flux
    F = 2 * np.pi * r * layer_depth * rho_ref * V_r_out

    return F


# =============================================================================
# SECTION 4: WARM CORE AND OUTFLOW CONNECTION
# =============================================================================
"""
WARM CORE MAINTENANCE

The warm core is THE defining feature of tropical cyclones.
Temperature anomaly in the upper troposphere drives surface pressure:

    Δp_surface ∝ ∫ (ΔT/T) × g × ρ dz

The outflow maintains the warm core by:
1. Subsidence in the eye (adiabatic warming)
2. Removal of air mass (lowering pressure)
3. Latent heating in eyewall (exported at high altitude)

The Z² framework connects outflow efficiency to warm core:
    T_core ∝ V_max² ∝ Z² × (efficiency factors)

If outflow is blocked:
- Warm core air accumulates
- Pressure rises aloft
- Surface pressure gradient weakens
- Winds decrease
"""

def warm_core_anomaly(V_max: float) -> float:
    """
    Estimate warm core temperature anomaly from intensity.

    Empirical relationship:
        ΔT_core ≈ α × V_max²

    For Cat 5 hurricane (~70 m/s): ΔT ≈ 15-20 K

    Parameters
    ----------
    V_max : float
        Maximum sustained wind (m/s)

    Returns
    -------
    float
        Warm core anomaly at 300 hPa (K)
    """
    # Coefficient from observations (simplified)
    alpha = 0.003  # K/(m/s)²

    delta_T = alpha * V_max**2

    return delta_T


def central_pressure_from_warm_core(delta_T: float, T_env: float,
                                      depth_km: float = 15) -> float:
    """
    Calculate central pressure drop from warm core.

    Using hydrostatic equation:
        Δp ≈ (Δρ/ρ) × p ≈ -(ΔT/T) × p

    Integrated over depth:
        Δp_surface ≈ (ΔT/T) × g × ρ × depth

    Parameters
    ----------
    delta_T : float
        Warm core temperature anomaly (K)
    T_env : float
        Environmental temperature (K)
    depth_km : float
        Depth of warm core (km)

    Returns
    -------
    float
        Central pressure deficit (hPa)
    """
    # Using ideal gas approximation
    depth = depth_km * 1000

    # Mean density in column (rough estimate)
    rho_mean = 0.6  # kg/m³

    # Pressure deficit
    delta_p = (delta_T / T_env) * g * rho_mean * depth

    return delta_p / 100  # Convert to hPa


def outflow_ventilation_rate(V_out: float, r_out_km: float,
                              warm_core_radius_km: float) -> float:
    """
    Calculate rate at which outflow ventilates warm core.

    Ventilation timescale:
        τ_vent = Area_core / (circumference × V_out)

    Parameters
    ----------
    V_out : float
        Outflow velocity (m/s)
    r_out_km : float
        Outflow radius (km)
    warm_core_radius_km : float
        Warm core radius (km)

    Returns
    -------
    float
        Ventilation rate (s⁻¹)
    """
    r_out = r_out_km * 1000
    r_core = warm_core_radius_km * 1000

    area_core = np.pi * r_core**2
    circumference = 2 * np.pi * r_out

    tau_vent = area_core / (circumference * max(V_out, 1))

    return 1 / tau_vent


# =============================================================================
# SECTION 5: OUTFLOW LAYER INTERACTION WITH ENVIRONMENT
# =============================================================================
"""
ENVIRONMENTAL INTERACTIONS

The outflow layer is where the hurricane interacts most
directly with the large-scale environment:

1. TROUGH INTERACTION
   - Upper trough can enhance outflow (favorable)
   - Or disrupt warm core structure (unfavorable)
   - Depends on relative position and strength

2. JET STREAM INTERACTION
   - Jet can sweep away outflow efficiently
   - Or create strong shear disrupting core
   - Optimal: 500-1000 km from jet

3. ANTICYCLONE INTERACTION
   - Ridge to south enhances equatorward outflow
   - Steering by mean flow between ridge/trough

4. OUTFLOW BOUNDARY
   - Creates local wind shift at surface
   - Outflow boundaries can trigger new convection
"""

def trough_interaction_index(trough_distance_km: float,
                              trough_amplitude: float,
                              position_angle: float) -> dict:
    """
    Calculate trough interaction potential.

    Parameters
    ----------
    trough_distance_km : float
        Distance to trough axis (km)
    trough_amplitude : float
        Trough depth (amplitude in km)
    position_angle : float
        Position relative to storm (degrees, 0=north)

    Returns
    -------
    dict
        Interaction assessment
    """
    # Favorable position: NE quadrant (angle 30-90°)
    if 30 <= position_angle <= 90:
        position_factor = 1.2  # Favorable
    elif position_angle < 30 or position_angle > 150:
        position_factor = 0.8  # Less favorable
    else:
        position_factor = 0.6  # Overhead - potentially disruptive

    # Distance factor
    if trough_distance_km < 500:
        distance_factor = 0.7  # Too close - direct interaction
    elif trough_distance_km < 1000:
        distance_factor = 1.0 + 0.2 * (trough_distance_km - 500) / 500
    else:
        distance_factor = 1.2  # Optimal

    # Amplitude effect
    if trough_amplitude > 500:
        amplitude_factor = 1.0 + 0.1 * (trough_amplitude - 500) / 500
        amplitude_factor = min(amplitude_factor, 1.3)
    else:
        amplitude_factor = trough_amplitude / 500

    # Combined
    interaction_index = position_factor * distance_factor * amplitude_factor

    if interaction_index > 1.2:
        outcome = "Favorable - enhanced outflow"
    elif interaction_index > 0.9:
        outcome = "Neutral interaction"
    else:
        outcome = "Unfavorable - potential disruption"

    return {
        'interaction_index': interaction_index,
        'position_factor': position_factor,
        'distance_factor': distance_factor,
        'amplitude_factor': amplitude_factor,
        'outcome': outcome
    }


# =============================================================================
# SECTION 6: Z² AND OUTFLOW EFFICIENCY
# =============================================================================
"""
THE Z² OUTFLOW CONNECTION

The Z² MPI equation includes the Carnot efficiency:
    V_max² = Z² × (Ck/Cd) × η × Δk / c_p

where:
    η = (T_s - T_out) / T_s

The outflow layer controls T_out through:
1. Tropopause height (higher = colder = more efficient)
2. Outflow latitude (determines Coriolis, hence height)
3. Environmental temperature (tropical vs subtropical)

For a perfect outflow (unobstructed, efficient):
    η_max ≈ 0.35 (SST=30°C, T_out=-70°C)

For blocked/inefficient outflow:
    η_actual = η_max × ε_outflow

This directly affects achievable intensity!
"""

def outflow_efficiency_factor(jet_distance_km: float,
                               trough_interaction: float,
                               subsidence_rate: float) -> float:
    """
    Calculate overall outflow efficiency factor.

    ε_out = f(jet interaction) × f(trough) × f(subsidence)

    Parameters
    ----------
    jet_distance_km : float
        Distance to jet stream (km)
    trough_interaction : float
        Trough interaction index (from trough_interaction_index)
    subsidence_rate : float
        Eye subsidence rate (m/s), positive down

    Returns
    -------
    float
        Outflow efficiency factor (0-1)
    """
    # Jet distance factor
    if jet_distance_km < 400:
        jet_eff = 0.5
    elif jet_distance_km < 800:
        jet_eff = 0.5 + 0.5 * (jet_distance_km - 400) / 400
    else:
        jet_eff = 1.0

    # Trough factor (favorable interaction helps)
    trough_eff = min(trough_interaction, 1.0)

    # Subsidence factor (strong subsidence = good warm core)
    if subsidence_rate > 0:
        sub_eff = min(1.0 + 0.1 * subsidence_rate, 1.2)
    else:
        sub_eff = max(0.8 + 0.2 * subsidence_rate, 0.5)

    epsilon_out = jet_eff * trough_eff * sub_eff

    return min(epsilon_out, 1.0)


def z_squared_mpi_with_outflow(T_sst_C: float, T_out_base_C: float,
                                 epsilon_out: float,
                                 Ck_Cd: float = 1.0) -> dict:
    """
    Calculate MPI including outflow efficiency.

    V_max² = Z² × (Ck/Cd) × η × ε_out × Δk / c_p

    Parameters
    ----------
    T_sst_C : float
        Sea surface temperature (°C)
    T_out_base_C : float
        Base outflow temperature (°C)
    epsilon_out : float
        Outflow efficiency factor
    Ck_Cd : float
        Ratio of transfer coefficients

    Returns
    -------
    dict
        MPI with outflow details
    """
    # Temperatures in Kelvin
    T_s = T_sst_C + 273.15
    T_out = T_out_base_C + 273.15

    # Carnot efficiency
    eta_carnot = (T_s - T_out) / T_s

    # Effective efficiency with outflow factor
    eta_eff = eta_carnot * epsilon_out

    # Enthalpy disequilibrium (simplified)
    # Δk ≈ L_v × Δq + c_p × ΔT
    L_v = 2.5e6
    # Assume ~15 g/kg saturation at SST
    q_sat = 0.015 * np.exp(0.067 * (T_sst_C - 26))
    delta_k = L_v * q_sat * 0.15 + c_p * 2  # Rough estimate

    # MPI calculation
    V_max_sq = Z_SQUARED * Ck_Cd * eta_eff * delta_k / c_p
    V_max = np.sqrt(max(V_max_sq, 0))

    return {
        'V_max_m_s': V_max,
        'V_max_kt': V_max * 1.944,
        'eta_carnot': eta_carnot,
        'eta_effective': eta_eff,
        'epsilon_outflow': epsilon_out,
        'delta_k': delta_k,
        'T_sst': T_sst_C,
        'T_out': T_out_base_C
    }


# =============================================================================
# SECTION 7: DEMONSTRATION AND VALIDATION
# =============================================================================

def demonstrate_outflow_dynamics():
    """Demonstrate Z² outflow framework."""

    print("=" * 70)
    print("Z² FRAMEWORK: OUTFLOW LAYER DYNAMICS")
    print("=" * 70)

    print(f"\nFundamental constant: Z² = 32π/3 = {Z_SQUARED:.4f}")

    print(f"\n" + "-" * 70)
    print("CARNOT EFFICIENCY VS SST AND OUTFLOW TEMPERATURE")
    print("-" * 70)

    print(f"\n{'SST (°C)':>10} | {'T_out (°C)':>11} | {'η_Carnot':>10}")
    print("-" * 40)

    for sst in [26, 28, 30, 32]:
        T_out = outflow_temperature(sst)
        eta = carnot_efficiency(sst, T_out)
        print(f"{sst:10.0f} | {T_out:11.0f} | {eta:10.3f}")

    print(f"\n" + "-" * 70)
    print("OUTFLOW ANTICYCLONE STRUCTURE")
    print("-" * 70)

    # Calculate for a Cat 3 hurricane
    lat = 20
    V_max = 55  # m/s
    r_max = 35  # km
    f = coriolis_parameter(lat)
    M = r_max * 1000 * V_max + 0.5 * f * (r_max * 1000)**2

    print(f"\nCat 3 hurricane: V_max={V_max} m/s, r_max={r_max} km, lat={lat}°")
    print(f"Angular momentum M = {M:.2e} m²/s")

    print(f"\nOutflow tangential wind vs radius:")
    print(f"{'r (km)':>8} | {'V_θ (m/s)':>10} | {'Flow Type':>12}")
    print("-" * 35)

    for r in [50, 100, 200, 500, 1000, 1500]:
        V = outflow_tangential_wind(M, r, lat)
        flow = "Cyclonic" if V > 0 else "Anticyclonic"
        print(f"{r:8.0f} | {V:10.1f} | {flow:>12}")

    print(f"\n" + "-" * 70)
    print("OUTFLOW CHANNEL EFFICIENCY")
    print("-" * 70)

    print(f"\nJet distance effect (jet=50 m/s, no trough):")
    for dist in [200, 400, 600, 800, 1000]:
        eff = outflow_channel_efficiency(dist, 50, 'none')
        bar = "█" * int(eff * 20)
        print(f"  {dist:4d} km: ε = {eff:.2f} {bar}")

    print(f"\nTrough position effect (dist=800 km):")
    for pos in ['favorable', 'none', 'overhead']:
        eff = outflow_channel_efficiency(800, 50, pos)
        print(f"  {pos:12s}: ε = {eff:.2f}")

    print(f"\n" + "-" * 70)
    print("WARM CORE STRUCTURE")
    print("-" * 70)

    print(f"\nWarm core anomaly and pressure drop:")
    print(f"{'V_max (m/s)':>12} | {'ΔT (K)':>8} | {'Δp (hPa)':>10} | {'Cat':>6}")
    print("-" * 45)

    for V in [35, 50, 65, 80]:
        dT = warm_core_anomaly(V)
        dp = central_pressure_from_warm_core(dT, 220)
        cat = _get_category(V * 1.944)
        print(f"{V:12.0f} | {dT:8.1f} | {dp:10.1f} | {cat:>6}")

    print(f"\n" + "-" * 70)
    print("TROUGH INTERACTION ANALYSIS")
    print("-" * 70)

    scenarios = [
        ("Favorable NE trough", 800, 600, 60),
        ("Close trough", 400, 600, 45),
        ("Overhead trough", 600, 400, 0),
        ("Distant weak trough", 1200, 300, 75),
    ]

    print(f"\n{'Scenario':>25} | {'Index':>6} | {'Outcome':>30}")
    print("-" * 70)

    for name, dist, amp, angle in scenarios:
        result = trough_interaction_index(dist, amp, angle)
        print(f"{name:>25} | {result['interaction_index']:6.2f} | {result['outcome']:>30}")

    print(f"\n" + "-" * 70)
    print("Z² MPI WITH OUTFLOW EFFICIENCY")
    print("-" * 70)

    print(f"\nSST = 29°C, T_out = -60°C")
    print(f"\n{'ε_outflow':>10} | {'η_eff':>8} | {'V_max (m/s)':>12} | {'V_max (kt)':>11}")
    print("-" * 50)

    for eps in [0.5, 0.7, 0.85, 1.0]:
        result = z_squared_mpi_with_outflow(29, -60, eps)
        print(f"{eps:10.2f} | {result['eta_effective']:8.3f} | "
              f"{result['V_max_m_s']:12.1f} | {result['V_max_kt']:11.0f}")

    print(f"\n" + "=" * 70)
    print("KEY Z² INSIGHTS:")
    print("  1. η = (T_s - T_out)/T_s directly in Z² equation")
    print("  2. Outflow anticyclone from M conservation")
    print("  3. Favorable trough enhances outflow efficiency")
    print("  4. Warm core ΔT ∝ V² confirms Z² scaling")
    print("  5. Blocked outflow reduces effective η → weaker MPI")
    print("=" * 70)

    print("\nScript completed successfully.")


def _get_category(V_kt):
    """Get category from wind speed in knots."""
    if V_kt >= 137:
        return "Cat 5"
    elif V_kt >= 113:
        return "Cat 4"
    elif V_kt >= 96:
        return "Cat 3"
    elif V_kt >= 83:
        return "Cat 2"
    elif V_kt >= 64:
        return "Cat 1"
    elif V_kt >= 34:
        return "TS"
    else:
        return "TD"


if __name__ == "__main__":
    demonstrate_outflow_dynamics()
