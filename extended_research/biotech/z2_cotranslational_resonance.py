#!/usr/bin/env python3
"""
Z² Cotranslational Resonance Folding

SPDX-License-Identifier: AGPL-3.0-or-later

PATHWAY 5: RIBOSOMAL TRANSLATION RESONANCE

Proteins don't fold after translation - they fold DURING translation.
The ribosome creates PAUSE SITES where nascent chain segments have
time to fold. These pauses are NOT random - they're Z² resonant.

MATHEMATICAL FOUNDATION:
========================
Ribosomal translation rate varies with codon:
- Rare codons → SLOW → time to fold
- Common codons → FAST → no time

The codon bias creates a TEMPORAL PROGRAM for folding.
In Z² theory, pause sites occur at intervals of ~Z residues.

PHYSICAL PRINCIPLE:
==================
The ribosome exit tunnel is ~80 Å long, fitting ~30 residues.
As each residue emerges, it has a folding window.

Z² predicts: Folding domains complete at residue positions
that are multiples of Z ≈ 5.79, corresponding to the
natural length scale for secondary structure.

This explains why helices are ~4-5 turns (≈Z residues per turn × 3.6 turn).

COTRANSLATIONAL PREDICTION:
===========================
By modeling the translation rate and Z² resonance, we can
predict which regions fold first and which intermediate
structures form during translation.

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import numpy as np
from scipy.signal import find_peaks
from scipy.ndimage import gaussian_filter1d
import json
from datetime import datetime

# ==============================================================================
# Z² CONSTANTS
# ==============================================================================

Z = 2 * np.sqrt(8 * np.pi / 3)  # ≈ 5.79
Z2 = Z**2  # ≈ 33.51
THETA_Z2 = np.pi / Z  # ≈ 31.09°

print("="*80)
print("Z² COTRANSLATIONAL RESONANCE FOLDING")
print("="*80)
print(f"Z = {Z:.4f} | Z² = {Z2:.4f}")
print("Predicting folding during ribosomal translation")
print("="*80)

# ==============================================================================
# CODON TABLES
# ==============================================================================

# Standard genetic code
CODON_TABLE = {
    'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L',
    'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S',
    'TAT': 'Y', 'TAC': 'Y', 'TAA': '*', 'TAG': '*',
    'TGT': 'C', 'TGC': 'C', 'TGA': '*', 'TGG': 'W',
    'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L',
    'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
    'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
    'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
    'ATT': 'I', 'ATC': 'I', 'ATA': 'I', 'ATG': 'M',
    'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
    'AAT': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
    'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
    'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V',
    'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
    'GAT': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
    'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G'
}

# E. coli codon frequencies (per 1000 codons)
# High frequency = fast translation, Low = slow (pause)
ECOLI_CODON_FREQUENCY = {
    'TTT': 22.0, 'TTC': 16.3, 'TTA': 13.7, 'TTG': 13.3,
    'TCT': 8.5, 'TCC': 8.8, 'TCA': 7.2, 'TCG': 8.8,
    'TAT': 16.2, 'TAC': 12.1, 'TAA': 2.0, 'TAG': 0.2,
    'TGT': 5.1, 'TGC': 6.3, 'TGA': 1.0, 'TGG': 15.2,
    'CTT': 10.8, 'CTC': 10.9, 'CTA': 3.8, 'CTG': 52.5,
    'CCT': 7.0, 'CCC': 5.5, 'CCA': 8.4, 'CCG': 22.7,
    'CAT': 12.8, 'CAC': 9.5, 'CAA': 15.0, 'CAG': 28.8,
    'CGT': 20.5, 'CGC': 21.5, 'CGA': 3.6, 'CGG': 5.6,
    'ATT': 30.2, 'ATC': 24.6, 'ATA': 4.5, 'ATG': 27.1,
    'ACT': 9.0, 'ACC': 22.9, 'ACA': 7.1, 'ACG': 14.3,
    'AAT': 17.7, 'AAC': 21.5, 'AAA': 33.6, 'AAG': 10.3,
    'AGT': 8.8, 'AGC': 15.9, 'AGA': 2.1, 'AGG': 1.2,
    'GTT': 18.2, 'GTC': 15.1, 'GTA': 10.9, 'GTG': 25.9,
    'GCT': 15.4, 'GCC': 25.3, 'GCA': 20.2, 'GCG': 33.1,
    'GAT': 32.1, 'GAC': 19.0, 'GAA': 39.4, 'GAG': 17.8,
    'GGT': 24.5, 'GGC': 28.7, 'GGA': 8.0, 'GGG': 11.0
}

# Normalize to relative translation rate
_max_freq = max(ECOLI_CODON_FREQUENCY.values())
TRANSLATION_RATE = {
    codon: freq / _max_freq
    for codon, freq in ECOLI_CODON_FREQUENCY.items()
}


# ==============================================================================
# Z² COTRANSLATIONAL MODEL
# ==============================================================================

class Z2CotranslationalFolder:
    """
    Model protein folding during ribosomal translation.

    Uses Z² resonance to predict folding intermediates.
    """

    def __init__(self, sequence, codons=None):
        """
        Initialize cotranslational folder.

        Args:
            sequence: Amino acid sequence
            codons: Optional DNA codons (if None, use most common)
        """
        self.sequence = sequence
        self.n = len(sequence)

        if codons is None:
            self.codons = self._infer_codons(sequence)
        else:
            self.codons = codons

        # Compute translation rate profile
        self.translation_rate = self._compute_translation_rates()

        # Exit tunnel parameters
        self.tunnel_length = 30  # residues in tunnel

        # Secondary structure propensity
        self.ss_propensity = self._compute_ss_propensity()

    def _infer_codons(self, sequence):
        """Infer most common codons for each amino acid."""
        # Reverse lookup: AA -> most common codon
        aa_to_best_codon = {}

        for aa in 'ACDEFGHIKLMNPQRSTVWY':
            best_codon = None
            best_freq = 0

            for codon, amino in CODON_TABLE.items():
                if amino == aa:
                    freq = ECOLI_CODON_FREQUENCY.get(codon, 0)
                    if freq > best_freq:
                        best_freq = freq
                        best_codon = codon

            aa_to_best_codon[aa] = best_codon

        return [aa_to_best_codon.get(aa, 'NNN') for aa in sequence]

    def _compute_translation_rates(self):
        """Compute translation rate at each position."""
        rates = np.array([
            TRANSLATION_RATE.get(codon, 0.5)
            for codon in self.codons
        ])
        return rates

    def _compute_ss_propensity(self):
        """Compute secondary structure propensity."""
        HELIX_PROP = {
            'A': 1.42, 'E': 1.51, 'L': 1.21, 'M': 1.45, 'Q': 1.11,
            'K': 1.16, 'R': 0.98, 'H': 1.00, 'V': 1.06, 'I': 1.08,
            'Y': 0.69, 'C': 0.70, 'W': 1.08, 'F': 1.13, 'T': 0.83,
            'G': 0.57, 'N': 0.67, 'P': 0.57, 'S': 0.77, 'D': 1.01
        }

        return np.array([HELIX_PROP.get(aa, 1.0) for aa in self.sequence])

    def compute_pause_sites(self, threshold=0.3):
        """
        Identify translation pause sites.

        Pauses occur at rare codons (low translation rate).
        """
        # Invert rate: low rate = high pause probability
        pause_prob = 1 - self.translation_rate

        # Smooth
        pause_smooth = gaussian_filter1d(pause_prob, sigma=2)

        # Find peaks (pause sites)
        peaks, properties = find_peaks(pause_smooth, height=threshold, distance=3)

        pause_sites = [
            {
                'position': int(p),
                'pause_strength': float(pause_smooth[p]),
                'codon': self.codons[p],
                'amino_acid': self.sequence[p]
            }
            for p in peaks
        ]

        return pause_sites

    def compute_z2_resonance(self):
        """
        Compute Z² resonance pattern.

        Folding is enhanced at positions that are Z² resonant:
        - Multiples of Z (domain boundaries)
        - θ_Z² angle completions (helix turns)
        """
        resonance = np.zeros(self.n)

        for i in range(self.n):
            # Distance from nearest Z multiple
            z_phase = (i % Z) / Z
            z_resonance = np.cos(2 * np.pi * z_phase)

            # Angular completion (helix turn at 3.6 residues ≈ 2π/θ_Z²)
            helix_phase = i * THETA_Z2
            helix_resonance = np.cos(helix_phase)

            # Combined resonance
            resonance[i] = 0.5 * (1 + z_resonance) * 0.5 * (1 + helix_resonance)

        return resonance

    def compute_folding_windows(self):
        """
        Compute time windows available for folding at each position.

        Folding window = pause time × Z² resonance × SS propensity
        """
        # Pause time (inverse of translation rate)
        pause_time = 1.0 / (self.translation_rate + 0.1)

        # Z² resonance
        resonance = self.compute_z2_resonance()

        # SS propensity (high propensity = wants to fold)
        propensity = self.ss_propensity / np.max(self.ss_propensity)

        # Combined folding window
        window = pause_time * resonance * propensity

        # Normalize
        window = window / np.max(window)

        return window

    def simulate_cotranslational_folding(self, time_step=0.01):
        """
        Simulate folding during translation.

        Returns folding trajectory showing which regions
        fold at each time point.
        """
        trajectory = []
        folded_mask = np.zeros(self.n, dtype=bool)

        # Folding windows
        windows = self.compute_folding_windows()

        # Pause sites
        pause_sites = {p['position']: p['pause_strength']
                       for p in self.compute_pause_sites()}

        # Simulate translation
        for position in range(self.n):
            # Time spent at this position
            rate = self.translation_rate[position]
            dwell_time = 1.0 / (rate + 0.1)

            # Extra pause time?
            if position in pause_sites:
                dwell_time *= (1 + pause_sites[position])

            # Which residues can fold?
            # Those emerged from tunnel and have high folding window
            emerged_start = max(0, position - self.tunnel_length)

            for i in range(emerged_start, position):
                if not folded_mask[i]:
                    # Probability of folding
                    p_fold = windows[i] * dwell_time * time_step

                    # Z² enhancement for secondary structure completion
                    if i > 3:
                        # Check if we're completing a helix turn
                        local_propensity = np.mean(self.ss_propensity[max(0,i-4):i])
                        if local_propensity > 1.1:  # Helix-forming region
                            # Z² turn completion
                            turns_complete = (i % int(2*np.pi/THETA_Z2))
                            if turns_complete < 1:
                                p_fold *= 2  # Resonance boost

                    if np.random.random() < p_fold:
                        folded_mask[i] = True

            # Record state
            trajectory.append({
                'translation_position': position,
                'folded_residues': folded_mask.copy(),
                'fraction_folded': np.mean(folded_mask[:position+1]) if position > 0 else 0
            })

        return trajectory

    def predict_folding_order(self):
        """
        Predict order in which regions fold.

        Uses Z² resonance and pause sites.
        """
        windows = self.compute_folding_windows()
        pause_sites = self.compute_pause_sites()

        # Score each position
        scores = []

        for i in range(self.n):
            score = windows[i]

            # Boost from nearby pause sites
            for pause in pause_sites:
                dist = abs(pause['position'] - i)
                if dist < self.tunnel_length:
                    score *= (1 + 0.5 * pause['pause_strength'] *
                              np.exp(-dist / 10))

            scores.append(score)

        # Sort by score (highest first)
        order = np.argsort(-np.array(scores))

        return order, np.array(scores)

    def identify_folding_domains(self, min_domain_size=10):
        """
        Identify cotranslational folding domains.

        Domains are regions that fold together during translation.
        """
        windows = self.compute_folding_windows()
        resonance = self.compute_z2_resonance()

        # Find domain boundaries (low resonance regions)
        boundaries = []

        # Smooth for boundary detection
        smooth_res = gaussian_filter1d(resonance, sigma=3)

        # Find valleys
        valleys, _ = find_peaks(-smooth_res, distance=min_domain_size)
        boundaries = list(valleys)

        # Add start and end
        boundaries = [0] + sorted(boundaries) + [self.n]

        # Define domains
        domains = []
        for i in range(len(boundaries) - 1):
            start = boundaries[i]
            end = boundaries[i+1]

            if end - start >= min_domain_size:
                domain_window = np.mean(windows[start:end])
                domain_propensity = np.mean(self.ss_propensity[start:end])

                domains.append({
                    'start': int(start),
                    'end': int(end),
                    'length': end - start,
                    'sequence': self.sequence[start:end],
                    'folding_window': float(domain_window),
                    'ss_propensity': float(domain_propensity),
                    'z2_phase': float((start % Z) / Z)
                })

        return domains


# ==============================================================================
# Z² TRANSLATION OPTIMIZER
# ==============================================================================

class Z2CodonOptimizer:
    """
    Optimize codon usage for better cotranslational folding.

    Uses Z² resonance to place pauses at optimal positions.
    """

    def __init__(self, sequence):
        self.sequence = sequence
        self.n = len(sequence)

    def optimize_codons(self):
        """
        Select codons to optimize cotranslational folding.

        Place rare codons (pauses) at Z² resonant positions.
        """
        # Compute where pauses would help
        folder = Z2CotranslationalFolder(self.sequence)
        resonance = folder.compute_z2_resonance()
        propensity = folder.ss_propensity

        optimized_codons = []

        for i, aa in enumerate(self.sequence):
            # Get available codons for this AA
            codons = [c for c, a in CODON_TABLE.items() if a == aa]

            if not codons:
                optimized_codons.append('NNN')
                continue

            # Sort by frequency
            codons_sorted = sorted(codons,
                                   key=lambda c: ECOLI_CODON_FREQUENCY.get(c, 0),
                                   reverse=True)

            # Should we pause here?
            pause_score = resonance[i] * propensity[i]

            if pause_score > 0.7:
                # Use rare codon (slow translation = pause)
                selected = codons_sorted[-1]  # Rarest
            elif pause_score > 0.4:
                # Medium frequency
                selected = codons_sorted[len(codons_sorted)//2]
            else:
                # Fast translation (common codon)
                selected = codons_sorted[0]  # Most common

            optimized_codons.append(selected)

        return optimized_codons


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    # Test on myoglobin (disease target - oxygen storage)
    # First 50 residues
    MYOGLOBIN = "MVLSGEDKSNIKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLS"

    print(f"\nAnalyzing: Myoglobin ({len(MYOGLOBIN)} residues)")
    print(f"Sequence: {MYOGLOBIN}")
    print("="*80)

    # Create cotranslational folder
    folder = Z2CotranslationalFolder(MYOGLOBIN)

    # Find pause sites
    print("\nTranslation Pause Sites:")
    pause_sites = folder.compute_pause_sites(threshold=0.25)

    for site in pause_sites[:10]:
        print(f"  Position {site['position']:3d}: {site['amino_acid']} "
              f"({site['codon']}) - strength {site['pause_strength']:.3f}")

    # Z² resonance
    print("\nZ² Resonance Pattern:")
    resonance = folder.compute_z2_resonance()

    # Find resonance peaks
    peaks = np.where(resonance > 0.8)[0]
    print(f"  High resonance positions: {peaks.tolist()}")
    print(f"  Mean spacing: {np.mean(np.diff(peaks)):.1f} residues (Z = {Z:.2f})")

    # Folding domains
    print("\nCotranslational Folding Domains:")
    domains = folder.identify_folding_domains(min_domain_size=8)

    for i, domain in enumerate(domains):
        print(f"\n  Domain {i+1}: residues {domain['start']}-{domain['end']}")
        print(f"    Length: {domain['length']}")
        print(f"    Sequence: {domain['sequence'][:20]}...")
        print(f"    Folding window: {domain['folding_window']:.3f}")
        print(f"    SS propensity: {domain['ss_propensity']:.3f}")
        print(f"    Z² phase: {domain['z2_phase']:.3f}")

    # Folding order prediction
    print("\nPredicted Folding Order (first 10):")
    order, scores = folder.predict_folding_order()

    for rank, pos in enumerate(order[:10]):
        print(f"  {rank+1}. Position {pos:3d} ({MYOGLOBIN[pos]}): score {scores[pos]:.3f}")

    # Simulate cotranslational folding
    print("\nSimulating cotranslational folding...")
    trajectory = folder.simulate_cotranslational_folding()

    # Show folding progress
    print("\nFolding Progress:")
    checkpoints = [10, 20, 30, 40, 50]
    for cp in checkpoints:
        if cp <= len(trajectory):
            state = trajectory[cp-1]
            folded = np.sum(state['folded_residues'])
            total = cp
            print(f"  After {cp:3d} residues translated: "
                  f"{folded}/{total} folded ({100*folded/total:.1f}%)")

    # Optimize codons
    print("\n" + "="*80)
    print("CODON OPTIMIZATION FOR ENHANCED FOLDING")
    print("="*80)

    optimizer = Z2CodonOptimizer(MYOGLOBIN)
    optimized_codons = optimizer.optimize_codons()

    # Compare pause profiles
    folder_orig = Z2CotranslationalFolder(MYOGLOBIN)
    folder_opt = Z2CotranslationalFolder(MYOGLOBIN, codons=optimized_codons)

    orig_windows = folder_orig.compute_folding_windows()
    opt_windows = folder_opt.compute_folding_windows()

    print(f"\nOriginal mean folding window: {np.mean(orig_windows):.3f}")
    print(f"Optimized mean folding window: {np.mean(opt_windows):.3f}")
    print(f"Improvement: {100*(np.mean(opt_windows)/np.mean(orig_windows)-1):.1f}%")

    # Save results
    results = {
        'framework': 'Z² Cotranslational Resonance',
        'timestamp': datetime.now().isoformat(),
        'Z2': Z2,
        'theta_Z2_deg': np.degrees(THETA_Z2),
        'sequence': MYOGLOBIN,
        'pause_sites': pause_sites,
        'domains': domains,
        'folding_order': order[:20].tolist(),
        'folding_scores': scores.tolist(),
        'resonance': resonance.tolist(),
        'translation_rate': folder.translation_rate.tolist(),
        'original_folding_window': float(np.mean(orig_windows)),
        'optimized_folding_window': float(np.mean(opt_windows))
    }

    with open('z2_cotranslational_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("\nSaved to z2_cotranslational_results.json")

    # Visualization
    print("\n" + "="*80)
    print("TRANSLATION PROFILE (rate and resonance)")
    print("="*80)

    for i in range(0, len(MYOGLOBIN), 5):
        chunk = MYOGLOBIN[i:i+5]
        rates = folder.translation_rate[i:i+5]
        res = resonance[i:i+5]

        rate_str = "".join("█" if r > 0.7 else "▓" if r > 0.4 else "░"
                           for r in rates)
        res_str = "".join("●" if r > 0.7 else "○" if r > 0.4 else "·"
                          for r in res)

        print(f"  {i:3d}-{i+4:3d}: {chunk} | Rate: {rate_str} | Z² Res: {res_str}")

    return results


if __name__ == '__main__':
    main()
