# CFG584: does the law's outer residual grow with baryonic mass? CONTRADICTED as frozen (marginal): WALLABY's slope is NEGATIVE

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (dc1d7398a). (owner chat 10-09, "run the mass trend test")
- **Script:** `cfg584_mass.py` → `cfg584_mass.out`, `cfg584_results.json`; MUTATE `CFG584_MUTATE=1` (+0.10 dex/dex) → `_MUTATE`.
- **Sample:** WALLABY DR2 discs exactly as CFG537 Part A built them, by executing `cfg537_wallaby.py` unedited up to its
  power-forecast section (no CFG537 files written; git status of CFG537 clean). 87 galaxies, 85 with an outer residual.
- κ = ½ fitted; footings never pooled; Υ_K fixed at 0.6; cold energy's mass still required; not theory closed.

## Power forecast (printed before any WALLABY slope)
SPARC (discovery) slope on CFG537's identical Δ_out statistic: +0.026 / +0.028 dex per dex (weaker than the +0.065 seen
on CFG583's statistic); scatter 0.130; WALLABY expected SE 0.029; expected Z at 0.065 = 2.21; P(Z ≥ 2) = 0.58 → not LOW POWER.

## Result
| footing | N | log M_b | slope (dex/dex) | Z | + early-type covariate | + f_gas covariate |
|---|---|---|---|---|---|---|
| canonical | 85 | 9.08–11.32 | −0.0716 ± 0.0343 | −2.09 | −0.075 ± 0.034 | −0.078 ± 0.040 |
| alt | 85 | 9.08–11.32 | −0.0686 ± 0.0343 | −2.00 | −0.072 ± 0.034 | −0.077 ± 0.040 |

- **Verdict as frozen: CONTRADICTED** (s < 0 with Z ≤ −2 on both footings) — marginally: alt sits exactly at Z = −2.00.
- Controls 2/2: C1 reproduces CFG537's matched early−late Δ_out (+0.026 / +0.028; max dev 0.0005); C2 N = 85.
- **MUTATE FAILS:** +0.10 dex/dex injected moves the slope by exactly +0.10 (to +0.028 / +0.031, Z +0.8 / +0.9), short of
  Z ≥ 2 because WALLABY's baseline is negative, not zero. The test recovers the injected shift; it cannot certify a
  +0.10 slope from a −0.07 baseline.

## Reading (not a verdict)
- SPARC's post-hoc mass hint does NOT replicate: the independent sample leans the other way (~2σ). There is no evidence
  for a general mass trend of the law's outer residual in disc rotation curves.
- So the KiDS deficit growing with M* (CFG531) is not mirrored by discs at low acceleration. That points to something
  specific to massive early types / lensing scales (≈ 50–100 kpc), consistent with CFG534's type-based SPARC excess,
  rather than a mass-dependent error of the law everywhere.
- A mass-dependent Υ_K error would also produce slopes of this size; neither sign is robust against that.
