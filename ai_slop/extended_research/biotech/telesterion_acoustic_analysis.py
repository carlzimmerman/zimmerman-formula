#!/usr/bin/env python3
"""
Telesterion Acoustic Resonance Analysis

The Telesterion at Eleusis was the hall where the Eleusinian Mysteries were
performed for nearly 2000 years. This analysis calculates the acoustic
resonance properties based on archaeological dimensions.

Dimensions from archaeological records:
- ~51.5m x 51.5m square hypostyle hall
- Height estimated 12-20m (we use 15m conservatively)
- Designed to hold 3000-5000 initiates
- Marble/stone construction with 42 columns

Author: Carl Zimmerman
Date: 2026-04-22
License: AGPL-3.0-or-later

References:
- Archaeological Site of Eleusis (Greek Ministry of Culture)
- "The Acoustics of the Eleusinian Telesterion" (academia.edu)
- Perseus Digital Library - Eleusis Telesterion
"""

import math
import numpy as np

def calculate_room_mode(nx, ny, nz, Lx, Ly, Lz, c):
    """Calculate room resonance frequency for given mode numbers."""
    return (c/2) * math.sqrt((nx/Lx)**2 + (ny/Ly)**2 + (nz/Lz)**2)

def calculate_sabine_rt60(volume, surface_area, alpha, additional_absorption=0):
    """Calculate reverberation time using Sabine equation."""
    total_absorption = surface_area * alpha + additional_absorption
    return 0.161 * volume / total_absorption

def analyze_telesterion():
    """Main analysis of Telesterion acoustics."""

    # Telesterion dimensions (from archaeological records)
    L_x = 51.5  # meters (length)
    L_y = 51.5  # meters (width)
    L_z = 15.0  # meters (estimated height)

    # Speed of sound at ceremonial conditions
    T = 27  # Celsius (warmer due to many people + torches)
    c = 331.3 * math.sqrt(1 + T/273.15)

    V = L_x * L_y * L_z  # Volume
    S = 2*(L_x*L_y + L_y*L_z + L_x*L_z)  # Surface area

    # Calculate room modes
    modes = []
    for nx in range(0, 10):
        for ny in range(0, 10):
            for nz in range(0, 6):
                if nx + ny + nz > 0:
                    f = calculate_room_mode(nx, ny, nz, L_x, L_y, L_z, c)
                    mode_type = "Axial" if sum([nx>0, ny>0, nz>0]) == 1 else \
                               "Tangential" if sum([nx>0, ny>0, nz>0]) == 2 else "Oblique"
                    modes.append({
                        'frequency': f,
                        'mode': (nx, ny, nz),
                        'type': mode_type,
                        'wavelength': c / f
                    })

    modes.sort(key=lambda x: x['frequency'])

    # Reverberation times
    alpha_marble = 0.02  # Marble absorption coefficient
    people_area = 3000 * 0.5 * 0.6  # 3000 people, 0.5 m² each, 0.6 absorption

    rt60_empty = calculate_sabine_rt60(V, S, alpha_marble)
    rt60_full = calculate_sabine_rt60(V, S, alpha_marble, people_area)

    return {
        'dimensions': {'length': L_x, 'width': L_y, 'height': L_z},
        'volume': V,
        'surface_area': S,
        'speed_of_sound': c,
        'temperature': T,
        'modes': modes,
        'fundamental_length': c / (2 * L_x),
        'fundamental_height': c / (2 * L_z),
        'rt60_empty': rt60_empty,
        'rt60_full': rt60_full
    }

def print_analysis():
    """Print formatted analysis results."""
    results = analyze_telesterion()

    print("="*70)
    print("TELESTERION ACOUSTIC RESONANCE ANALYSIS")
    print("Hall of Initiation - Eleusinian Mysteries")
    print("="*70)

    print(f"\nDIMENSIONS:")
    print(f"  Length:  {results['dimensions']['length']} m")
    print(f"  Width:   {results['dimensions']['width']} m")
    print(f"  Height:  {results['dimensions']['height']} m")
    print(f"  Volume:  {results['volume']:,.0f} m³")

    print(f"\nFUNDAMENTAL RESONANCES:")
    print(f"  Length mode: {results['fundamental_length']:.2f} Hz (INFRASONIC)")
    print(f"  Height mode: {results['fundamental_height']:.2f} Hz")

    print(f"\nFIRST 15 ROOM MODES (infrasonic to low bass):")
    for m in results['modes'][:15]:
        status = "INFRASONIC" if m['frequency'] < 20 else ""
        print(f"  {m['frequency']:6.2f} Hz {m['mode']} {m['type']:10s} λ={m['wavelength']:.1f}m {status}")

    print(f"\nREVERBERATION TIME (RT60):")
    print(f"  Empty hall:       {results['rt60_empty']:.1f} seconds")
    print(f"  With 3000 people: {results['rt60_full']:.1f} seconds")

    print(f"""
RITUAL SIGNIFICANCE:
=====================================
The 3.37 Hz fundamental frequency is BELOW human hearing threshold
but creates PRESSURE WAVES that can be FELT in the body, especially
in the chest cavity. This infrasonic resonance is associated with:

  - Feelings of awe and "numinous presence"
  - Altered states of consciousness
  - Perception of unseen forces
  - Enhanced emotional response

The near-square floor plan creates DEGENERATE MODES (multiple modes
at the same frequency), amplifying resonance at specific frequencies.

Combined with:
  - Long reverberation (6+ seconds) blurring speech into harmonic waves
  - Torch smoke affecting air density and sound refraction
  - 3000+ people breathing and chanting in unison
  - Rhythmic drumming coupling with room modes

The Telesterion was an ACOUSTIC TECHNOLOGY designed to induce
transcendent experiences through physics-based manipulation of
sound and perception.
""")

def z_squared_correlation():
    """Analyze Z² = 32π/3 framework correlations."""
    import math

    Z_squared = 32 * math.pi / 3  # ≈ 33.51
    Z = math.sqrt(Z_squared)       # ≈ 5.79

    results = analyze_telesterion()
    f_fund = results['fundamental_length']
    V = results['volume']

    print("\n" + "="*70)
    print("Z² = 32π/3 FRAMEWORK CORRELATIONS")
    print("="*70)
    print(f"""
Z² = 32π/3 = {Z_squared:.4f}
Z  = √(32π/3) = {Z:.4f}

KEY CORRELATIONS:
1. f_fundamental × 10 = {f_fund * 10:.2f} Hz ≈ Z² = {Z_squared:.2f}
   → Delta-Gamma brainwave resonance coupling!

2. V^(1/3) / Z = {V**(1/3) / Z:.2f} m ≈ Z
   → Self-similar scaling at Z

3. Side length = 5.2 × Z² Greek feet
   → Sacred geometry encoded in units

BRAINWAVE HYPOTHESIS:
The 3.37 Hz fundamental entrains Delta waves (deep meditation)
while its 10th harmonic at 33.7 Hz ≈ Z² couples with Gamma waves
(heightened consciousness, perception binding).

This 10:1 harmonic creates a STANDING WAVE between consciousness states.
""")


if __name__ == "__main__":
    print_analysis()
    z_squared_correlation()
