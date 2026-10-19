# Direct four-dimensional pion-vacuum result

**Calculated result:** the ordinary massive leading-order pion determinant on a closed round four-sphere has no term proportional to H. Its linear-H coefficient and the charge derivative of that coefficient are both zero at each fixed positive pion mass. This is a result for an evaluated infrared contribution, not a statement that the full proposed QCD coefficient is zero.

The [derivation](DERIVATION.md) starts with the exact scalar spectrum, retains the constant mode, derives the heat coefficients by half-integer Hurwitz residues and defines a finite proper-time subtraction. A controlled small-H asymptotic argument, rather than a finite grid, establishes the absence of the H term. Source versions and inspected pixels are recorded in [SOURCES.json](SOURCES.json).

For one real pion, after removing the constant, H² and H4 local terms, the first retained contributions are

\[
f_{\rm res}=-\frac{74}{63}\frac{H^6}{32\pi^2 M^2}
+O(H^8/M^4),\qquad
\rho_{\rm res}=+\frac{74}{63}\frac{H^6}{64\pi^2 M^2}
+O(H^8/M^4).
\]

The stress conversion is \(\rho=f-(H/4)\partial_H f\), with the mass held fixed. For the two charged modes and their leading mass shift \(\Delta=2e^2F^2Z\), the corresponding one-loop difference is

\[
\delta\rho_{\pi^\pm,\rm res}
=\frac{74}{63}\frac{H^6}{32\pi^2}
\left[\frac1{M^2+\Delta}-\frac1{M^2}\right]+O(H^8),
\]
\[
\left.\partial_{e^2}\delta\rho_{\pi^\pm,\rm res}\right|_0
=-\frac{74}{63}\frac{F^2 Z H^6}{16\pi^2M^4}+O(H^8).
\]

No numerical alpha or pion matching constant was assigned. These are explicit four-dimensional charge-dependent curvature terms. The first term's inverse-mass singularity supplies an infrared benchmark; it is not the entire fixed-mass H6 coefficient. Higher chiral curvature operators, interacting photons, higher loops and other QCD matching contributions remain. A mass-independent R³ contact with the same coefficient cancels in the artificial shifted-versus-unshifted comparison, whereas the physical charge response can contain independently matched charge-dependent curvature terms.

The hierarchy is H much smaller than M, with M inside the chiral regime. It must not be extrapolated to zero mass at fixed H, a nonadiabatic cosmological state, or an unspecified nonlocal/topological sector. Local higher-curvature terms do not create H terms, but completeness of ordinary local chiral EFT for the proposed full QCD/global response is a separate physical premise.

Within the calculated pion loop alone, a hypothetical self-accelerating branch cannot be inferred at small curvature. For three equal zero-charge masses the retained stress is \(3(74/63)H^6/(64\pi^2M^2)\). Its nonzero solution of \(H^2=(8\pi G/3)\rho\) would require \(H^4=8\pi M^2/[G(74/63)]\). For a hadronic mass far below the Planck mass this violates H much smaller than M, so that algebraic root lies outside the calculation. It is not a prediction of a physical cosmic scale or alpha.

## Independent checks and notation clarification

Run001 completed **31 exact and finite numerical checks**, with a validated manifest. It checks the exact coefficients, curved stress and charged multiplicity algebra, positive spectral heat sums and a separate UV-finite mass-resolvent sum using polygamma functions. The finite numerical comparisons are not interval-certified bounds on all omitted asymptotic terms. They test implementation; the hand asymptotic argument has separate premises.

An independent fresh child, given the problem but no target coefficients or coordinator files, derived the same heat coefficients and signs before comparison. The electromagnetic reviewer then read the implementation/manifest without rerunning the suite. Its [review packet](../../electromagnetic/s4_pion_review/REVIEW.md) records the exact scope, higher-curvature qualifications and input pins.

Clarification to the frozen derivation's final section: its expression \(\partial_{M^2}^3 f=V^{-1}\sum d_l/\lambda_l^3\) uses the *full scalar log determinant*, with UV-polynomial mass counterterms annihilated, rather than the mass-dependent heat-subtracted \(f_{\rm res}\). The latter's third derivative starts at H6. The numerical estimator explicitly subtracts the full determinant's lower H0,H²,H4 terms before comparing the H6 coefficient, so the computation is unaffected. Neither mass derivative alone fixes the integration terms; the proper-time definition does that for this determinant. DERIVATION.md and the executed input hashes remain unchanged.

The missing physical numerator remains the complete, matched QCD stress coefficient \(A_\rho\). This calculation shows that the proposed H term cannot be assigned to this ordinary pion determinant, while providing actual unfitted curvature and charge-response functions for comparison with a more complete calculation.
