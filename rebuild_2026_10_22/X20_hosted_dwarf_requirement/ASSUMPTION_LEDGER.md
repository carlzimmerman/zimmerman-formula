# X20 assumption ledger (committed with FROZEN_CRITERIA.md, before any script or number of this lane)

κ = ½ FITTED. Footings never pooled. No dark-matter particle. Not "theory closed".

## Inputs and their class

| input | class | used for |
|---|---|---|
| LVD tables `real_research/data/dsph/lvd_dwarf_{mw,m31,local_field}.csv` (Pace 2024, record copies) | RAW | σ, r_half, M★, ellipticity, refs, δσ |
| X1 committed stage tables + `x1_per_system.csv` + JSON (c74c622229) | FRAMEWORK-NATIVE (record results) | E per system, host field, d_host, K0/K1 |
| CFG257 Arroyo-Polonio 2026 Table A.1, Geha 2026 II Table A1, `geha_vs_lvd_match.csv` | RAW (record transcription) | binary ratio b (as X1), N★ |
| Collins 2013 VizieR table (record copy) | RAW | N★ for M31 rows citing it |
| Z2 `z2_per_system.csv` (14be14f282, another session's lane; read only) | FRAMEWORK-NATIVE (orbit in S1's MW field) | q = r₁₂/r_t at the PM pericentre |

## Assumptions (named)

- **A1 Baseline.** B_iso is primary (X19's choice: the successor's no-EFE baseline). B_EFE is v3s's static EFE
  (exact AQUAL + EFE at L★ = 0, as X19 used it). The v3 floor is not graded here.
- **A2 Labels.** Z ≥ 2 / Z < 1 are X19's conventions; per-system Z uses s_i with X1's 0.15 dex Υ prior.
- **A3 V_rel.** CFG939's criterion is stated for debris in a cluster. For a satellite the "settled medium" is the
  host's; V_rel is taken as the host circular speed at the present host distance (a circular-orbit speed), not a measured
  3D velocity. It therefore varies weakly between systems; the ordering is carried mostly by V_esc,b. Stated, not hidden.
- **A4 Plummer V_esc,b.** Stars only (M★ at Υ_V = 2), Plummer scale = r_half, evaluated at r₁/₂ = 4/3 r_half. Gas
  ignored (dSphs).
- **A5 Measurement variables are partial.** N★ exists only where the count belongs to the LVD dataset; no per-system
  single-epoch flag exists on disk (M5 unavailable). δσ/σ is the complete proxy. Binary correction is mostly a median
  ratio, so M3 is close to a UFD flag (M_V > −7.7), and is collinear with luminosity by construction.
- **A6 Collinearity.** Faint systems have fewer stars, larger δσ/σ, smaller x, and are found near the MW (Z2). A
  physical-vs-measurement split therefore needs the partial correlations; the [CONFOUNDED] qualifier reports it.
- **A7 Not blind.** Before freezing, X1's README (class rows and four individual systems), X19's README and Z2's README
  (member-count split −0.24 to −0.44 dex for N★ ≥ 10; luminosity proxy for the host-field trend) were read. No
  per-system correlation of this lane was computed before this commit.
- **A8 Sample.** X1's 89 LG systems only. Coma UDGs, UMa members, TDGs and DF2/DF4 are not X1 systems and have no
  per-system B_EFE solve on disk; they are outside this lane's per-system test.
