# Magnetic source shift and the subthreshold loading window

2026-10-13. This extends ../muon_portal_magnetic_storage_2026_10_13/REPORT.md
by matching the source's quadratic photon operator in the same soft muon loop.
It is a leading derivative and weak-field calculation, not the full in-field
production spectrum or a claimed observation of a new particle.

## Verified source and convention

Kniehl and Spira, *Low-Energy Theorems in Higgs Physics*,
[hep-ph/9505225v1](https://arxiv.org/pdf/hep-ph/9505225v1), submitted 3 May 1995,
Z. Phys. C69 (1995) 77–88, Eq. (22), gives the multi-scalar photon interaction.
Checked 2026-10-13. Retain its fermion contribution, set Nc=1 and charge squared=1,
omit the W contribution, and replace H/v by yR/m_mu. The muon mass is
m_mu(R)=m_mu+yR from L=-y R mubar mu. This yields

    L_loop = alpha/(6pi) log(1+yR/m_mu) F_mn F^mn.

The linear coefficient reproduces the magnitude already checked using the
on-shell triangle's heavy-muon limit. In L=-g R F^2/4 the signed coefficient is
now g=-2alpha*y/(3pi*m_mu). Attraction requires mu<0 for y>0; the previous report
chose the equivalent relative sign using positive g and mu. Decay widths are
unchanged by these sign choices. This is a known low-energy matching result,
not a new empirical mechanism. Search scope: primary arXiv low-energy-theorem
papers; Eq. (22) was read directly. No global novelty claim or local PDF cache
is made.

## Static response of the source and carrier

Take a prescribed magnetic field, F^2=2B_nat^2, and a renormalized quadratic
vacuum source potential. The effective potential at zero carrier density is

    V(R;B) = MR^2 R^2/2 - alpha*B_nat^2/(3pi) log(1+yR/m_mu).

Define x=yR0/m_mu and eta=alpha*y^2*B_nat^2/(3pi*MR^2*m_mu^2).
The stationary solution continuously connected to vacuum satisfies

    x(1+x)=eta,
    x=2eta/(1+sqrt(1+4eta)) >= 0.

The static curvature is

    M_curv^2 = MR^2 + alpha*y^2*B_nat^2/[3pi*m_mu^2*(1+x)^2].

Consequently, to leading B^2 order,

    delta_M_curv = alpha*y^2*B_nat^2/(6pi*m_mu^2*MR) > 0,
    R0 = alpha*y*B_nat^2/(3pi*m_mu*MR^2),
    U_phi = mu*R0/(2m) < 0.

A source with positive vacuum excess does not acquire negative excess from this
leading contribution. Its local excess above the shifted daughter threshold
increases by delta_M_curv-2U_phi. This closes the suggested automatic field-driven
crossing in this approximation; it is not a universal impossibility theorem.

For the previous y=2e-4, MR=2 MeV, m=1 MeV, |mu|=27.72246466 eV benchmark:

| Magnetic field | Source curvature mass shift | Daughter energy shift |
|---|---:|---:|
| 1 T | +2.64683e-29 eV | -1.93821e-28 eV |
| 10 T | +2.64683e-27 eV | -1.93821e-26 eV |
| 100 T | +2.64683e-25 eV | -1.93821e-24 eV |

The ratio of source shift to attractive depth is 0.1365602. The dimensionless
muon weak-field parameter eB/m_mu^2 is at most 5.30e-13 in this table.

## What a separately chosen subthreshold source would require

Let V=|U_phi|. Substituting the leading source shift into the necessary local
window -2V<delta_eff<0 gives a condition on the vacuum excess:

    -2V-delta_M_curv < delta_vac < -delta_M_curv.

At 10 T this is approximately

    -4.14111e-26 eV < delta_vac < -2.64683e-27 eV.

This is radically different from the previous assigned +2e-9 eV. The inequality
is necessary within the approximation; it neither guarantees discrete pair
levels nor their production. The prior ideal-well calculation already requires
a radius above 1.574 km at this depth before even a single bound state appears.
No Maxwell-compatible geometry, cooling process or stable reservoir is provided.

The photon width at the inherited coupling is Gamma_gamma=3.41884e-13 eV,
approximately 8.82e12 times the entire 2V energy window. To quantify only this
scale mismatch, take a normalized Lorentzian of constant full width Gamma_gamma
and place its center at the midpoint of [-2V,0]. Its weight in that interval is

    f_window = (2/pi) atan(2V/Gamma_gamma) = 7.21826e-14 at 10 T.

Analytic integration and independent high-precision quadrature agree. This is
NOT a branching fraction, a bound on achievable production, or evidence that
linewidth forbids monochromatic driving. Driven scattering fixes the incoming
energy; the actual rate depends on the pair spectral density, mode overlap,
energy-dependent self-energy and loss channels. Bound-pair spectra cannot be
replaced by this Lorentzian diagnostic. The old vacuum carrier decay width is
closed for a subthreshold source and must not be imported into its rate.

## Scope of the result and remaining mechanism work

Static curvature is the leading derivative approximation to the time-like pole.
MR^2/m_mu^2=3.58304e-4 is an expansion parameter, not a proved error bound. The
finite-frequency two-scalar/two-photon amplitude and wavefunction correction
have not been calculated here. The non-polynomial stationary solution resums
powers of yR/m_mu only within the leading F^2 action; it is not an all-field QED
solution. Independent higher operators or a vacuum cubic source interaction
would add terms and require their own matching. The renormalized quadratic
source potential is an explicit assumption, not enforced by a symmetry.

A full loading mechanism still needs a realizable potential supporting states,
a source coupled to their actual pair spectral density, and a calculable way
to keep the produced population. This calculation supplies a previously missing
quadratic photon coefficient and rules out automatic downward threshold crossing
from that contribution. It does not yet supply a manufacturing protocol.

Eighteen checks pass: two symbolic derivatives, five checks at each of three
fields, and reproduction of the preceding attractive energy shift. The run
manifest hashes both earlier numerical inputs. Numerical differences as small
as 1e-29 eV against MeV masses use 90-decimal arithmetic and rationalized square
root differences. No new Lean certification is claimed for the loop calculation;
the previous Lean energy-window algebra applies with delta replaced by delta_eff.

Reproduce:

    python3 sol61_push/muon_field_source_shift_2026_10_13/check.py /tmp/muon_field_shift_results.json
