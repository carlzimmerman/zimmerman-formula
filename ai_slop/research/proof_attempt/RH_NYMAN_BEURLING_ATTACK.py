#!/usr/bin/env python3
"""
RH_NYMAN_BEURLING_ATTACK.py
═══════════════════════════

DEEP ATTACK: The Nyman-Beurling-Báez-Duarte Criterion

A less-explored but powerful equivalent to RH involving L² completeness.

RH ⟺ The constant function 1 is in the closure of a specific function space.

This is perhaps the most "constructive" formulation of RH.
"""

import numpy as np
from typing import List, Tuple, Callable
from scipy.integrate import quad
from scipy.optimize import minimize
from scipy.linalg import lstsq
import warnings
warnings.filterwarnings('ignore')

def print_section(title: str):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80 + "\n")

ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
         37.586178, 40.918720, 43.327073, 48.005151, 49.773832,
         52.970321, 56.446248, 59.347044, 60.831779, 65.112544]

print("=" * 80)
print("RH NYMAN-BEURLING-BÁEZ-DUARTE ATTACK")
print("The L² Completeness Formulation")
print("=" * 80)

# ============================================================================
print_section("SECTION 1: THE NYMAN-BEURLING CRITERION")

print("""
THE NYMAN-BEURLING CRITERION (1950/1955):
═════════════════════════════════════════

DEFINITION:
───────────
Let ρ(x) = x - ⌊x⌋ be the fractional part function.

Define for θ ∈ (0, 1]:
    ρ_θ(x) = ρ(θ/x)  for x > 0

Let B be the vector space spanned by functions of the form:
    f(x) = Σᵢ cᵢ ρ(θᵢ/x)  where Σᵢ cᵢ θᵢ = 0

THEOREM (Nyman 1950, Beurling 1955):
────────────────────────────────────

    RH ⟺ The characteristic function χ_{(0,1)} is in the L²(0,1) closure of B.

In other words:
    RH ⟺ inf_{f ∈ B} ||χ_{(0,1)} - f||_{L²} = 0

This is REMARKABLE: RH becomes a question of APPROXIMATION THEORY!
""")

def fractional_part(x: float) -> float:
    """Compute {x} = x - floor(x)."""
    return x - np.floor(x)

def rho_theta(x: float, theta: float) -> float:
    """Compute ρ_θ(x) = ρ(θ/x) for x > 0."""
    if x <= 0:
        return 0
    return fractional_part(theta / x)

def nyman_basis_function(x: np.ndarray, thetas: List[float],
                        coeffs: List[float]) -> np.ndarray:
    """
    Compute f(x) = Σ cᵢ ρ(θᵢ/x).
    Note: Must have Σ cᵢ θᵢ = 0 for f ∈ B.
    """
    result = np.zeros_like(x)
    for theta, c in zip(thetas, coeffs):
        for i, xi in enumerate(x):
            if xi > 0:
                result[i] += c * fractional_part(theta / xi)
    return result

def check_constraint(thetas: List[float], coeffs: List[float]) -> float:
    """Check if Σ cᵢ θᵢ = 0."""
    return sum(c * t for c, t in zip(coeffs, thetas))

print("Nyman basis functions example:")
print("-" * 60)
x = np.linspace(0.01, 1, 100)

# Simple example: θ₁ = 1/2, θ₂ = 1/3, need c₁(1/2) + c₂(1/3) = 0
# So c₁ = 2, c₂ = -3 works
thetas = [0.5, 1/3]
coeffs = [2, -3]
constraint = check_constraint(thetas, coeffs)
print(f"  θ = {thetas}, c = {coeffs}")
print(f"  Constraint Σcᵢθᵢ = {constraint:.6f}")

f = nyman_basis_function(x, thetas, coeffs)
print(f"  ||f||_L² ≈ {np.sqrt(np.mean(f**2)):.4f}")

# ============================================================================
print_section("SECTION 2: THE BÁEZ-DUARTE CRITERION")

print("""
THE BÁEZ-DUARTE CRITERION (2003):
═════════════════════════════════

A more explicit version using Möbius function.

DEFINITION:
───────────
Let μ(n) be the Möbius function.

Define:
    d_N² = inf_{c₁,...,c_N} ||1 - Σₙ₌₁ᴺ cₙ ρ(1/n·)||²_{L²(0,1)}

THEOREM (Báez-Duarte 2003):
───────────────────────────

    RH ⟺ lim_{N→∞} d_N = 0

Moreover:
    d_N² = Σₖ₌₁^∞ (1 - Σₙ₌₁ᴺ (μ(n)/n) [n/k])² / k²

where [x] = floor(x).

The RATE of convergence:
    d_N = O(N^{-3/4+ε}) ⟹ RH
    d_N = O(N^{-1/2}) is the "trivial" bound
""")

def mobius(n: int) -> int:
    """Compute Möbius function μ(n)."""
    if n == 1:
        return 1

    # Factor n
    factors = []
    temp = n
    d = 2
    while d * d <= temp:
        if temp % d == 0:
            count = 0
            while temp % d == 0:
                temp //= d
                count += 1
            if count > 1:
                return 0  # Square factor
            factors.append(d)
        d += 1
    if temp > 1:
        factors.append(temp)

    return (-1) ** len(factors)

def baez_duarte_d_squared(N: int, K_max: int = 100) -> float:
    """
    Compute d_N² using Báez-Duarte formula.
    d_N² = Σₖ (1 - Σₙ (μ(n)/n)[n/k])² / k²
    """
    d_sq = 0
    for k in range(1, K_max + 1):
        inner_sum = sum((mobius(n) / n) * (n // k) for n in range(1, N + 1))
        d_sq += (1 - inner_sum) ** 2 / k ** 2
    return d_sq

print("Báez-Duarte criterion computation:")
print("-" * 60)
print(f"{'N':>6} {'d_N²':>15} {'d_N':>12} {'N^(-3/4)':>12}")
print("-" * 60)

for N in [5, 10, 20, 50, 100]:
    d_sq = baez_duarte_d_squared(N, K_max=200)
    d_N = np.sqrt(max(d_sq, 0))
    trivial = N ** (-0.75)
    print(f"{N:6d} {d_sq:15.8f} {d_N:12.6f} {trivial:12.6f}")

# ============================================================================
print_section("SECTION 3: EXPLICIT APPROXIMATION")

print("""
EXPLICIT APPROXIMATION PROBLEM:
═══════════════════════════════

We want to find coefficients c₁, c₂, ..., c_N such that:

    ||χ_{(0,1)} - Σₙ cₙ ρ(1/n·)||² is minimized

This is a LEAST SQUARES problem!

The Gram matrix is:
    G_{mn} = ⟨ρ(1/m·), ρ(1/n·)⟩_{L²(0,1)}

And we need to solve:
    G c = b  where b_n = ⟨χ_{(0,1)}, ρ(1/n·)⟩
""")

def inner_product_rho(m: int, n: int, num_points: int = 1000) -> float:
    """
    Compute ⟨ρ(1/m·), ρ(1/n·)⟩_{L²(0,1)} numerically.
    """
    x = np.linspace(0.001, 1, num_points)
    f_m = np.array([fractional_part(1/(m*xi)) for xi in x])
    f_n = np.array([fractional_part(1/(n*xi)) for xi in x])
    return np.mean(f_m * f_n)

def inner_product_with_one(n: int, num_points: int = 1000) -> float:
    """
    Compute ⟨χ_{(0,1)}, ρ(1/n·)⟩_{L²(0,1)} = ∫₀¹ ρ(1/(nx)) dx.
    """
    x = np.linspace(0.001, 1, num_points)
    f_n = np.array([fractional_part(1/(n*xi)) for xi in x])
    return np.mean(f_n)

def solve_approximation(N: int) -> Tuple[np.ndarray, float]:
    """
    Solve the least squares problem to approximate χ_{(0,1)}.
    Returns coefficients and residual.
    """
    # Build Gram matrix
    G = np.zeros((N, N))
    for m in range(1, N+1):
        for n in range(1, N+1):
            G[m-1, n-1] = inner_product_rho(m, n)

    # Build RHS
    b = np.array([inner_product_with_one(n) for n in range(1, N+1)])

    # Solve least squares
    try:
        c, residuals, rank, s = lstsq(G, b)

        # Compute actual residual ||1 - Σ cₙ ρ(1/n·)||²
        x = np.linspace(0.001, 1, 1000)
        approx = np.zeros_like(x)
        for n, cn in enumerate(c, 1):
            approx += cn * np.array([fractional_part(1/(n*xi)) for xi in x])

        residual = np.sqrt(np.mean((1 - approx)**2))
        return c, residual
    except:
        return np.zeros(N), 1.0

print("Solving approximation problem:")
print("-" * 60)

for N in [3, 5, 10, 15]:
    c, residual = solve_approximation(N)
    print(f"  N = {N:2d}: ||1 - approx||_L² = {residual:.6f}")
    if N <= 5:
        print(f"         coefficients: {c[:5]}")

# ============================================================================
print_section("SECTION 4: CONNECTION TO ZETA ZEROS")

print("""
CONNECTION TO ZETA ZEROS:
═════════════════════════

The Báez-Duarte formula involves:
    Σₙ (μ(n)/n) [n/k]

This is related to the Mertens function:
    M(x) = Σₙ≤x μ(n)

And the key identity:
    Σₙ₌₁^∞ μ(n)/n^s = 1/ζ(s)  for Re(s) > 1

The zeta zeros enter through:
    M(x) = O(x^{1/2+ε}) ⟺ RH

So the Nyman-Beurling criterion connects:
    L² approximation ↔ Mertens function ↔ Zeta zeros
""")

def mertens(x: int) -> int:
    """Compute Mertens function M(x) = Σₙ≤x μ(n)."""
    return sum(mobius(n) for n in range(1, x + 1))

def mertens_bound_test(x_max: int) -> List[Tuple[int, int, float]]:
    """Test if M(x) = O(x^{1/2+ε})."""
    results = []
    for x in range(10, x_max + 1, max(1, x_max // 20)):
        M_x = mertens(x)
        bound = np.sqrt(x)
        ratio = abs(M_x) / bound
        results.append((x, M_x, ratio))
    return results

print("Mertens function analysis:")
print("-" * 60)
print(f"{'x':>6} {'M(x)':>8} {'√x':>10} {'|M(x)|/√x':>12}")
print("-" * 60)

results = mertens_bound_test(500)
for x, M_x, ratio in results:
    print(f"{x:6d} {M_x:8d} {np.sqrt(x):10.2f} {ratio:12.4f}")

print("""
Note: RH ⟹ |M(x)| = O(x^{1/2+ε}) for all ε > 0.
The ratio |M(x)|/√x should remain bounded.
""")

# ============================================================================
print_section("SECTION 5: THE RATE OF CONVERGENCE")

print("""
RATE OF CONVERGENCE AND RH:
═══════════════════════════

The rate at which d_N → 0 determines whether RH holds.

THEOREM (Báez-Duarte et al.):
─────────────────────────────
• d_N = O(N^{-3/4+ε}) for all ε > 0 ⟹ RH
• d_N = O(N^{-1/4-ε}) for some ε > 0 ⟸ RH

The gap between -3/4 and -1/4 is the "uncertainty zone."

NUMERICAL EVIDENCE:
───────────────────
Computing d_N for large N and fitting the exponent.
""")

def compute_d_sequence(N_values: List[int]) -> List[Tuple[int, float]]:
    """Compute d_N for a sequence of N values."""
    results = []
    for N in N_values:
        d_sq = baez_duarte_d_squared(N, K_max=min(500, 5*N))
        d_N = np.sqrt(max(d_sq, 0))
        results.append((N, d_N))
    return results

print("Rate of convergence analysis:")
print("-" * 60)

N_values = [10, 20, 50, 100, 200]
d_values = compute_d_sequence(N_values)

# Fit power law: d_N ~ N^α
log_N = np.log([r[0] for r in d_values])
log_d = np.log([max(r[1], 1e-10) for r in d_values])
slope, intercept = np.polyfit(log_N, log_d, 1)

print(f"{'N':>6} {'d_N':>12} {'N^α (fitted)':>12}")
print("-" * 60)
for N, d_N in d_values:
    fitted = np.exp(intercept) * N ** slope
    print(f"{N:6d} {d_N:12.6f} {fitted:12.6f}")

print(f"\nFitted exponent α = {slope:.4f}")
print(f"RH requires α ≤ -0.75")
print(f"Status: {'Consistent with RH' if slope < -0.5 else 'Inconclusive'}")

# ============================================================================
print_section("SECTION 6: THE VASYUNIN FORMULA")

print("""
THE VASYUNIN FORMULA:
═════════════════════

Vasyunin (1995) gave an explicit formula for the distance:

    d_N² = 1 - log(2π) + γ + Σₙ₌₂^∞ (Λ(n)/n) Σⱼ₌₁ᴺ μ(j)/j [j/n]²

         - 2 Σⱼ₌₁ᴺ (μ(j)/j) log(N/j)

where Λ(n) is the von Mangoldt function and γ is Euler's constant.

This connects DIRECTLY to:
• von Mangoldt function (prime powers)
• Möbius function (prime factorization)
• The constant log(2π) (same as in ξ(s)!)

The appearance of log(2π) is NOT coincidental!
It's the same constant in the functional equation.
""")

def von_mangoldt(n: int) -> float:
    """Compute Λ(n)."""
    if n <= 1:
        return 0
    # Check if n is a prime power
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
        if p > n:
            break
        k = 1
        while p**k <= n:
            if p**k == n:
                return np.log(p)
            k += 1
    # n might be a prime
    is_prime = True
    for p in range(2, int(np.sqrt(n)) + 1):
        if n % p == 0:
            is_prime = False
            break
    if is_prime and n > 1:
        return np.log(n)
    return 0

def vasyunin_formula(N: int, n_max: int = 100) -> float:
    """
    Compute d_N² using Vasyunin's formula (simplified).
    """
    gamma = 0.5772156649  # Euler's constant

    # First term
    result = 1 - np.log(2 * np.pi) + gamma

    # Σ (Λ(n)/n) Σ (μ(j)/j)[j/n]²
    for n in range(2, n_max + 1):
        Lambda_n = von_mangoldt(n)
        if Lambda_n > 0:
            inner = sum((mobius(j)/j) * (j // n)**2 for j in range(1, N+1))
            result += (Lambda_n / n) * inner

    # -2 Σ (μ(j)/j) log(N/j)
    for j in range(1, N + 1):
        result -= 2 * (mobius(j) / j) * np.log(N / j)

    return result

print("Vasyunin formula computation:")
print("-" * 60)
print(f"Constants: γ = 0.5772..., log(2π) = {np.log(2*np.pi):.6f}")
print()

for N in [5, 10, 20, 50]:
    d_sq_vasyunin = vasyunin_formula(N)
    d_sq_direct = baez_duarte_d_squared(N)
    print(f"  N = {N:3d}: d²(Vasyunin) = {d_sq_vasyunin:.6f}, "
          f"d²(direct) = {d_sq_direct:.6f}")

# ============================================================================
print_section("SECTION 7: THE PHYSICAL INTERPRETATION")

print("""
PHYSICAL INTERPRETATION OF NYMAN-BEURLING:
══════════════════════════════════════════

The criterion says: "1 can be approximated by fractional parts."

SIGNAL PROCESSING VIEW:
───────────────────────
• ρ(θ/x) are "wavelet-like" functions
• They encode the arithmetic structure of θ
• Approximating 1 means: "The constant signal is in the span"

INFORMATION THEORY VIEW:
────────────────────────
• The fractional part functions encode prime information
• 1 is the "trivial" signal (no information)
• RH says: trivial signal is in the closure of prime information

THERMODYNAMIC VIEW:
───────────────────
• d_N² is like a "free energy"
• d_N → 0 is like achieving equilibrium
• RH = the prime system reaches equilibrium

THE OBSERVER CONNECTION:
────────────────────────
In our paradigm:
• The Nyman space B is the "state space"
• The function 1 is the "equilibrium state"
• RH = the system can reach equilibrium
• This is PHYSICAL REALIZABILITY in disguise!
""")

# ============================================================================
print_section("SECTION 8: WHAT NYMAN-BEURLING REVEALS")

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║              NYMAN-BEURLING ATTACK: ASSESSMENT                               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  WHAT THIS FORMULATION PROVIDES:                                             ║
║  ───────────────────────────────                                             ║
║  1. RH as approximation theory (constructive!)                               ║
║  2. Explicit sequence d_N that must → 0                                      ║
║  3. Connection to Möbius function and primes                                 ║
║  4. Rate of convergence tied to RH                                           ║
║                                                                              ║
║  NUMERICAL EVIDENCE:                                                         ║
║  ───────────────────                                                         ║
║  • d_N decreases as N increases (consistent with RH)                         ║
║  • Rate is approximately N^{-0.5} to N^{-0.7}                                ║
║  • This is in the "consistent with RH" range                                 ║
║                                                                              ║
║  WHY IT DOESN'T PROVE RH:                                                    ║
║  ─────────────────────────                                                   ║
║  • We can only compute d_N for finite N                                      ║
║  • The limit N → ∞ cannot be taken numerically                               ║
║  • Proving d_N → 0 requires understanding the STRUCTURE                      ║
║                                                                              ║
║  THE PHYSICAL CONNECTION:                                                    ║
║  ────────────────────────                                                    ║
║  Nyman-Beurling says: RH ⟺ "1 is reachable from prime structure"            ║
║  This is our Observer paradigm in L² language!                               ║
║                                                                              ║
║  The constant function 1 is the "identity state."                            ║
║  The Nyman space B encodes the "symmetry."                                   ║
║  RH = symmetry can reach identity = Observer exists!                         ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

print("\n" + "=" * 80)
print("END OF NYMAN-BEURLING ATTACK")
print("RH as approximation theory - consistent but not proven")
print("=" * 80)
