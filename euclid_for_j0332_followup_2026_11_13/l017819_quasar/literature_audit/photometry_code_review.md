# Independent pre-result review: L017819 point-source photometry

Reviewed fit_point_light.py, light_contract.json and imported light_shapes/fit_light_shapes.py::Renderer/physical read-only. **Verdict: appropriate conditional photometric feasibility model; no critical coordinate/normalization error identified by source review.** No fit result or actual-data success is certified here.

Coordinates: image row increases north, col increases west on0.1arcsec grid centered49.5. point() samples PSF center at((shape−1)/2) and translates in the right directions. The integer control(.05,.05) places a21x21PSF atrows/cols40:61(center50), consistent with that convention. Galaxy Renderer uses same grid, with major-axis Re and geometric radius Re_major*sqrt(q). Sérsic normalization integrates the intrinsic ellipse to1 over the infinite plane; padded convolution reduces cutout-edge artefacts. The analytic central quadrature avoids a raw cusp-center pixel approximation.

Both point and galaxy PSFs are normalized by finite-stamp sums. Point templates renormalize their rendered fullcutout sum as well; at the bounded central positions little cutoff should occur, but this still defines finite-template flux, not a calibrated infinite-wing measurement. Coefficients are native integrated image units for the templates, with sky in native units per pixel. MAGZERO is recorded, not used to falsely call native amplitudes µJy. A separate photometric conversion and Galactic-extinction audit is required before stellarSED use. Empirical PSF interpolation is an approximation to shifting a pixel-integrated PSF; cubic interpolation can create small negative lobes, and empirical PSF sampling/centering/chromatic mismatch remain systematic limitations. The linear interpolation sensitivity is useful.

Linear profiling is a weighted leastsquares solution for three amplitudes+sky, with nonnegative amplitudes enforced when needed. Residual Jacobian includes reprofiled amplitudes through repeated residual evaluations. Local pseudoinverse covariance is only a conditional local approximation and can hide nearlyunidentified directions; it is not a full nuisance-marginalized physical posterior. Positivity boundaries, n/Re degeneracy and active parameter bounds need inspection.

**Acceptance caveat:** best=min(freefits,chi2) does not first require success. A max_nfev-exhausted fit could be selected if it has the smallest chi². Inspect success/message, convergence, active bounds, residual morphology, alternative starts and fine-integration changes before calling a result usable. The hard astrometric boxes, common artifact mask and radius2/3 masks also condition the result; make sure candidate quasar cores are not masked out. The starts/bounds permit the literature positions approximately but are not an independent unrestricted astrometry measurement.

The synthetic test is strong for bookkeeping: independently finer galaxyquadrature, truth differs from start, independent amplitudes, subpixelPSFs, known sky and actualmask; recovery assertions test shapes and positions. It is noiseless and generated from the SAME oneSérsic/twoPSF model and empiricalPSF, so it cannot validate realistic uncertainty, PSFmismatch, extra foregroundcomponents, quasarhost light or correlatednoise. Fine rendering is evaluated at the fitted parameters rather than refitted; large deltaχ² would require higheraccuracy fitting, not merely a reportedcheck. Crossband independent fits offer a morphology sensitivity, not necessarily real stellar color gradients.

## Exact two-image shear degeneracy

Let d=theta_A−theta_B≠0, a=alpha_A−alpha_B, and efficiency b. The equality of their backprojected source coordinates requires

  Gamma d = d−b a = v,
  Gamma=[[g1,g2],[g2,−g1]].

Equivalently [[dx,dy],[−dy,dx]](g1,g2)^T=v. Determinant dx²+dy²>0, so for EVERY supplied mass/deflection and everyb there is a unique unrestricted shear:

  g1=(dx*vx−dy*vy)/|d|²,
  g2=(dy*vx+dx*vy)/|d|².

A source position is then chosen from either ray. Thus twoimage astrometry alone places no mass constraint when both shearcomponents are arbitrary; it is not a fourimage association witness. Independent point amplitudes add no fluxratio constraint. Finite/physical shearpriors, resolved host arcs, environmental information or independent aperturestellar dynamics can discriminate, but any resulting mass information must be attributed to those added assumptions/data. This photometric code correctly avoids imposing a fourpointgate and must not itself be interpreted as a gravityfit.
