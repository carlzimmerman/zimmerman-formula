# FGF055 independent author comparison audit

Primary verdict: **correct only after a stated restriction**. The precise
bounded cone-survival theorem is supported, but the frozen author's Section 6,
lines 310–311, must explicitly restrict its two small MATTER stress orders to
the exterior wedges/endpoints. The field orders hold throughout the interval.
This is a localized proof-text scope defect, not a counterexample to the
bounded theorem or the underlying PDE. No frozen author bytes are changed here.

## Target and provenance

Reviewed author `fgf055_run_001` claim: every fixed positive coefficient and
smooth positive compatible hydrostatic tuple in Vmax>(15/2)cs admits fixed
(15/2)cs<V<Vmax and 15/2<B<Bcap<V/cs. For sufficiently small independent
width epsilon, the exact unsmoothed packet has compatible C1/C1,1 evolution
through kappa epsilon/V on its explicit contained cone, while no positive
C1 solution survives on that same cone through B epsilon/V. Existing
prefixes have positive uniform density/field margins, evolved |v|<Vmax,
field-background O(epsilon), and exterior fluid O(epsilon^2). Constants may
depend on arbitrary fixed finite field speeds. No stationary-patched maximal
class, endpoint classification, or physical realization is claimed.

Verified before reading author content:

- DERIVATION.md SHA256 `289b493bbfba4613cf95f939e343bcdd00f0caf55037d107467c15e525e07b5f`.
- result.json SHA256 `c3d9ca6af3014758ca01ebeafbe1bdf4eb0913250c9e4d64e776067d40119e5c`.
- FREEZE.json SHA256 `89211fbf191fa854f4c9470fe9c4768374f7d98b56f68412d956e7aab866987f`.

The reviewer first froze its own proof and input pins without any new author
or stage42 root exposure. That proof remains SHA256
`42f9f30c8440cc40095ab4edfb10aebd6f2e5fc4ef736414f06d2bbf4f02a3d9`, and
its freeze remains `3eb3a94284106c2e4582d838eeb683436bc4912492361137c33a350577ad5f0f`.
The independent proof already obtained the same cone, acoustic cell, and
orders with a slightly coarser field time estimate. Agreement is not itself
the validation; the checks below reconstruct the critical implications.

After reading the pinned author proof, the reviewer independently identified
and sent the Section 6 scope defect to root. A root message flagging the same
sentence arrived immediately afterward. This post-freeze root cue is recorded;
no stage42 coordinator proof, refinement proof, or refinement audit was read.
The supplementary FGF051 local-construction source was verified against its
author-pinned hash `37a88c86cd0ba56c1d30e10d79a68fda0dc2160313ae976712ab39f470418ac3`
before Section 4 was read. No network or external theorem was used.

## Decisive defect and required restriction

Frozen DERIVATION lines 310–311 say:

> By the smooth chart, throughout I (and hence at A,D) one has
> Sf-Sf0=O(e), mf=O(e), whereas nv^2=O(e^4) and c^2(n-rho)=O(e^2).

The shared spatial qualifier naturally assigns all four orders to I. That
literal statement is false: at t=0, X=0, the initial packet gives
nv^2=rho(0)V^2>0, independent of e. No finite e-independent O(e^4) constant
can bound it as e decreases. Small n-rho is likewise only established on the
exterior wedges; Section 5 explicitly permits an order-one core disturbance.

Required minimal clarification: state that Sf-Sf0 and mf are O(e) throughout I,
then state separately that at A,D (indeed throughout the exterior wedges)
nv^2=O(e^4) and c^2(n-rho)=O(e^2). This is an explicit restriction of the
proof sentence, not an additional assumption, change of equations, or repair
of the theorem's mechanism. The theorem's Section 5 estimates already carry
endpoint brackets and use only the valid exterior orders. No dependent
capacity, energy or lower-time formula changes. The frozen version is not
reported as entirely correct as written until this correction is made or
accepted explicitly as a scope restriction in the review record.

## Dependency graph and critical checks

Pinned full equations/chart and local characteristic construction feed the
fresh lower-time derivative estimates. Separately, contained-cone acoustic
amplitudes feed the true density-source bound; exact field-background
subtraction feeds the field O(t) bound; the actual exterior characteristic
bootstrap feeds O(t^2) fluid errors; those errors and bounded core density
feed the variable-mass capacity identity and the strict moment contradiction.
The field momentum and energy equations are independent consistency checks.
No edge-H equality or stationary patching is a node in this graph.

1. **Actual source, chart and speed — passed.** In the author's coordinates,
   D_lambda(z)(z-z0)=H(q,z)-H(q0,z0)-[lambda(z)-lambda(z0)]z0_X.
   Only the known background derivative is multiplied by a speed difference.
   The source Lipschitz constant includes exp(q), both h_chi terms and scale
   response/restoration. Acoustic paths contained in the wide cone give
   |q-q*|<=V/(2c)+Ee/c and therefore uniform finite n bounds, even if unknown
   first gradients grow. Because V is fixed, exponential constants in V/c
   are legitimate. The actual field range remains in a half-chart margin
   and the evolved velocity is bounded by V+Ee<Vmax. These are simultaneous
   strict first-exit improvements, not assumed global speed/source bounds.

2. **Cone and incoming signals — passed.** S exceeds Vmax+c, tau^(-1/2),
   sqrt(J/sigma), and the lower-construction bound Slo. On positive g,
   0<A_g<1 gives the global field-speed ceiling b<tau^(-1/2). The cone starts
   with radius Hrad e=(3+S Bcap/V)e and still has radius 3e at Theta_cap.
   Every backward field/fluid path from its later sections stays in earlier
   sections under the bootstrap. Incoming field source points are included;
   no estimate is confined improperly to [-2e,2e]. Hrad is fixed though
   potentially huge, so Hrad e<R can always be imposed without retuning.

3. **Exterior centered invariants and geometry — passed.** Direct calculation
   gives D_(v+c)u+=-(g-g0)-c v q0_X and
   D_(v-c)u-=-(g-g0)+c v q0_X. The advective background terms are retained.
   Initially u+=u-=0 outside the packet, including its C1,1 joins. On the
   bootstrap |u±|<eta/2, the acoustic speeds lie between -c-eta/2 and
   c+eta/2. The right inner edge travels right at c+eta, so backward acoustic
   paths stay to its right; the left edge has the analogous reversed sign.
   Outer boundaries shrink faster than every characteristic. Thus no missing
   trace enters through a lateral edge. The integral source Cg t produces
   Uext<=(Cg/2)t^2 exp(c Kq t), which strictly improves the bootstrap after
   choosing e small. Because (c+eta)Bcap/V<1, A,D stay strictly inside these
   wedges with positive margins through the cap. Fields are free to arrive.

4. **Mass, momentum, first moment and signs — passed.** Direct integration
   gives M'=j(A)-j(D), P'=-[nv^2+c^2n]-int ng,
   I'=P-ell j(D). Hence Delta'=ell j(A)-P, and with P'=-R,
   Delta(T)=Delta0-P0T+int(T-t)R(t)dt+ell int j(A,t)dt.
   Hydrostatic c^2[rho]=-int rho g0 fixes the pressure sign. The last mass
   term uses A, not D, and has a plus sign. M is variable; pressure is never
   zeroed. All four remainders in author (5.4) have the stated respective
   orders e^3,e^4,e^6,e^4 with fixed constants. The positive initial moment
   margin is rho*[(16/15)B-8]e^2. A strict B>15/2 defeats all remainders for
   sufficiently small e. The displayed finite-e Ccap bound is sufficient.

5. **Field momentum and stress — passed except the scoped prose above.**
   Differentiating mf=-(tau p g+sigma w k)/C yields ng-(Sf)_X because
   (gA-W)_X=g A_X+Tscale k. The scale Tscale k terms cancel with the correct
   sign. Thus Fm'=-[Sf-Sf0]+int(ng-rho g0), and
   (P+Fm)'=-[nv^2+c^2(n-rho)+Sf-Sf0]. No field boundary stress is set to
   zero. Sf-Sf0,mf=O(e) throughout I imply Fm=O(e^2), but do not imply
   total momentum conservation. Section 5 uses the exact equivalent fluid
   balance, so it requires no unsupported cancellation of field stresses.

6. **Full energy and zero-velocity control — passed.** Fluid plus n phi
   contributes +np; Q contributes -np-Tscale w/C; scale contributes
   +Tscale w/C. Both -pA/C and -Jwk/C fluxes are present. At A,D the field
   flux is O(e), generally nonzero, and fluid flux is O(e^2). The moving
   interval rule adds beta' h(beta)-alpha' h(alpha), giving -S times the
   endpoint sum on the shrinking cone. No such integral is called conserved
   and no coercivity is used. With V=0 separately, H solves all equations,
   flux vanishes and the positive-momentum contradiction is absent.

7. **Fresh lower-time construction and exact joins — passed.** The pinned
   FGF051 Section 4 explicitly constructs a C1/C1,1 solution by frozen
   transport iteration, C0 contraction and derivative interpolation, and
   permits compatible restart. The author uses that construction, not its
   old N-dependent horizon. Fresh Pscale=V/e estimates close fluid gradients
   O(Pscale), field gradients O(1), and the complete derivative-Lipschitz
   seminorm O(Pscale^2) through kappa/Pscale. The exact join contribution is
   8V/e^2=(8/V)Pscale^2; no smoothing or classical f'' at a join is used.
   All constants are fixed in e. For each e, the weak derivative of the PDE
   bounds (U_X)_t, furnishing actual compatible C1 traces and a restart,
   rather than assuming continuation from formal norm bounds. Compatibility
   chi_X=k and phi_X=g follows from the diagonal equations and persists in
   the trace. S>Slo, initial Hrad e<R, and the shrinking cone ensure the
   auxiliary whole-line solution restricts to precisely the cone of the upper
   argument. No matching to H after field arrivals, no double potential-gauge
   matching, and no old maximal-germ equivalence are claimed or needed.

8. **Quantifiers and physical scope — passed.** Uniformity is only in small
   epsilon at fixed finite parameters; neither infinite-speed limits nor
   physically calibrated values are asserted. Both a0 normalizations and
   their backgrounds are separate, as are constant-vacuum and individually
   frozen a0 E(z) histories. Evolving reference, RAR/M/filtered-MONO
   substitutions, physical closure, maximal endpoint and sharpness claims
   are explicitly excluded. A failure of the sufficient cell is not a
   refutation of the PDE or framework.

## Source and executable checks

Read-only `verify_metadata.py` was inspected in full before execution. It
imports hashlib,json,pathlib,re; reads the pinned files; checks field presence,
input/output/manifest/freeze hashes and inventory; and prints results. It
performs no writes or mathematical computation. Executed:

    python3 deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-055/fgf055_run_001/verify_metadata.py

Observed: PASS for ten ancestry pins, all source/output/manifest/freeze hashes,
required fields and exact inventory. The proof/result digests printed matched
the supplied pins. This validates provenance only. The inequalities, signs,
geometry and local construction were audited analytically above. No numerical
sample, test of a discretized PDE, library install, service, or external-source
query occurred. Only this audit and its JSON result are written after exposure.

## Safe statement and next action

The author's exact bounded theorem is supported with the existing coefficient,
domain and regularity scope. Its Section 6 small matter orders must explicitly
refer to the exterior wedges/endpoints. Freeze the minimal clarification and
recheck that exact changed sentence and new provenance; a mathematical rerun
or a broader research program is not needed. The original independent proof
and pins remain immutable. A new maximal-domain/endpoint or physical-model
claim remains outside this review.
