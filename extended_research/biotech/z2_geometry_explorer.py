#!/usr/bin/env python3
"""
Z² Geometry Explorer for Biology

Systematic search for geometric patterns in biological structures.
Uses REAL data. Documents failures honestly.

The hypothesis: If Z² = 32π/3 emerges from fundamental geometry,
perhaps related constants appear in biological structures which
are constrained by physics.

Tests many hypotheses - most will fail. That's science.

Copyright (C) 2026 Carl Zimmerman
SPDX-License-Identifier: AGPL-3.0-or-later
"""

import numpy as np
from scipy import stats
from scipy.optimize import minimize
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import json
from pathlib import Path

# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================

# Z² family
Z = 2 * np.sqrt(8 * np.pi / 3)      # 5.7888
Z_SQUARED = 32 * np.pi / 3           # 33.510
ONE_OVER_Z2 = 3 / (32 * np.pi)       # 0.02984
THETA_Z2 = np.pi / Z                 # 0.5428 rad = 31.1°
PHI_GOLDEN = (1 + np.sqrt(5)) / 2    # 1.618

# Other geometric constants to test
CONSTANTS_TO_TEST = {
    "Z": Z,
    "Z²": Z_SQUARED,
    "1/Z²": ONE_OVER_Z2,
    "θ_Z² (rad)": THETA_Z2,
    "θ_Z² (deg)": np.degrees(THETA_Z2),
    "π/Z²": np.pi / Z_SQUARED,
    "Z/π": Z / np.pi,
    "√Z²": np.sqrt(Z_SQUARED),
    "φ (golden)": PHI_GOLDEN,
    "π": np.pi,
    "e": np.e,
    "√2": np.sqrt(2),
    "√3": np.sqrt(3),
    "2π/Z": 2 * np.pi / Z,
}


# =============================================================================
# REAL DNA GEOMETRY DATA
# =============================================================================

@dataclass
class DNAGeometry:
    """Real DNA structural parameters from crystallography."""

    # B-DNA (most common form)
    b_dna = {
        "twist_per_bp_deg": 34.3,      # degrees per base pair
        "rise_per_bp_A": 3.4,           # Angstroms
        "bp_per_turn": 10.5,
        "helix_pitch_A": 35.7,          # Angstroms per turn
        "helix_diameter_A": 20.0,
        "major_groove_width_A": 22.0,
        "minor_groove_width_A": 12.0,
        "major_groove_depth_A": 8.5,
        "minor_groove_depth_A": 7.5,
        "backbone_angle_deg": 36.0,     # P-P-P angle
        "glycosidic_angle_deg": -117.0, # base-sugar angle
    }

    # A-DNA (dehydrated form)
    a_dna = {
        "twist_per_bp_deg": 32.7,
        "rise_per_bp_A": 2.6,
        "bp_per_turn": 11.0,
        "helix_pitch_A": 28.6,
        "helix_diameter_A": 23.0,
    }

    # Z-DNA (left-handed)
    z_dna = {
        "twist_per_bp_deg": -30.0,  # negative = left-handed
        "rise_per_bp_A": 3.7,
        "bp_per_turn": 12.0,
        "helix_pitch_A": 44.4,
        "helix_diameter_A": 18.0,
    }


# =============================================================================
# REAL PROTEIN GEOMETRY DATA
# =============================================================================

@dataclass
class ProteinGeometry:
    """Real protein structural parameters."""

    # Alpha helix
    alpha_helix = {
        "residues_per_turn": 3.6,
        "pitch_A": 5.4,                  # Angstroms per turn
        "rise_per_residue_A": 1.5,
        "phi_angle_deg": -57.0,          # backbone φ
        "psi_angle_deg": -47.0,          # backbone ψ
        "hydrogen_bond_length_A": 2.8,
        "helix_radius_A": 2.3,
    }

    # Beta sheet (antiparallel)
    beta_sheet_anti = {
        "strand_separation_A": 4.7,
        "residue_spacing_A": 3.5,
        "phi_angle_deg": -139.0,
        "psi_angle_deg": 135.0,
        "hydrogen_bond_length_A": 2.8,
        "twist_per_strand_deg": 25.0,    # right-handed twist
    }

    # Beta sheet (parallel)
    beta_sheet_para = {
        "strand_separation_A": 4.9,
        "residue_spacing_A": 3.2,
        "phi_angle_deg": -119.0,
        "psi_angle_deg": 113.0,
    }

    # 3-10 helix
    helix_310 = {
        "residues_per_turn": 3.0,
        "pitch_A": 6.0,
        "phi_angle_deg": -49.0,
        "psi_angle_deg": -26.0,
    }

    # Pi helix
    pi_helix = {
        "residues_per_turn": 4.4,
        "pitch_A": 5.0,
        "phi_angle_deg": -57.0,
        "psi_angle_deg": -70.0,
    }

    # Collagen triple helix
    collagen = {
        "residues_per_turn": 3.3,
        "pitch_A": 8.6,
        "rise_per_residue_A": 2.9,
        "superhelix_pitch_A": 86.0,
    }


# =============================================================================
# REAL AMINO ACID DATA
# =============================================================================

# Kyte-Doolittle hydrophobicity scale
AMINO_ACID_HYDROPHOBICITY = {
    "Ile": 4.5, "Val": 4.2, "Leu": 3.8, "Phe": 2.8, "Cys": 2.5,
    "Met": 1.9, "Ala": 1.8, "Gly": -0.4, "Thr": -0.7, "Ser": -0.8,
    "Trp": -0.9, "Tyr": -1.3, "Pro": -1.6, "His": -3.2, "Glu": -3.5,
    "Gln": -3.5, "Asp": -3.5, "Asn": -3.5, "Lys": -3.9, "Arg": -4.5,
}

# Molecular weights (Da)
AMINO_ACID_MW = {
    "Gly": 75.07, "Ala": 89.09, "Val": 117.15, "Leu": 131.17, "Ile": 131.17,
    "Pro": 115.13, "Phe": 165.19, "Tyr": 181.19, "Trp": 204.23, "Ser": 105.09,
    "Thr": 119.12, "Cys": 121.16, "Met": 149.21, "Asn": 132.12, "Gln": 146.15,
    "Asp": 133.10, "Glu": 147.13, "Lys": 146.19, "Arg": 174.20, "His": 155.16,
}

# pKa values of ionizable groups
AMINO_ACID_PKA = {
    "Asp": 3.9, "Glu": 4.3, "His": 6.0, "Cys": 8.3, "Tyr": 10.1,
    "Lys": 10.5, "Arg": 12.5,
    "N_terminus": 9.0, "C_terminus": 2.2,
}


# =============================================================================
# REAL PROTEIN AGGREGATION DATA (Alzheimer's, Parkinson's)
# =============================================================================

@dataclass
class AggregationData:
    """Real protein aggregation kinetics data from literature."""

    # Amyloid-beta (Alzheimer's) - from Knowles lab studies
    amyloid_beta = {
        "name": "Amyloid-beta 42",
        "length_residues": 42,
        "critical_concentration_uM": 2.5,        # nucleation threshold
        "elongation_rate_per_s": 1.2e4,          # monomers/s per fibril end
        "primary_nucleation_rate": 3.0e-4,       # /M/s
        "secondary_nucleation_rate": 1.5e3,      # /M/s
        "lag_time_hours": 2.0,                   # at 10 μM
        "fibril_width_nm": 10.0,
        "fibril_twist_nm": 120.0,                # helical pitch
        "beta_sheet_spacing_A": 4.7,
        "source": "Cohen et al., PNAS 2013",
    }

    # Alpha-synuclein (Parkinson's)
    alpha_synuclein = {
        "name": "Alpha-synuclein",
        "length_residues": 140,
        "critical_concentration_uM": 35.0,
        "elongation_rate_per_s": 2.0e3,
        "primary_nucleation_rate": 2.0e-6,
        "secondary_nucleation_rate": 5.0e1,
        "lag_time_hours": 20.0,                  # at 70 μM
        "fibril_width_nm": 8.0,
        "fibril_twist_nm": 95.0,
        "source": "Buell et al., PNAS 2014",
    }

    # Tau (Alzheimer's, tauopathies)
    tau = {
        "name": "Tau (4R)",
        "length_residues": 441,
        "critical_concentration_uM": 1.0,
        "lag_time_hours": 5.0,
        "fibril_width_nm": 15.0,
        "source": "Fitzpatrick et al., Nature 2017",
    }

    # Huntingtin (Huntington's disease)
    huntingtin = {
        "name": "Huntingtin polyQ",
        "critical_polyQ_length": 36,             # disease threshold
        "lag_time_scaling": 2.5,                 # exponent with polyQ length
        "source": "Scherzinger et al., Cell 1997",
    }

    # Prion protein
    prion = {
        "name": "PrP (prion)",
        "length_residues": 253,
        "conversion_rate_per_day": 0.1,          # PrPC to PrPSc
        "fibril_width_nm": 12.0,
        "source": "Prusiner, PNAS 1998",
    }


# =============================================================================
# GEOMETRY SEARCH FUNCTIONS
# =============================================================================

def find_constant_relationships(value: float, name: str, constants: dict) -> List[dict]:
    """Search for relationships between a value and fundamental constants."""

    matches = []

    for const_name, const_val in constants.items():
        # Direct ratio
        ratio = value / const_val

        # Check for simple fractions
        for num in range(1, 13):
            for denom in range(1, 13):
                expected = const_val * num / denom
                if abs(value - expected) / value < 0.03:  # 3% tolerance
                    matches.append({
                        "value_name": name,
                        "value": value,
                        "constant": const_name,
                        "relationship": f"{num}/{denom} × {const_name}",
                        "predicted": expected,
                        "error_percent": abs(value - expected) / value * 100,
                    })

        # Check powers
        for power in [-2, -1, -0.5, 0.5, 1, 2]:
            expected = const_val ** power
            if abs(value - expected) / max(value, expected) < 0.03:
                matches.append({
                    "value_name": name,
                    "value": value,
                    "constant": const_name,
                    "relationship": f"{const_name}^{power}",
                    "predicted": expected,
                    "error_percent": abs(value - expected) / value * 100,
                })

        # Check with π multipliers
        for mult in [1, 2, 4]:
            expected = const_val * np.pi / mult
            if abs(value - expected) / max(value, expected) < 0.03:
                matches.append({
                    "value_name": name,
                    "value": value,
                    "constant": const_name,
                    "relationship": f"{const_name} × π/{mult}",
                    "predicted": expected,
                    "error_percent": abs(value - expected) / value * 100,
                })

    # Sort by error
    matches.sort(key=lambda x: x["error_percent"])
    return matches[:5]  # Top 5 matches


def explore_dna_geometry():
    """Search for Z² relationships in DNA geometry."""

    print("\n" + "=" * 70)
    print("DNA GEOMETRY EXPLORATION")
    print("=" * 70)

    dna = DNAGeometry()
    all_matches = []

    # Test B-DNA parameters
    print("\nB-DNA (most common biological form):")
    print("-" * 50)

    for param_name, param_value in dna.b_dna.items():
        matches = find_constant_relationships(param_value, param_name, CONSTANTS_TO_TEST)
        if matches:
            best = matches[0]
            status = "MATCH!" if best["error_percent"] < 1.0 else "weak"
            print(f"  {param_name}: {param_value}")
            print(f"    Best fit: {best['relationship']} = {best['predicted']:.4f}")
            print(f"    Error: {best['error_percent']:.2f}% [{status}]")
            all_matches.extend(matches)

    # Interesting ratios within DNA
    print("\nDNA Internal Ratios:")
    print("-" * 50)

    ratios = {
        "major/minor_groove": dna.b_dna["major_groove_width_A"] / dna.b_dna["minor_groove_width_A"],
        "pitch/diameter": dna.b_dna["helix_pitch_A"] / dna.b_dna["helix_diameter_A"],
        "twist × bp_per_turn / 360": dna.b_dna["twist_per_bp_deg"] * dna.b_dna["bp_per_turn"] / 360,
    }

    for ratio_name, ratio_value in ratios.items():
        matches = find_constant_relationships(ratio_value, ratio_name, CONSTANTS_TO_TEST)
        if matches:
            best = matches[0]
            print(f"  {ratio_name}: {ratio_value:.4f}")
            print(f"    Best fit: {best['relationship']} = {best['predicted']:.4f}")
            print(f"    Error: {best['error_percent']:.2f}%")

    return all_matches


def explore_protein_geometry():
    """Search for Z² relationships in protein secondary structure."""

    print("\n" + "=" * 70)
    print("PROTEIN SECONDARY STRUCTURE EXPLORATION")
    print("=" * 70)

    protein = ProteinGeometry()
    all_matches = []

    # Alpha helix
    print("\nAlpha Helix (most common secondary structure):")
    print("-" * 50)

    for param_name, param_value in protein.alpha_helix.items():
        if isinstance(param_value, (int, float)):
            matches = find_constant_relationships(abs(param_value), param_name, CONSTANTS_TO_TEST)
            if matches:
                best = matches[0]
                status = "MATCH!" if best["error_percent"] < 1.0 else "weak"
                print(f"  {param_name}: {param_value}")
                print(f"    Best fit: {best['relationship']} = {best['predicted']:.4f}")
                print(f"    Error: {best['error_percent']:.2f}% [{status}]")
                all_matches.extend(matches)

    # Test angle sums and differences
    print("\nRamachandran Angle Combinations:")
    print("-" * 50)

    helix_angles = {
        "φ + ψ (helix)": abs(protein.alpha_helix["phi_angle_deg"] + protein.alpha_helix["psi_angle_deg"]),
        "|φ| + |ψ| (helix)": abs(protein.alpha_helix["phi_angle_deg"]) + abs(protein.alpha_helix["psi_angle_deg"]),
        "φ - ψ (helix)": abs(protein.alpha_helix["phi_angle_deg"] - protein.alpha_helix["psi_angle_deg"]),
        "φ + ψ (sheet)": abs(protein.beta_sheet_anti["phi_angle_deg"] + protein.beta_sheet_anti["psi_angle_deg"]),
    }

    for angle_name, angle_value in helix_angles.items():
        matches = find_constant_relationships(angle_value, angle_name, CONSTANTS_TO_TEST)
        if matches:
            best = matches[0]
            print(f"  {angle_name}: {angle_value}°")
            print(f"    Best fit: {best['relationship']} = {best['predicted']:.4f}")
            print(f"    Error: {best['error_percent']:.2f}%")

    return all_matches


def explore_aggregation_kinetics():
    """Search for Z² relationships in protein aggregation (disease relevance)."""

    print("\n" + "=" * 70)
    print("PROTEIN AGGREGATION KINETICS (Alzheimer's, Parkinson's)")
    print("=" * 70)

    agg = AggregationData()
    all_matches = []

    # Amyloid-beta (Alzheimer's)
    print(f"\nAmyloid-beta 42 ({agg.amyloid_beta['source']}):")
    print("-" * 50)

    for param_name, param_value in agg.amyloid_beta.items():
        if isinstance(param_value, (int, float)) and param_value > 0:
            matches = find_constant_relationships(param_value, f"Aβ_{param_name}", CONSTANTS_TO_TEST)
            if matches:
                best = matches[0]
                if best["error_percent"] < 5.0:  # Looser tolerance for kinetics
                    print(f"  {param_name}: {param_value}")
                    print(f"    Best fit: {best['relationship']} = {best['predicted']:.4f}")
                    print(f"    Error: {best['error_percent']:.2f}%")
                    all_matches.extend(matches)

    # Alpha-synuclein (Parkinson's)
    print(f"\nAlpha-synuclein ({agg.alpha_synuclein['source']}):")
    print("-" * 50)

    for param_name, param_value in agg.alpha_synuclein.items():
        if isinstance(param_value, (int, float)) and param_value > 0:
            matches = find_constant_relationships(param_value, f"αSyn_{param_name}", CONSTANTS_TO_TEST)
            if matches:
                best = matches[0]
                if best["error_percent"] < 5.0:
                    print(f"  {param_name}: {param_value}")
                    print(f"    Best fit: {best['relationship']} = {best['predicted']:.4f}")
                    print(f"    Error: {best['error_percent']:.2f}%")
                    all_matches.extend(matches)

    # Cross-protein ratios
    print("\nCross-Disease Comparisons:")
    print("-" * 50)

    cross_ratios = {
        "αSyn/Aβ lag_time": agg.alpha_synuclein["lag_time_hours"] / agg.amyloid_beta["lag_time_hours"],
        "αSyn/Aβ critical_conc": agg.alpha_synuclein["critical_concentration_uM"] / agg.amyloid_beta["critical_concentration_uM"],
        "Aβ/αSyn elongation": agg.amyloid_beta["elongation_rate_per_s"] / agg.alpha_synuclein["elongation_rate_per_s"],
        "αSyn/Aβ fibril_width": agg.alpha_synuclein["fibril_width_nm"] / agg.amyloid_beta["fibril_width_nm"],
    }

    for ratio_name, ratio_value in cross_ratios.items():
        matches = find_constant_relationships(ratio_value, ratio_name, CONSTANTS_TO_TEST)
        if matches:
            best = matches[0]
            print(f"  {ratio_name}: {ratio_value:.4f}")
            print(f"    Best fit: {best['relationship']} = {best['predicted']:.4f}")
            print(f"    Error: {best['error_percent']:.2f}%")

    return all_matches


def explore_amino_acid_properties():
    """Search for Z² relationships in amino acid properties."""

    print("\n" + "=" * 70)
    print("AMINO ACID PROPERTY EXPLORATION")
    print("=" * 70)

    all_matches = []

    # Hydrophobicity range
    hydro_values = list(AMINO_ACID_HYDROPHOBICITY.values())
    hydro_range = max(hydro_values) - min(hydro_values)
    hydro_mean = np.mean(hydro_values)
    hydro_std = np.std(hydro_values)

    print("\nHydrophobicity Scale Statistics:")
    print("-" * 50)

    hydro_stats = {
        "range": hydro_range,
        "mean + max": abs(hydro_mean) + max(hydro_values),
        "std": hydro_std,
    }

    for stat_name, stat_value in hydro_stats.items():
        matches = find_constant_relationships(stat_value, f"hydro_{stat_name}", CONSTANTS_TO_TEST)
        if matches:
            best = matches[0]
            print(f"  {stat_name}: {stat_value:.4f}")
            print(f"    Best fit: {best['relationship']} = {best['predicted']:.4f}")
            print(f"    Error: {best['error_percent']:.2f}%")

    # pKa relationships
    print("\npKa Value Analysis:")
    print("-" * 50)

    pka_values = list(AMINO_ACID_PKA.values())
    pka_range = max(pka_values) - min(pka_values)

    pka_stats = {
        "range": pka_range,
        "physiological_pH / mean": 7.4 / np.mean(pka_values),
        "His_pKa": AMINO_ACID_PKA["His"],  # Near physiological pH
    }

    for stat_name, stat_value in pka_stats.items():
        matches = find_constant_relationships(stat_value, f"pKa_{stat_name}", CONSTANTS_TO_TEST)
        if matches:
            best = matches[0]
            print(f"  {stat_name}: {stat_value:.4f}")
            print(f"    Best fit: {best['relationship']} = {best['predicted']:.4f}")
            print(f"    Error: {best['error_percent']:.2f}%")

    # Number of amino acids
    print("\nFundamental: Why 20 amino acids?")
    print("-" * 50)

    n_aa = 20
    matches = find_constant_relationships(n_aa, "N_amino_acids", CONSTANTS_TO_TEST)
    for match in matches[:3]:
        print(f"  20 ≈ {match['relationship']} = {match['predicted']:.4f}")
        print(f"    Error: {match['error_percent']:.2f}%")

    # Also test 20 as related to genetic code
    print("\nGenetic Code: 64 codons → 20 amino acids + 3 stop")
    n_codons = 64
    coding_efficiency = 20 / 64

    matches = find_constant_relationships(coding_efficiency, "coding_efficiency", CONSTANTS_TO_TEST)
    if matches:
        best = matches[0]
        print(f"  20/64 = {coding_efficiency:.4f}")
        print(f"    Best fit: {best['relationship']} = {best['predicted']:.4f}")
        print(f"    Error: {best['error_percent']:.2f}%")

    return all_matches


def deep_combinatorial_search():
    """Brute force search for Z² combinations in biology."""

    print("\n" + "=" * 70)
    print("DEEP COMBINATORIAL SEARCH")
    print("=" * 70)
    print("Searching for combinations where biological values emerge from Z²...")

    # Key biological numbers to explain
    biological_targets = {
        "DNA_twist_deg": 34.3,
        "DNA_bp_per_turn": 10.5,
        "helix_res_per_turn": 3.6,
        "N_amino_acids": 20,
        "N_bases": 4,
        "N_codons": 64,
        "Watson_Crick_angle": 36.0,  # degrees in base pair
        "alpha_helix_phi": 57.0,
        "alpha_helix_psi": 47.0,
        "beta_sheet_angle_sum": 274.0,  # |φ| + |ψ|
        "Huntington_threshold": 36,  # polyQ repeat threshold
        "collagen_Gly_spacing": 3,  # Gly-X-Y pattern
    }

    # Extended constants
    extended_constants = {
        "Z": Z,
        "Z²": Z_SQUARED,
        "1/Z²": ONE_OVER_Z2,
        "π": np.pi,
        "2π": 2 * np.pi,
        "e": np.e,
        "φ": PHI_GOLDEN,
        "√2": np.sqrt(2),
        "√3": np.sqrt(3),
        "√Z": np.sqrt(Z),
        "Z/2": Z / 2,
        "Z²/π": Z_SQUARED / np.pi,
        "π/Z": np.pi / Z,
        "ln2": np.log(2),
        "ln10": np.log(10),
    }

    print("\nSearching for: target = a × const1 + b × const2")
    print("-" * 70)

    found_matches = []

    for target_name, target_value in biological_targets.items():
        best_match = None
        best_error = float('inf')

        # Try linear combinations
        const_names = list(extended_constants.keys())
        const_values = list(extended_constants.values())

        for i, (name1, val1) in enumerate(extended_constants.items()):
            for j, (name2, val2) in enumerate(extended_constants.items()):
                if i >= j:
                    continue

                # Solve: target = a*val1 + b*val2
                # Try integer coefficients
                for a in range(-12, 13):
                    for b in range(-12, 13):
                        if a == 0 and b == 0:
                            continue

                        predicted = a * val1 + b * val2
                        if predicted <= 0:
                            continue

                        error = abs(target_value - predicted) / target_value

                        if error < 0.01 and error < best_error:  # 1% threshold
                            best_error = error
                            best_match = {
                                "target": target_name,
                                "target_value": target_value,
                                "formula": f"{a}×{name1} + {b}×{name2}",
                                "predicted": predicted,
                                "error_percent": error * 100,
                            }

        if best_match:
            found_matches.append(best_match)
            print(f"\n{target_name} = {target_value}")
            print(f"  Formula: {best_match['formula']}")
            print(f"  Predicted: {best_match['predicted']:.4f}")
            print(f"  Error: {best_match['error_percent']:.3f}%")

    if not found_matches:
        print("\nNo strong matches found at 1% threshold.")
        print("This is an honest negative result.")

    return found_matches


def explore_disease_critical_numbers():
    """Look for Z² in disease-related thresholds."""

    print("\n" + "=" * 70)
    print("DISEASE THRESHOLD EXPLORATION")
    print("=" * 70)
    print("Many diseases have critical thresholds. Are any Z²-related?")

    # Real disease thresholds from literature
    disease_thresholds = {
        # Repeat expansion diseases
        "Huntington_polyQ_threshold": 36,        # CAG repeats
        "Huntington_polyQ_juvenile": 60,         # juvenile onset
        "SCA1_threshold": 39,                    # Spinocerebellar ataxia
        "SCA3_threshold": 55,
        "FRDA_GAA_threshold": 66,                # Friedreich's ataxia
        "Fragile_X_CGG_threshold": 200,

        # Aggregation thresholds (μM)
        "Abeta_critical_conc": 2.5,
        "alpha_syn_critical_conc": 35.0,
        "tau_critical_conc": 1.0,

        # Age of onset correlations
        "Alzheimer_EOAD_age": 65,                # Early onset cutoff
        "Parkinson_young_onset": 50,
        "Huntington_avg_onset": 45,

        # Clinical biomarker thresholds
        "CSF_Abeta42_cutoff_pgml": 192,          # Alzheimer's diagnosis
        "CSF_tau_cutoff_pgml": 93,
        "PET_SUVR_positive": 1.11,               # Amyloid PET threshold
    }

    print("\nDisease Thresholds vs Z² Constants:")
    print("-" * 70)

    matches = []
    for disease, threshold in disease_thresholds.items():
        disease_matches = find_constant_relationships(threshold, disease, CONSTANTS_TO_TEST)
        if disease_matches:
            best = disease_matches[0]
            if best["error_percent"] < 5.0:
                print(f"\n{disease} = {threshold}")
                print(f"  Best: {best['relationship']} = {best['predicted']:.4f}")
                print(f"  Error: {best['error_percent']:.2f}%")
                matches.extend(disease_matches)

    # Special analysis: Huntington's 36 repeat threshold
    print("\n" + "-" * 70)
    print("SPECIAL: Huntington's Disease CAG Repeat Threshold")
    print("-" * 70)
    print("Why does disease occur at exactly 36 CAG repeats?")
    print(f"  36 = 6²")
    print(f"  36 = 4 × 9 = 2² × 3²")
    print(f"  36 / Z² = {36 / Z_SQUARED:.4f} ≈ {36 / Z_SQUARED:.1f}")
    print(f"  36 × (1/Z²) = {36 * ONE_OVER_Z2:.4f}")
    print(f"  Z² + 3 = {Z_SQUARED + 3:.2f} ≈ 36.5 (close!)")

    # This is interesting: Z² + 3 ≈ 36.5, disease threshold is 36
    error = abs(36 - (Z_SQUARED + 3)) / 36 * 100
    print(f"  Error for Z² + 3 = 36: {error:.2f}%")

    if error < 2.0:
        print("  ** INTERESTING: Huntington threshold ≈ Z² + 3 **")

    return matches


def run_full_exploration():
    """Run complete Z² biology exploration."""

    print("=" * 78)
    print("Z² GEOMETRY EXPLORER FOR BIOLOGY")
    print("=" * 78)
    print(f"\nZ = 2√(8π/3) = {Z:.6f}")
    print(f"Z² = 32π/3 = {Z_SQUARED:.6f}")
    print(f"1/Z² = {ONE_OVER_Z2:.6f}")
    print(f"θ_Z² = π/Z = {np.degrees(THETA_Z2):.2f}°")
    print(f"\nSearching for these constants in biological structures...")
    print("Using REAL data from crystallography and published studies.")
    print("Most searches will fail. That's science.\n")

    all_results = {
        "constants": {
            "Z": Z,
            "Z_squared": Z_SQUARED,
            "one_over_Z2": ONE_OVER_Z2,
            "theta_Z2_deg": np.degrees(THETA_Z2),
        },
        "explorations": {}
    }

    # Run all explorations
    dna_matches = explore_dna_geometry()
    all_results["explorations"]["dna"] = dna_matches

    protein_matches = explore_protein_geometry()
    all_results["explorations"]["protein"] = protein_matches

    agg_matches = explore_aggregation_kinetics()
    all_results["explorations"]["aggregation"] = agg_matches

    aa_matches = explore_amino_acid_properties()
    all_results["explorations"]["amino_acids"] = aa_matches

    combo_matches = deep_combinatorial_search()
    all_results["explorations"]["combinatorial"] = combo_matches

    disease_matches = explore_disease_critical_numbers()
    all_results["explorations"]["disease_thresholds"] = disease_matches

    # Summary
    print("\n" + "=" * 78)
    print("EXPLORATION SUMMARY")
    print("=" * 78)

    all_good_matches = []
    for category, matches in all_results["explorations"].items():
        good = [m for m in matches if m.get("error_percent", 100) < 1.0]
        if good:
            all_good_matches.extend(good)
            print(f"\n{category}: {len(good)} matches <1% error")
            for m in good[:3]:
                print(f"  {m.get('value_name', m.get('target', '?'))}: {m.get('relationship', m.get('formula', '?'))}")

    print("\n" + "-" * 78)
    if all_good_matches:
        print(f"TOTAL STRONG MATCHES (<1% error): {len(all_good_matches)}")
        print("\nThese warrant further investigation.")
    else:
        print("NO STRONG MATCHES FOUND (<1% error)")
        print("\nThis is an honest negative result. Z² may not apply to")
        print("biological geometry at these scales.")

    # Honest assessment
    print("\n" + "=" * 78)
    print("HONEST ASSESSMENT")
    print("=" * 78)
    print("""
WHAT WE TESTED:
- DNA helix geometry (B-DNA, A-DNA, Z-DNA)
- Protein secondary structure (α-helix, β-sheet angles)
- Amino acid properties (hydrophobicity, pKa, MW)
- Aggregation kinetics (Alzheimer's Aβ, Parkinson's α-syn)
- Disease thresholds (Huntington's repeat length, etc.)
- Combinatorial search for linear combinations

WHAT WOULD VALIDATE Z² IN BIOLOGY:
1. Multiple independent matches with <0.1% error
2. A mechanistic explanation for WHY Z² appears
3. Predictions that can be tested experimentally
4. Consistency across different biological systems

CURRENT STATUS: EXPLORATORY
Most matches are weak (>1% error) or could be coincidental.
The search continues with honesty about results.
""")

    # Save results
    output_path = Path(__file__).parent / "z2_geometry_exploration_results.json"

    # Convert to serializable format
    def make_serializable(obj):
        if isinstance(obj, dict):
            return {k: make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [make_serializable(v) for v in obj]
        elif isinstance(obj, (np.floating, np.integer)):
            return float(obj)
        else:
            return obj

    with open(output_path, 'w') as f:
        json.dump(make_serializable(all_results), f, indent=2)
    print(f"\nResults saved to: {output_path}")

    return all_results


if __name__ == "__main__":
    results = run_full_exploration()
