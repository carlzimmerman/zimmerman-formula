# Mechanism triage: stop treating chemical accuracy as a force mechanism

Original objective **not achieved**. Base checkpoint e9030f6ac29e91eeaedc12414c6fdafece8ca560.
The user's request is to find the mechanism, not continue polishing molecular
rates without checking their connection to the desired force.

## Three discriminating routes

1. **Chemical activation of repulsion:** ruled out as a monopole switch in a
   uniform external electric field. The same constituents 2X+C have total +q
   before and after forming T=X2C. Sum_i q_i E=qE is unchanged. T has q/m=q/(201mC),
   compared with q/(100mC) for a bare X. This does not exclude changes in screening,
   mobility, polarizability, correlations, or finite-gradient forces. It proves
   only that molecular abundance is not itself an activation of net electric
   force. A collective constitutive law is a separate missing obligation.

2. **Simple equilibrium phase selector:** in the inherited mean profiles, both
   ideal quantum degeneracy and classical Coulomb freezing favor dwarfs over the
   disk. For common particle parameters and common species fractions,
   n lambda_T^3 is proportional to rho/sigma^3, while the classical coupling
   Gamma=q²/(4pi epsilon a kT) is proportional to rho^(1/3)/sigma².
   Relative to the disk, phase-space density is 14142 and127 times larger in the
   two dwarf profiles; Coulomb coupling is3420 and71 times larger. Thus a single
   monotone threshold in either quantity cannot turn on the disk while leaving
   both dwarfs off. This is a conditional result for these profiles and simple
   criteria, not a theorem excluding interacting or nonequilibrium phases.
   Galactic rotation's direct J=1 internal shift is hbar Omega=5.26e-30 eV in the
   disk proxy. At the previous alpha=.2,mC=10MeV, its ratio to the atomic line
   energy is3.51e-35. Global angular-momentum transport can still alter density
   and temperature; this estimate excludes treating direct atomic rotational
   splitting as a significant chemical selector at that parameter point.

3. **Atomic excitation cooling window:** remains viable as a selection route,
   not an established tethering mechanism. At leading Coulomb order the 1s-2p
   gap is Delta=3 alpha² mC c²/8. The inherited initial temperature is
   kT=(M+1)mC sigma²/2. Hence Delta/kT=3 alpha² c²/[4(M+1)sigma²], independent of
   mC. Equality occurs at alpha=.00008268,.0008268,.01169,.04773 for the four
   profiles. At alpha=.01 the approximate Delta/kT values are14630,146.3,.7315,
   and .04389. Thus a common microscopic threshold can strongly suppress dwarf
   excitation without suppressing disk excitation. At the old alpha=.2 the
   disk ratio is~292.6, so this cooling channel was thermally inaccessible there.
   These ratios do not determine ionization fractions, excitation cross sections,
   photon trapping, a cooling time, formation histories or cluster retention.
   The constituent mass and coupling remain hypotheses, not first-principles
   predictions. A threshold window is not a successful population trajectory.

## What must actually be derived

The strongest surviving route here is cooling and angular-momentum transport,
followed by a genuinely derived collective response. Its success requires ALL:
physical cooling faster than dynamical/assembly time in the appropriate systems;
slow cooling in both dwarfs and clusters across histories; avoidance of runaway
fragmentation; a charge-conserving macroscopic response that supplies repulsive
support; and the observed acceleration relation with common microscopic
parameters. No reaction-rate refinement alone proves these implications.

The present task does not authorize relabeling a dark disk, charged molecule,
condensate or neutral transition probability as this complete mechanism.
There are zero new physical cooling or photon trajectories in this stage.

## Literature checks and limits

- Roy et al., https://arxiv.org/abs/2304.09878: simulations of a6% dissipative
  atomic-dark-matter component form rotating structures but much of it collapses
  into compact clumps. This supports cooling as a physical disk-forming route;
  it does not establish a majority tethered component or a derived RAR.
- Gemmell et al., https://arxiv.org/abs/2311.02148: the tested atomic-DM parameters
  also make dwarfs overly compact. It is direct evidence against assuming that
  dissipation automatically leaves dwarfs free, not a universal exclusion.
- Berezhiani & Khoury, https://arxiv.org/abs/1507.01019: superfluid/normal phases
  distinguish galaxies and clusters, but the MOND-like phonon action is an input
  of that model. Importing it would not derive our microscopic force law.

Primary-source abstracts were checked for these bounded claims. No physical
rate tables or fitted potentials were imported. The four-profile diagnostic
uses the exact inherited environment scalings; its computation manifest pins
both the check script and the original environment source. The algebraic force
argument and phase-ordering interpretation were self-reviewed, not independently
reviewed. No general impossibility claim or discovery claim is made.

## Continuation

Prioritize physical atomic excitation/ionization plus photon escape at the
threshold window, and derive the collective constitutive response separately.
The full nuclear dissociation solver remains available but is no longer treated
as the sole prerequisite for deciding whether a mechanism exists. A plausible
continuation is open; neither rates nor the mechanism have been established.

## Conditional quantitative cooling discriminator

`run_freefree` evaluates20 profile/parameter cases using the nonrelativistic
free-free emissivity of Rosenberg & Fan, https://arxiv.org/pdf/1705.10341, Eq.(8),
with the first approximation g_ff=1. In Coulomb units,
P/(E_H/(t_D a_D³))=(16/3)sqrt(2pi/3) alpha³ n_X n_C sqrt(T).
With equal temperatures and n_X=n_C=n, U=3nT, so t_emit=U/P.
This is emitted power, not necessarily escaping power. At fixed density and
ionization, sqrt(T) decreases linearly in time; adding the emitted photon energy
to matter energy closes an exact ledger. This simplified ledger is tested.

At alpha=.01, mC=10MeV, M/mC=100, with the same inherited mass inventory for all
profiles, the disk and cluster ionized-thin emission times are respectively
7.062 million years and17.299 billion years. The corresponding idealized times
to the atomic excitation scale are2.044 million and27.350 billion years. These
are conditional estimates, NOT physical net-cooling predictions or trajectories
with chemistry. The dwarf line gap/temperature ratios are14629 and146.3, making
thermal excitation strongly suppressed if neutral atoms are available. Conversely,
if dwarfs remained fully ionized, their computed bremsstrahlung times are short;
neutralization history cannot be assumed away.

At this point the disk Thomson optical depth is only .00323, but a neutral
fraction of8.41e-5 already gives unit photoionization optical depth at the atomic
threshold along the proxy radius. Thus low Thomson depth does not justify
transparent cooling. This is a frequency-specific bound-free diagnostic, not
an opacity for all bremsstrahlung photons or a line-transfer calculation.
Recycling and ionization must be solved to decide actual escape and cooling.

The mass scan checks t_emit proportional to mC³ at fixed alpha, density and
velocity. Neither alpha nor mC has been derived from first principles; the common
example is an exploration of a surviving window, not an independently predicted
parameter point. Finite-mass, quantum Gaunt, weak-plasma, thermalization, neutral
fraction, optical-transfer, cosmological-history and collapse/fragmentation
conditions still require validation. The actual interaction is ordinary dark
Coulomb radiation, not an invented galaxy-dependent rate. It is a candidate for
morphological selection, not repulsive tethering or the acceleration relation.

This adds an approximate microscopic emissivity calculation; it does not add a
physical ionization/cooling/recycling trajectory. The earlier statement of zero
new physical cooling trajectories therefore still applies. Both manifests validate.
