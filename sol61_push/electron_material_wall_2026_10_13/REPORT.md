# Electron-density wall and its production cost

2026-10-13. A new conditional storage interaction, added to the muon-source
alternative. No new charged messenger S is reintroduced. The electron Yukawa
is an independently assigned parameter, not derived from the original carrier
symmetry or observed in the data.

## One interaction must be used in both the wall and source calculations

Take L_int=-mu R|phi|^2-ye R ebar e-ymu R mubar mu with mu=27.72246466 eV,
ymu=2e-4, m=1 MeV and MR approximately 2 MeV. For a nonrelativistic,
homogenized electron medium let ns=<ebar e> approximately equal the electron
number density in natural units. The static source equation gives

    R0=-ye ns/MR^2,
    U_wall=-mu*ye*ns/(2m*MR^2).

Repulsion requires mu*ye<0. The examples use ye<0. Charge-neutral matter still
contains scalar electron density; electric neutrality does not cancel this
scalar coupling. No nuclear coupling is assumed here. In actual atoms the scalar
density differs from electron number density through relativistic and binding
effects. Screening, interfaces, phonons and other material responses remain
uncomputed. ns=ne*(hbar*c)^3 is an explicit conversion, with ne=1e30/m^3 used as
a diagnostic density, not an experimentally qualified material specification.

The same result follows from a Born scattering length

    a_e=-mu*ye*m_reduced/(4pi*m*MR^2),
    U_wall=2pi*ns*a_e/m_reduced.

This checks the mean-potential normalization. It does not compute inelastic
loss, thermalization or reflection from a microscopic surface.

Because MR>2me, this interaction opens

    Gamma_ee=ye^2*MR/(8pi)*(1-4me^2/MR^2)^(3/2).

Eliminating ye gives a direct wall/decay relation:

    Gamma_ee = MR/(8pi)*(1-4me^2/MR^2)^(3/2)
               *[2m*MR^2*U_wall/(mu*ns)]^2.

At fixed masses, density and mu, a stronger wall necessarily increases this
competing decay quadratically. The wall cannot be varied while retaining the
previous muon-only source width.

## Photon amplitudes must also change coherently

The added electron loop is complex above its pair threshold. Therefore

    Gamma_gamma=alpha^2*MR^3/(256pi^3)
       *|ymu/m_mu*A_1/2(MR^2/(4m_mu^2))
          +ye/me*A_1/2(MR^2/(4me^2))|^2.

The form factor and conventions are those verified in
../ordinary_lepton_source_2026_10_13/REPORT.md. In particular, electron and muon
WIDTHS must not simply be added: their amplitudes interfere. The carrier width
for distinct phi and anti-phi is

    Gamma_phi=mu^2/(16pi*MR)*sqrt(1-4m^2/MR^2).

The source equations use [Rella, Döbrich and Yu, Phys. Rev. D 106, 035023 (2022)](https://scoap3-prod-backend.s3.cern.ch/media/files/72198/10.1103/PhysRevD.106.035023.pdf),
Eqs. (3), (6)–(9), already translated in the earlier source audit. This report
uses the formulas, not the paper's historical muon-anomaly preference. The
interaction assumptions and material application are additional model choices.

## Results at the original source excess

For delta=MR-2m=2e-9 eV the born kinetic energy is 1e-9 eV per carrier.

| ye | Wall height (eV) | Gamma_ee (eV) | Coherent Gamma_gamma (eV) | Delta a_e |
|---:|---:|---:|---:|---:|
| -1e-8 | 2.66257e-16 | 5.05418e-12 | 3.37546e-13 | 1.62218e-19 |
| -1e-6 | 2.66257e-14 | 5.05418e-8 | 5.47345e-13 | 1.62218e-15 |
| -1e-5 | 2.66257e-13 | 5.05418e-6 | 6.05145e-11 | 1.62218e-13 |

None of these walls retains the original source's kinetic energy. Matching that
energy would require |ye|=0.0375577 and would give Delta a_e=2.28821e-6. This is
in gross conflict with the precision scale of electron-moment tests in the
minimal uncancelled model. For context, [Fan et al., arXiv:2209.13084](https://arxiv.org/pdf/2209.13084),
PRL 130, 071801 (2023), discusses a 7e-13 comparison scale affected by independent
fine-structure-constant determinations. That historical scale is not used here
as a current confidence interval or as a global bound on the smaller Yukawas.
No cancellation or experimental exception has been supplied.

## Lower production energy: a conditional route, with a quantitative cost

As a separate assigned benchmark, set delta=U_wall, so center-produced carriers
have K=U_wall/2. This does not describe an available tuning knob. For ye=-1e-5:

    assigned delta = 2.66257e-13 eV,
    Gamma_phi = 3.94470e-15 eV,
    Br_phi at the assigned pole = 7.80474e-10,
    4 Gamma_gamma Gamma_phi/Gamma_total^2 = 3.73785e-14.

The last number is the partial-width factor relative to a unit-height,
equal-two-channel resonance. It is not an integrated yield. Here the total width
is about 1.90e7 times the wall height, so threshold energy dependence, the actual
beam spectrum and dispersive self-energy must be included before quoting a
production rate. A broad mediator does not prohibit production by a sufficiently
narrow drive, but its central mass and total decay branching alone do not predict
the cold, retained fraction. The electron channel produces ordinary visible
energy; this extension does not support a 'no trace' interpretation.

For a flat 1 cm thick wall, the under-barrier WKB exponent at K=U_wall/2 is

    2d*sqrt(2m*(U_wall-K))/(hbar*c) = 52.2991.

This is only a tunneling exponent, not a measured transmission or storage lifetime.
The two weaker couplings give exponents 1.65 and 16.54; the first is not in a
strong exponential-suppression regime. Finite cavity levels, collision attempts,
material inelastic channels and thermal fluctuations have not been computed.

Assuming ordinary gravity, U_wall corresponds to at most a 2.44 mm gravitational
drop from zero kinetic energy at ye=-1e-5. Nonzero initial kinetic energy reduces
that height. Thus a centimetre-scale vertical cavity cannot simply reuse a
zero-gravity trapping calculation. A thinner cavity requires its quantum level
spacing and gravity to be treated together; free fall is another distinct case.

## Audit and next decision

Nine checks pass: independent electron-moment integration, three forward-potential
normalizations, three coupling-elimination identities, and recovery of both
inherited muon-only widths. The run hashes the earlier source results. No new
Lean certification of the particle model or material physics is claimed.

This route produces a calculable material potential much larger than the inherited
magnetic potential, but adding it changes the source into a predominantly
ordinary-electron decay. Smaller delta can make the kinematics compatible with
the wall at the level of assigned parameters; that is not yet an admissible
production-and-storage mechanism. Applicable electron-coupled scalar searches,
cosmology, material response and the finite-cavity spectral calculation remain
open. Checking those restrictions should precede treating any row as a viable
point or advertising a production yield.

Reproduce:

    python3 sol61_push/electron_material_wall_2026_10_13/check.py /tmp/electron_wall_results.json
