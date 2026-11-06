# AC16 frozen criteria: a final label for v3s's (and AC2q's) nonlinear well-posedness

Frozen before any script producing a graded number exists. Kappa = 1/2 FITTED; not theory closed.
Adopts nothing. No dark-matter particle. Both footings: they only set unit scales here (as in AZ35),
so the dimensionless results are stated once and hold on both.

## Why

AZ35 (astra_goal_2026_11_05/AZ35_nonlinear_wellposedness, criteria db530f4da0) reached NO VERDICT. It
found that the soft branch's density/velocity norm grows linearly in k, but polarization/velocity
variables remove that growth. It left three routes open: (1) a nonlinear energy estimate, (2) the
characteristic caustic with forces kept, and (3) the moving D.P = 0 interface, where the action is C1
but not C2. AC16 settles a precisely stated version of each, to a PASS or FAIL.

## System (the record's own)

This is the PN label system of AC10's FROZEN_CRITERIA (552db86f89), checked symbolically by AC10's
s1_reduction.py (E1-E4). In planar symmetry, with v = -sigma_x:

    Pi_t + (Pi v)_x = 0,         P_x = Pi - s^2,
    v_t + v v_x = K M P - gamma d_x max(Pi, 0) - phi_x,     phi_xx = K(rho_b + Pi - s^2).

Here v3s is s = 0 with Pi = D.P. AC2q has Pi = D.P + s^2, with s^2 constant at PN order (AC10 S1). The
three-dimensional PN analogue replaces d_x with grad, with the same stiffness force -gamma grad max(Pi, 0)
(the P Euler-Lagrange equation, then the Euler identity D_t v = grad Xi - grad phi; AC10 E2).

## Claims graded

C1 (soft branch, Pi < 0 throughout, switch off). In (P, v) the principal part is v d_x times the identity.
The terms K M P and phi_x are of order zero (P = d_x^-1 of a transported density). Before shell crossing the
system is a family of independent per-label ODEs. Claim: local well-posedness in H^s x H^s for s > 3/2
(Kato-Majda quasilinear symmetric-hyperbolic theorem). The lifespan equals the first fold, J = 0.
- Graded, sympy: the principal matrix in (P, v) is v I. The per-label ODE closes: enclosed charge is constant
  on a label before crossing (residual 0).

C2 (stiff branch, Pi >= Pi_min > 0 throughout, gamma > 0). In (Pi, v) the principal matrix is
A = [[v, Pi], [gamma, v]], and H = diag(gamma, Pi) symmetrizes it (H A = A^T H). H > 0 if and only if
gamma Pi > 0. The speeds are v +- sqrt(gamma Pi). Claim: strictly hyperbolic, with local well-posedness in
H^s, s > 3/2.
- Graded, sympy: H A - A^T H = 0 exactly. The eigenvalues are real if and only if gamma Pi >= 0.

C3 (across the switch: the decisive claim). Suppose the data have a transverse switch interface: Pi(x*) = 0
and d_x Pi(x*) != 0. Then no C1 solution (v in C1, Pi in C1) exists on [0, T) for any T > 0. The proof is one
line. If v is C1, then D_t v = v_t + v v_x is continuous in x. But the right-hand side jumps at x* by
-gamma d_x Pi(x*+) != 0, because d_x max(Pi, 0) jumps, while K M P and phi_x are continuous. Continuity
keeps Pi's transverse zero for small t. The same argument holds in 3D (normal component of grad Pi).
Corollary, stated now: classical solutions can exist only on the compatible class, where d_x Pi = 0 at the
interface. Transport preserves that class, since Pi = Pi_0(a)/J with Pi_0'(a*) = 0. Planar static solutions
lie in it: there max(Pi, 0)_x = (K M P - phi_x)/gamma is continuous.
- Graded, sympy: the force jump equals -gamma Pi_x(x*) exactly, and the transport-preservation identity
  d_x Pi = J^-2 Pi_0' - Pi_0 J^-3 J_a gives 0 at a* when Pi_0'(a*) = 0.
- Graded, numerically (Lagrangian staggered scheme, gamma = 1, K = 0, since the zero-order continuous terms do
  not enter the jump at leading order; v_0 = 0, labels a in [-3, 3]):
  * N3a (transverse, stiff on the right, Pi_0 = tanh a): the jump D(t) = v(a = +h) - v(a = -h), with h = 0.05
    fixed, at t = 0.1. Across N = 400, 800, 1600, 3200 cells, D must converge (relative change between the
    last two rungs <= 2 %) to within 15 % of the leading-order prediction -gamma Pi_0'(0) t = -0.1 (h and O(t^2)
    corrections allowed for). It must not shrink with N.
  * N3b (the same data): the first time any cell inverts (X_{i+1} <= X_i) near the interface must fall with N,
    with doubling ratios t(N)/t(2N) in [1.2, 1.7] (predicted sqrt 2: overlap -t^2/2 against cell width ~ 1/N).
  * N3c (transverse, stiff on the left, Pi_0 = -tanh a): D at t = 0.1 converges to a positive value within 15 %
    of +0.1 (opening). Reported as the rarefaction side: v is Lipschitz but not C1.
  * N3d (control, compatible data Pi_0 = tanh(a)^3, which has Pi_0'(0) = 0): |D| at t = 0.1 must fall with N,
    with the last rung < 0.1 x |D| of N3a, and the time of the first inverted cell must not fall by the N3b
    ratio. If N3d behaves like N3a, the detector cannot tell the two classes apart and C3's numerics give no
    verdict.

## Lines

- C1, C2 PASS: the stated sympy identities hold.
- C3 FAIL-of-classical-well-posedness established: the sympy identities hold, N3a-N3c are within their lines,
  and N3d (control) separates.
- Overall label for the closure row, stated now:
  * if C1, C2 and C3 all hold: **FAIL (classical, generic data)**. v3s and AC2q are not classically
    well-posed for data with a transverse switch interface. They are well-posed on each branch away from it.
    Whether a classical theory exists on the compatible class, or a weak/entropy theory across the switch,
    stays outside this label.
  * if C3's numerics miss but its sympy holds: the analytic FAIL stands, with the numerics reported as not
    confirming.
  * if C1 or C2 fails: report that branch as FAIL as well.

## Controls (separate outputs)

- MUTATE (`AC16_MUTATE=1`): flip gamma -> -gamma. C2's hyperbolicity check must fail (the speeds become
  complex for Pi > 0; H is not positive). If it does not, C2 has no power and its PASS does not stand.
- N3d above is C3's power control.

## Scope stated now

PN order, as in AC10, H4 and AZ35. The full covariant (GR plus khronon) system is not graded. A FAIL here is
about classical (C1/H^s) solutions only; it does not rule out weak solutions with shocks, which would
be a different theory claim. AC16 grades no data, derives no constant and adopts nothing. Run: one
thread, nice -n 15.
