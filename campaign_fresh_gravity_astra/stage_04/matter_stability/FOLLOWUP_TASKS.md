# Three bounded follow-ups for coordinator dispatch

These are task specifications, not executed claims. They depend on the
finalized MS1 `DERIVATION.md` and its checked constitutive conventions.
Use separate task output directories; preserve failed runs and actual input
hashes. No literature searches, global cosmology claims, or field-only
substitutes for coupled dynamics.

## F1 — independent background and boundary audit

**Question:** do the recorded finite slabs and proposed perturbation boundaries
define the coupled problem used by F2 without assuming a locally homogeneous
unstable window?

Take the recorded isothermal slab on 0<=x<=L with p=cs² rho, g=phi'>0,
constant a, and b(g)=F^(-1)(g) for Q/R. Its equations are

    cs² rho' = −rho g,
    b'(g) g' = 4 pi G rho.

In chi=x a/cs², u=B/a, r=4piG cs² rho/a², they are

    u_chi=r, r_chi=−r f(u), f(u)=F(a u;a)/a.

Read the four accepted samples in MS1 `run_003/results.json`: Q/R,
initial B/a in {.01,1}, initial r=.1 and chi_max=1. Reconstruct their
equilibrium independently using at most four integrations. Convert starting
B to g with the appropriate F. Verify positivity, residuals and units.

Independently prove or refute kJ² Lrho Lg=1, with
Lrho=|rho/rho'|, Lg=|g/g'| and kJ²=4piG rho/(cs² b'(g)). The manuscript
concludes that k<kJ cannot satisfy k min(Lrho,Lg)>>1; do not assume that
conclusion in the review. Check whether impermeable displacement xi=0 and
scalar psi=0 at both walls produce F2's self-adjoint quadratic form without
discarded boundary-source terms. Trace required wall pressure/flux support;
do not describe the slab as an isolated finite-mass object.

**Decisive controls:** zero density leaves constant g. Independently check
r+integral_(u_initial)^u f(v)dv=r_initial. Changing K in {2,8} must leave
equilibria unchanged. Failure of a local unstable window is useful negative
evidence, not a failed equilibrium solve.

**Pass criterion:** independently confirm the assumptions or provide a minimal
counterexample. Do not infer global stability. Identify an accepted background
for F2 and any necessary correction to its boundary formulation.

## F2 — coupled eigenproblem on one accepted slab

**Depends on:** a recorded MS1 background confirmed by F1, with rho>0 and g>0.
Use its actual rho(x), A(x)=b'(g(x)); do not replace them by constants.
Let displacement xi vanish at the two impermeable walls, and scalar
perturbation psi obey homogeneous Dirichlet data. Define

    delta rho = −(rho xi)',
    xi_tt = −[cs² delta rho/rho + psi]',
    (K/c²) psi_tt −(A psi')' = −4 pi G delta rho.

Derive the discrete equations from the quadratic form rather than discretizing
the products independently:

    E2 = integral [rho xi_t²/2 + cs²(delta rho)²/(2rho)
                  +(K/c²)psi_t²/(8piG)
                  +A psi'²/(8piG)+delta rho psi] dx.

Test K in {2,8} at a declared fixed cs/c, or equivalently the scalar inertia
eta=K cs²/c² in {.01,.04}; never interchange these without recording units.
Use grids of 64,128,256 interior nodes and at most one Q and one R background.
Solve the symmetric generalized eigenproblem. Return the smallest ten
omega² values, eigenfunction samples, mass-matrix signs and convergence.

**Decisive controls:** remove the cross term and recover two positive
Dirichlet sectors; as a separate periodic-boundary control use constant rho,A
in the supported/subtracted problem and recover MS1's dispersion with xi sine
and psi cosine;
check Rayleigh quotients and the discrete quadratic energy. For the actual
slab, show whether a negative eigenvalue converges or disappears on refinement.
Changing K should change rates, while any zero-frequency crossing under a
separate static parameter continuation should not depend on K.

**Pass criterion:** sign-stable converged low eigenvalues with a symmetric
positive kinetic matrix and correct boundary treatment. A negative mode is
a conditional finite-slab result, not proof that every observed system collapses.

## F3 — quantify when a dynamic rate can identify K

**Question:** how much calibration precision is needed to distinguish K=2
from K=8 using a slow coupled mode, compared with a resolved scalar branch?
Use only MS1's explicitly supported/subtracted toy model.

For each Q/R branch, B/a in {.001,.01,.1,1}, theta in {0,pi/2}, cs/c in
{1e-4,1e-3,.1}, K in {2,8}, and k/kJ in {.3,.5,2}, compute x_± from (M2)
using a cancellation-safe root. Keep 4piG rho0 fixed in a declared time unit.
At fixed physical k, perturb rho0, cs² and L independently by ±1e-4 and
compare finite-difference sensitivities with implicit differentiation of

    (x−cs²k²)(Kx/c²−Lk²)=4piG rho0 k².

Do not change k when differentiating a nuisance parameter just because its
derived kJ changes. Compare hypothetical independent 0.1%,1%,10% calibration
errors, explicitly as synthetic scenarios. For two resolved modes use the
trace inversion K=c²L/[(x_++x_-)/k²−cs²]; for a single nonzero mode also
include density calibration as in (M10).

**Decisive controls:** static threshold and static susceptibility must have
zero K derivative; direct K inversion on noiseless pairs must recover inputs;
finite-difference derivatives must converge when step is halved; reject
threshold modes x=0 as singular single-mode inversion cases.

**Pass criterion:** a compact conditioning table separating formal
identifiability from sensitivity overwhelmed by declared nuisance uncertainty.
Do not describe these invented precision scenarios as observational priors,
a forecast, or a measured bound on K.
