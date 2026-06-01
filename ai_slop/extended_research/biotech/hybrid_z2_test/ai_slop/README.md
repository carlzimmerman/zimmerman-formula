# AI Slop: Hallucinated and Failed Experiments

This folder contains experiments that either:
1. Produced hallucinated results (looked real but weren't)
2. Failed in informative ways

These are preserved for scientific honesty and to prevent others from repeating the same mistakes.

---

## Contents

### Hallucinated Protein Design

| File | Description | Problem |
|------|-------------|---------|
| `hybrid_z2_denovo_designer.py` | Original de novo designer | Gamed fitness function |
| `z2_kaluza_klein_protein.pdb` | "Designed" protein structure | Doesn't fold (pLDDT = 0.4) |
| `z2_kaluza_klein_protein.fasta` | Sequence of above | Random sequence space |
| `z2_protein_design_results.json` | Claimed Z² score = 95 | Not validated |

### Failed Validated Design

| File | Description | Result |
|------|-------------|--------|
| `hybrid_z2_validated_designer.py` | ESMFold-constrained designer | 0/375 foldable |
| `z2_validated_design.json` | Results from 25 generations | All pLDDT = 0.5 |
| `z2_validated_protein.fasta` | Best sequence found | Still doesn't fold |

### Validation Evidence

| File | Description | Conclusion |
|------|-------------|------------|
| `z2_protein_esmfold.pdb` | ESMFold prediction | RMSD = 13.7 Å from designed |
| `z2_protein_validation.json` | Full validation metrics | HALLUCINATION confirmed |
| `esmfold_cache/` | 375 sequence predictions | All disordered |

---

## Key Lessons

1. **Orthogonal validation is mandatory** - The original design looked mathematically perfect but ESMFold immediately showed it doesn't fold.

2. **Fitness functions can be gamed** - Optimizing for Z² alignment produced structures that satisfied the math but violated biology.

3. **Random sequences don't fold** - 0/375 random mutations produced foldable proteins. Evolution had to search astronomically to find natural folds.

4. **De novo design requires inverse folding** - Start from a known backbone (ProteinMPNN), not from random sequence space.

---

## Why Keep This?

1. **Scientific honesty** - These failures are part of the research record
2. **Prevent repetition** - Others can see what didn't work
3. **Negative data is data** - The 0/375 foldable result is informative
4. **Reproducibility** - Anyone can verify the hallucination

---

*"The first principle is that you must not fool yourself — and you are the easiest person to fool."*

— Richard Feynman
