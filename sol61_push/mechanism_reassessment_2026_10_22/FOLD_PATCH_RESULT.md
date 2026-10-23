# Regular local absorption integrals through the two folds

The angular-momentum coordinate change now yields finite, convergent absorption integrals through the selected fifth- and sixth-harmonic energy folds. This calculation includes an actual potential Fourier coefficient rather than a constant numerator. It validates a local integration method needed for the response calculation; it does not solve the full response or a damped mode.

## Contract and normalization

Use the A10000 spherical equilibrium and the same finite-A dilation trial potential as KINETIC_WEIGHT_RESULT.md, normalized to max absolute potential1. Set omega=.8228. Around each energy minimum from DIRECT_FOLDS_RESULT.md, integrate a fixed energy interval with half-width1e-4. At every quadrature energy, solve n Omega(E,u)=omega for u in [.9u_center,1.1u_center], evaluate the fixed-energy derivative Omega_u, and compute C_n from the radial orbit. The scalar patch absorption is

    B_patch = 2 pi³ F integral_patch C_n(E,u(E))²/|Omega_u(E,u(E))| dE.

This is a single-counted local resonance arc. It includes both sides of the energy minimum as energy traverses the interval. It must not be added to a full-curve integral that already includes that arc. A nonzero C_n is required; a coordinate fold alone does not establish absorption.

## Results

| harmonic | B_patch, energy order32 | B_patch, energy order64 | relative change |
|---|---:|---:|---:|
|5|2.08866704e-5|2.08866688e-5|7.84e-8|
|6|4.03366222e-8|4.03366267e-8|1.12e-7|

Order16 uses1024 orbit-phase points and derivative step1e-4u; orders32/64 use2048 phase points and5e-5u. The combined16-to32 change is approximately3.7e-5 relative for each patch. Because multiple controls change together, that is a consistency comparison rather than a separate bound on each error source. The period/root calculation uses128-point Gauss integration; previous direct-fold work varied that integration order.

On the sampled patches, |Omega_u| stays above10.57 and12.15. The fifth-harmonic coefficients range approximately-.002971 to-.002886; the sixth approximately-.0001603 to-.0001129. These establish nonzero coupling for this prescribed trial. They do not give coupling to the self-consistent complex mode. The small sixth-harmonic patch value is not a bound on the whole sixth-harmonic curve, and the chosen patch widths are numerical domains, not physical selections.

## Verification and remaining work

fold_patch.py reconstructs the background through the definition-only prefix of direct_folds_v2.py, builds the dilation potential, and evaluates the two local integrals. The prefix delimiter excludes the earlier experiment loop. Declared dependencies include that file, cold_limit_run/results.json, and direct_folds_v2_run/results.json. fold_patch_run completed, its manifest validates, and four finite checks pass: resonance residual, nonzero coordinate derivative, positive absorption and32-to64 quadrature agreement. Reproduction argv, hashes, versions and timing are in fold_patch_run/manifest.json.

The result is conditional floating-point evidence for these patches. It does not provide exhaustive root coverage, full harmonic integrals, a response matrix, analytic continuation, a physical damping rate or formation. The next substantive step is a complete, nonoverlapping curve integration with matrix-valued Fourier products and frequency variation, checked against the existing absorption calculations away from folds.
