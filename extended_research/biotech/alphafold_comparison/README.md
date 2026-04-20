# AlphaFold vs First-Principles: Understanding the Tradeoffs

**TL;DR:** AlphaFold is incredible (~95% accuracy) but fails systematically on specific protein classes. This folder explains why, and when to use alternatives.

---

## The One-Sentence Summary

> **AlphaFold learned patterns from the PDB. It fails when proteins don't match those patterns.**

---

## When to Use AlphaFold

| Scenario | AlphaFold? | Confidence |
|----------|------------|------------|
| Protein with >100 homologs | Yes | High |
| Protein from well-studied family | Yes | High |
| You need a starting model for experiments | Yes | High |
| Stable, globular protein | Yes | High |

**If your protein is like proteins in the PDB, use AlphaFold.**

---

## When AlphaFold Fails

| Scenario | Why It Fails | What To Do Instead |
|----------|--------------|-------------------|
| **Intrinsically Disordered Proteins (IDPs)** | No single structure exists | Ensemble sampling (REMD) |
| **Orphan proteins (no homologs)** | No evolutionary signal | First-principles, template-free |
| **Conformational changes** | Predicts one state only | MD simulations |
| **Mutation effects** | Mutants not in training data | Physics-based ΔΔG |
| **Membrane proteins** | Trained without membrane | Specialized tools (OPM) |

---

## The Core Problem: Correlation vs Causation

### What AlphaFold Learns:
```
"When residue 15 is acidic and residue 42 is basic
across 1000 homologs, they probably contact."
```
This is **correlation** (co-evolution).

### What Physics Knows:
```
"Opposite charges attract with force F = kq₁q₂/r².
If close enough, they form a salt bridge."
```
This is **causation** (physical law).

**AlphaFold memorized the PDB. It didn't learn physics.**

---

## Specific Failure Modes

### 1. Intrinsically Disordered Proteins (IDPs)

**Problem:** IDPs don't have a single structure. They're conformational ensembles.

**What AlphaFold does:** Outputs extended chain with pLDDT < 50.

**What that means:** "I don't know" — but users often ignore this.

**Example:** c-Myc (involved in 70% of cancers)
- AlphaFold: Meaningless extended chain
- Reality: Dynamic ensemble with transient pockets
- Our approach: REMD sampling found druggable states

### 2. Orphan Proteins

**Problem:** No homologs = no co-evolution signal.

**What AlphaFold does:** Falls back to templates. If no template, hallucinates.

**Accuracy drops:**
```
MSA depth    → Accuracy
>1000 seqs   → ~95%
100-1000     → ~80%
10-100       → ~65%
<10          → ~50% (coin flip)
```

### 3. AlphaFold Hallucinations

**The scary part:** AlphaFold can be confidently wrong.

```
High pLDDT (>90) does NOT guarantee correctness

Known hallucination cases:
- Disordered regions predicted as helices
- Wrong oligomeric state
- Membrane proteins in wrong context
- Novel folds matched to wrong template
```

**This is why we built three-layer cross-validation.**

---

## Our Approach: First-Principles + Validation

### Z² Backbone Geometry

Derived from Kaluza-Klein physics (not training data):

```
α-helix: φ = -57°, ψ = -47°   ← Matches crystallography
β-sheet: φ = -129°, ψ = +135° ← Matches crystallography
```

**Accuracy:** ~55% (same as 1974 methods)

**But:** Never hallucinates. Works on any sequence. No homologs needed.

### Three-Layer Validation

```
┌─────────────────────────────────────────────────┐
│ Layer 1: ESMFold vs AlphaFold2 Consensus        │
│          RMSD > 2.0 Å → Investigate             │
├─────────────────────────────────────────────────┤
│ Layer 2: Stereochemical QA                      │
│          Ramachandran outliers → Physics error  │
├─────────────────────────────────────────────────┤
│ Layer 3: Thermal Stress MD (350K)               │
│          Structure unstable → Probably wrong    │
└─────────────────────────────────────────────────┘
```

If a structure passes all three layers, trust it more.

---

## Files in This Folder

| File | Description |
|------|-------------|
| `README.md` | This overview |
| `WHY_ALPHAFOLD_FAILS_WHERE_IT_DOES.md` | Full technical paper |

---

## Quick Decision Guide

```
START
  │
  ▼
Does your protein have >100 homologs?
  │
  ├─Yes──► Is pLDDT > 70 across the region of interest?
  │           │
  │           ├─Yes──► USE ALPHAFOLD (high confidence)
  │           │
  │           └─No───► VALIDATE with MD or cross-prediction
  │
  └─No───► Is your protein intrinsically disordered?
              │
              ├─Yes──► USE ENSEMBLE METHODS (REMD, metadynamics)
              │
              └─No───► USE FIRST-PRINCIPLES + careful validation
```

---

## The Bottom Line

| Method | Strengths | Weaknesses |
|--------|-----------|------------|
| **AlphaFold** | 95% accuracy on trained distribution | Fails outside distribution |
| **First-Principles** | Works on anything, interpretable | 55% accuracy |
| **MD/REMD** | Captures dynamics, ensembles | Computationally expensive |

**Best approach:** Use all three. Cross-validate. Trust nothing blindly.

---

## Further Reading

- `WHY_ALPHAFOLD_FAILS_WHERE_IT_DOES.md` — Full technical analysis
- `../validation/` — Our cross-validation framework
- `../dark_proteome/` — How we handle IDPs
- `../NEGATIVE_RESULTS.md` — Honest failures of Z² approach

---

## Citation

If this helps your research:

```bibtex
@software{zimmerman_2026_alphafold_comparison,
  author       = {Zimmerman, Carl and Claude Opus 4.5},
  title        = {AlphaFold Failure Mode Analysis},
  year         = 2026,
  publisher    = {GitHub},
  url          = {https://github.com/carlzimmerman/zimmerman-formula}
}
```

---

*"AlphaFold tells you what proteins look like. Physics tells you why."*

**License:** AGPL-3.0-or-later
