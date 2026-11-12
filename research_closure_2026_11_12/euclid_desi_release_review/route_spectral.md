# Spectral route: opposite-dispersion internal velocities

## Finding and status

There is a concrete measurement route worth a bounded pilot: take **double differences of the positions of the same isolated emission-line clumps in opposite dispersion orientations**. This cancels the unknown line-emitting morphology and an exposure-wide astrometric translation. It therefore improves on comparing an Halpha peak against a VIS continuum peak. It is an identifiability statement under explicit assumptions, not a new gravity result or a claim of methodological novelty.

The route is **not ready to produce an acceleration measurement from today's published 252 km/s example**. That example has only one blue-grism orientation, no velocity uncertainty or external kinematic validation, and no demonstrated flat outer velocity, gas mass or reliable individual disk geometry. Its Halpha wavelength is 1113.29 nm, outside the red grism. Opposite red-grism observations cannot supply the missing opposite Halpha image for that same galaxy.

The useful next result is a measurement validation, followed by a possible new dynamics sample. No a0, normalization, acceleration residual or agreement statistic was fitted here.

## 1. First-moment observable

Let x_k be the two-dimensional, flux-weighted sky centroid of emission from region k, in arcsec, for **one isolated atomic transition**. Let v_k be its line-flux-weighted line-of-sight velocity relative to the galaxy systemic wavelength. After rectification onto a common sky tangent plane at systemic observed wavelength lambda_sys, write

y_jk = x_k + u_j v_k + a_j + epsilon_jk,

where u_j = beta_j lambda_sys e_j / c has units arcsec/(km/s), beta_j is the locally calibrated angular displacement per nm, e_j is the signed sky dispersion unit vector, and a_j is an exposure-wide registration offset. The epsilon term includes PSF-centroid, local wavelength-calibration, masking and contamination errors. The first-order Doppler approximation is appropriate for galaxy internal velocities.

This equation does not require Halpha morphology to match the continuum. It requires the same region/transition, a stable emission distribution, consistent flux weighting and aperture treatment across orientations, a correct local dispersion vector, and no unresolved line mixture masquerading as that transition. The integrated centroid of a symmetric rotating galaxy measures approximately zero mean internal velocity; it does not measure rotation amplitude. Spatially distinct regions are essential.

For a matched opposite pair with u_plus = k e and u_minus = -k e,

v_k = e dot (y_plus,k - y_minus,k - a_plus + a_minus)/(2k).

The unknown spatial centroid cancels. The pair average recovers x_k, up to the mean registration offset. Thus **yes**, opposite dispersions can recover a matched region's mean wavelength without a prior spatial-centroid model, subject to the assumptions above. This does not mean a general extended galaxy becomes an IFU cube.

For two regions k,l, define D_plus = y_plus,k-y_plus,l and D_minus = y_minus,k-y_minus,l. Then

Delta v_kl = e dot (D_plus-D_minus)/(2k),
Delta x_kl = (D_plus+D_minus)/2.

Now both unknown intrinsic centroid separation and exposure-wide translations cancel in the velocity statistic. The perpendicular component e_perp dot (D_plus-D_minus) should be consistent with zero for pure wavelength displacement; it is a useful control for mismatched regions, distortions or unequal weighting. A contaminant aligned with dispersion can still pass that control.

For non-opposite calibrated vectors, replace 2k e by Delta u = u_1-u_2:

Delta v_kl = Delta u dot (D_1-D_2)/|Delta u|^2.

Unknown local astrometric changes are still nuisance parameters. Equal-dispersion directions have no leverage. With equal k and angular separation phi, centroid noise is amplified by 1/sin(phi/2) relative to an opposite pair: a four-degree pair is 28.65 times worse. Use the actual calibrated local vectors rather than nominal wheel-angle labels. The simple double-difference expression assumes the dispersion vector is constant across the small galaxy region. If k differs appreciably between clumps, the directly recovered combination is k_k v_k - k_l v_l; a local calibration and joint treatment of registration are needed before interpreting it as one k times a velocity difference.

## 2. Second moments: what can and cannot be separated

For the same photons and after subtracting the known PSF covariance, let

C_j = C_x + k^2 sigma_v^2 e_j e_j^T
      + k (e_j b^T + b e_j^T),

where C_x = Cov(x,x), b = Cov(x,v), and sigma_v^2 = Var(v). Units are arcsec^2, arcsec*(km/s), and (km/s)^2 respectively.

An opposite pair gives

(C_plus-C_minus)/(2k) = e b^T + b e^T,
(C_plus+C_minus)/2 = C_x + k^2 sigma_v^2 e e^T.

The odd part isolates position–velocity covariance. It can reveal a resolved velocity gradient, but outflows, interacting clumps or unresolved components can produce that covariance too. The even part remains degenerate between the source's spatial extent and its velocity variance.

An exact counterexample checked here uses k=0.001 arcsec/(km/s), b_x=200 arcsec*km/s, and the following two valid positive-semidefinite joint spatial/velocity covariances:

- Model A: C_x,xx=1 arcsec^2, sigma_v^2=40000 (km/s)^2.
- Model B: C_x,xx=0.99 arcsec^2, sigma_v^2=50000 (km/s)^2.

Both give the same even xx moment, 1.04 arcsec^2, and the same odd xx difference, 0.8 arcsec^2. Hence a single opposite pair cannot identify velocity variance from those moments.

Two nonparallel opposite pairs with matched photon weighting and calibrated PSFs can, in principle, separate C_x and sigma_v^2 by differencing their even moments; the direction matrices must span the relevant nuisance terms. Near-collinear angles are ill-conditioned. The nominal Wide red-grism sequence (approximately 0,180,-4,184 degrees) offers good opposite-direction centroid leverage but only a few degrees of distinct dispersion axes: it is not an orthogonal tomographic set. For even-moment axis separation of four degrees, the lever-arm penalty is approximately 1/sin(4 degrees)=14.3 relative to orthogonal axes.

Even perfectly recovering C_x does not identify inclination without a galaxy geometry model. For a circular oblate disk,

q_obs^2 = cos^2(i) + q0^2 sin^2(i),

so intrinsic thickness q0 is needed. A triaxial/prolate object can have the same projected moments. Dunn's population-level inference does not assign an exact inclination or disk geometry to an individual galaxy.

## 3. Counterexamples that survive naive reversal

**Spatially varying line ratios.** Consider two entirely stationary regions, each containing an unresolved Halpha+[NII] blend. Use approximate vacuum wavelengths Halpha=656.461, [NII]6549=654.986 and [NII]6584=658.527 nm; let r=F_6584/F_Halpha and impose F_6549=F_6584/3. The blend's apparent Halpha velocity is

v_blend(r) = (c/lambda_Halpha)
             r[(lambda_6584-lambda_Halpha)+(lambda_6549-lambda_Halpha)/3]
             /(1+4r/3).

Changing r from 0.1 to 0.5 produces **152.25 km/s of false differential velocity** even though both regions have zero true velocity. The odd displacement reverses with dispersion, exactly as Doppler motion does. Reversal alone cannot distinguish the two. This example is inside the line-ratio range used in Gabarra's injection tests. A deblending model can resolve it when data quality and spatial constraints allow; the counterexample invalidates treating an unseparated blend centroid as a pure Halpha velocity.

**Unequal spatial weighting.** If masks, persistence, crowding, continuum subtraction or PSF/aperture losses change which photons enter a region in each orientation, x_k itself becomes orientation-dependent. Spatial differencing then no longer cancels it. Two unresolved stationary knots whose relative weights reverse between exposures can fake a centroid velocity. Flux-conservation checks and common forward-modeled apertures are necessary.

**PSF and local calibration.** A normalized, centered convolution kernel preserves a full-aperture first moment. An uncalibrated PSF centroid, finite asymmetric aperture or spatially dependent PSF does not. Common exposure translation cancels in the clump double difference, but a differential local residual between regions/orientations is mathematically indistinguishable from Delta v. Detector/wavelength distortions need their spatial covariance measured, not just a global RMS quoted.

Fumana Table 3 reports PN wavelength residual rRMS of 0.205 nm for blue and approximately 0.137–0.189 nm for red configurations. At 1113.29 nm, 0.205 nm corresponds to approximately 55 km/s. This is **not a demonstrated local differential-velocity floor**: smooth/common errors can cancel over nearby clumps, whereas non-common errors do not. Fumana Sect.3.3 also describes per-exposure/detector residual trace corrections. Da Silva's NISP-P centroid requirement of 0.1 native pixels (0.03 arcsec) is a requirement for the photometric PSF pipeline, not an achieved spectroscopic differential-centroid error.

## 4. Scale and sensitivity: an optimistic illustration

At z=0.6959, nominal blue dispersion 1.239 nm/native pixel and scale 0.3 arcsec/pixel give k approximately 0.0008992 arcsec/(km/s). Actual work must use the local SIR calibration, not these nominal constants or rounded published shifts.

With a Gaussian PSF of FWHM=0.530 arcsec, a PSF-limited centroid at S/N=10 has an optimistic photon-only sigma_theta approximately 0.0225 arcsec. Four independent equal-quality centroids in the opposite-orientation/two-clump statistic then give

sigma(Delta v) = sigma_theta/k approximately 25.0 km/s,
sigma(W) = sigma_theta/(2k) approximately 12.5 km/s,

where W=Delta v/2. Extended clumps, contaminated pixels and calibration errors worsen this; repeated correlated errors need not average down. An uncorrected 0.02-arcsec **double-difference** positional bias corresponds to 11.1 km/s in Delta v. These are illustrative conversions, not errors measured for the published galaxy.

## 5. Connection to a direct dynamical test

If matched clumps demonstrably sample opposite tangent points at the same radius in a rotating circular disk, their pressure-corrected W approximates V_c(R) sin(i). In the deep, outer-flat regime,

A_proj = W^4/(G M_b) = a0 sin^4(i).

This is a useful measured projected statistic only when M_b is measured. It is not a0 until inclination, pressure support and the outer-flat/deep-regime assumptions are established. At finite radius, a resolved baryon model permits the quadratic-branch diagnostic

a0_eff(R) = [(V_c^2/R)^2 - g_bar(R)^2]/g_bar(R).

That diagnostic does not require a flat curve, but requires the correct deprojected radius, disk geometry, baryonic acceleration and a declared force/interpolation prescription. It cannot be evaluated from one published rotation-amplitude number alone.

For a deep-BTFR inference,

delta ln(a0) = 4 delta ln(W) - 4 cot(i) delta i - delta ln(M_b).

At i=54 degrees, a five-degree inclination error alone yields approximately 0.110 dex in log10(a0). The optimistic S/N=10 centroid example at W=204 km/s yields approximately 0.107 dex from velocity alone. Missing gas fractions 0.3 and 0.5 bias a stellar-mass-only pseudo-a0 upward by 0.155 and 0.301 dex. Assuming a zero-thickness disk when true q0 is 0.2,0.3,0.4 biases the inferred a0 upward by approximately 0.035,0.082,0.151 dex.

Gas and inclination can create non-identifiability, not merely a larger Gaussian error bar. With fixed known M_b but unknown inclination, A_proj is only a lower bound on a0 under the stated flat/deep assumptions. With fixed inclination and only a stellar-mass lower bound on M_b, V_c^4/(G M_star) is only an upper bound on a0. With both gas mass and inclination unconstrained, neither useful finite bound follows without additional assumptions.

## 6. Comparison with prior repo work and actual coverage

The prior archive scout already recognized that centroid precision can beat instrumental line width and that grism kinematics is real but coarse; its Section 1 also used an R>=1000/full-Halpha-window heuristic for a different z=1.5–2.5 target interval. Today's NISP result motivates a new empirical assessment for NISP resolved line-centroid work, rather than claiming the repo categorically prohibited all slitless velocities.

AT1_a0z_tracking_decision is a sample-level decision rule, not a one-galaxy test. Its relevant common-mode ceilings are approximately 0.055–0.084 dex, and it requires direct cold-gas information, declared small pressure corrections, low-baryonic-acceleration radii and a same-estimator low-z reference. Its fitted kappa cancels in the ratio; a successful tracking test would not derive kappa. For a 0.055-dex budget, each component by itself would require fractional W error below 3.17%, inclination error below approximately 2.50 degrees at i=54 degrees, or fractional mass error below approximately 12.7%; a combined budget is stricter. These ceilings apply to an uncancelled sample common mode or the final sample error, not a universal per-galaxy statistical-precision requirement: genuinely independent random errors can average down with a validated likelihood. Gabarra's published statistical sample spans 0.4<z<0.9, outside AT1's named bins starting at z=1.0.

Gabarra Sect.2 states 116 blue exposures at one orientation, plus 68 red exposures across four orientations in the same COSMOS verification field. The latter are a promising route at Halpha redshifts approximately 0.837–1.882, **if per-target coverage, masks and S/N actually supply the needed paired images**. No per-target coverage was inspected here. The z=0.6959 demonstration's Halpha is outside red coverage. At AT1 z=2.33, Halpha is beyond the red band; another line would need different ionization/outflow/blending controls.

A single 252 km/s illustration suffices to show that a potentially measurable spatial–spectral signature exists. It does not establish a calibrated speed, V_flat, baryonic mass, an acceleration measurement, a sample common-mode floor, or evidence for/against a0 tracking. A first useful pilot would test orientation reversal, flux weighting, line deblending and external velocity agreement, without looking at a0 agreement.

## 7. Computation evidence and provenance

The bounded computation uses exact rational arithmetic for 225 centroid-cancellation cases, a positive-semidefinite second-moment degeneracy, and the stationary line-blend counterexample. Floating-point calculations are confined to the illustrative error/units conversions above. There is no random sampling.

- Code: route_spectral_check.py. Direct deterministic reproduction in this delivered bundle: python /private/tmp/euclid_dr1_review_20261112/route_spectral_check.py (results directory is included). The initial bounded command and limits are preserved in the manifest.
- Contract: route_spectral_contract.json.
- Inputs/provenance: route_spectral_inputs.json.
- Output: route_spectral_run_001/results.json.
- Manifest: route_spectral_run_001/manifest.json; run.status=completed; validator returned valid evidence record.
- Interpretation: implementation and finite assertion verified in the stated exact toy cases. The uniform centroid/moment identities follow by the algebra above. This does not validate the assumptions on real sources.
- Requested repo base: 09b8dd7c6aad534bde13ade93b764607aae45b58. Observed HEAD during this route: 2ffc012fa56dcdcbb4b3d5f169ba757fe482bcb8. All three repository inputs below match the requested base byte-for-byte and were rehashed unchanged after the computation.

SHA256 inputs:

| Input | SHA256 |
|---|---|
| gabarra.pdf | a79d8dd75a74441842f948c08e0aeae70096a14fea2abc082965b4accace2508 |
| dunn.pdf | b3caa991d467137d1cd43979db5cbd304afd8d333f11e659c3bcb11a71cebae7 |
| fumana.pdf | 1e37c597c47f31ebb6bddbd6115e83c5214ada0981ab353dd4465865cb7c5d92 |
| dasilva.pdf | a835d7f308517f308d91cf9ed6846724a9fb3441d99eb05dd50adc5fcfdde517 |
| prep_2026/a0z_crossscale/archive_inventory_d2_2026.py | 1ac2d387196901cf22cd40242d3b7bf1021642363fe5760bc86aafa043bdd470 |
| rebuild_2026_10_22/AT1_a0z_tracking_decision/README.md | f82973dddd002546f5294cf0926c651d5574e28be87d13db94b23b5229e1f3a4 |
| rebuild_2026_10_22/AT1_a0z_tracking_decision/FROZEN_CRITERIA.md | 86fd40c5a0f3800a3256e58faa4b2d292dde9f57341e2d5c36082a457351f01b |

Sources reviewed for this route:

- [Gabarra et al.](https://pubs.euclid-ec.org/public/dr1/gabarra.pdf): Sects.2–4 pp.2–6 (coverage, reconstruction, injections and PSF); Sect.5.2 pp.7–9 (velocity illustration and opposite-orientation discussion); Sect.7 p.14 (limitations). GELSA is public; no calibrated velocity catalogue is supplied.
- [Fumana et al.](https://pubs.euclid-ec.org/public/dr1/fumana.pdf): Sect.3.3–3.5 pp.5–6 and Sect.5.4/Table3 pp.10–11 (local optical/trace/dispersion calibration and its residuals).
- [Da Silva et al.](https://pubs.euclid-ec.org/public/dr1/dasilva.pdf): Sect.2.2 p.2 and Sect.3–4 (photometric PSF requirements, models and sampling). This is NISP-P, not a spectroscopic velocity calibration.
- [Dunn et al.](https://pubs.euclid-ec.org/public/dr1/dunn.pdf): Sect.2 pp.2–3; Sect.5.3 pp.11–12; AppendixF pp.24–25 (population geometry assumptions and uncertainty limitations).
