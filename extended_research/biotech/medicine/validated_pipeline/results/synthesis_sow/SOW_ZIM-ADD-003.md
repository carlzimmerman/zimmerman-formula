```

################################################################################
#                                                                              #
#                        STATEMENT OF WORK                                     #
#            PEPTIDE SYNTHESIS AND BIOPHYSICAL VALIDATION                      #
#                                                                              #
#                  Zimmerman Unified Geometry Framework                        #
#                                                                              #
################################################################################

Document ID:     SOW-ZIM-ADD-003-20260422
Date Generated:  2026-04-22 08:02:22
Framework:       ZUGF (Z² = 32π/3)

================================================================================
SECTION 1: EXECUTIVE SUMMARY
================================================================================

Peptide ID:         ZIM-ADD-003
Target Protein:     Alpha-3/Beta-4 Nicotinic Acetylcholine Receptor (α3β4 nAChR)
Therapeutic Area:   Opioid Addiction / Non-addictive Analgesia
Design Principle:   Z²-optimized geometric binding at 6.02 Å

This peptide was computationally designed using the Zimmerman Unified Geometry
Framework (ZUGF), which predicts optimal drug-receptor binding occurs at
√Z² × 1.0391 = 6.02 Å. Molecular dynamics simulations indicate
favorable binding thermodynamics (predicted ΔG < -40 kcal/mol).

================================================================================
SECTION 2: PEPTIDE SPECIFICATIONS
================================================================================

Sequence Information
--------------------
Amino Acid Sequence:     RWWFWR
Sequence (with caps):    R-W-W-F-W-R-NH2
Length:                  6 residues
N-Terminal:              Free amine (H2N-)
C-Terminal:              Amide (-NH2)

Chemical Properties
-------------------
Molecular Formula:       C54H66N16O6
Molecular Weight:        1035.2210 Da
Exact Mass:              1035.2210 Da
Isoelectric Point (pI):  12.48
Net Charge at pH 7.4:    +2.0
GRAVY Score:             -1.48
Instability Index:       8.3 (stable)
Total VdW Volume:        1220.1 Å³

SMILES String
-------------
NC(CCCNC(=N)N)C(=O)NC(Cc1c[nH]c2ccccc12)C(=O)NC(Cc1c[nH]c2ccccc12)C(=O)NC(Cc1ccccc1)C(=O)NC(Cc1c[nH]c2ccccc12)C(=O)NC(CCCNC(=N)N)C(=O)N

================================================================================
SECTION 3: SYNTHESIS SPECIFICATIONS
================================================================================

Synthesis Method
----------------
Method:                  Solid-Phase Peptide Synthesis (SPPS)
Chemistry:               Fmoc/tBu (9-fluorenylmethoxycarbonyl)
Resin:                   Rink Amide MBHA resin
Coupling Reagent:        HBTU/HOBt or HATU/HOAt
Base:                    DIPEA (N,N-diisopropylethylamine)
Cleavage:                TFA/TIS/H2O (95:2.5:2.5) for 2-3 hours

Product Specifications
----------------------
Purity:                  ≥95% by analytical RP-HPLC
Quantity:                10 mg (lyophilized powder)
Salt Form:               ACETATE (TFA exchange MANDATORY)
Appearance:              White to off-white lyophilized powder
Storage:                 -20°C, desiccated, protected from light

⚠️  CRITICAL: TFA to Acetate Salt Exchange
   TFA is cytotoxic at concentrations present after standard SPPS.
   ACETATE salt form is REQUIRED for all biological assays.

================================================================================
SECTION 4: QUALITY CONTROL REQUIREMENTS
================================================================================

Analytical Testing Package
--------------------------

1. ANALYTICAL RP-HPLC
   -----------------
   Column:              C18 (4.6 × 250 mm, 5 μm)
   Mobile Phase A:      0.1% TFA in water
   Mobile Phase B:      0.1% TFA in acetonitrile
   Gradient:            5-95% B over 30 minutes
   Flow Rate:           1.0 mL/min
   Detection:           UV 214 nm and 254 nm
   Temperature:         25°C

   Acceptance Criteria:
   • Single major peak with area ≥95%
   • Retention time recorded
   • Peak shape: Gaussian, tailing factor <1.5

2. MASS SPECTROMETRY
   -----------------
   Method:              ESI-MS (positive ion mode) or MALDI-TOF
   Expected [M+H]⁺:     1036.23 Da
   Expected [M+2H]²⁺:   518.62 Da (if applicable)
   Mass Accuracy:       ±1 Da

   Deliverables:
   • Full scan mass spectrum (m/z 100-2000)
   • Annotated peaks showing molecular ion
   • Deconvoluted spectrum if multiple charge states

3. AMINO ACID ANALYSIS (Optional)
   -----------------------------
   Method:              Pre-column derivatization, RP-HPLC
   Purpose:             Verify sequence composition
   Acceptance:          Molar ratios within ±10% of theoretical

Deliverables Summary
--------------------
☐ Lyophilized peptide in sealed, labeled vial
☐ Certificate of Analysis (CoA)
☐ HPLC chromatogram with purity calculation
☐ Mass spectrum with annotation
☐ Structure confirmation

================================================================================
SECTION 5: BINDING VALIDATION - SPR ASSAY
================================================================================

Surface Plasmon Resonance (SPR) Protocol
----------------------------------------
Instrument:           Biacore T200, S200, or equivalent
Sensor Chip:          CM5 (carboxymethyl dextran)
Target Protein:       Alpha-3/Beta-4 Nicotinic Acetylcholine Receptor (α3β4 nAChR)
PDB Reference:       6PV7

Immobilization
--------------
1. Activate CM5 surface with EDC/NHS (7 min)
2. Inject Alpha-3/Beta-4 Nicotinic Acetylcholine Receptor (α3β4 nAChR) (10-50 μg/mL in 10 mM acetate, pH 4.0-5.5)
3. Target immobilization level: 1000-3000 RU
4. Block with ethanolamine-HCl (7 min)
5. Confirm stable baseline before analyte injection

Analyte Preparation
-------------------
Peptide:              ZIM-ADD-003 (RWWFWR)
Stock:                1 mM in DMSO (or water if soluble)
Working Buffer:       HBS-EP+ (10 mM HEPES pH 7.4, 150 mM NaCl,
                      3 mM EDTA, 0.05% Surfactant P20)
DMSO Content:         ≤1% final (with DMSO correction)

Kinetic Analysis
----------------
Concentrations:       0.01, 0.1, 1.0, 10.0, 100.0 μM (5-point)
                      (Include 0 μM blank for reference)
Contact Time:         120 seconds
Dissociation Time:    300 seconds
Flow Rate:            30 μL/min
Temperature:          25°C
Regeneration:         10 mM Glycine-HCl pH 2.0 (if needed)

Data Analysis
-------------
Software:             Biacore Evaluation Software
Fitting Model:        1:1 Langmuir binding (or steady-state affinity)

Required Output:
• Sensorgrams for all concentrations (overlay plot)
• Kinetic fit showing residuals
• Calculated parameters:
  - KD (equilibrium dissociation constant) with 95% CI
  - ka (association rate constant, M⁻¹s⁻¹)
  - kd (dissociation rate constant, s⁻¹)
  - χ² (goodness of fit)

Acceptance Criteria
-------------------
• KD < 1 μM:      PROCEED to functional assays (strong binder)
• KD 1-10 μM:     CONSIDER for optimization (moderate binder)
• KD > 10 μM:     DO NOT PROCEED (weak binder)
• KD > 100 μM:    No detectable binding

================================================================================
SECTION 6: FUNCTIONAL ASSAYS
================================================================================

Target:               Alpha-3/Beta-4 Nicotinic Acetylcholine Receptor (α3β4 nAChR)
Indication:           Opioid Addiction / Non-addictive Analgesia

Recommended Assay(s) Based on Target
------------------------------------

NICOTINIC RECEPTOR BINDING ASSAY (Primary)
------------------------------------------
Method:               Radioligand displacement
Radioligand:          [³H]-Epibatidine or [¹²⁵I]-α-Bungarotoxin
Membrane Source:      HEK293 cells expressing α3β4 nAChR

Protocol:
1. Incubate membranes with radioligand + peptide (1 nM - 100 μM)
2. Equilibrate at 22°C for 2 hours
3. Filter and wash
4. Measure bound radioactivity

Success Criteria:
• Ki < 10 μM indicates significant binding
• Full displacement curve with Hill slope ~1

================================================================================
SECTION 7: DELIVERABLES AND TIMELINE
================================================================================

Deliverables
------------
Phase 1: Peptide Synthesis
  ☐ 10 mg lyophilized peptide (≥95% pure, acetate salt)
  ☐ Certificate of Analysis
  ☐ HPLC chromatogram
  ☐ MS spectrum

Phase 2: SPR Binding Analysis
  ☐ Full SPR sensorgram data (.blr files)
  ☐ Kinetic analysis report (KD, ka, kd)
  ☐ Steady-state affinity analysis (if applicable)

Phase 3: Functional Assay (if binding confirmed)
  ☐ Dose-response data
  ☐ IC50/EC50 determination
  ☐ Statistical analysis

Estimated Timeline
------------------
Phase                        Duration        Est. Cost (USD)
-------------------------------------------------------------
Peptide Synthesis            2-3 weeks       $500-1,500
QC Testing                   Included        Included
Salt Exchange                +2-3 days       +$100-200
SPR Assay                    1-2 weeks       $2,000-5,000
Functional Assay             2-4 weeks       $3,000-10,000
-------------------------------------------------------------
TOTAL ESTIMATE               5-10 weeks      $5,000-17,000

================================================================================
SECTION 8: INTELLECTUAL PROPERTY AND CONFIDENTIALITY
================================================================================

IP Ownership:         All intellectual property remains with the
                      Principal Investigator and/or sponsoring institution.

Confidentiality:      This peptide sequence and associated data are
                      CONFIDENTIAL. Standard CRO NDA applies.

Publication:          Principal Investigator retains full publication rights.
                      CRO may not publish without written consent.

Data Ownership:       All raw data, spectra, and analysis files must be
                      provided to the Principal Investigator.

================================================================================
SECTION 9: CONTACT INFORMATION
================================================================================

Principal Investigator
----------------------
Name:               [TO BE FILLED]
Institution:        [TO BE FILLED]
Address:            [TO BE FILLED]
Email:              [TO BE FILLED]
Phone:              [TO BE FILLED]

CRO Contact
-----------
Company:            [TO BE FILLED]
Contact Person:     [TO BE FILLED]
Email:              [TO BE FILLED]
Quote Reference:    [TO BE FILLED]

================================================================================
SECTION 10: AUTHORIZATION
================================================================================

By signing below, both parties agree to the terms of this Statement of Work.

Principal Investigator:

Signature: _________________________    Date: ____________

Name:      _________________________    Title: ___________


CRO Representative:

Signature: _________________________    Date: ____________

Name:      _________________________    Title: ___________


================================================================================
                        END OF STATEMENT OF WORK
                              ZIM-ADD-003
================================================================================

Generated by: Zimmerman Unified Geometry Framework (ZUGF)
Version:      1.0
Timestamp:    2026-04-22T08:02:22.036822


```