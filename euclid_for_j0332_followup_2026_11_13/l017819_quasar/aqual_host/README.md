# Fixed-a0 L017819 resolved-host test

Research resumed after the paused checkpoint `dc5b24fe6f46cd989c7be091c07fed8f0ad57369`. `HANDOFF_PAUSED.md` is preserved as the historical pre-implementation state. The four bounded experiments below are now completed; no Newtonian or free-a0 experiment was launched.

**Finite conditional outcome:** isolated, smooth, unscreened AQUAL at a0=9.3603e-11 m/s² can reproduce substantial host structure with infinite-total stellar mass about2.14–2.33e11 Msun and required shear about.013–.014. Under both fixed foreground fixtures, the matched SIE field has lower residual χ² and lower penalized-MAP objective when the reconstructed source is constrained nonnegative. This ordering survives all three registered fixed source-prior strengths and the tested image-ray quadrature refinement. Both models retain structured residuals. This is not an accepted precision physical fit, empirical exclusion, Bayes factor, a0 measurement, full screened-action test or breakthrough.

## Physical-source results

Same2778 VIS mask pixels, native PSF convolution,21×21 source grid with.06arcsec spacing,6×6 image-ray quadrature; zero external convergence; two quasar positions fixed, fluxes independent. Trace-free shear is analytically eliminated to map the two points to the same source. That exact point association supplies no independent discrimination of the mass law. Fixed source precisions are log(lambda)=0,2,4; comparisons below always use the same lambda in AQUAL and SIE. Do not select among different precision fixtures by their MAP objective values.

| Fixed light fixture | log(lambda) | log10 M_infinity/Msun | Required shear | AQUAL χ² | Matched SIE χ² | AQUAL−SIE penalized-MAP objective |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| run04 | 0 | 11.366226 | .01407 | 6288.00 | 5671.00 | +310.21 |
| run04 | 2 | 11.366228 | .01407 | 6294.45 | 5672.44 | +317.91 |
| run04 | 4 | 11.366731 | .01328 | 6353.66 | 5696.88 | +337.03 |
| run03 | 0 | 11.331186 | .01296 | 6221.41 | 5755.98 | +234.42 |
| run03 | 2 | 11.331324 | .01273 | 6228.70 | 5757.45 | +242.69 |
| run03 | 4 | 11.332095 | .01144 | 6289.58 | 5783.82 | +261.44 |

The objective is one-half[χ²+coefficient-prior quadratic]. It profiles nonnegative source coefficients and four unconstrained coefficients (foreground amplitude, two quasar amplitudes, sky) with the same proper weak Gaussian priors as the control. All reported foreground/quasar amplitudes are positive. No truncated-Gaussian marginal integral is evaluated. Source positivity is solved through an analytic four-nuisance Schur complement, diagonal whitening, Cholesky least squares and Lawson-Hanson NNLS. Measured scaled projected gradients are about1–2e-13 and nuisance gradients satisfy the registered1e-5 bound; nonnegativity/complementarity are checked. This is a KKT-checked finite SPD quadratic MAP, not an optimizer-success flag alone.

Each physical-source fixture scanned31 actual mass points over11.2–11.5 in.01dex steps, then optimized up to three local minima in adjacent-node brackets. All best masses are interior; the registered expanded11.0–11.8 scan was not triggered. This finite search is not proof of a universal/global optimum. Source-edge flux fractions remain about7.6–8.6%, warning that the finite source support is still relevant. The profiles provide conditional optima, not statistically calibrated mass errors.

At log(lambda)=2 the masses are2.323954874e11 and2.144492008e11 Msun. Compared with Gaussian-source6×6 optima, positivity shifts log mass by only−.00095/−.00309dex. It substantially changes source reconstruction and residuals; it does not rescue the AQUAL/SIE ordering in these fixtures.

## Scope and conventions

Exact target geometry: zl=.32022095721117494, zs=1.210, H0=67.74, Omega_m=.3089, flat matter+Lambda distances. No source-redshift default for FOR J0332 is used. Deflections are already Dls/Ds reduced, in west/north arcseconds. The AQUAL equation is div[mu(|gradPhi|/a0)gradPhi]=4piG rho, mu=x/(1+x); the solver uses kpc,km/s,Msun, with equal weak-field lensing potentials. Smooth edge-on oblate Abel-deprojected Sérsic density has constant M/L; intrinsic q equals the observed q. External shear is a phenomenological lens-plane nuisance, not a self-consistent AQUAL external field.

| Fixture | Major-axis Re (arcsec/kpc) | Geometric-mean Re (arcsec) | n | q | Angle from west toward north |
| --- | --- | --- | --- | --- | --- |
| run04 | 1.27036353 / 6.10134350 | .95888007 | 5.52493455 | .56973454 | .952294388rad |
| run03 | 1.07343317 / 5.15551992 | .80329222 | 4.94822654 | .56001170 | .942136729rad |

Both share mass/light center west−.1444481647,north+.0467392620arcsec. Major-axis Re, converted to kpc, enters the oblate density; geometric-mean Re is not passed as the major radius. Mass is the infinite-total Sérsic normalization, not the released finite-aperture SED mass. No SED/IMF prior is imposed at this stage. Both light profiles were inferred using the same images and an SIE host model: they are deblending sensitivities, not independent photometric priors.

The fixed matched SIE pure field uses the run04 chosen theta_E,q,angle and its released mass center, recomputed through each identical fixed-light source operator. Its mass center differs from the fixed foreground center; this is explicit, not silently constrained equal. Its parameters and light fixtures were selected from the same data. Conditional MAP/score differences therefore are not model-selection evidence or measures of theory complexity.

The inherited adapter `params` arrays contain dummy SIE slots(.8,.7,1) that are ignored when evaluating an arbitrary supplied field. They are not AQUAL mass/shape parameters. Use each case's `logmass_total`, `light` and `best_field_config.json` for physical parameters.

## Numerical checks and limits

- The new-geometry independent spherical benchmark integrates exact Abel enclosed mass and the simple-mu radial force separately from the 2D field solve. At .2,.5,1,2,3arcsec, relative deflection differences are.0135–.0423%; the Abel total-mass integral is.999999949. The adapter independently reproduces the original SIE model/score exactly.
- AQUAL libraries contain21 masses11.0–11.8 by.04, field grid320×64, radial domain1e-5–500Re, polar map128×65 over.002–8arcsec and LOS192. Deposition mass and nonlinear residuals are retained without rescaling away deposition errors. Refined checks use448×80 fields,192×97 maps and LOS256, plus direct-ray LOS512.
- Direct/refined fields at the Gaussian6×6 mass optima reproduce the library's12×12 image checks: refined-minus-library χ²−.480/+.289; score−.597/−.746. Five direct probe-ray maximum library discrepancies are.000639/.000930arcsec; refined-map versus direct512LOS discrepancies are.0000220/.0000504arcsec. These finite checks do not prove a uniform continuum-error bound.
- The initial2×2 image-ray quadrature was inadequate: Gaussian-source model preferences changed with source grid and quadrature. `operator_01` preserves the complete1/2/3/4/6/8 sweep and6×6 mass/precision refits, with8×8/12×12 checks. Initial Gaussian optima are superseded for interpretation by those controls. At6×6 Gaussian best masses,8×8→12×12 χ² changes are3.91/10.77 for AQUAL and1.68/1.77 for SIE, already much smaller than2×2 artifacts.
- In the final physical-source profiles,6×6→8×8 changes χ² by1.3–4.7 for AQUAL and2.6–3.0 for SIE, far below the tested AQUAL−SIE gaps. At log(lambda)=2, exact-mass field projections change AQUAL χ² by+.0677/−.0533 relative to mass-library interpolation.
- Initial unscaled L-BFGS-B positive-source controls in `run_01` did not satisfy KKT despite one ftol success flag. They are deliberately preserved as inadequate controls. The whitened NNLS controls in `operator_01` and the mass-refitted `positive_01` are authoritative for positivity.

Source-support/regularization dependence, foreground deblending, source morphology, fixed astrometry, incomplete PSF/noise covariance, edge-on inclination, constant M/L and zero convergence remain important limitations. Shared structured residuals show the foreground/source/noise model is not yet an adequate precision decomposition. A strong next comparison would use the same positive-source mass profiling and common regularization treatment for another gravity field, accompanied by independent dynamics and deblended mass information; no Newtonian/free-a0 comparison has been performed here.

## Files, reproducibility and terminal state

- `run_01`: first two-field-library Gaussian host fit, spherical and adapter benchmarks, source-grid/quadrature controls; completed170.55s.
- `operator_01`:6×6 Gaussian mass/precision profiles,8×8/12×12 checks, KKT-positive fixed-model controls; completed52.11s.
- `field_check_01`: direct/refined fields at those Gaussian masses and12×12 image validation; completed15.09s.
- `positive_01`: authoritative physical-source fixed-precision mass profiles, matched SIE, KKT checks,8×8 controls, exact-mass central-precision validation; completed40.05s.

Each has a validated v2 `manifest.json`, frozen `contract*.json` and explicit `launch*.json` argv in this directory. Commands are recorded, not inferred from a prose plan. All runs used one numerical-library thread and stopped well inside their600/600/180/600second caps. No inputs were edited while their corresponding runs were live. All recorded scientific child processes exited0; exact manifest hashes and observed terminal sessions are in `terminal_state.json`. The sandbox denied an OS-wide `ps` inspection, so no broader process-inventory claim is made.

For root's dynamics comparison, the final physical-source fields are:

    positive_01/run_04/lnlambda_{0,2,4}/best_field.npz
    positive_01/run_03/lnlambda_{0,2,4}/best_field.npz

Each has a neighboring `best_field_config.json` specifying mass,Re,n,q,a0,geometry,bounds and units. Arrays are phi,gr,gt,xf,xc,tf,tc,rf,rc plus logmass/light/redshift/a0 metadata. The common representative log(lambda)=2 fields use exactly the masses above. Earlier higher-resolution fields at the Gaussian mass optima remain under `field_check_01/{run_04,run_03}/best_field_refined.npz`.

Per-case `reconstruction.npz` includes the nonnegative source, total valid-pixel model, coefficients, matched SIE source/model, mask, data and RMS. The registered plots reuse the renderer's generic “Gaussian source” title to describe its quadratic prior; `positive_01` arrays are constrained nonnegative and are not Gaussian posterior means. `summary.json`/final derived figures provide a concise index. No shared research inputs were edited.
