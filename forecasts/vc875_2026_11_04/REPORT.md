# VC875: galaxy-specific pre-release forecast, 2026-11-04

**Conclusion:** November13's high-resolution unit is valuable for resolving VC875's gas structure and motions, but the existing evidence does not support expecting a clean separation of PAPER66 F-DESI, constant-scale MOND and dark matter. Nominal model differences are3–10km/s over1.28–8kpc. A9.4% reduction in gas normalization, accompanied by a4.6% increase in stellar normalization, lets MOND mimic the entire nominal F-DESI curve within2.0km/s. The available baryonic uncertainties are larger. This is a correction to the optimism of the earlier target shortlist, not a positive test result.

## Inputs actually available

VC875=vuds_cosmos_5110377875, z[CII]=4.5505, RA150.3847deg Dec2.408447deg. Only public older data and public metadata were accessed.

| Input | Value and status |
|---|---|
| Stellar mass | log10(Mstar/Msun)=9.94 from summed JWST pixel fits. Integrated parametric/nonparametric alternatives9.68/9.97; legacy estimate10.2 also screened. Formal pixel-fit errors are not the total systematic uncertainty. |
| Stellar radius | **1.4kpc UV-size proxy**, not a measured stellar-mass half-radius. Alternatives0.93 and2.0kpc explicitly retained. A numerical JWST mass map was not obtained. |
| Existing public unit | uid://A001/X2d1f/X33c, project2022.1.01118.S, public since2024-03-24 |
| Cube used | Pipeline spw25 PB-corrected cube plus PB cube, downloaded from public product tar; no manual CLEAN or visibility reprocessing |
| Existing synthesized beam | 0.3353 x0.2965arcsec from FITS header |
| Channel width | 6.841km/s |
| Measured channel noise | 0.451mJy/beam before PB correction, equivalent0.373mJy/beam per10km/s |
| Integrated line flux | 3.30Jy km/s inside1.5arcsec, after continuum subtraction; aperture1–2arcsec gives3.12–3.30. Old catalogue2.77+/-0.17 is a useful comparison; different windows/masks/calibration can matter. |
| Gas/light morphology | Beam-convolved exponential approximation gives Re=4.14kpc, axis ratio0.663, sky PA158.4deg. Independent published older disk-size estimate is4.1+/-0.5kpc. This is a light profile, not an independently measured mass profile. |
| Fiducial gas mass | L[CII]=2.148e9 Lsun; alpha[CII]=31 gives6.658e10 Msun. This conversion is an assumption, not a direct gas weighing. |

Public cube measurement: continuum is the mean of channels with |v|>400km/s, integrated line window |v|<260km/s, using z4.5505. Moment fit uses a circularized Gaussian approximation to the beam; the residual RMS0.0388Jy km/s/beam is comparable to the off-source moment-map RMS0.0426. Its total extrapolated exponential flux3.97 differs from aperture flux3.30; the aperture value is used for normalization. Therefore detailed outer morphology remains uncertain. This fitting step measures brightness only and was not adjusted to favor a gravity model.

The baryonic model is two thin exponential discs, with this gas profile and the explicitly provisional stellar-size proxy. This is a galaxy-specific conditional forecast, **not a unique actual velocity prediction recoverable from perfectly known mass maps**. Missing neutral/ionized gas, nonuniform conversion factors, finite thickness and environment can change it.

## Predictions

PAPER66 canonical n1 law and a00=9.3603e-11m/s², fixed w0=-.838,wa=-.62, give a0(z)/a00=.6603445. Matched MOND uses the same local normalization/interpolation, constant with redshift. An additional1.2e-10 MOND normalization is in predictions.csv, but is a different calibration comparison. F-flat is identical to matched MOND.

| Radius kpc | Newtonian baryons | F-DESI | Matched MOND | Illustrative NFW halo, M200=1e12Msun | F-DESI–MOND gap |
|---:|---:|---:|---:|---:|---:|
| 1.28 | 181.1 | 187.3 | 190.2 | 208.5 | 2.8 |
| 2 | 210.0 | 218.3 | 222.0 | 244.9 | 3.7 |
| 3 | 227.2 | 238.4 | 243.3 | 271.6 | 4.9 |
| 3.84 | 232.1 | 245.8 | 251.6 | 284.0 | 5.8 |
| 5 | 231.5 | 248.7 | 255.8 | 293.2 | 7.1 |
| 6 | 226.9 | 247.3 | 255.3 | 296.8 | 8.1 |
| 8 | 212.2 | 238.9 | 248.7 | 297.4 | 9.8 |

All velocities km/s, circular speeds before pressure support. Radii are calculation points, not claims of detected outer rings. The1e12 halo is an illustrative fixed mass, not a unique Lambda-CDM prediction or a halo selected independently for VC875.

The108 mass/size branches span stellar logs9.68/9.94/9.97/10.2, stellar radii.93/1.4/2kpc, gas radii3/4.14/4.6kpc and alpha[CII]15.5/31/62. At3.84kpc F-DESI spans173–390km/s; at5kpc178–379. These are sensitivity envelopes, not credible intervals. Even this factor-two gas bracket is not an exhaustive inventory of possible gas conversions.

## Nuisance-model comparisons

Fitted coherently at15 radii1–8kpc, holding shapes fixed, allowing stellar shifts+/-0.2dex and gas shifts+/-0.3dex:

- Matched MOND: stellar shift+0.01957dex, gas shift-0.04282dex; RMS residual1.00km/s, maximum1.99km/s against the F-DESI curve. At5kpc this gives247.94 versus248.69km/s.
- NFW: mean Dutton–Maccio concentration relation, fitted total-equivalent M200=3.585e11Msun; stellar shift+0.01352dex, gas shift-0.14854dex. RMS residual2.35km/s, maximum4.64km/s. At5kpc246.90 versus248.69km/s.

The halo uses dark amplitude.843M200 and enforces baryonic mass<=.157M200. This fit hits that inventory limit, so it is a high-baryon-retention example, not a posterior-typical halo claim. No abundance-matching prior, contraction, core or scatter in concentration is fitted. A constructed admissible mimic defeats uniqueness in this family; it does not establish the cosmological probability of that halo. All fit starts are deterministic and the selected fits converged.

## November13 precision assessment

The upcoming uid://A001/X2d1f/X33a has QA2 pass, remains Proprietary, and is listed for2026-11-14 00:00UTC=November13 19:00EST. Metadata cover observations from2023 throughOctober2025, superseding the2023 paper's then-incomplete long-baseline status. Listed angular resolution0.04457arcsec is about0.300kpc in the adopted cosmology. Listed maximum recoverable scale1.143arcsec is about7.69kpc across, not a hard radius cutoff. Combining with the existing short-baseline data matters for extended emission.

The two line-containing spectral-window entries list0.589 and0.737mJy/beam per10km/s. They must not be assumed to be independent datasets and combined by sqrt2 without checking the actual delivered products. Actual CLEAN beam/noise depend on weighting and are not verified before release.

An idealized forward model of the measured exponential brightness was made with fixed inclination50deg, PA147deg, Gaussian line dispersions30 or60km/s, spatial beam convolution and10km/s channels. Summed squared cube differences are normalized by one independent sample per Gaussian beam area. This approximate noise model is **not an injection-calibrated significance**: it fixes geometry, flux, dispersion and masses; omits uv filtering, beam covariance details and pressure support; and does not measure actual long-baseline sensitivity.

| Scenario | Dispersion30km/s | Dispersion60km/s |
|---|---:|---:|
| New native0.0446arcsec,0.589mJy: fixed-mass model distance | 0.32 | 0.11 |
| Existing compact beam/noise: fixed-mass model distance | 2.44 | 1.05 |
| New native, after MOND mass adjustment | 0.064 | 0.024 |
| Existing compact, after MOND mass adjustment | 0.40 | 0.16 |

Numbers are sqrt(approximate Delta-chi-square) in this idealized model, not observational significance. The alternate listed new noise is worse. An explicitly hypothetical0.15arcsec/0.3mJy taper gives fixed-mass distances1.82/0.71 and mass-adjusted0.32/0.13; its noise is not promised by ALMA. Uniform high-resolution noise distributes diffuse flux over many beams: resolving small structures does not automatically improve an outer circular-speed comparison.

At3.84kpc a fixed-mass5.84km/s gap requires an effective single-point1sigma error below1.95km/s for nominal3sigma separation; at5kpc below2.36km/s. Once masses are allowed to vary, the residual requirements are substantially tighter. For comparison, inclination50+/-6deg alone gives about8.8% velocity uncertainty at first order; for245.8km/s that is21.6km/s. Improved geometry helps, but does not independently calibrate alpha[CII].

Conclusion on precision: **no credible forecast of clean discrimination from the November13 unit**. It can improve geometry and identify clumps/outflows; reduced-resolution imaging combined with the public compact data may improve rotation measurements. Neither the native metadata nor the conditional forward model demonstrates the total accuracy necessary to overcome mass degeneracy.

## Existing kinematic tension must not be hidden

Jones2021 reports Vrot=118.97+/-8.10km/s at1.28kpc and102.85+/-19.84 at3.84kpc, dispersions47.04 and60.84km/s, inclination50+/-6deg. These are rotation velocities, not pressure-corrected circular speeds; they are low-resolution, beam-sensitive measurements. The source also has reported asymmetric residuals/outflow or halo complications.

For illustration, using the fitted exponential scale length and constant dispersion, corrections Vc²=Vrot²+eta*sigma² R/Rd with eta1–2 yield124–128km/s at1.28 and128–149 at3.84. These are simplified pressure branches, not reliable new measurements. They remain below the nominal baryonic forecast. Thus the fiducial standard-alpha mass model is **not validated by the older velocities**. Beam smearing, gas conversion, geometry and non-equilibrium all need examination; one must not call this agreement or tune gas to the new curve and describe it as an independent prediction. All three positive-extra-gravity models share this input tension.

## Evidence and reproducibility

Sources:

- [Tsujita et al., Table2](https://arxiv.org/pdf/2510.18248): alternative stellar masses and fitting definitions.
- [Bethermin et al.2023](https://arxiv.org/pdf/2311.08474): compact observation, achieved beam/noise, alpha[CII]=31 conversion.
- [Accard et al.2025](https://arxiv.org/pdf/2508.13136): JWST morphology and sensitivity to gas-conversion prescriptions.
- [Jones et al.2021](https://arxiv.org/abs/2104.03099): older tilted-ring velocities, inclinations and caveats. Local extracted tables in data_assembly/highz_literature_tables/jones2021_alpine were cross-checked against the paper.
- [Fujimoto et al.2020](https://cris.unibo.it/retrieve/handle/11585/806102/e1dcb338-22ad-7715-e053-1705fe0a6cc9/11585_806102_postprint.pdf):4.1+/-0.5kpc gas-disk fit and0.93+/-0.3kpc UV size; morphology caveats.
- [Lemaux et al.](https://openaccess.inaf.it/server/api/core/bitstreams/81cef9d2-f627-4192-9f59-a099bbf17b9e/content): alternate1.4kpc UV size; neither UV size is a stellar-mass radius.
- [Dutton & Maccio](https://arxiv.org/pdf/1402.7073): halo concentration relation.
- [ALMA public product list](https://almascience.eso.org/datalink/sync?ID=uid://A001/X2d1f/X33c); data tar2022.1.01118.S_uid___A001_X2d1f_X33c_001_of_001.tar. Metadata query `SELECT * FROM ivoa.obscore WHERE target_name='vuds_cosmos_5110377875'` saved in inputs/archive_metadata.csv.

Code: measure.py and calculate_v2.py. Contract_v2.json and run02/manifest.json record inputs, hashes, versions and finite scope. Run02 completed, all five model checks passed, and the manifest validated. Checks cover profile count, optimizer convergence, analytic MOND separation ceiling, positive ordering and the disc point-mass limit. No independent full pipeline replication or calibrated detection test is claimed. Initial run01 failed solely because a numpy Boolean was not JSON-serializable; original code/record are retained, and calculate_v2.py fixes serialization. The bare exploratory measurement directory is superseded by run02/measurement.

All numerical predictions remain conditional on the declared mass/profile/pressure assumptions. Existing theory manuscripts, seals and scoring rules were not changed.
