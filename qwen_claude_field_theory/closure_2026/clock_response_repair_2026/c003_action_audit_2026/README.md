# Closure checkpoint: action, recoil, orbits, and unchanged initial data

Latest continuation: [Claude L191/L192 action audit](CLAUDE_L191_L192_REVIEW.md)
adds an anisotropic principal-symbol obstruction, metric-stress tests,
gradient-tracking identity and nine scoped Lean lemmas. The checkpoint below
records the earlier L189/C003 work, not certification of those later claims.

**Full theory: OPEN. No complete relativistic MOND theory or law-of-nature
certificate is claimed.** The literal recoil bookkeeping and several tested
realizations fail; this is not a no-go for every clock-based theory.

Audited source checkpoint: `1f0306787`, Claude/Fable L189 and Hermes C003.
Executions began after unrelated commit `5a87447af`; manifests pin each actual
execution HEAD and input hashes. No existing Fable/Hermes source, MOND kernel,
global a0, or coefficient function was changed. Carl's non-particle primordial
clock preference remains the construction target; particle-decay language in
C003 is an audited proposal, not an accepted replacement for that target.

## What changed mathematically

| Route | Executed discriminator | Strongest justified conclusion |
|---|---|---|
| [Action and trigger](ACTION_GATES.md) | Dust-action variation; angular kick moments; clock integrability | Unextended pressureless dust cannot realize nonzero isotropic heating; clock-frame speed is not automatically multistream dispersion |
| [Relativistic recoil](recoil/RECOIL_AUDIT.md) | Exact mass shells, numerical invariants, five Lean lemmas | At 650 km/s massless decay loses 0.21658% rest mass per event; conditional Poisson mean loss is 0.49858%, not the quoted quadratic proxy |
| [Actual orbits](orbits/REPORT.md) | Stationary fixed-NFW tracers, vector kicks, two seeds, timestep refinement | Cluster retention 0.80276 +/- 0.01280 and 0.77891 +/- 0.01249 exceeds the registered 0.70 ceiling in this surrogate |
| [Unchanged action](../fixed_action_initial_data_2026/REPORT.md) | 54 initial-data tuples, two root grids, forward/backward histories | 186 roots; 60 pass local screens. Of 30 positive-q histories, 27 fail backward and three fail forward after resolved follow-up. No exhaustive exclusion |
| [Slow clock excitation](medium_emission/REPORT.md) | Energy/momentum support and six Lean lemmas | Without internal release, positive-energy emission causes drag. With release, cold shutoff and isotropic fixed recoil do not follow from kinematics |

The orbit follow-up uses Hermes' spiral ceiling 0.15, not L189's stricter 0.105;
neither a point-estimate gate nor a Newtonian NFW surrogate establishes observed
lensing. No quoted forest/S8 proxy is upgraded to an observational likelihood.

The three distinct early histories can be continued backward to `ln a=-2.3`
with a positive computed scalar diagnostic, but the radiation fraction is only
0.2605 and conditioning is severe. They are not certified radiation-era/CMB
solutions. Forward refinement brackets a resolved negative-gradient crossing
in `ln a=[0.25,0.2625]`. Conserved-charge ratios distinguish these histories
from a relabeling of the old branch. Negative-q symmetry is not assumed exact:
one counterpart was explicitly checked.

## First-principles implication that survives the audits

In the stipulated nonrelativistic emission model, let `q>0` be outgoing
excitation momentum, `c_s>0` its propagation speed, and `Delta` the released
internal energy. Energy balance gives

\[
 \boxed{\Delta K=\Delta-c_s q.}
\]

Thus a passive emission-only clock medium cannot supply the heating invoked
to deplete galaxies. An actual interaction must supply a reservoir or energy
transfer and derive the recoil statistics. With fixed internal release and
fixed recoil magnitude, energy conservation also restricts the angle for a
moving element; isotropy conditional on its velocity cannot be assigned.
Absorption, externally pumped states, scattering and additional medium recoil
are not excluded by this restricted result. No novelty claim is made for
ordinary conservation algebra.

For the original massless relativistic realization the exact result is

\[
 \frac{m}{M}=\sqrt{\frac{1-v_k/c}{1+v_k/c}},\qquad
 \frac{\langle M_N\rangle}{M_0}
 =\exp\left[n\left(\frac mM-1\right)\right].
\]

The latter assumes an equal-fraction mass ladder and a Poisson event count.
It does not determine the global cosmological energy budget without exposure
and emitted-component stress accounting.

## Lean and verification boundary

There are **18 compiled algebraic lemmas**: seven in `ClockMoments.lean`, five
in `recoil/RecoilAccounting.lean`, six in `medium_emission/MediumEmission.lean`.
The proofs use only standard Mathlib foundations (`propext`, `Classical.choice`,
`Quot.sound`), not custom axioms or `sorryAx`. They do not formalize the full
action variation, Dirac closure, PDE existence, numerical integrations,
empirical likelihood, or the proposition that this is nature's gravity law.

The main agent reran 35 existing cosmological-bridge tests and nine new narrow
tests; all passed. Twenty orbit invariant/convergence checks also passed.
Scientific failures are explicitly stored separately from successful program
exit codes. Every new executable was run. Contracts, raw results, commands,
source/output hashes and failures remain in the linked run records.

A fresh read-only reviewer independently compiled all three Lean files,
checked dust and recoil algebra, reconstructed all 186 initial roots, recomputed
the initial/final spectra of the eight early continuations, and reran orbit
invariants plus the angle test. It did not rerun all orbit trajectories or
rederive the inherited complete perturbation action. Two review corrections
were applied: execution HEAD versus source baseline, and removing language
that turned observed timestep agreement into a rigorous error bound. Medium
documentation was also corrected concerning display precision and finite
emission jumps below threshold.

## One next action-level target, not a coefficient reconstruction

Specify an interaction involving the existing classical clock/medium fields,
then vary that action and derive its conserved stress and momentum-transfer
correlator. It must decide all of the following before another fitted kick
scan is useful:

1. Which positive-energy internal/background reservoir supplies heating?
2. Why does the transition amplitude vanish in cold cosmological flow yet act
   in the required halo states? A step function of relative speed is not a
   derivation, and local expansion is not automatically the background Hubble
   rate.
3. What drag, recoil-angle distribution, pressure and anisotropic stress come
   from that same interaction?
4. What propagating modes and constraints does it add or alter?

Then evolve its derived metric-plus-medium force self-consistently with the
fixed exponential law, global a0 and the actual observational apertures.
MOND, independent Phi/Psi, complete constraints and DOF, PPN, ordinary matter
Ward identity, tensor speed, zero modes, stability and cosmology must still
come from **that same action**. No first-principles derivation of kappa=1/2 has
been added here. Prescribed functions of a varied scalar can be covariant;
they do not automatically require adding new fields, but their form remains
to be physically explained and tested.

## Files, commands and outcomes

- This directory: action/trigger computation and tests, three Lean modules,
  recoil/medium/orbit computations, contracts, run evidence and reports.
- `../fixed_action_initial_data_2026/`: unchanged-action root/continuation
  computations, tests, diagnostics, contracts and seven evidence runs.
- [Main command index](COMMANDS.md), [recoil commands](recoil/RUNS.md),
  [medium commands](medium_emission/RUNS.md),
  [initial-data commands](../fixed_action_initial_data_2026/COMMANDS.md).
  Every bounded manifest stores exact argv and child exit status. The
  exploratory initial-data JSON is transient and not part of the commit.

Status labels: the erroneous quadratic rest-loss statement is **refuted**;
the fixed-NFW/C003 test and the sampled continued positive-q histories
**fail their specified gates**; general interacting-clock construction and
the requested complete theory remain **OPEN**.
