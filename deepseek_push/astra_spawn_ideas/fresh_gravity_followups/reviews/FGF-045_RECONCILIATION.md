# FGF045: conditional smooth-lifespan obstruction with actual fluid momentum

Accepted scoped analytic result after independent author and corrected-root
audits. The fixed Q potential is retained, while BOTH continuity and isothermal
fluid momentum are now actual equations. This advances FGF044's prescribed
velocity test. It is not a solution of the coupled gravity equations.

Take the same C1,1 compact polynomial initial velocity of amplitude v0 N and
width L/N³, with density initially rho on a regular positive-side neighborhood
of the Q crossing. Let omega=(v0/L)N4. For each such fixed background there
are finite constants B,N0, independent of N, such that no positive-density C1
solution covers the declared local characteristic cone through B/omega for
N>=N0. Hence this family cannot have a common N-independent smooth lifespan
on that neighborhood. The constants are very conservative, not sharp physical
times, and no finite numerical value has been computed.

The decisive calculation retains pressure: r=v+cs log(n/nref), l=v-cs log(n/nref)
travel at v±cs with forcing -g0. If alpha=r_x,beta=l_x and h=n^-1/2,
y=h alpha,z=h beta, then

D+ y=-y²/(2h)-g0' h, D- z=-z²/(2h)-g0' h, D0 h=(y+z)/4.

The mixed gradient term cancels exactly. Bounding the positive parts of y,z
controls h by h0+A omega t on the comparison slab. This supplies the density
lower bound rather than assuming it. A negative initial y of order omega then
obeys w'>=w²/[4(h0+A omega t)] for w=-y after explicit large-N force gates.
Integration of the varying coefficient makes 1/w negative at the proposed
endpoint, contradicting finite positive C1 survival. Replacing this coefficient
by its endpoint constant would lose the useful closure and was not done.

Both characteristic families and material curves remain inside a cone with
speed O(N). The chosen compression curve travels O(N^-3) through the comparison
time, away from the crossing and walls. The fixed initial cone base is not
shrinking; the small displacement is not a claim that all data have shrinking
support after evolution. Invariants bound density above for each fixed N;
the weighted envelope supplies the useful uniform lower bound on this short
cone. No N-uniform upper density or velocity cap is assumed. C1 characteristic
flow differentiation justifies the gradient ODEs without requiring C2 endpoints.
The magnitude of g0' is retained without imposing a favorable sign.

Exact fluid energy includes pressure work and n phi0 interaction. Its local
balance holds for every actual smooth fluid solution; integrated conservation
requires appropriate zero-flux fixed boundaries. A moving cone has boundary
terms and is not assigned conserved energy. At t=0 actual v_t=-v v_x cancels
the positive energy derivative from FGF044's stationary prescribed velocity.
The hydrostatic zero-velocity control solves the two fluid equations exactly.
Frozen gravity still has source residual C(n-rho), C=4pi G_Newton; no bound
or cancellation of that dynamic field mismatch is proved here.

Scope is essential: this proves nonexistence THROUGH the comparison time,
not existence before it, a maximal continuation theorem, an actual shock,
or classification of an earlier endpoint. Root's original interpretive sentence
claimed too much about that endpoint. Its independent auditor identified the
gap; the original is preserved and CORRECTION.md withdraws that statement.
The same auditor found a G notation collision; the correction distinguishes
force bound G_force from Newton's constant. Author and frozen reviewer already
stated the appropriate conditional scope; their proofs required no correction.
The corrected root theorem and author's theorem agree. No original failure
was erased or converted into a successful uncorrected proof.

The independent author reviewer first read a pre-freeze draft at hash
e906db202d89174f3e5f1dff41a6481ebb8e06b772e117b0a0bd95797a7fd11e,
then reread the frozen final proof at 889775ec9b85969afb58f7f05e4d64601fea4760325a07110dc5e0c8aec26a3b.
AUTHOR_EXPOSURE records that chronology. The author report discloses wording
clarifications before packaging; acceptance applies only to the final pinned
bytes. No claim of recovering the earlier draft from its hash is made.

FGF046 targets the missing direct local C1 existence/continuation construction
for these exact data. It is unlaunched; a new upper-bound calculation alone
would repeat an exhausted implication. A local solution construction still
would not solve dynamic gravity or the physical theory.

Both a0=9.3619e-11 and 1.1279e-10 m/s² remain separate; constant-vacuum,
frozen-H and evolving-H histories are distinct. Signed Q MOND source is kept.
No transfer to RAR/M/filtered MONO, criterion B, metric/photon/DOF, a physical
conserved scale reservoir, calibrated observations or historical novelty.
Proof-only: zero mathematical executable runs, synthetic experiments or real
data reductions. Primary AS228 ownership and cluster calibration stop unchanged.

## Evidence pins

- `campaign_fresh_gravity_astra/stage_32/fluid_momentum/CORRECTION.md` SHA256 `3d7f3a319de9db22fba6afadf58d66229e11b4a8a211066a18db002bd111cf21`.
- `campaign_fresh_gravity_astra/stage_32/fluid_momentum/INDEPENDENT_AUDIT.md` SHA256 `767ae92265e1f538339f808e9594f828b9d431c241cfd7c6c9b0d701bcd33eb0`.
- `campaign_fresh_gravity_astra/stage_32/fluid_momentum/PROOF_COMPARISON.json` SHA256 `04f0149cf3c9f79c32cf834191ca92a7c37552ee5a0ea821a2de80f79ccb3e5c`.
- `campaign_fresh_gravity_astra/stage_32/fluid_momentum/PROOF_RECORD.json` SHA256 `4e3bad37e0f52955c9029883194d0d58b12561fe835beb7c496dd445adafea70`.
- `campaign_fresh_gravity_astra/stage_32/fluid_momentum/ROOT_DERIVATION.md` SHA256 `e4c94d7b9019d61c91499bcc818d1f88f2b434a04c35533dace7061e853dd58d`.
- `campaign_fresh_gravity_astra/stage_32/fluid_momentum/audit_result.json` SHA256 `d3d41ba1a49723403f2aafb3571e4db60f3db098bea0d14ce618019215b87880`.
- `campaign_fresh_gravity_astra/stage_32/independent_audit/AUTHOR_EXPOSURE.json` SHA256 `13406aee1149f3dbc494f683e6c350f68b2a1859aa64c7b18c7083754411cf43`.
- `campaign_fresh_gravity_astra/stage_32/independent_audit/DERIVATION_FROZEN.json` SHA256 `3ad3d17a71cd28c34722d62470a712ea1a6007227b9735cefb28c13abfd9b086`.
- `campaign_fresh_gravity_astra/stage_32/independent_audit/FROZEN_DERIVATION.md` SHA256 `4cd8ed17a4305edb503d70e9082d5af4841a6da6eb16f9563039e4626e280028`.
- `campaign_fresh_gravity_astra/stage_32/independent_audit/INDEPENDENT_AUDIT.md` SHA256 `2dfbb313c6328e515e32e5c3e9cb49bd6cd0ff566cc6cdbff4eef1dbc3038c27`.
- `campaign_fresh_gravity_astra/stage_32/independent_audit/audit_result.json` SHA256 `977b24a9b239dd8e8991e1f0c6de3cb2a9f5c89aa34eab3c6c58948f0ff3ccef`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-045/fgf045_run_001/DERIVATION.md` SHA256 `889775ec9b85969afb58f7f05e4d64601fea4760325a07110dc5e0c8aec26a3b`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-045/fgf045_run_001/REPORT.md` SHA256 `fb5b6ae680a9ff44cac733dea70036126bd6034959665b4eebfdc386cf9b78f2`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-045/fgf045_run_001/input_sha256.json` SHA256 `7ff0a9e3a6f5281380fdf8ee3eefa8054fb38d2046c6c8c20dd79e995274c858`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-045/fgf045_run_001/result.json` SHA256 `c4429fcd1732e85a70161eb2575141b557578aa773d8332943e33f1c9d3b1789`.

Reconciled 2026-10-06T01:47:28.155836+00:00.
