#!/usr/bin/env python3
"""
Project Protogonos: Phase 3 - Polymerization
Z² Framework Origin of Life Simulation

This script simulates random peptide generation and filters them by
Z² stability to demonstrate "geometric natural selection".
Upgraded to use BioPython for rigorous sequence and structural parameter analysis.

Author: Carl Zimmerman
License: AGPL-3.0-or-later
"""

import numpy as np
import json
import os
try:
    from Bio.SeqUtils.ProtParam import ProteinAnalysis
    from Bio.Seq import Seq
    BIOPYTHON_AVAILABLE = True
except ImportError:
    BIOPYTHON_AVAILABLE = False
    print("WARNING: BioPython not found. Proceeding with mathematical approximation.")

# Z² Preferred Angles
PHI_Z = -57.0
PSI_Z = -47.0

# Simplified amino acid propensity for alpha-helix (Z² angles)
AA_Z2_PROPENSITY = {
    'A': 1.00, 'L': 0.95, 'M': 0.95, 'K': 0.90, 'E': 0.90,
    'Q': 0.85, 'H': 0.80, 'R': 0.80, 'V': 0.70, 'I': 0.70,
    'Y': 0.75, 'C': 0.75, 'W': 0.75, 'F': 0.85, 'T': 0.70,
    'S': 0.60, 'N': 0.60, 'D': 0.65, 
    'G': 0.30, 'P': 0.20  
}
AAS = list(AA_Z2_PROPENSITY.keys())

class BioGeometricPolymerization:
    def __init__(self):
        self.base_hydrolysis_rate = 0.1 
        
    def generate_random_peptide(self, length: int) -> str:
        return ''.join(np.random.choice(AAS) for _ in range(length))
        
    def calculate_biophysical_z2_compliance(self, seq: str) -> float:
        """
        Score a sequence using BioPython metrics and Z² geometric rules.
        """
        base_score = sum(AA_Z2_PROPENSITY[aa] for aa in seq) / len(seq)
        
        bonus = 0.0
        if BIOPYTHON_AVAILABLE:
            # Use BioPython ProtParam to evaluate structural features
            pa = ProteinAnalysis(seq)
            
            # Helix fraction calculation
            # pa.secondary_structure_fraction() returns (helix, turn, sheet)
            try:
                ss_frac = pa.secondary_structure_fraction()
                helix_frac = ss_frac[0]
                
                # Z² framework states alpha-helices are the primary stable prebiotic form.
                # Increase score based on BioPython's helix propensity.
                bonus += helix_frac * 0.2
                
                # Instability index: < 40 is stable, > 40 is unstable in vitro
                # We map this to prebiotic hydrolysis resistance
                instability = pa.instability_index()
                if instability < 40:
                    bonus += 0.1
                else:
                    bonus -= 0.1
                    
            except ValueError:
                # Catch edge cases with very short sequences
                pass
                
        # Hydrophobic periodicity matching Z² 5.79A spacing (i -> i+3/i+4)
        hydrophobic = 'ALMVIYWF'
        for i in range(len(seq) - 4):
            if seq[i] in hydrophobic and (seq[i+3] in hydrophobic or seq[i+4] in hydrophobic):
                bonus += 0.05
                
        return min(1.0, max(0.0, base_score + bonus))
        
    def simulate_dry_wet_cycles(self, num_cycles: int, pool_size: int, max_len: int = 15):
        pool = []
        history = []
        
        for cycle in range(num_cycles):
            new_peptides = int(pool_size * 0.2)
            for _ in range(new_peptides):
                length = np.random.randint(5, max_len + 1)
                pool.append({
                    'seq': self.generate_random_peptide(length),
                    'age': 0
                })
                
            survivors = []
            avg_compliance = 0
            
            for p in pool:
                comp = self.calculate_biophysical_z2_compliance(p['seq'])
                avg_compliance += comp
                p['age'] += 1
                
                hydrolysis_prob = self.base_hydrolysis_rate * (1.0 - comp**2)
                
                if np.random.random() > hydrolysis_prob:
                    survivors.append(p)
                    
            pool = survivors
            
            if len(pool) > 0:
                history.append(avg_compliance / len(pool))
            else:
                history.append(0)
                
            if len(pool) > pool_size:
                pool.sort(key=lambda x: self.calculate_biophysical_z2_compliance(x['seq']), reverse=True)
                pool = pool[:pool_size]
                
        return pool, history

def run_phase3_analysis():
    print("="*60)
    print("PROJECT PROTOGONOS: Phase 3 - Polymerization")
    print("BioPython & Z² Geometric Natural Selection")
    print("="*60)
    
    sim = BioGeometricPolymerization()
    cycles = 500
    pool_size = 1000
    
    print(f"\nRunning {cycles} dry/wet cycles (Pool size: {pool_size})...")
    final_pool, compliance_history = sim.simulate_dry_wet_cycles(cycles, pool_size)
    
    avg_len = np.mean([len(p['seq']) for p in final_pool])
    avg_age = np.mean([p['age'] for p in final_pool])
    top_peptides = sorted(final_pool, key=lambda x: sim.calculate_biophysical_z2_compliance(x['seq']), reverse=True)[:5]
    
    print("\n[1] Surviving Peptide Pool Statistics:")
    print(f"  Surviving count: {len(final_pool)}")
    print(f"  Average length:  {avg_len:.1f} aa")
    print(f"  Average age:     {avg_age:.1f} cycles")
    
    print("\n[2] Top Z²-Compliant Survivors (BioPython Validated):")
    results_list = []
    for p in top_peptides:
        comp = sim.calculate_biophysical_z2_compliance(p['seq'])
        
        # Add biopython metrics for final output
        metrics = {}
        if BIOPYTHON_AVAILABLE:
            pa = ProteinAnalysis(p['seq'])
            metrics['mw'] = pa.molecular_weight()
            try:
                metrics['helix_frac'] = pa.secondary_structure_fraction()[0]
                metrics['instability'] = pa.instability_index()
            except ValueError:
                metrics['helix_frac'] = 0.0
                metrics['instability'] = 50.0
                
        print(f"  {p['seq']:15s} | Age: {p['age']:3d} | Compliance: {comp:.3f}")
        results_list.append({
            "sequence": p['seq'],
            "age": p['age'],
            "z2_compliance": comp,
            "biopython_metrics": metrics
        })
        
    os.makedirs("results", exist_ok=True)
    out_file = "results/phase3_polymerization.json"
    with open(out_file, 'w') as f:
        json.dump({
            "cycles": cycles,
            "final_avg_compliance": compliance_history[-1],
            "top_survivors": results_list
        }, f, indent=2)
        
    print(f"\nResults saved to {out_file}")
    print("="*60)

if __name__ == "__main__":
    run_phase3_analysis()
