#!/usr/bin/env python3
"""
================================================================================
RIGOROUS VALIDATION TASK 4: Testable Experimental Predictions
================================================================================

GOAL: Generate specific, falsifiable experimental predictions that would
      test the Z² abiogenesis hypothesis.

SCIENTIFIC METHOD:
  A good hypothesis makes testable predictions.
  If the predictions fail, the hypothesis is falsified.
  This is how science progresses.

We generate predictions for BOTH outcomes:
  - What would SUPPORT Z² abiogenesis?
  - What would FALSIFY Z² abiogenesis?

Author: Carl Zimmerman + Claude
License: AGPL-3.0-or-later
================================================================================
"""

import numpy as np
from typing import Dict, List
import json
import os

# Z² Constants
Z_CONSTANT = 2 * np.sqrt(8 * np.pi / 3)  # 5.7888 Å
Z_SQUARED = 32 * np.pi / 3  # 33.51
FES2_LATTICE = 5.417  # Å


def generate_testable_predictions():
    """Generate specific, testable experimental predictions."""

    print("="*70)
    print("TASK 4: Testable Experimental Predictions")
    print("="*70)

    predictions = []

    # ==========================================================================
    # PREDICTION 1: FeS₂ vs Other Minerals Amino Acid Synthesis
    # ==========================================================================

    print("\n" + "-"*70)
    print("PREDICTION 1: Mineral Lattice Dependence of Amino Acid Synthesis")
    print("-"*70)

    pred1 = {
        'id': 1,
        'title': 'Mineral Lattice Dependence of Amino Acid Synthesis',
        'z2_prediction': """
            If Z² geometry is special, amino acid synthesis rates should
            peak for minerals with lattice parameters near Z = 5.79 Å.

            Specifically:
            - FeS₂ (5.417 Å, 6.8% from Z) → HIGH yield
            - Quartz (4.91 Å, 15% from Z) → LOWER yield
            - Calcite (4.99 Å, 14% from Z) → LOWER yield
            - Galena PbS (5.94 Å, 2.6% from Z) → HIGHEST yield
        """,
        'experiment': """
            1. Prepare identical prebiotic soup (CH₄, NH₃, H₂O, HCN, H₂S)
            2. Use identical conditions (T=350K, pH=7, pressure=1atm)
            3. Add 1g of each mineral powder with known lattice parameter
            4. Incubate for 7 days with UV irradiation
            5. Quantify amino acid yield by HPLC

            Control: No mineral (solution only)
        """,
        'z2_support_result': """
            Amino acid yield correlates with |a - Z|:
            - Galena (5.94 Å): HIGHEST yield
            - FeS₂ (5.417 Å): HIGH yield
            - Quartz (4.91 Å): LOWER yield
            - No mineral: LOWEST yield
        """,
        'z2_falsify_result': """
            Amino acid yield correlates with known surface chemistry:
            - FeS₂: HIGH (known iron-sulfur catalysis)
            - Other Fe/S minerals: HIGH
            - Galena: LOW (no redox activity)
            - Yield independent of lattice parameter

            This would show catalysis is redox chemistry, not geometry.
        """,
        'current_literature': """
            EXISTING DATA (from Wächtershäuser, Huber, etc.):
            - Iron-sulfur minerals ARE catalytically active
            - The activity correlates with REDOX potential, not geometry
            - No published study has tested lattice parameter dependence
            - The iron-sulfur world hypothesis explains activity without Z²
        """,
        'difficulty': 'MEDIUM - Standard prebiotic chemistry setup',
        'estimated_cost': '$5,000-10,000'
    }

    print(f"\n  Z² Prediction:\n{pred1['z2_prediction']}")
    print(f"\n  Experiment:\n{pred1['experiment']}")
    print(f"\n  Result supporting Z²:\n{pred1['z2_support_result']}")
    print(f"\n  Result falsifying Z²:\n{pred1['z2_falsify_result']}")
    predictions.append(pred1)

    # ==========================================================================
    # PREDICTION 2: Chirality Selection on Mineral Surfaces
    # ==========================================================================

    print("\n" + "-"*70)
    print("PREDICTION 2: Chirality Selection on Mineral Surfaces")
    print("-"*70)

    pred2 = {
        'id': 2,
        'title': 'Chirality Selection on Mineral Surfaces',
        'z2_prediction': """
            If Z² geometry creates chirality bias, then:
            - Achiral minerals near Z spacing should show L-excess
            - The enantiomeric excess (ee) should correlate with |a - Z|

            Specifically:
            - FeS₂ (achiral, 5.417 Å): ee > 0% toward L
            - Quartz (chiral faces): ee depends on face handedness
        """,
        'experiment': """
            1. Synthesize amino acids on flat FeS₂ (100) surface
               (This face is achiral by crystallographic symmetry)
            2. Extract and analyze by chiral HPLC
            3. Measure enantiomeric excess

            Control 1: Solution synthesis (no mineral)
            Control 2: Quartz (101) face (known chiral surface)
        """,
        'z2_support_result': """
            FeS₂ (100) achiral surface shows L-excess:
            - ee > 1% toward L-amino acids
            - Excess correlates with proximity to Z spacing
        """,
        'z2_falsify_result': """
            FeS₂ (100) shows NO chirality selection:
            - ee = 0 ± 0.1% (racemic within error)
            - Only chiral quartz faces show chirality selection

            This would prove that achiral surfaces CANNOT select chirality
            (which is required by symmetry).
        """,
        'current_literature': """
            EXISTING DATA:
            - Chiral mineral surfaces (quartz, calcite) DO select chirality
            - This is well-established surface chemistry
            - No study has shown achiral surfaces selecting chirality
            - Symmetry requires achiral surfaces give racemic products

            PREDICTION: This experiment would FALSIFY Z² chirality claims.
        """,
        'difficulty': 'MEDIUM - Requires chiral HPLC and clean mineral surfaces',
        'estimated_cost': '$10,000-20,000'
    }

    print(f"\n  Z² Prediction:\n{pred2['z2_prediction']}")
    print(f"\n  Expected result (from symmetry):\n{pred2['z2_falsify_result']}")
    predictions.append(pred2)

    # ==========================================================================
    # PREDICTION 3: Helix Pitch vs Z Spacing
    # ==========================================================================

    print("\n" + "-"*70)
    print("PREDICTION 3: α-Helix Pitch Preference Under Constraints")
    print("-"*70)

    pred3 = {
        'id': 3,
        'title': 'Constrained Folding: Does Z Spacing Affect Helix Formation?',
        'z2_prediction': """
            If Z² geometry governs helix formation, then:
            - Peptides confined to Z-spacing should preferentially form helices
            - The helix pitch should be exactly Z = 5.79 Å, not 5.4 Å (experimental)
        """,
        'experiment': """
            1. Synthesize a 20-residue alanine peptide (strong helix former)
            2. Confine between two surfaces at controlled spacing:
               - 5.0 Å (too small for helix)
               - 5.4 Å (experimental helix pitch)
               - 5.79 Å (Z spacing)
               - 6.5 Å (too large)
            3. Measure circular dichroism (CD) for helix content
            4. Use AFM/STM to measure actual pitch under confinement

            Control: Free peptide in solution
        """,
        'z2_support_result': """
            Maximum helix formation at Z = 5.79 Å spacing:
            - Helix adopts pitch exactly matching Z
            - CD signal strongest at Z spacing
        """,
        'z2_falsify_result': """
            Maximum helix formation at 5.4 Å spacing:
            - Helix pitch is 5.4 Å regardless of confinement
            - Confinement at 5.79 Å distorts helix (lower CD signal)
            - The 5.4 Å experimental value is intrinsic to H-bond geometry

            This would show helix pitch is determined by chemistry, not Z.
        """,
        'current_literature': """
            EXISTING DATA:
            - Helix pitch is determined by H-bond geometry (i→i+4)
            - The 5.4 Å pitch is consistent across all organisms
            - No evidence of pitch variation with environmental constraints
            - Confinement typically disrupts secondary structure

            PREDICTION: This experiment would likely FALSIFY Z² helix claims.
        """,
        'difficulty': 'HIGH - Requires nanoscale confinement apparatus',
        'estimated_cost': '$50,000-100,000'
    }

    print(f"\n  Z² Prediction:\n{pred3['z2_prediction']}")
    print(f"\n  Likely result:\n{pred3['z2_falsify_result']}")
    predictions.append(pred3)

    # ==========================================================================
    # PREDICTION 4: π-π Stacking Distance
    # ==========================================================================

    print("\n" + "-"*70)
    print("PREDICTION 4: π-π Stacking Distance in Nucleotides")
    print("-"*70)

    pred4 = {
        'id': 4,
        'title': 'Z² Prediction for Nucleobase Stacking',
        'z2_prediction': """
            If Z² geometry governs molecular assembly, nucleobase π-stacking
            should occur at Z_bio = 6.015 Å (claimed Z² biological constant).

            Current claim: "Aromatic stacking occurs at Z_bio = 6.015 Å"
        """,
        'experiment': """
            1. Use X-ray crystallography of DNA/RNA structures
            2. Measure base-base stacking distances
            3. Compare to Z_bio = 6.015 Å prediction

            Data source: Protein Data Bank (no new experiment needed!)
        """,
        'z2_support_result': """
            Mean stacking distance = 6.015 ± 0.1 Å
        """,
        'z2_falsify_result': """
            ACTUAL DATA FROM PDB:
            - B-DNA base stacking: 3.4 Å (rise per base pair)
            - A-DNA base stacking: 2.6 Å
            - RNA stacking: 3.3 Å
            - Free adenine dimers: 3.3-3.5 Å

            The Z² biological constant (6.015 Å) does NOT match any
            observed stacking distance. The claim is FALSE.
        """,
        'current_literature': """
            EXISTING DATA (from thousands of PDB structures):
            - π-π stacking is 3.3-3.5 Å, NOT 6.0 Å
            - This is determined by van der Waals radii of aromatic systems
            - The 6.015 Å claim has no basis in experimental data

            CONCLUSION: Z_bio = 6.015 Å claim is already FALSIFIED.
        """,
        'difficulty': 'TRIVIAL - Just check the PDB',
        'estimated_cost': '$0 (public database)'
    }

    print(f"\n  Z² Prediction:\n{pred4['z2_prediction']}")
    print(f"\n  ACTUAL PDB DATA:\n{pred4['z2_falsify_result']}")
    predictions.append(pred4)

    # ==========================================================================
    # PREDICTION 5: Membrane Spacing
    # ==========================================================================

    print("\n" + "-"*70)
    print("PREDICTION 5: Membrane Headgroup Spacing")
    print("-"*70)

    pred5 = {
        'id': 5,
        'title': 'Phospholipid Headgroup Spacing',
        'z2_prediction': """
            Original claim: "Membrane optimal headgroup spacing relaxes to
            Z = 5.79 Å"
        """,
        'experiment': """
            Use SAXS (Small Angle X-ray Scattering) or neutron diffraction
            on lipid bilayers to measure headgroup-headgroup distance.

            Data source: Existing literature (no new experiment needed!)
        """,
        'z2_support_result': """
            Headgroup spacing = 5.79 ± 0.2 Å
        """,
        'z2_falsify_result': """
            ACTUAL EXPERIMENTAL DATA:
            - Bilayer thickness: 45-50 Å
            - Headgroup region thickness: 8-9 Å per leaflet
            - Phosphate-phosphate distance: ~10 Å
            - Lipid-lipid spacing: ~5.5 Å (varies with saturation)

            The headgroup region is 8-9 Å, NOT 5.79 Å.
            The original claim was based on incorrect data.
        """,
        'current_literature': """
            EXISTING DATA (from SAXS/neutron diffraction):
            - Tristram-Nagle & Nagle (2004): PC headgroup ~9 Å
            - Kucerka et al. (2011): DOPC headgroup region 9.0 Å
            - The 5.79 Å claim is ALREADY FALSIFIED by existing data.
        """,
        'difficulty': 'TRIVIAL - Literature review',
        'estimated_cost': '$0 (existing data)'
    }

    print(f"\n  Z² Prediction:\n{pred5['z2_prediction']}")
    print(f"\n  ACTUAL DATA:\n{pred5['z2_falsify_result']}")
    predictions.append(pred5)

    return predictions


def summarize_predictions(predictions: List[Dict]):
    """Summarize the status of all predictions."""

    print("\n" + "="*70)
    print("SUMMARY: Z² ABIOGENESIS PREDICTIONS")
    print("="*70)

    print("""
    +--------------------------------------------------------------------+
    | PREDICTION                         | STATUS                       |
    +------------------------------------+------------------------------+
    | 1. Mineral lattice -> synthesis    | NOT TESTED (testable)        |
    | 2. Chirality on achiral surfaces   | FALSIFIED BY SYMMETRY        |
    | 3. Helix pitch at Z spacing        | LIKELY FALSE (5.4 != 5.79)   |
    | 4. pi-pi stacking at 6.015 A       | FALSIFIED (actual: 3.3 A)    |
    | 5. Membrane headgroup at 5.79 A    | FALSIFIED (actual: 8-9 A)    |
    +--------------------------------------------------------------------+

    HONEST ASSESSMENT:

    Of the 5 core Z² abiogenesis predictions:
    - 3 are ALREADY FALSIFIED by existing data (#2, #4, #5)
    - 1 is LIKELY FALSE based on known helix geometry (#3)
    - 1 is TESTABLE but has conventional explanation (#1)

    The only potentially interesting result:
    - FeS₂ (5.417 Å) IS catalytically active
    - But this is explained by iron-sulfur chemistry, not Z² geometry
    - No experiment has tested whether lattice spacing matters

    CONCLUSION:
    The Z² abiogenesis hypothesis is LARGELY FALSIFIED by existing data.
    The remaining testable prediction (#1) has a conventional explanation.

    This does NOT mean Z² is wrong in OTHER domains (particle physics, etc.).
    It means the specific abiogenesis claims are not supported.
    """)


def propose_decisive_experiment():
    """Propose a single decisive experiment."""

    print("\n" + "="*70)
    print("PROPOSED DECISIVE EXPERIMENT")
    print("="*70)

    print("""
    THE GALENA TEST:

    Galena (PbS) has lattice parameter a = 5.94 Å, only 2.6% from Z = 5.79 Å.
    This is CLOSER to Z than FeS₂ (6.8% error).

    If Z² geometry drives prebiotic catalysis, then:
    - Galena should be a BETTER catalyst than FeS₂
    - Galena should show higher amino acid synthesis rates

    However, Galena:
    - Is NOT redox-active (Pb²⁺ doesn't change oxidation state easily)
    - Is TOXIC to biological systems
    - Is NOT associated with any prebiotic chemistry

    PREDICTION:
    If the experiment shows:
    - FeS₂ >> Galena catalysis → Z² FALSIFIED (chemistry matters, not geometry)
    - Galena >> FeS₂ catalysis → Z² SUPPORTED (geometry matters)

    Expected result based on chemistry:
    FeS₂ will be much more catalytic than Galena, falsifying Z².

    WHY THIS EXPERIMENT IS DECISIVE:
    - Galena is closer to Z than FeS₂
    - But Galena lacks the chemistry FeS₂ has
    - If geometry mattered, Galena would win
    - If chemistry matters, FeS₂ wins
    - We expect FeS₂ to win, falsifying the geometry claim

    COST: ~$5,000-10,000
    TIME: 2-4 weeks
    DIFFICULTY: Medium (standard prebiotic chemistry)
    """)


# =============================================================================
# MAIN
# =============================================================================

def run_full_prediction_analysis():
    """Generate all predictions and summary."""

    predictions = generate_testable_predictions()
    summarize_predictions(predictions)
    propose_decisive_experiment()

    # Save predictions
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(output_dir, 'task4_predictions.json')

    with open(output_file, 'w') as f:
        json.dump(predictions, f, indent=2)

    print(f"\n  Predictions saved to: {output_file}")

    return predictions


if __name__ == "__main__":
    predictions = run_full_prediction_analysis()
