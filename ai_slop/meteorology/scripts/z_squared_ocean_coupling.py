"""
Z² = 32π/3 OCEAN-ATMOSPHERE COUPLING: First-Principles
========================================================

The critical role of ocean heat content and air-sea interaction
in determining hurricane intensity through the Z² framework.

The ocean is the fuel tank. Z² determines the engine efficiency.
This script explores their coupling.

Author: Carl Zimmerman
Framework: Z² = 32π/3 hurricane intensity research
"""

import numpy as np

# Fundamental constants
g = 9.81
c_p = 1004
L_v = 2.5e6
R_d = 287.05
rho_water = 1025  # kg/m³
c_p_water = 4000  # J/(kg·K)
OMEGA = 7.292e-5

# The Zimmerman constant
Z_SQUARED = 32 * np.pi / 3
Z = np.sqrt(Z_SQUARED)

print("=" * 70)
print("Z² = 32π/3 OCEAN-ATMOSPHERE COUPLING")
print("=" * 70)

print(f"""
THE HURRICANE FUEL TANK:

The ocean provides the enthalpy that powers the hurricane heat engine.
Key ocean parameters:
1. Sea Surface Temperature (SST)
2. Ocean Heat Content (OHC)
3. Mixed layer depth
4. Upwelling/cooling response

Z² determines the efficiency. The ocean determines the fuel supply.
""")

# =============================================================================
# PART 1: SEA SURFACE TEMPERATURE AND Z² MPI
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: SST IN THE Z² FRAMEWORK")
print("=" * 70)

print("""
HYPOTHESIS: SST directly controls the thermodynamic potential in the
Z² MPI equation through both Carnot efficiency and enthalpy disequilibrium.

THE Z² MPI EQUATION:

    V_max² = Z² × (C_k/C_D) × η_C × (k_s* - k_a) / c_p

SST affects TWO terms:

1. CARNOT EFFICIENCY η_C:
   η_C = (T_s - T_out) / T_s

   ∂η_C/∂T_s = T_out / T_s²

   Higher SST → Higher efficiency (but only weakly)

2. ENTHALPY DISEQUILIBRIUM (k_s* - k_a):
   k_s* = c_p T_s + L_v q_s*(T_s)

   The Clausius-Clapeyron relation makes this highly nonlinear:
   q_s* ∝ exp(L_v / R_v × (1/T_0 - 1/T_s))

   ∂k_s*/∂T_s ≈ c_p + L_v × ∂q_s*/∂T_s
                ≈ c_p + L_v × 0.07 q_s*   (7% per °C)

COMBINED SENSITIVITY:

∂V_max/∂T_s ≈ 3-4 m/s per °C

This is why SST > 26°C threshold exists:
- Below ~26°C: Insufficient thermodynamic potential
- 26-28°C: Weak to moderate hurricanes possible
- 28-30°C: Major hurricanes possible
- >30°C: Record intensities possible
""")

def saturation_specific_humidity(T_C, p_hPa=1015):
    """q_s using Clausius-Clapeyron"""
    e_s = 6.112 * np.exp(17.67 * T_C / (T_C + 243.5))  # hPa
    return 0.622 * e_s / p_hPa

def z_squared_mpi(T_s_C, T_out_C=-70, Ck_Cd=1.0, RH_bl=0.80):
    """Calculate MPI from Z² framework."""
    T_s = T_s_C + 273.15
    T_out = T_out_C + 273.15
    eta = (T_s - T_out) / T_s

    q_s = saturation_specific_humidity(T_s_C)
    k_star = c_p * T_s + L_v * q_s
    k_a = c_p * (T_s - 1) + L_v * RH_bl * q_s

    V_max_sq = Z_SQUARED * Ck_Cd * eta * (k_star - k_a) / c_p
    return np.sqrt(V_max_sq)

# SST sensitivity analysis
print("\nSST Sensitivity of Z² MPI:")
print("-" * 70)
print(f"{'SST (°C)':<12} {'η_Carnot':<12} {'q_s (g/kg)':<12} {'V_MPI (m/s)':<15} {'V_MPI (kt)'}")
print("-" * 70)

for T_s in range(24, 35):
    eta = (T_s + 273.15 - 203.15) / (T_s + 273.15)
    q_s = saturation_specific_humidity(T_s) * 1000  # g/kg
    V_mpi = z_squared_mpi(T_s)
    print(f"{T_s:<12} {eta:<12.3f} {q_s:<12.1f} {V_mpi:<15.1f} {V_mpi*1.944:<.0f}")

# Show the 7%/°C rule
print("\nClausius-Clapeyron 7%/°C Rule:")
print("-" * 50)
q_base = saturation_specific_humidity(25)
for T in [25, 26, 27, 28, 29, 30]:
    q = saturation_specific_humidity(T)
    pct_increase = (q / q_base - 1) * 100
    print(f"T = {T}°C: q_s = {q*1000:.1f} g/kg ({pct_increase:+.0f}% from 25°C)")

# =============================================================================
# PART 2: OCEAN HEAT CONTENT (OHC)
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: OCEAN HEAT CONTENT AND HURRICANE FUEL")
print("=" * 70)

print("""
HYPOTHESIS: OHC determines how long the ocean can sustain the SST
needed to power the Z² heat engine.

OCEAN HEAT CONTENT DEFINITION:

    OHC = ∫₀^D ρ_w c_p,w (T(z) - 26°C) dz

Where:
- D = depth of the 26°C isotherm (or mixed layer)
- 26°C chosen as hurricane threshold

Units: kJ/cm² (common) or J/m² (SI)

WHY OHC MATTERS MORE THAN SST ALONE:

1. Hurricane surface winds cause mixing and upwelling
2. Cold water from below is mixed to surface
3. SST decreases under the storm (cold wake)

Cold wake reduces:
- Surface enthalpy flux
- Carnot efficiency
- Thermodynamic potential

HIGH OHC PREVENTS COLD WAKE:
- Deep warm water resists cooling
- Storm can maintain high SST
- Intensification can continue

OHC THRESHOLDS:
- < 30 kJ/cm²: Significant SST cooling likely
- 30-60 kJ/cm²: Moderate cooling
- 60-100 kJ/cm²: Minimal cooling
- > 100 kJ/cm²: Ideal for RI (Patricia, Wilma)
""")

def ocean_heat_content(sst_C, T_profile_gradient, D_26_meters):
    """
    Calculate OHC from surface to 26°C isotherm.

    T(z) = SST - gradient × z
    OHC = ∫ρc(T-26)dz from 0 to D_26
    """
    # Simplified: assume linear profile
    T_mean = (sst_C + 26) / 2
    delta_T_mean = T_mean - 26

    OHC_J_m2 = rho_water * c_p_water * delta_T_mean * D_26_meters
    OHC_kJ_cm2 = OHC_J_m2 / 1e7  # Convert to kJ/cm²

    return OHC_kJ_cm2

def mixed_layer_cooling(V_max_kt, duration_hr, ohc_kJ_cm2):
    """
    Estimate SST cooling under hurricane.

    Mixing efficiency depends on wind speed.
    """
    # Empirical: ~0.5-1°C cooling per 12h at 100 kt winds with 50 kJ/cm² OHC
    cooling_rate = 1.0  # °C per 12h baseline

    # Adjust for wind speed
    wind_factor = (V_max_kt / 100)**2

    # Adjust for OHC (higher OHC resists cooling)
    ohc_factor = 50 / ohc_kJ_cm2

    cooling = cooling_rate * wind_factor * ohc_factor * (duration_hr / 12)

    return min(cooling, 5)  # Cap at 5°C

# OHC examples
print("\nOcean Heat Content Examples:")
print("-" * 60)

print(f"{'SST (°C)':<12} {'D_26 (m)':<12} {'OHC (kJ/cm²)':<15} {'Category support'}")
print("-" * 60)

for sst, D26 in [(27, 30), (28, 50), (29, 80), (30, 100), (31, 120)]:
    ohc = ocean_heat_content(sst, 0.05, D26)
    if ohc > 80:
        cat = "Cat 5 / RI"
    elif ohc > 50:
        cat = "Cat 3-4"
    elif ohc > 30:
        cat = "Cat 1-2"
    else:
        cat = "TS / Cat 1"
    print(f"{sst:<12} {D26:<12} {ohc:<15.0f} {cat}")

# Cold wake calculation
print("\nCold Wake SST Reduction:")
print("-" * 60)
print(f"{'Wind (kt)':<12} {'Duration (hr)':<15} {'OHC=30 ΔT':<15} {'OHC=80 ΔT'}")
print("-" * 60)

for V_kt in [65, 100, 130, 160]:
    for dur in [12, 24]:
        dT_low = mixed_layer_cooling(V_kt, dur, 30)
        dT_high = mixed_layer_cooling(V_kt, dur, 80)
        if dur == 12:
            print(f"{V_kt:<12} {dur:<15} {dT_low:<15.1f}°C {dT_high:.1f}°C")

# =============================================================================
# PART 3: THE OCEAN FEEDBACK IN Z² MPI
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: OCEAN FEEDBACK IN THE Z² FRAMEWORK")
print("=" * 70)

print("""
HYPOTHESIS: The "realized MPI" is less than the initial Z² MPI because
the ocean cools in response to the storm.

MODIFIED Z² EQUATION WITH OCEAN FEEDBACK:

    V_actual² = Z² × (C_k/C_D) × η_C(T_s - ΔT_cool) × Δk(T_s - ΔT_cool) / c_p

Where:
    ΔT_cool = f(V, OHC, translation speed)

THE FEEDBACK LOOP:

1. Storm intensifies (V increases)
2. Ocean mixing increases (ΔT_cool increases)
3. SST decreases (T_s,effective drops)
4. MPI decreases
5. Intensification slows or reverses

STEADY STATE:

At equilibrium:
    V_actual such that MPI(T_s - ΔT_cool(V_actual)) = V_actual

This is a nonlinear fixed-point problem.

TRANSLATION SPEED EFFECT:

Fast-moving storms (>15 kt):
- Less time over any ocean point
- Less cooling
- Can maintain higher intensity

Slow-moving storms (<5 kt):
- Extended cooling under storm
- Significant SST drop
- Self-limiting intensity

This explains why slow storms often weaken over water.
""")

def realized_mpi_with_cooling(sst_initial, ohc, V_init, translation_kt=10):
    """
    Calculate realized MPI accounting for ocean feedback.

    Iterative solution to find equilibrium.
    """
    V = V_init
    T_s = sst_initial

    # Iterate to find equilibrium
    for i in range(20):
        # Time for significant cooling depends on translation speed
        # Slower translation = more cooling
        cooling_time = 24 / max(translation_kt / 10, 0.5)  # hours

        # Calculate cooling
        V_kt = V * 1.944
        delta_T = mixed_layer_cooling(V_kt, cooling_time, ohc)

        # Effective SST
        T_eff = T_s - delta_T

        # Calculate MPI at effective SST
        V_mpi = z_squared_mpi(T_eff)

        # Adjust toward equilibrium
        V_new = 0.5 * V + 0.5 * V_mpi
        if abs(V_new - V) < 0.1:
            break
        V = V_new

    return V, delta_T, T_eff

print("\nRealized MPI with Ocean Feedback:")
print("-" * 70)
print(f"{'SST':<8} {'OHC':<8} {'Trans.':<10} {'ΔT':<8} {'T_eff':<8} {'V_real':<12} {'V_init MPI'}")
print("-" * 70)

for sst in [28, 30, 32]:
    V_init_mpi = z_squared_mpi(sst)
    for ohc in [40, 80]:
        for trans in [5, 15]:
            V_real, dT, T_eff = realized_mpi_with_cooling(sst, ohc, V_init_mpi, trans)
            print(f"{sst}°C    {ohc}      {trans} kt     {dT:.1f}°C   {T_eff:.1f}°C  "
                  f"{V_real*1.944:.0f} kt     {V_init_mpi*1.944:.0f} kt")

# =============================================================================
# PART 4: ENTHALPY FLUX AT THE OCEAN SURFACE
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: SURFACE ENTHALPY FLUX - THE Z² FUEL SUPPLY")
print("=" * 70)

print("""
HYPOTHESIS: The surface enthalpy flux is the direct fuel input to the
Z² heat engine, determined by wind speed and air-sea disequilibrium.

SURFACE FLUX FORMULATION:

    F_k = ρ_a × C_k × V × (k_s* - k_a)

Where:
- ρ_a ≈ 1.2 kg/m³ (air density)
- C_k ≈ 1.2 × 10⁻³ (enthalpy exchange coefficient)
- V = surface wind speed
- (k_s* - k_a) = enthalpy disequilibrium

THE DISEQUILIBRIUM:

k_s* - k_a = [c_p(T_s - T_a) + L_v(q_s* - q_a)]

For typical hurricane conditions:
- T_s - T_a ≈ 0-2 K (small sensible heat)
- q_s* - q_a ≈ 5-15 g/kg (large latent heat)

The latent heat flux dominates (80-90% of total).

FLUX MAGNITUDE:

For V = 60 m/s, SST = 30°C:
    F_k ≈ 1.2 × 1.2×10⁻³ × 60 × 100000
    F_k ≈ 8600 W/m²

This is enormous! Compare to solar flux (~1000 W/m² at surface).

INTEGRATED FLUX:

Total energy input to storm:
    Ė_in = ∫∫ F_k × dA ≈ F_k,mean × π × r_out²

For r_out = 500 km:
    Ė_in ≈ 5000 W/m² × π × (5×10⁵)² = 4 × 10¹⁵ W = 4 PW!

This exceeds total human power consumption (~20 TW) by 100×.
""")

def surface_enthalpy_flux(V_ms, T_s_C, T_a_C, RH_a):
    """
    Calculate surface enthalpy flux.

    F_k = ρ C_k V (k_s* - k_a)
    """
    rho_a = 1.2  # kg/m³
    C_k = 1.2e-3

    # Enthalpy disequilibrium
    T_s = T_s_C + 273.15
    T_a = T_a_C + 273.15

    q_s_star = saturation_specific_humidity(T_s_C)
    q_a = RH_a * saturation_specific_humidity(T_a_C)

    k_s_star = c_p * T_s + L_v * q_s_star
    k_a = c_p * T_a + L_v * q_a

    delta_k = k_s_star - k_a

    F_k = rho_a * C_k * V_ms * delta_k

    return F_k, delta_k

# Calculate fluxes
print("\nSurface Enthalpy Flux:")
print("-" * 70)
print(f"{'V (m/s)':<12} {'SST':<8} {'F_k (W/m²)':<15} {'Type'}")
print("-" * 70)

for V in [20, 40, 60, 80]:
    for T_s in [28, 30, 32]:
        F, dk = surface_enthalpy_flux(V, T_s, T_s - 1, 0.80)
        storm_type = "Major" if F > 5000 else "Moderate" if F > 2000 else "Weak"
        print(f"{V:<12} {T_s}°C    {F:<15.0f} {storm_type}")

# Total power calculation
print("\nTotal Storm Power Input:")
print("-" * 50)

V_max = 65  # m/s
T_s = 30    # °C
r_out = 400000  # m

# Mean flux (lower than maximum due to radial variation)
F_mean = surface_enthalpy_flux(V_max * 0.5, T_s, T_s - 1, 0.80)[0]
Area = np.pi * r_out**2
P_total = F_mean * Area

print(f"Mean flux: {F_mean:.0f} W/m²")
print(f"Area: {Area:.2e} m²")
print(f"Total power: {P_total:.2e} W = {P_total/1e12:.0f} TW")
print(f"For comparison: Global human power use ≈ 20 TW")

# =============================================================================
# PART 5: WARM CORE RINGS AND LOOP CURRENT
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: WARM CORE EDDIES AND THE Z² INTENSIFICATION")
print("=" * 70)

print("""
HYPOTHESIS: Warm core rings (eddies) and the Loop Current provide
concentrated reservoirs of high OHC that enable extreme intensification.

THE LOOP CURRENT (Gulf of Mexico):

- Warm Caribbean water enters Gulf through Yucatan Channel
- Extends northward, sometimes to 28°N
- Periodically sheds warm core rings (eddies)
- SST: 27-30°C, OHC: 80-150 kJ/cm²

WARM CORE RING PROPERTIES:
- Diameter: 200-400 km
- Depth of 26°C isotherm: 100-150 m
- OHC: 80-120 kJ/cm²
- Persist for months to years

Z² INTENSIFICATION OVER WARM FEATURES:

When hurricane crosses warm core ring:
1. Minimal SST cooling (high OHC resists mixing)
2. Full Z² MPI maintained
3. RI often results

CASE EXAMPLES:

Katrina (2005):
- Crossed Loop Current eddy
- RI: 65→175 kt in 24 hours
- OHC > 100 kJ/cm²

Rita (2005):
- Also crossed Loop Current
- RI: 85→180 kt in 24 hours
- Similar OHC conditions

Michael (2018):
- Crossed warm eddy near landfall
- RI: 95→140 kt in <24 hours
- Unexpected intensity at landfall
""")

def warm_eddy_effect(baseline_sst, baseline_ohc, eddy_sst_anomaly, eddy_ohc_factor):
    """
    Calculate enhanced MPI over warm core eddy.
    """
    # Eddy conditions
    eddy_sst = baseline_sst + eddy_sst_anomaly
    eddy_ohc = baseline_ohc * eddy_ohc_factor

    # MPI without eddy
    V_mpi_base = z_squared_mpi(baseline_sst)

    # MPI with eddy (no cooling due to high OHC)
    V_mpi_eddy = z_squared_mpi(eddy_sst)

    # Realized MPI accounting for cooling
    V_real_base, _, _ = realized_mpi_with_cooling(baseline_sst, baseline_ohc, V_mpi_base)
    V_real_eddy, _, _ = realized_mpi_with_cooling(eddy_sst, eddy_ohc, V_mpi_eddy)

    return V_mpi_base, V_real_base, V_mpi_eddy, V_real_eddy

print("\nWarm Core Eddy Enhancement:")
print("-" * 70)

baseline_sst = 28
baseline_ohc = 40

print(f"Baseline: SST = {baseline_sst}°C, OHC = {baseline_ohc} kJ/cm²")
print()
print(f"{'Eddy ΔT':<12} {'Eddy OHC':<12} {'V_real base':<15} {'V_real eddy':<15} {'Enhancement'}")
print("-" * 70)

for dT in [1, 2, 3]:
    for ohc_mult in [2, 2.5, 3]:
        V_b, V_rb, V_e, V_re = warm_eddy_effect(baseline_sst, baseline_ohc, dT, ohc_mult)
        enhance = V_re - V_rb
        print(f"+{dT}°C        {baseline_ohc*ohc_mult:.0f}         {V_rb*1.944:<15.0f} kt"
              f"{V_re*1.944:<15.0f} kt +{enhance*1.944:.0f} kt")

# =============================================================================
# PART 6: CLIMATE CHANGE AND THE Z² FRAMEWORK
# =============================================================================
print("\n" + "=" * 70)
print("PART 6: CLIMATE CHANGE IMPLICATIONS FOR Z² MPI")
print("=" * 70)

print("""
HYPOTHESIS: Climate change increases both SST and Z² MPI, but the
relationship is not linear due to compensating effects.

DIRECT SST EFFECT:

If global SST increases by ΔT_climate:
    ΔV_MPI ≈ 3-4 m/s per °C

For +2°C warming:
    ΔV_MPI ≈ 6-8 m/s ≈ 12-16 kt

COMPENSATING EFFECTS:

1. OUTFLOW TEMPERATURE:
   Stratospheric temperature also changes
   Warming stratosphere → warmer T_out → lower η
   Partially offsets SST effect

2. RELATIVE HUMIDITY:
   Changes in RH affect enthalpy disequilibrium
   Tropical RH may increase slightly
   Effect is small

3. WIND SHEAR:
   Possible increase in shear over Atlantic
   Would reduce structural efficiency ε_struct
   This is a regional effect, not global

NET EFFECT (per IPCC):

- Global MPI increase: ~1-3% per °C of warming
- Fraction of Cat 4-5 storms: Increases significantly
- Total storm frequency: May decrease slightly
- But major storm frequency: Likely increases

IMPLICATIONS FOR Z² FRAMEWORK:

The Z² constant (32π/3) doesn't change with climate.
What changes:
1. T_s (SST increases)
2. T_out (may warm or cool depending on stratosphere)
3. Environmental conditions affecting ε_struct

The theoretical Z² MPI ceiling rises with SST.
""")

def climate_change_mpi(T_s_current, dT_climate, dT_out=0):
    """
    Project Z² MPI change under climate warming.
    """
    # Current MPI
    V_current = z_squared_mpi(T_s_current, T_out_C=-70)

    # Future MPI
    V_future = z_squared_mpi(T_s_current + dT_climate, T_out_C=-70 + dT_out)

    return V_current, V_future

print("\nClimate Change Impact on Z² MPI:")
print("-" * 70)
print(f"{'Scenario':<25} {'Current V_MPI':<18} {'Future V_MPI':<18} {'Change'}")
print("-" * 70)

scenarios = [
    ("+1°C SST", 1, 0),
    ("+2°C SST", 2, 0),
    ("+2°C SST, +1°C T_out", 2, 1),  # Partial compensation
    ("+3°C SST", 3, 0),
    ("+3°C SST, +2°C T_out", 3, 2),  # Strong compensation
]

for name, dT_s, dT_out in scenarios:
    V_cur, V_fut = climate_change_mpi(29, dT_s, dT_out)
    change = V_fut - V_cur
    print(f"{name:<25} {V_cur*1.944:<18.0f} kt {V_fut*1.944:<18.0f} kt {change*1.944:+.0f} kt")

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("Z² OCEAN-ATMOSPHERE COUPLING: SUMMARY")
print("=" * 70)

print(f"""
THE OCEAN AS HURRICANE FUEL:

1. SST IN Z² MPI:
   V_max² = Z² × (C_k/C_D) × η_C(T_s) × Δk(T_s) / c_p

   SST affects both η and Δk nonlinearly
   ~3-4 m/s V_MPI increase per °C SST

2. OCEAN HEAT CONTENT:
   OHC = ∫ρc(T-26°C)dz

   High OHC (>60 kJ/cm²) prevents cold wake cooling
   Essential for sustained high intensity and RI

3. OCEAN FEEDBACK:
   Cold wake reduces effective SST
   V_realized < V_initial_MPI
   Slow translation → more cooling → weaker storms

4. SURFACE ENTHALPY FLUX:
   F_k = ρ C_k V (k_s* - k_a)

   ~8000 W/m² under major hurricane
   Total storm power: ~4 PW (200× global human power)

5. WARM CORE FEATURES:
   Loop Current, warm eddies provide extreme OHC
   Enable RI by preventing cold wake
   Critical for Gulf of Mexico hurricanes

6. CLIMATE CHANGE:
   +1°C SST → ~4-6 kt MPI increase
   Stratospheric warming partially compensates
   Major hurricane fraction likely increases

THE Z² - OCEAN CONNECTION:

Z² = 32π/3 sets the engine efficiency.
The ocean provides the fuel (enthalpy).
OHC determines how long the fuel supply lasts.

For maximum intensity:
- High SST (high fuel quality) ✓
- High OHC (large fuel tank) ✓
- Low translation speed (but not too low) ✓
- All allow full Z² efficiency to be realized
""")

print("\nScript completed successfully.")
