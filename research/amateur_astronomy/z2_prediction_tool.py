#!/usr/bin/env python3
"""
Z² Prediction Tool for Amateur Astronomers
===========================================

Calculate Z² framework predictions for any solar system object.
Input orbital elements, get predicted anomalous acceleration.

Usage:
    python z2_prediction_tool.py

Or import and use programmatically:
    from z2_prediction_tool import predict_anomaly

Carl Zimmerman | May 2026
"""

import numpy as np
from dataclasses import dataclass
from typing import Optional, Tuple

# =============================================================================
# CONSTANTS
# =============================================================================

# Physical constants (SI)
G = 6.674e-11       # m³ kg⁻¹ s⁻²
M_SUN = 1.989e30    # kg
AU = 1.496e11       # m
DAY = 86400         # seconds

# Z² framework
Z_SQUARED = 32 * np.pi / 3      # = 33.510321
Z = np.sqrt(Z_SQUARED)          # = 5.788810
ALPHA = 1 / (4 * Z_SQUARED + 3) # = 1/137.04
RATIO = 4 * ALPHA / Z_SQUARED   # = 8.71×10⁻⁴

# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def solar_gravity(r_AU: float) -> float:
    """
    Calculate solar gravitational acceleration at distance r.

    Args:
        r_AU: Heliocentric distance in AU

    Returns:
        Acceleration in m/s²
    """
    r_m = r_AU * AU
    return G * M_SUN / r_m**2


def z2_anomalous_acceleration(r_AU: float) -> float:
    """
    Calculate Z² predicted non-gravitational acceleration.

    a_ng = (4α/Z²) × GM☉/r²

    Args:
        r_AU: Heliocentric distance in AU

    Returns:
        Predicted acceleration in m/s²
    """
    return RATIO * solar_gravity(r_AU)


def position_drift_per_year(r_AU: float, bound_orbit: bool = True) -> Tuple[float, float]:
    """
    Calculate position drift from Z² effect over one year.

    For BOUND orbits, the radial acceleration largely cancels over a full
    orbit because it points in opposite directions on opposite sides of
    the Sun. The observable effect is much smaller than naive kinematics.

    For HYPERBOLIC trajectories (ISOs), the effect accumulates during the
    single passage.

    Args:
        r_AU: Heliocentric distance in AU
        bound_orbit: True for asteroids/comets, False for ISOs

    Returns:
        (drift_meters, drift_arcsec_at_1AU) - position drift
    """
    a = z2_anomalous_acceleration(r_AU)
    t = 365.25 * DAY  # one year in seconds

    if bound_orbit:
        # For bound orbits, radial acceleration causes secular drift in
        # orbital elements, not simple position drift.
        #
        # The main observable effect is a slow change in semi-major axis:
        # da/dt ≈ 2a² × (a_ng/μ) × e × sin(f) averaged over orbit
        #
        # For a circular orbit (e→0), this averages to zero!
        # For eccentric orbits, there's a small net effect.
        #
        # Approximate: the effective position drift is suppressed by
        # a factor of ~e (eccentricity) compared to naive kinematics.
        #
        # Also, over multiple orbits, the effect grows linearly with time
        # (not as t²) because it's a secular drift.
        #
        # Empirical constraint: observed dark comet accelerations are ~50,000×
        # weaker than Z² would predict. This implies extreme suppression.

        suppression_factor = 1e-4  # Constrained by non-detection in bound orbits
        drift_m = 0.5 * a * t**2 * suppression_factor
    else:
        # For hyperbolic trajectories, use full calculation
        # (but this is handled separately in ISO prediction code)
        drift_m = 0.5 * a * t**2

    # Convert to arcseconds as seen from 1 AU
    drift_AU = drift_m / AU
    drift_arcsec = drift_AU * 206265  # radians to arcsec

    return drift_m, drift_arcsec


def velocity_change_per_year(r_AU: float) -> float:
    """
    Calculate velocity change from Z² effect over one year.

    Args:
        r_AU: Heliocentric distance in AU

    Returns:
        Δv in m/s per year
    """
    a = z2_anomalous_acceleration(r_AU)
    t = 365.25 * DAY
    return a * t


def observable_residual(r_AU: float, years: float, distance_AU: float,
                        bound_orbit: bool = True, eccentricity: float = 0.2) -> float:
    """
    Calculate observable astrometric residual for bound orbits.

    For asteroids in bound orbits, the Z² effect causes SECULAR drift
    in orbital elements, not simple position drift. The observable
    residual grows roughly linearly with time (not as t²).

    The key observable is the along-track position error that accumulates
    as the semi-major axis drifts.

    Args:
        r_AU: Object's heliocentric distance in AU
        years: Time baseline in years
        distance_AU: Object's distance from Earth in AU
        bound_orbit: True for asteroids, False for hyperbolic
        eccentricity: Orbital eccentricity (affects sensitivity)

    Returns:
        Angular residual in arcseconds
    """
    a_ng = z2_anomalous_acceleration(r_AU)
    t = years * 365.25 * DAY

    if bound_orbit:
        # For bound orbits, the radial perturbation causes secular change
        # in the mean motion n = √(μ/a³).
        #
        # The along-track position error from Δa is:
        # Δλ ≈ (3/2) × (Δa/a) × n × t
        #
        # The change in a from radial acceleration (averaged over orbit):
        # da/dt ≈ (2a/n) × <a_ng × e × sin(f)>
        #       ≈ (2a/n) × a_ng × e × (1/2) for eccentric orbits
        #
        # This is approximate. The key point: effect scales with e.

        # Simplified model: along-track drift scales as
        # Δx ≈ a_ng × e × t² / (period/2)
        #
        # Actually, let's use empirical calibration from dark comet observations:
        # 1998 KY26 shows a_ng ≈ 1.6×10⁻¹¹ AU/d² ≈ 2.5×10⁻¹⁰ m/s²
        # This gives detectable orbital drift over years.
        #
        # For Z² effect (a_ng ≈ 5×10⁻⁶ m/s² at 1 AU), the drift would be
        # ~20,000× larger... which would have been detected long ago.
        #
        # This suggests Z² effect does NOT apply to bound asteroids,
        # OR there's a strong suppression mechanism.
        #
        # For now, report what WOULD be observable if the effect existed:

        # Suppression factor for bound orbits (theoretical)
        # The radial force averages to zero for circular orbits.
        # Net effect scales with eccentricity.
        #
        # Empirical constraint: dark comets show a_ng ~ 10⁻¹⁰ m/s²
        # Z² predicts ~5×10⁻⁶ m/s² at 1 AU
        # Ratio: ~50,000×
        # This means suppression must be ~10⁻⁵ to ~10⁻⁴
        suppression = eccentricity * 1e-4  # Constrained by non-detection

        drift_m = 0.5 * a_ng * t**2 * suppression
    else:
        # Hyperbolic - full effect
        drift_m = 0.5 * a_ng * t**2

    # Angular size from Earth
    distance_m = distance_AU * AU
    angle_rad = drift_m / distance_m
    angle_arcsec = angle_rad * 206265

    return angle_arcsec


# =============================================================================
# OBJECT ANALYSIS
# =============================================================================

@dataclass
class SolarSystemObject:
    """Solar system object for Z² analysis"""
    name: str
    a_AU: float      # Semi-major axis (AU)
    e: float         # Eccentricity
    period_years: Optional[float] = None

    def __post_init__(self):
        if self.period_years is None:
            # Kepler's 3rd law
            self.period_years = self.a_AU ** 1.5

    @property
    def perihelion_AU(self) -> float:
        return self.a_AU * (1 - self.e)

    @property
    def aphelion_AU(self) -> float:
        return self.a_AU * (1 + self.e)

    def analyze(self):
        """Print full Z² analysis for this object"""

        print(f"\n{'='*60}")
        print(f"Z² ANALYSIS: {self.name}")
        print(f"{'='*60}")

        print(f"\nOrbital Elements:")
        print(f"  Semi-major axis: {self.a_AU:.3f} AU")
        print(f"  Eccentricity: {self.e:.4f}")
        print(f"  Perihelion: {self.perihelion_AU:.3f} AU")
        print(f"  Aphelion: {self.aphelion_AU:.3f} AU")
        print(f"  Period: {self.period_years:.2f} years")

        print(f"\nZ² Predictions at PERIHELION ({self.perihelion_AU:.3f} AU):")
        a_ng = z2_anomalous_acceleration(self.perihelion_AU)
        a_solar = solar_gravity(self.perihelion_AU)
        print(f"  Solar gravity: {a_solar:.3e} m/s²")
        print(f"  Z² anomaly: {a_ng:.3e} m/s²")
        print(f"  Ratio: {a_ng/a_solar:.6e} (expected: {RATIO:.6e})")

        print(f"\nZ² Predictions at APHELION ({self.aphelion_AU:.3f} AU):")
        a_ng = z2_anomalous_acceleration(self.aphelion_AU)
        a_solar = solar_gravity(self.aphelion_AU)
        print(f"  Solar gravity: {a_solar:.3e} m/s²")
        print(f"  Z² anomaly: {a_ng:.3e} m/s²")

        print(f"\nAccumulated Effects (per orbit, {self.period_years:.1f} years):")
        # Average distance (rough)
        r_avg = self.a_AU
        dv = velocity_change_per_year(r_avg) * self.period_years
        drift_m, drift_arcsec = position_drift_per_year(r_avg)
        drift_m *= self.period_years**2  # scales as t²
        drift_arcsec *= self.period_years**2
        print(f"  Velocity change: {dv:.1f} m/s")
        print(f"  Position drift: {drift_m/1e3:.1f} km = {drift_m/AU:.2e} AU")

        print(f"\nObservability (from Earth at 1 AU, e={self.e:.2f}):")
        for years in [1, 5, 10]:
            residual = observable_residual(r_avg, years, 1.0,
                                          bound_orbit=True, eccentricity=self.e)
            print(f"  After {years} years: {residual:.2f} arcsec")

        print(f"\nDetectability Assessment:")
        residual_1yr = observable_residual(r_avg, 1, 1.0,
                                          bound_orbit=True, eccentricity=self.e)
        if residual_1yr > 1.0:
            print(f"  ★ DETECTABLE with amateur equipment (>{residual_1yr:.1f} arcsec/yr)")
        elif residual_1yr > 0.1:
            print(f"  ◆ CHALLENGING but possible ({residual_1yr:.2f} arcsec/yr)")
        else:
            print(f"  ✗ Very difficult to detect ({residual_1yr:.3f} arcsec/yr)")

        print(f"\n  ⚠ NOTE: If Z² effect applied to bound asteroids at full strength,")
        print(f"     it would have been detected decades ago. Either:")
        print(f"     1. The effect only applies to ISOs (not bound objects)")
        print(f"     2. There's a suppression mechanism we don't understand")
        print(f"     3. The effect doesn't exist (numerology)")


def analyze_known_objects():
    """Analyze well-known objects for Z² detectability"""

    objects = [
        SolarSystemObject("1998 KY26 (Dark Comet)", 1.23, 0.20),
        SolarSystemObject("(99942) Apophis", 0.922, 0.191),
        SolarSystemObject("(433) Eros", 1.458, 0.223),
        SolarSystemObject("(1566) Icarus", 1.078, 0.827),
        SolarSystemObject("(3200) Phaethon", 1.271, 0.890),
        SolarSystemObject("(101955) Bennu", 1.126, 0.204),
    ]

    print("\n" + "="*70)
    print("Z² DETECTABILITY FOR WELL-KNOWN ASTEROIDS")
    print("="*70)

    print("""
    NOTE: For bound orbits, the radial Z² acceleration largely CANCELS
    over a full orbit. The residuals below assume ~1-2% of the naive
    effect survives (scaled by eccentricity).

    If the full effect applied, residuals would be 1000s of arcsec/yr
    and would have been detected decades ago!
    """)

    print(f"{'Object':<25} {'a (AU)':<8} {'e':<6} {'Residual/yr':<12} {'Status'}")
    print("-"*70)

    for obj in objects:
        r_avg = obj.a_AU
        residual = observable_residual(r_avg, 1, 1.0,
                                      bound_orbit=True, eccentricity=obj.e)

        if residual > 1.0:
            status = "★ Detectable"
        elif residual > 0.1:
            status = "◆ Challenging"
        else:
            status = "✗ Difficult"

        print(f"{obj.name:<25} {obj.a_AU:<8.3f} {obj.e:<6.3f} {residual:<12.2f}\"    {status}")

    print("""
    ⚠ KEY INSIGHT: The observed "dark comets" show a_ng ~ 10⁻¹⁰ m/s²,
       which is ~50,000× WEAKER than Z² predicts (~5×10⁻⁶ m/s²).

       This suggests Z² effect either:
       1. Only applies to interstellar objects (ISOs)
       2. Is strongly suppressed for bound orbits
       3. Doesn't exist (numerology)

    The best test remains: observe future ISOs (4I, 5I, etc.)
    """)


# =============================================================================
# INTERACTIVE MODE
# =============================================================================

def interactive_mode():
    """Run interactive analysis"""

    print("\n" + "="*60)
    print("Z² PREDICTION TOOL FOR AMATEUR ASTRONOMERS")
    print("="*60)
    print(f"\nZ² = 32π/3 = {Z_SQUARED:.6f}")
    print(f"Predicted ratio: a_ng/a_solar = 4α/Z² = {RATIO:.6e}")

    print("\nOptions:")
    print("  1. Analyze a specific object (enter orbital elements)")
    print("  2. Show predictions for known asteroids")
    print("  3. Quick calculation at specific distance")
    print("  4. Exit")

    while True:
        print()
        choice = input("Enter choice (1-4): ").strip()

        if choice == "1":
            print("\nEnter orbital elements:")
            name = input("  Object name: ").strip() or "Custom Object"
            try:
                a = float(input("  Semi-major axis (AU): "))
                e = float(input("  Eccentricity: "))
                obj = SolarSystemObject(name, a, e)
                obj.analyze()
            except ValueError:
                print("Invalid input. Please enter numbers.")

        elif choice == "2":
            analyze_known_objects()

        elif choice == "3":
            try:
                r = float(input("  Distance from Sun (AU): "))
                a_ng = z2_anomalous_acceleration(r)
                a_solar = solar_gravity(r)
                dv_yr = velocity_change_per_year(r)
                drift_m, drift_arcsec = position_drift_per_year(r)

                print(f"\n  At r = {r} AU:")
                print(f"    Solar gravity: {a_solar:.3e} m/s²")
                print(f"    Z² anomaly: {a_ng:.3e} m/s²")
                print(f"    Ratio: {a_ng/a_solar:.6e}")
                print(f"    Δv per year: {dv_yr:.1f} m/s")
                print(f"    Position drift per year: {drift_arcsec:.3f} arcsec (at 1 AU)")
            except ValueError:
                print("Invalid input. Please enter a number.")

        elif choice == "4":
            print("\nGoodbye! Clear skies.")
            break

        else:
            print("Invalid choice. Please enter 1-4.")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--batch":
        # Batch mode: analyze known objects
        analyze_known_objects()

        # Also show example custom analysis
        print("\n" + "="*60)
        print("EXAMPLE: 3I/ATLAS ANALYSIS")
        print("="*60)
        atlas = SolarSystemObject("3I/ATLAS", a_AU=1.36/(1-6.14+1), e=6.14)
        # For hyperbolic, use perihelion directly
        atlas.a_AU = -1.36 / (6.14 - 1)  # Negative for hyperbolic
        atlas.e = 6.14
        # Just show quick calc at perihelion
        r = 1.36
        a_ng = z2_anomalous_acceleration(r)
        print(f"\nAt perihelion (r = {r} AU):")
        print(f"  Z² anomalous acceleration: {a_ng:.3e} m/s²")
        print(f"  This is the testable prediction!")

    else:
        # Interactive mode
        interactive_mode()
