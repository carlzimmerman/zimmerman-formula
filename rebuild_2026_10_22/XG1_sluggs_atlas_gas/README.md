# XG1_sluggs_atlas_gas: Chandra data confirm the extrapolated hot gas around NGC 4374; NGC 5846 untested; NGC 4365 not in the atlas

Criteria: `FROZEN_CRITERIA.md` (ef0c2788ae, committed alone, before any gas number); no amendment.

**Data.**
- Chandra Galaxy Atlas (Kim et al. 2019), packages N4374_90301 and N5846_90201.
- Downloaded at the owner's request to `_external_data/chandra_galaxy_atlas/` (untracked; the tarball sha256 is in the
  results JSON).
- Used: the adaptive-bin APEC emission-measure table.

κ = ½ FITTED. Not "theory closed". Nothing here says the data favour the framework.

## Verdict (frozen): **EXTRAPOLATED GAS SUPPORTED** (overall, on the one informative galaxy)

| | NGC 4374 | NGC 5846 |
|---|---|---|
| atlas coverage R_max | **64.9 kpc** | 28.6 kpc |
| record's measured edge r_meas / outer GC bin | 18.3 / 22.1 kpc | 30.0 / 53.6 kpc |
| β-model (R ≥ 2 kpc) | r_c 0.05 kpc (at the fit's lower bound), β 0.435 | r_c 3.40 kpc, β 0.473 |
| M_gas(<r_t): atlas / trunc / extrap | 1.77e9 / 1.29e9 / 1.70e9 M☉ | (r_t 28.6 kpc < r_meas) |
| **f** | **1.19 → SUPPORTED** | **NOT INFORMATIVE** |
| reported: β-model continued to the outer GC bin | 1.77e9 vs 1.70e9 | 2.32e10 vs 2.11e10 |

## Reading

- **NGC 4374.** The atlas measures hot gas to 65 kpc. At the outer GC radius (22 kpc), the gas mass implied by the
  atlas shape, normalised to the record's measured gas at 18 kpc, is **at or above** CFG331's extrapolation.
- **NGC 5846.** The atlas stops just inside the record's edge, so it cannot test the extrapolation. Its β-model
  continuation agrees with it, but that is reported only.
- **NGC 4365** is not in the atlas.

**Effect on SLUGGS (SG1, e8066d5698).** Under the extrapolated gas the class passed with 3/4 cleared, NGC 4365 staying
out. This lane confirms the extrapolated gas for one of the galaxies that need it, NGC 4374. SLUGGS remains a
**partially confirmed prediction**. A full confirmation needs deeper outer X-ray data for NGC 5846 beyond 30 kpc and
for NGC 4365.

## Disclosed

- The table's r column is read as arcmin. That is consistent with the atlas field sizes, since 64.9 kpc is 12′ at
  18.5 Mpc.
- NGC 4374's r_c sits at the fit's lower bound. It has a negligible effect at 18–22 kpc, where the profile is a power
  law with M ∝ r^(3 − 3β).
- A constant emissivity is assumed. The fitted APEC norms already absorb T, which spans 0.66–2.42 keV for NGC 4374.

## Checks: 3/3

- **K0:** trunc equals extrap inside r_meas.
- **K1:** the deprojection round trip holds to 1e-3.
- **K2:** the fitted β was used.
- **Rerun:** byte-identical.
- **MUTATE twin** (β = 1/3): K2 fails (and K1), exit 1.
