# CC10 statistics checkpoint

The missing one-body quantum conversion operator is constructed and executed.
It has actual leading projected F/C/gaugino group widths, physical spin
degeneracies, simultaneous Bose/Pauli factors and inverse conversions,
momentum recoil, massive gaugino energies, and an exact finite event energy
identity. This closes the operator-construction obligation for the declared
isotropic factorized entropy projection. It does not close the original
vacuum/charged-relic/photino history or establish continuum convergence of
all cascade channels. The coordinator owns common field feedback.

`quantum.py` is immutable after `run_local001`, and is shared with the cascade
agent. `quantum_v2.py` imports it and adds event-local implicit scalar-extent
sweeps for extreme soft-bath stiffness. It is likewise preserved after its
recorded executions. `ReactionEvents` and `conversion_events` are the reusable
APIs; `DERIVATION.md` gives the finite measure, quantum equilibrium, H theorem,
charge lift, varying-background energy/force and approximation boundaries.

## Completed finite computations

* `run_local001`: x=2,5,25.4000254000381, equilibrium perturbations evolved
  30 inverse maximal group widths. All checks pass. Event thermal balance
  <1e-12; energy/carrier/extra fixed-ordering invariant drifts <=3e-16;
  final relative equilibrium L1 <=2.8e-6, with positive, Pauli-bounded states
  and increasing entropy.
* `run_empty001`: global constrained Newton handles x=5 in 97 steps, with
  1e-16 invariant drift, but the x=25.4 soft empty bath hits the 240 s bound.
  Status is **timeout**, no complete result file. Its source, stdout and v2
  failure record are preserved. This is solver-resource inconclusiveness.
* `run_empty002`: exact empty C/gaugino bath and physical frozen FD F, at
  x=5 and 25.4,Tc=.004, evolved one inverse maximal partial width with
  symmetric event-local implicit extents. All invariants and quantum-domain
  checks pass. The coarse momentum grid overestimates the later U1 yield;
  use the next refined checkpoint for that observable.
* `run_refine001`: x=25.4,Tc=.004,z=Gamma_max tau=1; soft 16/32/64 nodes
  and common hard 40 nodes, six angular nodes. At soft 64, halving z step
  .025->.0125 changes U1 yield .410% and mean momentum .0553%; soft
  32->64 changes them -.566% and .0326%. Finest Y_U1=2.3318134e-10,
  mean p/mu=.0010653651, maximum gaugino occupation .99720. All energy,
  carrier, entropy and quantum-bound checks pass. Initial quadrature number
  normalization is explicitly stored; it is not silently replaced by an
  analytic continuum number. This is a fixed-background prepared-bath test,
  not a yield prediction for the recorded cosmology.
* `run_soft001`: actual FD-weighted massive two-body birth measure, 160
  parent radial nodes, 96 angular nodes, q_parent<=60, and resolved soft
  daughter histogram q=1e-12..100. Near the U1 threshold, histogram filling
  rates can exceed omega by 10^6 while the absolute birth rate per original
  carrier/H is only 10^-12. At offset dx=1e-4 all-group birth/H is
  6.74e-7, mostly q<1e-4; at dx=1e-3 the sub-q1e-4 component is 4.78e-6/H.
  These are sampled FD-weighted rates, not a uniform crossing integral or
  a continuum supremum of df/dtau. The reference T/omega comes from the
  **first saved row beyond** the threshold, N=.0201592; its inner turning
  point is already above threshold. No actual crossing dwell time is claimed.
* `run_cascade_compare001`: actual frozen cascade `network.py`/`reaction.py`,
  all 25 groups, current-projected lowest conversion replacements, x=3,5,
  Tc=.004. GL8 on five panels gives 40 positive q²dq nodes, six angles,
  physical F-only FD initial state, 20 B3 lifetimes. Full quantum and
  classical availability=1 operators both retain inverses. At x=3, quantum
  U1 yield is 8.88% below classical and mean momentum 4.22% higher; at x=5
  yield is 18.85% lower and mean momentum 6.86% higher. Classical x=5
  U1 occupation reaches 1.142; quantum reaches .506. Charged fractions are
  .79619/.80078 at x=3 and .80260/.80040 at x=5 (quantum/classical).
  Neutral force differs about 2%; massive neutral energy differs -3.61%
  at x=5. Energy drifts stay below 8e-15. BDF accepted populations have
  tiny negative tails at about 1e-12 (classical about 6e-11); positivity here
  is numerical to the declared 1e-7 tolerance, unlike the constrained extent
  solver's domain construction. Independent entropy chain-rule residual is
  <1.2e-14. Occupied-forward omitted measure is zero on the sampled graph;
  this does not bound inverse production through omitted external states.
* `run_cascade_compare002`: controlled radial increase GL40->60 at the same
  six angles. At x=3 the quantum/classical yields change -2.78%/-2.88%,
  leaving quantum/classical ratio .912176; at x=5 they change +.200%/-.147%,
  leaving ratio .814342. Mean momentum ratios are 1.04258 and 1.06764.
  Neutral-force radial shifts stay below .9%. The earlier classical x=5
  occupation maximum 1.142 is **not radially robust**: refined maximum is
  .916 (quantum .480). Only the group-integrated statistical suppression is
  stable at the tested precision; a claimed classical Pauli violation is
  not promoted. All declared checks pass. This is a single radial control,
  not a continuum extrapolation or angular convergence certificate.

The standalone conversion initial recorded orbit is exactly null: its outer
turning point is below the F->C threshold, and C=lambda=0. The supplied cold
endpoints do not store a gaugino bath. They cannot supply a nontrivial actual
conversion replay without earlier cascade/bath populations. The cascade agent
has separately advanced the common direct field/population history and is
refining it; those results are not reproduced as statistics-owned histories.

## Open dependencies and resumption

Use the actual cascade/field state and orbital time samples for a statistical
replay or common evolution. Do not infer that every light-gaugino bin is slow
from a number-averaged charged Gamma/omega. Ultra-soft high occupation and
absolute birth density are separate quantities. Refine the observables that
matter (group yields, momenta, force), not only a total-number norm dominated
by charged particles. Later Tc~1e-6 can require comoving daughter q~40000,
so qmax80 is unsuitable there without an adaptive hard tail and weighted
omission audit. Phase averaging, nonlocal resonance response, singlet density
matrices, vectors/2<->2 channels, and finite heavy-pole matching remain named
physical limitations. No combined DM/DE/relic success is claimed.

## Contract wording audit

Some descendant contract JSONs inherited a descriptive `mathematics.inputs`
string mentioning the local-equilibrium example T=.007 and fixed Tc=.004.
That string applies to `run_local001` only. The actual comparison equilibrium
audit uses T=.008; `run_soft001` obtains Tc=.004564311566 from its hashed
recorded history input. Their actual run code, exact input hashes, outputs,
and more specific assertion/bounds fix these parameters. Original contracts
are preserved; this correction does not alter a numeric source or result.
