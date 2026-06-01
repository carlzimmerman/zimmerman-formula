#!/usr/bin/env python3
"""
RH_DETECTION_FILTER_2_S_FUNCTION.py

THE S(t) ARGUMENT JUMP AND TURING BOUNDS

We analyze how an off-line zero quadruplet affects the argument function S(t)
and whether it violates proven bounds used in Turing's verification method.

S(t) = (1/π) arg ζ(1/2 + it)

This function tracks the "winding" of ζ and is used to count zeros.
"""

import numpy as np
from scipy import special
from typing import Tuple, Dict
import math

print("=" * 80)
print("DETECTION FILTER 2: THE S(t) ARGUMENT FUNCTION")
print("=" * 80)
print()

# =============================================================================
# PART 1: THE S(t) FUNCTION DEFINITION
# =============================================================================

print("PART 1: THE ARGUMENT FUNCTION S(t)")
print("-" * 60)
print()

print("""
DEFINITION: The argument function S(t) is defined as:

    S(t) = (1/π) arg ζ(1/2 + it)
         = (1/π) Im[log ζ(1/2 + it)]

where arg is taken by continuous variation along the line σ = 1/2.

THE COUNTING FORMULA (Riemann-von Mangoldt):
────────────────────────────────────────────
    N(T) = (1/π)θ(T) + 1 + S(T)

where N(T) = number of zeros with 0 < Im(ρ) ≤ T.

Since N(T) is an integer (counting function), and θ(T) is smooth,
S(T) measures the "deviation" from the smooth approximation.

KEY PROPERTY:
    S(t) jumps by +1 as t passes through a zero on the critical line
    (the argument increases by π).

PROVEN BOUNDS ON S(t):
──────────────────────
1. S(t) = O(log t)           [Littlewood, 1924]
2. S(t) = O(log t / log log t)   [conditionally under RH]
3. |S(t)| ≤ 0.137 log t + 0.443 log log t + 4.350   [Trudgian, 2014]
""")

def theta_function(t: float) -> float:
    """Riemann-Siegel theta function."""
    if t < 1:
        return 0.0
    return (t/2) * np.log(t / (2 * np.pi)) - t/2 - np.pi/8 + 1/(48*t)

def expected_N(T: float) -> float:
    """Expected number of zeros below height T (smooth part)."""
    if T < 1:
        return 0.0
    return theta_function(T) / np.pi + 1

def trudgian_bound(t: float) -> float:
    """Trudgian's explicit bound on |S(t)|."""
    if t < 2:
        return 10.0  # placeholder for small t
    return 0.137 * np.log(t) + 0.443 * np.log(np.log(t)) + 4.350

print("S(t) BOUNDS (Trudgian):")
print()
print("  t              |S(t)| ≤")
print("  " + "-" * 30)
for t in [1e3, 1e6, 1e9, 1e12, 1e15]:
    print(f"  {t:.0e}         {trudgian_bound(t):.2f}")
print()

# =============================================================================
# PART 2: HOW OFF-LINE ZEROS AFFECT N(T) AND S(T)
# =============================================================================

print("=" * 60)
print("PART 2: EFFECT OF OFF-LINE ZEROS ON N(T)")
print("-" * 60)
print()

print("""
THE COUNTING FORMULA:
    N(T) = (1/π)θ(T) + 1 + S(T)

counts ALL zeros with 0 < Im(ρ) ≤ T, regardless of their real part.

CRITICAL OBSERVATION:
─────────────────────
An off-line zero QUADRUPLET at height γ contributes to N(T) like any other zeros.
As we pass T = γ:
    N(T) increases by 2 (the pair ρ₁, ρ₂ at height γ)

But the CONTRIBUTION TO S(t) is different!

FOR ON-LINE ZEROS (ρ = 1/2 + iγ_n):
    As t passes γ_n, arg ζ(1/2 + it) increases by π
    S(t) jumps by +1

FOR OFF-LINE ZEROS (ρ = 1/2 ± ε + iγ):
    The zeros are NOT on the line s = 1/2 + it
    As t passes γ, arg ζ(1/2 + it) does NOT jump by π
    Instead, the argument changes continuously

THE DISCONTINUITY IN S(t):
──────────────────────────
For on-line zeros: S(t) has a jump discontinuity of +1 at each γ_n.
For off-line zeros: S(t) does NOT jump at γ.

But N(T) DOES increase by 2 at T = γ!

This creates a MISMATCH:
    • The counting function N(T) increases by 2
    • The argument S(T) does NOT jump correspondingly
    • The "missing" argument must be compensated elsewhere
""")

# =============================================================================
# PART 3: THE LOCAL S(t) ANOMALY
# =============================================================================

print("=" * 60)
print("PART 3: LOCAL STRUCTURE OF S(t) NEAR OFF-LINE ZERO")
print("-" * 60)
print()

print("""
DETAILED ANALYSIS:

Near an off-line zero pair at 1/2 ± ε + iγ, the zeta function factors as:

    ζ(s) ≈ C · (s - ρ₁)(s - ρ₂) · (other terms)
         = C · [(s - 1/2 - iγ)² - ε²] · (...)

On the critical line s = 1/2 + it:
    ζ(1/2 + it) ≈ C · [-(t - γ)² - ε²] · (...)

THE ARGUMENT:
    arg ζ(1/2 + it) ≈ arg C + arg[-(t-γ)² - ε²] + (other terms)

The factor -(t-γ)² - ε² is ALWAYS NEGATIVE (since (t-γ)² ≥ 0).
Its argument is constant = π.

CONSEQUENCE:
    As t varies through γ, the argument of ζ(1/2 + it) does NOT wind.
    S(t) does NOT jump.

CONTRAST WITH ON-LINE ZERO:
    For ρ = 1/2 + iγ_n on the line:
    ζ(1/2 + it) ≈ C · (t - γ_n) · (...)
    arg(t - γ_n) changes by π as t passes γ_n.
    S(t) jumps by +1.

THE ANOMALY:
────────────
In the region around t = γ:
    • Two zeros are "counted" by N(T) (the off-line pair)
    • But S(t) does NOT increase by 2
    • There's a "phase deficit" of approximately 2
""")

def phase_deficit(epsilon: float) -> float:
    """
    The phase "missing" from S(t) due to off-line zeros.
    For small ε, the deficit is approximately 2 (one for each zero in the pair).
    """
    return 2.0  # The pair contributes 2 to N(T) but ~0 to S(t) jump

print("PHASE DEFICIT ANALYSIS:")
print()
print("  For off-line pair at 1/2 ± ε + iγ:")
print("  • Contribution to N(T): +2 (two zeros counted)")
print(f"  • Jump in S(t): ~0 (no winding on critical line)")
print(f"  • Phase deficit: ~2")
print()

# =============================================================================
# PART 4: TURING'S VERIFICATION METHOD
# =============================================================================

print("=" * 60)
print("PART 4: TURING'S VERIFICATION METHOD")
print("-" * 60)
print()

print("""
TURING'S METHOD (1953):
───────────────────────
To verify that all zeros in an interval [T₁, T₂] lie on the critical line:

1. Compute N(T₂) - N(T₁) using the counting formula
2. Count sign changes of Z(t) in [T₁, T₂] (call this count n)
3. If n = N(T₂) - N(T₁), all zeros in the interval are ON the line

WHY IT WORKS:
    Each zero on the line causes exactly one sign change in Z(t).
    If a zero is OFF the line, it contributes to N(T) but NOT to sign changes.

THE DETECTION:
    Off-line zeros create a DISCREPANCY:
        N(T₂) - N(T₁) > (number of sign changes)

    This discrepancy is EXACTLY the number of off-line zero pairs.

IF AN OFF-LINE PAIR EXISTS AT HEIGHT γ:
    • In interval [γ - δ, γ + δ]:
    • N(γ+δ) - N(γ-δ) increases by 2 (due to the pair)
    • Sign changes of Z(t): 0 (there's a local extremum, not a crossing)
    • DISCREPANCY = 2

This is Turing's "litmus test" for off-line zeros.
""")

def turing_discrepancy(n_offpairs: int) -> int:
    """
    Discrepancy in Turing count due to off-line zero pairs.
    Each off-line pair creates a discrepancy of 2.
    """
    return 2 * n_offpairs

print("TURING DISCREPANCY:")
print()
print("  # Off-line pairs    Discrepancy")
print("  " + "-" * 35)
for n in range(5):
    print(f"  {n}                     {turing_discrepancy(n)}")
print()

# =============================================================================
# PART 5: LOCAL BOUNDS ON S'(t)
# =============================================================================

print("=" * 60)
print("PART 5: DOES THE QUADRUPLET VIOLATE S'(t) BOUNDS?")
print("-" * 60)
print()

print("""
THE QUESTION: Does the phase deficit violate any proven local bounds?

THE S(t) DERIVATIVE:
    S(t) = (1/π) Im[log ζ(1/2 + it)]
    S'(t) = (1/π) Im[(d/dt) log ζ(1/2 + it)]
          = (1/π) Im[iζ'(1/2+it)/ζ(1/2+it)]
          = (1/π) Re[ζ'(1/2+it)/ζ(1/2+it)]

KNOWN BOUNDS ON S'(t):
    There are no strong universal bounds on S'(t).
    S(t) is known to fluctuate by O(log t) over intervals of length O(1).

NEAR AN OFF-LINE ZERO:
    |ζ(1/2 + it)| has a local minimum ≈ ε² (as we computed)
    |ζ'(1/2 + it)| is O(log t) (standard estimate)

    So |S'(t)| ~ (1/π) |ζ'/ζ| ~ (log t) / ε²

FOR ε = 0.01:
    |S'(t)| ~ (log t) / 10⁻⁴ ~ 10⁴ log t

This is LARGE but not technically a violation of proven bounds,
since no strong local bounds on S'(t) exist.
""")

def S_prime_estimate(t: float, epsilon: float) -> float:
    """
    Estimate |S'(t)| near an off-line zero.
    """
    log_t = np.log(t)
    return log_t / (epsilon**2)

print("ESTIMATED |S'(t)| NEAR OFF-LINE ZERO:")
print()
print("  t              ε = 0.01        ε = 0.001       ε = 0.0001")
print("  " + "-" * 60)
for t in [1e6, 1e9, 1e12]:
    s1 = S_prime_estimate(t, 0.01)
    s2 = S_prime_estimate(t, 0.001)
    s3 = S_prime_estimate(t, 0.0001)
    print(f"  {t:.0e}      {s1:.2e}        {s2:.2e}        {s3:.2e}")

print()
print("""
CONCLUSION ON S'(t):
    The derivative S'(t) becomes VERY LARGE near an off-line zero.
    This is anomalous but doesn't violate proven bounds (which are weak).

    However, it DOES make the zero detectable:
    Unusually rapid variation in S(t) signals a potential off-line zero.
""")

# =============================================================================
# PART 6: THE MATHEMATICAL ALARM
# =============================================================================

print("=" * 60)
print("PART 6: THE MATHEMATICAL ALARM")
print("-" * 60)
print()

print("""
TURING'S ABSOLUTE ALARM:
────────────────────────
The definitive signal that a zero has drifted off the line:

    ALARM CONDITION: N(T₂) - N(T₁) ≠ (sign changes of Z(t) in [T₁, T₂])

More specifically:
    If N(T₂) - N(T₁) > sign changes, there are off-line zeros.
    The excess is EXACTLY 2 × (number of off-line pairs).

WHY THIS IS ABSOLUTE:
    • The counting formula N(T) is EXACT (no approximation)
    • Sign changes of Z(t) are EXACTLY countable
    • Any discrepancy is UNDENIABLE proof of off-line zeros

SECONDARY ALARMS:
    1. Local minimum of |Z(t)| that is anomalously small: |Z| ~ ε²
    2. Absence of sign change where Gram's Law predicts one
    3. Rapid variation in S(t): |S'(t)| ~ log(t)/ε²

DETECTION PROCEDURE:
    1. For each Gram block [g_n, g_{n+1}]:
       - Compute N(g_{n+1}) - N(g_n) using the formula
       - Count sign changes of Z(t) in the block
       - If discrepancy exists: ALARM

    2. This is EXACTLY what Odlyzko, Gourdon, and others do.

    3. They have verified 10^13 zeros with NO discrepancy.
""")

# =============================================================================
# PART 7: QUANTIFYING THE DETECTION
# =============================================================================

print("=" * 60)
print("PART 7: QUANTIFYING THE DETECTION THRESHOLD")
print("-" * 60)
print()

def detection_analysis(gamma: float, epsilon: float) -> Dict:
    """
    Analyze detectability of off-line zero at height gamma with deviation epsilon.
    """
    # Gram spacing at height gamma
    theta_prime = 0.5 * np.log(gamma / (2 * np.pi))
    gram_spacing = np.pi / theta_prime

    # Number of Gram blocks up to gamma
    n_gram_blocks = theta_function(gamma) / np.pi

    # The discrepancy appears in ONE Gram block
    # But involves contribution spread over interval ~ ε

    # Precision needed to count zeros accurately
    # We need to verify N(T) to integer accuracy

    # The key is: does the off-line zero cause detectable Turing discrepancy?
    # Answer: YES, always. The discrepancy is exactly 2.

    return {
        "gamma": gamma,
        "epsilon": epsilon,
        "gram_spacing": gram_spacing,
        "n_gram_blocks": n_gram_blocks,
        "turing_discrepancy": 2,
        "detectable": True  # Always detectable via Turing method
    }

print("TURING METHOD ANALYSIS:")
print()
print("  γ              Gram spacing    # Gram blocks    Turing discrepancy")
print("  " + "-" * 65)

for gamma in [1e6, 1e9, 1e12, 1e15]:
    result = detection_analysis(gamma, 0.01)
    print(f"  {gamma:.0e}        {result['gram_spacing']:.4f}          {result['n_gram_blocks']:.2e}          {result['turing_discrepancy']}")

print()
print("""
KEY FINDING:
────────────
The Turing discrepancy is ALWAYS exactly 2 for an off-line pair.
It does NOT depend on ε or γ.

The only way an off-line zero could escape detection is if:
    1. It's above the verified height (~10^12), OR
    2. The counting formula N(T) has an error

Option 2 is impossible: N(T) is derived from rigorous mathematics.
Option 1 means: if an off-line zero exists, it's VERY high.
""")

# =============================================================================
# FINAL SUMMARY
# =============================================================================

print("=" * 80)
print("FINAL ANSWER: THE S(t) DETECTION FILTER")
print("=" * 80)
print()

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    DETECTION FILTER 2: CONCLUSIONS                           ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  THE OFF-LINE ZERO CREATES A DEFINITE SIGNATURE IN S(t):                     ║
║                                                                              ║
║  1. TURING DISCREPANCY:                                                      ║
║     • N(T₂) - N(T₁) counts 2 zeros (the off-line pair)                       ║
║     • Sign changes of Z(t) count 0 (no crossing, just extremum)              ║
║     • Discrepancy = 2 (ABSOLUTE, independent of ε or γ)                      ║
║                                                                              ║
║  2. S(t) BEHAVIOR:                                                           ║
║     • On-line zeros: S(t) jumps by +1 at each zero                           ║
║     • Off-line zeros: S(t) does NOT jump                                     ║
║     • The "missing" phase creates an anomaly in integrated S(t)              ║
║                                                                              ║
║  3. S'(t) MAGNITUDE:                                                         ║
║     • Near off-line zero: |S'(t)| ~ log(γ)/ε²                                ║
║     • For ε = 0.01, γ = 10^12: |S'(t)| ~ 10^6                                ║
║     • This is anomalously large (rapid variation)                            ║
║                                                                              ║
║  TURING'S METHOD IS AN ABSOLUTE ALARM:                                       ║
║  ─────────────────────────────────────                                       ║
║  • Any discrepancy between N(T) and sign changes = proof of off-line zero    ║
║  • This is EXACTLY what computational verification uses                      ║
║  • 10^13 zeros verified with ZERO discrepancy                                ║
║                                                                              ║
║  THE CONCLUSION:                                                             ║
║  ───────────────                                                             ║
║  If an off-line zero exists below verified height, Turing's method           ║
║  MUST have found the discrepancy. It didn't.                                 ║
║                                                                              ║
║  Either RH is TRUE, or counterexamples are above 3×10^12.                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

print("Detection Filter 2 complete.")
print("=" * 80)
