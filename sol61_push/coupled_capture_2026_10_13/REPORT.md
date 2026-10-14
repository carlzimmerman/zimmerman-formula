# Coupled optical capture exposes a faster matter-pair instability

2026-10-13. The preceding goal turn constructed a biased single-mode preparation ramp. This turn couples that ramp to dynamical optical modes and then checks the resonant matter modes previously treated as a passive decay bath. The new constraint is substantial: coherent pair amplification can invalidate the passive-width approximation before the target state is sustained. No completed cold-energy mechanism is claimed.

## Combined nonlinear optical model

Use tau=Gamma t, z=b/b_target, optical amplitudes p and q scaled so their product drives z with unit coefficient, K=kappa/Gamma and J=h b_target/Gamma. The normalized equations are

\[
p'=-(K/2+iD_p)p-iJzq^*+E_p,\quad
q'=-(K/2+iD_p)q-iJzp^*+E_q,
\]
\[
z'=-[1/2+i(\Delta+C|z|^2)]z-ipq.
\]

The optical resonance is fixed at half the bare matter frequency, so the changing pump carrier gives Dp=Delta/2. This optical detuning was absent from the earlier resonant backreaction calculation. The matter self-shift and optical depletion are now present together, although spatial modes and additional nonlinear effective-action terms remain omitted.

For target z=-iR, choose Delta=-CR²+sigma with sigma=1/2. Let

\[
F=R'+R/2+i\sigma R,\quad P=\sqrt F,\quad
E=P'+(K/2+iD_p)P+iJ(-iR)P^*.
\]

Then p=q=P and z=-iR solve all three equations. The external optical envelopes supply both the photon loss and coherent depletion. A quintic ramp R=10s³-15s⁴+6s⁵, with s=tau/10, avoids a divergent derivative of sqrt(F) at the initial boundary. In particular P'(0)=sqrt(30/10³) is finite. Optical input may switch to this finite value at the initial time; a smooth hardware turn-on has not been modeled.

The test applies an antisymmetric drive imbalance Ep=E(1+10⁻⁶), Eq=E(1-10⁻⁶), integrating tracking errors from the initially empty optical and excited matter modes. The underlying daughter condensate is still stipulated, not created by this trajectory.

## Optical results

Four cases combine eta=10⁻¹² or 10⁻⁹ with photon number-loss rates 3.00×10¹⁰ s⁻¹ or 10⁶ s⁻¹. The first loss is a centimeter transit-time comparison, not a derivation of a real cavity or a continuum boundary condition.

Three cases complete the ramp and hold. Their maximum normalized optical amplitude errors remain below 1.5×10⁻⁶. The eta=10⁻⁹, kappa=10⁶ s⁻¹ case reaches the optical tracking-error stop of 0.1 at tau=2.6215, before capture. The terminal matter population in that case is not a held-state prediction.

The antisymmetric optical linearization has growth exponents

\[
\lambda=-K/2\pm\sqrt{J^2R^2-D_p^2}.
\]

The exact maximum of the discriminant over 0≤R²≤1 is computed, and agrees with the failure mechanism. Only antisymmetric drive imbalance was tested in the nonlinear combined model. The earlier single-mode coupling-error tests are not silently upgraded into combined-model robustness tests.

The weighted occupation Qmode=|p|²+|q|²+2J|z|² satisfies

\[
Q_{\rm mode}'=2\operatorname{Re}(E_p p^*+E_q q^*)
-K(|p|^2+|q|^2)-2J|z|^2.
\]

The conservative conversion terms cancel, including the self-frequency shift. This is an occupation-balance identity; with chirping and nonlinear mode energy, it should not be mislabeled as the entire laboratory energy balance. The additional work and energy stored in the nonlinear interaction would also need accounting.

## Why the matter bath cannot simply remain passive

The earlier dressed decay calculation gives the on-shell cubic amplitude A for one gapped excitation converting into two opposite lower-branch excitations. Replacing the source by the coherent prepared amplitude gives a resonant pair coupling

\[
\mu=|\mathcal A|\sqrt{n_s},\qquad
\mathcal A=(\delta/\sqrt n)\widetilde{\mathcal A},\qquad
\mu_{\rm SI}=\frac{\delta|\widetilde{\mathcal A}|\sqrt\eta}{\hbar}.
\]

At the benchmark, |Atilde|=0.00734277. This is the already computed full cubic vertex, including the contact contribution and interference; it is not a new interaction. The leading weak-excitation calculation uses the unshifted on-shell momentum. A small nonlinear frequency shift moves that shell and requires a refined calculation at larger populations.

With phases chosen so mu is real, each resonant pair obeys

\[
\dot a_k=-\kappa_p a_k/2+\mu a_{-k}^\dagger,
\]

and the conjugate equation. Kappa_p is a **number**-loss rate for the matter excitations; the amplitude-loss rate is kappa_p/2. At exact resonance, amplitude growth occurs if mu>kappa_p/2. For an equal pair occupation n and a real anomalous pair moment m, vacuum input gives

\[
\dot n=2\mu m-\kappa_p n,\qquad
\dot m=\mu(2n+1)-\kappa_p m.
\]

The +1 is the quantum seed. Setting both classical daughter amplitudes to zero and leaving out that seed would miss the instability. Without loss, n=sinh²(mu t). Below threshold, with kappa_p>2mu, the undepleted-source stationary occupation is 2mu²/(kappa_p²-4mu²). Six loss/gain ratios are checked by comparing direct ODE integration with the affine matrix-exponential solution and the lossless formula.

These are initial-growth equations. They do not follow source depletion, nonlinear saturation, detuning generated by the new excitations or the resulting thermal distribution. A growing solution cannot be extrapolated to infinite occupation as a physical prediction.

## Physical size comparison

The calculated on-shell matter group velocity is approximately 5.02×10⁵ m/s. If, only as an escape-loss estimate, kappa_p=v_group/L, suppressing resonant gain requires

\[
L<\frac{v_{\rm group}}{2\mu_{\rm SI}}.
\]

| Excited fraction eta | Matter-pair amplitude gain, s⁻¹ | Maximum L under this escape estimate |
|---:|---:|---:|
| 10⁻¹² | 5.58×10⁷ | 4.50 mm |
| 10⁻⁹ | 1.76×10⁹ | 142 micrometers |
| 10⁻⁶ | 5.58×10¹⁰ | 4.50 micrometers |

At the centimeter comparison scale, all three targets exceed this resonant gain threshold. Thus the successful optical-only trajectories do not yet demonstrate sustainable capture once resonant matter modes are available. A large self-gravitating cloud cannot inherit a small-sample escape rate without justification.

This is not a geometry-independent exclusion: a finite spectrum may detune modes, additional damping may suppress growth, and boundaries may change escape or reflect excitations. None of those effects has been derived for an actual sample here. The calculation states the required loss/detuning condition and exposes an omitted channel. It does not claim that small L supplies confinement of the dense condensate or that a physical trap already exists.

## Evidence and changed research direction

The audited package contains four combined capture runs, an analytic optical-instability scan over three target populations, six quantum-pair moment checks, and the physical gain conversion. Direct and tracking-coordinate optical right-hand sides and the weighted occupation identity are cross-checked at a nonzero perturbation. No new Lean certification is claimed for these dynamics.

The most useful next calculation is now matter-pair backreaction and a justified escape/detuning mechanism, rather than further optimization of the optical ramp alone. The stable-mode assumption needs a physical outlet for the energy deposited into matter. A consistent finite sample must admit both the condensate and that outlet while satisfying the earlier density, energy and gravity constraints. Those requirements remain open; the goal is not complete.
