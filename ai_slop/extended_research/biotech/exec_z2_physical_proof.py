#!/usr/bin/env python3
"""
Z² Physical Proof: Thermodynamic Stability Analysis
Executes folding and relaxation for high-value therapeutic candidates.
"""

import sys
import os
import json
import numpy as np
from pathlib import Path

# Add biotech directory to path
biotech_dir = Path("/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/biotech")
sys.path.append(str(biotech_dir))

try:
    from z2_protein_folder import Z2ProteinFolder
    from empirical_openmm_relaxation import relax_structure
except ImportError as e:
    print(f"Error importing Z2 modules: {e}")
    sys.exit(1)

def run_proof(name: str, sequence: str):
    print(f"\n[*] Starting Physical Proof for: {name}")
    print(f"[*] Sequence: {sequence}")
    
    # Step 1: Fold using Z2 geometric constraints
    folder = Z2ProteinFolder()
    folding_results = folder.fold(sequence, name=name)
    pdb_path = folding_results["pdb_file"]
    
    # Step 2: Thermodynamic relaxation
    print(f"\n[*] Initiating Thermodynamic Relaxation at 310K...")
    output_dir = biotech_dir / "physical_proof_results"
    
    # Use relax_structure from empirical_openmm_relaxation
    # This will automatically use OpenMM if available, otherwise fallback
    try:
        relaxation_results = relax_structure(
            pdb_path,
            name=f"{name}_relaxed",
            output_dir=str(output_dir),
            use_explicit_water=False,
            min_steps=5000,
            equil_steps=2000
        )
        
        print(f"\n[+] Physical Proof Complete for {name}")
        print(f"    - Initial PDB: {pdb_path}")
        print(f"    - Relaxed PDB: {relaxation_results['output_pdb']}")
        print(f"    - Final Energy: {relaxation_results.get('final_energy_kj', 'N/A')} kJ/mol")
        
        # Save combined results
        proof_file = output_dir / f"{name}_proof.json"
        with open(proof_file, 'w') as f:
            json.dump({
                "folding": folding_results,
                "relaxation": relaxation_results
            }, f, indent=2, default=str)
            
    except Exception as e:
        print(f"[!] Relaxation failed: {e}")

if __name__ == "__main__":
    # Target: METAB_GLP1R_002 (Ozempic/GLP-1 analog)
    glp1r_seq = "HAEGTFTSDWESWKWMKSMLAAALKMRKAE"
    run_proof("METAB_GLP1R_002", glp1r_seq)
    
    # Target: Abeta42 blocker
    abeta_seq = "DAEFRHDSGYEVHHQKLVFFAEDVGSNKGAIIGLMVGGVVIA"
    run_proof("Abeta42", abeta_seq)
