# WALLABY DR2 catalogues -- fetch log (2026-10-05, approved by the owner in chat)

Stored outside the repository in `_external_data/wallaby_dr2/` (sibling of the repo), with `FETCH_MANIFEST.jsonl` and `SHA256SUMS.txt` there.
Service: CADC TAP (https://ws-uv.canfar.net/youcat/sync), ADQL `SELECT * FROM <table>`, CSV.

| file | table | rows | bytes | sha256 |
|---|---|---|---|---|
| wallaby_dr2_kinematic_catalogue.csv | cirada.Wallaby_dr2_kinematic_catalogue | 303 | 184760 | 8a795b0e35f7e9f9713196842c670fbd660dfc6360f5a7ad42ed0a3ba7ef20ae |
| wallaby_dr2_source_catalogue.csv | cirada.Wallaby_dr2_source_catalogue | 3454 | 2145496 | 1550dfc7a63b5e2c854770e85f09e31498c1b8a3122c83392b50330bc665780b |

Kinematic columns: Rad, Vrot_model (+e, +e_inc), Rad_SD, SD_model, SD_FO_model (face-on HI surface density), Inc/PA/Vsys model, QFlag_model, team_release_kin.
No stellar masses are included; stellar photometry (e.g. AllWISE W1/W2) is a separate fetch that needs its own approval.
Sources: wallaby-survey.org/data/data-pilot-survey-dr2/ ; Murugeshan et al. 2024 (arXiv:2409.13130); Deg et al. 2022 (PASA, DR1 kinematic models).
