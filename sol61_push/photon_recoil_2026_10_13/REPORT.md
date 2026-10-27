# Photon scattering and recoil: a constraint on a cooling route

2026-10-13. The existing contact photon interaction permits elastic scattering, but a resting carrier gains recoil energy in each event. Soft-photon scattering is strongly suppressed. This package supplies a scattering kernel needed for a future cooling calculation; it does not establish cooling of a moving distribution, a heat bath, or a prepared carrier.

## Crossed contact amplitude

Retain L_int=-C |phi|² F_mu_nu F^mu_nu, as in the previous manufacture and annihilation calculations. For gamma + phi -> gamma + phi, the incoming photon is averaged over two polarizations and the outgoing photon is summed. The result is

\[
\overline{|\mathcal M|^2}=4C^2t^2,\qquad
\frac{d\sigma}{dt}=\frac{C^2t^2}{4\pi(s-m^2)^2}.
\]

The kinematic range is -(s-m²)²/s <= t <= 0. Integration yields

\[
\boxed{\sigma_{\rm el}=\frac{C^2(s-m^2)^4}{12\pi s^3}.}
\]

For an initially stationary carrier and incoming photon energy omega, s=m²+2m omega. Thus

\[
\sigma_{\rm el}=\frac{4C^2\omega^4}{3\pi m^2(1+2\omega/m)^3}
\longrightarrow\frac{4C^2\omega^4}{3\pi m^2}\quad(\omega\ll m).
\]

This is the tree contact contribution, not a full matched amplitude or an empirical cross section. Additional operators and loops remain unspecified. The scattering normalization is the same [PDG Kinematics, 2024, Eq. 49.33](https://pdg.lbl.gov/2024/reviews/rpp2024-rev-kinematics.pdf) checked in the previous packages. Here the incoming center-of-mass momentum is (s-m²)/(2 sqrt(s)); no identical-final-state factor applies.

## Exact recoil for the stationary target

Let theta be the laboratory photon scattering angle. The outgoing photon energy is

\[
\omega'=\frac{m\omega}{m+\omega(1-\cos\theta)}.
\]

The target's kinetic-energy increase is T=-t/(2m)=omega-omega', always nonnegative. Weighting by the contact differential cross section gives

\[
\boxed{\langle T\rangle=\frac{3(s-m^2)^2}{8ms}
=\frac{3\omega^2}{2(m+2\omega)}.}
\]

A stationary target therefore heats through recoil. A moving target can transfer kinetic energy to scattered photons; its net cooling depends on the photon distribution, Doppler shifts and recoil diffusion. That momentum-dependent collision integral has not been evaluated here. The stationary-target result alone neither demonstrates nor rules out such cooling.

## Competition with annihilation while the signs overlap

For a cold, uncorrelated mixture, the earlier contact annihilation rate per carrier is n_opposite a, where a=2 C²m²/pi in natural units. Photon scattering has rate n_gamma sigma_el. Their ratio is

\[
\frac{\Gamma_{\rm el}}{\Gamma_{\rm ann}}
=\frac{n_\gamma}{n_{\rm opposite}}
\frac{2}{3}\left(\frac{\omega}{m}\right)^4
(1+2\omega/m)^{-3}.
\]

The same C cancels. This is an event-count comparison, not a cooling-rate comparison: even one elastic event per annihilation lifetime is insufficient to assert cooling.

At m=1 MeV:

| Photon energy | Mean recoil on resting carrier | n_gamma/n_opposite for equal event rates |
|---:|---:|---:|
| 1 eV | 1.50 micro-eV | 1.50e24 |
| 1 keV | 1.497 eV | 1.509e12 |
| 100 keV | 12.5 keV | 2.592e4 |

These ratios apply to an overlapping mixture with this single contact coupling and spontaneous scattering into unoccupied photon states. After genuine charge separation, the local opposite-sign density is smaller, so the comparison changes. Coherent/stimulated fields, resonances and other interactions need separate treatment. No practical beam intensity or actual Wilson coefficient has been inferred from this table.

The calculation explains why simply adding low-energy light to the current model is not yet a cooling mechanism. A candidate must specify a photon spectrum and show that energy removal from moving carriers exceeds recoil heating and other losses. Any dense-condensate cooling proposal must also address collective excitations instead of silently applying this single-particle cross section.

## Verification

Eight checks pass: symbolic total cross section, mean recoil and soft-energy limit; explicit physical-polarization amplitude against the invariant result; and four independent laboratory-angle quadratures at omega/m=1e-6, 0.001, 0.1 and 1. The last point is a kinematic/contact normalization check, not a claim of EFT validity at every cutoff. The bounded manifest records the executed script and output. These checks are not empirical evidence or a Lean certification of quantum field theory.

The next useful calculation is a moving-particle cooling/heating kernel for a specified photon bath, using this cross section and the existing carrier mass and loss channels. Creation, confinement and preparation remain open.
