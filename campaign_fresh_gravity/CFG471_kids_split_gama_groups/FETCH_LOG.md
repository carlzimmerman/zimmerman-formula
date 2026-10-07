# CFG471 FETCH LOG

Owner-approved fetch for this lane (real catalogues only: GAMA DR4 release). Files stored in
`campaign_fresh_gravity/_external_data/cfg471/` (git-ignored, > 5 MB).

| date (UTC) | URL / query | file | bytes | sha256 |
|---|---|---|---|---|
| 2026-10-07 11:16 | `https://datacentral.org.au/vo/tap/sync` (ADQL, FORMAT=csv, MAXREC=1000000): `SELECT CATAID, RA, Dec, Z, Rpetro, SURVEY_CODE, GroupID, RankIterCen, RankBCG FROM gama_dr4.G3CGalv10` | G3CGalv10.csv (204,110 rows) | 20,695,642 | 051950e193e447ebf8bf7a9458c3ffe4ea368596b8042732ee933fc95f6ad9f8 |
| 2026-10-07 11:16 | same endpoint: `SELECT GroupID, Nfof, IterCenCATAID, IterCenRA, IterCenDec, IterCenZ, Zfof, BCGCATAID, GroupEdge, Zcomp, VelDisp, Rad50, MassA, MassAfunc FROM gama_dr4.G3CFoFGroupv10` | G3CFoFGroupv10.csv (26,194 rows) | 5,099,088 | eb81594ad6994e3fb44d2ee7c2e4eac4a99e3c7c27750bbf620d9f103a5b96c7 |

Notes
- Data Central (AAO) is the GAMA DR4 archive host; the tables are the DR4 `GroupFinding` DMU (G3C v10, Robotham et al. 2011).
  Schema descriptions were read from the TAP_SCHEMA of the same service.
- The primary GAMA site (www.gama-survey.org, `/dr4/data/cat/GroupFinding/v10/`) was tried first and timed out (TCP connect
  on 443; no bytes on 80 after 110 s). Nothing was downloaded from it.
- VizieR has the GAMA DR1-DR4 spectroscopic catalogues but no G3C table (J/MNRAS/416/2640 not found).
- To refetch: rerun the two queries above; the script refuses to run if either sha256 differs.
