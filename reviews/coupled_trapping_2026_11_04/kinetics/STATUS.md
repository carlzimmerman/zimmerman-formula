# CT09 kinetics checkpoint: coupled reduced histories, target remains open

The requested full energy/charge-consistent DE + small charged relic + cold
photino history has **not** been established. This package now executes actual
coupled charged-fermion/scalar occupation distributions and the field, with
changing force and a single energy ledger. It also contains a completed late
coherent finite-width continuation. These are explicitly conditional reduced
collision networks: gaugino Pauli/inverse terms, neutral daughter forces,
coherent time-dependent resonance memory and final photino distributions remain
missing. No finite grid or reduced-network success is a physical solution.

## Preferred checkpoint

`run_hybrid_bw_001/result.json` is the preferred completed late-pole diagnostic.
It starts from the completed 24-bulk-cell matched-leading NWA history at
Tc/mu=1e-5 and switches to the fixed-pole coherent Breit-Wigner kernel until
Tc/mu=1e-6. This switch is an explicit hybrid, not full BW evolution from the
initial population and not an upper bound on all possible histories.

- Same-family protected leading packet: e=.003, mu=2e6 GeV,
  epsilon=.0248616322541410413, cold leading minimum aligned exactly with the
  tree scalar pair pole x=25.4000254000381. This is a new physical gravity
  parameter choice, not the original protected packet.
- Initial charged FD state and xi=.02 remain conditional; initial x and Tc
  are retained from the prior protected spinodal packet.
- Late endpoint: Ycharged=6.302878928367489e-13, survival=1.71731386345e-6,
  entirely the charged scalar branch. The orbit is
  25.4000254000379 +/- 3.34564e-6. It is locally cold and remains charged.
- Number loss/H=.518268, J=7.54235e-18; gauge emission count from the named
  conversion source is .2584292125 per initial carrier.
- Particle/field + auxiliary radiation + Hubble-work ledger differs by
  1.1238e-4 of initial particle energy. The run completed in 135 seconds,
  measured peak RSS 86.7 MB, one numerical thread; local rates remain small
  compared with the field frequency.

The coordinator owns the all-future fixed-pole rate envelope and the comparison
with the charged allowance. No late time cutoff is used here as a proof of
physical freezeout. The auxiliary radiation ledger is not a photino abundance.

## What changed relative to fixed occupation

Fermion-only absorption is not the final charged-state history. At Tc=.0005,
64-bulk-bin fermion-only absorption gives survival .02064 canonical and .19696
protected, but actual F->S+gaugino rates convert the carriers to scalars.
The scalar singlet resonance at x=25.4000254 reopens an important late sink.
The two-species runs include isotropic two-body charged-daughter momentum
redistribution and the actual projected vacuum conversion widths.

For the original gravity packets, the two-species 24-bulk/16-orbit run reaches
Tc=.0005 with Ycharged=4.77946e-10 canonical and 4.74648e-8 protected. The
16-bulk/12-orbit values were 9.9674e-11 and 4.4076e-8: the canonical narrow
resonance abundance is not converged. These values are finite diagnostics,
not precision predictions. The endpoint charged population remains large.

For the matched-leading pole packet, complete NWA histories to Tc=1e-5 at
24 and 32 bulk cells give Ycharged=2.17745e-12 and 1.87763e-12, a 13.8%
shift. Both have loss/H about .512 at that endpoint. This is why the preferred
late result is reported as a hybrid finite-width diagnostic, with an endpoint
quadrature repeat, rather than a claim of converged physical abundance.

A terminal charged-deficit rate sensitivity run, using the actual tree cascade
multiplicity clipped to avoid pair multiplication, gives survival .47745
canonical and .84597 protected at Tc=.0005. This is only a rate-feedback test:
returning daughter momentum, scalar conversion and massive neutral forces are
omitted there. A neutral terminal daughter is never silently called a photon.

## Meaningful controls and independent review

- The finite-volume inverse-decay kernel agrees with the independent
  parent-momentum integral within 1.94e-4 at 192 bulk cells on three cases.
- Four explicitly resolved initial oscillations agree with averaged occupation
  evolution to 1.96e-5 of initial number. Two solver tolerances give direct
  energy-ledger errors below 3.7e-8.
- Conversion generators preserve carrier number (maximum column-sum residual
  1.1e-25), are positive off diagonal, and reproduce the independent exact
  massless-neutral two-body mean energy within 5.2e-8 on seven points.
- Pole-split harmonic phase quadrature, 4 versus 16 nodes per interval, agrees
  within 4.66e-4 at three cold temperatures.
- Finite-BW arctan angular integration agrees with the independent split-cosine
  API to weighted relative error below 3e-7 and entry errors below 8e-7.
- The inclusive production Gram/partial-width normalization agrees within
  4.2e-5. A 256-cell finite-BW/NWA rate ratio .76709 agrees with the independent
  neutral-exit probability .76984 within .36%; 128->256 shifts .793%.
- The fresh transport review confirms the total-carrier 1/2 annihilation
  factor, the Moller transformation and action covariance bookkeeping.
  It independently finds 24-bulk-cell FD number error about -2.01% and static
  NWA kernel errors about 5--8%; 32 cells reduce them. These numerical limits
  remain explicit. The final NWA action clamp is inactive at both reviewed
  endpoints; its inactivity at every earlier step was not certified.

Read `../transport_review/REVIEW.md` and its run records for the independent
review. `DERIVATION.md` states the action floor, within-domain turning-point
scope, Markov/locality issue and interpretation of every closure.

## Provenance and retained failures

Every job has a prior contract and a fresh v2 manifest with exact before/after
input hashes, wall<=240 s, CPU<=235 s, one numerical thread and measured RSS.
`RUN_INDEX.json` lists all records and their interpretation; `BASE_INPUTS.json`
collects the exact external input ancestry. `inputs_historical/archive_map.json`
links preserved failed source bytes to their manifest hashes.

Preserved failures include the initial global-minimum/local-well selection
bug; two JSON bool serialization attempts; an artificial instant-minimum-mass
cusp/separatrix; the first phase splitter's scalar-pole factor-of-four error;
loss of small energy differences in an older harmonic period calculation;
two normalization harness errors; a normalization refinement assertion that
correctly demanded the later 256-cell control; and the 240-second full BW
resource limit. A runner `completed` record with the wrong pole splitter is
explicitly excluded from pole-resolved evidence. No failed run is promoted to
successful cooling evidence.

The work is frozen at this scoped checkpoint after the final endpoint
quadrature/source diagnostics. Further work requires the actual gaugino
occupation/inverse/Pauli collision terms, neutral daughter distribution and
force, and a time-dependent resonance/memory treatment before a physical
capture/depletion/photino conclusion. No new portal, install or Git mutation
was introduced by this package.

## Final endpoint checks and named direct photino source

`run_hybrid_control_001` repeats the preferred saved endpoint, holding its
state fixed. Doubling angular nodes changes loss/H by 3.16e-8 relative;
doubling phase nodes per interval changes it by 7.05e-5. The action derivative
repeat also passes. This is endpoint rate convergence, not full abundance
convergence.

`run_source_diagnostic_001` computes the explicitly requested named conversion
source estimate. The numerical initial yield is 3.67019626553e-7; multiplying
by .258429212504 gauge emissions/carrier and the massless-Casimir U1 fraction
1/6 gives Ychi=1.58080988440e-8. At mchi=104.730749522 keV this is .00376271 of
the reference DM rest density, or .3763%. This is only the named F<->S+gaugino
conversion source in the conditional empty-daughter history, not an upper
bound on every neutral cascade or loop source and not a final momentum
prediction. The gaugino energy ledger was not used as a particle count.

At the saved endpoint the charged scalar mass is 77459.666924 GeV, so the
10%-DM yield allowance is 5.68037557444e-16. The recorded charged yield is
1109.59 times this allowance. The coordinator's separate
`../gravity_resonance/run_continuation002/result.json` then grants the
shape-independent fixed-matrix maximum cross section permanently at all
future velocities in radiation domination. It obtains future yield floors
1.2279e-13 (216.16 times the allowance) for vacuum widths and 2.3729e-14
(41.77 times the allowance) for the all-FFS-blocked bosonic-width extreme.
This closes the selected late fixed-pole channel after this hybrid endpoint;
it does not close other channels, histories, correlations, medium currents
or the full weak-branch physical research goal.
