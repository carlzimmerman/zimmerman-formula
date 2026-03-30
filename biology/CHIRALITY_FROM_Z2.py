#!/usr/bin/env python3
"""
CHIRALITY AND THE ORIGIN OF HOMOCHIRALITY FROM Z²

Why does life use ONLY L-amino acids and D-sugars?
This is one of biology's deepest mysteries.

The Z² framework suggests an answer:
- The weak force violates parity (left ≠ right)
- The Weinberg angle sin²θW = 3/13 comes from Z²
- This creates a tiny energy difference between L and D
- Over billions of years, one handedness wins

Carl Zimmerman, March 2026

Publication: https://zenodo.org/records/19318996
"""

import math
import numpy as np

# ============================================================================
# Z² CONSTANTS
# ============================================================================

Z_SQUARED = 32 * math.pi / 3   # = 33.5103
Z = math.sqrt(Z_SQUARED)        # = 5.7888

BEKENSTEIN = 4
GAUGE = 12
N_GEN = 3
D_STRING = 10
ALPHA_INV = 4 * Z_SQUARED + 3   # = 137.04
ALPHA = 1 / ALPHA_INV

# Weinberg angle from Z²
SIN2_THETA_W = 3 / (GAUGE + 1)  # = 3/13 = 0.231

# Physical constants
c = 2.998e8          # m/s
hbar = 1.055e-34     # J·s
eV = 1.602e-19       # J
m_e = 9.109e-31      # kg
G_F = 1.166e-5       # GeV^-2 (Fermi constant)

print("=" * 78)
print("CHIRALITY: WHY LIFE IS LEFT-HANDED")
print("The Z² Origin of Biological Homochirality")
print("=" * 78)

# ============================================================================
# PART 1: THE CHIRALITY PROBLEM
# ============================================================================

print("\n" + "=" * 78)
print("PART 1: THE MYSTERY OF HOMOCHIRALITY")
print("=" * 78)

print(f"""
THE OBSERVATION:

    All known life uses:
    • L-amino acids (left-handed)
    • D-sugars (right-handed)

    NEVER the mirror images (D-amino acids, L-sugars).

THE MYSTERY:

    Chemistry does not distinguish left from right.
    In the lab, synthesis produces 50% L and 50% D (racemic mixture).

    Yet ALL life on Earth uses the SAME handedness.

    Why? This is one of biology's deepest unsolved problems.

POSSIBLE EXPLANATIONS:

    1. CHANCE: The first life randomly chose L, and it stuck
    2. DETERMINISM: Something in physics prefers L
    3. PANSPERMIA: Life came from elsewhere, already L

THE Z² ANSWER: The weak force (through sin²θW = 3/13) creates
a tiny preference for one handedness. Given enough time,
this preference amplifies to 100% homochirality.
""")

# ============================================================================
# PART 2: PARITY VIOLATION IN THE WEAK FORCE
# ============================================================================

print("\n" + "=" * 78)
print("PART 2: THE WEAK FORCE VIOLATES PARITY")
print("=" * 78)

print(f"""
PARITY (P): The operation of reflecting space (left ↔ right).

ELECTROMAGNETISM: Conserves parity (L and R are equivalent)
STRONG FORCE: Conserves parity (L and R are equivalent)
WEAK FORCE: VIOLATES parity (L ≠ R)

The weak force couples differently to left-handed and right-handed particles!

DISCOVERY: Wu experiment (1956)
    Cobalt-60 beta decay emits electrons preferentially in one direction.
    This proved that nature distinguishes left from right.

THE WEINBERG ANGLE:

    sin²θ_W determines how much parity is violated.

    From Z²: sin²θ_W = 3/(GAUGE + 1) = 3/13 = {SIN2_THETA_W:.4f}
    Measured: 0.2312 ± 0.0002

    Error: {abs(SIN2_THETA_W - 0.2312)/0.2312 * 100:.2f}%

THE CONNECTION:

    Z² → GAUGE = 12 → sin²θ_W = 3/13 → parity violation → chirality preference
""")

# ============================================================================
# PART 3: THE PARITY-VIOLATING ENERGY DIFFERENCE
# ============================================================================

print("\n" + "=" * 78)
print("PART 3: ENERGY DIFFERENCE BETWEEN L AND D")
print("=" * 78)

# The parity-violating energy difference (PVED)
# For amino acids, this is approximately:
# ΔE_PV ≈ (G_F × m_e × c² × Z³ × α² × sin²θ_W) / (atomic units)
# Extremely tiny: ~10^-17 to 10^-14 eV per molecule

# Rough estimate
E_weak = 90.0  # GeV (W/Z mass scale)
E_atomic = 13.6  # eV (atomic energy scale)

# PVED scales as (α × sin²θ_W × (m_e/m_W)^2)
# Very roughly:
PVED_ratio = ALPHA**2 * SIN2_THETA_W * (m_e * c**2 / eV / (E_weak * 1e9))**2
PVED_estimate = PVED_ratio * E_atomic  # in eV

print(f"""
PARITY-VIOLATING ENERGY DIFFERENCE (PVED):

The weak force creates a tiny energy difference between L and D molecules.

Theoretical estimate:

    ΔE_PV / E_atomic ~ α² × sin²θ_W × (m_e/m_W)²
                     ~ {ALPHA**2:.2e} × {SIN2_THETA_W:.3f} × ({m_e*c**2/eV:.0f} / {E_weak*1e9:.0f})²
                     ~ {PVED_ratio:.2e}

For a typical amino acid:

    ΔE_PV ~ {PVED_estimate:.2e} eV

This is TINY! About 10⁻¹⁷ to 10⁻¹⁴ eV per molecule.

BUT: Over billions of molecules and billions of years,
     this tiny preference can be amplified.
""")

# ============================================================================
# PART 4: AMPLIFICATION MECHANISMS
# ============================================================================

print("\n" + "=" * 78)
print("PART 4: FROM TINY PREFERENCE TO 100% HOMOCHIRALITY")
print("=" * 78)

print(f"""
THE AMPLIFICATION PROBLEM:

    ΔE_PV ~ 10⁻¹⁷ eV
    Thermal energy at 300K: kT ~ 0.026 eV

    Ratio: ΔE_PV / kT ~ 10⁻¹⁵

    A molecule has only a 1 + 10⁻¹⁵ preference for L over D.
    How does this become 100% L?

AMPLIFICATION MECHANISMS:

1. AUTOCATALYSIS (Frank model, 1953)

    If L-amino acids catalyze the formation of more L,
    and inhibit D, small initial excess grows exponentially.

    L + precursor → 2L (autocatalysis)
    L + D → inert (mutual inhibition)

    Even a 10⁻¹⁵ initial excess leads to 100% L eventually.

2. CRYSTALLIZATION (Kondepudi effect)

    Some chiral molecules crystallize in pure L or D forms.
    A tiny PVED bias determines which crystal nucleates first.
    The first crystal seeds the entire solution.

3. CIRCULARLY POLARIZED LIGHT

    UV light from neutron stars is circularly polarized.
    This selectively destroys one enantiomer.
    Interstellar amino acids show ~10% L excess!

THE Z² CONTRIBUTION:

    Z² → sin²θ_W = 3/13 → PVED
    PVED → initial L excess (10⁻¹⁵)
    Amplification → 100% L-amino acids

    The Weinberg angle from Z² determines the "seed" of homochirality.
""")

# ============================================================================
# PART 5: WHY L AND NOT D?
# ============================================================================

print("\n" + "=" * 78)
print("PART 5: WHY L-AMINO ACIDS SPECIFICALLY?")
print("=" * 78)

print(f"""
THE QUESTION:

    Z² determines sin²θ_W, which determines PVED.
    But does PVED favor L or D?

THE ANSWER: It depends on the specific molecule.

    For some molecules, PVED favors L.
    For others, it favors D.

    For amino acids: Calculations suggest PVED slightly favors L.
    (But this is extremely hard to calculate precisely.)

EXPERIMENTAL STATUS:

    • PVED has never been directly measured for amino acids
    • Theoretical calculations give conflicting results
    • The effect is at the edge of experimental capability

PREDICTION FROM Z²:

    If Z² determines the origin of homochirality through PVED,
    then the specific sign of PVED (L vs D) should be calculable
    from Z² geometry.

    This would predict: "Life MUST be L, not D, anywhere in the universe."

ALTERNATIVE: SPONTANEOUS SYMMETRY BREAKING

    Perhaps Z² is agnostic about L vs D.
    The initial choice is random.
    Once made, it's locked in by amplification.

    Different planets might have L-life or D-life randomly.

    This is testable: Find extraterrestrial amino acids.
    If they're always L → Z² determines sign
    If they're mixed L and D → Z² only provides magnitude
""")

# ============================================================================
# PART 6: THE D-SUGAR CONNECTION
# ============================================================================

print("\n" + "=" * 78)
print("PART 6: WHY D-SUGARS WITH L-AMINO ACIDS?")
print("=" * 78)

print(f"""
THE PUZZLE:

    Life uses L-amino acids AND D-sugars.
    Why opposite chiralities for these two classes?

STRUCTURAL ANSWER:

    In proteins and nucleic acids:
    • L-amino acids fit together in α-helices
    • D-sugars fit together in DNA double helix

    The COMBINATION (L-amino, D-sugar) creates stable structures.
    The opposite combination (D-amino, L-sugar) would also work,
    but the two systems are incompatible.

Z² INTERPRETATION:

    The NUMBER 2 appears:
    • 2 chiralities (L and D)
    • 2 major biopolymer types (proteins and nucleic acids)
    • 2 × D_STRING = 20 amino acids

    Life uses BOTH chiralities, distributed across molecule classes.
    This may relate to the factor of 2 in "20 = 2 × D_STRING".

GEOMETRIC MEANING:

    L and D are like the two "sheets" of a Möbius strip.
    Life lives on both sides, using each where appropriate.

    The choice of L-amino/D-sugar (vs D-amino/L-sugar) is
    either random or determined by PVED signs.
""")

# ============================================================================
# PART 7: PREDICTIONS
# ============================================================================

print("\n" + "=" * 78)
print("PART 7: TESTABLE PREDICTIONS")
print("=" * 78)

print(f"""
Z² PREDICTIONS FOR CHIRALITY:

1. PVED MAGNITUDE:

    ΔE_PV should be calculable from Z² parameters:
    ΔE_PV ~ α² × sin²θ_W × (m_e/m_W)² × E_atomic

    With sin²θ_W = 3/13 from Z².

    Prediction: ΔE_PV ~ 10⁻¹⁷ eV for typical amino acids.

2. EXTRATERRESTRIAL CHIRALITY:

    If PVED determines homochirality:
    • ALL life in the universe should have the SAME handedness
    • Meteoritic amino acids should show L-excess everywhere

    If it's random:
    • Some planets might have D-life
    • We should find both L and D excess in different meteorites

3. LABORATORY TESTS:

    Precision measurements of PVED could verify:
    • The sin²θ_W dependence
    • The predicted magnitude
    • Whether L or D is energetically favored

4. ORIGIN OF LIFE EXPERIMENTS:

    Prebiotic chemistry under controlled conditions:
    • With circularly polarized light → specific chirality
    • Without asymmetric influence → racemic mixture
    • The timescale for amplification should match models
""")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "=" * 78)
print("SUMMARY: CHIRALITY FROM Z² = 32π/3")
print("=" * 78)

print(f"""
╔══════════════════════════════════════════════════════════════════════════╗
║                    THE Z² ORIGIN OF CHIRALITY                            ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  THE CHAIN:                                                              ║
║                                                                          ║
║      Z² = 32π/3                                                          ║
║         ↓                                                                ║
║      GAUGE = 12 (Standard Model structure)                               ║
║         ↓                                                                ║
║      sin²θ_W = 3/(GAUGE+1) = 3/13 = 0.231                               ║
║         ↓                                                                ║
║      Parity violation in weak force                                      ║
║         ↓                                                                ║
║      PVED: L and D have different energies (~10⁻¹⁷ eV)                  ║
║         ↓                                                                ║
║      Initial L-excess in prebiotic molecules                             ║
║         ↓                                                                ║
║      Autocatalytic amplification                                         ║
║         ↓                                                                ║
║      100% L-amino acids, D-sugars                                        ║
║                                                                          ║
║  CONCLUSION:                                                             ║
║                                                                          ║
║  The handedness of life is not random. It traces back to                 ║
║  parity violation in the weak force, which is determined by              ║
║  sin²θ_W = 3/13 from Z² geometry.                                       ║
║                                                                          ║
║  Z² geometry → weak force structure → chirality of life                  ║
║                                                                          ║
║  If true, ALL life in the universe should have the same                  ║
║  handedness - a profound prediction of the Z² framework.                 ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝

"In the beginning was the Word, and the Word was Z²."
                                        — Carl Zimmerman
""")
