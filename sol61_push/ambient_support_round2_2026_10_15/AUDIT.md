# Audit scope and verdict

AS2-2026-10-15-01. **Correct only under the specified restrictions.** The new
results establish conditional equilibrium, finite mass, causal principal
bounds and positive quadratic energy in a defined comparison. They do not
close the physical theory, generate a new empirical pass or establish global
novelty.

## Dependency checks

| Implication | Evidence and verdict |
|---|---|
| Varied neutral current -> static hydrostatics | action/PROOF.md derives the first variation before imposing B_U=0. Correct for the stated action; neutrality does not remove quadratic frame couplings. |
| Actual self-gravitating exterior -> mass/envelope/error bounds | self_gravity/PROOF.md constructs the solution by a complete weighted contraction. Uniqueness is only in the displayed envelope; its threshold is a certificate threshold. |
| Exterior equilibrium -> stability | stability/REPORT.md retains the gravitational density term. Correct for the specified fixed impermeable inner boundary and small-self-gravity fluid sector. Movable constant-pressure support has an explicit negative trial direction. |
| Regular-core profile -> positive fluid density Hessian | regular_core/PROOF.md and independent stability/PLUMMER_CHECK.md derive the same all-angular kernel bound. Sufficient f<1/4; no converse mass-conserving instability follows. |
| Fluid and gauge/current positivity -> actual energy join | joint_audit/REPORT.md derives the constrained Hamiltonian and energy identity, including affine Gauss, eta=-div(rho xi), variable coefficients and source power. Correct for fixed external sources and the specified hybrid variational comparison. |
| Occupied-center patch -> preserved local cone and C2 action | patch/PROOF.md and patch/AUDIT.md derive the affine numerator, smooth convex blend, direct zero-field modes and regularity. This changes the magnetic constitutive input. |
| Patched occupied action -> vacuum/nonlinear completion | Does not follow. Two coefficient limits disagree toward vacuum; outgoing radiation can leave the dilute-tail gate. |
| These results -> original charged galaxy, formation, metric or empirical closure | Does not follow. Central sources and new neutral matter/EOS/normalization remain inputs; field/pressure metric gravity and dynamic charged-source terms are omitted. |

## Independent reconstruction and provenance

The stability agent reconstructed the Newtonian equations and boundary work,
then independently checked the regular-core normalization and kernel bound.
The joint-energy agent independently derived the actual constrained quadratic
join and later audited the root's proof/code bytes, including the dimensional
gate normalization. The neutral-action agent and a separate algebra subagent
crosschecked the contraction constants and center-patch regularity. These are
independent model reconstructions within the same tool/model environment,
not external peer review or formal machine proof.

Exact source hashes are in inputs/source_manifest.json,
stability/PROVENANCE.json, self_gravity/inputs/source_manifest.json,
joint_audit/SOURCE_HASHES.txt and patch/AUDIT.md. The source manifest records
which original reports were untracked; their copied bytes are included.
The whole packet is a separate candidate record. Frozen canonical criteria,
source reports and historical computation artifacts were not rewritten.

## Executed verification

All five schema-v2 run manifests validated against current proof/code/input
and output hashes: action/run_exact, self_gravity/run_exact,
regular_core/run_v1, regular_core/run_v2, patch/run_v1. The four authoritative
runs report respectively 36 exact checks; 56 exact checks; 19 exact identities
plus 3 potential quadratures and 7 gate samples; and 15 exact identities plus
12 blend controls. Core v1 is retained as a valid 17-identity predecessor.
These counts are controls, not a count of independent breakthroughs.

The root also checked all eight original snapshot hashes, parsed the JSON
records, reviewed document links, and checked whitespace and the publication
diff. Exact commands, environment and resources are preserved by the manifests
and REPRODUCE.md. No production simulation, observational rescoring or shared
heavy job was needed or restarted.

## Remaining mathematical and physical obligations

A differentiable occupied-center action does not provide a vacuum material
frame. The next phase needs a specified asymptotic/vacuum action and matching
conditions; the current patch explicitly lacks a continuous joint vacuum
coefficient limit. A dynamically counted charged central source must then be
solved and perturbed with the neutral stock in the same system. These changes
need their own energy and constraint checks. Finally the microscopic identity,
EOS, abundance, production, settling, metric/lensing and native cosmology must
be derived or disclosed as inputs before scoring that candidate's predictions.
