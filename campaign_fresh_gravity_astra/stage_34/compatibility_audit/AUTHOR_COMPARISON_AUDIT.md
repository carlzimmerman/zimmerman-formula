# FGF047 narrow independent compatibility and energy audit

Primary verdict: **proved as written**, scoped ONLY to the following normalized
claim. For any C1 solution of the author's characteristic system (10), staying
in its positive g, positive n coordinate patch and carrying compatible initial
field gradients, reconstruction gives the original Q/scale/fluid equations,
propagates both gradient constraints, retains the dynamic MOND source, and
satisfies the full fixed-reference local energy law. The stationary hydrostatic
zero-velocity tuple solves the original equations and has zero energy flux.

This is not an independent verdict on the author's full local existence,
iteration, lifespan, uniqueness, or exterior-independence theorem. Those claims
remain outside this review even though the complete author document was loaded.
In particular identifying the constructed zero-velocity solution with the
stationary tuple relies on the separate uniqueness argument, not certified here.

## Exact targets and independence

Author target:
`deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-047/fgf047_run_001/DERIVATION.md`
SHA256 `1f11fd635d50a36b6cc747187595b26ebd1f4d2c4e19b9ee58c024cc5b47cf7a`.
The corresponding `result.json` is pinned at
`bbc88bd9ea34282728fd620b7973a1a329b80ffceccd8d611242a1a5adbb43ad`.
Both supplied target hashes matched before author exposure for this comparison.

The independent route was frozen beforehand at
`campaign_fresh_gravity_astra/stage_34/compatibility_audit/INDEPENDENT_DERIVATION.md`,
SHA256 `d7f9f0855671329ea79b511a8ece35b776675f8681a9b8decd908633d66e3ffe`.
`independent_freeze.json` records its freeze time, input manifest hash and lack
of author/new-reviewer exposure at freeze. Neither frozen artifact was revised.
No other new reviewer proof was read. The author uses b for scalar wave speed,
h for its primitive, w for scale velocity, and q for log density; the independent
route uses c,H,q,r, respectively. This notation translation is essential.

## Dependency graph

Pinned FGF032/023 action and task definitions -> exact Q derivatives and wave
speed positivity -> local invertibility of characteristic coordinates -> full
chain rule including h_chi -> off-constraint reconstructed equations -> homogeneous
gradient-defect propagation -> original dynamical source and field equations ->
matter, Q and scale energy exchange cancellation. The stationary control follows
directly from the pinned hydrostatic equations. No external mathematical source,
PDE existence theorem, numerical surrogate or literature mechanism is a leaf.

## Obligation matrix

| Obligation | Status | Exact author locator and comparison |
|---|---|---|
| Q derivatives and positive scalar speed | passed | (1),(2),(7): B_g=2g/sqrt(a^2+4g^2), B_chi=(a^2/sqrt(a^2+4g^2)-a)/2 |
| Local invertible coordinate map | passed | (8),(9): h_g=b>0; fluid and scale inverses use cs,d>0 only |
| Chi-dependent scalar wave coordinates | passed | (10): both h_chi w and -b h_chi k terms present with correct signs |
| Off-constraint scalar reconstruction | passed | (12): +b h_chi(chi_x-k) retained before imposing compatibility |
| k=chi_x propagation | passed | (11), k_t=w_x and chi_t=w; direct time integration, no second spatial derivative of w needed |
| g=phi_x propagation | passed | (12),(13), g_t=p_x before use of k=chi_x; same time-integral argument |
| Original coupled source, no static substitution | passed | Sections 2,3: B_x=Cn+tau phi_tt after compatibility |
| Coincident characteristic speeds | passed | (9),(10): no differences of characteristic speeds enter the coordinate inverse |
| Evolving matter-interaction energy | passed | (30), Section 8: +np after cancellation of +/-nvg |
| Q and scale exchanges and both fluxes | passed | (31),(32): -np-Tw/C and +Tw/C; fluxes -pB/C and -Jwk/C |
| Total local energy and moving endpoints | passed | (33),(34): exact cancellation and correct endpoint transport signs |
| Hydrostatic stationary tuple | passed | (3), Section 8: n=rho,v=p=w=0 solves all four original equations with zero flux |
| Identification of constructed control by uniqueness | not addressed | Depends on Section 7 uniqueness theorem, beyond this narrow audit |
| Complete iteration, C1,1 estimates and classical limit | out of scope | Sections 4-6 not independently audited |
| Lifespan, coefficient-margin propagation, uniqueness and extension independence | out of scope | Requires full existence/localization review |
| Crossing/walls/global results and physical theory closure | out of scope | No such conclusion authorized or inferred |

## Decisive algebra and negative controls

Let eta=k-chi_x and xi=g-phi_x. Adding and subtracting the two scalar
characteristic equations, without setting eta=0, gives exactly

  g_t=p_x,
  p_t=b^2 g_x+A-b h_chi eta.

This is the author's (12) and the independently frozen formula. The scale
pair gives k_t=w_x; chi_t=w then gives eta(t,x)=eta(0,x), while reconstruction
of phi yields xi(t,x)=xi(0,x). All uses of vertical time integration require
the vertical segment to remain in the domain, as stated in author Section 7;
for the conditional local identity one restricts to such a domain.

The author's first-order display (6) is a compatible-state lift, not an
assertion that its p equation is the exact off-constraint inverse of (10).
Section 3 explicitly supplies and cancels the extra feedback term. Thus no
missing constraint-feedback term or sign correction is needed in this package.

A stringent independent off-constraint check, not required as an additional
author claim, is

  B_x=Cn+tau p_t-(B_chi-tau b h_chi)eta,
  E_t+F_x=-nv xi+[p(B_chi-tau b h_chi)/C]eta.

Both reduce to the author's identities precisely when compatibility has been
proved. This distinguishes their chosen diagonal extension from the baseline
lift in (6), which has a different off-constraint residual.

The negative control frozen before author exposure deletes both h_chi sources.
It gives g_t=p_x-h_chi w/b, which generally fails gradient propagation. The
author retains those terms. The stationary nonconstant-chi control separately
requires -b h_chi k: Rplus=h, Rminus=-h have transport left sides -b h_x;
hydrostatics gives A=-b^2 g_x, so their sources A-b h_chi k agree exactly.
This checks the source dependence even when w=0.

For energy, e+pressure=cs^2 n log(n/nref), so the author's compact matter
flux nv[v^2/2+cs^2 log(n/nref)+phi] is precisely
(E_m+pressure+n phi)v. Thus there is no missing -cs^2 n term. Multiplying
the two field equations by their velocities and using W_chi=-T gives the
separate exchanges in (31),(32), with the stated negative field-flux signs.
Leibniz differentiation produces +beta' E(beta)-alpha' E(alpha), confirming
(34) including the two negative S terms for the shrinking interval.

The last initial-slice diagnostic in Section 8, tau p_tt=C(rho v_in)_x,
has the correct sign wherever the indicated derivatives exist: p_t is
initially zero, and differentiating tau p_t=B_x-Cn gives -C n_t because
initial g_t=p_x=0 and chi_t=w=0. The author explicitly makes this diagnostic
conditional on those derivatives and does not use it in the construction.
This audit does not supply extra third-derivative regularity at the joins.

## Source and execution checks

Both FGF032 and FGF023 ancestry hashes match the task pins; these source
identities and the task/common contracts are in the frozen input manifest.
Author target hashes were verified with Python hashlib SHA256 and exact
assertions. Artifact writing and hash checks are administrative operations;
no mathematical executable computation was run and no numeric sampled range
is claimed. No network, install, service, commit, outside-scope write, external
source lookup, or new-reviewer proof read was used.

## Remaining gap and strongest safe conclusion

There is no missing implication within the normalized conditional algebra,
compatibility and energy claim audited above. Existence of a sufficiently
regular diagonal solution and the author's quantitative construction require
a separate full review; this narrow certificate must not be promoted to that
review. The cheapest next check is the already distinct independent audit of
the iteration and its derivative-limit and localization arguments.

Both positive reference normalizations are separate fixed backgrounds. This
energy proof does not cover an evolving external H/reference protocol, and
neither an actual varying diagnostic scale nor this local identity establishes
pointwise vacuum closure, two gravitational DOF, M/filtered-MONO transfer,
metric/photon dynamics, clusters, cosmology, global evolution or novelty.
