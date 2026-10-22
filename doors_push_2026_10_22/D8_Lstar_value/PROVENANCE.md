# D8 provenance: Stilp et al. 2013 superprofile table (fetched with the owner's OK, 2026-10-22)

- **Paper:** Stilp, Dalcanton, Warren, Skillman, Ott & Koribalski 2013, "Global HI Kinematics in Dwarf Galaxies",
  ApJ 765, 136; arXiv:1301.1989v2. VLA-ANGST + THINGS dwarfs, HI cubes smoothed to a common 200 pc beam,
  velocity resolution 0.6–2.6 km/s (paper §2).
- **Table:** Table "Measured Superprofile Parameters" (`\label{tab:measurements}`), 23 galaxies. Columns used:
  (2) ⟨σ_m2⟩, the intensity-weighted global HI second moment; (3) σ_central, the width of the central
  superprofile peak (secondary).
- **Source URL:** https://arxiv.org/e-print/1301.1989v2 (the authors' LaTeX source). It is not on VizieR:
  J/ApJ/773/88, J/AJ/144/96, J/MNRAS/466/4159 and J/AJ/151/15 returned no metadata; the Iorio+2017 ReadMe URL
  returned 404.
- **Retrieved:** 2026-10-22T18:17Z, with curl.
- **sha256:**
  - tarball `_external_data/d8_stilp2013_2026_10_22/arXiv_1301.1989v2_src`:
    `fdbd3badbf7b6b031e395109e71f01ab19a1546a0339eea1b9cee27b628f1bb0`
  - committed copy `stilp2013_table-measurements.tex`:
    `155d780cf9064d904529b04924d431519b065933b6844fdc34fce220dfdd5ac1`
- **Handling:** the tarball sits in its own new directory. Only `*.tex` files were extracted and nothing was
  executed. The table is parsed as text with `python3 -I`. The raw tarball is not committed (`_external_data/`).
- An empty directory `_external_data/d8_iorio2017_2026_10_22/` remains from the failed Iorio attempt. It is
  empty and was not deleted (no-delete rule).
- Public catalogue data. No personal information.
