# Gravitational susceptibility: finite-time test

2026-10-13. Status: conditional response bound and bounded numerical evidence; the cold-energy mechanism remains open. This calculation tests whether a large susceptibility can amplify ordinary gravity quickly. It supplies no experimental evidence for a new interaction.

## Assumptions and reduction

The pinned `INPUT_CARRIER_ACTION.tex` supplies the two-field carrier. In natural units its nonrelativistic equations have the form

\[
i\dot\psi=-\nabla^2\psi/(2m)+2c_3b\psi^*+2k|\psi|^2\psi,\qquad
i\dot b=(-\nabla^2/(2M)+\delta)b+c_3\psi^2.
\]

For a well-prepared, slow, off-resonant source only, eliminating it gives
\(b\simeq-c_3\psi^2/\delta\) and
\(k_{\rm eff}=k-c_3^2/\delta>0\). A condensate state is an additional assumption. Source elimination is not valid at the actual pair-production resonance. Its derivative expansion and source fraction must be small in any proposed physical realization.

The resulting contact fluid has \(P=k_{\rm eff}n^2\), \(\rho=mn\), and \(c_s^2=2k_{\rm eff}n/m\) in natural units. We **add** ordinary Newtonian gravity, rather than derive it from that matter action. The homogeneous background is defined in a periodic box with the Poisson zero mode removed:

\[
\nabla^2\Phi=4\pi G(\delta\rho_c+\delta\rho_b).
\]

These density contrasts have zero spatial mean. This prescription avoids claiming an unsupported static, infinite, homogeneous gravitating equilibrium. No cosmological fit or ΛCDM assumption enters the calculation. The established GP/Jeans framework and homogeneous-background difficulty are discussed by [Suárez and Chavanis, arXiv:1710.10486](https://arxiv.org/html/1710.10486); the response calculation below is explicit and is not claimed as a new physical law.

## Linear response and exact bound

Linearizing continuity and Euler equations, including quantum pressure, gives for each nonzero Fourier mode (the dispersion here is in SI units)

\[
\ddot{\delta\rho_c}+\omega_k^2\delta\rho_c=J\delta\rho_b,
\quad J=4\pi G\rho_0,
\quad \omega_k^2=c_s^2k^2+\frac{\hbar^2k^4}{4m^2}-J.
\]

For a stable mode \(w^2=\omega_k^2>0\), a fixed step density contrast \(B\), and zero initial carrier contrast and velocity,

\[
R(t)\equiv\frac{\delta\rho_c(t)}{B}
=\frac{J(1-\cos wt)}{w^2}
=\frac{2J\sin^2(wt/2)}{w^2},\qquad
\boxed{0\le R(t)\le2\pi G\rho_0t^2.}
\]

The inequality follows from \(\sin^2x\le x^2\), with a finite marginal limit \(R=Jt^2/2\). Static total gain \(A_{\rm static}=1+J/w^2\) can diverge near the Jeans threshold, but the first time the step response reaches that static value is

\[
t_{\rm first}=\frac{\pi}{2w}
=\frac{\pi\sqrt{A_{\rm static}-1}}{2\sqrt J}.
\]

Without damping it oscillates and overshoots; it does not settle. A diverging static susceptibility is therefore not an arbitrarily fast force amplifier. For arbitrary bounded forcing \(|B(t)|\le B_{\max}\), the same absolute response bound follows by integrating the retarded kernel and using \(|\sin(wu)|/w\le u\). That extension is an analytical observation, not part of the Lean certificate.

For an unstable mode \(\omega_k^2=-\kappa^2\), the step response becomes \(J(\cosh\kappa t-1)/\kappa^2\). Nonnegative pressure and quantum stiffness imply \(\kappa^2\le J\), hence \(R\le\cosh(\sqrt Jt)-1\), by the positive power series. This is a growing instability, not a stable amplifier. Nonlinear saturation or collapse is outside the linear result.

## Force and density scales

For a sinusoidal contrast of wavelength \(L\), requiring linear amplitude \(|\delta\rho_c|\le\eta\rho_0\) gives

\[
|\delta a_c|\le\frac{4\pi G\eta\rho_0}{2\pi/L}
=2G\eta\rho_0L.
\]

With \(G=6.67430\times10^{-11}\) SI, an induced gain of 99 within one second requires at least \(2.36075\times10^{11}\) kg/m³ under the stable response bound. A sinusoidal extra acceleration of 0.02 m/s² with \(\eta=0.1\) and \(L=1\) m requires at least \(1.49828\times10^9\) kg/m³. These are necessary scales, not viable designs: compatibility with the nonrelativistic condensate and source elimination has not been established. The acceleration is local to the Fourier profile, not uniform over a device.

At density 1000 kg/m³, the one-second induced gain is at most \(4.19359\times10^{-7}\). Tuning static total gain to 100 gives a first-crossing time of 17,065.9 seconds. Mass conservation permits redistribution, not creation of a new monopole mass.

## Executed tests

`check.py` compares the analytic response against independent DOP853 integration of \(R''+\epsilon R=1\), with dimensionless time \(s=\sqrt Jt\). All 32 combinations of \(\epsilon=0,10^{-8},10^{-4},0.01,1,100,-0.01,-1\) and \(s=0.01,0.1,1,3\) passed their recorded tolerances. Stable and nonnegative-stiffness bounds were also checked on that finite grid.

`field_check.py` evolves the actual nonlinear periodic GP–Poisson equation in one spatial dimension (equivalently, a planar mode invariant in transverse directions):

\[
i\dot\psi=-\tfrac12\psi_{xx}+[g(|\psi|^2-1)+\Phi_s-B\cos x]\psi,
\quad (\Phi_s)_k=-(|\psi|^2-1)_k/k^2\ (k\ne0),
\quad (\Phi_s)_0=0.
\]

Here \(J=\hbar=m=\rho_0=1\), the box length is \(2\pi\), \(g=0.75+\epsilon\), and initially \(\psi=1\). Six cases use \(\epsilon=10^{-4},0.01,1\), \(B=10^{-4},10^{-3}\), and final time 3. A symmetric split-step Fourier evolution uses 128 points and time step 0.002, compared with 64 points and 0.004. This paired refinement does not separately establish temporal and spatial convergence or continuum certification.

All six cases pass the stated amplitude, resolution, mass, positive-density and energy checks. At \(\epsilon=10^{-4}\), nominal static total gain is **10,001**, but the computed total gain at time 3 is **5.49966**. Relative deviations from linear response are below \(2\times10^{-6}\) in these small-amplitude cases. This is numerical evidence about this stipulated PDE, not a measurement of cold energy.

`GravityResponse.lean` certifies five exact statements: the trigonometric time bound, response nonnegativity, static-gain algebra, the density/time implication, and the wavelength/force identity. It does not formalize the field reduction, Poisson completion, empirical inputs, or numerical convergence. The compiler reports only standard Lean axioms; three deliberately damaged proofs fail as expected. All three run manifests validate against current input/output hashes.

Reproduction: `python3 check.py /tmp/gravity-mode-results.json`, `python3 field_check.py /tmp/gravity-field-results.json` from this folder; Lean requires the pinned Mathlib environment identified in `lean_contract.json`. Full executed commands, environment, bounds, logs and hashes are in `run/manifest.json`, `field_run/manifest.json`, and `lean_run/manifest.json`.

## Remaining mechanism question

This closes the claim that passive, stable susceptibility alone yields instant strong gravity in this particular Newtonian condensate completion. It does not rule out a different metric coupling, externally powered dynamics, non-condensate phases, or nonlinear collapse. None is demonstrated here. The existing action still supplies no photon-production rate or established apparatus capable of moving an object gravitationally.

The next discriminating calculation is the full, driven two-field system with source depletion and a stated energy budget, before eliminating the source. A claimed gain must be measured against the ordinary gravity of the complete apparatus, while tracking where both energy and mass move. Any proposed new metric interaction must first be specified by an action and tested for stability; inserting a gain factor would not derive it. Optical emission remains a separate, unvalidated interaction in the preceding light/gravity report.

Provenance clarification: the original run manifests retain copied metadata phrases about adaptive quadrature/finite differences (numerical runs) and finite sums/Brownian reflection (Lean run). Those phrases do not describe these computations. The actual executed scripts and commands are authoritative; the adjacent contract files correct these descriptive fields after execution. No executable input or result was changed.
