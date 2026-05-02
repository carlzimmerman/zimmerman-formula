#!/usr/bin/env python3
"""
LONG-TERM WEATHER PATTERNS, CO2, AND EARTH SYSTEMS RESEARCH
============================================================

First-principles investigation of:
1. Multi-decadal climate oscillations (ENSO, PDO, AMO, NAO)
2. CO2 and radiative forcing physics
3. Magnetic pole drift and geomagnetic changes

Philosophy: Separate well-established physics from areas of active research
"""

import numpy as np
from typing import Dict, List, Tuple

print("=" * 70)
print("LONG-TERM CLIMATE & EARTH SYSTEMS RESEARCH")
print("First-Principles Investigation")
print("=" * 70)


# =============================================================================
# PART 1: MULTI-DECADAL CLIMATE OSCILLATIONS
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: MULTI-DECADAL CLIMATE OSCILLATIONS")
print("=" * 70)

print("""
THE MAJOR CLIMATE OSCILLATIONS
==============================

Earth's climate naturally oscillates on multiple timescales.
These are NOT random - they're driven by ocean-atmosphere coupling.

1. ENSO (El Niño-Southern Oscillation)
   - Period: 2-7 years
   - Location: Tropical Pacific
   - Mechanism: Walker circulation + thermocline feedback
   - Global impact: Strongest single driver of year-to-year variability

2. PDO (Pacific Decadal Oscillation)
   - Period: 20-30 years
   - Location: North Pacific
   - Mechanism: Ocean gyre dynamics + ENSO integration
   - Impact: Affects North American climate for decades

3. AMO (Atlantic Multidecadal Oscillation)
   - Period: 60-80 years
   - Location: North Atlantic
   - Mechanism: Thermohaline circulation variability
   - Impact: Hurricane activity, Sahel rainfall, European climate

4. NAO (North Atlantic Oscillation)
   - Period: Interannual to decadal
   - Location: North Atlantic
   - Mechanism: Pressure difference Iceland-Azores
   - Impact: European winters, Atlantic storm tracks
""")


# ENSO Physics
print("\n" + "-" * 70)
print("ENSO: THE DOMINANT CLIMATE OSCILLATION")
print("-" * 70)

print("""
ENSO PHYSICS (Bjerknes Feedback):

                    WALKER CIRCULATION

    West Pacific          ←←← Trade Winds ←←←         East Pacific
    (Warm Pool)                                       (Cold Tongue)

    ↑ Rising air                                      ↓ Sinking air
    ☁ Convection                                      ☀ Clear skies
    30°C SST                                          22°C SST

    Thermocline: DEEP (150m)                          SHALLOW (50m)


EL NIÑO (Warm Phase):
----------------------
- Trade winds weaken
- Warm water sloshes eastward
- Thermocline flattens
- Peru/Ecuador: heavy rain, flooding
- Australia/Indonesia: drought
- Global: +0.1-0.2°C temperature anomaly

LA NIÑA (Cold Phase):
---------------------
- Trade winds strengthen
- Cold upwelling intensifies
- Thermocline tilts more
- Australia/Indonesia: flooding
- Americas: drought
- Global: -0.1-0.2°C temperature anomaly
""")

def enso_index(sst_anomaly_nino34: float) -> Dict:
    """
    Classify ENSO state from Nino 3.4 SST anomaly.

    Nino 3.4 region: 5°N-5°S, 170°W-120°W
    """
    if sst_anomaly_nino34 >= 1.5:
        state = "Strong El Niño"
        impacts = {
            'california': 'Wet winter, flooding risk',
            'australia': 'Drought, bushfire risk',
            'atlantic_hurricanes': 'Suppressed (increased shear)',
            'pacific_hurricanes': 'Enhanced',
            'global_temp': '+0.15 to +0.25°C',
        }
    elif sst_anomaly_nino34 >= 0.5:
        state = "El Niño"
        impacts = {
            'california': 'Above normal precipitation',
            'australia': 'Below normal precipitation',
            'atlantic_hurricanes': 'Below normal',
            'pacific_hurricanes': 'Above normal',
            'global_temp': '+0.05 to +0.15°C',
        }
    elif sst_anomaly_nino34 <= -1.5:
        state = "Strong La Niña"
        impacts = {
            'california': 'Drought conditions',
            'australia': 'Flooding, wet conditions',
            'atlantic_hurricanes': 'Enhanced activity',
            'pacific_hurricanes': 'Suppressed',
            'global_temp': '-0.15 to -0.25°C',
        }
    elif sst_anomaly_nino34 <= -0.5:
        state = "La Niña"
        impacts = {
            'california': 'Below normal precipitation',
            'australia': 'Above normal precipitation',
            'atlantic_hurricanes': 'Above normal',
            'pacific_hurricanes': 'Below normal',
            'global_temp': '-0.05 to -0.15°C',
        }
    else:
        state = "Neutral"
        impacts = {
            'california': 'Near normal',
            'australia': 'Near normal',
            'atlantic_hurricanes': 'Near normal',
            'pacific_hurricanes': 'Near normal',
            'global_temp': 'Near baseline',
        }

    return {'state': state, 'sst_anomaly': sst_anomaly_nino34, 'impacts': impacts}


print("\nENSO impacts by state:")
print("-" * 60)
for anomaly in [2.0, 1.0, 0.0, -1.0, -2.0]:
    result = enso_index(anomaly)
    print(f"\nNino 3.4 = {anomaly:+.1f}°C → {result['state']}")
    print(f"  Atlantic hurricanes: {result['impacts']['atlantic_hurricanes']}")
    print(f"  Global temp effect: {result['impacts']['global_temp']}")


# PDO and AMO
print("\n" + "-" * 70)
print("PDO AND AMO: DECADAL TO MULTIDECADAL OSCILLATIONS")
print("-" * 70)

print("""
PACIFIC DECADAL OSCILLATION (PDO):
==================================

Pattern: Horseshoe-shaped SST anomaly in North Pacific

PDO+ (Warm Phase):     │  PDO- (Cool Phase):
- Warm eastern Pacific │  - Cool eastern Pacific
- Cool central Pacific │  - Warm central Pacific
- More El Niños        │  - More La Niñas
- US West Coast: warm  │  - US West Coast: cool
- Alaska: warm         │  - Alaska: cool

Recent PDO history:
- 1925-1946: Warm phase
- 1947-1976: Cool phase
- 1977-1998: Warm phase
- 1999-2013: Cool phase (hiatus contributor?)
- 2014-present: Variable

IMPORTANT: PDO is NOT independent of ENSO!
PDO = low-frequency integration of ENSO + North Pacific dynamics


ATLANTIC MULTIDECADAL OSCILLATION (AMO):
========================================

Pattern: Basin-wide North Atlantic SST anomaly

AMO+ (Warm Phase):     │  AMO- (Cool Phase):
- Warm North Atlantic  │  - Cool North Atlantic
- More Atlantic TCs    │  - Fewer Atlantic TCs
- Sahel: wet           │  - Sahel: dry
- Europe: warm summers │  - Europe: cool summers

Recent AMO history:
- 1930-1960: Warm phase (1930s Dust Bowl era)
- 1965-1995: Cool phase (quiet Atlantic TCs)
- 1995-2020s: Warm phase (active Atlantic TCs!)

Mechanism: Thermohaline circulation (AMOC) variability
- Warm phase: strong AMOC, warm SSTs
- Cool phase: weak AMOC, cool SSTs

WARNING: AMOC may be weakening due to Greenland melt
This could trigger rapid AMO phase change (uncertain!)
""")


def combined_hurricane_outlook(enso_state: str, amo_phase: str) -> Dict:
    """
    Combine ENSO and AMO for Atlantic hurricane season outlook.
    """
    # Base ACE (Accumulated Cyclone Energy) expectation
    base_ace = 105  # Median 1991-2020

    # ENSO effect
    if 'Niño' in enso_state:
        enso_factor = 0.75 if 'Strong' in enso_state else 0.85
    elif 'Niña' in enso_state:
        enso_factor = 1.35 if 'Strong' in enso_state else 1.20
    else:
        enso_factor = 1.0

    # AMO effect
    amo_factor = 1.25 if amo_phase == 'warm' else 0.85

    expected_ace = base_ace * enso_factor * amo_factor

    if expected_ace > 150:
        outlook = "HYPERACTIVE"
    elif expected_ace > 120:
        outlook = "ABOVE NORMAL"
    elif expected_ace > 90:
        outlook = "NEAR NORMAL"
    elif expected_ace > 60:
        outlook = "BELOW NORMAL"
    else:
        outlook = "QUIET"

    return {
        'expected_ace': expected_ace,
        'outlook': outlook,
        'enso_factor': enso_factor,
        'amo_factor': amo_factor,
    }


print("\nAtlantic Hurricane Season Outlook by Climate State:")
print("-" * 70)
print(f"{'ENSO State':<20} | {'AMO Phase':<10} | {'Exp. ACE':>10} | {'Outlook':<15}")
print("-" * 70)

for enso in ['Strong El Niño', 'Neutral', 'Strong La Niña']:
    for amo in ['warm', 'cool']:
        result = combined_hurricane_outlook(enso, amo)
        print(f"{enso:<20} | {amo:<10} | {result['expected_ace']:>10.0f} | {result['outlook']:<15}")

print("""

KEY INSIGHT: 2024's hyperactive season
- La Niña developing (ENSO factor ~1.2)
- AMO still warm (AMO factor ~1.25)
- Record-warm Atlantic SSTs (additional boost)
- Result: Helene, Milton, Beryl - all major hurricanes
""")


# =============================================================================
# PART 2: CO2 AND RADIATIVE FORCING
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: CO2 AND RADIATIVE FORCING PHYSICS")
print("=" * 70)

print("""
THE GREENHOUSE EFFECT: FIRST-PRINCIPLES PHYSICS
===============================================

1. SOLAR INPUT
   - Sun emits shortwave radiation (visible, UV)
   - Earth receives: S = 1361 W/m² (solar constant)
   - After reflection (albedo α ≈ 0.30): absorbed = 239 W/m²

2. EARTH'S EMISSION
   - Earth radiates longwave (infrared) to space
   - Stefan-Boltzmann: P = εσT⁴
   - For balance: T_effective = 255 K = -18°C

3. BUT Earth's surface is ~288 K = +15°C
   - Difference: 33°C warmer than bare-rock calculation
   - This is the GREENHOUSE EFFECT

4. HOW IT WORKS
   - CO2, H2O, CH4 absorb and re-emit infrared
   - Atmosphere acts like a "blanket"
   - Surface receives downward IR from atmosphere
   - Surface must warm to achieve radiation balance
""")

# Physical constants
sigma = 5.67e-8  # Stefan-Boltzmann constant (W/m²/K⁴)
S_0 = 1361       # Solar constant (W/m²)
albedo = 0.30    # Earth's average albedo

def effective_temperature(solar_constant: float, albedo: float) -> float:
    """Calculate effective radiating temperature (no atmosphere)."""
    absorbed = solar_constant * (1 - albedo) / 4  # /4 for sphere
    T_eff = (absorbed / sigma) ** 0.25
    return T_eff

def greenhouse_warming(co2_ppm: float, baseline_ppm: float = 280) -> float:
    """
    Estimate greenhouse warming from CO2 change.

    Radiative forcing: ΔF = 5.35 × ln(C/C₀) W/m²
    Climate sensitivity: ~0.8 K per W/m² (no feedbacks)
                        ~2-4.5 K per W/m² (with feedbacks)
    """
    delta_F = 5.35 * np.log(co2_ppm / baseline_ppm)

    # Direct warming (no feedbacks)
    lambda_0 = 0.3  # K per W/m² (Planck response)
    warming_direct = delta_F * lambda_0

    # With feedbacks (water vapor, ice-albedo, clouds)
    lambda_total = 0.8  # K per W/m² (central estimate)
    warming_total = delta_F * lambda_total

    # Equilibrium Climate Sensitivity range
    ecs_low = delta_F * 0.5   # Low sensitivity
    ecs_high = delta_F * 1.2  # High sensitivity

    return {
        'co2_ppm': co2_ppm,
        'radiative_forcing': delta_F,
        'warming_direct': warming_direct,
        'warming_with_feedbacks': warming_total,
        'ecs_range': (ecs_low, ecs_high),
    }


print(f"\nBasic calculation:")
T_eff = effective_temperature(S_0, albedo)
print(f"  Solar constant: {S_0} W/m²")
print(f"  Albedo: {albedo}")
print(f"  Effective temperature (no greenhouse): {T_eff:.1f} K = {T_eff - 273.15:.1f}°C")
print(f"  Actual surface temperature: ~288 K = ~15°C")
print(f"  Greenhouse effect: ~33°C of warming")

print("""

CO2 RADIATIVE FORCING:
======================

The formula: ΔF = 5.35 × ln(C/C₀) W/m²

This is LOGARITHMIC - each doubling has same effect:
- 280 → 560 ppm: +3.7 W/m²
- 560 → 1120 ppm: +3.7 W/m² (additional)

Why logarithmic?
- CO2 absorption bands become saturated
- Adding more CO2 only affects band edges
- Diminishing returns (but still positive forcing)
""")

print("\nCO2 levels and warming estimates:")
print("-" * 70)
print(f"{'CO2 (ppm)':<12} | {'Forcing (W/m²)':>15} | {'Direct (°C)':>12} | {'Total (°C)':>12}")
print("-" * 70)

for co2 in [280, 350, 420, 560, 800, 1000]:
    result = greenhouse_warming(co2)
    label = ""
    if co2 == 280:
        label = " (pre-industrial)"
    elif co2 == 420:
        label = " (current ~2024)"
    elif co2 == 560:
        label = " (2× pre-industrial)"
    print(f"{co2:<12} | {result['radiative_forcing']:>15.2f} | {result['warming_direct']:>12.2f} | {result['warming_with_feedbacks']:>12.2f}{label}")


print("""

FEEDBACKS: WHY UNCERTAINTY EXISTS
=================================

The direct CO2 effect is well-constrained: ~1.1°C per doubling.
But feedbacks amplify or dampen this:

POSITIVE FEEDBACKS (amplify warming):
1. Water vapor feedback: +1.5 to +2.0 W/m²/K
   - Warmer air holds more H2O (Clausius-Clapeyron)
   - H2O is also a greenhouse gas
   - WELL UNDERSTOOD, largest feedback

2. Ice-albedo feedback: +0.2 to +0.4 W/m²/K
   - Ice melts → darker surface → absorbs more heat
   - WELL UNDERSTOOD

3. Permafrost/methane feedback: uncertain
   - Warming releases CH4 from permafrost
   - Could be significant, poorly quantified

NEGATIVE FEEDBACKS (dampen warming):
1. Planck feedback: -3.2 W/m²/K
   - Warmer Earth radiates more (T⁴ law)
   - This is why we don't have runaway warming
   - FUNDAMENTAL PHYSICS

2. Lapse rate feedback: -0.5 to -1.0 W/m²/K
   - Tropics warm more aloft than surface
   - More efficient radiation to space

UNCERTAIN FEEDBACKS:
1. Cloud feedback: -0.5 to +1.0 W/m²/K
   - Low clouds cool (reflect sunlight)
   - High clouds warm (trap IR)
   - Net effect: THE major uncertainty
""")

# Climate sensitivity calculation
print("\nEquilibrium Climate Sensitivity (ECS) for 2×CO2:")
print("-" * 50)
print("""
Definition: Warming at equilibrium from doubling CO2

IPCC AR6 Assessment (2021):
- Very likely range: 2.5°C to 4.0°C
- Best estimate: 3.0°C
- Likely (66%): 2.5°C to 4.0°C

Why the range?
- Cloud feedback uncertainty: ±0.7°C
- Aerosol forcing uncertainty: ±0.3°C
- Historical warming estimate: ±0.2°C

What observations tell us:
- Warming since 1850: ~1.2°C
- CO2 increase: 280 → 420 ppm (50%)
- Implied sensitivity: ~2.5°C (but not at equilibrium yet!)
""")


# Carbon cycle
print("\n" + "-" * 70)
print("THE CARBON CYCLE: WHERE DOES CO2 GO?")
print("-" * 70)

print("""
ANNUAL CARBON BUDGET (2010-2019 average):
=========================================

SOURCES (adding CO2 to atmosphere):
- Fossil fuels + cement:     +9.4 GtC/year
- Land use change:           +1.6 GtC/year
                            ---------------
  Total emissions:          +11.0 GtC/year

SINKS (removing CO2 from atmosphere):
- Ocean uptake:              -2.5 GtC/year
- Land uptake (plants):      -3.4 GtC/year
                            ---------------
  Total sinks:               -5.9 GtC/year

NET ATMOSPHERIC INCREASE:    +5.1 GtC/year
                            (about 2.4 ppm/year)

Key insight: ~46% of emissions stay in atmosphere
             ~54% absorbed by ocean and land

BUT: Sink efficiency may decrease as:
- Ocean becomes more acidic (less CO2 uptake)
- Land ecosystems stressed by heat/drought
- This is a potential positive feedback
""")


# =============================================================================
# PART 3: MAGNETIC POLE DRIFT
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: MAGNETIC POLE DRIFT - WHY IS 'NORTH' CHANGING?")
print("=" * 70)

print("""
EARTH'S MAGNETIC FIELD: BASICS
==============================

Earth has a dipole magnetic field, like a bar magnet.
But the magnetic poles are NOT at the geographic poles!

Current positions (2024):
- Magnetic North Pole: ~86°N, 156°W (Canadian Arctic → Siberia)
- Magnetic South Pole: ~64°S, 136°E (off coast of Antarctica)
- Geographic North Pole: 90°N (axis of rotation)

DECLINATION: Angle between magnetic north and true north
- Varies by location (can be 0° to 25°+)
- Changes over time as poles move
- Critical for navigation!
""")

def magnetic_declination_change(year: int) -> Dict:
    """
    Approximate magnetic north pole position over time.
    Based on historical observations and WMM model.
    """
    # Simplified model of pole movement
    # Actual path is complex - this captures the trend

    if year < 1900:
        lat = 70 + (year - 1800) * 0.05
        lon = -97 - (year - 1800) * 0.1
        speed = 10  # km/year (historical average)
    elif year < 1990:
        lat = 75 + (year - 1900) * 0.08
        lon = -100 - (year - 1900) * 0.3
        speed = 10
    else:
        # Acceleration since 1990!
        lat = 82 + (year - 1990) * 0.12
        lon = -130 - (year - 1990) * 1.5
        speed = 50 + (year - 2000) * 1.5  # Accelerating!

    lat = min(90, lat)

    return {
        'year': year,
        'lat': lat,
        'lon': lon,
        'speed_km_yr': speed,
        'location': f"{lat:.1f}°N, {abs(lon):.1f}°W",
    }


print("\nMagnetic North Pole Movement:")
print("-" * 60)
print(f"{'Year':<8} | {'Position':<25} | {'Speed (km/yr)':>15}")
print("-" * 60)

for year in [1900, 1950, 1990, 2000, 2010, 2020, 2024]:
    result = magnetic_declination_change(year)
    print(f"{result['year']:<8} | {result['location']:<25} | {result['speed_km_yr']:>15.0f}")

print("""

THE ACCELERATION IS REAL!
=========================

Historical drift: ~10 km/year (for centuries)
Recent drift: ~50-55 km/year (since ~2000)

The pole is racing from Canada toward Siberia!

This is NOT:
✗ Related to climate change
✗ Caused by human activity
✗ A sign of imminent pole reversal (probably)

This IS:
✓ Natural geodynamic process
✓ Driven by fluid flow in outer core
✓ Unpredictable on long timescales
✓ Requiring frequent model updates
""")


print("""

WHY IS THE MAGNETIC FIELD MOVING?
=================================

EARTH'S STRUCTURE:

          ┌─────────────────┐
          │   CRUST (solid) │  ~30 km thick
          ├─────────────────┤
          │   MANTLE        │  ~2,900 km
          │   (solid but    │  (convects slowly)
          │    convecting)  │
          ├─────────────────┤
          │  OUTER CORE     │  ~2,200 km
          │  (LIQUID IRON)  │  ← GENERATES FIELD!
          ├─────────────────┤
          │  INNER CORE     │  ~1,200 km radius
          │  (solid iron)   │
          └─────────────────┘

THE GEODYNAMO:
1. Outer core is liquid iron (+ nickel)
2. It's electrically conducting
3. Convection (heat escaping) causes flow
4. Moving conductor in magnetic field → electric currents
5. Electric currents generate magnetic field
6. Self-sustaining dynamo!

WHY THE POLE MOVES:
- Flow in outer core is turbulent and chaotic
- "Blobs" of different magnetic polarity form
- These migrate and interact
- Result: poles wander unpredictably

CURRENT HYPOTHESIS FOR ACCELERATION:
- A high-latitude "jet stream" in outer core
- Stretching of magnetic field lines
- Weakening of field under Canada
- Field now "pulled" toward Siberia
""")


print("""

PRACTICAL IMPLICATIONS:
=======================

1. NAVIGATION
   - Compass points to magnetic north, not true north
   - Declination must be corrected for accurate navigation
   - Aviation charts updated frequently
   - GPS doesn't use magnetic field (uses satellites)

2. WORLD MAGNETIC MODEL (WMM)
   - Updated every 5 years (normally)
   - 2020 update came early due to rapid change
   - Used by smartphones, aircraft, ships, military

3. RUNWAY NUMBERS
   - Runways named by magnetic heading (09, 27, etc.)
   - Must be renamed as declination changes
   - This has happened at many airports!

4. ANIMAL NAVIGATION
   - Birds, sea turtles use magnetic field
   - Rapid changes could affect migration
   - Unclear how significant this is

5. RADIATION PROTECTION
   - Magnetic field shields Earth from solar wind
   - Field has weakened ~10% since 1800
   - South Atlantic Anomaly (weak spot) growing
   - Satellites report more radiation there
""")


# Pole reversal
print("\n" + "-" * 70)
print("POLE REVERSALS: SHOULD WE WORRY?")
print("-" * 70)

print("""
GEOMAGNETIC REVERSALS:
======================

Earth's magnetic field has REVERSED many times!
- North becomes South, South becomes North
- Average: every 200,000 - 300,000 years
- Last reversal: ~780,000 years ago (Brunhes-Matuyama)
- We're "overdue" (but that doesn't mean imminent)

DURING A REVERSAL:
1. Field weakens significantly (~10-20% of normal)
2. Multiple magnetic poles may exist
3. Process takes 1,000-10,000 years
4. Compasses would be useless
5. More radiation reaches surface (but not catastrophic)

IS CURRENT WEAKENING A REVERSAL BEGINNING?
- Field has weakened 10% since 1800
- South Atlantic Anomaly (weak region) growing
- BUT: similar fluctuations have happened before
- Current weakening could reverse
- No way to know for certain

SCIENTIFIC CONSENSUS:
- Reversal is NOT imminent (next few centuries)
- Current changes are within normal variability
- Pole wandering is normal, not a reversal sign
- We'd have centuries of warning if reversal began
""")


# =============================================================================
# PART 4: CONNECTIONS AND SYNTHESIS
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: CONNECTIONS AND SYNTHESIS")
print("=" * 70)

print("""
HOW THESE SYSTEMS INTERACT (AND DON'T):
=======================================

CLIMATE OSCILLATIONS ↔ CO2/WARMING:
-----------------------------------
- ENSO affects year-to-year CO2 growth rate
  (El Niño → more CO2 release from tropics)
- But ENSO doesn't cause long-term warming trend
- Warming may intensify El Niño events (uncertain)
- AMO may mask or amplify warming regionally

MAGNETIC FIELD ↔ CLIMATE:
-------------------------
- Weak connection (if any)
- Some hypothesize cosmic ray → cloud link
  (weaker field → more cosmic rays → more clouds → cooling)
- Evidence is weak and controversial
- NOT a significant climate driver
- Pole movement has zero climate effect

CO2 ↔ MAGNETIC FIELD:
---------------------
- NO connection whatsoever
- Different Earth systems entirely
- CO2: atmosphere/ocean/biosphere
- Magnetic: deep Earth (outer core)
- Anyone claiming connection is wrong


WHAT'S WELL-UNDERSTOOD:
=======================
✓ CO2 greenhouse physics (textbook since 1800s)
✓ ENSO mechanism and predictions (1-9 months out)
✓ AMO/PDO patterns (description, not prediction)
✓ Magnetic field generation (geodynamo theory)
✓ Pole movement observations (very precise)

WHAT'S UNCERTAIN:
=================
? Cloud feedback magnitude
? Future AMOC behavior
? Permafrost/methane feedback
? Tipping point locations
? Pole movement prediction (decades out)
? Whether/when reversal will occur

WHAT'S SPECULATIVE:
===================
✗ Cosmic ray-climate connection
✗ Solar cycle as major climate driver
✗ Magnetic-climate connections
✗ Pole reversal imminent
""")


# =============================================================================
# PART 5: HONEST ASSESSMENT
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: HONEST ASSESSMENT")
print("=" * 70)

print("""
SCIENTIFIC CONFIDENCE LEVELS:
=============================

VERY HIGH CONFIDENCE (>95%):
- CO2 is a greenhouse gas (physics proven in lab)
- Human emissions have increased CO2 by 50%
- Earth has warmed ~1.2°C since 1850
- Most warming is due to human activities
- Continued emissions will cause more warming
- Magnetic poles wander naturally
- Outer core fluid motion generates field

HIGH CONFIDENCE (>80%):
- Equilibrium climate sensitivity: 2.5-4.0°C per doubling
- ENSO will continue oscillating
- AMO will continue oscillating
- Ocean will continue absorbing CO2 (but less efficiently)
- Magnetic field will continue changing

MEDIUM CONFIDENCE (50-80%):
- Regional climate projections
- Extreme weather attribution
- Tipping point locations
- AMOC behavior this century
- Cloud feedback sign and magnitude

LOW CONFIDENCE (<50%):
- Decadal climate predictions
- When/if AMOC will collapse
- Permafrost feedback magnitude
- Pole movement beyond ~5 years
- Reversal timing (centuries to millions of years)


WHAT GOOD SCIENCE REQUIRES:
===========================
1. State confidence levels explicitly
2. Distinguish observation from inference
3. Acknowledge uncertainties
4. Update with new evidence
5. Resist confirmation bias
6. Separate physics from politics
""")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("RESEARCH SUMMARY")
print("=" * 70)

print("""
KEY TAKEAWAYS:
==============

1. CLIMATE OSCILLATIONS
   - ENSO (2-7 yr): Strongest interannual driver
   - PDO (20-30 yr): North Pacific, affects ENSO expression
   - AMO (60-80 yr): Atlantic, affects hurricanes/Europe
   - These modulate regional climate but don't cause long-term trends

2. CO2 AND WARMING
   - Greenhouse physics is well-established (19th century)
   - Radiative forcing: ΔF = 5.35 × ln(C/C₀) W/m²
   - Direct effect: ~1.1°C per doubling
   - With feedbacks: ~3°C per doubling (uncertain: 2.5-4.0)
   - Current: 420 ppm, +1.2°C, accelerating

3. MAGNETIC POLE DRIFT
   - Pole racing from Canada to Siberia (~55 km/year)
   - Caused by fluid flow in outer core
   - NOT related to climate change
   - NOT a sign of imminent reversal
   - Requires frequent navigation model updates

4. CRITICAL THINKING
   - Distinguish physics (certain) from predictions (uncertain)
   - Multiple systems operate independently
   - Don't conflate correlation with causation
   - Beware of fringe theories (cosmic rays, magnetics→climate)


NEXT RESEARCH DIRECTIONS:
=========================
1. ENSO prediction skill and limits
2. Cloud feedback observations from space
3. Paleoclimate constraints on sensitivity
4. AMOC monitoring (RAPID array)
5. Core flow models from satellite magnetometry
""")

print("\n" + "=" * 70)
print("END OF LONG-TERM CLIMATE & EARTH SYSTEMS RESEARCH")
print("=" * 70)
