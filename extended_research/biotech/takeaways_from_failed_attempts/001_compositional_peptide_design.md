# Failed Attempt #001: Compositional Peptide Design

**Date:** 2026-04-22
**Status:** FAILED - Negative controls outperformed designed peptides

## The Hypothesis

Design therapeutic peptides using compositional constraints:
- Length: 4-10 amino acids
- No consecutive prolines (structural breakers)
- Max 50% hydrophobic residues (solubility)
- At least 1 charged residue (stability)
- RDKit validation for synthesizability

## The Experiment

Ran batch pipeline on 4 target system targets:
- Parkinson's (P37840 alpha-synuclein)
- Alzheimer's (P10636 tau)
- C2_Homodimer_A (P04578 gp120)
- Childbirth (P30559 oxytocin receptor)

**Protocol:**
1. Generate 15-20 "designed" peptides per target using compositional rules
2. Generate 50-100 random control peptides (same length distribution)
3. Predict 3D structures via ESMFold API
4. Compare pLDDT (structure confidence) pass rates

## The Results

| Target | Designed Pass Rate | Control Pass Rate |
|--------|-------------------|-------------------|
| Alpha-synuclein | 45% | 40% |
| Tau | 20% | 38% |
| gp120 | 33% | 56% |
| Oxytocin R | 33% | 40% |
| **Average** | **28.9%** | **44.7%** |

**Verdict:** Random peptides outperformed designed peptides by ~16 percentage points.

## Why It Failed

### The Core Mistake: Designing for Stability, Not Affinity

The compositional constraints forced peptides to:
1. **Fold tightly into stable balls** - High pLDDT means confident structure
2. **Hide their functional groups** - Hydrophobic cores with polar shells
3. **Have no exposed "sticky bits"** - Nothing to grab the target protein

**Gemini's insight:** "You built perfectly stable marbles that just roll off the receptor."

### What pLDDT Actually Measures

pLDDT (predicted Local Distance Difference Test) measures:
- How confident ESMFold is about the predicted structure
- Whether the peptide folds into a well-defined shape
- NOT whether it will bind to anything

A high pLDDT score means "this folds nicely" - it says nothing about therapeutic potential.

### The Random Control Advantage

Random peptides may actually be BETTER for binding because:
- More disordered = more exposed functional groups
- Less constrained = can adapt to target shape
- Natural peptide drugs often have intrinsic disorder

## The Lesson

**You cannot design a drug by looking only at the drug.**

The drug must complement the target. Design must start from:
1. The target's binding pocket geometry
2. Specific anchor atoms (H-bond donors/acceptors)
3. Optimal interaction distances (6.02 Å from Z² framework)
4. Then build the peptide to fit those constraints

## What We Salvaged

The pipeline infrastructure is excellent:
- UniProt/PDB/ChEMBL API integration works
- ESMFold structure prediction works
- Batch processing with error handling works
- Negative control system works (it caught this failure!)

Only the design strategy (m04_peptide_design.py) needs replacement.

## Next Step

Create `m04b_pharmacophore_design.py` using **Geometric Pharmacophore Mapping**:
1. Read target binding pocket from PDB
2. Identify anchor atoms in pocket
3. Project ideal interaction points at 6.02 Å
4. Build peptide backbone to connect those points
5. Select amino acids that place sidechains at optimal positions

This ensures the peptide is designed TO the target, not in isolation.

## Files to Archive

Move to `failed_attempts/compositional_peptide_design/`:
- `framework/m04_peptide_design.py` (keep copy, mark deprecated)
- Design results showing failure

## Key Quote

> "The negative controls did exactly what they were supposed to do. You built a brilliantly automated, API-connected, chemically validated pipeline... and it objectively proved that your 'designed' peptides perform worse than total random chance. This isn't a failure. It's a massive success of the scientific method."

---

**Analogy to Kepler:** Just as Kepler tried circles before discovering ellipses, we tried compositional design before discovering that target-complementary geometry is required. Each failed hypothesis narrows the search space.
