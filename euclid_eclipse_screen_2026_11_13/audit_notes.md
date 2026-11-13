# Numerical sensitivity screen audit

The formulas and selection in `screen.py` support a target ranking under a
spherical, isolated, stellar-only, unscreened simple-mu diagnostic. They do not
constitute a fit of the adopted screened v3s action or a statistical exclusion.
No material formula or unit error was found in the reviewed implementation.

For gN = G M3D(<r)/r², the algebraic force and fixed-baryon sensitivity are

    g = (gN + sqrt(gN² + 4 a0 gN))/2
    Sg = d ln g / d ln a0 = (1 - sqrt(gN/(gN+4 a0)))/2.

The unreduced deflection at fixed impact R is

    alpha_hat(R) = (4 R/c²) integral_0^(pi/2) g(R sec t) sec t dt.

S_alpha is the same integral weighted by Sg and divided by the unweighted
integral. The implementation has the correct prefactor and units. Multiplying
by Dls/Ds gives reduced deflection. The code's flat-background Dls/Ds expression
is correct. Local gN(RE)/a0 is a useful diagnostic but is not S_alpha.

For one mass normalization, d ln alpha / d ln Mstar = 1 - S_alpha. Accordingly,
the conditional mass-error propagation in `screen.py` has the correct linear
Jacobian. This is a local degeneracy indicator, not a marginalized uncertainty
on a0. IMF and stellar-population uncertainties are additional issues, and the
stellar SED mass must be refitted when the assumed lens redshift changes.
The verified-redshift outputs explicitly hold photo-z SED mass fixed, so their
alpha/thetaE values must not be interpreted as a theory residual or exclusion.

The PS enclosed-mass approximation is normalized correctly. Its independent
Abel mass validation uses gamma shape 2n+1 and the correct angular kernel.
The broad validation grid's 29% maximum relative mass error occurs in a small
enclosed-mass regime; it does not imply a 29% lensing error for the candidates.
Actual deflection checks are provided in `exact_sersic_check.py` and its JSON.
The exact Abel integral is independently benchmarked against the analytic
three-dimensional Gaussian (Sersic n=0.5): M3D(<r)/Mtot = P(3/2, ln(2)(r/Re)²).
The adaptive LOS integration differs from the screen's fixed-node quadrature.

For FOR J0332 / EUCL-DR1-L014994:

- Exact fixed-impact S_alpha = 0.237183570; PS gives 0.237210319.
- PS deflection error versus exact Abel/adaptive LOS = -0.03166%.
- Halving a0 changes exact deflection by -13.2615%; doubling gives +20.4595%.
- Raising stellar mass by 0.2 dex gives +43.4900% at fixed geometry and a0.

For SDSS J1524 / EUCL-DR1-L017819:

- Exact S_alpha = 0.132767132; PS gives 0.132730701.
- PS deflection error = +0.01306%.
- Halving a0 changes exact deflection by -7.2076%; doubling gives +11.8527%.
- Raising stellar mass by 0.2 dex gives +50.2620%.

Finite-difference sensitivities agree with the weighted analytic derivative to
better than 1e-7; the script asserts this and checks candidate approximation
errors below 0.1% in deflection and 1e-4 in S_alpha. These checks cover two named
candidates, not all catalog rows or arbitrary Sersic profiles. The code also
compares the screen's Abel function at each candidate Einstein radius.

The strict sample's 2,959/2,964 rows with S_alpha >= 0.1 are numerically
plausible: median gN(RE)/a0 is 4.14354 and median S_alpha is 0.21927. The
line-of-sight tail passes through lower accelerations. These counts indicate
raw model sensitivity, not the number of measured or decisive a0 tests.

Read-only output checks found actual boolean flags, no nonpositive nonmissing
DESI redshifts in the A/B table, and no infinite computed ranked values.
The rank filters reject missing, nonpositive, or deliberately unsupported
inputs. Broad numerical rankability is intentionally more permissive than
the strict photometry/model-quality and simple-geometry subsets.

External convergence, shear, morphology, gas, mass-to-light gradients and the
external field remain nuisances. In particular the Einstein condition becomes
alpha_gal(RE) = (1-kappa_ext) thetaE in the presence of an external mass sheet.
The screen's sensitivity bins are triage choices, not evidence thresholds.

Reproduction command (from repository root):

    python3 euclid_eclipse_screen_2026_11_13/exact_sersic_check.py --output euclid_eclipse_screen_2026_11_13/exact_sersic_check.json

The check reads `screen.py` and `run_02/screen_all_15072.csv`. The parent run
should hash those inputs and the check script when adding runner provenance.
