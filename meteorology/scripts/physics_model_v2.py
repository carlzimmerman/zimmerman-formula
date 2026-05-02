#!/usr/bin/env python3
"""
PHYSICS-BASED INTENSITY MODEL v2.0
===================================

Building on first principles with:
1. Ocean Heat Content (OHC) integration
2. Stability-based ERC prediction
3. Forward speed effects
4. Ocean feedback (upwelling)
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

print("=" * 70)
print("PHYSICS-BASED INTENSITY MODEL v2.0")
print("=" * 70)

# =============================================================================
# PHYSICAL CONSTANTS
# =============================================================================
L_v = 2.5e6        # Latent heat (J/kg)
c_p = 1005         # Specific heat of air (J/kg/K)
c_w = 4186         # Specific heat of water (J/kg/K)
rho_air = 1.15     # Air density (kg/m³)
rho_water = 1025   # Water density (kg/m³)
OMEGA = 7.292e-5   # Earth rotation (rad/s)

# Exchange coefficients
C_k = 1.2e-3
C_d = 1.5e-3

@dataclass
class OceanState:
    """Ocean thermal structure."""
    sst: float           # Sea surface temperature (°C)
    ohc: float           # Ocean heat content (kJ/cm²)
    mixed_layer_depth: float  # Mixed layer depth (m)
    thermocline_gradient: float  # °C per 100m below mixed layer

@dataclass
class AtmosphericState:
    """Environmental atmospheric conditions."""
    shear_magnitude: float   # Wind shear (m/s)
    shear_direction: float   # Shear direction relative to motion (degrees)
    relative_humidity: float  # Mid-level RH (0-1)
    outflow_temp: float      # Outflow temperature (°C)

@dataclass
class StormState:
    """Hurricane state variables."""
    vmax: float          # Maximum sustained wind (m/s)
    rmw: float           # Radius of maximum wind (km)
    eye_radius: float    # Eye radius (km)
    central_pressure: float  # Central pressure (mb)
    latitude: float      # Position (degrees N)
    forward_speed: float  # Translation speed (m/s)
    in_erc: bool         # Currently in ERC?
    erc_progress: float  # ERC completion (0-1)


# =============================================================================
# PART 1: ENHANCED MPI WITH OHC
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: OHC-ENHANCED MPI")
print("=" * 70)

def saturation_specific_humidity(T_celsius: float) -> float:
    """Saturation specific humidity (kg/kg)."""
    e_sat = 6.11 * np.exp(17.27 * T_celsius / (T_celsius + 237.3))
    return 0.622 * e_sat / (1013 - 0.378 * e_sat)

def compute_mpi(ocean: OceanState, atm: AtmosphericState) -> float:
    """
    Compute MPI with OHC correction.

    High OHC means the ocean can sustain energy transfer longer,
    effectively increasing the MPI a storm can achieve.
    """
    T_s = ocean.sst + 273.15
    T_o = atm.outflow_temp + 273.15

    # Base thermodynamic calculation
    q_star = saturation_specific_humidity(ocean.sst)
    q_air = atm.relative_humidity * saturation_specific_humidity(ocean.sst - 1)
    delta_k = c_p * 1.0 + L_v * (q_star - q_air)

    eta = (T_s - T_o) / T_o
    v_mpi_base = np.sqrt(max(0, (C_k/C_d) * eta * delta_k))

    # OHC correction factor
    # Higher OHC means storm can extract more energy before cooling surface
    # Reference OHC = 50 kJ/cm² (typical threshold)
    ohc_factor = 1.0 + 0.15 * np.log(max(1, ocean.ohc / 50))

    # Humidity correction (dry air reduces MPI)
    rh_factor = 0.8 + 0.2 * atm.relative_humidity

    v_mpi = v_mpi_base * ohc_factor * rh_factor

    return v_mpi

print("""
OHC-Enhanced MPI adds:
1. OHC factor: MPI × (1 + 0.15 × ln(OHC/50))
   - OHC = 50: factor = 1.0 (baseline)
   - OHC = 100: factor = 1.10 (+10% MPI)
   - OHC = 150: factor = 1.16 (+16% MPI)

2. Humidity factor: Dry air reduces efficiency
""")

# Demonstrate OHC effect
print("\nMPI at SST=28°C for different OHC levels:")
print("-" * 50)
atm = AtmosphericState(shear_magnitude=5, shear_direction=0,
                        relative_humidity=0.8, outflow_temp=-70)
for ohc in [30, 50, 75, 100, 125, 150]:
    ocean = OceanState(sst=28, ohc=ohc, mixed_layer_depth=50, thermocline_gradient=0.5)
    mpi = compute_mpi(ocean, atm)
    print(f"  OHC = {ohc:3d} kJ/cm²: MPI = {mpi:.1f} m/s = {mpi*1.944:.0f} kt")


# =============================================================================
# PART 2: OCEAN FEEDBACK (UPWELLING/COOLING)
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: OCEAN FEEDBACK MODEL")
print("=" * 70)

def compute_ocean_cooling(
    storm: StormState,
    ocean: OceanState,
    dt_hours: float
) -> float:
    """
    Compute SST cooling due to storm-induced mixing.

    Slow-moving storms cause more upwelling and cooling.
    Deep mixed layers and high OHC resist cooling.
    """
    # Mixing depth increases with intensity
    mixing_depth = 30 + storm.vmax * 0.5  # meters

    # Time over a given point depends on storm size and speed
    # Residence time ~ RMW / forward_speed
    residence_time = (storm.rmw * 1000) / max(1, storm.forward_speed) / 3600  # hours

    # Cooling rate depends on:
    # 1. How deep we mix (mixing_depth)
    # 2. Temperature gradient below mixed layer
    # 3. How long storm sits there (residence time)

    if mixing_depth > ocean.mixed_layer_depth:
        # Mixing into thermocline - brings up cold water
        extra_depth = mixing_depth - ocean.mixed_layer_depth
        temp_deficit = extra_depth * ocean.thermocline_gradient / 100

        # Cooling is proportional to residence time
        cooling = temp_deficit * min(1, residence_time / 12)
    else:
        # Not mixing deep enough - minimal cooling
        cooling = 0.1 * residence_time / 24

    # OHC resistance: high OHC means more heat reservoir
    ohc_resistance = 1 / (1 + ocean.ohc / 100)

    return cooling * ohc_resistance

print("""
Ocean Feedback Physics:
- Slow storms (< 5 m/s) cause significant SST cooling
- Deep mixed layers (> 50m) resist cooling
- High OHC provides thermal inertia
- Cooling reduces effective MPI for trailing portions of storm
""")

# Demonstrate forward speed effect
print("\nSST cooling for a 140 kt storm vs forward speed:")
print("-" * 50)
ocean = OceanState(sst=29, ohc=75, mixed_layer_depth=40, thermocline_gradient=0.8)
for speed_kt in [5, 10, 15, 20, 25]:
    speed_ms = speed_kt * 0.514
    storm = StormState(vmax=72, rmw=25, eye_radius=10, central_pressure=935,
                       latitude=25, forward_speed=speed_ms, in_erc=False, erc_progress=0)
    cooling = compute_ocean_cooling(storm, ocean, 12)
    print(f"  Forward speed = {speed_kt:2d} kt: SST cooling = {cooling:.2f}°C")


# =============================================================================
# PART 3: STABILITY-BASED ERC PREDICTION
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: ERC PREDICTION FROM VORTEX STABILITY")
print("=" * 70)

def compute_erc_probability(storm: StormState, ocean: OceanState) -> Tuple[float, str]:
    """
    Compute probability of ERC onset from vortex stability theory.

    ERCs occur when:
    1. Intensity is high (V > ~140 kt typically)
    2. Eye is small (< 15 km)
    3. RMW is contracted (< 30 km)
    4. Filamentation time becomes comparable to convective time
    """
    v_kt = storm.vmax * 1.944

    # Filamentation criterion
    # τ_fil = 1 / (dV/dr) ~ RMW / V_max
    # When τ_fil < convective time (~30 min), eyewall becomes unstable
    filamentation_time = (storm.rmw * 1000) / storm.vmax / 60  # minutes
    convective_time = 30  # minutes (typical)

    fil_factor = convective_time / max(1, filamentation_time)

    # Intensity factor - ERCs rare below ~140 kt
    intensity_threshold = 72  # m/s (~140 kt)
    if storm.vmax < intensity_threshold:
        intensity_factor = 0
    else:
        intensity_factor = (storm.vmax - intensity_threshold) / 20

    # Eye size factor - small eyes more prone to instability
    if storm.eye_radius > 15:
        eye_factor = 0.2
    elif storm.eye_radius > 10:
        eye_factor = 0.5
    else:
        eye_factor = 1.0

    # Combine factors
    probability = min(0.95, intensity_factor * eye_factor * (fil_factor / 2))

    # Generate explanation
    if probability < 0.2:
        reason = "Low: Intensity below ERC threshold"
    elif probability < 0.5:
        reason = f"Moderate: V={v_kt:.0f}kt, Eye={storm.eye_radius:.0f}km"
    else:
        reason = f"High: V={v_kt:.0f}kt, Eye={storm.eye_radius:.0f}km, τ_fil={filamentation_time:.0f}min"

    return probability, reason

def simulate_erc(storm: StormState, duration_hours: int = 18) -> Dict:
    """
    Simulate ERC weakening and recovery.

    ERC typically:
    - Takes 12-24 hours
    - Causes 20-50 kt weakening
    - Eye expands by ~1.6× (golden ratio!)
    - RMW increases
    """
    initial_vmax = storm.vmax

    # Weakening magnitude depends on initial intensity
    # Higher intensity = more weakening
    excess_intensity = max(0, storm.vmax - 72)  # m/s above 140 kt
    weakening_fraction = 0.15 + 0.10 * (excess_intensity / 15)  # 15-25%

    min_vmax = initial_vmax * (1 - weakening_fraction)

    # Recovery - usually back to ~90% of initial
    recovery_vmax = initial_vmax * 0.90

    # Structural changes
    phi = 1.618
    new_eye = storm.eye_radius * phi
    new_rmw = storm.rmw * 1.3

    return {
        'duration': duration_hours,
        'weakening_ms': initial_vmax - min_vmax,
        'weakening_kt': (initial_vmax - min_vmax) * 1.944,
        'min_vmax_kt': min_vmax * 1.944,
        'recovery_vmax_kt': recovery_vmax * 1.944,
        'new_eye_km': new_eye,
        'new_rmw_km': new_rmw,
    }

print("""
ERC Physics:
1. Filamentation instability: When τ_fil < τ_convective
   - Convective cells spiral too quickly
   - Can't maintain coherent eyewall
   - Secondary eyewall forms at larger radius

2. Angular momentum barrier:
   - High V at small r creates strong M gradient
   - Difficult for new convection to penetrate
   - Leads to secondary eyewall formation

3. Weakening mechanism:
   - Outer eyewall starves inner eyewall
   - Inner eye fills, outer contracts
   - ~15-25% intensity loss typical
""")

# Demonstrate ERC prediction
print("\nERC probability at different intensities (eye = 8 km):")
print("-" * 60)
for v_kt in [120, 130, 140, 150, 160, 170, 180]:
    v_ms = v_kt / 1.944
    rmw = max(15, 60 - v_kt/5)  # RMW contracts with intensity
    eye = 8
    storm = StormState(vmax=v_ms, rmw=rmw, eye_radius=eye, central_pressure=920,
                       latitude=20, forward_speed=5, in_erc=False, erc_progress=0)
    ocean = OceanState(sst=29, ohc=80, mixed_layer_depth=50, thermocline_gradient=0.5)
    prob, reason = compute_erc_probability(storm, ocean)
    print(f"  {v_kt:3d} kt: P(ERC) = {prob:.0%} - {reason}")


# =============================================================================
# PART 4: COMPLETE INTENSITY TENDENCY
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: COMPLETE INTENSITY TENDENCY EQUATION")
print("=" * 70)

def intensity_tendency(
    storm: StormState,
    ocean: OceanState,
    atm: AtmosphericState,
) -> float:
    """
    Full intensity tendency equation incorporating all physics.

    dV/dt = Generation - Dissipation - Shear - OceanFeedback - ERC
    """
    # Compute MPI
    mpi = compute_mpi(ocean, atm)

    # Generation term (from thermodynamics)
    alpha = 0.05  # Base intensification rate (1/hr)
    v_scale = 20  # Scale for intensification onset (m/s)

    if mpi > 0:
        generation = alpha * (mpi - storm.vmax) * (1 - np.exp(-storm.vmax / v_scale))
    else:
        generation = 0

    # Shear term (quadratic penalty)
    # Direction matters: shear aligned with motion is less harmful
    shear_factor = 1.0 - 0.3 * np.cos(np.radians(atm.shear_direction))
    effective_shear = atm.shear_magnitude * shear_factor

    beta = 0.003  # Shear sensitivity
    shear_penalty = beta * effective_shear ** 2

    # Dry air penalty (mid-level humidity)
    gamma = 0.02
    dry_air_penalty = gamma * (1 - atm.relative_humidity) * storm.vmax / 50

    # Ocean feedback (cooling effect)
    sst_cooling = compute_ocean_cooling(storm, ocean, 1)
    ocean_penalty = 0.5 * sst_cooling  # m/s reduction per °C cooling

    # ERC effect
    if storm.in_erc:
        # During ERC, strong negative tendency
        erc_penalty = 3.0 * (1 - storm.erc_progress)  # m/s/hr
    else:
        erc_penalty = 0

    # Net tendency
    dv_dt = generation - shear_penalty - dry_air_penalty - ocean_penalty - erc_penalty

    return dv_dt

print("""
Complete tendency equation:

dV/dt = α(MPI-V)(1-e^(-V/V₀)) - β·S_eff² - γ·(1-RH)·V/50 - δ·ΔT - ERC

Where:
- α = 0.05/hr (generation efficiency)
- β = 0.003 (shear sensitivity)
- γ = 0.02 (dry air sensitivity)
- δ = 0.5 m/s per °C SST cooling
- S_eff = shear adjusted for direction relative to motion
""")


# =============================================================================
# PART 5: FULL SIMULATION
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: HELENE SIMULATION WITH FULL PHYSICS")
print("=" * 70)

def simulate_storm(
    initial_vmax_kt: float,
    hours: int,
    ocean_profile: List[OceanState],
    atm_profile: List[AtmosphericState],
    latitude: float = 25,
    forward_speed_kt: float = 15,
) -> List[Dict]:
    """Run full physics simulation."""

    results = []
    v = initial_vmax_kt / 1.944  # Convert to m/s

    # Initial structure
    rmw = 60 - initial_vmax_kt / 5
    eye = rmw * 0.4

    in_erc = False
    erc_progress = 0
    erc_start_v = 0

    for hour in range(hours):
        # Get environmental conditions
        ocean = ocean_profile[min(hour, len(ocean_profile)-1)]
        atm = atm_profile[min(hour, len(atm_profile)-1)]

        # Current storm state
        storm = StormState(
            vmax=v, rmw=rmw, eye_radius=eye,
            central_pressure=1013 - 0.14 * (v * 1.944) ** 1.3,  # Simplified P-V
            latitude=latitude, forward_speed=forward_speed_kt * 0.514,
            in_erc=in_erc, erc_progress=erc_progress
        )

        # Check for ERC onset
        if not in_erc:
            erc_prob, _ = compute_erc_probability(storm, ocean)
            if np.random.random() < erc_prob * 0.1:  # 10% of probability per hour
                in_erc = True
                erc_start_v = v
                erc_progress = 0

        # Update ERC progress
        if in_erc:
            erc_progress += 1 / 18  # 18-hour ERC
            if erc_progress >= 1:
                in_erc = False
                # Eye expands after ERC
                eye = min(25, eye * 1.6)
                rmw = min(50, rmw * 1.3)

        # Compute tendency
        dv_dt = intensity_tendency(storm, ocean, atm)

        # Update intensity
        mpi = compute_mpi(ocean, atm)
        v = max(10, min(mpi, v + dv_dt))

        # Update structure (simplified)
        rmw = max(15, 60 - v * 1.944 / 5)
        if not in_erc:
            eye = rmw * 0.4

        results.append({
            'hour': hour,
            'vmax_kt': v * 1.944,
            'mpi_kt': mpi * 1.944,
            'rmw_km': rmw,
            'eye_km': eye,
            'sst': ocean.sst,
            'ohc': ocean.ohc,
            'shear': atm.shear_magnitude,
            'in_erc': in_erc,
            'tendency': dv_dt * 1.944 * 24,
        })

    return results

# Helene-like simulation
print("\nSimulating Helene with full physics model:")
print("-" * 70)

# Ocean profile: Loop Current encounter
ocean_profile = [
    OceanState(sst=28, ohc=60, mixed_layer_depth=40, thermocline_gradient=0.8),  # Caribbean
    OceanState(sst=28, ohc=60, mixed_layer_depth=40, thermocline_gradient=0.8),
] * 12 + [
    OceanState(sst=29, ohc=90, mixed_layer_depth=60, thermocline_gradient=0.5),  # Loop Current
    OceanState(sst=30, ohc=110, mixed_layer_depth=70, thermocline_gradient=0.4),
    OceanState(sst=30, ohc=120, mixed_layer_depth=75, thermocline_gradient=0.4),
] * 20 + [
    OceanState(sst=29, ohc=80, mixed_layer_depth=50, thermocline_gradient=0.6),  # Near coast
] * 60

# Atmospheric profile: Initially sheared, then favorable
atm_profile = [
    AtmosphericState(shear_magnitude=12, shear_direction=90, relative_humidity=0.70, outflow_temp=-65),
] * 12 + [
    AtmosphericState(shear_magnitude=8, shear_direction=45, relative_humidity=0.75, outflow_temp=-70),
] * 12 + [
    AtmosphericState(shear_magnitude=5, shear_direction=30, relative_humidity=0.80, outflow_temp=-70),
] * 60

# Run simulation
np.random.seed(42)  # For reproducibility
results = simulate_storm(
    initial_vmax_kt=35,
    hours=96,
    ocean_profile=ocean_profile,
    atm_profile=atm_profile,
    latitude=23,
    forward_speed_kt=15,
)

print("Hour | Vmax | MPI  | SST | OHC | Shear | ERC | Tendency")
print("-" * 70)
for r in results[::12]:
    erc_flag = "YES" if r['in_erc'] else ""
    print(f" {r['hour']:3d} | {r['vmax_kt']:4.0f} | {r['mpi_kt']:4.0f} | {r['sst']:.0f}  | {r['ohc']:3.0f} |  {r['shear']:.0f}   | {erc_flag:3s} | {r['tendency']:+5.0f}")

peak = max(results, key=lambda x: x['vmax_kt'])
print(f"\nPeak: {peak['vmax_kt']:.0f} kt at hour {peak['hour']}")
print(f"Helene actual: 140 kt at hour ~90")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("MODEL v2.0 SUMMARY")
print("=" * 70)

print("""
PHYSICS INCORPORATED:

1. EMANUEL MPI with OHC enhancement
   - Base MPI from Carnot heat engine theory
   - OHC factor: MPI × (1 + 0.15·ln(OHC/50))
   - Humidity correction for dry air

2. OCEAN FEEDBACK
   - Upwelling/mixing induced SST cooling
   - Forward speed dependence (slow = more cooling)
   - Mixed layer depth resistance
   - OHC thermal inertia

3. INTENSITY TENDENCY
   - Generation from thermodynamics
   - Shear penalty (direction-dependent)
   - Dry air penalty
   - Ocean cooling penalty

4. ERC DYNAMICS
   - Filamentation instability criterion
   - Intensity and eye size thresholds
   - 18-hour typical duration
   - 15-25% weakening, eye expansion

WHAT'S STILL MISSING:
- Terrain interaction
- Trough interaction
- Diurnal cycle
- Mesoscale features (hot towers, etc.)
- Detailed boundary layer physics

HONEST ASSESSMENT:
This model captures the essential physics better than v1,
but is still simplified compared to full dynamical models.
~20-30 kt errors expected on individual storms.
""")
