# CFG517 FROZEN CRITERIA: do galaxy-cluster counts avoid the directions where the Milky Way's cold energy is thickest?

Written and committed alone, before any script for this lane exists and before any cluster position is compared with
any cold-column map. Offline only: data already on disk; local compute (nice -n 15, <= 4 threads). Nothing is
downloaded; anything else that would be needed is listed as "needs owner go". κ = ½ is FITTED. Both footings:
a0 = 9.36e-11 (canonical) and 1.13e-10 (alt) m/s². The cold energy's MASS is still required (no particle species is
added). Not theory closed.

## 0. The question and the expectation

Owner (10-08): in which sky directions do we find galaxy clusters, and do they avoid the directions where we look
through the most of the Milky Way's own cold energy? If the cold energy obscured our view, cluster counts would be
suppressed where the predicted cold column is largest.

Expectation, stated before computing: cold energy is transparent and interacts only gravitationally. The only route to
a count change is gravitational: magnification bias by the MW halo, with κ ~ 1e-6 (CFG514 O8). That is negligible.
So the expected answer is NO dependence. A dependence at fixed dust and |b| would be surprising and important, and it
would have to survive the controls below before it is called anything.

The main confound is the Galactic disc (dust, stars, foreground emission: the zone of avoidance), which suppresses
detections at low |b|. Dust depends mainly on |b|. A round cold component centred on the Galactic centre gives a column
that depends mainly on ψ, the angle from the Galactic centre (cos ψ = cos l cos b). So the discriminating comparison is
towards vs away from the Galactic centre at the same |b|.

## 1. The cold-column maps (model; computed before touching cluster positions)

Baryons: McMillan 2017, exactly CFG514's implementation (executed from CFG514's committed file, lines before the
"build the framework / rival" marker; not edited). Kernel ν_mono, full QUMOND phantom ρ_ph on CFG514's grid.

- **ROUND (primary, the data-favoured shape; CFG514 MUTATE = CFG516 RM-φ):** ρ_cold(r) = the spherical shell average
  of ρ_ph. Column C(n̂) = ∫_0^100 kpc ρ_cold ds along the sightline from the Sun (R0 = 8.122 kpc, z = 0), Msun/pc².
- **DISC (comparison, CFG514's phantom disc):** the same integral of the full flattened ρ_ph.
- Both footings. Amplitude A = 1 (F0). The statistic uses x = ln C, so only the map's SHAPE matters.
- Map resolution: HEALPix NSIDE = 32 (pixel ≈ 1.8°), C evaluated at pixel centres.
- Map control M0: the round map must be a function of ψ only (spread of ln C within 1° ψ bins < 1%); its
  GC-direction / anticentre ratio and plane/pole ratio are printed beside CFG514's O9 values (CFG514's DISC map numbers
  3.05 / 3.25 canonical must be reproduced within 5%, different pixelisation).

## 2. Catalogues (on disk) and samples

- **PSZ2 (primary verdict catalogue):** Planck 2015 union SZ catalogue, real_research/data/psz2_union.tsv (VizieR
  J/A+A/594/A27), GLON/GLAT given. Primary sample: all 1653 entries. Variants: (P-z) those with a redshift (z > 0);
  (P-C) COSMO = 1. SZ selection does not depend on optical depth or X-ray foreground; it does depend on Planck's
  noise (deeper near the ecliptic poles) and on Galactic dust/synchrotron at low |b|.
- **eRASS1 (robustness catalogue):** Bulbul+24 primary cluster catalogue, real_research/data/erass1cl_primary_v3.2.fits,
  RA/DEC → Galactic (astropy). Footprint: eROSITA-DE half, 180.5° < l < 359.5° (a 0.5° margin from the half-sky
  boundary). Primary sample: EXT_LIKE ≥ 6 and PCONT < 0.5. Variant (E-all): all 12,247. Variant (E-12): EXT_LIKE ≥ 12.
  Declared confound, in advance: eRASS1 is X-ray selected, and the soft X-ray foreground (eROSITA bubbles, Loop I /
  North Polar Spur) is brightest towards the Galactic centre at |b| up to ~80°. A deficit towards the GC in eRASS1 is
  therefore EXPECTED from the foreground alone and cannot by itself indicate cold energy. Exposure varies with ecliptic
  latitude (deepest at the south ecliptic pole, l = 276°, b = −30°); no exposure map is on disk (needs owner go).
- **MCXC (informational only, not in the verdict):** Piffaretti+11 meta-catalogue, gext_vectors_2026/data/raw/mcxc.tsv.
  Heterogeneous ROSAT-based selection; reported for completeness.
- Not on disk (needs owner go): ACT DR5 / SPT-SZ / SPT-ECS SZ catalogues, redMaPPer, Abell/ACO, the PSZ2 and eRASS1
  selection-function / exposure maps, the Planck Galactic masks.

## 3. Masks (fixed now)

Dust map: SFD 1998 E(B−V), real_research/data/dustmaps/sfd/SFD_dust_4096_{ngp,sgp}.fits (ZEA), read with the FITS WCS.
Per NSIDE-32 pixel, E(B−V) = the mean over its 64 NSIDE-256 sub-pixel centres.

- **Primary mask M-P:** |b| ≥ 20° (pixel centre) AND pixel E(B−V) < 0.15 AND outside the LMC (6° around l = 280.47°,
  b = −32.89°) and SMC (3° around l = 302.80°, b = −44.30°). For eRASS1 also the footprint above.
- **Variant M-1 (strict):** |b| ≥ 30°, E(B−V) < 0.10, same LMC/SMC holes.
- **Variant M-2 (loose):** |b| ≥ 15°, E(B−V) < 0.30, same holes.
- A cluster counts if its pixel is unmasked.

## 4. Statistic (fixed now)

Poisson regression over unmasked NSIDE-32 pixels i, counts N_i:

  ln λ_i = α_band(i) + β x_i + γ1 E_i + γ2 E_i² + c1 s_i + c2 s_i² + c3 s_i³

- x_i = ln C_i − median over unmasked pixels (round map unless stated);
- α_band: one intercept per |b| band (edges 15, 20, 30, 40, 50, 60, 90°) × hemisphere (N/S), only bands present;
- E_i = pixel E(B−V); s_i = sin(ecliptic latitude) at the pixel centre (exposure / scan-depth nuisance).
- Fit by maximum likelihood (Newton/IRLS). **β is the statistic**: the log-response of cluster density to the predicted
  cold column at fixed |b| band, hemisphere, dust and ecliptic latitude. Obscuration predicts β < 0.
- Error σ_β = max(σ_Poisson × √max(φ, 1), σ_rot), where σ_Poisson is from the Fisher matrix, φ = Pearson χ²/dof, and
  σ_rot is the standard deviation of β over the ROTATION NULL: the same fit with the cold map rotated in longitude by
  Δl = 40°, 50°, …, 320° (29 rotations; clusters, masks, dust and nuisances unchanged). The rotation null keeps the real
  cluster clustering (cosmic variance; e.g. the Shapley region), the masks and the |b| structure, and moves only the
  towards/away-from-GC pattern. For eRASS1 the rotated map is evaluated over the same footprint pixels.
- z = β / σ_β. Suppression amplitude reported as S = 1 − exp(β (x̄_top − x̄_bot)), the fractional density deficit of the
  top-tercile-column pixels relative to the bottom-tercile pixels (terciles over unmasked pixels), with its 95% interval
  from β ± 1.96 σ_β.
- Direct contrast (informational, the "key direction"): per catalogue, the density ratio of pixels with ψ < 70° to
  pixels with ψ > 110°, pooled over the |b| bands with band-matched weights (each band's expected counts under a common
  density), error by Poisson ⊕ rotation spread (same 29 rotations, ψ recomputed about the rotated centre).

## 5. Controls and MUTATEs (fixed now)

- **MUTATE A (180° rotation):** the cold map rotated by 180° in longitude (towards ↔ away from the GC), written
  separately (_MUTATE outputs). A real directional effect must flip: β_MUT must have the opposite sign to β with
  |z_MUT| ≥ 2 whenever |z| ≥ 3. On the injection mock (below), β_MUT must have the opposite sign to the injected
  response (else the test is responding to |b| structure, not direction, and the lane reports a FAILED control).
- **MUTATE B / injection I1 (on the real catalogue):** remove each cluster in a top-tercile-column pixel with probability
  0.20 (50 seeds). PASS if the mean recovered shift Δβ = β_inj − β_real gives mean |Δβ|/σ_β ≥ 3 and S_inj − S_real is
  within 2σ of 20% on average. The mean |Δβ|/σ_β is the POWER of that catalogue for a 20% suppression.
- **I2 (synthetic, estimator bias):** 200 Poisson mocks drawn from each catalogue's fitted null model (β set to 0) at the
  real N; (a) false-positive rate |β/σ_Poisson| ≥ 3 must be ≤ 2%; (b) with a 20% top-tercile suppression injected, the
  mean recovered S must be within 0.03 of 0.20.
- Map control M0 (section 1). Nuisance collinearity: the correlation of x with every nuisance column is printed; if
  |corr| > 0.8 with any nuisance, that catalogue/mask cell is NOT DIAGNOSTIC.

## 6. Verdict rule (fixed now)

Primary cell: PSZ2 primary sample, mask M-P, ROUND map, canonical footing. Robustness set: masks M-1/M-2, PSZ2 variants
P-z/P-C, alt footing, and eRASS1 primary.

- **DEPENDENCE FOUND:** primary |z| ≥ 3; the same sign with |z| ≥ 2 in M-1, M-2 and the alt footing; eRASS1 primary the
  same sign with |z| ≥ 2; and MUTATE A flips (section 5). The sign is reported: β < 0 = suppression (obscuration-like),
  β > 0 = enhancement (not obscuration).
- **NO OBSCURATION:** primary |z| < 3, the PSZ2 power for a 20% suppression ≥ 3 (I1), and controls I2 pass. The
  sensitivity is stated as the 95% interval on S (the largest suppression still allowed). If eRASS1 alone shows |z| ≥ 3
  while PSZ2 is null, this is reported as an X-ray-foreground-confounded, catalogue-specific signal, NOT a dependence.
- **NOT DIAGNOSTIC:** otherwise: PSZ2 power < 3 for a 20% suppression; or primary |z| ≥ 3 that fails the robustness or
  MUTATE requirements; or a failed control (I2, M0, collinearity).
- The DISC map runs are reported beside the ROUND ones as a comparison; they do not enter the verdict.
- A pass is verified as hard as a fail: every number in the README is read from the JSON.

## 7. Outputs

cfg517_clusters_cold_column.py → .out, cfg517_results.json, cfg517_skymap.png (clusters over the predicted ROUND cold
column, and the DISC map, with masks); CFG517_MUTATE=1 → _MUTATE.out, _MUTATE.json, _MUTATE.png. README.md in plain
words. Only this folder is committed; no data. Committed locally, not pushed.
