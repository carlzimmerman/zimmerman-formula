# Initial carrier production after a thermal mass update

2026-10-13. This extends the real threshold-limit calculation in
../thermal_source_carrier_shift_2026_10_13/REPORT.md. It supplies a finite-detuning
check and an initial collision source within a narrow on-shell particle
approximation. It does not solve the coupled source/carrier evolution.

## Prescribed starting state and principal value

Keep the equilibrium R bath, negligible initial phi and anti-phi populations,
mu=27.72246466 eV, vacuum m=1 MeV, and the assigned weak-wall vacuum excess
delta=2.6625713955e-16 eV. Set the independent R^2|phi|^2 coefficient to zero as
in the preceding calculation. Apply ONE mass update m*=m+Delta m(T), using its
thermal-R real contribution. Both daughter dispersions use this same m*.
The parent pole remains MR=2m+delta. This is a specified approximation, not a
solved gap equation or a fully dressed spectral function.

At finite positive MR-2m*, the real forward integral is

    Pi=-mu^2*MR^2/(8pi^2*m*^2) * PV integral_0^infinity dk
           k^2*nB(ER)/[ER*(k^2-k0^2)],
    k0=MR/(2m*)*sqrt((MR-2m*)*(MR+2m*)),
    ER=sqrt(MR^2+k^2).

Here 'm*^2' means (m*) squared. To evaluate the principal value, use q=k/T,
b=k0/T and h(q)=nB(sqrt(q^2+(MR/T)^2))/sqrt(q^2+(MR/T)^2). Then

    J=integral h(q)dq
       +b^2*integral [h(q)-h(b)]/(q^2-b^2)dq.

The second integrand has a removable singularity. The identity uses
PV integral_0^infinity dq/(q^2-b^2)=0. No imaginary collision contribution is
inferred by incorrectly treating this principal value as an ordinary integral.

For bath temperatures 0.5, 1, 2 and 3 MeV, the finite-detuning real result differs
from the prior threshold-limit contribution by at most 2.7e-11 fractionally.
This verifies continuity of this particular real contribution for the tested
one-step masses. It does not bound all higher-order or finite-width corrections.

## Initial collision source and detailed balance

For R -> phi+anti-phi, the statistical gain-minus-loss factor is

    fR*(1+fphi)*(1+fanti) - (1+fR)*fphi*fanti
      = fR*(1+fphi+fanti)-fphi*fanti.

Initially both daughter distributions vanish, leaving spontaneous production.
As they grow, Bose enhancement and inverse reactions must both be retained.
At common temperature, zero chemical potentials and ER=Ephi+Eanti, the factor
vanishes exactly. The accompanying Lean source proves its algebraic expansion
and the thermal rational-function identity. It does not establish the validity
of the on-shell kinetic approximation.

The invariant collision expression for one daughter is

    dfphi(p)/dt = mu^2/(2Ep) * integral dPi_R dPi_anti (2pi)^4
                 delta^4(k-p-q) * [gain-minus-loss],
    dPi_i=d^3p_i/[(2pi)^3*2Ei].

There is no identical-final-particle factor: phi and anti-phi are distinct.
For the initial p=0 mode this reduces to

    S0 = mu^2*k0/(8pi*m*^2) * nB(MR^2/(2m*)),

in natural units. Direct reduction of the phase-space energy delta function
supplies the same Jacobian. S0 describes df/dt for a phase-space occupation,
not a number of stored particles per second.

For all momenta combined, the initial daughter-number source is

    dn_total/dt = 2 Gamma_phi nR <MR/ER>,
    Gamma_phi=mu^2/(16pi*MR)*sqrt(1-4m*^2/MR^2),
    nR=MR^2*T/(2pi^2)*sum_n K2(nMR/T)/n,
    <MR/ER>=[sum_n K1(nMR/T)/n]/[sum_n K2(nMR/T)/n].

This includes Bose-Einstein statistics for the parent and initially empty
final states. The denominator used to normalize the source in the table below,
n_phi,eq, is the equilibrium number density of BOTH daughter species at T. It
is a reference scale, not an assumption that the initial daughters are thermal.

## Calculated initial values

| Bath T | Updated excess MR-2m* (eV) | Initial df(p=0)/dt (1/s) | Initial (dn_total/dt)/n_phi,eq (1/s) |
|---:|---:|---:|---:|
| 0.5 MeV | 4.40286e-7 | 1.150e3 | 1.472e3 |
| 1 MeV | 4.92382e-6 | 3.227e4 | 8.500e3 |
| 2 MeV | 2.28312e-5 | 2.584e5 | 1.767e4 |
| 3 MeV | 4.56778e-5 | 6.626e5 | 2.105e4 |

At 2 MeV the initial spontaneous partial width in this approximation is
3.65282e-11 eV. The previously calculated expansion rate near that temperature
was about 2.82/s. Thus neglecting carrier production indefinitely is inconsistent
with these prescribed-bath initial rates. It does NOT follow that equilibrium
is reached on the inverse tabulated timescale: source depletion, inverse decay,
new mass shifts and redistribution change the rates as soon as populations grow.

Most parents in a MeV bath are moving. A rest-mode occupation source does not
mean the whole emitted population is cold, and the integrated source counts all
momenta. Neither number is a laboratory capture yield or evidence for a
macroscopic cold-energy reservoir.

## Scope and remaining work

The calculation retains unit quasiparticle residues and narrow on-shell phase
space. It omits a source-pole update, finite-width spectral functions, carrier
self-interaction corrections after population, and other bath contributions.
The independent mixed quartic can change the mass update, as already quantified.
No exponential Bose growth is extrapolated, no final relic abundance is given,
and the R-only neutrino result is not promoted to a full-model exclusion.

The standard collision-factor framework and its on-shell limitations are
explained in [Weinstock, *Boltzmann Collision Term*, hep-ph/0510417v1](https://arxiv.org/pdf/hep-ph/0510417),
31 October 2005, introduction and Secs. II–IV. That source supports the kinetic
framework, not these particle parameters or the one-step mass approximation.
The specific two-body phase-space reduction and integrals are derived here.

Twenty checks pass: four threshold-integral reproductions, four finite-detuning
comparisons, four daughter mass-shell identities, four phase-space Jacobian
checks and four detailed-balance checks. The principal-value integrals use
45-decimal arithmetic; thermodynamic sums use 120 terms. Two Lean algebraic
lemmas compile with standard axioms. These checks do not certify new physics.

The next necessary calculation must evolve source and daughter populations
together with their energy accounting and medium-dependent thresholds. The
initial-rate result makes that requirement concrete; it does not complete the
manufacturing objective.

Reproduce:

    python3 sol61_push/thermal_carrier_initial_production_2026_10_13/check.py /tmp/thermal_carrier_initial_results.json
