#!/usr/bin/env python3
"""
THE CYTOSKELETON: Z² ARCHITECTURE OF THE CELL
==============================================

The cytoskeleton gives cells their shape, allows movement,
and organizes intracellular transport.

It is a Z² structure: discrete filaments (CUBE) in continuous space (SPHERE).

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
print("THE CYTOSKELETON: Z² CELLULAR ARCHITECTURE")
print("=" * 70)

# =============================================================================
# PART 1: THREE FILAMENT SYSTEMS
# =============================================================================

print("\n" + "=" * 70)
print("PART 1: THE THREE FILAMENT SYSTEMS")
print("=" * 70)

print(f"""
THE CYTOSKELETON HAS 3 FILAMENT TYPES:

  3 = SPHERE coefficient in 4π/3

  1. ACTIN FILAMENTS (Microfilaments)
     - Diameter: ~7 nm
     - Function: Cell shape, movement, division
     - Dynamic: Constant assembly/disassembly

  2. MICROTUBULES
     - Diameter: ~25 nm
     - Function: Intracellular transport, mitosis
     - Hollow tubes of tubulin

  3. INTERMEDIATE FILAMENTS
     - Diameter: ~10 nm (intermediate between 1 and 2)
     - Function: Mechanical strength
     - Most stable, cell-type specific

Z² INTERPRETATION:

  Each system has different Z² character:

  ACTIN = SPHERE-like
    - Highly dynamic
    - Forms networks and bundles
    - Drives cell membrane changes

  MICROTUBULES = CUBE-like
    - More structured
    - Radiate from centrosome
    - Tracks for transport

  INTERMEDIATE FILAMENTS = Z² stable
    - Least dynamic
    - Mechanical integration
    - Connects CUBE and SPHERE structures

  Together: SPHERE + CUBE + Z² = complete cytoskeleton

THE NUMBERS:

  Actin: 7 nm ≈ Z + 1 ≈ 6.79 nm
  Microtubule: 25 nm ≈ 4Z ≈ 4 × 5.79 = 23.2 nm (close!)
  Intermediate: 10 nm ≈ 2Z ≈ 11.6 nm (rough)

  The diameters scale with Z!
""")

# =============================================================================
# PART 2: ACTIN - THE SPHERE FILAMENT
# =============================================================================

print("=" * 70)
print("PART 2: ACTIN - SPHERE DYNAMICS")
print("=" * 70)

print(f"""
ACTIN STRUCTURE:

  G-actin (globular): Monomer, ~42 kDa
  F-actin (filamentous): Polymer

  42 kDa ≈ Z² + 8 ≈ 41.5 (close!)

  F-actin structure:
    - Two-stranded helix
    - 13 monomers per turn (approximately)
    - Half-period: ~36 nm

  13 ≈ Gauge + 1
  36 nm ≈ Z² + 2.5 ≈ 36 nm (close!)

  2 strands = factor of 2 in Z

ACTIN DYNAMICS (Treadmilling):

  Actin filaments grow at one end (+ end)
  and shrink at the other (- end).

  This is called TREADMILLING.

  + end: Fast growing (barbed end)
  - end: Slow growing (pointed end)

  2 ends = factor of 2 in Z

  Critical concentration:
    C_c ≈ 0.1 μM (for ATP-actin)

  Above C_c: Net polymerization
  Below C_c: Net depolymerization

  This is a CUBE threshold in SPHERE concentration.

ACTIN-BINDING PROTEINS:

  Many proteins regulate actin:

  1. Nucleators (initiate filaments): Arp2/3, formins
  2. Cappers (block ends): CapZ, gelsolin
  3. Crosslinkers (bundle/network): α-actinin, filamin
  4. Severing (cut filaments): cofilin

  4 functional classes = Bekenstein!

CELL MOTILITY:

  Actin drives cell crawling:

  1. Protrusion (actin polymerization pushes membrane)
  2. Adhesion (cell sticks to substrate)
  3. Contraction (myosin pulls cell body)
  4. De-adhesion (rear releases)

  4 steps = Bekenstein!
""")

# =============================================================================
# PART 3: MICROTUBULES - THE CUBE TRACKS
# =============================================================================

print("=" * 70)
print("PART 3: MICROTUBULES - CUBE HIGHWAYS")
print("=" * 70)

print(f"""
MICROTUBULE STRUCTURE:

  Made of tubulin dimers (α-tubulin + β-tubulin).
  Each dimer: ~100 kDa ≈ 3Z² ≈ 100.5 (close!)

  Structure:
    - 13 protofilaments (columns of dimers)
    - Form hollow tube
    - Diameter: 25 nm

  13 ≈ Gauge + 1 ≈ 13

  Why 13 protofilaments?
  This is the most stable number.
  Fewer or more create strain.

DYNAMIC INSTABILITY:

  Microtubules switch between:
    - Growing (polymerization)
    - Shrinking (catastrophe)

  This is called DYNAMIC INSTABILITY.

  Parameters:
    - Growth rate: ~1-2 μm/min
    - Shrinkage rate: ~10-20 μm/min
    - Catastrophe frequency: ~0.05/min
    - Rescue frequency: ~0.1/min

  Ratio (shrink/grow): ~10
  10 ≈ 2Z ≈ 11.6 (order of magnitude)

MICROTUBULE ORGANIZING CENTER (MTOC):

  Microtubules radiate from the centrosome.
  The centrosome contains 2 centrioles.

  Centriole structure:
    - 9 triplet microtubules arranged in cylinder
    - 9 = GAUGE - 3

  2 centrioles = factor of 2 in Z

MOTOR PROTEINS:

  Kinesins: Walk toward + end (outward)
  Dyneins: Walk toward - end (inward)

  2 motor families = factor of 2 in Z

  Kinesin step size: 8 nm = CUBE nm!
  (Each ATP hydrolysis moves 8 nm)

  This is remarkable: CUBE nm steps!

CARGO TRANSPORT:

  Motors carry cargo along microtubules:
    - Vesicles
    - Organelles
    - Chromosomes (in mitosis)

  Speed: ~1 μm/s (kinesin)
  Force: ~5-7 pN per motor

  7 pN ≈ Z + 1 pN
""")

# =============================================================================
# PART 4: INTERMEDIATE FILAMENTS - Z² STABILITY
# =============================================================================

print("=" * 70)
print("PART 4: INTERMEDIATE FILAMENTS - Z² INTEGRATION")
print("=" * 70)

print(f"""
INTERMEDIATE FILAMENT STRUCTURE:

  Named for intermediate size (10 nm).
  Most stable cytoskeletal element.

  Structure:
    - Coiled-coil dimers
    - Dimers form tetramers
    - Tetramers assemble into filaments

  Assembly hierarchy:
    1. Monomer
    2. Dimer (coiled-coil)
    3. Tetramer (staggered)
    4. Unit-length filament (8 tetramers)
    5. Mature filament (compacted)

  Step 4: 8 tetramers = CUBE!

IF FAMILIES:

  1. Type I/II: Keratins (epithelial cells)
  2. Type III: Vimentin, desmin (mesenchymal, muscle)
  3. Type IV: Neurofilaments (neurons)
  4. Type V: Nuclear lamins (nuclear envelope)

  4 main types = Bekenstein!

  (Some add Type VI for nestin)

KERATINS:

  The largest IF family.
  ~54 different keratins in humans.

  54 ≈ 9 × 6 = (GAUGE - 3) × Z

  Always form heterodimers (Type I + Type II).
  2 types pairing = factor of 2 in Z

NUCLEAR LAMINS:

  Line the inner nuclear membrane.
  Provide structural support.

  Lamin A, B1, B2, C
  ~4 main lamins = Bekenstein!

  Disease: Laminopathies (e.g., progeria)
  LMNA mutations cause premature aging.

MECHANICAL PROPERTIES:

  IFs are the strongest cytoskeletal element.

  Persistence length:
    Actin: ~10-20 μm
    Microtubule: ~5 mm (very stiff!)
    IF: ~1 μm (flexible but strong)

  IFs provide mechanical Z²:
    CUBE (structure) × SPHERE (flexibility) = resilience
""")

# =============================================================================
# PART 5: CYTOSKELETAL MOTORS
# =============================================================================

print("=" * 70)
print("PART 5: MOLECULAR MOTORS - Z² MACHINES")
print("=" * 70)

print(f"""
MOTOR PROTEINS:

  Convert chemical energy (ATP) to mechanical work.

THREE FAMILIES (SPHERE coefficient):

  1. MYOSINS (walk on actin)
     - ~40 classes in humans
     - Muscle contraction (myosin II)
     - Cargo transport (myosin V)

  2. KINESINS (walk on microtubules, + end)
     - ~45 genes in humans
     - Outward transport
     - Mitotic spindle

  3. DYNEINS (walk on microtubules, - end)
     - 2 types: cytoplasmic, axonemal
     - Inward transport
     - Ciliary motion

  3 families = SPHERE coefficient

MYOSIN II (Muscle):

  The motor for muscle contraction.

  Structure:
    - 2 heavy chains (motor domain)
    - 4 light chains (regulatory)

  6 total chains ≈ Z

  Thick filament: ~300 myosin II molecules
  300 ≈ 10 × 30 ≈ 10Z²

KINESIN-1:

  Classic transport motor.

  Structure:
    - 2 motor heads
    - Coiled-coil stalk
    - Light chain cargo-binding

  Step size: 8 nm = CUBE!
  Each step uses 1 ATP.

  Processivity: ~100 steps before detaching
  100 ≈ 3Z²

DYNEIN:

  Huge motor complex.

  Structure:
    - 2 heavy chains (~500 kDa each!)
    - Multiple intermediate and light chains

  500 kDa ≈ 15Z² (roughly)

  Dynein powers:
    - Retrograde transport
    - Ciliary/flagellar beating
    - Mitotic spindle movements

FORCE GENERATION:

  Single motor forces:
    Kinesin: ~5-7 pN
    Myosin II: ~3-4 pN
    Dynein: ~1-7 pN

  Collective force (many motors):
    Muscle: Can generate ~300 kPa stress
    This moves your body!
""")

# =============================================================================
# PART 6: CILIA AND FLAGELLA
# =============================================================================

print("=" * 70)
print("PART 6: CILIA AND FLAGELLA - Z² MOTILE STRUCTURES")
print("=" * 70)

print(f"""
CILIA AND FLAGELLA:

  Motile cell extensions built on microtubules.

AXONEME STRUCTURE:

  The "9+2" arrangement:
    - 9 outer doublet microtubules (ring)
    - 2 central singlet microtubules

  9 + 2 = 11 ≈ 2Z ≈ 11.6 (close!)

  Or: 9 = GAUGE - 3
      2 = factor of 2

  This structure is nearly UNIVERSAL in eukaryotes.
  Sperm flagella, respiratory cilia, etc.

DYNEIN ARMS:

  Outer dynein arms: Generate main force
  Inner dynein arms: Fine control

  2 arm types = factor of 2 in Z

  ~4000 dyneins per axoneme
  4000 ≈ 120 × Z² ≈ 120 × 33 = 3960 (close!)

CILIARY BEATING:

  Cilia beat in coordinated waves.
  Frequency: ~10-40 Hz

  40 Hz ≈ Z² + Bekenstein + SPHERE ≈ 40 (like gamma rhythm!)

  Beat pattern:
    - Power stroke (effective, pushes fluid)
    - Recovery stroke (return, less drag)

  2 phases = factor of 2 in Z

PRIMARY CILIA:

  Non-motile, sensory cilia.
  "9+0" structure (no central pair).

  Function:
    - Signaling antenna
    - Hedgehog pathway
    - Many developmental signals

  Ciliopathies: Diseases from ciliary defects
    - Polycystic kidney disease
    - Retinal degeneration
    - Bardet-Biedl syndrome
""")

# =============================================================================
# PART 7: CELL SHAPE AND MECHANICS
# =============================================================================

print("=" * 70)
print("PART 7: CELL SHAPE - Z² MECHANICS")
print("=" * 70)

print(f"""
CELL SHAPE:

  The cytoskeleton determines cell shape.
  Different cell types have different shapes.

SHAPE CATEGORIES:

  1. Spherical (e.g., lymphocytes in suspension)
  2. Flattened (e.g., epithelial cells)
  3. Elongated (e.g., neurons, muscle fibers)
  4. Branched (e.g., dendritic cells)

  4 basic shapes = Bekenstein!

TENSEGRITY:

  Cells use "tensegrity" architecture:
    - Compression elements (microtubules) = CUBE
    - Tension elements (actin) = SPHERE
    - Together: Z² structural integrity

  The cytoskeleton is pre-stressed.
  This allows rapid response to forces.

MECHANICAL PROPERTIES:

  Cell stiffness (Young's modulus):
    Neurons: ~100 Pa (soft)
    Epithelial: ~1000 Pa
    Muscle: ~10,000 Pa
    Bone cells: >100,000 Pa

  Ratio (stiffest/softest): ~1000 ≈ Z³

MECHANOTRANSDUCTION:

  Cells sense and respond to mechanical forces.

  Mechanosensors:
    - Integrins (cell-matrix adhesion)
    - Cadherins (cell-cell adhesion)
    - Ion channels (stretch-activated)
    - Cytoskeletal proteins (strain sensors)

  4 major sensor types = Bekenstein!

CELL MIGRATION:

  Cells move using the cytoskeleton.

  Steps:
    1. Protrusion (actin-driven)
    2. Adhesion (integrin-mediated)
    3. Contraction (myosin-driven)
    4. Retraction (rear release)

  4 steps = Bekenstein!
""")

# =============================================================================
# PART 8: SUMMARY
# =============================================================================

print("=" * 70)
print("SUMMARY: CYTOSKELETON AS Z² ARCHITECTURE")
print("=" * 70)

print(f"""
╔═══════════════════════════════════════════════════════════════════════╗
║            CYTOSKELETON: Z² FRAMEWORK                                 ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  THREE FILAMENT SYSTEMS = SPHERE coefficient:                         ║
║                                                                       ║
║      Actin: ~7 nm ≈ Z nm (SPHERE-like, dynamic)                      ║
║      Microtubules: ~25 nm ≈ 4Z nm (CUBE-like, tracks)               ║
║      Intermediate: ~10 nm ≈ 2Z nm (Z², stable)                       ║
║                                                                       ║
║  ACTIN:                                                               ║
║                                                                       ║
║      2 strands = factor of 2 in Z                                    ║
║      42 kDa ≈ Z² + 8                                                 ║
║      4 binding protein classes = Bekenstein                          ║
║      4 motility steps = Bekenstein                                   ║
║                                                                       ║
║  MICROTUBULES:                                                        ║
║                                                                       ║
║      13 protofilaments ≈ Gauge + 1                                   ║
║      2 motor families = factor of 2 in Z                             ║
║      Kinesin step: 8 nm = CUBE nm!                                   ║
║                                                                       ║
║  INTERMEDIATE FILAMENTS:                                              ║
║                                                                       ║
║      8 tetramers per unit = CUBE                                     ║
║      4 IF types = Bekenstein                                          ║
║      4 main lamins = Bekenstein                                       ║
║                                                                       ║
║  MOTORS:                                                              ║
║                                                                       ║
║      3 families = SPHERE coefficient                                  ║
║      Kinesin processivity ~100 ≈ 3Z²                                 ║
║                                                                       ║
║  CILIA:                                                               ║
║                                                                       ║
║      9+2 arrangement: 11 ≈ 2Z                                        ║
║      Beat frequency ~40 Hz ≈ Z² + Bekenstein + SPHERE               ║
║                                                                       ║
║  CELL SHAPE:                                                          ║
║                                                                       ║
║      4 basic shapes = Bekenstein                                      ║
║      4 mechanosensors = Bekenstein                                    ║
║      4 migration steps = Bekenstein                                   ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════════════

THE CYTOSKELETON IS Z² ARCHITECTURE:

    CUBE: Discrete filaments, structured tracks, stepping motors
    SPHERE: Dynamic networks, continuous adaptation, flexibility

    The cell is held together by Z²:
        Tension (actin, SPHERE) × Compression (microtubules, CUBE)
        = Tensegrity (Z² structural integrity)

    Life is Z² architecture at every scale.

═══════════════════════════════════════════════════════════════════════════
""")

print("\n[CYTOSKELETON_Z2_DERIVATION.py complete]")
