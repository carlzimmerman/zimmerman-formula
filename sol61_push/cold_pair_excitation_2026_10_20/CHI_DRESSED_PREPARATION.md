# Distinct quasistatic-chi Cauchy preparation

The frozen initial-data audit completed **56/56 checks** in `chi_dressed_initial_run_001`; its manifest validates. It generated four separately named `dressed_Y20_K{0,1,50,500}.bin` files. This is a restricted neutral-field preparation of new Cauchy data. No field evolution or physical cooling occurred.

## Preserved failed implication

The undressed constructor `clean_mode_seeds.py` and completed 26-check `clean_mode_initial_run_001` are unchanged. Although that run correctly retrieved prescribed linear mode coordinates near 50 and 500, the actual full-action excess `Delta E - omega Delta Q` was 549.09285279 and 50811.41287609. Nominal linear K therefore did not specify the actual finite-amplitude excess energy. In particular the raw K500 seed should not be interpreted as an isolated 500-energy excitation.

A heavy neutral field that is displaced by only the linear eigenmode need not remain near its nonlinear energy-minimizing value at the perturbed charged density. The difference between those preparations can carry substantial energy without a correspondingly large change in the linear projected coordinate.

## Exact restricted equations and controls

Keep all eight charged field/momentum arrays fixed byte-for-byte. With `I=|Psi|^2`, minimize the neutral configuration functional

`F[h;I] = sum FVvolume [ (grad h)^2/2 + U(h) + a h I ]`.

The same cylindrical finite-volume, axis-regular, zero-Dirichlet Laplacian used in `pair_axisym_v2.c` gives

`-Lap h + U'(h) = -a I`,

`U'(h)=M^2 h - 3 M h^2/8 + h^3`.

The Hessian is strictly positive because

`U''(h)=3(h-M/8)^2+61 M^2/64 > 0`,

and the weighted discrete `-Lap` is positive. Thus the fixed-I neutral configuration minimizer is unique. The mass-dominated fixed-point iteration keeps the same equation and stops at the frozen absolute/scaled residual tolerances; it does not alter potential coefficients or thresholds.

Differentiating the static equation supplies the instantaneous tangent:

`(-Lap + U''(h)) hdot = -a Idot`,

`Idot=2 Re(Psi* Psidot)`.

Here the asterisk denotes complex conjugation. This is tangent data for the restricted static manifold, not proof that the full field dynamics follows that manifold. At a general phase the neutral kinetic energy may change either way. In these turning-point seeds `max|Idot| <= 6.31e-16`, so the tangent is already zero within the frozen tolerances.

The static solves used 3, 4, 5 and 6 updates for K0, K1, K50 and K500. Their largest final absolute residual was `5.619e-9` and largest scaled residual `3.794e-13`; tangent residuals were at most `8.428e-14`. Observed-iterate supnorm contraction bounds stayed below 0.01312. The source signs were independently checked by central variations of the complete same-grid energy at the raw K50/K500 configurations: relative errors `4.77e-10` and `2.41e-10`.

All charged arrays remain byte-identical to their raw input, hence total Q is **exactly unchanged** in the discrete diagnostic. K1 is explicitly constructed by interpolating K0/K50 charged fields and momenta with the original linear coordinate, rather than importing a new normal-mode solution. Positive-face and Laplacian energy sums agree; each output roundtrips exactly; net axial momentum is negligible. Axisymmetry enforces Jz=0 and supplies no orbital angular-momentum transport test. Peak RSS was 212713472 bytes.

## Actual prepared data

The reference carrier is fixed at `omega=0.9120838357251844`; the radial Q136000 cache is an interpolated discrete stationary reference, not a true-origin continuum BVP. Actual snapshot Q is deliberately reported instead of forced to the radial reference.

| Nominal linear K | Actual Q | Actual E | Conditional projected K | Actual Delta(E-omega Q) from dressed K0 | Energy change versus raw preparation |
| --- | --- | --- | --- | --- | --- |
| 0 | 136190.66135136 | 127610.61668185 | 0.00000004 | 0.00000000 | -0.00000204 |
| 1 | 136220.48754565 | 127638.65771910 | 0.99953338 | 0.83704756 | -0.20000512 |
| 50 | 137537.66931626 | 128888.11063856 | 49.99624607 | 48.90976534 | -500.18308949 |
| 500 | 149498.21682388 | 140638.90420050 | 500.01982321 | 890.68127915 | -49920.73159898 |

The neutral minimization removes 500.18308949 and 49920.73159898 units of energy **between different preparations** at K50 and K500. Those are not emitted energy or a radiative efficiency. The actual dressed K500 excess remains 890.68127915, so even the dressed seed does not satisfy `actual excess = nominal K`. K1 gives actual excess 0.83704756; this coarse FV preparation and reference projection are not an exact finite-grid nonlinear normal mode.

Full-field mismatch relative to the spherical reference is approximately 0.09679 at K50 and 0.30639 at K500. The tiny ell2 reconstruction residual after chi preparation means that the projected ell2 state remains close to its linear coordinate; it does not turn the full nonspherical state into a nonlinear periodic solution or its projected coordinate into conserved energy. The new neutral response also contains angular sectors beyond the seed ell2 perturbation. Neither charged monopole/DC data nor a nonlinear carrier/shape frequency were solved.

## Next discriminating use

These files are suitable for a separately authorized, immutable-source field-evolution comparison with their own K0 control. Track actual charge and energy, escaped inventory and aperture stock; require time/grid convergence; examine ell2 phase/frequency and reconstruction residual after the initial transient. Compare the prepared finite-amplitude state with the actual merger remnant under the same matched-reference conventions. A coherent softened frequency in this clean comparison would support an amplitude effect; persistent residuals or evolving monopole/background would leave a mixed-state interpretation. The present initial audit alone selects neither outcome.

Do not apply a weak-amplitude second-harmonic damping rate to K500 merely from successful coordinate retrieval. No merger injection fraction, physical mass/length/time calibration, dwarf-selective cold retention, Fornax/Leo I non-overboost or full-theory completion follows from this preparation.
