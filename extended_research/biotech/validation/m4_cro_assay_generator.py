#!/usr/bin/env python3
"""
M4 CRO Assay Documentation Generator
======================================

Generates professional-quality assay protocols and documentation
for Contract Research Organization (CRO) submission.

ASSAY TYPES:
1. Surface Plasmon Resonance (SPR) - Biacore, Carterra
2. Bio-Layer Interferometry (BLI) - Octet
3. Isothermal Titration Calorimetry (ITC)
4. Fluorescence Polarization (FP)
5. Cell-based activity assays

OUTPUT:
- Protocol documents (PDF-ready markdown)
- Sample submission forms
- Assay design with controls
- Data analysis specifications
- Quotation request templates

LICENSE: AGPL-3.0-or-later
AUTHOR: Carl Zimmerman & Claude Opus 4.5
DATE: April 2026
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional
from textwrap import dedent


@dataclass
class PeptideCandidate:
    """Peptide candidate for CRO testing."""
    peptide_id: str
    sequence: str
    target: str
    disease: str
    predicted_kd_nM: float
    molecular_weight: float = 0.0
    purity_required: float = 95.0
    amount_mg: float = 5.0
    modifications: List[str] = field(default_factory=list)


@dataclass
class AssayRequest:
    """Complete CRO assay request."""
    project_name: str
    requestor: str
    organization: str
    peptides: List[PeptideCandidate]
    target_protein: str
    assay_type: str  # SPR, BLI, ITC, FP, Cell
    priority: str = "Standard"  # Standard, Rush
    special_requirements: str = ""
    budget_usd: Optional[float] = None


@dataclass
class SPRProtocol:
    """SPR assay protocol details."""
    instrument: str = "Biacore T200"
    chip_type: str = "CM5"
    immobilization: str = "Amine coupling"
    ligand: str = ""  # Target protein
    analyte: str = ""  # Peptides
    buffer: str = "HBS-EP+ (10 mM HEPES pH 7.4, 150 mM NaCl, 3 mM EDTA, 0.05% P20)"
    flow_rate: float = 30.0  # µL/min
    contact_time: int = 120  # seconds
    dissociation_time: int = 600  # seconds
    regeneration: str = "10 mM Glycine pH 2.0"
    concentrations: List[float] = field(default_factory=lambda: [0.1, 0.3, 1, 3, 10, 30, 100, 300])
    temperature: float = 25.0  # °C


def calculate_mw(sequence: str) -> float:
    """Calculate approximate molecular weight from sequence."""
    aa_weights = {
        'A': 89.1, 'R': 174.2, 'N': 132.1, 'D': 133.1, 'C': 121.2,
        'E': 147.1, 'Q': 146.2, 'G': 75.1, 'H': 155.2, 'I': 131.2,
        'L': 131.2, 'K': 146.2, 'M': 149.2, 'F': 165.2, 'P': 115.1,
        'S': 105.1, 'T': 119.1, 'W': 204.2, 'Y': 181.2, 'V': 117.1
    }
    mw = sum(aa_weights.get(aa.upper(), 110.0) for aa in sequence)
    mw -= 18.0 * (len(sequence) - 1)  # Water loss
    return round(mw, 1)


def generate_spr_protocol(request: AssayRequest) -> str:
    """Generate SPR protocol document."""
    protocol = SPRProtocol(
        ligand=request.target_protein,
        analyte=", ".join([p.peptide_id for p in request.peptides])
    )

    # Adjust concentrations based on predicted Kd
    avg_kd = sum(p.predicted_kd_nM for p in request.peptides) / len(request.peptides)
    if avg_kd < 1:
        protocol.concentrations = [0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30]
    elif avg_kd < 100:
        protocol.concentrations = [0.1, 0.3, 1, 3, 10, 30, 100, 300]
    else:
        protocol.concentrations = [1, 3, 10, 30, 100, 300, 1000, 3000]

    doc = f"""# Surface Plasmon Resonance (SPR) Assay Protocol

## Project Information

| Field | Value |
|-------|-------|
| Project Name | {request.project_name} |
| Requestor | {request.requestor} |
| Organization | {request.organization} |
| Date | {datetime.now().strftime("%Y-%m-%d")} |
| Priority | {request.priority} |

---

## 1. Objective

Determine binding kinetics and affinity (kₐ, k_d, K_D) for {len(request.peptides)} peptide candidates against {request.target_protein} using Surface Plasmon Resonance.

---

## 2. Materials

### 2.1 Instrument
- **Instrument**: {protocol.instrument}
- **Sensor Chip**: {protocol.chip_type}
- **Temperature**: {protocol.temperature}°C

### 2.2 Target Protein (Ligand)
| Parameter | Specification |
|-----------|---------------|
| Protein | {request.target_protein} |
| Source | Recombinant (specify supplier) |
| Purity | >95% (SDS-PAGE) |
| Amount | 100 µg minimum |
| Buffer | PBS or compatible |

### 2.3 Peptide Analytes

| Peptide ID | Sequence | MW (Da) | Predicted K_D (nM) | Amount (mg) |
|------------|----------|---------|-------------------|-------------|
"""

    for p in request.peptides:
        mw = calculate_mw(p.sequence) if p.molecular_weight == 0 else p.molecular_weight
        doc += f"| {p.peptide_id} | {p.sequence[:20]}{'...' if len(p.sequence) > 20 else ''} | {mw:.1f} | {p.predicted_kd_nM:.2f} | {p.amount_mg} |\n"

    doc += f"""
### 2.4 Buffers and Reagents
- **Running Buffer**: {protocol.buffer}
- **Regeneration**: {protocol.regeneration}
- **Immobilization Kit**: Amine Coupling Kit (EDC/NHS)

---

## 3. Experimental Design

### 3.1 Chip Preparation
1. Dock new {protocol.chip_type} sensor chip
2. Prime system with running buffer (3 cycles)
3. Normalize flow cells

### 3.2 Immobilization Protocol
1. **Pre-concentration**: Test pH 4.0, 4.5, 5.0, 5.5 for optimal electrostatic binding
2. **Activation**: EDC/NHS mixture, 7 min at 10 µL/min
3. **Coupling**: Inject {request.target_protein} at optimal pH, target RU: 500-1000
4. **Deactivation**: Ethanolamine-HCl pH 8.5, 7 min
5. **Reference**: Use flow cell 1 as reference (activated/deactivated, no ligand)

### 3.3 Kinetic Analysis
| Parameter | Value |
|-----------|-------|
| Flow Rate | {protocol.flow_rate} µL/min |
| Contact Time | {protocol.contact_time} seconds |
| Dissociation Time | {protocol.dissociation_time} seconds |
| Regeneration | {protocol.regeneration}, 30 sec |

### 3.4 Concentration Series
Prepare 2-fold serial dilutions in running buffer:
**{', '.join([f'{c} nM' for c in protocol.concentrations])}**

Include:
- Blank injections (buffer only) at start and end
- Duplicate of middle concentration for reproducibility

---

## 4. Run Order

```
1. Startup cycles (3x buffer)
2. Blank injection #1
3. Peptide A: {protocol.concentrations[0]} nM → {protocol.concentrations[-1]} nM
4. Blank injection #2
5. Peptide A duplicate: {protocol.concentrations[3]} nM
6. Peptide B: {protocol.concentrations[0]} nM → {protocol.concentrations[-1]} nM
... (repeat for all peptides)
N. Final blank injection
N+1. Shutdown
```

---

## 5. Data Analysis

### 5.1 Software
- Biacore Evaluation Software or Scrubber

### 5.2 Processing Steps
1. Reference subtraction (Fc1)
2. Blank subtraction
3. Baseline alignment
4. Global fitting to 1:1 Langmuir model

### 5.3 Reported Parameters
For each peptide-target pair:

| Parameter | Units | Description |
|-----------|-------|-------------|
| k_a (k_on) | M⁻¹s⁻¹ | Association rate constant |
| k_d (k_off) | s⁻¹ | Dissociation rate constant |
| K_D | nM | Equilibrium dissociation constant (k_d/k_a) |
| Rmax | RU | Maximum binding capacity |
| χ² | - | Goodness of fit |

### 5.4 Quality Criteria
- χ² < 10% of Rmax
- Duplicate CV < 20%
- Sensorgrams show clean association/dissociation phases
- No mass transport limitation

---

## 6. Controls

| Control | Purpose |
|---------|---------|
| Buffer blank | Baseline and reference subtraction |
| Reference surface | Non-specific binding |
| Duplicate injection | Reproducibility |
| Known binder (if available) | System validation |

---

## 7. Deliverables

1. **Raw Data**: Sensorgrams in Biacore format
2. **Processed Data**: Reference/blank subtracted curves
3. **Kinetic Report**: Table of k_a, k_d, K_D for all peptides
4. **Sensorgram Figures**: Fitted curves with residuals
5. **Methods Summary**: Detailed protocol as performed
6. **QC Report**: Chip preparation, baseline stability

---

## 8. Timeline

| Phase | Duration |
|-------|----------|
| Chip preparation & optimization | 1 day |
| Sample preparation | 1 day |
| Kinetic runs | 2-3 days |
| Data analysis | 1-2 days |
| Report generation | 1 day |
| **Total** | **6-8 business days** |

---

## 9. Special Instructions

{request.special_requirements if request.special_requirements else "None specified."}

---

## 10. Contact

| Role | Name | Contact |
|------|------|---------|
| Requestor | {request.requestor} | [email] |
| Project Manager | [CRO PM] | [email] |
| Scientist | [CRO Scientist] | [email] |

---

*Protocol generated by M4 CRO Assay Generator*
*{datetime.now().strftime("%Y-%m-%d %H:%M")}*
*License: AGPL-3.0-or-later*
"""

    return doc


def generate_bli_protocol(request: AssayRequest) -> str:
    """Generate BLI (Octet) protocol document."""
    doc = f"""# Bio-Layer Interferometry (BLI) Assay Protocol

## Project Information

| Field | Value |
|-------|-------|
| Project Name | {request.project_name} |
| Requestor | {request.requestor} |
| Organization | {request.organization} |
| Date | {datetime.now().strftime("%Y-%m-%d")} |
| Assay Type | BLI Kinetic Analysis |

---

## 1. Objective

Determine binding kinetics and affinity for {len(request.peptides)} peptide candidates against {request.target_protein} using Bio-Layer Interferometry (ForteBio Octet).

---

## 2. Materials

### 2.1 Instrument
- **Instrument**: ForteBio Octet RED96 or Octet K2
- **Biosensors**: Anti-His (HIS1K) or Streptavidin (SA)
- **Temperature**: 25°C (or 30°C for stability)
- **Shake Speed**: 1000 rpm

### 2.2 Target Protein
- **Protein**: {request.target_protein}
- **Tag**: His-tag or Biotin (for immobilization)
- **Loading Concentration**: 10-20 µg/mL
- **Loading Target**: 1.0-2.0 nm shift

### 2.3 Peptide Analytes

| Peptide ID | Sequence | MW (Da) | Predicted K_D (nM) |
|------------|----------|---------|-------------------|
"""

    for p in request.peptides:
        mw = calculate_mw(p.sequence) if p.molecular_weight == 0 else p.molecular_weight
        doc += f"| {p.peptide_id} | {p.sequence[:20]}... | {mw:.1f} | {p.predicted_kd_nM:.2f} |\n"

    doc += f"""
---

## 3. Assay Protocol

### 3.1 Assay Steps

| Step | Duration | Description |
|------|----------|-------------|
| Baseline | 60 sec | Kinetics buffer |
| Loading | 300 sec | Capture {request.target_protein} on sensor |
| Baseline 2 | 120 sec | Wash and stabilize |
| Association | 180 sec | Peptide binding |
| Dissociation | 600 sec | Buffer dissociation |
| Regeneration | 3 × 5 sec | Glycine pH 1.5 |
| Neutralization | 5 sec | Buffer |

### 3.2 Concentration Series
- 8-point 2-fold dilution: 0.1, 0.3, 1, 3, 10, 30, 100, 300 nM
- Include 0 nM (reference sensors)
- Run in duplicate for key concentrations

### 3.3 Plate Layout (96-well)
```
    1    2    3    4    5    6    7    8    9   10   11   12
A [Load][Load][Load][Load][Load][Load][Load][Load][Ref][Ref][Regen][Neut]
B [P1 0.1][P1 0.3][P1 1][P1 3][P1 10][P1 30][P1 100][P1 300][Buffer]...
...
```

---

## 4. Data Analysis

### 4.1 Processing
1. Reference subtraction (unloaded sensors)
2. Y-axis alignment
3. Inter-step correction
4. Savitzky-Golay smoothing (optional)

### 4.2 Fitting
- Model: 1:1 binding
- Global fit: k_on and k_off
- Report: K_D = k_off / k_on

### 4.3 Quality Criteria
- R² > 0.95
- Response > 0.1 nm for top concentration
- Full association/dissociation curves

---

## 5. Deliverables

1. Kinetic parameters (k_on, k_off, K_D) for all peptide-target pairs
2. Sensorgrams with fits
3. Steady-state analysis (if applicable)
4. Raw data files (.frd format)
5. Summary report

---

## 6. Timeline

Estimated completion: **5-7 business days** from sample receipt

---

*Protocol generated by M4 CRO Assay Generator*
*{datetime.now().strftime("%Y-%m-%d %H:%M")}*
"""

    return doc


def generate_sample_submission_form(request: AssayRequest) -> str:
    """Generate sample submission form."""
    doc = f"""# Sample Submission Form

## Project Details

| Field | Information |
|-------|-------------|
| Project Name | {request.project_name} |
| Requestor | {request.requestor} |
| Organization | {request.organization} |
| Submission Date | {datetime.now().strftime("%Y-%m-%d")} |
| Requested Assay | {request.assay_type} |
| Priority | {request.priority} |

---

## Sample Information

### Target Protein

| Field | Information |
|-------|-------------|
| Name | {request.target_protein} |
| Source | [Specify: In-house / Commercial supplier] |
| Catalog # | [If commercial] |
| Lot # | [Required] |
| Concentration | [mg/mL] |
| Volume Provided | [µL] |
| Buffer | [Buffer composition] |
| Storage | [Temperature] |
| Tag | [His / Biotin / None] |

### Peptide Samples

| # | Peptide ID | Sequence | MW (Da) | Amount (mg) | Purity (%) | Format |
|---|------------|----------|---------|-------------|------------|--------|
"""

    for i, p in enumerate(request.peptides, 1):
        mw = calculate_mw(p.sequence) if p.molecular_weight == 0 else p.molecular_weight
        doc += f"| {i} | {p.peptide_id} | {p.sequence} | {mw:.1f} | {p.amount_mg} | >{p.purity_required} | Lyophilized |\n"

    doc += f"""
---

## Sample Handling

| Requirement | Specification |
|-------------|---------------|
| Storage Temperature | -20°C or -80°C |
| Light Sensitive | No (unless specified) |
| Reconstitution Buffer | DMSO or aqueous (specify) |
| Max Freeze-Thaw Cycles | 3 |

---

## Shipping Instructions

- **Carrier**: FedEx Priority Overnight (domestic) / World Courier (international)
- **Packaging**: Ship on dry ice
- **Documentation**: Include this form and CoA for all samples
- **Notify**: Email CRO upon shipment with tracking number

---

## Regulatory & Safety

| Item | Status |
|------|--------|
| MSDS Required | Yes |
| BSL Level | BSL-1 (unless otherwise specified) |
| Special Hazards | None identified |
| Disposal | Standard biohazard waste |

---

## Authorization

| Role | Signature | Date |
|------|-----------|------|
| Requestor | _____________ | _______ |
| PI/Supervisor | _____________ | _______ |
| CRO Received By | _____________ | _______ |

---

## Contact Information

**Requestor**:
- Name: {request.requestor}
- Email: [email]
- Phone: [phone]

**Emergency Contact**:
- Name: [backup contact]
- Phone: [phone]

---

*Form generated by M4 CRO Assay Generator*
*Submit with samples to CRO*
"""

    return doc


def generate_quotation_request(request: AssayRequest) -> str:
    """Generate quotation request letter."""
    doc = f"""# Request for Quotation (RFQ)

**Date**: {datetime.now().strftime("%B %d, %Y")}

**To**: [CRO Name]
**From**: {request.requestor}, {request.organization}
**Subject**: RFQ for {request.assay_type} Binding Assay Services

---

## Project Overview

We are seeking quotations for binding affinity characterization of {len(request.peptides)} peptide candidates against {request.target_protein}.

### Project Details

| Parameter | Specification |
|-----------|---------------|
| Number of Peptides | {len(request.peptides)} |
| Target Protein | {request.target_protein} |
| Assay Type | {request.assay_type} |
| Deliverables | Kinetic parameters (k_on, k_off, K_D) |
| Timeline | {request.priority} priority |
| Budget Range | {"USD ${:,.0f}".format(request.budget_usd) if request.budget_usd else "TBD"} |

---

## Scope of Work

### Phase 1: Assay Development (if needed)
- Target protein immobilization optimization
- Regeneration condition screening
- Buffer compatibility testing

### Phase 2: Kinetic Characterization
- Single-cycle or multi-cycle kinetics
- 8-point concentration series per peptide
- Duplicate measurements for QC

### Phase 3: Data Analysis & Reporting
- Global kinetic fitting (1:1 model)
- Steady-state affinity (if applicable)
- Full report with sensorgrams

---

## Peptide Candidates

| Peptide ID | MW (Da) | Expected K_D (nM) | Notes |
|------------|---------|-------------------|-------|
"""

    for p in request.peptides:
        mw = calculate_mw(p.sequence) if p.molecular_weight == 0 else p.molecular_weight
        doc += f"| {p.peptide_id} | {mw:.0f} | {p.predicted_kd_nM:.1f} | {p.disease} |\n"

    doc += f"""
---

## Requested Information

Please provide quotation including:

1. **Cost per peptide** for kinetic characterization
2. **Assay development costs** (if applicable)
3. **Rush fees** (if applicable)
4. **Timeline** from sample receipt to report delivery
5. **Sample requirements** (amount, purity, format)
6. **Target protein handling** (CRO procurement or client-provided)

---

## Selection Criteria

Quotations will be evaluated based on:
- Technical capability and experience
- Timeline
- Cost
- Data quality guarantees

---

## Submission Instructions

Please submit quotation by: **{(datetime.now() + timedelta(days=14)).strftime("%B %d, %Y")}**

Submit to:
- **Email**: [requestor email]
- **Subject Line**: "RFQ Response - {request.project_name}"

---

## Questions

Direct technical questions to:
- {request.requestor}
- [phone]
- [email]

---

*RFQ generated by M4 CRO Assay Generator*
*{datetime.now().strftime("%Y-%m-%d")}*
"""

    return doc


def generate_all_documents(request: AssayRequest, output_dir: Path) -> Dict[str, Path]:
    """Generate all CRO documentation."""
    output_dir.mkdir(parents=True, exist_ok=True)

    documents = {}

    # Protocol
    if request.assay_type.upper() == "SPR":
        protocol = generate_spr_protocol(request)
        protocol_path = output_dir / f"{request.project_name}_SPR_Protocol.md"
    elif request.assay_type.upper() == "BLI":
        protocol = generate_bli_protocol(request)
        protocol_path = output_dir / f"{request.project_name}_BLI_Protocol.md"
    else:
        protocol = generate_spr_protocol(request)  # Default to SPR
        protocol_path = output_dir / f"{request.project_name}_Protocol.md"

    with open(protocol_path, "w") as f:
        f.write(protocol)
    documents["protocol"] = protocol_path

    # Sample submission form
    submission = generate_sample_submission_form(request)
    submission_path = output_dir / f"{request.project_name}_Sample_Submission.md"
    with open(submission_path, "w") as f:
        f.write(submission)
    documents["submission_form"] = submission_path

    # Quotation request
    rfq = generate_quotation_request(request)
    rfq_path = output_dir / f"{request.project_name}_RFQ.md"
    with open(rfq_path, "w") as f:
        f.write(rfq)
    documents["rfq"] = rfq_path

    # Summary JSON
    summary = {
        "project_name": request.project_name,
        "requestor": request.requestor,
        "organization": request.organization,
        "assay_type": request.assay_type,
        "target": request.target_protein,
        "n_peptides": len(request.peptides),
        "peptides": [asdict(p) for p in request.peptides],
        "generated": datetime.now().isoformat(),
        "documents": {k: str(v) for k, v in documents.items()}
    }

    summary_path = output_dir / f"{request.project_name}_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    documents["summary"] = summary_path

    return documents


def run_demo():
    """Generate demo CRO documents for top peptide candidates."""
    print("=" * 70)
    print("M4 CRO ASSAY DOCUMENTATION GENERATOR")
    print("=" * 70)
    print()
    print("This tool generates professional CRO submission documents")
    print("for binding affinity validation of peptide candidates.")
    print()

    # Create demo request with top candidates
    demo_peptides = [
        PeptideCandidate(
            peptide_id="METAB_GLP1R_002",
            sequence="HAEGTFTSDVSSYLEGQAAKEFIAWLVKGR",
            target="GLP-1R",
            disease="Obesity/T2D",
            predicted_kd_nM=0.011,
            amount_mg=5.0
        ),
        PeptideCandidate(
            peptide_id="NONADD_Oxytocin_R_004",
            sequence="CYIQNCPLG",
            target="Oxytocin-R",
            disease="Depression/Anxiety",
            predicted_kd_nM=0.48,
            amount_mg=5.0
        ),
        PeptideCandidate(
            peptide_id="NEURO_GBA1_001",
            sequence="KLVFFAEDVGSNKGA",
            target="GBA1",
            disease="Parkinson's",
            predicted_kd_nM=0.10,
            amount_mg=5.0
        ),
        PeptideCandidate(
            peptide_id="PED_CFTR_007",
            sequence="WQEKFQTPEVR",
            target="CFTR",
            disease="Cystic Fibrosis",
            predicted_kd_nM=22.6,
            amount_mg=5.0
        ),
        PeptideCandidate(
            peptide_id="BAFF_pep002",
            sequence="CYCRPGWYCALRPG",
            target="BAFF",
            disease="Lupus/RA",
            predicted_kd_nM=79.6,
            amount_mg=5.0
        )
    ]

    request = AssayRequest(
        project_name="M4_TopCandidates_Binding",
        requestor="Carl Zimmerman",
        organization="Z² Research",
        peptides=demo_peptides,
        target_protein="Multiple targets (see peptide list)",
        assay_type="SPR",
        priority="Standard",
        budget_usd=25000.0,
        special_requirements="Please test each peptide against its specified target. "
                           "All peptides will be provided lyophilized >95% purity."
    )

    # Generate documents
    output_dir = Path(__file__).parent / "cro_documents" / "demo"
    documents = generate_all_documents(request, output_dir)

    print("Generated Documents:")
    for doc_type, path in documents.items():
        print(f"  {doc_type}: {path}")

    print()
    print("=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)
    print()
    print("The generated documents are ready for CRO submission:")
    print()
    print("1. Protocol - Detailed SPR/BLI assay protocol")
    print("2. Sample Submission Form - Required for sample shipment")
    print("3. RFQ - Request for quotation from CROs")
    print()
    print("RECOMMENDED CROs for peptide binding:")
    print("  - Proteros (Munich) - High-quality SPR")
    print("  - Reaction Biology (PA) - BLI/SPR")
    print("  - WuXi AppTec - Large-scale screening")
    print("  - Charles River - Full preclinical package")
    print()

    return request, documents


def generate_for_pipeline(peptide_data: List[Dict], target: str,
                           output_dir: Path) -> Dict[str, Path]:
    """
    Generate CRO documents from pipeline output.

    Args:
        peptide_data: List of peptide dicts from ranking pipeline
        target: Target protein name
        output_dir: Output directory

    Returns:
        Dictionary of generated document paths
    """
    peptides = []
    for p in peptide_data[:10]:  # Top 10 for CRO
        peptide = PeptideCandidate(
            peptide_id=p.get("peptide_id", "UNKNOWN"),
            sequence=p.get("sequence", ""),
            target=p.get("target", target),
            disease=p.get("disease", ""),
            predicted_kd_nM=p.get("predicted_kd", p.get("affinity", 100.0)),
            amount_mg=5.0
        )
        peptides.append(peptide)

    request = AssayRequest(
        project_name=f"M4_{target}_Validation",
        requestor="[Requestor Name]",
        organization="[Organization]",
        peptides=peptides,
        target_protein=target,
        assay_type="SPR",
        priority="Standard"
    )

    return generate_all_documents(request, output_dir)


if __name__ == "__main__":
    run_demo()
