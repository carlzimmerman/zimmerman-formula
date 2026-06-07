# How to publish "The Zimmerman Law of Gravity" to Zenodo (manual)

This is the step-by-step to turn the comprehensive paper into a Zenodo record yourself. Nothing here is automated — you upload the PDF and paste the metadata.

## Files in this folder
- `ZIMMERMAN_LAW_OF_GRAVITY.md` — the paper (source of truth, ~8,600 words, 16 sections + 4 appendices).
- `ZIMMERMAN_LAW_OF_GRAVITY.tex` — Overleaf-ready LaTeX (auto-generated from the .md by pandoc; all Unicode mapped).
- `unicode_header.tex` — the Unicode/compile header the .tex already includes (only needed if you regenerate the .tex).
- `figures/fig1_rar.png`, `figures/fig2_a0z.png`, `figures/fig3_btfr.png` — the three figures.
- `ZIMMERMAN_LAW_OF_GRAVITY.zenodo.json` — the metadata, machine-readable (copy/paste from here or use the table below).

## Step 1 — make the PDF on Overleaf
1. New Project → Upload Project (or blank project), and upload **`ZIMMERMAN_LAW_OF_GRAVITY.tex`**.
2. Create a folder named **`figures/`** and upload the three PNGs into it (`fig1_rar.png`, `fig2_a0z.png`, `fig3_btfr.png`).
3. Menu → Compiler → **XeLaTeX** (recommended; pdfLaTeX also works — every glyph is mapped both ways).
4. Recompile, then **Download → PDF**. That PDF is what you upload to Zenodo.

## Step 2 — create the Zenodo record
1. zenodo.org → **New upload**.
2. **Upload files:** the PDF from Step 1. (Optional but nice: also drag in `ZIMMERMAN_LAW_OF_GRAVITY.md`, `ZIMMERMAN_LAW_OF_GRAVITY.tex`, and the three figures as supplementary files so the record is self-contained.)
3. Fill the metadata using the table below.
4. **Publish.** Zenodo mints the DOI.

> Note: this is a *new, distinct* work from the earlier Zenodo record (DOI 10.5281/zenodo.19244651), which was the older "Z² unified framework." This paper is the gravity-only result and explicitly **retracts** the particle-physics numerology that record contained (see §13 and `RETRACTIONS.md`). Publish it as a **new record** (not a new version of the old one), unless you specifically want to supersede the old DOI.

## Step 3 — the metadata to paste

| Field | Value |
|---|---|
| **Upload type** | Publication → Preprint (or Article) |
| **Title** | The Zimmerman Law of Gravity: The Galaxy Acceleration Scale Is Set by the Cosmological Constant (a₀ = c²√(Λ/32π)) |
| **Authors** | Zimmerman, Carl P. — Briar Creek Tech |
| **Description** | *(use the abstract — paste the paragraph below)* |
| **Version** | v2 — comprehensive edition (2026-06-06) |
| **Language** | English |
| **Keywords** | modified gravity; MOND; dark sector; dark energy; cosmological constant; radial acceleration relation; baryonic Tully–Fisher relation; galaxy rotation curves; de Sitter horizon; emergent gravity; modified inertia; acceleration scale a0; external field effect; DESI; SPARC |
| **License** | **Choose one** — `CC-BY-4.0` (standard for an open-access manuscript, recommended) **or** `AGPL-3.0-or-later` (to match the repository's code license). |
| **Related identifiers** | "is supplemented by this upload": `https://github.com/carlzimmerman/zimmerman-formula` (the code + data that reproduce every number). |
| **Notes** | All quantitative claims are reproducible: clone the repo, `pip install numpy scipy astropy`, run the scripts in `real_research/`. |

### Abstract (paste into Description)
The dynamics of galaxies require either unseen matter or a modification of gravity below a characteristic acceleration a₀ ≈ 1.2×10⁻¹⁰ m s⁻². This scale numerically coincides with c√Λ and with cH₀ — a coincidence ΛCDM treats as accidental. The Zimmerman Law of Gravity proposes that the coincidence is causal: the acceleration scale is set by the cosmological constant, a₀ = c²√(Λ/32π) = (c/2)√(Gρ_Λ) = cH_Λ/Z, with Z = √(32π/3) = 5.789, evaluated on the dark-energy density alone, giving a₀ = 9.36×10⁻¹¹ m s⁻². The paper assembles both the empirical confrontation (at this single a₀ and Υ≈0.70 the Radial Acceleration, Baryonic Tully–Fisher, and deep-MOND mass-discrepancy relations agree to 8%; the rising a₀∝cH rival is excluded; the ΛCDM-impossible External Field Effect leans the predicted way) and the theoretical foundation: the deep-MOND shape is derived (Milgrom's de Sitter–Unruh modified inertia), the existence of a₀ is supplied volume-law-free by that route, the galaxy-scale sign is forced by a computed DSSYK kernel that also predicts the cluster failure, the value of Λ is welded to a₀ as one Cohen–Kaplan–Nelson seesaw, and the evolving dark energy is string-swampland-compatible where ΛCDM is forbidden. The limits are stated equally plainly: the O(1) coefficient is a posit, the covariant completion is unwritten, and this is a theory of gravity and the dark sector — not a theory of everything (every geometric formula for a Standard-Model constant is retracted numerology). The distinctive prediction — a₀(z=3) = 0.74 a₀(0), a declining acceleration scale tracking the dark-energy density — is falsifiable with ELT-class spectroscopy this decade.

## Regenerating the .tex (only if you edit the .md)
```
cd real_research/papers
pandoc ZIMMERMAN_LAW_OF_GRAVITY.md -s --include-in-header=unicode_header.tex -o ZIMMERMAN_LAW_OF_GRAVITY.tex
```
