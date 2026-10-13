# Glow as a reaction output: a conditional spectrum and rate

2026-10-13. **The joint glow-plus-gravity mechanism is still open.** This work derives a testable optical consequence of one explicitly added interaction, rather than assigning a glow to the existing dark action. It also evolves the two homogeneous carrier fields without eliminating the source. The photon calculation and coherent-field simulations are separate approximations, not a self-consistent radiating, gravitating apparatus.

## Candidate reaction and assumptions

The existing carrier action in `INPUT_CARRIER_ACTION.tex` has no electromagnetic coupling. Retain the previously proposed hypothetical extension

\[
\Delta\mathcal L=-\frac{\zeta}{4\Lambda^3}
(\chi^*\phi^2+\chi\phi^{*2})F_{\mu\nu}F^{\mu\nu}.
\]

It permits \(\chi\to\phi\phi\gamma\gamma\), preserving the stated global charge. Here \(\zeta\) is dimensionless, \(\Lambda\) is an energy scale, \(M=2m+\delta\), and \(0<\delta\ll m\). Natural units are used. This calculation assumes vacuum final states, a resting source, tree level, perturbatively weak interactions, and final-state rescattering small enough to neglect. It excludes stimulated emission, plasma/material reprocessing, bound-state lines and other portal operators. The effective expansion and positive Maxwell kinetic coefficient must hold. No measured value or experimentally admissible range for this portal has been established.

Three routes are distinguished: direct radiative conversion (calculated below); coherent conversion with source depletion (numerically evolved below); and transfer to ordinary luminous material (deferred because no material coupling has been specified). These are alternative optical mechanisms; none supplies the missing gravitational enhancement.

## Amplitude and phase space

For photon momenta \(k_1,k_2\) and polarizations \(\epsilon_1,\epsilon_2\), the contact amplitude, up to an irrelevant overall phase, is

\[
\mathcal M=\frac{2\zeta}{\Lambda^3}
[(k_1\!\cdot k_2)(\epsilon_1\!\cdot\epsilon_2)
 -(k_1\!\cdot\epsilon_2)(k_2\!\cdot\epsilon_1)],
\quad
\sum_{\rm pol}|\mathcal M|^2
=\frac{8\zeta^2}{\Lambda^6}E_1^2E_2^2(1-\mu)^2,
\]

where \(\mu\) is the angle cosine between the photons. The factor two in the amplitude comes from the identical scalar daughters. Both daughter and photon symmetry factors must also appear in the rate:

\[
d\Gamma_\gamma=\frac{1}{2M\,2!\,2!}|\mathcal M|^2
(2\pi)^4\delta^4(P-\textstyle\sum p_i)
\prod_i\frac{d^3p_i}{(2\pi)^3 2E_i}.
\]

This normalization follows the [PDG kinematics review, §§49.4–49.4.2](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-kinematics.pdf). That reference supplies phase-space conventions, not evidence for the proposed portal.

Integrating the two daughter momenta gives \(\beta_d/(8\pi)\), where
\(\beta_d=\sqrt{1-4m^2/s_d}\) and
\(s_d=(M-E_1-E_2)^2-|\mathbf k_1+\mathbf k_2|^2\).
At leading order in \(\delta/m\), this is
\(\sqrt{\delta-E_1-E_2}/(8\pi\sqrt m)\).
The photon angular integral is
\(\int d\Omega_1d\Omega_2(1-\mu)^2=64\pi^2/3\).
Consequently,

\[
\boxed{\frac{d^2\Gamma_\gamma}{dE_1dE_2}
=\frac{\zeta^2}{96\pi^5M\sqrt m\,\Lambda^6}
 E_1^3E_2^3\sqrt{\delta-E_1-E_2}}
\]

on \(E_1,E_2\ge0\), \(E_1+E_2\le\delta\), to leading near-threshold order. Photon field strengths suppress the soft-photon region; a flat photon-energy distribution would be incorrect for this operator.

## The spectrum and energy split

The energy fractions \((E_1/\delta,E_2/\delta,K/\delta)\) have the leading Dirichlet distribution with parameters \((4,4,3/2)\). For one photon, \(x=E_\gamma/\delta\) has density

\[
p(x)=\frac{x^3(1-x)^{9/2}}{\mathrm B(4,11/2)},\quad0<x<1.
\]

Thus

\[
E_{\rm mode}=\frac25\delta,\qquad
\langle E_\gamma\rangle=\frac8{19}\delta,\qquad
\langle E_{\gamma\gamma}\rangle=\frac{16}{19}\delta,\qquad
\langle K_{\phi\phi}\rangle=\frac3{19}\delta.
\]

The last relation means this radiative branch leaves colder daughters than the nonradiative branch at the same gap. It does not mean conversion of 16/19 of the source's rest energy: only the small released gap is partitioned this way. To leading order, each daughter's RMS speed is \(v_{\rm rms}/c=\sqrt{3\delta/(19m)}\).

Using 400–700 nm solely as the stated visible band:

| Gap | Photon spectrum mode | Fraction of photons in band | Fraction of radiated energy in band |
|---|---:|---:|---:|
| 3 eV | 1.2 eV | 14.52% | 23.03% |
| 5 eV | 2.0 eV | 54.05% | 60.69% |
| 8 eV | 3.2 eV | 33.57% | 24.89% |
| 399.960008 eV | 159.984 eV | 0.0000297% | 0.000000460% |

The 5 eV choice produces a broad optical component in this hypothetical channel; it is not a prediction that the actual carrier has this gap. For \(m=1\) MeV, the associated daughter RMS speed is \(8.885\times10^{-4}c\). Apparent brightness and visual comfort still require luminosity, geometry, spectrum and exposure; the word “glow” does not establish any of them.

## Rate: the important bottleneck

Let \(\mathcal B_3=\Gamma(4)^2\Gamma(3/2)/\Gamma(19/2)
\simeq2.67445\times10^{-4}\). Integrating the spectrum gives

\[
\Gamma_\gamma=\frac{\zeta^2\mathcal B_3}{96\pi^5M\sqrt m\Lambda^6}\delta^{17/2}.
\]

Relative to the original vacuum tree width
\(\Gamma_0=g^2\sqrt{1-4m^2/M^2}/(8\pi M)\), the leading ratio for nonzero \(g\) is

\[
\boxed{\frac{\Gamma_\gamma}{\Gamma_0}
\simeq2.28799\times10^{-7}
\left(\frac{\zeta\delta^4}{g\Lambda^3}\right)^2.}
\]

At fixed couplings and heavy mass, reducing the gap from 400 eV to 5 eV suppresses this ratio by \((5/400)^8\simeq5.96\times10^{-16}\). The visible spectrum therefore does not by itself produce appreciable light. A tiny \(g\), different operator, large source population or externally sustained process can change the comparison, but requires new quantitative inputs and validity checks. This is not a universal no-go for light emission.

For a dilute, incoherent source population \(N_\chi\), ignoring competing processes and trapping effects, the conditional luminosity is

\[
P_\gamma=N_\chi\Gamma_\gamma\frac{16\delta}{19},\qquad
P_{\rm vis}=P_\gamma f_{E,\rm vis}.
\]

With \(\Gamma\) converted to inverse seconds and \(\delta\) to joules, this gives watts. Coherent simulations below do not justify substituting their source population into this dilute decay law without a further quantum kinetic derivation.

## Full homogeneous carrier evolution

The simulations retain both fields:

\[
i\dot\psi=2c_3b\psi^*+2k|\psi|^2\psi,\qquad
i\dot b=\delta b+c_3\psi^2.
\]

They omit spatial transport, gravity, photons and external pumping. With \(n=|\psi|^2\), \(n_b=|b|^2\), \(S=2\Re(b^*\psi^2)\), the invariants are

\[
Q=n+2n_b,\qquad D=\delta n_b+c_3S+kn^2.
\]

In particular, for \(c_3\ne0\),

\[
S=\frac{D-\delta(Q-n)/2-kn^2}{c_3}.
\]

This neutral bilinear cannot be assigned an independent arbitrary time history while claiming the same closed carrier dynamics. In the common rest-phase convention \(\phi=\psi e^{-imt}/\sqrt{2m}\), \(\chi=b e^{-2imt}/\sqrt{2M}\), the fast rest phases cancel in \(\chi^*\phi^2\). The hypothetical Maxwell coefficient is
\(I=1+\zeta S/(2m\sqrt{2M}\Lambda^3)\).
A time-varying coefficient is not by itself a classical light source: the homogeneous Maxwell equation still has the zero-field solution. Vacuum photon production needs quantization and backreaction accounting. The quantum decay calculation above is a separate controlled limit.

For an initially undepleted homogeneous pump \(b=B e^{-i\delta t}\), a small zero-momentum daughter seed has linear growth exponent
\(\gamma^2=4c_3^2|B|^2-\delta^2/4\).
For a momentum pair, replace \(-\delta/2\) by \(E_p-\delta/2\); a homogeneous calculation does not test every resonant momentum mode.

Nine trajectories use \(\delta=1\), \(b(0)=1\), \(\psi(0)=0,0.001,0.01\), and \((c_3,k)=(0.2,0.1),(0.3,0.2),(0.5,0.35)\), all with \(k>c_3^2/\delta\). They run to dimensionless time 100. At \(c_3=0.3,k=0.2,\psi(0)=0.001\), about **96.35%** of the charge temporarily occupies daughters and then returns toward the source. Conservation checks pass. An exactly zero classical seed remains zero in all three cases; this does not negate spontaneous quantum decay. These results exhibit reversible coherent conversion and depletion, not sustained radiation or gravitational amplification.

## Verification and limits

`check.py` passes 43 recorded checks: charge/energy/bilinear identities on nine trajectories, zero-seed controls, phase-space quadrature/refinement, and five explicit transverse-polarization sums. The scalar phase-space factor was also evaluated with exact relativistic daughter invariant mass, using 64- and 128-point quadrature in each of three variables. At \(\delta/m=4\times10^{-4}\), its rate integral is 0.999723 times the leading expression; at 0.01 it is 0.993135. These are finite tolerance-dependent comparisons, not a universal error bound.

`ConversionConservation.lean` proves three conditional algebraic identities: charge derivative cancellation, energy derivative cancellation and the neutral-bilinear expression. Two damaged coefficient controls are rejected. The photon amplitude, integration, physical assumptions and numerical convergence are **not Lean-certified**. Both evidence manifests validate. This is self-reviewed work without an independent agent review.

Reproduce numerics from the repository root with `python3 sol61_push/radiative_conversion_2026_10_13/check.py /tmp/radiative-results.json`. The contracts and `run/manifest.json`, `lean_run/manifest.json` record pinned execution inputs, actual commands, environments, bounds, raw logs and result hashes.

## What remains to connect light and motion

This supplies a concrete *conditional* glow spectrum and a rate bottleneck. It does not establish the portal's existence or connect glow intensity to a new gravitational force. The radiated energy leaves the source; retained daughters carry most of its original rest mass. Their spatial redistribution could alter ordinary gravity, but the homogeneous calculation contains no such redistribution.

The next joint obligation is a spatial, energy-conserving carrier–photon calculation with a specified coupling, source preparation, escape geometry and measured force observable. A proposed metric enhancement requires its own action and stability analysis. The earlier passive-condensate gravity bound remains applicable in its stated regime; the present reaction calculation does not evade it. A different optical interaction or ordinary material reprocessing remains an open alternative, requiring an explicit interaction before another spectrum can be predicted.
