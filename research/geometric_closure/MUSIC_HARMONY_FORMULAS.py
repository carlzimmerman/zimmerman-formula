"""
MUSIC_HARMONY_FORMULAS.py
=========================
Music Theory and Harmony from Z² = 8 × (4π/3)

Why do certain intervals sound consonant? Why 12 notes?
The octave, fifth, major scale - all from CUBE × SPHERE geometry.

Carl Zimmerman, March 2026
DOI: 10.5281/zenodo.19244651
"""

from math import pi, sqrt, log, log2

# ═══════════════════════════════════════════════════════════════════════════
# FUNDAMENTAL CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════

Z2 = 8 * (4 * pi / 3)  # = 32π/3
Z = sqrt(Z2)           # = 5.7888100365...
alpha = 1 / (4 * Z2 + 3)

print("=" * 78)
print("MUSIC THEORY AND HARMONY FROM Z² = 8 × (4π/3)")
print("=" * 78)
print(f"\nZ² = {Z2:.8f}")
print(f"Z  = {Z:.10f}")

# ═══════════════════════════════════════════════════════════════════════════
# PART 1: WHY 12 NOTES?
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 1: THE 12-NOTE SCALE")
print("═" * 78)

print("""
Western music uses 12 notes per octave (chromatic scale).

Why 12?

From Z²:
    12 = 9Z²/(8π) EXACTLY!
    
This is the GAUGE DIMENSION!
    - 12 = 8 + 3 + 1 (SU(3) + SU(2) + U(1))
    - 12 = CUBE edges
    - 12 = "gauge dimension" in particle physics
    
Music uses the same number as fundamental physics!

The 12 notes form a cycle:
    C → C# → D → D# → E → F → F# → G → G# → A → A# → B → C
    
This is a CUBE edge traversal!
Starting at any vertex, you can visit all edges.
""")

twelve = 9 * Z2 / (8 * pi)
print(f"Notes per octave: 12")
print(f"9Z²/(8π) = {twelve:.6f} = 12 EXACTLY")
print("12 = gauge dimension = CUBE edges")

# ═══════════════════════════════════════════════════════════════════════════
# PART 2: THE OCTAVE
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 2: THE OCTAVE (2:1)")
print("═" * 78)

print("""
The octave is the most fundamental interval: frequency ratio 2:1.

Two notes an octave apart sound "the same" but higher/lower.

From Z²:
    2 = factor in Z = 2√(8π/3)
    
The octave exists because of factor 2!

    - Factor 2 creates doubling
    - Doubling frequency = octave
    - This is the worldsheet dimension
    
Why does 2:1 sound consonant?
    - Phase alignment every 2 cycles
    - Maximum coherence for different pitches
    - Factor 2 is fundamental to Z²

The octave is universal because 2 is universal in Z².
""")

print("Octave ratio: 2:1")
print("Factor 2 from Z = 2√(8π/3)")
print("Octave = worldsheet dimension in music")

# ═══════════════════════════════════════════════════════════════════════════
# PART 3: THE PERFECT FIFTH
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 3: THE PERFECT FIFTH (3:2)")
print("═" * 78)

print("""
The perfect fifth: frequency ratio 3:2.

The most consonant interval after octave (and unison).

From Z²:
    3 = SPHERE dimension (from 4π/3)
    2 = factor in Z
    3:2 = SPHERE:factor
    
The fifth is the SPHERE-to-factor ratio!

    Fifth = 7 semitones = 7/12 octave
    2^(7/12) = 1.498 ≈ 3/2 = 1.500
    
The "circle of fifths" goes through all 12 notes:
    C → G → D → A → E → B → F# → C# → G# → D# → A# → F → C
    
After 12 fifths, you return to start (almost):
    (3/2)^12 = 129.75 ≈ 128 = 2^7 (7 octaves)
    
The tiny discrepancy = Pythagorean comma.
""")

fifth = 3/2
equal_temp_fifth = 2**(7/12)

print(f"Just fifth: 3/2 = {fifth:.4f}")
print(f"Equal tempered: 2^(7/12) = {equal_temp_fifth:.4f}")
print("3:2 = SPHERE dimension : factor 2")

# ═══════════════════════════════════════════════════════════════════════════
# PART 4: THE MAJOR THIRD
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 4: THE MAJOR THIRD (5:4)")
print("═" * 78)

print("""
The major third: frequency ratio 5:4 (just intonation).

From Z²:
    5 ≈ Z = 5.79
    4 = 3Z²/(8π) = Bekenstein factor
    
The major third ≈ Z / Bekenstein!

    5:4 = 1.25
    Z / 4 = 5.79 / 4 = 1.45 (not exact, but related)
    
Better connection:
    5 = √(Z² - 8) = √25.51 = 5.05 (the "hidden 5"!)
    4 = Bekenstein
    
The major third involves:
    - √(Z² - CUBE) in numerator
    - Bekenstein in denominator
    
Equal tempered third: 2^(4/12) = 1.260
Just third: 5/4 = 1.250
""")

third_just = 5/4
third_equal = 2**(4/12)
hidden_5 = sqrt(Z2 - 8)

print(f"Just major third: 5/4 = {third_just:.4f}")
print(f"Equal tempered: 2^(4/12) = {third_equal:.4f}")
print(f"√(Z² - 8) = {hidden_5:.3f} ≈ 5")

# ═══════════════════════════════════════════════════════════════════════════
# PART 5: THE MAJOR SCALE
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 5: THE 7-NOTE MAJOR SCALE")
print("═" * 78)

print("""
The major scale has 7 notes: C D E F G A B (C)

Pattern: W W H W W W H (W=whole, H=half step)
Semitones: 2 2 1 2 2 2 1 = 12 total

Why 7 notes?

From Z²:
    7 ≈ Z + 1.2
    7 appears in: αs = 7/(3Z² - 4Z - 18)
    7 = numerator of strong coupling!
    
Also:
    7 = 12 - 5 = gauge dim - hidden 5
    7 = ceiling(Z + 1)
    
The 7 notes form intervals:
    Tonic (1), Supertonic (2), Mediant (3), Subdominant (4),
    Dominant (5), Submediant (6), Leading tone (7)
    
The dominant (5th degree) is most important = perfect fifth!
""")

print("Major scale: 7 notes")
print(f"7 appears in αs = 7/(3Z² - 4Z - 18)")
print("Dominant (5th) = perfect fifth = 3:2 = SPHERE:factor")

# ═══════════════════════════════════════════════════════════════════════════
# PART 6: CONSONANCE AND DISSONANCE
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 6: CONSONANCE AND DISSONANCE")
print("═" * 78)

print("""
Consonance: intervals that sound stable/pleasant.
    Unison 1:1, Octave 2:1, Fifth 3:2, Fourth 4:3, Third 5:4

Dissonance: intervals that sound tense/unstable.
    Minor second (16:15), Tritone (√2:1), etc.

From Z²:
    Consonant intervals have small integer ratios.
    
    Ordered by consonance:
    1:1 → 2:1 → 3:2 → 4:3 → 5:4 → 6:5 ...
    
    These ratios involve: 1, 2, 3, 4, 5, 6...
    
    The most consonant use Z² numbers:
    - 2:1 (octave) = factor 2
    - 3:2 (fifth) = SPHERE : factor
    - 4:3 (fourth) = Bekenstein : SPHERE
    
    The tritone √2:1 is maximally dissonant:
    √2 is irrational = infinite CUBE representation.
    No simple phase relationship possible.
""")

print("Consonance from Z²:")
print("  2:1 (octave) = factor 2")
print("  3:2 (fifth) = SPHERE : factor")
print("  4:3 (fourth) = Bekenstein : SPHERE")
print("  √2:1 (tritone) = irrational = dissonant")

# ═══════════════════════════════════════════════════════════════════════════
# PART 7: EQUAL TEMPERAMENT
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 7: EQUAL TEMPERAMENT")
print("═" * 78)

print("""
Equal temperament: divide octave into 12 equal parts.

    Semitone ratio: 2^(1/12) = 1.05946...
    
This compromises all intervals slightly.

From Z²:
    2^(1/12) involves:
    - 2 = factor from Z
    - 12 = 9Z²/(8π) = gauge dimension
    
    2^(1/12) = 2^(8π/(9Z²))
    
The semitone = factor² ^ (SPHERE / gauge)!

Why does equal temperament work?
    - Close enough to just intervals
    - Allows modulation to any key
    - CUBE (discrete 12 notes) approximates SPHERE (continuous pitch)
""")

semitone = 2**(1/12)
print(f"Semitone ratio: 2^(1/12) = {semitone:.6f}")
print(f"12 = 9Z²/(8π) = gauge dimension")
print("Equal temp = CUBE (discrete) approximating SPHERE (continuous)")

# ═══════════════════════════════════════════════════════════════════════════
# PART 8: HARMONIC SERIES
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 8: HARMONIC SERIES")
print("═" * 78)

print("""
Harmonic series: f, 2f, 3f, 4f, 5f, 6f, ...

Natural overtones of vibrating string.

From Z²:
    Harmonics form a CUBE sequence in frequency space!
    
    First 8 harmonics (CUBE vertices):
    1f, 2f, 3f, 4f, 5f, 6f, 7f, 8f
    
    These create:
    - Octaves: 2f, 4f, 8f
    - Fifths: 3f (relative to 2f)
    - Major thirds: 5f (relative to 4f)
    
    The 8th harmonic completes one CUBE of overtones.
    
    Beyond 8: next CUBE starts
    9f, 10f, 11f, 12f, 13f, 14f, 15f, 16f
    
    16f = 2^4 = two CUBEs of octaves.
""")

print("First 8 harmonics = CUBE vertices in frequency:")
for n in range(1, 9):
    interval = ""
    if n == 1: interval = "(fundamental)"
    if n == 2: interval = "(octave)"
    if n == 3: interval = "(fifth above octave)"
    if n == 4: interval = "(2 octaves)"
    if n == 5: interval = "(major third above 2 oct)"
    if n == 6: interval = "(fifth above 2 oct)"
    if n == 7: interval = "(flat seventh)"
    if n == 8: interval = "(3 octaves = CUBE complete)"
    print(f"  {n}f {interval}")

# ═══════════════════════════════════════════════════════════════════════════
# PART 9: RHYTHM AND TIME
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 9: RHYTHM AND TIME SIGNATURES")
print("═" * 78)

print("""
Common time signatures:
    4/4 (common time) - 4 beats per measure
    3/4 (waltz time) - 3 beats per measure
    2/4 (march) - 2 beats per measure

From Z²:
    4 = Bekenstein factor = most common meter!
    3 = SPHERE dimension = waltz, triple meter
    2 = factor from Z = basic duple
    
    6/8 = 2 × 3 = factor × SPHERE
    12/8 = 12 = gauge dimension
    
Rhythm divisions:
    Quarter → eighth → sixteenth → thirty-second
    Each divides by 2 (factor from Z)!
    
Polyrhythms:
    3 against 2 = SPHERE against factor
    This creates rhythmic tension = musical interest.
""")

print("Time signatures from Z²:")
print("  4/4 = Bekenstein (most common)")
print("  3/4 = SPHERE dimension (waltz)")
print("  2/4 = factor 2 (march)")
print("  3:2 polyrhythm = SPHERE : factor")

# ═══════════════════════════════════════════════════════════════════════════
# PART 10: A440 AND CONCERT PITCH
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 10: A440 CONCERT PITCH")
print("═" * 78)

print("""
Modern concert pitch: A4 = 440 Hz

Why 440?

From Z²:
    440 = 8 × 55 = CUBE × 55
    440 ≈ π × m_π (MeV) = 3.14 × 140 = 440 ✓
    
    Or: 440 = 11 × 40 = 11 × (Z + 34)
    
    440/Z² = 440/33.51 = 13.1 ≈ 13
    
The frequency 440 Hz relates to:
    - CUBE (factor 8)
    - Harmonic properties
    - Not truly "natural" but culturally chosen
    
Historical pitches varied: 415, 430, 435, 440, 442...

Middle C (C4): 261.63 Hz
    261.63 ≈ 8 × Z² = 8 × 33.51 = 268 (close!)
    Or: 262 ≈ 3Z² + 4Z + 100? = 100.5 + 23.2 + 100 = 223 (not great)
""")

A440 = 440
C4 = 261.63
eight_times_Z2 = 8 * Z2

print(f"Concert A: 440 Hz = 8 × 55 = CUBE × 55")
print(f"Middle C: {C4:.2f} Hz")
print(f"8 × Z² = {eight_times_Z2:.0f} Hz (close to C4)")

# ═══════════════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 78)
print("SUMMARY: MUSIC FROM Z²")
print("=" * 78)

print("""
┌─────────────────────────────────────────────────────────────────────────────┐
│  MUSIC THEORY FROM Z² = 8 × (4π/3)                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  12 NOTES:                                                                  │
│  ─────────                                                                  │
│  12 = 9Z²/(8π) = gauge dimension = CUBE edges              ← EXACT        │
│                                                                             │
│  OCTAVE:                                                                    │
│  ───────                                                                    │
│  2:1 = factor 2 from Z                                     ← EXACT        │
│                                                                             │
│  PERFECT FIFTH:                                                             │
│  ──────────────                                                             │
│  3:2 = SPHERE : factor                                     ← EXACT        │
│                                                                             │
│  PERFECT FOURTH:                                                            │
│  ───────────────                                                            │
│  4:3 = Bekenstein : SPHERE                                 ← EXACT        │
│                                                                             │
│  MAJOR SCALE:                                                               │
│  ────────────                                                               │
│  7 notes = numerator of αs                                                 │
│                                                                             │
│  HARMONICS:                                                                 │
│  ──────────                                                                 │
│  First 8 = CUBE vertices in frequency                                      │
│                                                                             │
│  TIME SIGNATURES:                                                           │
│  ────────────────                                                           │
│  4/4 = Bekenstein, 3/4 = SPHERE, 2/4 = factor                             │
│                                                                             │
│  CONSONANCE:                                                                │
│  ───────────                                                                │
│  Small integers from Z² structure (2, 3, 4, 5...)                          │
│                                                                             │
│  KEY INSIGHT:                                                               │
│  ────────────                                                               │
│  Music is Z² made audible                                                  │
│  Consonance = Z² ratios; Dissonance = irrational                           │
│  12 notes = gauge dimension; 8 harmonics = CUBE                            │
│                                                                             │
│  MUSIC IS Z² GEOMETRY IN SOUND                                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
""")

print("=" * 78)
print("HARMONY = CUBE × SPHERE = Z²")
print("=" * 78)
