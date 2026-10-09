# CFG519 FETCH LOG

The owner approved (2026-10-08) downloading public KiDS-bright and GAMA DR4 tables for this lane. **Nothing new was downloaded.**
Everything needed was already on disk from earlier logged fetches.

| file | origin | bytes | sha256 | used as |
|---|---|---|---|---|
| `KiDS_DR4_brightsample.fits` | already in `real_research/data/lensing_rar/` (record's KiDS-1000 bright sample, Bilicki+21; used since CFG96) | 89,259,840 | not re-hashed; check C2 instead reproduces CFG502's 605,531 lens candidates exactly | pool, lenses |
| `KiDS_DR4_brightsample_LePhare.fits` | same | 257,817,600 | same (C2) | log M*, u - r |
| `G3CGalv10.csv` | CFG471's fetch, 2026-10-07, Data Central TAP (`gama_dr4.G3CGalv10`), see `../CFG471_kids_split_gama_groups/FETCH_LOG.md`; copied on 2026-10-09 02:30 UTC to `../_external_data/cfg519_work/` | 20,695,642 | 051950e193e447ebf8bf7a9458c3ffe4ea368596b8042732ee933fc95f6ad9f8 | spec-z, G3C membership |
| `G3CFoFGroupv10.csv` | same (`gama_dr4.G3CFoFGroupv10`) | 5,099,088 | eb81594ad6994e3fb44d2ee7c2e4eac4a99e3c7c27750bbf620d9f103a5b96c7 | Nfof, IterCenCATAID |

- The script refuses to run unless both G3C SHA-256 values match (check C3).
- G3CGal v10 holds every GAMA-II galaxy used by the group finder: r < 19.8, good redshift, grouped or not. GroupID = 0 means ungrouped.
- It covers G09, G12 and G15 (184,081 rows) plus G02, which is outside KiDS. G23 is not in it.
- No GAMA stellar-mass or spectroscopic table was needed. Lens and companion masses are the KiDS LePhare masses the isolation uses, so the selection is identical to the record's.
