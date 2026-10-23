# Principal-value response exposes phase-sensitive absorption

The real principal-value kinetic response is now numerically resolved on the tested orbit interpolation and quadratures. Combining it with the independently computed absorptive matrix recovers a complex collective response near .8228. Allowing relative phases among field components substantially reduces absorption compared with a projection on a fixed real mode shape.

However, a tentative real-axis decay indicator changes by a factor about7.5 between four and eight field shapes. This is not a converged physical damping rate or lifetime. The new result identifies why a fixed-shape absorption estimate can mislead and where the next convergence test must focus.

## Principal-value construction

For each fixed u=L² and harmonic n, the real matrix integrand is

    F pi G(E)/f(E),
    G(E)=4pi n² Omega_r(E) C_n(E) C_n(E)^T,
    f(E)=omega²-n² Omega_r(E)².

For each simple root er, subtract A/(E-er), where

    A=G(er)/f'(er)=-2pi C_n(er)C_n(er)^T/partial_E Omega_r(er),

and add the analytic term A log[(Emax-er)/(er-Emin)]. This removes the pole before numerical integration. Endpoint-completed PCHIP functions represent the orbit quantities. Energy integration uses16 or32 Gauss points per interpolation interval, with64 or128 angular-momentum action nodes.

The two energy quadratures agree in relative matrix norm to better than5.9e-7 at the three tested frequencies. Differences in the near-zero generalized eigenvalue are below2.6e-10. The64/128 action grids agree closely in that eigenvalue as well. These checks control the tested interpolation and integration; they do not certify its continuum error uniformly. The direct-orbit imaginary matrix from the prior checkpoint is retained separately rather than silently replacing it with interpolated coefficients.

At action order128 and32-point energy integration, the near-zero eigenvalue of Re D=S-Re Pi, normalized by S, is:

| omega | real-response eigenvalue |
|---|---:|
| .8220 | -.00448000 |
| .8228 | -.000840739 |
| .8236 | .00278208 |

A real-only null direction is not necessarily the correct complex mode when the absorptive matrix mixes field shapes.

## Complex field direction

Combine the real matrix with B=-Im Pi from direct resonant-curve integration:

    D_boundary(omega)=S-Pi_PV(omega)+iB.

For this diagnostic B is held at omega=.8228 across the three nearby frequencies. Solve the complex generalized eigenproblem D x=lambda S x. With x* S x=1, the exact matrix identity

    Im lambda=x* B x

checks that the resulting absorption is nonnegative. It also shows why the complex eigenvector matters. At omega=.8228, the eight-shape128-grid eigenvalue is approximately

    lambda=1.758e-5 + i 3.0603e-4.

By comparison, the fixed finite-broadening real direction used previously had projection .00618524, and the real principal-value direction has projection about .00313793. These are different directions and should not be substituted for one another. The complex direction has a smaller absorptive projection because its relative field phases change the orbital coupling. This is a property of the linear response eigenvector, not evidence that the medium dynamically chooses a loss-minimizing configuration during formation.

## Basis dependence prevents a lifetime claim

As an explicitly provisional diagnostic, linearly interpolate the zero of Re lambda and form Im lambda/(d Re lambda/d omega) at the center frequency. A single weakly damped analytically continued pole could motivate such a ratio, but that pole has not been solved here. B's frequency dependence, complex continuation and basis convergence remain missing.

| action order | field shapes | linearized crossing | provisional ratio |
|---|---:|---:|---:|
|64|4|.82248686|5.2045e-4|
|128|4|.82248621|5.2102e-4|
|64|8|.82279624|6.9046e-5|
|128|8|.82279603|6.9065e-5|

The action-grid comparison is close, but changing the field space changes the ratio by about7.5. A stable frequency is therefore not sufficient evidence for a stable decay rate. No numerical value in this table is reported as a physical damping rate, cooling time, lifetime bound or formation efficiency.

The eight-shape ratio is on the scale of the excess widths observed at moderate numerical broadening in LINEWIDTH_RESULT.md. That is a consistency observation, not an independent confirmation of a continuum pole; both calculations use the same field truncation and underlying equilibrium.

## Consequence for the mechanism search

Resonant absorption exists in the tested kinetic model, but the collective mode can couple much less strongly than a fixed real trial suggests. The next meaningful calculation is enlargement of the complex field space with consistent real and imaginary response, checking mode direction and absorption as well as frequency. Refining quadrature alone is no longer the main unresolved issue for this diagnostic.

Formation and occupation selection remain separate: a weakly damped perturbation around an imposed A10000 equilibrium is not a mechanism producing that equilibrium from cosmological initial conditions. No new coupling, phenomenological friction or complete parent has been added. Novelty is unestablished.

## Evidence

pv_run performs the bounded principal-value calculation and the complex diagnostic using pinned direct-resonance data. It passes three numerical checks and its manifest validates. The diagnostic driver reads the newly computed principal-value output, rather than relying only on the earlier probe. All interpretation is self-reviewed. The numerical checks do not certify basis convergence, which the table above does not establish.
