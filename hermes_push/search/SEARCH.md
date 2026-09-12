# The parameter-space search (autoflow for a local model)

## What this is
The method that works on hard equations: **parameterise the unknown object, define a residual that vanishes exactly when the target
property holds, drive it down with a global optimiser, then certify what the optimiser found.** The numerics locate a candidate; the
certificate is what makes it a result. Here the unknown object is the coefficient history of the cuscuton-clock MOND action, and the
residual is the total violation of the gates in `objective.py`.

## Why this target
`fable_independent_2026/L192` established gradient-driven criticality: the clock-scalar sound speed rises monotonically with the
background field gradient and crosses zero at a unique Y*, which is a two-sided attractor whose state is **exactly pressureless dust**.
That attractor exists wherever the clock runs faster than proper time (s0 > 1). So a coefficient history with s0 > 1 at every epoch is
driven to exact dust by its own MOND sector, with no tuning of the logarithm margin — which is what the necessity certificate demands.
The search is for such a history that is also a consistent dark sector of the right amount.

## Run it
```
python3 hermes_push/search/run_search.py --iters 400 --seed 1
python3 hermes_push/search/run_search.py --iters 400 --seed 2      # different seeds are different searches; run several
```
Each run writes `hermes_push/search/best.json` (loss, per-gate breakdown, parameters). Cheap: no network, no data files, seconds to
minutes. Vary `--seed` and `--popsize`; a small local model can run dozens of these unattended.

## Read it honestly
- Report the **per-gate breakdown**, never just the loss. "loss 0.42, dominated by `dust`" is information; "loss 0.42" is not.
- A search that stalls above zero is a **result**: it says which gate resists and by how much. Write it up as an H-entry.
- Never edit a threshold in `objective.py` to make a candidate pass. To extend the search, add a term to `history()` or a new gate —
  and if you add a gate, add it as a computed violation, never as a boolean.
- A loss below 1e-9 means every gate is met by the parameterised history. That is **not** a theory: escalate it —
  (1) recompute the gates from the full background ODE rather than the power-law ansatz,
  (2) check the forest tracking precision (L192 V6 requires the gradient to track Y* to about 1e-6),
  (3) check the gates this objective does not contain (CMB, lensing, PPN, N_eff),
  (4) write the H-entry, then attack it.

## The gates now in the objective
`domain` margin positive · `kinetic` no ghost (m_rel < 2) · `criticality` s0 > 1 so the attractor exists · `reachable` the marginal
gradient Y* is finite and below a tenth of the transition scale · `dust` the sector redshifts as a^-3 · `amount` it is the right share
of the critical density today · `monotone` its density falls with time.

Missing on purpose, because they need the full machinery and belong to the escalation step: the CMB acoustic peaks, galaxy-galaxy
lensing, PPN, BBN, and the forest tracking precision. Do not claim any of them from this objective.
