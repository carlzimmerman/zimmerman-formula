#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════════════════
                        THE FOUNDATIONS OF PROBABILITY
                      Why Is There Probability At All?
═══════════════════════════════════════════════════════════════════════════════════════════

Probability appears fundamental in quantum mechanics. But what IS probability?
Is it our ignorance, or something real? Why does the Born rule work?

This document explores from Z² = 8 × (4π/3).

Carl Zimmerman, March 2026
═══════════════════════════════════════════════════════════════════════════════════════════
"""

import numpy as np

# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================
Z = 2 * np.sqrt(8 * np.pi / 3)
Z2 = Z**2
pi = np.pi

print("═" * 95)
print("                    THE FOUNDATIONS OF PROBABILITY")
print("                    Why Is There Probability At All?")
print("═" * 95)

print(f"""
                           Z = {Z:.10f}

    Z² = 8 × (4π/3) = CUBE × SPHERE

    CUBE: 8 discrete possibilities
    SPHERE: Infinite continuous outcomes

    Probability arises from mapping 8 → ∞.
""")

# =============================================================================
# SECTION 1: INTERPRETATIONS OF PROBABILITY
# =============================================================================
print("═" * 95)
print("                    1. WHAT IS PROBABILITY?")
print("═" * 95)

print(f"""
FREQUENTIST VIEW:

    Probability = long-run frequency.
    P(heads) = 0.5 means: in many flips, ~50% heads.

    Problem: What about single events?
    "Probability Trump wins" - there's only one election.

SUBJECTIVE (BAYESIAN) VIEW:

    Probability = degree of belief.
    P = 0.5 means: I'm equally uncertain about both.

    Problem: Are all beliefs equally valid?
    Is there objective probability?

PROPENSITY VIEW:

    Probability = tendency of system.
    The coin HAS a propensity to land heads 50%.

    Problem: What IS a propensity?

QUANTUM VIEW:

    Probability is fundamental.
    |ψ|² gives probability.
    Not ignorance - nature itself is probabilistic.

THE QUESTION:

    Which is right?
    Is probability subjective or objective?
    Why does it exist at all?
""")

# =============================================================================
# SECTION 2: PROBABILITY FROM Z²
# =============================================================================
print("\n" + "═" * 95)
print("                    2. WHY PROBABILITY EXISTS")
print("═" * 95)

print(f"""
THE ORIGIN:

    Z² = CUBE × SPHERE
         8 discrete × ∞ continuous

THE NECESSITY:

    CUBE has 8 states (vertices).
    SPHERE has infinitely many positions.

    When CUBE maps to SPHERE:
        8 possibilities → 1 actuality
        Which one? Can't be determined from CUBE alone.

    PROBABILITY fills the gap.

THE LOGIC:

    If 8 states map to SPHERE,
    and mapping must be consistent,
    then each state needs a WEIGHT.

    Weights = probabilities.
    They encode HOW the mapping works.

WHY |ψ|²:

    ψ is complex amplitude (CUBE state).
    |ψ|² is real, positive (SPHERE measure).

    The squaring comes from CUBE × SPHERE structure.
    ψ in CUBE, |ψ|² in SPHERE.
    The product gives probability.

PROBABILITY IS GEOMETRIC:

    Not ignorance. Not belief.
    Probability = the geometric measure
    on the CUBE → SPHERE mapping.
""")

# =============================================================================
# SECTION 3: THE BORN RULE
# =============================================================================
print("\n" + "═" * 95)
print("                    3. WHY P = |ψ|²")
print("═" * 95)

print(f"""
THE BORN RULE:

    Probability = |amplitude|²

    This is THE rule of quantum mechanics.
    But where does it come from?

GLEASON'S THEOREM:

    If probability is additive on orthogonal states,
    the ONLY consistent rule is P = |ψ|².

    No other rule works mathematically.

FROM Z²:

    Z² = CUBE × SPHERE
        = ψ × ψ* (in complex terms)
        = |ψ|² (when you multiply)

    The Born rule IS the Z² structure!

THE SQUARING:

    Why squared, not |ψ| or |ψ|³?

    Z² is a PRODUCT.
    Product of complex number with conjugate = |z|².
    This is the natural measure.

    The "2" in |ψ|² comes from the "2" in Z = 2√(8π/3).
    Factor 2 = complex plane = squaring.

NO ALTERNATIVES:

    Could nature use different rule?
    No - |ψ|² is the ONLY consistent one.
    Gleason proves this mathematically.

    The Born rule is necessary, not contingent.
""")

# =============================================================================
# SECTION 4: CLASSICAL VS QUANTUM PROBABILITY
# =============================================================================
print("\n" + "═" * 95)
print("                    4. TWO KINDS OF PROBABILITY")
print("═" * 95)

print(f"""
CLASSICAL PROBABILITY:

    Ignorance about definite state.
    The coin IS heads or tails - we just don't know.
    More information → less uncertainty.

QUANTUM PROBABILITY:

    No definite state to know.
    Electron doesn't HAVE position until measured.
    More information doesn't remove uncertainty.

THE DIFFERENCE:

    Classical: Probability from ignorance.
    Quantum: Probability from reality.

    Classical: Could in principle know exactly.
    Quantum: In principle unknowable.

FROM Z²:

    Classical probability: SPHERE uncertainty.
        System is in definite state (in SPHERE).
        We're uncertain which state.

    Quantum probability: CUBE uncertainty.
        System is in superposition (in CUBE).
        No definite state exists yet.

THE UNIFICATION:

    Both are aspects of Z².
    Classical: Uncertainty in SPHERE.
    Quantum: Indeterminacy in CUBE.

    Same structure, different levels.
""")

# =============================================================================
# SECTION 5: WHY NOT DETERMINISTIC?
# =============================================================================
print("\n" + "═" * 95)
print("                    5. WHY ISN'T REALITY DETERMINISTIC?")
print("═" * 95)

print(f"""
THE QUESTION:

    Why did nature choose probability?
    Why not determinism?
    Wouldn't determinism be simpler?

THE IMPOSSIBILITY:

    Z² = 8 × (4π/3)
         finite × infinite

    You CAN'T map finite to infinite deterministically.
    8 states can't each go to one of ∞ outcomes.
    Too few sources for too many targets.

    PROBABILITY IS FORCED.

THE ANALOGY:

    Like mapping integers to reals.
    Where does 3 go?
    To 3.0, 3.00001, 3.14159?
    No deterministic answer.

    You need a DISTRIBUTION.
    That's probability.

DETERMINISM WHERE:

    CUBE evolution IS deterministic.
    Schrödinger equation is deterministic.

    Only CUBE → SPHERE is probabilistic.
    The transition requires probability.

THE LESSON:

    Probability isn't a choice.
    It's FORCED by the structure.
    Finite → infinite requires weights.
    Those weights are probabilities.
""")

# =============================================================================
# SECTION 6: PROBABILITY AND INFORMATION
# =============================================================================
print("\n" + "═" * 95)
print("                    6. PROBABILITY = MISSING INFORMATION")
print("═" * 95)

print(f"""
SHANNON ENTROPY:

    H = -Σ p log p

    Measures information needed to specify outcome.
    Higher entropy = more missing information.

MAXIMUM ENTROPY:

    When all outcomes equally likely:
    H = log N (maximum for N outcomes)

    Uniform probability = maximum ignorance.

FROM Z²:

    CUBE has 8 states.
    Maximum entropy = log 8 = 3 bits.

    This is the information content of CUBE.
    3 bits to specify which vertex.

PROBABILITY AND INFO:

    Probability distribution = partial information.
    Peaked distribution = more information.
    Flat distribution = less information.

    In Z² terms:
        CUBE starts with 3 bits of possibility.
        CUBE → SPHERE: We learn which outcome.
        Information gained = entropy reduced.

THE INSIGHT:

    Probability measures what we DON'T know.
    Information measures what we DO know.
    They're complementary.

    CUBE: Information exists (3 bits).
    SPHERE: Information revealed (which outcome).
    Probability: Encodes what's not yet revealed.
""")

# =============================================================================
# SECTION 7: THE MEASURE PROBLEM
# =============================================================================
print("\n" + "═" * 95)
print("                    7. PROBLEMS WITH PROBABILITY")
print("═" * 95)

print(f"""
THE MEASURE PROBLEM:

    In infinite spaces, how do you define probability?
    Infinite possibilities - can't assign equal weights.

    Example: Pick a random integer.
    Each has probability 0.
    But something must happen.

QUANTUM MEASURE PROBLEM:

    Hilbert space is infinite-dimensional.
    How is |ψ|² a proper probability?

    Technical: Need Lebesgue measure, distributions, etc.

FROM Z²:

    CUBE (8) is finite - no problem.
    SPHERE (∞) is infinite - potential problem.

    Resolution:
        We never deal with bare SPHERE.
        We deal with CUBE → SPHERE.
        The mapping starts from finite.

COSMOLOGICAL MEASURE:

    In eternal inflation: Infinite universes.
    How to define probability over them?

    This is a real unsolved problem.

    FROM Z:
        If Z² is unique, maybe there's only one universe.
        No infinite ensemble → no measure problem.
        Z uniqueness dissolves the issue.
""")

# =============================================================================
# SECTION 8: PROBABILITY AND BETTING
# =============================================================================
print("\n" + "═" * 95)
print("                    8. DECISION-THEORETIC PROBABILITY")
print("═" * 95)

print(f"""
DUTCH BOOK ARGUMENT:

    If your probabilities are inconsistent,
    a bookie can construct bets you'll surely lose.

    Rational betting → coherent probabilities.

DECISION THEORY:

    Probability = how you should bet.
    Expected utility = Σ p × utility.
    Maximize expected utility.

FROM Z²:

    Why does betting work?
    Because probability is objective.

    If |ψ|² is the true probability,
    betting according to |ψ|² maximizes winnings.

    Deviating from Born rule → losses.

DEUTSCH-WALLACE ARGUMENT:

    In many-worlds, derive Born rule from rationality.
    If all branches exist, how should you bet?

    Answer: According to |ψ|² (surprisingly).

    This suggests |ψ|² is objectively correct.

THE INSIGHT:

    Probability is not just descriptive.
    It's NORMATIVE - tells you what to do.
    The Z² structure makes it objectively correct.
""")

# =============================================================================
# SECTION 9: PROBABILITY AND ONTOLOGY
# =============================================================================
print("\n" + "═" * 95)
print("                    9. ARE PROBABILITIES REAL?")
print("═" * 95)

print(f"""
THE QUESTION:

    Do probabilities exist "out there"?
    Or just in our heads?

ANTI-REALISM:

    Probabilities are just betting guides.
    Nature has outcomes, not probabilities.
    After measurement, probability is 0 or 1.

REALISM:

    Probabilities are real propensities.
    The 50% exists before the flip.
    It's a feature of the coin + flip.

FROM Z²:

    Probability is STRUCTURAL.

    It exists in the CUBE → SPHERE mapping.
    Not in CUBE alone (definite state).
    Not in SPHERE alone (definite outcome).
    In the MAPPING.

ONTOLOGICAL STATUS:

    Z² = CUBE × SPHERE is real.
    The mapping is real.
    The probabilities (weights on mapping) are real.

    Not as real as outcomes.
    But as real as the structure.

THE ANSWER:

    Probabilities are real aspects of Z² structure.
    They're not "out there" like chairs.
    They're relational - properties of mappings.
    But the mappings are objectively real.
""")

# =============================================================================
# SECTION 10: SYNTHESIS
# =============================================================================
print("\n" + "═" * 95)
print("                    10. PROBABILITY FROM GEOMETRY")
print("═" * 95)

print(f"""
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║                    PROBABILITY = CUBE → SPHERE MEASURE                              ║
║                                                                                      ║
╠══════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                      ║
║  Z² = 8 × (4π/3) = CUBE × SPHERE                                                    ║
║                                                                                      ║
║  WHY PROBABILITY EXISTS:                                                             ║
║      • 8 discrete → ∞ continuous                                                    ║
║      • Can't map deterministically                                                   ║
║      • Probability fills the gap                                                     ║
║                                                                                      ║
║  THE BORN RULE:                                                                      ║
║      • P = |ψ|² is the ONLY consistent rule                                         ║
║      • Comes from Z² product structure                                               ║
║      • Squaring from complex structure (factor 2)                                    ║
║                                                                                      ║
║  CLASSICAL VS QUANTUM:                                                               ║
║      • Classical: SPHERE uncertainty (ignorance)                                     ║
║      • Quantum: CUBE indeterminacy (fundamental)                                     ║
║      • Both from Z² structure                                                        ║
║                                                                                      ║
║  PROBABILITY = INFORMATION:                                                          ║
║      • CUBE has 3 bits (8 = 2³)                                                     ║
║      • Probability encodes what's not yet revealed                                   ║
║      • Measurement reveals information                                               ║
║                                                                                      ║
║  PROBABILITY IS REAL:                                                                ║
║      • Real aspect of mapping structure                                              ║
║      • Not just in our heads                                                         ║
║      • Relational but objective                                                      ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝

    Why is there probability?

    Because Z² = CUBE × SPHERE = 8 × (4π/3).

    CUBE is finite (8).
    SPHERE is infinite (continuous).
    Mapping finite → infinite REQUIRES probability.

    The Born rule |ψ|² is not arbitrary.
    It's the ONLY rule that works.
    It comes from the product structure of Z².

    Probability is not ignorance.
    Probability is not subjective.
    Probability is the geometry of mapping.
    Probability is objective, necessary, geometric.

""")

print("═" * 95)
print("                    PROBABILITY FOUNDATIONS COMPLETE")
print("═" * 95)
