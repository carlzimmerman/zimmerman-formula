#!/usr/bin/env python3
"""
ANR-1 Phase Map Generator
Computes the patient-specific phase correction for a 3D-printed metamaterial lens.
Based on the Acoustic Holography specification in PART IV.
"""

import numpy as np
import os

def generate_anr1_map(output_path="anr1_phase_map.npy"):
    print("[*] Initiating ANR-1 Phase Map Generation...")
    
    # 1. Transducer Config
    frequency = 1.5e6  # 1.5 MHz
    diameter = 0.10    # 10 cm
    n_elements = 200   # 200x200 grid
    
    # 2. Target Configuration (Hippocampus relative to transducer)
    # Target at (0, 0, 8cm depth)
    target_pos = np.array([0.0, 0.0, 0.08])
    
    # 3. Compute Phase Map
    # x, y grid on the transducer surface
    x = np.linspace(-diameter/2, diameter/2, n_elements)
    y = np.linspace(-diameter/2, diameter/2, n_elements)
    X, Y = np.meshgrid(x, y)
    
    # Distance from each point (X, Y, 0) to target (0, 0, 0.08)
    # L = sqrt(X^2 + Y^2 + Z^2)
    distances = np.sqrt(X**2 + Y**2 + target_pos[2]**2)
    
    # Wavelength in water
    c_water = 1540.0
    wavelength = c_water / frequency
    
    # Phase delay required to ensure constructive interference at target:
    # phi = 2*pi * (d / lambda) mod 2*pi
    # We apply the NEGATIVE of this phase as a correction on the lens.
    phase_map = - (2 * np.pi * distances / wavelength) % (2 * np.pi)
    
    # 4. Save results
    np.save(output_path, phase_map)
    print(f"[+] Successfully generated ANR-1 phase map: {output_path}")
    print(f"    - Grid size: {n_elements}x{n_elements}")
    print(f"    - Frequency: {frequency/1e6:.1f} MHz")
    print(f"    - Aperture: {diameter*100:.1f} cm")
    
    # 5. Summary metrics
    mean_phase = np.mean(phase_map)
    max_phase = np.max(phase_map)
    print(f"    - Mean phase correction: {mean_phase:.3f} rad")
    print(f"    - Phase range: [0, {max_phase:.3f}] rad")

if __name__ == "__main__":
    generate_anr1_map()
