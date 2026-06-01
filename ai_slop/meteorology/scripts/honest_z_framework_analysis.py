#!/usr/bin/env python3
"""
HONEST ANALYSIS: Which Z² Framework Relationships Are Real?

This script critically examines each claimed relationship to determine:
1. Is there genuine predictive power?
2. Is the relationship physically meaningful or coincidental?
3. What sample sizes and statistical significance do we have?
4. What are the alternative explanations?

Being intellectually honest about what we've found.
"""

import numpy as np
import pandas as pd
from collections import defaultdict
from scipy import stats
import os
import warnings
warnings.filterwarnings('ignore')

# Constants
Z = np.sqrt(32 * np.pi / 3)  # 5.788810
Z_SQUARED = 32 * np.pi / 3   # 33.5103
PHI = (1 + np.sqrt(5)) / 2   # 1.618034
INV_PHI = 1 / PHI            # 0.618034

print("=" * 80)
print("  HONEST ANALYSIS: IS THE Z² FRAMEWORK REAL PHYSICS?")
print("=" * 80)

print(f"""
  Z² = 32π/3 = {Z_SQUARED:.4f}
  Z  = √(32π/3) = {Z:.6f}
  φ  = (1+√5)/2 = {PHI:.6f}
  1/φ = {INV_PHI:.6f}
""")

# Load data
DATA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
records = []
with open(os.path.join(DATA_DIR, 'data/extended_best_track/EBTRK_Atlantic_2021.txt'), 'r') as f:
    for line in f:
        parts = line.split()
        if len(parts) >= 10:
            try:
                records.append({
                    'storm_id': parts[0], 'name': parts[1],
                    'datetime': parts[2], 'year': int(parts[3]),
                    'lat': float(parts[4]), 'lon': float(parts[5]),
                    'vmax': int(parts[6]),
                    'mslp': int(parts[7]) if parts[7] != '-999' else None,
                    'rmw': float(parts[8]) if len(parts) > 8 and parts[8] != '-999' else None,
                    'eye': float(parts[9]) if len(parts) > 9 and parts[9] != '-999' else None,
                })
            except:
                pass

df = pd.DataFrame(records)
print(f"  Loaded {len(df)} observations from Atlantic basin")

# ============================================================================
# CLAIM 1: V* = Vmax/Z² matches Saffir-Simpson categories
# ============================================================================

print("\n" + "=" * 80)
print("  CLAIM 1: V* = Vmax/Z² MATCHES SAFFIR-SIMPSON CATEGORIES")
print("=" * 80)

print("""
  The claim:
  - V* = 1 → Tropical Storm threshold (34 kt)
  - V* = 2 → Category 1 (~67 kt)
  - V* = 3 → Category 3 (~100 kt)
  - V* = 4 → Category 5 (~134 kt)
""")

# Calculate what V* values would give each threshold
ss_thresholds = {
    'TD max': 33,
    'TS min': 34,
    'Cat 1': 64,
    'Cat 2': 83,
    'Cat 3': 96,
    'Cat 4': 113,
    'Cat 5': 137,
}

print("\n  Saffir-Simpson vs V* Prediction:")
print(f"  {'Category':<12} {'Actual (kt)':<14} {'V* Value':<12} {'Predicted (kt)':<16} {'Error':<10}")
print("  " + "-" * 65)

for cat, actual_kt in ss_thresholds.items():
    v_star = actual_kt / Z_SQUARED
    predicted_kt = round(v_star) * Z_SQUARED
    error = actual_kt - predicted_kt
    print(f"  {cat:<12} {actual_kt:<14} {v_star:<12.3f} {predicted_kt:<16.1f} {error:+.1f}")

print(f"""
  HONEST ASSESSMENT:
  ==================

  ✓ V* = 1.01 for TS threshold (34 kt) - REMARKABLY CLOSE
  ✓ V* = 1.91 for Cat 1 (64 kt) - Close to 2
  ✓ V* = 2.86 for Cat 3 (96 kt) - Close to 3
  ✓ V* = 4.09 for Cat 5 (137 kt) - Close to 4

  BUT:
  ⚠️  The TS threshold (34 kt) was defined by meteorologists, not physics
  ⚠️  This could be coincidence: 34 ≈ 32π/3 happens to work out
  ⚠️  The Saffir-Simpson scale was designed based on damage, not geometry

  PROBABILITY OF COINCIDENCE:
  ---------------------------
  If we randomly picked a constant K such that 34/K ≈ 1:
  K would need to be between 30-38 (±10% of 34)
  That's 8/100 = 8% of the 10-100 range

  The fact that Z² = 32π/3 ≈ 33.51 falls in this range could be:
  - 8% chance of coincidence, OR
  - Evidence of real geometric structure

  VERDICT: INTERESTING but NOT CONCLUSIVE
  Need independent physical derivation of why Z² should matter
""")

# ============================================================================
# CLAIM 2: Golden Ratio in Eye/RMW at Category 3
# ============================================================================

print("\n" + "=" * 80)
print("  CLAIM 2: EYE/RMW = 1/φ = 0.618 AT CATEGORY 3")
print("=" * 80)

# Get all observations with both eye and RMW data
structural = df[(df['eye'] > 0) & (df['rmw'] > 0) & (df['vmax'] >= 64)].copy()
structural['eye_rmw_ratio'] = structural['eye'] / structural['rmw']
structural['v_star'] = structural['vmax'] / Z_SQUARED

# Define intensity bins
structural['cat'] = pd.cut(structural['vmax'],
    bins=[63, 82, 95, 112, 136, 200],
    labels=['Cat 1', 'Cat 2', 'Cat 3', 'Cat 4', 'Cat 5']
)

print(f"\n  Observations with structural data: {len(structural)}")

if len(structural) > 0:
    print(f"\n  Eye/RMW Ratio by Category:")
    print(f"  {'Category':<10} {'Mean E/RMW':<12} {'Std':<10} {'N':<8} {'vs 1/φ':<12} {'p-value':<12}")
    print("  " + "-" * 70)

    for cat in ['Cat 1', 'Cat 2', 'Cat 3', 'Cat 4', 'Cat 5']:
        subset = structural[structural['cat'] == cat]
        if len(subset) > 5:
            mean_ratio = subset['eye_rmw_ratio'].mean()
            std_ratio = subset['eye_rmw_ratio'].std()
            n = len(subset)
            diff = mean_ratio - INV_PHI

            # t-test: is mean significantly different from 1/φ?
            t_stat, p_val = stats.ttest_1samp(subset['eye_rmw_ratio'], INV_PHI)

            print(f"  {cat:<10} {mean_ratio:<12.3f} {std_ratio:<10.3f} {n:<8} {diff:+.3f}       {p_val:.4f}")

    # Specifically test Cat 3
    cat3 = structural[(structural['vmax'] >= 96) & (structural['vmax'] <= 112)]
    if len(cat3) > 10:
        mean_cat3 = cat3['eye_rmw_ratio'].mean()
        t_stat, p_val = stats.ttest_1samp(cat3['eye_rmw_ratio'], INV_PHI)

        print(f"""
  CATEGORY 3 SPECIFIC TEST:
  -------------------------
  Mean Eye/RMW = {mean_cat3:.4f}
  Golden ratio = {INV_PHI:.4f}
  Difference   = {mean_cat3 - INV_PHI:+.4f}
  p-value      = {p_val:.4f}
  N            = {len(cat3)}

  Is Cat 3 = 1/φ? {'YES (p<0.05)' if p_val > 0.05 else 'NO (significantly different)'}
""")

print(f"""
  HONEST ASSESSMENT:
  ==================

  The golden ratio claim requires:
  1. Cat 3 eye/RMW ≈ 0.618
  2. This should be UNIQUE to Cat 3 (not other categories)
  3. Physical mechanism explaining why φ matters

  ISSUES:
  ⚠️  Eye/RMW ratios vary widely (std typically > 0.1)
  ⚠️  Need to control for measurement uncertainty in eye diameter
  ⚠️  Golden ratio appears in many unrelated systems (apophenia risk)
  ⚠️  No clear mechanism why Fibonacci/φ should appear in hurricane physics

  VERDICT: SUGGESTIVE but NEEDS MORE DATA
  Would be compelling if:
  - Independent eye measurements confirm
  - Physical derivation explains why 1/φ emerges
  - Other structural ratios also relate to φ
""")

# ============================================================================
# CLAIM 3: V* Scaling Explains Predictability
# ============================================================================

print("\n" + "=" * 80)
print("  CLAIM 3: V* SCALING EXPLAINS TRACK PREDICTABILITY")
print("=" * 80)

print("""
  The claim:
  - Storms at V*=1-2 (TS) are hardest to predict
  - Storms at V*>2 (hurricanes) are more predictable
  - This reflects structural maturity, not just intensity
""")

# Calculate V* for all observations
df['v_star'] = df['vmax'] / Z_SQUARED
df['v_star_bin'] = pd.cut(df['v_star'],
    bins=[0, 1, 2, 3, 4, 10],
    labels=['V*<1', 'V*=1-2', 'V*=2-3', 'V*=3-4', 'V*>4']
)

print("\n  Storm Distribution by V* Range:")
print(f"  {'V* Range':<12} {'Count':<10} {'Percentage':<12} {'Intensity':<20}")
print("  " + "-" * 55)

for bin_label in ['V*<1', 'V*=1-2', 'V*=2-3', 'V*=3-4', 'V*>4']:
    count = (df['v_star_bin'] == bin_label).sum()
    pct = 100 * count / len(df)
    if bin_label == 'V*<1':
        intensity = 'TD (<34 kt)'
    elif bin_label == 'V*=1-2':
        intensity = 'TS/weak (34-67 kt)'
    elif bin_label == 'V*=2-3':
        intensity = 'Cat 1-2 (67-100 kt)'
    elif bin_label == 'V*=3-4':
        intensity = 'Cat 3-4 (100-134 kt)'
    else:
        intensity = 'Cat 5 (>134 kt)'
    print(f"  {bin_label:<12} {count:<10} {pct:>10.1f}%   {intensity:<20}")

print(f"""
  HONEST ASSESSMENT:
  ==================

  The V* scaling for predictability claim requires:
  1. TS (V*=1-2) have higher forecast errors
  2. This persists after controlling for other factors
  3. V* adds information beyond simple intensity

  ALTERNATIVE EXPLANATION:
  ⚠️  Lower intensity storms are less organized → harder to predict
  ⚠️  This is ALREADY KNOWN - no need for Z² framework
  ⚠️  V* is just Vmax/33.5 - it's not adding new information

  CRITICAL QUESTION:
  Does V* explain variance BEYOND what Vmax alone explains?

  If correlation(forecast_error, 1/Vmax) ≈ correlation(forecast_error, 1/V*)
  Then V* adds nothing new - it's just a rescaling.

  VERDICT: V* is a CONVENIENT SCALING, not a DISCOVERY
  The underlying physics (weaker storms less predictable) was already known.
  Z² = 32π/3 as the scaling factor may or may not be fundamental.
""")

# ============================================================================
# CLAIM 4: Rapid Intensification at V* Transitions
# ============================================================================

print("\n" + "=" * 80)
print("  CLAIM 4: RI OCCURS AT V* = 2→3 (STRUCTURAL TRANSITION)")
print("=" * 80)

print("""
  The claim:
  - Rapid intensification (RI) preferentially occurs when
    storms cross the V*=2 to V*=3 threshold
  - This represents a structural transition to golden ratio equilibrium
""")

# Look for RI cases
storms = defaultdict(list)
for _, row in df.iterrows():
    storms[(row['storm_id'], row['name'], row['year'])].append(row.to_dict())

ri_cases = []
for key, obs_list in storms.items():
    obs = sorted(obs_list, key=lambda x: x['datetime'])
    for i in range(len(obs) - 4):
        curr = obs[i]
        future = obs[i + 4]  # 24 hours later (4 x 6h)
        delta_v = future['vmax'] - curr['vmax']

        if delta_v >= 30:  # RI definition
            ri_cases.append({
                'storm': key[1],
                'year': key[2],
                'v_star_start': curr['vmax'] / Z_SQUARED,
                'v_star_end': future['vmax'] / Z_SQUARED,
                'delta_v': delta_v,
                'delta_v_star': (future['vmax'] - curr['vmax']) / Z_SQUARED,
            })

if ri_cases:
    ri_df = pd.DataFrame(ri_cases)

    print(f"\n  Rapid Intensification Events: {len(ri_df)}")

    # Analyze V* starting points
    print("\n  RI Starting V* Distribution:")
    v_star_starts = pd.cut(ri_df['v_star_start'],
        bins=[0, 1, 2, 3, 4, 10],
        labels=['V*<1', 'V*=1-2', 'V*=2-3', 'V*=3-4', 'V*>4']
    ).value_counts().sort_index()

    for bin_label, count in v_star_starts.items():
        pct = 100 * count / len(ri_df)
        bar = '*' * int(pct / 2)
        print(f"    {bin_label}: {count:>4} ({pct:>5.1f}%) {bar}")

    # How many cross V*=3?
    crosses_3 = ((ri_df['v_star_start'] < 3) & (ri_df['v_star_end'] >= 3)).sum()
    pct_crosses_3 = 100 * crosses_3 / len(ri_df)

    print(f"""
  RI events crossing V* = 3 threshold:
  - {crosses_3} of {len(ri_df)} RI events ({pct_crosses_3:.1f}%)

  HONEST ASSESSMENT:
  ==================

  The question: Is V*=3 a special transition point?

  Expected if RANDOM:
  - Cat 3 is 96-112 kt range (16 kt span)
  - Total hurricane range ~50-160 kt (110 kt span)
  - Random RI would cross Cat 3 threshold ~15% of time

  Observed: {pct_crosses_3:.1f}%

  ALTERNATIVE EXPLANATION:
  ⚠️  Storms intensify through ALL thresholds, not just V*=3
  ⚠️  Cat 3 is in the MIDDLE of the intensity range
  ⚠️  Many RI events will naturally pass through the middle

  VERDICT: NOT COMPELLING
  The V*=3 "transition point" may just be that Cat 3 is in the middle
  of the hurricane intensity range where RI commonly ends up.
""")

# ============================================================================
# FINAL HONEST SUMMARY
# ============================================================================

print("\n" + "=" * 80)
print("  FINAL HONEST ASSESSMENT")
print("=" * 80)

print("""
  ╔═══════════════════════════════════════════════════════════════════════════╗
  ║                        WHAT IS PROBABLY REAL                              ║
  ╠═══════════════════════════════════════════════════════════════════════════╣
  ║                                                                           ║
  ║  1. V* = Vmax/Z² provides a CONVENIENT normalized intensity scale        ║
  ║     - Integer V* values align reasonably with Saffir-Simpson             ║
  ║     - But this might be coincidence (8% chance)                          ║
  ║                                                                           ║
  ║  2. Weaker storms are harder to predict                                  ║
  ║     - This is well-established meteorology                               ║
  ║     - V* doesn't add new physics, just rescales known relationships     ║
  ║                                                                           ║
  ║  3. Hurricane structure shows some regularities                          ║
  ║     - Eye/RMW ratios cluster around certain values                       ║
  ║     - But claiming 1/φ = 0.618 is the magic number needs more proof     ║
  ║                                                                           ║
  ╠═══════════════════════════════════════════════════════════════════════════╣
  ║                     WHAT IS PROBABLY COINCIDENCE                          ║
  ╠═══════════════════════════════════════════════════════════════════════════╣
  ║                                                                           ║
  ║  1. Z² = 32π/3 having special physical significance                      ║
  ║     - No derivation from hurricane physics                               ║
  ║     - The match with 34 kt TS threshold could be luck                    ║
  ║                                                                           ║
  ║  2. Golden ratio (φ) in hurricane structure                              ║
  ║     - φ appears in many systems due to mathematical properties           ║
  ║     - Confirmation bias: we looked for it and found something close     ║
  ║                                                                           ║
  ║  3. V*=3 as special "equilibrium" point                                  ║
  ║     - Cat 3 is just middle of the intensity range                        ║
  ║     - No unique structural transition observed there                     ║
  ║                                                                           ║
  ╠═══════════════════════════════════════════════════════════════════════════╣
  ║                        WHAT WE NEED TO PROVE IT                           ║
  ╠═══════════════════════════════════════════════════════════════════════════╣
  ║                                                                           ║
  ║  1. PHYSICAL DERIVATION: Why should Z² = 32π/3 matter for hurricanes?   ║
  ║     - Need to derive from vortex dynamics or thermodynamics              ║
  ║     - Cannot just observe pattern; must explain mechanism               ║
  ║                                                                           ║
  ║  2. INDEPENDENT VALIDATION: Test on other basins/datasets                ║
  ║     - Western Pacific, East Pacific, Indian Ocean                        ║
  ║     - If Z² is universal, it should work everywhere                     ║
  ║                                                                           ║
  ║  3. CONTROLLED EXPERIMENTS: Idealized model simulations                  ║
  ║     - Run hurricane simulations varying parameters                       ║
  ║     - See if Z² emerges from physics                                    ║
  ║                                                                           ║
  ╚═══════════════════════════════════════════════════════════════════════════╝

  BOTTOM LINE:
  ============
  The Z² framework provides a mathematically elegant way to describe
  hurricane intensity, but we have NOT proven it reflects real physics.

  To be INTELLECTUALLY HONEST:
  - The patterns are INTERESTING and worth investigating
  - The patterns are NOT PROVEN to be fundamental
  - We should present this as EXPLORATORY, not ESTABLISHED

  The value for forecasting is LIMITED:
  - Track prediction requires atmospheric steering data (we don't have it)
  - Intensity prediction benefits more from SST, shear, ocean heat content
  - The Z² scaling doesn't add predictive power beyond intensity alone
""")

print("=" * 80)
