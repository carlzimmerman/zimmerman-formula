# Zenodo Upload Instructions for Version 8.0

## Summary of Changes from v7 to v8

**Major revisions for honesty and rigor:**

1. **Removed claim of "36 parameters derived"** — Previous version overclaimed; many were empirical fits
2. **Added T³/division algebra derivation** — New rigorous section on SM=Cube correspondence
3. **Clear derivation status** — Each claim now has honest confidence level (100%, ~80%, ~50%)
4. **Removed numerological formulas** — Specific formulas lacking derivation (Z^21.5, 50°, etc.)
5. **Separated derived vs empirical** — Clear distinction throughout

---

## PDF Creation

### Option 1: Online Converter (Easiest)
1. Go to https://md2pdf.netlify.app/ or https://www.markdowntopdf.com/
2. Paste contents of `ZIMMERMAN_UNIFIED_THEORY_v8.md`
3. Download PDF

### Option 2: VS Code Extension
1. Install "Markdown PDF" extension in VS Code
2. Open `ZIMMERMAN_UNIFIED_THEORY_v8.md`
3. Cmd+Shift+P → "Markdown PDF: Export (pdf)"

---

## Zenodo Metadata

### Upload Type
**Publication → Preprint** (Update of existing record)

### Basic Information

**Title:**
```
The Zimmerman Framework: Geometric Foundations of the Standard Model (v8.0 - Rigorous Edition)
```

**Authors:**
```
Zimmerman, Carl
```

**Publication Date:**
```
2026-04-13
```

### Description (Abstract)

```
Version 8.0 provides a rigorous reassessment of the Zimmerman Framework, clearly distinguishing derived results from empirical observations.

RIGOROUSLY DERIVED:
• Z = 2√(8π/3) from Einstein's Friedmann equations
• Bekenstein factor 4 from black hole thermodynamics
• g_H = cH/2 from Newtonian gravity at Hubble radius
• N_gen = b₁(T³) = 3 from Atiyah-Singer index theorem on 3-torus
• dim(SU(3)) = 8 from octonion automorphism structure
• rank(G_SM) = 4 = dim(H) from quaternion dimension

NEW IN THIS VERSION:
This edition introduces the T³ and division algebra derivation explaining WHY the Standard Model structure (8, 12, 4, 3) equals the cube structure (vertices, edges, body diagonals, face pairs). The 3-torus T³ has the cube as its fundamental domain, and its first Betti number b₁ = 3 gives the number of fermion generations through the index theorem.

PHYSICALLY MOTIVATED (needs further work):
• a₀ = cH/Z — MOND acceleration scale (testable via JWST high-z kinematics)
• α⁻¹ = 4Z² + 3 = 137.04 — Fine structure constant structure

HONEST ASSESSMENT:
Many formulas in previous versions lacked rigorous derivation and have been removed or clearly labeled as empirical observations. This version prioritizes theoretical integrity over parameter count.

Key testable prediction: The MOND acceleration scale evolves with redshift as a₀(z) = a₀(0) × E(z), distinguishing this framework from constant-a₀ MOND.
```

### Keywords
```
cosmology
gauge theory
fine structure constant
division algebras
octonions
3-torus
T3 compactification
index theorem
Standard Model
cube geometry
Friedmann equation
MOND
```

### Additional Metadata

**Language:** English

**License:** Creative Commons Attribution 4.0 International (CC BY 4.0)

**Related Identifiers:**
- **Is new version of:** 10.5281/zenodo.19121510 (v7)
- **Is documented by:** https://github.com/carlzimmerman/zimmerman-formula

### Version
```
8.0.0
```

### Release Notes
```
v8.0 - Rigorous Edition (April 2026)
- Added T³/division algebra derivation for SM=Cube correspondence
- Clear categorization of derived vs empirical results
- Removed numerological formulas lacking derivation
- Honest confidence levels for all claims
- Focus on what IS derived rather than overclaiming
```

---

## Files to Upload

1. **ZIMMERMAN_UNIFIED_THEORY_v8.pdf** (create using instructions above)
2. **ZIMMERMAN_UNIFIED_THEORY_v8.md** (source markdown)

---

## After Upload

1. Copy the new DOI
2. Update README.md with the new version
3. Update GitHub repo to reference v8

---

## What Was Removed from v7

The following claims from v7 were removed or clearly labeled as empirical because they lack rigorous first-principles derivation:

- α_s = Ω_Λ/Z (no derivation for why this should hold)
- sin²θ_W = 1/4 - α_s/(2π) (the 2π is unexplained)
- M_Pl = 2v × Z^21.5 (the exponent 21.5 is unexplained)
- H₀ = c/(l_Pl × Z⁸⁰) × √(π/2) (the exponent 80 is unexplained)
- γ = π/3 + α_s × 50° (the 50° factor is unexplained)
- Many fermion mass formulas with specific exponents
- λ_H = (Z-5)/6 (the constants 5 and 6 are unexplained)
- Λ_QCD = v/(Z × 200) (the 200 is unexplained)
- PMNS corrections with α_em × π
- Various other specific numerical relationships

**These may represent genuine physics or may be numerical coincidences. Honest science requires acknowledging this uncertainty.**

---

## What Was Added in v8

1. **T³ Topology Section** — The 3-torus as internal compact space
2. **Division Algebra Connection** — Octonions → SU(3), Quaternions → rank
3. **Index Theorem Derivation** — N_gen = b₁(T³) = 3
4. **SM=Cube Correspondence** — (8,12,4,3) matching explained
5. **Derivation Status Framework** — Clear confidence levels
6. **Honest Assessment Section** — What IS and IS NOT derived
7. **Testable Predictions** — Clear falsification criteria
