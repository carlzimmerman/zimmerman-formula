# Zenodo Upload Instructions for "The Zimmerman Formula Proofs"

## Quick PDF Creation

Since LaTeX isn't installed, use one of these methods:

### Option 1: Online Converter (Easiest)
1. Go to https://md2pdf.netlify.app/ or https://www.markdowntopdf.com/
2. Paste contents of `ZIMMERMAN_FORMULA_PROOFS_PDF.md`
3. Download PDF

### Option 2: VS Code Extension
1. Install "Markdown PDF" extension in VS Code
2. Open `ZIMMERMAN_FORMULA_PROOFS_PDF.md`
3. Cmd+Shift+P → "Markdown PDF: Export (pdf)"

### Option 3: Print HTML to PDF
1. Open `paper/ZIMMERMAN_FORMULA_PROOFS.html` in Chrome/Safari
2. File → Print → Save as PDF

### Option 4: Typora (if installed)
1. Open `ZIMMERMAN_FORMULA_PROOFS_PDF.md` in Typora
2. File → Export → PDF

---

## Zenodo Metadata

### Upload Type
**Publication → Preprint**

### Basic Information

**Title:**
```
The Zimmerman Formula Proofs: Applications to 25 Unsolved Problems in Astrophysics and Cosmology
```

**Authors:**
```
Zimmerman, Carl
```

**Publication Date:**
```
2026-03-19
```

**DOI:** (Leave blank - Zenodo will assign one, or reserve one first)

### Description (Abstract)

```
We present detailed derivations and quantitative predictions for 25 applications of the Zimmerman Formula to unsolved problems in astrophysics and cosmology. The Zimmerman Formula derives the MOND acceleration scale from cosmological first principles:

a₀ = c√(Gρc)/2 = cH₀/5.79

where the coefficient 5.79 = 2√(8π/3) emerges naturally from the Friedmann equation. The formula achieves 0.5% precision in predicting the observed a₀ value and makes a key testable prediction: the acceleration scale evolves with redshift as a₀(z) = a₀(0) × E(z), where E(z) = √(Ωm(1+z)³ + ΩΛ).

This paper documents applications including:
- Tier 1 (Definitive): Cosmic coincidence problem, Hubble tension
- Tier 2 (Strong): JWST early galaxies, El Gordo cluster, BTFR evolution, early black holes, S8 tension
- Tier 3 (Clear): Downsizing, galaxy size evolution, satellite planes, RAR, ultra-diffuse galaxies, core-cusp, missing baryons
- Tier 4 (Testable): BAO, Lyman-α forest, cosmic web, void galaxies, peculiar velocities, 21cm cosmology, globular clusters

The formula has been validated against 175 SPARC galaxies (BTFR slope = 4.000 exactly) and JWST z > 6 kinematics (2× better χ² than constant a₀). It predicts H₀ = 71.5 km/s/Mpc from local a₀, intermediate between Planck (67.4) and SH0ES (73.0).

This is a companion paper to the main Zimmerman Formula publication (DOI: 10.5281/zenodo.14961024).
```

### Keywords
```
MOND
Modified Newtonian Dynamics
acceleration scale
cosmology
galaxy dynamics
Hubble tension
dark matter
modified gravity
JWST
galaxy rotation curves
```

### Additional Metadata

**Language:** English

**License:** Creative Commons Attribution 4.0 International (CC BY 4.0)

**Related Identifiers:**
- **Is supplement to:** 10.5281/zenodo.14961024 (The Zimmerman Formula main paper)
- **Is documented by:** https://github.com/carlzimmerman/zimmerman-formula

**Grants:** (Leave blank unless you have funding)

### Subjects
```
Astrophysics
Cosmology
Galaxy dynamics
Modified gravity
```

### Version
```
1.0.0
```

---

## Files to Upload

1. **ZIMMERMAN_FORMULA_PROOFS.pdf** (create using instructions above)

2. Optionally also upload:
   - **ZIMMERMAN_FORMULA_PROOFS_PDF.md** (source markdown)

---

## After Upload

1. Copy the new DOI
2. Update README.md with the new DOI badge
3. Update the GitHub repo to reference both DOIs

### README Badge Code:
```markdown
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
```

---

## Linking to Original Paper

In the Zenodo "Related identifiers" section, add:

| Relation | Identifier | Scheme |
|----------|------------|--------|
| Is supplement to | 10.5281/zenodo.14961024 | DOI |
| Is documented by | https://github.com/carlzimmerman/zimmerman-formula | URL |

This creates a formal link between the two publications.
