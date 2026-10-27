# Continue from the pump, not from an assigned release

Read STATUS.md, MECHANISM.md and SELF_REVIEW.md first. The older
selective_stress_2026_10_25/HANDOFF.md contains the preceding research and dead
ends. Do not repeat its frozen-profile outlet tests or entropy scans.

The actual static model still supplies a conditional finite-radius branch
with a filled profile, unconverted exterior and a sub-percent law residual.
This phase shows why that is not yet formation: the natural slow source and
its forced tangent front receive negligible radiative/mode energy on the
tested density curve. Most release stays in infall kinetic energy.

Two exact facts to retain:

* g partial_mu chi j_T^mu has no bulk scalar source where j_T is conserved.
* A passive outlet cannot manufacture input energy for the linear front; the
  parameter-dependent norm bound states the exact assumptions.

The next full test must allow material density and phases to evolve, derive
Gamma from their continuity equations, and retain the connection force from
spatially varying chi. In particular, the infall port and changing source
shape must be present in the energy ledger. A test of nonlinear feedback must
not be described as covered by the single-port theorem.

The endpoint-interpolation lambda coordinate is deliberately restricted and
its transport inertia grows sharply near lambda=1. Do not extrapolate through
that endpoint or infer a general formation-time bound from it. For an actual
attractor test release this density restriction, the locked phase profile and
the alignment-only kinetic closure. Seed formation from the known unstable
all-F phase mode; lambda=1/16 rest data omit that initial stage.

Potential new operators that directly respond to compression would need their
own canonical completion, static-limit and reservoir checks. A derivative
coupling to another conserved current is still a boundary term. A slow,
compact scalar source must also face the existing SS-05 induced-inertia/rate
bound; naming compression does not evade it. No new coefficient or density
gate was fitted in this phase.

## Runs and reproduction

All five bounded runs completed and their manifests validate against current
inputs. Keep their scripts, contracts and outputs immutable. Reproduction
requires a fresh output directory in each command:

```
python3 physical_completion_2026_10_25/launch.py front_dynamics_2026_10_25/branch_contract.json NEW_RUN front_dynamics_2026_10_25/branch_test.py 300
python3 physical_completion_2026_10_25/launch.py front_dynamics_2026_10_25/branch_checked_contract.json NEW_RUN front_dynamics_2026_10_25/branch_checked.py 300
python3 physical_completion_2026_10_25/launch.py front_dynamics_2026_10_25/forced_front_contract.json NEW_RUN front_dynamics_2026_10_25/forced_front.py 300
python3 physical_completion_2026_10_25/launch.py front_dynamics_2026_10_25/geometry_contract.json NEW_RUN front_dynamics_2026_10_25/geometry_audit.py 300
python3 physical_completion_2026_10_25/launch.py front_dynamics_2026_10_25/forced_checked_contract.json NEW_RUN front_dynamics_2026_10_25/forced_checked.py 300
```

The scripts reading another run use its recorded original result path; do not
overwrite that path during reproduction. Change dependencies only in a new
script/contract if rerouting a complete reproduction chain.

The phase started with observed HEAD
84c0302c22c9e371ed7116d0d2996c806d15ae7b. Other work advanced HEAD during this
phase; manifests record their own observations and input hashes. No index,
unrelated tracked file, inherited research file, commit or remote was changed
by this phase. These new research files are local.
