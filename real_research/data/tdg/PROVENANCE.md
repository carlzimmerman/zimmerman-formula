# Tidal dwarf galaxies — provenance

`lelli2015_tdgs.csv` — transcribed 2026-09-03 for hunt item 46 (`hunt_2026/h46_tdg_btfr.py`) from the
**authors' own LaTeX tables** in the arXiv source package of

> **Lelli et al. 2015, A&A 584, A113** — "Gas dynamics in tidal dwarf galaxies: disc formation at z = 0"
> — arXiv:1509.05404

    curl https://arxiv.org/e-print/1509.05404   ->  TDGs.tex, Tables 2 (tab:TDGkin), 4 (tab:budget), 5 (tab:MOND)

VizieR carries only the FITS data cubes for this paper (J/A+A/584/A113/list), not the derived quantities,
so the numbers come from the paper source.  Six bona-fide TDGs around NGC 4694, NGC 5291 and NGC 7252.

The file deliberately also carries the paper's OWN MOND predictions (`VISO1, VEFE1` for the n = 1
interpolation function at its a0 = 1.30e-10 m/s^2).  That function is identical to this repository's
Route A kernel, so those columns are a published cross-check that the script must reproduce before it is
allowed to quote anything at the repository's own a0 footings.

Public data from the published paper.  No personal information.
