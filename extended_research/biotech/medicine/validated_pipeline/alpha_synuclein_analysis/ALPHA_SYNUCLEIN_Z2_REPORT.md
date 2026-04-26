# α-Synuclein Fibril Z² Analysis Report

**SPDX-License-Identifier: AGPL-3.0-or-later**

**PRIOR ART PUBLICATION - DEFENSIVE DISCLOSURE**

Published: 2026-04-24

---

## Executive Summary

**CRITICAL FINDING:** α-Synuclein fibrils do NOT use Z² (6.015 Å) aromatic spacing.

Instead, the cross-β amyloid stacking distance is consistently **~4.9 Å**, which is
approximately **1.1 Å shorter** than Z². This suggests amyloid fibrils operate
under a different geometric principle than the symmetric oligomeric enzymes
(C2_Homodimer_A protease, Monomeric_Cleft_C NS3, etc.) where Z² was validated.

**Implication:** Different therapeutic design strategy required for Parkinson's.

---

## Target Information

| Property | Value |
|----------|-------|
| **Protein** | α-Synuclein (140 aa) |
| **target system** | Parkinson's target system, Dementia with Lewy Bodies, MSA |
| **Structure Type** | Amyloid fibril (cross-β) |
| **PDB IDs Analyzed** | 6CU7 (rod), 6H6B (standard) |
| **Resolution** | 3.4-3.5 Å (Cryo-EM) |

---

## Z² Analysis Results

### Summary Table

| Structure | Z² Matches | Strong | Moderate | Best Distance |
|-----------|------------|--------|----------|---------------|
| 6CU7 | 0 | 0 | 0 | 4.95 Å |
| 6H6B | 0 | 0 | 0 | 4.99 Å |

### Zero Z² Matches Found

Both fibril structures show **NO aromatic pairs** within ±500 mÅ of Z² (6.015 Å).

---

## Key Finding: Amyloid Stacking Distance

### Cross-β Fibril Geometry

α-Synuclein fibrils use a characteristic **~4.9 Å stacking repeat**, consistent
with the canonical cross-β amyloid architecture:

| Residue | Inter-Chain Distance | Z² Deviation |
|---------|---------------------|--------------|
| TYR39 ↔ TYR39 | 4.82-4.99 Å | -1.0 to -1.2 Å |
| HIS50 ↔ HIS50 | 4.81-4.95 Å | -1.1 to -1.2 Å |
| PHE94 ↔