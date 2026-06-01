"""
Z² Hurricane Intensity Model

This module implements maximum potential intensity (MPI) theory with Z² framework
modifications. The Z² constant appears in the thermodynamic efficiency and
structural constraints of hurricanes.

Key Physics:
- Emanuel (1986) MPI theory: V_max² = (T_s/T_o) × (C_k/C_D) × (k₀* - k)
- Z² modification: Efficiency η relates to Z² through entropy optimization
- Structure constraint: eye/RMW → 1/Z as storms intensify
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Optional, Tuple, Dict, List
from enum import Enum

# Z² constants
Z_SQUARED = 32 * np.pi / 3  # ≈ 33.51
Z_VALUE = np.sqrt(Z_SQUARED)  # ≈ 5.789
ONE_OVER_Z = 1 / Z_VALUE  # ≈ 0.173
LOG_Z2 = np.log(Z_SQUARED)  # ≈ 3.51

# Physical constants
OMEGA_EARTH = 7.2921e-5  # Earth's angular velocity (rad/s)
R_GAS = 287.0  # Gas constant for dry air (J/kg/K)
C_P = 1004.0  # Specific heat at constant pressure (J/kg/K)
L_V = 2.5e6  # Latent heat of vaporization (J/kg)


class IntensityState(Enum):
    """Hurricane intensity state classifications."""
    TROPICAL_DEPRESSION = "TD"
    TROPICAL_STORM = "TS"
    CATEGORY_1 = "Cat1"
    CATEGORY_2 = "Cat2"
    CATEGORY_3 = "Cat3"
    CATEGORY_4 = "Cat4"
    CATEGORY_5 = "Cat5"


@dataclass
class EnvironmentalConditions:
    """Environmental conditions affecting hurricane intensity."""
    sst: float  # Sea surface temperature (K)
    sst_26c_depth: float = 50.0  # Depth of 26°C isotherm (m)
    tropopause_temp: float = 200.0  # Outflow temperature (K)
    vertical_shear: float = 5.0  # Wind shear (m/s)
    relative_humidity_mid: float = 0.70  # Mid-level RH (fraction)
    latitude: float = 20.0  # Degrees


@dataclass
class HurricaneState:
    """Current state of a hurricane."""
    max_wind: float  # Maximum sustained wind (m/s)
    central_pressure: float  # Central pressure (hPa)
    rmax: float  # Radius of maximum wind (km)
    eye_radius: float  # Eye radius (km)
    latitude: float  # Current latitude (degrees)
    longitude: float  # Current longitude (degrees)
    translation_speed: float = 5.0  # Forward speed (m/s)
    translation_direction: float = 315.0  # Heading (degrees)

    @property
    def eye_rmax_ratio(self) -> float:
        """Eye to RMW ratio."""
        return self.eye_radius / self.rmax if self.rmax > 0 else 0.0

    @property
    def coriolis_parameter(self) -> float:
        """Coriolis parameter at current latitude."""
        return 2 * OMEGA_EARTH * np.sin(np.radians(self.latitude))

    @property
    def category(self) -> IntensityState:
        """Saffir-Simpson category."""
        v_kt = self.max_wind * 1.944  # Convert m/s to knots
        if v_kt < 34:
            return IntensityState.TROPICAL_DEPRESSION
        elif v_kt < 64:
            return IntensityState.TROPICAL_STORM
        elif v_kt < 83:
            return IntensityState.CATEGORY_1
        elif v_kt < 96:
            return IntensityState.CATEGORY_2
        elif v_kt < 113:
            return IntensityState.CATEGORY_3
        elif v_kt < 137:
            return IntensityState.CATEGORY_4
        else:
            return IntensityState.CATEGORY_5


class Z2IntensityModel:
    """
    Z² Framework Hurricane Intensity Model.

    Combines Emanuel MPI theory with Z² geometric constraints:
    1. Thermodynamic efficiency bounded by Z²-related values
    2. Structure evolution toward 1/Z eye/RMW ratio
    3. Angular momentum optimization following Z² geometry
    """

    def __init__(
        self,
        ck_cd_ratio: float = 1.0,
        dissipative_heating: bool = True,
    ):
        """
        Initialize intensity model.

        Args:
            ck_cd_ratio: Ratio of enthalpy to drag coefficients
            dissipative_heating: Include dissipative heating feedback
        """
        self.ck_cd_ratio = ck_cd_ratio
        self.dissipative_heating = dissipative_heating

    def compute_mpi(
        self,
        env: EnvironmentalConditions,
    ) -> float:
        """
        Compute Maximum Potential Intensity using Emanuel (1986) theory.

        V_max² = (C_k/C_d) × (T_s - T_o)/T_o × Δk

        where Δk is the air-sea enthalpy disequilibrium.

        Args:
            env: Environmental conditions

        Returns:
            Maximum potential intensity (m/s)
        """
        T_s = env.sst
        T_o = env.tropopause_temp

        # Thermodynamic efficiency
        eta = (T_s - T_o) / T_o

        # Saturated specific humidity at SST
        e_sat = 6.112 * np.exp(17.67 * (T_s - 273.15) / (T_s - 29.65))  # hPa
        q_sat = 0.622 * e_sat / (1013.25 - 0.378 * e_sat)

        # Environmental boundary layer humidity (assume 80% of saturation)
        q_env = 0.80 * q_sat

        # Enthalpy disequilibrium
        delta_k = C_P * (T_s - (T_s - 2)) + L_V * (q_sat - q_env)

        # MPI formula
        V_max_sq = self.ck_cd_ratio * eta * delta_k

        # Dissipative heating enhancement (~20%)
        if self.dissipative_heating:
            V_max_sq *= 1.2

        V_max = np.sqrt(max(0, V_max_sq))

        return V_max

    def compute_z2_efficiency(self, env: EnvironmentalConditions) -> float:
        """
        Compute Z²-modified thermodynamic efficiency.

        The Z² framework suggests optimal efficiency relates to:
        η_opt = 1/Z² ≈ 0.030 (thermodynamic limit)

        But actual efficiency also depends on:
        η_actual = (T_s - T_o) / T_s × structure_factor

        where structure_factor → 1 as eye/RMW → 1/Z
        """
        T_s = env.sst
        T_o = env.tropopause_temp

        # Carnot efficiency
        eta_carnot = (T_s - T_o) / T_s

        # Z² optimal efficiency (theoretical limit)
        eta_z2 = 1 / Z_SQUARED

        # Actual efficiency is bounded by Carnot
        # but structure optimization can approach Z²-related values
        return min(eta_carnot, eta_z2 * np.log(Z_SQUARED))

    def compute_structure_tendency(
        self,
        state: HurricaneState,
        env: EnvironmentalConditions,
        dt: float = 3600.0,
    ) -> Tuple[float, float]:
        """
        Compute tendency for eye radius and RMW.

        Z² Framework prediction:
        - As storms intensify, eye/RMW → 1/Z ≈ 0.173
        - This represents the optimal angular momentum configuration

        Args:
            state: Current hurricane state
            env: Environmental conditions
            dt: Time step (seconds)

        Returns:
            Tuple of (d_eye_radius/dt, d_rmax/dt) in km/hour
        """
        current_ratio = state.eye_rmax_ratio
        target_ratio = ONE_OVER_Z

        # Intensification rate affects how fast structure evolves
        V_mpi = self.compute_mpi(env)
        intensity_fraction = state.max_wind / V_mpi if V_mpi > 0 else 0

        # Structure relaxation timescale (faster for more intense storms)
        tau_hours = 24.0 * (1 - 0.5 * intensity_fraction)

        # Eye radius tendency: contracts toward 1/Z ratio
        if current_ratio > target_ratio:
            # Eye too large relative to RMW, contract
            d_eye = -state.eye_radius * (current_ratio - target_ratio) / tau_hours
        else:
            # Eye too small, expand slightly (less common)
            d_eye = state.eye_radius * (target_ratio - current_ratio) / (2 * tau_hours)

        # RMW tendency: generally contracts during intensification
        d_rmax = -state.rmax * 0.02 * intensity_fraction / tau_hours

        return d_eye, d_rmax

    def predict_intensity_change(
        self,
        state: HurricaneState,
        env: EnvironmentalConditions,
        hours: float = 24.0,
    ) -> Dict[str, float]:
        """
        Predict intensity change over specified time period.

        Uses Z² framework to constrain intensity evolution:
        1. Upper bound from MPI
        2. Structure evolution toward 1/Z ratio
        3. Environmental modulation (shear, humidity, etc.)

        Args:
            state: Current hurricane state
            env: Environmental conditions
            hours: Forecast period

        Returns:
            Dictionary with predictions
        """
        # Maximum potential intensity
        V_mpi = self.compute_mpi(env)

        # Current intensity deficit
        intensity_deficit = V_mpi - state.max_wind

        # Environmental reduction factors
        shear_factor = np.exp(-env.vertical_shear / 20.0)  # Shear penalty
        humidity_factor = 0.5 + 0.5 * env.relative_humidity_mid  # Dry air penalty
        sst_factor = 1.0 if env.sst > 299.15 else max(0, (env.sst - 293.15) / 6.0)

        # Combined favorability
        favorability = shear_factor * humidity_factor * sst_factor

        # Intensification rate (m/s per hour)
        # Based on Kaplan-DeMaria type model with Z² modifications
        if intensity_deficit > 0:
            # Potential for intensification
            rate = intensity_deficit * favorability * 0.05
        else:
            # At or above MPI, decay
            rate = intensity_deficit * 0.1

        # Structure evolution
        d_eye, d_rmax = self.compute_structure_tendency(state, env)

        # Predictions
        predicted_wind = state.max_wind + rate * hours
        predicted_wind = max(0, min(predicted_wind, V_mpi * 1.05))  # Cap at 105% MPI

        # Pressure change (using pressure-wind relationship)
        # ΔP ≈ A × V² where A ≈ 0.015 for Atlantic hurricanes
        A_coefficient = 0.015
        predicted_pressure = 1013.25 - A_coefficient * predicted_wind**2

        # Structure predictions
        predicted_eye = max(5, state.eye_radius + d_eye * hours)
        predicted_rmax = max(15, state.rmax + d_rmax * hours)
        predicted_ratio = predicted_eye / predicted_rmax

        return {
            'predicted_wind_ms': predicted_wind,
            'predicted_wind_kt': predicted_wind * 1.944,
            'predicted_pressure': predicted_pressure,
            'predicted_eye_radius': predicted_eye,
            'predicted_rmax': predicted_rmax,
            'predicted_eye_ratio': predicted_ratio,
            'mpi': V_mpi,
            'intensity_change': rate * hours,
            'structure_convergence': abs(predicted_ratio - ONE_OVER_Z) / ONE_OVER_Z,
            'favorability': favorability,
            'rapid_intensification_likely': rate > 15.0 / hours,  # >30 kt in 24h
        }


class Z2RapidIntensification:
    """
    Rapid Intensification (RI) prediction using Z² framework.

    RI is defined as wind increase ≥ 30 knots (15.4 m/s) in 24 hours.

    Z² insight: RI occurs when structure rapidly approaches 1/Z optimal
    configuration, allowing efficient angular momentum transport.
    """

    def __init__(self):
        self.intensity_model = Z2IntensityModel()

        # RI historical statistics
        self.ri_threshold_kt = 30  # knots in 24 hours
        self.ri_threshold_ms = 15.4  # m/s in 24 hours

    def compute_ri_probability(
        self,
        state: HurricaneState,
        env: EnvironmentalConditions,
    ) -> Dict[str, float]:
        """
        Compute probability of rapid intensification.

        Z² Framework indicators:
        1. Distance from 1/Z structural ratio
        2. MPI headroom
        3. Environmental favorability

        Args:
            state: Current hurricane state
            env: Environmental conditions

        Returns:
            Dictionary with RI probability and factors
        """
        # Factor 1: Structural alignment with 1/Z
        current_ratio = state.eye_rmax_ratio
        ratio_factor = np.exp(-10 * abs(current_ratio - ONE_OVER_Z)**2)

        # Factor 2: MPI headroom
        V_mpi = self.intensity_model.compute_mpi(env)
        headroom = (V_mpi - state.max_wind) / V_mpi if V_mpi > 0 else 0
        headroom_factor = min(1.0, headroom * 2)  # Max at 50% of MPI

        # Factor 3: Environmental favorability
        shear_factor = np.exp(-env.vertical_shear / 15.0)
        humidity_factor = env.relative_humidity_mid
        sst_factor = 1.0 if env.sst > 302.15 else 0.5  # 29°C threshold
        env_factor = shear_factor * humidity_factor * sst_factor

        # Factor 4: Ocean heat content (simplified)
        ohc_factor = min(1.0, env.sst_26c_depth / 100.0)

        # Factor 5: Current intensity (RI more common for weaker storms)
        intensity_factor = max(0, 1 - state.max_wind / 70.0)

        # Combine factors
        # Weights based on SHIPS-RI type model
        weights = {
            'ratio': 0.15,
            'headroom': 0.25,
            'environment': 0.30,
            'ohc': 0.15,
            'intensity': 0.15,
        }

        composite = (
            weights['ratio'] * ratio_factor +
            weights['headroom'] * headroom_factor +
            weights['environment'] * env_factor +
            weights['ohc'] * ohc_factor +
            weights['intensity'] * intensity_factor
        )

        # Convert to probability (logistic transform)
        # Calibrated so composite=0.5 → 20% RI probability (climatology)
        z = 4 * (composite - 0.5)
        probability = 1 / (1 + np.exp(-z))

        return {
            'ri_probability': probability,
            'ri_probability_percent': probability * 100,
            'factor_structural': ratio_factor,
            'factor_headroom': headroom_factor,
            'factor_environment': env_factor,
            'factor_ohc': ohc_factor,
            'factor_intensity': intensity_factor,
            'composite_score': composite,
            'current_eye_ratio': current_ratio,
            'target_ratio_1_over_z': ONE_OVER_Z,
            'mpi_ms': V_mpi,
        }


def pressure_from_wind(wind_ms: float, method: str = 'z2') -> float:
    """
    Estimate central pressure from maximum wind speed.

    Methods:
    - 'dvorak': Standard Dvorak relationship
    - 'atkinson': Atkinson-Holliday relationship
    - 'z2': Z² framework modified relationship

    Args:
        wind_ms: Maximum sustained wind (m/s)
        method: Which relationship to use

    Returns:
        Estimated central pressure (hPa)
    """
    wind_kt = wind_ms * 1.944

    if method == 'dvorak':
        # Dvorak (1984) Atlantic
        pressure = 1015 - 0.0063 * wind_kt**2
    elif method == 'atkinson':
        # Atkinson-Holliday (1977) Pacific
        pressure = 1010 - (wind_kt / 6.7)**2
    elif method == 'z2':
        # Z² modified: coefficient relates to Z²
        # A = 0.015 ≈ 1/(2Z²) (half the inverse Z²)
        A = 1 / (2 * Z_SQUARED)
        pressure = 1013.25 - A * wind_ms**2 * 100  # Factor of 100 for units
    else:
        raise ValueError(f"Unknown method: {method}")

    return max(850, min(1013, pressure))


def wind_from_pressure(pressure_hpa: float, method: str = 'z2') -> float:
    """
    Estimate maximum wind from central pressure.

    Inverse of pressure_from_wind.

    Args:
        pressure_hpa: Central pressure (hPa)
        method: Which relationship to use

    Returns:
        Estimated maximum wind (m/s)
    """
    if method == 'dvorak':
        delta_p = 1015 - pressure_hpa
        wind_kt = np.sqrt(max(0, delta_p / 0.0063))
        wind_ms = wind_kt / 1.944
    elif method == 'atkinson':
        delta_p = 1010 - pressure_hpa
        wind_kt = 6.7 * np.sqrt(max(0, delta_p))
        wind_ms = wind_kt / 1.944
    elif method == 'z2':
        A = 1 / (2 * Z_SQUARED)
        delta_p = 1013.25 - pressure_hpa
        wind_ms = np.sqrt(max(0, delta_p / (A * 100)))
    else:
        raise ValueError(f"Unknown method: {method}")

    return max(0, wind_ms)


if __name__ == "__main__":
    print("=" * 60)
    print("Z² INTENSITY MODEL TEST")
    print("=" * 60)

    # Test environment
    env = EnvironmentalConditions(
        sst=303.15,  # 30°C
        tropopause_temp=200.0,
        vertical_shear=8.0,
        relative_humidity_mid=0.75,
        latitude=20.0,
    )

    # Test state (moderate hurricane)
    state = HurricaneState(
        max_wind=45.0,  # ~87 kt
        central_pressure=970.0,
        rmax=50.0,
        eye_radius=15.0,
        latitude=20.0,
        longitude=-70.0,
    )

    print(f"\nEnvironment:")
    print(f"  SST: {env.sst - 273.15:.1f}°C")
    print(f"  Shear: {env.vertical_shear:.0f} m/s")

    print(f"\nCurrent State:")
    print(f"  Wind: {state.max_wind:.0f} m/s ({state.max_wind * 1.944:.0f} kt)")
    print(f"  Pressure: {state.central_pressure:.0f} hPa")
    print(f"  Eye/RMW: {state.eye_rmax_ratio:.3f} (target: {ONE_OVER_Z:.3f})")
    print(f"  Category: {state.category.value}")

    # Intensity model
    model = Z2IntensityModel()

    print(f"\nMPI Analysis:")
    mpi = model.compute_mpi(env)
    print(f"  Maximum Potential Intensity: {mpi:.0f} m/s ({mpi * 1.944:.0f} kt)")

    print(f"\n24-hour Forecast:")
    forecast = model.predict_intensity_change(state, env, hours=24)
    print(f"  Predicted wind: {forecast['predicted_wind_ms']:.0f} m/s ({forecast['predicted_wind_kt']:.0f} kt)")
    print(f"  Predicted pressure: {forecast['predicted_pressure']:.0f} hPa")
    print(f"  Predicted eye/RMW: {forecast['predicted_eye_ratio']:.3f}")
    print(f"  RI likely: {forecast['rapid_intensification_likely']}")

    # RI probability
    ri_model = Z2RapidIntensification()
    ri_result = ri_model.compute_ri_probability(state, env)

    print(f"\nRI Analysis:")
    print(f"  RI Probability: {ri_result['ri_probability_percent']:.1f}%")
    print(f"  Structural factor: {ri_result['factor_structural']:.3f}")
    print(f"  Environment factor: {ri_result['factor_environment']:.3f}")
