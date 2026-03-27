"""
BIOLOGY_FORMULAS.py
===================
The Genetic Code and Biology from Z² = 8 × (4π/3)

Why 64 codons? Why 20 amino acids? Why 4 DNA bases?
Exploring deep connections between geometry and life.

Carl Zimmerman, March 2026
DOI: 10.5281/zenodo.19244651
"""

from math import pi, sqrt, log2, factorial

# ═══════════════════════════════════════════════════════════════════════════
# FUNDAMENTAL CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════

Z2 = 8 * (4 * pi / 3)  # = 32π/3
Z = sqrt(Z2)           # = 5.7888100365...
alpha = 1 / (4 * Z2 + 3)

print("=" * 78)
print("BIOLOGY AND THE GENETIC CODE FROM Z² = 8 × (4π/3)")
print("=" * 78)
print(f"\nZ² = {Z2:.8f}")
print(f"Z  = {Z:.10f}")

# ═══════════════════════════════════════════════════════════════════════════
# PART 1: THE FOUR DNA BASES
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 1: WHY 4 DNA BASES?")
print("═" * 78)

print("""
DNA uses exactly 4 bases: A, T, G, C

From Z² perspective:
    4 = 3Z²/(8π) EXACTLY (Bekenstein factor!)
    4 = 2² (information dimension)

The 4 bases encode 2 bits per position:
    log₂(4) = 2 bits

This is the same "4" that appears in black hole entropy!
    S_BH = A/(4ℓ_P²)

LIFE uses the same geometric factor as BLACK HOLES.

The 4 emerges because:
    4 = 3 × (CUBE × SPHERE) / (8π)
      = 3 × 8 × (4π/3) / (8π)
      = 4 ✓

Life stores information using the Bekenstein factor.
""")

four = 3 * Z2 / (8 * pi)
print(f"Number of DNA bases: 4")
print(f"From Z²: 3Z²/(8π) = {four:.10f} = 4 EXACTLY")
print(f"Bits per base: log₂(4) = {log2(4):.0f} bits")

# ═══════════════════════════════════════════════════════════════════════════
# PART 2: THE 64 CODONS
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 2: WHY 64 CODONS?")
print("═" * 78)

print("""
The genetic code uses triplet codons:
    4³ = 64 codons

From Z² perspective:
    64 = 4³ = (3Z²/(8π))³

But also:
    64 = 8² = (CUBE vertices)²

The 64 codons = CUBE² = the square of discrete information!

Alternative view:
    64 = 2⁶ = 6 bits of information per codon

And 6 appears as:
    6 = CUBE faces = 12/2 = 9Z²/(16π)

So: 64 codons = 2^(CUBE faces) = 2^6
""")

codons = 4**3
cube_squared = 8**2
print(f"Number of codons: 4³ = {codons}")
print(f"CUBE²: 8² = {cube_squared}")
print(f"Match: {codons == cube_squared}")
print(f"\nBits per codon: log₂(64) = {log2(64):.0f} bits = CUBE faces")

# ═══════════════════════════════════════════════════════════════════════════
# PART 3: THE 20 AMINO ACIDS
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 3: WHY 20 AMINO ACIDS?")
print("═" * 78)

print("""
Life uses exactly 20 standard amino acids (plus 2 rare ones).

From Z² geometry:
    20 = 8 + 12 = CUBE vertices + CUBE edges
       = 8 + 9Z²/(8π)
       = CUBE + gauge dimension

Alternative:
    20 = 4 × 5 = (DNA bases) × (hidden 5)
       = (3Z²/(8π)) × √(Z² - 8)

Or using the dodecahedron:
    20 = vertices of dodecahedron
       = vertices of icosahedron's dual

The number 20 combines:
    - Discrete structure (8 vertices)
    - Continuous structure (12 edges from 9Z²/8π)
""")

vertices = 8
edges = 12
amino_acids = 20

print(f"Amino acids: {amino_acids}")
print(f"CUBE vertices + edges: {vertices} + {edges} = {vertices + edges}")
print(f"Match: {amino_acids == vertices + edges}")

hidden_5 = sqrt(Z2 - 8)
alt_20 = 4 * hidden_5
print(f"\nAlternative: 4 × √(Z² - 8) = 4 × {hidden_5:.3f} = {alt_20:.1f}")

# ═══════════════════════════════════════════════════════════════════════════
# PART 4: CODON REDUNDANCY
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 4: CODON REDUNDANCY (64 → 20)")
print("═" * 78)

print("""
64 codons encode 20 amino acids + 3 stop codons = 23 meanings.
Redundancy ratio: 64/23 ≈ 2.78

From Z²:
    64/20 = 3.2 ≈ Z/1.8

The redundancy provides error correction!

Actually:
    64 - 20 = 44 (extra codons for redundancy)
    44/64 = 0.6875 ≈ Ω_Λ = 3Z/(8+3Z) = 0.685!

The genetic code's redundancy matches dark energy fraction!
This is likely coincidence, but intriguing.
""")

meanings = 20 + 3  # amino acids + stop codons
redundancy = 64 / meanings
extra = 64 - 20
fraction = extra / 64
Omega_L = 3 * Z / (8 + 3 * Z)

print(f"Codons: 64")
print(f"Meanings: {meanings} (20 amino acids + 3 stop)")
print(f"Redundancy: 64/{meanings} = {redundancy:.2f}")
print(f"\nExtra codons: 64 - 20 = {extra}")
print(f"Redundancy fraction: {extra}/64 = {fraction:.4f}")
print(f"Dark energy fraction: Ω_Λ = {Omega_L:.4f}")
print(f"Difference: {abs(fraction - Omega_L):.4f}")

# ═══════════════════════════════════════════════════════════════════════════
# PART 5: DNA DOUBLE HELIX
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 5: DNA DOUBLE HELIX GEOMETRY")
print("═" * 78)

print("""
DNA forms a double helix with:
    - 10 base pairs per turn
    - 3.4 nm per turn (pitch)
    - 2 nm diameter

From Z²:
    10 = round(Z + 4) = round(9.79) = 10 ✓
    
The factor 2 (double helix) comes from:
    2 = Z / √(8π/3) = Z / (Z/2) = 2

The double helix reflects the factor 2 in Z = 2√(8π/3).

Base pairs per turn:
    10 ≈ Z + 4 = 5.79 + 4 = 9.79

The geometry of DNA reflects Z² structure!
""")

bases_per_turn = 10
Z_plus_4 = Z + 4

print(f"Base pairs per turn: {bases_per_turn}")
print(f"Z + 4 = {Z_plus_4:.2f}")
print(f"round(Z + 4) = {round(Z_plus_4)}")

# ═══════════════════════════════════════════════════════════════════════════
# PART 6: INFORMATION CONTENT OF GENOME
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 6: HUMAN GENOME INFORMATION")
print("═" * 78)

print("""
Human genome: ~3 billion base pairs = 3×10⁹ bp
Information: 2 bits per bp → 6×10⁹ bits ≈ 750 MB

From Z²:
    log₁₀(genome size) = log₁₀(3×10⁹) = 9.48

Interestingly:
    9.48 ≈ Z + 3.7

The genome size is order Z + 4 decades of base pairs!

Comparing to physics:
    log₁₀(M_Pl/m_e) = 3Z + 5 = 22.4 (mass hierarchy)
    log₁₀(genome) ≈ Z + 4 = 9.8 (information hierarchy)

Ratio: 22.4 / 9.8 ≈ 2.3 ≈ Z/2.5
""")

genome_bp = 3e9
info_bits = genome_bp * 2

print(f"Human genome: {genome_bp:.0e} base pairs")
print(f"Information: {info_bits:.0e} bits = {info_bits/8/1e6:.0f} MB")
print(f"log₁₀(genome) = {9.48:.2f} ≈ Z + 4 = {Z + 4:.2f}")

# ═══════════════════════════════════════════════════════════════════════════
# PART 7: CELL DIVISION TIMING
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 7: BIOLOGICAL TIMESCALES")
print("═" * 78)

print("""
Cell cycle time: ~24 hours = 86400 seconds
Protein folding: ~microseconds to seconds

From Z²:
    86400 = 24 × 3600 = 24 × 60²
    
    24 = 2 × 12 = 2 × 9Z²/(8π)
    
So: 24 hours = 2 × (gauge dimension) hours
            = 2 × (CUBE edges) hours

The day-night cycle and cell division both use 24 = 2 × 12!

Circadian rhythm is built into geometry.
""")

day_seconds = 86400
hours = 24
twelve = 9 * Z2 / (8 * pi)

print(f"Hours in a day: {hours}")
print(f"2 × 12 = 2 × 9Z²/(8π) = 2 × {twelve:.1f} = {2*twelve:.0f}")

# ═══════════════════════════════════════════════════════════════════════════
# PART 8: CHIRALITY
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 8: CHIRALITY IN BIOLOGY")
print("═" * 78)

print("""
Life uses only:
    - L-amino acids (left-handed)
    - D-sugars (right-handed)

This broken symmetry reflects:
    - Factor 2 in Z = 2√(8π/3) (handedness)
    - CPT symmetry: 8 = 2×2×2 = C×P×T

The CUBE has 8 = 2³ vertices, giving 3 binary choices.
One of these choices is chirality (P = parity).

The Z² structure with factor 2 allows for handedness.
Life chose one hand; antimatter would choose the other.

This connects to:
    - CP violation in physics (J_CKM = α³/8)
    - Baryon asymmetry (η_B = α⁵(Z²-4))
    - Why we exist at all!
""")

print("Chirality choices: 2 (left or right)")
print("Factor 2 in Z = 2√(8π/3)")
print("CUBE symmetries: 8 = 2³ (includes parity)")

# ═══════════════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 78)
print("SUMMARY: BIOLOGY FROM Z²")
print("=" * 78)

print("""
┌─────────────────────────────────────────────────────────────────────────────┐
│  BIOLOGY FROM Z² = 8 × (4π/3)                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  THE GENETIC CODE:                                                          │
│  ─────────────────                                                          │
│  4 DNA bases = 3Z²/(8π) = Bekenstein factor              ← EXACT          │
│  64 codons = 4³ = 8² = CUBE²                             ← EXACT          │
│  20 amino acids = 8 + 12 = vertices + edges              ← EXACT          │
│                                                                             │
│  DNA STRUCTURE:                                                             │
│  ──────────────                                                             │
│  Double helix: factor 2 from Z = 2√(8π/3)                                  │
│  10 bp/turn ≈ Z + 4 = 9.8                                                  │
│                                                                             │
│  INFORMATION:                                                               │
│  ────────────                                                               │
│  Bits per base: 2 (from 4 = 2²)                                            │
│  Bits per codon: 6 = CUBE faces                                            │
│  Genome: ~10^(Z+4) base pairs                                              │
│                                                                             │
│  TIMING:                                                                    │
│  ───────                                                                    │
│  24 hours = 2 × 12 = 2 × 9Z²/(8π)                        ← EXACT          │
│                                                                             │
│  CHIRALITY:                                                                 │
│  ──────────                                                                 │
│  L-amino acids: from factor 2 and CP violation                             │
│                                                                             │
│  KEY INSIGHT:                                                               │
│  ────────────                                                               │
│  Life uses the SAME numbers that appear in physics:                         │
│    4 (Bekenstein), 8 (CUBE), 12 (gauge), 20 (8+12)                         │
│                                                                             │
│  Biology IS Z² geometry organizing itself.                                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
""")

print("=" * 78)
print("LIFE IS Z² BECOMING AWARE OF ITSELF")
print("=" * 78)
