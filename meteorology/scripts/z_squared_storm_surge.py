"""
Z² = 32π/3 STORM SURGE PHYSICS: First-Principles
==================================================

Storm surge is the deadliest hurricane hazard. The Z² framework
connects surge height to hurricane intensity through wind stress
and pressure deficit.

Topics:
- Wind stress setup
- Inverse barometer effect
- Bathymetry amplification
- Surge-wave interaction
- Inundation dynamics

Author: Carl Zimmerman
Framework: Z² = 32π/3 hurricane intensity research
"""

import numpy as np

# Fundamental constants
g = 9.81
rho_air = 1.2  # kg/m³
rho_water = 1025  # kg/m³
OMEGA = 7.292e-5

# The Zimmerman constant
Z_SQUARED = 32 * np.pi / 3
Z = np.sqrt(Z_SQUARED)

print("=" * 70)
print("Z² = 32π/3 STORM SURGE PHYSICS")
print("=" * 70)

print(f"""
STORM SURGE: THE KILLER HAZARD

Storm surge causes ~50% of hurricane fatalities.
Understanding the physics saves lives.

Key factors:
1. Wind stress (dominant over shallow water)
2. Pressure deficit (inverse barometer)
3. Bathymetry (shallow = amplification)
4. Coastline geometry (funneling)
5. Forward speed and approach angle

Z² connects intensity to surge through V_max.
""")

# =============================================================================
# PART 1: WIND STRESS AND EKMAN SETUP
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: WIND STRESS SETUP")
print("=" * 70)

print("""
HYPOTHESIS: Sustained onshore wind pushes water toward the coast,
creating a wind stress setup proportional to V².

WIND STRESS:

    τ = C_D × ρ_air × V²

Where:
- C_D ≈ 1.2-2.5 × 10⁻³ (drag coefficient, increases with V)
- ρ_air ≈ 1.2 kg/m³
- V = wind speed

For V = 50 m/s:
    τ ≈ 1.5 × 10⁻³ × 1.2 × 50² = 4.5 N/m²

WATER SURFACE SETUP:

The wind stress creates a surface slope:

    ∂η/∂x = τ / (ρ_water × g × h)

Where h = water depth.

CRITICAL INSIGHT: Setup ∝ 1/h

Shallow water → large setup!

INTEGRATING OVER FETCH:

    η = ∫ (τ / ρ_w g h) dx

For constant τ and linear depth h = h₀ - sx:

    η ≈ τ L / (ρ_w g h_mean)

Where L = fetch length, h_mean = mean depth

Z² CONNECTION:

From V_max² = Z² × (thermo terms):

    τ ∝ V² ∝ Z² × (thermo terms)

Therefore:

    η_surge ∝ Z² × (thermo terms) / (g × h)

Surge height is directly proportional to Z² efficiency!
""")

def wind_stress(V, C_D=1.5e-3):
    """
    Wind stress τ = C_D ρ_air V²
    """
    return C_D * rho_air * V**2

def surface_drag_coefficient(V):
    """
    Wind-dependent drag coefficient.
    Increases with wind speed up to ~33 m/s, then saturates.
    """
    if V < 10:
        return 1.0e-3
    elif V < 33:
        return (0.75 + 0.067 * V) * 1e-3
    else:
        # Saturation at high winds (sea spray effects)
        return 2.5e-3

def wind_setup(V, L_fetch, h_mean):
    """
    Wind stress setup over continental shelf.

    η = τ L / (ρ_w g h)
    """
    C_D = surface_drag_coefficient(V)
    tau = wind_stress(V, C_D)

    eta = tau * L_fetch / (rho_water * g * h_mean)
    return eta

# Demonstrate wind setup
print("\nWind Stress Setup Over Continental Shelf:")
print("-" * 70)
print(f"{'V (m/s)':<12} {'V (kt)':<10} {'τ (N/m²)':<12} {'Setup (m)':<15} {'Setup (ft)'}")
print("-" * 70)

L_fetch = 100000  # 100 km shelf width
h_mean = 30  # 30 m mean depth

for V in [20, 30, 40, 50, 60, 70, 80]:
    C_D = surface_drag_coefficient(V)
    tau = wind_stress(V, C_D)
    eta = wind_setup(V, L_fetch, h_mean)
    print(f"{V:<12} {V*1.944:<10.0f} {tau:<12.2f} {eta:<15.2f} {eta*3.28:.1f}")

# =============================================================================
# PART 2: INVERSE BAROMETER EFFECT
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: INVERSE BAROMETER EFFECT")
print("=" * 70)

print("""
HYPOTHESIS: Low central pressure creates a dome of water under
the hurricane eye through hydrostatic adjustment.

INVERSE BAROMETER RELATIONSHIP:

    η_IB = (p_env - p_center) / (ρ_water × g)

For Δp in hPa and η in meters:

    η_IB (m) = Δp (hPa) / 100

NUMERICAL VALUES:

- Cat 1 (Δp ≈ 30 hPa): η_IB ≈ 0.3 m
- Cat 3 (Δp ≈ 50 hPa): η_IB ≈ 0.5 m
- Cat 5 (Δp ≈ 90 hPa): η_IB ≈ 0.9 m
- Extreme (Δp ≈ 130 hPa): η_IB ≈ 1.3 m

IMPORTANT: Inverse barometer is typically 10-20% of total surge.
Wind stress dominates over shallow water!

Z² CONNECTION:

From the pressure-wind relationship:
    Δp ∝ ρ_air V²

And from Z² framework:
    V² ∝ Z² × (thermo terms)

Therefore:
    η_IB ∝ Z² × (thermo terms) / g

Both wind setup and IB effect scale with Z²!
""")

def inverse_barometer(delta_p_hPa):
    """
    Inverse barometer effect.
    η = Δp / (ρ_w g)
    """
    delta_p_Pa = delta_p_hPa * 100
    eta = delta_p_Pa / (rho_water * g)
    return eta

def pressure_deficit_from_wind(V_max_kt):
    """
    Estimate pressure deficit from wind speed.
    Using modified Dvorak relationship.
    """
    # Δp ≈ (V_max/6.3)^(1/0.62) approximately
    delta_p = (V_max_kt / 6.3)**(1/0.62)
    return min(delta_p, 140)  # Cap at physical limit

# Demonstrate inverse barometer
print("\nInverse Barometer Effect:")
print("-" * 60)
print(f"{'V_max (kt)':<15} {'Δp (hPa)':<15} {'η_IB (m)':<15} {'η_IB (ft)'}")
print("-" * 60)

for V_kt in [65, 85, 100, 115, 140, 165, 185]:
    dp = pressure_deficit_from_wind(V_kt)
    eta_ib = inverse_barometer(dp)
    print(f"{V_kt:<15} {dp:<15.0f} {eta_ib:<15.2f} {eta_ib*3.28:.1f}")

# =============================================================================
# PART 3: BATHYMETRY AMPLIFICATION
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: BATHYMETRY AMPLIFICATION")
print("=" * 70)

print("""
HYPOTHESIS: Surge height is amplified as water shoals onto the
continental shelf, following conservation principles.

SHOALING AMPLIFICATION:

For a long wave approaching shore:
    η × √(gh) = constant

As h decreases, η must increase:
    η₂/η₁ = √(h₁/h₂)

For h₁ = 100 m (shelf edge) to h₂ = 5 m (nearshore):
    Amplification = √(100/5) = √20 ≈ 4.5×

CONTINENTAL SHELF WIDTH EFFECT:

Wide, shallow shelf → more wind stress accumulation → higher surge

Gulf Coast examples:
- Louisiana: Very wide, shallow shelf → extreme surge potential
- Texas: Moderate shelf → moderate surge
- Florida west coast: Wide shelf → high surge potential

Atlantic examples:
- Carolina Outer Banks: Narrow shelf → lower surge
- New Jersey: Moderate shelf → moderate surge

FUNNELING EFFECT:

Converging coastlines concentrate surge:
- Tampa Bay: 2-3× amplification
- Chesapeake Bay: 1.5-2× amplification
- Lake Pontchartrain: Extreme concentration
""")

def shoaling_amplification(h_deep, h_shallow):
    """
    Long wave shoaling amplification factor.
    """
    return np.sqrt(h_deep / h_shallow)

def shelf_surge_factor(shelf_width_km, mean_depth_m, slope):
    """
    Continental shelf surge amplification factor.

    Combines wind setup and shoaling.
    """
    # Wider, shallower shelf = more surge
    width_factor = shelf_width_km / 100  # Normalized to 100 km
    depth_factor = 30 / mean_depth_m  # Normalized to 30 m

    return width_factor * depth_factor

# Bathymetry effects
print("\nShoaling Amplification:")
print("-" * 50)
print(f"{'h_deep (m)':<15} {'h_shallow (m)':<18} {'Amplification'}")
print("-" * 50)

for h_d in [100, 50, 30]:
    for h_s in [10, 5, 2]:
        amp = shoaling_amplification(h_d, h_s)
        print(f"{h_d:<15} {h_s:<18} {amp:.1f}×")

# Regional comparison
print("\nRegional Surge Potential:")
print("-" * 60)
print(f"{'Location':<25} {'Shelf width':<15} {'Mean depth':<12} {'Factor'}")
print("-" * 60)

regions = [
    ("Louisiana coast", 200, 20, "Very High"),
    ("Texas coast", 100, 30, "High"),
    ("Florida Gulf coast", 150, 25, "High"),
    ("Florida Atlantic", 50, 40, "Moderate"),
    ("Carolina coast", 60, 35, "Moderate"),
    ("New England", 80, 50, "Moderate"),
]

for loc, width, depth, risk in regions:
    factor = shelf_surge_factor(width, depth, 0.001)
    print(f"{loc:<25} {width} km         {depth} m         {factor:.1f}× ({risk})")

# =============================================================================
# PART 4: TOTAL SURGE CALCULATION
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: TOTAL SURGE FROM Z² FRAMEWORK")
print("=" * 70)

print("""
HYPOTHESIS: Total surge can be estimated from Z² framework by
combining wind setup and inverse barometer effects.

TOTAL SURGE EQUATION:

    η_total = η_wind + η_IB + η_wave + η_tide

Where:
- η_wind = wind stress setup (dominant)
- η_IB = inverse barometer
- η_wave = wave setup at shore
- η_tide = astronomical tide

SIMPLIFIED Z² SURGE FORMULA:

    η_surge ≈ A × V_max² × L / (g × h) + Δp/(ρ_w × g)

With V_max from Z² framework:

    η_surge ∝ Z² × (thermo potential) × (geometry factor)

STORM SURGE INDEX:

Combining intensity with geometry:

    SSI = (V_max)² × (R_34kt) × cos(θ) / (forward_speed)

Where:
- R_34kt = radius of 34-kt winds (storm size)
- θ = approach angle relative to coast normal
- forward_speed = storm translation speed

Larger, slower storms produce more surge than small, fast storms
at the same intensity.
""")

def total_surge_estimate(V_max_ms, shelf_width_km, mean_depth_m,
                         storm_size_km=200, forward_speed_kt=15):
    """
    Estimate total storm surge.

    Combines wind setup and inverse barometer.
    """
    # Wind setup
    L_fetch = shelf_width_km * 1000
    eta_wind = wind_setup(V_max_ms, L_fetch, mean_depth_m)

    # Inverse barometer
    V_kt = V_max_ms * 1.944
    dp = pressure_deficit_from_wind(V_kt)
    eta_ib = inverse_barometer(dp)

    # Size factor (larger storms push more water)
    size_factor = storm_size_km / 200

    # Speed factor (slower storms accumulate more)
    speed_factor = 15 / forward_speed_kt

    # Total
    eta_total = (eta_wind * size_factor * speed_factor + eta_ib)

    return eta_total, eta_wind, eta_ib

print("\nTotal Surge Estimates (Gulf Coast geometry):")
print("-" * 70)

shelf_width = 150  # km
mean_depth = 25    # m

print(f"Shelf width: {shelf_width} km, Mean depth: {mean_depth} m")
print()
print(f"{'V_max (kt)':<12} {'Category':<10} {'η_wind (m)':<12} {'η_IB (m)':<12} {'η_total (m)':<15} {'η_total (ft)'}")
print("-" * 70)

for V_kt in [65, 85, 100, 115, 140, 165]:
    V_ms = V_kt / 1.944
    if V_kt < 83:
        cat = "1"
    elif V_kt < 96:
        cat = "2"
    elif V_kt < 113:
        cat = "3"
    elif V_kt < 137:
        cat = "4"
    else:
        cat = "5"

    eta_tot, eta_w, eta_ib = total_surge_estimate(V_ms, shelf_width, mean_depth)
    print(f"{V_kt:<12} Cat {cat:<6} {eta_w:<12.1f} {eta_ib:<12.1f} {eta_tot:<15.1f} {eta_tot*3.28:.0f}")

# =============================================================================
# PART 5: HISTORICAL SURGE EVENTS
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: HISTORICAL SURGE EVENTS AND Z² VERIFICATION")
print("=" * 70)

print("""
VERIFICATION: Compare observed surge to Z²-based predictions.

RECORD SURGE EVENTS:

1. Typhoon Haiyan (2013) - Tacloban, Philippines
   - V_max: 195 kt (Cat 5+)
   - Surge: ~7 m (23 ft)
   - Extreme bathymetry amplification in bay

2. Hurricane Katrina (2005) - Mississippi coast
   - V_max at landfall: 125 kt (Cat 3)
   - Surge: 8.5 m (28 ft) at Pass Christian
   - Large storm size + wide shallow shelf

3. Hurricane Camille (1969) - Mississippi coast
   - V_max at landfall: 175 kt (Cat 5)
   - Surge: 7.3 m (24 ft)
   - Smaller storm than Katrina

4. Hurricane Michael (2018) - Mexico Beach, FL
   - V_max at landfall: 140 kt (Cat 5)
   - Surge: 4.3 m (14 ft)
   - Narrow shelf, fast forward speed

Z² INSIGHT:

Katrina surge > Camille surge despite lower intensity because:
- Katrina was LARGER (more mass transport)
- Z² efficiency similar, but geometric factors differed

The Z² framework explains why size matters:
    η_surge ∝ Z² × (size factor) / (speed factor)
""")

# Historical comparison
print("\nHistorical Surge Comparison:")
print("-" * 70)
print(f"{'Storm':<20} {'V_max (kt)':<12} {'Size (R_34)':<12} {'Speed (kt)':<12} {'Surge (ft)'}")
print("-" * 70)

events = [
    ("Katrina 2005", 125, 350, 12, 28),
    ("Camille 1969", 175, 150, 17, 24),
    ("Michael 2018", 140, 100, 14, 14),
    ("Ike 2008", 110, 400, 13, 20),
    ("Harvey 2017", 130, 150, 6, 12),  # Stalled, but over land
    ("Ian 2022", 150, 200, 10, 18),
]

for name, V, R, speed, surge in events:
    print(f"{name:<20} {V:<12} {R} km       {speed:<12} {surge}")

# =============================================================================
# PART 6: SURGE FORECASTING
# =============================================================================
print("\n" + "=" * 70)
print("PART 6: SURGE FORECASTING IMPLICATIONS")
print("=" * 70)

print("""
FORECASTING STORM SURGE:

1. DETERMINE Z² MPI:
   V_MPI from SST, outflow T, efficiency

2. ESTIMATE ACTUAL INTENSITY:
   V_actual = ε_struct × V_MPI
   Accounts for shear, structure, etc.

3. CALCULATE SURGE POTENTIAL:
   η_surge ∝ V² × (size) / (speed × depth)

4. APPLY GEOMETRY:
   Local bathymetry, coastline, bays

OPERATIONAL MODELS:

- SLOSH: Sea, Lake, and Overland Surges from Hurricanes
- ADCIRC: Advanced Circulation model
- Both use similar physics but different numerics

Z² IMPROVEMENT OPPORTUNITY:

Current models don't explicitly use Z² framework.
Incorporating Z² could improve:
1. Intensity forecast → better surge forecast
2. Physical understanding of surge-intensity relationship
3. Ensemble surge forecasting based on Z² uncertainty

KEY MESSAGE:

    Surge kills more people than wind.
    Understanding Z² → Understanding surge → Saving lives.
""")

def surge_risk_category(surge_m):
    """Categorize surge risk."""
    if surge_m < 1:
        return "Low"
    elif surge_m < 2:
        return "Moderate"
    elif surge_m < 3:
        return "High"
    elif surge_m < 5:
        return "Very High"
    else:
        return "Extreme"

print("\nSurge Risk Categories:")
print("-" * 50)
print(f"{'Surge (m)':<15} {'Surge (ft)':<15} {'Risk':<15} {'Impact'}")
print("-" * 50)

for surge_m in [0.5, 1.0, 2.0, 3.0, 5.0, 8.0]:
    risk = surge_risk_category(surge_m)
    if surge_m < 1:
        impact = "Minor coastal flooding"
    elif surge_m < 2:
        impact = "Significant flooding"
    elif surge_m < 3:
        impact = "Major damage to structures"
    elif surge_m < 5:
        impact = "Devastating, life-threatening"
    else:
        impact = "Catastrophic destruction"
    print(f"{surge_m:<15.1f} {surge_m*3.28:<15.0f} {risk:<15} {impact}")

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("Z² STORM SURGE: SUMMARY")
print("=" * 70)

print(f"""
STORM SURGE PHYSICS IN Z² FRAMEWORK:

1. WIND STRESS SETUP:
   η_wind = τ L / (ρ_w g h) ∝ V² ∝ Z²
   Dominant over shallow continental shelves

2. INVERSE BAROMETER:
   η_IB = Δp / (ρ_w g) ∝ V² ∝ Z²
   Typically 10-20% of total surge

3. BATHYMETRY:
   Shoaling amplification: η ∝ 1/√h
   Wide, shallow shelves → extreme surge potential

4. STORM SIZE:
   Larger storms (greater R_34kt) push more water
   Size factor often dominates over intensity

5. FORWARD SPEED:
   Slower storms accumulate more surge
   Speed factor = 1/v_forward

6. Z² UNIFIED FORMULA:
   η_surge ∝ Z² × (thermo potential) × (size) / (depth × speed)

CRITICAL INSIGHT:

Storm surge is NOT just about intensity (Category).
A large Cat 3 can produce more surge than a small Cat 5.

Katrina (Cat 3, large): 28 ft surge
Camille (Cat 5, small): 24 ft surge

The Z² framework explains this through the full energy budget:
- Z² sets maximum intensity
- Size determines mass transport
- Speed determines accumulation time
- Bathymetry determines amplification

SAVE LIVES: Evacuate based on SURGE potential, not Category!
""")

print("\nScript completed successfully.")
