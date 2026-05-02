#!/usr/bin/env python3
"""
ATMOSPHERIC PREDICTABILITY - FIRST PRINCIPLES
==============================================

Deriving the physics of chaos, Lyapunov exponents,
error growth, and the fundamental limits of weather prediction.
"""

import numpy as np

print("=" * 70)
print("ATMOSPHERIC PREDICTABILITY - FIRST PRINCIPLES")
print("=" * 70)


# =============================================================================
# PART 1: CHAOS AND SENSITIVITY TO INITIAL CONDITIONS
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: CHAOS IN THE ATMOSPHERE")
print("=" * 70)

chaos_text = """
WHAT IS CHAOS?
==============

DETERMINISTIC CHAOS:
- Deterministic system (no randomness)
- Bounded solutions
- Sensitive dependence on initial conditions
- Long-term unpredictability

LORENZ DISCOVERY (1963):

Edward Lorenz found that simple atmospheric equations:

dx/dt = σ(y - x)
dy/dt = x(ρ - z) - y
dz/dt = xy - βz

With σ=10, ρ=28, β=8/3:
→ CHAOTIC behavior!

KEY INSIGHT:

Two solutions starting 0.000001 apart:
- After short time: still close
- After longer time: completely different trajectories!
- The "butterfly effect"

"Does the flap of a butterfly's wings in Brazil
set off a tornado in Texas?" - Lorenz, 1972

SENSITIVITY TO INITIAL CONDITIONS:

Small error δ₀ at t=0 grows as:
δ(t) ≈ δ₀ × e^(λt)

Where λ = LYAPUNOV EXPONENT

If λ > 0: CHAOTIC (errors grow exponentially)
If λ < 0: Stable (errors decay)
If λ = 0: Neutral

ATMOSPHERE: λ ≈ 1/(2 days) = 0.5/day

Error DOUBLES every 2 days!
"""
print(chaos_text)

def error_growth(initial_error, lyapunov_exponent, time):
    """
    Calculate error growth in chaotic system.

    δ(t) = δ₀ × exp(λt)
    """
    return initial_error * np.exp(lyapunov_exponent * time)

def doubling_time(lyapunov_exponent):
    """
    Time for error to double.

    t_double = ln(2) / λ
    """
    return np.log(2) / lyapunov_exponent

def predictability_limit(initial_error, final_error, lyapunov_exponent):
    """
    Time until error reaches saturation.

    t_pred = (1/λ) × ln(δ_sat / δ₀)
    """
    return (1/lyapunov_exponent) * np.log(final_error / initial_error)

# Atmospheric Lyapunov exponent
lambda_atm = 0.5  # per day (error doubles every ~2 days)

print("\nError Growth in Atmosphere:")
print(f"Lyapunov exponent: λ ≈ {lambda_atm} /day")
print(f"Error doubling time: {doubling_time(lambda_atm):.1f} days")

print("\n" + "-" * 60)
print(f"{'Day':<10} {'Error growth factor':<25} {'Remaining predictability'}")
print("-" * 60)

for day in range(0, 17, 2):
    growth = error_growth(1, lambda_atm, day)
    # Saturation when error = climatological variance
    remaining = max(0, 14 - day)  # Rough
    print(f"{day:<10} {growth:<25.1f} {remaining} days")


# =============================================================================
# PART 2: LORENZ'S TWO TYPES OF PREDICTABILITY
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: TWO TYPES OF PREDICTABILITY")
print("=" * 70)

two_types_text = """
LORENZ'S INSIGHT (1969):
========================

TWO FUNDAMENTALLY DIFFERENT PREDICTABILITY PROBLEMS:

1. FIRST KIND: Initial value problem
   - How long can we predict from today's state?
   - Limited by chaos (Lyapunov growth)
   - Weather forecasting (days to 2 weeks)

2. SECOND KIND: Boundary value problem
   - Given external forcing, what's the statistics?
   - Not limited by chaos!
   - Climate prediction (years to centuries)

ANALOGY: ROLLING DICE

First kind: Predict the SEQUENCE of rolls
- Impossible beyond first roll
- Deterministic but chaotic

Second kind: Predict the STATISTICS
- Average = 3.5
- Variance = 35/12
- Perfectly predictable!

FOR ATMOSPHERE:

Weather (1st kind): "Will it rain on April 26, 2027?"
→ Impossible beyond ~2 weeks

Climate (2nd kind): "What's average April rainfall?"
→ Predictable decades ahead (given CO₂, etc.)

THE BOUNDARY CONDITIONS:

Climate depends on:
- Solar forcing (known)
- Greenhouse gases (can be projected)
- Land surface (known)
- Ocean state (partially predictable)

These SET the climate statistics!
Weather is sampling from that distribution.
"""
print(two_types_text)


# =============================================================================
# PART 3: THE PREDICTABILITY LIMIT
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: THE ~2 WEEK LIMIT")
print("=" * 70)

limit_text = """
THE FUNDAMENTAL LIMIT:
======================

WHY ~2 WEEKS?

Error doubling time: τ ≈ 2 days
Initial error: δ₀ ~ analysis error
Saturation: δ_max ~ climatological variance

Number of doublings needed:
n = log₂(δ_max / δ₀)

For atmosphere:
δ₀ / δ_max ≈ 0.1 (10% of variance)
n ≈ log₂(10) ≈ 3.3

Total time: n × τ = 3.3 × 2 = 6.6 days

BUT WAIT - why is practical limit 14 days?

THE ERROR SPECTRUM:

Different scales have different growth rates!

Small scales: Fast error growth (hours)
Large scales: Slower error growth (days)

Error "cascade" from small to large:
Small → Medium → Large → Saturate

SCALE-DEPENDENT PREDICTABILITY:

Scale (km)    Predictability limit
───────────────────────────────────
10            ~1 hour
100           ~1 day
1000          ~3-5 days
5000          ~10-14 days

LIMITS TO IMPROVEMENT:

Even PERFECT observations + PERFECT model:
Still ~2-3 weeks maximum for weather!

Why? Observing every molecule impossible
Some uncertainty ALWAYS remains
"""
print(limit_text)

def scale_predictability(scale_km):
    """
    Rough predictability limit for given scale.

    Derived from scale-dependent Lyapunov exponent.
    """
    # Larger scales have longer predictability
    # Approximately: t_pred ~ scale^(2/3)
    t_days = 0.5 * (scale_km / 100)**(2/3)
    return min(t_days, 14)  # Cap at 2 weeks

print("\nScale-Dependent Predictability:")
print("-" * 50)
print(f"{'Scale (km)':<15} {'Predictability limit'}")
print("-" * 50)

for scale in [10, 50, 100, 500, 1000, 2000, 5000, 10000]:
    t = scale_predictability(scale)
    if t < 1:
        print(f"{scale:<15} {t*24:.0f} hours")
    else:
        print(f"{scale:<15} {t:.1f} days")


# =============================================================================
# PART 4: FORECAST SKILL AND IMPROVEMENT
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: FORECAST IMPROVEMENT OVER TIME")
print("=" * 70)

improvement_text = """
FORECAST SKILL IMPROVEMENT:
===========================

HISTORICAL PROGRESS:

The useful forecast range has extended ~1 day per decade!

Year    Useful forecast range
─────────────────────────────
1950    ~1-2 days
1970    ~3-4 days
1990    ~5-6 days
2010    ~7-8 days
2024    ~9-10 days

WHY IMPROVEMENT?

1. BETTER OBSERVATIONS
   - Satellites (1960s onward)
   - Radiosondes network
   - Aircraft data (AMDAR)
   - GPS radio occultation

2. BETTER MODELS
   - Higher resolution
   - Better physics parameterization
   - Coupled atmosphere-ocean

3. BETTER DATA ASSIMILATION
   - 4D-VAR
   - Ensemble Kalman filter
   - Satellite radiance assimilation

4. MORE COMPUTING POWER
   - Exascale computing
   - Higher resolution possible

DIMINISHING RETURNS:

Each improvement takes MORE effort
Approaching fundamental limit
~2 weeks is HARD ceiling

CURRENT ECMWF SKILL:

Day 3:  ~95% of theoretical limit
Day 5:  ~85% of theoretical limit
Day 7:  ~70% of theoretical limit
Day 10: ~50% of theoretical limit
Day 15: ~25% of theoretical limit
"""
print(improvement_text)

def forecast_skill(day, practical_limit=10):
    """
    Model forecast skill vs lead time.

    Skill = 1 - (RMSE_forecast / RMSE_climatology)²
    """
    if day == 0:
        return 1.0

    # Exponential decay with half-life ~4 days
    half_life = 4
    skill = np.exp(-0.693 * day / half_life)
    return skill

def theoretical_vs_practical(day, current_practical=10, theoretical=14):
    """
    Compare current skill to theoretical limit.
    """
    skill_current = forecast_skill(day, current_practical)
    skill_theoretical = forecast_skill(day, theoretical)

    if skill_theoretical > 0:
        ratio = skill_current / skill_theoretical
    else:
        ratio = 0
    return skill_current, skill_theoretical, ratio

print("\nForecast Skill Comparison:")
print("-" * 65)
print(f"{'Day':<8} {'Current skill':<18} {'Theoretical':<18} {'% of limit'}")
print("-" * 65)

for day in [1, 2, 3, 5, 7, 10, 14]:
    curr, theo, ratio = theoretical_vs_practical(day)
    print(f"{day:<8} {curr:<18.2f} {theo:<18.2f} {ratio*100:.0f}%")


# =============================================================================
# PART 5: ENSEMBLE FORECASTING
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: ENSEMBLE FORECASTING")
print("=" * 70)

ensemble_text = """
EMBRACING UNCERTAINTY:
======================

Since we can't eliminate uncertainty, QUANTIFY it!

ENSEMBLE APPROACH:

Run N forecasts with:
1. Perturbed initial conditions
2. (Optionally) perturbed physics

Each member samples possible error growth paths

ENSEMBLE PRODUCTS:

1. ENSEMBLE MEAN
   - Average of all members
   - Filters out unpredictable noise
   - Often more skillful than single forecast!

2. ENSEMBLE SPREAD
   - Standard deviation of members
   - Estimates uncertainty
   - Should match RMSE (reliability)

3. PROBABILITY FORECASTS
   - P(rain > 5mm) = fraction of members
   - More useful than deterministic!

INITIAL PERTURBATIONS:

Methods:
a) Bred vectors (grow fastest errors)
b) Singular vectors (optimal error growth)
c) Ensemble Kalman filter (from DA ensemble)

Size: ~ analysis uncertainty

THE ATTRACTOR:

In chaos theory: STRANGE ATTRACTOR
- All trajectories approach it
- But trajectory on attractor is unpredictable
- Ensemble samples the attractor

SPREAD-SKILL RELATIONSHIP:

Good ensemble: Spread ≈ expected error
- Large spread → low confidence
- Small spread → high confidence
- Calibration is KEY
"""
print(ensemble_text)

def ensemble_spread_growth(day, initial_spread=0.1, e_folding=2):
    """
    Model ensemble spread growth.

    Spread grows then saturates at climatological variance.
    """
    spread = initial_spread * np.exp(day / e_folding)
    saturated = min(spread, 1.0)  # Normalized to climatological variance
    return saturated

def ensemble_skill_vs_spread(n_members, spread, truth_in_spread_pct=68):
    """
    Model reliability: fraction of time truth within spread.

    Perfect ensemble: 68% within 1 sigma, 95% within 2 sigma
    """
    # More members → better sampling → more reliable
    reliability = truth_in_spread_pct * (1 - 1/np.sqrt(n_members))
    return reliability

print("\nEnsemble Spread Growth:")
print("-" * 50)
print(f"{'Day':<10} {'Spread (normalized)':<25} {'Useful?'}")
print("-" * 50)

for day in range(0, 17, 2):
    spread = ensemble_spread_growth(day)
    useful = "Yes" if spread < 0.7 else "Marginal" if spread < 0.9 else "No"
    print(f"{day:<10} {spread:<25.2f} {useful}")

print("\n\nEnsemble Size and Reliability:")
print("-" * 50)
print(f"{'N members':<15} {'Expected reliability'}")
print("-" * 50)

for n in [10, 20, 31, 51, 100]:
    rel = ensemble_skill_vs_spread(n, 0.5)
    print(f"{n:<15} {rel:.0f}%")


# =============================================================================
# PART 6: EXTENDED-RANGE PREDICTABILITY
# =============================================================================
print("\n" + "=" * 70)
print("PART 6: PREDICTABILITY BEYOND 2 WEEKS")
print("=" * 70)

extended_text = """
SUBSEASONAL-TO-SEASONAL (S2S):
==============================

Gap between weather (2 weeks) and climate (seasons+)

CAN WE PREDICT 2 WEEKS TO 2 MONTHS?

Yes! But differently than weather:
- Not synoptic details
- Statistical shifts in probability

SOURCES OF S2S PREDICTABILITY:

1. MADDEN-JULIAN OSCILLATION (MJO)
   - 30-60 day tropical oscillation
   - Affects global weather patterns
   - Predictable 2-4 weeks ahead!

2. STRATOSPHERE-TROPOSPHERE COUPLING
   - SSW events → surface impacts
   - 2-4 week influence
   - Added skill in winter

3. SOIL MOISTURE
   - Memory effect (weeks to months)
   - Affects temperature/rainfall
   - Important over land

4. SEA ICE
   - Slow evolution
   - Affects Arctic/midlatitude patterns
   - Monthly timescale

5. OCEAN MEMORY
   - SST anomalies persist
   - El Niño/La Niña (months)
   - Predictable 6-12 months ahead

PRACTICAL S2S SKILL:

Week 2: Significant skill (overlap with weather)
Week 3: Some skill (pattern-dependent)
Week 4: Limited skill
Month 2: Mainly from ENSO/MJO

THE "PREDICTABILITY DESERT":

Weeks 3-4 are hardest!
- Weather skill gone
- S2S signals emerging but weak
"""
print(extended_text)

def s2s_skill(week, mjo_phase=None, enso_state=None):
    """
    Estimate S2S skill based on conditions.
    """
    base_skill = 0.5 ** (week / 2)  # Decay

    # MJO enhancement
    if mjo_phase and week < 4:
        base_skill += 0.1

    # ENSO enhancement
    if enso_state in ['El Nino', 'La Nina'] and week > 2:
        base_skill += 0.15

    return min(base_skill, 0.9)

print("\nS2S Predictability Sources:")
print("-" * 65)
print(f"{'Week':<8} {'Base skill':<15} {'With MJO':<15} {'With ENSO':<15}")
print("-" * 65)

for week in [1, 2, 3, 4, 6, 8]:
    base = s2s_skill(week)
    mjo = s2s_skill(week, mjo_phase=3)
    enso = s2s_skill(week, enso_state='El Nino')
    print(f"{week:<8} {base:<15.2f} {mjo:<15.2f} {enso:.2f}")


# =============================================================================
# PART 7: AI/ML AND PREDICTABILITY
# =============================================================================
print("\n" + "=" * 70)
print("PART 7: AI/ML WEATHER PREDICTION")
print("=" * 70)

ai_text = """
AI WEATHER MODELS (2022-2024):
==============================

BREAKTHROUGH: Neural network weather models
approaching physics-based model skill!

EXAMPLES:
- Google DeepMind: GraphCast, GenCast
- Huawei: Pangu-Weather
- NVIDIA: FourCastNet
- Microsoft: ClimaX

ADVANTAGES:
- 1000× faster than physics models
- Can learn from data directly
- May find patterns humans miss

CURRENT STATUS (2024):
- 10-day forecasts competitive with ECMWF
- Some metrics BEAT physics models
- Rapidly improving

BUT: FUNDAMENTAL LIMITS REMAIN!

AI CANNOT:
✗ Beat the chaos limit (~2 weeks)
✗ Create information not in initial state
✗ Violate thermodynamics

AI STILL NEEDS:
✓ Physics models for training data
✓ Good initial conditions (from physics DA)
✓ Physical constraints for extremes

THE FUTURE:

Hybrid approaches likely:
- AI for fast ensemble generation
- Physics for data assimilation
- AI for post-processing
- Physics for novel situations

Chaos doesn't care if prediction is from
physics or AI - the limit is the limit!
"""
print(ai_text)

print("\nAI vs Physics Model Comparison (2024):")
print("-" * 60)
print(f"{'Metric':<25} {'ECMWF IFS':<18} {'GraphCast'}")
print("-" * 60)

comparisons = [
    ("Runtime (10-day)", "~1 hour", "~1 minute"),
    ("Day 5 RMSE (Z500)", "Baseline", "~5% better"),
    ("Day 10 RMSE (Z500)", "Baseline", "Comparable"),
    ("Extreme events", "Good", "Learning"),
    ("Tropical cyclones", "Good", "Improving"),
    ("Uncertainty quant.", "Ensembles", "Emerging"),
]

for metric, ecmwf, ai in comparisons:
    print(f"{metric:<25} {ecmwf:<18} {ai}")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: ATMOSPHERIC PREDICTABILITY")
print("=" * 70)

summary = """
KEY PREDICTABILITY PHYSICS:
==========================

1. CHAOS
   - Sensitive dependence on initial conditions
   - Lyapunov exponent λ ≈ 0.5/day
   - Error doubles every ~2 days
   - Fundamental, not fixable!

2. TWO TYPES OF PREDICTABILITY
   - 1st kind: Weather (initial value, ~2 weeks)
   - 2nd kind: Climate (boundary value, unlimited)
   - Different problems, different limits

3. THE ~2 WEEK LIMIT
   - Error grows exponentially
   - Saturates at climatological variance
   - Scale-dependent: larger = longer
   - Even perfect model: ~14-17 days max

4. FORECAST IMPROVEMENT
   - ~1 day per decade over 50 years
   - Observations + models + computing
   - Diminishing returns approaching limit

5. ENSEMBLE FORECASTING
   - Quantify uncertainty
   - Spread should match error
   - Probability > deterministic
   - Embraces rather than fights chaos

6. EXTENDED RANGE (S2S)
   - MJO: 2-4 weeks
   - Stratosphere: 2-4 weeks
   - Soil moisture: weeks-months
   - ENSO: 6-12 months

7. AI/ML
   - 1000× faster than physics
   - Approaching physics skill
   - CANNOT beat chaos limit
   - Hybrid future likely


THE PHYSICS TELLS US:
====================
- Weather prediction has a HARD ceiling (~2 weeks)
- This is PHYSICS, not lack of technology
- Climate prediction is different (boundary forcing)
- Uncertainty quantification (ensembles) is essential
- Progress continues but with diminishing returns
"""
print(summary)

print("\n" + "=" * 70)
print("END OF ATMOSPHERIC PREDICTABILITY")
print("=" * 70)
