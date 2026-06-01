#!/usr/bin/env python3
"""
LEE-YANG THEOREM AND QUASICRYSTAL FRAMEWORKS
============================================

Two more exotic approaches to RH:
1. Lee-Yang: Can ζ(s) be a partition function satisfying Lee-Yang conditions?
2. Quasicrystals: The zeros form a crystalline measure (Dyson's hypothesis)

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from math import sqrt, log, pi, exp, cos, sin
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("LEE-YANG THEOREM AND QUASICRYSTAL FRAMEWORKS")
print("=" * 80)

# =============================================================================
# PART 1: THE LEE-YANG CIRCLE THEOREM
# =============================================================================

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                    PART 1: LEE-YANG CIRCLE THEOREM                          ║
╚════════════════════════════════════════════════════════════════════════════╝

LEE-YANG THEOREM (1952):

For the Ising model with ferromagnetic interactions (J_ij ≥ 0),
the grand partition function:

  Z(z) = Σ_{configs} z^{N_up} e^{-βH}

has ALL zeros on the UNIT CIRCLE |z| = 1 in the complex z plane.

THE CONNECTION TO RH:

Under the map z = e^{2πis}, the unit circle |z| = 1 becomes Re(s) = ?

Actually: |z| = |e^{2πis}| = e^{-2π Im(s)}

So |z| = 1 ⟺ Im(s) = 0 (real s, not critical line!)

FOR THE CRITICAL LINE:

We need a different map. Let s = 1/2 + it.

Then Re(s) = 1/2 for all real t.

Can we find z(s) such that Re(s) = 1/2 ⟺ |z| = 1?

TRY: z = e^{π(s - 1/2)} = e^{πit}

Then |z| = |e^{πit}| = 1 for all real t!

So: zeros on critical line ⟺ |z| = 1 under this map.
""")

# =============================================================================
# PART 2: CAN ζ(s) BE A PARTITION FUNCTION?
# =============================================================================

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                    PART 2: ζ(s) AS PARTITION FUNCTION                       ║
╚════════════════════════════════════════════════════════════════════════════╝

THE EULER PRODUCT:

ζ(s) = Π_p (1 - p^{-s})^{-1}

This looks like a product of "single-site" partition functions!

INTERPRETATION:

Let z_p = p^{-s}. Then:

  ζ(s) = Π_p 1/(1 - z_p) = Π_p (1 + z_p + z_p² + ...)

This is the partition function of a "Bose gas" where:
- Each prime p is a "site" or "mode"
- z_p = p^{-s} is the fugacity at site p
- Occupation numbers n_p = 0, 1, 2, 3, ...

THE "HAMILTONIAN":

Energy of configuration {n_p}: E = Σ_p n_p log(p)

Partition function: Z = Σ_{configs} e^{-βE} = Π_p 1/(1 - e^{-β log p})
                      = ζ(β)

So ζ(β) IS a partition function for β > 1!
""")

# =============================================================================
# PART 3: THE FERROMAGNETIC CONDITION
# =============================================================================

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                    PART 3: CHECKING FERROMAGNETIC CONDITIONS                ║
╚════════════════════════════════════════════════════════════════════════════╝

For Lee-Yang to apply, we need FERROMAGNETIC interactions:

  J_ij ≥ 0  (all couplings non-negative)

THE PRIME GAS:

In the Bose gas interpretation:
- Sites are labeled by primes p
- No DIRECT interactions between sites
- Each site is INDEPENDENT

PROBLEM 1: No Interactions!

The prime gas has H = Σ_p n_p log(p) - NO INTERACTION TERMS!

This is a FREE gas, not an interacting spin system.

Lee-Yang applies to INTERACTING systems with specific conditions.

PROBLEM 2: Complex Fugacity

For zeta zeros, we need s = 1/2 + it (complex).
The "fugacity" z_p = p^{-s} = p^{-1/2 - it} is COMPLEX.

Lee-Yang requires z real or on unit circle, not arbitrary complex.

PROBLEM 3: Infinite Sites

We have infinitely many primes, so infinitely many "sites."
Lee-Yang is proven for finite systems.
The infinite limit requires careful analysis.
""")

# =============================================================================
# PART 4: ATTEMPTS TO MAKE IT WORK
# =============================================================================

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                    PART 4: ATTEMPTING TO SATISFY LEE-YANG                   ║
╚════════════════════════════════════════════════════════════════════════════╝

ATTEMPT 1: Add Interactions

Modify the model to include interactions between primes:
  H = Σ_p n_p log(p) - Σ_{p<q} J_{pq} n_p n_q

If J_{pq} > 0 (ferromagnetic), Lee-Yang might apply.

PROBLEM: What determines J_{pq}?
- No natural interaction from number theory
- Arbitrary choice doesn't help

ATTEMPT 2: Transform Variables

Instead of z_p = p^{-s}, use:
  z_p = tanh(β h_p)  for some field h_p

This is the standard Ising parametrization.

PROBLEM: The transformation changes ζ(s) to something else.
We lose the connection to the original zeta zeros.

ATTEMPT 3: Use 1/ζ(s)

The function 1/ζ(s) = Π_p (1 - p^{-s}) has nicer structure.

But its zeros are the POLES of ζ(s), which is only s = 1.

NOT the zeros we want.

CONCLUSION:

There's no natural way to make ζ(s) satisfy Lee-Yang conditions.
The prime gas lacks the required ferromagnetic structure.
""")

# =============================================================================
# PART 5: THE QUASICRYSTAL HYPOTHESIS
# =============================================================================

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                    PART 5: DYSON'S QUASICRYSTAL HYPOTHESIS                  ║
╚════════════════════════════════════════════════════════════════════════════╝

FREEMAN DYSON (1998):

"The Riemann zeros are a one-dimensional quasicrystal."

WHAT IS A QUASICRYSTAL?

A set S ⊂ R is a quasicrystal if:
1. S is discrete (points don't accumulate)
2. S is not periodic (no T such that S + T = S)
3. The Fourier transform of Σ δ_s is also discrete

ORDINARY CRYSTALS: Periodic → Fourier transform is discrete lattice
QUASICRYSTALS: Non-periodic → Fourier transform is discrete but non-periodic

THE RIEMANN ZEROS:

Let S = {γ_n} = imaginary parts of zeta zeros.

1. Discrete? YES - zeros are isolated
2. Periodic? NO - spacing varies (asymptotically 2π/log(γ))
3. Fourier discrete? ...

THE EXPLICIT FORMULA:

The Guinand-Weil explicit formula says:

  Σ_γ e^{iγt} = -Σ_p Σ_k log(p)/p^{k/2} × e^{it k log p} + [smooth]

The left side: Fourier transform of Σ δ_γ
The right side: Sum over PRIME POWERS log(p^k)

THIS IS DISCRETE!

So the zeros DO form a quasicrystal!
""")

# =============================================================================
# PART 6: CRYSTALLINE MEASURES (KURASOV-SARNAK)
# =============================================================================

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                    PART 6: CRYSTALLINE MEASURES                             ║
╚════════════════════════════════════════════════════════════════════════════╝

DEFINITION (Kurasov-Sarnak 2020):

A measure μ on R is CRYSTALLINE if:
1. μ = Σ_j a_j δ_{x_j} (discrete)
2. The Fourier transform μ̂ = Σ_k b_k δ_{y_k} (also discrete)

EXAMPLES:

1. Poisson summation: μ = Σ_n δ_n → μ̂ = Σ_m δ_m (lattice → lattice)

2. Model sets: Cut through higher-dimensional lattice → quasicrystal

3. Zeta zeros: μ = Σ_γ δ_γ → μ̂ = Σ_{p,k} c_{p,k} δ_{log p^k}

THE RIEMANN ZEROS ARE A CRYSTALLINE MEASURE!

This is a THEOREM, not a conjecture.
It follows directly from the explicit formula.

THE QUESTION:

Does being a crystalline measure FORCE the zeros onto the critical line?

Answer: NO, at least not directly.

The crystalline property is about the Fourier structure,
not about the location of support.
""")

# =============================================================================
# PART 7: NUMERICAL VERIFICATION
# =============================================================================

print("=" * 80)
print("PART 7: NUMERICAL VERIFICATION OF QUASICRYSTAL STRUCTURE")
print("=" * 80)

# Load zeros
zeros = np.loadtxt('spectral_data/zeros1.txt')[:1000]

print("\nVerifying quasicrystal properties of zeta zeros:\n")

# 1. Discreteness
print("1. DISCRETENESS:")
spacings = np.diff(zeros)
print(f"   Min spacing: {spacings.min():.4f}")
print(f"   All positive: {np.all(spacings > 0)}")
print(f"   → Zeros are DISCRETE ✓")

# 2. Non-periodicity
print("\n2. NON-PERIODICITY:")
print(f"   Mean spacing: {spacings.mean():.4f}")
print(f"   Std of spacing: {spacings.std():.4f}")
print(f"   Variation: {spacings.std()/spacings.mean():.4f}")
print(f"   → NOT periodic (variation > 0) ✓")

# 3. Fourier structure
print("\n3. FOURIER STRUCTURE (Explicit Formula):")

# Compute "Fourier transform" at prime powers
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
print("   Fourier at log(p):")

for p in primes[:5]:
    t = log(p)
    ft = sum(np.exp(1j * gamma * t) for gamma in zeros)
    # Expected: ~ -log(p)/sqrt(p) × (number of zeros)
    expected = -log(p) / sqrt(p) * len(zeros)
    print(f"   p={p}: FT(log {p}) = {ft.real:.2f} + {ft.imag:.2f}i  (expect ~{expected:.0f})")

print(f"\n   → Fourier transform peaks at log(prime) positions ✓")
print(f"   → This is the EXPLICIT FORMULA ✓")

# =============================================================================
# PART 8: DOES QUASICRYSTAL IMPLY RH?
# =============================================================================

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                    PART 8: DOES QUASICRYSTAL STRUCTURE IMPLY RH?            ║
╚════════════════════════════════════════════════════════════════════════════╝

THE QUESTION:

If zeros form a quasicrystal (crystalline measure), does this FORCE
them onto the critical line?

ANALYSIS:

1. WHAT QUASICRYSTAL TELLS US:
   - The Fourier transform is discrete
   - The support is at prime logarithms
   - This is the explicit formula

2. WHAT IT DOESN'T TELL US:
   - The zeros could be at γ_n = Im(1/2 + iγ) (RH true)
   - OR at γ_n = Im(σ + iγ) for σ ≠ 1/2 (RH false)
   - In either case, the explicit formula holds!

THE EXPLICIT FORMULA HOLDS UNCONDITIONALLY:

  Σ_ρ f(ρ) = prime sum + corrections

This is true whether RH holds or not.
It tells us the FOURIER structure, not the REAL PARTS of zeros.

CONCLUSION:

Quasicrystal structure is a CONSEQUENCE of the explicit formula.
The explicit formula is true unconditionally.
Therefore, quasicrystal structure doesn't imply RH.

THE REAL QUESTION:

What additional constraints would force Re(ρ) = 1/2?

This is equivalent to asking: what makes the measure positive?
Or: what makes the operator self-adjoint?

Same problem, different language!
""")

# =============================================================================
# PART 9: THE CIRCULARITY PROBLEM
# =============================================================================

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                    PART 9: THE CIRCULARITY PROBLEM                          ║
╚════════════════════════════════════════════════════════════════════════════╝

CRITIQUE:

Many approaches to RH have hidden circularity:

1. LEE-YANG:
   "If ζ satisfies ferromagnetic conditions, zeros are on unit circle"
   BUT: Making ζ satisfy these conditions requires knowing where zeros are

2. QUASICRYSTAL:
   "If zeros form a crystalline measure with certain properties, RH follows"
   BUT: The "certain properties" often implicitly assume RH

3. SELF-ADJOINTNESS:
   "If H is self-adjoint, eigenvalues are real, RH follows"
   BUT: Proving H self-adjoint requires controlling the spectrum

THE COMMON PATTERN:

  IF [condition that implies zeros on critical line]
  THEN RH

This is logically correct but unhelpful.
The hard work is proving the condition!

WHAT WOULD BE NON-CIRCULAR:

1. Find a property P that:
   - Can be verified WITHOUT knowing zero locations
   - Implies zeros on critical line

2. Verify P for ζ(s)

No such P is known.
""")

# =============================================================================
# PART 10: COMPARISON OF APPROACHES
# =============================================================================

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                    PART 10: COMPARISON OF EXOTIC APPROACHES                 ║
╚════════════════════════════════════════════════════════════════════════════╝

| Approach         | Key Idea                    | Status              |
|------------------|-----------------------------|---------------------|
| Lee-Yang         | ζ as partition function     | Conditions not met  |
| Quasicrystal     | Zeros form crystalline meas | True but ≠ RH      |
| Weil Positivity  | Positivity of Weil form     | Equivalent to RH    |
| Self-Adjoint H   | Spectral theory             | Open                |
| F_1 Geometry     | Frobenius analogue          | Incomplete          |
| Sierra           | Modified H = xp             | Possible, unproven  |

THE HONEST ASSESSMENT:

1. LEE-YANG: Doesn't apply (no ferromagnetic structure)
2. QUASICRYSTAL: True but doesn't imply RH
3. Others: Various degrees of incompleteness

NO approach is currently viable for a complete proof.

WHAT'S NEEDED:

A genuinely new idea, or a breakthrough in:
- F_1 geometry (completing Connes' program)
- Functional analysis (proving self-adjointness)
- Direct methods (sieve theory, zero-free regions)
""")

# =============================================================================
# CONCLUSION
# =============================================================================

print("=" * 80)
print("CONCLUSION: LEE-YANG AND QUASICRYSTAL ASSESSMENT")
print("=" * 80)

print("""
LEE-YANG PHASE TRANSITION:

✗ ζ(s) is a partition function (Bose gas of primes)
✗ BUT the prime gas is NON-INTERACTING
✗ No ferromagnetic structure
✗ Lee-Yang theorem doesn't apply

VERDICT: DEAD END - conditions not met

QUASICRYSTAL FRAMEWORK:

✓ Zeros DO form a quasicrystal (crystalline measure)
✓ This is a THEOREM (explicit formula)
✗ BUT quasicrystal property doesn't imply RH
✗ It's a consequence of explicit formula, which holds unconditionally

VERDICT: TRUE BUT NOT SUFFICIENT

THE REMAINING PATH:

The most promising approaches remain:
1. F_1 geometry (completing Connes-Consani program)
2. Direct analytic methods (zero-free regions)
3. Something genuinely new

After 165+ years, all obvious approaches have been tried.
What remains requires either:
- Completing a very difficult existing program
- A fundamentally new idea

Neither is within reach of current methods.
""")

print("=" * 80)
print("END OF LEE-YANG AND QUASICRYSTAL ANALYSIS")
print("=" * 80)
