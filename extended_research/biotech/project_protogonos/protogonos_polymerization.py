#!/usr/bin/env python3
"""
Project Protogonos: Phase 3 - Polymerization
Z² Framework Origin of Life Simulation

This script simulates random peptide generation and filters them by
Z² stability to demonstrate "geometric natural selection" without biology.

Author: Carl Zimmerman
License: AGPL-3.0-or-later
"""

import numpy as np
import json
import os

# Z² Preferred Angles
PHI_Z = -57.0
PSI_Z = -47.0

# Simplified amino acid propensity for alpha-helix (Z² angles)
# 1.0 = highly compliant, 0.0 = structure breaker
AA_Z2_PROPENSITY = {
    'A': 1.00, 'L': 0.95, 'M': 0.95, 'K': 0.90, 'E': 0.90,
    'Q': 0.85, 'H': 0.80, 'R': 0.80, 'V': 0.70, 'I': 0.70,
    'Y': 0.75, 'C': 0.75, 'W': 0.75, 'F': 0.85, 'T': 0.70,
    'S': 0.60, 'N': 0.60, 'D': 0.65, 
    'G': 0.30, # Too flexible
    'P': 0.20  # Breaks helix
}
AAS = list(AA_Z2_PROPENSITY.keys())

class GeometricPolymerization:
    def __init__(self):
        self.base_hydrolysis_rate = 0.1 # per cycle
        
    def generate_random_peptide(self, length: int) -> str:
        return ''.join(np.random.choice(AAS) for _ in range(length))
        
    def calculate_z2_compliance(self, seq: str) -> float:
        """Score a sequence based on how well it adopts Z² geometry."""
        score = sum(AA_Z2_PROPENSITY[aa] for aa in seq) / len(seq)
        
        # Periodicity bonus (i -> i+3/i+4 hydrophobic moments match Z² 5.79A spacing)
        # Simplified: Check if hydrophobic residues are spaced appropriately
        hydrophobic = 'ALMVIYWF'
        bonus = 0
        for i in range(len(seq) - 4):
            if seq[i] in hydrophobic and (seq[i+3] in hydrophobic or seq[i+4] in hydrophobic):
                bonus += 0.05
                
        return min(1.0, score + bonus)
        
    def simulate_dry_wet_cycles(self, num_cycles: int, pool_size: int, max_len: int = 15):
        """Simulate prebiotic dry/wet cycling where peptides form and hydrolyze."""
        # Initial pool is empty
        pool = []
        
        history = []
        
        for cycle in range(num_cycles):
            # 1. Dry phase: Dehydration synthesis (random polymerization)
            # Add new random peptides
            new_peptides = int(pool_size * 0.2)
            for _ in range(new_peptides):
                length = np.random.randint(5, max_len + 1)
                pool.append({
                    'seq': self.generate_random_peptide(length),
                    'age': 0
                })
                
            # 2. Wet phase: Hydrolysis
            # Z² compliance acts as a shield against hydrolysis
            survivors = []
            avg_compliance = 0
            
            for p in pool:
                comp = self.calculate_z2_compliance(p['seq'])
                avg_compliance += comp
                p['age'] += 1
                
                # Hydrolysis probability is inversely proportional to Z² compliance
                # Highly compliant structures (helices) hide their backbone H-bonds
                hydrolysis_prob = self.base_hydrolysis_rate * (1.0 - comp**2)
                
                if np.random.random() > hydrolysis_prob:
                    survivors.append(p)
                    
            pool = survivors
            
            if len(pool) > 0:
                history.append(avg_compliance / len(pool))
            else:
                history.append(0)
                
            # Cap pool size
            if len(pool) > pool_size:
                # Keep oldest/most stable
                pool.sort(key=lambda x: self.calculate_z2_compliance(x['seq']), reverse=True)
                pool = pool[:pool_size]
                
        return pool, history

def run_phase3_analysis():
    print("="*60)
    print("PROJECT PROTOGONOS: Phase 3 - Polymerization")
    print("Z² Geometric Natural Selection")
    print("="*60)
    
    sim = GeometricPolymerization()
    cycles = 500
    pool_size = 1000
    
    print(f"\nRunning {cycles} dry/wet cycles (Pool size: {pool_size})...")
    final_pool, compliance_history = sim.simulate_dry_wet_cycles(cycles, pool_size)
    
    # Analysis
    avg_len = np.mean([len(p['seq']) for p in final_pool])
    avg_age = np.mean([p['age'] for p in final_pool])
    top_peptides = sorted(final_pool, key=lambda x: sim.calculate_z2_compliance(x['seq']), reverse=True)[:5]
    
    print("\n[1] Surviving Peptide Pool Statistics:")
    print(f"  Surviving count: {len(final_pool)}")
    print(f"  Average length:  {avg_len:.1f} aa")
    print(f"  Average age:     {avg_age:.1f} cycles")
    
    print("\n[2] Top Z²-Compliant Survivors:")
    results_list = []
    for p in top_peptides:
        comp = sim.calculate_z2_compliance(p['seq'])
        print(f"  {p['seq']:15s} | Age: {p['age']:3d} | Compliance: {comp:.3f}")
        results_list.append({
            "sequence": p['seq'],
            "age": p['age'],
            "z2_compliance": comp
        })
        
    # Save results
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
