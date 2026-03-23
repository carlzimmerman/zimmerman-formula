# arXiv Submission Guide

## Quick Submit (Manual - Required by arXiv)

arXiv requires human verification for all submissions. Here's the fastest process:

### Step 1: Compile the Paper (if not using GitHub Actions)
```bash
cd papers/
pdflatex deriving_mond_scale.tex
pdflatex deriving_mond_scale.tex  # Run twice for references
```

### Step 2: Submit to arXiv

1. Go to https://arxiv.org/submit
2. Login (or create account if needed)
3. Choose category: **gr-qc** (General Relativity and Quantum Cosmology)
   - Cross-list to: **astro-ph.CO** (Cosmology and Nongalactic Astrophysics)
4. Upload: `deriving_mond_scale.tex`
5. Fill metadata:
   - **Title**: Deriving the MOND Acceleration Scale from Horizon Thermodynamics
   - **Authors**: Carl Zimmerman
   - **Abstract**: (copy from paper)
   - **Comments**: 6 pages, 1 table

### Step 3: Wait for Processing
- arXiv reviews submissions (usually 1-2 days)
- First submission may need endorsement for gr-qc

---

## Suggested Abstract (copy-paste ready)

```
We present a first-principles derivation of the MOND acceleration scale
a_0 ≈ 1.2×10^{-10} m/s^2 from general relativistic cosmology and horizon
thermodynamics. The derivation yields a_0 = cH_0/Z where Z = 2√(8π/3) = 5.7888.
This geometric constant emerges naturally: the factor √(8π/3) comes from the
Friedmann equation relating the Hubble parameter to critical density, while
the factor of 2 arises from the horizon mass via the Bekenstein bound. The
result predicts a_0 should evolve with redshift as a_0(z) = a_0(0)×E(z),
where E(z) = √(Ω_m(1+z)^3 + Ω_Λ). This evolution is potentially testable
with high-redshift kinematic observations from JWST.
```

---

## Alternative: Zenodo (Automatic!)

Zenodo gives you a citable DOI automatically:

1. Go to https://zenodo.org/account/settings/github/
2. Login with GitHub
3. Enable the `zimmerman-formula` repository
4. Every GitHub Release automatically gets a DOI

The GitHub Action in this repo creates releases automatically when you push to `papers/`.

---

## Files for Submission

| File | Purpose |
|------|---------|
| `deriving_mond_scale.tex` | Main LaTeX source |
| `deriving_mond_scale.pdf` | Compiled PDF |

No figures needed - the paper is self-contained.

---

## Category Recommendations

**Primary**: gr-qc (General Relativity and Quantum Cosmology)
- Best fit: derives physics from GR + thermodynamics

**Cross-list**:
- astro-ph.CO (Cosmology) - for the H(z) evolution prediction
- astro-ph.GA (Galaxies) - for MOND/galaxy dynamics connection

---

## If You Need Endorsement

For first-time submissions to gr-qc, you may need an endorser. Options:
1. Ask Lucas Lombriser (if he's willing)
2. Submit first to astro-ph.GA (often doesn't require endorsement)
3. Use Zenodo for immediate DOI while waiting for arXiv endorsement
