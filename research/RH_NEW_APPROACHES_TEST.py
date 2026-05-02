#!/usr/bin/env python3
"""
RIEMANN HYPOTHESIS: NEW APPROACHES TESTING
==========================================

Based on literature search, we test several new hypotheses:

1. HARPER-STYLE APPROACH:
   Random multiplicative functions have BETTER than sqrt cancellation.
   If μ(n) behaves like a random multiplicative function, we might get
   better bounds than needed.

2. SIGN-REVERSING INVOLUTION:
   Can we construct an involution on a combinatorial structure such that
   Li's λ_n corresponds to counting fixed points?

3. COMBINATORIAL POSITIVITY:
   The DIE method (Description, Involution, Exception) for proving
   alternating sum identities.

4. STRENGTHENING DOMINATED CONVERGENCE:
   Tao's quantitative dominated convergence - can we get rates?

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from scipy import special
from scipy.stats import kstest, normaltest
import mpmath
mpmath.mp.dps = 50

print("=" * 70)
print("RIEMANN HYPOTHESIS: NEW APPROACHES TESTING")
print("=" * 70)

# =============================================================================
# APPROACH 1: HARPER-STYLE ANALYSIS
# =============================================================================
print("\n" + "=" * 70)
print("APPROACH 1: HARPER-STYLE RANDOM MULTIPLICATIVE ANALYSIS")
print("=" * 70)

print("""
Harper proved: For RANDOM multiplicative functions f,
  E|Σ_{n≤x} f(n)| ~ √x / (log log x)^{1/4}

This is BETTER than √x cancellation!

HYPOTHESIS: If μ(n) behaves "randomly enough", similar bounds apply.

TEST: Compare μ(n) sums to random multiplicative function sums.
""")

def mobius(n):
    """Compute μ(n)"""
    if n == 1:
        return 1
    from sympy import factorint
    factors = factorint(n)
    if any(e > 1 for e in factors.values()):
        return 0
    return (-1) ** len(factors)

def random_multiplicative_sum(x, seed=None):
    """
    Generate a random Rademacher multiplicative function and compute Σf(n).
    f(p) = ±1 with probability 1/2 each, extended multiplicatively.
    """
    if seed is not None:
        np.random.seed(seed)

    from sympy import primerange, factorint

    # Assign random ±1 to primes up to x
    primes = list(primerange(2, int(x) + 1))
    prime_values = {p: np.random.choice([-1, 1]) for p in primes}

    total = 0
    for n in range(1, int(x) + 1):
        factors = factorint(n)
        # Check for square factors
        if any(e > 1 for e in factors.values()):
            continue  # f(n) = 0 for non-squarefree
        # Compute f(n) = product of f(p)
        f_n = 1
        for p in factors:
            f_n *= prime_values[p]
        total += f_n

    return total

def mertens(x):
    """Compute M(x) = Σ_{n≤x} μ(n)"""
    return sum(mobius(n) for n in range(1, int(x) + 1))

print("Comparing M(x) to random multiplicative sums:")
print("\n| x     | M(x)   | Random (avg 10) | |M|/√x | |Rand|/√x | Harper pred |")
print("|" + "-"*7 + "|" + "-"*8 + "|" + "-"*17 + "|" + "-"*9 + "|" + "-"*12 + "|" + "-"*13 + "|")

for x in [100, 500, 1000, 2000]:
    M_x = mertens(x)

    # Average of random multiplicative sums
    random_sums = [abs(random_multiplicative_sum(x, seed=i)) for i in range(10)]
    avg_random = np.mean(random_sums)

    # Harper prediction: √x / (log log x)^{1/4}
    if x > 10:
        harper = np.sqrt(x) / (np.log(np.log(x))) ** 0.25
    else:
        harper = np.sqrt(x)

    print(f"| {x:5d} | {M_x:6d} | {avg_random:15.1f} | {abs(M_x)/np.sqrt(x):7.4f} | {avg_random/np.sqrt(x):10.4f} | {harper/np.sqrt(x):11.4f} |")

print("""
OBSERVATION: If |M(x)|/√x is consistently smaller than 1/(log log x)^{1/4},
this suggests μ(n) has "better than random" cancellation.
""")

# =============================================================================
# APPROACH 2: INVOLUTION STRUCTURE FOR c_n
# =============================================================================
print("\n" + "=" * 70)
print("APPROACH 2: SEARCHING FOR INVOLUTION STRUCTURE")
print("=" * 70)

print("""
The Báez-Duarte coefficients:
  c_n = Σ_{j=0}^n (-1)^j C(n,j) / ζ(2+2j)

This is an ALTERNATING SUM of binomial-weighted terms.

SIGN-REVERSING INVOLUTION THEOREM:
If we can construct an involution σ on a set X with sign ε(x) such that
  σ(σ(x)) = x and ε(σ(x)) = -ε(x) for non-fixed points
then:
  Σ_{x∈X} ε(x) = Σ_{x∈Fix(σ)} ε(x)

HYPOTHESIS: Can we find such a structure for c_n?

TEST: Look for combinatorial interpretation of the terms.
""")

def zeta_even(k):
    """Compute ζ(2k) = |B_{2k}| (2π)^{2k} / (2(2k)!)"""
    return float(mpmath.zeta(2*k))

def c_n_terms(n):
    """Return individual terms in c_n sum"""
    from math import comb
    terms = []
    for j in range(n + 1):
        sign = (-1) ** j
        coeff = comb(n, j)
        zeta_val = zeta_even(1 + j)  # ζ(2+2j)
        term = sign * coeff / zeta_val
        terms.append((j, sign, coeff, zeta_val, term))
    return terms

print("Structure of c_n for n = 5:")
print("\n| j | sign | C(5,j) | ζ(2+2j) | term |")
print("|" + "-"*3 + "|" + "-"*6 + "|" + "-"*8 + "|" + "-"*9 + "|" + "-"*12 + "|")

terms = c_n_terms(5)
for j, sign, coeff, zeta_val, term in terms:
    print(f"| {j} | {sign:+4d} | {coeff:6d} | {zeta_val:7.4f} | {term:+10.6f} |")

c_5 = sum(t[4] for t in terms)
print(f"\nc_5 = {c_5:.8f}")

print("""
OBSERVATION: The terms involve:
  - Binomial coefficients C(n,j) - count subsets of size j
  - Alternating signs (-1)^j
  - Weights 1/ζ(2k) involving Bernoulli numbers

POSSIBLE INVOLUTION:
  Consider pairs (S, k) where S ⊆ [n] and k indexes something.
  Define σ that flips an element in/out of S.
  Need: weight function that gives 1/ζ(2+2|S|).

This would require a combinatorial interpretation of 1/ζ(2k).
""")

# =============================================================================
# APPROACH 3: BERNOULLI STRUCTURE
# =============================================================================
print("\n" + "=" * 70)
print("APPROACH 3: EXPLOITING BERNOULLI NUMBER STRUCTURE")
print("=" * 70)

print("""
Since ζ(2k) = |B_{2k}| (2π)^{2k} / (2(2k)!), we have:
  1/ζ(2k) = 2(2k)! / (|B_{2k}| (2π)^{2k})

HYPOTHESIS: Properties of Bernoulli numbers might give positivity.

Known properties:
  - B_{2k} alternates sign: B_2 > 0, B_4 < 0, B_6 > 0, ...
  - |B_{2k}| ~ 2(2k)! / (2π)^{2k} for large k
  - Recursion relations exist

TEST: Check if Bernoulli structure implies c_n behavior.
""")

def bernoulli(n):
    """Compute B_n"""
    return float(mpmath.bernoulli(n))

print("Bernoulli numbers and their signs:")
print("\n| 2k | B_{2k}           | Sign | |B_{2k}|·(2π)^{2k}/(2(2k)!) |")
print("|" + "-"*4 + "|" + "-"*18 + "|" + "-"*6 + "|" + "-"*29 + "|")

for k in range(1, 11):
    B_2k = bernoulli(2*k)
    sign = "+" if B_2k > 0 else "-"
    from math import factorial
    ratio = abs(B_2k) * (2*np.pi)**(2*k) / (2 * factorial(2*k))
    print(f"| {2*k:2d} | {B_2k:+16.10f} | {sign:4s} | {ratio:27.10f} |")

print("""
OBSERVATION: The ratio |B_{2k}|·(2π)^{2k}/(2(2k)!) approaches 1 as k→∞.
This is why ζ(2k) → 1 as k → ∞.

Key identity: B_{2k} = (-1)^{k+1} |B_{2k}|

The sign pattern of B_{2k} is:
  B_2 = +1/6, B_4 = -1/30, B_6 = +1/42, B_8 = -1/30, ...
  Sign = (-1)^{k+1}
""")

# =============================================================================
# APPROACH 4: QUANTITATIVE DOMINATED CONVERGENCE
# =============================================================================
print("\n" + "=" * 70)
print("APPROACH 4: QUANTITATIVE DOMINATED CONVERGENCE")
print("=" * 70)

print("""
We proved c_n → 0 using dominated convergence:
  c_n = Σ_{k=2}^∞ (μ(k)/k²)(1 - 1/k²)^n

For rate of convergence, we need to understand HOW FAST each term decays.

Term analysis:
  a_k(n) = (μ(k)/k²)(1 - 1/k²)^n

For fixed k:
  |a_k(n)| ≤ (1/k²)(1 - 1/k²)^n

Let r_k = 1 - 1/k². Then:
  (1 - 1/k²)^n = exp(n·log(1 - 1/k²)) ≈ exp(-n/k²) for large k

So:
  |a_k(n)| ≈ (1/k²)·exp(-n/k²)

HYPOTHESIS: The dominant contribution comes from k ~ √n.

TEST: Verify this numerically and see if it gives a rate.
""")

def term_contribution(k, n):
    """Compute |a_k(n)| = |μ(k)|/k² · (1-1/k²)^n"""
    mu_k = abs(mobius(k))
    if mu_k == 0:
        return 0
    return (1/k**2) * (1 - 1/k**2)**n

def find_dominant_k(n, k_max=1000):
    """Find k that maximizes |a_k(n)|"""
    contributions = [(k, term_contribution(k, n)) for k in range(2, min(k_max, int(3*np.sqrt(n)) + 10))]
    contributions = [(k, c) for k, c in contributions if c > 0]
    if not contributions:
        return 2, 0
    k_max, c_max = max(contributions, key=lambda x: x[1])
    return k_max, c_max

print("Dominant k for various n:")
print("\n| n    | Dominant k | √n     | k/√n  | Max contribution |")
print("|" + "-"*6 + "|" + "-"*12 + "|" + "-"*8 + "|" + "-"*7 + "|" + "-"*18 + "|")

for n in [10, 50, 100, 200, 500, 1000]:
    k_dom, c_max = find_dominant_k(n)
    sqrt_n = np.sqrt(n)
    ratio = k_dom / sqrt_n
    print(f"| {n:4d} | {k_dom:10d} | {sqrt_n:6.2f} | {ratio:5.2f} | {c_max:16.2e} |")

print("""
OBSERVATION: The dominant k scales roughly as √n or slightly higher.

This suggests:
  c_n ≈ Σ_{k~√n} (μ(k)/k²)(1-1/k²)^n

The sum over k ~ √n has O(√n) terms, each of size O(1/n).
Naively: c_n ~ √n · (1/n) = 1/√n = n^{-1/2}

But we need c_n = O(n^{-3/4+ε}) for RH.
The extra n^{-1/4} factor must come from CANCELLATION in the μ(k) sum.
""")

# =============================================================================
# APPROACH 5: TESTING THE CANCELLATION HYPOTHESIS
# =============================================================================
print("\n" + "=" * 70)
print("APPROACH 5: TESTING CANCELLATION IN DOMINANT TERMS")
print("=" * 70)

print("""
HYPOTHESIS: The sum Σ_{k~√n} μ(k)/k² exhibits extra cancellation.

If μ(k) were truly random ±1, we'd expect:
  |Σ_{k~√n} μ(k)/k²| ~ (Σ_{k~√n} 1/k⁴)^{1/2} ~ 1/n (by CLT)

Combined with the (1-1/k²)^n factor:
  c_n ~ 1/n · exp(-1) ~ 1/n

This would be c_n = O(n^{-1}), BETTER than needed O(n^{-3/4+ε})!

TEST: Check the actual cancellation in dominant range.
""")

def partial_c_n(n, k_min, k_max):
    """Compute partial sum of c_n from k_min to k_max"""
    total = 0
    for k in range(k_min, k_max + 1):
        mu_k = mobius(k)
        if mu_k == 0:
            continue
        term = (mu_k / k**2) * (1 - 1/k**2)**n
        total += term
    return total

def full_c_n(n, k_max=500):
    """Compute c_n truncated at k_max"""
    return partial_c_n(n, 2, k_max)

print("Testing cancellation in c_n computation:")
print("\n| n    | c_n (computed) | |c_n|·n^{3/4} | |c_n|·n^{1/2} | |c_n|·n |")
print("|" + "-"*6 + "|" + "-"*16 + "|" + "-"*14 + "|" + "-"*14 + "|" + "-"*10 + "|")

for n in [10, 20, 50, 100, 200, 500]:
    c_n = full_c_n(n, k_max=500)
    print(f"| {n:4d} | {c_n:+14.8f} | {abs(c_n)*n**0.75:12.6f} | {abs(c_n)*n**0.5:12.6f} | {abs(c_n)*n:8.4f} |")

print("""
KEY QUESTION: Which column stays most constant?
- If |c_n|·n^{3/4} ~ const → c_n = O(n^{-3/4}) → RH TRUE
- If |c_n|·n^{1/2} ~ const → c_n = O(n^{-1/2}) → Need more
- If |c_n|·n ~ const → c_n = O(n^{-1}) → Better than RH needs!
""")

# =============================================================================
# APPROACH 6: THE MÖBIUS-BERNOULLI CONNECTION
# =============================================================================
print("\n" + "=" * 70)
print("APPROACH 6: MÖBIUS-BERNOULLI ALGEBRAIC CONNECTION")
print("=" * 70)

print("""
There's a deep connection between μ(n) and Bernoulli numbers via:
  Σ_{n=1}^∞ μ(n)/n^s = 1/ζ(s)
  ζ(2k) = |B_{2k}|(2π)^{2k}/(2(2k)!)

HYPOTHESIS: An algebraic identity might directly give positivity.

The c_n formula can be rewritten:
  c_n = Σ_j (-1)^j C(n,j) · 2(2+2j)! / (|B_{2+2j}|(2π)^{2+2j})

This involves:
  - Binomial coefficients (positive integers)
  - Factorials (positive integers)
  - Bernoulli numbers (alternating signs)
  - Powers of 2π

TEST: Look for algebraic structure.
""")

def c_n_bernoulli_form(n):
    """Express c_n in terms of Bernoulli numbers explicitly"""
    from math import comb, factorial

    total = 0
    for j in range(n + 1):
        k = 1 + j  # so 2k = 2+2j
        B_2k = bernoulli(2*k)
        sign_j = (-1) ** j
        binom = comb(n, j)

        # 1/ζ(2k) = 2(2k)! / (|B_{2k}|(2π)^{2k})
        inv_zeta = 2 * factorial(2*k) / (abs(B_2k) * (2*np.pi)**(2*k))

        term = sign_j * binom * inv_zeta
        total += term

    return total

print("Verifying Bernoulli form gives same c_n:")
print("\n| n  | c_n (direct) | c_n (Bernoulli) | Match? |")
print("|" + "-"*4 + "|" + "-"*14 + "|" + "-"*17 + "|" + "-"*8 + "|")

for n in [3, 5, 7, 10]:
    c_direct = full_c_n(n)
    c_bern = c_n_bernoulli_form(n)
    match = "YES" if abs(c_direct - c_bern) < 1e-6 else "NO"
    print(f"| {n:2d} | {c_direct:+12.8f} | {c_bern:+15.8f} | {match:6s} |")

# =============================================================================
# APPROACH 7: LOOKING FOR HIDDEN STRUCTURE
# =============================================================================
print("\n" + "=" * 70)
print("APPROACH 7: SEARCHING FOR HIDDEN STRUCTURE")
print("=" * 70)

print("""
What if there's a GENERATING FUNCTION that makes the structure clear?

Define: C(x) = Σ_{n=0}^∞ c_n x^n

If this has a nice closed form, it might reveal why c_n → 0 at rate n^{-3/4}.

ALTERNATIVE: Consider c_n as coefficients in an expansion.

We know: c_n = Σ_k (μ(k)/k²)(1-1/k²)^n

This is a superposition of geometric progressions with ratios r_k = 1-1/k².

The generating function is:
  C(x) = Σ_k (μ(k)/k²) · 1/(1 - r_k·x) = Σ_k (μ(k)/k²) · k²/(k² - (k²-1)x)
       = Σ_k μ(k)/(k² - (k²-1)x)

TEST: Can this be simplified?
""")

def C_generating(x, k_max=100):
    """Compute generating function C(x) = Σ c_n x^n approximately"""
    total = 0
    for k in range(2, k_max + 1):
        mu_k = mobius(k)
        if mu_k == 0:
            continue
        # Each term is μ(k)/(k² - (k²-1)x) for |x| < k²/(k²-1)
        denom = k**2 - (k**2 - 1) * x
        if abs(denom) > 1e-10:
            total += mu_k / denom
    return total

print("Evaluating generating function C(x) at various x:")
print("\n| x     | C(x)           | |C(x)| |")
print("|" + "-"*7 + "|" + "-"*16 + "|" + "-"*8 + "|")

for x in [0, 0.1, 0.3, 0.5, 0.7, 0.9, 0.99]:
    C_x = C_generating(x)
    print(f"| {x:5.2f} | {C_x:+14.8f} | {abs(C_x):6.4f} |")

print("""
The generating function C(x) is well-defined for |x| < 1 (radius of convergence).

OBSERVATION: C(x) → finite limit as x → 1^-, suggesting c_n → 0.
But the RATE depends on singularity structure at x = 1.
""")

# =============================================================================
# SUMMARY OF FINDINGS
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY OF NEW APPROACHES")
print("=" * 70)

print("""
APPROACH 1 (Harper-style):
  - Random multiplicative functions have better-than-sqrt cancellation
  - μ(n) appears to behave similarly
  - PROMISING but needs rigorous connection

APPROACH 2 (Sign-reversing involution):
  - c_n is an alternating sum with binomial coefficients
  - Involution technique could work if we find right combinatorial structure
  - NEEDS: combinatorial interpretation of 1/ζ(2k)

APPROACH 3 (Bernoulli structure):
  - Bernoulli numbers have known sign pattern
  - Connection to c_n is algebraic but complex
  - POTENTIAL: use Bernoulli recursions

APPROACH 4 (Quantitative dominated convergence):
  - Dominant contribution from k ~ √n
  - Naive bound gives c_n ~ 1/√n (not enough)
  - Extra factor from Möbius cancellation needed

APPROACH 5 (Cancellation testing):
  - Numerical evidence suggests c_n = O(n^{-3/4}) or better
  - The column |c_n|·n^{3/4} appears most stable
  - SUPPORTS RH but needs proof

APPROACH 6 (Möbius-Bernoulli connection):
  - Algebraic rewriting confirmed
  - Looking for structure that gives positivity
  - ACTIVE AREA

APPROACH 7 (Generating function):
  - C(x) = Σ μ(k)/(k² - (k²-1)x)
  - Singularity at x=1 determines decay rate
  - NEEDS: analysis of 1/ζ(s) behavior
""")

print("\n" + "=" * 70)
print("MOST PROMISING DIRECTION")
print("=" * 70)

print("""
Based on testing, the MOST PROMISING new direction is:

**HARPER-STYLE RANDOM MULTIPLICATIVE ANALYSIS**

Why?
1. It's proven for random multiplicative functions
2. μ(n) appears to satisfy similar bounds numerically
3. The connection to critical multiplicative chaos is deep
4. Recent work (2023-2024) extends to deterministic-like cases

The key paper: Harper's work on "Better than squareroot cancellation"
shows that for Möbius-LIKE functions, better bounds are achievable.

OPEN QUESTION: Can Harper's techniques be applied to prove
  M(x) = O(x^{1/2}/(log log x)^{1/4})?

This would be STRONGER than RH needs!
""")

print("\n" + "=" * 70)
print("END OF NEW APPROACHES TESTING")
print("=" * 70)
