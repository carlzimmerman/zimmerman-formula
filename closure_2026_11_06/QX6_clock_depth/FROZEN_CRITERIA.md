# QX6 frozen criteria: derive QX5's clock-depth boost F(Q-1) from the action, with no cluster input

Frozen before any QX6 script exists. Rules: closure_2026_11_06/SWARM_BRIEF.md (binding). Kappa = 1/2 FITTED; not
theory closed. Adopts nothing. No dark-matter particle. No LCDM inputs.

## Why

QX5 (00f9e19c9b, 8912072109) left one cluster lead. Class a is a phantom multiplier F keyed on the khronon clock
depth k = Q - 1 = |Phi|/c^2. It passes X-COP (+0.016/0.079) and groups only when X-COP sets F's threshold and
amplitude (F_req median 4.09 canonical / 3.66 alt). Galaxy keys are <= 4.6e-6, X-COP keys 4.5e-5 to 1.2e-4. Coma's
UDGs need F 22-26. QX6 asks whether the action fixes F, with threshold and amplitude from record constants
{a0, rho_DE, kappa, Lstar, mu_K, c, G} and no cluster input. Three routes, one iteration each (iter_*/).

## Data and machinery (reused, not rebuilt)

QX5's builders are executed from qx5.py's own source, up to its class loop: X-COP 35 points (gate G-X:
|mean Delta| <= 0.05 and rms <= 0.10), SPARC, 7 ellipticals, KiDS lensing, 20 Lovisari groups, and the key-a
construction. QX2's psi profile (potential of the measured HSE mass) serves the K(Q) term. Both footings, never
pooled: canonical a0 9.3603e-11, Lstar 21.7 pc; alt a0 1.1312e-10, Lstar 22.9 pc.

## Labels (per route)

- DERIVED-PASS: F follows from the action's own static equation, with every constant fixed by a non-cluster
  observable already on the record. It must pass G-X on both footings, the groups gate (QX5's bracket rule),
  and QX5's galaxy rechecks (SPARC rms +<= 0.01, mean +-0.02; ellipticals mean +-0.15; lensing mean +-0.05).
  Coma UDGs are reported against QX5 a2's line.
- DEAD: the derived F fails a gate for every value of its constants allowed by the route's derivation,
  or the route gives F - 1 too small by a stated factor.
- CLUSTER-SET: passes only if a constant is set from clusters. That is a FAIL under the no-tuning rule.
- COINCIDENCE (never PASS): a dimensionless group from record constants happens to land where clusters need it,
  with no term in the action that produces it. Reported with the trial count, as a lead only.

Door rule: clusters stay FAIL unless some route is DERIVED-PASS.

## Controls and Lean

Each iteration has a MUTATE that must bite (stated per iteration), written to separate outputs. Lean:
fable_independent_2026/lean_2026/QX6_clock_depth.lean plus a _MUTATE twin, 0 sorry, standard axioms, with .out
files saved. It certifies route 2's bound, route 1's window logic, and route 3's window membership arithmetic.

## Scope

Statics, spherical symmetry, hydrostatic masses, and the phantom-multiplier or extra-density form. Lensing =
dynamics, the Bullet-type offset and growth are owed for any survivor. Cassini/PPN: a phantom multiplier is
harmless for F <= 4.8e7 (C6P). For route 1's density form, the Sun is checked explicitly (iter_1).
