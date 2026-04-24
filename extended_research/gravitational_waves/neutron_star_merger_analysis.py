#!/usr/bin/env python3
"""
Binary Neutron Star Merger & Kilonova Analysis
===============================================
Author: Carl Zimmerman
Date: 2026-04-24

Deep analysis of GW170817-type events:
- Gravitational wave emission
- Kilonova electromagnetic counterpart
- r-process nucleosynthesis
- Equation of state constraints
"""

import numpy as np
import json
from dataclasses import dataclass
from typing import Tuple, Dict, List

# =============================================================================
# CONSTANTS
# =============================================================================

# Fundamental
G = 6.67430e-11          # m³/kg/s²
c = 2.99792458e8         # m/s
hbar = 1.054571817e-34   # J·s
M_sun = 1.98847e30       # kg
R_sun = 6.96340e8        # m
L_sun = 3.828e26         # W
pc = 3.08567758e16       # m
Mpc = pc * 1e6
eV = 1.602176634e-19     # J
MeV = 1e6 * eV
c2 = c**2

# Nuclear/Astrophysical
m_neutron = 1.674927471e-27   # kg
m_proton = 1.672621898e-27    # kg
m_u = 1.66054e-27             # atomic mass unit

# Neutron star typical values
NS_RADIUS_TYPICAL = 12e3      # 12 km typical radius
NS_DENSITY_CORE = 1e18        # kg/m³ (above nuclear density)

# =============================================================================
# GW170817 OBSERVED PARAMETERS
# =============================================================================

GW170817 = {
    "name": "GW170817",
    "date": "2017-08-17",
    "m1_solar": 1.46,           # Primary mass (solar masses)
    "m2_solar": 1.27,           # Secondary mass
    "m1_range": (1.36, 1.60),   # 90% credible interval
    "m2_range": (1.17, 1.36),
    "distance_mpc": 40,         # ~130 million light years
    "distance_range": (35, 45),
    "chirp_mass_solar": 1.186,
    "total_mass_solar": 2.73,
    "remnant_mass_solar": 2.7,  # Before collapse (if any)

    # Timing
    "gw_duration_s": 100,       # In LIGO band (>20 Hz)
    "gw_to_grb_delay_s": 1.7,   # GW to gamma-ray burst
    "merger_time_utc": "12:41:04.4",

    # Electromagnetic counterparts
    "grb_name": "GRB 170817A",
    "kilonova_name": "AT 2017gfo",
    "host_galaxy": "NGC 4993",

    # GW signal properties
    "snr": 32.4,                # Signal-to-noise ratio
    "peak_strain": 1e-21,       # Approximate
    "f_start_hz": 24,           # Entered LIGO band
    "f_end_hz": 500,            # Where signal faded (not ISCO)
}


# =============================================================================
# NEUTRON STAR PHYSICS
# =============================================================================

@dataclass
class NeutronStar:
    """Neutron star model"""
    mass_solar: float
    radius_km: float = 12.0
    spin_hz: float = 0.0

    def __post_init__(self):
        self.mass = self.mass_solar * M_sun
        self.radius = self.radius_km * 1e3

    @property
    def compactness(self) -> float:
        """C = GM/(Rc²) - dimensionless compactness"""
        return G * self.mass / (self.radius * c2)

    @property
    def surface_gravity(self) -> float:
        """Surface gravity in m/s²"""
        return G * self.mass / self.radius**2

    @property
    def escape_velocity(self) -> float:
        """Escape velocity at surface"""
        return np.sqrt(2 * G * self.mass / self.radius)

    @property
    def average_density(self) -> float:
        """Average density in kg/m³"""
        volume = (4/3) * np.pi * self.radius**3
        return self.mass / volume

    @property
    def schwarzschild_radius(self) -> float:
        """Schwarzschild radius in meters"""
        return 2 * G * self.mass / c2

    @property
    def binding_energy(self) -> float:
        """
        Gravitational binding energy (approximate)
        E_bind ≈ 0.6 * GM²/R (for uniform density)
        More accurate: E_bind ≈ 0.084 * Mc² for typical NS
        """
        return 0.084 * self.mass * c2

    def tidal_deformability(self, k2: float = 0.1) -> float:
        """
        Dimensionless tidal deformability Λ

        Λ = (2/3) * k2 * (R/M)^5

        where k2 is the Love number (~0.05-0.15 for NS)
        This is constrained by GW170817!
        """
        R_over_M = self.radius / (G * self.mass / c2)
        return (2/3) * k2 * R_over_M**5


# =============================================================================
# MERGER DYNAMICS
# =============================================================================

def chirp_mass(m1: float, m2: float) -> float:
    """Chirp mass in kg"""
    return (m1 * m2)**(3/5) / (m1 + m2)**(1/5)


def inspiral_time(M_c: float, f_start: float, f_end: float) -> float:
    """
    Time to inspiral from f_start to f_end

    τ = (5/256) * (c⁵/G^(5/3)) * M_c^(-5/3) * [f_start^(-8/3) - f_end^(-8/3)]
    """
    coeff = (5/256) * (c**5 / G**(5/3)) * M_c**(-5/3)
    return coeff * (f_start**(-8/3) - f_end**(-8/3))


def gw_frequency_at_separation(M_total: float, r: float) -> float:
    """GW frequency for given orbital separation"""
    f_orb = (1/(2*np.pi)) * np.sqrt(G * M_total / r**3)
    return 2 * f_orb  # Factor of 2 for quadrupole


def separation_at_contact(R1: float, R2: float) -> float:
    """Orbital separation when neutron stars touch"""
    return R1 + R2


def orbital_velocity_at_separation(M_total: float, r: float) -> float:
    """Orbital velocity"""
    return np.sqrt(G * M_total / r)


def energy_radiated_in_gw(M_c: float, f_start: float, f_end: float) -> float:
    """
    Total energy radiated in gravitational waves during inspiral

    E = (π²/3) * c⁵/G * M_c^(5/3) * [f_end^(2/3) - f_start^(2/3)]

    For GW170817: ~0.025 M_sun * c²
    """
    coeff = (np.pi**2 / 3) * (c**5 / G) * (G * M_c / c**3)**(5/3)
    return coeff * (f_end**(2/3) - f_start**(2/3))


# =============================================================================
# KILONOVA PHYSICS
# =============================================================================

@dataclass
class KilonovaModel:
    """
    Kilonova electromagnetic emission model

    Powered by radioactive decay of r-process elements
    """
    ejecta_mass_solar: float        # Mass of ejected material
    ejecta_velocity_c: float        # Velocity as fraction of c
    opacity_cm2_g: float = 10.0     # Lanthanide opacity
    heating_efficiency: float = 0.5  # Thermalization efficiency

    def __post_init__(self):
        self.ejecta_mass = self.ejecta_mass_solar * M_sun
        self.ejecta_velocity = self.ejecta_velocity_c * c

    @property
    def kinetic_energy(self) -> float:
        """Kinetic energy of ejecta in Joules"""
        return 0.5 * self.ejecta_mass * self.ejecta_velocity**2

    @property
    def diffusion_timescale(self) -> float:
        """
        Photon diffusion timescale (peak emission time)

        t_peak ≈ sqrt(2 * κ * M / (β * v * c))

        where κ = opacity, β ≈ 13.7 (geometric factor)
        """
        kappa = self.opacity_cm2_g * 1e-4  # Convert to m²/kg
        beta = 13.7
        t_diff = np.sqrt(2 * kappa * self.ejecta_mass /
                        (beta * self.ejecta_velocity * c))
        return t_diff

    def radioactive_heating_rate(self, time_s: float) -> float:
        """
        Radioactive heating rate from r-process decay

        Q̇ ≈ 2 × 10¹⁰ * (t/day)^(-1.3) erg/s/g

        This is the "Metzger et al." formula
        """
        time_days = time_s / 86400
        # erg/s/g -> W/kg
        q_dot = 2e10 * (time_days)**(-1.3) * 1e-7 * 1e3  # W/kg
        return q_dot * self.ejecta_mass * self.heating_efficiency

    def bolometric_luminosity(self, time_s: float) -> float:
        """
        Bolometric luminosity at given time

        Simple model: L ~ Q̇ at early times, then diffusion-limited
        """
        t_peak = self.diffusion_timescale
        Q_dot = self.radioactive_heating_rate(time_s)

        if time_s < t_peak:
            # Rising phase
            return Q_dot * (time_s / t_peak)**2
        else:
            # Declining phase
            return Q_dot

    def temperature_blackbody(self, time_s: float) -> float:
        """
        Blackbody temperature assuming spherical expansion

        T = (L / (4π R² σ))^(1/4)
        """
        L = self.bolometric_luminosity(time_s)
        R = self.ejecta_velocity * time_s
        sigma = 5.670374419e-8  # Stefan-Boltzmann constant

        if R > 0:
            return (L / (4 * np.pi * R**2 * sigma))**(1/4)
        return 0

    def peak_magnitude_absolute(self) -> float:
        """
        Approximate absolute magnitude at peak

        Typical kilonova: M_peak ~ -15 to -17
        """
        L_peak = self.bolometric_luminosity(self.diffusion_timescale)
        # L_sun corresponds to M = 4.83
        M = 4.83 - 2.5 * np.log10(L_peak / L_sun)
        return M


# =============================================================================
# R-PROCESS NUCLEOSYNTHESIS
# =============================================================================

# Elements produced in r-process (atomic number Z, mass fraction estimate)
R_PROCESS_YIELDS = {
    "Gold (Au)": {"Z": 79, "A": 197, "fraction": 0.001},
    "Platinum (Pt)": {"Z": 78, "A": 195, "fraction": 0.002},
    "Uranium (U)": {"Z": 92, "A": 238, "fraction": 0.0001},
    "Europium (Eu)": {"Z": 63, "A": 152, "fraction": 0.0005},
    "Neodymium (Nd)": {"Z": 60, "A": 144, "fraction": 0.001},
    "Strontium (Sr)": {"Z": 38, "A": 88, "fraction": 0.01},
    "Silver (Ag)": {"Z": 47, "A": 108, "fraction": 0.0005},
    "Iodine (I)": {"Z": 53, "A": 127, "fraction": 0.0002},
}


def element_mass_produced(element: str, ejecta_mass_solar: float) -> float:
    """Calculate mass of specific element produced in kg"""
    if element in R_PROCESS_YIELDS:
        fraction = R_PROCESS_YIELDS[element]["fraction"]
        return fraction * ejecta_mass_solar * M_sun
    return 0


def earth_masses_of_element(element: str, ejecta_mass_solar: float) -> float:
    """Express mass in Earth masses"""
    M_earth = 5.972e24  # kg
    mass_kg = element_mass_produced(element, ejecta_mass_solar)
    return mass_kg / M_earth


# =============================================================================
# EQUATION OF STATE CONSTRAINTS
# =============================================================================

def tidal_constraint_from_gw170817() -> Dict:
    """
    GW170817 measured the combined tidal deformability

    Λ̃ = (16/13) * [(m1 + 12*m2)*m1^4*Λ1 + (m2 + 12*m1)*m2^4*Λ2] / (m1+m2)^5

    Result: Λ̃ < 800 (90% confidence)

    This constrains the neutron star radius to R < 13.5 km
    """
    return {
        "combined_lambda_90": 800,
        "combined_lambda_50": 300,
        "radius_constraint_km": (10.5, 13.5),
        "implication": "Rules out very stiff equations of state"
    }


def maximum_ns_mass_constraint() -> Dict:
    """
    Constraints on maximum neutron star mass

    GW170817 remnant: ~2.7 M_sun
    - If no prompt collapse: M_max > 2.7 M_sun
    - But GRB delay suggests collapse occurred
    - Combined with pulsar observations: M_max ≈ 2.2-2.3 M_sun
    """
    return {
        "psr_j0740": 2.08,      # Heaviest confirmed NS
        "gw170817_remnant": 2.7,
        "theoretical_max": (2.2, 2.4),
        "implication": "Remnant likely collapsed to black hole"
    }


# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def analyze_gw170817():
    """Complete analysis of GW170817"""

    print("=" * 80)
    print("  BINARY NEUTRON STAR MERGER ANALYSIS: GW170817")
    print("  The First Multi-Messenger Gravitational Wave Detection")
    print("=" * 80)

    # Create neutron star objects
    ns1 = NeutronStar(mass_solar=GW170817["m1_solar"], radius_km=12.0)
    ns2 = NeutronStar(mass_solar=GW170817["m2_solar"], radius_km=11.5)

    print(f"\n{'NEUTRON STAR PROPERTIES':=^80}")
    for i, ns in enumerate([ns1, ns2], 1):
        print(f"\n  Neutron Star {i}:")
        print(f"    Mass:                {ns.mass_solar:.3f} M_sun ({ns.mass:.3e} kg)")
        print(f"    Radius:              {ns.radius_km:.1f} km")
        print(f"    Compactness (GM/Rc²):{ns.compactness:.4f}")
        print(f"    Surface gravity:     {ns.surface_gravity:.3e} m/s² ({ns.surface_gravity/9.81:.2e} g)")
        print(f"    Escape velocity:     {ns.escape_velocity/c:.4f} c ({ns.escape_velocity/1000:.0f} km/s)")
        print(f"    Average density:     {ns.average_density:.3e} kg/m³")
        print(f"                         ({ns.average_density/1e17:.1f} × 10¹⁷ kg/m³)")
        print(f"    Schwarzschild R:     {ns.schwarzschild_radius/1000:.2f} km")
        print(f"    Binding energy:      {ns.binding_energy:.3e} J ({ns.binding_energy/(M_sun*c2):.4f} M_sun c²)")
        print(f"    Tidal deformability: Λ ≈ {ns.tidal_deformability():.0f}")

    # Merger dynamics
    print(f"\n{'MERGER DYNAMICS':=^80}")

    M_c = chirp_mass(ns1.mass, ns2.mass)
    M_total = ns1.mass + ns2.mass

    print(f"\n  Chirp mass:            {M_c/M_sun:.4f} M_sun")
    print(f"  Total mass:            {M_total/M_sun:.3f} M_sun")

    # Contact parameters
    r_contact = separation_at_contact(ns1.radius, ns2.radius)
    f_contact = gw_frequency_at_separation(M_total, r_contact)
    v_contact = orbital_velocity_at_separation(M_total, r_contact)

    print(f"\n  At Contact:")
    print(f"    Separation:          {r_contact/1000:.1f} km")
    print(f"    GW frequency:        {f_contact:.0f} Hz")
    print(f"    Orbital velocity:    {v_contact/c:.3f} c ({v_contact/1000:.0f} km/s)")

    # ISCO (if it were a point mass)
    r_isco = 6 * G * M_total / c2
    f_isco = gw_frequency_at_separation(M_total, r_isco)

    print(f"\n  ISCO (point mass limit):")
    print(f"    ISCO radius:         {r_isco/1000:.1f} km")
    print(f"    ISCO frequency:      {f_isco:.0f} Hz")

    # Inspiral time
    t_inspiral = inspiral_time(M_c, 24, f_contact)
    print(f"\n  Inspiral (24 Hz to contact):")
    print(f"    Duration:            {t_inspiral:.1f} s ({t_inspiral/60:.2f} min)")

    # Energy radiated
    E_gw = energy_radiated_in_gw(M_c, 24, f_contact)
    print(f"\n  Energy radiated in GW:")
    print(f"    Total:               {E_gw:.3e} J")
    print(f"                         {E_gw/(M_sun*c2):.4f} M_sun c²")
    print(f"                         ({E_gw/1e46:.1f} × 10⁴⁶ J)")

    # Kilonova
    print(f"\n{'KILONOVA (AT 2017gfo)':=^80}")

    # GW170817 kilonova parameters (observed)
    kilonova = KilonovaModel(
        ejecta_mass_solar=0.05,      # ~0.05 M_sun ejected
        ejecta_velocity_c=0.2,       # ~0.2c
        opacity_cm2_g=10.0,          # Lanthanide-rich "red" component
    )

    print(f"\n  Ejecta Properties:")
    print(f"    Mass ejected:        {kilonova.ejecta_mass_solar:.3f} M_sun ({kilonova.ejecta_mass:.3e} kg)")
    print(f"    Velocity:            {kilonova.ejecta_velocity_c:.2f} c ({kilonova.ejecta_velocity/1000:.0f} km/s)")
    print(f"    Kinetic energy:      {kilonova.kinetic_energy:.3e} J")
    print(f"                         ({kilonova.kinetic_energy/1e44:.1f} × 10⁴⁴ J)")

    print(f"\n  Light Curve:")
    t_peak = kilonova.diffusion_timescale
    print(f"    Peak time:           {t_peak/86400:.2f} days")
    print(f"    Peak luminosity:     {kilonova.bolometric_luminosity(t_peak):.3e} W")
    print(f"                         ({kilonova.bolometric_luminosity(t_peak)/L_sun:.2e} L_sun)")
    print(f"    Peak absolute mag:   {kilonova.peak_magnitude_absolute():.1f}")

    print(f"\n  Temperature evolution:")
    for t_days in [0.5, 1, 2, 5, 10]:
        t_s = t_days * 86400
        T = kilonova.temperature_blackbody(t_s)
        L = kilonova.bolometric_luminosity(t_s)
        print(f"    t = {t_days:.1f} day:  T = {T:.0f} K, L = {L:.2e} W")

    # R-process elements
    print(f"\n{'R-PROCESS NUCLEOSYNTHESIS':=^80}")
    print(f"\n  Heavy elements synthesized in this single event:")
    print(f"  (Estimated from ejecta mass = {kilonova.ejecta_mass_solar:.3f} M_sun)\n")

    for element, data in R_PROCESS_YIELDS.items():
        mass_kg = element_mass_produced(element, kilonova.ejecta_mass_solar)
        mass_earth = earth_masses_of_element(element, kilonova.ejecta_mass_solar)
        print(f"    {element:20s}: {mass_kg:.3e} kg = {mass_earth:.4f} Earth masses")

    # Gold calculation specifically
    gold_mass = element_mass_produced("Gold (Au)", kilonova.ejecta_mass_solar)
    gold_earth = earth_masses_of_element("Gold (Au)", kilonova.ejecta_mass_solar)
    print(f"\n  >> This single merger produced ~{gold_earth:.2f} Earth masses of GOLD!")
    print(f"     ({gold_mass:.2e} kg = {gold_mass/1e12:.0f} million metric tons)")

    # EOS constraints
    print(f"\n{'EQUATION OF STATE CONSTRAINTS':=^80}")

    tidal = tidal_constraint_from_gw170817()
    print(f"\n  Tidal deformability constraint:")
    print(f"    Λ̃ < {tidal['combined_lambda_90']} (90% confidence)")
    print(f"    Implies R < {tidal['radius_constraint_km'][1]} km")
    print(f"    {tidal['implication']}")

    mass_const = maximum_ns_mass_constraint()
    print(f"\n  Maximum NS mass:")
    print(f"    Heaviest known pulsar:  {mass_const['psr_j0740']:.2f} M_sun (PSR J0740+6620)")
    print(f"    GW170817 remnant:       {mass_const['gw170817_remnant']:.1f} M_sun")
    print(f"    Theoretical M_max:      {mass_const['theoretical_max'][0]:.1f}-{mass_const['theoretical_max'][1]:.1f} M_sun")
    print(f"    {mass_const['implication']}")

    # Multi-messenger summary
    print(f"\n{'MULTI-MESSENGER OBSERVATIONS':=^80}")
    print(f"""
  Timeline of GW170817:

  t = -100 s     Gravitational waves enter LIGO band (f > 24 Hz)
  t = 0          Merger (GW signal ends)
  t = +1.7 s     Gamma-ray burst GRB 170817A detected (Fermi, INTEGRAL)
  t = +11 hours  Optical counterpart found (AT 2017gfo in NGC 4993)
  t = +9 days    X-ray emission detected (Chandra)
  t = +16 days   Radio emission detected (VLA)

  This was the FIRST time we observed:
  - Gravitational waves AND light from the same cosmic event
  - Direct proof that neutron star mergers create heavy elements
  - A "kilonova" - the radioactive glow of r-process elements
  - The origin of short gamma-ray bursts CONFIRMED
    """)

    # Cosmic implications
    print(f"\n{'COSMIC IMPLICATIONS':=^80}")
    print(f"""
  Rate of NS-NS mergers in Milky Way: ~1 per 10,000-100,000 years

  Heavy element budget:
  - All gold on Earth (~200,000 tons): from ancient NS mergers
  - GW170817 alone: ~10 Earth masses of gold created
  - NS mergers likely produce MOST of the universe's heavy elements

  Hubble constant measurement:
  - GW170817 provided independent H₀ = 70 ± 12 km/s/Mpc
  - "Standard siren" method (no cosmic distance ladder needed)
  - May help resolve H₀ tension with more events
    """)

    print("=" * 80)
    print("  Analysis complete!")
    print("=" * 80)

    return {
        "ns1": ns1,
        "ns2": ns2,
        "kilonova": kilonova,
        "chirp_mass_solar": M_c / M_sun,
        "energy_radiated_gw": E_gw,
        "gold_produced_kg": gold_mass,
    }


def parameter_study():
    """Study how signal changes with NS masses"""

    print("\n" + "=" * 80)
    print("  PARAMETER STUDY: NS MASS VARIATIONS")
    print("=" * 80)

    mass_pairs = [
        (1.2, 1.2, "Light equal mass"),
        (1.35, 1.35, "Typical equal mass"),
        (1.4, 1.4, "Chandrasekhar mass"),
        (1.6, 1.2, "Asymmetric"),
        (2.0, 1.4, "Heavy primary"),
        (2.0, 2.0, "Maximum mass pair"),
    ]

    print(f"\n  {'Configuration':<25} {'M_chirp':>10} {'f_ISCO':>10} {'t_insp':>12} {'E_GW':>12}")
    print(f"  {'':25} {'(M_sun)':>10} {'(Hz)':>10} {'(s)':>12} {'(M_sun c²)':>12}")
    print("-" * 80)

    for m1, m2, label in mass_pairs:
        M1 = m1 * M_sun
        M2 = m2 * M_sun
        M_c = chirp_mass(M1, M2)
        M_total = M1 + M2

        # Approximate contact frequency (assuming 12 km radius each)
        r_contact = 24e3  # 24 km
        f_contact = gw_frequency_at_separation(M_total, r_contact)

        t_insp = inspiral_time(M_c, 20, min(f_contact, 2000))
        E_gw = energy_radiated_in_gw(M_c, 20, min(f_contact, 2000))

        print(f"  {label:<25} {M_c/M_sun:>10.4f} {f_contact:>10.0f} {t_insp:>12.1f} {E_gw/(M_sun*c2):>12.5f}")

    print("-" * 80)


if __name__ == "__main__":
    results = analyze_gw170817()
    parameter_study()

    # Save results
    output = {
        "event": "GW170817",
        "chirp_mass_solar": results["chirp_mass_solar"],
        "energy_gw_joules": results["energy_radiated_gw"],
        "gold_produced_kg": results["gold_produced_kg"],
        "gold_earth_masses": results["gold_produced_kg"] / 5.972e24,
    }

    with open("/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/gravitational_waves/gw170817_analysis.json", "w") as f:
        json.dump(output, f, indent=2)

    print("\n✓ Results saved to gw170817_analysis.json")
