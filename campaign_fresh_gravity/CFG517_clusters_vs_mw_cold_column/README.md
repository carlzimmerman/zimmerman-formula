# CFG517: do galaxy clusters avoid the directions where the Milky Way's cold energy is thickest?

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (05fd82e81).
- **Script:** `cfg517_clusters_cold_column.py` (~15 s). Outputs: `cfg517_clusters_cold_column.out`, `cfg517_results.json`, `cfg517_skymap.png`.
- **MUTATE:** `CFG517_MUTATE=1` (cold map rotated 180° in longitude). Outputs: `*_MUTATE.out`, `cfg517_results_MUTATE.json`, `cfg517_skymap_MUTATE.png`.
- **Settings:** κ = ½ is FITTED. Both footings (9.36e-11 / 1.13e-10). ν_mono QUMOND phantom on McMillan 2017 baryons, using CFG514's committed solver unchanged. On-disk data only; nothing was downloaded. The cold energy's MASS is still required. This is not "theory closed".

## Bottom line

**Verdict (frozen rule): NOT DIAGNOSTIC.** The data show no dependence of cluster counts on the predicted cold column. But the declared error is too large for a 20% suppression to have been detected.

- **Where the clusters are.** Clusters are found all over the sky away from the Galactic plane: PSZ2 (1653) and MCXC (1743) cover the whole sky, and eRASS1 (12,247) covers the western half. The only big hole is the zone of avoidance (|b| ≲ 15–20°, plus dusty patches), which comes from dust and stars. The sky-map figure shows this.
- **Where the cold energy is.** The data-favoured ROUND cold energy (CFG514/CFG516) gives a column that depends only on ψ, the angle from the Galactic centre. Out to 100 kpc it is 59–281 M☉ pc⁻² (canonical).
  - In the plane, the Galactic-centre direction has ×5.5 the column of the anticentre.
  - At |b| ≥ 20°, sightlines with ψ < 70° have ×2.4 the column of those with ψ > 110°.
  - The phantom-DISC comparison map is mostly a function of |b| instead: plane/pole ×3.5.
- **The primary test.** PSZ2 with mask M-P and the round canonical map gives β = d ln(cluster density) / d ln(column) = −0.19 ± 0.44 (z = −0.43). This is measured at fixed |b| band, hemisphere, SFD dust and ecliptic latitude.
  - As a suppression of the top-column third relative to the bottom third, that is S = +13%, with a 95% range of −66% to +55%.
  - The 20% injection moves β by −0.25, which is a power of only 0.56σ. PSZ2 would need S ≳ 63% to reach 3σ.
- **The key direction.** At the same |b|, PSZ2 has 302 clusters towards the GC (ψ < 70°) and 317 away from it (ψ > 110°). Band-matched, that is a ratio of 0.94 ± 0.08 (z = −0.8), although the column differs ×2.4. This contrast was declared informational, so it does not set the verdict. Its rotation spread equals its Poisson error. Read this way, any suppression towards the GC is below 20% at 95% (ratio ≥ 0.80).
- **Physics expectation, unchanged.** Cold energy is transparent. The only route to an effect is MW-halo lensing magnification (κ ~ 1e-6, CFG514). Nothing here contradicts the expectation of NO dependence. The frozen statistic simply cannot exclude a 20% effect.

## Why the frozen test has little power

The error is σ_β = max(Poisson × √overdispersion, rotation-null spread). The rotation null rotates the cold map in longitude by 40°–320° and refits. Its spread is 4.7× Poisson for PSZ2 (0.44 vs 0.093) and 18× for eRASS1 (0.89 vs 0.049).

The spread comes from a few rotations: Δl ≈ 90–110° and 260–290°. Those place the rotated column peak next to the survey deep fields at the ecliptic poles (l = 96°, b = +30° and l = 276°, b = −30°), where β jumps to +1 to +4. The eRASS1 clusters visibly pile up around the south ecliptic pole in the figure. A smooth ecliptic-latitude polynomial does not absorb those deep fields, and no exposure or selection maps are on disk.

So the rotation null is measuring survey-depth structure. The test as declared is limited by it.

## Post-freeze information (not in the verdict)

| catalogue (M-P, round canonical) | β | Poisson-only z | robust-null z (median / MAD of rotations) | rank among 29 rotations | MUTATE (180°) β |
|---|---|---|---|---|---|
| PSZ2 (1241 in mask) | −0.189 | −2.01 | −0.95 | lowest (0/29 below) | +0.060 |
| eRASS1 EXT_LIKE ≥ 6, PCONT < 0.5 (5904) | −0.186 | −3.24 | −0.72 | 21% below | +0.125 |
| MCXC (1561) | −0.231 | −2.36 | −1.25 | 24% below | +0.183 |

- **A naive Poisson-only reading** would see a ~13% deficit towards the inner-Galaxy side in all three catalogues: 2.0σ, 3.2σ and 2.4σ.
- **Why it is not a cold-energy signal:**
  - β stays at about −0.15 to −0.19 for every rotation within ±60–70° of the true orientation. The deficit is broad over the inner-Galaxy hemisphere and not shaped like the column.
  - Against the robust null it is ≤ 1.3σ.
  - The eRASS1 deficit was declared in advance as expected from the soft X-ray foreground (eROSITA bubbles, Loop I / North Polar Spur), which is brightest towards the GC. MCXC (ROSAT) shares that foreground.
  - PSZ2's deficit is 2σ. Its candidate foreground causes (Galactic synchrotron/dust residuals near the GC) were not tested here: no Planck noise or mask maps are on disk.
- **The 180° MUTATE flips the sign** in all three catalogues. Whatever the small deficit is, it is tied to the towards/away-GC direction and not to the |b| structure. Because the primary |z| < 3, the frozen flip requirement did not apply.
- **The DISC map** gives β = −0.30 ± 0.47 (PSZ2) and the same pattern.

## Controls

**PASS:**
- Catalogue sizes: PSZ2 1653, eRASS1 12,247.
- I1, PSZ2/eRASS1/MCXC: the mean recovered ΔS is +0.147 / +0.164 / +0.157, each within 2σ_S of 0.20.
- I2a, false-positive rate on Poisson null mocks: 0.5% / 0.5% / 0%.
- I2b, recovered S for an injected 20%: 0.176 / 0.183 / 0.179, each within 0.03.
- MUTATE-A on the injection (MUTATE run): the injected suppression seen through the 180° map gives Δβ > 0 in all three catalogues. The test responds to direction.
- Collinearity of x with the nuisances is ≤ 0.34 in every primary cell.

**FAILED, as frozen.** Any failed control makes the verdict NOT DIAGNOSTIC; power had already done so.
- **I1 PSZ2 power 0.56 < 3.** This failure is what decides the verdict.
- **M0a FAILED (ln C spread in 1° ψ bins 0.0102 / 0.0120 vs < 0.01).** The criterion was mis-specified: even an exact function of ψ has a 1°-bin spread of 0.0104 / 0.0122 from its own gradient near the GC.
  - The correctly specified post-freeze check (M0a′, PASS) has the map deviating from a pure function of ψ by 0.0017 in ln C. Its enclosed mass to 120 kpc agrees with the grid to +0.26%.
- **M0b FAILED (7.2% vs 5%).** The DISC map's GC/anticentre and plane/pole ratios differ from CFG514's O9 because of pixelisation (HEALPix centres vs CFG514's 72 × 36 equal-area cells).
  - Evaluated on CFG514's own cells, the same map gives 3.065 / 3.305 (canonical) against CFG514's 3.053 / 3.246, and 3.199 / 3.431 (alt) against 3.187 / 3.369. Those are ≤ 1.9% off.

**Disclosed numerical fix (post-freeze).** On the first run, the M0 diagnostics showed that CFG514's `Grid.shell_average` leaves ±10% angular noise in the "round" field. It averages cells in 3% log-r bins, so each bin samples only a few polar angles. The ROUND map is now built as a true angle average of the same phantom (400 μ points), which is the frozen definition computed accurately. β changed by < 0.001 (PSZ2 −0.1889 → −0.1895). CFG514/CFG516 used enclosed masses and fields, which their K5 control showed are accurate to 0.3%, so their results are unaffected.

## Catalogues, masks, assumptions

- **PSZ2** (Planck 2015 union, VizieR J/A+A/594/A27): primary all 1653; variants with redshift (1094) and COSMO (507).
- **eRASS1** (Bulbul+24 primary): eROSITA-DE footprint 180.5° < l < 359.5°. Primary sample EXT_LIKE ≥ 6 and PCONT < 0.5 (6473); variants all (12,247) and EXT_LIKE ≥ 12 (3386).
- **MCXC**: informational only.
- **Masks:** M-P is |b| ≥ 20°, pixel-mean SFD E(B−V) < 0.15, with LMC/SMC holes. M-1 is 30° / 0.10, M-2 is 15° / 0.30. No variant reaches |z| ≥ 1 under the frozen error, in any catalogue or footing.
- **Pixels:** HEALPix NSIDE 32. The cold column is integrated from the Sun out to 100 kpc.

## Needs an owner go (not on disk)

- The PSZ2 selection function / Planck noise maps and Planck Galactic masks.
- eRASS1 exposure and background maps.
- The ACT DR5, SPT-SZ / SPT-ECS SZ catalogues.
- redMaPPer and Abell/ACO.

With the exposure/noise maps, the deep-field structure could be modelled instead of leaving it in the error. With ACT/SPT, a second SZ catalogue with independent foregrounds would be available. Those are the two changes that could make this test diagnostic.
