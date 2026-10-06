# A velocity residual with an analytic pressure kernel

## Decision

Use the change in baryon-minus-cold relative velocity across epochs to remove the inherited relative-velocity integration constant. A wave pressure term and a thermally decoupled gas have the same leading EdS time kernel, but different powers of comoving wavenumber. Time evolution alone cannot distinguish them. This is a conditional model discriminator, not a measurement of cold particle identity.

## Derivation

Take two nonrelativistic fluids with common gravitational potential, no drag, negligible baryon pressure except when explicitly added, and an EdS background H=H_m a^(-3/2). Let Delta=delta_b-delta_c and U=a^2 dot(Delta). In the Born approximation use the common unperturbed growing mode delta_b=delta_c=A(k)a. Common gravity cancels from the relative equation. An explicitly massive free wave gives

dot(U)=Q k^4 delta_c/a^2=Q k^4 A/a, Q=hbar^2/(4m^2).

This follows from the linearized quantum pressure in the existing wave-pressure derivation in [the previous growth report](../../growth_and_identity/REPORT.md). The calculation uses comoving k in inverse metres, a dimensionless scale factor, and SI time. It adds no microscopic abundance or mass prediction.

Integrating dt= a^(1/2) da/H_m gives

U(a)-U(a_d)=2 Q k^4 A (sqrt(a)-sqrt(a_d))/H_m,

Delta(a)-Delta(a_d)=2 U(a_d)(a_d^(-1/2)-a^(-1/2))/H_m
+2 Q k^4 A [ln(a/a_d)-2(1-sqrt(a_d/a))]/H_m^2.

For a thermally decoupled gas c_b^2=v_0^2/a^2, replace Q k^4 by -v_0^2 k^2: the time kernel is identical. A two-epoch statistic therefore obeys

S(k) = H_m [U(a_2)-U(a_1)]/[2 A(k)(sqrt(a_2)-sqrt(a_1)) k^2]
     = Q k^2-v_0^2.

Initial U cancels and primordial growing-mode amplitude A cancels, provided A is independently reconstructed within the assumed linear model. At least two k values separate the constant gas coefficient from the wave slope. If the unperturbed baryon and cold amplitudes differ, the gas term is instead -v_0^2 A_b(k)/A_c(k); arbitrary scale dependence of that ratio spoils the two-k separation. A freely fitted k-dependent sound speed, species-dependent gravity, drag, shear, or arbitrary nongrowing cold initial mode can defeat this identification. The cold density and velocity are not directly observed; converting data to S needs an explicit transfer/observation model.

## Domain and sensitivity ceiling

The controlling Born parameter is epsilon=Q k^4/(H_m^2 a_d). It must be small at the initial epoch, and the induced relative correction must also remain small. Radiation-era evolution, recombination drag, and late vacuum domination are excluded from this analytic kernel. Actual CLASS transfers in the sibling lane test the pressureless reference more realistically.

The script records illustrative SI numbers at H0=67.36 km/s/Mpc, Omega_m=0.315, a_d=0.02, and m=2e-20 eV/c^2. These are declared benchmark inputs, not fitted measurements or an endorsed mass bound. At k=0.1/Mpc epsilon is of order 1e-14; at k=100/Mpc it is of order 1e-2; at k=1000/Mpc it exceeds unity and the Born approximation fails. Large-scale pressure signatures at this benchmark mass are therefore extremely small. A proposed recombination clue must confront sensitivity, not just exhibit a formal k^4 term.

## Evidence

The bounded script compares both integrated formulas with independent quadrature, recovers mixed gas/wave coefficients from two wavenumbers and two epochs, checks cancellation of arbitrary initial U and amplitude, and detects a deliberately omitted wave power of k. A finite result verifies these formulas and stated benchmarks, not the full cosmological model. Root derivation and sibling review should be recorded separately from manifest validity.
