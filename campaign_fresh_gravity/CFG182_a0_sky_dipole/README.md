# CFG182 — is SPARC's acceleration scale different in different directions on the sky? (2026-09-29)

**Bottom line: NULL.** With the per-galaxy nuisances (Υ_disk, Υ_bul, distance, inclination) profiled under the Li, McGaugh & Lelli 2018 priors, the best-fit sky dipole of a₀ in the 149-galaxy clean SPARC sample is **A = 0.24 ± 0.20** toward (l, b) = (237°, −44°), and the permutation null gives **p = 0.77**. None of the three frozen signal lines passes (S1 significance, S2 distance-split stability, S3 not footprint-aligned). The 95% upper limit for a random flow direction is **A₉₅ = 0.43**, so the owner's directional flow may change a₀ by at most ±43% from upwind to downwind sky (±21% in the deep-MOND force). The two published SPARC dipole claims (0.25 ± 0.04 and a hemisphere anisotropy of 0.37 ± 0.04) are **neither confirmed nor excluded**. Along their directions this lane measures 0.11 ± 0.23 and 0.15 ± 0.22. Its errors are about 5× theirs, because it marginalises distance and inclination and keeps the real galaxy-to-galaxy scatter of a₀ in the null.

Frozen question, pass lines and MUTATE control: `FROZEN_QUESTION.md`, written before any script. Its Addendum 1, written after the curves were built and before any fit on the real positions, only extended the injection grid to 0.9. κ = ½ stays FITTED. a₀ is fitted here, so κ enters no pass line.

## What was done
- **Data.** The 175 SPARC rotation curves (`real_research/data/sparc_data`) and the master table `SPARC_Lelli2016c.mrt`, read as CFG4 reads them. Positions come from the VizieR copy of Lelli+2016 table 1, which has all 175 galaxies. They agree with `sparc_cosmicweb_match.csv` to ≤ 0.03° for the 165 galaxies that table resolves (it leaves 10 F-series LSBs UNRESOLVED). Note: `real_research/data/SPARC_table.txt` is an HTTP 404 page, not data. It was not used and not edited.
- **Clean sample.** Q ≤ 2, Inc ≥ 30°, ≥ 5 usable points: 149 galaxies and 3150 points. By distance method: 81 Hubble-flow, 37 TRGB, 3 Cepheid, 2 SNIa, 26 Ursa Major. The footprint is lopsided: the mean position vector has |⟨n⟩| = 0.60 toward (142°, 55°), and 117 of 149 galaxies are at b > 0.
- **Model (part A).** For each galaxy and each log a₀ on a 0.01-dex grid, the four nuisances are minimised: a profile likelihood in velocity space, kernel ν_mono. A dipole acts on a galaxy only through its own a₀_i = ā₀(1 + D·n_i), so the global point-level fit is exactly the sum of these curves. Each curve is divided by its Birge factor max(1, χ²_min/dof) (median 1.72). This keeps galaxies whose wiggles far exceed their formal errors from dominating.
- **Nulls (part B).** 5000 permutations of the sky positions among galaxies, refitting the free direction every time. Two schemes were run: simple, and Ursa Major as one block. The larger p is used. Also: a curve-level Gaussian null (5000) including the fitted extra scatter τ, and a point-level generative Gaussian null (100 full-pipeline mocks, part C).
- **Other analyses.** Galaxy bootstrap (2000). Fixed-direction fits. The Zhou-style hemisphere scan with its own permutation null. Distance-method and inclination splits. Footprint alignment. A peculiar-velocity template. A distance trend. Kernel, scaling and sample variants. A Neyman upper limit from dipoles injected into position-permuted data.

## Results (primary: `cfg182_b_dipole.out`)
| quantity | value |
|---|---|
| no-dipole ā₀ (ν_mono, LML priors) | 1.13 × 10⁻¹⁰ m/s² |
| best dipole | A = 0.238 toward (237.2°, −44.2°); Δχ² = 10.3 for 3 parameters |
| σ_A | bootstrap 0.201; Fisher 0.082 (too small: see scatter below) |
| direction cones | 68% within 59°, 95% within 115° |
| **permutation p_A** | **0.772 (simple), 0.774 (block)**. Null Â median 0.34, 95% 0.62. Δχ² p = 0.73 / 0.76 |
| Gaussian null, curve level (τ = 0.34 dex) | p = 0.89 |
| Gaussian null, point level (error model only) | p = 0.010 (0 of 100 mocks); **anti-conservative**: mocks have reduced χ² 0.68 against the data's 4.20 |
| hemisphere max H (the Zhou statistic) | 0.595 toward (295°, 5°); isotropic null median 0.51, 95% 0.73; **p = 0.24** |
| distance split | Hubble-flow: A = 0.47 toward (259°, 46°). TRGB/Cepheid/SNIa: A = 0.40 toward (183°, −62°). Vectors differ at p = 0.11. Along the full-sample direction: −0.76σ and +1.41σ → **S2 fails** |
| inclination split | consistent (p = 0.42) |
| footprint | footprint axis 53° from the fitted axis, inside the 115° cone → **S3 fails** (aligned within errors) |
| peculiar-velocity template (Hubble-flow only) | 209 km/s, Δχ² = 12.2 (the dipole's is 10.3), p = 0.58 |
| distance trend | β = +0.02 dex/dex (Δχ² 0.4); the dipole is unchanged by it |
| variants | no Birge: 0.61, p = 0.12. Kernel P2: 0.23, p = 0.78. Kernel simple: 0.22, p = 0.84. All 171 usable galaxies: 0.31, p = 0.59 |
| **A₉₅ (random direction)** | **0.425** (simple 0.425, block 0.375; Monte Carlo noise about ±0.05) |
| 95% upper ends along fixed directions | CMB dipole 0.24 · bulk flow 0.36 · Virgo 0.19 · Ursa Major 0.19 · Chang+18 0.55 · Zhou+17 0.53 |
| orientation reading (quadrupole weighted by P₂(cos i)) | ε = −1.5, Δχ² 27.7, p = 0.46. No signal, and no useful bound |

**Galaxy-to-galaxy scatter.** The per-galaxy best a₀ values scatter 0.39 dex (MAD) against a median profile width of 0.26 dex. Their ML extra scatter is τ = 0.34 dex, and 19 of 149 galaxies have |pull| > 3. The LML error model does not reproduce this: generative mocks give a reduced χ² of 0.68 against the real 4.20. That is why the curvature error (0.08) and the error-model-only null (p = 0.01) overstate any direction's significance. The permutation null keeps the real scatter and is the one the frozen lines use. Whether the scatter is intrinsic or comes from the error model (non-circular motions, distance errors beyond e_D, Υ beyond 0.1 dex) is not decided here. A dipole of 0.24 would contribute only about 0.06 dex rms, so the scatter is not the dipole.

**MUTATE (point-level injection of A = 0.20 toward (114.6°, −41.9°), `cfg182_b_dipole_MUTATE.out`).**
- **M1 PASS, at the edge of its tolerance.** The fitted dipole vector moved by 0.151, 22° from the injected direction. The tolerance was 0.20 ± 0.05 and ≤ 25°.
- **M2 not required.** σ_A = 0.20, so 0.20 < 4σ_A. The mutated p is 0.56: SPARC cannot detect a 0.20 dipole.
- **Why recovery is short (part E, post hoc).** The per-galaxy curve minima move by 0.98× the injected shift, and point-level and curve-level injection agree (0.151 against 0.161). The global fit then returns about 0.77 of the injection. With no residuals, recovery is exact (0.2000 at 0.0°). With centres on the model, it is 0.187. The shortfall comes from fitting the multiplicative form log(1 + D·n) to over-dispersed per-galaxy values. The Neyman A₉₅ injects into the same real curves, so it already includes this attenuation.
- **Secondary MUTATE.** Recovery is exact: 0.199 at 3°.
- **Part C MUTATE.** The mock Â median moves from 0.107 to 0.198.

**Secondary (the repo's per-galaxy table, 122 galaxies; `cfg182_d_pergalaxy_table.out`).** Labelled as inheriting per-galaxy fitting noise: fixed Υ, fixed distance and inclination, equal weights, deep-point estimator.
- Dipole: A = 0.30 ± 0.16 toward (244°, −16°), permutation p = 0.20 (block 0.17).
- Hemisphere: H_max = 0.28, p = 0.73. At Zhou's axis H = 0.13 ± 0.13. Along Chang's direction A = 0.07 ± 0.17.
- Hubble-flow and independent-distance subsamples differ at p = 0.11.
- The same null, with a direction within about 30° of the primary's.

**Post hoc (`cfg182_e_posthoc.out`, after all results were seen; not a finding).**
- The Hubble-flow subsample's best direction lies 4° from the CMB dipole. Its amplitude along the CMB direction is +0.47 ± 0.23 (two-sided permutation p = 0.05, with the direction chosen after looking).
- The TRGB/Cepheid/SNIa subsample gives −0.29 ± 0.20 along the same direction.
- A Hubble-distance frame error would put an a₀ dipole exactly there, because a₀ ∝ D² at fixed data. That makes this a distance systematic to watch, not the flow.
- Removing the ten largest-pull galaxies gives A = 0.19, p = 0.74.

## Comparison with the published claims (abstract-level only; the papers' methods were not read)
- **Chang et al. 2018 (arXiv:1803.08344):** dipole 0.25 ± 0.04 toward (171.3°, −15.4°). Along that direction this lane finds 0.11 ± 0.23 (secondary 0.07 ± 0.17), so 0.25 lies 0.6σ above and is **not excluded**. It is also not supported: the fitted direction is 62° away and the free-direction p is 0.77.
- **Zhou et al. 2017 (arXiv:1707.00417):** hemisphere anisotropy 0.37 ± 0.04 at (175.5°, −6.5°). This lane gets H = 0.15 ± 0.22 at that axis, 1.0σ below, so **not excluded**. The key point is the null: a **maximum** hemisphere anisotropy of 0.37 is unremarkable for isotropic SPARC once distance and inclination are marginalised and the real scatter is kept. The permutation null's H_max has median 0.51, and this lane's own maximum is 0.60 at p = 0.24.
- **Why the errors differ by about 5×.** a₀ ∝ D² in the deep regime, so distance errors of 5–30% alone give 0.04–0.23 dex per galaxy. On top of that is the 0.34-dex galaxy-to-galaxy scatter. If the published ±0.04 comes from fixed-nuisance fits with a scatter-free error model, it is too small by roughly that factor. This is conditional, because their full texts were not read.

## Door 11, gate G8 (the owner's directional flow)
For variant 11B′, a flow that modulates a₀ with sky direction as a₀(1 + ε f̂·n) must have **ε < 0.43** at 95% for an unknown direction. The deep-MOND force anisotropy is then **< 0.21**. The bounds are tighter along specific directions: ε < 0.24 along the CMB dipole, < 0.36 along the local bulk flow, and < 0.19 toward Virgo.

This is a weak bound, because SPARC cannot see a sky dipole below about 40% in a₀. It constrains only the readings in which the flow's effect depends on where a galaxy sits on the sky: a flow with a source direction or a gradient, or a velocity coupling (G7) that correlates with direction. A perfectly uniform flow gives every galaxy the same a₀ and predicts no sky dipole at all. Its signature would be the orientation quadrupole, which was fitted and is not constrained usefully by SPARC (p = 0.46).

The hand estimates in the frozen file were too optimistic: σ_A came out 0.20 against 0.06–0.12 expected, and A₉₅ 0.43 against 0.2–0.35.

## Plain-language summary for the owner
If dark energy streams in from one direction and boosts gravity as it goes, galaxies on the upstream side of the sky should show a different acceleration scale from those downstream. We checked 149 well-measured SPARC galaxies. We allowed each galaxy's distance, tilt and stellar mass to move within their measured uncertainties, then asked whether any direction on the sky stands out.

None does. The best direction is no more lopsided than what we get by randomly shuffling the galaxies around the sky: 77% of random shuffles look at least as lopsided. So the data allow no more than about a 43% difference in the acceleration scale between the two sides of the sky, which is roughly a 20% difference in the extra pull.

The two earlier papers that claimed such a lopsidedness are not ruled out. They are also not supported, and our shuffling test shows that numbers as large as theirs are what random skies produce once the real uncertainties are included. Better distances (Gaia, TRGB) and more southern-sky galaxies are what would sharpen this test.

A flow that is the same everywhere would not show up in this test at all.

## Reproduce (each script < 10 min uncontended; run from the repository root)
```
python3 campaign_fresh_gravity/CFG182_a0_sky_dipole/cfg182_a_profiles.py          # ~15 s  (curves; MUTATE=1: ~5 s)
python3 campaign_fresh_gravity/CFG182_a0_sky_dipole/cfg182_b_dipole.py            # ~2.5 min (MUTATE=1: ~3 min, needs both npz)
python3 campaign_fresh_gravity/CFG182_a0_sky_dipole/cfg182_c_gaussnull.py         # ~3 min (MUTATE=1 after the plain run)
python3 campaign_fresh_gravity/CFG182_a0_sky_dipole/cfg182_d_pergalaxy_table.py   # ~1 min
python3 campaign_fresh_gravity/CFG182_a0_sky_dipole/cfg182_e_posthoc.py           # ~1 min (after a, b and MUTATE a)
```
- **Outputs.** `*.out`, `*_results.json` and `*.npz`, with MUTATE runs written to `*_MUTATE.*`. Sky maps: `cfg182_b_skymap.png` and `cfg182_b_skymap_MUTATE.png`.
- **Checks.** All load-bearing checks pass: the optimizer check, finiteness, positions, single-start agreement, M1, the secondary M1 and part C's MUTATE check. The reported FAILs are the signal lines S1–S3 (a NULL) and part C's G1 (the error model does not reproduce the scatter).
- **Warnings.** Spurious floating-point warnings from numpy 1.26 matmul on macOS Accelerate were checked to give identical results to einsum and are silenced in the hemisphere scan.
- **Scope.** Nothing outside this directory was edited. `CFG4_common` and FP1's ν_mono are imported read-only.
