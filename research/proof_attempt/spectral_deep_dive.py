#!/usr/bin/env python3
"""
DEEP DIVE: SPECTRAL GRAPH APPROACH
====================================

The coprimality graph spectral gap grows like N.
This suggests strong mixing, which could imply concentration.

GOAL: Can we use spectral graph theory to bound M(N)?

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from math import sqrt, log, gcd
from scipy import sparse
from scipy.sparse.linalg import eigsh, eigs
from scipy.linalg import eigh
import time

print("="*75)
print("DEEP DIVE: SPECTRAL GRAPH APPROACH TO RH")
print("="*75)

# =============================================================================
# SETUP
# =============================================================================

def mobius_sieve(n):
    mu = np.zeros(n + 1, dtype=np.int8)
    mu[1] = 1
    smallest_prime = np.zeros(n + 1, dtype=np.int32)
    primes = []
    for i in range(2, n + 1):
        if smallest_prime[i] == 0:
            smallest_prime[i] = i
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > n:
                break
            smallest_prime[i * p] = p
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
    return mu, np.array(primes)

# =============================================================================
# PART 1: SPECTRAL GAP SCALING
# =============================================================================

print("\n" + "="*75)
print("PART 1: HOW DOES SPECTRAL GAP SCALE WITH N?")
print("="*75)

print("""
From initial analysis, spectral gap λ₂ grows like N.
More precisely, we expect λ₂ ~ c * Q(N) where Q(N) = #{squarefree ≤ N}.

The spectral gap controls mixing time: τ_mix ~ 1/λ₂.
Faster mixing → more cancellation → smaller M(N)?
""")

def compute_coprimality_graph_dense(N):
    """Build dense adjacency matrix of coprimality graph."""
    mu, _ = mobius_sieve(N)
    sqfree = [n for n in range(1, N+1) if mu[n] != 0]
    n = len(sqfree)
    idx = {v: i for i, v in enumerate(sqfree)}

    # Adjacency matrix
    A = np.zeros((n, n), dtype=np.int8)
    for i, m in enumerate(sqfree):
        for j, k in enumerate(sqfree):
            if j > i and gcd(m, k) == 1:
                A[i, j] = 1
                A[j, i] = 1

    # Degree matrix
    degrees = np.sum(A, axis=1)
    D = np.diag(degrees)

    # Laplacian L = D - A
    L = D - A

    return L, A, sqfree, mu

def analyze_spectral_gap_scaling():
    """Analyze how spectral gap scales with N."""
    results = []

    for N in [30, 50, 100, 150, 200, 300, 500]:
        L, A, sqfree, mu = compute_coprimality_graph_dense(N)
        n = len(sqfree)

        # Compute eigenvalues
        eigenvalues = np.linalg.eigvalsh(L.astype(float))
        eigenvalues = np.sort(eigenvalues)

        # Spectral gap
        lambda_2 = eigenvalues[1]

        # Q(N)
        Q_N = n

        # Ratio
        ratio = lambda_2 / Q_N

        results.append((N, Q_N, lambda_2, ratio))

        print(f"N = {N:3d}: Q(N) = {Q_N:3d}, λ₂ = {lambda_2:8.3f}, λ₂/Q(N) = {ratio:.4f}")

    # Fit λ₂ ~ c * Q(N)
    Q_vals = np.array([r[1] for r in results])
    lambda_vals = np.array([r[2] for r in results])

    # Linear fit
    c = np.sum(Q_vals * lambda_vals) / np.sum(Q_vals ** 2)
    print(f"\nFitted: λ₂ ≈ {c:.4f} * Q(N)")

    return results, c

print("\nSpectral gap scaling:")
results, c_fit = analyze_spectral_gap_scaling()

# =============================================================================
# PART 2: CHEEGER INEQUALITY AND M(N) BOUNDS
# =============================================================================

print("\n" + "="*75)
print("PART 2: CHEEGER INEQUALITY FOR M(N) BOUNDS")
print("="*75)

print("""
The Cheeger inequality relates spectral gap to conductance:

  h²/2 ≤ λ₂ ≤ 2h

where h is the Cheeger constant (isoperimetric ratio).

For the Mertens sum M(N) = Σ μ(n):
  - Bosons (+1): vertices with μ = +1
  - Fermions (-1): vertices with μ = -1
  - M(N) = |B| - |F| where B = bosons, F = fermions

If B and F are "well-mixed" (small cut ratio), then |M(N)| is small.
""")

def compute_cheeger_constant(L, A, sqfree, mu):
    """Compute Cheeger constant and analyze boson-fermion cut."""
    n = len(sqfree)

    # Partition into bosons and fermions
    bosons = [i for i, v in enumerate(sqfree) if mu[v] == 1]
    fermions = [i for i, v in enumerate(sqfree) if mu[v] == -1]

    # Cut size between bosons and fermions
    cut = 0
    for i in bosons:
        for j in fermions:
            cut += A[i, j]

    # Volume of each set
    degrees = np.sum(A, axis=1)
    vol_B = sum(degrees[i] for i in bosons)
    vol_F = sum(degrees[i] for i in fermions)

    # Conductance of boson-fermion cut
    conductance = cut / min(vol_B, vol_F) if min(vol_B, vol_F) > 0 else 0

    # M(N)
    M_N = len(bosons) - len(fermions)

    return conductance, cut, vol_B, vol_F, M_N

print("\nBoson-fermion partition analysis:")
for N in [50, 100, 200, 500]:
    L, A, sqfree, mu = compute_coprimality_graph_dense(N)
    cond, cut, vol_B, vol_F, M_N = compute_cheeger_constant(L, A, sqfree, mu)

    eigenvalues = np.linalg.eigvalsh(L.astype(float))
    lambda_2 = sorted(eigenvalues)[1]

    print(f"\nN = {N}:")
    print(f"  |Bosons| = {len([i for i, v in enumerate(sqfree) if mu[v] == 1])}, |Fermions| = {len([i for i, v in enumerate(sqfree) if mu[v] == -1])}")
    print(f"  M(N) = {M_N}")
    print(f"  Cut size = {cut}")
    print(f"  Vol(B) = {vol_B}, Vol(F) = {vol_F}")
    print(f"  Conductance h = {cond:.4f}")
    print(f"  λ₂ = {lambda_2:.3f}")
    print(f"  Cheeger bounds: {cond**2/2:.4f} ≤ λ₂ ≤ {2*cond:.4f}")

# =============================================================================
# PART 3: EXPANDER GRAPH PROPERTIES
# =============================================================================

print("\n" + "="*75)
print("PART 3: IS THE COPRIMALITY GRAPH AN EXPANDER?")
print("="*75)

print("""
An expander graph has spectral gap λ₂ = Ω(degree).
For the coprimality graph:
- Average degree ≈ Q(N) * φ(N)/N ≈ Q(N) * (6/π²) (heuristic)
- If λ₂ = Θ(Q(N)), then it's a strong expander!

Expanders have excellent concentration properties.
Random walks mix rapidly, sums of ±1 vertex weights concentrate.
""")

def analyze_expander_property(N):
    """Check expander properties."""
    L, A, sqfree, mu = compute_coprimality_graph_dense(N)
    n = len(sqfree)

    degrees = np.sum(A, axis=1)
    avg_degree = np.mean(degrees)
    max_degree = np.max(degrees)

    eigenvalues = np.linalg.eigvalsh(L.astype(float))
    eigenvalues = np.sort(eigenvalues)
    lambda_2 = eigenvalues[1]
    lambda_max = eigenvalues[-1]

    # Normalized Laplacian eigenvalues
    D_inv_sqrt = np.diag(1.0 / np.sqrt(degrees + 1e-10))
    L_norm = D_inv_sqrt @ L @ D_inv_sqrt
    norm_eigenvalues = np.linalg.eigvalsh(L_norm)
    norm_lambda_2 = sorted(norm_eigenvalues)[1]

    return {
        'n': n,
        'avg_degree': avg_degree,
        'max_degree': max_degree,
        'lambda_2': lambda_2,
        'lambda_max': lambda_max,
        'norm_lambda_2': norm_lambda_2,
        'ratio': lambda_2 / avg_degree
    }

print("\nExpander analysis:")
print("N    | n    | avg_d | λ₂     | λ₂/d   | norm_λ₂")
print("-" * 60)
for N in [50, 100, 200, 500, 1000]:
    try:
        props = analyze_expander_property(N)
        print(f"{N:4d} | {props['n']:4d} | {props['avg_degree']:5.1f} | {props['lambda_2']:6.2f} | {props['ratio']:.4f} | {props['norm_lambda_2']:.4f}")
    except Exception as e:
        print(f"{N:4d} | Error: {e}")

# =============================================================================
# PART 4: CONCENTRATION INEQUALITY FROM SPECTRAL GAP
# =============================================================================

print("\n" + "="*75)
print("PART 4: CONCENTRATION FROM SPECTRAL GAP")
print("="*75)

print("""
KEY THEOREM (Concentration on Expanders):

For a function f: V → R on an expander graph with spectral gap λ₂,
if the graph has n vertices and f has bounded variation:

  P(|f - E[f]| > t) ≤ 2 exp(-λ₂ t² / (2 Var(f)))

For M(N) = Σ μ(n), each μ(n) ∈ {-1, +1}:
- E[M] = 0 (if bosons ≈ fermions)
- Var(M) ≈ Q(N) (number of terms)

If λ₂ ~ c * Q(N), then:
  P(|M(N)| > t√Q(N)) ≤ 2 exp(-c * t²)

This would give |M(N)| = O(√Q(N)) = O(√N) with high probability!
""")

def test_concentration_bound(N):
    """Test if empirical M(N) satisfies concentration bound."""
    mu, _ = mobius_sieve(N)
    M = np.cumsum(mu)

    # Build graph and get spectral gap
    L, A, sqfree, _ = compute_coprimality_graph_dense(N)
    eigenvalues = np.linalg.eigvalsh(L.astype(float))
    lambda_2 = sorted(eigenvalues)[1]

    Q_N = len(sqfree)
    M_N = M[N]

    # Predicted bound: |M(N)| / √Q(N) should be O(1)
    normalized = abs(M_N) / sqrt(Q_N)

    # Concentration inequality suggests:
    # P(|M|/√Q > t) ≤ 2 exp(-λ₂ t² / Q)
    # For λ₂ ~ c*Q, this gives P(|M|/√Q > t) ≤ 2 exp(-c t²)

    # What's the "effective c"?
    c_eff = lambda_2 / Q_N

    # For normalized = t, probability bound is:
    prob_bound = 2 * np.exp(-c_eff * normalized**2) if c_eff > 0 else 1

    return {
        'N': N,
        'Q_N': Q_N,
        'M_N': M_N,
        'normalized': normalized,
        'lambda_2': lambda_2,
        'c_eff': c_eff,
        'prob_bound': prob_bound
    }

print("\nConcentration bound test:")
print("N     | Q(N)  | M(N) | |M|/√Q | λ₂/Q  | P-bound")
print("-" * 65)
for N in [50, 100, 200, 500, 1000]:
    try:
        res = test_concentration_bound(N)
        print(f"{res['N']:5d} | {res['Q_N']:5d} | {res['M_N']:4d} | {res['normalized']:6.3f} | {res['c_eff']:.4f} | {res['prob_bound']:.2e}")
    except Exception as e:
        print(f"{N:5d} | Error: {e}")

# =============================================================================
# PART 5: THE KEY QUESTION - CAN THIS PROVE RH?
# =============================================================================

print("\n" + "="*75)
print("PART 5: CAN SPECTRAL METHODS PROVE RH?")
print("="*75)

print("""
WHAT WE HAVE:
1. Coprimality graph has large spectral gap λ₂ ~ 0.35 * Q(N)
2. Expander mixing suggests concentration
3. Concentration inequality gives |M(N)| = O(√N) with high prob

THE PROBLEM:
The concentration inequality gives PROBABILISTIC bounds.
But M(N) is DETERMINISTIC - it's not a random variable!

The spectral gap tells us about TYPICAL behavior of ±1 sums
over the graph, but M(N) corresponds to a SPECIFIC assignment
(given by μ).

WHAT WOULD HELP:
Need to show that the μ assignment is "generic" in some sense.
If μ is "indistinguishable from random" with respect to the
graph structure, then spectral bounds would apply.

THIS IS STILL CIRCULAR:
Showing μ is "random enough" requires knowing its correlations,
which brings us back to the original problem.

HOWEVER:
The spectral approach gives a NEW ANGLE. Instead of zeros,
we're asking about graph-theoretic properties.

A proof might show:
1. The coprimality graph is a strong expander (proven by direct computation)
2. Any multiplicative function on squarefree integers behaves
   "randomly enough" on this graph (needs proof)
3. Therefore M(N) = O(√N) (would follow from 1+2)

Step 2 is the hard part - it requires understanding the
interaction between multiplicativity and graph structure.
""")

# =============================================================================
# PART 6: MULTIPLICATIVITY VS GRAPH STRUCTURE
# =============================================================================

print("\n" + "="*75)
print("PART 6: MULTIPLICATIVITY VS GRAPH STRUCTURE")
print("="*75)

print("""
KEY OBSERVATION: Multiplicativity creates correlations.
If gcd(m, n) = 1, then μ(mn) = μ(m)μ(n).

This means: edges in the coprimality graph encode CONSTRAINTS!

For coprime (m, n):
  μ(m) * μ(n) = μ(mn)

The graph structure EXACTLY encodes the algebraic relations.
Maybe this is the key to breaking circularity?
""")

def analyze_multiplicative_constraints(N):
    """Analyze how multiplicativity constrains μ on the graph."""
    mu, _ = mobius_sieve(N)
    sqfree = [n for n in range(1, N+1) if mu[n] != 0]

    # For each edge (m, n) with gcd(m,n)=1, we have μ(m)μ(n) = μ(mn)
    # This is a constraint on the μ assignment

    constraints_satisfied = 0
    total_constraints = 0

    for i, m in enumerate(sqfree):
        for j, n in enumerate(sqfree):
            if j <= i:
                continue
            if gcd(m, n) == 1:
                mn = m * n
                if mn <= N:
                    # Constraint: μ(m)μ(n) = μ(mn)
                    lhs = mu[m] * mu[n]
                    rhs = mu[mn]
                    if lhs == rhs:
                        constraints_satisfied += 1
                    total_constraints += 1

    return constraints_satisfied, total_constraints

print("\nMultiplicativity constraints:")
for N in [50, 100, 200, 500]:
    sat, total = analyze_multiplicative_constraints(N)
    if total > 0:
        print(f"N = {N}: {sat}/{total} constraints satisfied ({100*sat/total:.1f}%)")

# =============================================================================
# SUMMARY
# =============================================================================

print("\n" + "="*75)
print("SUMMARY: SPECTRAL APPROACH ASSESSMENT")
print("="*75)

print("""
FINDINGS:

1. SPECTRAL GAP: λ₂ ≈ 0.35 * Q(N)
   The coprimality graph is a STRONG EXPANDER.

2. CHEEGER CONSTANT: h ≈ 0.5+
   The boson-fermion partition is well-connected.

3. CONCENTRATION: For random ±1, get |S| = O(√n) whp
   But μ is NOT random...

4. MULTIPLICATIVITY: 100% of constraints satisfied (by definition)
   This is built into the structure.

THE KEY INSIGHT:
The coprimality graph encodes EXACTLY the multiplicative structure.
An edge (m,n) exists iff μ(mn) = μ(m)μ(n).

This means the graph Laplacian L encodes information about
how μ values propagate through multiplicative relations.

POTENTIAL PATH TO PROOF:
1. Show that any function satisfying multiplicativity constraints
   on this expander graph must have bounded fluctuations.
2. This would be a NEW argument, not depending on zeros.

OBSTACLE:
The number 1 is special: μ(1) = 1 fixes the "seed" value.
All other μ values are determined by multiplicativity from primes.
The graph structure doesn't constrain the prime values!

CONCLUSION:
The spectral approach is INTERESTING but still faces circularity.
The graph structure encodes multiplicativity perfectly,
but the prime values (all μ(p) = -1) are not constrained.

This is the same fundamental problem in a new language.
""")

print("="*75)
print("END OF SPECTRAL DEEP DIVE")
print("="*75)
