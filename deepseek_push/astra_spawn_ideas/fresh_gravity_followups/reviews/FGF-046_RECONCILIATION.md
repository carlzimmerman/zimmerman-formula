# FGF046: constructed classical fluid branch and a localized continuation result

Accepted local analytic construction for the EXACT C1,1 polynomial data in the
same fixed Q potential, with independently checked derivative-limit and domain
arguments. This supplies the existence missing from FGF045's upper-time theorem.
For each sufficiently large N there is a positive C1 fluid solution on the
regular patch for at least k N^-4, k>0 depending on fixed physical data.
No PDE existence theorem or external mechanism supplies the construction.

Invariants r=v+cs log(n/nref), s=v-cs log(n/nref) solve two transport equations
with speeds (r+s)/2±cs and source -g0. Freeze the previous iterate's velocities,
construct its characteristic flows, and integrate the new state. Uniform first
derivative bounds make this a C0 contraction. Uniform spatial Lipschitz bounds
for those derivatives plus the explicit estimate
||d_x||inf <= 2 sqrt(2 H ||d||inf) promote convergence to C1; the PDE then
identifies the continuous time derivative. Both original fluid equations and
exact initial traces hold. Positive density follows from the exponential map.

Initial first derivatives scale as N4 and their Lipschitz seminorm as N7.
The latter is retained, not incorrectly treated as fixed, but does not force
a smaller lower-time power: the second-derivative envelope closes linearly
with the same N^-4 time gate. Finite characteristic speed, causal cones and
local uniqueness prove independence from arbitrary auxiliary exterior choices
on their common physical domain. The original compact profile is not smoothed.
The energy law is now valid for an actual constructed solution, with interaction
and pressure work; moving boundaries retain their terms. Hydrostatic zero
velocity is the exact control. Frozen gravity still has C(n-rho) source residual.

The AUTHOR's sufficient continuation gate retains positive state, first-derivative
and gradient-Lipschitz bounds on a buffered interior patch. Its trace/restart
proof is accepted in exactly that scope. It does not classify every earlier
endpoint using first derivatives alone. The independent reviewer reconstructs
the same conservative local statement, with its own frozen derivation.

A SEPARATE ROOT result uses a hydrostatic auxiliary extension of the background
on the line. It derives Q(t) <= [Q(0)+F2 t] exp(3 integral P), where P bounds
first derivatives and Q their Lipschitz seminorm. The root-only auditor checks
this by comparing gradient ODEs along two characteristics, avoiding a hidden
C2 assumption. Thus bounded first derivatives supply the higher-norm restart
gate for this auxiliary branch. Invariant bounds control amplitudes and keep
density finite and positive for each fixed N. Finite propagation keeps its
compact disturbance inside the original regular patch up to the old upper time;
outside it the hydrostatic state is unchanged. Its unique maximal classical
branch has lower and upper lifespan bounds of order N^-4, and an unbounded
limsup of first derivatives at its finite endpoint. This is a localized
first-gradient result for that specified construction, not a theorem for any
unbuffered cone endpoint, a jump shock profile, or a post-breakdown solution.

The root extension is hydrostatic by construction; the author's independent
extension need only match on the physical patch. Agreement follows by local
uniqueness where both exist. The root's private route preceded an author preview,
but its FILE freeze followed that preview; no fully blinded root freeze is
claimed. The separate root auditor read no new author/reviewer proof. These
provenance limits are preserved rather than treating three actors as a proof.
The load-bearing evidence is the explicit iteration, interpolation, gradient
comparison, continuation and localization arguments. Both audits are scoped.

The remaining central gap is actual field response: fluid energy conservation
in a frozen potential does not make its changed-density MOND source vanish.
FGF047 therefore changes to the full diagnostic Q/scale/fluid evolution on a
regular positive-gradient patch, with compatibility constraints and full energy.
It is a ready specification, not a launched run; no new fixed-force lifespan
sweep is needed. No result here covers the zero-gradient crossing.

Both a0 normalizations and constant-vacuum/frozen-H/evolving-H histories remain
separate. Signed Q and its source are not substituted for RAR/M/filtered MONO.
This compressive nonrelativistic fluid family neither refutes the core framework
nor proves physical stability, a conserved physical vacuum-scale sector,
metric/photon/DOF closure, calibrated observations or historical novelty.
Proof-only, zero mathematical executable computations or observational runs.

## Evidence pins

- `campaign_fresh_gravity_astra/stage_33/independent_audit/AUTHOR_EXPOSURE.json` SHA256 `4d769490ac92dc3ce06aa7ff73db6a0af6083f1da3c809c409fd0e0e1c4f35fb`.
- `campaign_fresh_gravity_astra/stage_33/independent_audit/DERIVATION_FROZEN.json` SHA256 `33fae0591fdb572995d120db5f2e3e75c1118fefd805606e9c6979c3df4a171f`.
- `campaign_fresh_gravity_astra/stage_33/independent_audit/FROZEN_DERIVATION.md` SHA256 `c29434e8abbabc2034833a1d4936cb804fef6467fd51c31d42c964bbb88c2d62`.
- `campaign_fresh_gravity_astra/stage_33/independent_audit/INDEPENDENT_AUDIT.md` SHA256 `ae3487b053df58d03744825a96448ec00636f5f82a6217523cd0daf9b0f798a9`.
- `campaign_fresh_gravity_astra/stage_33/independent_audit/audit_result.json` SHA256 `57e685ac09363c3fb9d80d86546ae4511db68b827b1169d9c9442ccd73991db7`.
- `campaign_fresh_gravity_astra/stage_33/local_existence/INDEPENDENT_AUDIT.md` SHA256 `8de5befb76119de458bc9b5f7753d251fbb68860f419b41e7c7d15a611b5cea3`.
- `campaign_fresh_gravity_astra/stage_33/local_existence/PROOF_COMPARISON.json` SHA256 `f3d778b8fe66924d8a54e85267e5582c97f194ec43ad68c25da134875b4d5c90`.
- `campaign_fresh_gravity_astra/stage_33/local_existence/PROOF_RECORD.json` SHA256 `7d95ef893f5c32524edf5282699c8c43673301496a97492fba820d2d56183bf5`.
- `campaign_fresh_gravity_astra/stage_33/local_existence/ROOT_DERIVATION.md` SHA256 `79bb774b90b1dd381ad65836a380c775307e69ad6b3202ac985cf1691db01037`.
- `campaign_fresh_gravity_astra/stage_33/local_existence/audit_result.json` SHA256 `af45f66d5ece9d8d1afb2884a96dae130c954b183e4b4ba877c51a8b5f36fb64`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-046/fgf046_run_001/DERIVATION.md` SHA256 `60fe268cf837456527205f8f3a8337646c5cc8eaf6560446d2ec0b3805a075e1`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-046/fgf046_run_001/REPORT.md` SHA256 `f6b4d193fb25a660589908a59711583367734561caf8741da1c80b85faca8b75`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-046/fgf046_run_001/input_sha256.json` SHA256 `6db42cf17f7ffef92eca249d089a05dc832c2fd305e2230308ccfe9c33fecded`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-046/fgf046_run_001/result.json` SHA256 `8ed09eb44ace4214dffe87a7c396a43a8b12a80c5b751c7a1495dee785b610f1`.

Reconciled 2026-10-06T02:47:25.553040+00:00.
