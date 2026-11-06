# AC16: v3s / AC2q nonlinear well-posedness: FAIL (classical, generic data); well-posed on each branch

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: FROZEN_CRITERIA.md (0d4b7bc237),
frozen before any graded number. Script: ac16.py (sympy plus a small Lagrangian scheme; about 4 s, one thread).
This replaces AZ35's NO VERDICT with a label on a precisely stated claim. The system is the PN label system
of AC10, which is the same for v3s (s = 0) and AC2q (charge Pi = D.P + s^2).

## Result

- **C1, soft branch (switch off): PASS.** In (P, v) the principal part is v times the identity, and the
  gravity and W terms are of order zero. Before shell crossing each label obeys its own ODE, and the
  enclosed charge is constant on a label. So the system is locally well-posed in H^s x H^s (s > 3/2), with
  lifespan equal to the first fold J = 0. This is the nonlinear version of AZ35's polarization repair.
- **C2, stiff branch (Pi > 0, switch on): PASS.** A = [[v, Pi], [gamma, v]] is symmetrized by
  H = diag(gamma, Pi), with H A - A^T H = 0 exactly. The speeds v +- sqrt(gamma Pi) are real, so the branch is
  strictly hyperbolic and locally well-posed in H^s while Pi >= Pi_min > 0. It is a gamma-law gas with
  exponent 2, since the force -gamma Pi_x comes from the pressure gamma Pi^2/2.
- **C3, across the switch: FAIL of classical well-posedness.** If the data cross D.P = 0 transversally
  (Pi = 0 with Pi_x != 0 there), no C1 solution exists on any interval [0, T), T > 0. For C1 velocity,
  D_t v is continuous, but the force -gamma d_x max(Pi, 0) jumps by -gamma Pi_x at the interface; the other
  terms are continuous. The sympy check reproduces the jump exactly. The same argument holds in 3D. This is
  AZ35's "C1 but not C2" interface, made into a no-go.
  - Numerics (gamma = 1, labels in [-3, 3], N = 400 to 3200): the velocity jump across the interface at
    t = 0.1 is -0.09970, against the leading-order prediction -0.1 (N3a). It is stable in N to 3e-6.
  - The first crossed cell appears at t = 0.209, 0.147, 0.104 and 0.074. Each doubling of N divides that
    time by 1.42, 1.41 and 1.42, against the predicted sqrt 2 (N3b): crossing is immediate in the continuum.
  - Control N3d (compatible data, Pi_0 = tanh^3, Pi_x = 0 at the interface): the jump is -7.5e-4, which is
    0.75 % of N3a and falls with N. No crossing occurs before t of about 1, so the detector separates the two
    classes.
- **Compatible class.** Classical solutions can exist only where Pi_x = 0 at the switch. Transport preserves
  that class exactly (sympy). Planar static solutions lie in it. Whether a classical theory exists there is
  not decided; the near-interface sound speed vanishes linearly, a degenerate-vacuum problem.

**Label for the closure row: FAIL (classical, generic data).** Smooth data with a transverse D.P = 0
interface fold at once at the interface, in v3s and AC2q alike. The theory is well-posed on each branch away
from the switch. This closes AZ35's route 3 as a negative result. Routes 1 and 2 are answered by C1 and C2,
and by the first fold J = 0 already known from X14 and AC10.

## A frozen line missed (kept on the record)

N3c (stiff side on the left) was frozen with the prediction "D -> +0.1 (opening)". The run gives D = -0.0997,
and cells cross at the same times as in N3a. The frozen sign was wrong. The stiff side's pressure always
pushes it into the soft side, whatever the orientation, so both orientations overlap; neither opens a gap.
This is a post-run reading. It strengthens C3: the interface crosses at once in both orientations. Under the
frozen line, N3c is a FAIL, and the run label carries "[C3 numerics not fully confirming]" for that reason.
The analytic theorem and N3a, N3b and N3d do not depend on it.

## Controls

- MUTATE (`AC16_MUTATE=1`, outputs ac16_MUTATE.*): with gamma -> -gamma, H is not positive and the speeds are
  complex, so C2 fails and the script exits 1. The control bites.
- Rerun: ac16.json is byte-identical (sha1 df2169023963).

## What it does not show

The system is the PN one, as in AC10, H4 and AZ35; the full covariant system is not graded. The FAIL is about
classical (C1 / H^s) solutions. Weak solutions with shocks or multistream continuation across the switch
might exist, but they would be a different, larger claim about the theory, not tested here. The numerics drop
the zero-order K terms (continuous, absent from the jump at leading order). No data are graded and no
constant is derived.
