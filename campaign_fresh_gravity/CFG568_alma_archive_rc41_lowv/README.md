# CFG568: no archival ALMA CO/[CI] line coverage for any of the five low-velocity RC41 discs (metadata only, no download)

Criteria 2090ceed5 (committed before the query). Script `cfg568_alma.py` (ALMA Science Archive TAP, `ivoa.obscore`; column list and line parser copied from `data_assembly/alma_archive_footprint/`). Read-only: no data product was downloaded.

| target | z | archival rows / proposals | CO or [CI] window at its z | verdict |
|---|---|---|---|---|
| GS4_13143 | 0.760 | 64 / 6 (GOODS-ALMA 2015.1.00543.S, 2017.1.00755.S; Wide ASPECS 2017.1.00138.S; 2021.1.00024.S; 2021.1.00547.S; 2026.1.00363.S) | none | COVERAGE ONLY |
| GS4_03228 | 0.822 | 0 | — | NONE |
| COS3_22796 | 0.907 | 12 / 2 (2018.1.00231.S; 2024.1.00534.L) | none | COVERAGE ONLY |
| U3_05138 | 0.810 | 0 | — | NONE |
| zC_405501 (by target name) | 2.154 | 4 / 1 (2019.1.00477.S) | none | COVERAGE ONLY |

**Reading.**
- None of CFG567's five low-velocity RC41 near-misses has a resolved archival gas map. Their existing coverage is continuum (or line scans that miss their CO lines).
- Four of the five are at z ≈ 0.8–0.9, not the z ≈ 2–2.5 where the framework and feedback-ΛCDM separate most.
- Together with the 09-29 KURVS footprint (`data_assembly/alma_archive_footprint/`), the **only archival resolved-gas chance among CFG567's cheapest-path targets is KURVS-15** (Molina 2019.1.01238.S, CO(2-1) at 0.11″, 0.53 mJy/beam per 10 km/s), plus KURVS-13 at 1.09″. Each is a single object at z ≈ 1.5.
- The self-calibrated a₀(z) test therefore needs **new observations** (ALMA CO at ≤ 0.25″ for ~10 discs of V ≈ 120–180 km/s at z ≈ 1.5–2.5, plus JWST/AO inner kinematics). The archive cannot supply it.

**Controls.**
- Positive (GOODS-ALMA centre returns both GOODS-ALMA proposals): PASS.
- Negative (RA 150, Dec +60): PASS.
- MUTATE (targets shifted +1° in Dec): coverage changes, detected (exit 1).

**Departure (declared).** zC_405501 has no position on disk, so it was queried by `target_name LIKE '%405501%'`. An observation of it under a different target name would be missed.

One-line summary: CFG568 ALMA archive (metadata) for the five low-V RC41 discs: no CO/[CI] line coverage at any; with the 09-29 KURVS footprint, KURVS-15 (0.11″ CO(2-1)) is the only archival resolved-gas chance. The high-z self-cal test needs new observations.
