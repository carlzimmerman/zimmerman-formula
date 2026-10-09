# CFG562 fetch log (owner approved the SAGA fetch for this lane)

| file | URL | UTC date | bytes | sha256 |
|---|---|---|---|---|
| data/saga-dr3-tableC1.txt (101 hosts) | https://sagasurvey.org/data/saga-dr3-tableC1.txt | 2026-10-09 02:36 | 24884 | 278239bbdbebb6093555b65fd91dbc3ec6bebf225c81c035ca0e8e8ae0a595bf |
| data/saga-dr3-tableC3.txt (378 satellites) | https://sagasurvey.org/data/saga-dr3-tableC3.txt | 2026-10-09 02:36 | 139445 | 14c0841d13b270468dee202f3246dd671f1e1ce05f83c66d33ff41c291d75f8b |
| data/saga-dr3-tableC4.txt (candidates, unused) | https://sagasurvey.org/data/saga-dr3-tableC4.txt | 2026-10-09 02:36 | 22989 | c2d37d05e8cf74694d7576ed676029ea4d36c07505d0d82784815f029cda3851 |

Source: SAGA DR3 (Mao et al. 2024, ApJ 976, 117, Appendix C; Geha et al. 2024). AAS MRT format, read with astropy ascii.mrt.
Table C2 (background redshifts, 10.8 MB) was NOT fetched (not needed). All files < 5 MB, kept in the lane dir.
The script checks the sha256 of C1 and C3 before use.
