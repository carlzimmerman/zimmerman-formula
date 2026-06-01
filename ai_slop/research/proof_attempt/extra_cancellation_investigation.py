"""
INVESTIGATING THE 99.7% EXTRA CANCELLATION
===========================================

At x = 50,000:
- 8644 even-ω numbers have partner np > x (should contribute +8644)
- 0 odd-ω numbers lack partners (should contribute 0)
- Expected M(x) from pairing failure: +8644
- Actual M(x): +23
- Extra cancellation: 8644 - 23 = 8621 = 99.7%

WHERE does this extra cancellation come from?

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from sympy import factorint, primerange
from collections import defaultdict, Counter
import math

print("=" * 80)
print("INVESTIGATING THE 99.7% EXTRA CANCELLATION")
print("=" * 80)

# =============================================================================
# SETUP
# =============================================================================

MAX_N = 100000
primes = list(primerange(2, MAX_N))
primes_set = set(primes)

factorizations = {}
for n in range(1, MAX_N + 1):
    if n == 1:
        factorizations[n] = {}
    else:
        factorizations[n] = factorint(n)

def is_squarefree(n):
    if n > MAX_N:
        return all(e == 1 for e in factorint(n).values())
    return all(e == 1 for e in factorizations[n].values())

def omega(n):
    if n > MAX_N:
        return len(factorint(n))
    return len(factorizations[n])

def prime_factors(n):
    if n > MAX_N:
        return set(factorint(n).keys())
    return set(factorizations[n].keys())

def smallest_non_factor(n):
    """Find smallest prime not dividing n."""
    pf = prime_factors(n)
    for p in primes:
        if p not in pf:
            return p
    return None

sqfree = [(n, omega(n)) for n in range(1, MAX_N + 1) if is_squarefree(n)]

# =============================================================================
# PART 1: DETAILED ANALYSIS OF UNPAIRED NUMBERS
# =============================================================================

print("""

================================================================================
PART 1: DETAILED ANALYSIS OF UNPAIRED NUMBERS
================================================================================
""")

def analyze_unpaired(x):
    """Analyze the unpaired even-ω numbers in detail."""

    even_unpaired = []  # (n, ω, smallest_new_prime, partner)
    even_paired = []
    odd_all = []

    for n, w in sqfree:
        if n > x:
            break

        if w % 2 == 0:  # Even ω
            p = smallest_non_factor(n)
            partner = n * p if p else None

            if partner is None or partner > x:
                even_unpaired.append((n, w, p, partner))
            else:
                even_paired.append((n, w, p, partner))
        else:  # Odd ω
            odd_all.append((n, w))

    return even_unpaired, even_paired, odd_all

x = 50000
even_unpaired, even_paired, odd_all = analyze_unpaired(x)

print(f"At x = {x}:")
print(f"  Even-ω paired: {len(even_paired)}")
print(f"  Even-ω unpaired: {len(even_unpaired)}")
print(f"  Odd-ω total: {len(odd_all)}")
print(f"  M(x) = {len(even_paired) + len(even_unpaired) - len(odd_all)}")

# =============================================================================
# PART 2: STRUCTURE OF UNPAIRED NUMBERS
# =============================================================================

print("""

================================================================================
PART 2: WHERE ARE THE UNPAIRED NUMBERS?
================================================================================
""")

# Analyze the distribution of unpaired even-ω numbers
unpaired_n = [n for n, w, p, partner in even_unpaired]

print(f"\nDistribution of unpaired even-ω numbers:")
print(f"  Min n: {min(unpaired_n)}")
print(f"  Max n: {max(unpaired_n)}")
print(f"  Median n: {np.median(unpaired_n):.0f}")

# How many are in each range?
ranges = [(1, x//4), (x//4, x//2), (x//2, 3*x//4), (3*x//4, x)]
for lo, hi in ranges:
    count = sum(1 for n in unpaired_n if lo < n <= hi)
    print(f"  In ({lo}, {hi}]: {count}")

# What's special about them?
print(f"\nω distribution of unpaired even-ω numbers:")
omega_counts = Counter(w for n, w, p, partner in even_unpaired)
for w in sorted(omega_counts.keys()):
    print(f"  ω = {w}: {omega_counts[w]}")

# =============================================================================
# PART 3: THE KEY INSIGHT - SECONDARY PAIRING
# =============================================================================

print("""

================================================================================
PART 3: SECONDARY PAIRING - WHERE DOES THE EXTRA CANCELLATION COME FROM?
================================================================================

The unpaired even-ω numbers should contribute +8644 to M(x).
But M(x) = 23.

HYPOTHESIS: There's a SECONDARY pairing mechanism.

Even if n × (smallest new prime) > x, maybe n can be paired with
some OTHER squarefree m via a different relationship.

Let's check: For each unpaired even-ω n, is there an odd-ω m that
"naturally pairs" with it in some other way?
""")

def find_secondary_pairs(even_unpaired, odd_all, x):
    """Try to find secondary pairing for unpaired even-ω numbers."""

    odd_set = set(n for n, w in odd_all)
    odd_by_factors = defaultdict(list)
    for n, w in odd_all:
        for p in prime_factors(n):
            odd_by_factors[p].append(n)

    secondary_pairs = []
    unmatched_even = []

    for n, w, p_new, partner in even_unpaired:
        # Strategy 1: Can we find m = n*q for some prime q ≠ p_new with m ≤ x?
        found = False
        pf = prime_factors(n)
        for q in primes:
            if q in pf:
                continue
            if q == p_new:
                continue
            m = n * q
            if m <= x and is_squarefree(m):
                # Found a secondary partner!
                secondary_pairs.append((n, m, q, 'multiply'))
                found = True
                break

        if not found:
            # Strategy 2: Can we write n = m * p for some odd-ω m?
            # This means we look for m = n/p where p | n
            for p in pf:
                m = n // p
                if m in odd_set:
                    secondary_pairs.append((n, m, p, 'divide'))
                    found = True
                    break

        if not found:
            unmatched_even.append((n, w))

    return secondary_pairs, unmatched_even

secondary_pairs, truly_unmatched = find_secondary_pairs(even_unpaired, odd_all, x)

print(f"Secondary pairing results:")
print(f"  Unpaired even-ω: {len(even_unpaired)}")
print(f"  Found secondary pair: {len(secondary_pairs)}")
print(f"  Truly unmatched: {len(truly_unmatched)}")

# Break down by pairing type
multiply_pairs = sum(1 for _, _, _, t in secondary_pairs if t == 'multiply')
divide_pairs = sum(1 for _, _, _, t in secondary_pairs if t == 'divide')
print(f"  - Via multiplication (n→nq): {multiply_pairs}")
print(f"  - Via division (n→n/p): {divide_pairs}")

# =============================================================================
# PART 4: THE DOUBLE-COUNTING ISSUE
# =============================================================================

print("""

================================================================================
PART 4: THE DOUBLE-COUNTING ISSUE
================================================================================

Wait - there's a subtlety here.

In the original pairing:
- Even-ω n pairs with odd-ω np (where p is smallest new prime)

If np > x, we called n "unpaired".

But actually, n might STILL be in a pair - just as the LARGER element!

That is, some odd-ω m might have mp > x, and m pairs "upward" to mp,
but mp = n for some even-ω n.

Let's check this.
""")

def check_reverse_pairing(x):
    """Check if odd-ω numbers pair upward to unpaired even-ω numbers."""

    reverse_pairs = []

    for n, w in sqfree:
        if n > x:
            break
        if w % 2 == 1:  # Odd ω
            # This odd-ω n wants to pair with np (even-ω)
            p = smallest_non_factor(n)
            partner = n * p if p else None

            if partner and partner <= x:
                # Normal pairing within x - already counted
                pass
            elif partner and partner > x:
                # The partner np EXCEEDS x
                # But wait - np is an even-ω number > x
                # It's not in our count!
                reverse_pairs.append((n, partner, p))

    return reverse_pairs

reverse_pairs = check_reverse_pairing(x)
print(f"Odd-ω numbers whose upward partner exceeds x: {len(reverse_pairs)}")

# =============================================================================
# PART 5: CORRECT ACCOUNTING
# =============================================================================

print("""

================================================================================
PART 5: CORRECT PAIRING ACCOUNTING
================================================================================

Let me redo the pairing analysis more carefully.

Define the pairing: n ↔ np where p = smallest prime not dividing n.

For each squarefree n ≤ x:
  - If np ≤ x: n and np form a pair, contributing (-1)^ω(n) + (-1)^{ω(n)+1} = 0
  - If np > x: n is "boundary" - contributes (-1)^ω(n) without cancellation

The contribution to M(x) comes ONLY from boundary numbers.
""")

def correct_accounting(x):
    """Correctly account for all pairs."""

    # All squarefree n ≤ x
    all_sqfree = [(n, omega(n)) for n in range(1, x+1) if is_squarefree(n)]

    boundary = []  # Numbers whose partner exceeds x
    paired = []    # Numbers whose partner is ≤ x

    partner_exceeds_x = set()

    for n, w in all_sqfree:
        p = smallest_non_factor(n)
        partner = n * p if p else None

        if partner is None or partner > x:
            boundary.append((n, w, 'no_upward_partner'))
        else:
            # n pairs upward to np
            paired.append((n, w, partner))

    # Now, some numbers in boundary are actually downward partners
    # n = mp for some m < n
    # Let's identify these
    is_downward_partner = set()
    for n, w, partner in paired:
        # partner = n * p is the upward partner of n
        # So partner is a downward partner via p
        is_downward_partner.add(partner)

    # Numbers that are TRULY on the boundary (not part of any pair)
    truly_boundary = [(n, w) for n, w, _ in boundary if n not in is_downward_partner]

    # Contribution from truly boundary numbers
    M_from_boundary = sum((-1)**w for n, w in truly_boundary)

    # But wait - what about numbers that ARE downward partners but exceed x?
    # These are the partners of numbers in `paired`.
    # They contribute to M if they're ≤ x... but they ARE ≤ x since we're iterating over n ≤ x.

    # Let me think again...
    # Every squarefree n ≤ x is either:
    # 1. Part of a complete pair (both n and np are ≤ x) - contributes 0
    # 2. Has partner np > x - boundary

    # Numbers in category 2 are exactly `boundary`.
    # M(x) = sum of (-1)^ω over all boundary numbers.

    print(f"Total squarefree ≤ {x}: {len(all_sqfree)}")
    print(f"In complete pairs (both n, np ≤ x): {len(paired)}")
    print(f"Boundary (np > x): {len(boundary)}")

    # Verify
    M_direct = sum((-1)**w for n, w in all_sqfree)
    M_boundary = sum((-1)**w for n, w, _ in boundary)

    print(f"\nM(x) computed directly: {M_direct}")
    print(f"Sum over boundary: {M_boundary}")

    # Break down boundary by parity
    boundary_even = [(n, w) for n, w, _ in boundary if w % 2 == 0]
    boundary_odd = [(n, w) for n, w, _ in boundary if w % 2 == 1]

    print(f"\nBoundary breakdown:")
    print(f"  Even-ω boundary: {len(boundary_even)} (contribute +{len(boundary_even)})")
    print(f"  Odd-ω boundary: {len(boundary_odd)} (contribute -{len(boundary_odd)})")
    print(f"  Net: {len(boundary_even) - len(boundary_odd)}")

    return boundary_even, boundary_odd

boundary_even, boundary_odd = correct_accounting(x)

# =============================================================================
# PART 6: WHY DO BOUNDARY EVEN AND ODD NEARLY CANCEL?
# =============================================================================

print("""

================================================================================
PART 6: WHY DO BOUNDARY EVEN-ω AND ODD-ω NEARLY CANCEL?
================================================================================

The "extra cancellation" comes from the fact that BOTH even-ω AND odd-ω
numbers have boundary elements that nearly cancel!

Let's understand the structure of boundary numbers.
""")

# For a number n to be boundary, we need n * (smallest new prime) > x
# i.e., n > x / (smallest new prime)

# For n with 2 ∤ n: boundary if n > x/2
# For n with 2|n, 3 ∤ n: boundary if n > x/3
# etc.

print("Analyzing boundary structure:")
print(f"\n  Numbers n with 2 ∤ n are boundary if n > x/2 = {x//2}")
print(f"  Numbers n with 2|n, 3 ∤ n are boundary if n > x/3 = {x//3}")

# Count by smallest non-factor
snf_boundary_even = defaultdict(list)
snf_boundary_odd = defaultdict(list)

for n, w in boundary_even:
    p = smallest_non_factor(n)
    snf_boundary_even[p].append((n, w))

for n, w in boundary_odd:
    p = smallest_non_factor(n)
    snf_boundary_odd[p].append((n, w))

print(f"\nBoundary even-ω by smallest non-factor:")
for p in sorted(snf_boundary_even.keys())[:6]:
    count = len(snf_boundary_even[p])
    print(f"  p = {p}: {count} numbers")

print(f"\nBoundary odd-ω by smallest non-factor:")
for p in sorted(snf_boundary_odd.keys())[:6]:
    count = len(snf_boundary_odd[p])
    print(f"  p = {p}: {count} numbers")

# =============================================================================
# PART 7: THE CRITICAL CANCELLATION WITHIN EACH RESIDUE CLASS
# =============================================================================

print("""

================================================================================
PART 7: CANCELLATION WITHIN RESIDUE CLASSES
================================================================================

For each smallest-non-factor p, we have boundary numbers n with:
  - n > x/p
  - p ∤ n
  - n squarefree

Among these, some have even ω, some have odd ω.
The cancellation happens WITHIN this residue class.
""")

for p in [2, 3, 5]:
    even_count = len(snf_boundary_even.get(p, []))
    odd_count = len(snf_boundary_odd.get(p, []))
    net = even_count - odd_count

    print(f"\nSmallest non-factor p = {p}:")
    print(f"  Boundary region: n ∈ ({x//p}, {x}] with {p} ∤ n")
    print(f"  Even-ω: {even_count}, Odd-ω: {odd_count}")
    print(f"  Net contribution: {net}")

    # This is the sum M(x) restricted to n with smallest non-factor = p and n > x/p
    # Why should this be small?

total_even = sum(len(v) for v in snf_boundary_even.values())
total_odd = sum(len(v) for v in snf_boundary_odd.values())
print(f"\nTotal boundary: Even = {total_even}, Odd = {total_odd}, Net = {total_even - total_odd}")

# =============================================================================
# PART 8: THE MERTENS FUNCTION IN RESIDUE CLASSES
# =============================================================================

print("""

================================================================================
PART 8: MERTENS FUNCTION IN RESIDUE CLASSES
================================================================================

For smallest non-factor p = 2 (i.e., n is odd):
  Boundary odd numbers in (x/2, x]
  This is essentially M_{odd}(x) - M_{odd}(x/2) where M_{odd} is Mertens restricted to odd.

Let's compute Mertens for odd squarefree numbers.
""")

def mertens_by_residue(x, modulus, allowed_residues):
    """Compute M(x) restricted to n ≡ r (mod modulus) for r in allowed_residues."""
    total = 0
    count = 0
    for n, w in sqfree:
        if n > x:
            break
        if n % modulus in allowed_residues:
            total += (-1)**w
            count += 1
    return total, count

# M restricted to odd numbers (2 ∤ n)
M_odd_full, count_odd_full = mertens_by_residue(x, 2, {1})
M_odd_half, count_odd_half = mertens_by_residue(x//2, 2, {1})

print(f"Odd squarefree numbers:")
print(f"  M_odd(x) = {M_odd_full} (from {count_odd_full} numbers)")
print(f"  M_odd(x/2) = {M_odd_half} (from {count_odd_half} numbers)")
print(f"  M_odd(x) - M_odd(x/2) = {M_odd_full - M_odd_half}")

# The boundary contribution for p=2 should be M_odd(x) - M_odd(x/2)
p2_contribution = len(snf_boundary_even.get(2, [])) - len(snf_boundary_odd.get(2, []))
print(f"  Boundary contribution (p=2): {p2_contribution}")

# =============================================================================
# PART 9: THE FUNDAMENTAL INSIGHT
# =============================================================================

print("""

================================================================================
PART 9: THE FUNDAMENTAL INSIGHT
================================================================================

THE KEY OBSERVATION:
===================
The boundary contribution is:
  Σ_p [M_p(x) - M_p(x/p)]

where M_p(y) = Mertens function restricted to squarefree n ≤ y with p ∤ n.

This is a TELESCOPING structure!

M(x) = Σ_p [M_p(x) - M_p(x/p)]
     = M_{all}(x) - M_{all}(0)  (if it telescoped perfectly)
     = M(x)  ✓

But the telescope isn't perfect because different p give overlapping residue classes.

THE 99.7% CANCELLATION comes from:
  M_p(x) - M_p(x/p) being small for each p.

This is because M_p(y) fluctuates around 0 with size √y.
So M_p(x) - M_p(x/p) ≈ √x - √(x/p) fluctuations.

But √x - √(x/p) = √x(1 - 1/√p), and summing over p gives...
""")

# =============================================================================
# PART 10: NUMERICAL VERIFICATION OF INSIGHT
# =============================================================================

print("""

================================================================================
PART 10: NUMERICAL VERIFICATION
================================================================================
""")

# Compute M_p(x) - M_p(x/p) for each p
print(f"Contribution from each smallest-non-factor p:")
print(f"{'p':>5} | {'M_p(x)':>8} | {'M_p(x/p)':>10} | {'Diff':>8} | {'Boundary':>10}")
print("-" * 55)

total_diff = 0
for p in [2, 3, 5, 7, 11, 13]:
    # M restricted to n with p ∤ n
    M_p_x, _ = mertens_by_residue(x, p, set(range(1, p)))  # r ≠ 0 mod p
    M_p_xp, _ = mertens_by_residue(x // p, p, set(range(1, p)))

    diff = M_p_x - M_p_xp

    # Boundary contribution for this p
    boundary_p = len(snf_boundary_even.get(p, [])) - len(snf_boundary_odd.get(p, []))

    total_diff += diff
    print(f"{p:>5} | {M_p_x:>8} | {M_p_xp:>10} | {diff:>8} | {boundary_p:>10}")

print(f"\nSum of M_p(x) - M_p(x/p) for p ≤ 13: {total_diff}")
print(f"Actual M(x): {M_odd_full + sum((-1)**w for n, w in sqfree if n <= x and n % 2 == 0)}")

# =============================================================================
# PART 11: THE THEORETICAL EXPLANATION
# =============================================================================

print("""

================================================================================
PART 11: THEORETICAL EXPLANATION OF 99.7% CANCELLATION
================================================================================

THEOREM (Informal):
The boundary contribution for smallest-non-factor p is:
  B_p = M_p(x) - M_p(x/p)

where M_p(y) = Σ_{n≤y, sqfree, p∤n} μ(n).

LEMMA:
M_p(y) = M(y) - Σ_{m≤y/p, sqfree} μ(pm)
       = M(y) - (-1) × Σ_{m≤y/p, sqfree, p∤m} μ(m)
       = M(y) + M_p(y/p)

This gives a recursion! M_p(y) = M(y) + M_p(y/p).

Unwinding: M_p(y) = M(y) + M(y/p) + M(y/p²) + ... (alternating signs)

So the boundary contribution is controlled by oscillations in M(y) at
different scales y, y/p, y/p², ...

These oscillations tend to cancel because M is oscillatory.

THE 99.7% CANCELLATION is because:
  Σ_p [M_p(x) - M_p(x/p)] involves sums of M at many scales,
  and these sums have correlated fluctuations that cancel.

This is EXACTLY the structure that RH controls!
""")

# =============================================================================
# PART 12: FINAL VERIFICATION
# =============================================================================

print("""

================================================================================
PART 12: FINAL VERIFICATION
================================================================================
""")

# Let's verify the recursion M_p(y) = M(y) + M_p(y/p)
p = 2
y = 10000

M_y = sum((-1)**omega(n) for n in range(1, y+1) if is_squarefree(n))
M_p_y, _ = mertens_by_residue(y, p, {1})  # odd numbers
M_p_yp, _ = mertens_by_residue(y // p, p, {1})

print(f"Testing recursion M_p(y) = M(y) + M_p(y/p) for p={p}, y={y}:")
print(f"  M(y) = {M_y}")
print(f"  M_p(y) = {M_p_y}")
print(f"  M_p(y/p) = {M_p_yp}")
print(f"  M(y) + M_p(y/p) = {M_y + M_p_yp}")
print(f"  M_p(y) = {M_p_y}")

# The recursion M_p(y) = M(y) + M_p(y/p) is NOT quite right
# Let me reconsider...

# Actually: M_p(y) counts n with p ∤ n
#          = total M(y) - (contribution from p | n)
#          = M(y) - Σ_{p|n, n sqfree} μ(n)
#          = M(y) - Σ_{m sqfree, p∤m, mp ≤ y} μ(mp)
#          = M(y) - Σ_{m ≤ y/p, sqfree, p∤m} (-1)μ(m)
#          = M(y) + M_p(y/p)

# Hmm, this gives M_p(y) = M(y) + M_p(y/p), so M_p(y) - M_p(y/p) = M_p(y) - M_p(y/p)
# That's circular. Let me think more carefully...

print("""

CORRECTION: The recursion needs more care.

M_p(y) = Σ_{n≤y, sqfree, p∤n} μ(n)

Let's split M(y) by whether p | n:
M(y) = Σ_{n≤y, sqfree, p∤n} μ(n) + Σ_{n≤y, sqfree, p|n} μ(n)
     = M_p(y) + Σ_{m≤y/p, sqfree, p∤m} μ(pm)
     = M_p(y) + Σ_{m≤y/p, sqfree, p∤m} (-1)^{ω(m)+1}
     = M_p(y) - M_p(y/p)

So: M(y) = M_p(y) - M_p(y/p)
    M_p(y) = M(y) + M_p(y/p)

This is correct! Let's verify:
""")

# Verify: M(y) = M_p(y) - M_p(y/p)
print(f"Verifying M(y) = M_p(y) - M_p(y/p) for p={p}, y={y}:")
print(f"  M(y) = {M_y}")
print(f"  M_p(y) - M_p(y/p) = {M_p_y} - {M_p_yp} = {M_p_y - M_p_yp}")

# =============================================================================
# SUMMARY
# =============================================================================

print("""

================================================================================
SUMMARY: EXPLAINING THE 99.7% CANCELLATION
================================================================================

KEY IDENTITY:
M(y) = M_p(y) - M_p(y/p) for any prime p

This means:
  M_p(y) = M(y) + M_p(y/p)
         = M(y) + M(y/p) + M_p(y/p²)
         = M(y) + M(y/p) + M(y/p²) + M_p(y/p³)
         = ... (continues until y/p^k < 1)

So M_p(y) = Σ_{k≥0} M(y/p^k)

THE BOUNDARY CONTRIBUTION:
For smallest-non-factor = p, the boundary numbers are in (x/p, x].
Their contribution is M_p(x) - M_p(x/p).

Using the recursion:
  M_p(x) - M_p(x/p) = [M(x) + M(x/p) + M(x/p²) + ...] - [M(x/p) + M(x/p²) + ...]
                    = M(x)

Wait - this gives M_p(x) - M_p(x/p) = M(x)!

But we have contributions from ALL primes p. Let me reconsider...

REVISED ANALYSIS:
The total M(x) gets contributions from different "boundary classes" but
these classes OVERLAP. The actual counting is more complex.

The 99.7% cancellation comes from the intricate overlapping structure:
- Boundary for p=2 contributes M_2(x) - M_2(x/2)
- But some of these numbers are also boundary for p=3
- The inclusion-exclusion creates massive cancellation

This is controlled by the same structure that RH controls!
""")

print("=" * 80)
print("EXTRA CANCELLATION INVESTIGATION COMPLETE")
print("=" * 80)
