# Explicit outgoing transport changes the matter-pair threshold

2026-10-13. This replaces the *rough escape-loss comparison* in the preceding coupled-capture report with a specified one-dimensional transport problem. It does not change the microscopic pair coupling or establish a physical confining boundary. The previous turn was progress because it exposed the matter-pair channel; this turn tests whether that channel necessarily grows in a finite open region.

## Boundary problem

For a phase-matched counterpropagating pair in a uniform pumped region 0<x<L,

\[
(\partial_t+v\partial_x)u=\mu w,\qquad
(\partial_t-v\partial_x)w=\mu u.
\]

Here w is the conjugate envelope of the opposite mode, v>0 is its group speed and mu>0 is the coherent pair coupling. Impose **no incoming coherent waves**, u(0)=0 and w(L)=0, with no reflection. This is a boundary condition, not an assumed local exponential loss rate.

For time dependence exp(lambda t), the spatial matrix is

\[
\frac{d}{dx}\binom uw=\frac1v
\begin{pmatrix}-\lambda&\mu\\-\mu&\lambda\end{pmatrix}\binom uw.
\]

For real |lambda|<mu, the characteristic condition is

\[
\cos(qL/v)+(\lambda/q)\sin(qL/v)=0,
\quad q=\sqrt{\mu^2-\lambda^2}.
\]

The first zero-growth solution occurs at

\[
\boxed{\mu L/v=\pi/2.}
\]

This differs by a factor pi from the earlier estimate obtained by assigning the number-loss rate v/L and then applying the well-mixed oscillator threshold. That estimate was explicitly conditional, and should not be treated as the outgoing-boundary solution.

## Exclusion of growing modes below threshold

The threshold is not only a real-root diagnostic. For Re(lambda)≥0, integrating the two characteristics with these incoming boundary conditions gives

\[
|u(x)|\le (\mu/v)^2\int_0^x ds\int_s^L dt\,|u(t)|.
\]

The positive integral operator on the right has kernel min(x,t). It is the inverse of -d²/dx² with f(0)=0 and f'(L)=0. Its eigenfunctions are sin((j+1/2)pi x/L), with largest L² eigenvalue (2L/pi)². Taking the L² norm excludes a nonzero normal mode with Re(lambda)≥0 whenever mu L/v<pi/2. At equality a zero mode exists. Above threshold the characteristic equation has a positive real root.

This is a statement about exponentially growing normal modes of the stated linear envelope problem. It does not by itself bound every transient, prove nonlinear stability after depletion or establish the boundary conditions for the proposed material.

## Numerical cross-checks

Seven gain-length values between 0.5 and 3 are tested on 80-, 160- and 320-cell upwind grids. All seven eigenvalue errors decrease under refinement. The largest finest-grid error in dimensionless growth rate is 0.0193; therefore the exact threshold, not the finite-grid sign at the threshold itself, supplies the marginal-stability result.

Shift-invert finds an eigenpair near the analytic prediction. To avoid treating that targeting as an independent confirmation, the script also checks the eigenvector is strictly positive and verifies its matrix residual. The discretized generator is irreducible with nonnegative off-diagonal entries, so that eigenpair is its dominant real mode. Five separate spatial ODE integrations check the outgoing boundary residual below 10⁻¹⁰.

An initial untargeted eigenvalue search was stopped after unexpectedly long execution. The successful bounded run uses the targeted solve, a 2000-iteration cap and a cooperative single-thread cap. `run_v2/` is the canonical record with the clarified contract; `run/` records the same executed script before the metadata was clarified. Neither exploratory runtime nor a targeted solver alone is treated as physical evidence.

## Escape does not eliminate pair production

At zero frequency, allowing incoming quantum fields gives a Bogoliubov scattering map with transmission amplitude sec(G) and pair amplitude tan(G), where G=mu L/v. It obeys

\[
\sec^2G-\tan^2G=1.
\]

Consequently vacuum inputs still produce an output occupation tan²(G) per frequency channel, below threshold. Four values check this commutator identity. These are not an integrated power or heat calculation. An open region may avoid an absolute instability while continuously losing energy and particles through amplified outgoing modes; source replenishment and backreaction remain necessary.

## Physical comparisons and three-dimensional limits

Using the previously computed microscopic vertex and v approximately 5.02×10⁵ m/s:

| Target excitation fraction | Critical open path length pi v/(2 mu) |
|---:|---:|
| 10⁻¹² | 14.14 mm |
| 10⁻⁹ | 447 micrometers |
| 10⁻⁶ | 14.14 micrometers |

For the lowest target, a one-centimeter path has G=1.1109<pi/2 and has no growing normal mode under these outgoing assumptions. Thus the previous rough centimeter estimate does **not** exclude this particular open-path configuration. The two higher targets remain above threshold on that path.

An infinite planar slab is not stabilized for all directions merely by making its thickness small: grazing rays have longer escape paths. For a finite ball in a straight-ray approximation, requiring its **maximum chord**, the diameter, to satisfy the bound is a sufficient condition for every independent ray channel in that approximation. This is not a full three-dimensional Bogoliubov/interface calculation. Reflections, angular coupling, density variation and diffraction can change it.

Most importantly, allowing energetic excitations to escape does not explain how the underlying very dense, repulsively interacting condensate is held in place. The interface must confine the background while admitting the assumed outgoing modes. No such trap or boundary interaction has yet been derived from the proposed action. A planetary self-gravitating configuration cannot borrow millimeter escape paths without a separate transport argument.

## Research consequence

A finite open geometry can change the earlier instability verdict, so it was necessary to solve the boundary problem rather than promote the leakage estimate into a no-go theorem. This leaves a conditional path: sufficiently short nonreflecting matter-mode trajectories, together with continuous externally powered preparation. It also makes the remaining construction requirement precise: **selective confinement of the condensate with transmission of the produced excitations**, followed by a replenishment and heat budget.

The audited result is analytic and numerical, not newly Lean-certified. It supplies neither an experimentally established portal nor a gravity-enhancing mechanism. The overall goal remains incomplete.
