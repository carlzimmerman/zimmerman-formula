# CT09 continuation

The requested combined goal is still open. Read README.md and CLOSEOUT.md,
then kinetics/STATUS.md and the two independent reviews. Exact base revision,
input hashes, run statuses and assessment revision are pinned in the contracts,
manifests, BASE_PINS.json and VERIFICATION.json. No Git commit was made here.

## Current decisive state

At equal weak coupling e=.003, g=sqrt(29/200)e, the original canonical and
protected cases admit conditional charged-supported trajectories but leave
large heavy relics. A new charged-scalar pair resonance occurs at
X/mu=sqrt[60/(31e)]=25.4000254000381. It was absent from the prior light-fermion
inverse-decay calculation. Its full four-state absorptive matrix is in
microphysics/run_pole002 and run_medium001; do not sum independent degenerate
Breit-Wigner poles or insert a factor-of-two guessed from real scalar counts.

The lighter same-family candidate has mu=2e6GeV, photino about104.73keV and
charged scalar77.46TeV. Necessary coldness, leading current survival and ideal
pole capacity pass. Finite local scalar vacuum: gravity_resonance/run_candidate001.
Consistently aligned *leading trajectory action*: run_leading001, with its
mixed local stability check run_stability001. These are different truncations;
the finite and leading minima otherwise differ by about.0029 in X/mu.

Preferred trajectory evidence:

- kinetics/run_leading_fine_001: matched-leading32-bin NWA reference to Tc/mu=1e-5.
- kinetics/run_hybrid_bw_001: starts from the24-bin NWA state at1e-5 and uses
  the stationary coherent finite-width pair kernel to1e-6. Ycharged=6.30e-13,
  about1,110 times the10%-DM gate. It retains a local bound orbit.
- gravity_resonance/run_continuation002: even maximal additional future loss
  through this fixed pole leaves at least about42 times the allowance after
  removing all fermionic pole exits. This bounds continuation from that
  conditional endpoint, not every possible earlier history.
- kinetics/run_source_diagnostic_001: direct unblocked conversions produce
  about.376% of the required photino DM density. This is a named-source count,
  not a bound on neutral/loop/cascade production.

The full initial-to-final finite-width run timed out. Its missing result must
not be promoted to a completed history. Source versions and failed runs are
retained. Radial-bin trajectory convergence remains unresolved; local endpoint
angular/phase controls are much tighter but test a different obligation.

## First unresolved physical implication

Derive a common collision description for the changing background and actual
populations. The existing absorbing-parent and empty-gaugino approximations do
not establish irreversible depletion in the microscopic model. Attack this
dependency before sweeping more couplings:

1. Determine the neutral scalar self-energy correlation/dephasing time and
   dynamical four-state propagator along the recorded cold orbits. Test when
   stationary local inverse-decay/Breit-Wigner rates follow. Gamma/omega alone
   is not the criterion; parent lifetimes are about1.4--2.7 oscillations.
2. Retain neutral resonance occupations and their actual charged-returning
   cascades. Track massive neutral daughter distributions and their occupation
   forces. Endpoint daughters/derivatives are in microphysics/run_endpoint002.
3. Couple charged F and C distributions to all twelve light gauginos with
   Pauli factors, Bose factors for charged scalars, inverse decays and charged
   daughter recoil. The projected conversion vertices are in photino/source.py
   and run_source004. A soft prompt burst is already overoccupied; it cannot
   simply be normalized to the desired abundance.
4. Keep number, charge, energy, field force and oscillation action in the same
   system. Preserve the action covariance in ACTION_IDENTITY.md. Gauge-covariant
   factorized one-particle populations justify component equipartition; gauge
   symmetry alone does not remove possible two-particle correlations.

If correlation/dephasing justifies a Markov reduction, use it with measured
regime checks. If it does not, solve the delayed-parent/density-matrix system
rather than inserting a prompt radiation sink. Either outcome changes the
current scientific decision. The tested reduced histories are not a proof
that this entire route is impossible.

## Separate dependencies and resumption conditions

- Heavy pole matching: real one-loop threshold shifts are comparable with the
  narrow widths. Retune physical scalar masses and gravity placement together;
  a tree-threshold coordinate is not a finite mass prediction. Linear normal
  CW/two-loop vacuum terms alone do not supply all heavy pole self-energies.
- Dark matter source: direct conversions underproduce in the recorded history.
  Neutral cascade/loop sources require actual operators and branchings before
  any abundance claim. Bare C Cbar->gauginos has a conservative finite leading
  tree bound in microphysics/run_tchannel002; long-range/correlation treatments
  have their explicitly narrower domains.
- Full SUGRA1PI current/spectrum: the leading inclusive current-norm lifetime
  bound survives arbitrary neutral pole mass, but its quantum normalization and
  additional operators are not matched. Do not restore the old81eV pole claim.
- DE: the residual is still selected by W0 adjustment. A predictive protection
  or selection relation is a separate new physical input, not more tuning.
- Cosmological initialization/modulus population: the cold hidden FD initial
  state, xi=.02 and stationary modulus remain explicit assumptions. Local scalar
  stability does not derive their preparation or exclude modulus cosmology.

No remaining route is called exhausted. The statistical/dynamical-parent
collision action and matched heavy poles are the load-bearing open work. Every
new experiment must use a fresh bounded v2 record, one numerical thread, actual
input hashes and measured RSS. Preserve TP01--CT09 science. No install, new
portal, Git mutation or external message follows automatically from this handoff.
