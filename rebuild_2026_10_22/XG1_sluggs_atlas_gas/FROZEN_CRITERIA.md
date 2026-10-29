# XG1_sluggs_atlas_gas: FROZEN CRITERIA (committed alone, before any gas number of this lane)

Written 2026-10-29, at the owner's request: "download the two atlas packages (~1.6 GB) and freeze a deprojection
lane: beta-model gas density from the surface-brightness profiles, M_gas(<r) at the GC radii vs CFG331's
extrapolation."

**Why.** SG1 (e8066d5698) found that SLUGGS passes only with CFG331's gas **extrapolated** beyond the measured X-ray
edges:
- NGC 4374: measured to 18 kpc, outer GC bin 22 kpc;
- NGC 5846: measured to 30 kpc, outer GC bin 54 kpc.

With the measured (truncated) gas it fails. Does deeper X-ray data contain the extrapolated gas?

**Data.**
- Chandra Galaxy Atlas (Kim et al. 2019), packages N4374_90301 and N5846_90201.
- Downloaded at the owner's request to `_external_data/chandra_galaxy_atlas/` (untracked; sha256 recorded by the
  script).
- NGC 4365 is not in the atlas, so it is not tested (disclosed).
- **Used:** the atlas's adaptive-bin spectral-fit table `*_AB_sn20_APECnPL_sum.dat`, with columns r, area, T and the
  APEC norm per area (N/area).

**Seen before freezing (disclosed):** the table's column header and its first three rows for NGC 4374.

**Standing rules.**
- κ = ½ FITTED.
- Not "theory closed". Nothing here may say the data favour the framework.
- Data-only: no model of gravity enters.

## 1. Method (frozen)

1. **Projected emission measure.** The APEC norm per area is proportional to the projected emission measure Σ_EM(R),
   since norm ∝ ∫ n_e n_H dV.
   - **Radius:** the table's r column is read as arcmin and converted to kpc at CFG331's distance for each galaxy.
   - **Absolute units:** not needed. See step 3.
2. **β-model fit.** A weighted least-squares fit in log space of Σ_EM(R) = A (1 + (R/r_c)²)^(−3β + 1/2), with weights
   from the table's N_lo/N_up bounds.
   - **Fit range:** R ≥ 2 kpc (excludes the AGN/core bins) out to the atlas's outermost bin R_max.
   - **Deprojection:** analytic, n_e ∝ (1 + (r/r_c)²)^(−3β/2), and M_gas,shape(<r) = ∫ 4π r² n_e dr.
3. **Normalisation by the record's own measured gas.**
   - The atlas shape is scaled so that M_gas,atlas(<r_n) equals CFG331's **measured** M_gas(<r_n) at
     r_n = min(r_meas, R_max).
   - The atlas thus decides only the **shape beyond the record's edge**, which is exactly the question.
4. **Test radius.** r_t = min(r_GC,outer, R_max), where r_GC,outer is CFG331's outermost GC bin radius. The atlas is not
   extrapolated beyond its own data.

**Statistic:** f = (M_atlas(<r_t) − M_trunc(<r_t)) / (M_extrap(<r_t) − M_trunc(<r_t)). Here M_trunc is CFG331's
measured gas held flat beyond r_meas, and M_extrap is CFG331's extrapolation, both from CFG528's `gas_profile`.

## 2. Verdict (frozen, per galaxy and overall)

| verdict | condition |
|---|---|
| **NOT INFORMATIVE** | R_max ≤ r_meas: the atlas does not reach beyond the record's edge |
| **EXTRAPOLATED GAS SUPPORTED** | f ≥ 0.5 at r_t |
| **EXTRAPOLATED GAS NOT SUPPORTED** | f < 0.5 |

**Overall:**
- **SUPPORTED** iff both informative galaxies are supported;
- **NOT SUPPORTED** iff any informative galaxy is not;
- **NOT INFORMATIVE** if neither is informative.

**Reported:**
- r_c, β, R_max and r_t;
- f at r_t;
- the β-model's continuation to r_GC,outer (variant, not graded);
- the temperature range used.

**Disclosed:** a constant emissivity across radius is assumed. Σ_EM is taken directly from the fitted norms, which
already account for T.

## 3. Checks and twin

- **K0.** CFG331's gas profile, loaded via CFG528's functions, reproduces CFG528's trunc = extrap inside r_meas, to
  1e-12.
- **K1.** The deprojection recovers the projected profile it was fitted to: projecting n_e² back along the line of
  sight reproduces Σ_EM(R) to 1e-3 at three radii.
- **Rerun.** The results JSON is byte-identical.
- **MUTATE (`XG1_MUTATE=1`, separate outputs).** β is fixed at 1/3 (a flat profile) on the graded path, while K2
  checks that the fitted β was used, so K2 fails and the run exits 1.

**Run:** `PYTHONHASHSEED=0 python3 -I xg1_atlas_gas.py`
