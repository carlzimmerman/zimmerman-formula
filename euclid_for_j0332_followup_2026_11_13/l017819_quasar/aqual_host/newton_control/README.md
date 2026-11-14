# Fair stars-only Newtonian control

**Finite conditional result:** with identical light-centered oblate stellar-density shapes and nonnegative-source constraints, Newtonian stars-only fields fit slightly better than fixed-a0 AQUAL in both tested foreground fixtures. They require about28% larger infinite-total stellar masses. This is not a cosmological dark-matter comparison, a calibrated gravity exclusion or a precise physical decomposition; both retain strong structured residuals.

| Fixture | Newton log10 M_infinity | Newton mass/Msun | Newton shear | Newton χ² | AQUAL χ² | Newton−AQUAL penalized-MAP objective |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| run04 | 11.47417006 | 2.979682965e11 | .0289731 | 6259.995 | 6294.445 | −15.0103 |
| run03 | 11.43988753 | 2.753515546e11 | .0242189 | 6192.876 | 6228.701 | −16.7962 |

The corresponding AQUAL masses are2.323954874e11 and2.144492008e11 Msun, from the previously frozen `positive_01` common-log(lambda)=2 cases. Each AQUAL fit was independently recomputed through the same positive-source engine and agreed with its saved χ² and penalized objective within1e-6. The comparison is directly Newton versus AQUAL, not versus the displaced-center/different-shape SIE control.

Conditions are held identical: west/north coordinates; zl=.32022095721117494,zs=1.210; edge-on deprojected Sérsic density; fixed foreground/light center,major-axis Re,n,q and angle; constant M/L; no external convergence; native VIS PSF and2778-pixel mask;21×21 source nodes,.06arcsec spacing,6×6 image-ray quadrature; two independent quasar amplitudes; common fixed log source precision2. Source coefficients are nonnegative. The foreground/quasar amplitudes and sky retain the same proper Gaussian nuisance priors and are profiled without sign bounds; fitted foreground/quasar amplitudes are positive. Two-point association eliminates unrestricted shear analytically and supplies no independent gravity discrimination.

Newton uses `aqual_lensing.make_field(...,mu_one=True)` with the same Abel density. Its a0 metadata is9.3603e-11 m/s² for schema consistency but is ignored by the Newtonian equation and Newtonian LOS tail. The stored fields explicitly contain `mu_one=True`; do not treat them as simple-mu AQUAL fields. One audited anchor field/map at logM11.4 per fixture supplies all scan deflections by exact Newtonian linear mass scaling. A fresh exact-best-mass solve verifies that scaling and supplies the physical field for dynamics.

Each fixture evaluated61 mass nodes over11.1–11.7 by.01dex, then optimized up to three local minima in neighboring-node intervals. Both optima are interior; the registered expanded10.7–12.1 range was not triggered. This is a finite scan/local optimization, not proof of the global minimum over all masses or physical profiles. Mass is the infinite-total Sérsic normalization, not the catalogue finite-aperture mass. No stellar-population/IMF or independent stellar-mass prior was applied.

The reported penalized-MAP objective is one-half[χ²+prior quadratic] at the same fixed precision and source/nuisance constraints. It is not a truncated-source marginal likelihood, model evidence or p-value. Source positivity uses the same nuisance Schur complement, diagonal whitening, Cholesky least squares and NNLS as `positive_01`. Scaled projected gradients are1.35–1.42e-13; nuisance-gradient and complementarity checks pass. Source-edge flux fractions are11.3–12.1%, so support/grid effects remain material.

## Checks

- Independent Newtonian spherical benchmark: analytic projected Sérsic mass `M*gammainc(2n,b*(R/Re)^(1/n))` in the thin-lens point-mass formula versus the2D field and explicit-target-geometry LOS integral. At.2,.5,1,2,3arcsec, differences are.0132–.0818%; transverse parity is satisfied.
- Newtonian field scaling from the anchor to freshly solved best mass has relative L2 discrepancies below2.7e-11 across phi,gr,gt.
- Exact-best-mass projected maps versus scaled anchor maps change image χ² by only2–3e-11.
- Higher field/map/LOS resolution (448×80,192×97,LOS256) changes χ² by+1.048/+.828. The baseline is320×64,128×65,LOS192, radial field boundaries1e-5–500Re.
- The6×6→8×8 image-ray quadrature changes Newton χ² by+2.375/+2.784 at fixed mass. These are smaller than the matched-law χ² differences34.45/35.83, but are finite fixtures rather than a uniform convergence theorem.
- Maximum five-probe baseline-map versus direct refined LOS512 discrepancies are.000231/.000272arcsec; refined-map discrepancies are.0000313/.0000653arcsec.

This fair comparison is much closer than the earlier SIE/AQUAL comparison. An inference is that much of that larger gap concerns the SIE's different density shape/center and associated source reconstruction, rather than an isolated sensitivity to mu. The individual shape and center contributions were not separately fitted. No Newtonian-plus-halo model, free-a0 grid, external-field AQUAL solution or full screened action was tested.

The main limitations are foreground/host deblending, finite source support/regularization, fixed astrometry/PSFs, diagonal-noise assumptions, fixed inclination and M/L profile, unknown environment, and residual model inadequacy. Independent dynamics and a properly deblended/aperture-normalized mass prior are needed to assess whether the roughly.108dex stellar-mass shift is informative. The finite image result alone supplies no modified-gravity preference or breakthrough.

## Provenance and retained fields

`run_01` completed in25.39seconds under a180second, one-numerical-thread cap. Its v2 manifest validated against current inputs. `contract_01.json` and `launch_01.json` freeze26 inputs and the explicit command. Registered result files, parent code, priors and earlier reports were not edited. The scientific child/session66492 was observed terminal with exit0; no further experiment was launched.

The exact-best Newton fields for root's Jeans calculation are:

    run_01/run_04/best_field.npz
    run_01/run_03/best_field.npz

Higher-resolution versions are neighboring `best_field_refined.npz`. Each has a `*_config.json` with mass,shape,center,a0,mu_one,redshifts,bounds and units. NPZ schema: phi,gr,gt,xf,xc,tf,tc,rf,rc,mu_one,logmass,light,zl,zs,a0. Gradients are (km/s)²/kpc and potential is (km/s)² with an arbitrary zero at the outer sphere. Each fixture also retains its anchor field/map, full mass profile, actual source/model arrays and matched-law residual figure. `terminal_state.json` records exact hashes and terminal state.
