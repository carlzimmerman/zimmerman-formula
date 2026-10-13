# Colored-bath checkpoint handoff

Status: original cold-energy mechanism OPEN. Owned scope:
sol61_push/colored_bath_2026_10_13/. Starting shared revision
45cd126e7489ec6703c9c6650cbbeda227f28f13. Publication parent
ee12ad4fb672cb3564083f58d4982c4eaed42058 on codex/cold-energy-equations.

New evidence: single-notch filter leaves third-harmonic diffusion. The explicit
delayed OU difference kills all orbital harmonics and gives second-order D~q^2
at a chosen non-isochronous orbit. External divergence-form drift still fails
to select the target. A separately prescribed quadratic-diffusion toy selector
has finite added power c_*Q/6. Time-domain finite variance remains nonzero.
Nonlinear trajectories cross the fixed bare-energy cutoff in about 90% of
sampled near-edge cases, with coupled timestep consistency checks.

These are externally prescribed-bath assumptions, not consequences established
from the carrier Lagrangian. No Lambda-CDM/MOND premises. No new empirical data.
Report contains exact covariance, normalization, closure derivation, limitations,
and source attribution. Do not promote a leading-order diffusion zero to an
all-orders barrier, or a bare-energy crossing to permanent geometric escape.

Eight Lean theorems certify spectral nonnegativity, matched harmonic phase and
zero, finite sum zero, target/unselected currents, log drift and conditional
mean-power algebra. They do not certify stochastic averaging, infinite-series
limits, process boundary classification or the carrier action.

Executed routes: fundamental-only notch fails; all-harmonic delay succeeds as
a leading-order filter but not a selector; nonlinear hard-wall interpretation
fails in the finite tested family. Open continuations: derive reciprocal drift
and covariance from the same carrier coupling; derive an actual boundary or a
uniform finite-amplitude treatment; address L-dependent synchronization. The
missing input is a microscopic interaction/state selecting these quantities,
not another arbitrary delay fit. Self-review only.

Reproduction: use contract JSON argv and the computation-audit runner. Numerical
script uses Python3 NumPy/SciPy; Lean driver uses Python3.11 and the existing
fable_independent_2026/lean_2026 Lake environment. See three run manifests for
actual execution bases, full inputs, caps and output hashes. No unrelated files
or shared Git index were changed.

Hashes:
- check.py: SHA256 `3e94c295c8009562d1e9856cec853243885de21cd05eccf674cc3a6f56310e45`
- trajectories.py: SHA256 `f1c28c9ec00077b87429a91c7f57b7f3a37044119af9ddfab696da5df74cc4cf`
- ColoredBath.lean: SHA256 `2c8b7c9bc566872d8e569cd1f8b32de3b543f779d500940065bd09cc61071fec`
- run/manifest.json: SHA256 `85a793c03e06d362c40fb228482edec59e3f35d9bfafe626e00031224ae94dab`
- lean_run/manifest.json: SHA256 `63d90041277ffe89c2113ec6c983199f21643144d37ccbb6c6b9a68b4674982d`
- trajectory_run/manifest.json: SHA256 `c3fb76dcf3c3a0a7d8b589546db80b2c9fbcab3d103ce85ccb30726dab27d3be`
