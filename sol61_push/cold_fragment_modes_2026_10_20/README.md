# Natural cooling of cold fragments

20 October 2026. **Conditional mechanism found; full theory open.**

An excited fragment's trapped quadrupole oscillation generates its own
escaping second harmonic in the specified alternative common matter action.
A chiral mode exports energy, particle charge and intrinsic spin. A standing
combination of opposite chiralities exports energy and charge with zero net
spin, mostly through a monopole harmonic. No external pump or friction was
inserted. These are weak-amplitude frequency-domain calculations, not evolved
mergers or a demonstrated dwarf formation history.

Start with [ACTION_AND_MECHANISMS.md](ACTION_AND_MECHANISMS.md) for the action,
field equations, conserved quantities, nonlinear sources, damping and charge
backreaction. [HANDOFF_TO_CLAUDE.md](HANDOFF_TO_CLAUDE.md) gives the next test.
The prior [common-action report](../cold_completion_2026_10_20/EQUATIONS_AND_MECHANISMS.md)
contains the production, energy-floor and dense-phase derivations.

The leading loss law is `dK_exc/dt=-gamma K_exc^2`, with
`K_exc=E_bound-E_stat(Q_bound)`. Both modes emit positive Psi charge, so the
retained mass inventory must change. At Q160000 the chiral/standing gamma
values are 1.6773341e-7/1.4410450e-5 in the declared natural units. The scale
m has not been identified physically; these are not dwarf cooling times.

| Evidence | Record | Scope |
|---|---|---|
| True-origin stationary profiles | profile_origin/run_001 | 23 controls; regular-origin BVP, branch energies |
| Same-action finite spectra | grid_run_002 | 95 controls; deterministic starts, symmetry and convergence |
| Natural quadratic source | natural_run_002 | 49 controls; normalized chiral mode and actual self-source |
| Chiral scalar radiation | radiation_run_002 | 60 controls; outgoing E/Q/intrinsic-J flux |
| Static initial charge backreaction | dc_run_001 | 75 controls; cancellation through order K |
| Zero-net-spin standing radiation | standing_run_001 | 172 controls; natural monopole/quadrupole outlets |

Counts are scoped controls, not independent confirmations or continuum
proofs. Completed manifests pin commands, source/data bytes and software.
Measured per-run RSS is below 200 MB. Both failed finite-r_min attempts and
historical unpinned ARPACK runs are retained. See [PROVENANCE_NOTES.md](PROVENANCE_NOTES.md).

Independent reconstructions are in [REVIEW_FINITE_SPECTRA.md](REVIEW_FINITE_SPECTRA.md),
[REVIEW_NATURAL_RADIATION.md](REVIEW_NATURAL_RADIATION.md),
[REVIEW_DC.md](REVIEW_DC.md), [DC_RECIPROCITY.md](DC_RECIPROCITY.md) and
[REVIEW_STANDING.md](REVIEW_STANDING.md). Review provenance identifies shared
authorship where applicable; it is not an external blind review.

The [merger ledger](MERGER_LEDGER.md) keeps charge loss and chirality costs
explicit. [QUANTUM_CORRESPONDENCE.md](QUANTUM_CORRESPONDENCE.md) describes
conditional pair-loss selection rules and the unresolved few-quantum limit.
[CLAUDE_UPDATE.md](CLAUDE_UPDATE.md) reconciles finalized CFG932/933 artifacts:
post-hoc receiver completion is now acknowledged; P2 remains fragile.
[The finalized CFG934 audit](CLAUDE_CFG934_ARRIVAL.md) finds a
PARTIAL/FRAGILE primary cooling-floor result that leaves Draco's
extra-support factor zero. It supplies no microscopic transport rate.

**Still required:** merger excitation/capture and nonlinear validity; a
physical mass/abundance normalization; galactic outward orbital torque and
receiver survival; stock-compatible Draco/Sextans profiles without excess
Fornax/Leo I; a consistent gravity/lensing architecture; cosmology and quantum
robustness. No frozen criteria, publication or shared CE-FM-093 pointer changed.
