# Checkpoint: a balanced responsive-scale slab

2026-09-30, 03:22 UTC heartbeat pass. Parent: [stage eight](../stage_08/README.md).
The objective remains open. This pass addresses the artificial-background gap
in FGF-014 by deriving a finite slab with genuine hydrostatic matter balance
and a spatially varying scale field. It is a proof-only investigation of the
inherited Q/R diagnostic action, not the operative filtered-MONO metric theory.

## Exact changed premise

With C=4piG and a=a_ref exp(chi), the equilibrium obeys

    B'=C rho,   cs² rho'=-rho F(B,a),
    chi'=w,    J w'=U'(chi)-T(F(B,a),a),
    phi'=F(B,a).

There is no density subtraction or acceleration canceler. Smooth local ODE
existence with B_i,rho_i,w_i>0 and chi_i=0 gives a short interval with positive
matter density and nonconstant density and scale. Field endpoint values and
wall pressures are induced by that solution; arbitrary preassigned physical
boundary values, an isolated centered slab and the g=0 limit are not solved.
The endpoint flux difference equals C times the actual slab mass.

## Why the old stability proof needed correction

Let lambda=b_g, q=g lambda-B, m=U''-T_chi and M=m-q²/lambda. The complete
quadratic potential with fixed-wall perturbations xi=psi=eta=0 is

    2V = integral {cs² rho xi'²
         +lambda/C [psi'+(C rho xi-q eta)/lambda]²
         +J eta'²/C +M eta²/C
         +(rho q/lambda)(chi' xi²+2xi eta)} dx.

The integration boundary term is [cs²rho'xi²-2rho xi psi], which vanishes
for those walls. The last two coupling terms cannot be omitted. For the
inherited cosh potential, the nonuniform identity is

    M=S0 exp(-2chi)+Bq/lambda+2J chi''.

The positive uniform-background field identity therefore cannot simply be
transferred. Freezing eta alone leaves the chi' term. Setting eta=0 and
chi'=0 recovers the old fixed-scale algebra, but generally not an actual
finite-J, varying-density Q/R equilibrium of this responsive-scale action.

A sufficient Poincare bound compares the positive gradient terms with these
lower-order couplings. On sufficiently short nondegenerate patches the bound
is strictly positive. The kinetic quadratic form is positive by its stated
coefficient assumptions, and the full perturbation-energy boundary flux
vanishes at the fixed walls. This supplies conditional longitudinal linear
stability for a nonempty family of balanced slabs. No numerical spectrum was
needed or claimed; failure of the sufficient inequality is inconclusive.

## The field boundary condition survives static elimination

For f=C rho xi-q eta, static minimization over Dirichlet psi gives a residual

    [integral f/lambda dx]² / [C integral1/lambda dx].

The minimizing flux is a constant fixed by integral psi'=0. Setting the
completed square pointwise to zero would generally violate the second wall.
A sine displacement fixture makes this failure explicit. This reduction is
static; the two fields remain dynamical when their kinetic coefficients are
positive. Further scale-field elimination must retain the complete boundary
operator and its positivity/invertibility conditions.

## Evidence, limitations and next step

The root independently derived the Hessian and bound while the FGF-023 author
worked in a separate scope. A separate agent audited root's proof, density
mass constraint, endpoint terms and Dirichlet reduction. See
[scoped reconciliation](../../deepseek_push/astra_spawn_ideas/fresh_gravity_followups/reviews/FGF-023_RECONCILIATION.md),
[root derivation](slab_audit/ROOT_DERIVATION.md),
[wall reduction](slab_audit/DIRICHLET_REDUCTION.md),
[independent audit](slab_audit/INDEPENDENT_AUDIT.md), and
[coordinator receipt](COORDINATOR_VERIFICATION.json).
This pass has analytic evidence and source hashes, not a new numerical manifest.

Both a0 normalizations and separate constant-vacuum versus frozen H(z)
comparison families remain explicit. The source uses Q or R MOND flux; no
registered M action is invented. The actual local scale varies: compatibility
with a literal pointwise constant-vacuum scale relation remains unresolved.
No metric/photon coupling, 3D/nonlinear stability or empirical acceptance follows.

The next continuation must separate loss of the sufficient short-domain bound
from an actual negative-energy direction on a specified longer equilibrium.
Preserve wall compatibility in the reduced operator. FGF-024's pressure
information task remains separately ready. The AS228 repair remains with its
acknowledged primary owner; unchanged primary return inventory was not reaudited.

FGF-025 records that longer-slab continuation as an unlaunched task. The queue
has 25 tasks: twelve reviewed_scoped and thirteen ready. Both actual agents
completed; no FGF worker running. The peer acknowledged AS228 ownership and
was sent this checked proof; no completed metric repair is claimed.
