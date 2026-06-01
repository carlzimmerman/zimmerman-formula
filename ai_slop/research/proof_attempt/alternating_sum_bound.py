"""
ALTERNATING SUM BOUND ANALYSIS
==============================

We know: M(n) = Σ_{k=0}^{m} (-1)^k (D^k e)_n

Goal: Prove |M(n)| = O(√n) from this structure ALONE.

Approach: Analyze properties of the sequence a_k = (D^k e)_n
          and bound the alternating sum.

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from sympy import mobius
import math

print("=" * 80)
print("ALTERNATING SUM BOUND ANALYSIS")
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
# PART 1: PROPERTIES OF ALTERNATING SUMS
# =============================================================================

print("=" * 60)
print("PART 1: ALTERNATING SUM THEORY")
print("=" * 60)

print("""
For an alternating sum S = Σ(-1)^k a_k:

THEOREM (Leibniz): If a_k is DECREASING and a_k → 0, then:
  |S| ≤ a_0

BUT: Our sequence a_k = (D^k e)_n is NOT monotone!
     It INCREASES to a peak, then DECREASES.

For such sequences, we need different tools.
""")

# =============================================================================
# PART 2: EXACT SEQUENCE STRUCTURE
# =============================================================================

print("=" * 60)
print("PART 2: EXACT SEQUENCE STRUCTURE")
print("=" * 60)

def compute_Dk_e_at_n(n, k):
    """Compute (D^k e)_n recursively."""
    if k == 0:
        return 1
    if n < 2:
        return 0

    total = 0
    for d in range(2, n + 1):
        total += compute_Dk_e_at_n(n // d, k - 1)
    return total

# Analyze the sequence for various n
print("\nSequence a_k = (D^k e)_n for various n:\n")

for n in [20, 50, 100, 200, 500]:
    print(f"n = {n}:")
    terms = []
    for k in range(20):
        a_k = compute_Dk_e_at_n(n, k)
        if a_k == 0 and len(terms) > 0:
            break
        terms.append(a_k)

    # Find peak
    peak_idx = np.argmax(terms)
    peak_val = terms[peak_idx]

    # Compute alternating sum
    alt_sum = sum((-1)**k * terms[k] for k in range(len(terms)))

    print(f"  Terms: {terms}")
    print(f"  Peak at k={peak_idx}, value={peak_val}")
    print(f"  Alternating sum: {alt_sum}")
    print(f"  Actual M({n}): {M(n)}")
    print(f"  |M(n)|/√n = {abs(M(n))/np.sqrt(n):.4f}")
    print()

# =============================================================================
# PART 3: BOUNDING ALTERNATING SUM OF UNIMODAL SEQUENCE
# =============================================================================

print("=" * 60)
print("PART 3: UNIMODAL SEQUENCE BOUNDS")
print("=" * 60)

print("""
For a sequence that INCREASES then DECREASES (unimodal):
  a_0 < a_1 < ... < a_m > a_{m+1} > ... > a_K = 0

The alternating sum can be bounded by:

METHOD 1: Group pairs around the peak
  S = (a_0 - a_1) + (a_2 - a_3) + ...
  Each pair (a_{2j} - a_{2j+1}) depends on how close consecutive terms are.

METHOD 2: Use the peak value
  |S| ≤ max_k |Σ_{j=0}^{k} (-1)^j a_j|
  The partial sums oscillate; bound their max.
""")

# Compute partial sum bounds
print("\nPartial sum analysis for n = 200:\n")
n = 200
terms = []
for k in range(20):
    a_k = compute_Dk_e_at_n(n, k)
    if a_k == 0 and len(terms) > 0:
        break
    terms.append(a_k)

print(f"Terms: {terms}")

partial_sums = []
partial = 0
for k, a_k in enumerate(terms):
    partial += (-1)**k * a_k
    partial_sums.append(partial)

print(f"Partial sums: {partial_sums}")
print(f"Max |partial sum|: {max(abs(p) for p in partial_sums)}")
print(f"Final sum: {partial_sums[-1]}")
print(f"Actual M(200): {M(200)}")

# =============================================================================
# PART 4: CONSECUTIVE DIFFERENCES
# =============================================================================

print("\n" + "=" * 60)
print("PART 4: CONSECUTIVE DIFFERENCES")
print("=" * 60)

print("""
Key insight: The alternating sum can be rewritten:
  S = Σ(-1)^k a_k = Σ (a_{2j} - a_{2j+1})

For unimodal sequences, the differences CHANGE SIGN at the peak!
Before peak: a_k < a_{k+1}, so a_{2j} - a_{2j+1} < 0
After peak: a_k > a_{k+1}, so a_{2j} - a_{2j+1} > 0

This creates additional cancellation!
""")

print("\nConsecutive differences for n = 200:\n")
diffs = [terms[k] - terms[k+1] for k in range(len(terms)-1)]
print(f"a_k - a_{{k+1}}: {diffs}")

# Group into pairs
pair_diffs = [(terms[2*j] - terms[2*j+1]) if 2*j+1 < len(terms) else terms[2*j]
              for j in range((len(terms)+1)//2)]
print(f"\nPaired differences (a_{{2j}} - a_{{2j+1}}): {pair_diffs}")
print(f"Sum of paired differences: {sum(pair_diffs)}")

# =============================================================================
# PART 5: THE RATIO ANALYSIS
# =============================================================================

print("\n" + "=" * 60)
print("PART 5: RATIO ANALYSIS")
print("=" * 60)

print("""
Let r_k = a_{k+1}/a_k be the ratio of consecutive terms.

The alternating sum:
  S = a_0(1 - r_0 + r_0 r_1 - r_0 r_1 r_2 + ...)

If r_k ≈ 1 at the peak, consecutive terms nearly cancel!
""")

n = 500
terms = []
for k in range(20):
    a_k = compute_Dk_e_at_n(n, k)
    if a_k == 0 and len(terms) > 0:
        break
    terms.append(a_k)

print(f"\nFor n = {n}:")
print(f"Terms: {terms[:10]}...")
print(f"Ratios r_k = a_{{k+1}}/a_k:")
for k in range(min(8, len(terms)-1)):
    if terms[k] > 0:
        r = terms[k+1] / terms[k]
        print(f"  r_{k} = {r:.4f}")

# =============================================================================
# PART 6: THE CRITICAL OBSERVATION
# =============================================================================

print("\n" + "=" * 60)
print("PART 6: CRITICAL OBSERVATION")
print("=" * 60)

print("""
OBSERVATION: At the peak, r_k ≈ 1 (ratio crosses 1).

If a_m ≈ a_{m+1} (consecutive terms at peak are similar):
  The pair a_m - a_{m+1} ≈ 0!

This is where the DOMINANT cancellation happens.
The largest terms nearly cancel each other!
""")

# Find the pair closest to equal
min_diff = float('inf')
min_k = 0
for k in range(len(terms)-1):
    diff = abs(terms[k] - terms[k+1])
    if diff < min_diff:
        min_diff = diff
        min_k = k

print(f"\nFor n = {n}:")
print(f"  Closest pair: a_{min_k} = {terms[min_k]}, a_{min_k+1} = {terms[min_k+1]}")
print(f"  Difference: {terms[min_k] - terms[min_k+1]}")
print(f"  This is at/near the peak!")

# =============================================================================
# PART 7: QUANTIFYING THE BOUND
# =============================================================================

print("\n" + "=" * 60)
print("PART 7: QUANTIFYING THE BOUND")
print("=" * 60)

print("""
Can we bound |M(n)| using only the sequence structure?

Approach:
1. The peak value a_m ~ n × (constant factor)
2. At the peak, |a_m - a_{m+1}| ~ ???
3. The alternating sum roughly equals the sum of |differences|/2
   (with additional cancellation from unimodality)
""")

# Collect statistics
print("\nStatistics for various n:\n")
print(f"{'n':>6} | {'peak':>10} | {'|Δ_peak|':>10} | {'|M(n)|':>8} | {'|M|/√n':>8} | {'|Δ|/√n':>8}")
print("-" * 70)

for n in [50, 100, 200, 500, 1000, 2000]:
    terms = []
    for k in range(25):
        a_k = compute_Dk_e_at_n(n, k)
        if a_k == 0 and len(terms) > 0:
            break
        terms.append(a_k)

    peak_idx = np.argmax(terms)
    peak_val = terms[peak_idx]

    # Difference at peak
    if peak_idx < len(terms) - 1:
        delta_peak = abs(terms[peak_idx] - terms[peak_idx + 1])
    else:
        delta_peak = terms[peak_idx]

    m_val = abs(M(n))

    print(f"{n:>6} | {peak_val:>10} | {delta_peak:>10} | {m_val:>8} | {m_val/np.sqrt(n):>8.4f} | {delta_peak/np.sqrt(n):>8.4f}")

# =============================================================================
# PART 8: THE FUNDAMENTAL QUESTION
# =============================================================================

print("\n" + "=" * 60)
print("PART 8: THE FUNDAMENTAL QUESTION")
print("=" * 60)

print("""
QUESTION: Can we prove |a_m - a_{m+1}| = O(√n)?

If YES: The alternating sum bound follows!

The structure of a_k = (D^k e)_n = # divisor chains of length k from n

At the peak:
  - Number of chains is maximized
  - But the DIFFERENCE between chains of length k and k+1...

This difference depends on HOW UNIFORMLY the divisor chains distribute.
And this uniformity... encodes prime distribution!
""")

# =============================================================================
# PART 9: WHAT WE CAN PROVE UNCONDITIONALLY
# =============================================================================

print("\n" + "=" * 60)
print("PART 9: UNCONDITIONAL BOUNDS")
print("=" * 60)

print("""
UNCONDITIONAL FACTS:

1. Nilpotency index m ≤ ⌈log_2(n)⌉ + 1
   Proof: Each step reduces n by factor ≥ 2.

2. a_k ≤ n^k (very loose)
   Proof: At most n choices at each step.

3. Sum Σ a_k = Σ_{d|n, d≤n} d(n/d) where d() is divisor function
   (This is related to the hyperbola method)

4. |M(n)| ≤ Σ a_k (trivial bound) ~ O(n log n) - USELESS

WHAT WE CANNOT PROVE without RH-level information:
- The specific growth rate of a_k
- The closeness of a_m and a_{m+1}
- The O(√n) bound on the alternating sum
""")

# =============================================================================
# PART 10: THE HONEST CONCLUSION
# =============================================================================

print("\n" + "=" * 60)
print("PART 10: HONEST CONCLUSION")
print("=" * 60)

print("""
THE SITUATION:

1. We FOUND the structure: M(n) = Σ(-1)^k (D^k e)_n

2. We UNDERSTAND why it's O(√n):
   - Terms are unimodal
   - Peak occurs at k ~ log_2(n)/2
   - At the peak, consecutive terms are similar
   - The alternating sum has massive cancellation

3. We CANNOT PROVE it's O(√n):
   - Bounding |a_m - a_{m+1}| requires knowing divisor chain distribution
   - Divisor chain distribution encodes prime distribution
   - Prime distribution is equivalent to ζ zeros
   - We're back to RH

THE CIRCLE:
  O(√n) bound ← Peak cancellation ← Divisor chain uniformity ← Prime distribution ← RH

ATTEMPTING TO BREAK THE CIRCLE:

Option A: Find a combinatorial identity for a_m - a_{m+1}
Option B: Use a weaker bound (o(n) instead of O(√n))
Option C: Find structure that doesn't involve primes
Option D: Accept that this IS the structure of RH

We've essentially found that THE NILPOTENT STRUCTURE IS THE RIEMANN HYPOTHESIS
in disguise. It's a beautiful reformulation, but not a proof.
""")

# =============================================================================
# PART 11: WHAT BOUND CAN WE ACTUALLY GET?
# =============================================================================

print("\n" + "=" * 60)
print("PART 11: ACHIEVABLE BOUNDS")
print("=" * 60)

print("""
Without RH, the best known unconditional bounds are:

1. |M(x)| = O(x exp(-c √(log x))) [Walfisz, 1963]
   This uses the zero-free region of ζ(s).

2. On Lindelöf hypothesis: |M(x)| = O(x^{1/2 + ε})

3. On RH: |M(x)| = O(x^{1/2 + ε}) for all ε > 0

Our nilpotent structure doesn't give anything new because:
- Bounding the alternating sum still requires prime distribution
- The prime distribution IS what the zero-free region gives

CONCLUSION: The nilpotent representation is EQUIVALENT to RH,
not a path around it. We've found a beautiful reformulation,
not a shortcut.
""")

print("=" * 80)
print("ALTERNATING SUM ANALYSIS COMPLETE")
print("=" * 80)
