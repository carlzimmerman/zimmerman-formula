# Finite-temperature kicks and the reservoir–wall compatibility condition

2026-10-13. Conditional extension of the ideal neutral messenger Fermi reservoir. This calculation identifies a storage constraint; it supplies no observed particles, manufacturing protocol, or propulsion mechanism.

## A bath inside the cavity changes the barrier

The existing messenger contact interaction gives the carrier a mean potential

    U(n) = h n (hbar c)^3 / (4 m M_S).

Here densities n are in m^-3 and masses in eV, with h=1, m=1 MeV and M_S=10 MeV. In the same leading contact/mean-field approximation, the barrier experienced by a carrier in an interior bath is the potential difference:

    E_b = U(n_wall) - U(n_bath).

Consequently filling the old cavity with n_bath=1e25 m^-3 while keeping the old wall at n_wall=1e25 m^-3 removes its messenger barrier. The bath cannot simply be added to the old vacuum-interior design. Retaining the old relative barrier E_b=1.92087639236e-9 eV requires n_wall=2e25 m^-3. This is an assumed redesign, not a demonstrated material. It also shifts pair energies and requires revisiting the production resonance; no fixed old source rate is combined with this calculation.

The following rates use that stipulated *relative* barrier, a resting dilute impurity, and a spatially uniform interior bath. A kick exceeding E_b is energetically eligible for escape, not proof of an actual boundary crossing.

## Finite-temperature response derived from occupations

Use natural units hbar=c=k_B=1 until conversion to seconds. The neutral messenger-plus-electron atom has M_A=10510986.005756367 eV. Treat it as a noninteracting, unpaired, two-spin Fermi gas of total density 1e25 m^-3. The contact coupling is g=h/(4mM_S). No phase-stability or atom-production claim is made.

For bath energy gain omega, define

    S(q,omega) = 2 integral d^3k/(2pi)^3 f(e_k)[1-f(e_{k+q})]
                 delta(omega-e_{k+q}+e_k),
    e_k = k^2/(2M_A).

Angular integration fixes k_z=M_A omega/q-q/2. Integrating the remaining transverse kinetic energy gives

    E_min = (M_A omega/q-q/2)^2/(2M_A),
    S = M_A^2 T/(2pi^2 q)
        [log(1+exp((mu-E_min)/T))
         -log(1+exp((mu-E_min-omega)/T))] / [1-exp(-omega/T)].

This obeys detailed balance S(q,-omega)=exp(-omega/T)S(q,omega). The code checks the closed form against direct radial occupation integrals for four positive/negative transfer cases. Chemical potential mu is solved at each temperature to preserve density; it is not held at the zero-temperature Fermi energy. E_F=8.2283638367e-4 eV.

A resting impurity absorbs E=q^2/(2m) from the bath. Golden-rule heating and above-barrier kick rates are

    P_up = g^2/pi integral_0^infinity q^2 dq E S(q,-E),
    Gamma_> = g^2/pi integral_sqrt(2mE_b)^infinity q^2 dq S(q,-E).

At small momentum transfer well inside the degenerate bath's available phase space,

    P_up = g^2 M_A^2 m zeta(3) T^3 / pi^3,
    Gamma_> = g^2 M_A^2 m T^2/(2pi^3)
              integral_(E_b/T)^infinity y/(exp(y)-1) dy.

The code uses the full finite-temperature structure factor, not these asymptotes. The logarithm difference is between zero and y, providing an upper bound by the asymptotic integrands. Truncation at y=100 omits exponentially suppressed tails bounded by integrals of y exp(-y)/(1-exp(-100)) or y^2 exp(-y)/(1-exp(-100)); cutoffs 80 and 100 are compared. Inverse rates below are frozen-state waiting scales. After any sub-barrier collision the carrier is no longer at rest, so these are NOT full evaporation lifetimes.

| Bath temperature | Heating of resting carrier (eV/s) | Single-kick rate above barrier (1/s) | Inverse rate |
|---|---:|---:|---:|
| 11.60 microkelvin | 4.0670e-21 | 7.7219e-13 | 41,037 years |
| 1.160 millikelvin | 4.0670e-15 | 2.7504e-8 | 1.152 years |
| 0.1160 kelvin | 4.0670e-9 | 2.7824e-4 | 59.90 minutes |
| 1.160 kelvin | 2.6039e-6 | 2.4095e-2 | 41.50 seconds |

The warmest case has only 64.0% of the small-q heating asymptote and 86.6% of its kick rate, so finite phase-space restrictions matter. The earlier zero-temperature bath cannot heat a resting carrier: Fermi motion itself is not a temperature floor. Thermal holes permit the upward transitions calculated here.

## Consequence for creation and evidence limits

In-cavity creation remains conditional on hypothetical particles and couplings. A proposed cooling reservoir changes both the confinement landscape and the production threshold, and a finite-temperature reservoir can return energy to carriers. The next discriminating calculation is a self-consistent source threshold and transport model using the same interior density and wall potential, with a moving carrier distribution. Adding a zero-temperature cooling drift to the resting-particle heating result would not supply that model.

Twenty bounded numerical checks pass: four independent occupation integrals, four density constraints, eight integration-cutoff comparisons, and four phase-space bounds. The validated run manifest records code hashes, environment and outputs. These checks support the stated numerical calculation only. No Lean certification of the thermal response, experimental confirmation, actual lifetime, full atom material, or enhanced gravity is claimed.

Reproduce with the computation-audit runner arguments recorded in run/manifest.json, or directly with:

    python3 sol61_push/finite_temperature_kicks_2026_10_13/check.py /tmp/finite_temperature_kicks_results.json

Related repository evidence: ../neutral_reservoir_statistics_2026_10_13/REPORT.md, ../in_cavity_creation_2026_10_13/REPORT.md, and ../resonance_storage_shift_2026_10_13/REPORT.md. The response formula here is derived from the displayed occupation integral, rather than imported as an experimentally established description of hypothetical atoms.
