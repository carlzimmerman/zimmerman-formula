# AZ34 amendments

## A1 — POST-RESULT quadrature diagnostic, 2026-11-05 UTC

The frozen global512/1024-point quadrature failed at large n. Its outputs
and failed checks are retained unchanged. The exact analytic derivative-norm
identity and energy bound do not depend on that numerical approximation.

Before the diagnostic script is run, freeze a change of integration variable
y=n|x|. Integrate on unit y intervals from0 to n using16 and32 Gauss nodes
per interval. Splitting at x0 removes the absolute-value join; the transformed
transition has n-independent width. Compare the two total energies within
relative1e-6 and the norm with its exact integral within1e-8, unchanged
tolerances. n remains16,32,64,128 and amplitude1/2. Run both switch orientations.

This is additional post-result evidence about quadrature resolution, not a
replacement of the initial failing checks, a widened gate, or a proof of full
leaf existence. Preserve separate `quadrature_diagnostic` outputs and labels.
