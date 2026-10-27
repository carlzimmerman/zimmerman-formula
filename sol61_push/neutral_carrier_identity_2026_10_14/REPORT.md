# Identity gate: optical neutral pairs are not yet the cosmological carrier

Parent: 1e8d0153678dd36b8e065548f80f2123cfd506cc.
The optical preparation model and the earlier cold-carrier Hamiltonian cannot
be identified merely because both use eV bosons. The optical source creates
opposite-charge pairs. In a dilute coherent reduction, their near-resonant
interaction is attractive and differs dramatically from the older repulsive
single-species contact model. At an assigned halo density the same reduction
loses its small parameter entirely. This does not refute laboratory pair
creation, or prove that no many-body completion exists; it identifies the
missing bridge to the requested cold-energy mechanism.

## Reconcile the actual repository claims

The October 10 cold_field_identity report says the substance is not uniquely
identified and excludes only specified stationary single-mode support models.
The microscopic_carrier report declares a multimode massive-field candidate
with a repulsive contact interaction, but explicitly leaves abundance, halo
selection and the dark-energy connection unresolved. Neither report proves
that an arbitrary massive boson reproduces the target halo law.

The October 14 ev_resonance_reciprocity report already showed that classical
binary-collision estimates are not automatically admitted at its illustrative
halo occupation and collision-memory scales. The new calculation below is a
separate coherent mean-field diagnostic, not a replacement for that audit or
a kinetic solution for the actual halo state.

## Keep both charges and the resonant mediator

Let a,b be nonrelativistic carrier fields for the two charge signs and r the
near-threshold mediator amplitude. The retained rotating-frame interaction
energy density has terms

    delta |r|^2 + h(r* a b + r a* b*)
    + gs/2 (|a|^4+|b|^4) + gc0 |a|^2 |b|^2,

where h=mu/(2m sqrt(2M_R)). For the assigned parameters, the leading
nonresonant matching used in the preparation work gives

    h=0.0005 eV^(-1/2),
    gs=lambda/(2m^2)-mu^2/(4m^2 M_R^2)=2.5e-7 eV^-2,
    gc0=(lambda-mu^2/(4M_R^2))/m^2=7.5e-7 eV^-2.

This truncation omits other operators and dynamical/environmental corrections.
If frequencies, gradients and density-induced mixing are small relative to
delta, completing the square gives

    r approximately -h a b/delta,
    gc=gc0-h^2/delta approximately -125 eV^-2.

The same-sign coupling stays positive. For a coherent equal mixture the
interaction-density Hessian is [[gs,gc],[gc,gs]]. Its density eigenvector
(1,1) has eigenvalue gs+gc<0; its charge eigenvector (1,-1) has gs-gc>0.
This is not the pressure law of a repulsive one-component fluid.

For a homogeneous coherent mixture of total carrier density n, the eliminated
Bogoliubov density branch would have

    (hbar omega_k)^2=epsilon_k [epsilon_k+n(gs+gc)],
    epsilon_k=k^2/(2m).

That formula has long-wavelength unstable modes WHEN its elimination and
coherent homogeneous-state hypotheses hold. It is not a stability verdict
for arbitrary multimode halos, a finite trap or the full relativistic theory.
In particular, negative quartic energy in this limited rotating-frame
elimination is not proof that the underlying relativistic potential is
unbounded.

## Test the elimination scale before extrapolating

A useful coherent mixing parameter is

    epsilon_mix=h sqrt(n)/delta,
    epsilon_mix^2=(h^2 n/delta)/delta.

Here n is in natural units. It compares a collective coupling scale to the
mediator detuning; numerical factors depend on the specified mode/state
linearization. It is a diagnostic for this coherent ansatz, not a universal
admissibility criterion for all distributions.

The assigned parameters give epsilon_mix=1 at total number density
2.08238e9 /m^3, and epsilon_mix=0.1 at 2.08238e7 /m^3.

| Assigned state-density proxy | epsilon_mix |
|---|---:|
| Two carriers divided by a 2 cm sphere volume | 0.00535 |
| One hundred pairs divided by that volume | 0.0535 |
| 0.3 GeV/cm^3 divided by 1 eV per carrier | 379.56 |

The last density, 3e14 /m^3, is an inherited illustrative assignment, not a
measurement in this calculation. Its nominal second-order shift/detuning
ratio is 1.44e5. An eliminated weak-mixing description therefore cannot be
used to predict that state's spectrum or pressure. The code deliberately
omits an instability-growth prediction for that row.

For the first two rows the formal homogeneous fastest-growth wavelengths
are 5.18 m and 0.518 m, both much larger than the 4 cm trap diameter.
A two-particle state is not a coherent fluid, and these homogeneous wavelengths
are not finite-trap eigenmodes. Their tabulated growth rates must not be
presented as escape or collapse times for the laboratory pair calculation.
A finite geometry and the actual quantum state must be treated explicitly.

## Required bridge, rather than a change of name

A candidate next description must retain mediator dynamics, for example

    i hbar a_dot = [K_a + gs|a|^2 + gc0|b|^2]a + h r b*,
    i hbar b_dot = [K_b + gs|b|^2 + gc0|a|^2]b + h r a*,
    i hbar r_dot = [delta+K_r]r + h a b,

with kinetic/gravitational operators K, required additional operators and a
justified treatment of statistical mode occupations. In the closed rotating-
wave model, N=integral(|a|^2+|b|^2+2|r|^2) and Q=integral(|a|^2-|b|^2)
are conserved. Optical preparation from vacuum supplies Q=0. A one-component
reduction must derive how its state and effective pressure emerge from that
neutral system; it cannot simply discard the opposite charge.

Even a consistent many-body state would still have to derive the repo's
baryon-dependent halo normalization and its proposed dark-energy dependence.
The displayed local portal does not introduce that selector. Producing its
quanta is therefore not, by itself, producing an identified realization of
the repo's cosmological cold energy.

## Evidence and outcome

Exact symbolic checks verify square completion and the two Hessian
eigenvectors. The density/unit calculations and coefficient signs are recorded
in the bounded run; input reports and output hashes validate in its manifest.
This is an analytic self-review, with no new Lean certification or empirical
claim. The ordinary-complex-amplitude derivation is conditional on its stated
nonrelativistic coherent truncation.

The goal remains open at a more fundamental point than optical engineering:
the created neutral pair sector has not been shown to be the required
cosmological medium. The next useful theoretical step is the explicit
three-field dynamics at fixed N and Q, or a valid kinetic alternative,
followed by a test of the gravitational state. Further optical improvement
alone cannot establish that identity.
