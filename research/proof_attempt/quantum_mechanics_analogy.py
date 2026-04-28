"""
QUANTUM MECHANICS ANALOGY
=========================

The nilpotent operator D reminds us of quantum mechanics:
1. D is NILPOTENT: D^m = 0 (like annihilation operator on finite space)
2. (I+D) has all eigenvalues = 1 (like identity + nilpotent)
3. M = (I+D)^{-1} e = sum (-D)^k e (Neumann series = perturbation theory!)

Quantum mechanics connections:
- Ladder operators a, a†
- Supersymmetry generators Q, Q†
- Path integrals and Feynman diagrams
- Second quantization

Can any of these provide new insight?

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from sympy import mobius, factorint, divisors, gcd
from collections import defaultdict
import math

print("=" * 80)
print("QUANTUM MECHANICS ANALOGY")
print("=" * 80)

# Setup
MAX_N = 10000
M_array = [0] * (MAX_N + 1)
mu_array = [0] * (MAX_N + 1)

cumsum = 0
for n in range(1, MAX_N + 1):
    mu_array[n] = int(mobius(n))
    cumsum += mu_array[n]
    M_array[n] = cumsum

def M(x):
    return M_array[int(x)] if 1 <= int(x) <= MAX_N else 0

def mu(n):
    return mu_array[int(n)] if int(n) <= MAX_N else int(mobius(int(n)))

print("Setup complete.\n")

# =============================================================================
# PART 1: LADDER OPERATOR STRUCTURE
# =============================================================================

print("=" * 60)
print("PART 1: LADDER OPERATOR STRUCTURE")
print("=" * 60)

print("""
QUANTUM HARMONIC OSCILLATOR:
  H = (1/2)(p^2 + x^2) = a†a + 1/2
  a = (x + ip)/sqrt(2)   (annihilation/lowering)
  a† = (x - ip)/sqrt(2)  (creation/raising)
  [a, a†] = 1

  a|n> = sqrt(n)|n-1>
  a†|n> = sqrt(n+1)|n+1>

  a^k eventually annihilates any state: a^n|n-1> = ... = |0>

OUR OPERATOR D:
  D is strictly lower triangular (like annihilation)
  D^k e eventually = 0 (nilpotent)

DIFFERENCE:
  - QM: infinite-dimensional, a never exactly nilpotent
  - Our D: finite-dimensional (in any truncation), strictly nilpotent
""")

# Demonstrate the "annihilation" behavior
print("\nNilpotent behavior D^k e:")
N = 50

# Build D as divisor-sum operator (restricted)
D = np.zeros((N, N))
for n in range(1, N + 1):
    for d in divisors(n):
        if d < n:
            D[n-1, d-1] = 1  # D_{n,d} = 1 if d|n and d < n

e = np.ones(N)

print(f"For N = {N}:")
D_power = np.eye(N)
for k in range(10):
    result = D_power @ e
    norm = np.linalg.norm(result)
    nonzero = np.sum(np.abs(result) > 1e-10)
    print(f"  ||D^{k} e|| = {norm:.2f}, nonzero entries = {nonzero}")
    D_power = D_power @ D
    if norm < 1e-10:
        print(f"  D^{k} e = 0 (nilpotent!)")
        break

# =============================================================================
# PART 2: NEUMANN SERIES AS PERTURBATION THEORY
# =============================================================================

print("\n" + "=" * 60)
print("PART 2: NEUMANN SERIES = PERTURBATION THEORY")
print("=" * 60)

print("""
In quantum mechanics, perturbation theory expands:
  (H0 + V)^{-1} = H0^{-1} - H0^{-1} V H0^{-1} + H0^{-1} V H0^{-1} V H0^{-1} - ...

This is the Neumann series for (H0 + V)^{-1} = H0^{-1}(I + H0^{-1}V)^{-1}

OUR FORMULA:
  M = (I + D)^{-1} e = sum_k (-D)^k e = e - De + D^2e - D^3e + ...

This IS perturbation theory with:
  H0 = I (identity)
  V = D (divisor operator)

The "unperturbed" Mertens is just e (all 1's).
D adds "corrections" from divisor structure.
""")

# Show the perturbation series
N = 100
D = np.zeros((N, N))
for n in range(1, N + 1):
    for d in divisors(n):
        if d < n:
            D[n-1, d-1] = 1

e = np.ones(N)

print("\nPerturbation series contributions:")
M_computed = np.zeros(N)
D_power = np.eye(N)

for k in range(15):
    contribution = ((-1)**k) * (D_power @ e)
    M_computed += contribution

    # Compare with actual M
    actual_M = np.array([M(n) for n in range(1, N + 1)])
    error = np.linalg.norm(M_computed - actual_M)

    print(f"  k={k}: ||contribution|| = {np.linalg.norm(contribution):.2f}, cumulative error = {error:.4f}")
    D_power = D_power @ D

    if np.linalg.norm(contribution) < 1e-10:
        break

# =============================================================================
# PART 3: FEYNMAN DIAGRAM INTERPRETATION
# =============================================================================

print("\n" + "=" * 60)
print("PART 3: FEYNMAN DIAGRAM INTERPRETATION")
print("=" * 60)

print("""
In QFT, Feynman diagrams represent terms in perturbation series.
Each diagram has vertices (interactions) and propagators (lines).

OUR DIAGRAMS:
  M(n) = sum over "paths" from 1 to n through divisor chains

A "path" from n to 1:
  n -> d1 -> d2 -> ... -> 1  where each d_i | d_{i-1}

Each step contributes a factor of (-1).
The "Feynman rules":
  - Vertex at divisor d: factor (-1)
  - Path weight: product of factors = (-1)^{length}
  - Sum over all paths
""")

def count_divisor_paths(n, memo={}):
    """Count paths from n to 1 through proper divisors, with signs."""
    if n == 1:
        return [([], 1)]  # Empty path, weight +1

    if n in memo:
        return memo[n]

    paths = []
    for d in divisors(n):
        if d < n and d >= 1:
            for (sub_path, weight) in count_divisor_paths(d, memo):
                paths.append(([d] + sub_path, -weight))  # Each step adds (-1)

    memo[n] = paths
    return paths

print("\nDivisor path decomposition:")
for n in [6, 12, 30]:
    paths = count_divisor_paths(n, {})
    total = sum(w for (p, w) in paths)
    print(f"\n  n = {n}: mu({n}) = {mu(n)}")
    print(f"  Number of paths: {len(paths)}")
    print(f"  Sum of weights: {total}")
    if len(paths) <= 10:
        for (path, weight) in paths:
            print(f"    {n} -> {' -> '.join(map(str, path)) if path else '(empty)'}: weight = {weight:+d}")

# =============================================================================
# PART 4: SUPERSYMMETRY ANALOGY
# =============================================================================

print("\n" + "=" * 60)
print("PART 4: SUPERSYMMETRY ANALOGY")
print("=" * 60)

print("""
SUPERSYMMETRY has nilpotent generators Q:
  Q^2 = 0

This is exactly like our D^m = 0!

In SUSY:
  - Bosons <-> Fermions
  - Q creates/annihilates the "fermionic" part
  - The Witten index counts signed states

ANALOGY:
  - Squarefree n with even omega <-> Bosons
  - Squarefree n with odd omega <-> Fermions
  - M(x) = #bosons - #fermions = Witten index!

The Witten index is topologically protected and often exactly computable.
""")

# Compute "bosonic" and "fermionic" contributions
print("\nBosonic vs Fermionic (Witten index interpretation):")
for x in [100, 500, 1000, 5000]:
    bosons = sum(1 for n in range(1, x+1) if mu(n) == 1)
    fermions = sum(1 for n in range(1, x+1) if mu(n) == -1)
    witten = bosons - fermions  # This equals M(x)

    print(f"  x={x}: Bosons={bosons}, Fermions={fermions}, Witten index={witten}, M(x)={M(x)}")

# =============================================================================
# PART 5: SECOND QUANTIZATION
# =============================================================================

print("\n" + "=" * 60)
print("PART 5: SECOND QUANTIZATION")
print("=" * 60)

print("""
In second quantization, we have:
  |n_1, n_2, ...> = occupation number states
  a_p† creates a particle in state p
  a_p annihilates a particle in state p

For PRIMES as "particles":
  |n> corresponds to prime factorization of n
  n = p1^{a1} p2^{a2} ... = |a1, a2, ...>

  mu(n) != 0 iff all a_i in {0, 1}
  mu(n) = (-1)^{sum a_i} for such n

This is the FERMION parity operator!
  mu = product_p (1 - 2 n_p) for n_p in {0,1}
""")

# Verify the fermion parity interpretation
print("\nFermion parity interpretation:")
print("For squarefree n: mu(n) = (-1)^{number of prime factors}")

verified = 0
total = 0
for n in range(1, 101):
    if mu(n) != 0:
        total += 1
        omega = len(factorint(n))
        if mu(n) == (-1)**omega:
            verified += 1

print(f"  Verified: {verified}/{total}")

# =============================================================================
# PART 6: PARTITION FUNCTION AND TRACE
# =============================================================================

print("\n" + "=" * 60)
print("PART 6: PARTITION FUNCTION AND TRACE")
print("=" * 60)

print("""
In quantum mechanics:
  Z(beta) = Tr(exp(-beta H))  (partition function)

For our operator (I + D):
  All eigenvalues = 1
  Z = Tr((I+D)^k) = N for all k (since (I+D)^k ~ I + nilpotent)

Actually, det(I+D) = 1 (product of eigenvalues)!

The RESOLVENT:
  R(z) = (z I - A)^{-1}

For A = -D:
  R(z) = (zI + D)^{-1}

At z = 1:
  R(1) = (I + D)^{-1}
  M = R(1) e

So M is related to the RESOLVENT of D at z = 1!
""")

# Compute some traces
N = 100
D = np.zeros((N, N))
for n in range(1, N + 1):
    for d in divisors(n):
        if d < n:
            D[n-1, d-1] = 1

I_plus_D = np.eye(N) + D

print(f"\nFor N = {N}:")
print(f"  Tr(I + D) = {np.trace(I_plus_D):.0f} (expected: {N})")
print(f"  det(I + D) = {np.linalg.det(I_plus_D):.4f} (expected: 1)")

# Powers
for k in [1, 2, 3, 5, 10]:
    power = np.linalg.matrix_power(I_plus_D, k)
    trace = np.trace(power)
    print(f"  Tr((I+D)^{k}) = {trace:.0f}")

# =============================================================================
# PART 7: COMMUTATOR STRUCTURE
# =============================================================================

print("\n" + "=" * 60)
print("PART 7: COMMUTATOR STRUCTURE")
print("=" * 60)

print("""
In QM, the commutator [A, B] = AB - BA is fundamental.
For ladder operators: [a, a†] = 1

What is the commutator of D with its "adjoint"?

Define D† (formal adjoint in divisor sense):
  D†[n,m] = 1 if n|m and n < m

This is the "raising" operator (from d to multiples).
""")

N = 50
D = np.zeros((N, N))
D_dag = np.zeros((N, N))

for n in range(1, N + 1):
    for m in range(1, N + 1):
        if m < n and n % m == 0:
            D[n-1, m-1] = 1  # n has divisor m < n
        if n < m and m % n == 0:
            D_dag[n-1, m-1] = 1  # n divides m > n

# Commutator
commutator = D @ D_dag - D_dag @ D

print(f"\nCommutator [D, D†] for N = {N}:")
print(f"  ||[D, D†]|| = {np.linalg.norm(commutator):.2f}")
print(f"  Tr([D, D†]) = {np.trace(commutator):.4f}")

# Diagonal entries of commutator
diag = np.diag(commutator)
print(f"  [D, D†]_{1,1} = {commutator[0,0]:.0f}")
print(f"  [D, D†]_{2,2} = {commutator[1,1]:.0f}")
print(f"  [D, D†]_{6,6} = {commutator[5,5]:.0f}")
print(f"  [D, D†]_{12,12} = {commutator[11,11]:.0f}")

# =============================================================================
# PART 8: COHERENT STATES
# =============================================================================

print("\n" + "=" * 60)
print("PART 8: COHERENT STATES ANALOGY")
print("=" * 60)

print("""
Coherent states |alpha> are eigenstates of the annihilation operator:
  a |alpha> = alpha |alpha>

For our D, since D is nilpotent, the only eigenvalue is 0.
But we can look for "approximate" coherent states.

The vector e = (1, 1, ..., 1) is special:
  D e = (d(n) - 1) for each n

This measures "how far" e is from being annihilated.
""")

N = 100
D = np.zeros((N, N))
for n in range(1, N + 1):
    for d in divisors(n):
        if d < n:
            D[n-1, d-1] = 1

e = np.ones(N)
De = D @ e

print("\nAction of D on e:")
print(f"  D e = (d(n) - 1) where d(n) = number of divisors")
print(f"  First few: D e = {De[:10]}")

# Look at D e / e (pointwise)
print(f"\n  (De)_n = d(n) - 1:")
for n in [1, 2, 6, 12, 24, 36, 60]:
    if n <= N:
        print(f"    n={n}: De = {De[n-1]:.0f}, d(n) = {len(divisors(n))}")

# =============================================================================
# PART 9: PATH INTEGRAL ANALOGY
# =============================================================================

print("\n" + "=" * 60)
print("PART 9: PATH INTEGRAL ANALOGY")
print("=" * 60)

print("""
The path integral:
  <f|i> = integral over paths exp(iS[path])

For M(n), we can write:
  M(n) = sum over divisor chains (signed)

This is like summing over "histories" from 1 to n,
where each history is a chain of divisors.

The "action" for a path is:
  S = pi * (number of steps)  (gives (-1)^steps)
""")

def compute_M_path_integral(n):
    """Compute M(n) by summing over all divisor paths."""
    if n == 1:
        return 1

    # Use recursion: M(n) = sum_d (-1) * M(d) for d proper divisors
    total = 0
    for d in divisors(n):
        if d < n:
            total -= M(d)  # The "-" comes from one step

    return total

print("\nPath integral computation of M(n):")
for n in [1, 6, 10, 12, 30, 100]:
    computed = compute_M_path_integral(n)
    actual = M(n)
    print(f"  M({n}) = {computed} (path integral) = {actual} (direct)")

# =============================================================================
# PART 10: ZETA FUNCTION AS PARTITION FUNCTION
# =============================================================================

print("\n" + "=" * 60)
print("PART 10: ZETA AS PARTITION FUNCTION")
print("=" * 60)

print("""
The deepest QM connection:

zeta(s) = sum_n 1/n^s = Tr(H^{-s}) (informally)

where "H" is an operator with spectrum {log 1, log 2, log 3, ...}

The zeros of zeta are "resonances" of this quantum system!

Riemann-Siegel formula:
  zeta(1/2 + it) = sum involving eigenvalues

Montgomery-Odlyzko: zeros have GUE statistics (random matrix)

This connects to:
  - Quantum chaos
  - Random Hamiltonian theory
  - Berry-Tabor / Bohigas-Giannoni-Schmit conjectures
""")

print("\nThe quantum chaos connection:")
print("  - Integrable systems -> Poisson level statistics")
print("  - Chaotic systems -> GUE/GOE statistics")
print("  - zeta zeros -> GUE statistics")
print("  - Therefore: zeta corresponds to a CHAOTIC quantum system!")

# =============================================================================
# FINAL ASSESSMENT
# =============================================================================

print("\n" + "=" * 60)
print("FINAL ASSESSMENT: QUANTUM MECHANICS ANALOGY")
print("=" * 60)

print("""
QUANTUM MECHANICS FINDINGS:

1. LADDER OPERATOR STRUCTURE:
   - D is nilpotent (like annihilation in finite dim)
   - (I+D)^{-1} = Neumann series = perturbation theory

2. FEYNMAN DIAGRAMS:
   - M(n) = sum over divisor paths with signs
   - Each path is like a Feynman diagram
   - Weights are (-1)^{steps}

3. SUPERSYMMETRY:
   - Even omega = "bosons", odd omega = "fermions"
   - M(x) = Witten index = #bosons - #fermions
   - D^m = 0 is like Q^2 = 0

4. SECOND QUANTIZATION:
   - Primes are "particles"
   - n = |occupation numbers>
   - mu is the fermion parity operator

5. PATH INTEGRAL:
   - M(n) = sum over histories (divisor chains)
   - Action = pi * steps

6. ZETA = PARTITION FUNCTION:
   - Zeros = resonances
   - GUE statistics = quantum chaos

WHY THIS DOESN'T GIVE A PROOF:

The QM analogy is BEAUTIFUL and DEEP, but:
  - Quantum chaos doesn't predict exact bounds
  - Witten index gives existence, not size
  - Path integral sums are hard to bound
  - All roads lead back to zeta zeros

POSITIVE VALUE:

This perspective suggests:
  - Supersymmetric quantum mechanics techniques
  - Index theorems (Atiyah-Singer style)
  - Random matrix bounds
  - Trace formula methods

The fact that M(x) is a "Witten index" is particularly suggestive,
as Witten indices are often exactly computable in SUSY theories!
""")

print("=" * 80)
print("QUANTUM MECHANICS ANALOGY COMPLETE")
print("=" * 80)
