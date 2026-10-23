# Final pass: a late screening obstruction and a dilute-source relic estimate

The useful new result is an energy bound: **the high-H source cannot be
continued indefinitely as an independently redshifting Phi sector that
stabilizes a freely oscillating homogeneous X reservoir.** That continuation
develops a negative instantaneous fluctuation direction near the vacuum
X-decay epoch in the simulated benchmark. This locates a late conversion
regime without assuming a thermal Phi distribution or a cold seed.

It does **not** calculate nonlinear conversion efficiency or the final
high-H cold abundance. The other completed calculation follows the much
smaller Hinf=m quantum spectrum through late decay and quantum-reaction
diagnostics. Its leading relic is cold but about 1e-29 of the target amount.
These two source branches must not be combined into a claimed solution.

## 1. Bounding the late regime without assuming Phi thermalization

Keep the original potential and the radiation background. Let E(a) be the
positive dimensionless Phi conformal Hamiltonian, including gradient,
canonical kinetic, quartic and quadratic terms, with the X interaction
temporarily omitted to test a proposed no-transfer continuation. Let
r^2=q1^2+q2^2 and mhat=m/(sqrt(lambda) Fmax). Then

\[
 {dE\over da}=\hat m^2 a\langle r^2\rangle,
 \qquad \langle r^2\rangle\le\sqrt{\langle r^4\rangle}
 \le2\sqrt E.
\]

Consequently, for a>=a0,

\[
 \sqrt{E(a)}\le\sqrt{E_0}+{\hat m^2\over2}(a^2-a_0^2),
\]

and the physical field variance obeys

\[
 \langle|\Phi|^2\rangle
 \le {F_{\max}^2\sqrt{E_0}\over a^2}
 +{m^2\over2\lambda}\left(1-{a_0^2\over a^2}\right).
\]

This uses positivity and Cauchy-Schwarz, not a guessed temperature, occupation
number, thermal mass, or particular pattern of fragmented Phi waves. The
mass-work term is retained; merely extrapolating rho proportional to a^-4
would not be valid once the quadratic term matters.

At a peak of a homogeneous radial X oscillation, choose the real Phi
direction in which the cubic coupling contributes -2g|X| to its Hessian.
The quartic contribution in any real direction is at most 6lambda|Phi|^2.
A spatially uniform test perturbation has no gradient energy. The Rayleigh
principle therefore gives

\[
 \lambda_{\min}({\cal H}_\Phi)
 \le m^2+6\lambda\langle|\Phi|^2\rangle-2g|X|
 \le4m^2+{S\over a^2}-2g|X|,
 \qquad S=6\lambda F_{\max}^2\sqrt{E_0}.
\]

The last inequality drops a negative term, so is conservative. A negative
right-hand side guarantees an instantaneous negative Hessian eigenvalue in
this specified continuation. Since a perturbation restricted to Phi is also
a test direction of the full field Hessian, allowing X perturbations does
not remove that negative direction.

For the freely evolving homogeneous X in radiation, the exact regular
solution is proportional to (Mt)^(-1/4) J_(1/4)(Mt). Its late oscillation
amplitude is

\[
 A_X(a)=B|X_0|(a_X/a)^{3/2},\quad
 a_X=\sqrt{H_{\rm inf}/M},\quad
 B=\sqrt{8\Gamma(5/4)^2/\pi}=1.44640908.
\]

Thus the stabilizing variance bound decreases approximately as a^-2 before
the mass floor matters, while the surviving X pump decreases as a^-3/2.
For a sufficiently large source, the proposed stabilization cannot persist.
This is a test of a no-transfer history, not an assumption that the actual
coupled system follows that history after it becomes unstable.

## 2. Where that test fails for the simulated high-H source

Use the saved 96^3 state, E0 approximately 0.263140664, and its originally
vacuum-built coarse X amplitude. The quadratic term at the matching epoch is
below numerical precision relative to E0. Defining
Cphi=lambda Fmax^4 E0 gives 2.48986e40 GeV^4. The bound changes sign at

\[
 a\simeq6.573\times10^{10},\qquad
 H\simeq3.112\times10^{-12}\ {\rm GeV}.
\]

Under the same visible-radiation assumption used in the source calculations,
this is Tvis approximately 1.49 TeV. At that epoch the vacuum decay width
satisfies Gamma_X/H approximately 0.601. This numerical proximity is a
benchmark result, not a universal relation derived from the action.

At twice that scale factor, the peak negative-curvature bound has magnitude

\[
 \sqrt{-\lambda_{\min,\mathrm{bound}}}\simeq0.0461\ {\rm GeV}
 \simeq46.1m\simeq23.1M.
\]

The bound is negative during about half an assumed X cycle, considering the
two alternating Phi directions. **This is not a computed growth exponent or
a daughter momentum spectrum.** A time-dependent negative Hessian does not
by itself prove irreversible amplification; the coupled fluctuation evolution
and nonlinear backreaction remain to be calculated.

The significance is that a passive background plus a narrow vacuum decay
line is not a self-consistent complete description of the surviving dense
source. Either its evolution departs from the no-transfer continuation
earlier, or that continuation reaches an unstable fluctuation regime. The
departure could involve reversible transfer or changes to X motion, not
necessarily immediate irreversible conversion. A hot conversion product
could later redshift cold, so this does not rule out a cold relic.

The source amplitude is that of one conditional coarse patch. The omitted
inflationary IR/UV covariance, possible horizon reentry of unresolved modes,
and the imposed Hinf and reheating history remain limitations. The displayed
epoch is not a cosmological prediction with those uncertainties eliminated.

`screening_exit_bound_v2_run` is the current mass-inclusive calculation. The
earlier `screening_exit_bound_run` imposed a stronger radiation-energy cap;
it is retained as a historical conditional diagnostic, not the preferred
bound. Neither calculation solves quantum number-changing conversion.

## 3. Following the dilute Hinf=m quantum source past decay

This separate branch uses the saved vacuum occupations, not the high-H
classical lattice state. The source has m=1 MeV and Hinf=m. Both charge signs
are included. The dominant channel X <-> Phi Phi has the quantum statistical
gain/loss factor

\[
 f_X(1+f_1)(1+f_2)-(1+f_X)f_1f_2
 =f_X(1+f_1+f_2)-f_1f_2.
\]

Within this reaction subnetwork, Nphi+2 NX is conserved exactly by
stoichiometry, even with Bose enhancement and inverse formation. This is
**not** a conserved quantity of the full action: 4-to-2, X-antiparticle
annihilation and other channels can violate it. It explains why speeding up
vacuum decay cannot by itself cure a source abundance deficit.

For a freely redshifting isotropic Phi occupation, inverse formation of both
X signs reduces to

\[
 R_{\rm inv}={g^2m^2\over8\pi^3}
 \int de_1\,f(e_1)\int_{e_-}^{e_+}de_2\,f(e_2),
\]

where C=1+2u_*^2, D=sqrt(C^2-1), e_+-=C e1 +- D sqrt(e1^2-1).
The implementation uses equivalent momentum limits to avoid cancellation
near a resting partner. It includes the identical-incoming-particle factor
and does not double-count an elastic resonance as a second formation process.

The integrated inverse events affect only 1.30647e-7 of the weighted initial
population. Doubling time quadrature and Gaussian orders changes that result
by less than one part per million. The inverse formula independently matches
the exact Maxwell-Boltzmann detailed-balance rate at T/m=0.05, 0.2 and 1 to
about 4e-14 relative error.

The vacuum width is Gamma_X=1.86941e-12 GeV. Integrating its decay-time
distribution, daughter recoil and subsequent redshift gives the leading
post-decay estimate

\[
 Y_\Phi\simeq4.29965\times10^{-36},\quad
 {mY_\Phi\over4.37\times10^{-10}\ {\rm GeV}}
 \simeq9.8390\times10^{-30}.
\]

At a visible temperature 0.8 eV, using g*s=3.91 for the late entropy mapping,
the leading rms speed is approximately 3.76e-16 c. Only 0.334% of the final
weighted number originates in X in this source; its late recoil dominates
this tiny rms speed. This is a momentum-redshift result, not a full
free-streaming transfer function or gravitational collapse calculation.

Diagnostics supporting the dilute treatment are:

- integrated quartic phase scale approximately 4.78e-6;
- a conservative early stimulated-event bound of about 1.45e-5 per Phi,
  on the truncated saved momentum support;
- forward X-antiparticle annihilation loss diagnostic about 1.80e-23 of
  the weighted source, even neglecting depletion by decay;
- after X has decayed and all retained daughters have redshifted well below
  u*, integrated forward 4-to-2 loss diagnostic about 2.29e-70.

The last number applies only to the stated late reference epoch and must not
be used as a bound on the entire earlier history. The full early resonant
3-to-2/4-to-2 network, real-intermediate-state subtraction, all Bose factors
and correlated quantum corrections have **not** been integrated. Therefore
the yield is a leading dilute-branch estimate with small tested corrections,
not a rigorously certified all-channel survival interval. The original
spectrum's IR/UV and cosmological assumptions also remain in force.

This branch now has a computed late decay spectrum and reaction diagnostics,
rather than only an early-time occupation. It is comfortably cold in the
leading treatment and overwhelmingly underabundant. It does not rescue or
exclude the separate dense high-H branch.

## Evidence and remaining question

Completed current evidence records are `dilute_quantum_survival_v2_run`,
`screening_exit_bound_v2_run` and `audit_late_kinetics_run`. All checks pass
and manifests validate. The initial dilute run failed JSON serialization and
is preserved as failed; it is not evidence. The free-X envelope factor was
also independently checked against the exact Bessel solution.

The high-H final cold yield remains undetermined. The new bound narrows the
problem: it supplies a late fluctuation-stability test without requiring
millions of unvalidated early-field steps or an assumed thermal closure.
It does not supply the conversion efficiency needed to finish the requested
relic calculation. No cold normalization has been inserted into collapse,
and no novelty or breakthrough claim is established by these internal checks.
