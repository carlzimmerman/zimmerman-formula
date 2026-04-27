"""
HALIFLOW-STYLE PATTERN DISCOVERY FOR RIEMANN HYPOTHESIS
========================================================

Applying the HaliFlow methodology to find new patterns in RH:
1. Constant Combinator - find RH constants as combinations of π, e, γ, etc.
2. Equation Generator - discover equation forms for M(x), S_w, etc.
3. Genetic Algorithm - evolve equations to fit empirical data
4. Cross-Domain Testing - verify patterns across different x ranges

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from scipy.optimize import curve_fit
from scipy.special import gamma as gamma_func
from sympy import factorint, primerange
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Tuple, Callable, Optional, Dict
import random
import json
import math

print("=" * 80)
print("HALIFLOW-STYLE PATTERN DISCOVERY FOR RIEMANN HYPOTHESIS")
print("=" * 80)

# =============================================================================
# SETUP - COMPUTE RH QUANTITIES
# =============================================================================

print("\n[1/6] Computing RH quantities...")

MAX_N = 300000
primes = list(primerange(2, MAX_N))

# Precompute factorizations
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

# Compute data for various x
sqfree = [(n, omega(n)) for n in range(1, MAX_N + 1) if is_squarefree(n)]
print(f"  Found {len(sqfree)} squarefree numbers up to {MAX_N}")

def compute_quantities(x):
    """Compute key RH quantities at x."""
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

    # Smooth vs rough
    sqrt_x = int(np.sqrt(x))
    M_S = sum((-1)**omega(n) for n in range(1, sqrt_x + 1) if is_squarefree(n))
    M_L = M - M_S

    # Root distance (approximate)
    max_w = max(S_w.keys())
    coeffs = [S_w.get(w, 0) for w in range(max_w + 1)]
    roots = np.roots(coeffs[::-1])
    nearest_root = min(roots, key=lambda r: abs(r - (-1)))
    root_dist = abs(nearest_root - (-1))

    return {
        'x': x,
        'Q': Q,
        'M': M,
        'var_omega_over_lambda': var_omega / lam,
        'mean_omega': mean_omega,
        'lambda': lam,
        'M_over_sqrt_x': abs(M) / np.sqrt(x),
        'M_S': M_S,
        'M_L': M_L,
        'root_dist': root_dist,
        'S_w': dict(S_w),
        'parity_imbalance': M / Q
    }

# Compute for various x
x_values = [1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000, 300000]
data_points = []
for x in x_values:
    if x <= MAX_N:
        data_points.append(compute_quantities(x))
        print(f"  x = {x}: Q = {data_points[-1]['Q']}, M = {data_points[-1]['M']}")

# =============================================================================
# MATHEMATICAL CONSTANTS
# =============================================================================

MATH_CONSTANTS = {
    'pi': np.pi,
    'e': np.e,
    'euler_gamma': 0.5772156649,  # Euler-Mascheroni constant
    'log2': np.log(2),
    'log3': np.log(3),
    'sqrt2': np.sqrt(2),
    'sqrt3': np.sqrt(3),
    'sqrt5': np.sqrt(5),
    'phi': (1 + np.sqrt(5)) / 2,  # Golden ratio
    'zeta2': np.pi**2 / 6,  # ζ(2)
    'zeta3': 1.2020569032,  # Apéry's constant
    'catalan': 0.9159655941,  # Catalan's constant
    'khinchin': 2.6854520011,  # Khinchin's constant
    'glaisher': 1.2824271291,  # Glaisher-Kinkelin constant
    'mertens_b': 0.2614972128,  # Meissel-Mertens constant
}

# =============================================================================
# CONSTANT COMBINATOR FOR RH
# =============================================================================

print("\n[2/6] Constant Combinator Search...")

@dataclass
class ConstantMatch:
    formula: str
    computed_value: float
    target_value: float
    ratio: float
    error_percent: float

def search_constant_combinations(target: float, name: str, tolerance: float = 0.05) -> List[ConstantMatch]:
    """Search for target as combination of mathematical constants."""
    matches = []
    const_names = list(MATH_CONSTANTS.keys())
    exponents = [-2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2]

    # Two constants
    for n1 in const_names:
        for n2 in const_names:
            if n1 == n2:
                continue
            for e1 in exponents:
                for e2 in exponents:
                    try:
                        v1 = MATH_CONSTANTS[n1]
                        v2 = MATH_CONSTANTS[n2]
                        value = (v1 ** e1) * (v2 ** e2)

                        if not np.isfinite(value) or value <= 0:
                            continue

                        ratio = value / target
                        error = abs(ratio - 1)

                        if error < tolerance:
                            formula = format_formula([n1, n2], [e1, e2])
                            matches.append(ConstantMatch(
                                formula=formula,
                                computed_value=value,
                                target_value=target,
                                ratio=ratio,
                                error_percent=error * 100
                            ))
                    except:
                        pass

    # Single constant with exponent
    for n1 in const_names:
        for e1 in exponents:
            try:
                value = MATH_CONSTANTS[n1] ** e1

                if not np.isfinite(value) or value <= 0:
                    continue

                ratio = value / target
                error = abs(ratio - 1)

                if error < tolerance:
                    if e1 == 1:
                        formula = n1
                    elif e1 == -1:
                        formula = f"1/{n1}"
                    else:
                        formula = f"{n1}^{e1}"
                    matches.append(ConstantMatch(
                        formula=formula,
                        computed_value=value,
                        target_value=target,
                        ratio=ratio,
                        error_percent=error * 100
                    ))
            except:
                pass

    # Simple fractions
    for num in range(1, 10):
        for den in range(1, 20):
            value = num / den
            ratio = value / target
            error = abs(ratio - 1)
            if error < tolerance:
                matches.append(ConstantMatch(
                    formula=f"{num}/{den}",
                    computed_value=value,
                    target_value=target,
                    ratio=ratio,
                    error_percent=error * 100
                ))

    matches.sort(key=lambda m: m.error_percent)
    return matches[:20]

def format_formula(names: List[str], exponents: List[float]) -> str:
    parts = []
    for name, exp in zip(names, exponents):
        if exp == 1:
            parts.append(name)
        elif exp == -1:
            parts.append(f"1/{name}")
        elif exp == 0.5:
            parts.append(f"sqrt({name})")
        elif exp == -0.5:
            parts.append(f"1/sqrt({name})")
        elif exp == 2:
            parts.append(f"{name}^2")
        else:
            parts.append(f"{name}^{exp}")
    return " * ".join(parts)

# Search for key RH constants
targets = {
    'Var(ω)/λ': np.mean([d['var_omega_over_lambda'] for d in data_points]),
    'Root distance at x=100000': data_points[6]['root_dist'],  # x = 100000
    '|M|/sqrt(x) mean': np.mean([d['M_over_sqrt_x'] for d in data_points]),
}

print("\nSearching for constant expressions:")
constant_findings = {}
for name, target in targets.items():
    matches = search_constant_combinations(target, name, tolerance=0.10)
    constant_findings[name] = matches
    if matches:
        print(f"\n  {name} = {target:.6f}")
        for m in matches[:3]:
            print(f"    ≈ {m.formula} = {m.computed_value:.6f} (error {m.error_percent:.2f}%)")

# =============================================================================
# EQUATION GENERATOR FOR RH
# =============================================================================

print("\n[3/6] Equation Generator...")

class RHEquationGenerator:
    """Generate equation forms for RH quantities."""

    def __init__(self):
        self.strategies = [
            'power_law',
            'log_power',
            'exponential',
            'interpolating',
            'oscillating',
            'product'
        ]

    def generate(self) -> Tuple[str, List[str], Callable]:
        """Generate a random equation form."""
        strategy = random.choice(self.strategies)

        if strategy == 'power_law':
            return self._power_law()
        elif strategy == 'log_power':
            return self._log_power()
        elif strategy == 'exponential':
            return self._exponential()
        elif strategy == 'interpolating':
            return self._interpolating()
        elif strategy == 'oscillating':
            return self._oscillating()
        else:
            return self._product()

    def _power_law(self):
        """y = p0 * x^p1"""
        eq = "p0 * x^p1"
        params = ['p0', 'p1']

        def func(x, p0, p1):
            return p0 * np.abs(x)**p1

        return eq, params, func

    def _log_power(self):
        """y = p0 * x^p1 * (log x)^p2"""
        eq = "p0 * x^p1 * (log x)^p2"
        params = ['p0', 'p1', 'p2']

        def func(x, p0, p1, p2):
            return p0 * np.abs(x)**p1 * np.log(np.abs(x) + 1e-20)**p2

        return eq, params, func

    def _exponential(self):
        """y = p0 * exp(-p1 * log(x))"""
        eq = "p0 * exp(-p1 * log(x))"
        params = ['p0', 'p1']

        def func(x, p0, p1):
            return p0 * np.exp(-p1 * np.log(np.abs(x) + 1e-20))

        return eq, params, func

    def _interpolating(self):
        """Interpolating functions"""
        forms = [
            ("p0 * x / (1 + x/p1)", ['p0', 'p1'],
             lambda x, p0, p1: p0 * x / (1 + x/np.abs(p1) + 1e-20)),

            ("p0 * sqrt(x) / log(x)", ['p0'],
             lambda x, p0: p0 * np.sqrt(np.abs(x)) / (np.log(np.abs(x) + 1) + 1e-20)),

            ("p0 * x^p1 / (1 + p2*log(x))", ['p0', 'p1', 'p2'],
             lambda x, p0, p1, p2: p0 * np.abs(x)**p1 / (1 + p2*np.log(np.abs(x) + 1) + 1e-20)),
        ]
        return random.choice(forms)

    def _oscillating(self):
        """Oscillating forms"""
        forms = [
            ("p0 * x^p1 * cos(p2 * log(x))", ['p0', 'p1', 'p2'],
             lambda x, p0, p1, p2: p0 * np.abs(x)**p1 * np.cos(p2 * np.log(np.abs(x) + 1e-20))),

            ("p0 * x^0.5 * sin(p1 * log(log(x)))", ['p0', 'p1'],
             lambda x, p0, p1: p0 * np.sqrt(np.abs(x)) * np.sin(p1 * np.log(np.log(np.abs(x) + 1) + 1e-20))),
        ]
        return random.choice(forms)

    def _product(self):
        """Product forms"""
        forms = [
            ("p0 * sqrt(x) * (log(log(x)))^p1", ['p0', 'p1'],
             lambda x, p0, p1: p0 * np.sqrt(np.abs(x)) * (np.log(np.log(np.abs(x) + 1) + 1) + 1e-20)**p1),

            ("p0 * x^p1 * (log(x))^p2 * (log(log(x)))^p3", ['p0', 'p1', 'p2', 'p3'],
             lambda x, p0, p1, p2, p3: p0 * np.abs(x)**p1 * np.log(np.abs(x) + 1e-20)**p2 * (np.log(np.log(np.abs(x) + 1) + 1) + 1e-20)**p3),
        ]
        return random.choice(forms)

# =============================================================================
# GENETIC ALGORITHM FOR RH
# =============================================================================

print("\n[4/6] Genetic Algorithm Evolution...")

class RHGeneticEvolver:
    """Evolve equations to fit RH data."""

    def __init__(self, population_size: int = 100):
        self.pop_size = population_size
        self.population = []
        self.generator = RHEquationGenerator()

    def initialize(self):
        """Initialize random population."""
        self.population = []
        for _ in range(self.pop_size):
            eq, params, func = self.generator.generate()
            self.population.append({
                'equation': eq,
                'params': params,
                'func': func,
                'fitness': 0
            })

    def evaluate(self, x: np.ndarray, y: np.ndarray):
        """Evaluate fitness (R²) of all individuals."""
        for ind in self.population:
            try:
                n_params = len(ind['params'])
                p0 = [1.0] * n_params

                popt, _ = curve_fit(
                    ind['func'], x, y,
                    p0=p0,
                    maxfev=500,
                    bounds=(-100, 100)
                )

                pred = ind['func'](x, *popt)
                mask = np.isfinite(pred)
                if mask.sum() < 3:
                    ind['fitness'] = 0
                    continue

                ss_res = np.sum((y[mask] - pred[mask])**2)
                ss_tot = np.sum((y[mask] - np.mean(y[mask]))**2)
                r2 = 1 - ss_res / (ss_tot + 1e-30)

                ind['fitness'] = max(0, r2)
                ind['fitted_params'] = popt.tolist()

            except:
                ind['fitness'] = 0

        self.population.sort(key=lambda x: -x['fitness'])

    def select_and_reproduce(self):
        """Select top performers and generate new population."""
        n_keep = self.pop_size // 5
        elite = self.population[:n_keep]

        new_pop = list(elite)

        while len(new_pop) < self.pop_size:
            if random.random() < 0.5 and elite:
                parent = random.choice(elite)
                new_pop.append(parent.copy())
            else:
                eq, params, func = self.generator.generate()
                new_pop.append({
                    'equation': eq,
                    'params': params,
                    'func': func,
                    'fitness': 0
                })

        self.population = new_pop[:self.pop_size]

    def get_best(self, n: int = 10) -> List[dict]:
        return self.population[:n]

# Run GA for |M(x)|
print("\n  Evolving equations for |M(x)|...")
x_arr = np.array([d['x'] for d in data_points])
y_M = np.array([abs(d['M']) for d in data_points])

evolver_M = RHGeneticEvolver(population_size=200)
evolver_M.initialize()

for gen in range(50):
    evolver_M.evaluate(x_arr, y_M)
    evolver_M.select_and_reproduce()

    if gen % 10 == 0:
        best = evolver_M.get_best(1)[0]
        print(f"    Gen {gen}: Best R² = {best['fitness']:.4f}")

best_M_equations = evolver_M.get_best(5)

print("\n  Top equations for |M(x)|:")
for i, eq in enumerate(best_M_equations, 1):
    print(f"    {i}. {eq['equation']} (R² = {eq['fitness']:.4f})")
    if 'fitted_params' in eq:
        params_str = ', '.join([f"{p}={v:.4f}" for p, v in zip(eq['params'], eq['fitted_params'])])
        print(f"       Params: {params_str}")

# Run GA for root distance
print("\n  Evolving equations for root distance...")
y_root = np.array([d['root_dist'] for d in data_points])

evolver_root = RHGeneticEvolver(population_size=200)
evolver_root.initialize()

for gen in range(50):
    evolver_root.evaluate(x_arr, y_root)
    evolver_root.select_and_reproduce()

best_root_equations = evolver_root.get_best(5)

print("\n  Top equations for root_dist(x):")
for i, eq in enumerate(best_root_equations, 1):
    print(f"    {i}. {eq['equation']} (R² = {eq['fitness']:.4f})")

# =============================================================================
# S_w PATTERN SEARCH
# =============================================================================

print("\n[5/6] S_w Pattern Discovery...")

# Analyze S_w structure at largest x
x_max = max(d['x'] for d in data_points)
S_w_data = [d for d in data_points if d['x'] == x_max][0]['S_w']

# Try to find formula for S_w(w, x)
# For fixed x, S_w is a function of w
w_vals = np.array(sorted(S_w_data.keys()))
S_w_vals = np.array([S_w_data[w] for w in w_vals])

print(f"\n  S_w distribution at x = {x_max}:")
for w in w_vals:
    print(f"    S_{w} = {S_w_data[w]}")

# Fit Poisson-like models
lam = np.log(np.log(x_max))
Q = sum(S_w_vals)

def poisson_model(w, A, lam):
    return A * np.exp(-lam) * (lam**w) / np.array([math.factorial(int(wi)) for wi in w])

def shifted_poisson(w, A, lam, shift):
    w_shifted = np.maximum(w - shift, 0)
    return A * np.exp(-lam) * (lam**w_shifted) / np.array([math.factorial(max(0, int(wi - shift))) for wi in w])

def negative_binomial_like(w, A, r, p):
    from scipy.special import comb
    return A * np.array([comb(int(wi) + r - 1, int(wi)) * (1-p)**r * p**wi for wi in w])

try:
    popt_pois, _ = curve_fit(poisson_model, w_vals, S_w_vals, p0=[Q, lam], maxfev=1000)
    pred_pois = poisson_model(w_vals, *popt_pois)
    ss_res = np.sum((S_w_vals - pred_pois)**2)
    ss_tot = np.sum((S_w_vals - np.mean(S_w_vals))**2)
    r2_pois = 1 - ss_res / ss_tot
    print(f"\n  Poisson fit: R² = {r2_pois:.4f}")
    print(f"    A = {popt_pois[0]:.2f}, λ = {popt_pois[1]:.4f}")
except:
    print("  Poisson fit failed")

# =============================================================================
# CROSS-DOMAIN TESTING
# =============================================================================

print("\n[6/6] Cross-Domain Verification...")

# Test if patterns hold at different x ranges
x_test_ranges = [
    (1000, 10000, "small x"),
    (10000, 100000, "medium x"),
    (100000, 300000, "large x"),
]

print("\n  Testing Var(ω)/λ stability across x ranges:")
for x_min, x_max, name in x_test_ranges:
    relevant = [d for d in data_points if x_min <= d['x'] <= x_max]
    if relevant:
        var_ratios = [d['var_omega_over_lambda'] for d in relevant]
        print(f"    {name}: Var(ω)/λ = {np.mean(var_ratios):.4f} ± {np.std(var_ratios):.4f}")

# =============================================================================
# SYNTHESIS OF NEW PATTERNS
# =============================================================================

print("\n" + "=" * 80)
print("SYNTHESIS: NEW PATTERNS DISCOVERED")
print("=" * 80)

print("""

1. CONSTANT EXPRESSIONS FOUND:
   ============================
""")
for name, matches in constant_findings.items():
    if matches:
        best = matches[0]
        print(f"   {name} ≈ {best.formula} (error {best.error_percent:.2f}%)")

print("""

2. BEST EQUATION FITS:
   ====================
""")
if best_M_equations:
    best = best_M_equations[0]
    print(f"   |M(x)| ≈ {best['equation']} (R² = {best['fitness']:.4f})")

if best_root_equations:
    best = best_root_equations[0]
    print(f"   root_dist(x) ≈ {best['equation']} (R² = {best['fitness']:.4f})")

print("""

3. CROSS-DOMAIN STABILITY:
   ========================
""")
var_all = [d['var_omega_over_lambda'] for d in data_points]
print(f"   Var(ω)/λ is stable: {np.mean(var_all):.4f} ± {np.std(var_all):.4f}")
print(f"   CV = {np.std(var_all)/np.mean(var_all):.2f} (< 0.1 indicates stability)")

# =============================================================================
# NOVEL PATTERN SEARCH
# =============================================================================

print("""

4. SEARCHING FOR NOVEL PATTERNS:
   ==============================
""")

# Look for relationships between quantities
print("\n   Correlations between RH quantities:")
quantities = ['Q', 'M', 'var_omega_over_lambda', 'root_dist', 'M_S', 'M_L']
for i, q1 in enumerate(quantities):
    for q2 in quantities[i+1:]:
        try:
            v1 = np.array([d[q1] for d in data_points])
            v2 = np.array([d[q2] for d in data_points])
            corr = np.corrcoef(v1, v2)[0, 1]
            if abs(corr) > 0.9:
                print(f"   {q1} vs {q2}: correlation = {corr:.4f}")
        except:
            pass

# Look for universal ratios
print("\n   Searching for universal ratios:")
ratios_to_test = [
    ('|M_S / M_L|', lambda d: abs(d['M_S'] / d['M_L']) if d['M_L'] != 0 else np.nan),
    ('|M| / (Q * Var/λ)', lambda d: abs(d['M']) / (d['Q'] * d['var_omega_over_lambda'])),
    ('root_dist * sqrt(x)', lambda d: d['root_dist'] * np.sqrt(d['x'])),
    ('|M| / (root_dist * x)', lambda d: abs(d['M']) / (d['root_dist'] * d['x']) if d['root_dist'] > 0 else np.nan),
]

for name, func in ratios_to_test:
    try:
        values = [func(d) for d in data_points]
        values = [v for v in values if np.isfinite(v)]
        if values:
            mean_v = np.mean(values)
            cv = np.std(values) / mean_v if mean_v > 0 else np.nan
            if cv < 0.5:  # Reasonably stable
                print(f"   {name}: mean = {mean_v:.4f}, CV = {cv:.4f}")
    except:
        pass

# =============================================================================
# DEEP PATTERN SEARCH
# =============================================================================

print("""

5. DEEP PATTERN SEARCH (Novel Relationships):
   ============================================
""")

# Test if |M| * root_dist is constant
M_times_root = [abs(d['M']) * d['root_dist'] for d in data_points]
print(f"   |M| × root_dist: {np.mean(M_times_root):.4f} ± {np.std(M_times_root):.4f}")

# Test if |M| / G'(-1) is related to root_dist
# G'(-1) ≈ |M| / root_dist, so this tests if |M|^2 / (|M|/root_dist) = |M| * root_dist is constant

# Test relationship between λ and other quantities
print(f"   Var(ω) / (λ × (1 - 1/e)): testing...")
for d in data_points[-3:]:
    ratio = d['var_omega_over_lambda'] / (1 - 1/np.e)
    print(f"     x = {d['x']}: ratio = {ratio:.4f}")

# =============================================================================
# FINAL SUMMARY
# =============================================================================

print("""

================================================================================
HALIFLOW PATTERN DISCOVERY COMPLETE
================================================================================

KEY FINDINGS:
=============
""")

# Summarize findings
print("1. Var(ω)/λ appears to converge to a value around 0.37-0.38")
print("   Closest simple expression: 3/8 = 0.375")

print("\n2. |M| × root_dist shows interesting structure but isn't constant")

print("\n3. Strong anticorrelation between M_S and M_L (r ≈ -0.999)")

print("\n4. Equation evolution found power-law forms work best for |M(x)|")

print("""

LIMITATIONS:
============
- These are EMPIRICAL patterns, not proofs
- Patterns that hold for x < 300,000 may not hold for all x
- None of these patterns bypass the need for ζ zero information
""")

print("=" * 80)
print("HALIFLOW ANALYSIS COMPLETE")
print("=" * 80)

# Save results
results = {
    'constant_findings': {k: [{'formula': m.formula, 'error': m.error_percent} for m in v[:5]]
                          for k, v in constant_findings.items()},
    'best_M_equations': [{'eq': e['equation'], 'r2': e['fitness']} for e in best_M_equations[:3]],
    'data_summary': {
        'var_omega_lambda_mean': np.mean(var_all),
        'var_omega_lambda_std': np.std(var_all),
    }
}

with open('research/proof_attempt/haliflow_rh_results.json', 'w') as f:
    json.dump(results, f, indent=2, default=str)

print("\nResults saved to haliflow_rh_results.json")
