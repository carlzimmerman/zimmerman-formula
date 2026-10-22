# FGF044: exact transport removes the persistent flux, but fails exact energy admissibility

Accepted bounded analytic result, recovered and independently audited on 2026-10-06.
Original proofs were saved on October 1 before usage-limit interruption. The
interruption snapshot preserves the stale assignment and partial-file provenance.
Package recovery is self-review, not an independent proof. Fresh author audit
rechecks the inherited frozen reconstruction then the author proof; it does not
claim a newly blind freeze. A separate root-only auditor read neither new author
nor reviewer proof. Original scientific bytes remain unchanged; no correction
was required. All package and audit hashes were checked before this promotion.

On the fixed signed-Q crossing choose x* on the positive regular side, g0>0 and rho'<0, with a support away from center/walls.
Use fixed physical v0,L,T and dimensionless N, ell=L/N^3, V=v0 N, s=Vt/ell;
f(y)=(1-y²)² inside (-1,1), zero outside. This declared C1,1 profile gives
F'=1/f and Y_s=F^{-1}(F(y)+s). Its positive Jacobian gives
n(t,X)X_x=rho exactly. Only the initial support mass m_N=O(N^-3)
participates; there is no incoming supply and endpoints remain fixed.

The polynomial Jacobian bound yields D(n||rho)=O(N^-3 log N), uniformly on
[0,T], and K=O(N^-1). The FULL energy density retains interaction:
H-H0=nv²/2+cs² h(n,rho)+mu(n-rho), with hydrostatic mu constant.
Its integral is Erel=K+cs²D; its L1 norm tends to zero uniformly. Nevertheless
Erel'(0)=-(1/3) integral rho' v_N³ >0. The exact inequality
Erel(t)<=Erel(0) therefore fails for each N on some short N-dependent interval.
No duration or equality with the flux transient scale is inferred. Author's
vanishing-error budget is valid. Root independently sharpens its error to
O(N^-4)+O(N^-3 log N) by centered layer-set overlap; this extra was separately
audited. Neither estimate repairs the failed exact inequality.

Each moving label travels at most 2ell, so integral j dt dx<=2ell m_N=O(N^-6)
and integral nv³/2 dt dx<=V² ell m_N=O(N^-4). Full current
Q=nv³/2+cs²nv log(n/rho)+mu nv thus tends to zero in spacetime L1,
including enthalpy and potential. The initial spatial cubic flux still tends
to a nonzero delta; at every fixed positive time it vanishes. Times of order
ell/V retain a transient profile, but their total time-integrated flux vanishes;
there is no temporal delta. Uniform flux convergence through t=0 is false.

Continuity is exact. Frozen fields give Rphi=C(n-rho), small but nonzero,
and Rchi=0. Matter momentum is j_t+(nv²+cs²(n-rho))_x+(n-rho)g0;
combined momentum omits the last term via the actual field-source correction.
Both vanish in the declared compact spacetime C1-test dual. Author's interior
rate O(N^-3) is sharper than root's O(N^-1); initial momentum trace O(N^-2)
is separate. A checked reviewer supplement finds an order-N² fast-layer
spatial obstruction, so no uniform-time spatial residual improvement follows.
Full local-energy residual tends to zero by direct energy-density/current L1
bounds, without multiplying weak residuals by unbounded v. Initial energy trace
is O(N^-1); mass trace is exact; all wall perturbation currents/traction vanish.
The zero-velocity control recovers the static background exactly.

This closes the single finite-supply test. It constructs only an exact
continuity solution, with residual momentum/field equations and failed exact
global energy admissibility. It proves no exact coupled evolution, general
compactness, nonlinear stability or physical closure. Proof-only: zero
mathematical executable computations, synthetic tests or observational data.

Both a0=9.3619e-11 and 1.1279e-10 remain separate; constant-vacuum and frozen
H references are not evolving-H solutions. Signed MOND Q source is retained.
No transfer to RAR, M, filtered MONO, criterion B, metric/photon/DOF or a physical
conserved scale sector is proved. Cluster calibration stop and AS228 ownership
remain. FGF045 changes the next equation to actual fluid momentum in the fixed
background and tests smooth lifespan; it is a specification, not a launched run.

## Evidence pins

- `campaign_fresh_gravity_astra/stage_31/exact_continuity/INDEPENDENT_AUDIT.md` SHA256 `47400d804487818ac860617b1b7eb758f96898996d7eee12f4e583e66f474ecc`.
- `campaign_fresh_gravity_astra/stage_31/exact_continuity/PROOF_COMPARISON.json` SHA256 `fd3135f8f20676cc16f54178194cb0b3edb978ab4adbba6cfd5e0fcfb01015ea`.
- `campaign_fresh_gravity_astra/stage_31/exact_continuity/PROOF_RECORD.json` SHA256 `0ffce17e6bb5f35eb432544f0f4a6baa8e14ba5b8d4471d57d9db893cf0b91ab`.
- `campaign_fresh_gravity_astra/stage_31/exact_continuity/ROOT_DERIVATION.md` SHA256 `4e426c18438987afdfdf87ea06bfee428a195584b22b514fa1a9bf2c047ad337`.
- `campaign_fresh_gravity_astra/stage_31/exact_continuity/audit_result.json` SHA256 `b753403ee815799e6965f8ea965facdf9729ec610ba84b037531c31a92149a4d`.
- `campaign_fresh_gravity_astra/stage_31/independent_audit/DERIVATION_FROZEN.json` SHA256 `8d54b9c5c78c5ba891a8d4a2b4d799c7dd14e397b656ef2dd6e3e3d72a74f6a2`.
- `campaign_fresh_gravity_astra/stage_31/independent_audit/FROZEN_DERIVATION.md` SHA256 `2240566ca05c2efdf90b70d4b6acceed993595c996a7fea4bc9a0387c5169e23`.
- `campaign_fresh_gravity_astra/stage_31/independent_audit/INDEPENDENT_AUDIT.md` SHA256 `740a06e266e0d4be38869f24cd376770bab358180b3ee677680b5e617ae19f16`.
- `campaign_fresh_gravity_astra/stage_31/independent_audit/audit_result.json` SHA256 `f8055a09408521111e620a498b6bfaf24f0f0148379cd6db157d0bb5948d7700`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/handoffs/FGF044_INTERRUPTION_20261006.json` SHA256 `ab54f3b1d61dc96c3ea202a331b265abfd8ed2b7c398a79f11d7a56ad138ca04`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-044/fgf044_run_001/DERIVATION.md` SHA256 `5603934d74e5f9236a388aee63adfe714ad6fb8e218f95de4a5436fec7c5d9fb`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-044/fgf044_run_001/REPORT.md` SHA256 `e66c58db90981bc37f42c552782db53567e84c879dfa7a246bf76a81d8f33b2b`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-044/fgf044_run_001/input_sha256.json` SHA256 `8f6608c19ed0a16de28dab0bfffb71b7ba09c25083ce4ebf9d126badeb4073d8`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-044/fgf044_run_001/result.json` SHA256 `5472cc19350935a6a09c18a69e10914211c7fb2e7cf3876f3e0054f062d2341c`.

Reconciled 2026-10-06T00:44:51.664051+00:00.
