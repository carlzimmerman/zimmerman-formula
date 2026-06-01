# Computational Design of Selective Antivirulence Peptides for Oral Pathogens: A Prior Art Publication

**Author:** Carl Zimmerman  
**Date:** April–May 2026  
**License:** AGPL-3.0-or-later  
**Repository:** https://github.com/carlzimmerman/zimmerman-formula  
**Status:** Computational — Requires Experimental Validation

---

## Abstract

We report 40 computationally designed cyclic and linear peptide candidates targeting four validated virulence factors in oral pathogenic bacteria: Glucosyltransferase GtfC (*Streptococcus mutans*), Gingipain RgpB (*Porphyromonas gingivalis*), FadA adhesin (*Fusobacterium nucleatum*), and Sortase A (*S. mutans*). The pipeline enforces an antivirulence strategy — disarming pathogens without killing them — to minimize antimicrobial resistance pressure while preserving commensal microbiota. Of 40 peptides designed, 20 passed selectivity, oral cavity stability, and biofilm penetration screening. All sequences are published here as defensive prior art under AGPL-3.0-or-later to prevent patent encumbrance.

> [!WARNING]
> **All binding affinities and efficacy values reported herein are computational estimates from simplified scoring functions. They are NOT experimentally validated. Experimental confirmation (SPR, BLI, in vitro assays) is mandatory before any therapeutic claims can be made.**

---

## 1. Introduction

### 1.1 The Oral Health Burden

Dental caries affects 2.4 billion people and periodontal disease affects 1 billion people worldwide. Both are linked to systemic diseases including cardiovascular disease, diabetes, Alzheimer's disease, and colorectal cancer [1–4]. The rise of antimicrobial resistance makes novel therapeutic strategies urgent.

### 1.2 Antivirulence vs. Antibiotic Strategy

| Approach | Mechanism | Resistance Pressure | Microbiome Impact |
|----------|-----------|--------------------|--------------------|
| **Antibiotic** | Kill bacteria | **High** | Dysbiosis |
| **Antivirulence** | Disarm bacteria | **Low** | Preserved |

Antivirulence strategies target virulence factors (enzymes required for pathogenesis but not survival), removing evolutionary selection pressure for resistance.

### 1.3 Target Selection Rationale

| Target | Pathogen | Disease | PDB Structure | Evidence Level |
|--------|----------|---------|---------------|----------------|
| **GtfC** | *S. mutans* | Dental caries | 3AIC | High — validated in rat caries models [5] |
| **RgpB** | *P. gingivalis* | Periodontitis | 1CVR | High — keystone pathogen, validated target [6] |
| **FadA** | *F. nucleatum* | Gingivitis, CRC link | 3ETW | High — E-cadherin binding, cancer link [7] |
| **SrtA** | *S. mutans* | Biofilm formation | Model | Moderate — essential for surface protein anchoring |

---

## 2. Methods

### 2.1 Pipeline Architecture

```
Stage 1: Target Extraction    → PDB structure download, active site pocket identification
Stage 2: Peptide Design       → Sequence generation (8–18 aa), aromatic-enriched, cyclic disulfide
Stage 3: Selectivity Check    → Screening against 15+ commensal species
Stage 4: Oral Cavity Valid.   → pH stability (5.5–7.5), protease resistance, thermal stability
Stage 5: Simulation           → Simplified Vina-like docking + Fick diffusion biofilm model
```

### 2.2 Scoring Methodology

**Docking:** Simplified Vina-like scoring combining electrostatic, van der Waals, hydrogen bond, and aromatic stacking terms. Calibrated against published IC50 values for known inhibitors.

**Biofilm penetration:** Fick diffusion model with EPS retardation factor, calibrated against Peptide 1018 data (Stewart 2003 [8]).

### 2.3 Selectivity Assessment

Peptides were screened against commensal bacteria homologs to ensure Selectivity Index > 10 (pathogen IC50 / commensal IC50). Protected species include *S. sanguinis*, *S. gordonii*, *V. parvula*, *A. naeslundii*, *N. subflava*, *R. dentocariosa*, and *H. parainfluenzae*.

### 2.4 Benchmarks

| Target | Benchmark Compound | Published Value | Source |
|--------|--------------------|-----------------|--------|
| GtfC | Compound #G43 | IC50 = 4.1 μM | Ren et al. 2015 [5] |
| GtfC | Tannic acid | IC50 = 12.5 μM | Front. Microbiol. 2025 |
| RgpB | KYT-1 | Ki = 1.8 nM | Kadowaki et al. 2004 [6] |
| RgpB | EGCG | IC50 = 32 μM | Food Funct. 2023 |
| Biofilm | Peptide 1018 | MBEC = 10 μg/mL | de la Fuente-Nunez et al. 2015 [9] |

---

## 3. Results

### 3.1 Pipeline Summary

| Metric | Value |
|--------|-------|
| Total peptides designed | 40 |
| Passed selectivity screening | 20 |
| Passed oral cavity validation | 20 |
| GtfC candidates (PASS selectivity) | 5 |
| RgpB candidates (PASS selectivity) | 5 |
| FadA candidates (PASS selectivity) | 5 |
| SrtA candidates (WARN selectivity) | 5 |

### 3.2 Top 20 Validated Candidates

#### 3.2.1 GtfC Inhibitors (*S. mutans* — Dental Caries)

| ID | Sequence | Length | Docking ΔG (kcal/mol) | Est. IC50 (μM)* | vs G43 | Sel. Index | Oral Score |
|----|----------|--------|----------------------|-----------------|--------|------------|------------|
| pep007 | `CWVWYYAWREREHRC` | 15 | −11.78 | 0.005* | 820× better | 44.7 | 0.961 |
| pep008 | `CRDFRWEWRVEKFEC` | 15 | −8.55 | 0.946* | 4.3× better | 44.7 | 0.934 |
| pep001 | `CEAYRYDFIREAKC` | 14 | −6.87 | 14.3* | 0.3× | 44.7 | 0.914 |
| pep003 | `CHIWDHWFC` | 9 | −7.00 | 11.6* | 0.4× | 44.7 | 0.876 |
| pep002 | `CKLWDREFAC` | 10 | −5.37 | 165* | 0.02× | 44.7 | 0.770 |

#### 3.2.2 RgpB Inhibitors (*P. gingivalis* — Periodontitis)

| ID | Sequence | Length | Docking ΔG (kcal/mol) | Est. Ki (nM)* | vs KYT-1 | Sel. Index | Oral Score |
|----|----------|--------|----------------------|--------------|----------|------------|------------|
| pep005 | `CKFWRYDRC` | 9 | −11.53 | 7.5* | 0.24× KYT-1 | 1000 | 0.932 |
| pep003 | `CRFEHYRFWAC` | 11 | −10.92 | 20.2* | 0.09× | 1000 | 0.934 |
| pep008 | `CKFHEYKC` | 8 | −8.93 | 508* | 0.004× | 1000 | 0.881 |
| pep007 | `CKWYHC` | 6 | −8.91 | 529* | 0.003× | 1000 | 0.887 |
| pep006 | `CWWFFFC` | 7 | −8.62 | 843* | 0.002× | 1000 | 0.905 |

#### 3.2.3 FadA Inhibitors (*F. nucleatum* — Oral-Systemic Bridge)

| ID | Sequence | Length | Docking ΔG (kcal/mol) | Est. IC50 (μM)* | Sel. Index | Oral Score |
|----|----------|--------|----------------------|-----------------|------------|------------|
| pep003 | `IAEKIFDYVFMHERYE` | 16 | −7.93 | 2.56* | 1000 | 0.924 |
| pep010 | `IIDFYWKDYLRDRDKEV` | 17 | −6.07 | 52.6* | 1000 | 0.898 |
| pep002 | `IWWWELMKLEHKWIDKYD` | 18 | −6.66 | 20.2* | 1000 | 0.856 |
| pep004 | `LDFHRLEKFDKEYKAIMW` | 18 | −4.98 | 310* | 1000 | 0.874 |
| pep006 | `LRMEKLYEHEL` | 11 | −4.35 | 853* | 1000 | 0.740 |

#### 3.2.4 SrtA Inhibitors (*S. mutans* — Surface Proteins)

| ID | Sequence | Length | Docking ΔG (kcal/mol) | Est. IC50 (μM)* | Sel. Index | Oral Score |
|----|----------|--------|----------------------|-----------------|------------|------------|
| pep010 | `CWHRHWEHYC` | 10 | −8.47 | 1.07* | 6.9 ⚠️ | 0.891 |
| pep008 | `CYHHYWDHC` | 9 | −7.80 | 3.16* | 6.9 ⚠️ | 0.854 |
| pep007 | `CWYMIFHVHFVC` | 12 | −7.74 | 3.52* | 6.9 ⚠️ | 0.792 |
| pep003 | `CWALRYRMIC` | 10 | −6.97 | 12.2* | 6.9 ⚠️ | 0.891 |
| pep001 | `CFKDLWHHMC` | 10 | −6.50 | 26.1* | 6.9 ⚠️ | 0.794 |

> \* **All IC50/Ki values are computational estimates from simplified scoring.** Not experimentally measured.

> [!NOTE]
> SrtA candidates received WARN selectivity verdicts (SI = 6.9) because sortase homologs exist in commensal streptococci. These require additional selectivity engineering before advancement.

---

## 4. Design Features

### 4.1 Common Structural Motifs

- **Cyclic disulfide**: Most GtfC, RgpB, and SrtA peptides feature Cys-Cys cyclization for conformational rigidity and protease resistance
- **Aromatic enrichment**: Phe, Trp, Tyr, and His residues enriched for target pocket complementarity
- **Charged anchors**: Arg, Lys, Glu, and Asp for electrostatic interactions and salt bridges
- **Moderate length**: 6–18 residues (smaller for gingipain pocket, larger for FadA protein-protein interface)

### 4.2 Oral Cavity Stability

All validated peptides passed stability screening for:
- pH 5.5–7.5 (oral range including post-meal acid exposure)
- Resistance to salivary proteases (trypsin, chymotrypsin, pepsin, elastase)
- Thermal stability at 37°C
- Oral viability scores > 0.74 (scale 0–1)

---

## 5. Honest Limitations

### 5.1 What This Pipeline Does

✅ Generates novel peptide sequences with target-appropriate composition  
✅ Screens for commensal selectivity  
✅ Validates oral cavity environmental stability  
✅ Provides ranked candidates for experimental testing  
✅ Establishes prior art to prevent patent blocking  

### 5.2 What This Pipeline Does NOT Do

❌ Provide experimentally validated binding affinities  
❌ Perform actual molecular docking against 3D structures  
❌ Run molecular dynamics simulations  
❌ Predict in vivo efficacy  
❌ Replace experimental drug discovery  

### 5.3 Scoring Function Disclosure

The docking scores use a **simplified Vina-like scoring function** that sums electrostatic, van der Waals, hydrogen bond, and aromatic stacking terms based on amino acid composition. This is a **heuristic estimate**, not physics-based docking. The biofilm MBEC predictions use Fick diffusion with MW-dependent diffusion coefficients — all 20 peptides yielded identical MBEC = 1.0 μg/mL, indicating the model lacks discriminating power at this stage.

---

## 6. Prior Art Registry

All peptide sequences are cryptographically registered with SHA-256 hashes for timestamp verification. Full manifest available in `results/PRIOR_ART_MANIFEST.json`.

| Peptide ID | Sequence | SHA-256 (first 16 chars) |
|------------|----------|--------------------------|
| GtfC_pep007 | CWVWYYAWREREHRC | 5c38cca4b5bc58b0 |
| GtfC_pep008 | CRDFRWEWRVEKFEC | 63862d05f6c04919 |
| RgpB_pep003 | CRFEHYRFWAC | effdfebbe27d6ca2 |
| RgpB_pep005 | CKFWRYDRC | a3631bb20916b93e |
| RgpB_pep006 | CWWFFFC | b87c9e06c53f0555 |
| FadA_pep003 | IAEKIFDYVFMHERYE | cc7817f1bdbc3688 |
| FadA_pep010 | IIDFYWKDYLRDRDKEV | dea2ef459b61eb15 |
| SrtA_pep003 | CWALRYRMIC | 304a1cf8775d0851 |
| SrtA_pep010 | CWHRHWEHYC | ee8c428e5580a5ea |

**Full 40-sequence registry:** [PRIOR_ART_MANIFEST.json](file:///Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/biotech/oral_health/results/PRIOR_ART_MANIFEST.json)

**Manifest hash:** `40990eb7d4672e6c260e3f2e9cf6d45a9380658422e9db51a280e137c256a443`

---

## 7. Recommended Experimental Validation

### Priority 1: In Vitro Binding

| Peptide | Target | Method | Expected Timeline |
|---------|--------|--------|-------------------|
| GtfC_pep007 | GtfC | SPR / BLI | 2–4 weeks |
| RgpB_pep005 | RgpB | Fluorogenic substrate assay | 2–4 weeks |
| FadA_pep003 | FadA | Cell adhesion assay | 4–6 weeks |

### Priority 2: Selectivity Confirmation

- Test against commensal panel (*S. sanguinis*, *S. gordonii*, *V. parvula*)
- MIC determination to confirm no bactericidal activity

### Priority 3: Biofilm Efficacy

- MBEC assay against *S. mutans* biofilms
- Multi-species oral biofilm model (CDFF or drip-flow reactor)

### Priority 4: Stability and Delivery

- Salivary stability (ex vivo saliva incubation)
- Formulation testing (mouth rinse, gel, toothpaste incorporation)

---

## 8. References

1. Koo H et al. The exopolysaccharide matrix: a virulence determinant of cariogenic biofilm. *J Dent Res* 2013; 92(12):1065-73.
2. Hajishengallis G. Periodontitis: from microbial immune subversion to systemic inflammation. *Nat Rev Immunol* 2015; 15:30-44.
3. Rubinstein MR et al. *Fusobacterium nucleatum* promotes colorectal carcinogenesis. *Cell Host Microbe* 2013; 14:195-206.
4. Dominy SS et al. *Porphyromonas gingivalis* in Alzheimer's disease brains. *Sci Adv* 2019; 5(1):eaau3333.
5. Ren Z et al. Molecule targeting glucosyltransferase inhibits *S. mutans* biofilm. *Antimicrob Agents Chemother* 2015; 60(1):126-35.
6. Kadowaki T et al. Suppression of pathogenicity of *P. gingivalis* by KYT peptides. *J Biol Chem* 2004; 279(6):4918-25.
7. A distinct *Fusobacterium nucleatum* clade dominates the colorectal cancer niche. *Nature* 2024.
8. Stewart PS. Diffusion in biofilms. *Antimicrob Agents Chemother* 2003; 47(1):317-23.
9. de la Fuente-Nunez C et al. D-enantiomeric peptides that eradicate biofilms. *PLoS ONE* 2015; 10(7):e0132512.

---

## Code Availability

All pipeline code is available at: https://github.com/carlzimmerman/zimmerman-formula

```
extended_research/biotech/oral_health/
├── m4_oral_pathogen_target_extraction.py    # Stage 1
├── m4_antivirulence_peptide_designer.py     # Stage 2
├── m4_commensal_selectivity_checker.py      # Stage 3
├── m4_oral_cavity_validator.py              # Stage 4
├── m4_simulation_validation.py             # Stage 5
├── m4_oral_pipeline_controller.py          # Orchestration
├── results/
│   ├── TOP_CANDIDATES.json                 # All validated candidates
│   ├── PRIOR_ART_MANIFEST.json             # SHA-256 registry
│   └── pipeline_result_*.json              # Full pipeline output
└── simulations/
    ├── docking_simulation_*.json            # Binding energy estimates
    └── biofilm_simulation_*.json            # Penetration modeling
```

**License:** AGPL-3.0-or-later  
**Copyright:** Carl Zimmerman, 2026
