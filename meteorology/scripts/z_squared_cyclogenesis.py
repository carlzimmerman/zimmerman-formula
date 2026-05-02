#!/usr/bin/env python3
"""
Z² Framework: Tropical Cyclogenesis
=====================================

First-principles derivation of tropical cyclone formation using
the Z² = 32π/3 framework. Genesis represents the transition from
a disorganized convective cluster to an organized warm-core vortex
capable of accessing the Carnot heat engine.

The Z² efficiency factor ε_genesis quantifies how close a disturbance
is to achieving self-sustaining intensification.

Author: Claude (Anthropic) & Carl Zimmerman
Date: 2024
"""

import numpy as np
from dataclasses import dataclass
from typing import Tuple, Optional, List
import warnings

# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================

# The Zimmerman constant
Z_SQUARED = 32 * np.pi / 3  # ≈ 33.51
Z = np.sqrt(Z_SQUARED)       # ≈ 5.79

# Physical constants
g = 9.81              # Gravitational acceleration (m/s²)
rho_a = 1.15          # Air density (kg/m³)
c_p = 1005            # Specific heat (J/kg/K)
L_v = 2.5e6           # Latent heat of vaporization (J/kg)
Omega = 7.292e-5      # Earth rotation rate (rad/s)
R_earth = 6.371e6     # Earth radius (m)

# =============================================================================
# SECTION 1: GENESIS PREREQUISITES
# =============================================================================
"""
FIRST PRINCIPLES: From Cluster to Cyclone

The Z² framework describes mature hurricane intensity:
    V_max² = Z² × (Ck/Cd) × η × (k_s* - k_a) / c_p

But this equation assumes:
1. Closed circulation exists
2. Warm core structure established
3. Boundary layer convergence organized
4. Outflow anticyclone developed

GENESIS is the process of establishing these prerequisites.

The key transition is from:
- Open wave trough (no closed circulation)
- Disorganized convection (random heating)
- Cold core (trough deepens with height)

To:
- Closed surface low
- Organized convection (symmetric heating)
- Warm core (trough weakens with height)

This requires:
1. Sufficient rotation (Coriolis → f > f_crit)
2. Warm ocean (SST > 26°C for adequate enthalpy)
3. Low wind shear (allows organization)
4. Mid-level moisture (reduces dilution)
5. Upper-level outflow channel (exhaust valve)
6. Pre-existing disturbance (seed vortex)
"""

def coriolis_parameter(latitude: float) -> float:
    """
    Calculate Coriolis parameter at given latitude.

    f = 2Ω sin(φ)

    Genesis requires f > f_crit ≈ 3×10⁻⁵ rad/s
    This corresponds to |latitude| > ~5°

    Parameters
    ----------
    latitude : float
        Latitude in degrees (positive NH, negative SH)

    Returns
    -------
    float
        Coriolis parameter (rad/s)
    """
    return 2 * Omega * np.sin(np.radians(latitude))


def rossby_deformation_radius(latitude: float, H: float = 12000) -> float:
    """
    Calculate the Rossby radius of deformation.

    L_R = (gH)^0.5 / f

    This sets the natural scale of developing cyclones.
    Disturbances larger than L_R can develop into TCs.

    Parameters
    ----------
    latitude : float
        Latitude in degrees
    H : float
        Equivalent depth (m) - related to static stability

    Returns
    -------
    float
        Rossby radius (km)
    """
    f = abs(coriolis_parameter(latitude))
    if f < 1e-6:
        return np.inf

    c = np.sqrt(g * H)  # Gravity wave speed
    L_R = c / f

    return L_R / 1000  # Convert to km


# =============================================================================
# SECTION 2: GENESIS PARAMETER (GP)
# =============================================================================
"""
GENESIS PARAMETER

Following Gray (1968, 1979), genesis potential is controlled by:
1. Thermal factor (SST, instability)
2. Dynamic factor (vorticity, convergence)
3. Coriolis factor (latitude)
4. Humidity factor (mid-level moisture)
5. Shear factor (vertical wind shear)

The Z² framework incorporates these through:

    ε_genesis = ε_thermal × ε_dynamic × ε_coriolis × ε_humidity × ε_shear

When ε_genesis > 1, genesis is favored.
The higher ε_genesis, the faster development.
"""

def sst_factor(SST_C: float) -> float:
    """
    Calculate SST contribution to genesis potential.

    Physics:
    - SST > 26°C required for adequate enthalpy flux
    - Ocean mixed layer > 50m needed to prevent cooling
    - Clausius-Clapeyron: water vapor ∝ exp(0.067×T)

    The factor follows a sigmoid curve:
        ε_SST = 1 / (1 + exp(-(SST - 26.5)/1.5))

    Parameters
    ----------
    SST_C : float
        Sea surface temperature (°C)

    Returns
    -------
    float
        SST genesis factor (0-1)
    """
    # Sigmoid centered at 26.5°C (traditional 26°C threshold)
    SST_crit = 26.5
    steepness = 1.5

    epsilon_sst = 1 / (1 + np.exp(-(SST_C - SST_crit) / steepness))

    return epsilon_sst


def vorticity_factor(zeta_850: float, f: float) -> float:
    """
    Calculate low-level vorticity contribution.

    Genesis requires pre-existing cyclonic rotation.
    This can come from:
    - Easterly waves
    - Monsoon trough
    - Frontal remnants
    - Previous TC remnants

    The relative vorticity must exceed:
        ζ > ζ_crit ≈ f/2

    Parameters
    ----------
    zeta_850 : float
        850 hPa relative vorticity (s⁻¹)
    f : float
        Coriolis parameter (s⁻¹)

    Returns
    -------
    float
        Vorticity genesis factor (0-2)
    """
    # Normalize by Coriolis parameter
    zeta_norm = abs(zeta_850) / max(abs(f), 1e-5)

    # Factor increases with vorticity, saturates at ~2×f
    if zeta_norm < 0.3:
        return zeta_norm / 0.3
    else:
        return min(1 + (zeta_norm - 0.3) / 2, 2.0)


def humidity_factor(RH_700: float, RH_500: float) -> float:
    """
    Calculate mid-level humidity contribution.

    Dry air entrainment kills convection through:
    - Evaporative downdrafts
    - Dilution of updraft buoyancy
    - Reduction of condensational heating

    Genesis favored when RH > 60% at 500-700 hPa.

    Parameters
    ----------
    RH_700 : float
        700 hPa relative humidity (0-1)
    RH_500 : float
        500 hPa relative humidity (0-1)

    Returns
    -------
    float
        Humidity genesis factor (0-1.5)
    """
    RH_mean = (RH_700 + RH_500) / 2

    # Linear increase to 0.7, then saturates
    if RH_mean < 0.4:
        return RH_mean / 0.4 * 0.5  # Strongly inhibited
    elif RH_mean < 0.7:
        return 0.5 + (RH_mean - 0.4) / 0.3 * 0.5
    else:
        return 1.0 + (RH_mean - 0.7) / 0.3 * 0.5  # Bonus for very moist

    return min(factor, 1.5)


def shear_factor(V_shear: float) -> float:
    """
    Calculate vertical wind shear factor.

    Shear tilts the developing vortex, preventing:
    - Warm core development
    - Organization of convection
    - Alignment of low/upper circulations

    Genesis requires shear < 10-15 m/s.

    Parameters
    ----------
    V_shear : float
        200-850 hPa wind shear (m/s)

    Returns
    -------
    float
        Shear genesis factor (0-1)
    """
    if V_shear < 5:
        return 1.0  # Ideal - no shear penalty
    elif V_shear < 10:
        return 1.0 - (V_shear - 5) / 10
    elif V_shear < 20:
        return 0.5 * np.exp(-(V_shear - 10) / 10)
    else:
        return 0.01  # Essentially impossible


def genesis_potential_index(latitude: float, SST_C: float,
                            zeta_850: float, V_shear: float,
                            RH_700: float, RH_500: float) -> dict:
    """
    Calculate Genesis Potential Index using Z² framework.

    Combines all factors multiplicatively:
        GPI = ε_SST × ε_vort × ε_RH × ε_shear × f^α

    Parameters
    ----------
    latitude : float
        Latitude (degrees)
    SST_C : float
        Sea surface temperature (°C)
    zeta_850 : float
        850 hPa vorticity (s⁻¹)
    V_shear : float
        200-850 hPa shear (m/s)
    RH_700, RH_500 : float
        Relative humidity (0-1)

    Returns
    -------
    dict
        GPI and component factors
    """
    f = coriolis_parameter(latitude)

    eps_sst = sst_factor(SST_C)
    eps_vort = vorticity_factor(zeta_850, f)
    eps_rh = humidity_factor(RH_700, RH_500)
    eps_shear = shear_factor(V_shear)

    # Coriolis factor (weak at equator, strong poleward)
    eps_coriolis = min(abs(f) / 5e-5, 2.0)

    # Combined GPI
    GPI = eps_sst * eps_vort * eps_rh * eps_shear * eps_coriolis

    # Categorize
    if GPI > 3:
        category = "Very High"
    elif GPI > 1.5:
        category = "High"
    elif GPI > 0.8:
        category = "Moderate"
    elif GPI > 0.3:
        category = "Low"
    else:
        category = "Very Low"

    return {
        'GPI': GPI,
        'category': category,
        'epsilon_SST': eps_sst,
        'epsilon_vorticity': eps_vort,
        'epsilon_humidity': eps_rh,
        'epsilon_shear': eps_shear,
        'epsilon_coriolis': eps_coriolis,
        'f_parameter': f,
        'limiting_factor': _identify_limiting_factor_genesis(
            eps_sst, eps_vort, eps_rh, eps_shear, eps_coriolis
        )
    }


def _identify_limiting_factor_genesis(sst, vort, rh, shear, cor):
    """Identify primary limiting factor for genesis."""
    factors = {
        'SST': sst,
        'Vorticity': vort,
        'Humidity': rh,
        'Shear': shear,
        'Coriolis': cor
    }
    min_factor = min(factors, key=factors.get)
    return min_factor


# =============================================================================
# SECTION 3: SPIN-UP DYNAMICS
# =============================================================================
"""
SPIN-UP: From Disturbance to Depression

Once environmental conditions are favorable, spin-up occurs through:

1. VORTICITY CONVERGENCE
   dζ/dt = -ζ∇·v - v·∇ζ + tilting + solenoidal

   The ζ∇·v term (stretching) concentrates vorticity
   when low-level convergence exists.

2. DIABATIC VORTEX ENHANCEMENT
   Latent heating creates potential vorticity (PV)
   in the mid-troposphere, which then builds downward.

3. WIND-INDUCED SURFACE HEAT EXCHANGE (WISHE)
   V → flux → heating → ΔT → pressure drop → V
   This is the nascent form of the Z² Carnot engine!

The transition time depends on:
- Initial vorticity amplitude
- SST (controls WISHE intensity)
- Environmental moisture
"""

def vorticity_stretching_rate(zeta: float, divergence: float) -> float:
    """
    Calculate vorticity tendency from stretching.

    dζ/dt = -(ζ + f)∇·V

    Convergence (∇·V < 0) increases vorticity.
    This is the fundamental spin-up mechanism.

    Parameters
    ----------
    zeta : float
        Relative vorticity (s⁻¹)
    divergence : float
        Horizontal divergence (s⁻¹), negative for convergence

    Returns
    -------
    float
        Vorticity tendency (s⁻¹ per hour)
    """
    # Include planetary vorticity
    f_typical = 5e-5

    dzeta_dt = -(zeta + f_typical) * divergence

    # Convert to per hour
    return dzeta_dt * 3600


def wishe_feedback_rate(V_sfc: float, SST_C: float, T_air_C: float) -> float:
    """
    Calculate WISHE feedback intensity.

    Wind-Induced Surface Heat Exchange:
    Higher wind → more evaporation → more heating → lower pressure → higher wind

    The feedback rate:
        λ_WISHE = dV/dV × (V_current/V_typical)

    where dV/dV represents feedback strength per unit wind increase.

    Parameters
    ----------
    V_sfc : float
        Surface wind speed (m/s)
    SST_C : float
        Sea surface temperature (°C)
    T_air_C : float
        Near-surface air temperature (°C)

    Returns
    -------
    float
        WISHE feedback rate (dimensionless, higher = stronger)
    """
    # Sea-air temperature difference drives flux
    delta_T = SST_C - T_air_C

    # Clausius-Clapeyron: moisture capacity
    q_sat = 0.001 * np.exp(0.067 * SST_C)  # Simplified

    # Feedback strength
    feedback = (V_sfc / 10) * (delta_T / 2) * (q_sat / 0.020)

    return feedback


def genesis_timescale(GPI: float, zeta_initial: float,
                       SST_C: float) -> float:
    """
    Estimate time to tropical depression formation.

    Based on spin-up rate from WISHE and vortex stretching.

    Empirically:
        τ_genesis ≈ τ_0 / (GPI × ζ_initial / ζ_crit)

    where τ_0 ≈ 48-72 hours for marginal conditions.

    Parameters
    ----------
    GPI : float
        Genesis Potential Index
    zeta_initial : float
        Initial low-level vorticity (s⁻¹)
    SST_C : float
        Sea surface temperature (°C)

    Returns
    -------
    float
        Estimated genesis timescale (hours)
    """
    # Base timescale (hours)
    tau_0 = 60

    # Vorticity factor (stronger seed → faster genesis)
    zeta_crit = 2e-5  # Typical threshold
    vort_factor = max(abs(zeta_initial) / zeta_crit, 0.3)

    # SST factor (warmer → faster)
    sst_factor = 1 + 0.1 * (SST_C - 27)

    # Genesis timescale
    tau = tau_0 / (GPI * vort_factor * sst_factor)

    # Physical bounds
    return max(min(tau, 120), 12)  # 12-120 hours


# =============================================================================
# SECTION 4: MARSUPIAL PARADIGM
# =============================================================================
"""
MARSUPIAL PARADIGM (Dunkerton et al. 2009)

Tropical cyclones often form within the "pouch" of an
easterly wave, protected from hostile environmental air.

The pouch is a region of closed streamlines in the
wave-relative frame:
    ψ_relative = ψ_absolute + C_wave × y

where C_wave is the wave phase speed.

Inside the pouch:
- Air recirculates, becoming moist
- Convection is protected from dry air
- Vorticity accumulates
- Genesis can proceed

The Z² framework connects:
- Pouch provides ε_humidity ~ 1
- Recirculation builds ε_vorticity
- Protection allows low ε_shear
"""

def wave_phase_speed(wavelength_km: float, latitude: float) -> float:
    """
    Calculate easterly wave phase speed.

    African easterly waves: λ ~ 2500 km, c ~ 7-9 m/s (westward)
    Caribbean waves: similar

    Phase speed from barotropic Rossby wave:
        c = U - β / k²

    Parameters
    ----------
    wavelength_km : float
        Wavelength (km)
    latitude : float
        Latitude (degrees)

    Returns
    -------
    float
        Phase speed (m/s, negative = westward)
    """
    # Beta parameter
    beta = 2 * Omega * np.cos(np.radians(latitude)) / R_earth

    # Wavenumber
    k = 2 * np.pi / (wavelength_km * 1000)

    # Mean flow (easterly trade winds)
    U_mean = -8  # m/s (westward)

    # Phase speed
    c = U_mean - beta / k**2

    return c


def pouch_strength(wave_amplitude: float, wave_speed: float,
                   background_wind: float) -> float:
    """
    Calculate wave pouch strength.

    A strong pouch has:
    - Wave amplitude > background wind variability
    - Closed streamlines in wave-relative frame

    Strength metric:
        S = V_wave / |U_mean - c|

    Parameters
    ----------
    wave_amplitude : float
        Perturbation wind in wave (m/s)
    wave_speed : float
        Phase speed (m/s)
    background_wind : float
        Environmental mean flow (m/s)

    Returns
    -------
    float
        Pouch strength (>1 = closed pouch exists)
    """
    relative_flow = abs(background_wind - wave_speed)

    if relative_flow < 0.5:
        return wave_amplitude / 0.5  # Nearly stationary → strong pouch

    strength = wave_amplitude / relative_flow

    return strength


def marsupial_genesis_probability(pouch_strength: float,
                                   GPI: float) -> float:
    """
    Calculate genesis probability from marsupial paradigm.

    Probability depends on:
    1. Pouch strength (protection from environment)
    2. GPI (favorability of environment)

    P(genesis) = P_pouch × P_environment

    Parameters
    ----------
    pouch_strength : float
        Dimensionless pouch strength
    GPI : float
        Genesis Potential Index

    Returns
    -------
    float
        Genesis probability (0-1)
    """
    # Pouch probability (must have closed streamlines)
    if pouch_strength < 0.5:
        P_pouch = 0.1
    elif pouch_strength < 1.0:
        P_pouch = 0.3 + 0.3 * (pouch_strength - 0.5) / 0.5
    else:
        P_pouch = 0.6 + 0.3 * min((pouch_strength - 1.0), 1.0)

    # Environment probability
    if GPI < 0.5:
        P_env = 0.1 * GPI
    elif GPI < 1.5:
        P_env = 0.1 + 0.3 * (GPI - 0.5)
    else:
        P_env = 0.4 + 0.5 * (1 - np.exp(-(GPI - 1.5) / 2))

    return P_pouch * P_env


# =============================================================================
# SECTION 5: SUBTROPICAL GENESIS
# =============================================================================
"""
SUBTROPICAL CYCLOGENESIS

Not all TCs form in the deep tropics. Subtropical genesis
occurs through different pathways:

1. BAROCLINIC INITIATION
   - Upper-level trough interacts with warm SSTs
   - Cut-off low develops warm core
   - Transition to tropical structure

2. TROPICAL TRANSITION
   - Extratropical low moves over warm water
   - Convection wraps around center
   - Gradual loss of frontal characteristics

The Z² framework applies once warm core develops:
    V² = Z² × ε_subtropical × (Ck/Cd) × η × Δk/c_p

where ε_subtropical accounts for:
- Partial warm core (hybrid structure)
- Asymmetric heat sources
- Shear from jet stream proximity
"""

def subtropical_genesis_potential(latitude: float, SST_C: float,
                                   upper_PV: float, low_shear: float) -> dict:
    """
    Assess subtropical genesis potential.

    Subtropical genesis requires:
    1. SST > 23-24°C (lower threshold than tropical)
    2. Upper-level forcing (PV anomaly)
    3. Moderate shear (can be higher than tropical)

    Parameters
    ----------
    latitude : float
        Latitude (degrees)
    SST_C : float
        Sea surface temperature (°C)
    upper_PV : float
        Upper-level PV anomaly (PVU)
    low_shear : float
        850-500 hPa shear (m/s)

    Returns
    -------
    dict
        Subtropical genesis assessment
    """
    # SST factor (lower threshold for subtropical)
    if SST_C < 22:
        sst_factor = 0
    elif SST_C < 26:
        sst_factor = (SST_C - 22) / 4
    else:
        sst_factor = 1.0

    # Upper forcing (PV must be > 1 PVU for forcing)
    if upper_PV < 1:
        pv_factor = upper_PV / 2
    elif upper_PV < 3:
        pv_factor = 0.5 + (upper_PV - 1) / 4
    else:
        pv_factor = 1.0

    # Shear (can tolerate more shear initially)
    if low_shear < 15:
        shear_factor = 1.0
    elif low_shear < 25:
        shear_factor = 1 - (low_shear - 15) / 20
    else:
        shear_factor = 0.5 * np.exp(-(low_shear - 25) / 10)

    # Latitude factor (must be subtropical, not polar)
    if 20 < abs(latitude) < 40:
        lat_factor = 1.0
    elif 15 < abs(latitude) <= 20 or 40 <= abs(latitude) < 50:
        lat_factor = 0.7
    else:
        lat_factor = 0.3

    # Combined index
    SGPI = sst_factor * pv_factor * shear_factor * lat_factor

    return {
        'SGPI': SGPI,
        'favorable': SGPI > 0.5,
        'sst_factor': sst_factor,
        'upper_forcing_factor': pv_factor,
        'shear_factor': shear_factor,
        'latitude_factor': lat_factor,
        'pathway': _determine_pathway(upper_PV, low_shear)
    }


def _determine_pathway(pv, shear):
    """Determine likely subtropical development pathway."""
    if pv > 2 and shear > 15:
        return "Baroclinic → TC transition"
    elif pv > 1.5:
        return "Upper trough interaction"
    else:
        return "Tropical-like"


# =============================================================================
# SECTION 6: COMPLETE GENESIS ASSESSMENT
# =============================================================================

@dataclass
class GenesisAssessment:
    """Complete genesis assessment using Z² framework."""

    latitude: float
    SST_C: float
    zeta_850: float      # s⁻¹
    V_shear: float       # m/s
    RH_700: float        # 0-1
    RH_500: float        # 0-1
    wave_amplitude: float = 5.0  # m/s

    def __post_init__(self):
        """Calculate all genesis metrics."""
        self.f = coriolis_parameter(self.latitude)
        self.L_R = rossby_deformation_radius(self.latitude)

    def tropical_genesis(self) -> dict:
        """Calculate tropical genesis potential."""
        return genesis_potential_index(
            self.latitude, self.SST_C, self.zeta_850,
            self.V_shear, self.RH_700, self.RH_500
        )

    def development_timescale(self) -> float:
        """Estimate time to tropical depression."""
        gpi = self.tropical_genesis()['GPI']
        return genesis_timescale(gpi, self.zeta_850, self.SST_C)

    def marsupial_probability(self) -> float:
        """Calculate marsupial-paradigm genesis probability."""
        # Estimate wave properties
        c = wave_phase_speed(2500, self.latitude)
        U_mean = -8  # m/s typical trades
        ps = pouch_strength(self.wave_amplitude, c, U_mean)
        gpi = self.tropical_genesis()['GPI']
        return marsupial_genesis_probability(ps, gpi)


# =============================================================================
# SECTION 7: DEMONSTRATION AND VALIDATION
# =============================================================================

def demonstrate_cyclogenesis():
    """Demonstrate Z² genesis framework."""

    print("=" * 70)
    print("Z² FRAMEWORK: TROPICAL CYCLOGENESIS")
    print("=" * 70)

    print(f"\nFundamental constant: Z² = 32π/3 = {Z_SQUARED:.4f}")

    print(f"\n" + "-" * 70)
    print("CORIOLIS AND ROSSBY RADIUS VS LATITUDE")
    print("-" * 70)

    print(f"\nLatitude | f (s⁻¹)   | L_R (km) | Genesis Favored?")
    print("-" * 55)

    for lat in [0, 5, 10, 15, 20, 25, 30]:
        f = coriolis_parameter(lat)
        L_R = rossby_deformation_radius(lat)
        favored = "Yes" if lat >= 5 else "No (f too small)"
        print(f"  {lat:3d}°   | {f:9.2e} | {L_R:7.0f}  | {favored}")

    print(f"\n" + "-" * 70)
    print("INDIVIDUAL GENESIS FACTORS")
    print("-" * 70)

    print(f"\nSST Factor:")
    for sst in [24, 25, 26, 27, 28, 29, 30]:
        eps = sst_factor(sst)
        bar = "█" * int(eps * 20)
        print(f"  {sst}°C: {eps:.3f} {bar}")

    print(f"\nShear Factor:")
    for shear in [0, 5, 10, 15, 20, 25]:
        eps = shear_factor(shear)
        bar = "█" * int(eps * 20)
        print(f"  {shear:2d} m/s: {eps:.3f} {bar}")

    print(f"\n" + "-" * 70)
    print("GENESIS POTENTIAL INDEX - EXAMPLE SCENARIOS")
    print("-" * 70)

    scenarios = [
        ("Tropical - favorable", 15, 29, 3e-5, 5, 0.75, 0.65),
        ("Tropical - marginal shear", 15, 29, 3e-5, 12, 0.70, 0.60),
        ("Tropical - dry", 15, 29, 3e-5, 5, 0.50, 0.40),
        ("Tropical - cool SST", 15, 25, 3e-5, 5, 0.70, 0.60),
        ("Near equator", 3, 29, 1e-5, 5, 0.70, 0.60),
        ("Subtropical", 28, 27, 2e-5, 8, 0.65, 0.55),
    ]

    print(f"\nScenario                  | GPI   | Category   | Limiting")
    print("-" * 70)

    for name, lat, sst, zeta, shear, rh7, rh5 in scenarios:
        gpi = genesis_potential_index(lat, sst, zeta, shear, rh7, rh5)
        print(f"{name:25s} | {gpi['GPI']:5.2f} | {gpi['category']:10s} | "
              f"{gpi['limiting_factor']}")

    print(f"\n" + "-" * 70)
    print("GENESIS TIMESCALE ESTIMATION")
    print("-" * 70)

    print(f"\nFor moderate conditions (GPI=1.5):")
    for zeta in [1e-5, 2e-5, 3e-5, 5e-5]:
        tau = genesis_timescale(1.5, zeta, 28)
        print(f"  ζ = {zeta:.0e} s⁻¹: τ = {tau:.0f} hours ({tau/24:.1f} days)")

    print(f"\nFor strong vortex (ζ=3×10⁻⁵), varying GPI:")
    for gpi in [0.5, 1.0, 1.5, 2.0, 3.0]:
        tau = genesis_timescale(gpi, 3e-5, 28)
        print(f"  GPI = {gpi:.1f}: τ = {tau:.0f} hours")

    print(f"\n" + "-" * 70)
    print("MARSUPIAL PARADIGM - EASTERLY WAVE GENESIS")
    print("-" * 70)

    print(f"\nEasterly wave at 15°N, λ=2500 km:")
    c = wave_phase_speed(2500, 15)
    print(f"  Phase speed: {c:.1f} m/s")

    print(f"\nPouch strength vs wave amplitude (background = -8 m/s):")
    for amp in [3, 5, 7, 10]:
        ps = pouch_strength(amp, c, -8)
        closed = "Closed" if ps > 1 else "Open"
        print(f"  V_wave = {amp} m/s: strength = {ps:.2f} ({closed})")

    print(f"\nGenesis probability (strong pouch, varying GPI):")
    for gpi in [0.5, 1.0, 1.5, 2.0, 2.5]:
        prob = marsupial_genesis_probability(1.5, gpi)
        print(f"  GPI = {gpi:.1f}: P(genesis) = {prob:.1%}")

    print(f"\n" + "-" * 70)
    print("COMPLETE GENESIS ASSESSMENT")
    print("-" * 70)

    assessment = GenesisAssessment(
        latitude=15,
        SST_C=29,
        zeta_850=3e-5,
        V_shear=7,
        RH_700=0.72,
        RH_500=0.65,
        wave_amplitude=6
    )

    gpi = assessment.tropical_genesis()
    tau = assessment.development_timescale()
    prob = assessment.marsupial_probability()

    print(f"\n  Location: {assessment.latitude}°N")
    print(f"  SST: {assessment.SST_C}°C")
    print(f"  850 hPa vorticity: {assessment.zeta_850:.1e} s⁻¹")
    print(f"  Shear: {assessment.V_shear} m/s")
    print(f"  RH (700/500): {assessment.RH_700:.0%}/{assessment.RH_500:.0%}")
    print(f"\n  Results:")
    print(f"    GPI = {gpi['GPI']:.2f} ({gpi['category']})")
    print(f"    Development timescale: {tau:.0f} hours")
    print(f"    Marsupial genesis probability: {prob:.1%}")
    print(f"    Rossby radius: {assessment.L_R:.0f} km")

    print(f"\n" + "=" * 70)
    print("KEY Z² INSIGHTS:")
    print("  1. Z² framework requires closed circulation - genesis establishes this")
    print("  2. Genesis efficiency ε_genesis = product of environmental factors")
    print("  3. Spin-up occurs when WISHE feedback exceeds frictional decay")
    print("  4. Easterly wave pouches provide protected incubation region")
    print("  5. Once TD forms, Z² intensification physics takes over!")
    print("=" * 70)

    print("\nScript completed successfully.")


if __name__ == "__main__":
    demonstrate_cyclogenesis()
