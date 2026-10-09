# CFG570 FROZEN CRITERIA: ALMA archive metadata survey of the z 1.2–2.0 "best window"

Committed alone, before any script. Owner request (10-09): "look back into the alma data and see what you can find in this range" — the z 1.2–2.0 window marked on the a0(z) chart, where a CFG385 self-calibrated disc sample (~0.1 dex) would separate a0 ∝ √ρ_DE from both rivals. Metadata only: **no data product is downloaded** (a download needs a separate owner yes).

## Sample (positions from committed files, read-only)
- **S_all:** every KMOS3D catalogue galaxy (`data_assembly/kmos3d_phibss/kmos3d_catalog.csv`) with 1.2 ≤ Z ≤ 2.0, plus every KURVS galaxy (`data_assembly/arxiv_tables/kurvs_positions/kurvs_positions.csv`) with 1.2 ≤ z_halpha ≤ 2.0.
- **Deep-kinematics flag (K):** the galaxy is a RC100 disc (`CFG289_rc100_csv_bound/cfg90_per_object_RC100FIX.csv`, name matched to KMOS3D ID/ID_TARGETED after removing spaces/underscores), an RC41 disc (`price2021_rc41.csv`), a KURVS disc, or a `highSN` fit in `kmos3d_cubes/k3d_fits_main_final.csv`.
- RC100 discs in the window with no KMOS3D position (EGS, zC, D3a, GK names) are listed as "no position on disk", not searched.

## Query
- ALMA TAP `https://almascience.eso.org/tap/sync`, `ivoa.obscore`, one box query per field (COS, GS/CDFS, UDS) on s_ra/s_dec with a 0.5° margin; a galaxy is "covered" by a row if its angular separation from (s_ra, s_dec) is < s_fov/2.
- Every tier-A or tier-B candidate is then confirmed with a per-position `CONTAINS(POINT, s_region)` query; disagreements are reported, and the CONTAINS result is the one used.
- Line windows parsed from frequency_support (CFG568 parser) for CO(2-1), CO(3-2), CO(4-3), CO(5-4), [CI](1-0), [CI](2-1) at the galaxy's redshift.

## Tiers (per galaxy, best row)
- **A:** a line window, s_resolution ≤ 0.25″ (resolves ~2 kpc at z 1.2–2: a gas profile out to ~10 kpc is possible in principle).
- **B:** a line window, 0.25″ < s_resolution ≤ 0.5″.
- **C:** a line window, coarser than 0.5″ (integrated gas only).
- **D:** covered, continuum/other only.
- **E:** not covered.
- **Usable for CFG385 (metadata level):** tier A or B **and** flag K. This is a pointing, not a detection: CO may be undetected (CFG569), and the Hα curve must still span g_obs ×6 or more.

## Controls
- **C1 positive:** KURVS-15 (RA 53.070583, Dec −27.834461, z 1.613) must come out with a CO(2-1) window at ≤ 0.25″ from 2018.1.00164.S (the CFG569 programme). Tests the box + s_fov method and the line parser.
- **C2 negative:** an empty position (RA 150.0, Dec +60.0) has no coverage.
- **MUTATE:** shift every sample position by +1.0° in Dec; the tier A+B count must change (exit 1). Output written with the _MUTATE tag.
- Failed controls are kept and reported.

## Pre-data expectation
A handful (0–5) of usable discs; most deep-kinematics discs will have no line window or only coarse (tier C) PHIBSS-like CO. A count of zero is a valid outcome and means the window needs new observations.

## Not claimed
No a0 number, no detection, no z-trend. κ = ½ fitted; the cold mass is still required.
