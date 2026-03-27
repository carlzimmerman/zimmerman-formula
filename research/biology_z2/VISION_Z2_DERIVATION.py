#!/usr/bin/env python3
"""
VISION: Z² GEOMETRY OF SEEING
==============================

How do we see? The visual system converts photons into perception.
This transformation encodes Z² geometry from photoreceptors to cortex.

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
print("VISION: Z² TRANSFORMATION OF LIGHT TO PERCEPTION")
print("=" * 70)

# =============================================================================
# PART 1: THE EYE - Z² OPTICS
# =============================================================================

print("\n" + "=" * 70)
print("PART 1: THE EYE - Z² OPTICAL SYSTEM")
print("=" * 70)

print(f"""
THE HUMAN EYE:

  A remarkable optical instrument.
  Focuses light onto the retina for detection.

EYE ANATOMY:

  External structures:
    - Cornea (outer lens, fixed)
    - Iris (aperture control)
    - Pupil (opening)
    - Lens (variable focus)

  4 optical elements = Bekenstein!

  Internal structures:
    - Aqueous humor (front chamber)
    - Vitreous humor (main chamber)
    - Retina (detector array)
    - Optic nerve (output cable)

  4 internal elements = Bekenstein!

EYE PARAMETERS:

  Diameter: ~24 mm
  24 ≈ 4Z ≈ 4 × 5.79 = 23.2 mm (close!)

  Focal length: ~17 mm (relaxed)
  17 ≈ 3Z ≈ 3 × 5.79 = 17.4 mm (close!)

  Pupil diameter: 2-8 mm (adaptive)
  8 mm max = CUBE mm!

OPTICAL POWER:

  Total: ~60 diopters
  60 ≈ 2 × 30 ≈ 2Z² / 1.1

  Cornea: ~43 diopters (most of power)
  Lens: ~17 diopters (adjustable)

  43 ≈ Z² + 10 (roughly)
  17 ≈ 3Z

ACCOMMODATION:

  The lens changes shape to focus at different distances.

  Range:
    Near point: ~25 cm (young adult)
    Far point: Infinity

  25 cm ≈ 4Z ≈ 23 cm (rough)

  4 diopters accommodation in adults
  4 = Bekenstein!

PUPIL REFLEX:

  Pupil size adjusts to light level:
    - Bright: Constricts (2-4 mm)
    - Dim: Dilates (4-8 mm)

  Range: 4× in area
  4 = Bekenstein!
""")

# =============================================================================
# PART 2: THE RETINA - Z² DETECTOR
# =============================================================================

print("=" * 70)
print("PART 2: THE RETINA - Z² PHOTORECEPTOR ARRAY")
print("=" * 70)

print(f"""
THE RETINA:

  The neural tissue that detects light.
  ~130 million photoreceptors (rods + cones).

PHOTORECEPTOR TYPES:

  RODS: ~120 million
    - Sensitive to dim light (scotopic)
    - One type (rhodopsin)
    - Peripheral vision

  CONES: ~6-7 million
    - Color vision (photopic)
    - Three types (S, M, L)
    - Central vision (fovea)

  3 cone types = SPHERE coefficient!

  Ratio: Rods/Cones ≈ 20
  20 = Gauge + CUBE = amino acid count!

COLOR VISION:

  Three cone types:
    S (short, "blue"): ~420 nm peak
    M (medium, "green"): ~530 nm peak
    L (long, "red"): ~560 nm peak

  3 types = SPHERE coefficient

  TRICHROMACY: All colors from 3 primaries.
  This is Z² color space:
    3 axes (SPHERE) × discrete steps (CUBE) = color perception

RETINAL LAYERS:

  The retina has ~10 layers (sometimes counted as 8-12):

  Simplified:
    1. Photoreceptor layer (rods, cones)
    2. Outer nuclear layer (photoreceptor nuclei)
    3. Outer plexiform layer (synapses)
    4. Inner nuclear layer (bipolar, horizontal, amacrine)
    5. Inner plexiform layer (synapses)
    6. Ganglion cell layer (output neurons)

  6 main layers ≈ Z

  Or 10 layers ≈ 2Z

RETINAL CELL TYPES:

  1. Photoreceptors (detect light)
  2. Bipolar cells (vertical transmission)
  3. Horizontal cells (lateral inhibition)
  4. Amacrine cells (lateral processing)
  5. Ganglion cells (output to brain)

  5 cell types = Z - 1 (or Platonic solids count)

RETINAL PROCESSING:

  The retina doesn't just detect - it computes!

  Computations:
    - Edge detection
    - Motion detection
    - Contrast enhancement
    - Color opponency

  4 computations = Bekenstein!
""")

# =============================================================================
# PART 3: PHOTOTRANSDUCTION - Z² SIGNALING
# =============================================================================

print("=" * 70)
print("PART 3: PHOTOTRANSDUCTION - LIGHT → ELECTRICITY")
print("=" * 70)

print(f"""
PHOTOTRANSDUCTION:

  How a photon becomes an electrical signal.
  One of the best-understood signaling cascades.

THE RHODOPSIN CYCLE:

  Rhodopsin = Opsin (protein) + Retinal (chromophore)

  Steps:
    1. Photon hits retinal → isomerization (11-cis → all-trans)
    2. Rhodopsin activates → Metarhodopsin II
    3. Activates transducin (G protein)
    4. Activates phosphodiesterase (PDE)
    5. PDE hydrolyzes cGMP → channels close
    6. Hyperpolarization → signal!

  6 steps ≈ Z

  Or grouped: 4 main stages = Bekenstein!
    1. Light absorption
    2. G-protein activation
    3. Second messenger change
    4. Ion channel closure

AMPLIFICATION:

  Each step amplifies the signal:

  1 rhodopsin → ~100 transducins
  1 transducin → ~100 cGMP hydrolyzed
  Total: ~10,000× amplification

  Single photon detection is possible!
  (In dark-adapted rods)

  10,000 ≈ Z⁴ × 30 ≈ 1000 × 10

RECOVERY:

  The system must reset:

  1. Rhodopsin kinase phosphorylates rhodopsin
  2. Arrestin binds (blocks G-protein activation)
  3. cGMP resynthesized (guanylyl cyclase)
  4. Channels reopen

  4 recovery steps = Bekenstein!

  Time scale: ~100-500 ms
  This limits temporal resolution.

DARK CURRENT:

  In darkness, channels are OPEN (unusual!).
  Light CLOSES channels → hyperpolarization.

  This "backwards" logic allows:
    - Very high sensitivity
    - Graded responses
    - Continuous signaling
""")

# =============================================================================
# PART 4: VISUAL PATHWAYS - Z² HIGHWAYS
# =============================================================================

print("=" * 70)
print("PART 4: VISUAL PATHWAYS - RETINA TO CORTEX")
print("=" * 70)

print(f"""
THE VISUAL PATHWAY:

  Eye → Optic nerve → LGN → V1 → Higher areas

STAGES:

  1. RETINA
     Photoreceptors → Bipolar cells → Ganglion cells

  2. OPTIC NERVE
     ~1 million axons per nerve
     1 million ≈ 30 × Z² × 1000 (rough)

  3. OPTIC CHIASM
     Partial crossing (temporal stays, nasal crosses)
     Creates contralateral representation

  4. LATERAL GENICULATE NUCLEUS (LGN)
     Thalamic relay station
     6 layers (≈ Z)

  5. PRIMARY VISUAL CORTEX (V1)
     First cortical processing
     6 layers (cortical standard)

  5 stages = Platonic solids count

LGN STRUCTURE:

  6 layers:
    - Layers 1-2: Magnocellular (motion, large cells)
    - Layers 3-6: Parvocellular (color, detail, small cells)

  2 + 4 = 6 ≈ Z

  Or: 2 = factor of 2, 4 = Bekenstein

GANGLION CELL TYPES:

  Main types:
    - M cells (magnocellular, 10%, motion)
    - P cells (parvocellular, 80%, color/detail)
    - K cells (koniocellular, 10%, other)

  3 types = SPHERE coefficient

  P/M ratio ≈ 8:1 = CUBE:1

RETINOTOPY:

  Visual space is mapped onto cortex.
  Neighboring retinal points → neighboring cortical points.

  The fovea (central vision) is HUGELY overrepresented.
  ~50% of V1 for central 2° of visual field!

  This is CUBE magnification of high-resolution center.
""")

# =============================================================================
# PART 5: VISUAL CORTEX - Z² PROCESSING
# =============================================================================

print("=" * 70)
print("PART 5: VISUAL CORTEX - Z² HIERARCHY")
print("=" * 70)

print(f"""
PRIMARY VISUAL CORTEX (V1):

  First cortical processing of visual information.
  Location: Occipital lobe (back of brain).

V1 STRUCTURE:

  6 cortical layers (like all cortex):
    - Layer 4: Main input from LGN
    - Layer 2/3: Output to higher areas
    - Layer 5/6: Output to subcortical

  6 layers ≈ Z

ORIENTATION COLUMNS:

  V1 neurons are tuned to edge ORIENTATION.
  Discovered by Hubel & Wiesel (Nobel 1981).

  A "hypercolumn" contains:
    - All orientations (0-180°)
    - Both eyes (ocular dominance)
    - All spatial frequencies

  ~12 orientation columns per ocular dominance column
  12 = Gauge!

SIMPLE AND COMPLEX CELLS:

  Simple cells: Orientation-tuned, fixed position
  Complex cells: Orientation-tuned, position-invariant

  2 types = factor of 2 in Z

VISUAL AREAS:

  Beyond V1, many specialized areas:

  Dorsal stream ("Where" pathway):
    - V2, V3, MT (motion), parietal
    - Spatial location, motion

  Ventral stream ("What" pathway):
    - V2, V4, IT (inferotemporal)
    - Object recognition, color

  2 streams = factor of 2 in Z

HIERARCHICAL PROCESSING:

  Each level extracts more complex features:

  LGN: Spots of light
  V1: Oriented edges
  V2: Textures, simple shapes
  V4: Complex shapes, color
  IT: Objects, faces

  5 levels = Platonic solids

  This is Z² hierarchy:
    Simple (CUBE) → Complex (SPHERE) → Recognition (Z²)
""")

# =============================================================================
# PART 6: COLOR VISION - Z² OPPONENCY
# =============================================================================

print("=" * 70)
print("PART 6: COLOR VISION - Z² COLOR SPACE")
print("=" * 70)

print(f"""
COLOR PERCEPTION:

  We see millions of colors from just 3 cone types.
  This is efficient CUBE encoding of SPHERE wavelengths.

OPPONENT CHANNELS:

  Color is processed as 3 opponent channels:

  1. Red-Green (L-M cones)
  2. Blue-Yellow (S vs L+M)
  3. Luminance (L+M, brightness)

  3 channels = SPHERE coefficient

  This is more efficient than raw LMS.
  Opponent processing happens in retina and LGN.

COLOR CONSTANCY:

  We perceive colors consistently despite illumination changes.
  This requires comparing across the scene.

  The visual system estimates:
    - Illuminant color
    - Surface reflectance

  2 estimates = factor of 2 in Z

COLOR CATEGORIES:

  Basic color terms (Berlin & Kay):
    - Black, white
    - Red, green, blue, yellow
    - Brown, purple, pink, orange, grey

  11 basic terms ≈ 2Z ≈ 11.6

  Or: 6 chromatic + 2 achromatic = 8 primary = CUBE

COLOR BLINDNESS:

  Genetic absence of cone types:
    - Protanopia (no L cones, "red-blind")
    - Deuteranopia (no M cones, "green-blind")
    - Tritanopia (no S cones, "blue-blind")

  3 types = SPHERE coefficient (matching 3 cones)

  ~8% of males affected (color blindness genes on X)
  8% ≈ 1/CUBE × 64% (roughly)

THE VISIBLE SPECTRUM:

  Human vision: ~380-700 nm
  Range: ~320 nm

  320 ≈ 10 × Z² ≈ 10 × 33 = 330 nm (close!)

  Peak sensitivity: ~555 nm (yellow-green)
  555 ≈ 17 × Z² ≈ 17 × 33 = 561 nm (close!)
""")

# =============================================================================
# PART 7: MOTION AND DEPTH - Z² 3D PERCEPTION
# =============================================================================

print("=" * 70)
print("PART 7: MOTION AND DEPTH - Z² SPATIAL VISION")
print("=" * 70)

print(f"""
MOTION PERCEPTION:

  Detecting movement is crucial for survival.
  Specialized pathway (dorsal, MT/V5).

MOTION PROCESSING:

  Levels:
    1. Local motion (V1, direction-selective cells)
    2. Pattern motion (MT, integrates local)
    3. Object motion (MST, heading, optic flow)
    4. Action perception (STS, biological motion)

  4 levels = Bekenstein!

SMOOTH PURSUIT:

  Eyes track moving objects.
  Requires matching eye velocity to target velocity.

  Gain: ~0.9 (eyes slightly lag target)
  Latency: ~100-150 ms to initiate

  100 ms ≈ 3Z² ms (rough)

DEPTH PERCEPTION:

  We perceive 3D from 2D retinal images.

  Cues:
    BINOCULAR:
      - Stereopsis (disparity between eyes)

    MONOCULAR:
      - Perspective
      - Texture gradient
      - Motion parallax
      - Occlusion
      - Size constancy
      - Shading/shadows

  ~8 depth cues = CUBE!

STEREOPSIS:

  Two eyes see slightly different views.
  Disparity → Depth perception.

  Eye separation: ~6 cm = ~Z cm!
  (Actually ~6.3 cm average)

  Binocular neurons in V1/V2 compute disparity.
  Tuned to specific disparities (near, far, zero).

MOTION SICKNESS:

  Mismatch between visual and vestibular signals.
  The Z² system expects consistency.

  When inconsistent:
    - Nausea, dizziness
    - Conflict resolution attempts
    - System confusion

  4 main symptoms = Bekenstein (nausea, sweating, pallor, vomiting)
""")

# =============================================================================
# PART 8: ATTENTION AND AWARENESS
# =============================================================================

print("=" * 70)
print("PART 8: VISUAL ATTENTION - Z² SELECTION")
print("=" * 70)

print(f"""
VISUAL ATTENTION:

  We can't process everything - attention selects.
  This is CUBE selection from SPHERE visual field.

ATTENTIONAL CAPACITY:

  How many objects can we track?
    ~4 objects = Bekenstein!

  Multiple object tracking (MOT) experiments confirm this.

TYPES OF ATTENTION:

  1. Bottom-up (stimulus-driven, "pop-out")
  2. Top-down (goal-driven, search)

  2 types = factor of 2 in Z

FEATURE INTEGRATION:

  Treisman's theory:
    - Features detected in parallel (SPHERE)
    - Binding requires attention (CUBE)
    - Object perception = Z² (features bound)

CHANGE BLINDNESS:

  We miss obvious changes when attention is elsewhere.
  This shows the CUBE capacity limit.

  The visual system creates illusion of full awareness
  from sparse CUBE sampling of SPHERE visual field.

VISUAL SEARCH:

  Finding target among distractors.

  Feature search: Parallel, fast (SPHERE)
  Conjunction search: Serial, slow (CUBE)

  2 modes = factor of 2 in Z

INATTENTIONAL BLINDNESS:

  Failing to see obvious objects when attending elsewhere.
  Famous example: Gorilla in basketball game video.

  This demonstrates:
    - Attention is required for awareness
    - CUBE capacity is severely limited
    - Z² creates subjective completeness from sparse samples
""")

# =============================================================================
# PART 9: VISUAL CONSCIOUSNESS
# =============================================================================

print("=" * 70)
print("PART 9: VISUAL CONSCIOUSNESS - Z² SEEING")
print("=" * 70)

print(f"""
WHAT IS SEEING?

  Vision is not just detection - it's EXPERIENCE.
  Why do photons create subjective visual awareness?

THE BINDING PROBLEM:

  Features are processed separately:
    - Color (V4)
    - Motion (MT)
    - Shape (IT)
    - Location (parietal)

  How are they BOUND into unified percept?

  Answer: Z²

  CUBE (discrete features) × SPHERE (unified field) = Z² percept

NEURAL CORRELATES:

  What brain activity correlates with visual awareness?

  Candidates:
    - V1 activity (necessary but not sufficient)
    - Higher areas (IT, PFC)
    - Feedback connections
    - Gamma synchrony

  4 candidate mechanisms = Bekenstein!

BINOCULAR RIVALRY:

  Different images to each eye → alternating percepts.
  One image dominates at a time.

  Alternation rate: ~2-3 seconds per switch
  2-3 ≈ SPHERE coefficient / 1-1.5

  This shows:
    - Perception is competitive
    - Brain "decides" what to see
    - Z² selects CUBE from SPHERE possibilities

VISUAL ILLUSIONS:

  Illusions reveal processing assumptions.

  Types:
    - Geometrical (angles, lengths)
    - Color (contrast, constancy)
    - Motion (aftereffects, apparent motion)
    - 3D (impossible figures)

  4 types = Bekenstein!

  Illusions are Z² trying to make CUBE sense of SPHERE input.

BLINDSIGHT:

  Damage to V1 → Conscious blindness.
  But: Can still respond to visual stimuli!

  Shows: Vision without awareness is possible.
  V1 seems required for conscious Z² experience.
""")

# =============================================================================
# PART 10: SUMMARY
# =============================================================================

print("=" * 70)
print("SUMMARY: VISION AS Z² TRANSFORMATION")
print("=" * 70)

print(f"""
╔═══════════════════════════════════════════════════════════════════════╗
║            VISION: Z² FRAMEWORK                                       ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  THE EYE:                                                             ║
║                                                                       ║
║      4 optical elements = Bekenstein                                  ║
║      4 internal structures = Bekenstein                              ║
║      Diameter ~24 mm ≈ 4Z mm                                         ║
║      Pupil max 8 mm = CUBE mm                                        ║
║                                                                       ║
║  THE RETINA:                                                          ║
║                                                                       ║
║      3 cone types = SPHERE coefficient                               ║
║      4 computations = Bekenstein                                      ║
║      6 layers ≈ Z                                                    ║
║                                                                       ║
║  PHOTOTRANSDUCTION:                                                   ║
║                                                                       ║
║      4 main stages = Bekenstein                                       ║
║      4 recovery steps = Bekenstein                                    ║
║      ~10,000× amplification                                          ║
║                                                                       ║
║  VISUAL PATHWAY:                                                      ║
║                                                                       ║
║      LGN: 6 layers ≈ Z                                               ║
║      12 orientation columns = Gauge                                  ║
║      2 cortical streams = factor of 2 in Z                           ║
║                                                                       ║
║  COLOR:                                                               ║
║                                                                       ║
║      3 opponent channels = SPHERE coefficient                        ║
║      8 basic colors = CUBE                                           ║
║      Spectrum ~320 nm ≈ 10 × Z²                                      ║
║                                                                       ║
║  ATTENTION:                                                           ║
║                                                                       ║
║      ~4 objects tracked = Bekenstein                                 ║
║      4 illusion types = Bekenstein                                    ║
║      2 attention types = factor of 2 in Z                            ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════════════

VISION IS Z² TRANSFORMATION:

    Light (SPHERE, continuous wavelengths)
    → Photoreceptors (CUBE, discrete detection)
    → Neural processing (Z², hierarchical integration)
    → Perception (CUBE, discrete objects in SPHERE visual field)

    We see through Z²:
        CUBE (discrete features) × SPHERE (unified awareness)
        = Visual experience

    The world appears unified (SPHERE)
    but is constructed from discrete samples (CUBE).
    This is the Z² of seeing.

═══════════════════════════════════════════════════════════════════════════
""")

print("\n[VISION_Z2_DERIVATION.py complete]")
