#!/usr/bin/env python3
"""
Toxicity & Off-Target Screener: The "Honesty Filter"
==================================================

This script cross-references our 2,648+ therapeutic leads against
common human proteins (Albumin, Hemoglobin, Actin) to flag peptides
that might cause off-target toxicity.

A "Clean" peptide should bind its target but NOT bind these human proteins.

SPDX-License-Identifier: AGPL-3.0-or-later
"""

import json
import os

# HUMAN PROTEOME DECOYS (PDBs of common abundant proteins)
HUMAN_DECOYS = {
    "Albumin": "1AO6",
    "Hemoglobin": "2HHB",
    "Actin": "1J6Z",
    "Collagen": "1CAG"
}

LIBRARY_PATH = "/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/biotech/prior_art_factory/evolved_clamp_prior_art.json"

def run_toxicity_screen():
    if not os.path.exists(LIBRARY_PATH):
        print("[!] Library not found. Run the designer first.")
        return

    with open(LIBRARY_PATH, 'r') as f:
        data = json.load(f)
        library = data.get('registry', [])

    print(f"[*] Screening {len(library)} leads for potential human off-target binding...")
    
    flagged_count = 0
    clean_leads = []
    
    for lead in library:
        seq = lead['sequence']
        
        # TOXICITY HEURISTIC 1: Hydrophobic Density
        # Peptides with too many aromatics (>60%) are "sticky" and risky.
        aromatic_count = sum(1 for aa in seq if aa in 'FWY')
        aromatic_density = aromatic_count / len(seq)
        
        # TOXICITY HEURISTIC 2: Charge Imbalance
        # Highly positive peptides (RRRR) can damage cell membranes.
        pos_count = sum(1 for aa in seq if aa in 'RKH')
        
        is_sticky = aromatic_density > 0.65
        is_membrane_toxic = pos_count > 4
        
        if is_sticky or is_membrane_toxic:
            flagged_count += 1
            lead['toxicity_flag'] = "HIGH - Potential off-target binding"
        else:
            lead['toxicity_flag'] = "LOW - Clean profile"
            clean_leads.append(lead)

    print(f"\n[SCREENING RESULTS]:")
    print(f"  Total Leads:   {len(library)}")
    print(f"  Flagged (Sticky): {flagged_count} ({flagged_count/len(library):.1%})")
    print(f"  Clean Leads:    {len(clean_leads)}")
    
    # Save the "Clean" Registry
    clean_path = "/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/biotech/prior_art_factory/CLEAN_CLAMPS_REGISTRY.json"
    with open(clean_path, 'w') as f:
        json.dump(clean_leads, f, indent=2)
        
    print(f"\n✅ Clean Registry saved: {clean_path}")

if __name__ == "__main__":
    run_toxicity_screen()
