# How to publish "The Zimmerman Theory of Gravity" to Zenodo (manual)

Step-by-step to turn the paper into a Zenodo record yourself. You upload the PDF and paste the metadata — nothing here is automated.

## Files in this folder (`real_research/papers/`)
- `ZIMMERMAN_THEORY_OF_GRAVITY.md` — the paper (source of truth, ~8,500 words, 16 sections + 3 appendices, 8 figures).
- `ZIMMERMAN_THEORY_OF_GRAVITY.tex` — Overleaf-ready LaTeX (auto-generated from the .md by pandoc; all Unicode mapped).
- `unicode_header.tex` — the Unicode/compile header the .tex already includes (only needed if you regenerate the .tex).
- `figures/` — the eight figures:
  `fig1_rar.png`, `fig2_a0z.png`, `fig3_btfr.png`, `fig4_threelaw.png`, `fig5_seesaw.png`,
  `fig6_derivation_ladder.png`, `fig7_confirmation_ladder.png`, `fig8_galaxy_cluster_split.png`.
- `zimmerman_theory_charts.py` — regenerates figures 2, 4, 5, 6, 7, 8 (figures 1 and 3 are the SPARC data plots).
- `ZIMMERMAN_THEORY_OF_GRAVITY.zenodo.json` — the metadata, machine-readable.

## Step 1 — make the PDF on Overleaf
**Easiest (foolproof):** locally zip the whole `real_research/papers/` folder and use Overleaf **New Project → Upload Project** on the zip — it keeps the `figures/` folder intact, so the images just work. Then jump to step 3.

Otherwise, manually:
1. Overleaf → **New Project → Upload Project** (or a blank project), and upload **`ZIMMERMAN_THEORY_OF_GRAVITY.tex`**.
2. Upload **all eight PNGs**. They can go in a folder named **`figures/`** **or** directly in the project root — the `.tex` finds them in both (it sets `\graphicspath`).
3. Menu → Compiler → **XeLaTeX** (recommended; pdfLaTeX also works — every glyph is mapped both ways).
4. Recompile, then **Download → PDF**. That PDF is what you upload to Zenodo.

## Step 2 — create the Zenodo record
1. zenodo.org → **New upload**.
2. **Upload files:** the PDF from Step 1. (Optional but nice: also drag in `ZIMMERMAN_THEORY_OF_GRAVITY.md`, `ZIMMERMAN_THEORY_OF_GRAVITY.tex`, and the eight figures so the record is self-contained.)
3. Fill the metadata using the table below.
4. **Publish.** Zenodo mints the DOI.

> This is a *new, distinct* work from the earlier Zenodo record (DOI 10.5281/zenodo.19244651). Publish it as a **new record** (not a new version of the old one), unless you specifically want to supersede that DOI.

## Step 3 — the metadata to paste

| Field | Value |
|---|---|
| **Upload type** | Publication → Preprint |
| **Title** | The Zimmerman Theory of Gravity: The Galaxy Acceleration Scale Is Set by the Cosmological Constant (a₀ = c²√(Λ/32π)) |
| **Authors** | Zimmerman, Carl P. — Briar Creek Tech |
| **Description** | *(paste the abstract paragraph below)* |
| **Version** | comprehensive edition (2026-06-06) |
| **Language** | English |
| **Keywords** | modified gravity; MOND; dark sector; dark energy; cosmological constant; radial acceleration relation; baryonic Tully–Fisher relation; galaxy rotation curves; de Sitter horizon; emergent gravity; modified inertia; acceleration scale a0; external field effect; DESI; SPARC |
| **License** | **Choose one** — `CC-BY-4.0` (standard for an open-access manuscript, recommended) **or** `AGPL-3.0-or-later` (to match the repository's code license). |
| **Related identifiers** | "is supplemented by this upload": `https://github.com/carlzimmerman/zimmerman-formula` |
| **Notes** | All quantitative claims are reproducible: clone the repo, `pip install numpy scipy astropy`, run the scripts in `real_research/`. |

### Abstract (paste into Description)
The dynamics of galaxies require either unseen matter or a modification of gravity below a characteristic acceleration a₀ ≈ 1.2×10⁻¹⁰ m s⁻². This scale numerically coincides with c√Λ and with cH₀ — a coincidence ΛCDM treats as accidental. The Zimmerman Theory of Gravity proposes that the coincidence is causal: the acceleration scale is set by the cosmological constant, a₀ = c²√(Λ/32π) = (c/2)√(Gρ_Λ) = cH_Λ/Z, with Z = √(32π/3) = 5.789, evaluated on the dark-energy density alone, giving a₀ = 9.36×10⁻¹¹ m s⁻². The paper assembles both the empirical confrontation (at this single a₀ and Υ≈0.70 the Radial Acceleration, Baryonic Tully–Fisher, and deep-MOND mass-discrepancy relations agree to 8%; the rising a₀∝cH rival is excluded; the ΛCDM-impossible External Field Effect leans the predicted way) and the theoretical foundation: the deep-MOND shape is derived (Milgrom's de Sitter–Unruh modified inertia), the existence of a₀ is supplied volume-law-free by that route, the galaxy-scale sign is forced by a computed DSSYK kernel that also predicts the cluster failure, the value of Λ is welded to a₀ as one Cohen–Kaplan–Nelson seesaw, and the evolving dark energy is string-swampland-compatible where ΛCDM is forbidden. The limits are stated equally plainly: the O(1) coefficient is a posit, the covariant completion is unwritten, and this is a theory of gravity and the dark sector — not a theory of everything. The distinctive prediction — a₀(z=3) = 0.74 a₀(0), a declining acceleration scale tracking the dark-energy density — is falsifiable with ELT-class spectroscopy this decade.

## Regenerating the .tex (only if you edit the .md)
```
cd real_research/papers
bash build_tex.sh
```
This runs pandoc and applies the Overleaf-compatibility fixes (strips `alt=`, makes the figure paths bare so they resolve in `figures/` **or** the project root).
