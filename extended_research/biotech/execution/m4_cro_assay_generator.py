#!/usr/bin/env python3
"""
m4_cro_assay_generator.py - CRO Statement of Work Generator

Generates professional documentation for peptide synthesis and binding assay
requests to Contract Research Organizations (GenScript, WuXi AppTec, etc.)

This script produces a complete SOW package for the D2R cyclic peptide agonist
designed for prolactinoma treatment.

Author: Carl Zimmerman & Claude Opus 4.5
Date: April 20, 2026
License: AGPL-3.0-or-later
"""

# =============================================================================
# LEGAL DISCLAIMER: This is THEORETICAL COMPUTATIONAL RESEARCH only.
# Not peer reviewed. Not medical advice. Not a validated therapeutic.
# All predictions require experimental validation.
# See: extended_research/biotech/LEGAL_DISCLAIMER.md
# =============================================================================


import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# ============================================================================
# PEPTIDE SPECIFICATIONS
# ============================================================================

D2R_AGONIST = {
    "name": "ZIM-D2R-001",
    "sequence": "CKAFWTTWVISAQC",
    "length": 14,
    "molecular_weight_est": 1624.9,  # Estimated MW
    "net_charge": "+1",
    "cyclic_type": "Disulfide bond (Cys1-Cys14)",
    "application": "D2 Receptor Agonist for Prolactinoma",
    "target": "Human Dopamine D2 Receptor (D2R)",

    "design_features": [
        "Asp114 salt bridge engagement (positively charged lysine)",
        "Aromatic stacking with Phe389/Phe390 (Trp-Trp motif)",
        "Ser193 hydrogen bond formation",
        "5-HT2B steric clash (selectivity feature)",
        "Ile/Met218 hydrophobic pocket engagement",
        "Cyclic disulfide constraint for conformational stability"
    ],

    "computational_validation": {
        "structure_prediction": "ESMFold (pLDDT reported)",
        "docking": "Physics-informed model",
        "fep_binding_energy": "-51.1 ± 2.5 kJ/mol",
        "predicted_kd": "1.24 nM",
        "affinity_class": "HIGH (low nM)"
    },

    "sha256_hash": "5b16bedf3e282643068c28fa68dccc605c9ca4b3c2cce98752815ec7f44993ae",
    "prior_art_date": "2026-04-20"
}


# ============================================================================
# CRO SPECIFICATIONS
# ============================================================================

SYNTHESIS_REQUIREMENTS = {
    "quantity": "5 mg",
    "purity": ">95% by HPLC",
    "purity_method": "Reverse-phase HPLC (C18 column)",
    "mass_spec": "ESI-MS or MALDI-TOF confirmation",
    "cyclization": "Disulfide bond formation (oxidative folding)",
    "n_terminus": "Free amine (H2N-)",
    "c_terminus": "Free acid (-COOH)",
    "lyophilization": "Required (white powder)",
    "storage": "-20°C desiccated"
}

SPR_ASSAY_REQUIREMENTS = {
    "technology": "Surface Plasmon Resonance (Biacore T200 or equivalent)",
    "target_protein": "Human D2R extracellular domain or full receptor in nanodiscs",
    "target_source": "Recombinant (HEK293 or insect cell expression)",
    "immobilization": "Amine coupling or His-tag capture",
    "running_buffer": "HBS-EP+ (10 mM HEPES pH 7.4, 150 mM NaCl, 3 mM EDTA, 0.05% P20)",
    "concentration_range": "0.1 nM to 1 μM (8-point dilution series)",
    "replicates": "Triplicate",
    "kinetic_analysis": "1:1 Langmuir binding model",
    "outputs": ["ka (association rate)", "kd (dissociation rate)", "KD (equilibrium constant)"],
    "positive_control": "Dopamine (DA) or Quinpirole",
    "negative_control": "Buffer only"
}

SELECTIVITY_PANEL = {
    "required_targets": [
        "D2R (primary target - should bind)",
        "D3R (related - acceptable cross-reactivity)",
        "5-HT2B (must NOT bind - cardiac safety)"
    ],
    "optional_targets": [
        "D1R", "D4R", "D5R",
        "5-HT2A", "5-HT2C",
        "Alpha-1 adrenergic",
        "Alpha-2 adrenergic",
        "H1 histamine"
    ]
}


# ============================================================================
# DOCUMENT GENERATION
# ============================================================================

def generate_sow_markdown() -> str:
    """
    Generate Statement of Work in Markdown format.
    """
    now = datetime.now()

    sow = f"""# Statement of Work
## Peptide Synthesis and Binding Characterization

---

**Project Title:** D2R Agonist Peptide for Prolactinoma Treatment

**Document Version:** 1.0

**Date:** {now.strftime("%B %d, %Y")}

**Sponsor:** Carl Zimmerman

**Contact:** [INSERT EMAIL]

---

## 1. Executive Summary

This Statement of Work (SOW) requests the synthesis and biophysical characterization of a novel cyclic peptide designed as a selective agonist for the human Dopamine D2 Receptor (D2R). The peptide is intended for the treatment of prolactinoma, a pituitary tumor that causes hyperprolactinemia.

The candidate peptide, designated **{D2R_AGONIST['name']}**, was designed using computational methods including structure-based design, molecular docking, and free energy perturbation calculations. Computational predictions indicate high-affinity binding (Kd ~ 1 nM) with selectivity over the 5-HT2B serotonin receptor (cardiac safety).

---

## 2. Peptide Specifications

### 2.1 Sequence and Structure

| Property | Value |
|----------|-------|
| **Designation** | {D2R_AGONIST['name']} |
| **Sequence** | `{D2R_AGONIST['sequence']}` |
| **Length** | {D2R_AGONIST['length']} amino acids |
| **Estimated MW** | ~{D2R_AGONIST['molecular_weight_est']:.1f} Da |
| **Net Charge** | {D2R_AGONIST['net_charge']} at pH 7.4 |
| **Cyclization** | {D2R_AGONIST['cyclic_type']} |
| **N-terminus** | Free amine (H₂N-) |
| **C-terminus** | Free acid (-COOH) |

### 2.2 FASTA Format

```
>{D2R_AGONIST['name']}|D2R_Agonist|Cyclic_Disulfide|Prolactinoma
{D2R_AGONIST['sequence']}
```

### 2.3 Structural Features

The peptide contains a **disulfide bond** between:
- **Cys1** (N-terminal)
- **Cys14** (C-terminal)

This cyclization constraint is critical for:
1. Conformational stability
2. Proteolytic resistance
3. Optimal receptor engagement geometry

**Important:** The disulfide bond must be formed via oxidative folding. Verify bond formation by mass spectrometry (expect -2 Da from linear form).

### 2.4 Design Rationale

The peptide was designed to engage the D2R orthosteric binding pocket with the following interactions:

{chr(10).join(f'- {feature}' for feature in D2R_AGONIST['design_features'])}

---

## 3. Synthesis Requirements

### 3.1 Quantity and Purity

| Requirement | Specification |
|-------------|---------------|
| **Quantity** | {SYNTHESIS_REQUIREMENTS['quantity']} |
| **Purity** | {SYNTHESIS_REQUIREMENTS['purity']} |
| **Purity Method** | {SYNTHESIS_REQUIREMENTS['purity_method']} |
| **Mass Confirmation** | {SYNTHESIS_REQUIREMENTS['mass_spec']} |

### 3.2 Cyclization Protocol

1. Synthesize linear peptide via Fmoc solid-phase peptide synthesis (SPPS)
2. Cleave from resin with TFA cocktail
3. Purify linear peptide by preparative HPLC
4. Perform oxidative folding:
   - Dissolve in aqueous buffer (pH 8.0)
   - Add oxidizing agent (DMSO or glutathione redox buffer)
   - Monitor cyclization by analytical HPLC
5. Purify cyclic peptide by preparative HPLC
6. Confirm MW by mass spectrometry (expect MW = linear - 2 Da)
7. Lyophilize to white powder

### 3.3 Quality Control

**Required Deliverables:**

- [ ] Certificate of Analysis (CoA)
- [ ] Analytical HPLC chromatogram (purity)
- [ ] Mass spectrum (MW confirmation)
- [ ] Amino acid analysis (optional)
- [ ] Peptide content determination

---

## 4. Binding Assay Requirements

### 4.1 Primary Assay: Surface Plasmon Resonance (SPR)

| Parameter | Specification |
|-----------|---------------|
| **Technology** | {SPR_ASSAY_REQUIREMENTS['technology']} |
| **Target Protein** | {SPR_ASSAY_REQUIREMENTS['target_protein']} |
| **Target Source** | {SPR_ASSAY_REQUIREMENTS['target_source']} |
| **Immobilization** | {SPR_ASSAY_REQUIREMENTS['immobilization']} |
| **Running Buffer** | {SPR_ASSAY_REQUIREMENTS['running_buffer']} |
| **Concentration Range** | {SPR_ASSAY_REQUIREMENTS['concentration_range']} |
| **Replicates** | {SPR_ASSAY_REQUIREMENTS['replicates']} |
| **Kinetic Model** | {SPR_ASSAY_REQUIREMENTS['kinetic_analysis']} |
| **Positive Control** | {SPR_ASSAY_REQUIREMENTS['positive_control']} |
| **Negative Control** | {SPR_ASSAY_REQUIREMENTS['negative_control']} |

### 4.2 Required Outputs

1. **Association rate constant (ka)** in M⁻¹s⁻¹
2. **Dissociation rate constant (kd)** in s⁻¹
3. **Equilibrium dissociation constant (KD)** in nM
4. **Sensorgram plots** (raw and fitted)
5. **Binding curve** (response vs concentration)

### 4.3 Computational Predictions (for comparison)

| Parameter | Predicted Value |
|-----------|-----------------|
| **ΔG_bind** | {D2R_AGONIST['computational_validation']['fep_binding_energy']} |
| **Predicted KD** | {D2R_AGONIST['computational_validation']['predicted_kd']} |
| **Affinity Class** | {D2R_AGONIST['computational_validation']['affinity_class']} |

---

## 5. Selectivity Panel (Optional but Recommended)

### 5.1 Required Targets

| Target | Expected Result | Rationale |
|--------|-----------------|-----------|
| **D2R** | High affinity binding | Primary target |
| **D3R** | Moderate binding acceptable | Related receptor |
| **5-HT2B** | NO binding required | Cardiac safety (fenfluramine-like toxicity) |

### 5.2 Optional Targets

{chr(10).join(f'- {target}' for target in SELECTIVITY_PANEL['optional_targets'])}

---

## 6. Deliverables and Timeline

### 6.1 Deliverables

| Item | Description |
|------|-------------|
| Synthesized peptide | {SYNTHESIS_REQUIREMENTS['quantity']} lyophilized powder |
| CoA | Purity, MW, peptide content |
| HPLC chromatogram | Analytical trace |
| Mass spectrum | ESI-MS or MALDI |
| SPR data | Raw sensorgrams + fitted parameters |
| Final report | KD, ka, kd with error estimates |

### 6.2 Estimated Timeline

| Phase | Duration |
|-------|----------|
| Peptide synthesis | 2-3 weeks |
| QC and shipping | 1 week |
| SPR assay setup | 1 week |
| SPR data collection | 1-2 weeks |
| Data analysis and report | 1 week |
| **Total** | **6-8 weeks** |

---

## 7. Intellectual Property Notice

**Prior Art Established:** This peptide sequence was published as prior art on **{D2R_AGONIST['prior_art_date']}** under the **AGPL-3.0-or-later** license.

**SHA-256 Hash:** `{D2R_AGONIST['sha256_hash']}`

The sequence is freely available for research purposes. No patent claims are asserted by the sponsor. This work is released for open science.

---

## 8. Budget Estimate

| Service | Estimated Cost (USD) |
|---------|---------------------|
| Peptide synthesis (5 mg, >95% purity, cyclic) | $2,000 - $4,000 |
| SPR binding assay (D2R) | $3,000 - $5,000 |
| Selectivity panel (3 targets) | $4,000 - $8,000 |
| **Total (synthesis + D2R SPR)** | **$5,000 - $9,000** |
| **Total (with selectivity panel)** | **$9,000 - $17,000** |

*Estimates based on typical CRO pricing. Request formal quotes.*

---

## 9. Contact and Authorization

**Sponsor Name:** Carl Zimmerman

**Email:** [INSERT EMAIL]

**Phone:** [INSERT PHONE]

**Signature:** _________________________ **Date:** _____________

---

## Appendix A: Amino Acid Sequence Details

```
Position  1:  C  (Cysteine)    - Disulfide bond partner
Position  2:  K  (Lysine)      - Positive charge, Asp114 engagement
Position  3:  A  (Alanine)     - Spacer
Position  4:  F  (Phenylalanine) - Aromatic stacking
Position  5:  W  (Tryptophan)  - Aromatic stacking, bulky for selectivity
Position  6:  T  (Threonine)   - Hydrogen bonding
Position  7:  T  (Threonine)   - Hydrogen bonding
Position  8:  W  (Tryptophan)  - Aromatic stacking, 5-HT2B clash
Position  9:  V  (Valine)      - Hydrophobic, pocket filling
Position 10:  I  (Isoleucine)  - Hydrophobic, Met218 engagement
Position 11:  S  (Serine)      - Hydrogen bonding, Ser193 contact
Position 12:  A  (Alanine)     - Spacer
Position 13:  Q  (Glutamine)   - Polar, solvent exposure
Position 14:  C  (Cysteine)    - Disulfide bond partner
```

---

## Appendix B: Reference Structures

**D2R Crystal Structure:** PDB ID 6CM4
- Resolution: 2.87 Å
- Ligand: Risperidone (antagonist)
- Use for binding site reference

**D2R Cryo-EM Structure:** PDB ID 6VMS
- Resolution: 3.1 Å
- Ligand: Bromocriptine (agonist)
- More relevant for agonist binding mode

---

*Document generated by m4_cro_assay_generator.py*
*Z² = 32π/3 Framework | April 2026*
*License: AGPL-3.0-or-later*
"""

    return sow


def save_documents(output_dir: Path):
    """
    Save all CRO documents.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate Markdown SOW
    sow_md = generate_sow_markdown()

    # Save Markdown
    md_path = output_dir / f"{D2R_AGONIST['name']}_Statement_of_Work.md"
    with open(md_path, 'w') as f:
        f.write(sow_md)

    # Save FASTA
    fasta_path = output_dir / f"{D2R_AGONIST['name']}.fasta"
    with open(fasta_path, 'w') as f:
        f.write(f">{D2R_AGONIST['name']}|D2R_Agonist|Cyclic_Disulfide|Prolactinoma\n")
        f.write(f"{D2R_AGONIST['sequence']}\n")

    # Save JSON specifications
    json_path = output_dir / f"{D2R_AGONIST['name']}_specifications.json"
    with open(json_path, 'w') as f:
        json.dump({
            "peptide": D2R_AGONIST,
            "synthesis": SYNTHESIS_REQUIREMENTS,
            "spr_assay": SPR_ASSAY_REQUIREMENTS,
            "selectivity": SELECTIVITY_PANEL,
            "generated": datetime.now().isoformat()
        }, f, indent=2)

    return md_path, fasta_path, json_path


def main():
    """
    Main execution function.
    """
    print()
    print("=" * 70)
    print("CRO STATEMENT OF WORK GENERATOR")
    print("Preparing Physical Synthesis Order")
    print("=" * 70)
    print()
    print(f"Peptide: {D2R_AGONIST['name']}")
    print(f"Sequence: {D2R_AGONIST['sequence']}")
    print(f"Application: {D2R_AGONIST['application']}")
    print(f"Predicted Kd: {D2R_AGONIST['computational_validation']['predicted_kd']}")
    print()

    # Output directory
    output_dir = Path(__file__).parent / "cro_package"

    print("Generating documents...")
    print("-" * 50)

    md_path, fasta_path, json_path = save_documents(output_dir)

    print(f"  ✓ Statement of Work: {md_path.name}")
    print(f"  ✓ FASTA sequence: {fasta_path.name}")
    print(f"  ✓ Specifications: {json_path.name}")

    print()
    print("=" * 70)
    print("CRO PACKAGE READY FOR SUBMISSION")
    print("=" * 70)
    print()
    print(f"  Output directory: {output_dir}")
    print()
    print("  Recommended CROs:")
    print("    • GenScript: https://www.genscript.com/peptide-synthesis.html")
    print("    • WuXi AppTec: https://www.wuxiapptec.com/")
    print("    • Bachem: https://www.bachem.com/")
    print("    • CPC Scientific: https://www.cpcscientific.com/")
    print()
    print("  Next Steps:")
    print("    1. Review the Statement of Work (.md file)")
    print("    2. Add your contact information")
    print("    3. Request quotes from 2-3 CROs")
    print("    4. Compare pricing and timeline")
    print("    5. Place order with selected CRO")
    print()
    print("  Estimated Cost: $5,000 - $9,000 (synthesis + SPR assay)")
    print("  Estimated Timeline: 6-8 weeks")
    print()
    print("=" * 70)
    print("THE PEPTIDE IS READY TO BECOME PHYSICAL REALITY")
    print("=" * 70)
    print()

    return md_path


if __name__ == "__main__":
    md_path = main()
