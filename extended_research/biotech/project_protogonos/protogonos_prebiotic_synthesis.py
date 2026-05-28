#!/usr/bin/env python3
"""
Project Protogonos: Phase 1 - Prebiotic Chemistry
Z² Framework Origin of Life Simulation

This script computes the thermodynamic landscape for amino acid synthesis
under prebiotic conditions, specifically analyzing how Z² geometric mineral
surfaces (lattice spacing ~5.79 Å) act as catalysts by lowering the
activation energy barrier.

Author: Carl Zimmerman
License: AGPL-3.0-or-later
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Dict, List, Tuple
import json
import os

# Z² Fundamental Constants
Z_SQUARED = 32 * np.pi / 3  # ~33.51
Z_CONSTANT = 2 * np.sqrt(8 * np.pi / 3)  # ~5.7888 Å
Z_BIOLOGICAL_CONSTANT = 6.015152508891966  # Å (Aromatic stacking)

@dataclass
class MineralSurface:
    name: str
    lattice_spacing_angstroms: float
    surface_charge: float # e
    porosity: float # 0-1

# Candidate prebiotic minerals
MINERALS = [
    MineralSurface("Montmorillonite Clay", 5.80, -0.1, 0.4), # Highly Z² compliant
    MineralSurface("Iron Pyrite (FeS2)", 5.41, 0.2, 0.1),
    MineralSurface("Quartz (SiO2)", 4.91, -0.05, 0.05),
    MineralSurface("Calcite (CaCO3)", 4.99, 0.1, 0.05),
    MineralSurface("Ideal Z2 Mineral", Z_CONSTANT, 0.0, 0.5)
]

class PrebioticThermodynamics:
    def __init__(self):
        # Universal gas constant (J/(mol*K))
        self.R = 8.314
        
        # Standard free energies of formation (ΔG°_f) in kJ/mol (simplified models)
        # Aqueous phase, 298.15 K, 1 bar
        self.G_f_0 = {
            'CH4': -34.33,
            'NH3': -26.5,
            'H2O': -237.14,
            'CO2': -386.0,
            'H2': 0.0,
            'HCN': 119.7,
            'Glycine': -373.4,
            'Alanine': -371.3
        }

    def calc_delta_g_reaction(self, temp_K: float, pressure_atm: float) -> float:
        """
        Calculate free energy for Strecker synthesis of Glycine:
        CH4 + NH3 + CO2 -> Glycine + H2O + H2
        (Highly simplified prebiotic pathway)
        """
        # ΔG = ΔG° + RT ln(Q) + ΔV(P - P°)
        # For simplicity, we approximate ΔG(T) using standard entropy/enthalpy approximations.
        
        # Standard reaction ΔG° at 298K
        delta_g_0 = (self.G_f_0['Glycine'] + self.G_f_0['H2O'] + self.G_f_0['H2']) - \
                    (self.G_f_0['CH4'] + self.G_f_0['NH3'] + self.G_f_0['CO2'])
        
        # Temperature correction (approximate entropy term)
        # Prebiotic synthesis is generally entropically unfavorable (gas -> solid/aqueous)
        delta_s_approx = -0.2  # kJ/(mol*K)
        
        delta_g_T = delta_g_0 - (temp_K - 298.15) * delta_s_approx
        
        # Pressure correction (approximate)
        delta_g_P = delta_g_T + (pressure_atm - 1) * 0.01 
        
        return delta_g_P

    def geometric_catalysis_factor(self, mineral: MineralSurface) -> float:
        """
        Calculate catalytic energy reduction based on Z² geometry match.
        Minerals with lattice spacing near Z (5.79 A) provide perfect
        templates for prebiotic precursor assembly.
        """
        # Resonance well depth (kJ/mol) based on geometric alignment
        max_catalysis_energy = 45.0 
        
        # Gaussian dropoff based on distance from Z_CONSTANT
        deviation = abs(mineral.lattice_spacing_angstroms - Z_CONSTANT)
        catalysis = max_catalysis_energy * np.exp(-(deviation**2) / (0.1**2))
        
        return catalysis

    def simulate_environment(self, temp_range: Tuple[float, float], pressure_range: Tuple[float, float], mineral: MineralSurface):
        """
        Map the free energy landscape over T and P for a given mineral surface.
        """
        temps = np.linspace(temp_range[0], temp_range[1], 50)
        pressures = np.linspace(pressure_range[0], pressure_range[1], 50)
        
        T_grid, P_grid = np.meshgrid(temps, pressures)
        Z_grid = np.zeros_like(T_grid)
        
        catalytic_bonus = self.geometric_catalysis_factor(mineral)
        
        for i in range(len(pressures)):
            for j in range(len(temps)):
                # Base thermodynamics
                dg_base = self.calc_delta_g_reaction(temps[j], pressures[i])
                
                # The mineral surface acts as a geometric catalyst, lowering the activation 
                # barrier, and through confinement, shifting the equilibrium (effectively lowering ΔG)
                dg_catalyzed = dg_base - catalytic_bonus
                
                Z_grid[i, j] = dg_catalyzed
                
        return T_grid, P_grid, Z_grid

def run_phase1_analysis():
    print("="*60)
    print("PROJECT PROTOGONOS: Phase 1 - Prebiotic Chemistry")
    print("Z² Geometric Mineral Catalysis Analysis")
    print("="*60)
    
    thermo = PrebioticThermodynamics()
    
    # Analyze minerals
    print("\n[1] Mineral Surface Z² Geometric Affinity:")
    results_list = []
    for m in MINERALS:
        catalysis = thermo.geometric_catalysis_factor(m)
        print(f"  {m.name:25s} | Lattice: {m.lattice_spacing_angstroms:.2f} Å | Z-Catalysis: {catalysis:.1f} kJ/mol")
        results_list.append({
            "mineral": m.name,
            "lattice_spacing": m.lattice_spacing_angstroms,
            "catalysis_kj_mol": catalysis
        })
        
    # Find thermodynamic sweet spot for Montmorillonite (highest real Z-affinity)
    best_real_mineral = MINERALS[0] 
    
    # 0 - 200 C, 1 - 250 atm (hydrothermal vent conditions)
    T, P, G = thermo.simulate_environment((273.15, 473.15), (1.0, 250.0), best_real_mineral)
    
    # Find minimum ΔG (most favorable)
    min_idx = np.unravel_index(np.argmin(G, axis=None), G.shape)
    optimal_T_C = T[min_idx] - 273.15
    optimal_P = P[min_idx]
    optimal_G = G[min_idx]
    
    print("\n[2] Thermodynamic 'Sweet Spot' for Amino Acid Synthesis:")
    print(f"  Catalyst:     {best_real_mineral.name} (Lattice ~Z)")
    print(f"  Temperature:  {optimal_T_C:.1f} °C")
    print(f"  Pressure:     {optimal_P:.1f} atm")
    print(f"  ΔG (catalyzed): {optimal_G:.1f} kJ/mol (spontaneous if < 0)")
    
    # Save results
    os.makedirs("results", exist_ok=True)
    out_file = "results/phase1_prebiotic_thermo.json"
    with open(out_file, 'w') as f:
        json.dump({
            "minerals": results_list,
            "optimal_conditions": {
                "temperature_C": optimal_T_C,
                "pressure_atm": optimal_P,
                "delta_g_kj_mol": optimal_G,
                "catalyst": best_real_mineral.name
            }
        }, f, indent=2)
        
    print(f"\nResults saved to {out_file}")
    print("="*60)

if __name__ == "__main__":
    run_phase1_analysis()
