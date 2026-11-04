# CC11 energy live checkpoint

Owner scope is `energy/` only. No prior source or integration file was edited.
The derivation and finite controls are in `DERIVATION.md`. All experiment
source versions remain immutable after their first recorded execution.

The constructive method splits expansion and collision, uses the same actual
particle increment to determine the collision endpoint action on a constant
Hamiltonian surface, and iterates the collision geometry at midpoint **action**
and populations. Independent Simpson FRW work is computed from the physical
stress-energy, not from the energy change. The overall BE-based state method
is first-order and requires time refinement.

Promoted local evidence:

* The old one-step coupling's energy defect is reproduced; the split passes
  an independent work check at roughly 3e-10 of excitation.
* The small-action moving-minimum obstruction is diagnosed and corrected.
  Mid-action stage excess falls from .473% to 3.73e-7 relative under the
  tested refinement, with no action floor or accepted clipping.
* Previous-outer Newton guesses reproduce the unseeded physical root.
* Exactly zero physical daughter tests pass an independent high-precision
  reference; guesses are not physical initial populations.
* Fresh N=0 first-step test now passes using four hierarchy passes for the
  Newton guess, with independent energy error 5.02e-10 of excitation.

Current new source is `split_energy_v7.py`, backed by `hybrid_number_v4.py`
and `seeded_number_v3.py`. It is injected with a common orbit model and
physical-number operator factory, so no 25-species assumption is imposed.
The new 30-group common vector model must retain its supplied bosonic eta.

Completed fresh benchmarks:

* `run_fresh_coarse002` through `run_fresh_coarse006`: clean original N=0
  packet, nominal max dN=1e-4, target N=.0021690179772784167 reached.
  Source `fresh_history_v4.py`, unchanged throughout the matched prefix.
  Final J=2.12177629116e-6 and Ycharged=3.03795083398e-7. Independent work
  residual is 3.5985e-7 of orbital excitation, versus the old preferred
  23.85% result. All five endpoint checks pass.

* `run_fresh_fine002` through `run_fresh_fine007`: same original N=0
  input and target, nominal max dN=5e-5. Final J=2.22418570094e-6,
  Ycharged=3.03677916615e-7 and independent work error 1.16579e-7 of
  orbital excitation. All endpoint checks pass.
* `run_benchmark001` checks and consolidates both full ancestries. Action
  changes +4.8266% under refinement, U1 yield -1.7141%, charged yield
  -.03857%, and mean U1 momentum -1.3100%. Ledger closure does not imply
  1% state accuracy.

Terminal midpoint experiment:

* `run_midpoint001`: resource-limited before an actual dN=5e-5 endpoint.
* `run_midpoint002`: reduced interval 1e-6; complete 1/2 substep cases, but
  four-substep case exhausts its 50s budget after 3 substeps and its third
  residual exceeds the 1e-12 diagnostic target. No order claim or promotion.
  Both known stiff linear-decay sign/rejection tests pass.
* No energy-package jobs remain active. The accepted reference is v7 BE.

The histories save full state after every accepted step and are bounded at
240 wall/235 CPU seconds. Earlier `run_fresh_*001` attempts are valid
partial matched-energy prefixes but wasted time on the all-seed log guess;
they are not the promoted fresh histories. Initial-step failures and trace
records are preserved as numerical failures, not physical exclusions.

Optional `split_energy_v8.py` checks final true midpoint geometry explicitly
and uses Anderson iteration guesses. Its two equivalence controls pass, but
a runtime improvement was not demonstrated; the benchmark stays on v7.

The fresh energy obligation is met in both finite discretizations.
Population/action time accuracy is distinct from ledger closure: common-N
coarse/fine action differences remain at percent scale. The inherited
J<J_initial*1e-7 branch is explicitly a harmonic-geometry approximation,
not an action floor. No cold-matter viability claim is made.
