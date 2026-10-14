# Scoped stellar-constraint audit of the assigned eV portal

Parent: 54a261c4af5f1c2a6e7903d18986110443dbe98d.
The assigned portal couplings are smaller than the particular stellar
reference bounds checked here. That is a narrow consistency comparison,
not empirical evidence for the carriers or global admission of the model.
The added carrier interaction also changes the decay phenomenology so much
that a blanket transfer of photon-decay exclusions would be invalid.

## Primary-source check

Caputo, Raffelt and Vitagliano, “Muonic boson limits: Supernova redux,”
Phys. Rev. D 105, 035022 (published February 22, 2022), was inspected in
its [published PDF](https://journals.aps.org/prd/pdf/10.1103/PhysRevD.105.035022)
on October 14, 2026. Section II A uses a scalar muon Yukawa interaction and
assumes no other tree-level interactions. Its scalar maps to this repo's R,
its scalar Yukawa to |y_mu|, and its photon coefficient to |g|.

Equations (15)-(16) give the light-mass HB benchmarks G_gamma_gamma<6.7e-11
GeV^-1 and |y_mu|<4.6e-9. Table I gives scalar SN cooling benchmarks
4.2e-9 and 1.9e-9 for its cold and hot reference models. Those are the
explicit Table I values used here. Stellar populations, composition,
transport and SN models enter their interpretation; they are not
assumption-free measurements of a new coupling. Section VII A also makes
its cosmological discussion depend on early thermal equilibrium.

Access/provenance details are in source_record.json. The source was read
remotely; no local PDF hash is claimed. This is a bounded source/application
audit, not a current exhaustive literature survey or a novelty claim.

## Match units and couplings

The assigned g=1e-20/eV equals 1e-11/GeV: the inverse-energy conversion
MULTIPLIES the numerical value by 1e9. Using the already specified muon-loop
completion,

    g=-2 alpha y_mu/(3 pi m_mu),
    |y_mu|=6.82306850e-10.

| Reference comparison | Benchmark / reference upper value |
|---|---:|
| HB photon coupling | 0.1493 |
| HB muonic scalar Yukawa | 0.1483 |
| SN scalar cooling, Table I cold model | 0.1625 |
| SN scalar cooling, Table I hot model | 0.3591 |

These ratios are arithmetic comparisons, not likelihoods, confidence levels,
safety margins or proof that the extended model obeys all constraints.
In particular, a parameter below a source's upper bound is not a positive
observation of that parameter. No change to the assigned values is made.

## Quantify the additional interaction's effect

The repo also assigns L_int=-mu R |phi|^2, mu=.002 eV, m_phi=1 eV,
M_R=2m_phi+delta with delta=2e-9 eV. The tree-level vacuum decay widths are

    beta=sqrt[delta(4m_phi+delta)]/M_R,
    Gamma_dark=mu^2 beta/(16 pi M_R),
    Gamma_photons=g^2 M_R^3/(64 pi).

The beta expression avoids subtracting nearly equal floating-point numbers.
For distinguishable phi and anti-phi there is no identical-particle half
factor in Gamma_dark. The resulting values are

    Gamma_dark=1.77940636e-12 eV,
    Gamma_photons=3.97887359e-42 eV,
    Br(R->photons)=2.23607e-30,
    vacuum rest lifetime=0.000369905 s.

These are properties of the assigned model, not measured decay data. They
show why a radiative signal calculation with a photon-dominated branching
ratio cannot be copied over. They do not show that every photon constraint
vanishes: secondary production, inverse processes, transport and altered
populations can matter. Replacing a lifetime or multiplying one bound by a
branching ratio is not a complete recast.

Illustrative boosted mean decay lengths at R energies 1 keV, 10 keV and
100 MeV are 5.54e7 m, 5.54e8 m and 5.54e12 m, respectively. These follow
beta_gamma c tau and are not stellar spectra. In particular, a short REST
lifetime does not establish local energy deposition by highly boosted R.
Nor does conversion into carriers necessarily return the energy to ordinary
matter. A coupled transport calculation is required to decide where energy
is carried and whether it escapes.

## What this admits and what it does not

This check finds no immediate arithmetic contradiction with the named
reference upper values. Because the microscopic model is extended, it does
not independently establish even those observational constraints for the
full system. No assumption-free empirical support for cold-energy creation
has been obtained. The observational inputs remain those underlying the
published stellar analysis, with its stated physical assumptions.

A full admission audit still needs the produced R/phi distributions,
carrier transport and self-interactions, early-universe history, relevant
laboratory and short-range-force searches, and uncertainties in the complete
material response. The repo's proposed cosmological role cannot be inferred
from laboratory pair-preparation algebra. Strongly interacting cold-sector
transport already has separate unresolved issues in the resonance-reciprocity
package; this portal comparison does not close them.

The computational record checks loop-matching arithmetic, reference ratios
and width hierarchy. Its bounded manifest validates provenance, not external
source correctness or experimental admission. No new Lean proof is claimed.
The overall goal stays open. The next physical test is to calculate transport
for the added carrier sector under explicitly stated environments, or to find
a laboratory observable that can distinguish this model from no new particles.
Further polishing of the optical apparatus alone cannot resolve that gap.
