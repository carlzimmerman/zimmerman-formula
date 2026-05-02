#!/usr/bin/env python3
"""
RADIATIVE TRANSFER PHYSICS - FIRST PRINCIPLES
==============================================

Deriving Earth's energy balance, greenhouse effect, and
climate sensitivity from fundamental radiation physics.
"""

import numpy as np

print("=" * 70)
print("RADIATIVE TRANSFER PHYSICS - FIRST PRINCIPLES")
print("=" * 70)


# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================
h = 6.626e-34       # Planck constant (J·s)
c = 2.998e8         # Speed of light (m/s)
k_B = 1.381e-23     # Boltzmann constant (J/K)
sigma = 5.67e-8     # Stefan-Boltzmann constant (W/m²/K⁴)
S_0 = 1361          # Solar constant (W/m²)
R_earth = 6.371e6   # Earth radius (m)


# =============================================================================
# PART 1: BLACKBODY RADIATION
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: BLACKBODY RADIATION (PLANCK FUNCTION)")
print("=" * 70)

planck_text = """
PLANCK'S LAW - FOUNDATION OF THERMAL RADIATION:
================================================

The spectral radiance of a blackbody:

B(λ,T) = (2hc²/λ⁵) × 1/(exp(hc/λkT) - 1)

Where:
- h = Planck constant = 6.626×10⁻³⁴ J·s
- c = speed of light = 3×10⁸ m/s
- k = Boltzmann constant = 1.381×10⁻²³ J/K
- λ = wavelength
- T = temperature

WIEN'S DISPLACEMENT LAW:
Peak wavelength: λ_max = 2898 μm·K / T

Sun (5778 K): λ_max = 0.50 μm (visible, green)
Earth (288 K): λ_max = 10 μm (infrared)

This is why solar = shortwave, terrestrial = longwave!

STEFAN-BOLTZMANN LAW:
Total power: P = σT⁴

Where σ = 5.67×10⁻⁸ W/m²/K⁴

This is the integrated Planck function!
"""
print(planck_text)

def planck_function(wavelength_um, T):
    """
    Planck function for spectral radiance.

    wavelength_um: wavelength in micrometers
    T: temperature in Kelvin
    Returns: W/m²/sr/μm
    """
    lam = wavelength_um * 1e-6  # Convert to meters
    factor1 = 2 * h * c**2 / lam**5
    factor2 = 1 / (np.exp(h * c / (lam * k_B * T)) - 1)
    return factor1 * factor2 * 1e-6  # Convert to per μm

def wien_peak(T):
    """Peak wavelength from Wien's law."""
    return 2898 / T  # μm

def stefan_boltzmann(T):
    """Total emitted power per unit area."""
    return sigma * T**4

print("\nWien's Displacement Law - Peak Emission:")
print("-" * 50)
print(f"{'Object':<20} {'T (K)':<10} {'λ_max (μm)':<15}")
print("-" * 50)
for name, T in [("Sun", 5778), ("Earth surface", 288), ("Atmosphere avg", 255),
                ("Hot desert", 330), ("Ice", 273), ("Tropopause", 217)]:
    lam = wien_peak(T)
    print(f"{name:<20} {T:<10} {lam:<15.2f}")


# =============================================================================
# PART 2: EARTH'S ENERGY BALANCE
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: EARTH'S ENERGY BALANCE")
print("=" * 70)

energy_balance_text = """
PLANETARY ENERGY BALANCE:
=========================

INCOMING SOLAR:
Solar flux at Earth: S₀ = 1361 W/m²
Intercepted by Earth: πR² × S₀
Spread over surface: 4πR²
Average flux: S₀/4 = 340 W/m²

ABSORBED SOLAR:
Planetary albedo α ≈ 0.30 (30% reflected)
Absorbed flux: (1-α) × S₀/4 = 239 W/m²

OUTGOING LONGWAVE:
Earth must emit to balance absorbed solar
F_out = σT_eff⁴ = 239 W/m²
→ T_eff = 255 K = -18°C

But surface temperature = 288 K = +15°C!
The difference = GREENHOUSE EFFECT = 33°C
"""
print(energy_balance_text)

def effective_temperature(albedo=0.30, S0=1361):
    """Calculate planetary effective temperature."""
    absorbed = (1 - albedo) * S0 / 4
    T_eff = (absorbed / sigma) ** 0.25
    return T_eff, absorbed

T_eff, F_absorbed = effective_temperature()
print(f"\nEarth Energy Balance Calculation:")
print("-" * 50)
print(f"Solar constant: {S_0} W/m²")
print(f"Average insolation: {S_0/4:.0f} W/m²")
print(f"Planetary albedo: 0.30")
print(f"Absorbed solar: {F_absorbed:.0f} W/m²")
print(f"Effective temperature: {T_eff:.1f} K = {T_eff-273.15:.1f}°C")
print(f"Observed surface T: 288 K = 15°C")
print(f"Greenhouse effect: {288 - T_eff:.0f} K = 33°C")


# =============================================================================
# PART 3: ATMOSPHERIC ABSORPTION
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: ATMOSPHERIC ABSORPTION")
print("=" * 70)

absorption_text = """
MOLECULAR ABSORPTION OF RADIATION:
==================================

Molecules absorb/emit at specific wavelengths based on:
1. Vibrational modes
2. Rotational modes
3. Electronic transitions

GREENHOUSE GASES absorb INFRARED (Earth's emission):

CO₂ (Carbon Dioxide):
- 15 μm band (strongest)
- 4.3 μm band
- Currently 424 ppm, was 280 ppm pre-industrial

H₂O (Water Vapor):
- Multiple bands throughout IR
- 6.3 μm, rotation bands
- Concentrations vary (0-4%)
- Strongest greenhouse gas by effect!

CH₄ (Methane):
- 7.7 μm band
- ~1.9 ppm, 2.5× pre-industrial

N₂O (Nitrous Oxide):
- 4.5 μm, 7.8 μm, 8.6 μm bands
- ~330 ppb

O₃ (Ozone):
- 9.6 μm band
- Critical for stratosphere

ATMOSPHERIC WINDOW:
8-12 μm: Relatively transparent
This is where Earth loses most heat to space!
"""
print(absorption_text)

# CO2 band saturation
def co2_radiative_forcing(C, C0=280):
    """
    CO₂ radiative forcing.

    Logarithmic relationship (band saturation):
    ΔF = 5.35 × ln(C/C₀)

    C: current CO₂ (ppm)
    C0: reference CO₂ (ppm)
    """
    return 5.35 * np.log(C / C0)

print("\nCO₂ Radiative Forcing:")
print("-" * 50)
print(f"{'CO₂ (ppm)':<15} {'ΔF (W/m²)':<15} {'Relative to pre-industrial'}")
print("-" * 50)
for co2 in [280, 350, 400, 424, 450, 560, 700, 1000]:
    df = co2_radiative_forcing(co2)
    rel = co2 / 280
    print(f"{co2:<15} {df:<15.2f} {rel:.2f}×")


# =============================================================================
# PART 4: LAYER MODEL OF GREENHOUSE
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: SIMPLE GREENHOUSE MODEL")
print("=" * 70)

layer_text = """
ONE-LAYER ATMOSPHERE MODEL:
===========================

Simplest model that captures greenhouse effect:

      Space
        ↑ σT_a⁴ (upward)
    -----------  Atmosphere (T_a)
        ↓ σT_a⁴ (downward)    ↑ σT_s⁴ (from surface)
    ===========  Surface (T_s)
        ↓ Absorbed solar F_s

BALANCE EQUATIONS:

Surface: F_s + σT_a⁴ = σT_s⁴
Atmosphere: σT_s⁴ = 2σT_a⁴
(absorbs all surface emission, emits up and down)

SOLVING:
T_a⁴ = T_s⁴/2 → T_a = T_s / 2^(1/4)
T_s⁴ = F_s + F_s/2 = 3F_s/2

For F_s = 239 W/m²:
T_s = (3 × 239 / (2σ))^(1/4) = 303 K

This gives T_s - T_eff = 303 - 255 = 48°C warming!
(Actual is 33°C because atmosphere isn't opaque)
"""
print(layer_text)

def one_layer_greenhouse(F_absorbed):
    """One-layer atmosphere model."""
    T_s = ((3/2) * F_absorbed / sigma) ** 0.25
    T_a = T_s / 2**0.25
    return T_s, T_a

T_s_model, T_a_model = one_layer_greenhouse(239)
print(f"\nOne-Layer Model Results:")
print("-" * 50)
print(f"Absorbed solar: 239 W/m²")
print(f"Surface temperature: {T_s_model:.1f} K = {T_s_model-273.15:.1f}°C")
print(f"Atmosphere temperature: {T_a_model:.1f} K = {T_a_model-273.15:.1f}°C")
print(f"Greenhouse warming: {T_s_model - T_eff:.1f}°C")
print(f"(Observed: 33°C - model overestimates due to assumptions)")


# =============================================================================
# PART 5: CLIMATE SENSITIVITY
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: CLIMATE SENSITIVITY")
print("=" * 70)

sensitivity_text = """
CLIMATE SENSITIVITY:
====================

Definition: Temperature change per doubling of CO₂

DIRECT (NO-FEEDBACK) SENSITIVITY:
ΔF_2×CO₂ = 5.35 × ln(2) = 3.7 W/m²

From Stefan-Boltzmann:
ΔT = ΔF / (4σT³) = 3.7 / (4 × 5.67e-8 × 255³)
ΔT_direct ≈ 1.1°C

This is the "Planck response" - minimum possible warming.

WITH FEEDBACKS:
ΔT = ΔT_direct / (1 - f)

Where f = feedback factor (sum of all feedbacks)

MAJOR FEEDBACKS:

1. WATER VAPOR (+): Warming → more H₂O → more greenhouse
   Amplifies by ~1.8×
   Most certain positive feedback!

2. ICE-ALBEDO (+): Less ice → lower albedo → more absorption
   Amplifies by ~1.1×

3. LAPSE RATE (-): Tropical upper troposphere warms more
   Partially offsets by ~0.9×

4. CLOUD (??): High clouds warm, low clouds cool
   Net effect uncertain: -0.5 to +1.0 W/m²/K
   THIS IS THE DOMINANT UNCERTAINTY

EQUILIBRIUM CLIMATE SENSITIVITY (ECS):
Best estimate: 3.0°C (range: 2.5-4.0°C)
IPCC very likely range: 2.0-5.0°C
"""
print(sensitivity_text)

def climate_sensitivity(forcing, feedback_factor):
    """
    Calculate equilibrium temperature change.

    ΔT = λ × ΔF / (1 - f)
    where λ = 1/4σT³ ≈ 0.30 K/(W/m²)
    """
    lambda_0 = 1 / (4 * sigma * 255**3)  # Planck parameter
    return lambda_0 * forcing / (1 - feedback_factor)

# Direct sensitivity
forcing_2xCO2 = 5.35 * np.log(2)
T_direct = climate_sensitivity(forcing_2xCO2, 0)

print(f"\nClimate Sensitivity Calculations:")
print("-" * 60)
print(f"Forcing for 2×CO₂: {forcing_2xCO2:.2f} W/m²")
print(f"\nDirect (no-feedback): {T_direct:.2f}°C")

print(f"\n{'Feedback scenario':<30} {'f':<10} {'ECS (°C)':<15}")
print("-" * 60)
for name, f in [("No feedbacks", 0), ("Water vapor only", 0.45),
                ("WV + ice-albedo", 0.55), ("All positive (low)", 0.60),
                ("IPCC central", 0.65), ("All positive (high)", 0.70),
                ("High cloud feedback", 0.75)]:
    ecs = climate_sensitivity(forcing_2xCO2, f)
    print(f"{name:<30} {f:<10.2f} {ecs:<15.2f}")


# =============================================================================
# PART 6: SPECTRAL EVIDENCE
# =============================================================================
print("\n" + "=" * 70)
print("PART 6: SPECTRAL EVIDENCE FOR GREENHOUSE EFFECT")
print("=" * 70)

spectral_text = """
OBSERVATIONAL PROOF:
====================

SATELLITE MEASUREMENTS:
Looking down from space, we see Earth's emission spectrum.

Expected (no atmosphere): Smooth blackbody at T_surface ≈ 288 K

Observed: ABSORPTION BANDS carved into spectrum!
- 15 μm: Deep notch (CO₂)
- 9.6 μm: Ozone band
- Continuum: Water vapor absorption

The "missing" radiation = absorbed by greenhouse gases
                        = warming the surface instead of escaping

TEMPORAL EVIDENCE:
Comparing spectra from 1970 vs 2006 satellites:
- Deeper CO₂ notch (more CO₂)
- Slightly narrower (stratosphere cooling!)
- Matches predictions from radiative transfer models

GROUND-BASED:
Looking UP at atmosphere from surface:
- "Downwelling" longwave radiation measured
- ~300-350 W/m² depending on humidity
- Increases with more CO₂ (measured!)

This is direct proof that more CO₂ = more downward radiation.
"""
print(spectral_text)


# =============================================================================
# PART 7: TRANSIENT VS EQUILIBRIUM
# =============================================================================
print("\n" + "=" * 70)
print("PART 7: TRANSIENT CLIMATE RESPONSE")
print("=" * 70)

transient_text = """
WHY WARMING TAKES TIME:
=======================

The ocean stores HUGE amounts of heat!
- Top 3m of ocean = entire atmosphere heat capacity
- Full ocean mixing takes centuries

EQUILIBRIUM CLIMATE SENSITIVITY (ECS):
Temperature after centuries (full equilibration)
Best estimate: 3.0°C per doubling

TRANSIENT CLIMATE RESPONSE (TCR):
Temperature at time of doubling (after ~70 years of 1%/yr increase)
Best estimate: 1.8°C per doubling

TCR/ECS ≈ 0.6 (ocean uptake "hides" some warming)

"COMMITTED WARMING":
Even if CO₂ stabilizes, temperature continues rising
toward equilibrium over centuries.

Current CO₂ (424 ppm):
- ΔF = 5.35 × ln(424/280) = 2.2 W/m²
- Already committed to ~0.8°C more warming
- Even after "net zero" emissions
"""
print(transient_text)

def committed_warming(co2_current, co2_preindustrial=280, ecs=3.0):
    """
    Calculate committed warming from current CO₂.

    Assumes no further emissions.
    """
    forcing = co2_radiative_forcing(co2_current, co2_preindustrial)
    forcing_2x = 5.35 * np.log(2)
    dT_eq = ecs * forcing / forcing_2x
    return dT_eq

print(f"\nCommitted Warming Estimates:")
print("-" * 60)
current_forcing = co2_radiative_forcing(424)
print(f"Current CO₂: 424 ppm")
print(f"Current forcing: {current_forcing:.2f} W/m²")
print(f"Observed warming: ~1.2°C")

for ecs in [2.5, 3.0, 4.0]:
    committed = committed_warming(424, ecs=ecs)
    additional = committed - 1.2
    print(f"ECS = {ecs}°C: Equilibrium warming = {committed:.1f}°C ({additional:+.1f}°C additional)")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: RADIATIVE TRANSFER PHYSICS")
print("=" * 70)

summary = """
KEY RADIATIVE PHYSICS:
=====================

1. PLANCK'S LAW
   - All objects emit thermal radiation
   - Spectrum depends on temperature
   - Wien: λ_max = 2898/T μm

2. STEFAN-BOLTZMANN
   - P = σT⁴ (total emitted power)
   - Foundation of energy balance

3. EARTH'S ENERGY BALANCE
   - Absorbed solar = 239 W/m²
   - T_eff = 255 K (from S-B)
   - Surface = 288 K
   - Greenhouse effect = 33°C

4. MOLECULAR ABSORPTION
   - CO₂: 15 μm band
   - H₂O: Multiple bands
   - Creates atmospheric "blanket"

5. CO₂ FORCING
   - ΔF = 5.35 × ln(C/C₀) W/m²
   - Logarithmic (band saturation)
   - 2×CO₂ → 3.7 W/m²

6. CLIMATE SENSITIVITY
   - Direct: 1.1°C per doubling
   - With feedbacks: 2.5-4.0°C
   - Cloud feedback = main uncertainty

7. TRANSIENT RESPONSE
   - Ocean delays warming
   - TCR ≈ 0.6 × ECS
   - Committed warming even if emissions stop


THE PHYSICS IS UNAMBIGUOUS:
===========================
- Greenhouse effect: Textbook physics (known since 1850s)
- CO₂ is increasing: Measured (Keeling curve, ice cores)
- More CO₂ = more forcing: Radiative transfer
- Warming must occur: Energy balance

The only uncertainty is HOW MUCH (sensitivity),
not WHETHER (physics guarantees warming).
"""
print(summary)

print("\n" + "=" * 70)
print("END OF RADIATIVE TRANSFER PHYSICS")
print("=" * 70)
