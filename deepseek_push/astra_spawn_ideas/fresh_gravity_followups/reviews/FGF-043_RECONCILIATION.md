# FGF043: weak equations plus global energy do not enforce local balance

Accepted exact approximate-state counterexample and conditional full-fluid-flux
estimate. The static cubic moment was already FGF042 evidence; the new result
is its actual equation-residual, local energy, initial and wall audit. No exact
nonlinear solution or physical-theory failure is inferred. Proof-only, zero
mathematical computations/manifests.

On the same fixed Q crossing choose a compact regular-side support and fixed
physical v0,L. The inherited family is n=rho, phi=phi0, chi=chi0, zero field
velocities, v_N=v0 N f(N³(x-x*)/L), j_N=rho v_N; make it time independent on
one fixed time slab. All couplings, mass and walls remain fixed. Signed Q source
and scale residuals are exactly zero. Actual continuity residual is (rho v_N)_x,
conservative matter/combined momentum residual is (rho v_N²)_x. They are
O(N^-2), O(N^-1) respectively in the spatial dual of bounded C1 tests, uniformly
in time. Continuity is additionally H^-1-small. No H^-1-small or strong L1
momentum residual is claimed. Primitive momentum equals rho v_N v_N,x and is
also small in the declared weak test space, with the proper continuity correction.

FULL energy density differs from background by rho v_N²/2. Its integral and
initial value are O(N^-1)->0, exactly constant in time, hence obey a global
energy inequality. Every perturbation flux is zero near outer walls; initial
energy and momentum are strongly prepared with no hidden initial energy defect.
All field/internal/interaction terms are retained. Hydrostatic equilibrium makes
mu=cs²log(rho/rho_ref)+phi0 constant, so actual full energy flux is

Q_N=rho v_N³/2+mu rho v_N.

Its measure limit is K delta_x*, K=rho(x*)v0³L integral f³/2>0. Consequently
RE_N=partial_t H_N+partial_x Q_N tends to K partial_x delta_x*, with pairing
-K integral zeta_x(t,x*)dt. This is NONZERO, even though all listed weak
mass/field/momentum residuals vanish and global energy is small and constant.
The derivative integrates to zero spatially and takes both signs on nonnegative
compact tests; neither a local equality nor a dissipative local inequality with
vanishing error admits it. There is no net energy creation. Initial time-density
terms cancel correctly for static states, and cannot cancel the interior flux
residual. The limiting background itself still solves its equations.

The off-shell identity identifies the invalid inference. For conservative Rj
and continuity Rc, RE=v Rj+(e'+phi-v²/2)Rc+field residual work; equivalently
RE=v Rv+(e'+phi+v²/2)Rc with primitive Rv. Direct expansion checks both signs.
Multiplying weakly small residuals by the unbounded N-dependent velocity and
its square is uncontrolled. Identities are applied at finite N before any limit.
No rough limiting distribution product is silently formed.

Author/root remove the factor N for a fixed-velocity amplitude control; reviewer
uses sqrt(N) instead, leaving an unbounded peak with vanishing cubic flux mass.
Both controls make all declared residuals, including local energy, vanish.
These are exact distinct controls, not a parameter scan.

For GENERAL FGF042 zero-energy states, adding one fixed physical bound |j|<=Vn
suffices to identify the complete fluid energy current in L1, without any density
upper/lower cap. Cubic transport <=V times kinetic energy. With
h=n log(n/rho)-n+rho>=0, the exact estimate
|n log(n/rho)|<=h+|n-rho| controls logarithmic enthalpy by relative entropy and
density L1 convergence. The remaining background logarithm/potential factors
are bounded and multiply j->0 in L1. At vacuum all conservative terms extend
by zero. The velocity cap is EXTRA, not derived from energy or promoted to a
physical cutoff. Field flux is already controlled by FGF042.

A ROOT SCOPE CORRECTION is retained: the original paragraph after root estimate(2)
passed from spatial convergence to a spacetime consequence without explicitly
requiring time integrability. The independent root-only auditor identified this.
CORRECTION.md requires the right-hand side to tend to zero in L1_t, plus spacetime
L1 energy-density/field-flux convergence. FGF042's uniform-in-time hypotheses on
a finite slab suffice. Pointwise-in-time convergence alone is NOT enough. Root
original bytes and credited correction are both preserved and audited. Author
and independent reviewer already stated the uniform-time qualification explicitly;
their scientific proof required no correction. The stationary counterexample is
unaffected. No original failure is silently erased.

Author metadata was amended only to record a narrower unexecuted follow-up after
its original result hash was sent; original result_before_followup_refinement.json
is preserved byte-for-byte. DERIVATION and REPORT did not change. Final audit pins
the current result and original; this is a metadata revision, not a new run.

Next FGF044 changes a violated equation: solve continuity exactly from the same
rho under ONE prescribed localized one-sign stationary velocity, then check
finite mass supply, entropy/full energy, spacetime flux and all remaining coupled
residuals. This is not executed here. No static density replenishment may be
silently retained, and a continuity repair is not an exact coupled solution.

Both a0 footings and vacuum/frozen-H/evolving-H histories remain separate; signed
Q MOND source and actual inertias retained. The diagnostic matter model has no
physical metric speed ceiling; this unbounded-velocity family makes no physical
superluminal prediction. No RAR/M/filtered-MONO, metric/photon/DOF, physical scale
reservoir, calibrated observations, historical novelty or theory closure follows.
FGF031 calibration stop, primary AS228 owner and prior errors/failures preserved.

## Evidence pins

- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-043/fgf043_run_001/result.json` SHA256 `a867f0fdb7ea9957fe6b48ca5aa2868530a819e2e01814038a8cc324e2542bde`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-043/fgf043_run_001/DERIVATION.md` SHA256 `dd56899478c637f5d8e1c51fddde2b4754d24795234037e3cee9526336f6e414`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-043/fgf043_run_001/FOLLOWUP_SCOPE.md` SHA256 `f6eb65331ba5739459d917d2ce21d4827dd2e595f57859d26a6d786462dc5393`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-043/fgf043_run_001/REPORT.md` SHA256 `fe37fef0d68022f84b87991b726e2855c6ac26f9a9c8389fbd3441b06775f161`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-043/fgf043_run_001/input_sha256.json` SHA256 `cdc5394e65db46891775f0fc9d15ba1e2af5c974c7ada63670dad23b85070129`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-043/fgf043_run_001/result_before_followup_refinement.json` SHA256 `0a04e0cfc35bb005581bc9a10337ac78821e252dd8dd2b6aa7a56eb43ef5a961`.
- `campaign_fresh_gravity_astra/stage_30/local_energy/CORRECTION.md` SHA256 `cfa5cc3117ba7b42b3fafee936fec35f1353042c5d429986277a24e51fdafa74`.
- `campaign_fresh_gravity_astra/stage_30/local_energy/INDEPENDENT_AUDIT.md` SHA256 `7b459fc71af5173beabfbc06b8e7f5078e6085cc74280e70b55799901f479c0f`.
- `campaign_fresh_gravity_astra/stage_30/local_energy/PROOF_COMPARISON.json` SHA256 `d3f94d8ec85d19ceae78db6d6fe830973335d279f13460e951ac51c8d211440f`.
- `campaign_fresh_gravity_astra/stage_30/local_energy/PROOF_RECORD.json` SHA256 `1b232c9b97c284dc0a640302fe8486316f4c22cbae0ebf5e88a0362a831b8197`.
- `campaign_fresh_gravity_astra/stage_30/local_energy/ROOT_DERIVATION.md` SHA256 `45236fe01ee93bdcedbe785bcb2948d408b4ea05869aa81235095e2cfec2ca27`.
- `campaign_fresh_gravity_astra/stage_30/local_energy/audit_result.json` SHA256 `bab7274e201d4e1c995f255b2902d69fa54788851cc98c046f963a950de43a51`.
- `campaign_fresh_gravity_astra/stage_30/independent_audit/DERIVATION_FROZEN.json` SHA256 `936d2575baf1960639fb68138fc12affb5895beb0cb8e4e0e91e6eb0e6a1d452`.
- `campaign_fresh_gravity_astra/stage_30/independent_audit/FROZEN_DERIVATION.md` SHA256 `5945a75110202161cc4ead8c84bea637851fea32c204557d645005461e2ebfa3`.
- `campaign_fresh_gravity_astra/stage_30/independent_audit/INDEPENDENT_AUDIT.md` SHA256 `564a7eeafbc50937e53604709f069e0101768dc41c5b37c3142ff2b5e671e96d`.
- `campaign_fresh_gravity_astra/stage_30/independent_audit/audit_result.json` SHA256 `ce39589b9c0ae3986f3c81f1ce94d3e7ced4de497bd4f530334c97479d4411f1`.

Reconciled 2026-10-01T00:44:07.961590+00:00.
