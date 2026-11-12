# Independent full-SPARC design-scan audit

12 November 2026. Read-only inspection of scan.py, selection/contract and run01 results. I independently recounted all copied input rows and recomputed the weighted projection using an SVD projection rather than the script's least-squares fitted coefficients. This lightweight verification did not fit an observed gravity residual or rerun a physics model/background calculation.

## Verdict

The reported coverage counts and best ideal information are correct for the declared fiducial pointwise simple-mu design. No load-bearing unit, gas-sign or bulge-normalization error was found. The result is a negative target-design checkpoint in this particular source/acceleration convention, not rejection of the law or a forecast of achieved precision.

## Formula and nuisance interpretation

For angular source amplitudes A_gas, A_disk and (when present) A_bulge, plus T=D a0, reparameterize

    S_q=T/A_gas,
    r_disk=A_disk/A_gas,
    r_bulge=A_bulge/A_gas.

A common change of A_gas with these ratios fixed shifts log w uniformly, because all source amplitudes and T rescale together. At the fiducial point the log-w derivatives are therefore

    target dlogw/dlogS_q=t=a0/(g+2a0),
    nuisance common amplitude=1,
    nuisance diskratio=(1-t)f_disk,
    nuisance bulgeratio=(1-t)f_bulge.

This is exactly the script's weighted projection. With gas conversion alpha_g, S_q=a0/alpha_g; it is not T, an absolute stellar-normalization-free a0 measurement, or a gas-conversion-free observable. The common amplitude can absorb a pure velocity/inclination scale in the fixed-source-geometry model; coupled photometric geometry is not included.

The script adds a separate bulge nuisance whenever its fiducial bulge field is nonzero. All 32 bulged galaxies therefore profile both disk-to-gas and bulge-to-gas amplitudes rather than falsely forcing one common stellar normalization. This is necessary for its optimistic information interpretation.

Acceleration units are correct: (km/s)^2 becomes m²/s² with 10^6, and kpc becomes metres with 3.085677581491367e19. Gas is sign(Vgas)*Vgas², preserving negative radial gas contributions. Disk and bulge fiducials .5 and .7 match the selection. All total sources must be positive; two nonpositive-source rows are explicitly removed. e=2 errorV/V is the linearized natural-log w error. The code fits no comparison between observed V and law-predicted V; observed velocities only supply validity and fractional error weights.

## Independent numerical recount

- Input files: 175 unique rotmod templates.
- Galaxies parsed/scored: 175; galaxy exclusions: 0; metadata matches: 175.
- Raw radial rows: 3391; finite/positive-measurement exclusions: 0.
- Nonpositive fiducial total-source exclusions: 2, both UGC01281; scored rows: 3389.
- Galaxies with separate bulge nuisance: 32.
- Rows satisfying gas fraction >.5 AND .3<gbar/a0<3: **0** across all scored rows.
- Hence any-overlap galaxies, three-radius/span-coverage galaxies and coverage-plus-information intersection: all **0**.
- Best projected I: **NGC2403, 31.9464605703701**.
- Corresponding ideal local sigma_log10(S_q): **0.0768374488487dex**.
- The declared .05dex one-standard-error information threshold is **75.4446788046456**. No galaxy reaches it.

My SVD-projection recomputation agrees with the stored I values to maximum absolute difference 1.37e-13 over all 175 templates. Thus the zero intersection is not a ranking, parser or projection artifact in the stated scan. It remains dependent on fixed fiducial source shapes, stellar normalizations, acceleration value and overlap thresholds.

## Information and inference boundaries

I is the norm squared of the target log-response after projection against the stated finite global-amplitude nuisance columns. Its inverse-square-root conversion is a local linear/Gaussian ideal error with independent radial log-errors and perfect source templates. It is not an observed posterior, a calibrated uncertainty, a source-gradient-robust bound or a confidence statement about a theory. Rank thresholds and near-collinearity remain numerical design issues, though the independent projector reproduces current results.

Quality and inclination metadata are descriptive only; they do not rank or filter the result. Thus the 175 denominator is transparent and does not conceal post-outcome quality cuts. Conversely low-quality systems have not thereby been validated as usable targets. Radial covariance, pressure support, gas shape/calibration uncertainty, radial stellar/IMF gradients, warps, distance/light deprojection, PSF effects and actual nonspherical AQUAL dynamics are omitted.

The zero gas/transition overlap is a result for these existing templates and the chosen .5/.7 stellar fiducials and canonical acceleration. It does not prove no galaxy in nature, no alternative allowed population template or no future Euclid/external sample can meet the design condition. The illustrative overlap criterion is an input requirement, not a universal theorem that every informative experiment needs exactly these cuts.

NGC2403's top ranking is for this ideal quotient-information design only. It is not best agreement with the theory, an independent prediction, an observed fit or an automatically authorized follow-up target. Nor may the individual I values simply be summed to claim a population precision without defining which quotient/conversion/acceleration parameters are common and modelling their shared systematics. No ensemble result is supplied by this scan.

## Publication-ready conclusion

Accept the narrow counts and ranking. Safe wording: 'In all 175 copied local SPARC templates, the fixed design found no gas-dominated transition rows, and none reached the illustrative individual .05dex ideal quotient-information threshold; the best perfect-template local value was .0768dex. This identifies an input-coverage limitation, not an observational failure of the acceleration law.'

No correction to the current computation is required. Keep the quotient parameter name and design-versus-data distinction explicit in the report.

## Reviewed artifact hashes
- `scan.py`: `a6ea545ce411c6a172eee02ef6f6f8e043aef14af2f57258192f1cc040e59bc1`
- `selection.json`: `7f172fa011d97b78bef3e9bd599135f7ad37986113efb0511e584b8fdc4d217d`
- `contract.json`: `a02cb07f1fb89719a70c08121bb607f24ce462626bae6f384637ab23222ef051`
- `run01/results.json`: `2e64edc5ed1ff8963b1a5201856c2c46d0f66c7040de54b6543f5636911d45ae`
