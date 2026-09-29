# Where the GOODS-S ALMA catalogues are hosted (data front, 2026-09-29; read-only search, no downloads)

Question: where can the GOODS-ALMA source catalogue be obtained, so the 22 KURVS-CDFS positions (`arxiv_tables/kurvs_positions/`) can be cross-matched?
Everything below is from HTML pages, abstracts and search results; no table was downloaded. "Not found" means not found by me, not that it does not exist.

| catalogue | where I found it | status |
|---|---|---|
| GOODS-ALMA 2.0 (Gomez-Guijarro+2022, A&A 658, A43; arXiv:2106.13246) | the 88-source catalogue is printed in the paper's Tables 2 and 3 (arXiv HTML page, per the page summary); neither the arXiv HTML nor the Caltech record states a separate hosting site | **in the paper only.** Not on VizieR under J/A+A/658/A43 (ReadMe not found; TAP table-name search empty). Publisher pages (aanda.org) return HTTP 403 and were not bypassed. Raw ALMA data: programmes 2015.1.00543.S and 2017.1.00755.S (ALMA archive) |
| GOODS-ALMA 1.0 (Franco+2018, A&A 620, A152; arXiv:1803.00157) | Table 3 of the paper; no data-availability statement | in the paper only; not on VizieR under J/A+A/620/A152 |
| ASAGAO (Hatsukade+2018, PASJ 70, 105; arXiv:1808.04502) | project site https://sites.google.com/view/asagao26/home (no download links; says to contact the PI); Zenodo 10.5281/zenodo.3629310 is only a slide presentation, not data | catalogue in the paper only; the site quotes a ~5′×5′ field and 0.06 mJy/beam rms at 1.2 mm; centre not stated |
| A3GOODSS (Adscheid+2024, arXiv:2403.03125) | its arXiv abstract says the catalogues are on CDS and on https://sites.google.com/view/a3cosmos; ~4,000 archival ALMA continuum images over COSMOS + GOODS-S, 2,050 unique sources | **the one compiled, machine-readable route found** (covers archival ALMA in GOODS-S, which includes GOODS-ALMA data). I did not find its VizieR table name (a description search returned only the 2019 A3COSMOS table J/ApJS/244/40), so it is unconfirmed on VizieR |
| ASPECS 1.2 mm (arXiv:2006.04284) | abstract only | not looked into |

## Routes to the cross-match, cheapest first
1. **Read the tables from the GOODS-ALMA 2.0 arXiv HTML page** (HTML read, no file download): 88 rows, coordinates plus 1.1 mm flux and S/N. This is what my user approved earlier in kind (HTML reading); the page summariser may drop rows, so every row I use is re-read against the printed table.
2. **The paper's LaTeX source from arXiv** (a small tarball, as done for KURVS and others): exact table text, needs the owner's go with filename, source and size stated first.
3. **A3GOODSS on CDS** for archival ALMA sources in the same field: needs its VizieR name first.
None of these supplies a local map rms at each KURVS position; that needs the maps (ALMA archive or the survey team), not the catalogues.
