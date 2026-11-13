# FOR J0332 data audit

Reproduce: `/private/tmp/forj0332-fit-venv/bin/python data_audit/audit.py` and `data_audit/deflection_audit.py` from the fit directory. Input SHA256s are in audit.json; no inputs were modified. The separate inputs/fetch_provenance.json records public URLs and fetch times.

## Orientation / masks

FITS data have north increasing with row and west increasing with column. For zero-based array indices i,j, the 100x100 cutout grid is X_west=(j-49.5)*0.1 arcsec and N_north=(i-49.5)*0.1. Pipeline y_south=-N, x_west=X. The supplied circle uses y_south centre +.35, x_west centre -.25, radius4.77008609 arcsec. Source segmentation includes bright extended arc and fainter counterimage; artefact masks remove other compact objects. Source/lens mask regions can overlap slightly: do not sum their counts as disjoint.

## PSF and published model

Raw VIS PSF sum=.9476920533441808; centred maximum at(10,10); tiny negative minimum -1.27e-7. Unit-sum normalization is empirically REQUIRED to reproduce released convolution: convolving pre_psf VIS_GALAXY_1 with normalized PSF matches model VIS_GALAXY_1 at relative L2 2.78e-14. Unnormalized mismatch5.23%. Lens galaxy mismatch after normalization .232%, plausibly finite image-edge/blurring-region or oversampling differences; not exactly reproduced. Do not silently clip tiny negative PSF entries without recording it.

Released model sum versus observations with supplied RMS and circle+artefact mask: N6711, chi2=4086.861, chi2/N=.608979. This is not reduced chi-square: no parameter count/effective regularized-source degrees of freedom subtracted. Source region N415 has chi2/N2.77270 and structured residuals visible. Background residual std .6743; residual RMS over full valid region .7801. Pixels are correlated: clipped outer-background nearest-neighbour Pearson .2301 horizontal/.2288 vertical, diagonal .0753. These are descriptive local estimates after selection/clipping, not a full stationary noise covariance model. Supplied diagonal RMS likelihood cannot be treated as independent unit-normal pixels; nor does global chi2/N<1 establish arc adequacy.

## Sersic radius convention

CSV posterior medians give q=.809921 and Re1.0621497,n5.66335. Test of median shape versus released unconvolved lens map (free scalar normalization only, .3<r<3 arcsec): geometric-mean radius R=sqrt(q*x_major^2+y_minor^2/q) gives relative RMS .0277; semi-major radius sqrt(x_major^2+y_minor^2/q^2) gives .0731. Correct y_south centre/orientation strongly preferred over flipped y.

Using COOLEST-Sersic POINT ESTIMATE instead of CSV medians improves geometric-radius agreement to .00301 relative RMS, versus .04168 for major radius. This supports Re as geometric-mean/circularized effective radius; do not divide by sqrt(q) twice. Residual differences and distinct posterior summaries prevent claiming machine-precision Sersic-map reconstruction. COOLEST point values Re1.13918,n5.86872,q.813379 differ from CSV medians. The published image model is not necessarily generated from posterior medians.

## Exact released SIE deflection reproduction

Deflection/convergence/potential maps are 102x102 with a one-pixel border. Their WCS CRPIX shifts by+1 vs100x100 science image. Crop [1:-1,1:-1] for science pixels. Headers explicitly state SKYFRAME pipeline+y south,+x west and DEFLECTIONS_Y>0 south. Set alpha_N=-DEFLECTIONS_Y; alpha_X=DEFLECTIONS_X. Grid X=(j-50.5)*.1,N=(i-50.5)*.1 for102x102.

Use coolest.json mass POINT ESTIMATE (not CSV median). Sky coordinates X=west,N=north; lens centre (cx,cn)=(-.1945893971,-.3150031621). Major-axis angle a=pi/2+phi_COOL, where phi_COOL=-32.62048648deg. q=.7632323814, theta_E=1.4792113260. Rotate centred sky coords: u=cos(a)*(X-cx)+sin(a)*(N-cn), v=-sin(a)*(X-cx)+cos(a)*(N-cn). Set f=sqrt(1-q^2), psi=sqrt(q^2*u^2+v^2), b=theta_E/sqrt(q). Then alpha_u=b*q/f*atan(f*u/psi), alpha_v=b*q/f*atanh(f*v/psi), and rotate back into(X,N).

Add external shear about the GRID ORIGIN (not lens centre): angle a_g=pi/2+phi_ext_COOL, phi_ext_COOL33.75855308deg, gamma=.06796891320; g1=gamma*cos2a_g,g2=gamma*sin2a_g; alpha_X,shear=g1*X+g2*N; alpha_N,shear=g2*X-g1*N. This reproduces BOTH full-map deflections at vector RMS4.35e-16arcsec excludingr<.4arcsec! Implementation and 48 tested convention alternatives in deflection_audit.py/deflection_tests.json.

Source-plane mapping beta_X=X-alpha_X, beta_N=N-alpha_N; CSV source reconstruction y uses SOUTH, so beta_y_south=-beta_N. Source coefficients/noises live on an irregular mesh (vis_pix_source_plane_reconstruction_0.csv). Exact ray-traced pixelized source reconstruction additionally requires the original interpolation/oversampling scheme and regularization; a generic triangulation is not established as identical here. However released pre_psf source image plus normalized PSF reproduces its final blurred source map exactly. COOLEST placeholder lens/source z=.5/1.0 MUST be replaced by real .986/3.773 for physical-distance calculations; the angular deflection reproduction needs no redshift values.

## Diagnostic image

vis_diagnostics.png displays observed/model, normalized residual and source/artefact/circle masks with explicit orientation. It was rendered and visually inspected. Audit only; no user-theory model fitted.
