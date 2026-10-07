# CFG395 fetch log (all 2026-10-06; data fetches approved by the owner for this lane)

| # | URL | bytes | sha256 | kept |
|---|---|---|---|---|
| 1 | https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=J/A%2BA/581/A98&-out.max=5 | 2,555,904 | not computed (discarded) | no: VizieR has no J/A+A/581/A98; the reply was a fuzzy match over unrelated catalogues |
| 2 | https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=J/A%2BA/581/A98*&-meta | small | n/a | no: "Table or Catalog not found" |
| 3 | https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=J/ApJ/836/152&-meta | small | n/a | no: not found (Lelli+2017) |
| 4 | https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=J/MNRAS/460/1382&-meta | small | n/a | no: not found (Serra+2016) |
| 5 | https://export.arxiv.org/api/query (two metadata queries: Serra+Oosterloo; id 1610.08981) | small | n/a | no |
| 6 | https://arxiv.org/e-print/1509.05236 (den Heijer+2015) | 378,431 | c262ba093920f625833a139671ed408b6ab1c679139b1b4d47f1890ed83a5ad9 | not committed; identical hash to CFG37's fetch; confirms there are no rotation curves, one outer point per galaxy |
| 7 | https://arxiv.org/e-print/1604.07902 (Serra+2016) | 782,515 | 0c3409392a762e4aa819b82e532747af04b7fe23b9923e3b6613f4e0cc3e0309 | not committed; Table 1 parsed by `parse_sources.py` |
| 8 | https://arxiv.org/e-print/1610.08981 (Lelli+2017) | 1,457,339 | 3e6bd3e5bc7860900c0a3b5f51f4a5f395335f754fc49e62b308a82a82658be4 | not committed; TableETG.tex parsed by `parse_sources.py` |

No WebFetch summaries were used; every number comes from the LaTeX tables. `parse_sources.py` checks both sha256 values and rebuilds `etg16_serra16_lelli17.tsv` byte-identically.
