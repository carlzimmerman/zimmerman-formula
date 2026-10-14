# The proposed photon portal also supplies a coherent preparation route

2026-10-13. Conditional theory calculation; no experimental identification of the portal or condensate. The mathematical route uses external optical energy to prepare an excitation. It does not produce energy from an unexcited stationary state or supply a new gravitational interaction.

## Geometry matters

The preceding hypothetical interaction gives an effective linear coupling -g chi F²/4 for the source excitation, with g=zeta n/(2m Lambda³), followed by its Bogoliubov vertex factor Vg. In natural units F²=2(B²-E²). A single ideal traveling plane wave has F²=0 and cannot provide this classical drive through that term. This does not exclude focused fields, other geometries or quantum scattering.

For equal, parallel-polarized waves traveling in opposite directions,

\[
E_x=E_0[\cos(kz-\omega_p t)+\cos(kz+\omega_p t)],\quad
B_y=E_0[\cos(kz-\omega_p t)-\cos(kz+\omega_p t)],
\]
\[
F^2=-4E_0^2[\cos(2kz)+\cos(2\omega_p t)].
\]

There is a spatially uniform oscillatory term at twice the pump frequency, and a static spatial modulation. Opposite photon momenta can therefore drive the zero-momentum gapped excitation when 2 omega_p equals omega_g. The static modulation has not been solved here and cannot be dropped in a complete spatial model.

## Linear diagnostic

Let alpha be the coherent excitation amplitude per square-root volume, so n_s=|alpha|². Retain the previous matter width a and vacuum photon width b, and write Gamma=a+b. With detuning Delta=omega_g-2 omega_p, an undepleted prescribed pump and a rotating-wave approximation give

\[
\dot\alpha=-(\Gamma/2+i\Delta)\alpha-i\mathcal F,\qquad
\mathcal F=\frac{gV_g E_0^2}{2\sqrt{2M}}
=\frac{gV_g u_{\rm beam}}{\sqrt{2M}},
\]

where u_beam=E0²/2 is the time-averaged energy density of **each** traveling beam. At resonance,

\[
n_s=4|\mathcal F|^2/\Gamma^2,\qquad
I_{\rm beam}=c\,\frac{\Gamma\sqrt{n_s}\sqrt{2M}}{2|gV_g|}.
\]

The second equation uses natural-unit energy densities internally; the script converts Gamma from s⁻¹ to eV and energy density from eV⁴ to J/m³ before multiplying by c. The assumed pump-independent damping is a diagnostic assumption, not a validated strong-field approximation.

For the preceding benchmark (m=1 MeV, delta=5 eV, lambda_tot=10⁻⁶, epsilon=10⁻⁴, x=2/7, Lambda=10M and zeta=1), the two-photon resonance frequency is about 8.64 × 10¹⁴ Hz, with pump wavelength near 694 nm. In this linear diagnostic its intensity linewidth in two-photon detuning is 26.2 Hz and the amplitude relaxation time is 0.0121 s.

| Excitation density / daughter density | Intensity of each beam, W/m² | Vacuum spontaneous photon power, W/m³ |
|---:|---:|---:|
| 10⁻¹² | 9.07 × 10¹² | 5.22 × 10⁻⁴ |
| 10⁻⁹ | 2.87 × 10¹⁴ | 0.522 |
| 10⁻⁶ | 9.07 × 10¹⁵ | 522 |

These are diagnostic values for a prescribed dense medium, not practical performance predictions. Density is approximately 3.31 × 10⁸ kg/m³. No sample, confinement or optical propagation solution is provided. The spontaneous photon column excludes pump light and pump-induced scattering; it is not total emergent brightness or visibility.

## Energy accounting and the missing strong-field calculation

Writing alpha=r+i s and taking the drive real gives the exact oscillator identity

\[
\frac{d|\alpha|^2}{dt}=-\Gamma|\alpha|^2-2\mathcal F\,s.
\]

At resonance in the stationary state, optical power transferred to this excitation equals omega_g Gamma n_s. Of that modeled loss, omega_g a n_s enters matter excitations and omega_g b n_s enters the stipulated vacuum radiative channel. Thus this mechanism prepares excitations using supplied optical work; it is not evidence for spontaneous energy release from the ground state. Recovering matter excitation energy would require additional dynamical accounting.

A strong pump also enters the photon fluctuation equations. Expanding F=F_pump+f introduces a term proportional to chi F_pump f as well as the coherent source chi F_pump². Consequently stimulated conversion, photon-mode mixing, pump depletion, possible instabilities, and the static density modulation must be solved together before using the table as a prediction. Small field amplitude relative to the cutoff does not establish negligible resonant backreaction. The script's field/cutoff diagnostic is not a strong-field admission test.

This finds an explicit preparation term within the already hypothetical portal, rather than inserting an unrelated drive by hand. The unresolved implication is now whether the coupled Maxwell–matter dynamics admits a stable, confined, optically accessible operating state. No gravitational force enhancement follows from the drive calculation. The external drive and condensate stress-energy would still need a consistent gravitational calculation.

## Verification and provenance

Four detunings test the numerical complex-oscillator evolution against its analytic solution over eight damping units. Two exact symbolic Maxwell identities check the plane-wave geometry. The contract and run manifest pin the script and copied prior widths. These checks verify the stated reduced equations; they do not validate the approximations against a physical system.

DriveIdentities.lean certifies the counterpropagating-field polynomial identity and oscillator energy-balance identity. The accompanying compiler logs and hash record document the direct Lean check. Those two algebraic facts do not certify the portal, coherent-drive normalization, linewidth, kinetic damping or a device. An initial compiler invocation failed because the source file was written relative to the wrong working directory; it was corrected before the recorded successful compilation. No scientific output depends on that failed invocation.
