# FGF039: density-cap removal, with a corrected equality claim

Accepted after explicit equality clarification: the exact static lower-energy
bound extends to ALL nonnegative fixed-mass finite-entropy densities on a
sufficiently short Q crossing. Potential and scale perturbations remain H1_0,
with the scale quarter-cap. No potential-gradient supremum cap is imposed.
This is a strict energetic minimum, not a nonlinear solution theorem.

For bounded psi the unique mass-M density minimizer is
rho_psi=rho exp(-psi/cs²)/Z, Z=M^-1 integral rho exp(-psi/cs²).
Exact algebra gives the full matter remainder as cs²D(n||rho_psi)
-M cs² log Z-integral rho psi. D is the nonnegative isothermal relative
entropy, including n=0 by continuity. A directly proved tilted-variance bound
gives F_min >= -M(osc psi)²/(8cs²). Weighted endpoint control bounds oscillation
by (integral1/A)(integral A psi'^2). There is no imported statistical theorem
or small-amplitude exponential approximation.

Retaining the entire scale and field remainder and signed MOND source yields,
under the author's explicit sufficient gates alpha=C M integral1/A/(8cs²)
<=k/4 and beta=ell²Rmax/J<=1/4, k=exp(-1/4)/64,

DeltaE >= cs²D(n||rho_psi)+(k/4)E_p+E_eta/4
                         +S0 integral eta²/(2C).

Here E_p=integral A psi'^2/C, E_eta=J integral eta'^2/C, and R is the
reviewed finite-scale coefficient in the proof. The same central solution
satisfies the gates after shortening, with coefficients fixed and induced
mass/walls. Both density upper and lower caps are removed from this energy
comparison class. The background MOND flux cancels the linear matter work;
new comparison densities are not required to satisfy a static source equation.

The entropy reference is rho_psi, not rho. Elementary convexity and Cauchy
prove D(n||q)>=||n-q||_1²/(4M). Author additionally integrates the normalized
density path to bound ||rho_psi-rho||_1<=M osc(psi)/cs², giving a full stated
L1 bound to rho. Root's independent exponential conversion is weaker but
valid. Neither is an L-infinity or no-vacuum estimate.

A decisive control: set n=0 on a shrinking interval of background mass m,
and n=M rho/(M-m) elsewhere, keeping fields fixed. Exact energy is
cs² M log[M/(M-m)] ->0. These finite-entropy mass-preserving states violate
the old density cap and include vacuum. Root independently constructs smooth
localized depletion with disjoint compensation, with energy O(epsilon), also
allowing a vacuum plateau. This does not prove vacuum formation by a solution.
It disproves a positive ENERGY threshold that alone enforces that density cap.

By the two-endpoint H1 estimate, reaching ||eta||infinity=1/4 costs at least
J/(16 C ell) under the author's gates. Root's stronger retained gradient term
under its different sufficient gate gives J/(8 C ell). These are compatible
sufficient barriers, not competing sharp thresholds. A first-exit argument
uses the FULL total excess energy including nonnegative kinetic terms, and
requires an already-existing trajectory with fixed mass/walls/reference,
finite-action/entropy states and H1-time-continuous scale. It proves cap
continuation only during that trajectory's existing admissible lifetime.
No existence, weak energy equality, uniqueness or continuation past singularity
is thereby obtained; evolving-H work cannot be discarded.

## Preserved failed claim and correction ancestry

The original author and root wording said equality in the lower bound forces
the background. That literal assertion is false: psi=eta=0 with any admissible
n!=rho gives equality of both sides at positive cs²D(n||rho). Independent
author audit identified it. The valid statement is DeltaE=0 implies the
background. The exact inequality and strict energetic minimum survive.
Author correction history, reviewer pre-correction snapshot/request and root
frozen proof plus CORRECTION.md are preserved. Root auditor initially read
'equality' too charitably as zero energy; that interpretation was corrected
after the audit cue. The initial root audit Markdown was reconstructed and
verified byte-exactly against its emitted hash; its initial JSON was overwritten
before preservation and survives only as an explicitly labeled reconstruction
with its original timestamp unrecovered. No exact JSON recovery is claimed.
No saturation
uniqueness is accepted. This is a mathematical wording failure, not a numerical
execution failure, and the correction is not claimed independently frozen.

## Remaining implication and scope

Removing the density cap enlarges the class toward a nonlinear energy domain,
but finite entropy and L2 field gradient may not define the separate Euler
force-density product. FGF040 records that distinct integrability and weak
momentum-formulation gate, ready and UNLAUNCHED. It must prove or refute force
integrability and check any conservative reformulation from the inherited
equations; no new weak solution existence is accepted in this pass.

FGF037's upper/Taylor obstruction survives. Zero mathematical computations or
manifests; no numerical physical radius, empirical evidence or historical
novelty. Both a0 values and separate vacuum/frozen-H/evolving-H branches remain.
Q diagnostic only, with locally responsive scale an added premise; no RAR/M,
filtered-MONO, physical scale reservoir, metric/photon/DOF or calibrated cluster
transfer. FGF031 calibration stop and primary AS228 ownership remain unchanged.

## Evidence pins

- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-039/fgf039_run_001/result.json` SHA256 `7a3ffddec2231f7d8606a94d243027b3c21b2d1ef1b456747ca9d9e2f41bb8b5`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-039/fgf039_run_001/CORRECTION.md` SHA256 `bdf8001c004384856e8fcb07209b3ce61dddd4fff1d2591ead1ab47f769a50fe`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-039/fgf039_run_001/DERIVATION.md` SHA256 `c0f098c821ab9ec3346c3365fd9e45d8d536fe437ad47850fe38ecc523ebead8`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-039/fgf039_run_001/DERIVATION_PRE_CORRECTION.md` SHA256 `71ef5d150ff3912c378bec4df457a6ef8e0ab727628c5aa3177991b8f2e1d6a3`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-039/fgf039_run_001/REPORT.md` SHA256 `d85b87242d0c04f1f6c2623454b7a114b3367509498cf3d50b380de4bc7727a8`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-039/fgf039_run_001/input_sha256.json` SHA256 `d580648fc5e7ab7364c32652d290b1e40b1b72e3092b794d48b16d88fe9e243a`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-039/fgf039_run_001/result_pre_correction.json` SHA256 `c6a0f4289ea47959a825ad102f39d52e93aca78391269031c778a2b5a343b363`.
- `campaign_fresh_gravity_astra/stage_26/entropy_domain/CORRECTION.md` SHA256 `074561af900385e111dc8e7fe5cd8cf0e1124057b8cb5e17217e6a5e79ed1371`.
- `campaign_fresh_gravity_astra/stage_26/entropy_domain/INDEPENDENT_AUDIT.md` SHA256 `7cb27ca1243969af3e00437e99669a62dd009e58f979cf1ae8bd43af1ed7bcc0`.
- `campaign_fresh_gravity_astra/stage_26/entropy_domain/PRE_CORRECTION_INDEPENDENT_AUDIT.md` SHA256 `a30f29ac33c6ad9e4482081b028692effb2d66b7659d08681d024f23fee55acd`.
- `campaign_fresh_gravity_astra/stage_26/entropy_domain/PRE_CORRECTION_audit_result.json` SHA256 `83117d6b80b1ba01f3f9538d0c36470c0d04502ed85dee59a273293d35e8d879`.
- `campaign_fresh_gravity_astra/stage_26/entropy_domain/PROOF_COMPARISON.json` SHA256 `393bc382c5c8e0dea97e0580dc428238ca631fd12342747ce38d552f44fb77fb`.
- `campaign_fresh_gravity_astra/stage_26/entropy_domain/PROOF_RECORD.json` SHA256 `3eca9d728844f3846162adaa8c4df2ffd15360446c86cc806b3f6c900b50ffe4`.
- `campaign_fresh_gravity_astra/stage_26/entropy_domain/ROOT_DERIVATION.md` SHA256 `d227f50e3a8027db221f2a34c69481fedb55008d2edc6158c6fb0240cffced11`.
- `campaign_fresh_gravity_astra/stage_26/entropy_domain/audit_result.json` SHA256 `2accec5b0bd30502a6f504b3a7b428bed6239539886209cf0414efa85735784a`.
- `campaign_fresh_gravity_astra/stage_26/independent_audit/CORRECTION_REQUEST.json` SHA256 `c748857882f9414c82d4a22a3234886deaed3796504cb113996667bf956cf724`.
- `campaign_fresh_gravity_astra/stage_26/independent_audit/DERIVATION_FROZEN.json` SHA256 `3cd0da5dd0c119ac9a32bb0f793545ba6f3f39d86eac87d160b617d705737e7d`.
- `campaign_fresh_gravity_astra/stage_26/independent_audit/FROZEN_ENERGY_DERIVATION.md` SHA256 `016c2af282b0f484887efe87a0f1582ab8afbd1188ecae409dcf1d13bcd51f53`.
- `campaign_fresh_gravity_astra/stage_26/independent_audit/INDEPENDENT_AUDIT.md` SHA256 `1c67e6252471f2921682d63e5d153b7d6bbfbe255f27d57c92013a48940fe29a`.
- `campaign_fresh_gravity_astra/stage_26/independent_audit/REVIEWED_CANDIDATE_BEFORE_CORRECTION.md` SHA256 `71ef5d150ff3912c378bec4df457a6ef8e0ab727628c5aa3177991b8f2e1d6a3`.
- `campaign_fresh_gravity_astra/stage_26/independent_audit/audit_result.json` SHA256 `3580392febf5e7ef910be0008495ec12848734aab40dd01f59a19fadd4ae9704`.

Reconciled 2026-09-30T20:42:59.264781+00:00.
