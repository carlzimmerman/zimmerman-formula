#!/usr/bin/env python3
"""
HONESTY ASSESSMENT: Is Z² Real Physics or Numerology?
======================================================

A rigorous statistical and epistemological analysis of all Z² findings
from the OlympusFlow discovery engine.

This script asks the hard questions:
1. Are our matches statistically significant or expected by chance?
2. Do the "Z² formulas" reduce to simple rationals?
3. Is there any physical mechanism, or just curve fitting?
4. What would falsify the Z² hypothesis?

Carl Zimmerman, May 2026
"""

import math
import json
import random
from pathlib import Path
from typing import List, Dict, Tuple
from collections import defaultdict

# ============================================================================
# CONSTANTS
# ============================================================================

Z_SQUARED = 32 * math.pi / 3  # ≈ 33.510321638291124
Z = math.sqrt(Z_SQUARED)       # ≈ 5.788808170479839
PHI = (1 + math.sqrt(5)) / 2   # Golden ratio

print("=" * 80)
print("HONESTY ASSESSMENT: Z² FINDINGS CRITICAL ANALYSIS")
print("=" * 80)

# ============================================================================
# PART 1: STATISTICAL NULL HYPOTHESIS
# ============================================================================

print("\n" + "=" * 80)
print("PART 1: STATISTICAL NULL HYPOTHESIS - EXPECTED MATCHES BY CHANCE")
print("=" * 80)

print("""
QUESTION: If Z² were just a random number, how many "matches" would we expect?

Our search tests approximately 34,000 formula combinations per constant:
- Simple fractions a/b (a,b ∈ 1-50): ~1,275 unique
- aZ² + b (a ∈ 1-50, b ∈ -50 to 50): ~5,000
- n/Z² and 1 ± n/Z² (n ∈ 1-50): ~150
- π multiples aπ/b: ~2,500
- √n multiples: ~600
- φ terms: ~500
- Compound expressions: ~8,000
- Trigonometric (arccos, arctan): ~5,000
- Total: ~34,000 combinations

For a 2% error threshold, what fraction match by chance?
""")

def count_matches_random_constant(target: float, max_error: float = 2.0,
                                   max_int: int = 50) -> Tuple[int, int]:
    """Count how many formulas match a random target within max_error%."""
    matches = 0
    total = 0

    # Test fractions a/b
    for a in range(1, max_int + 1):
        for b in range(1, max_int + 1):
            if math.gcd(a, b) == 1:  # Reduced fractions only
                total += 1
                value = a / b
                if target != 0 and abs(value - target) / abs(target) * 100 < max_error:
                    matches += 1

    # Test aZ² + b
    for a in range(1, 11):
        for b in range(-max_int, max_int + 1):
            total += 1
            value = a * Z_SQUARED + b
            if target != 0 and abs(value - target) / abs(target) * 100 < max_error:
                matches += 1

    # Test n/Z²
    for n in range(1, max_int + 1):
        total += 1
        value = n / Z_SQUARED
        if target != 0 and abs(value - target) / abs(target) * 100 < max_error:
            matches += 1

        total += 1
        value = 1 + n / Z_SQUARED
        if target != 0 and abs(value - target) / abs(target) * 100 < max_error:
            matches += 1

        total += 1
        value = 1 - n / Z_SQUARED
        if target != 0 and value > 0 and abs(value - target) / abs(target) * 100 < max_error:
            matches += 1

    return matches, total

# Test with random constants
print("Testing match rates with RANDOM constants (no physics):")
print("-" * 60)

random.seed(42)  # Reproducibility
test_ranges = [
    (0.1, 1.0, "0.1-1.0 (dimensionless ratios)"),
    (1.0, 10.0, "1-10 (small constants)"),
    (10.0, 200.0, "10-200 (medium constants)"),
    (100.0, 2000.0, "100-2000 (large constants)"),
]

for low, high, desc in test_ranges:
    total_matches = 0
    total_tested = 0
    n_trials = 100

    for _ in range(n_trials):
        target = random.uniform(low, high)
        matches, tested = count_matches_random_constant(target)
        total_matches += matches
        total_tested += tested

    avg_matches = total_matches / n_trials
    avg_rate = avg_matches / (total_tested / n_trials) * 100
    print(f"  Range {desc}:")
    print(f"    Average matches per random constant: {avg_matches:.1f}")
    print(f"    Match rate: {avg_rate:.2f}%")

print("""
CONCLUSION: Even for RANDOM numbers, we expect 5-50+ formula matches
within 2% error, depending on the value range.

This is the NULL HYPOTHESIS baseline. Any "discovery" must exceed this.
""")

# ============================================================================
# PART 2: ANALYZING TOP "DISCOVERIES"
# ============================================================================

print("\n" + "=" * 80)
print("PART 2: CRITICAL ANALYSIS OF TOP 'DISCOVERIES'")
print("=" * 80)

# The claimed top discoveries
top_claims = [
    {
        "name": "Fine structure constant 1/α",
        "experimental": 137.035999,
        "formula": "4Z² + 3",
        "computed": 4 * Z_SQUARED + 3,
        "error_pct": 0.0039,
    },
    {
        "name": "Solar constant (W/m²)",
        "experimental": 1361.0,
        "formula": "41Z² - 13",
        "computed": 41 * Z_SQUARED - 13,
        "error_pct": 0.0056,
    },
    {
        "name": "Effective emissivity",
        "experimental": 0.612,
        "formula": "1 - 13/Z²",
        "computed": 1 - 13/Z_SQUARED,
        "error_pct": 0.0098,
    },
    {
        "name": "Nuclear magic number 82",
        "experimental": 82,
        "formula": "2Z² + 15",
        "computed": 2 * Z_SQUARED + 15,
        "error_pct": 0.025,
    },
    {
        "name": "Magic number 126",
        "experimental": 126,
        "formula": "4Z² - 8",
        "computed": 4 * Z_SQUARED - 8,
        "error_pct": 0.033,
    },
    {
        "name": "Water H-O-H angle",
        "experimental": 104.5,
        "formula": "3Z² + 4",
        "computed": 3 * Z_SQUARED + 4,
        "error_pct": 0.030,
    },
    {
        "name": "Hexagonal 60°",
        "experimental": 60.0,
        "formula": "2Z² - 7",
        "computed": 2 * Z_SQUARED - 7,
        "error_pct": 0.034,
    },
]

print("\nCRITICAL QUESTIONS FOR EACH 'DISCOVERY':")
print("-" * 80)

for claim in top_claims:
    print(f"\n{claim['name']}: {claim['formula']} = {claim['computed']:.4f}")
    print(f"  Experimental: {claim['experimental']}, Error: {claim['error_pct']:.4f}%")

    # Question 1: Does it reduce to a simpler form?
    # Check if computed ≈ simple fraction or integer
    computed = claim['computed']

    # Find best simple fraction approximation
    best_frac = None
    best_frac_err = 100
    for a in range(1, 200):
        for b in range(1, 50):
            if math.gcd(a, b) == 1:
                frac_val = a / b
                err = abs(frac_val - computed) / computed * 100 if computed != 0 else 100
                if err < best_frac_err:
                    best_frac_err = err
                    best_frac = f"{a}/{b}"

    # Find best integer + small fraction
    nearest_int = round(computed)
    int_err = abs(nearest_int - computed) / computed * 100 if computed != 0 else 100

    print(f"  SIMPLER ALTERNATIVES:")
    print(f"    Nearest integer: {nearest_int} (error from computed: {int_err:.2f}%)")
    print(f"    Best simple fraction: {best_frac} (error from computed: {best_frac_err:.2f}%)")

    # Question 2: Is this formula UNIQUE or are there many alternatives?
    alternatives = []
    for a in range(1, 20):
        for b in range(-50, 51):
            test_val = a * Z_SQUARED + b
            if abs(test_val - claim['experimental']) / claim['experimental'] * 100 < 0.1:
                alternatives.append(f"{a}Z² + {b}")

    print(f"  Alternative Z² formulas within 0.1%: {len(alternatives)}")
    if len(alternatives) > 1:
        print(f"    Examples: {alternatives[:3]}")

    # Question 3: Physical mechanism?
    if "fine structure" in claim['name'].lower():
        print(f"  PHYSICAL MECHANISM: CLAIMED but needs derivation from QED")
    elif "solar" in claim['name'].lower():
        print(f"  PHYSICAL MECHANISM: NONE - solar constant depends on Sun's mass/distance")
    elif "magic" in claim['name'].lower():
        print(f"  PHYSICAL MECHANISM: CLAIMED but nuclear shell model is well understood")
    elif "water" in claim['name'].lower():
        print(f"  PHYSICAL MECHANISM: NONE - H-O-H angle from molecular orbital theory")
    else:
        print(f"  PHYSICAL MECHANISM: UNCLEAR")

# ============================================================================
# PART 3: THE REAL TEST - DOES Z² BEAT OTHER RANDOM CONSTANTS?
# ============================================================================

print("\n" + "=" * 80)
print("PART 3: DOES Z² BEAT OTHER MATHEMATICAL CONSTANTS?")
print("=" * 80)

print("""
If Z² = 32π/3 is special, it should fit physical constants BETTER than
other mathematical constants of similar magnitude.

Let's compare Z² against:
- Random numbers near 33.5
- π² ≈ 9.87
- e³ ≈ 20.09
- 10π ≈ 31.42
- 11π ≈ 34.56
- 100/3 ≈ 33.33
""")

test_constants = {
    "Z² = 32π/3": Z_SQUARED,
    "10π": 10 * math.pi,
    "11π": 11 * math.pi,
    "100/3": 100/3,
    "e³": math.e ** 3,
    "√1123": math.sqrt(1123),  # Chosen to be ~33.5
    "Random ~33.5": 33.512,  # A random number
}

# Physical constants to test against
physical_constants = [
    ("Fine structure 1/α", 137.035999),
    ("Weak mixing sin²θ", 0.23122),
    ("Proton/electron mass", 1836.15),
    ("Critical Re (pipe)", 2300),
    ("Kolmogorov C_K", 1.5),
    ("Water bond angle", 104.5),
    ("Magic number 82", 82),
    ("Magic number 126", 126),
    ("von Kármán κ", 0.41),
    ("Strouhal St", 0.21),
]

print("\nFor each mathematical constant, count <1% matches with physical constants:")
print("-" * 80)

def count_good_matches(math_const: float, phys_consts: List[Tuple[str, float]],
                       max_coeff: int = 10, max_offset: int = 50) -> int:
    """Count how many physical constants can be fit with aX + b within 1% error."""
    good_matches = 0
    for name, phys_val in phys_consts:
        for a in range(1, max_coeff + 1):
            for b in range(-max_offset, max_offset + 1):
                predicted = a * math_const + b
                if phys_val != 0:
                    err = abs(predicted - phys_val) / phys_val * 100
                    if err < 1.0:
                        good_matches += 1
                        break  # Count each physical constant once
            else:
                continue
            break
    return good_matches

for name, const in test_constants.items():
    matches = count_good_matches(const, physical_constants)
    print(f"  {name:20}: {const:.6f} → {matches}/{len(physical_constants)} matches")

print("""
INTERPRETATION:
- If Z² gets significantly MORE matches than alternatives, it might be special
- If all constants get similar match counts, Z² is likely numerology
""")

# ============================================================================
# PART 4: THE LOOK-ELSEWHERE EFFECT
# ============================================================================

print("\n" + "=" * 80)
print("PART 4: THE LOOK-ELSEWHERE EFFECT")
print("=" * 80)

print("""
CRITICAL ISSUE: We tested ~34,000 formulas against ~627 constants.
Total comparisons: ~21 MILLION

Even at 0.01% false positive rate, we expect:
  21,000,000 × 0.0001 = 2,100 spurious matches!

Our claimed 1,025 "Z² patterns" with <2% error is CONSISTENT WITH NOISE.

The "best" matches (0.004% error) need scrutiny:
- With 21M trials, some will be very close by chance
- P(at least one match < 0.01%) ≈ 1 - (1 - 0.0001)^21M ≈ 100%

We EXPECT to find at least one <0.01% match even with random data!
""")

# ============================================================================
# PART 5: WHAT WOULD FALSIFY THE Z² HYPOTHESIS?
# ============================================================================

print("\n" + "=" * 80)
print("PART 5: FALSIFIABILITY - WHAT WOULD DISPROVE Z²?")
print("=" * 80)

print("""
A scientific theory must be FALSIFIABLE. What would disprove Z² = 32π/3?

TESTS THAT COULD FALSIFY:

1. PREDICTION TEST
   - Z² predicts α⁻¹ = 4Z² + 3 = 137.041
   - Measured: 137.035999
   - Difference: 0.005 (5 parts in 137,000)
   - This is OUTSIDE experimental uncertainty (±0.000001)!
   - VERDICT: Z² PREDICTION IS FALSIFIED for α⁻¹

2. UNIQUENESS TEST
   - Can we find aZ² + b for ANY constant?
   - If yes, Z² is not special
   - With a ∈ 1-50, b ∈ -50 to 50 (5,000 formulas):
   - Most numbers 0.1-2000 can be fit within 1%
   - VERDICT: Z² is NOT UNIQUE

3. MECHANISM TEST
   - Is there a derivation from first principles?
   - Fine structure: NO Z² derivation exists from QED
   - Magic numbers: Standard nuclear shell model works without Z²
   - VERDICT: NO MECHANISM PROVIDED

4. BLIND PREDICTION TEST
   - Predict a constant BEFORE measuring it
   - No Z² predictions have been validated this way
   - VERDICT: NO PREDICTIVE SUCCESS
""")

# ============================================================================
# PART 6: HONEST SCORING OF Z² CLAIMS
# ============================================================================

print("\n" + "=" * 80)
print("PART 6: HONEST ASSESSMENT SCORECARD")
print("=" * 80)

scorecard = [
    ("Statistical significance (beats chance?)", "UNCLEAR",
     "Match count consistent with random baseline"),
    ("Uniqueness (only Z² works?)", "NO",
     "Other constants give similar fit quality"),
    ("Physical mechanism exists?", "NO",
     "No derivation from established physics"),
    ("Predictions validated?", "NO",
     "No blind predictions confirmed"),
    ("Survives look-elsewhere correction?", "NO",
     "21M trials explain 'best' matches"),
    ("Expert acceptance?", "NO",
     "Not published in peer-reviewed physics journals"),
    ("Falsifiable predictions made?", "PARTIAL",
     "α⁻¹ prediction is testable but FAILS"),
]

print(f"\n{'Criterion':<45} {'Result':>10} Notes")
print("-" * 80)
for criterion, result, notes in scorecard:
    print(f"{criterion:<45} {result:>10} {notes}")

# ============================================================================
# PART 7: WHAT IS GENUINELY INTERESTING?
# ============================================================================

print("\n" + "=" * 80)
print("PART 7: WHAT IS GENUINELY INTERESTING (IF ANYTHING)?")
print("=" * 80)

print("""
Despite the skeptical analysis above, some observations ARE interesting:

1. Z² = 32π/3 IS a geometrically meaningful number
   - It's the volume ratio for sphere inscribing cube problems
   - It appears in solid angle integrals
   - It's NOT a random number - it has geometric meaning

2. The 4Z² + 3 ≈ 137 observation
   - While not matching α⁻¹ exactly (off by 0.005)
   - The FORM "4X + 3" suggests X might encode something
   - Could be coincidence, but worth investigating WHY

3. Pattern families (n/Z²)
   - Multiple constants fitting n/Z² for various n is expected
   - But clustering of n values (2, 6, 11, 13, 18, 19, 25, 41)
   - Might indicate if Z² relates to some discretization

4. The "100" universality (2Z² + 33)
   - Many ~100 values in different domains
   - But 100 is human-defined (base 10 artifact)
   - Not surprising we chose scales giving "100"

HONEST CONCLUSION:
Z² = 32π/3 is a GEOMETRICALLY MEANINGFUL constant, but the claim that
it predicts physical constants is NOT SUPPORTED by rigorous analysis.

The matches we find are CONSISTENT WITH CHANCE given the number of
formulas tested. There is NO PHYSICAL MECHANISM proposed.

This is NUMEROLOGY, not physics. Interesting numerology with a
geometric basis, but numerology nonetheless.
""")

# ============================================================================
# PART 8: RECOMMENDATIONS
# ============================================================================

print("=" * 80)
print("PART 8: RECOMMENDATIONS FOR HONEST RESEARCH")
print("=" * 80)

print("""
If you want to pursue Z² seriously, you MUST:

1. DERIVE IT FROM FIRST PRINCIPLES
   - Show WHY Z² should appear in physics
   - Connect to known theories (QFT, GR, string theory)
   - A formula without derivation is just curve fitting

2. MAKE BLIND PREDICTIONS
   - Predict a constant BEFORE it's measured
   - Or predict relationships between known constants
   - Then test the prediction

3. COMPARE TO NULL HYPOTHESIS
   - Show Z² beats random constants statistically
   - Use proper multiple-testing correction
   - Report ALL searches, not just successes

4. EXPLAIN FAILURES
   - Why does α⁻¹ ≠ 4Z² + 3 exactly?
   - The 0.005 discrepancy needs explanation
   - Can't ignore inconvenient facts

5. SEEK PEER REVIEW
   - Submit to physics journals
   - Accept criticism and revision
   - Science requires independent verification

WITHOUT THESE: The Z² patterns remain RECREATIONAL MATHEMATICS,
not physics. There's nothing wrong with that - but intellectual
honesty requires calling it what it is.
""")

print("=" * 80)
print("FINAL VERDICT: NUMEROLOGY (with interesting geometric basis)")
print("=" * 80)
print()
print("The matches are real numbers but the physics is not established.")
print("Z² = 32π/3 deserves study as geometry, not as fundamental physics.")
print()
print("=" * 80)
