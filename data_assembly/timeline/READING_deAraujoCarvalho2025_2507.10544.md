# Reading note: de Araujo-Carvalho et al. 2025, arXiv:2507.10544 (ApJ, doi 10.3847/1538-4357/adef06)

"Observational biases on rotation curves from IFU data at cosmic noon". The full text (arXiv HTML v1) was read on 2026-10-27, replacing the abstract-only entry in `ONE_OFF_DATASETS_2026-09-29.md` and `ACCUMULATION_ROUTES_2026-09-29.md`. This is a reading only: nothing was computed for the law, and no lane was re-run.

## What the paper does
- **Sample:** 19 Lyman Break Analogues at z 0.10–0.27, observed in Paα with Keck/OSIRIS + AO (Gonçalves+2010 data). Spatial resolution is under 200 pc. The galaxies are compact (UV half-light radius 0.08–3.0 kpc, most under 1.4 kpc), with log M* 9.1–10.9. Many are mergers or interacting.
- **Mocks:** the same cubes are moved to z = 2.2 (Hα) by the Law+2006 recipe, which applies (1+z)^-4 dimming, the sky model, and 2–3 h integrations. There are two instruments: OSIRIS + AO (Strehl losses included) and SINFONI seeing-limited (0.5″ Gaussian, 0.125″ pixels, with **no extra dimming applied**, on the argument that the higher sensitivity offsets it).
- **Analysis:** 2-D only (PaFit, folded major-axis curves, Kinemetry), with no 3-D forward modelling and no beam-smearing correction. The authors say this matches common cosmic-noon practice. Curves are measured for 15 objects, and the OSIRIS mock comparison uses 11 (4 too small).

## What it measures (numbers stated in the text)
| quantity | z ≈ 0.2 real | mock OSIRIS+AO | mock SINFONI | comparison quoted |
|---|---|---|---|---|
| mean side-to-side Δχ²_red (Übler+2021 method) | 158.05 | 2.81 | 33.04 | Übler+21: TNG50 mocks 46.8, Genzel observed discs 2.1 |
| rotation-curve extent | 1 | ≈ 1/1.5 | reaches the outskirts | — |
| asymmetry vs radius (real) | rises outward (Spearman 0.84, Pearson 0.77) | flattened | flattened | — |
| inferred inclination | — | biased toward face-on | biased toward face-on | figure only |
| V_rms = √(V² + σ²) | — | off the 1:1 line | off the 1:1 line | figure only, no number |

They also report a qualitative effect: dimming removes the **high-velocity values in the outskirts** (strongest in the AO mock), and the kinematic centre and PA can shift a lot.

## What it does NOT show
1. **It never measures a bias in the outer slope** (falling vs flat). There is no result of the form "a flat curve is made to fall by X". The headline is that the curves look *more regular* than they really are, and that is a statement about asymmetry and extent, not about slope.
2. **Its galaxies are not Genzel's.** LBAs are compact, often merging systems of ≲10^10.5 M☉ with sub-kpc to few-kpc radii. Genzel+2017's six are massive (Table 1 v_c ≈ 257–364 km/s, as transcribed in cfg400_test.py), extended (R_1/2 ≈ 3–7 kpc) discs with deep integrations (the paper itself quotes 4–20 h as typical) and forward-modelled beam smearing. The transfer is a qualitative argument by analogy, not a calibration.
3. **The V_rms and inclination results are figure-only.** No size of the bias in V_c or in i is quoted, so none can be applied to a lane.
4. **The SINFONI mock skips dimming,** and that is the mock closest to KMOS3D/SINS practice. Its "smoother" result is therefore beam smearing alone.
5. **The Δχ² comparison mixes samples.** The paper's own mock value (2.81) is compared with Übler's Genzel value (2.1). That shows high-z curves *can* look symmetric for instrumental reasons. It does not show that Genzel's discs are in fact asymmetric.

**Grade: a systematic WARNING, unquantified for slope.** It cannot be used as a correction in any lane. The record entry should read "makes disturbed outskirts invisible and curves look regular; no slope bias measured".

## Where it touches the record: CFG401's zC 400569 (same galaxy as CFG278)
CFG401 (230413b75c) lists zC 400569 as one of the three "a0 → 0 (grid edge)" discs behind the possible high-z tension. The same galaxy is CFG278's Lelli+2023 disc, where ALMA CO and Hα are nearly flat to ~0.88″ (V_rot mean 254 km/s, SD 21.6).

The following is from the committed digitised points, with no fit or new computation:
- CFG401 fits only points beyond the 0.6″ FWHM cut. For zC 400569 that leaves 6 points (cfg400_points.csv, observed major-axis v): −0.875″ 209.6, −0.745″ 222.6, −0.616″ 204.6, +0.703″ 216.6, +0.832″ 216.6, **+0.982″ 183.5 km/s**.
- **Only one of the six declines:** the outermost receding-side point. It lies beyond the last CO/Hα point of Lelli+2023 (0.88″), and the approaching side has no point that far out.
- Inside the shared range, the curves agree in shape: flat. Deprojected with Lelli's i = 54.5°, Genzel's flat part gives 251–274 km/s, against Lelli's 266–285 km/s at 0.66–0.88″. Genzel's Table 1 inclination (45°, used by CFG400/401) gives 289–315. The two inclinations differ by ~10°, which changes the normalisation, not the shape.

**Reading.** For this galaxy, the "falling" shape that sends a0 to the grid edge rests on one one-sided point, in the faintest outer annulus. That is exactly the regime the paper says is unreliable (outskirt high-velocity values lost to dimming, asymmetry rising outward). In the same galaxy, a colder tracer shows no decline out to the radius it reaches. This does **not** show that the point is wrong, and the paper gives no number to correct it with.

**Inclination, the paper's other bias.** The paper finds high-z inclinations biased toward face-on. In Genzel's Table 1 (as transcribed in cfg400_test.py), the two lowest inclinations of the six are D3a 6397 (30°) and zC 406690 (25°), and both are CFG401 grid-edge discs. The third, zC 400569, has 45° in Genzel against 54.5 ± 5.0° from Lelli's CO 3-D fit. With the baryon scale free, a normalisation change is not fully absorbed by the fit, so a0 can respond to it. This is a coincidence noted from the table, not a tested cause: two of two face-on discs, out of six.

**Possible follow-up (not run, needs frozen criteria first):** rerun CFG401's G-CONSISTENCY with each galaxy's single outermost point removed and with sides folded symmetrically, to see whether the three grid-edge discs leave the edge. If zC 400569's a0 moves off the edge when 0.982″ is dropped, the tension is driven by a single point. The other two (D3a 6397, zC 406690) would need the same check, plus an inclination variant (for example i ± 10°).

## Other leads the paper points to (already on disk)
- Lelli+2023 (arXiv:2302.00030): CFG278. CO flat for zC-400569 and zC-488879. The baryon-budget conflict there is the SED-vs-dynamical stellar mass, not the shape.
- Tiley+2019 (stack shape depends on normalisation; flat when normalised by R_d): in the citation works index.
- Lang+2017 (arXiv:1703.05491): the stacked falling curve. The paper's point that outskirt asymmetry is random bears on stacking.
- Übler+2021 (TNG50 mock asymmetries, 46.8 vs observed 2.1): 2 mentions on disk.

kappa = 1/2 FITTED; not theory closed.
