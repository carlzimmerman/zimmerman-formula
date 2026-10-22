# D8b provenance

The three tables are copies of files in the Stilp et al. 2013 LaTeX source (ApJ 765, 136; arXiv:1301.1989v2). That source was
already on disk under `_external_data/d8_stilp2013_2026_10_22/src/`. The owner OK'd the fetch, and D8's `PROVENANCE.md` records it
(tarball sha256 fdbd3bad...). Nothing new was downloaded. The tables are parsed as text with `python3 -I`.

| committed copy | source file | sha256 |
|---|---|---|
| stilp2013_table-derived-properties.tex | table-derived-properties.tex | 4673d84985696d64a9786ffefed907ce4c85f7b7e7233ca04bf2bcd8b3e5bc54 |
| stilp2013_table-sample.tex | table-sample.tex | 835fef56f5d4018e997857f3b251874fd431ff9df9b1f24d58b54c1451e9be23 |
| stilp2013_table-correlations.tex | table-correlations.tex | 01c95604dc5cf6762f611c01ebd43bd29c91d925c7eb02548cddbb34a9174046 |

The σ table is D8's committed copy, `../D8_Lstar_value/stilp2013_table-measurements.tex` (sha256 155d780c...).
I read the correlations table only after the frozen criteria were committed (97ec7892fa). It is public catalogue data with no personal information.
