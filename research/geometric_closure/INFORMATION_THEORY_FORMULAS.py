"""
INFORMATION_THEORY_FORMULAS.py
==============================
Shannon Entropy, Channel Capacity, and Information from Z² = 8 × (4π/3)

Why is information discrete? Why does channel capacity exist?
The CUBE × SPHERE geometry provides the foundations.

Carl Zimmerman, March 2026
DOI: 10.5281/zenodo.19244651
"""

from math import pi, sqrt, log, log2, exp

# ═══════════════════════════════════════════════════════════════════════════
# FUNDAMENTAL CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════

Z2 = 8 * (4 * pi / 3)  # = 32π/3
Z = sqrt(Z2)           # = 5.7888100365...
alpha = 1 / (4 * Z2 + 3)

print("=" * 78)
print("INFORMATION THEORY FROM Z² = 8 × (4π/3)")
print("=" * 78)
print(f"\nZ² = {Z2:.8f}")
print(f"Z  = {Z:.10f}")

# ═══════════════════════════════════════════════════════════════════════════
# PART 1: THE BIT AND WHY IT EXISTS
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 1: WHY THE BIT?")
print("═" * 78)

print("""
The bit (binary digit) is the fundamental unit of information.

    1 bit = log₂(2) = 1

From Z²:
    The factor 2 in Z = 2√(8π/3) is why bits are fundamental!
    
    2 = the smallest non-trivial distinction
    2 = yes/no, on/off, 0/1
    2 = worldsheet dimensions
    2 = subject/object split
    
If the universe were based on Z = √(8π/3) (no factor 2):
    There would be no natural binary distinction.
    Information would be fundamentally different.

The bit exists because Z = 2 × (something).
The factor 2 is the origin of discrete information.
""")

print(f"Factor 2 in Z: Z = 2 × √(8π/3) = 2 × {sqrt(8*pi/3):.6f}")
print(f"1 bit = log₂(2) = {log2(2):.0f}")
print(f"The bit exists because 2 is in Z!")

# ═══════════════════════════════════════════════════════════════════════════
# PART 2: SHANNON ENTROPY
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 2: SHANNON ENTROPY")
print("═" * 78)

print("""
Shannon entropy (information content):

    H(X) = -Σ p(x) log₂(p(x)) bits

For uniform distribution over n outcomes:
    H = log₂(n)

From Z²:
    CUBE with 8 vertices → H = log₂(8) = 3 bits
    Z² as system → H = log₂(Z²) = log₂(33.51) = 5.07 bits
    
Key entropies:
    - 1 bit: distinguishing 2 states (factor 2)
    - 3 bits: CUBE (2³ = 8 states)
    - ~5 bits: Z² system
    - 6 bits: CUBE² = 64 states (codons!)
    - 10 bits: Z⁴ × 9/π² = 1024 states
""")

H_2 = log2(2)
H_cube = log2(8)
H_Z2 = log2(Z2)
H_codon = log2(64)
H_1024 = log2(1024)

print(f"Shannon entropy for different systems:")
print(f"  2 states (bit): H = {H_2:.0f} bit")
print(f"  8 states (CUBE): H = {H_cube:.0f} bits")
print(f"  Z² states: H = {H_Z2:.2f} bits")
print(f"  64 states (codons): H = {H_codon:.0f} bits")
print(f"  1024 states (Z⁴×9/π²): H = {H_1024:.0f} bits")

# ═══════════════════════════════════════════════════════════════════════════
# PART 3: CHANNEL CAPACITY
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 3: CHANNEL CAPACITY")
print("═" * 78)

print("""
Shannon's channel capacity theorem:

    C = B log₂(1 + S/N) bits/second

where B = bandwidth, S/N = signal-to-noise ratio.

The factor log₂ appears because information is binary!

From Z²:
    At S/N = 1: C = B × log₂(2) = B bits/s
    At S/N = 7: C = B × log₂(8) = 3B bits/s (CUBE!)
    At S/N = Z²-1: C = B × log₂(Z²) = 5.07B bits/s
    
The magical SNR values:
    1 → 1 bit (factor 2)
    7 → 3 bits (CUBE vertices)
    ~33 → 5 bits (Z²)
    63 → 6 bits (codons)
""")

C_snr1 = log2(1 + 1)
C_snr7 = log2(1 + 7)
C_snrZ2 = log2(1 + Z2 - 1)
C_snr63 = log2(1 + 63)

print(f"Channel capacity (per bandwidth):")
print(f"  S/N = 1: C/B = log₂(2) = {C_snr1:.0f} bit/s")
print(f"  S/N = 7: C/B = log₂(8) = {C_snr7:.0f} bits/s (CUBE)")
print(f"  S/N ≈ Z²: C/B = log₂(Z²) = {C_snrZ2:.2f} bits/s")
print(f"  S/N = 63: C/B = log₂(64) = {C_snr63:.0f} bits/s (codons)")

# ═══════════════════════════════════════════════════════════════════════════
# PART 4: DATA COMPRESSION
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 4: DATA COMPRESSION (SOURCE CODING)")
print("═" * 78)

print("""
Shannon's source coding theorem:
    You cannot compress n i.i.d. symbols below n × H(X) bits.

Compression ratio limited by entropy!

From Z²:
    English text: H ≈ 1.0-1.5 bits/character (highly redundant)
    Random text: H = log₂(26) = 4.7 bits/character
    
    Interestingly: 4.7 ≈ Z - 1 = 4.79!
    
    Random 26-letter text ≈ (Z - 1) bits/character.
    
DNA compression:
    4 bases → 2 bits/base (theoretical minimum)
    But redundancy exists (codons, genes)
    Actual: ~1.8 bits/base
    
    1.8 ≈ Z/3.2 or (Z-1)/2.7
""")

H_english = 1.3  # approximate
H_random_26 = log2(26)
Z_minus_1 = Z - 1

print(f"Entropy comparisons:")
print(f"  English: H ≈ {H_english} bits/char")
print(f"  Random 26-letter: H = log₂(26) = {H_random_26:.2f} bits/char")
print(f"  Z - 1 = {Z_minus_1:.2f}")
print(f"  Random text entropy ≈ Z - 1!")

# ═══════════════════════════════════════════════════════════════════════════
# PART 5: ERROR CORRECTION
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 5: ERROR CORRECTION CODES")
print("═" * 78)

print("""
Error correction adds redundancy to protect information.

Hamming bound: For t-error correcting code with n bits, k data bits:
    2^k × Σ_{i=0}^{t} C(n,i) ≤ 2^n

Perfect codes saturate this bound.

Famous codes:
    [7,4,3] Hamming code: 4 data bits + 3 parity = 7 total
    [23,12,7] Golay code: 12 data + 11 parity = 23 total
    
From Z²:
    7 ≈ Z + 1.2
    23 ≈ 4Z = 4 × 5.79 = 23.16
    
The Golay code's total length ≈ 4Z!

Also:
    12 = 9Z²/(8π) = gauge dimension (data bits in Golay)
    11 ≈ 2Z (parity bits in Golay)
""")

print(f"Hamming [7,4,3]: total = 7 ≈ Z + 1.2 = {Z + 1.2:.1f}")
print(f"Golay [23,12,7]: total = 23 ≈ 4Z = {4*Z:.1f}")
print(f"  Data bits: 12 = 9Z²/(8π) = {9*Z2/(8*pi):.0f} (gauge!)")
print(f"  Parity bits: 11 ≈ 2Z = {2*Z:.1f}")

# ═══════════════════════════════════════════════════════════════════════════
# PART 6: MUTUAL INFORMATION
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 6: MUTUAL INFORMATION")
print("═" * 78)

print("""
Mutual information: How much X tells about Y.

    I(X;Y) = H(X) + H(Y) - H(X,Y)
           = H(X) - H(X|Y)

Properties:
    I(X;Y) ≥ 0 (information is non-negative)
    I(X;Y) = I(Y;X) (symmetric)
    I(X;X) = H(X) (self-information = entropy)

From Z²:
    Mutual information connects CUBE to SPHERE!
    
    If X = CUBE state, Y = SPHERE position:
    I(CUBE; SPHERE) = H(CUBE) = 3 bits
    
    Perfect correlation: knowing CUBE determines SPHERE
    
    This is consciousness! (from CONSCIOUSNESS_FIRST_PRINCIPLES.py)
    Mind (CUBE) is perfectly correlated with experience (SPHERE).
""")

print(f"Self-information: I(CUBE;CUBE) = H(CUBE) = {log2(8):.0f} bits")
print(f"Maximum mutual info for CUBE: 3 bits")
print(f"Perfect correlation → consciousness!")

# ═══════════════════════════════════════════════════════════════════════════
# PART 7: KOLMOGOROV COMPLEXITY
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 7: KOLMOGOROV COMPLEXITY")
print("═" * 78)

print("""
Kolmogorov complexity: shortest program that produces string x.

    K(x) = min{|p| : U(p) = x}

Properties:
    - K(x) is uncomputable!
    - Random strings have K(x) ≈ |x|
    - Structured strings have K(x) << |x|

From Z²:
    Z² is highly structured despite its transcendental value.
    K(Z²) is very small: "8 × (4π/3)"
    
    Only ~15 characters describe Z²!
    K(Z²) ≈ 15 bytes ≈ 120 bits
    
    But Z² "contains" all of physics!
    This is the power of good compression.
    
    The universe's complexity:
    K(universe) ≈ K(Z²) + K(initial conditions)
                ≈ 120 bits + ???
""")

# Rough estimate of Z² description length
K_Z2_description = len("8*(4*pi/3)")
print(f"Description of Z²: '8*(4*pi/3)' = {K_Z2_description} characters")
print(f"K(Z²) ≈ {K_Z2_description * 8} bits")
print(f"Z² compresses the universe into ~100 bits!")

# ═══════════════════════════════════════════════════════════════════════════
# PART 8: QUANTUM INFORMATION
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 8: QUANTUM vs CLASSICAL INFORMATION")
print("═" * 78)

print("""
Quantum information uses qubits instead of bits.

    1 qubit = |α|²|0⟩ + |β|²|1⟩ with |α|² + |β|² = 1

Qubit lives on Bloch sphere (S²)!

From Z²:
    Classical bit: CUBE vertex (discrete)
    Qubit: SPHERE point (continuous)
    
    Classical: 0 or 1
    Quantum: anywhere on unit sphere
    
    Z² = CUBE × SPHERE = classical × quantum!
    
    One "Z² bit" contains:
    - 1 classical bit (log₂(2) = 1)
    - Infinite quantum amplitude (sphere has ∞ points)
    - Net accessible info: ~5 bits per Z² unit
    
Holevo bound: max classical info from n qubits = n bits
Despite infinite precision, you can only extract finite info!
""")

print(f"Classical bit: 2 states → 1 bit")
print(f"Qubit: sphere surface → ∞ states but 1 bit extractable")
print(f"Z² unit: CUBE × SPHERE → ~5 bits effective")

# ═══════════════════════════════════════════════════════════════════════════
# PART 9: ALGORITHMIC INFORMATION AND π
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 9: π AND INFORMATION")
print("═" * 78)

print("""
π appears in Z² = 8 × (4π/3) = 32π/3

π is transcendental: its digits contain "infinite information."

But π has very low Kolmogorov complexity:
    K(π) = just a few bytes (various formulas)
    
From Z²:
    π = 3Z²/32 (by construction)
    
    The infinite digits of π are determined by finite Z².
    
    This suggests:
    - The universe contains infinite detail
    - But all derivable from finite Z²
    - Information creates complexity
    
    π's digits pass all randomness tests.
    Yet π is completely deterministic!
    
    Z² is similarly "random-looking but determined."
""")

pi_from_Z = 3 * Z2 / 32
print(f"π = 3Z²/32 = {pi_from_Z:.15f}")
print(f"Actual π = {pi:.15f}")
print(f"Difference: {abs(pi_from_Z - pi):.2e}")
print(f"(This is exact by construction)")

# ═══════════════════════════════════════════════════════════════════════════
# PART 10: THE INFORMATION CONTENT OF THE UNIVERSE
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 10: COSMIC INFORMATION")
print("═" * 78)

print("""
Lloyd's estimate: The universe has computed ~10^120 ops on ~10^90 bits.

From Z²:
    Observable universe has ~10^80 particles.
    log₁₀(10^80) = 80 ≈ 14Z = 14 × 5.79 = 81
    
    So: N_particles ≈ 10^(14Z)
    
    Information in universe:
    I ~ N × log₂(states per particle)
    ~ 10^80 × (some factor)
    
    If factor ≈ 10^10 = 10^(2Z):
    I ~ 10^80 × 10^10 = 10^90 bits ✓
    
Bekenstein bound on cosmic information:
    I_max ~ A/(4ℓ_P²) ~ (R_H/ℓ_P)² ~ 10^122 bits
    
    122 ≈ 21Z = 21 × 5.79 = 122
    
    Cosmic information bound ≈ 10^(21Z) bits!
""")

particles = 80
particles_from_Z = 14 * Z

print(f"Particle count: 10^80")
print(f"14Z = {particles_from_Z:.0f}")
print(f"Universe particles ≈ 10^(14Z)")

print(f"\nBekenstein bound: ~10^122 bits")
print(f"21Z = {21 * Z:.0f}")
print(f"Cosmic info bound ≈ 10^(21Z) bits")

# ═══════════════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 78)
print("SUMMARY: INFORMATION THEORY FROM Z²")
print("=" * 78)

print("""
┌─────────────────────────────────────────────────────────────────────────────┐
│  INFORMATION THEORY FROM Z² = 8 × (4π/3)                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  THE BIT:                                                                   │
│  ────────                                                                   │
│  Factor 2 in Z = 2√(8π/3) → bits exist                     ← fundamental  │
│                                                                             │
│  SHANNON ENTROPY:                                                           │
│  ────────────────                                                           │
│  CUBE entropy: log₂(8) = 3 bits                            ← EXACT        │
│  Z² entropy: log₂(Z²) ≈ 5.07 bits                                          │
│                                                                             │
│  ERROR CORRECTION:                                                          │
│  ─────────────────                                                          │
│  Golay [23,12,7]: 23 ≈ 4Z, 12 = gauge dimension            ← remarkable   │
│                                                                             │
│  COMPRESSION:                                                               │
│  ────────────                                                               │
│  Random 26-letter text: log₂(26) ≈ Z - 1 bits/char         ← remarkable   │
│                                                                             │
│  QUANTUM INFO:                                                              │
│  ─────────────                                                              │
│  Classical = CUBE (discrete), Quantum = SPHERE (continuous)                │
│  Z² = classical × quantum information                                      │
│                                                                             │
│  COSMIC INFORMATION:                                                        │
│  ───────────────────                                                        │
│  Particles: ~10^(14Z), Bekenstein bound: ~10^(21Z)         ← from Z       │
│                                                                             │
│  KOLMOGOROV:                                                                │
│  ───────────                                                                │
│  K(Z²) ≈ 100 bits, but Z² describes all physics!                          │
│  Maximum compression = Z²                                                  │
│                                                                             │
│  KEY INSIGHT:                                                               │
│  ────────────                                                               │
│  Information = CUBE structure                                              │
│  Communication = CUBE → SPHERE → CUBE transfer                             │
│  The universe IS information, and information IS Z².                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
""")

print("=" * 78)
print("IT FROM BIT FROM Z²")
print("=" * 78)
