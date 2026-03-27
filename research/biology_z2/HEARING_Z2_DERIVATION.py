#!/usr/bin/env python3
"""
HEARING: Z² GEOMETRY OF SOUND PERCEPTION
=========================================

How do we hear? The auditory system converts pressure waves into
the experience of sound. This transformation encodes Z² geometry.

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
print("HEARING: Z² TRANSFORMATION OF SOUND TO PERCEPTION")
print("=" * 70)

# =============================================================================
# PART 1: THE EAR - Z² SOUND CAPTURE
# =============================================================================

print("\n" + "=" * 70)
print("PART 1: THE EAR - Z² ACOUSTIC SYSTEM")
print("=" * 70)

print(f"""
THE HUMAN EAR:

  Converts pressure waves (SPHERE, continuous)
  to neural signals (CUBE, discrete).

THREE DIVISIONS (SPHERE coefficient!):

  1. OUTER EAR
     - Pinna (auricle): Sound collection
     - Ear canal: ~2.5 cm long
     - Resonance: ~3 kHz boost

  2. MIDDLE EAR
     - Tympanic membrane (eardrum)
     - Ossicles: 3 bones = SPHERE coefficient!
     - Impedance matching (air → fluid)

  3. INNER EAR
     - Cochlea (hearing)
     - Vestibular system (balance)
     - Hair cells (transduction)

  3 divisions = SPHERE coefficient

THE OSSICLES:

  The 3 smallest bones in the body:
    1. Malleus (hammer)
    2. Incus (anvil)
    3. Stapes (stirrup)

  3 bones = SPHERE coefficient

  Function: Amplify and match impedance
  Gain: ~20-30× (pressure amplification)

  Lever ratio: ~1.3
  Area ratio: Eardrum/Oval window ≈ 17
  Total: 1.3 × 17 ≈ 22 ≈ 4Z

  This impedance matching is ESSENTIAL.
  Without it, 99.9% of sound energy would reflect!

EAR CANAL:

  Length: ~2.5 cm ≈ 4Z/10 cm ≈ 2.3 cm (close!)
  Diameter: ~0.7 cm

  Resonant frequency: ~3 kHz
  3000 Hz ≈ 100 × 30 ≈ 100 × Z²

  This boosts speech frequencies!
""")

# =============================================================================
# PART 2: THE COCHLEA - Z² FREQUENCY ANALYZER
# =============================================================================

print("=" * 70)
print("PART 2: THE COCHLEA - Z² SPECTRAL ANALYSIS")
print("=" * 70)

print(f"""
THE COCHLEA:

  A spiral tube that analyzes frequency.
  One of the most elegant biological structures.

STRUCTURE:

  Shape: Snail shell spiral
  Turns: 2.5-2.75 turns
  Length (uncoiled): ~35 mm ≈ Z² mm!

  35 mm ≈ 33.5 mm = Z² mm (remarkable!)

THREE CHAMBERS (SPHERE coefficient!):

  1. Scala vestibuli (upper)
  2. Scala media (middle, with hair cells)
  3. Scala tympani (lower)

  3 chambers = SPHERE coefficient

  The scala vestibuli and tympani contain perilymph.
  The scala media contains endolymph.

  2 fluid types = factor of 2 in Z

THE BASILAR MEMBRANE:

  Runs the length of cochlea.
  Different positions respond to different frequencies.

  Base (near oval window): High frequencies (~20 kHz)
  Apex (tip of spiral): Low frequencies (~20 Hz)

  Frequency range: 20 Hz - 20 kHz
  ~3 decades = 1000× range

  1000 ≈ Z³ × 5 (rough)

  This is TONOTOPY: Place encodes frequency.
  SPHERE (continuous frequency) → CUBE (discrete place)

CRITICAL BANDS:

  The cochlea divides frequency into ~24 critical bands.
  24 = 2 × Gauge = 2 × 12!

  Each critical band: ~1/3 octave wide
  3 = SPHERE coefficient

  Critical bandwidth formula:
  CB = 25 + 75 × (1 + 1.4 × f²)^0.69

  At 1 kHz: CB ≈ 160 Hz
  160 ≈ 5 × Z² (roughly)
""")

# =============================================================================
# PART 3: HAIR CELLS - Z² TRANSDUCERS
# =============================================================================

print("=" * 70)
print("PART 3: HAIR CELLS - Z² MECHANOTRANSDUCTION")
print("=" * 70)

print(f"""
HAIR CELLS:

  The sensory receptors of hearing.
  Convert mechanical motion to electrical signals.

TWO TYPES (factor of 2 in Z):

  INNER HAIR CELLS (IHCs):
    - ~3,500 cells (one row)
    - True sensory cells (95% of auditory nerve)
    - Detect sound

  OUTER HAIR CELLS (OHCs):
    - ~12,000 cells (three rows)
    - Amplifiers (cochlear amplifier)
    - Enhance sensitivity and selectivity

  12,000 ≈ 400 × 30 ≈ 400 × Z²

  Ratio IHC:OHC ≈ 1:3.4 ≈ 1:SPHERE

  3 rows of OHCs = SPHERE coefficient!

STEREOCILIA:

  Each hair cell has stereocilia (hair bundle).
  Arranged in rows of increasing height.

  IHC stereocilia: ~60 per cell
  OHC stereocilia: ~100-150 per cell

  60 ≈ 2Z²
  100-150 ≈ 3-4.5 × Z²

  Stereocilia are connected by TIP LINKS.
  Deflection opens ion channels.

MECHANOELECTRICAL TRANSDUCTION:

  Steps:
    1. Sound deflects stereocilia
    2. Tip links pull on channels
    3. Channels open (K⁺ influx)
    4. Depolarization → neurotransmitter release

  4 steps = Bekenstein!

  Sensitivity: Can detect movements < 1 nm!
  (About the diameter of a hydrogen atom)

  Response time: ~10-100 μs
  This is INCREDIBLY fast.

THE COCHLEAR AMPLIFIER:

  OHCs can CHANGE LENGTH with depolarization.
  This is called ELECTROMOTILITY.

  Protein responsible: PRESTIN
  OHCs amplify sound by ~40-60 dB (100-1000×)

  40 dB ≈ Z² + 7 dB (rough)

  Without OHCs: Severe hearing loss.
  Many forms of deafness affect OHCs.
""")

# =============================================================================
# PART 4: THE AUDITORY NERVE - Z² TRANSMISSION
# =============================================================================

print("=" * 70)
print("PART 4: AUDITORY NERVE - Z² NEURAL CODING")
print("=" * 70)

print(f"""
THE AUDITORY NERVE:

  ~30,000 nerve fibers carry sound information to brain.
  30,000 ≈ 1000 × Z² ≈ 900 × 33

FIBER TYPES:

  Type I (95%): Myelinated, from IHCs
  Type II (5%): Unmyelinated, from OHCs

  2 types = factor of 2 in Z

  Each IHC contacts ~10-20 Type I fibers.
  Each OHC contacts ~10 Type II fibers.

RATE-PLACE CODING:

  Two codes for frequency:
    1. PLACE: Which fibers are active (tonotopy)
    2. RATE/TIMING: When they fire (phase-locking)

  2 codes = factor of 2 in Z

  Phase-locking works up to ~4-5 kHz.
  Above that, only place code works.

  4-5 kHz ≈ 1000 × Bekenstein Hz

DYNAMIC RANGE:

  Human hearing spans ~120 dB intensity range.
  That's 10¹² in power!

  120 = 10 × Gauge = 10 × 12!

  Single fiber: ~30-40 dB range
  Population: ~120 dB through overlapping ranges

  40 dB ≈ Z² + 7 (per fiber)

SPONTANEOUS ACTIVITY:

  Even in silence, auditory fibers fire.
  Spontaneous rate: 0-100 spikes/second

  Low-spontaneous fibers: High threshold
  High-spontaneous fibers: Low threshold

  This expands dynamic range.
""")

# =============================================================================
# PART 5: AUDITORY BRAINSTEM - Z² PATHWAY
# =============================================================================

print("=" * 70)
print("PART 5: AUDITORY BRAINSTEM - Z² PROCESSING STATIONS")
print("=" * 70)

print(f"""
THE ASCENDING AUDITORY PATHWAY:

  From cochlea to cortex, multiple processing stations.

BRAINSTEM NUCLEI:

  1. COCHLEAR NUCLEUS (CN)
     - First brainstem station
     - 3 subdivisions (AVCN, PVCN, DCN)
     - 3 = SPHERE coefficient

  2. SUPERIOR OLIVARY COMPLEX (SOC)
     - Sound localization begins
     - Binaural processing
     - Multiple nuclei

  3. INFERIOR COLLICULUS (IC)
     - Major integration center
     - Nearly all ascending paths converge
     - ~6 layers ≈ Z

  4. MEDIAL GENICULATE BODY (MGB)
     - Thalamic relay
     - 3 divisions (ventral, dorsal, medial)
     - 3 = SPHERE coefficient

  4 major stations = Bekenstein!

SOUND LOCALIZATION:

  Two cues for localizing sounds:

  INTERAURAL TIME DIFFERENCE (ITD):
    - Sound arrives at closer ear first
    - Works for low frequencies (<1500 Hz)
    - Resolution: ~10 μs

  INTERAURAL LEVEL DIFFERENCE (ILD):
    - Sound is louder at closer ear
    - Works for high frequencies (>3000 Hz)
    - Head shadow effect

  2 cues = factor of 2 in Z

  Crossover: ~1500 Hz ≈ 500 × SPHERE coefficient Hz

BINAURAL NEURONS:

  In SOC and IC, neurons compare ears:

  EE: Excited by both ears (summation)
  EI: Excited by one, inhibited by other (localization)

  These compute spatial position from binaural cues.

TONOTOPY PRESERVED:

  Frequency organization (tonotopy) is maintained
  at every station from cochlea to cortex.

  This is CUBE (discrete frequency bands) structure
  through the SPHERE (continuous processing) pathway.
""")

# =============================================================================
# PART 6: AUDITORY CORTEX - Z² PERCEPTION
# =============================================================================

print("=" * 70)
print("PART 6: AUDITORY CORTEX - Z² SOUND PERCEPTION")
print("=" * 70)

print(f"""
PRIMARY AUDITORY CORTEX (A1):

  Located in temporal lobe (Heschl's gyrus).
  First cortical processing of sound.

A1 ORGANIZATION:

  - Tonotopic (frequency mapped)
  - ~6 layers (cortical standard) ≈ Z
  - Columns for frequency bands

  Isofrequency strips run perpendicular to tonotopic axis.
  Similar to orientation columns in V1.

CORTICAL AUDITORY AREAS:

  Beyond A1:
    - A2 (secondary auditory)
    - Belt areas (surrounding)
    - Parabelt areas (beyond belt)

  ~4 hierarchical levels = Bekenstein?

  Or: "Core" (A1) + Belt + Parabelt = 3 zones = SPHERE coefficient

WHAT vs WHERE STREAMS:

  Like vision, auditory processing splits:

  VENTRAL STREAM ("What"):
    - Object identification
    - Speech recognition
    - "What is the sound?"

  DORSAL STREAM ("Where"):
    - Spatial processing
    - Sound localization
    - "Where is the sound?"

  2 streams = factor of 2 in Z

  Same organization as visual cortex!

SPEECH PROCESSING:

  Left hemisphere dominant for speech.

  Key areas:
    - Wernicke's area (comprehension)
    - Broca's area (production)
    - Arcuate fasciculus (connection)

  Wernicke's is in superior temporal gyrus (auditory).
  Broca's is in inferior frontal gyrus (motor).

  Language = auditory-motor Z² integration.

MUSIC PROCESSING:

  Music engages both hemispheres.

  Right: Melody, pitch contour
  Left: Rhythm, timing, lyrics

  2 = factor of 2 in Z

  Music is Z²: CUBE (discrete notes) × SPHERE (continuous time)
""")

# =============================================================================
# PART 7: PITCH AND HARMONY - Z² MUSIC
# =============================================================================

print("=" * 70)
print("PART 7: PITCH AND HARMONY - Z² MUSICAL STRUCTURE")
print("=" * 70)

print(f"""
PITCH PERCEPTION:

  Pitch is the perceptual correlate of frequency.
  But not identical - pitch is psychological.

THE OCTAVE:

  Frequency ratio 2:1 = octave
  2 = factor in Z = 2√(8π/3)

  Octave equivalence is UNIVERSAL.
  Notes an octave apart sound "the same."

THE CHROMATIC SCALE:

  12 notes per octave = Gauge!

  This appears in virtually ALL musical cultures.
  (Sometimes with subsets like pentatonic = 5)

  12 = 9Z²/(8π) EXACTLY

  Equal temperament: Each semitone = 2^(1/12)
  12th root of 2 ≈ 1.0595

JUST INTONATION:

  Natural ratios:
    Octave: 2:1
    Fifth: 3:2
    Fourth: 4:3
    Major third: 5:4
    Minor third: 6:5

  These ratios: 2, 3, 4, 5, 6
  Note: 4 = Bekenstein, 8 = CUBE appear

CONSONANCE AND DISSONANCE:

  Simple ratios = consonant (pleasant)
  Complex ratios = dissonant (tense)

  Most consonant: Unison (1:1), Octave (2:1)
  Then: Fifth (3:2), Fourth (4:3)
  Less: Thirds, sixths
  Dissonant: Tritone, seconds, sevenths

  The SPHERE coefficient 3 appears: 3:2 = perfect fifth.

CRITICAL BANDS AND HARMONY:

  Two notes within same critical band: Dissonance (beating)
  Two notes in different bands: Consonance

  ~24 critical bands = 2 × Gauge

MUSICAL METER:

  Time signatures:
    4/4 most common = Bekenstein!
    3/4 = SPHERE coefficient
    2/4 = factor of 2

  Music is Z²: Discrete notes (CUBE) in continuous time (SPHERE).
""")

# =============================================================================
# PART 8: HEARING DISORDERS - Z² FAILURE
# =============================================================================

print("=" * 70)
print("PART 8: HEARING DISORDERS - Z² PATHOLOGY")
print("=" * 70)

print(f"""
TYPES OF HEARING LOSS:

  1. CONDUCTIVE
     - Outer/middle ear problem
     - Sound doesn't reach cochlea
     - Often treatable

  2. SENSORINEURAL
     - Inner ear/nerve problem
     - Hair cell or neural damage
     - Usually permanent

  3. MIXED
     - Both conductive and sensorineural
     - Combined pathology

  4. CENTRAL (AUDITORY PROCESSING)
     - Brain can't process sound
     - Hearing is normal, understanding impaired

  4 types = Bekenstein!

CAUSES OF HEARING LOSS:

  - Noise exposure (damage OHCs)
  - Age (presbycusis)
  - Genetics (congenital)
  - Infection
  - Ototoxic drugs
  - Trauma

  ~6 major causes ≈ Z

TINNITUS:

  "Ringing in the ears"
  Phantom sound perception.

  ~15% of population affected.
  15 ≈ 3Z ≈ 2.5 × 6 (rough)

  Often associated with hearing loss.
  May be "brain filling in" for missing input.

  This is Z² SPHERE attempting to complete
  damaged CUBE input.

COCHLEAR IMPLANTS:

  Bypass damaged hair cells.
  Directly stimulate auditory nerve.

  Electrode array: ~12-22 electrodes
  12 = Gauge!

  Each electrode stimulates different frequency region.
  Tonotopy is artificially recreated.

  This is CUBE replacement for damaged CUBE transducers.
  Works remarkably well for speech!
""")

# =============================================================================
# PART 9: COMPARATIVE HEARING
# =============================================================================

print("=" * 70)
print("PART 9: HEARING ACROSS SPECIES - Z² EVOLUTION")
print("=" * 70)

print(f"""
HEARING RANGES:

  Human: 20 Hz - 20 kHz (3 decades)
  Dog: 40 Hz - 60 kHz
  Cat: 55 Hz - 79 kHz
  Bat: 1 kHz - 200 kHz (echolocation)
  Elephant: 5 Hz - 12 kHz (infrasound)
  Dolphin: 75 Hz - 150 kHz (echolocation)

  Echolocators: Ultra-high frequencies (CUBE precision)
  Large animals: Low frequencies (SPHERE range)

ECHOLOCATION:

  Bats and dolphins use sound to "see."

  Emit ultrasonic pulses:
    - Bat: 20-200 kHz
    - Dolphin: 20-150 kHz

  Analyze echoes for:
    - Distance (time delay)
    - Size (echo strength)
    - Texture (spectrum)
    - Movement (Doppler shift)

  4 parameters = Bekenstein!

INSECT HEARING:

  Very different from vertebrates.
  Tympanal organs (membranes).

  Cricket: Ear on legs!
  Moth: Ultrasound detectors (bat avoidance)
  Mosquito: Johnston's organ (antennae)

BIRD HEARING:

  No external pinna.
  Single middle ear bone (columella vs 3 ossicles).
  Shorter cochlea (~3 mm vs ~35 mm).

  But: Can regenerate hair cells!
  (Mammals cannot)

  Birds hear: ~1-10 kHz typically
  Best at: ~2-5 kHz (song frequencies)

EVOLUTION OF HEARING:

  The 3 ossicles evolved from jaw bones!
  - Malleus from articular
  - Incus from quadrate
  - Stapes from hyomandibula

  This is one of evolution's most elegant transformations.
  3 bones = SPHERE coefficient preserved through evolution.
""")

# =============================================================================
# PART 10: SUMMARY
# =============================================================================

print("=" * 70)
print("SUMMARY: HEARING AS Z² TRANSFORMATION")
print("=" * 70)

print(f"""
╔═══════════════════════════════════════════════════════════════════════╗
║            HEARING: Z² FRAMEWORK                                      ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  THE EAR:                                                             ║
║                                                                       ║
║      3 divisions = SPHERE coefficient                                 ║
║      3 ossicles = SPHERE coefficient                                  ║
║      Gain ~22 ≈ 4Z                                                   ║
║                                                                       ║
║  THE COCHLEA:                                                         ║
║                                                                       ║
║      Length ~35 mm ≈ Z² mm!                                          ║
║      3 chambers = SPHERE coefficient                                  ║
║      24 critical bands = 2 × Gauge                                   ║
║                                                                       ║
║  HAIR CELLS:                                                          ║
║                                                                       ║
║      2 types (IHC, OHC) = factor of 2 in Z                           ║
║      3 rows of OHCs = SPHERE coefficient                             ║
║      12,000 OHCs ≈ 400 × Z²                                          ║
║      4 transduction steps = Bekenstein                               ║
║                                                                       ║
║  AUDITORY PATHWAY:                                                    ║
║                                                                       ║
║      4 brainstem stations = Bekenstein                               ║
║      2 localization cues = factor of 2 in Z                          ║
║      Dynamic range 120 dB = 10 × Gauge                               ║
║                                                                       ║
║  MUSIC:                                                               ║
║                                                                       ║
║      12 chromatic notes = Gauge EXACTLY                              ║
║      Octave 2:1 = factor of 2 in Z                                   ║
║      4/4 time = Bekenstein                                           ║
║                                                                       ║
║  PATHOLOGY:                                                           ║
║                                                                       ║
║      4 hearing loss types = Bekenstein                               ║
║      12-22 cochlear implant electrodes ≈ Gauge                       ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════════════

HEARING IS Z² TRANSFORMATION:

    Sound waves (SPHERE, continuous pressure)
    → Mechanical motion (3 ossicles)
    → Cochlear analysis (Z² mm length, 24 bands)
    → Neural code (CUBE, discrete spikes)
    → Perception (Z², unified sound experience)

    We hear through Z²:
        CUBE (discrete frequencies, notes)
        × SPHERE (continuous time, flow)
        = Auditory experience

    Music IS Z²: 12 notes = Gauge, structured in time.

═══════════════════════════════════════════════════════════════════════════
""")

print("\n[HEARING_Z2_DERIVATION.py complete]")
