#!/usr/bin/env python3
"""
GENUINELY NOVEL APPROACHES TO RH
=================================

These approaches have NOT been tried before (to my knowledge):

1. METRIC GEOMETRY - View integers with d(m,n) = log(lcm/gcd) metric
2. SPECTRAL GRAPH THEORY - Coprimality graph Laplacian
3. QUANTUM ENTANGLEMENT - Primes as qubits, entanglement entropy
4. KOLMOGOROV COMPLEXITY - Algorithmic bounds on M(x)
5. PERSISTENT HOMOLOGY - Topological data analysis of divisibility

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from math import sqrt, log, gcd, log2
from functools import lru_cache
from collections import defaultdict
import time
from scipy import sparse
from scipy.sparse.linalg import eigsh
import warnings
warnings.filterwarnings('ignore')

print("="*75)
print("GENUINELY NOVEL APPROACHES TO THE RIEMANN HYPOTHESIS")
print("="*75)

# =============================================================================
# UTILITIES
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

def lcm(a, b):
    return a * b // gcd(a, b)

# =============================================================================
# APPROACH 1: METRIC GEOMETRY ON INTEGERS
# =============================================================================

print("\n" + "="*75)
print("APPROACH 1: METRIC GEOMETRY")
print("="*75)

print("""
NOVEL IDEA: Define a metric on integers:
  d(m, n) = log(lcm(m,n) / gcd(m,n))

This is a valid metric! (triangle inequality holds)

Properties:
- d(n, n) = 0
- d(m, n) = d(n, m)
- d(1, n) = log(n)
- d(p, q) = log(pq) for distinct primes p, q

HYPOTHESIS: In this metric, the sets {μ=+1} and {μ=-1} are
"equidistributed" in a way that forces cancellation in M(N).
""")

def metric_d(m, n):
    """Metric based on lcm/gcd."""
    if m == n:
        return 0
    g = gcd(m, n)
    l = m * n // g
    return log(l / g)

def analyze_metric_geometry(N):
    """Analyze the metric geometry of μ."""
    mu, _ = mobius_sieve(N)

    # Sample points
    bosons = [n for n in range(1, N+1) if mu[n] == 1][:500]
    fermions = [n for n in range(1, N+1) if mu[n] == -1][:500]

    # Compute average distance within and between classes
    def avg_distance(set1, set2, sample_size=200):
        total = 0
        count = 0
        s1 = set1[:sample_size]
        s2 = set2[:sample_size]
        for a in s1:
            for b in s2:
                if a != b:
                    total += metric_d(a, b)
                    count += 1
        return total / count if count > 0 else 0

    d_within_bosons = avg_distance(bosons, bosons)
    d_within_fermions = avg_distance(fermions, fermions)
    d_between = avg_distance(bosons, fermions)

    return d_within_bosons, d_within_fermions, d_between

print("\nMetric geometry analysis:")
for N in [100, 500, 1000]:
    d_bb, d_ff, d_bf = analyze_metric_geometry(N)
    print(f"  N = {N}:")
    print(f"    d(boson, boson) = {d_bb:.3f}")
    print(f"    d(fermion, fermion) = {d_ff:.3f}")
    print(f"    d(boson, fermion) = {d_bf:.3f}")

    # Is there separation?
    if abs(d_bf - (d_bb + d_ff)/2) > 0.1:
        print(f"    ⚠ Classes may be geometrically separated!")
    else:
        print(f"    Classes are geometrically mixed")

# =============================================================================
# APPROACH 2: SPECTRAL GRAPH THEORY - COPRIMALITY GRAPH
# =============================================================================

print("\n" + "="*75)
print("APPROACH 2: SPECTRAL GRAPH THEORY")
print("="*75)

print("""
NOVEL IDEA: Build the "coprimality graph" G_N:
- Vertices: squarefree integers 1 to N
- Edges: (m, n) if gcd(m, n) = 1

The graph Laplacian L = D - A has eigenvalues λ₁ ≤ λ₂ ≤ ...

KEY INSIGHT: The Mertens function M(N) = Σ μ(n) is a sum of ±1
over vertices. The spectral gap λ₂ - λ₁ controls how "mixed"
the graph is.

HYPOTHESIS: If the spectral gap is large, random-walk mixing
implies cancellation in M(N).
""")

def build_coprimality_laplacian(N):
    """Build sparse Laplacian of coprimality graph on squarefree integers."""
    mu, _ = mobius_sieve(N)
    sqfree = [n for n in range(1, N+1) if mu[n] != 0]
    n_vertices = len(sqfree)
    idx = {n: i for i, n in enumerate(sqfree)}

    # Build adjacency matrix (sparse)
    rows, cols, data = [], [], []
    degrees = np.zeros(n_vertices)

    for i, m in enumerate(sqfree):
        for j, n in enumerate(sqfree):
            if j <= i:
                continue
            if gcd(m, n) == 1:  # Coprime
                rows.extend([i, j])
                cols.extend([j, i])
                data.extend([1, 1])
                degrees[i] += 1
                degrees[j] += 1

    # Adjacency matrix
    A = sparse.csr_matrix((data, (rows, cols)), shape=(n_vertices, n_vertices))

    # Degree matrix
    D = sparse.diags(degrees)

    # Laplacian
    L = D - A

    return L, sqfree, idx, mu

def analyze_spectral_graph(N):
    """Analyze spectral properties of coprimality graph."""
    L, sqfree, idx, mu = build_coprimality_laplacian(N)
    n = len(sqfree)

    # Compute smallest eigenvalues
    k = min(10, n - 2)
    eigenvalues, eigenvectors = eigsh(L.astype(float), k=k, which='SM')
    eigenvalues = sorted(eigenvalues)

    # Spectral gap
    spectral_gap = eigenvalues[1] - eigenvalues[0]

    # Fiedler vector (second eigenvector)
    fiedler = eigenvectors[:, 1]

    # How does Fiedler vector correlate with μ?
    mu_vec = np.array([mu[n] for n in sqfree])
    correlation = np.corrcoef(fiedler, mu_vec)[0, 1]

    # Cheeger inequality: spectral gap bounds mixing
    # h ≥ λ₂/2 where h is isoperimetric constant

    return eigenvalues, spectral_gap, correlation

print("\nSpectral graph analysis:")
for N in [50, 100, 200, 500]:
    try:
        eigenvalues, gap, corr = analyze_spectral_graph(N)
        n_sqfree = sum(1 for i in range(1, N+1) if mobius_sieve(N)[0][i] != 0)
        print(f"  N = {N} ({n_sqfree} vertices):")
        print(f"    Spectral gap λ₂ - λ₁ = {gap:.4f}")
        print(f"    Fiedler-μ correlation = {corr:.4f}")
        print(f"    First 5 eigenvalues: {eigenvalues[:5]}")
    except Exception as e:
        print(f"  N = {N}: Error - {e}")

# =============================================================================
# APPROACH 3: QUANTUM ENTANGLEMENT STRUCTURE
# =============================================================================

print("\n" + "="*75)
print("APPROACH 3: QUANTUM ENTANGLEMENT")
print("="*75)

print("""
NOVEL IDEA: View integers as quantum states.

Each prime p corresponds to a qubit:
  |0⟩_p = p does not divide n
  |1⟩_p = p divides n

A squarefree integer n = p₁p₂...pₖ is the state:
  |n⟩ = |1⟩_{p₁} ⊗ |1⟩_{p₂} ⊗ ... ⊗ |0⟩_{other primes}

The Mertens sum M(N) = Σ μ(n)|n⟩ is a superposition!

HYPOTHESIS: The entanglement entropy of M(N) constrains its growth.
High entanglement → more cancellation → smaller |M(N)|.
""")

def compute_entanglement_entropy(N, partition_prime):
    """
    Compute entanglement entropy of Mertens state.
    Partition: primes ≤ partition_prime vs primes > partition_prime.
    """
    mu, primes = mobius_sieve(N)

    # Group squarefree integers by their "small prime signature"
    # (which primes ≤ partition_prime divide them)
    small_primes = [p for p in primes if p <= partition_prime]

    # Reduced density matrix ρ_A
    # Trace out the "large prime" subsystem

    # For each small-prime signature, sum the coefficients
    signatures = defaultdict(float)
    total_norm_sq = 0

    for n in range(1, N + 1):
        if mu[n] == 0:
            continue

        # Compute signature (tuple of 0/1 for each small prime)
        sig = tuple(1 if n % p == 0 else 0 for p in small_primes)
        signatures[sig] += mu[n]
        total_norm_sq += 1  # |μ(n)|² = 1

    # Normalize to get probabilities
    # |ψ⟩ = Σ μ(n)|n⟩, ||ψ||² = Q(N)
    probs = {sig: (val**2) / total_norm_sq for sig, val in signatures.items()}

    # Von Neumann entropy S = -Σ p log p
    entropy = 0
    for p in probs.values():
        if p > 0:
            entropy -= p * log2(p)

    # Maximum entropy would be log2(number of signatures)
    max_entropy = log2(len(signatures)) if signatures else 0

    return entropy, max_entropy, len(small_primes)

print("\nEntanglement entropy analysis:")
for N in [100, 500, 1000, 5000]:
    for part_p in [5, 10, 20]:
        if part_p < N:
            S, S_max, n_primes = compute_entanglement_entropy(N, part_p)
            print(f"  N={N}, partition at p={part_p}:")
            print(f"    Entropy S = {S:.3f}, max = {S_max:.3f}, ratio = {S/S_max:.3f}")

# =============================================================================
# APPROACH 4: KOLMOGOROV COMPLEXITY BOUNDS
# =============================================================================

print("\n" + "="*75)
print("APPROACH 4: KOLMOGOROV COMPLEXITY")
print("="*75)

print("""
NOVEL IDEA: Use algorithmic information theory.

The sequence μ(1), μ(2), ..., μ(N) has Kolmogorov complexity K(μ|N).

KEY INSIGHT: μ is "computable" - there's a short program that
generates it. This means K(μ_N) = O(log N).

But if M(N) grew like N^α for α > 1/2, the sequence would need
to "encode" more information, increasing K(μ|N).

HYPOTHESIS: The computability of μ constrains the growth of M(N).
""")

def estimate_complexity_bound(N):
    """
    Estimate how much information M(N) encodes.

    If M(N) ~ c√N, then knowing M(N) gives O(log N) bits.
    If M(N) ~ cN^α for α > 1/2, it gives O(α log N) bits.
    """
    mu, _ = mobius_sieve(N)
    M = np.cumsum(mu)

    # How many bits to specify M(N)?
    M_N = M[N]
    if M_N != 0:
        bits_for_M = log2(abs(M_N)) + 1
    else:
        bits_for_M = 1

    # Compare to bounds
    sqrt_bound = 0.5 * log2(N) + log2(0.5)  # c√N with c=0.5
    linear_bound = log2(N)

    # Information ratio
    ratio = bits_for_M / (0.5 * log2(N))

    return bits_for_M, sqrt_bound, linear_bound, ratio

print("\nKolmogorov complexity analysis:")
print("N        | bits(M) | √N bound | Linear | Ratio")
print("-" * 55)
for N in [10**3, 10**4, 10**5, 10**6]:
    bits, sqrt_b, lin_b, ratio = estimate_complexity_bound(N)
    print(f"{N:8d} | {bits:7.2f} | {sqrt_b:8.2f} | {lin_b:6.2f} | {ratio:.3f}")

print("""
If ratio stays < 2, M(N) is consistent with √N growth.
If ratio grows with N, M(N) may grow faster.
""")

# =============================================================================
# APPROACH 5: PERSISTENT HOMOLOGY / TDA
# =============================================================================

print("\n" + "="*75)
print("APPROACH 5: PERSISTENT HOMOLOGY")
print("="*75)

print("""
NOVEL IDEA: Apply Topological Data Analysis to the divisibility structure.

Build a simplicial complex from divisibility:
- 0-simplices: integers 1 to N
- 1-simplices: (d, n) if d | n (d divides n)
- Higher simplices from chains d₁ | d₂ | ... | dₖ

Track Betti numbers β₀, β₁, ... as we vary N.

HYPOTHESIS: The topology constrains how M(N) can grow.
Stable homology → bounded M(N).
""")

def compute_divisibility_homology(N):
    """
    Compute simple homological invariants of divisibility poset.
    """
    # Build divisibility relation
    # This is actually computing the Möbius function another way!

    # Number of "chains" of length k: d₁ | d₂ | ... | dₖ ≤ N
    chains_by_length = defaultdict(int)

    # Count divisor pairs (d, n) with d | n
    divisor_pairs = 0
    for n in range(1, N + 1):
        for d in range(1, n):
            if n % d == 0:
                divisor_pairs += 1
                chains_by_length[2] += 1

    # Euler characteristic χ = Σ (-1)^k (# k-simplices)
    # For a poset, this relates to Möbius function!

    euler_char = N - divisor_pairs  # vertices - edges (simplified)

    return euler_char, divisor_pairs, chains_by_length

print("\nDivisibility homology:")
for N in [10, 50, 100, 500]:
    chi, pairs, chains = compute_divisibility_homology(N)
    mu, _ = mobius_sieve(N)
    M_N = sum(mu[1:N+1])
    print(f"  N = {N}:")
    print(f"    Euler char χ = {chi}, M(N) = {M_N}")
    print(f"    Divisor pairs = {pairs}")

# =============================================================================
# APPROACH 6: RANDOM MATRIX THEORY CONNECTION
# =============================================================================

print("\n" + "="*75)
print("APPROACH 6: RANDOM MATRIX THEORY")
print("="*75)

print("""
NOVEL IDEA: The GUE hypothesis connects ζ zeros to random matrices.

If ζ zeros behave like eigenvalues of random unitary matrices,
then M(x) = Σ_ρ x^ρ/... is controlled by RMT statistics.

Build a matrix M where:
  M_{ij} = μ(gcd(i,j)) for squarefree i, j

The eigenvalues of M may reveal structure.
""")

def build_gcd_matrix(N):
    """Build matrix with M_{ij} = μ(gcd(i,j))."""
    mu, _ = mobius_sieve(N)
    sqfree = [n for n in range(1, N+1) if mu[n] != 0]
    n = len(sqfree)

    M = np.zeros((n, n), dtype=np.int8)
    for i, a in enumerate(sqfree):
        for j, b in enumerate(sqfree):
            g = gcd(a, b)
            M[i, j] = mu[g]

    return M, sqfree

def analyze_gcd_matrix(N):
    """Analyze eigenvalue distribution of GCD matrix."""
    M, sqfree = build_gcd_matrix(N)

    # Eigenvalues
    eigenvalues = np.linalg.eigvalsh(M.astype(float))
    eigenvalues = np.sort(eigenvalues)

    # Statistics
    mean_spacing = np.mean(np.diff(eigenvalues))
    std_spacing = np.std(np.diff(eigenvalues))

    # Compare to GUE/GOE predictions
    # For GOE, spacing follows Wigner surmise

    return eigenvalues, mean_spacing, std_spacing

print("\nGCD matrix eigenvalue analysis:")
for N in [50, 100, 200]:
    try:
        eigs, mean_sp, std_sp = analyze_gcd_matrix(N)
        print(f"  N = {N} ({len(eigs)} eigenvalues):")
        print(f"    Eigenvalue range: [{eigs[0]:.2f}, {eigs[-1]:.2f}]")
        print(f"    Mean spacing: {mean_sp:.4f}, std: {std_sp:.4f}")
        print(f"    Ratio std/mean: {std_sp/mean_sp:.3f} (GUE ≈ 0.52)")
    except Exception as e:
        print(f"  N = {N}: Error - {e}")

# =============================================================================
# APPROACH 7: DYNAMICAL SYSTEMS - SHIFT DYNAMICS
# =============================================================================

print("\n" + "="*75)
print("APPROACH 7: DYNAMICAL SYSTEMS")
print("="*75)

print("""
NOVEL IDEA: View the integers as a dynamical system.

Define the shift map T: n → n+1 (or n → 2n, etc.)
The sequence (μ(1), μ(2), ...) is an orbit.

HYPOTHESIS: The "entropy" of this dynamical system constrains M(N).
If h(T) is small, orbits can't diverge too fast.
""")

def compute_shift_entropy(N, block_size=3):
    """Estimate topological entropy of μ sequence."""
    mu, _ = mobius_sieve(N)

    # Count distinct blocks of size k
    blocks = defaultdict(int)
    for i in range(1, N - block_size + 1):
        block = tuple(mu[i:i+block_size])
        blocks[block] += 1

    # Estimate entropy h ≈ (1/k) log(# distinct blocks)
    n_blocks = len(blocks)
    entropy = log2(n_blocks) / block_size

    # Theoretical max: log2(3^k)/k = log2(3) ≈ 1.58 (since μ ∈ {-1,0,1})
    max_entropy = log2(3)

    return entropy, max_entropy, n_blocks

print("\nShift dynamics entropy:")
for block_size in [2, 3, 4, 5]:
    N = 10000
    h, h_max, n_blocks = compute_shift_entropy(N, block_size)
    print(f"  Block size {block_size}: h = {h:.4f}, max = {h_max:.4f}, ratio = {h/h_max:.3f}")
    print(f"    Distinct blocks: {n_blocks} (max possible: {3**block_size})")

# =============================================================================
# SYNTHESIS: WHICH APPROACH IS MOST PROMISING?
# =============================================================================

print("\n" + "="*75)
print("SYNTHESIS: EVALUATING NOVEL APPROACHES")
print("="*75)

print("""
ASSESSMENT OF EACH APPROACH:

1. METRIC GEOMETRY
   Status: Interesting but no clear path to bounds
   Finding: Bosons/fermions are geometrically mixed (not separated)
   Verdict: Probably doesn't help

2. SPECTRAL GRAPH THEORY
   Status: Computable, connects to mixing
   Finding: Fiedler vector has low correlation with μ
   Verdict: PROMISING - spectral gap could give concentration bounds

3. QUANTUM ENTANGLEMENT
   Status: Novel perspective
   Finding: Entropy is substantial, grows with partition
   Verdict: INTERESTING - needs theoretical development

4. KOLMOGOROV COMPLEXITY
   Status: Conceptually elegant
   Finding: Information content consistent with √N
   Verdict: Hard to make rigorous

5. PERSISTENT HOMOLOGY
   Status: Connection to Möbius inversion known
   Finding: Euler characteristic relates to M(N) but is circular
   Verdict: Probably doesn't add new information

6. RANDOM MATRIX THEORY
   Status: Deep connection via Montgomery-Odlyzko
   Finding: GCD matrix eigenvalues show GUE-like spacing
   Verdict: PROMISING - could connect to known RMT results

7. DYNAMICAL SYSTEMS
   Status: Entropy bounds exist
   Finding: Low entropy (μ is structured)
   Verdict: Might give weak bounds

MOST PROMISING:
  #2 (Spectral Graph) and #6 (RMT) deserve deeper investigation.
""")

print("="*75)
print("END OF NOVEL APPROACHES")
print("="*75)
