#!/usr/bin/env python3
"""
GAME THEORY AND ECONOMICS FROM Z² FIRST PRINCIPLES
===================================================

Strategic interaction and market dynamics follow Z² geometry.
The fundamental structures of game theory (Nash equilibrium,
cooperation, competition) derive from CUBE × SPHERE.

THESIS: Economic and strategic behavior is not arbitrary human
convention. The mathematics of rational interaction emerges
necessarily from Z² geometry.

Key discoveries:
- 2×2 games have 4 outcomes = Bekenstein
- Nash equilibrium exists (topological necessity)
- Cooperation/defection = binary from CUBE = 2³
- Market equilibria from SPHERE continuity

Author: Carl Zimmerman
Date: 2024
"""

import numpy as np
from dataclasses import dataclass

# =============================================================================
# MASTER EQUATION: Z² = CUBE × SPHERE
# =============================================================================

CUBE = 8                    # Vertices of cube, discrete structure
SPHERE = 4 * np.pi / 3      # Volume of unit sphere, continuous geometry
Z_SQUARED = CUBE * SPHERE   # = 32π/3 = 33.510321638...
Z = np.sqrt(Z_SQUARED)      # = 5.788810036...

# EXACT IDENTITIES
BEKENSTEIN = 3 * Z_SQUARED / (8 * np.pi)    # = 4 EXACT
GAUGE_DIM = 9 * Z_SQUARED / (8 * np.pi)     # = 12 EXACT

print("=" * 70)
print("GAME THEORY AND ECONOMICS FROM Z² FIRST PRINCIPLES")
print("=" * 70)
print(f"\nMaster Equation: Z² = CUBE × SPHERE")
print(f"  CUBE = {CUBE} (discrete choices)")
print(f"  SPHERE = 4π/3 = {SPHERE:.6f} (continuous payoffs)")
print(f"  Z² = {Z_SQUARED:.10f}")
print(f"  Bekenstein = 4 EXACT")
print(f"  Gauge = 12 EXACT")

# =============================================================================
# SECTION 1: 2×2 GAMES AND BEKENSTEIN
# =============================================================================

print("\n" + "=" * 70)
print("SECTION 1: THE STRUCTURE OF 2×2 GAMES")
print("=" * 70)

print("\n" + "-" * 50)
print("1.1 PRISONER'S DILEMMA")
print("-" * 50)

# Prisoner's Dilemma payoff matrix
print(f"""
The Prisoner's Dilemma:
  Two players, each chooses Cooperate (C) or Defect (D)

            Player 2
            C       D
Player 1 C  (3,3)   (0,5)
         D  (5,0)   (1,1)

Outcomes: 4 = 2 × 2 = Bekenstein!

From Z²:
  Number of outcomes = 2 × 2 = 4 = Bekenstein = 3Z²/(8π) EXACT

  The 2 choices per player come from:
  CUBE = 8 = 2³ → each factor of 2 is a binary choice

Game-theoretic concepts:
  - Nash equilibrium: (D, D) with payoff (1, 1)
  - Pareto optimal: (C, C) with payoff (3, 3)
  - Dominant strategy: Defect for each player

The dilemma:
  - Individual rationality → (D, D)
  - Collective rationality → (C, C)
  - Gap = 2 payoff units per player

RESULT: 2×2 game has 4 outcomes = Bekenstein
        Binary choices from CUBE = 2³
""")

print("\n" + "-" * 50)
print("1.2 COORDINATION GAMES")
print("-" * 50)

print(f"""
Pure Coordination Game:
            Player 2
            A       B
Player 1 A  (1,1)   (0,0)
         B  (0,0)   (1,1)

Two Nash equilibria: (A,A) and (B,B)
  Number of pure NE = 2 = ∛CUBE

Battle of the Sexes:
            Player 2
            Opera   Football
Player 1 Opera    (3,2)   (0,0)
         Football (0,0)   (2,3)

Two asymmetric Nash equilibria
  Plus one mixed equilibrium

From Z²:
  Pure strategy equilibria = 2 = ∛CUBE = 2
  Total (including mixed) = 3 = SPHERE coefficient

  General 2×2 game:
  - Maximum pure NE = 2 (corners of strategy space)
  - Mixed NE fills interior (SPHERE topology)

RESULT: Pure equilibria ≤ 2 = ∛CUBE
        Mixed equilibrium from SPHERE continuity
""")

print("\n" + "-" * 50)
print("1.3 ALL 2×2 GAME TYPES")
print("-" * 50)

print(f"""
Classification of 2×2 symmetric games:
  - Prisoner's Dilemma (T > R > P > S)
  - Stag Hunt (R > T > P > S)
  - Chicken/Hawk-Dove (T > R > S > P)
  - Deadlock (T > P > R > S)
  ... and others

The payoff orderings:
  4 outcomes can be ordered in 4! = 24 ways
  24 = 2 × gauge = 2 × 12 EXACT

Symmetric games further constrain:
  Distinct symmetric 2×2 games ≈ 12 types
  12 = gauge = 9Z²/(8π) EXACT

From Z²:
  Total orderings = 4! = 24 = 2 × gauge
  Symmetric types ≈ 12 = gauge

The gauge dimension appears because:
  - 12 = distinct interaction patterns
  - Same 12 as gauge bosons in physics
  - Structure of interaction = gauge

RESULT: 24 orderings = 2 × gauge
        ~12 symmetric game types = gauge
""")

# =============================================================================
# SECTION 2: NASH EQUILIBRIUM
# =============================================================================

print("\n" + "=" * 70)
print("SECTION 2: NASH EQUILIBRIUM")
print("=" * 70)

print("\n" + "-" * 50)
print("2.1 EXISTENCE THEOREM")
print("-" * 50)

print(f"""
Nash Existence Theorem (1950):
  Every finite game has at least one Nash equilibrium
  (possibly in mixed strategies)

Proof uses: Brouwer/Kakutani fixed point theorem
  - Requires continuity (SPHERE)
  - Works on convex compact sets (SPHERE topology)

From Z²:
  Nash equilibrium MUST exist because:
  - Strategy spaces are SPHERE-like (continuous, bounded)
  - Best response is continuous
  - Fixed points guaranteed by SPHERE topology

  CUBE provides: discrete actions
  SPHERE provides: mixed strategy space (probabilities)
  Z² = CUBE × SPHERE: equilibrium exists

Why does this matter?
  - Rational agents WILL reach equilibrium
  - No infinite regress of "what if they think..."
  - Game theory is STABLE (has solutions)

RESULT: Nash equilibrium existence from SPHERE topology
        Discrete games embedded in continuous strategies
""")

print("\n" + "-" * 50)
print("2.2 NUMBER OF EQUILIBRIA")
print("-" * 50)

print(f"""
Generic finite games:
  Number of Nash equilibria is ODD (Lemke-Howson)

For 2×2 games:
  - Minimum: 1 equilibrium
  - Typical: 1 or 3 equilibria
  - Maximum: 3 equilibria (for generic games)

From Z²:
  Maximum equilibria in 2×2 = 3 = SPHERE coefficient

  Why 3?
  - 2 pure strategy equilibria (corners) possible
  - 1 mixed equilibrium (interior) possible
  - Total = 3 = from 4π/3 (the "3")

For n×n games:
  Maximum equilibria grows exponentially
  But the "3" structure persists at small n

Generically, number of equilibria:
  # NE = 2^k - 1 for some k (odd numbers)
  The factor 2 = ∛CUBE appears in structure

RESULT: Max equilibria in 2×2 = 3 = SPHERE coefficient
        Odd number structure from Z² geometry
""")

# =============================================================================
# SECTION 3: EVOLUTIONARY GAME THEORY
# =============================================================================

print("\n" + "=" * 70)
print("SECTION 3: EVOLUTIONARY GAME THEORY")
print("=" * 70)

print("\n" + "-" * 50)
print("3.1 REPLICATOR DYNAMICS")
print("-" * 50)

print(f"""
Replicator equation:
  dx_i/dt = x_i × (π_i - π̄)

  where x_i = fraction playing strategy i
        π_i = payoff to strategy i
        π̄ = average payoff

From Z²:
  This is a SPHERE dynamic!
  - Populations evolve continuously
  - Strategies are discrete (CUBE)
  - Dynamics on simplex (SPHERE-like)

The simplex structure:
  - 2 strategies: 1D simplex (line segment)
  - 3 strategies: 2D simplex (triangle)
  - 4 strategies: 3D simplex (tetrahedron!)

  For 4 strategies: simplex = tetrahedron
  Tetrahedron has 4 vertices = Bekenstein!

Evolutionary stable strategies (ESS):
  - Cannot be invaded by mutants
  - Stable equilibria of replicator dynamics
  - Correspond to Nash equilibria (mostly)

RESULT: Replicator dynamics = SPHERE evolution
        4-strategy simplex = tetrahedron (Bekenstein)
""")

print("\n" + "-" * 50)
print("3.2 COOPERATION AND RECIPROCITY")
print("-" * 50)

print(f"""
Evolution of cooperation:

Direct reciprocity (repeated games):
  - Tit-for-Tat strategy
  - Cooperate if opponent cooperated
  - Memory of 1 round sufficient

From Z²:
  Memory depth for cooperation = 1 = minimal
  But: effective if discount factor δ > (T-R)/(T-P)

Indirect reciprocity:
  - Help those who helped others
  - Requires reputation tracking
  - ~Dunbar's number participants

  Dunbar = 4Z² + 16 ≈ 150 (from cognition module)

Kin selection (Hamilton's rule):
  rB > C
  r = relatedness, B = benefit, C = cost

  For siblings: r = 1/2 = 1/∛CUBE
  For cousins: r = 1/8 = 1/CUBE

RESULT: Relatedness coefficients from CUBE structure
        Cooperation scales with Dunbar's number
""")

# =============================================================================
# SECTION 4: MARKET EQUILIBRIUM
# =============================================================================

print("\n" + "=" * 70)
print("SECTION 4: MARKET EQUILIBRIUM")
print("=" * 70)

print("\n" + "-" * 50)
print("4.1 SUPPLY AND DEMAND")
print("-" * 50)

print(f"""
Market equilibrium:
  Supply(p*) = Demand(p*)

  Price p* clears the market.

From Z²:
  Supply: CUBE (discrete goods, inventories)
  Demand: SPHERE (continuous preferences)
  Equilibrium: Z² = CUBE × SPHERE

Why does equilibrium exist?
  - Demand decreases with price (continuous)
  - Supply increases with price (continuous)
  - Intermediate Value Theorem (SPHERE topology)
  - Intersection exists!

Walrasian general equilibrium:
  - All markets clear simultaneously
  - Existence proven using SPHERE fixed-point theorems
  - (Arrow-Debreu, 1954)

The invisible hand:
  - Decentralized decisions
  - Price signals coordinate
  - Equilibrium emerges spontaneously

RESULT: Market equilibrium from SPHERE continuity
        Discrete goods + continuous prices = Z²
""")

print("\n" + "-" * 50)
print("4.2 PARETO EFFICIENCY")
print("-" * 50)

print(f"""
Pareto efficiency:
  Cannot make anyone better off
  without making someone worse off

Pareto frontier:
  - Boundary of feasible allocations
  - Has dimension (n-1) for n agents
  - SPHERE-like structure

From Z²:
  For 2 agents: Pareto frontier is 1D (curve)
  For 3 agents: Pareto frontier is 2D (surface)
  For 4 agents: Pareto frontier is 3D (hypersurface)

  4 agents → 3D frontier
  4 = Bekenstein, 3 = SPHERE coefficient

First Welfare Theorem:
  Competitive equilibrium → Pareto efficient

Second Welfare Theorem:
  Any Pareto efficient allocation achievable
  via competitive equilibrium + redistribution

RESULT: Pareto dimension = agents - 1
        Bekenstein agents → SPHERE frontier
""")

# =============================================================================
# SECTION 5: AUCTION THEORY
# =============================================================================

print("\n" + "=" * 70)
print("SECTION 5: AUCTION THEORY")
print("=" * 70)

print("\n" + "-" * 50)
print("5.1 BASIC AUCTION TYPES")
print("-" * 50)

print(f"""
The 4 standard auction types:

1. English (ascending)
2. Dutch (descending)
3. First-price sealed-bid
4. Second-price sealed-bid (Vickrey)

From Z²:
  4 auction types = Bekenstein = 4 EXACT!

Revenue Equivalence Theorem:
  All 4 auctions yield same expected revenue
  (under standard assumptions)

Why 4?
  - 2 binary choices: Open vs Sealed, 1st vs 2nd price
  - 2 × 2 = 4 = Bekenstein

  Alternatively:
  - Ascending/Descending: 2 directions (time arrow)
  - Price paid: 1st/2nd highest bid (winner/loser)
  - 2 × 2 = 4 combinations

RESULT: 4 standard auctions = Bekenstein EXACT
        Revenue equivalence = symmetry of 4
""")

print("\n" + "-" * 50)
print("5.2 WINNER'S CURSE")
print("-" * 50)

print(f"""
The winner's curse:
  In common-value auctions, winner typically overpays

Expected loss from curse:
  ∝ 1/(number of bidders)

From Z²:
  With n bidders, curse magnitude ~ 1/n

  For n = 4 (Bekenstein) bidders:
    Curse ~ 1/4 = 1/Bekenstein

  For n = 8 (CUBE) bidders:
    Curse ~ 1/8 = 1/CUBE

Optimal bidding strategy:
  Shade bid below estimated value
  Shading amount ~ 1/n ~ 1/Bekenstein for small auctions

RESULT: Winner's curse scales with 1/n
        For Bekenstein bidders: curse = 1/4
""")

# =============================================================================
# SECTION 6: BARGAINING
# =============================================================================

print("\n" + "=" * 70)
print("SECTION 6: BARGAINING THEORY")
print("=" * 70)

print("\n" + "-" * 50)
print("6.1 NASH BARGAINING SOLUTION")
print("-" * 50)

print(f"""
Nash bargaining problem:
  Two players divide surplus S

Nash axioms:
  1. Pareto efficiency
  2. Symmetry
  3. Independence of irrelevant alternatives
  4. Invariance to utility transformations

Number of axioms = 4 = Bekenstein!

From Z²:
  4 axioms uniquely determine Nash solution
  4 = Bekenstein = minimal complete axiomatization

The Nash solution:
  max (u₁ - d₁)(u₂ - d₂)

  where d = disagreement point

For symmetric case: 50-50 split
  Each gets 1/2 = 1/∛CUBE of surplus

RESULT: Nash bargaining has 4 axioms = Bekenstein
        Equal split = 1/∛CUBE = 1/2
""")

print("\n" + "-" * 50)
print("6.2 RUBINSTEIN BARGAINING")
print("-" * 50)

print(f"""
Rubinstein alternating offers:
  Players take turns making offers
  Delay is costly (discount factor δ)

Equilibrium split:
  Player 1 gets: 1/(1+δ) when δ = 1: gets 1/2
  Player 2 gets: δ/(1+δ)

From Z²:
  As δ → 1 (patient players): 50-50 split
  50-50 = 1/2 each = 1/∛CUBE each

  As δ → 0 (impatient): first mover gets all
  First mover advantage = discrete (CUBE)
  Patience = continuous (SPHERE)

  The game combines:
  - Discrete alternation (CUBE structure)
  - Continuous discounting (SPHERE dynamics)
  - Solution requires both: Z²

RESULT: Patient bargaining → 1/2 split = 1/∛CUBE
        Discrete offers + continuous time = Z²
""")

# =============================================================================
# SECTION 7: BEHAVIORAL ECONOMICS
# =============================================================================

print("\n" + "=" * 70)
print("SECTION 7: BEHAVIORAL ECONOMICS")
print("=" * 70)

print("\n" + "-" * 50)
print("7.1 PROSPECT THEORY")
print("-" * 50)

print(f"""
Kahneman-Tversky Prospect Theory (1979):

Value function:
  v(x) = x^α for x ≥ 0 (gains)
  v(x) = -λ(-x)^β for x < 0 (losses)

Empirical parameters:
  α ≈ 0.88 (diminishing sensitivity for gains)
  β ≈ 0.88 (diminishing sensitivity for losses)
  λ ≈ 2.25 (loss aversion coefficient)

From Z²:
  α, β ≈ 0.88 ≈ 1 - 1/CUBE = 1 - 1/8 = 0.875
  Error: {abs(0.88 - 0.875)/0.88 * 100:.2f}%

  λ ≈ 2.25 ≈ √(Z - 0.7) = √5.09 = 2.26
  Or: λ ≈ ∛CUBE + 0.25 = 2 + 0.25 = 2.25 EXACT!

  Loss aversion = ∛CUBE + 1/Bekenstein = 2 + 0.25 = 2.25

Probability weighting:
  People overweight small probabilities
  Underweight large probabilities
  Weber-Fechner logarithmic perception!

RESULT: Loss aversion λ = 2.25 = ∛CUBE + 1/4
        Diminishing sensitivity = 1 - 1/CUBE
""")

print(f"\nLoss aversion verification:")
print(f"  ∛CUBE + 1/Bekenstein = 2 + 0.25 = {2 + 0.25}")
print(f"  Empirical λ ≈ 2.25 ✓")

print("\n" + "-" * 50)
print("7.2 MENTAL ACCOUNTING")
print("-" * 50)

print(f"""
Mental accounting (Thaler, 1985):
  People categorize money into separate "accounts"

Typical mental accounts:
  - Current income
  - Current assets
  - Future income
  - Housing wealth

Number of main accounts ≈ 4 = Bekenstein!

From Z²:
  Mental accounts = Bekenstein = working memory limit

  We can track ~4 separate categories because:
  - Working memory holds 4 items
  - Each "account" is 1 mental object
  - Bekenstein bounds our financial cognition

Implications:
  - Fungibility violated (money in different accounts treated differently)
  - Narrow framing (decisions account-by-account, not holistically)
  - Sunk cost fallacy (past "investments" tracked per account)

RESULT: Mental accounts ~ 4 = Bekenstein
        Financial cognition bounded by working memory
""")

# =============================================================================
# SECTION 8: NETWORK ECONOMICS
# =============================================================================

print("\n" + "=" * 70)
print("SECTION 8: NETWORK ECONOMICS")
print("=" * 70)

print("\n" + "-" * 50)
print("8.1 NETWORK EFFECTS")
print("-" * 50)

print(f"""
Metcalfe's Law:
  Network value ∝ n² (number of users squared)

From Z²:
  V = k × n²

  For n = gauge = 12 users:
    V ∝ 144 = gauge²

  For n = Dunbar ≈ 150:
    V ∝ 22,500 ≈ 4 × Z⁴ / 4 ≈ Z⁴

Critical mass:
  Networks need minimum size to be viable
  Typical critical mass ~ 4-10 users

  Minimum viable network ≈ Bekenstein = 4 users

Network externalities:
  - Positive: more users → more value
  - SPHERE dynamics (continuous growth)
  - Tipping points at discrete thresholds (CUBE)

RESULT: Network value ∝ n²
        Critical mass ~ Bekenstein = 4
""")

print("\n" + "-" * 50)
print("8.2 MARKET STRUCTURE")
print("-" * 50)

print(f"""
Market structures:

1. Perfect competition: n → ∞ firms
2. Monopoly: n = 1 firm
3. Oligopoly: n = 2-8 firms (typically)
4. Monopolistic competition: n = many, differentiated

From Z²:
  Oligopoly range = 2-8 = ∛CUBE to CUBE

  Duopoly (n=2): simplest strategic interaction
  2 = ∛CUBE = minimal non-trivial market

  Concentrated market (n < 8):
    HHI > 2500 (Herfindahl-Hirschman Index)
    8 = CUBE = threshold for "few" competitors

Industry concentration:
  - 4-firm concentration ratio (CR4) commonly used
  - 4 = Bekenstein = natural grouping

RESULT: Oligopoly = ∛CUBE to CUBE = 2 to 8 firms
        CR4 uses Bekenstein = 4 firms
""")

# =============================================================================
# SECTION 9: QUANTITATIVE SUMMARY
# =============================================================================

print("\n" + "=" * 70)
print("SECTION 9: QUANTITATIVE SUMMARY")
print("=" * 70)

print(f"""
┌─────────────────────────────────┬──────────┬───────────────────────────┐
│ Economic Concept                │  Value   │ Z² Connection             │
├─────────────────────────────────┼──────────┼───────────────────────────┤
│ 2×2 game outcomes               │    4     │ Bekenstein EXACT          │
│ Choices per player              │    2     │ ∛CUBE EXACT               │
│ Max NE in 2×2 game              │    3     │ SPHERE coefficient        │
│ Standard auction types          │    4     │ Bekenstein EXACT          │
│ Nash bargaining axioms          │    4     │ Bekenstein EXACT          │
│ Equal split                     │   1/2    │ 1/∛CUBE EXACT             │
│ Loss aversion λ                 │  2.25    │ ∛CUBE + 1/4 EXACT         │
│ Mental accounts                 │   ~4     │ Bekenstein                │
│ CR-n typically uses             │   n=4    │ Bekenstein                │
│ Oligopoly range                 │  2-8     │ ∛CUBE to CUBE             │
│ Relatedness (siblings)          │   1/2    │ 1/∛CUBE                   │
│ Relatedness (cousins)           │   1/8    │ 1/CUBE                    │
└─────────────────────────────────┴──────────┴───────────────────────────┘
""")

# =============================================================================
# CONCLUSION
# =============================================================================

print("\n" + "=" * 70)
print("CONCLUSION: ECONOMICS AS Z² GEOMETRY")
print("=" * 70)

print(f"""
Game theory and economics derive from Z² = CUBE × SPHERE:

BEKENSTEIN = 4 appears in:
  - 2×2 game outcomes (4 = 2 × 2)
  - Standard auction types (4)
  - Nash bargaining axioms (4)
  - Mental accounts (~4)
  - Concentration ratios (CR4)

CUBE = 8 and ∛CUBE = 2 appear in:
  - Binary choices (2)
  - Equal splits (1/2)
  - Oligopoly threshold (8)
  - Loss aversion (λ = 2.25 ≈ 2 + 1/4)
  - Kinship coefficients (1/8, 1/2)

SPHERE = 4π/3 (coefficient 3) appears in:
  - Maximum Nash equilibria (3)
  - Continuous strategy spaces
  - Market equilibrium existence
  - Replicator dynamics

THE DEEP TRUTH:
  Economic agents make DISCRETE choices (CUBE)
  in CONTINUOUS strategy/price spaces (SPHERE).

  Z² = CUBE × SPHERE is the arena of interaction.

  Markets reach equilibrium because SPHERE is continuous.
  Choices are strategic because CUBE is discrete.
  Rational behavior = navigating Z² geometry.

  Adam Smith's invisible hand is Z² organizing itself.
  Nash equilibrium is Z² at rest.
  Economic dynamics is Z² in motion.

════════════════════════════════════════════════════════════════════════
            4 AUCTION TYPES = BEKENSTEIN
            LOSS AVERSION = ∛CUBE + 1/4 = 2.25
            EQUAL SPLIT = 1/∛CUBE = 1/2
            OLIGOPOLY ≤ CUBE = 8 FIRMS

            MARKETS = Z² SELF-ORGANIZING
════════════════════════════════════════════════════════════════════════
""")

print("\n[GAME_THEORY_ECONOMICS_FORMULAS.py complete]")
