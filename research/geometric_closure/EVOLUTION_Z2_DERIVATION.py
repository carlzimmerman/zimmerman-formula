#!/usr/bin/env python3
"""
EVOLUTION: Z² GEOMETRY OF ADAPTATION
=====================================

How does life evolve? Darwin's theory of natural selection
can be understood through Z² geometry.

Evolution = CUBE variation × SPHERE selection = Z² adaptation

Z² = CUBE × SPHERE = 8 × (4π/3) = 32π/3
Bekenstein = 3Z²/(8π) = 4
Gauge = 9Z²/(8π) = 12

Author: Carl Zimmerman
Date: 2026
"""

import numpy as np

# =============================================================================
# ZIMMERMAN CONSTANTS
# =============================================================================

CUBE = 8
SPHERE = 4 * np.pi / 3
Z_SQUARED = CUBE * SPHERE
Z = np.sqrt(Z_SQUARED)
BEKENSTEIN = 3 * Z_SQUARED / (8 * np.pi)  # = 4
GAUGE = 9 * Z_SQUARED / (8 * np.pi)       # = 12

print("=" * 70)
print("EVOLUTION: Z² MECHANISM OF ADAPTATION")
print("=" * 70)

# =============================================================================
# PART 1: THE DARWIN EQUATION
# =============================================================================

print("\n" + "=" * 70)
print("PART 1: THE DARWIN EQUATION - Z² EVOLUTION")
print("=" * 70)

print(f"""
DARWIN'S INSIGHT:

  Evolution requires 3 conditions (SPHERE coefficient!):

  1. VARIATION
     - Individuals differ
     - Heritable differences
     - This is CUBE: discrete genetic variants

  2. SELECTION
     - Some variants survive/reproduce better
     - Environmental pressure
     - This is SPHERE: continuous fitness landscape

  3. INHERITANCE
     - Successful variants pass on traits
     - DNA replication
     - This is Z²: CUBE information × SPHERE time

THE EVOLUTION EQUATION:

  Δp = p(1-p) × s × h

  where:
    p = frequency of allele
    s = selection coefficient
    h = dominance

  This is the Price Equation in simplified form.

Z² INTERPRETATION:

  p(1-p) = SPHERE term (variance, continuous)
  s = CUBE term (discrete fitness difference)
  h = Z² coupling (how genotype maps to phenotype)

  Evolution = CUBE × SPHERE = Z²

RATE OF EVOLUTION:

  Fisher's Fundamental Theorem:
    dW/dt = V_A

  Rate of fitness increase = Additive genetic variance

  V_A is the SPHERE of genetic possibilities.
  Selection acts as CUBE filter.
  Result: Z² adaptation.
""")

# =============================================================================
# PART 2: MUTATION - CUBE ERRORS
# =============================================================================

print("=" * 70)
print("PART 2: MUTATION - CUBE VARIATION")
print("=" * 70)

print(f"""
MUTATION AS CUBE EVENTS:

  Mutations are DISCRETE changes to DNA.
  They are the raw material for evolution.

MUTATION TYPES (Bekenstein = 4?):

  1. POINT MUTATIONS
     - Single nucleotide changes
     - Transitions (Pu↔Pu, Py↔Py)
     - Transversions (Pu↔Py)

  2. INSERTIONS/DELETIONS (Indels)
     - Add or remove bases
     - Can cause frameshifts

  3. DUPLICATIONS
     - Copy segments
     - Gene duplication → new functions

  4. CHROMOSOMAL REARRANGEMENTS
     - Inversions, translocations
     - Large-scale changes

  4 major types = Bekenstein!

MUTATION RATES:

  DNA polymerase error rate: ~10⁻¹⁰ per bp per replication
  (After proofreading and mismatch repair)

  Human genome: 3.2 × 10⁹ bp
  Mutations per generation: ~3.2 × 10⁹ × 10⁻¹⁰ × 2 ≈ 0.6

  Actually, observed: ~70 new mutations per generation
  (Includes germline-specific effects)

  70 ≈ 2 × Z² ≈ 2 × 33.5 = 67 (close!)

THE 4 NUCLEOTIDES:

  A, T, G, C = 4 = Bekenstein

  For each position:
    3 possible mutations (to the other 3 bases)
    3 = SPHERE coefficient

  Transition/transversion ratio: ~2:1
  (Transitions are more common)

  2 = factor in Z = 2√(8π/3)

NEUTRAL THEORY:

  Kimura's neutral theory:
    Most mutations are neutral (no fitness effect)
    Evolution is largely genetic drift

  The neutral mutation rate:
    μ_neutral = μ × f_neutral

  where f_neutral ≈ 0.7-0.9 (most mutations neutral)

  This is SPHERE: continuous neutral wandering in sequence space.
  Selection (CUBE) only acts on the minority.
""")

# =============================================================================
# PART 3: SELECTION - SPHERE FITNESS LANDSCAPE
# =============================================================================

print("=" * 70)
print("PART 3: SELECTION - SPHERE FITNESS LANDSCAPE")
print("=" * 70)

print(f"""
THE FITNESS LANDSCAPE:

  Sewall Wright's concept:
    - Genotype space (CUBE: discrete sequences)
    - Fitness surface (SPHERE: continuous values)
    - Populations climb fitness peaks

FITNESS COMPONENTS:

  Fitness = Survival × Reproduction

  W = l × m

  where:
    l = probability of surviving to reproduce
    m = number of offspring if survives

  2 components = factor of 2 in Z

SELECTION MODES (Bekenstein = 4?):

  1. DIRECTIONAL SELECTION
     - Favors one extreme
     - Shifts population mean
     - Classic adaptation

  2. STABILIZING SELECTION
     - Favors intermediate
     - Reduces variation
     - Maintains optimum

  3. DISRUPTIVE SELECTION
     - Favors extremes
     - Increases variation
     - Can lead to speciation

  4. BALANCING SELECTION
     - Maintains multiple alleles
     - Heterozygote advantage
     - Frequency-dependent

  4 selection modes = Bekenstein!

SELECTION COEFFICIENT:

  s = (W_A - W_a) / W_A

  For weak selection: s << 1
  For strong selection: s → 1

  Time to fixation of beneficial mutation:
    t ≈ (2/s) × ln(2N) generations

  For s = 1/Z ≈ 0.17:
    t ≈ 12 × ln(2N) ≈ Gauge × ln(2N)

EPISTASIS:

  Gene interactions modify fitness landscape.

  Types:
    - Additive (no interaction)
    - Synergistic (together > sum)
    - Antagonistic (together < sum)

  Epistasis makes the landscape RUGGED.
  This is CUBE structure in the SPHERE landscape.
""")

# =============================================================================
# PART 4: GENETIC DRIFT - SPHERE RANDOMNESS
# =============================================================================

print("=" * 70)
print("PART 4: GENETIC DRIFT - SPHERE STOCHASTICITY")
print("=" * 70)

print(f"""
GENETIC DRIFT:

  Random changes in allele frequencies.
  Stronger in small populations.

  This is SPHERE: continuous, probabilistic wandering.

THE WRIGHT-FISHER MODEL:

  Each generation: sample 2N alleles with replacement
  Variance: p(1-p)/(2N)

  Effective population size Ne:
    Ne = 4 × (N_males × N_females) / (N_males + N_females)

  The "4" is Bekenstein!

COALESCENT THEORY:

  Looking backward in time:
    Lineages merge (coalesce) to common ancestors.

  Time to most recent common ancestor:
    E[TMRCA] = 2N × (1 - 1/k) for k lineages

  For k = 2: E[TMRCA] = 2N generations

  2 = factor in Z

FOUNDER EFFECTS:

  When small group starts new population:
    - Genetic bottleneck
    - Random sampling of original variation
    - CUBE selection from SPHERE possibilities

  Examples:
    - Island colonization
    - New species founding
    - Human populations

MOLECULAR CLOCK:

  Neutral mutations accumulate at constant rate.
  This allows dating divergences.

  Rate: ~1-2% sequence divergence per million years
  (For many genes)

  1-2% ≈ 1/100 to 2/100 ≈ 1/Z² to 2/Z²
  (Sequence divergence per ~30,000-60,000 generations)
""")

# =============================================================================
# PART 5: SPECIATION - Z² BRANCHING
# =============================================================================

print("=" * 70)
print("PART 5: SPECIATION - Z² DIVERSIFICATION")
print("=" * 70)

print(f"""
SPECIATION:

  The formation of new species.
  One Z² lineage becomes two.

SPECIATION MODES (Bekenstein = 4):

  1. ALLOPATRIC SPECIATION
     - Geographic isolation
     - Most common mode
     - Populations diverge in isolation

  2. PERIPATRIC SPECIATION
     - Small peripheral population
     - Founder effect + isolation
     - Rapid divergence

  3. PARAPATRIC SPECIATION
     - Partial isolation
     - Gradient selection
     - Cline → species

  4. SYMPATRIC SPECIATION
     - No geographic isolation
     - Ecological specialization
     - Most controversial

  4 modes = Bekenstein!

REPRODUCTIVE ISOLATION:

  What makes species "real"?
  Reproductive isolation mechanisms:

  Pre-zygotic:
    - Habitat isolation
    - Temporal isolation
    - Behavioral isolation
    - Mechanical isolation
    - Gametic isolation

  Post-zygotic:
    - Hybrid inviability
    - Hybrid sterility
    - Hybrid breakdown

  ~8 main barriers = CUBE!

THE SPECIES PROBLEM:

  What is a species?
    - Biological species concept (interbreeding)
    - Phylogenetic species concept (monophyly)
    - Ecological species concept (niche)
    - Morphological species concept (form)

  4 major concepts = Bekenstein!

  Reality: Species are Z² entities:
    CUBE (discrete, identifiable)
    × SPHERE (continuous variation, fuzzy boundaries)

TREE OF LIFE:

  All life shares common ancestor.
  Tree has ~8.7 million species (estimated).

  8.7 × 10⁶ ≈ 3^(14) ≈ 3^(Gauge + 2)

  Or: 8.7 × 10⁶ ≈ (100)^3.5 ≈ (3Z²)^3.5

  The diversity is vast but structured.
""")

# =============================================================================
# PART 6: PHYLOGENETICS - Z² HISTORY
# =============================================================================

print("=" * 70)
print("PART 6: PHYLOGENETICS - Z² TREE STRUCTURE")
print("=" * 70)

print(f"""
PHYLOGENETIC TREES:

  Trees represent evolutionary relationships.
  They are Z² structures:
    Nodes = CUBE (discrete branching events)
    Branches = SPHERE (continuous time)

TREE TOPOLOGY:

  For n taxa, number of possible unrooted trees:
    T(n) = (2n-5)!! = 1×3×5×...×(2n-5)

  For n = 4: T(4) = 3
  For n = 5: T(5) = 15
  For n = 10: T(10) = 2,027,025

  The combinatorial explosion is SPHERE-like.
  Choosing one tree is CUBE-like.

MOLECULAR PHYLOGENETICS:

  Using DNA/protein sequences to build trees.

  Methods:
    - Distance (UPGMA, Neighbor-Joining)
    - Parsimony (minimum changes)
    - Likelihood (probabilistic)
    - Bayesian (posterior probabilities)

  4 major methods = Bekenstein!

THE TREE OF LIFE:

  Three domains (SPHERE coefficient!):
    1. Bacteria
    2. Archaea
    3. Eukarya

  Eukaryotes have:
    - Animals
    - Plants
    - Fungi
    - Protists

  4 eukaryotic kingdoms = Bekenstein (simplified)

HORIZONTAL GENE TRANSFER:

  Not all evolution is vertical (tree-like).
  Genes can transfer between lineages:
    - Bacterial conjugation
    - Viral transduction
    - Transformation

  This makes the "tree" more like a "web."
  SPHERE (network) reality vs CUBE (tree) model.

MOLECULAR EVOLUTION:

  Substitution models:
    - JC69 (equal rates)
    - K80 (transition/transversion)
    - HKY (unequal frequencies)
    - GTR (general time-reversible)

  4 common models = Bekenstein!
""")

# =============================================================================
# PART 7: ADAPTATION - Z² OPTIMIZATION
# =============================================================================

print("=" * 70)
print("PART 7: ADAPTATION - Z² OPTIMIZATION")
print("=" * 70)

print(f"""
ADAPTATION:

  The process of becoming better suited to environment.
  Evolution by natural selection.

ADAPTIVE TRAITS:

  Examples of remarkable adaptations:
    - Eye (independent evolution 40+ times)
    - Flight (4 times: insects, pterosaurs, birds, bats)
    - Echolocation (2+ times: bats, dolphins)
    - Photosynthesis C4 (60+ times)

  Flight evolved 4 times = Bekenstein!

CONVERGENT EVOLUTION:

  Similar solutions evolve independently.
  This suggests certain forms are Z²-optimal.

  Examples:
    - Streamlined shape (fish, dolphins, ichthyosaurs)
    - Camera eyes (vertebrates, cephalopods)
    - Wings (many origins)
    - C4 photosynthesis (60+ origins)

  Convergence shows SPHERE of possibilities collapsing
  to CUBE of optimal solutions.

CONSTRAINTS ON EVOLUTION:

  Not all conceivable forms exist.
  Constraints limit possibilities:

  1. Physical constraints (physics, chemistry)
  2. Developmental constraints (how organisms build)
  3. Phylogenetic constraints (historical legacy)
  4. Genetic constraints (available variation)

  4 constraint types = Bekenstein!

  Constraints are CUBE boundaries on SPHERE possibilities.

TRADE-OFFS:

  Can't optimize everything simultaneously.
  Improving one trait may harm another.

  Classic trade-offs:
    - Reproduction vs survival
    - Size vs number of offspring
    - Speed vs endurance

  Trade-offs create fitness SURFACE (SPHERE)
  with multiple peaks (CUBE optima).

EVOLUTIONARY ARMS RACES:

  Predator-prey coevolution.
  Red Queen dynamics.

  "It takes all the running you can do to stay in place."

  This is Z² in action:
    CUBE (discrete adaptations)
    × SPHERE (continuous change)
    = Z² (dynamic equilibrium)
""")

# =============================================================================
# PART 8: MAJOR TRANSITIONS
# =============================================================================

print("=" * 70)
print("PART 8: MAJOR EVOLUTIONARY TRANSITIONS")
print("=" * 70)

print(f"""
THE MAJOR TRANSITIONS IN EVOLUTION:

  Maynard Smith & Szathmáry identified key transitions:

  1. Replicating molecules → Populations of molecules
  2. Independent replicators → Chromosomes
  3. RNA as gene and enzyme → DNA + protein (genetic code)
  4. Prokaryotes → Eukaryotes
  5. Asexual clones → Sexual populations
  6. Protists → Animals, plants, fungi (multicellularity)
  7. Solitary → Colonies (eusociality)
  8. Primate societies → Human societies (language)

  8 major transitions = CUBE!

COMMON THEME:

  Each transition involves:
    - Cooperation of previously independent units
    - New level of organization
    - Information transmission changes

  This is Z² level-jumping:
    CUBE (individual units)
    → Z² (organized system)
    → new CUBE (higher-level individual)

ORIGIN OF LIFE:

  Transition 1-3: From chemistry to biology.

  Key steps:
    1. Self-replicating molecules
    2. Compartmentalization (membranes)
    3. Genetic code (DNA → RNA → protein)
    4. Metabolism (energy capture)

  4 key steps = Bekenstein!

EUKARYOGENESIS:

  Prokaryote → Eukaryote transition.
  Endosymbiosis: Mitochondria and chloroplasts.

  This is Z² merger:
    Host (CUBE) × Symbiont (SPHERE)
    = Eukaryote (Z² hybrid)

MULTICELLULARITY:

  Evolved independently many times:
    - Animals (1×)
    - Plants (1×)
    - Fungi (1×)
    - Red algae (1×)
    - Brown algae (1×)
    - Green algae (2×)
    - Slime molds (2×)

  At least 8+ origins = CUBE order of magnitude
""")

# =============================================================================
# PART 9: HUMAN EVOLUTION
# =============================================================================

print("=" * 70)
print("PART 9: HUMAN EVOLUTION - Z² COGNITION")
print("=" * 70)

print(f"""
HUMAN EVOLUTION:

  Hominins split from chimps ~6-7 million years ago.
  6-7 ≈ Z ≈ 5.79

KEY HOMININ SPECIES:

  - Australopithecus (~4-2 Ma)
  - Homo habilis (~2.4-1.4 Ma)
  - Homo erectus (~1.9-0.1 Ma)
  - Homo heidelbergensis (~0.7-0.2 Ma)
  - Homo neanderthalensis (~0.4-0.04 Ma)
  - Homo sapiens (~0.3 Ma - present)

  ~6 major species in human lineage ≈ Z

BRAIN EVOLUTION:

  Chimp brain: ~400 cm³
  Australopithecus: ~450 cm³
  Homo habilis: ~600 cm³
  Homo erectus: ~900 cm³
  Modern human: ~1400 cm³

  Ratio (human/chimp): 1400/400 = 3.5 ≈ SPHERE coefficient

  Brain increased ~3× in 3 million years.
  3 = SPHERE coefficient

KEY HUMAN ADAPTATIONS:

  1. Bipedalism (walking upright)
  2. Tool use (technology)
  3. Language (symbolic communication)
  4. Culture (cumulative learning)

  4 key adaptations = Bekenstein!

CULTURAL EVOLUTION:

  Humans evolve culturally as well as biologically.
  Cultural evolution is MUCH faster.

  Cultural inheritance:
    - Teaching
    - Language
    - Writing
    - Digital

  4 modes = Bekenstein!

  Culture is Z²:
    CUBE (discrete memes, ideas)
    × SPHERE (continuous cultural matrix)
    = Z² civilization
""")

# =============================================================================
# PART 10: SUMMARY
# =============================================================================

print("=" * 70)
print("SUMMARY: EVOLUTION AS Z² PROCESS")
print("=" * 70)

print(f"""
╔═══════════════════════════════════════════════════════════════════════╗
║            EVOLUTION: Z² FRAMEWORK                                    ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  THE DARWIN EQUATION:                                                 ║
║                                                                       ║
║      Evolution = Variation × Selection × Inheritance                 ║
║               = CUBE × SPHERE × Z²                                   ║
║                                                                       ║
║  MUTATION (CUBE):                                                     ║
║                                                                       ║
║      4 mutation types = Bekenstein                                   ║
║      4 nucleotides = Bekenstein                                       ║
║      ~70 mutations/generation ≈ 2Z²                                  ║
║                                                                       ║
║  SELECTION (SPHERE):                                                  ║
║                                                                       ║
║      4 selection modes = Bekenstein                                   ║
║      Fitness landscape is SPHERE                                      ║
║      Selection acts as CUBE filter                                    ║
║                                                                       ║
║  SPECIATION:                                                          ║
║                                                                       ║
║      4 speciation modes = Bekenstein                                  ║
║      ~8 reproductive barriers = CUBE                                  ║
║      4 species concepts = Bekenstein                                  ║
║                                                                       ║
║  PHYLOGENETICS:                                                       ║
║                                                                       ║
║      3 domains = SPHERE coefficient                                   ║
║      4 methods = Bekenstein                                           ║
║      Nodes = CUBE, branches = SPHERE                                  ║
║                                                                       ║
║  MAJOR TRANSITIONS:                                                   ║
║                                                                       ║
║      8 major transitions = CUBE                                       ║
║      4 origin-of-life steps = Bekenstein                             ║
║      Each = CUBE → Z² → new CUBE                                     ║
║                                                                       ║
║  HUMAN EVOLUTION:                                                     ║
║                                                                       ║
║      4 key adaptations = Bekenstein                                   ║
║      Brain 3× increase = SPHERE coefficient                          ║
║      Culture = Z² transmission                                        ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════════════

EVOLUTION IS Z² EXPLORING POSSIBILITY SPACE:

    Mutation: CUBE (discrete genetic changes)
    Selection: SPHERE (continuous fitness gradient)
    Drift: SPHERE (random wandering)
    Adaptation: Z² (CUBE solutions in SPHERE landscape)

    Life evolves by Z² = CUBE × SPHERE.

    Variation provides the CUBE of possibilities.
    Selection sculpts the SPHERE of fitness.
    The product is Z² adaptation.

═══════════════════════════════════════════════════════════════════════════
""")

print("\n[EVOLUTION_Z2_DERIVATION.py complete]")
