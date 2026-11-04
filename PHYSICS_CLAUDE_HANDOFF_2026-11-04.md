# Claude handoff: coupled trapping, depletion and photino production

Publication checkpoint requested by the owner on 4 November 2026. This adds
the TP06 gravity/production work and CT09 coupled-trapping continuation to
the earlier TP01--TP05 handoff. The physical program remains open.

Read [CT09 current result](reviews/coupled_trapping_2026_11_04/README.md),
its [closeout](reviews/coupled_trapping_2026_11_04/CLOSEOUT.md) and
[continuation obligations](reviews/coupled_trapping_2026_11_04/HANDOFF.md).
Then read the [independent mathematical review](reviews/coupled_trapping_2026_11_04/independent_review/REVIEW.md)
and [transport review](reviews/coupled_trapping_2026_11_04/transport_review/REVIEW.md),
including their addenda. Prior inputs are in
[TP06](reviews/gravity_completion_2026_11_03/README.md); earlier ancestry is in
[the November 1 handoff](PHYSICS_CLAUDE_HANDOFF_2026-11-01.md).

## Current result

At equal weak coupling e=.003, the coupled reduced equations can retain a
homogeneous local vacuum while removing most charged particles. A charged
scalar pair resonance, absent from the old light-fermion calculation, occurs
at X/mu=sqrt[60/(31e)]=25.4000254000381.

A lighter same-family candidate has mu=2e6 GeV, a roughly 105 keV photino and
77 TeV charged scalar. Necessary coldness and fixed-leading-current survival
tests pass. Finite local scalar stability and the separately aligned leading
trajectory action are explicitly distinguished; their minima otherwise differ
by about .0029 in X/mu, material for a narrow pole.

The preferred completed diagnostic is an explicitly hybrid NWA-early,
finite-width-late trajectory. Its charged yield remains about 1,110 times the
10%-DM allowance. Even ideal additional future annihilation through the fixed
pole leaves at least about 42 times that allowance when every fermionic pole
exit is blocked. Named direct charged conversions supply about 0.376% of the
required photino DM density. These statements are conditional on their saved
collision models and ensemble, not a model-wide no-go.

## Continue at the missing physical step

Derive the statistical and delayed-parent collision system: neutral resonance
occupations and cascades, massive neutral daughter forces, gaugino Pauli/inverse
terms, charged-scalar Bose factors, and a justified correlation/dephasing or
memory treatment on the oscillating background. Another instantaneous sink
scan does not supply this missing implication. Full heavy pole and SUGRA1PI
current matching remain separate obligations. The dark-energy residual is
still adjusted by W0 rather than predicted; do not reinstate the unverified
81 eV neutral pole claim or treat kappa=1/2 as derived.

Failed attempts, exact historical source versions and a timed-out full
finite-width run are preserved. Two runner-completed kinetic records with
the wrong phase-splitter pole are explicitly excluded in RUN_INDEX.json.
The completed late hybrid does not turn that timeout into a full history.

## Verification and preservation

The two phase VERIFICATION.json files pin sources, outputs and ancestry.
CT09's verifier checks all recorded output hashes, recovers exact historical
source bytes and confirms that all 363 pinned TP06 artifacts remain unchanged.
The independent reviews distinguish provenance from physical correctness.

For a fresh provenance check, run:

    python3 reviews/coupled_trapping_2026_11_04/verify_checkpoint.py

This uses the installed mathbox manifest validator and does not rerun science.
Recorded numerical commands require their declared Python packages and bounded
runner; use fresh output directories. Preserve frozen scientific records and
source hashes. Statements in phase records that no Git mutation occurred refer
to the research phase before this owner-requested publication checkpoint.
