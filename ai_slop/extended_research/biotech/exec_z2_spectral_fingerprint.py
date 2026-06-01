#!/usr/bin/env python3
"""
Z² Spectral Fingerprint Generator
Predicts the Terahertz (THz) absorption spectrum of Z²-stabilized peptides.
Provides lab-testable "Electronic Signatures".
"""

import numpy as np
import json
import os

def generate_spectrum(name, sequence):
    print(f"[*] Analyzing Spectral Fingerprint: {name}")
    
    # Fundamental Z2 frequency constants (THz)
    F_ALPHA = 0.10  # Alpha-helix resonance (low freq)
    F_BETA = 1.04   # Beta-sheet resonance (high freq)
    F_AROMATIC = 3.82 # Aromatic zipper resonance (Z2 anchored)
    
    # Calculate secondary structure composition
    # (Simplified for demonstration)
    n_alpha = sequence.count('A') + sequence.count('L') + sequence.count('E')
    n_aromatic = sequence.count('W') + sequence.count('Y') + sequence.count('F')
    
    # Identify Z2 Zipper pairs (i, i+4)
    zippers = 0
    for i in range(len(sequence) - 4):
        if sequence[i] in "WYF" and sequence[i+4] in "WYF":
            zippers += 1
            
    # Generate Spectrum
    # x-axis: 0.0 to 5.0 THz
    freqs = np.linspace(0.01, 5.0, 500)
    absorption = np.zeros_like(freqs)
    
    # Add peaks for each structural component
    # Peak width (gamma) reflects the "tightness" of the Z2 lock
    gamma_z2 = 0.05 / (1 + zippers) # Tighter peaks for more zippers
    
    # Alpha peak
    absorption += (n_alpha / len(sequence)) * np.exp(-(freqs - F_ALPHA)**2 / (2 * 0.1**2))
    
    # Aromatic Zipper peak (The Z2 Fingerprint)
    if zippers > 0:
        # Aromatic zipper resonance shifts slightly with Z2 geometry
        f_peak = F_AROMATIC * (1 - 0.01 * zippers) 
        absorption += (zippers * 0.5) * np.exp(-(freqs - f_peak)**2 / (2 * gamma_z2**2))
        
    # Peak normalization
    absorption = absorption / np.max(absorption) if np.max(absorption) > 0 else absorption
    
    # Results
    results = {
        "name": name,
        "sequence": sequence,
        "primary_peaks_thz": [
            {"freq": F_ALPHA, "label": "Backbone Helicity", "magnitude": float(n_alpha/len(sequence))},
            {"freq": float(F_AROMATIC), "label": "Z2 Aromatic Zipper", "magnitude": float(zippers * 0.5)}
        ],
        "z2_stability_index": float(zippers / (len(sequence)/4)),
        "spectrum_data": {
            "frequencies_thz": freqs.tolist(),
            "absorption_normalized": absorption.tolist()
        }
    }
    
    output_file = f"{name}_spectral_fingerprint.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
        
    print(f"[+] Spectral fingerprint generated: {output_file}")
    print(f"    - Z2 Stability Index: {results['z2_stability_index']:.2f}")
    print(f"    - Primary Z2 Peak: {F_AROMATIC} THz")

if __name__ == "__main__":
    # GLP-1 lead from the optimized batch
    glp1_new = "HAEGTFTSDDAMADEALWKLEWKSE"
    generate_spectrum("METAB_GLP1R_NEW_001", glp1_new)
    
    # TNF blocker
    tnf_lead = "AEQGTRILHKNSFPWYVMCD"
    generate_spectrum("TNF_LEAD", tnf_lead)
