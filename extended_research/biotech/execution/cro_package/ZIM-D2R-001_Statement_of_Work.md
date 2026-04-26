# Statement of Work
## Peptide Synthesis and Binding Characterization

---

## LEGAL DISCLAIMER

**This peptide is based on THEORETICAL COMPUTATIONAL RESEARCH only.**

- Computational predictions are NOT experimentally validated
- Binding affinity estimates are heuristic, NOT measured
- This work has NOT been peer reviewed
- No therapeutic claims are made

The purpose of this synthesis is EXPERIMENTAL VALIDATION of computational predictions.

---

**Project Title:** D2R Agonist Peptide for Prolactinoma Treatment

**Document Version:** 1.0

**Date:** April 20, 2026

**Sponsor:** Carl Zimmerman

**Contact:** [INSERT EMAIL]

---

## 1. Executive Summary

This Statement of Work (SOW) requests the synthesis and biophysical characterization of a novel cyclic peptide designed as a selective agonist for the human Dopamine D2 Receptor (D2R). The peptide is intended for the treatment of prolactinoma, a pituitary tumor that causes hyperprolactinemia.

The candidate peptide, designated **ZIM-D2R-001**, was designed using computational methods including structure-based design, molecular docking, and free energy perturbation calculations. Computational predictions indicate high-affinity binding (Kd ~ 1 nM) with selectivity over the 5-HT2B serotonin receptor (cardiac safety).

---

## 2. Peptide Specifications

### 2.1 Sequence and Structure

| Property | Value |
|----------|-------|
| **Designation** | ZIM-D2R-001 |
| **Sequence** | `CKAFWTTWVISAQC` |
| **Length** | 14 amino acids |
| **Estimated MW** | ~1624.9 Da |
| **Net Charge** | +1 at pH 7.4 |
| **Cyclization** | Disulfide bond (Cys1-Cys14) |
| **N-terminus** | Free amine (H₂N-) |
| **C-terminus** | Free acid (-COOH) |

### 2.2 FASTA Format

```
>ZIM-D2R-001|D2R_Agonist|Cyclic_Disulfide|Prolactinoma
CKAFWTTWVISAQC
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

- Asp114 salt bridge engagement (positively charged lysine)
- Aromatic stacking with Phe389/Phe390 (Trp-Trp motif)
- Ser193 hydrogen bond formation
- 5-HT2B steric clash (selectivity feature)
- Ile/Met218 hydrophobic pocket engagement
- Cyclic disulfide constraint for conformational stability

---

## 3. Synthesis Requirements

### 3.1 Quantity and Purity

| Requirement | Specification |
|-------------|---------------|
| **Quantity** | 5 mg |
| **Purity** | >95% by HPLC |
| **Purity Method** | Reverse-phase HPLC (C18 column) |
| **Mass Confirmation** | ESI-MS or MALDI-TOF confirmation |

### 3.2 Cyclization Protocol

1. fabricate sequence linear peptide via Fmoc solid-phase peptide synthesis (SPPS)
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
| **Technology** | Surface Plasmon Resonance (Biacore T200 or equivalent) |
| **Target Protein** | Human D2R extracellular domain or full receptor in nanodiscs |
| **Target Source** | Recombinant (HEK293 or insect cell expression) |
| **Immobilization** | Amine coupling or His-tag capture |
| **Running Buffer** | HBS-EP+ (10 mM HEPES pH 7.4, 150 mM NaCl, 3 mM EDTA, 0.05% P20) |
| **Concentration Range** | 0.1 nM to 1 μM (8-point dilution series) |
| **Replicates** | Triplicate |
| **Kinetic Model** | 1:1 Langmuir binding model |
| **Positive Control** | Dopamine (DA) or Quinpirole |
| **Negative Control** | Buffer only |

### 4.2 Required Outputs

1. **Association rate constant (ka)** in M⁻¹s⁻¹
2. **Dissociation rate constant (kd)** in s⁻¹
3. **Equilibrium dissociation constant (KD)** in nM
4. **Sensorgram plots** (raw and fitted)
5. **Binding curve** (response vs concentration)

### 4.3 Computational Predictions (for comparison)

| Parameter | Predicted Value |
|-----------|-----------------|
| **ΔG_bind** | -51.1 ± 2.5 kJ/mol |
| **Predicted KD** | 1.24 nM |
| **Affinity Class** | HIGH (low nM) |

---

## 5. Selectivity Panel (Optional but Recommended)

### 5.1 Required Targets

| Target | Expected Result | Rationale |
|--------|-----------------|-----------|
| **D2R** | High affinity binding | Primary target |
| **D3R** | Moderate binding acceptable | Related receptor |
| **5-HT2B** | NO binding required | Cardiac safety (fenfluramine-like toxicity) |

### 5.2 Optional Targets

- D1R
- D4R
- D5R
- 5-HT2A
- 5-HT2C
- Alpha-1 adrenergic
- Alpha-2 adrenergic
- H1 histamine

---

## 6. Deliverables and Timeline

### 6.1 Deliverables

| Item | Description |
|------|-------------|
| fabricate sequence peptide | 5 mg lyophilized powder |
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

**Prior Art Established:** This peptide sequence was published as prior art on **2026-04-20** under the **AGPL-3.0-or-later** license.

**SHA-256 Hash:** `5b16bedf3e282643068c28fa68dccc605c9ca4b3c2cce98752815ec7f44993ae`

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
