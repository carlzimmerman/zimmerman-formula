# Neutralizing the messenger changes the cooling statistics

2026-10-13. A positive scalar messenger S bound to one electron would be a neutral spin-half atom. An ideal gas of these atoms at the proposed density is quantum degenerate at low temperature. Including Pauli blocking gives a very slow energy-loss law for a sufficiently slow carrier, rather than the stationary-independent-target cooling estimate. This tests one hypothetical reservoir state; it does not demonstrate that such atoms exist or that this is their stable many-body phase.

## A specified neutralization option

Take M_S=10 MeV and an ordinary electron bound by the Coulomb interaction. At leading hydrogenic order the reduced electron mass gives binding energy 12.944 eV and radius 5.562e-11 m. The atom mass is M_A approximately 10.511 MeV. With a spin-zero nucleus and one electron the atom is fermionic. Assume two equally populated spin states in an unpaired, noninteracting gas at T=0, with total atom density n_A=1e25 m^-3.

Then

\[
k_F=(3\pi^2 n_A)^{1/3},\qquad E_F=k_F^2/(2M_A),
\]

with natural-unit density conversion. Numerically k_F=131.52 eV, E_F=8.228e-4 eV and T_F=9.55 K. These are model scales, not evidence of an achievable reservoir. Molecular formation, interactions, phase transitions, electron-mediated responses and the messenger's viability require their own treatment.

At momentum transfers much smaller than the inverse atom radius, the existing h|Phi|²|S|² interaction couples the carrier to atom number density with leading nonrelativistic strength

\[
g=\frac{h}{4mM_S}.
\]

The scattering target's kinetic mass is M_A, while the coupling normalization retains M_S because it originates from the constituent messenger density. The low-momentum atomic form factor is taken as one. This approximation is screened numerically below, not established for all collisions.

## Pauli-allowed density response

Define the number-density structure factor, with no hidden 2 pi multiplying the energy delta function,

\[
S(q,\omega)=2\int\frac{d^3k}{(2\pi)^3}
\theta(k_F-k)\theta(|\mathbf k+\mathbf q|-k_F)
\delta\left(\omega-\frac{q^2+2\mathbf k\cdot\mathbf q}{2M_A}\right).
\]

The factor two counts spin states. Align q along z. The delta function fixes k_z=M_A omega/q-q/2, leaving an annulus of allowed transverse momenta. In the interior particle-hole region this evaluates to

\[
S(q,\omega)=\frac{M_A^2\omega}{2\pi^2q},\qquad \omega>0.
\]

The code also evaluates the clipped annulus geometry, rather than extending this formula outside the Fermi sphere. At T=0, transitions that require the bath to release energy are absent in this ideal ground state. Fermi motion is therefore not equivalent to a classical bath temperature that would inevitably heat a resting carrier.

Pauli suppression of collisions is experimentally established for ordinary atomic Fermi gases, for example [DeMarco, Papp and Jin, cond-mat/0101445v2](https://arxiv.org/abs/cond-mat/0101445). That result supplies context only; its measured rates and suppression factors are not used here. The response and coefficient below are derived for this specified ideal model.

## Slow-carrier energy drift

For a dilute carrier with velocity v, the energy available to the bath for momentum transfer q is omega=v q cos(theta)-q²/(2m). Golden-rule energy loss is

\[
P\equiv-\dot K=2\pi g^2\int\frac{d^3q}{(2\pi)^3}
\omega S(q,\omega)\,\theta(\omega).
\]

For slow enough carriers that the whole allowed transfer region lies in the interior particle-hole region, 0<q<2mv and q/(2mv)<cos(theta)<1. Integrating gives

\[
\boxed{P=\frac{g^2M_A^2m^4v^6}{105\pi^3}
=\frac{h^2(M_A/M_S)^2K^3}{210\pi^3m}.}
\]

The last expression uses K=m v²/2. Natural-unit P has dimension energy squared; dividing by hbar converts it to eV/s. The leading coefficient does not depend on density while the allowed transfers remain within the stated region. Increasing density cannot be assumed to improve this low-velocity rate indefinitely.

The derivation uses a single weakly coupled impurity, an infinite prescribed ideal bath, and leading Born scattering. It is not a dense-condensate cooling law or a solution for a changing bath.

## Numerical scales

For m=1 MeV, h=1 and the reservoir above:

| Carrier kinetic energy | Energy drift (eV/s) | Instantaneous K / absolute drift |
|---:|---:|---:|
| 1e-9 eV | -2.578e-22 | 123,000 years |
| 1e-7 eV | -2.578e-16 | 12.29 years |
| 1e-5 eV | -2.578e-10 | 0.001229 years |

These are conditional drift scales, not mean first-passage times or a proven cooling curve for an ensemble. At 1e-9 eV, v/v_F=0.00357, q_max/k_F=0.000680 and q_max a0/(hbar c)=2.52e-5. The carrier is slow and cannot resolve the internal atom in that example. At the highest listed energy v/v_F=0.357, so it is less deeply in the low-velocity regime; applicability depends on the actual particle-hole support, not just a label of 'cold'.

Finite temperature, interatomic interactions, pairing and collective modes can change the response. They must be calculated before choosing this medium as a controller or coolant. This result does not establish that every neutralization mechanism fails.

## Verification and research consequence

Sixteen checks pass: the analytic phase-space polynomial integral, six direct two-dimensional quadratures against the drift coefficient with six resolution checks, and three annulus-geometry checks. The run manifest pins code and results. No new Lean certification or empirical evidence for the proposed material is claimed.

The earlier stationary-target calculation remains a valid classical kinematic example, but cannot be used as the cooling rate for this proposed neutral fermionic reservoir. A controller made from this medium needs a consistent finite-temperature/many-body treatment. This closes an important assumption gap before treating a prescribed cold density profile as a physical manufacturing component; it does not complete the creation mechanism.
