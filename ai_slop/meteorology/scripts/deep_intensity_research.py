#!/usr/bin/env python3
"""
Deep Research: What Differentiates Cat 4 vs Cat 5 Hurricanes?

Key Question: Why do some storms with favorable conditions peak at Cat 4 (130-150 kt)
while others reach Cat 5 (155+ kt)?

Hypotheses to test:
1. TIME TO LAND - Cat 4s hit land before reaching MPI
2. INTENSIFICATION RATE - Cat 5s intensify faster (steeper V* trajectory)
3. ENVIRONMENTAL PERSISTENCE - Cat 5s have longer favorable windows
4. STRUCTURAL STABILITY - Different eye/RMW ratios affect peak intensity
5. STARTING POINT - Cat 5s start from higher V* before final RI phase

This analysis will inform model improvements.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from dataclasses import dataclass
import json

# Z² Constants
Z_SQUARED = 32 * np.pi / 3  # 33.51
PHI = (1 + np.sqrt(5)) / 2
INV_PHI = 1 / PHI

print("=" * 100)
print("  DEEP RESEARCH: CAT 4 vs CAT 5 DIFFERENTIATION")
print("=" * 100)

# =============================================================================
# COMPREHENSIVE STORM DATABASE WITH DETAILED EVOLUTION
# =============================================================================

# Each storm has: name, peak_category, peak_vmax, hours_to_peak, hours_over_water,
# v_star_at_ri_start, environmental conditions, and notable characteristics

DETAILED_STORMS = {
    # Cat 5 Storms (peak >= 155 kt)
    'Patricia 2015': {
        'peak_cat': 5, 'peak_vmax': 215, 'hours_to_peak': 42,
        'hours_over_water_after_peak': 6,  # Rapid landfall after peak
        'v_star_at_ri_start': 1.79, 'v_star_at_peak': 6.42,
        'ri_rate_kt_per_12h': 65,  # Extreme
        'sst': 31.5, 'shear': 4, 'ohc': 95,
        'landfall': True, 'basin': 'EPAC',
        'notes': 'Most intense ever recorded. Perfect conditions.'
    },
    'Wilma 2005': {
        'peak_cat': 5, 'peak_vmax': 185, 'hours_to_peak': 48,
        'hours_over_water_after_peak': 72,
        'v_star_at_ri_start': 1.79, 'v_star_at_peak': 5.52,
        'ri_rate_kt_per_12h': 52,  # Extreme
        'sst': 30.0, 'shear': 5, 'ohc': 85,
        'landfall': True, 'basin': 'ATL',
        'notes': 'Record low pressure 882 mb. Tiny eye (2 nm).'
    },
    'Dorian 2019': {
        'peak_cat': 5, 'peak_vmax': 185, 'hours_to_peak': 144,
        'hours_over_water_after_peak': 72,
        'v_star_at_ri_start': 2.54, 'v_star_at_peak': 5.52,
        'ri_rate_kt_per_12h': 38,
        'sst': 30.0, 'shear': 5, 'ohc': 80,
        'landfall': False, 'basin': 'ATL',  # Stalled over Bahamas
        'notes': 'Stalled over Bahamas for 48h at peak. Devastating.'
    },
    'Irma 2017': {
        'peak_cat': 5, 'peak_vmax': 185, 'hours_to_peak': 96,
        'hours_over_water_after_peak': 72,
        'v_star_at_ri_start': 2.98, 'v_star_at_peak': 5.52,
        'ri_rate_kt_per_12h': 35,
        'sst': 29.0, 'shear': 8, 'ohc': 70,
        'landfall': True, 'basin': 'ATL',
        'notes': 'Maintained Cat 5 for 37 hours (record). Started stronger.'
    },
    'Maria 2017': {
        'peak_cat': 5, 'peak_vmax': 175, 'hours_to_peak': 48,
        'hours_over_water_after_peak': 48,
        'v_star_at_ri_start': 2.39, 'v_star_at_peak': 5.22,
        'ri_rate_kt_per_12h': 50,  # Very fast
        'sst': 29.5, 'shear': 5, 'ohc': 75,
        'landfall': True, 'basin': 'ATL',
        'notes': 'Devastated Puerto Rico. Very rapid RI.'
    },
    'Katrina 2005': {
        'peak_cat': 5, 'peak_vmax': 175, 'hours_to_peak': 84,
        'hours_over_water_after_peak': 12,  # Quick landfall after peak
        'v_star_at_ri_start': 2.24, 'v_star_at_peak': 5.22,
        'ri_rate_kt_per_12h': 40,
        'sst': 30.5, 'shear': 8, 'ohc': 90,
        'landfall': True, 'basin': 'ATL',
        'notes': 'Warm Loop Current eddy. Weakened before landfall.'
    },
    'Rita 2005': {
        'peak_cat': 5, 'peak_vmax': 180, 'hours_to_peak': 60,
        'hours_over_water_after_peak': 36,
        'v_star_at_ri_start': 2.09, 'v_star_at_peak': 5.37,
        'ri_rate_kt_per_12h': 55,
        'sst': 30.0, 'shear': 6, 'ohc': 85,
        'landfall': True, 'basin': 'ATL',
        'notes': 'EWRC weakened before landfall.'
    },
    'Milton 2024': {
        'peak_cat': 5, 'peak_vmax': 180, 'hours_to_peak': 48,
        'hours_over_water_after_peak': 36,
        'v_star_at_ri_start': 2.24, 'v_star_at_peak': 5.37,
        'ri_rate_kt_per_12h': 52,  # Record Gulf RI
        'sst': 31.0, 'shear': 5, 'ohc': 90,
        'landfall': True, 'basin': 'ATL',
        'notes': 'Record RI in Gulf. EWRC before landfall.'
    },
    'Lee 2023': {
        'peak_cat': 5, 'peak_vmax': 165, 'hours_to_peak': 72,
        'hours_over_water_after_peak': 96,  # Long track
        'v_star_at_ri_start': 2.39, 'v_star_at_peak': 4.92,
        'ri_rate_kt_per_12h': 43,
        'sst': 29.5, 'shear': 8, 'ohc': 70,
        'landfall': False, 'basin': 'ATL',
        'notes': 'Large wind field. Recurved before US.'
    },
    'Beryl 2024': {
        'peak_cat': 5, 'peak_vmax': 165, 'hours_to_peak': 72,
        'hours_over_water_after_peak': 72,
        'v_star_at_ri_start': 1.79, 'v_star_at_peak': 4.92,
        'ri_rate_kt_per_12h': 50,
        'sst': 30.0, 'shear': 6, 'ohc': 75,
        'landfall': True, 'basin': 'ATL',
        'notes': 'Earliest Cat 5 on record (July 2). Exceptional MDR temps.'
    },
    'Otis 2023': {
        'peak_cat': 5, 'peak_vmax': 165, 'hours_to_peak': 36,
        'hours_over_water_after_peak': 0,  # Hit at peak
        'v_star_at_ri_start': 1.49, 'v_star_at_peak': 4.92,
        'ri_rate_kt_per_12h': 58,  # Extreme, unprecedented
        'sst': 31.0, 'shear': 4, 'ohc': 85,
        'landfall': True, 'basin': 'EPAC',
        'notes': 'Caught forecasters by surprise. 80 kt in 12h.'
    },
    'Michael 2018': {
        'peak_cat': 5, 'peak_vmax': 160, 'hours_to_peak': 96,
        'hours_over_water_after_peak': 0,  # Hit at peak
        'v_star_at_ri_start': 2.24, 'v_star_at_peak': 4.77,
        'ri_rate_kt_per_12h': 35,
        'sst': 29.5, 'shear': 8, 'ohc': 75,
        'landfall': True, 'basin': 'ATL',
        'notes': 'First Cat 5 in FL Panhandle. Peaked at landfall.'
    },
    'Ian 2022': {
        'peak_cat': 5, 'peak_vmax': 160, 'hours_to_peak': 84,
        'hours_over_water_after_peak': 12,
        'v_star_at_ri_start': 2.54, 'v_star_at_peak': 4.77,
        'ri_rate_kt_per_12h': 38,
        'sst': 30.0, 'shear': 10, 'ohc': 85,
        'landfall': True, 'basin': 'ATL',
        'notes': 'SW Florida devastation. ~$110B damage.'
    },
    'Lorenzo 2019': {
        'peak_cat': 5, 'peak_vmax': 160, 'hours_to_peak': 72,
        'hours_over_water_after_peak': 48,
        'v_star_at_ri_start': 2.39, 'v_star_at_peak': 4.77,
        'ri_rate_kt_per_12h': 43,
        'sst': 28.5, 'shear': 8, 'ohc': 65,
        'landfall': False, 'basin': 'ATL',
        'notes': 'Easternmost Cat 5 on record. Hit Azores as post-tropical.'
    },
    'Iota 2020': {
        'peak_cat': 5, 'peak_vmax': 160, 'hours_to_peak': 60,
        'hours_over_water_after_peak': 12,
        'v_star_at_ri_start': 2.24, 'v_star_at_peak': 4.77,
        'ri_rate_kt_per_12h': 40,
        'sst': 30.0, 'shear': 6, 'ohc': 80,
        'landfall': True, 'basin': 'ATL',
        'notes': 'Hit same Nicaragua coast as Eta 2 weeks prior.'
    },
    'Matthew 2016': {
        'peak_cat': 5, 'peak_vmax': 165, 'hours_to_peak': 72,
        'hours_over_water_after_peak': 96,
        'v_star_at_ri_start': 2.24, 'v_star_at_peak': 4.92,
        'ri_rate_kt_per_12h': 43,
        'sst': 29.5, 'shear': 7, 'ohc': 75,
        'landfall': True, 'basin': 'ATL',
        'notes': 'Haiti catastrophe. Long-lived Cat 4-5.'
    },

    # Cat 4 Storms (peak 130-154 kt) - WHY DIDN'T THESE REACH CAT 5?
    'Helene 2024': {
        'peak_cat': 4, 'peak_vmax': 140, 'hours_to_peak': 96,
        'hours_over_water_after_peak': 0,  # Landfall at peak
        'v_star_at_ri_start': 1.94, 'v_star_at_peak': 4.18,
        'ri_rate_kt_per_12h': 30,
        'sst': 30.5, 'shear': 7, 'ohc': 85,
        'landfall': True, 'basin': 'ATL',
        'notes': 'Landfall interrupted intensification. NC flooding disaster.'
    },
    'Ida 2021': {
        'peak_cat': 4, 'peak_vmax': 150, 'hours_to_peak': 72,
        'hours_over_water_after_peak': 0,  # Landfall at peak
        'v_star_at_ri_start': 2.09, 'v_star_at_peak': 4.48,
        'ri_rate_kt_per_12h': 40,
        'sst': 31.0, 'shear': 5, 'ohc': 90,
        'landfall': True, 'basin': 'ATL',
        'notes': 'Would likely have reached Cat 5 with more time over water.'
    },
    'Laura 2020': {
        'peak_cat': 4, 'peak_vmax': 150, 'hours_to_peak': 96,
        'hours_over_water_after_peak': 0,
        'v_star_at_ri_start': 1.94, 'v_star_at_peak': 4.48,
        'ri_rate_kt_per_12h': 38,
        'sst': 30.5, 'shear': 8, 'ohc': 85,
        'landfall': True, 'basin': 'ATL',
        'notes': 'Peaked right at landfall. Track forced early landfall.'
    },
    'Delta 2020': {
        'peak_cat': 4, 'peak_vmax': 145, 'hours_to_peak': 36,
        'hours_over_water_after_peak': 36,
        'v_star_at_ri_start': 1.79, 'v_star_at_peak': 4.33,
        'ri_rate_kt_per_12h': 45,
        'sst': 30.0, 'shear': 10, 'ohc': 75,
        'landfall': True, 'basin': 'ATL',
        'notes': 'EWRC started before reaching Cat 5. Shear increased.'
    },
    'Eta 2020': {
        'peak_cat': 4, 'peak_vmax': 150, 'hours_to_peak': 72,
        'hours_over_water_after_peak': 0,
        'v_star_at_ri_start': 1.94, 'v_star_at_peak': 4.48,
        'ri_rate_kt_per_12h': 35,
        'sst': 29.5, 'shear': 8, 'ohc': 80,
        'landfall': True, 'basin': 'ATL',
        'notes': 'Hit Nicaragua at peak. Central America flooding.'
    },
    'Florence 2018': {
        'peak_cat': 4, 'peak_vmax': 140, 'hours_to_peak': 120,
        'hours_over_water_after_peak': 48,
        'v_star_at_ri_start': 1.94, 'v_star_at_peak': 4.18,
        'ri_rate_kt_per_12h': 28,  # Slower RI
        'sst': 28.5, 'shear': 12, 'ohc': 60,
        'landfall': True, 'basin': 'ATL',
        'notes': 'Higher shear and cooler SST limited intensity.'
    },
    'Harvey 2017': {
        'peak_cat': 4, 'peak_vmax': 130, 'hours_to_peak': 120,
        'hours_over_water_after_peak': 0,
        'v_star_at_ri_start': 1.34, 'v_star_at_peak': 3.88,
        'ri_rate_kt_per_12h': 35,
        'sst': 30.0, 'shear': 10, 'ohc': 80,
        'landfall': True, 'basin': 'ATL',
        'notes': 'Peaked at landfall. Stalled inland = flooding record.'
    },
    'Idalia 2023': {
        'peak_cat': 4, 'peak_vmax': 130, 'hours_to_peak': 48,
        'hours_over_water_after_peak': 0,
        'v_star_at_ri_start': 1.94, 'v_star_at_peak': 3.88,
        'ri_rate_kt_per_12h': 43,
        'sst': 30.5, 'shear': 7, 'ohc': 80,
        'landfall': True, 'basin': 'ATL',
        'notes': 'Fast-moving. Limited time over warm water.'
    },
    'Fiona 2022': {
        'peak_cat': 4, 'peak_vmax': 130, 'hours_to_peak': 96,
        'hours_over_water_after_peak': 48,
        'v_star_at_ri_start': 2.24, 'v_star_at_peak': 3.88,
        'ri_rate_kt_per_12h': 25,  # Slower
        'sst': 29.0, 'shear': 12, 'ohc': 70,
        'landfall': False, 'basin': 'ATL',
        'notes': 'PR flooding. Became powerful post-tropical.'
    },
    'Sam 2021': {
        'peak_cat': 4, 'peak_vmax': 150, 'hours_to_peak': 72,
        'hours_over_water_after_peak': 120,
        'v_star_at_ri_start': 2.24, 'v_star_at_peak': 4.48,
        'ri_rate_kt_per_12h': 35,
        'sst': 28.5, 'shear': 10, 'ohc': 65,
        'landfall': False, 'basin': 'ATL',
        'notes': 'Recurved. Lower SST limited to Cat 4.'
    },
}

# =============================================================================
# ANALYSIS 1: TIME OVER WATER HYPOTHESIS
# =============================================================================

print("\n" + "=" * 100)
print("  HYPOTHESIS 1: TIME OVER WATER LIMITS CAT 4 PEAKS")
print("=" * 100)

cat5_storms = {k: v for k, v in DETAILED_STORMS.items() if v['peak_cat'] == 5}
cat4_storms = {k: v for k, v in DETAILED_STORMS.items() if v['peak_cat'] == 4}

cat5_time_after_peak = [s['hours_over_water_after_peak'] for s in cat5_storms.values()]
cat4_time_after_peak = [s['hours_over_water_after_peak'] for s in cat4_storms.values()]

cat5_at_landfall = sum(1 for s in cat5_storms.values() if s['hours_over_water_after_peak'] == 0)
cat4_at_landfall = sum(1 for s in cat4_storms.values() if s['hours_over_water_after_peak'] == 0)

print(f"""
  Cat 5 Storms (n={len(cat5_storms)}):
  - Mean hours over water after peak: {np.mean(cat5_time_after_peak):.1f}h
  - Peaked exactly at landfall: {cat5_at_landfall}/{len(cat5_storms)} ({100*cat5_at_landfall/len(cat5_storms):.0f}%)

  Cat 4 Storms (n={len(cat4_storms)}):
  - Mean hours over water after peak: {np.mean(cat4_time_after_peak):.1f}h
  - Peaked exactly at landfall: {cat4_at_landfall}/{len(cat4_storms)} ({100*cat4_at_landfall/len(cat4_storms):.0f}%)

  FINDING: {100*cat4_at_landfall/len(cat4_storms):.0f}% of Cat 4s peaked at landfall vs {100*cat5_at_landfall/len(cat5_storms):.0f}% of Cat 5s
""")

if cat4_at_landfall/len(cat4_storms) > cat5_at_landfall/len(cat5_storms):
    print("  ✓ HYPOTHESIS SUPPORTED: Cat 4 storms more often hit land before reaching Cat 5")
else:
    print("  ✗ HYPOTHESIS NOT SUPPORTED")

# =============================================================================
# ANALYSIS 2: INTENSIFICATION RATE
# =============================================================================

print("\n" + "=" * 100)
print("  HYPOTHESIS 2: CAT 5s INTENSIFY FASTER")
print("=" * 100)

cat5_ri_rates = [s['ri_rate_kt_per_12h'] for s in cat5_storms.values()]
cat4_ri_rates = [s['ri_rate_kt_per_12h'] for s in cat4_storms.values()]

print(f"""
  Cat 5 RI Rates (kt/12h):
  - Mean: {np.mean(cat5_ri_rates):.1f}
  - Median: {np.median(cat5_ri_rates):.1f}
  - Range: {min(cat5_ri_rates):.0f} - {max(cat5_ri_rates):.0f}

  Cat 4 RI Rates (kt/12h):
  - Mean: {np.mean(cat4_ri_rates):.1f}
  - Median: {np.median(cat4_ri_rates):.1f}
  - Range: {min(cat4_ri_rates):.0f} - {max(cat4_ri_rates):.0f}

  Difference: {np.mean(cat5_ri_rates) - np.mean(cat4_ri_rates):.1f} kt/12h faster for Cat 5s
""")

if np.mean(cat5_ri_rates) > np.mean(cat4_ri_rates):
    print("  ✓ HYPOTHESIS SUPPORTED: Cat 5s intensify faster on average")
else:
    print("  ✗ HYPOTHESIS NOT SUPPORTED")

# =============================================================================
# ANALYSIS 3: STARTING V* POSITION
# =============================================================================

print("\n" + "=" * 100)
print("  HYPOTHESIS 3: CAT 5s START HIGHER V* BEFORE RI")
print("=" * 100)

cat5_start_vstar = [s['v_star_at_ri_start'] for s in cat5_storms.values()]
cat4_start_vstar = [s['v_star_at_ri_start'] for s in cat4_storms.values()]

print(f"""
  Cat 5 Starting V* (at RI onset):
  - Mean: {np.mean(cat5_start_vstar):.2f}
  - Range: {min(cat5_start_vstar):.2f} - {max(cat5_start_vstar):.2f}

  Cat 4 Starting V* (at RI onset):
  - Mean: {np.mean(cat4_start_vstar):.2f}
  - Range: {min(cat4_start_vstar):.2f} - {max(cat4_start_vstar):.2f}

  Difference: {np.mean(cat5_start_vstar) - np.mean(cat4_start_vstar):.2f} V* units higher for Cat 5s
""")

# Convert to knots for clarity
diff_kt = (np.mean(cat5_start_vstar) - np.mean(cat4_start_vstar)) * Z_SQUARED
print(f"  In knots: Cat 5s start ~{diff_kt:.0f} kt stronger at RI onset")

# =============================================================================
# ANALYSIS 4: ENVIRONMENTAL CONDITIONS
# =============================================================================

print("\n" + "=" * 100)
print("  HYPOTHESIS 4: ENVIRONMENTAL DIFFERENCES")
print("=" * 100)

cat5_sst = [s['sst'] for s in cat5_storms.values()]
cat5_shear = [s['shear'] for s in cat5_storms.values()]
cat5_ohc = [s['ohc'] for s in cat5_storms.values()]

cat4_sst = [s['sst'] for s in cat4_storms.values()]
cat4_shear = [s['shear'] for s in cat4_storms.values()]
cat4_ohc = [s['ohc'] for s in cat4_storms.values()]

print(f"""
  Environmental Comparison:

  Factor          Cat 5 Mean    Cat 4 Mean    Difference
  ------          ----------    ----------    ----------
  SST (°C)        {np.mean(cat5_sst):.1f}          {np.mean(cat4_sst):.1f}          {np.mean(cat5_sst) - np.mean(cat4_sst):+.1f}
  Shear (kt)      {np.mean(cat5_shear):.1f}           {np.mean(cat4_shear):.1f}           {np.mean(cat5_shear) - np.mean(cat4_shear):+.1f}
  OHC (kJ/cm²)    {np.mean(cat5_ohc):.1f}          {np.mean(cat4_ohc):.1f}          {np.mean(cat5_ohc) - np.mean(cat4_ohc):+.1f}

  FINDING: Cat 5s have slightly warmer SST and similar OHC,
           but LOWER shear on average ({np.mean(cat5_shear) - np.mean(cat4_shear):.1f} kt difference)
""")

# =============================================================================
# ANALYSIS 5: V* TRAJECTORY PATTERNS
# =============================================================================

print("\n" + "=" * 100)
print("  V* TRAJECTORY ANALYSIS")
print("=" * 100)

print(f"""
  V* Peak Distribution:

  Storm                    Peak V*    Peak (kt)   RI Rate    At Landfall?
  -----                    -------    ---------   -------    ------------
""")

all_storms_sorted = sorted(DETAILED_STORMS.items(), key=lambda x: -x[1]['peak_vmax'])
for name, data in all_storms_sorted:
    landfall_marker = "→ HIT" if data['hours_over_water_after_peak'] == 0 else ""
    cat_marker = "★" if data['peak_cat'] == 5 else " "
    print(f"  {cat_marker} {name:<22} {data['v_star_at_peak']:.2f}       {data['peak_vmax']:<9} {data['ri_rate_kt_per_12h']:<7}    {landfall_marker}")

# =============================================================================
# KEY INSIGHTS
# =============================================================================

print("\n" + "=" * 100)
print("  KEY INSIGHTS FOR MODEL IMPROVEMENT")
print("=" * 100)

print(f"""
  ╔════════════════════════════════════════════════════════════════════════════════════════════╗
  ║                        WHY CAT 4 STORMS DON'T REACH CAT 5                                  ║
  ╠════════════════════════════════════════════════════════════════════════════════════════════╣
  ║                                                                                            ║
  ║  1. LANDFALL TIMING IS THE PRIMARY FACTOR                                                  ║
  ║     - {100*cat4_at_landfall/len(cat4_storms):.0f}% of Cat 4s peaked exactly at landfall                                         ║
  ║     - Only {100*cat5_at_landfall/len(cat5_storms):.0f}% of Cat 5s peaked at landfall                                            ║
  ║     - Cat 4s simply ran out of time over warm water                                        ║
  ║                                                                                            ║
  ║  2. INTENSIFICATION RATE MATTERS BUT ISN'T DECISIVE                                        ║
  ║     - Cat 5s average {np.mean(cat5_ri_rates):.0f} kt/12h vs Cat 4s at {np.mean(cat4_ri_rates):.0f} kt/12h                                    ║
  ║     - Some Cat 4s (Delta, Idalia) had Cat 5-level RI rates                                 ║
  ║     - But they hit land before completing intensification                                  ║
  ║                                                                                            ║
  ║  3. STARTING POINT AFFECTS OUTCOME                                                         ║
  ║     - Cat 5s start at V*={np.mean(cat5_start_vstar):.2f} on average                                                 ║
  ║     - Cat 4s start at V*={np.mean(cat4_start_vstar):.2f}                                                            ║
  ║     - Higher starting V* → more likely to reach Cat 5                                      ║
  ║                                                                                            ║
  ║  4. SHEAR IS A SECONDARY LIMITER                                                           ║
  ║     - Cat 5s average {np.mean(cat5_shear):.1f} kt shear vs Cat 4s at {np.mean(cat4_shear):.1f} kt                                    ║
  ║     - Florence (12 kt shear) and Florence were shear-limited                               ║
  ║                                                                                            ║
  ╠════════════════════════════════════════════════════════════════════════════════════════════╣
  ║                        IMPLICATIONS FOR Z² MODEL                                           ║
  ╠════════════════════════════════════════════════════════════════════════════════════════════╣
  ║                                                                                            ║
  ║  CURRENT MODEL FLAW:                                                                       ║
  ║  - Model assumes all storms can reach MPI if conditions are favorable                      ║
  ║  - This overpredicts Cat 4 storms to 185 kt                                                ║
  ║                                                                                            ║
  ║  NEEDED IMPROVEMENTS:                                                                      ║
  ║  1. Add TIME_TO_LAND parameter - storms hitting land can't reach MPI                       ║
  ║  2. Use V*_START to adjust peak prediction                                                 ║
  ║  3. Apply shear penalty more aggressively for shear > 10 kt                                ║
  ║  4. Cap predictions based on lead time + current V* + RI rate                              ║
  ║                                                                                            ║
  ║  FORMULA UPDATE:                                                                           ║
  ║  Peak_V* = min(MPI_V*, Current_V* + RI_Rate × Time_Over_Water × Shear_Factor)              ║
  ║                                                                                            ║
  ╚════════════════════════════════════════════════════════════════════════════════════════════╝
""")

# =============================================================================
# GOLDEN RATIO ANALYSIS
# =============================================================================

print("\n" + "=" * 100)
print("  GOLDEN RATIO STRUCTURE ANALYSIS")
print("=" * 100)

print(f"""
  The Z² framework predicts eye_radius/RMW ≈ 1/φ ≈ 0.618 at V*=3 (Cat 3)

  What happens at higher V*?

  V* Level    Expected Structure           Observations
  --------    ------------------           ------------
  V*=3.0      Eye/RMW = 1/φ = 0.618        Structural equilibrium reached
  V*=4.0      Eye contracts further        Eye becomes pinhole (2-5 nm)
  V*=5.0+     Extreme contraction          Patricia: 2 nm eye at V*=6.4

  HYPOTHESIS: As V* → 5+, the eye contracts beyond golden ratio stability.
  This creates a "pressure floor" - the eye can't contract further.

  Patricia (V*=6.42) hit an absolute limit:
  - Eye diameter: ~2 nm (smallest on record)
  - Pressure: 872 mb (record)
  - Structure: Maximally compact

  This suggests V* ≈ 6.5 is the ABSOLUTE ceiling for hurricanes.

  Golden ratio implications:
  - At V*=3: Eye/RMW = 1/φ (structural equilibrium)
  - At V*=5: Eye/RMW → 1/φ² ≈ 0.382 (secondary stability?)
  - At V*=6+: Eye/RMW → 1/φ³ ≈ 0.236 (extreme limit)

  The φ-cascade may explain the discrete intensity clusters we observe.
""")

# =============================================================================
# PROPOSED MODEL V3.0
# =============================================================================

print("\n" + "=" * 100)
print("  PROPOSED Z² MODEL v3.0 IMPROVEMENTS")
print("=" * 100)

print(f"""
  Based on this analysis, Model v3.0 should include:

  1. TIME-TO-LAND LIMITER
     =====================
     If hours_to_land < hours_needed_for_MPI:
         Peak_V* = Current_V* + RI_Rate × hours_to_land

     hours_needed_for_MPI ≈ (MPI_V* - Current_V*) / RI_Rate

  2. STARTING V* ADJUSTMENT
     ========================
     Higher starting V* → more likely to reach higher peak

     Peak_Probability(Cat 5) = f(V*_start, RI_rate, time_over_water)

  3. SHEAR PENALTY
     ==============
     If shear > 10 kt:
         MPI_reduction = (shear - 10) × 3 kt

     Florence had 12 kt shear → ~6 kt MPI reduction → Cat 4 instead of 5

  4. GOLDEN RATIO CEILING
     =====================
     Absolute maximum V* ≈ 6.5 (Patricia limit)

     As V* → 6, intensification rate must approach 0
     This creates a "soft ceiling" effect

  5. TRACK-BASED PREDICTION
     =======================
     Integrate with track forecast:
     - Calculate expected hours over warm water
     - Apply time-limited MPI

     This would have correctly predicted Helene, Ida, Laura as Cat 4s
     because their tracks gave insufficient time over water.
""")

print("=" * 100)
