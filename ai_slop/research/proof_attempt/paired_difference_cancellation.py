"""
PAIRED DIFFERENCE CANCELLATION ANALYSIS
========================================

Key finding: The peak difference |a_m - a_{m+1}| grows like O(n),
but |M(n)| = O(√n). So the PAIRED DIFFERENCES must cancel!

M(n) = Σ (a_{2j} - a_{2j+1})

The individual differences are O(n), but their SUM is O(√n).
This is where the second level of cancellation happens.

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from sympy import mobius
import math

print("=" * 80)
print("PAIRED DIFFERENCE CANCELLATION")
print("=" * 80)

# Setup
MAX_N = 5000
M_array = [0] * (MAX_N + 1)
mu_array = [0] * (MAX_N + 1)
cumsum = 0
for n in range(1, MAX_N + 1):
    mu_array[n] = int(mobius(n))
    cumsum += mu_array[n]
    M_array[n] = cumsum

def M(x):
    return M_array[int(x)] if 1 <= int(x) <= MAX_N else 0

print("Setup complete.\n")

# =============================================================================
# PART 1: THE TWO-LEVEL CANCELLATION
# =============================================================================

print("=" * 60)
print("PART 1: TWO-LEVEL CANCELLATION STRUCTURE")
print("=" * 60)

print("""
LEVEL 1: Alternating sum cancels terms
  M(n) = a_0 - a_1 + a_2 - a_3 + ...

LEVEL 2: Regroup as paired differences
  M(n) = (a_0 - a_1) + (a_2 - a_3) + ...
       = d_0 + d_1 + d_2 + ...
  where d_j = a_{2j} - a_{2j+1}

The d_j are O(n) individually but sum to O(√n)!
This is a SECOND LEVEL of cancellation.
""")

def compute_Dk_e_at_n(n, k):
    """Compute (D^k e)_n recursively with memoization."""
    memo = {}
    def helper(n, k):
        if (n, k) in memo:
            return memo[(n, k)]
        if k == 0:
            return 1
        if n < 2:
            return 0
        total = 0
        for d in range(2, n + 1):
            total += helper(n // d, k - 1)
        memo[(n, k)] = total
        return total
    return helper(n, k)

# Analyze paired differences
print("\nPaired difference structure:\n")

for n in [100, 200, 500, 1000]:
    # Get terms
    terms = []
    for k in range(25):
        a_k = compute_Dk_e_at_n(n, k)
        if a_k == 0 and len(terms) > 0:
            break
        terms.append(a_k)

    # Compute paired differences
    d = []
    for j in range((len(terms) + 1) // 2):
        if 2*j + 1 < len(terms):
            d.append(terms[2*j] - terms[2*j+1])
        else:
            d.append(terms[2*j])

    total_d = sum(d)
    sum_abs_d = sum(abs(x) for x in d)

    print(f"n = {n}:")
    print(f"  Paired diffs d_j: {d}")
    print(f"  Sum(d_j) = {total_d} = M({n})")
    print(f"  Σ|d_j| = {sum_abs_d}")
    print(f"  Cancellation: {100 * (1 - abs(total_d)/sum_abs_d):.1f}%")
    print()

# =============================================================================
# PART 2: SIGNS OF PAIRED DIFFERENCES
# =============================================================================

print("=" * 60)
print("PART 2: SIGN PATTERN OF d_j")
print("=" * 60)

print("""
The paired differences d_j = a_{2j} - a_{2j+1} have a SIGN PATTERN:

Before peak (increasing part): d_j < 0 (because a_{2j} < a_{2j+1})
After peak (decreasing part): d_j > 0 (because a_{2j} > a_{2j+1})

This creates another level of cancellation!
""")

for n in [200, 500, 1000]:
    terms = []
    for k in range(25):
        a_k = compute_Dk_e_at_n(n, k)
        if a_k == 0 and len(terms) > 0:
            break
        terms.append(a_k)

    peak_idx = np.argmax(terms)

    # Paired differences with sign analysis
    print(f"\nn = {n} (peak at k = {peak_idx}):")
    d_neg = 0
    d_pos = 0
    for j in range((len(terms) + 1) // 2):
        if 2*j + 1 < len(terms):
            d_j = terms[2*j] - terms[2*j+1]
            if d_j < 0:
                d_neg += d_j
            else:
                d_pos += d_j
            sign = "−" if d_j < 0 else "+"
            print(f"  d_{j} = a_{2*j} - a_{2*j+1} = {terms[2*j]} - {terms[2*j+1]} = {d_j} ({sign})")

    print(f"  Negative sum: {d_neg}")
    print(f"  Positive sum: {d_pos}")
    print(f"  Total: {d_neg + d_pos}")

# =============================================================================
# PART 3: THE BALANCE EQUATION
# =============================================================================

print("\n" + "=" * 60)
print("PART 3: THE BALANCE EQUATION")
print("=" * 60)

print("""
Define:
  D⁻ = Σ_{d_j < 0} d_j  (sum of negative paired diffs)
  D⁺ = Σ_{d_j > 0} d_j  (sum of positive paired diffs)

Then: M(n) = D⁺ + D⁻

The O(√n) behavior requires: |D⁺ + D⁻| = O(√n)

This means: D⁺ ≈ -D⁻ (they nearly cancel!)

Let's quantify this cancellation.
""")

print(f"\n{'n':>6} | {'D⁻':>12} | {'D⁺':>12} | {'D⁺+D⁻':>10} | {'|D⁺-D⁻|':>10} | {'ratio':>8}")
print("-" * 75)

for n in [50, 100, 200, 500, 1000, 2000]:
    terms = []
    for k in range(25):
        a_k = compute_Dk_e_at_n(n, k)
        if a_k == 0 and len(terms) > 0:
            break
        terms.append(a_k)

    d_neg = 0
    d_pos = 0
    for j in range((len(terms) + 1) // 2):
        if 2*j + 1 < len(terms):
            d_j = terms[2*j] - terms[2*j+1]
        else:
            d_j = terms[2*j]
        if d_j < 0:
            d_neg += d_j
        else:
            d_pos += d_j

    total = d_neg + d_pos
    diff = abs(d_pos - abs(d_neg))
    if abs(d_neg) > 0:
        ratio = d_pos / abs(d_neg)
    else:
        ratio = float('inf')

    print(f"{n:>6} | {d_neg:>12} | {d_pos:>12} | {total:>10} | {diff:>10} | {ratio:>8.4f}")

# =============================================================================
# PART 4: WHY DO THEY BALANCE?
# =============================================================================

print("\n" + "=" * 60)
print("PART 4: WHY DO D⁺ AND D⁻ BALANCE?")
print("=" * 60)

print("""
The balance D⁺ ≈ -D⁻ is equivalent to M(n) being small!

This is NOT something we can prove independently:
  D⁺ + D⁻ = M(n) = O(√n)   ← THIS IS WHAT RH CLAIMS!

We're looking at the same phenomenon from a different angle.

The balance EXPLAINS the O(√n) behavior:
- Before the peak: differences are negative
- After the peak: differences are positive
- These nearly cancel

But PROVING the balance is exactly what RH asks!
""")

# =============================================================================
# PART 5: THE STRUCTURE AROUND THE PEAK
# =============================================================================

print("\n" + "=" * 60)
print("PART 5: STRUCTURE AROUND THE PEAK")
print("=" * 60)

print("""
Let's look more closely at what happens at the peak.

The peak is where the ratio r_k = a_{k+1}/a_k crosses 1.
At this point, consecutive terms are most similar.

If the peak happens at an EVEN index 2m:
  d_m = a_{2m} - a_{2m+1} ≈ 0 (both near peak)

If the peak happens at an ODD index 2m+1:
  d_m = a_{2m} - a_{2m+1} is large negative
  d_{m+1} = a_{2m+2} - a_{2m+3} is large positive
  These need to balance!
""")

for n in [200, 500, 1000]:
    terms = []
    for k in range(25):
        a_k = compute_Dk_e_at_n(n, k)
        if a_k == 0 and len(terms) > 0:
            break
        terms.append(a_k)

    peak_idx = np.argmax(terms)

    print(f"\nn = {n}: peak at k = {peak_idx} ({'even' if peak_idx % 2 == 0 else 'odd'})")
    print(f"  a_{peak_idx} = {terms[peak_idx]}")
    if peak_idx > 0:
        print(f"  a_{peak_idx-1} = {terms[peak_idx-1]}")
    if peak_idx < len(terms) - 1:
        print(f"  a_{peak_idx+1} = {terms[peak_idx+1]}")

# =============================================================================
# PART 6: THE TELESCOPING PERSPECTIVE
# =============================================================================

print("\n" + "=" * 60)
print("PART 6: TELESCOPING PERSPECTIVE")
print("=" * 60)

print("""
Alternative view: Think of M(n) as a telescoping sum.

M(n) = Σ_{k=0}^{K} (-1)^k a_k
     = a_0 - (a_1 - a_2) - (a_3 - a_4) - ...   if K odd
     = a_0 - (a_1 - a_2) - ... + a_K            if K even

Each bracket (a_{2j+1} - a_{2j+2}) is POSITIVE (decreasing after peak)
or NEGATIVE (increasing before peak).

The sum of brackets needs to nearly equal a_0 = 1!
This is a very strong constraint.
""")

n = 500
terms = []
for k in range(25):
    a_k = compute_Dk_e_at_n(n, k)
    if a_k == 0 and len(terms) > 0:
        break
    terms.append(a_k)

print(f"\nFor n = {n}:")
print(f"  a_0 = 1")

bracket_sum = 0
for j in range((len(terms) - 1) // 2):
    bracket = terms[2*j+1] - terms[2*j+2]
    bracket_sum += bracket
    print(f"  (a_{2*j+1} - a_{2*j+2}) = {terms[2*j+1]} - {terms[2*j+2]} = {bracket}")

print(f"  Sum of brackets = {bracket_sum}")
print(f"  a_0 - Sum = 1 - {bracket_sum} = {1 - bracket_sum}")
print(f"  M({n}) = {M(n)}")

# =============================================================================
# PART 7: THE FUNDAMENTAL IDENTITY
# =============================================================================

print("\n" + "=" * 60)
print("PART 7: SEARCHING FOR A FUNDAMENTAL IDENTITY")
print("=" * 60)

print("""
Is there an IDENTITY that forces the cancellation?

We know: [Σ_{d≤n} M(n/d)]² = 1 (exact!)

This is equivalent to: (I+D) M = e

Does this imply bounds on the paired differences?
Let's check if there's structure in the d_j values.
""")

# Look for patterns in d_j
print("\nRatios of consecutive d_j (when both nonzero):\n")

for n in [200, 500]:
    terms = []
    for k in range(25):
        a_k = compute_Dk_e_at_n(n, k)
        if a_k == 0 and len(terms) > 0:
            break
        terms.append(a_k)

    d = []
    for j in range((len(terms) + 1) // 2):
        if 2*j + 1 < len(terms):
            d.append(terms[2*j] - terms[2*j+1])
        else:
            d.append(terms[2*j])

    print(f"n = {n}: d = {d}")
    print("  Ratios d_{j+1}/d_j:", end=" ")
    for j in range(len(d) - 1):
        if d[j] != 0:
            r = d[j+1] / d[j]
            print(f"{r:.3f}", end=" ")
    print()

# =============================================================================
# PART 8: HONEST ASSESSMENT
# =============================================================================

print("\n" + "=" * 60)
print("PART 8: HONEST ASSESSMENT")
print("=" * 60)

print("""
WHAT WE'VE FOUND:

1. TWO-LEVEL CANCELLATION:
   - Level 1: Alternating sum of terms a_k
   - Level 2: Paired differences d_j also cancel (D⁺ ≈ -D⁻)

2. THE BALANCE D⁺ ≈ -D⁻:
   - Differences before peak are negative
   - Differences after peak are positive
   - These nearly cancel to give O(√n)

3. THE CIRCULARITY:
   - D⁺ + D⁻ = M(n)
   - So |D⁺ + D⁻| = O(√n) IS the Mertens bound
   - We're not proving anything new

WHY WE CAN'T BREAK THE CIRCLE:

The balance D⁺ ≈ -D⁻ depends on:
- How terms grow BEFORE the peak
- How terms shrink AFTER the peak
- The rate of growth/shrinkage depends on divisor chains
- Divisor chain behavior encodes prime distribution
- Prime distribution is controlled by ζ zeros

THE NILPOTENT STRUCTURE DOESN'T AVOID THE PRIME DISTRIBUTION:
It just REPACKAGES it in a different form.

The structure M = Σ(-D)^k e is EQUIVALENT to saying:
"The Mertens function is controlled by how evenly divisor chains distribute"
And that evenness IS the Riemann Hypothesis.
""")

# =============================================================================
# FINAL SUMMARY
# =============================================================================

print("\n" + "=" * 60)
print("FINAL SUMMARY")
print("=" * 60)

print("""
THE INVESTIGATION RESULT:

1. ✓ We found beautiful structure: M(n) = Σ(-D)^k e
2. ✓ We explained the cancellation: D⁺ ≈ -D⁻
3. ✓ We identified the gap: balancing D⁺ and D⁻ IS the RH
4. ✗ We cannot prove RH from this structure alone

THE FUNDAMENTAL REASON:

The divisor chains that make up (D^k e)_n encode exactly the
same information as the distribution of primes. There is no
way to prove bounds on them without either:
  (a) Assuming something equivalent to RH, or
  (b) Finding an entirely new approach

WHAT WE ACHIEVED:

A REFORMULATION of RH in terms of nilpotent operators:
  RH ⟺ The alternating nilpotent series Σ(-D)^k e = O(√N)
  RH ⟺ D⁺ + D⁻ = O(√N) where D±= positive/negative paired diffs

This is a legitimate mathematical contribution:
- New perspective on the Mertens function
- Connection to operator theory
- Quantitative understanding of cancellation

But it is NOT a proof of RH.
""")

print("=" * 80)
print("PAIRED DIFFERENCE ANALYSIS COMPLETE")
print("=" * 80)
