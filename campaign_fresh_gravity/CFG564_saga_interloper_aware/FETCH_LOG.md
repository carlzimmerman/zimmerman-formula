# CFG564 fetch log (owner approved fetching SAGA DR3 Table C2 for this lane)

| file | URL | UTC date | bytes | sha256 |
|---|---|---|---|---|
| _external_data/cfg564/saga-dr3-tableC2.txt (redshift catalogue; git-ignored, > 5 MB) | https://sagasurvey.org/data/saga-dr3-tableC2.txt | 2026-10-09 10:47 | 10828083 | 91e8ab349c0f54f526f7c43e9f2cf4d6cce0a0d3a31a1c4054e694f139dde3cd |

Tables C1 and C3 are read from CFG562's committed copies (sha256 in CFG562/FETCH_LOG.md). Source: SAGA DR3 (Mao et al. 2024,
ApJ 976, 117, Appendix C). AAS MRT format, read with astropy ascii.mrt. The script checks all three sha256 values.
