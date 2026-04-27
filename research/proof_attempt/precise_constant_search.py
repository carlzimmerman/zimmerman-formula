"""
PRECISE CONSTANT SEARCH FOR RH
==============================

Like we found a₀ = H₀ / 5.78881 connecting to Friedman equation,
let's search for EXACT matches between RH quantities and
known mathematical constants.

The key is computing quantities with HIGH PRECISION and looking
for matches to known values from number theory.

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from sympy import factorint, primerange
from collections import defaultdict
from fractions import Fraction
import math

print("=" * 80)
print("PRECISE CONSTANT SEARCH FOR RIEMANN HYPOTHESIS")
print("=" * 80)

# =============================================================================
# KNOWN MATHEMATICAL CONSTANTS (high precision)
# =============================================================================

KNOWN_CONSTANTS = {
    # Basic
    'pi': 3.14159265358979323846,
    'e': 2.71828182845904523536,
    'phi': 1.61803398874989484820,  # Golden ratio
    'sqrt(2)': 1.41421356237309504880,
    'sqrt(3)': 1.73205080756887729353,
    'sqrt(5)': 2.23606797749978969641,

    # Logarithms
    'ln(2)': 0.69314718055994530942,
    'ln(3)': 1.09861228866810969140,
    'ln(10)': 2.30258509299404568402,
    'log10(2)': 0.30102999566398119521,

    # Euler-Mascheroni
    'gamma': 0.57721566490153286061,
    '1-gamma': 0.42278433509846713939,
    'exp(gamma)': 1.78107241799019798524,
    'exp(-gamma)': 0.56145948356651485648,

    # Zeta values
    'zeta(2)': 1.64493406684822643647,  # pi^2/6
    'zeta(3)': 1.20205690315959428540,  # Apéry
    'zeta(4)': 1.08232323371113819152,  # pi^4/90
    'zeta(5)': 1.03692775514336992633,

    # Reciprocal zeta
    '1/zeta(2)': 0.60792710185402662866,  # 6/pi^2 = P(squarefree)
    '1/zeta(3)': 0.83190737258070746868,
    '1/zeta(4)': 0.92393284867396889021,

    # Mertens/Prime-related
    'M_Mertens': 0.26149721284764278376,  # Meissel-Mertens B
    'M_1': 0.57721566490153286061 + 0.26149721284764278376,  # gamma + B
    'C_twin': 0.66016181584686957392,  # Twin prime constant

    # Other
    'Catalan': 0.91596559417721901505,
    'Khinchin': 2.68545200106530644531,
    'Glaisher': 1.28242712910062263688,
    'Omega': 0.56714329040978387300,  # Lambert W at 1
    'Soldner': 1.45136923488338105029,  # Ramanujan-Soldner

    # Simple fractions
    '1/3': 0.33333333333333333333,
    '2/3': 0.66666666666666666667,
    '1/4': 0.25,
    '3/4': 0.75,
    '3/8': 0.375,
    '5/8': 0.625,
    '1/5': 0.2,
    '2/5': 0.4,
    '3/5': 0.6,
    '4/5': 0.8,
    '1/6': 0.16666666666666666667,
    '5/6': 0.83333333333333333333,
    '1/7': 0.14285714285714285714,
    '2/7': 0.28571428571428571429,
    '3/7': 0.42857142857142857143,
    '1/e': 0.36787944117144232160,
    '1-1/e': 0.63212055882855767840,
    '1-2/e': 0.26424088234289464680,
    '2/e': 0.73575911765710535320,
    '1/pi': 0.31830988618379067154,
    '2/pi': 0.63661977236758134308,
    '4/pi': 1.27323954473516268615,

    # Combinations
    'pi/e': 1.15572734979092171791,
    'e/pi': 0.86525597943226508722,
    'pi*e': 8.53973422267356706546,
    'pi+e': 5.85987448204883847382,
    'pi-e': 0.42331082513074800310,
    'ln(pi)': 1.14472988584940017415,
    'ln(2)/2': 0.34657359027997265471,
    'ln(3)/2': 0.54930614433405484570,
    'gamma/2': 0.28860783245076643030,
    'pi/4': 0.78539816339744830962,
    'pi/6': 0.52359877559829887308,
    'sqrt(pi)': 1.77245385090551602730,
    '1/sqrt(2)': 0.70710678118654752440,
    '1/sqrt(3)': 0.57735026918962576451,
    '1/sqrt(pi)': 0.56418958354775628695,
    '2*gamma': 1.15443132980306572121,
    'gamma^2': 0.33317792683698080261,
    'e^(-1/e)': 0.69220062755534635387,

    # Number theoretic
    'A': 0.37395581361920228805,  # Artin's constant
    'A_EM': 1.45136923488338105029,  # Erdos-Borwein constant
    'K': 0.76422365358922066299,  # Landau-Ramanujan constant
    'B_L': 0.26149721284764278376,  # Meissel-Mertens constant
    'delta': 0.00000000000000000000,  # de Bruijn-Newman constant (now proven = 0)
}

# =============================================================================
# COMPUTE RH QUANTITIES WITH HIGH PRECISION
# =============================================================================

print("\n[1/4] Computing RH quantities with high precision...")

MAX_N = 500000
primes = list(primerange(2, MAX_N))

# Precompute
factorizations = {}
for n in range(1, MAX_N + 1):
    if n == 1:
        factorizations[n] = {}
    else:
        factorizations[n] = factorint(n)

def is_squarefree(n):
    return all(e == 1 for e in factorizations[n].values())

def omega(n):
    return len(factorizations[n])

sqfree = [(n, omega(n)) for n in range(1, MAX_N + 1) if is_squarefree(n)]
print(f"  Found {len(sqfree)} squarefree numbers up to {MAX_N}")

def compute_precise_quantities(x):
    """Compute RH quantities with high precision."""
    S_w = defaultdict(int)
    for n, w in sqfree:
        if n <= x:
            S_w[w] += 1

    Q = sum(S_w.values())
    M = sum((-1)**w * S_w[w] for w in S_w)

    omega_vals = [w for n, w in sqfree if n <= x]
    lam = np.log(np.log(x))
    mean_omega = np.mean(omega_vals)
    var_omega = np.var(omega_vals)

    # Key ratios
    var_over_lambda = var_omega / lam
    mean_over_lambda = mean_omega / lam

    # Parity
    P_even = sum(S_w[w] for w in S_w if w % 2 == 0) / Q
    P_odd = sum(S_w[w] for w in S_w if w % 2 == 1) / Q
    parity_diff = P_even - P_odd

    # E[(-1)^omega]
    E_alt = M / Q

    # Root distance
    max_w = max(S_w.keys())
    coeffs = [S_w.get(w, 0) for w in range(max_w + 1)]
    roots = np.roots(coeffs[::-1])
    nearest_root = min(roots, key=lambda r: abs(r - (-1)))
    root_dist = abs(nearest_root - (-1))

    # G'(-1) / Q
    G_prime = sum(w * S_w[w] * ((-1)**(w-1)) for w in S_w)
    G_prime_over_Q = G_prime / Q

    return {
        'x': x,
        'Q': Q,
        'M': M,
        'var_over_lambda': var_over_lambda,
        'mean_over_lambda': mean_over_lambda,
        'lambda': lam,
        'P_even': P_even,
        'P_odd': P_odd,
        'parity_diff': parity_diff,
        'E_alt': E_alt,
        'root_dist': root_dist,
        'G_prime_over_Q': G_prime_over_Q,
        'M_over_sqrt_x': abs(M) / np.sqrt(x),
        'Q_over_x': Q / x,
    }

# Compute at multiple x
x_values = [10000, 50000, 100000, 200000, 300000, 400000, 500000]
data = []
for x in x_values:
    if x <= MAX_N:
        d = compute_precise_quantities(x)
        data.append(d)
        print(f"  x = {x}: Var(ω)/λ = {d['var_over_lambda']:.8f}")

# =============================================================================
# SEARCH FOR EXACT MATCHES
# =============================================================================

print("\n[2/4] Searching for exact matches to known constants...")

def find_matches(value, name, tolerance=0.001):
    """Find known constants matching value within tolerance."""
    matches = []

    for const_name, const_value in KNOWN_CONSTANTS.items():
        if const_value == 0:
            continue

        # Direct match
        diff = abs(value - const_value)
        if diff < tolerance * abs(const_value):
            matches.append({
                'formula': const_name,
                'value': const_value,
                'diff': diff,
                'rel_error': diff / abs(const_value)
            })

        # Ratio to simple numbers
        for mult in [2, 3, 4, 5, 6, 7, 8, 9, 10]:
            if abs(value * mult - const_value) < tolerance * abs(const_value):
                matches.append({
                    'formula': f"{const_name}/{mult}",
                    'value': const_value / mult,
                    'diff': abs(value - const_value / mult),
                    'rel_error': abs(value - const_value / mult) / abs(const_value / mult)
                })
            if abs(value / mult - const_value) < tolerance * abs(const_value):
                matches.append({
                    'formula': f"{mult}*{const_name}",
                    'value': const_value * mult,
                    'diff': abs(value - const_value * mult),
                    'rel_error': abs(value - const_value * mult) / abs(const_value * mult)
                })

    # Product of two constants
    const_names = list(KNOWN_CONSTANTS.keys())
    for i, c1 in enumerate(const_names):
        for c2 in const_names[i+1:]:
            v1, v2 = KNOWN_CONSTANTS[c1], KNOWN_CONSTANTS[c2]
            if v1 == 0 or v2 == 0:
                continue

            # c1 * c2
            prod = v1 * v2
            if abs(value - prod) < tolerance * abs(prod):
                matches.append({
                    'formula': f"{c1}*{c2}",
                    'value': prod,
                    'diff': abs(value - prod),
                    'rel_error': abs(value - prod) / abs(prod)
                })

            # c1 / c2
            ratio = v1 / v2
            if abs(value - ratio) < tolerance * abs(ratio):
                matches.append({
                    'formula': f"{c1}/{c2}",
                    'value': ratio,
                    'diff': abs(value - ratio),
                    'rel_error': abs(value - ratio) / abs(ratio)
                })

    matches.sort(key=lambda m: m['rel_error'])
    return matches[:10]

# Quantities to search
quantities_to_search = {
    'Var(ω)/λ (at x=500000)': data[-1]['var_over_lambda'],
    'E[ω]/λ (at x=500000)': data[-1]['mean_over_lambda'],
    'Q/x (at x=500000)': data[-1]['Q_over_x'],
    'P_even (at x=500000)': data[-1]['P_even'],
    '|G\'(-1)|/Q (at x=500000)': abs(data[-1]['G_prime_over_Q']),
}

print("\nSearching for matches:")
all_findings = {}
for name, value in quantities_to_search.items():
    print(f"\n  {name} = {value:.10f}")
    matches = find_matches(value, name, tolerance=0.01)
    all_findings[name] = matches
    if matches:
        for m in matches[:3]:
            print(f"    ≈ {m['formula']} = {m['value']:.10f} (error {m['rel_error']*100:.4f}%)")
    else:
        print(f"    No close matches found")

# =============================================================================
# DEEP SEARCH FOR SCALING RELATIONSHIPS
# =============================================================================

print("\n[3/4] Deep search for scaling relationships...")

# Test various scalings
print("\n  Testing: root_dist * x^α for various α")
root_dists = np.array([d['root_dist'] for d in data])
x_arr = np.array([d['x'] for d in data])

for alpha in [0.3, 0.4, 0.45, 0.5, 0.55, 0.6]:
    scaled = root_dists * (x_arr ** alpha)
    cv = np.std(scaled) / np.mean(scaled)
    print(f"    α = {alpha}: mean = {np.mean(scaled):.6f}, CV = {cv:.4f}")
    if cv < 0.2:
        # This is promising - search for the constant
        print(f"      STABLE! Searching for constant match...")
        matches = find_matches(np.mean(scaled), f"root_dist*x^{alpha}", tolerance=0.02)
        if matches:
            print(f"      ≈ {matches[0]['formula']} (error {matches[0]['rel_error']*100:.3f}%)")

# Test |M| scalings
print("\n  Testing: |M| / x^α for various α")
M_arr = np.array([abs(d['M']) for d in data])

for alpha in [0.2, 0.25, 0.3, 0.35, 0.4, 0.5]:
    scaled = M_arr / (x_arr ** alpha)
    cv = np.std(scaled) / np.mean(scaled)
    print(f"    α = {alpha}: mean = {np.mean(scaled):.6f}, CV = {cv:.4f}")

# =============================================================================
# EXTRAPOLATION OF Var(ω)/λ
# =============================================================================

print("\n[4/4] Extrapolating Var(ω)/λ to infinity...")

# Fit Var(ω)/λ = A + B/log(x) + C/log(x)^2
from scipy.optimize import curve_fit

def model1(x, A, B):
    return A + B / np.log(x)

def model2(x, A, B, C):
    return A + B / np.log(x) + C / (np.log(x)**2)

var_ratios = np.array([d['var_over_lambda'] for d in data])

try:
    popt1, _ = curve_fit(model1, x_arr, var_ratios)
    A1, B1 = popt1
    print(f"\n  Model 1: Var(ω)/λ = A + B/log(x)")
    print(f"    A = {A1:.10f} (limiting value)")
    print(f"    B = {B1:.6f}")

    # Search for A in known constants
    print(f"    Searching for A = {A1:.8f}...")
    matches = find_matches(A1, "A", tolerance=0.02)
    if matches:
        for m in matches[:3]:
            print(f"      ≈ {m['formula']} = {m['value']:.10f} (error {m['rel_error']*100:.4f}%)")
except Exception as e:
    print(f"  Model 1 fit failed: {e}")

try:
    popt2, _ = curve_fit(model2, x_arr, var_ratios, p0=[0.4, -0.5, 0.1])
    A2, B2, C2 = popt2
    print(f"\n  Model 2: Var(ω)/λ = A + B/log(x) + C/log(x)^2")
    print(f"    A = {A2:.10f} (limiting value)")
    print(f"    B = {B2:.6f}")
    print(f"    C = {C2:.6f}")

    # Search for A in known constants
    print(f"    Searching for A = {A2:.8f}...")
    matches = find_matches(A2, "A", tolerance=0.02)
    if matches:
        for m in matches[:3]:
            print(f"      ≈ {m['formula']} = {m['value']:.10f} (error {m['rel_error']*100:.4f}%)")
except Exception as e:
    print(f"  Model 2 fit failed: {e}")

# =============================================================================
# KEY FINDING: CHECK SPECIFIC VALUES
# =============================================================================

print("\n" + "=" * 80)
print("KEY FINDINGS")
print("=" * 80)

# Check if Var(ω)/λ → 1 - 1/sqrt(e) = 1 - e^{-0.5}
target1 = 1 - np.exp(-0.5)
print(f"\n1. Is Var(ω)/λ → 1 - e^(-0.5) = {target1:.8f}?")
print(f"   Current value at x=500000: {var_ratios[-1]:.8f}")
print(f"   Difference: {var_ratios[-1] - target1:.8f}")

# Check 3/8
target2 = 3/8
print(f"\n2. Is Var(ω)/λ → 3/8 = {target2:.8f}?")
print(f"   Current value at x=500000: {var_ratios[-1]:.8f}")
print(f"   Difference: {var_ratios[-1] - target2:.8f}")

# Check 1/e
target3 = 1/np.e
print(f"\n3. Is Var(ω)/λ → 1/e = {target3:.8f}?")
print(f"   Current value at x=500000: {var_ratios[-1]:.8f}")
print(f"   Difference: {var_ratios[-1] - target3:.8f}")

# Check gamma - 1/4
target4 = 0.5772156649 - 0.25
print(f"\n4. Is Var(ω)/λ → γ - 1/4 = {target4:.8f}?")
print(f"   Current value at x=500000: {var_ratios[-1]:.8f}")
print(f"   Difference: {var_ratios[-1] - target4:.8f}")

# Check if limiting value might be special
print(f"\n5. Extrapolated limiting value from fit:")
if 'A1' in dir():
    print(f"   Model 1: A = {A1:.10f}")

    # Check against many known constants
    best_match = None
    best_diff = float('inf')
    for name, val in KNOWN_CONSTANTS.items():
        diff = abs(A1 - val)
        if diff < best_diff:
            best_diff = diff
            best_match = (name, val)

    print(f"   Closest known constant: {best_match[0]} = {best_match[1]:.10f}")
    print(f"   Difference: {best_diff:.10f}")

# =============================================================================
# SEARCH FOR THE FRIEDMAN-LIKE CONNECTION
# =============================================================================

print("\n" + "=" * 80)
print("SEARCHING FOR EXACT NUMERICAL CONNECTIONS")
print("=" * 80)

# Like a₀ = H₀ / 5.78881 from Friedman, search for RH connections
print("\nSearching for patterns like a₀ = H₀ / 5.78881...")

# Key quantity: the extrapolated limit of Var(ω)/λ
if 'A1' in dir():
    limit_val = A1

    print(f"\nTarget: Var(ω)/λ limit = {limit_val:.10f}")

    # Search for simple expressions
    print("\nTrying simple expressions:")

    # 1 - k/pi for various k
    for k in range(1, 10):
        expr_val = 1 - k / np.pi
        if 0 < expr_val < 1:
            diff = abs(limit_val - expr_val)
            if diff < 0.01:
                print(f"  1 - {k}/π = {expr_val:.8f} (diff = {diff:.6f})")

    # k/(k+1) fractions
    for k in range(1, 20):
        expr_val = k / (k + 1)
        diff = abs(limit_val - expr_val)
        if diff < 0.01:
            print(f"  {k}/{k+1} = {expr_val:.8f} (diff = {diff:.6f})")

    # 1 - 1/k for various k
    for k in [np.e, np.pi, 2, 3, 4, 5]:
        expr_val = 1 - 1/k
        diff = abs(limit_val - expr_val)
        if diff < 0.02:
            print(f"  1 - 1/{k:.4f} = {expr_val:.8f} (diff = {diff:.6f})")

    # gamma combinations
    gamma = 0.5772156649
    for num in range(-5, 6):
        for den in range(1, 10):
            expr_val = gamma + num/den
            if 0.3 < expr_val < 0.5:
                diff = abs(limit_val - expr_val)
                if diff < 0.01:
                    sign = '+' if num >= 0 else ''
                    print(f"  γ {sign}{num}/{den} = {expr_val:.8f} (diff = {diff:.6f})")

# =============================================================================
# FINAL CHECK: ROOT DISTANCE CONNECTION
# =============================================================================

print("\n" + "=" * 80)
print("ROOT DISTANCE SCALING ANALYSIS")
print("=" * 80)

# If root_dist ~ C * x^{-1/2}, find C
print("\nFitting root_dist = C * x^α")
from scipy.optimize import curve_fit

def power_law(x, C, alpha):
    return C * x ** alpha

try:
    popt, _ = curve_fit(power_law, x_arr, root_dists, p0=[1, -0.5])
    C_fit, alpha_fit = popt
    print(f"  C = {C_fit:.8f}")
    print(f"  α = {alpha_fit:.8f}")
    print(f"  (RH predicts α = -0.5, we found α = {alpha_fit:.4f})")

    if abs(alpha_fit + 0.5) < 0.1:
        print(f"\n  This is consistent with RH!")
        print(f"  The constant C = {C_fit:.8f}")

        # Search for C
        print(f"  Searching for C in known constants...")
        matches = find_matches(C_fit, "C", tolerance=0.02)
        if matches:
            for m in matches[:3]:
                print(f"    ≈ {m['formula']} = {m['value']:.8f} (error {m['rel_error']*100:.3f}%)")
except Exception as e:
    print(f"  Fit failed: {e}")

print("\n" + "=" * 80)
print("PRECISE CONSTANT SEARCH COMPLETE")
print("=" * 80)
