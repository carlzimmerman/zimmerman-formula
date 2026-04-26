#!/usr/bin/env python3
"""
res_09_cro_sow_generator.py

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

res_09_cro_sow_generator.py - Contract Research Organization Statement of Work Generator

PURPOSE:
Automatically generate a professional Statement of Work (SOW) for peptide
synthesis and validation by Contract Research Organizations (CROs).

OUTPUT:
- PDF document specifying synthesis, purification, and assay parameters
- Ready to submit to GenScript, WuXi AppTec, Bachem, or similar CROs

SPECIFICATIONS:
- Solid-Phase Peptide Synthesis (SPPS)
- >95% HPLC purity
- TFA to Acetate salt exchange
- Mass spectrometry confirmation
- Surface Plasmon Resonance (SPR) binding assay

AGPL-3.0-or-later License
Author: Carl Zimmerman
Date: April 21, 2026
"""
import numpy as np
from pathlib import Path
from datetime import datetime
import json
from typing import Dict, List, Optional

OUTPUT_DIR = Path(__file__).parent / "results" / "cro_sow"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("CRO STATEMENT OF WORK GENERATOR")
print("Preparing peptide synthesis and validation orders")
print("=" * 80)
print()

# =============================================================================
# AMINO ACID PROPERTIES
# =============================================================================

AA_PROPERTIES = {
    'A': {'name': 'Alanine', 'mw': 89.09, 'hydropathy': 1.8},
    'R': {'name': 'Arginine', 'mw': 174.20, 'hydropathy': -4.5},
    'N': {'name': 'Asparagine', 'mw': 132.12, 'hydropathy': -3.5},
    'D': {'name': 'Aspartic acid', 'mw': 133.10, 'hydropathy': -3.5},
    'C': {'name': 'Cysteine', 'mw': 121.15, 'hydropathy': 2.5},
    'E': {'name': 'Glutamic acid', 'mw': 147.13, 'hydropathy': -3.5},
    'Q': {'name': 'Glutamine', 'mw': 146.15, 'hydropathy': -3.5},
    'G': {'name': 'Glycine', 'mw': 75.07, 'hydropathy': -0.4},
    'H': {'name': 'Histidine', 'mw': 155.16, 'hydropathy': -3.2},
    'I': {'name': 'Isoleucine', 'mw': 131.17, 'hydropathy': 4.5},
    'L': {'name': 'Leucine', 'mw': 131.17, 'hydropathy': 3.8},
    'K': {'name': 'Lysine', 'mw': 146.19, 'hydropathy': -3.9},
    'M': {'name': 'Methionine', 'mw': 149.21, 'hydropathy': 1.9},
    'F': {'name': 'Phenylalanine', 'mw': 165.19, 'hydropathy': 2.8},
    'P': {'name': 'Proline', 'mw': 115.13, 'hydropathy': -1.6},
    'S': {'name': 'Serine', 'mw': 105.09, 'hydropathy': -0.8},
    'T': {'name': 'Threonine', 'mw': 119.12, 'hydropathy': -0.7},
    'W': {'name': 'Tryptophan', 'mw': 204.23, 'hydropathy': -0.9},
    'Y': {'name': 'Tyrosine', 'mw': 181.19, 'hydropathy': -1.3},
    'V': {'name': 'Valine', 'mw': 117.15, 'hydropathy': 4.2},
}


# =============================================================================
# PEPTIDE PROPERTY CALCULATION
# =============================================================================

def calculate_peptide_properties(sequence: str, n_cap: str = None, c_cap: str = None) -> Dict:
    """
    Calculate molecular weight, pI, and GRAVY for a peptide sequence.
    """
    # Molecular weight
    mw = 18.015  # H2O for terminal groups
    for aa in sequence.upper():
        if aa in AA_PROPERTIES:
            mw += AA_PROPERTIES[aa]['mw'] - 18.015  # Subtract water for peptide bond

    # Add caps
    if n_cap == 'ACE':
        mw += 42.04  # Acetyl group
    if c_cap == 'NME':
        mw += 14.03  # N-methyl amide

    # GRAVY (Grand Average of Hydropathy)
    gravy_values = []
    for aa in sequence.upper():
        if aa in AA_PROPERTIES:
            gravy_values.append(AA_PROPERTIES[aa]['hydropathy'])

    gravy = np.mean(gravy_values) if gravy_values else 0.0

    # Estimated pI (simplified)
    # Count charged residues
    positive = sequence.upper().count('R') + sequence.upper().count('K') + sequence.upper().count('H')
    negative = sequence.upper().count('D') + sequence.upper().count('E')

    if positive > negative:
        pI_estimate = 9.0 + (positive - negative) * 0.5
    elif negative > positive:
        pI_estimate = 5.0 - (negative - positive) * 0.5
    else:
        pI_estimate = 7.0

    pI_estimate = max(3.0, min(12.0, pI_estimate))

    return {
        'molecular_weight_Da': float(mw),
        'gravy': float(gravy),
        'pI_estimate': float(pI_estimate),
        'length': len(sequence),
        'n_positive': positive,
        'n_negative': negative,
        'net_charge_pH7': positive - negative,
    }


# =============================================================================
# SOW GENERATION
# =============================================================================

def generate_sow_text(
    peptide_id: str,
    sequence: str,
    target_protein: str,
    properties: Dict,
    n_cap: str = None,
    c_cap: str = None,
    amount_mg: float = 5.0,
) -> str:
    """
    Generate Statement of Work text document.
    """
    # Full sequence with caps
    full_sequence = ""
    if n_cap == 'ACE':
        full_sequence = "Ac-"
    full_sequence += "-".join(list(sequence))
    if c_cap == 'NME':
        full_sequence += "-NH2"
    else:
        full_sequence += "-OH"

    sow_text = f"""
================================================================================
                    STATEMENT OF WORK
                    PEPTIDE SYNTHESIS AND VALIDATION
================================================================================

Date: {datetime.now().strftime('%Y-%m-%d')}
Project ID: {peptide_id}
Principal Investigator: [TO BE FILLED]
Organization: [TO BE FILLED]

================================================================================
SECTION 1: PEPTIDE SPECIFICATIONS
================================================================================

Peptide ID:           {peptide_id}
Sequence:             {full_sequence}
Amino Acid Sequence:  {sequence}
Length:               {properties['length']} residues
N-Terminal Cap:       {'Acetyl (Ac)' if n_cap == 'ACE' else 'Free amine'}
C-Terminal Cap:       {'Amide (NH2)' if c_cap == 'NME' else 'Free carboxyl'}

Calculated Properties:
  Molecular Weight:   {properties['molecular_weight_Da']:.2f} Da
  Isoelectric Point:  {properties['pI_estimate']:.1f} (estimated)
  GRAVY Score:        {properties['gravy']:.2f}
  Net Charge (pH 7):  {'+' if properties['net_charge_pH7'] > 0 else ''}{properties['net_charge_pH7']}

================================================================================
SECTION 2: SYNTHESIS REQUIREMENTS
================================================================================

Synthesis Method:     Solid-Phase Peptide Synthesis (SPPS)
Resin Type:           {'Rink Amide' if c_cap == 'NME' else 'Wang'} resin
Coupling Chemistry:   Fmoc/tBu strategy
Activation Reagent:   HBTU/DIPEA or equivalent

Amount Required:      {amount_mg:.1f} mg (lyophilized powder)
Purity:               >95% by analytical HPLC
Salt Form:            Acetate (TFA to Acetate exchange REQUIRED)

CRITICAL: TFA salt exchange is mandatory. TFA is cytotoxic and will
compromise downstream cell-based assays.

================================================================================
SECTION 3: QUALITY CONTROL
================================================================================

Required QC Tests:
1. HPLC Analysis
   - Column: C18 reverse phase
   - Gradient: 5-95% acetonitrile/water (0.1% TFA)
   - Acceptance: Single peak >95% area

2. Mass Spectrometry
   - Method: MALDI-TOF or ESI-MS
   - Target: {properties['molecular_weight_Da']:.2f} Da (+/- 1 Da)
   - Report: Full spectrum with annotated peaks

3. Amino Acid Analysis (optional)
   - Composition verification

Deliverables:
- Lyophilized peptide in sealed vial
- HPLC chromatogram with retention time and purity %
- Mass spectrum with m/z annotation
- Certificate of Analysis (CoA)

================================================================================
SECTION 4: BINDING VALIDATION (SPR ASSAY)
================================================================================

Target Protein:       {target_protein}
Method:               Surface Plasmon Resonance (SPR)
Instrument:           Biacore T200 or equivalent

Protocol:
1. Immobilize {target_protein} on CM5 sensor chip via amine coupling
2. Target density: 1000-3000 RU
3. Flow peptide at concentrations: 10 nM, 100 nM, 1 μM, 10 μM
4. Running buffer: HBS-EP+ (10 mM HEPES, 150 mM NaCl, 3 mM EDTA, 0.05% P20)
5. Temperature: 25°C
6. Contact time: 120 s, dissociation: 300 s

Required Output:
- Sensorgrams for each concentration
- Kinetic fit (1:1 Langmuir model)
- KD (dissociation constant) with 95% CI
- ka (association rate) and kd (dissociation rate)

Success Criterion:
- KD < 1 μM: Proceed to functional assays
- KD 1-10 μM: Consider optimization
- KD > 10 μM: Binding insufficient

================================================================================
SECTION 5: FUNCTIONAL ASSAY (target system-SPECIFIC)
================================================================================

Target target system:       [SPECIFY]
Assay Type:           [SPECIFY BASED ON TARGET]

Example Assays by Target:
- Alzheimer's/Parkinson's: Thioflavin T (ThT) aggregation assay
- Obesity (GLP-1R): cAMP accumulation assay in CHO-GLP1R cells
- Superbugs (MBL): Nitrocefin cleavage assay
- Cancer (PD-L1): PD-1/PD-L1 binding competition ELISA

================================================================================
SECTION 6: TIMELINE AND PRICING
================================================================================

Phase                          Est. Time        Est. Cost (USD)
--------------------------------------------------------------
Peptide Synthesis              2-3 weeks        $500-1,500
QC (HPLC + MS)                 Included         Included
Salt Exchange                  +2 days          +$100
SPR Binding Assay              1-2 weeks        $2,000-5,000
Functional Assay               2-4 weeks        $3,000-10,000
--------------------------------------------------------------
TOTAL ESTIMATE                 4-8 weeks        $5,000-15,000

================================================================================
SECTION 7: SHIPPING AND HANDLING
================================================================================

Shipping:             On dry ice (peptide) / 4°C (protein)
Documentation:        CoA, MSDS, customs declaration
Insurance:            Required for international shipping

================================================================================
SECTION 8: LEGAL AND IP
================================================================================

Confidentiality:      Standard NDA required
IP Ownership:         All IP remains with Principal Investigator
Data Ownership:       All raw data to be provided
Publication Rights:   PI retains publication rights

================================================================================
AUTHORIZED SIGNATURES
================================================================================

Principal Investigator: _________________________  Date: ____________

CRO Representative:     _________________________  Date: ____________

================================================================================
END OF STATEMENT OF WORK
================================================================================
"""

    return sow_text


def save_sow_files(
    peptide_id: str,
    sow_text: str,
    properties: Dict,
    output_dir: Path,
) -> Dict:
    """
    Save SOW to text file (and optionally PDF if reportlab available).
    """
    # Save as text
    txt_file = output_dir / f"SOW_{peptide_id}.txt"
    with open(txt_file, 'w') as f:
        f.write(sow_text)

    print(f"    Saved: {txt_file}")

    # Try to generate PDF
    pdf_file = output_dir / f"SOW_{peptide_id}.pdf"
    pdf_generated = False

    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import inch

        c = canvas.Canvas(str(pdf_file), pagesize=letter)
        width, height = letter

        # Simple text rendering
        y = height - inch
        for line in sow_text.split('\n'):
            if y < inch:
                c.showPage()
                y = height - inch
            c.setFont("Courier", 8)
            c.drawString(0.5 * inch, y, line[:100])  # Truncate long lines
            y -= 10

        c.save()
        pdf_generated = True
        print(f"    PDF:   {pdf_file}")

    except ImportError:
        print("    (reportlab not available - PDF not generated)")

    return {
        'txt_file': str(txt_file),
        'pdf_file': str(pdf_file) if pdf_generated else None,
        'pdf_generated': pdf_generated,
    }


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Generate SOW documents for approved peptides."""

    # Peptides that passed validation (example list)
    approved_peptides = {
        "ZIM-ALZ-005": {
            "sequence": "FPF",
            "n_cap": "ACE",
            "c_cap": "NME",
            "target_protein": "Alpha-synuclein",
            "indication": "Parkinson's target system / Alzheimer's target system",
        },
        "ZIM-GLP2-006": {
            "sequence": "HGPGAGPG",
            "n_cap": None,
            "c_cap": None,
            "target_protein": "GLP-1 Receptor",
            "indication": "Type 2 Diabetes / Obesity",
            "cyclic": True,
        },
        "ZIM-ADD-003": {
            "sequence": "RWWFWR",
            "n_cap": None,
            "c_cap": None,
            "target_protein": "α3β4 nAChR",
            "indication": "Opioid Addiction",
        },
    }

    results = {
        'timestamp': datetime.now().isoformat(),
        'peptides': {},
    }

    print(f"Generating SOW documents for {len(approved_peptides)} approved peptides...\n")

    for peptide_id, peptide_info in approved_peptides.items():
        print(f"\n{'=' * 60}")
        print(f"Processing: {peptide_id}")
        print(f"  Sequence: {peptide_info['sequence']}")
        print(f"  Target: {peptide_info['target_protein']}")
        print(f"  Indication: {peptide_info['indication']}")
        print(f"{'=' * 60}")

        # Calculate properties
        properties = calculate_peptide_properties(
            peptide_info['sequence'],
            peptide_info.get('n_cap'),
            peptide_info.get('c_cap'),
        )

        print(f"\n  Calculated Properties:")
        print(f"    MW: {properties['molecular_weight_Da']:.2f} Da")
        print(f"    pI: {properties['pI_estimate']:.1f}")
        print(f"    GRAVY: {properties['gravy']:.2f}")

        # Generate SOW
        sow_text = generate_sow_text(
            peptide_id,
            peptide_info['sequence'],
            peptide_info['target_protein'],
            properties,
            peptide_info.get('n_cap'),
            peptide_info.get('c_cap'),
        )

        # Save files
        file_info = save_sow_files(peptide_id, sow_text, properties, OUTPUT_DIR)

        results['peptides'][peptide_id] = {
            'peptide_info': peptide_info,
            'properties': properties,
            'files': file_info,
        }

    # Summary
    print("\n" + "=" * 80)
    print("SOW GENERATION COMPLETE")
    print("=" * 80)
    print(f"\n  Generated {len(approved_peptides)} Statement of Work documents")
    print(f"  Output directory: {OUTPUT_DIR}")
    print("\n  Next Steps:")
    print("    1. Fill in PI information in each SOW")
    print("    2. Contact CROs (GenScript, WuXi AppTec, Bachem)")
    print("    3. Request quotes based on specifications")
    print("    4. Sign NDA and submit order")

    # Save results
    output_json = OUTPUT_DIR / "sow_generation_results.json"
    with open(output_json, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n  Results saved: {output_json}")

    return results


if __name__ == "__main__":
    results = main()
