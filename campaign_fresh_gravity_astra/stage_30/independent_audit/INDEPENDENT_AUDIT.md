# Independent FGF043 audit

**Verdict: proved as written**, for the exact analytic counterexample to inferring LOCAL energy balance from the specified weak mass/field/momentum residuals, small full initial relative energy and a scalar global energy inequality. The extra bounded-velocity full-flux criterion also holds in the stated FGF042 zero-excess class. These approximate states fail local energy balance; they are not exact solutions or a nonlinear instability result.

## Claim, ancestry and independence

The already-known FGF042 comparison family is embedded as time-independent states on one fixed slab: n=rho, both fields at the reviewed Q equilibrium, zero field velocities, and v_N=v0 N f(N³(x-x*)/L), j_N=rho v_N. Here f is one nonnegative nonzero smooth compact profile, v0,L are fixed physical velocity/length units, N is dimensionless, and x* lies on a regular side away from crossing/walls. All sufficiently large N are covered analytically. The bare static cubic-moment mismatch is ancestry, not newly promoted. The changed conclusion checks all actual residuals, the local energy current and initial/wall terms.

My independent proof was frozen at 2026-10-01T00:37:08.586570+00:00, SHA256 5945a75110202161cc4ead8c84bea637851fea32c204557d645005461e2ebfa3, before new author/root proof or formula previews. I then notified both agents, received the author's readiness message and read its raw proof. The author's additional primitive residual and off-shell energy identities were checked after my freeze. My amplitude control is v0 sqrt(N)f at the same width, while the author's is v0 f; both are valid fixed controls. No new root proof was read. Old stage29 root ancestry was hash-checked only. No numerical experiment or scan was executed.

The dependency graph is the pinned fixed-reference action and actual static crossing -> FGF032 full energy current and FGF040 full momentum current -> direct residual substitution and profile measure limit; separately, FGF042 zero-excess estimates -> bounded-velocity complete-flux criterion. Raw old FGF032/040 derivations were read and separately pinned by this audit. No external mathematical theorem or literature mechanism is a load-bearing leaf. Hash agreement verifies source identity, not mathematical correctness.

## Obligations

| Obligation | Status | Decisive check |
|---|---|---|
| Fixed physical class/support | Passed | Only velocity changes, with compact support strictly inside one regular side for large N. |
| Mass and both field residuals | Passed | Rc=(rho v)_x, Rphi=Rchi=0 by actual signed Q equilibrium. |
| Separate/primitive/combined momentum | Passed | Conservative residual is (rho v²)_x; primitive residual and full-current signs checked. |
| Full initial/global energy | Passed | Only rho v²/2 changes; O(N^-1) full excess is exactly time independent. |
| Local energy counterexample | Passed | Full current tends to F_* delta_x*, hence residual tends to nonzero F_* delta'_x* dt. |
| Initial/wall accounting | Passed | Relative temporal/initial terms cancel and vanish; perturbative wall currents are exactly zero. |
| Amplitude control | Passed | Bounded amplitude gives O(N^-3) full current and vanishing local residual. |
| Vacuum/logarithmic transport gate | Passed conditionally | EXTRA fixed |j|<=Vn plus exact entropy convergence controls full matter flux. |
| Trajectories, cap preservation, exact continuity followup | Not established | No new flow or approximation result accepted. |
| Physical/observational completion | Out of scope | No transfer licensed. |

## Actual residuals and test spaces

Changing variables y=N³(x-x*)/L gives

    integral rho v_N^k dx
      =v0^k L N^(k-3) integral rho(x*+Ly/N³)f(y)^k dy.

For k=1,2,3 this yields ||j_N||1=O(N^-2), integral rho v_N²=O(N^-1), and cubic flux rho v_N³ dx/2 -> F_* delta_x*, F_*=rho(x*)v0³L integral f³/2>0. The actual background density is retained throughout.

The source relation is B_x=C n+tau Phi_tt with signed Q B. Since fields and density remain at equilibrium, both field residuals vanish exactly. Continuity residual is Rc=(rho v_N)_x. Pressure and force cancel hydrostatically, giving Rm=(rho v_N²)_x. Separate force rho g0 is bounded and meaningful. For smooth compact spatial tests with bounded value and first derivative, a derivative of an L1 coefficient is bounded by that L1 norm. Consequently Rc=O(N^-2), Rm=O(N^-1) in this declared weak norm, uniformly in time, and both vanish on compact spacetime tests. Fixed reference units give the norm its dimensional interpretation. No stronger topology is implied. In particular ||j_N||2=O(N^-1/2) also gives a mass H^-1 bound, whereas the momentum-flux coefficient has L2 norm O(N^(1/2)); no analogous H^-1-small momentum claim is accepted.

The author's primitive residual obeys

    Rv=rho v_N v_N'=(rho v_N²)_x/2-rho'v_N²/2,
    Rm=Rv+v_N Rc.

Because rho' is bounded on the compact regular support, Rv is also O(N^-1) in the same weak tests. Direct substitution into the FULL currents yields P_N=j_N, Pi_N=Pi0+rho v_N², with equilibrium Pi0 constant, so Rcomb=Rm. All field kinetic, signed BG-W, scale gradient/potential and pressure terms are included. This conclusion does not multiply a weak residual by a diverging coefficient.

## Full local energy and the surviving defect

The exact total density changes only by rho v_N²/2. Its integral is O(N^-1), constant at every time, so the scalar global energy inequality holds exactly as a property of the ansatz. It is not derived from exact equations. Initial full energy density converges strongly L1; fields, scale and entropy equal the background, and fluid weighted kinetic norm tends to zero. There is no initial energy-density concentration.

The inherited complete current is

    S=v[j²/(2n)+e(n)+cs² n+n Phi]
                           -[Phi_t B+J X_t X_x]/C.

Since e(rho)+cs²rho=rho e'(rho) and e'(rho)+phi0=mu is spatially constant, S_N=rho v_N³/2+mu rho v_N exactly. Thus enthalpy and potential are retained together. Their combined term is O(N^-2) in L1, but the cubic current tends to F_* delta_x*. Time independence gives

    RE_N=partial_x S_N -> F_* partial_x delta_x* tensor dt,
    <RE_N,zeta> -> -F_* integral zeta_x(t,x*)dt.

A fixed compact product test with nonzero spatial derivative at x* detects the nonzero limit. Every finite-N residual is well-defined. Nonnegative tests can have either derivative sign at x*, so the limit also fails either fixed-sign local dissipative inequality with error tending to zero on tests. An actual local energy equality/admissibility condition therefore excludes this family. The residual integrates spatially to zero because wall flux vanishes, explaining compatibility with the global budget without energy creation.

The author's exact off-shell identities check by direct expansion:

    RE_N=v_N Rm+(mu-v_N²/2)Rc
        =v_N Rv+(mu+v_N²/2)Rc.

In the first expression, v Rm contributes rho'v³+2rho v²v'; -(v²/2)Rc subtracts rho'v³/2+rho v²v'/2, leaving (rho v³/2)' plus mu Rc. The second follows from Rm=Rv+v Rc. The unbounded v and v² factors explain why convergence in the declared weak norms cannot be inserted into this identity to infer local balance.

Velocity/current perturbations vanish near both walls. Mass/energy wall currents are exactly zero; background momentum traction can be nonzero, and only its perturbation is zero. Actual equilibrium Pi0 has equal endpoint values. Static time dependence supplies ordinary initial traces for each member. For a test vanishing at final time, the relative energy time term and initial trace cancel exactly, and each tends to zero separately. The flux defect already survives on interior-time tests, so no suppressed wall/initial measure cancels it.

## Control and complete bounded-velocity condition

The author's single control v_N^small=v0 f(N³(x-x*)/L) has all moments through cubic and the full current O(N^-3) in L1. Field residuals remain zero; every listed weak residual, including local energy, now vanishes. My independent sqrt(N)-amplitude control still has unbounded peak velocity but kinetic energy O(N^-2) and cubic current O(N^-3/2), with the same no-defect conclusion. These are independently selected analytic controls, not a scan or exact-solution construction.

In the general FGF042 zero-excess class, impose EXTRA |j|<=Vn with fixed finite physical V, taking v=j/n on n>0 and v=0 on vacuum. Energy does not supply this hypothesis. The inherited convergence gives integral j²/n->0, ||j||1->0, D(n|rho)->0, ||n-rho||1->0 and uniformly bounded Phi. Cubic flux is bounded by (V/2)integral j²/n; potential flux by ||Phi||infinity||j||1. The exact nonnegative entropy integrand h=n log(n/rho)-n+rho gives

    |n log(n/rho)|<=h+|n-rho|,
    integral |j log(n/rho_ref)|
      <=V[D(n|rho)+||n-rho||1]
          +||log(rho/rho_ref)||infinity||j||1 ->0.

The background logarithm is bounded because rho is positive bounded. At vacuum n log n and v n log n have their conservative zero extensions; no undefined product or positive lower density assumption is introduced. This proves integrability and strong L1 convergence of enthalpy current, not just a signed-integral cancellation. After multiplication by cs² and addition of kinetic/potential pieces, the complete matter flux is identified. FGF042 already controls the field flux.

When the zero-excess bounds and V hold uniformly in time, they imply spacetime L1 current convergence on a fixed slab. Strong energy-density convergence then gives convergence of the local residual to the zero background residual. Slice-wise convergence without a time bound is insufficient, and the author's uniform-time qualification is essential. This is a sufficient zero-excess compactness gate, not a proof of exact local balance for each approximant, dynamical preservation of V, finite nonzero-energy compactness or existence.

## Provenance, preserved metadata change and limits

The scientific proof is unchanged at SHA256 dd56899478c637f5d8e1c51fddde2b4754d24795234037e3cee9526336f6e414. The original result SHA256 0a04e0cfc35bb005581bc9a10337ac78821e252dd8dd2b6aa7a56eb43ef5a961 is preserved byte-for-byte as result_before_followup_refinement.json. The CURRENT audited result is a867f0fdb7ea9957fe6b48ca5aa2868530a819e2e01814038a8cc324e2542bde. A metadata-only update added FOLLOWUP_SCOPE.md and changed only next_unresolved_implication, suggested_followup, artifacts_sha256 and finished_utc. The proof and report did not change. My first final-write attempt stopped on an old-result hash guard BEFORE writing either audit report/result; no prior finalized audit was overwritten. This administrative stale-pin event is not a failed mathematical test.

The revised followup proposes solving continuity exactly for a selected stationary velocity flow, then checking the other residuals/budgets. I read it solely as an UNEXECUTED target. No flow formula, estimate, acceptance result or new scientific claim is promoted by this audit. The old generic approximation gap remains scientifically true; the narrower next target is separately to test exact-continuity repair while retaining all residual and energy requirements.

Administrative Python verified the current 12 input hashes and 5 artifact hashes (including original result and followup scope), matching input-map JSON, required result fields, all 7 independently frozen source pins and the frozen derivation. Full source mappings are in audit_result.json. No correction to the proof was required, no frozen derivation was changed, and no mathematical computation/manifest is claimed.

Both a0 hypotheses, actual signed MOND Q and constant-vacuum/frozen-H/evolving-H distinctions remain. Responsive scale/inertias remain diagnostic assumptions. This closes only the precise local-admissibility implication and sufficient flux gate. It does not establish a trajectory, preserve a velocity cap, settle existence or provide RAR/M/filtered-MONO, metric/photon/DOF, physical reservoir, empirical or theory closure.
