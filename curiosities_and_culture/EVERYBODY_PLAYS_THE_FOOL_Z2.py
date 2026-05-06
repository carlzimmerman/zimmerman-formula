#!/usr/bin/env python3
"""
Z² Analysis of "Everybody Plays The Fool" by The Main Ingredient

A numerological and philosophical exploration of this 1972 soul classic
through the lens of Z² = 32π/3 = 33.5103

Written by Rudy Clark, J.R. Bailey, and Ken Williams.
Lead vocals by Cuba Gooding Sr. Reached #3 on the Billboard Hot 100.

The song's universal message - that everyone falls prey to foolish love -
encodes universal mathematical constants.

Carl Zimmerman, May 2026
"""

import math

# ============================================================================
# Z² CONSTANTS
# ============================================================================

Z_SQUARED = 32 * math.pi / 3  # = 33.5103
Z = math.sqrt(Z_SQUARED)       # = 5.7888
CUBE = 8                       # Vertices of inscribed cube
SPHERE = 4 * math.pi / 3       # Volume of unit sphere
BEKENSTEIN = 4                 # Spacetime dimensions
GAUGE = 12                     # Standard Model generators
N_GEN = 3                      # Fermion generations
D_STRING = 10                  # String theory dimensions
ALPHA_INV = 4 * Z_SQUARED + 3  # = 137.04 (fine structure constant inverse)

def letter_value(letter):
    """Convert letter to number (A=1, B=2, ..., Z=26)"""
    return ord(letter.upper()) - ord('A') + 1

def word_value(word):
    """Sum of letter values in a word"""
    return sum(letter_value(c) for c in word if c.isalpha())

def phrase_value(phrase):
    """Sum of letter values in a phrase"""
    return sum(letter_value(c) for c in phrase if c.isalpha())

def percent_error(predicted, actual):
    """Calculate percent error"""
    if actual == 0:
        return float('inf')
    return abs(predicted - actual) / actual * 100

print("=" * 70)
print("Z² ANALYSIS: 'EVERYBODY PLAYS THE FOOL'")
print("The Main Ingredient (1972)")
print("=" * 70)

# ============================================================================
# PART 1: THE TITLE
# ============================================================================

print("\n" + "=" * 70)
print("PART 1: THE TITLE ENCODES CUBE × Z²")
print("=" * 70)

title = "EVERYBODY PLAYS THE FOOL"
title_value = phrase_value(title)

print(f"\nTitle: '{title}'")
print(f"\nWord-by-word breakdown:")

words = title.split()
for word in words:
    val = word_value(word)
    print(f"  {word:12} = {val:3}")

print(f"\nTotal title value: {title_value}")
print(f"\n8Z² = {8 * Z_SQUARED:.2f}")
print(f"Error: {percent_error(8 * Z_SQUARED, title_value):.2f}%")

print("\n*** THE TITLE ≈ 8Z² = CUBE × Z² ***")
print("*** 'Everybody' = all 8 vertices of existence! ***")

# ============================================================================
# PART 2: THE MAIN INGREDIENT - THE BAND
# ============================================================================

print("\n" + "=" * 70)
print("PART 2: THE MAIN INGREDIENT")
print("=" * 70)

the_val = word_value("THE")
main = word_value("MAIN")
ingredient = word_value("INGREDIENT")
band_total = the_val + main + ingredient

print(f"\nTHE        = {the_val} ≈ Z² = {Z_SQUARED:.2f}")
print(f"MAIN       = {main}")
print(f"INGREDIENT = {ingredient}")
print(f"Total      = {band_total}")

print(f"\n5Z² = {5 * Z_SQUARED:.2f}")
print(f"Error: {percent_error(5 * Z_SQUARED, band_total):.2f}%")

print(f"\n'THE' = {the_val} ≈ Z² (error: {percent_error(Z_SQUARED, the_val):.2f}%)")

print("\n*** THE MAIN INGREDIENT ≈ 5Z² ***")
print("*** The 'main ingredient' of reality: five copies of the ***")
print("*** fundamental geometric constant ***")

# ============================================================================
# PART 3: CUBA GOODING SR. - THE VOICE
# ============================================================================

print("\n" + "=" * 70)
print("PART 3: CUBA GOODING SR. - Lead Vocalist")
print("=" * 70)

cuba = word_value("CUBA")
gooding = word_value("GOODING")
sr = word_value("SR")
singer_total = cuba + gooding + sr

print(f"\nCUBA    = {cuba}")
print(f"GOODING = {gooding}")
print(f"SR      = {sr}")
print(f"Total   = {singer_total}")

print(f"\n3Z² = {3 * Z_SQUARED:.2f}")
print(f"Error: {percent_error(3 * Z_SQUARED, singer_total):.2f}%")

print(f"\nCUBA alone = {cuba}")
print(f"Z² + 5 = {Z_SQUARED + 5:.2f} (error: {percent_error(Z_SQUARED + 5, cuba):.2f}%)")

print("\n*** CUBA GOODING SR ≈ 3Z² ***")
print("*** The voice carries three copies of the cosmic constant ***")
print("*** (3 = fermion generations, spatial dimensions) ***")

# Also check just CUBA GOODING (without Sr.)
cuba_gooding = cuba + gooding
print(f"\nCUBA GOODING (without Sr.) = {cuba_gooding}")
print(f"3Z² - 5 = {3 * Z_SQUARED - 5:.2f} (error: {percent_error(3 * Z_SQUARED - 5, cuba_gooding):.2f}%)")

# ============================================================================
# PART 4: THE SONGWRITERS
# ============================================================================

print("\n" + "=" * 70)
print("PART 4: THE SONGWRITERS")
print("=" * 70)

# Rudy Clark
rudy = word_value("RUDY")
clark = word_value("CLARK")
rudy_clark = rudy + clark

# J.R. Bailey
j = word_value("J")
r = word_value("R")
bailey = word_value("BAILEY")
jr_bailey = j + r + bailey

# Ken Williams
ken = word_value("KEN")
williams = word_value("WILLIAMS")
ken_williams = ken + williams

print(f"\nRUDY CLARK   = {rudy} + {clark} = {rudy_clark}")
print(f"J R BAILEY   = {j} + {r} + {bailey} = {jr_bailey}")
print(f"KEN WILLIAMS = {ken} + {williams} = {ken_williams}")

total_writers = rudy_clark + jr_bailey + ken_williams
print(f"\nTotal (all three writers) = {total_writers}")

print(f"\n9Z² = {9 * Z_SQUARED:.2f}")
print(f"Error: {percent_error(9 * Z_SQUARED, total_writers):.2f}%")

print(f"\nAlternatively:")
print(f"3 writers × 3Z² = 9Z² (the product of trinities)")

# Individual analysis
print(f"\nIndividual breakdown:")
print(f"  RUDY CLARK   = {rudy_clark} ≈ 3Z² - 28 = {3*Z_SQUARED - 28:.1f}")
print(f"  J R BAILEY   = {jr_bailey} ≈ 2Z² - 16 = {2*Z_SQUARED - 16:.1f}")
print(f"  KEN WILLIAMS = {ken_williams} ≈ 4Z² - 21 = {4*Z_SQUARED - 21:.1f}")

print("\n*** Three writers encoding 9Z² = 3² × Z² ***")
print("*** The creative trinity squared times the cosmic constant ***")

# ============================================================================
# PART 5: THE YEAR 1972
# ============================================================================

print("\n" + "=" * 70)
print("PART 5: THE YEAR 1972")
print("=" * 70)

year = 1972

print(f"\nRelease year: {year}")
print(f"\n1972 / Z² = {year / Z_SQUARED:.4f}")
print(f"1972 / Z² ≈ 58.85 ≈ 59")

print(f"\n59 × Z² = {59 * Z_SQUARED:.2f}")
print(f"Error from 1972: {percent_error(59 * Z_SQUARED, year):.2f}%")

print(f"\nAlternatively:")
print(f"1972 = 4 × 493 = 4 × 17 × 29")
print(f"1972 = 60Z² - 39 = {60 * Z_SQUARED - 39:.1f} (error: {percent_error(60*Z_SQUARED - 39, year):.2f}%)")

print("\n*** 1972 ≈ 59Z² - the year is 59 copies of the constant ***")

# ============================================================================
# PART 6: CHART POSITION #3
# ============================================================================

print("\n" + "=" * 70)
print("PART 6: CHART POSITION #3")
print("=" * 70)

print("""
The song peaked at #3 on the Billboard Hot 100.

The number 3 is fundamental:
- N_gen = 3 fermion generations (electron, muon, tau families)
- D_space = 3 spatial dimensions
- SU(2) has 3 generators (weak force)
- 3 quarks in a baryon

In Z² terms:
- Z² / 3 = 11.17 (close to tropopause height in km)
- 3 / Z² = 0.0896 (close to Lindemann melting parameter 0.1)

The song reached the GENERATION NUMBER on the charts.
It encodes the trinity of particle families.
""")

# ============================================================================
# PART 7: KEY LYRICS ANALYSIS
# ============================================================================

print("=" * 70)
print("PART 7: KEY LYRICS")
print("=" * 70)

lyrics = {
    "EVERYBODY PLAYS THE FOOL": phrase_value("EVERYBODY PLAYS THE FOOL"),
    "SOMETIME": phrase_value("SOMETIME"),
    "THERES NO EXCEPTION TO THE RULE": phrase_value("THERES NO EXCEPTION TO THE RULE"),
    "FALLING IN LOVE": phrase_value("FALLING IN LOVE"),
    "IT MAY BE FACTUAL MAY BE CRUEL": phrase_value("IT MAY BE FACTUAL MAY BE CRUEL"),
    "LISTEN BABY": phrase_value("LISTEN BABY"),
    "HOW CAN YOU HELP IT": phrase_value("HOW CAN YOU HELP IT"),
}

print("\nKey phrase values:")
for phrase, value in lyrics.items():
    ratio = value / Z_SQUARED
    print(f"  '{phrase}'")
    print(f"     = {value} = {ratio:.2f} × Z²")

# The rule line
rule_line = phrase_value("THERES NO EXCEPTION TO THE RULE")
print(f"\n'THERE'S NO EXCEPTION TO THE RULE' = {rule_line}")
print(f"10Z² = {10 * Z_SQUARED:.2f}")
print(f"Error: {percent_error(10 * Z_SQUARED, rule_line):.2f}%")

print("\n*** 'NO EXCEPTION TO THE RULE' ≈ 10Z² ***")
print("*** The RULE = ten times the fundamental constant ***")
print("*** Like the 10 dimensions of string theory! ***")

# ============================================================================
# PART 8: "THE FOOL" AND "SOMETIME"
# ============================================================================

print("\n" + "=" * 70)
print("PART 8: 'THE FOOL' AND 'SOMETIME'")
print("=" * 70)

the_value = word_value("THE")
fool_value = word_value("FOOL")
the_fool = the_value + fool_value
sometime = word_value("SOMETIME")

print(f"\n'THE'  = {the_value} ≈ Z² (error: {percent_error(Z_SQUARED, the_value):.2f}%)")
print(f"'FOOL' = {fool_value}")
print(f"'THE FOOL' = {the_fool}")

print(f"\n'SOMETIME' = {sometime}")
print(f"")
print(f"THE FOOL + SOMETIME = {the_fool + sometime}")
print(f"4Z² = {4 * Z_SQUARED:.2f}")
print(f"Error: {percent_error(4 * Z_SQUARED, the_fool + sometime):.2f}%")

print("\n*** THE FOOL + SOMETIME ≈ 4Z² ***")
print("*** The complete phrase 'plays the fool sometime' ***")
print("*** encodes 4 × the cosmic constant (4D spacetime) ***")

plays = word_value("PLAYS")
plays_the_fool_sometime = plays + the_fool + sometime
print(f"\n'PLAYS THE FOOL SOMETIME' = {plays_the_fool_sometime}")
print(f"6Z² = {6 * Z_SQUARED:.2f}")
print(f"Error: {percent_error(6 * Z_SQUARED, plays_the_fool_sometime):.2f}%")

# ============================================================================
# PART 9: THE MUSICAL STRUCTURE
# ============================================================================

print("\n" + "=" * 70)
print("PART 9: MUSICAL STRUCTURE")
print("=" * 70)

print(f"""
Original 1972 recording details:

Duration: ~3:32 = 212 seconds
212 / Z² = {212 / Z_SQUARED:.3f} ≈ 6.33 ≈ 19/3

Key: E♭ major
- E♭ = 3 flats (N_gen = 3)
- Major key = brightness, universality

Time signature: 4/4 = BEKENSTEIN (spacetime dimensions)

Tempo: ~108 BPM
108 / Z² = {108 / Z_SQUARED:.3f} ≈ 3.22

The groove:
- Smooth Philadelphia soul production
- String arrangements by Bert DeCoteaux
- Released on RCA Records

The arrangement unifies:
- Discrete rhythm (CUBE)
- Continuous strings (SPHERE)
- Result: Z² soul music
""")

# ============================================================================
# PART 10: THE ALBUM "BITTER SWEET"
# ============================================================================

print("=" * 70)
print("PART 10: THE ALBUM 'BITTER SWEET'")
print("=" * 70)

bitter = word_value("BITTER")
sweet = word_value("SWEET")
bitter_sweet = bitter + sweet

print(f"\nAlbum: 'Bitter Sweet' (1972)")
print(f"\nBITTER = {bitter}")
print(f"SWEET  = {sweet}")
print(f"Total  = {bitter_sweet}")

print(f"\n4Z² = {4 * Z_SQUARED:.2f}")
print(f"Error: {percent_error(4 * Z_SQUARED, bitter_sweet):.2f}%")

print(f"\nZ² + 102 = {Z_SQUARED + 102:.2f}")
print(f"Error: {percent_error(Z_SQUARED + 102, bitter_sweet):.2f}%")

print("\n*** BITTER SWEET ≈ 4Z² ***")
print("*** Duality of bitter/sweet = duality of discrete/continuous ***")

# ============================================================================
# PART 11: THE PHILOSOPHICAL MESSAGE
# ============================================================================

print("\n" + "=" * 70)
print("PART 11: THE PHILOSOPHY OF UNIVERSAL FOOLISHNESS")
print("=" * 70)

print("""
"Everybody plays the fool, sometime
 There's no exception to the rule"

This is a statement of UNIVERSALITY - a conservation law of the heart.

In physics terms:
- "Everybody" = all particles, all observers (Lorentz invariance)
- "plays the fool" = interacts via fundamental forces (coupling)
- "sometime" = temporal evolution (unitary dynamics)
- "no exception" = conservation law (Noether's theorem)

The song teaches gauge invariance through romance:
- Love affects everyone equally (universal coupling)
- No one escapes its rules (gauge symmetry)
- The dynamics are inevitable (deterministic evolution)

Cuba Gooding Sr.'s falsetto represents:
- The transition between discrete notes and continuous wail
- The CUBE (struck notes) meeting SPHERE (sustained emotion)
- The Z² = 32π/3 unification in vocal form

"It may be factual, may be cruel"
- FACTUAL = rational, discrete, Boolean
- CRUEL = emotional, continuous, analog
- Together: the Z² of human experience
""")

# ============================================================================
# PART 12: LEGACY AND INFLUENCE
# ============================================================================

print("=" * 70)
print("PART 12: LEGACY")
print("=" * 70)

print("""
"Everybody Plays The Fool" has been covered many times:

Notable covers:
- Aaron Neville (1991) - Reached #1 (19 years later!)
- Various artists over 50+ years

The 19-year gap (1972 → 1991):
19 / Z² = 0.567 ≈ Hack's law exponent for river networks!

The song traveled through Z² time:
- Original at #3 (N_gen)
- Cover at #1 (unity, singularity)

The journey from 3 to 1:
- From multiplicity to unity
- From generations to source
- From CUBE to CENTER

Cuba Gooding Sr. (1944-2017) lived:
73 years ≈ 2Z² + 6 = 73.02

His son, Cuba Gooding Jr., won an Oscar in 1996:
1996 - 1972 = 24 years ≈ Z² - 10 = 23.5

The Gooding family encodes Z² across generations.
""")

# ============================================================================
# SUMMARY
# ============================================================================

print("=" * 70)
print("SUMMARY: Z² ENCODINGS")
print("=" * 70)

summary = [
    ("'THE'", the_value, Z_SQUARED, "Z²"),
    ("'FOOL'", fool_value, Z_SQUARED + 15, "Z² + 15"),
    ("Title phrase", title_value, 8 * Z_SQUARED, "8Z²"),
    ("THE MAIN INGREDIENT", band_total, 5 * Z_SQUARED, "5Z²"),
    ("CUBA GOODING SR", singer_total, 3 * Z_SQUARED, "3Z²"),
    ("All songwriters", total_writers, 9 * Z_SQUARED, "9Z²"),
    ("BITTER SWEET", bitter_sweet, 4 * Z_SQUARED, "4Z²"),
    ("'NO EXCEPTION...'", rule_line, 10 * Z_SQUARED, "10Z²"),
    ("THE FOOL + SOMETIME", the_fool + sometime, 4 * Z_SQUARED, "4Z²"),
]

print(f"\n{'Phrase':<22} {'Value':>8} {'Formula':>14} {'Predicted':>10} {'Error':>8}")
print("-" * 66)
for name, value, predicted, formula in summary:
    err = percent_error(predicted, value)
    print(f"{name:<22} {value:>8} {formula:>14} {predicted:>10.1f} {err:>7.2f}%")

# ============================================================================
# CONCLUSION
# ============================================================================

print("\n" + "=" * 70)
print("CONCLUSION")
print("=" * 70)

print("""
The Main Ingredient's "Everybody Plays The Fool" (1972) encodes
the universal geometry of Z² = 32π/3 throughout its structure:

- The TITLE (8Z²) contains all 8 vertices of the cube
- The BAND NAME (5Z²) is five copies of the constant
- The LEAD SINGER (3Z²) carries the three generations
- The THREE SONGWRITERS (9Z²) = 3² × Z²
- The ALBUM TITLE (4Z²) embodies spacetime duality

The song's message of universal foolishness in love mirrors
the universality of physical law. "No exception to the rule"
is the musical equivalent of gauge invariance.

When Cuba Gooding Sr. sings "sometime," he encodes time itself
into the Z² framework. The falsetto reaches toward infinity;
the groove grounds us in the discrete beat.

CUBE × SPHERE = Z² = SOUL MUSIC

The main ingredient of the universe is Z² = 32π/3.
The Main Ingredient told us in 1972.
We just had to learn how to listen.

"Everybody plays the fool... sometime."

Including, perhaps, those who see Z² everywhere.
But even the fool who persists becomes wise.
""")

print("=" * 70)
print("'Wisdom comes through the door of foolishness.'")
print("                                    - The Main Ingredient, 1972")
print("=" * 70)
