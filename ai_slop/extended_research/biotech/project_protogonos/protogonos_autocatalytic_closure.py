#!/usr/bin/env python3
"""
Project Protogonos: Phase 4 - Autocatalytic Closure
Z² Framework Origin of Life Simulation

This script models a network of Z²-compliant peptides to discover Reflexively
Autocatalytic and Food-generated (RAF) sets—minimal networks where the elements
mutually catalyze each other's formation.

Author: Carl Zimmerman
License: AGPL-3.0-or-later
"""

import numpy as np
import networkx as nx
import json
import os
import itertools

# Z² Aromatic Stacking Distance
Z_STACKING = 6.015  # Å

class AutocatalyticNetwork:
    def __init__(self, num_peptides: int = 50):
        self.num_peptides = num_peptides
        # Generate random "food" molecules (short peptides that feed the system)
        self.food_set = [f"F{i}" for i in range(10)]
        
        # Generate peptide species (products of reactions)
        self.species = [f"P{i}" for i in range(num_peptides)]
        
        # We assign each peptide a "geometric signature" related to Z² folding
        # 0.0 to 1.0 (1.0 = perfect Z² structural match)
        self.signatures = {p: np.random.random() for p in self.species + self.food_set}
        
        self.reactions = []
        self.G = nx.DiGraph()

    def catalysis_probability(self, catalyst: str, reactant1: str, reactant2: str) -> float:
        """
        Determine probability that `catalyst` catalyzes R1 + R2 -> Product.
        In Z² theory, this is driven by structural complementarity (aromatic stacking).
        """
        cat_sig = self.signatures[catalyst]
        r1_sig = self.signatures[reactant1]
        r2_sig = self.signatures[reactant2]
        
        # Synergy: if catalyst signature complements the reactants
        # Perfect complement would be sig(cat) ~ 1.0 - mean(sig(R1), sig(R2))
        avg_r = (r1_sig + r2_sig) / 2
        complementarity = 1.0 - abs(cat_sig - (1.0 - avg_r))
        
        # Base probability scaled by complementarity
        base_prob = 0.05
        return base_prob * (complementarity ** 2)

    def generate_reaction_network(self):
        """Generate possible reactions based on Z² catalysis rules."""
        # Simple model: R1 + R2 -> P
        # Where R1, R2 can be from food or existing species
        all_reactants = self.food_set + self.species
        
        # We'll randomly assign a product to each pair, then check if any species catalyzes it
        for r1, r2 in itertools.combinations(all_reactants, 2):
            # Only generate a subset of possible reactions to keep it sparse
            if np.random.random() > 0.1:
                continue
                
            product = np.random.choice(self.species)
            
            # Find catalysts
            catalysts = []
            for potential_cat in self.species:
                if np.random.random() < self.catalysis_probability(potential_cat, r1, r2):
                    catalysts.append(potential_cat)
                    
            if catalysts:
                self.reactions.append({
                    'reactants': [r1, r2],
                    'product': product,
                    'catalysts': catalysts
                })
                
                # Add to graph
                for cat in catalysts:
                    self.G.add_edge(cat, product, type='catalyzes')
                self.G.add_edge(r1, product, type='reacts_to')
                self.G.add_edge(r2, product, type='reacts_to')

    def find_autocatalytic_sets(self):
        """
        Identify RAF sets. A set R of reactions is a RAF if:
        1. Reflexively Autocatalytic: Every reaction in R is catalyzed by a product of R (or food)
        2. Food-generated: Every reactant in R can be produced from food using only reactions in R
        
        Simplified approximation: Find cycles in the catalysis graph.
        """
        # A true RAF algorithm is complex (e.g., Hordijk-Steel algorithm).
        # We approximate by finding strongly connected components in the catalysis graph.
        
        # Subgraph of only catalysis edges
        cat_edges = [(u, v) for u, v, d in self.G.edges(data=True) if d['type'] == 'catalyzes']
        cat_graph = nx.DiGraph()
        cat_graph.add_edges_from(cat_edges)
        
        try:
            sccs = list(nx.strongly_connected_components(cat_graph))
            # Filter out single nodes without self-loops
            raf_candidates = [scc for scc in sccs if len(scc) > 1 or (list(scc)[0], list(scc)[0]) in cat_graph.edges()]
            return raf_candidates
        except Exception:
            return []

def run_phase4_analysis():
    print("="*60)
    print("PROJECT PROTOGONOS: Phase 4 - Autocatalytic Closure")
    print("Z² Geometric Reflexively Autocatalytic Sets (RAF)")
    print("="*60)
    
    network = AutocatalyticNetwork(num_peptides=100)
    
    print("\nGenerating reaction network driven by Z² aromatic stacking complementarity...")
    network.generate_reaction_network()
    
    print(f"  Total generated reactions: {len(network.reactions)}")
    
    print("\nSearching for Autocatalytic Sets (RAF)...")
    raf_sets = network.find_autocatalytic_sets()
    
    print(f"  Found {len(raf_sets)} autocatalytic sets.")
    
    results_list = []
    for i, raf in enumerate(raf_sets):
        print(f"\n  RAF Set {i+1} (Size {len(raf)}):")
        print(f"    Members: {', '.join(list(raf)[:10])}{'...' if len(raf) > 10 else ''}")
        results_list.append(list(raf))
        
    # Save results
    os.makedirs("results", exist_ok=True)
    out_file = "results/phase4_autocatalytic.json"
    with open(out_file, 'w') as f:
        json.dump({
            "num_peptides": network.num_peptides,
            "total_reactions": len(network.reactions),
            "num_raf_sets": len(raf_sets),
            "raf_sets": results_list
        }, f, indent=2)
        
    print(f"\nResults saved to {out_file}")
    print("="*60)

if __name__ == "__main__":
    run_phase4_analysis()
