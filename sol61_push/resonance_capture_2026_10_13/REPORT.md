# A biased frequency ramp prepares the nonlinear mode in the reduced model

2026-10-13. Conditional progress toward preparation, not a completed cold-energy mechanism. The previous turn found that self-detuning invalidated the fixed-frequency linear drive estimate. This turn constructs a trajectory from zero excitation and tests limited parameter errors, rather than merely prescribing a final resonant state.

## Constructive trajectory

Use tau=Gamma t and normalize amplitude to the desired final excitation density. The nonlinear oscillator is

\[
\alpha'= -[1/2+i(\Delta+C|\alpha|^2)]\alpha-iF,
\]

where C is the final nonlinear shift divided by the total linewidth, and Delta is the carrier detuning in the same units. F is a complex, phase-controlled drive envelope. The previous benchmark gives C approximately 26.33, 26327.89 and 2.63×10⁷ for target excitation fractions 10⁻¹², 10⁻⁹ and 10⁻⁶ respectively.

Choose a real target R(tau) rising smoothly from zero to one. An exact solution alpha=-iR is obtained with

\[
\Delta(\tau)=-C R^2+\sigma,\qquad
F(\tau)=R'+R/2+i\sigma R.
\]

Substitution verifies both real and imaginary equations. This specifies both amplitude and phase of the optical drive; changing only the carrier frequency is insufficient. It is an open-loop calculation with stipulated knowledge of C and Gamma, not a measurement-feedback system.

The test ramp is R=3s²-2s³ for s=tau/10 between zero and one, then R=1. It starts from alpha=0. For the earlier Gamma=164.7375 s⁻¹, the ramp takes about **0.0607 s**, followed by the same duration of holding. The matter-state preparation is conditional on an already existing dense condensate and a realizable optical envelope.

## Why a small bias helps

At the final target, the real error Jacobian is

\[
J=\begin{pmatrix}-1/2&\sigma+2C\\-\sigma&-1/2\end{pmatrix},
\quad
\lambda_\pm=-1/2\pm i\sqrt{\sigma(\sigma+2C)}\quad(\sigma>0).
\]

At exact compensation sigma=0 the eigenvalues are also negative, but the triangular matrix can transiently amplify perturbations. Its propagator contains a shear 2C tau; at tau=2 there is an amplitude-gain lower bound 4C/e. Negative eigenvalues alone do not establish robust tracking.

A positive bias sigma=1/2 moves the local eigenvalues into a damped oscillatory pair. Its final |F| is 1/sqrt(2), compared with 1/2 for sigma=0. Because optical intensity is proportional to |F| for the two-beam product drive, this costs a factor **sqrt(2)** in each equal beam's final intensity at fixed target population. It does not cost a factor of two in intensity. Non-normal transient response remains possible; this change is not a universal robustness proof.

## Perturbed capture results

Test the actual nonlinear coefficient C(1+epsilon) while retaining the nominal ramp. Twelve cases cover C=26.3279 and 26327.8934, sigma=0 and 1/2, and epsilon=0, +10⁻⁶, -10⁻⁶. Each run stops if normalized complex-amplitude tracking error reaches 0.1, with a separate evaluation cap.

For the biased ramp, all six tested cases complete the ramp and hold. At nonzero coefficient error, the largest amplitude tracking error is below **7.4×10⁻⁷**. Final population errors are approximately one part per million. Thus this reduced-model route survives the particular positive and negative coefficient errors tested, instead of requiring exact parameters.

At C=26327.8934 without the bias, epsilon=-10⁻⁶ reaches the 0.1 tracking-error stop at tau approximately **4.7648**, before the target is reached. This is a verified loss of the stated tracking tolerance, not proof that no later capture or different ramp could work. Its terminal population is not a final held-state population. The positive-error case completes but has roughly 0.001 maximum amplitude error.

The highest target fraction, 10⁻⁶, has only the analytic nominal trajectory and terminal local Jacobian in this package. Its perturbed nonlinear capture has **not** been simulated. No broad claim about noise, drive-phase error, damping error, timing error or spatially varying detuning is supported by this small parameter family.

## Numerical conditioning and formal scope

Direct integration in alpha coordinates became expensive in the large-C cases. Two exploratory runs were stopped and a capped direct-coordinate run was inconclusive for several cases. Those are numerical limitations, not evidence of physical instability. The retained `check_direct_initial.py` is the rejected direct-coordinate implementation, with its failed completion assertion; it is not the successful evidence script.

The successful calculation integrates the error e=alpha+iR. For fractional coefficient error epsilon, its exactly equivalent equation is

\[
e'=-(1/2+i\sigma)e-iC\left[|e|^2-2R\operatorname{Im}e+\epsilon|e-iR|^2\right](e-iR).
\]

This removes cancellation of large terms along the target. The transformed and original right-hand sides are checked independently at six nonzero-error states. Nominal zero-error runs then remain exactly on the analytic solution by construction; their zero numerical error is not an independent test of physical capture. The nonzero-error trajectories provide the informative dynamical checks.

Three Lean statements certify the polynomial coordinate transformation, with compiler output and input hashes retained. They do not certify the nonlinear ODE solver, robustness, portal, material or device. The successful bounded-run manifest pins the script, input resonance data, tolerances, evaluated cases and outputs.

## What this advances, and what remains

The nonlinear single-mode equations now have an explicit finite-duration preparation trajectory from zero, with limited error tolerance improved by a deliberate detuning bias. This addresses the immediate self-detuning obstacle in that model. It does not establish that the same trajectory survives the full coupled optical modes: the preceding three-mode pump-depletion calculation did not include this nonlinear ramp, and results from those two approximations cannot be silently combined into a full-system proof.

The route still assumes the hypothetical photon interaction, dense condensate inventory, confinement, phase-controlled optical access and approximately fixed damping. It consumes external optical energy. The extremely small spontaneous radiative branching fraction remains; preparing a mode does not solve efficient glow generation or demonstrate enhanced gravity.

The next required test is to combine this biased ramp with the dynamical photon modes and input-output losses, then check the actual deposited matter energy and any spatial detuning. The original objective remains active and unverified.
