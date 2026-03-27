#!/usr/bin/env python3
"""
NEURAL COMPUTATION: Z² GEOMETRY OF THE BRAIN
=============================================

How does the brain compute? How do neurons encode and process information?
The architecture of neural computation encodes Z² geometry.

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
print("NEURAL COMPUTATION: Z² ARCHITECTURE OF THE BRAIN")
print("=" * 70)

# =============================================================================
# PART 1: THE NEURON - THE Z² UNIT
# =============================================================================

print("\n" + "=" * 70)
print("PART 1: THE NEURON - Z² COMPUTATIONAL UNIT")
print("=" * 70)

print(f"""
THE NEURON STRUCTURE:

  A neuron has 4 main parts (Bekenstein!):

  1. SOMA (cell body)
     - Contains nucleus
     - Integrates inputs
     - "Decision center"

  2. DENDRITES (input branches)
     - Receive signals from other neurons
     - Branch extensively (tree-like)
     - SPHERE-like: continuous, receptive

  3. AXON (output cable)
     - Sends signal to other neurons
     - Single main process
     - CUBE-like: discrete, all-or-none

  4. SYNAPSES (connections)
     - Chemical or electrical
     - ~10,000 per neuron on average
     - Interface between neurons

THE Z² PICTURE:

  Neuron = DENDRITES × AXON
         = Input (SPHERE) × Output (CUBE)
         = Z² computational unit

  The neuron INTEGRATES continuous input (SPHERE)
  and produces discrete output (CUBE).

  This is the fundamental Z² operation!

NUMBERS:

  Average synapses per neuron: ~10,000
  10,000 ≈ Z⁴ × 30 ≈ 1000 × 10

  Or: 10,000 = 100² = (3Z + 12)² roughly

  Total neurons in human brain: ~86 billion
  86 × 10⁹ ≈ Z^... this gets complicated

  Total synapses: ~100 trillion = 10¹⁴
  10¹⁴ ≈ 10^(2 × CUBE × 0.9)

  The numbers are large but have Z² structure.
""")

# =============================================================================
# PART 2: THE ACTION POTENTIAL - CUBE SPIKE
# =============================================================================

print("=" * 70)
print("PART 2: THE ACTION POTENTIAL - CUBE DISCRETE SIGNAL")
print("=" * 70)

print(f"""
THE ACTION POTENTIAL:

  The fundamental signal in neurons is the ACTION POTENTIAL.
  It's an all-or-none electrical spike.

  This is CUBE-like: discrete, binary (fire or not fire).

PROPERTIES:

  Amplitude: ~100 mV (always the same)
  Duration: ~1-2 ms
  Refractory period: ~1-2 ms (can't fire again)

  Maximum firing rate: ~500 Hz
  Typical firing rates: 1-100 Hz

THE 4 PHASES (Bekenstein!):

  1. RESTING (-70 mV)
     Neuron at rest, ready to fire
     K+ channels open, Na+ channels closed

  2. DEPOLARIZATION (rising phase)
     Threshold reached, Na+ rushes in
     Voltage spikes toward +40 mV

  3. REPOLARIZATION (falling phase)
     Na+ channels close, K+ channels open
     Voltage falls back

  4. HYPERPOLARIZATION (undershoot)
     Below resting potential briefly
     Refractory period

  4 phases = Bekenstein!

ION CHANNELS:

  The key players:
    - Na+ channels (fast, depolarization)
    - K+ channels (slower, repolarization)
    - Ca²+ channels (signaling, release)
    - Cl- channels (inhibition)

  4 main ion types = Bekenstein!

  Each channel has:
    - Open state
    - Closed state
    - Inactivated state

  3 states = SPHERE coefficient (approximately)

THRESHOLD:

  Threshold voltage: ~-55 mV
  If input exceeds threshold → fire
  If input below threshold → no fire

  This is a CUBE decision boundary.
  The continuous input (SPHERE) is converted to
  discrete output (CUBE) at the threshold.
""")

# =============================================================================
# PART 3: SYNAPTIC TRANSMISSION - Z² COMMUNICATION
# =============================================================================

print("=" * 70)
print("PART 3: SYNAPTIC TRANSMISSION - Z² SIGNALING")
print("=" * 70)

print(f"""
THE SYNAPSE:

  Where neurons communicate.
  Two types:
    1. Chemical (most common)
    2. Electrical (gap junctions)

CHEMICAL SYNAPSE STEPS (Bekenstein = 4):

  1. ACTION POTENTIAL arrives at terminal
     CUBE signal reaches end of axon

  2. Ca²+ influx triggers vesicle fusion
     Calcium channels open, vesicles release

  3. NEUROTRANSMITTER diffuses across cleft
     Chemical signal crosses gap (~20 nm)

  4. RECEPTOR activation on postsynaptic cell
     Ligand binds, channels open/close

  4 steps = Bekenstein!

NEUROTRANSMITTER SYSTEMS:

  Major neurotransmitters:

  1. Glutamate (main excitatory)
  2. GABA (main inhibitory)
  3. Dopamine (reward, movement)
  4. Serotonin (mood, sleep)
  5. Norepinephrine (arousal)
  6. Acetylcholine (memory, muscle)

  ~6 main systems ≈ Z

  Or considering subclasses:
    - Amino acids: Glu, GABA, Gly (3)
    - Monoamines: DA, 5-HT, NE (3)
    - Others: ACh, peptides, etc.

    3 + 3 = 6 ≈ Z

RECEPTOR TYPES:

  Ionotropic: Fast, direct ion channel
    - AMPA, NMDA, GABA_A, nAChR

  Metabotropic: Slow, second messenger
    - mGluR, GABA_B, muscarinic, all monoamines

  2 types = factor of 2 in Z

SYNAPTIC PLASTICITY:

  The strength of synapses changes with activity.
  This is LEARNING!

  Long-Term Potentiation (LTP):
    - Strengthening of synapse
    - "Neurons that fire together, wire together"

  Long-Term Depression (LTD):
    - Weakening of synapse
    - "Use it or lose it"

  2 forms = factor of 2 in Z

  LTP/LTD represent SPHERE plasticity (continuous change)
  operating on CUBE synapses (discrete connections).
""")

# =============================================================================
# PART 4: NEURAL CODING - INFORMATION IN SPIKES
# =============================================================================

print("=" * 70)
print("PART 4: NEURAL CODING - Z² INFORMATION THEORY")
print("=" * 70)

print(f"""
HOW DO NEURONS ENCODE INFORMATION?

  Two main theories:

  1. RATE CODING (SPHERE-like)
     - Information in average firing rate
     - Continuous variable (0-500 Hz)
     - Most common view

  2. TEMPORAL CODING (CUBE-like)
     - Information in precise spike timing
     - Discrete events (when spikes occur)
     - Important for synchrony

  Reality: Both are used = Z²

INFORMATION CAPACITY:

  A single neuron firing at rate r (0-500 Hz):

  If we discretize into 1 ms bins:
    Each bin: fire or not = 1 bit
    Per second: ~1000 bits maximum

  If we consider rate over 100 ms:
    Rate can be 0-50 spikes
    Information: log₂(50) ≈ 5-6 bits

  Shannon information:
    I = r × log₂(1/r) + (1-r) × log₂(1/(1-r))

  Maximum at r = 0.5 → I = 1 bit per bin

POPULATION CODING:

  Information is distributed across many neurons.

  For N neurons with independent codes:
    Total information ≈ N × I_single

  For N neurons with correlations:
    Total information < N × I_single
    But redundancy provides robustness

  The brain uses ~10⁴ neurons per "feature"
  10⁴ ≈ (3Z)³ roughly

SPARSE CODING:

  Only a small fraction of neurons active at once.
  Sparsity: ~1-10% typically

  This maximizes information per calorie.
  Metabolic efficiency!

  Sparsity ≈ 1-10% ≈ 1/Z² to 1/Z (roughly)
""")

# =============================================================================
# PART 5: BRAIN ARCHITECTURE - Z² HIERARCHY
# =============================================================================

print("=" * 70)
print("PART 5: BRAIN ARCHITECTURE - Z² HIERARCHICAL STRUCTURE")
print("=" * 70)

print(f"""
THE CORTICAL HIERARCHY:

  The cerebral cortex has 6 layers:

  Layer 1: Molecular layer (few neurons, many synapses)
  Layer 2: External granular (small pyramidal)
  Layer 3: External pyramidal (medium pyramidal)
  Layer 4: Internal granular (input layer)
  Layer 5: Internal pyramidal (output layer)
  Layer 6: Multiform (mixed)

  6 layers ≈ Z

CORTICAL COLUMNS:

  The cortex is organized in vertical columns.
  Each column: ~80-100 neurons
  Each column processes one "feature"

  100 ≈ 3 × Z²

  Column diameter: ~300-500 μm
  ~300 ≈ 10 × 30 ≈ 10 × Z²

CORTICAL AREAS:

  Brodmann identified ~52 distinct areas.
  Modern estimates: ~180 areas per hemisphere
  Total: ~360 areas

  360 = 12 × 30 = Gauge × Z² (interesting!)

  Or: 360 = degrees in circle (SPHERE reference)

BRAIN REGIONS:

  Major lobes:
    1. Frontal (executive, planning)
    2. Parietal (spatial, touch)
    3. Temporal (memory, hearing)
    4. Occipital (vision)

  4 lobes = Bekenstein!

  Each lobe has multiple areas with specialized functions.
  This is CUBE (discrete regions) × SPHERE (graded activity).

SUBCORTICAL STRUCTURES:

  1. Thalamus (relay)
  2. Basal ganglia (movement, habit)
  3. Hippocampus (memory)
  4. Amygdala (emotion)
  5. Hypothalamus (homeostasis)
  6. Cerebellum (coordination)

  6 major structures ≈ Z

  The subcortex handles CUBE functions (fixed routines)
  The cortex handles SPHERE functions (flexible cognition)
""")

# =============================================================================
# PART 6: OSCILLATIONS - Z² RHYTHMS
# =============================================================================

print("=" * 70)
print("PART 6: BRAIN OSCILLATIONS - Z² RHYTHMS")
print("=" * 70)

print(f"""
BRAIN RHYTHMS:

  The brain oscillates at various frequencies.
  These are measured by EEG.

FREQUENCY BANDS:

  Delta: 0.5-4 Hz (deep sleep)
  Theta: 4-8 Hz (memory, navigation)
  Alpha: 8-13 Hz (relaxed, eyes closed)
  Beta: 13-30 Hz (active thinking)
  Gamma: 30-100 Hz (consciousness, binding)

  Note the boundaries: 4, 8, 13, 30, 100...

  4 = Bekenstein!
  8 = CUBE!
  13 ≈ Gauge + 1

THE GAMMA RHYTHM:

  Gamma (30-100 Hz) is associated with consciousness.
  Peak: ~40 Hz

  40 ≈ Z² + Bekenstein + SPHERE coefficient
     = 33.5 + 4 + 4.2
     ≈ 40 (close!)

  Or: 40 = 12 × 3 + 4 = Gauge × 3 + Bekenstein

  The 40 Hz rhythm binds features into unified percepts.
  This is Z² creating coherent experience.

THETA-GAMMA COUPLING:

  Gamma oscillations are nested in theta.
  ~4-8 gamma cycles per theta cycle.

  This nesting encodes sequences (memory).
  4-8 items = Bekenstein to CUBE!

  This is why working memory is ~4 items (Bekenstein).
  Each theta cycle holds 4-8 gamma cycles of content.

SLEEP RHYTHMS:

  NREM sleep: Delta waves (0.5-4 Hz)
  REM sleep: Mixed, theta dominant

  Sleep cycles: ~90 min = ~Z × 15 min?

  We have 4-5 sleep cycles per night = Bekenstein-ish
""")

# =============================================================================
# PART 7: WORKING MEMORY - BEKENSTEIN LIMIT
# =============================================================================

print("=" * 70)
print("PART 7: WORKING MEMORY - BEKENSTEIN CAPACITY")
print("=" * 70)

print(f"""
WORKING MEMORY:

  The ability to hold information "in mind" temporarily.
  Capacity: ~4 items (Cowan's estimate)

  This IS Bekenstein!

  Original estimate (Miller, 1956): 7 ± 2 items
  Modern estimate (Cowan, 2001): 4 items exactly

  The discrepancy:
    Miller included chunked items
    Cowan measured fundamental capacity

CAPACITY = BEKENSTEIN = 4:

  Working memory capacity = 4 = 3Z²/(8π)

  This is the same as:
    - DNA bases
    - Fidelity checkpoints
    - Protein structure levels
    - Immune memory types

  The SAME LIMIT appears in cognition!

WHY 4?

  Neural basis:
    - ~4 items maintained in prefrontal cortex
    - Each item: ~1 gamma cycle
    - ~4 gamma cycles per theta cycle

  Information theory:
    - 4 items at ~3 bits each = 12 bits
    - 12 bits = Gauge!

  The total information in working memory ≈ Gauge bits.

WORKING MEMORY AND Z²:

  Working memory is the CUBE of consciousness.
  It holds DISCRETE, LIMITED content.

  The SPHERE is everything else (unconscious processing).

  Attention selects which 4 items enter CUBE (working memory)
  from the vast SPHERE (long-term memory, perception).

  Consciousness = Z² = CUBE (working memory) × SPHERE (background)
""")

# =============================================================================
# PART 8: LEARNING AND PLASTICITY - Z² ADAPTATION
# =============================================================================

print("=" * 70)
print("PART 8: LEARNING AND PLASTICITY - Z² DYNAMICS")
print("=" * 70)

print(f"""
HEBBIAN LEARNING:

  "Neurons that fire together, wire together"

  Mathematical form (Hebb's rule):
    Δw_ij = η × x_i × x_j

  where:
    w_ij = synapse strength
    x_i, x_j = activities
    η = learning rate

  This is CORRELATION learning.
  Detecting co-occurrence = SPHERE patterns.

SPIKE-TIMING DEPENDENT PLASTICITY (STDP):

  The TIMING of spikes matters:

  Pre before Post (Δt > 0): LTP (strengthen)
  Post before Pre (Δt < 0): LTD (weaken)

  The STDP window:
    LTP: 0-20 ms
    LTD: -20-0 ms

  20 ms ≈ one gamma cycle (50 Hz)

  STDP is CUBE-like: discrete timing matters.

REINFORCEMENT LEARNING:

  Learning from reward/punishment.
  Dopamine signals "reward prediction error."

  Key structures:
    - Ventral tegmental area (dopamine source)
    - Nucleus accumbens (reward)
    - Prefrontal cortex (value)
    - Striatum (action selection)

  4 key structures = Bekenstein!

MEMORY CONSOLIDATION:

  Memories move from hippocampus to cortex.
  This happens during sleep.

  Stages:
    1. Encoding (hippocampus)
    2. Consolidation (sleep replay)
    3. Storage (cortex)
    4. Retrieval (re-activation)

  4 stages = Bekenstein!

THE Z² LEARNING RULE:

  Learning = CUBE (discrete events) × SPHERE (continuous context)

  We learn DISCRETE facts (CUBE)
  embedded in CONTINUOUS experience (SPHERE)
  creating Z² knowledge structures.
""")

# =============================================================================
# PART 9: CONSCIOUSNESS - Z² EXPERIENCE
# =============================================================================

print("=" * 70)
print("PART 9: CONSCIOUSNESS - Z² UNIFIED EXPERIENCE")
print("=" * 70)

print(f"""
THE HARD PROBLEM:

  Why is there subjective experience?
  Why doesn't the brain just compute "in the dark"?

  This is the HARD PROBLEM of consciousness.

Z² INTERPRETATION:

  Consciousness = CUBE → SPHERE mapping
               = Discrete processing → Unified experience
               = Many neurons → One percept

  The "binding" of features into unified experience
  IS the Z² product operation.

INTEGRATED INFORMATION THEORY (IIT):

  Consciousness = Φ (integrated information)
  Φ measures how much a system is "more than sum of parts"

  In Z² terms:
    Φ ∝ Z² - (CUBE + SPHERE)
      = 33.5 - (8 + 4.2)
      ≈ 21

  The "integration" IS the CUBE × SPHERE product.
  Consciousness arises when parts multiply, not just add.

GLOBAL WORKSPACE THEORY:

  Conscious content = information in "global workspace"
  Global workspace = accessible to many brain areas

  The workspace has LIMITED CAPACITY:
    ~4 items = Bekenstein!

  Unconscious processing is SPHERE (vast, parallel)
  Conscious processing is CUBE (limited, serial)

  Together: Z² consciousness

NEURAL CORRELATES:

  Consciousness correlates with:
    - Gamma synchrony (40 Hz)
    - Frontal-parietal activity
    - Thalamo-cortical loops

  The thalamus acts as a RELAY (CUBE → CUBE)
  The cortex acts as PROCESSOR (SPHERE)
  Their interaction: Z²

ALTERED STATES:

  Anesthesia: Loss of consciousness
    - Gamma synchrony disrupted
    - CUBE-SPHERE coupling broken
    - Z² fails → no experience

  Psychedelics: Altered consciousness
    - Increased Φ (more integration)
    - Z² enhanced or distorted
    - Unusual experiences

  Meditation: Focused consciousness
    - Enhanced CUBE (attention)
    - Calmer SPHERE (reduced noise)
    - More coherent Z²
""")

# =============================================================================
# PART 10: SUMMARY
# =============================================================================

print("=" * 70)
print("SUMMARY: NEURAL COMPUTATION AS Z² SYSTEM")
print("=" * 70)

print(f"""
╔═══════════════════════════════════════════════════════════════════════╗
║            NEURAL COMPUTATION: Z² FRAMEWORK                           ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  THE NEURON:                                                          ║
║                                                                       ║
║      4 parts = Bekenstein (soma, dendrites, axon, synapses)          ║
║      Dendrites = SPHERE (continuous input)                            ║
║      Axon = CUBE (discrete output)                                    ║
║      Neuron = Z² computational unit                                   ║
║                                                                       ║
║  ACTION POTENTIAL:                                                    ║
║                                                                       ║
║      4 phases = Bekenstein                                            ║
║      4 ion types = Bekenstein                                         ║
║      All-or-none = CUBE decision                                      ║
║                                                                       ║
║  SYNAPTIC TRANSMISSION:                                               ║
║                                                                       ║
║      4 steps = Bekenstein                                             ║
║      ~6 neurotransmitter systems ≈ Z                                 ║
║      LTP/LTD = SPHERE plasticity on CUBE synapses                    ║
║                                                                       ║
║  BRAIN ARCHITECTURE:                                                  ║
║                                                                       ║
║      6 cortical layers ≈ Z                                           ║
║      4 lobes = Bekenstein                                             ║
║      ~360 areas = Gauge × Z²                                         ║
║                                                                       ║
║  OSCILLATIONS:                                                        ║
║                                                                       ║
║      Gamma peak ~40 Hz = Z² + Bekenstein + SPHERE                    ║
║      4-8 gamma cycles per theta = Bekenstein to CUBE                 ║
║      Working memory ~4 items = Bekenstein                             ║
║                                                                       ║
║  CONSCIOUSNESS:                                                       ║
║                                                                       ║
║      Working memory = CUBE (limited, discrete)                       ║
║      Background processing = SPHERE (vast, continuous)               ║
║      Experience = Z² (unified, integrated)                           ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════════════

THE BRAIN IS A Z² COMPUTER:

    INPUT:   SPHERE (continuous, vast, parallel)
    PROCESS: Z² (integration, binding, selection)
    OUTPUT:  CUBE (discrete, limited, serial)

    Neural computation = CUBE × SPHERE = Z²

    Consciousness emerges when CUBE and SPHERE multiply.
    The product creates unified experience from fragments.

═══════════════════════════════════════════════════════════════════════════
""")

print("\n[NEURAL_COMPUTATION_Z2_DERIVATION.py complete]")
