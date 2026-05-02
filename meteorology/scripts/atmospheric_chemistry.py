#!/usr/bin/env python3
"""
ATMOSPHERIC CHEMISTRY - FIRST PRINCIPLES
=========================================

Deriving the physics and chemistry of air quality,
ozone formation, aerosols, and atmospheric reactions.
"""

import numpy as np

print("=" * 70)
print("ATMOSPHERIC CHEMISTRY - FIRST PRINCIPLES")
print("=" * 70)


# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================
k_B = 1.381e-23    # Boltzmann constant (J/K)
N_A = 6.022e23     # Avogadro's number
R = 8.314          # Gas constant (J/mol/K)
h = 6.626e-34      # Planck constant


# =============================================================================
# PART 1: ATMOSPHERIC COMPOSITION
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: ATMOSPHERIC COMPOSITION")
print("=" * 70)

composition_text = """
ATMOSPHERIC COMPOSITION:
========================

DRY AIR (by volume):

Species          Mixing ratio      Residence time
─────────────────────────────────────────────────────
N₂               78.08%            Geological
O₂               20.95%            ~10,000 years
Ar               0.93%             Geological
CO₂              ~420 ppm          ~100 years
Ne               18 ppm            Geological
He               5 ppm             Geological
CH₄              ~1.9 ppm          ~10 years
H₂               0.5 ppm           ~2 years
N₂O              ~330 ppb          ~120 years
O₃               10-100 ppb        Days to months
CO               50-200 ppb        ~2 months

WATER VAPOR:

Highly variable: 0-4% by volume
Residence time: ~10 days

TRACE GASES (pollutants):

NO₂              0.1-100 ppb       ~1 day
SO₂              0.1-10 ppb        ~1 day (clean)
VOCs             1-1000 ppb        Hours to days

MIXING RATIO UNITS:

ppm = parts per million = μmol/mol = 10⁻⁶
ppb = parts per billion = nmol/mol = 10⁻⁹
ppt = parts per trillion = pmol/mol = 10⁻¹²

CONVERSION TO CONCENTRATION:

n = P × χ / (R × T)

Where χ = mixing ratio (volume)

At STP (1 atm, 25°C):
1 ppm ≈ 40.9 μg/m³ × (M/29)

Where M = molecular weight
"""
print(composition_text)

def mixing_ratio_to_concentration(mixing_ratio_ppm, P_Pa=101325, T_K=298, M_gmol=29):
    """
    Convert mixing ratio to mass concentration.

    Returns μg/m³
    """
    # Number density (mol/m³)
    n_total = P_Pa / (R * T_K)
    # Moles of species per m³
    n_species = n_total * mixing_ratio_ppm * 1e-6
    # Mass concentration
    conc = n_species * M_gmol * 1e6  # μg/m³
    return conc

def concentration_to_mixing_ratio(conc_ugm3, P_Pa=101325, T_K=298, M_gmol=29):
    """Convert mass concentration to mixing ratio."""
    n_total = P_Pa / (R * T_K)
    n_species = conc_ugm3 / (M_gmol * 1e6)
    mixing_ratio = n_species / n_total * 1e6  # ppm
    return mixing_ratio

print("\nConversion Examples:")
print("-" * 60)
print(f"{'Species':<12} {'Mixing ratio':<15} {'Concentration'}")
print("-" * 60)

species_data = [
    ("CO₂", 420, 44),
    ("CH₄", 1.9, 16),
    ("O₃", 0.050, 48),  # 50 ppb
    ("NO₂", 0.020, 46),  # 20 ppb
    ("SO₂", 0.005, 64),  # 5 ppb
]

for name, ppm, M in species_data:
    conc = mixing_ratio_to_concentration(ppm, M_gmol=M)
    if ppm < 1:
        print(f"{name:<12} {ppm*1000:.0f} ppb{'':<8} {conc:.1f} μg/m³")
    else:
        print(f"{name:<12} {ppm:.1f} ppm{'':<9} {conc:.0f} μg/m³")


# =============================================================================
# PART 2: PHOTOCHEMISTRY
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: PHOTOCHEMISTRY")
print("=" * 70)

photochem_text = """
PHOTOCHEMISTRY:
===============

Light drives atmospheric chemistry!

PHOTODISSOCIATION:

AB + hν → A + B

Energy requirement:
E = hν = hc/λ

BOND DISSOCIATION ENERGIES:

Bond          D (kJ/mol)    λ_threshold (nm)
───────────────────────────────────────────────
O=O           498           240
O-O (in O₃)   107           1120
N=O (NO₂)     305           393
H-O-H         498           240
C-C           347           345

PHOTOLYSIS RATE:

J = ∫ σ(λ) × Φ(λ) × F(λ) dλ

Where:
- σ(λ) = absorption cross-section
- Φ(λ) = quantum yield
- F(λ) = actinic flux (photons/cm²/s/nm)

KEY PHOTOLYSIS REACTIONS:

1. O₃ + hν → O₂ + O(¹D)        λ < 320 nm
              → O₂ + O(³P)     λ = 320-1100 nm

2. NO₂ + hν → NO + O           λ < 420 nm

3. HCHO + hν → H + HCO         λ < 330 nm
              → H₂ + CO        λ < 360 nm

4. H₂O₂ + hν → 2 OH            λ < 350 nm

OH RADICAL - THE ATMOSPHERIC DETERGENT:

Most important oxidant!
Concentration: ~10⁶ molecules/cm³ (daytime)
Lifetime: ~1 second

OH + CO → CO₂ + H
OH + CH₄ → CH₃ + H₂O
OH + VOC → products
"""
print(photochem_text)

def photon_energy(wavelength_nm):
    """Calculate photon energy in kJ/mol."""
    c = 3e8  # m/s
    wavelength_m = wavelength_nm * 1e-9
    E_joule = h * c / wavelength_m
    E_kJ_mol = E_joule * N_A / 1000
    return E_kJ_mol

def threshold_wavelength(bond_energy_kJ_mol):
    """Calculate threshold wavelength for photodissociation."""
    c = 3e8
    E_joule = bond_energy_kJ_mol * 1000 / N_A
    wavelength_m = h * c / E_joule
    return wavelength_m * 1e9  # nm

print("\nPhoton Energy vs Wavelength:")
print("-" * 50)
print(f"{'Wavelength (nm)':<18} {'Energy (kJ/mol)':<18} {'Region'}")
print("-" * 50)

wavelengths = [200, 254, 300, 350, 400, 500, 700]
regions = ["UV-C", "UV-C", "UV-B", "UV-A", "Visible", "Visible", "Red"]

for wl, region in zip(wavelengths, regions):
    E = photon_energy(wl)
    print(f"{wl:<18} {E:<18.0f} {region}")


# =============================================================================
# PART 3: TROPOSPHERIC OZONE
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: TROPOSPHERIC OZONE (SMOG)")
print("=" * 70)

ozone_text = """
TROPOSPHERIC OZONE FORMATION:
=============================

Ground-level ozone is a POLLUTANT
(Unlike stratospheric ozone which protects us)

THE NULL CYCLE (no net O₃ production):

NO₂ + hν → NO + O           (J_NO2 ~ 0.01 s⁻¹)
O + O₂ + M → O₃             (fast)
O₃ + NO → NO₂ + O₂          (k ~ 2×10⁻¹² cm³/s)

Net: Nothing! Just cycles NO ↔ NO₂

PHOTOSTATIONARY STATE:

[O₃] = J_NO2 × [NO₂] / (k × [NO])

WHY DOES O₃ ACCUMULATE?

VOCs (Volatile Organic Compounds) break the cycle!

RH + OH → R + H₂O
R + O₂ → RO₂
RO₂ + NO → RO + NO₂         ← Converts NO to NO₂ WITHOUT consuming O₃!
RO + O₂ → R'CHO + HO₂
HO₂ + NO → OH + NO₂         ← Again, NO → NO₂

Net result:
RH + 4 O₂ + 2 hν → R'CHO + 2 O₃ + H₂O

ONE VOC MOLECULE → TWO OZONE MOLECULES!

OZONE ISOPLETHS:

O₃ production depends on:
- NOx concentration
- VOC concentration
- VOC/NOx ratio

NOx-limited: More NOx → more O₃
VOC-limited: More VOC → more O₃
             More NOx → LESS O₃ (!!)

Urban areas often VOC-limited
Rural areas often NOx-limited
"""
print(ozone_text)

def photostationary_ozone(NO2_ppb, NO_ppb, J_NO2=0.01):
    """
    Photostationary state ozone concentration.

    [O₃] = J × [NO₂] / (k × [NO])
    """
    k = 2e-12 * 2.5e10  # Convert to ppb units (approx)
    if NO_ppb == 0:
        return float('inf')
    O3 = J_NO2 * NO2_ppb / (k * NO_ppb) * 1e12
    return O3

def ozone_production_rate(VOC_ppb, NOx_ppb, k_OH_VOC=5e-12):
    """
    Simplified ozone production rate.

    P(O₃) depends on VOC, NOx, and their ratio.
    """
    # Simplified: P ∝ [VOC][NOx] at low NOx
    #             P ∝ [VOC] at high NOx (VOC-limited)

    NOx_threshold = 10  # ppb, transition

    if NOx_ppb < NOx_threshold:
        # NOx-limited
        P = 0.1 * VOC_ppb * NOx_ppb / NOx_threshold
    else:
        # VOC-limited
        P = 0.1 * VOC_ppb * (1 + np.log(NOx_ppb / NOx_threshold))

    return P  # Relative production rate

print("\nOzone Production Regimes:")
print("-" * 60)
print(f"{'VOC (ppb)':<12} {'NOx (ppb)':<12} {'VOC/NOx':<12} {'O₃ production':<15} {'Regime'}")
print("-" * 60)

for voc in [50, 100, 200]:
    for nox in [5, 20, 50]:
        ratio = voc / nox
        P = ozone_production_rate(voc, nox)
        regime = "NOx-limited" if nox < 10 else "VOC-limited"
        print(f"{voc:<12} {nox:<12} {ratio:<12.0f} {P:<15.1f} {regime}")


# =============================================================================
# PART 4: AEROSOLS
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: AEROSOL PHYSICS")
print("=" * 70)

aerosol_text = """
AEROSOL PHYSICS:
================

Aerosols = suspended particles in air
Size: 1 nm to 100 μm

SIZE DISTRIBUTIONS:

Mode              Size range        Sources
────────────────────────────────────────────────────
Nucleation        1-10 nm           Gas-to-particle conversion
Aitken            10-100 nm         Combustion, condensation
Accumulation      100 nm - 1 μm     Coagulation, cloud processing
Coarse            > 1 μm            Dust, sea salt, pollen

LOG-NORMAL DISTRIBUTION:

n(D) = N / (√(2π) ln(σ_g) D) × exp[-(ln D - ln D_g)² / (2 ln²σ_g)]

Where:
- N = total number concentration
- D_g = geometric mean diameter
- σ_g = geometric standard deviation

LIFETIME AND REMOVAL:

Nucleation mode: minutes to hours (coagulation)
Accumulation mode: days to weeks (wet deposition)
Coarse mode: hours to days (sedimentation)

OPTICAL PROPERTIES:

Extinction coefficient:
b_ext = b_scat + b_abs

Visibility:
V ≈ 3.9 / b_ext

PM2.5 and visibility:
b_ext ≈ 3 × [PM2.5] (approx, Mm⁻¹ per μg/m³)

AEROSOL OPTICAL DEPTH (AOD):

τ = ∫ b_ext dz

Clean: τ < 0.1
Moderate: τ = 0.1-0.3
Polluted: τ = 0.3-1.0
Severe: τ > 1.0
"""
print(aerosol_text)

def settling_velocity(diameter_um, rho_particle=2000):
    """
    Stokes settling velocity for aerosol.

    v = ρ_p × D² × g / (18 × μ)
    """
    mu = 1.8e-5  # Air viscosity (Pa·s)
    D = diameter_um * 1e-6  # Convert to meters
    rho_air = 1.2  # kg/m³

    # Stokes law (valid for Re < 1)
    v = rho_particle * D**2 * 9.81 / (18 * mu)

    # Cunningham correction for small particles
    lambda_mfp = 0.065e-6  # Mean free path (m)
    Cc = 1 + (2 * lambda_mfp / D) * (1.257 + 0.4 * np.exp(-0.55 * D / lambda_mfp))

    return v * Cc * 100  # cm/s

def visibility_from_pm25(pm25_ugm3):
    """
    Estimate visibility from PM2.5.

    Based on empirical relationships.
    """
    # b_ext ≈ 3 × PM2.5 (Mm⁻¹)
    b_ext = 3 * pm25_ugm3 + 10  # Add Rayleigh background
    V_km = 3900 / b_ext  # Koschmieder equation
    return V_km

print("\nAerosol Settling Velocities:")
print("-" * 55)
print(f"{'Diameter (μm)':<18} {'Settling velocity (cm/s)':<25} {'Lifetime'}")
print("-" * 55)

for D in [0.01, 0.1, 1, 10, 50, 100]:
    v = settling_velocity(D)
    # Estimate lifetime in 1 km mixed layer
    if v > 0:
        lifetime_hr = 100000 / (v * 3600)
        if lifetime_hr < 1:
            life_str = f"{lifetime_hr*60:.0f} min"
        elif lifetime_hr < 24:
            life_str = f"{lifetime_hr:.0f} hr"
        else:
            life_str = f"{lifetime_hr/24:.1f} days"
    else:
        life_str = "Very long"
    print(f"{D:<18} {v:<25.4f} {life_str}")

print("\n\nPM2.5 and Visibility:")
print("-" * 50)
print(f"{'PM2.5 (μg/m³)':<18} {'Visibility (km)':<18} {'Air quality'}")
print("-" * 50)

for pm in [5, 12, 35, 55, 100, 200, 500]:
    V = visibility_from_pm25(pm)
    if pm <= 12:
        aq = "Good"
    elif pm <= 35:
        aq = "Moderate"
    elif pm <= 55:
        aq = "Unhealthy (sensitive)"
    elif pm <= 150:
        aq = "Unhealthy"
    else:
        aq = "Hazardous"
    print(f"{pm:<18} {V:<18.1f} {aq}")


# =============================================================================
# PART 5: ACID DEPOSITION
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: ACID DEPOSITION")
print("=" * 70)

acid_text = """
ACID RAIN CHEMISTRY:
====================

SULFUR PATHWAY:

SO₂ emissions (coal, volcanoes)
↓
Gas-phase oxidation:
SO₂ + OH → HOSO₂
HOSO₂ + O₂ → HO₂ + SO₃
SO₃ + H₂O → H₂SO₄

Aqueous-phase oxidation (in cloud):
SO₂ + H₂O ↔ H₂SO₃
H₂SO₃ + H₂O₂ → H₂SO₄ + H₂O
H₂SO₃ + O₃ → H₂SO₄ + O₂

Sulfuric acid: H₂SO₄ (strong acid, pKa << 0)

NITROGEN PATHWAY:

NO + O₃ → NO₂ + O₂
NO₂ + OH → HNO₃ (daytime)
N₂O₅ + H₂O → 2 HNO₃ (nighttime)

Nitric acid: HNO₃ (strong acid)

NATURAL RAIN pH:

Pure water: pH = 7
With CO₂ equilibrium:
CO₂ + H₂O ↔ H₂CO₃ ↔ H⁺ + HCO₃⁻

Natural rain pH ≈ 5.6

ACID RAIN:

pH < 5.6 (often pH 4-5)
Most acidic recorded: pH ≈ 2 (like lemon juice!)

IMPACTS:
- Lake acidification (fish kills)
- Forest damage
- Building/monument erosion
- Soil chemistry changes

RECOVERY:

Clean Air Act (US): SO₂ down 90% since 1980
Rain pH recovering in eastern US/Europe
"""
print(acid_text)

def rain_ph_from_acids(H2SO4_mol_L, HNO3_mol_L, NH3_mol_L=0):
    """
    Estimate rain pH from acid/base concentrations.

    Simplified: H⁺ = 2×[H₂SO₄] + [HNO₃] - [NH₃]
    Plus background from CO₂
    """
    # Background H+ from CO₂ equilibrium
    H_background = 10**(-5.6)

    # Strong acids fully dissociate
    H_acids = 2 * H2SO4_mol_L + HNO3_mol_L

    # Ammonia neutralizes
    H_net = H_background + H_acids - NH3_mol_L

    if H_net <= 0:
        return 7.0  # Neutral

    pH = -np.log10(H_net)
    return pH

def sulfate_from_so2(so2_ppb, oxidation_rate=0.01):
    """
    Estimate sulfate formation from SO2.

    Rate ~ 1%/hr in gas phase, faster in clouds
    """
    # Conversion over 24 hours
    fraction_converted = 1 - np.exp(-oxidation_rate * 24)
    sulfate = so2_ppb * fraction_converted * 96/64  # MW ratio
    return sulfate

print("\nAcid Rain Formation:")
print("-" * 60)
print(f"{'SO₂ (ppb)':<12} {'NO₂ (ppb)':<12} {'Sulfate formed':<18} {'Est. rain pH'}")
print("-" * 60)

for so2 in [1, 5, 20, 50]:
    for no2 in [5, 20, 50]:
        sulfate = sulfate_from_so2(so2)
        # Very rough pH estimate
        H2SO4 = sulfate * 1e-9 * 40.9 / 1000  # mol/L approximation
        HNO3 = no2 * 0.3 * 1e-9 * 40.9 / 1000
        pH = rain_ph_from_acids(H2SO4, HNO3)
        if so2 == 5:
            print(f"{so2:<12} {no2:<12} {sulfate:<18.1f} {pH:.1f}")


# =============================================================================
# PART 6: METHANE AND CARBON CYCLE
# =============================================================================
print("\n" + "=" * 70)
print("PART 6: METHANE CHEMISTRY")
print("=" * 70)

methane_text = """
METHANE (CH₄):
==============

Second most important anthropogenic greenhouse gas
GWP₁₀₀ = 28-36 (vs CO₂ = 1)

SOURCES (Tg CH₄/yr):

Natural:
- Wetlands: 150-200
- Termites: 10-20
- Ocean: 10-15
- Hydrates: 5-10

Anthropogenic (~60% of total):
- Livestock: 90-100
- Rice paddies: 30-40
- Fossil fuels: 80-100
- Landfills: 40-50
- Biomass burning: 30-40

Total: ~550-600 Tg/yr

SINKS:

OH oxidation (troposphere): ~500 Tg/yr
Soil uptake: ~30 Tg/yr
Stratospheric loss: ~40 Tg/yr

Lifetime: ~10 years

OXIDATION CHAIN:

CH₄ + OH → CH₃ + H₂O           k = 2.5×10⁻¹² × exp(-1775/T)
CH₃ + O₂ + M → CH₃O₂ + M
CH₃O₂ + NO → CH₃O + NO₂
CH₃O + O₂ → HCHO + HO₂
HCHO + hν → H₂ + CO  or  H + HCO

Net: CH₄ + 4 O₂ + 2 hν → CO₂ + H₂O + H₂O + products

METHANE FEEDBACK:

More CH₄ → depletes OH → CH₄ lasts longer → more CH₄
Positive feedback factor: ~1.3-1.4

CLIMATE IMPACT:

Current: ~1.9 ppm (up from 0.7 ppm pre-industrial)
Radiative forcing: ~0.5 W/m² (direct)
"""
print(methane_text)

def methane_lifetime(oh_concentration=1e6):
    """
    Calculate methane lifetime.

    τ = 1 / (k × [OH])
    """
    T = 270  # Representative tropospheric T
    k = 2.5e-12 * np.exp(-1775/T)  # cm³/molecule/s

    tau_seconds = 1 / (k * oh_concentration)
    tau_years = tau_seconds / (365.25 * 24 * 3600)
    return tau_years

def methane_gwp(time_horizon=100):
    """
    Estimate methane Global Warming Potential.

    GWP = integrated forcing relative to CO₂
    """
    # Simplified: accounts for decay
    tau_ch4 = 10  # years

    if time_horizon == 20:
        return 84
    elif time_horizon == 100:
        return 28
    else:
        # Rough interpolation
        return 28 * (1 + np.exp(-time_horizon/tau_ch4))

print("\nMethane Lifetime vs OH:")
print("-" * 50)
print(f"{'[OH] (molec/cm³)':<20} {'CH₄ lifetime (years)'}")
print("-" * 50)

for oh in [5e5, 1e6, 1.5e6, 2e6]:
    tau = methane_lifetime(oh)
    print(f"{oh:<20.1e} {tau:.1f}")

print("\n\nMethane GWP by Time Horizon:")
print("-" * 40)
for horizon in [20, 100, 500]:
    gwp = methane_gwp(horizon)
    print(f"GWP_{horizon}: {gwp}")


# =============================================================================
# PART 7: AIR QUALITY INDEX
# =============================================================================
print("\n" + "=" * 70)
print("PART 7: AIR QUALITY INDEX (AQI)")
print("=" * 70)

aqi_text = """
AIR QUALITY INDEX:
==================

Standardized scale for communicating air quality

US EPA AQI:

AQI Range    Category              Health Impact
──────────────────────────────────────────────────────────
0-50         Good                  None
51-100       Moderate              Sensitive groups
101-150      Unhealthy (sensitive) Sensitive groups affected
151-200      Unhealthy             General public affected
201-300      Very unhealthy        Health alert
301-500      Hazardous             Emergency conditions

POLLUTANTS INCLUDED:

1. PM2.5 (24-hr average)
   AQI 100 = 35 μg/m³
   AQI 500 = 500 μg/m³

2. PM10 (24-hr average)
   AQI 100 = 150 μg/m³

3. O₃ (8-hr average)
   AQI 100 = 70 ppb

4. NO₂ (1-hr average)
   AQI 100 = 100 ppb

5. SO₂ (1-hr average)
   AQI 100 = 75 ppb

6. CO (8-hr average)
   AQI 100 = 9 ppm

CALCULATION:

AQI = (AQI_hi - AQI_lo)/(C_hi - C_lo) × (C - C_lo) + AQI_lo

Overall AQI = maximum of individual pollutant AQIs
"""
print(aqi_text)

def pm25_to_aqi(pm25):
    """
    Convert PM2.5 (μg/m³) to AQI.

    US EPA breakpoints.
    """
    breakpoints = [
        (0, 12, 0, 50),
        (12.1, 35.4, 51, 100),
        (35.5, 55.4, 101, 150),
        (55.5, 150.4, 151, 200),
        (150.5, 250.4, 201, 300),
        (250.5, 500.4, 301, 500),
    ]

    for C_lo, C_hi, AQI_lo, AQI_hi in breakpoints:
        if C_lo <= pm25 <= C_hi:
            AQI = (AQI_hi - AQI_lo) / (C_hi - C_lo) * (pm25 - C_lo) + AQI_lo
            return int(AQI)

    return 500  # Beyond scale

def aqi_category(aqi):
    """Return AQI category."""
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 150:
        return "Unhealthy (sensitive)"
    elif aqi <= 200:
        return "Unhealthy"
    elif aqi <= 300:
        return "Very unhealthy"
    else:
        return "Hazardous"

print("\nPM2.5 to AQI Conversion:")
print("-" * 55)
print(f"{'PM2.5 (μg/m³)':<18} {'AQI':<10} {'Category'}")
print("-" * 55)

for pm in [5, 12, 25, 35, 55, 100, 150, 250, 400]:
    aqi = pm25_to_aqi(pm)
    cat = aqi_category(aqi)
    print(f"{pm:<18} {aqi:<10} {cat}")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: ATMOSPHERIC CHEMISTRY")
print("=" * 70)

summary = """
KEY ATMOSPHERIC CHEMISTRY:
=========================

1. COMPOSITION
   - N₂ (78%), O₂ (21%), trace gases
   - Mixing ratio ↔ concentration conversion
   - Residence times: seconds to geological

2. PHOTOCHEMISTRY
   - E = hc/λ determines which bonds break
   - J = ∫σΦF dλ (photolysis rate)
   - OH radical: atmospheric detergent

3. TROPOSPHERIC OZONE
   - Null cycle: NO₂ ↔ NO (no net O₃)
   - VOCs break cycle → O₃ accumulates
   - NOx-limited vs VOC-limited regimes

4. AEROSOLS
   - Sizes: 1 nm to 100 μm
   - Settling: v ∝ D² (Stokes)
   - Visibility: V ≈ 3.9/b_ext

5. ACID DEPOSITION
   - SO₂ → H₂SO₄ (sulfuric acid)
   - NO₂ → HNO₃ (nitric acid)
   - Natural rain pH ≈ 5.6
   - Acid rain pH < 5

6. METHANE
   - τ ≈ 10 years
   - GWP₁₀₀ = 28
   - Positive OH feedback

7. AIR QUALITY
   - AQI: 0-500 scale
   - PM2.5, O₃, NO₂, SO₂, CO
   - Health impacts quantified


THE PHYSICS/CHEMISTRY TELLS US:
==============================
- Sunlight drives atmospheric chemistry
- OH controls lifetime of most pollutants
- VOC+NOx → ozone (counterintuitive!)
- Particle size determines fate
- Acid rain largely solved (policy works!)
- Methane is potent but short-lived
"""
print(summary)

print("\n" + "=" * 70)
print("END OF ATMOSPHERIC CHEMISTRY")
print("=" * 70)
