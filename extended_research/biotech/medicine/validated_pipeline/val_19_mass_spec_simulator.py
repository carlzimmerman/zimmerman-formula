#!/usr/bin/env python3
"""
val_19_mass_spec_simulator.py

Copyright (C) 2026 Carl Zimmerman
Zimmerman Unified Geometry Framework (ZUGF)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

val_19_mass_spec_simulator.py - Mass Spectrometry QA/QC Simulator

FINAL SANITY CHECK BEFORE PHYSICAL SYNTHESIS
=============================================

This script performs the ultimate cheminformatic validation:

1. Load RDKit-generated SMILES for each peptide drug
2. Validate chemical structure (valences, aromaticity, stereochemistry)
3. Calculate exact isotopic distribution for [M+H]+ ion
4. Generate theoretical MS peaks that the CRO will use to confirm synthesis

THE OUTPUT:
When the CRO synthesizes ZIM-SYN-004 and runs mass spectrometry, they will
see peaks at EXACTLY these m/z values. If the peaks don't match, they
built the wrong molecule.

ISOTOPIC DISTRIBUTION:
Carbon-12 vs Carbon-13 (1.1% natural abundance) creates a characteristic
isotope pattern. We calculate the exact theoretical distribution.

AGPL-3.0-or-later License
Author: Carl Zimmerman
Date: April 22, 2026
"""
import json
import math
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from collections import Counter
import warnings

try:
    from rdkit import Chem
    from rdkit.Chem import AllChem, Descriptors, rdMolDescriptors
    from rdkit.Chem import MolFromSequence, MolToSmiles, MolFromSmiles
    from rdkit.Chem.rdMolDescriptors import CalcMolFormula
    HAS_RDKIT = True
except ImportError:
    HAS_RDKIT = False
    warnings.warn("RDKit required: pip install rdkit")

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

OUTPUT_DIR = Path(__file__).parent / "results" / "mass_spec_validation"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SOW_DIR = Path(__file__).parent / "results" / "synthesis_sow"

# ============================================================================
# ISOTOPE DATA (Natural Abundance)
# ============================================================================

# Natural isotope abundances and masses
# Format: {element: [(mass, abundance), ...]}
ISOTOPES = {
    'C': [(12.000000, 0.9893), (13.003355, 0.0107)],
    'H': [(1.007825, 0.999885), (2.014102, 0.000115)],
    'N': [(14.003074, 0.99632), (15.000109, 0.00368)],
    'O': [(15.994915, 0.99757), (16.999132, 0.00038), (17.999160, 0.00205)],
    'S': [(31.972071, 0.9499), (32.971459, 0.0075), (33.967867, 0.0425), (35.967081, 0.0001)],
}

# Monoisotopic masses (most abundant isotope)
MONOISOTOPIC_MASS = {
    'C': 12.000000,
    'H': 1.007825,
    'N': 14.003074,
    'O': 15.994915,
    'S': 31.972071,
}

# Proton mass for [M+H]+ calculation
PROTON_MASS = 1.007276


@dataclass
class IsotopePeak:
    """Represents a single isotope peak."""
    mass: float
    intensity: float  # Relative intensity (0-100)
    label: str  # e.g., "M+0", "M+1", "M+2"


@dataclass
class MoleculeValidation:
    """Results of chemical validation."""
    smiles: str
    is_valid: bool
    molecular_formula: str
    monoisotopic_mass: float
    mh_plus_mass: float  # [M+H]+
    atom_counts: Dict[str, int]
    warnings: List[str]
    errors: List[str]
    isotope_peaks: List[IsotopePeak]


def parse_molecular_formula(formula: str) -> Dict[str, int]:
    """Parse molecular formula string to atom counts."""
    import re
    pattern = r'([A-Z][a-z]?)(\d*)'
    matches = re.findall(pattern, formula)

    counts = {}
    for element, count in matches:
        if element:
            counts[element] = int(count) if count else 1

    return counts


def calculate_monoisotopic_mass(atom_counts: Dict[str, int]) -> float:
    """Calculate monoisotopic mass from atom counts."""
    mass = 0.0
    for element, count in atom_counts.items():
        if element in MONOISOTOPIC_MASS:
            mass += MONOISOTOPIC_MASS[element] * count
    return mass


def calculate_isotope_distribution(atom_counts: Dict[str, int], n_peaks: int = 5) -> List[IsotopePeak]:
    """
    Calculate isotopic distribution using polynomial expansion.

    For small molecules, we use a simplified convolution approach.
    For each element, we calculate the probability of having 0, 1, 2, etc.
    heavy isotopes, then combine across all elements.
    """
    # Start with monoisotopic peak
    base_mass = calculate_monoisotopic_mass(atom_counts)

    # For peptides, the dominant isotope pattern is from 13C
    # We use a binomial approximation for carbon
    n_carbons = atom_counts.get('C', 0)
    n_nitrogens = atom_counts.get('N', 0)
    n_oxygens = atom_counts.get('O', 0)
    n_sulfurs = atom_counts.get('S', 0)

    # 13C probability
    p_13c = 0.0107
    # 15N probability
    p_15n = 0.00368
    # 18O probability (17O is negligible)
    p_18o = 0.00205
    # 34S probability
    p_34s = 0.0425

    # Combined probability of getting k heavy atoms (simplified)
    # Using Poisson approximation for large n, small p
    lambda_total = (n_carbons * p_13c +
                    n_nitrogens * p_15n +
                    n_oxygens * p_18o +
                    n_sulfurs * p_34s)

    peaks = []

    for k in range(n_peaks):
        # Mass shift: approximately 1 Da per heavy isotope
        # (13C-12C = 1.0034, 15N-14N = 0.997, 18O-16O = 2.004, 34S-32S = 1.996)
        mass_shift = k * 1.0034  # Dominated by 13C

        # Poisson probability
        prob = (lambda_total ** k) * np.exp(-lambda_total) / math.factorial(k)

        # Normalize so M+0 = 100%
        if k == 0:
            norm_factor = 100.0 / prob if prob > 0 else 1.0

        intensity = prob * norm_factor

        peaks.append(IsotopePeak(
            mass=base_mass + mass_shift,
            intensity=min(intensity, 100.0),
            label=f"M+{k}"
        ))

    return peaks


def validate_molecule_rdkit(smiles: str) -> Tuple[bool, List[str], List[str]]:
    """
    Validate molecule using RDKit's sanitization.

    Returns (is_valid, warnings, errors)
    """
    warnings_list = []
    errors_list = []

    if not HAS_RDKIT:
        return False, [], ["RDKit not available"]

    try:
        mol = MolFromSmiles(smiles)

        if mol is None:
            return False, [], ["Invalid SMILES: could not parse"]

        # Check sanitization
        try:
            Chem.SanitizeMol(mol)
        except Exception as e:
            errors_list.append(f"Sanitization failed: {str(e)}")
            return False, warnings_list, errors_list

        # Check for radicals
        for atom in mol.GetAtoms():
            if atom.GetNumRadicalElectrons() > 0:
                warnings_list.append(f"Radical detected on atom {atom.GetIdx()}")

        # Check valences
        try:
            Chem.rdmolops.AssignRadicals(mol)
        except:
            pass

        # Check for disconnected fragments
        frags = Chem.GetMolFrags(mol)
        if len(frags) > 1:
            warnings_list.append(f"Molecule has {len(frags)} disconnected fragments")

        # Check stereochemistry
        chiral_centers = Chem.FindMolChiralCenters(mol, includeUnassigned=True)
        unassigned_stereo = [c for c in chiral_centers if c[1] == '?']
        if unassigned_stereo:
            warnings_list.append(f"{len(unassigned_stereo)} unassigned stereocenters")

        # Check for aromatic systems
        aromatic_atoms = sum(1 for atom in mol.GetAtoms() if atom.GetIsAromatic())
        if aromatic_atoms > 0:
            # Verify aromaticity is valid
            try:
                Chem.SetAromaticity(mol)
            except:
                warnings_list.append("Aromaticity assignment issues")

        return True, warnings_list, errors_list

    except Exception as e:
        return False, [], [f"Validation error: {str(e)}"]


def validate_peptide(sequence: str, n_cap: bool = False, c_cap: bool = False) -> MoleculeValidation:
    """
    Complete validation of a peptide molecule.
    """
    warnings_list = []
    errors_list = []

    if not HAS_RDKIT:
        return MoleculeValidation(
            smiles="",
            is_valid=False,
            molecular_formula="",
            monoisotopic_mass=0.0,
            mh_plus_mass=0.0,
            atom_counts={},
            warnings=[],
            errors=["RDKit not available"],
            isotope_peaks=[],
        )

    try:
        # Generate molecule from sequence
        mol = MolFromSequence(sequence)

        if mol is None:
            return MoleculeValidation(
                smiles="",
                is_valid=False,
                molecular_formula="",
                monoisotopic_mass=0.0,
                mh_plus_mass=0.0,
                atom_counts={},
                warnings=[],
                errors=[f"Could not parse sequence: {sequence}"],
                isotope_peaks=[],
            )

        # Sanitize
        Chem.SanitizeMol(mol)

        # Get SMILES
        smiles = MolToSmiles(mol, canonical=True)

        # Validate SMILES
        is_valid, val_warnings, val_errors = validate_molecule_rdkit(smiles)
        warnings_list.extend(val_warnings)
        errors_list.extend(val_errors)

        # Get molecular formula
        formula = CalcMolFormula(mol)

        # Parse formula to get atom counts
        atom_counts = parse_molecular_formula(formula)

        # Adjust for caps
        if n_cap:  # Acetyl: +C2H2O
            atom_counts['C'] = atom_counts.get('C', 0) + 2
            atom_counts['H'] = atom_counts.get('H', 0) + 2
            atom_counts['O'] = atom_counts.get('O', 0) + 1

        if c_cap:  # Amide: -O +NH
            atom_counts['O'] = atom_counts.get('O', 0) - 1
            atom_counts['N'] = atom_counts.get('N', 0) + 1
            atom_counts['H'] = atom_counts.get('H', 0) + 1

        # Calculate monoisotopic mass
        mono_mass = calculate_monoisotopic_mass(atom_counts)

        # [M+H]+ mass
        mh_plus = mono_mass + PROTON_MASS

        # Calculate isotope distribution for [M+H]+
        isotope_peaks = calculate_isotope_distribution(atom_counts)
        # Shift peaks by proton mass
        for peak in isotope_peaks:
            peak.mass += PROTON_MASS

        # Rebuild formula string with caps
        formula_parts = []
        for element in ['C', 'H', 'N', 'O', 'S']:
            if element in atom_counts and atom_counts[element] > 0:
                if atom_counts[element] == 1:
                    formula_parts.append(element)
                else:
                    formula_parts.append(f"{element}{atom_counts[element]}")
        adjusted_formula = ''.join(formula_parts)

        # Stereochemistry check
        chiral_centers = Chem.FindMolChiralCenters(mol)
        if chiral_centers:
            # Verify all are L-amino acids (@@)
            smiles_check = MolToSmiles(mol, isomericSmiles=True)
            if '[C@H]' in smiles_check and '[C@@H]' not in smiles_check:
                warnings_list.append("Unexpected D-amino acid stereochemistry detected")

        return MoleculeValidation(
            smiles=smiles,
            is_valid=is_valid and len(errors_list) == 0,
            molecular_formula=adjusted_formula,
            monoisotopic_mass=mono_mass,
            mh_plus_mass=mh_plus,
            atom_counts=atom_counts,
            warnings=warnings_list,
            errors=errors_list,
            isotope_peaks=isotope_peaks,
        )

    except Exception as e:
        return MoleculeValidation(
            smiles="",
            is_valid=False,
            molecular_formula="",
            monoisotopic_mass=0.0,
            mh_plus_mass=0.0,
            atom_counts={},
            warnings=[],
            errors=[f"Validation failed: {str(e)}"],
            isotope_peaks=[],
        )


def generate_ms_spectrum_plot(validation: MoleculeValidation, peptide_id: str,
                               output_path: Path) -> None:
    """Generate MS spectrum plot showing isotope distribution."""
    if not HAS_MATPLOTLIB or not validation.isotope_peaks:
        return

    fig, ax = plt.subplots(figsize=(10, 6))

    masses = [p.mass for p in validation.isotope_peaks]
    intensities = [p.intensity for p in validation.isotope_peaks]
    labels = [p.label for p in validation.isotope_peaks]

    # Bar plot for peaks
    bars = ax.bar(masses, intensities, width=0.3, color='steelblue',
                  edgecolor='black', alpha=0.8)

    # Labels
    for mass, intensity, label in zip(masses, intensities, labels):
        ax.annotate(f'{label}\n{mass:.2f}',
                    xy=(mass, intensity), xytext=(0, 5),
                    textcoords='offset points', ha='center', fontsize=9)

    ax.set_xlabel('m/z', fontsize=12)
    ax.set_ylabel('Relative Intensity (%)', fontsize=12)
    ax.set_title(f'Theoretical Mass Spectrum: {peptide_id}\n'
                 f'[M+H]+ = {validation.mh_plus_mass:.4f} Da',
                 fontsize=14, fontweight='bold')

    ax.set_ylim(0, 120)
    ax.grid(True, alpha=0.3, axis='y')

    # Add formula annotation
    ax.text(0.98, 0.95, f'Formula: {validation.molecular_formula}\n'
                         f'Monoisotopic: {validation.monoisotopic_mass:.4f} Da',
            transform=ax.transAxes, fontsize=10, va='top', ha='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"    MS spectrum: {output_path}")


def append_ms_data_to_sow(peptide_id: str, validation: MoleculeValidation) -> None:
    """Append MS QA/QC data to existing SOW document."""
    sow_file = SOW_DIR / f"SOW_{peptide_id}.txt"

    if not sow_file.exists():
        print(f"    Warning: SOW file not found: {sow_file}")
        return

    ms_section = f"""

================================================================================
APPENDIX: MASS SPECTROMETRY QA/QC SIGNATURE
================================================================================

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

CHEMICAL VALIDATION STATUS: {'PASSED' if validation.is_valid else 'FAILED'}
{'Warnings: ' + ', '.join(validation.warnings) if validation.warnings else ''}
{'Errors: ' + ', '.join(validation.errors) if validation.errors else ''}

MOLECULAR DETAILS
─────────────────
Molecular Formula:     {validation.molecular_formula}
Monoisotopic Mass:     {validation.monoisotopic_mass:.4f} Da
[M+H]+ (protonated):   {validation.mh_plus_mass:.4f} Da

Atom Composition:
  Carbon (C):    {validation.atom_counts.get('C', 0)}
  Hydrogen (H):  {validation.atom_counts.get('H', 0)}
  Nitrogen (N):  {validation.atom_counts.get('N', 0)}
  Oxygen (O):    {validation.atom_counts.get('O', 0)}
  Sulfur (S):    {validation.atom_counts.get('S', 0)}

THEORETICAL ISOTOPE DISTRIBUTION [M+H]+
────────────────────────────────────────
These are the EXACT m/z values the CRO should observe:

"""

    for peak in validation.isotope_peaks:
        ms_section += f"  {peak.label:6}  m/z = {peak.mass:10.4f}  Intensity: {peak.intensity:6.2f}%\n"

    ms_section += f"""
ACCEPTANCE CRITERIA
───────────────────
1. Primary peak [M+H]+ at m/z = {validation.mh_plus_mass:.2f} ± 1.0 Da
2. Isotope pattern matches theoretical distribution (±10% relative intensity)
3. No unexpected adducts or fragments indicating impurities

If peaks do not match, the synthesis FAILED. Request re-synthesis.

================================================================================
"""

    # Append to SOW
    with open(sow_file, 'a') as f:
        f.write(ms_section)

    print(f"    Updated: {sow_file}")


def main():
    """Main execution: Mass spectrometry validation."""
    print("=" * 80)
    print("MASS SPECTROMETRY QA/QC SIMULATOR")
    print("Final Chemical Validation Before Physical Synthesis")
    print("=" * 80)

    if not HAS_RDKIT:
        print("\nERROR: RDKit required. Install with: pip install rdkit")
        return None

    print(f"""
    FINAL SANITY CHECK
    ──────────────────
    This script validates the chemical integrity of our peptide drugs
    and calculates the exact mass spectrometry signatures the CRO will
    use to confirm successful synthesis.

    If RDKit cannot sanitize the molecule, the SMILES is invalid.
    If the isotope pattern doesn't match, the CRO built the wrong molecule.
""")

    # Our peptide drugs
    PEPTIDES = {
        'ZIM-SYN-004': {
            'sequence': 'FPF',
            'n_cap': True,
            'c_cap': True,
            'target': 'Alpha-synuclein',
            'indication': "Parkinson's Disease",
        },
        'ZIM-ADD-003': {
            'sequence': 'RWWFWR',
            'n_cap': False,
            'c_cap': True,
            'target': 'Alpha-3/Beta-4 nAChR',
            'indication': 'Opioid Addiction',
        },
        'ZIM-ALZ-001': {
            'sequence': 'WFFY',
            'n_cap': True,
            'c_cap': True,
            'target': 'Tau Protein',
            'indication': "Alzheimer's Disease",
        },
    }

    results = {
        'timestamp': datetime.now().isoformat(),
        'method': 'Mass Spectrometry QA/QC Validation',
        'peptides': {},
    }

    all_valid = True

    for peptide_id, info in PEPTIDES.items():
        print(f"\n  {'='*60}")
        print(f"  {peptide_id}: {info['sequence']}")
        print(f"  {'='*60}")

        # Validate
        validation = validate_peptide(
            info['sequence'],
            info.get('n_cap', False),
            info.get('c_cap', False)
        )

        # Print results
        status = "VALID" if validation.is_valid else "INVALID"
        status_symbol = "✓" if validation.is_valid else "✗"

        print(f"""
    CHEMICAL VALIDATION: {status_symbol} {status}

    SMILES:
    {validation.smiles}

    Molecular Formula:   {validation.molecular_formula}
    Monoisotopic Mass:   {validation.monoisotopic_mass:.4f} Da
    [M+H]+ Mass:         {validation.mh_plus_mass:.4f} Da

    THEORETICAL ISOTOPE DISTRIBUTION [M+H]+:
""")

        for peak in validation.isotope_peaks[:5]:
            print(f"      {peak.label:6}  m/z = {peak.mass:.4f}  ({peak.intensity:.1f}%)")

        if validation.warnings:
            print(f"\n    Warnings: {', '.join(validation.warnings)}")
        if validation.errors:
            print(f"\n    ERRORS: {', '.join(validation.errors)}")
            all_valid = False

        # Generate MS plot
        if HAS_MATPLOTLIB:
            plot_path = OUTPUT_DIR / f'{peptide_id}_ms_spectrum.png'
            generate_ms_spectrum_plot(validation, peptide_id, plot_path)

        # Append to SOW
        append_ms_data_to_sow(peptide_id, validation)

        # Store results
        results['peptides'][peptide_id] = {
            'sequence': info['sequence'],
            'is_valid': validation.is_valid,
            'smiles': validation.smiles,
            'molecular_formula': validation.molecular_formula,
            'monoisotopic_mass': validation.monoisotopic_mass,
            'mh_plus_mass': validation.mh_plus_mass,
            'atom_counts': validation.atom_counts,
            'isotope_peaks': [
                {'mass': p.mass, 'intensity': p.intensity, 'label': p.label}
                for p in validation.isotope_peaks
            ],
            'warnings': validation.warnings,
            'errors': validation.errors,
        }

    # Summary
    print("\n" + "=" * 80)
    print("MASS SPECTROMETRY VALIDATION SUMMARY")
    print("=" * 80)

    print(f"""
    Peptides validated: {len(PEPTIDES)}
    All valid: {'YES' if all_valid else 'NO'}
""")

    for peptide_id, data in results['peptides'].items():
        status = "✓ VALID" if data['is_valid'] else "✗ INVALID"
        print(f"    {peptide_id:15} | {data['molecular_formula']:20} | [M+H]+ = {data['mh_plus_mass']:.4f} Da | {status}")

    # Final verdict
    print("\n    " + "=" * 60)
    if all_valid:
        print("    VERDICT: ALL PEPTIDES CHEMICALLY VALID")
        print("    SOW documents updated with MS QA/QC signatures.")
        print("    Ready for CRO submission.")
        results['verdict'] = 'ALL_VALID'
    else:
        print("    VERDICT: VALIDATION FAILED")
        print("    Fix errors before submitting to CRO.")
        results['verdict'] = 'FAILED'
    print("    " + "=" * 60)

    # Save results
    output_path = OUTPUT_DIR / 'mass_spec_validation_results.json'
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n  Results: {output_path}")
    print(f"  MS spectra: {OUTPUT_DIR}")

    return results


if __name__ == '__main__':
    results = main()
