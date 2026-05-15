"""
Interstellar Objects Raw Data
=============================
Comprehensive numerical data for 1I/'Oumuamua, 2I/Borisov, 3I/ATLAS,
and dark comets for physics analysis.

Carl Zimmerman | May 2026
"""

import numpy as np
from dataclasses import dataclass
from typing import Optional, Tuple

# Physical constants
AU_KM = 1.496e8  # km
AU_M = 1.496e11  # m
C = 2.998e8  # m/s
G = 6.674e-11  # m^3 kg^-1 s^-2
M_SUN = 1.989e30  # kg
YEAR_S = 3.156e7  # seconds

@dataclass
class OrbitalElements:
    """Orbital elements for a body"""
    q: float  # Perihelion distance (AU)
    e: float  # Eccentricity
    i: float  # Inclination (degrees)
    Omega: float  # Longitude of ascending node (degrees)
    omega: float  # Argument of perihelion (degrees)
    M: Optional[float] = None  # Mean anomaly (degrees)
    epoch: Optional[str] = None  # Epoch description
    q_err: Optional[float] = None
    e_err: Optional[float] = None
    i_err: Optional[float] = None

@dataclass
class NonGravAccel:
    """Non-gravitational acceleration parameters"""
    A1: float  # Radial component
    A2: float  # Transverse component
    A3: float  # Normal component
    A1_err: Optional[float] = None
    A2_err: Optional[float] = None
    A3_err: Optional[float] = None
    magnitude_at_1AU: Optional[float] = None  # m/s^2
    detection_sigma: Optional[float] = None


class Oumuamua:
    """
    1I/'Oumuamua (1I/2017 U1)
    First confirmed interstellar object
    Discovered: 2017 October 19
    """

    name = "1I/'Oumuamua"
    designation = "1I/2017 U1"
    discovery_date = "2017-10-19"
    discoverer = "Robert Weryk"
    telescope = "Pan-STARRS1"

    # Orbital elements (JPL, Epoch 2017 Nov 22.0)
    orbit = OrbitalElements(
        q=0.2559116,      # AU
        e=1.201134,
        i=122.74171,      # degrees
        Omega=24.59691,   # degrees
        omega=241.8105,   # degrees
        M=51.1576,        # degrees
        epoch="2017 Nov 22.0 (JD 2458080.5)",
        q_err=0.0000067,
        e_err=0.000021,
        i_err=0.00029
    )

    # Pre/post encounter eccentricities
    e_pre_encounter = 1.196488  # ± 0.000164
    e_post_encounter = 1.200366  # ± 0.000167

    # Velocities (km/s)
    v_infinity = 26.1  # Hyperbolic excess velocity
    v_perihelion = 87.3  # At closest approach to Sun
    v_pre_encounter = 26.1
    v_post_encounter = 26.4
    delta_v_anomalous = 17.0  # m/s (from non-grav acceleration)

    # Non-gravitational acceleration
    nongrav = NonGravAccel(
        A1=2.79e-7,
        A2=1.44e-8,
        A3=1.57e-8,
        A1_err=0.36e-7,
        A2_err=2.45e-8,
        A3_err=2.25e-8,
        magnitude_at_1AU=2.5e-6,  # m/s^2 at ~1.4 AU
        detection_sigma=30.0
    )

    # Physical properties (assuming albedo 0.04)
    albedo = 0.04  # Assumed
    H = 22.08  # Absolute magnitude
    H_err = 0.45

    # Size estimates for different albedos
    size_estimates = {
        # albedo: (effective_diameter_m, length_10to1_m, width_10to1_m)
        0.01: (510, 1600, 160),
        0.04: (260, 810, 81),
        0.10: (160, 510, 51),
        0.30: (93, 290, 29),
        0.90: (54, 170, 17),
    }

    effective_diameter_m = 260  # Most likely (albedo 0.04)
    length_m = 810  # Long axis
    width_m = 81  # Short axis
    axial_ratio = 10  # a/c ratio

    # Rotation
    rotation_periods_hr = [7.34, 7.5483, 6.831, 8.1, 8.14, 8.256]  # Multiple measurements
    rotation_period_hr = 7.34  # Meech et al. value
    lightcurve_amplitude_mag = 2.5  # ± 0.1
    tumbling = True  # Non-principal axis rotation

    # Spectroscopic
    spectral_slope_per_100nm = 0.10  # 10% ± 6% per 100 nm
    color_BV = 0.70  # ± 0.06
    color_VR = 0.45  # ± 0.05

    # Activity limits
    dust_production_limit_g_s = 1.7  # Upper limit
    mass_loss_fraction = 0.10  # ~10% during passage

    # Key dates
    perihelion_date = "2017-09-09"
    perihelion_jd = 2458006.00732
    closest_earth_date = "2017-10-15"
    closest_earth_distance_AU = 0.162

    @classmethod
    def get_acceleration_at_distance(cls, r_AU: float) -> float:
        """
        Calculate non-gravitational acceleration at distance r
        Follows r^-2 dependence

        Args:
            r_AU: Heliocentric distance in AU

        Returns:
            Acceleration in m/s^2
        """
        # Reference: 2.5e-6 m/s^2 at ~1.4 AU
        r_ref = 1.4
        a_ref = 2.5e-6
        return a_ref * (r_ref / r_AU)**2


class Borisov:
    """
    2I/Borisov (2I/2019 Q4)
    First interstellar comet with visible activity
    Discovered: 2019 August 30
    """

    name = "2I/Borisov"
    designation = "2I/2019 Q4"
    discovery_date = "2019-08-30"
    discoverer = "Gennady Borisov"
    telescope = "0.65m personal observatory, Crimea"

    # Orbital elements
    orbit = OrbitalElements(
        q=2.0,  # AU (approximate)
        e=3.356191,
        i=44.0,  # degrees
        Omega=0.0,  # Not precisely specified in sources
        omega=0.0,  # Not precisely specified in sources
        e_err=0.000015
    )

    # Velocities
    v_infinity = 32.0  # km/s
    v_at_discovery = 49.2  # km/s (177,000 km/hr)

    # Physical properties
    nucleus_diameter_m = 975  # Primary estimate
    nucleus_diameter_range_m = (440, 1400)  # Range of estimates
    nucleus_upper_limit_m = 500  # HST constraint

    # Mass loss
    mass_loss_fraction_preperihelion = 0.004  # >0.4%
    fragmentation_observed = True  # March 2020

    # Gas production rates (molecules/s)
    H2O_production = {
        "2019-11-01": 7.0e26,
        "2019-12-01": 10.7e26,  # Peak
        "2019-12-21": 4.9e26,
    }
    CO_production = {
        "ALMA_1": 3.3e26,
        "ALMA_2": 5.0e26,
    }

    # Composition - CRITICAL DATA
    CO_H2O_ratio = 1.50  # 130-173%, using 150% as representative
    CO_H2O_ratio_range = (1.30, 1.73)
    # Compare to solar system comets: 0.002-0.23 (typical 0.02-0.10)

    C_O_elemental_enhancement = 6.0  # 6x solar system comets

    # Spectroscopic
    color = "slightly reddish"
    polarization = "higher than typical solar system comets"

    # Key dates
    perihelion_date = "2019-12-08"

    # Origin
    incoming_direction = "Cassiopeia (near Perseus border)"
    outgoing_direction = "Telescopium"
    origin = "Galactic plane"


class Atlas3I:
    """
    3I/ATLAS (C/2025 N1)
    Third interstellar object, largest discovered
    Discovered: 2025 July 1
    """

    name = "3I/ATLAS"
    designation = "C/2025 N1"
    discovery_date = "2025-07-01"
    discoverer = "ATLAS survey"
    telescope = "ATLAS (Rio Hurtado, Chile)"

    # Orbital elements (D. Farnocchia, Epoch JD 2460868.5)
    orbit = OrbitalElements(
        q=1.36,  # AU
        e=6.141,
        i=175.0,  # degrees (retrograde)
        Omega=0.0,  # Not specified
        omega=0.0,  # Not specified
        e_err=0.00002
    )

    # Velocities (km/s)
    v_infinity = 57.9763  # ± 0.0044
    v_infinity_err = 0.0044
    v_perihelion = 68.0

    # Galactic velocity components (km/s)
    U_galactic = -51.0  # Away from Galactic Center
    W_galactic = 18.5   # Upward through galactic plane

    # Physical properties
    nucleus_radius_min_km = 0.16  # Assuming albedo 0.04
    nucleus_radius_max_km = 2.8   # Assuming albedo 0.04
    diameter_upper_limit_km = 5.6  # NASA
    diameter_lower_estimate_km = 0.44

    # Spectroscopic
    spectral_slope_per_100nm = 17.1  # ± 0.2 %/100nm
    spectral_slope_err = 0.2
    color = "slightly redder than D-type asteroids"

    # Activity
    activity = True  # Confirmed comet with coma and tail
    coma_detected = True
    tail_detected = True

    # Composition detected
    detected_species = ["dust", "H2O", "organic molecules", "CO2"]

    # Non-gravitational acceleration
    nongrav_detected = True
    nongrav_consistent_with_CO = True  # Ordinary CO outgassing

    # Key dates
    perihelion_date = "2025-10-29"
    perihelion_time = "11:45 UT"
    announcement_date = "2025-07-02"

    # Origin - SIGNIFICANT
    origin = "Galactic thick disk"
    age_estimate_gyr = (9, 13)  # 9-13 billion years
    formation_era = "Cosmic noon (intense star formation)"


@dataclass
class DarkComet:
    """Dark comet data structure"""
    name: str
    a: Optional[float] = None  # Semi-major axis (AU)
    e: Optional[float] = None  # Eccentricity
    i: Optional[float] = None  # Inclination (degrees)
    H: Optional[float] = None  # Absolute magnitude
    nongrav_accel: Optional[float] = None  # AU/d^2
    origin: Optional[str] = None


# Known dark comets
DARK_COMETS = {
    "inner": [
        DarkComet("1998 KY26", a=1.23, e=0.2, i=1.48, H=25.7,
                  nongrav_accel=1.6e-11, origin="Inner Main Belt"),
        DarkComet("2003 RM", origin="Outer Main Belt"),
        DarkComet("2005 VL1", origin="Inner Main Belt"),
        DarkComet("2006 RH120", origin="Inner Main Belt"),
        DarkComet("2010 RF12", origin="Inner Main Belt"),
        DarkComet("2010 VL65", origin="Inner Main Belt"),
        DarkComet("2016 NJ33", origin="Inner Main Belt"),
    ],
    "outer": [
        DarkComet("1998 FR11", origin="Outer Main Belt (5:2 resonance)"),
        DarkComet("2001 ME1", origin="Outer Main Belt"),
        # Plus 5 additional identified
    ]
}


# Comparison data
ISO_COMPARISON = {
    "property": ["Discovery year", "Eccentricity", "Perihelion (AU)",
                 "v_infinity (km/s)", "Size (m)", "Activity",
                 "Non-grav accel", "Shape", "Color", "Origin", "Age (Gyr)"],
    "1I/'Oumuamua": [2017, 1.20, 0.26, 26, 260, "None visible",
                     "Yes (30σ)", "Elongated 10:1", "Red", "Thin disk", "<2"],
    "2I/Borisov": [2019, 3.36, 2.0, 32, 975, "Strong comet",
                   "Yes", "Normal", "Red", "Galactic plane", "Unknown"],
    "3I/ATLAS": [2025, 6.14, 1.36, 58, "440-5600", "Moderate comet",
                 "Yes (small)", "Unknown", "Very red", "Thick disk", "9-13"],
}


def calculate_solar_escape_velocity(r_AU: float) -> float:
    """
    Calculate solar escape velocity at distance r

    Args:
        r_AU: Distance from Sun in AU

    Returns:
        Escape velocity in km/s
    """
    r_m = r_AU * AU_M
    v_esc = np.sqrt(2 * G * M_SUN / r_m)
    return v_esc / 1000  # Convert to km/s


def is_hyperbolic(v_km_s: float, r_AU: float) -> bool:
    """
    Check if velocity exceeds escape velocity (hyperbolic orbit)

    Args:
        v_km_s: Velocity in km/s
        r_AU: Distance from Sun in AU

    Returns:
        True if hyperbolic (interstellar)
    """
    v_esc = calculate_solar_escape_velocity(r_AU)
    return v_km_s > v_esc


def anomalous_acceleration_ratio(a_ng: float, r_AU: float) -> float:
    """
    Calculate ratio of non-gravitational acceleration to solar gravity

    Args:
        a_ng: Non-gravitational acceleration in m/s^2
        r_AU: Heliocentric distance in AU

    Returns:
        Ratio a_ng / a_solar
    """
    r_m = r_AU * AU_M
    a_solar = G * M_SUN / r_m**2
    return a_ng / a_solar


# Key numerical results
if __name__ == "__main__":
    print("=" * 60)
    print("INTERSTELLAR OBJECTS - KEY DATA SUMMARY")
    print("=" * 60)

    print("\n1I/'Oumuamua:")
    print(f"  Eccentricity: {Oumuamua.orbit.e}")
    print(f"  v∞: {Oumuamua.v_infinity} km/s")
    print(f"  Size: {Oumuamua.effective_diameter_m} m (albedo {Oumuamua.albedo})")
    print(f"  Non-grav accel: {Oumuamua.nongrav.magnitude_at_1AU:.2e} m/s² at 1.4 AU")
    print(f"  Detection significance: {Oumuamua.nongrav.detection_sigma}σ")
    print(f"  Δv from anomaly: {Oumuamua.delta_v_anomalous} m/s")

    # Calculate ratio to solar gravity at 1.4 AU
    ratio = anomalous_acceleration_ratio(2.5e-6, 1.4)
    print(f"  Ratio to solar gravity: {ratio:.2e}")

    print("\n2I/Borisov:")
    print(f"  Eccentricity: {Borisov.orbit.e}")
    print(f"  v∞: {Borisov.v_infinity} km/s")
    print(f"  Size: {Borisov.nucleus_diameter_m} m")
    print(f"  CO/H₂O ratio: {Borisov.CO_H2O_ratio:.0%} (solar system: 2-23%)")

    print("\n3I/ATLAS:")
    print(f"  Eccentricity: {Atlas3I.orbit.e}")
    print(f"  v∞: {Atlas3I.v_infinity} km/s")
    print(f"  Size range: {Atlas3I.diameter_lower_estimate_km*1000:.0f} - {Atlas3I.diameter_upper_limit_km*1000:.0f} m")
    print(f"  Age estimate: {Atlas3I.age_estimate_gyr[0]}-{Atlas3I.age_estimate_gyr[1]} Gyr")
    print(f"  Origin: {Atlas3I.origin}")

    print("\nSolar escape velocities:")
    for r in [0.26, 1.0, 1.36, 2.0]:
        v_esc = calculate_solar_escape_velocity(r)
        print(f"  At {r} AU: {v_esc:.1f} km/s")

    print("\nHyperbolic checks (at perihelion):")
    print(f"  'Oumuamua at 0.26 AU: hyperbolic = {is_hyperbolic(87.3, 0.26)}")
    print(f"  Borisov at 2.0 AU: hyperbolic = {is_hyperbolic(49.2, 2.0)}")
    print(f"  ATLAS at 1.36 AU: hyperbolic = {is_hyperbolic(68.0, 1.36)}")
