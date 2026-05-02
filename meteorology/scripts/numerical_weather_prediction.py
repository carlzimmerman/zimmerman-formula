#!/usr/bin/env python3
"""
NUMERICAL WEATHER PREDICTION - FIRST PRINCIPLES
================================================

How weather forecasting actually works: from observations
to equations to predictions.
"""

import numpy as np

print("=" * 70)
print("NUMERICAL WEATHER PREDICTION (NWP) - FIRST PRINCIPLES")
print("=" * 70)


# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================
omega = 7.29e-5     # Earth rotation (rad/s)
R_earth = 6.371e6   # Earth radius (m)
g = 9.81            # Gravity (m/s²)
R_d = 287.0         # Gas constant dry air (J/kg/K)
c_p = 1004          # Specific heat (J/kg/K)


# =============================================================================
# PART 1: THE PRIMITIVE EQUATIONS
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: GOVERNING EQUATIONS OF THE ATMOSPHERE")
print("=" * 70)

equations_text = """
THE PRIMITIVE EQUATIONS:
========================

All NWP models solve these 7 equations for 7 unknowns:
(u, v, w, T, q, p, ρ)

1. MOMENTUM (Newton's 2nd Law + Coriolis):

   ∂u/∂t = -u∂u/∂x - v∂u/∂y - w∂u/∂z - (1/ρ)∂p/∂x + fv + F_x

   ∂v/∂t = -u∂v/∂x - v∂v/∂y - w∂v/∂z - (1/ρ)∂p/∂y - fu + F_y

   (Acceleration = Advection + Pressure gradient + Coriolis + Friction)

2. HYDROSTATIC BALANCE:
   ∂p/∂z = -ρg

   (Vertical pressure gradient balances gravity)

3. CONTINUITY (mass conservation):
   ∂ρ/∂t + ∇·(ρV) = 0

4. THERMODYNAMIC (energy):
   ∂T/∂t = -V·∇T + (Q/c_p) + (g w/c_p)

   (Temperature changes from advection, heating, compression)

5. MOISTURE:
   ∂q/∂t = -V·∇q + E - C

   (Humidity changes from advection, evaporation, condensation)

6. EQUATION OF STATE:
   p = ρ R T

   (Connects pressure, density, temperature)

These are NONLINEAR PARTIAL DIFFERENTIAL EQUATIONS
- No analytical solution exists!
- Must solve numerically
"""
print(equations_text)


# =============================================================================
# PART 2: DISCRETIZATION - FROM CONTINUOUS TO DISCRETE
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: DISCRETIZATION")
print("=" * 70)

discretization_text = """
MAKING EQUATIONS COMPUTABLE:
============================

SPATIAL DISCRETIZATION:
Divide atmosphere into a 3D GRID

Modern global models:
- Horizontal: ~10-25 km spacing
- Vertical: 50-150 levels (hybrid σ-p)
- Total grid points: ~10⁹ to 10¹⁰

Example: ECMWF IFS (2024)
- 9 km horizontal (Tco1279)
- 137 vertical levels
- ~1 billion grid points

FINITE DIFFERENCES:
∂T/∂x ≈ (T(x+Δx) - T(x-Δx)) / (2Δx)

More sophisticated: Spectral methods
- Represent fields as spherical harmonics
- Better for global models

TIME DISCRETIZATION:
Step forward in time:
T(t+Δt) = T(t) + (∂T/∂t) × Δt

Typical Δt: 1-10 minutes
- Must satisfy CFL condition: Δt < Δx/c
- c = fastest wave speed (~300 m/s for sound)
"""
print(discretization_text)

def cfl_timestep(dx, c_wave=300):
    """Calculate maximum stable timestep."""
    return dx / c_wave

def grid_points_global(resolution_km, n_levels=100):
    """Estimate number of grid points for global model."""
    circumference = 2 * np.pi * R_earth / 1000  # km
    n_lon = circumference / resolution_km
    n_lat = n_lon / 2
    return n_lon * n_lat * n_levels

print("\nGrid Resolution and Computational Load:")
print("-" * 70)
print(f"{'Resolution (km)':<18} {'Grid points':<18} {'CFL Δt (s)':<15} {'Steps/day'}")
print("-" * 70)

for res in [100, 50, 25, 10, 5, 2]:
    points = grid_points_global(res)
    dt = cfl_timestep(res * 1000)
    steps = 86400 / dt
    print(f"{res:<18} {points:<18.2e} {dt:<15.0f} {steps:<.0f}")


# =============================================================================
# PART 3: DATA ASSIMILATION
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: DATA ASSIMILATION - THE INITIAL STATE")
print("=" * 70)

da_text = """
THE INITIAL VALUE PROBLEM:
==========================

Weather prediction is an INITIAL VALUE PROBLEM:
Given the state now, predict the future.

But we don't KNOW the exact state now!
- Observations are sparse, noisy, incomplete
- Need to ESTIMATE the best initial conditions

DATA ASSIMILATION combines:
1. Short-range forecast (background/first guess)
2. New observations
3. Error statistics

METHODS:

1. 3D-VAR (3-Dimensional Variational):
   Minimize: J = (x-x_b)ᵀB⁻¹(x-x_b) + (y-Hx)ᵀR⁻¹(y-Hx)

   Where:
   - x = analysis state
   - x_b = background (forecast)
   - y = observations
   - H = observation operator
   - B = background error covariance
   - R = observation error covariance

2. 4D-VAR (4-Dimensional):
   Same but includes time evolution
   More accurate, more expensive

3. ENSEMBLE KALMAN FILTER:
   Use ensemble of forecasts for error statistics
   Better for chaotic systems

OBSERVATION TYPES:
- Surface stations: 10,000+
- Radiosondes: ~1000 (2× daily)
- Aircraft (AMDAR): 300,000/day
- Satellites: Billions of measurements
  - Polar orbiters (temperature profiles)
  - Geostationary (clouds, winds)
  - GPS radio occultation
"""
print(da_text)

def observation_density_impact(n_obs, forecast_error):
    """
    Simplified impact of observations on analysis error.

    Analysis error ≈ background error × √(n_background / (n_background + n_obs))
    """
    n_background = 100  # Effective degrees of freedom per region
    analysis_error = forecast_error * np.sqrt(n_background / (n_background + n_obs))
    return analysis_error

print("\nObservation Impact on Analysis Error:")
print("-" * 60)
print(f"{'Observations':<20} {'Analysis error (relative)':<25}")
print("-" * 60)

for n_obs in [0, 10, 50, 100, 500, 1000]:
    error = observation_density_impact(n_obs, 1.0)
    print(f"{n_obs:<20} {error:<25.2f}")


# =============================================================================
# PART 4: PARAMETERIZATION
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: PARAMETERIZATION - SUBGRID PROCESSES")
print("=" * 70)

param_text = """
THE SUBGRID PROBLEM:
====================

Many important processes are SMALLER than grid spacing:
- Cumulus clouds (~1 km)
- Turbulence (~1-100 m)
- Microphysics (~μm to mm)
- Radiation (molecular scale)

These must be PARAMETERIZED:
Represent bulk effect using grid-scale variables

MAJOR PARAMETERIZATIONS:

1. CONVECTION
   - Detect instability (CAPE, CIN)
   - Compute cloud mass flux
   - Distribute heating, moistening, momentum
   - Schemes: Kain-Fritsch, Betts-Miller, Tiedtke

2. RADIATION
   - Shortwave (solar): reflection, absorption
   - Longwave (terrestrial): emission, absorption
   - Need to know: clouds, aerosols, gases
   - Very expensive: done every ~1-3 hours

3. BOUNDARY LAYER
   - Turbulent fluxes of heat, moisture, momentum
   - Monin-Obukhov similarity
   - PBL height evolution

4. MICROPHYSICS
   - Phase changes
   - Droplet/ice growth
   - Precipitation formation
   - 1-moment to 3-moment schemes

5. GRAVITY WAVE DRAG
   - Unresolved mountain waves
   - Momentum deposition in stratosphere

Parameterizations are the MAIN source of model error!
"""
print(param_text)


# =============================================================================
# PART 5: ENSEMBLE FORECASTING
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: ENSEMBLE FORECASTING")
print("=" * 70)

ensemble_text = """
DEALING WITH CHAOS:
===================

Weather is CHAOTIC: small errors grow exponentially
- Perfect forecast impossible beyond ~2 weeks
- But we can quantify UNCERTAINTY

ENSEMBLE APPROACH:
Run multiple forecasts with:
1. Perturbed initial conditions
2. (Sometimes) perturbed physics

Ensemble size: 20-100 members

PRODUCTS:
- Ensemble mean (best estimate)
- Ensemble spread (uncertainty)
- Probability distributions
- Extreme scenario identification

ENSEMBLE SPREAD:
At t=0: Spread small (all start similar)
As t increases: Spread grows
Eventually: Spread = climatological variance (no skill)

RELIABILITY:
Good ensemble: Observations fall within spread
with correct frequency (probabilistic calibration)

OPERATIONAL SYSTEMS:
- ECMWF ENS: 51 members, 15 days, 18 km
- GFS: 31 members, 16 days, 25 km
- UKMO MOGREPS: 44 members
"""
print(ensemble_text)

def ensemble_spread_growth(n_days, initial_spread=0.01, e_folding=2.5):
    """
    Model ensemble spread growth.

    Spread grows exponentially until saturation.
    """
    climatological_spread = 1.0  # Normalized
    spread = initial_spread * np.exp(n_days / e_folding)
    return min(spread, climatological_spread)

print("\nEnsemble Spread Growth Over Time:")
print("-" * 50)
print(f"{'Day':<10} {'Spread (normalized)':<25} {'Useful?'}")
print("-" * 50)

for day in range(0, 17, 2):
    spread = ensemble_spread_growth(day)
    useful = "Yes" if spread < 0.5 else "Marginal" if spread < 0.8 else "No"
    print(f"{day:<10} {spread:<25.2f} {useful}")


# =============================================================================
# PART 6: FORECAST VERIFICATION
# =============================================================================
print("\n" + "=" * 70)
print("PART 6: VERIFICATION - ARE FORECASTS ANY GOOD?")
print("=" * 70)

verification_text = """
FORECAST VERIFICATION METRICS:
==============================

1. DETERMINISTIC SCORES:

   RMSE = √[(1/n) Σ(F - O)²]
   Root Mean Square Error

   MAE = (1/n) Σ|F - O|
   Mean Absolute Error

   Bias = (1/n) Σ(F - O)
   Systematic over/under prediction

   Correlation: How well patterns match

2. PROBABILISTIC SCORES:

   Brier Score (for binary events):
   BS = (1/n) Σ(p - o)²
   Where p = probability, o = 0 or 1

   CRPS (Continuous Ranked Probability Score):
   For full distributions

3. SKILL SCORES:
   Compare to reference (climatology or persistence):

   Skill = 1 - (Score_forecast / Score_reference)

   Skill > 0: Better than reference
   Skill = 1: Perfect forecast
   Skill < 0: Worse than reference!

CURRENT FORECAST SKILL (approx):
Day 1: 95% of useful skill
Day 3: 85% of useful skill
Day 5: 70% of useful skill
Day 7: 50% of useful skill
Day 10: 25% of useful skill
Day 14: ~10% of useful skill
"""
print(verification_text)

def forecast_skill_decay(day, skill_halflife=4):
    """Model forecast skill decay with lead time."""
    return 0.95 * (0.5 ** (day / skill_halflife))

print("\nForecast Skill vs Lead Time:")
print("-" * 50)
print(f"{'Lead time':<15} {'Skill':<15} {'Useful info retained'}")
print("-" * 50)

for day in [1, 2, 3, 5, 7, 10, 14]:
    skill = forecast_skill_decay(day)
    print(f"{day:<15} {skill:<15.2f} {skill*100:.0f}%")


# =============================================================================
# PART 7: MODEL HIERARCHY
# =============================================================================
print("\n" + "=" * 70)
print("PART 7: OPERATIONAL MODEL HIERARCHY")
print("=" * 70)

models_text = """
OPERATIONAL NWP SYSTEMS:
========================

GLOBAL MODELS:
- ECMWF IFS: 9 km, arguably best global model
- GFS (NCEP): 13 km, US operational
- UKMO: 10 km, UK Met Office
- GEM (Canada): 15 km
- JMA: 20 km, Japan

REGIONAL MODELS (higher resolution):
- HRRR (US): 3 km, hourly updates
- NAM (US): 12 km / 3 km nested
- AROME (France): 1.3 km
- UKV (UK): 1.5 km

CONVECTION-ALLOWING:
- Grid spacing < 4 km
- Explicitly resolve convection
- No convective parameterization
- Better for severe weather

MODEL RUNS:
- Global: Every 6-12 hours
- Regional: Every 1-6 hours
- Initialization to output: 1-4 hours

COMPUTING REQUIREMENTS:
Modern NWP center: 10-100 petaFLOPS
Power: 1-10 MW
Cost: $10-100 million/year
"""
print(models_text)

print("\nModel Resolution Comparison:")
print("-" * 70)
print(f"{'Model':<15} {'Resolution':<15} {'Domain':<15} {'Update freq':<15}")
print("-" * 70)

models = [
    ("ECMWF IFS", "9 km", "Global", "6-hourly"),
    ("GFS", "13 km", "Global", "6-hourly"),
    ("NAM", "12 km", "N. America", "6-hourly"),
    ("HRRR", "3 km", "CONUS", "Hourly"),
    ("AROME", "1.3 km", "France", "Hourly"),
    ("ICON-D2", "2 km", "Germany", "Hourly"),
]

for model, res, domain, freq in models:
    print(f"{model:<15} {res:<15} {domain:<15} {freq:<15}")


# =============================================================================
# PART 8: FUTURE OF NWP
# =============================================================================
print("\n" + "=" * 70)
print("PART 8: FUTURE OF WEATHER PREDICTION")
print("=" * 70)

future_text = """
FUTURE DIRECTIONS:
==================

1. HIGHER RESOLUTION
   - Global models → 1-5 km by 2030
   - Resolve more convection explicitly
   - Need exascale computing

2. MACHINE LEARNING / AI
   - Neural network weather models (GraphCast, Pangu, FourCastNet)
   - 1000× faster than physics models
   - Approaching physics model skill
   - BUT: Need physics for rare events

3. BETTER OBSERVATIONS
   - More satellites (commercial + gov)
   - Improved data assimilation
   - Uncrewed aerial systems

4. COUPLED MODELS
   - Ocean-atmosphere coupling
   - Land surface improvements
   - Aerosol-chemistry coupling

5. SUBSEASONAL-TO-SEASONAL (S2S)
   - Bridge weather-climate gap
   - 2 weeks to 2 months
   - Predictability from MJO, soil moisture, sea ice

FUNDAMENTAL LIMITS:
- 2 weeks: Weather predictability limit (chaos)
- BUT: Probabilistic skill extends further
- Climate predictions: Different problem (forced response)
"""
print(future_text)


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: NUMERICAL WEATHER PREDICTION")
print("=" * 70)

summary = """
KEY NWP CONCEPTS:
================

1. EQUATIONS
   - Primitive equations (7 equations, 7 unknowns)
   - Momentum, continuity, thermodynamic, moisture
   - Nonlinear PDEs with no analytical solution

2. DISCRETIZATION
   - 3D grid: 10⁹ - 10¹⁰ points
   - Time steps: 1-10 minutes
   - CFL condition limits stability

3. DATA ASSIMILATION
   - Combine forecast + observations
   - 3D-VAR, 4D-VAR, EnKF
   - Creates best initial conditions

4. PARAMETERIZATION
   - Subgrid processes: convection, radiation, PBL
   - Main source of model error
   - Active research area

5. ENSEMBLES
   - Multiple forecasts quantify uncertainty
   - 20-100 members typical
   - Spread → confidence

6. VERIFICATION
   - RMSE, MAE, Brier Score, CRPS
   - Skill score vs climatology
   - ~50% skill at day 7

7. MODEL HIERARCHY
   - Global (9-25 km) + Regional (1-5 km)
   - Convection-allowing < 4 km
   - Hourly to 6-hourly updates


THE PHYSICS IS COMPLETE:
========================
NWP is applied physics + applied math + massive computation.
The equations are RIGHT; errors come from:
- Initial condition uncertainty
- Resolution limitations
- Parameterization approximations
- Chaos (fundamental limit)
"""
print(summary)

print("\n" + "=" * 70)
print("END OF NUMERICAL WEATHER PREDICTION")
print("=" * 70)
