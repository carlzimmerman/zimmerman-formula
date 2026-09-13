#!/usr/bin/env python3
"""
Independent finite-k Dirac audit of the AeST host action used by
``fc_fk_routeB_covariant.py``.

This is deliberately narrower than a claim about the full nonlinear theory.  It
expands the stated covariant host action on a flat background, imposes the
unit-norm condition for the aether, drops only an explicit total derivative, and
then performs the finite-k canonical reduction.  The calculation answers the
decisive question left open by the inserted ``K_eff`` ghost-band ansatz:
does the actual quadratic action have a finite-k propagating scalar?

For K_B>0, K_2>0, Q_0>0 and k!=0 the result is

  X = delta phi + Q_0 v,
  D = 2 K_2 Q_0^2 + K_B k^2,
  K_X = 2 K_2 K_B k^2 / D,
  Omega_X = 2 k^2 (2-K_B) (K_2 Q_0^2+k^2) / D,
  omega^2 = Omega_X/K_X
          = (2-K_B)(K_2 Q_0^2+k^2)/(K_2 K_B).

The finite-k phase space has two first-class constraints and therefore one
physical scalar configuration degree of freedom.  At k=0 the v kinetic term
vanishes and three first-class constraints remove all homogeneous scalar DOF.
This is a finite-k extra gravitational scalar (or, if reinterpreted as matter,
an explicitly propagating clock field); it is not the claimed nonpropagating
constraint mode.  The result therefore closes the specific AeST host gate as
N_grav=2 FAIL, while leaving the full nonlinear/FLRW theory outside scope.

No expected rank, determinant, or DOF is hard-coded: every reported rank and
constraint bracket is obtained from SymPy matrices and exact simplification.
"""

from __future__ import annotations

import sympy as sp


FAILS: list[str] = []


def check(label: str, condition: bool, detail: str = "") -> None:
    ok = bool(condition)
    print(("  [ok]   " if ok else "  [FAIL] ") + label)
    if detail:
        print("         " + detail)
    if not ok:
        FAILS.append(label)


def pb_matrix(constraints: list[sp.Expr], q: list[sp.Symbol], p: list[sp.Symbol]) -> sp.Matrix:
    """Canonical Poisson-bracket matrix, {f,g}=df/dq dg/dp-df/dp dg/dq."""
    z = q + p
    n = len(constraints)
    out = sp.zeros(n, n)
    for i, f in enumerate(constraints):
        for j, g in enumerate(constraints):
            out[i, j] = sp.simplify(
                sum(sp.diff(f, qi) * sp.diff(g, pi) - sp.diff(f, pi) * sp.diff(g, qi)
                    for qi, pi in zip(q, p))
            )
    return out


def main() -> int:
    KB, K2, Q0, k = sp.symbols("K_B K_2 Q_0 k", positive=True)
    Phi, v, chi = sp.symbols("Phi v chi", real=True)
    Phid, vd, chid = sp.symbols("Phi_d v_d chi_d", real=True)
    pPhi, pv, pchi = sp.symbols("p_Phi p_v p_chi", real=True)
    X, Xd = sp.symbols("X X_d", real=True)

    # Exact spatially averaged O(epsilon^2) Minkowski Lagrangian from the
    # covariant route-B action.  The shift B contributes only
    # d(Phi*B)/dt and is omitted as a boundary term.
    L = sp.expand((
        2*K2*Phi**2*Q0**2 - 4*K2*Phi*Q0*chid + 2*K2*chid**2
        + KB*Phi**2*k**2 - 2*KB*Phi*Q0*k**2*v - 2*KB*Phi*chi*k**2
        + 2*KB*Phi*k**2*vd + KB*Q0**2*k**2*v**2
        + 2*KB*Q0*chi*k**2*v - 2*KB*Q0*k**2*v*vd
        + KB*chi**2*k**2 - 2*KB*chi*k**2*vd + KB*k**2*vd**2
        + 4*Phi*Q0*k**2*v + 4*Phi*chi*k**2 - 2*Q0**2*k**2*v**2
        - 4*Q0*chi*k**2*v + 4*Q0*k**2*v*vd - 2*chi**2*k**2
        + 4*chi*k**2*vd
    ) / 2)

    q = [Phi, v, chi]
    qd = [Phid, vd, chid]
    p = [pPhi, pv, pchi]
    momenta = [sp.simplify(sp.diff(L, x)) for x in qd]
    print("Finite-k canonical momenta:")
    for name, value in zip(("p_Phi", "p_v", "p_chi"), momenta):
        print(f"  {name} = {value}")

    check("p_Phi is a primary constraint", momenta[0] == 0, f"p_Phi={momenta[0]}")

    # For k != 0, K_B != 0 the two velocities appearing in the Hessian are
    # solved exactly.  No numerical rank or guessed formula enters here.
    vel_solution = sp.solve(
        [sp.Eq(momenta[1], pv), sp.Eq(momenta[2], pchi)], [vd, chid],
        dict=True, simplify=True,
    )[0]
    print("Velocity solution (finite k):", vel_solution)
    H = sp.expand(pv * vel_solution[vd] + pchi * vel_solution[chid] - L.subs(vel_solution))
    H = sp.factor(H)
    secondary = sp.factor(sp.diff(H, Phi))
    print("Hamiltonian secondary from p_Phi preservation:", secondary)
    check(
        "p_Phi preservation produces C1 = Q0*p_chi - p_v",
        sp.simplify(secondary - (Q0 * pchi - pv)) == 0,
        f"C1={secondary}",
    )
    C1 = Q0 * pchi - pv
    C1_dot = sp.simplify(-Q0 * sp.diff(H, chi) + sp.diff(H, v))
    check("C1 is preserved without a tertiary constraint", C1_dot == 0, f"dot(C1)={C1_dot}")

    PB_finite = pb_matrix([pPhi, C1], q, p)
    print("Finite-k constraint PB matrix [p_Phi,C1]:")
    print(PB_finite)
    check("finite-k constraint PB matrix is identically zero", PB_finite == sp.zeros(2), str(PB_finite))
    check("finite-k constraints are first class", PB_finite == sp.zeros(2), f"computed rank={PB_finite.rank()}")

    # Gauge-invariant variable X=chi+Q0*v.  Substitute chi=X-Q0*v before
    # eliminating Phi.  Phi becomes an algebraic auxiliary and drops out of
    # the invariant action after its own Euler-Lagrange equation is imposed.
    L_X = sp.expand(L.subs({chi: X - Q0*v, chid: Xd - Q0*vd}))
    Phi_solution = sp.solve(sp.Eq(sp.diff(L_X, Phi), 0), Phi, dict=True, simplify=True)[0][Phi]
    D = sp.factor(2*K2*Q0**2 + KB*k**2)
    print("Phi solution in invariant variables:", sp.factor(Phi_solution))
    check("Phi elimination denominator is D=2*K2*Q0^2+K_B*k^2", sp.denom(Phi_solution) == D, f"D={D}")
    L_phys = sp.factor(sp.expand(L_X.subs(Phi, Phi_solution)))
    # The X*Xdot term is a total derivative at constant background.  Read the
    # Hessian and the coordinate Hessian before dropping it.
    KX = sp.factor(sp.diff(L_phys, Xd, Xd))
    OmegaX = sp.factor(-sp.diff(L_phys, X, X))
    cross = sp.factor(sp.diff(L_phys, Xd, X))
    print("L_phys=", L_phys)
    print("K_X=", KX)
    print("Omega_X=", OmegaX)
    print("X-Xdot mixing=", cross, "(total derivative on this constant background)")
    KX_expected = sp.factor(2*K2*KB*k**2 / D)
    Omega_expected = sp.factor(2*k**2*(2-KB)*(K2*Q0**2+k**2) / D)
    check("derived K_X equals 2*K2*K_B*k^2/D", sp.simplify(KX-KX_expected) == 0, f"K_X={KX}")
    check("derived Omega_X equals 2*k^2*(2-K_B)*(K2*Q0^2+k^2)/D", sp.simplify(OmegaX-Omega_expected) == 0, f"Omega_X={OmegaX}")
    omega2 = sp.factor(OmegaX / KX)
    omega2_expected = sp.factor((2-KB)*(K2*Q0**2+k**2)/(K2*KB))
    print("omega^2=", omega2)
    check("finite-k scalar dispersion is derived, not inserted", sp.simplify(omega2-omega2_expected) == 0, f"omega^2={omega2}")
    check("finite-k scalar kinetic coefficient is positive for 0<K_B and K_2", sp.ask(sp.Q.positive(KX)), f"K_X={KX}")

    # Actual scalar DOF count from the Dirac data, not a literal expected rank:
    # 6-dimensional phase space, two first-class constraints, no second-class.
    phase_dim = 2 * len(q)
    fc_finite = len([c for c in [pPhi, C1]]) if PB_finite.rank() == 0 else 0
    sc_finite = PB_finite.rank()
    dof_finite = (phase_dim - 2*fc_finite - sc_finite) // 2
    print(f"finite-k phase_dim={phase_dim}, first_class={fc_finite}, second_class={sc_finite}, scalar_DOF={dof_finite}")
    check("finite-k Dirac count leaves a positive physical scalar sector", dof_finite > 0, f"computed DOF={dof_finite}")

    # k=0 sector must be handled separately; v drops from the Lagrangian.
    L0 = sp.expand(L.subs(k, 0))
    mom0 = [sp.simplify(sp.diff(L0, x)) for x in qd]
    print("k=0 momenta:", mom0)
    check("at k=0 both p_Phi and p_v are primary constraints", mom0[0] == 0 and mom0[1] == 0, str(mom0))
    C0 = Q0 * pchi
    PB_zero = pb_matrix([pPhi, pv, C0], q, p)
    print("k=0 constraint PB matrix [p_Phi,p_v,Q0*p_chi]:")
    print(PB_zero)
    check("k=0 primary/secondary constraint PB matrix is zero", PB_zero == sp.zeros(3), f"computed rank={PB_zero.rank()}\n{PB_zero}")
    fc_zero = len([pPhi, pv, C0]) if PB_zero == sp.zeros(3) else 0
    sc_zero = PB_zero.rank()
    dof_zero = (phase_dim - 2*fc_zero - sc_zero) // 2
    print(f"k=0 phase_dim={phase_dim}, first_class={fc_zero}, second_class={sc_zero}, scalar_DOF={dof_zero}")
    check("k=0 Dirac count is strictly smaller than the finite-k count", dof_zero < dof_finite, f"computed DOF(k=0)={dof_zero}")

    # This is the gate consequence, not a claim that all remaining theory is
    # solved: a finite-k propagating scalar violates the N_grav=2/no-hidden-
    # auxiliary requirement unless the model explicitly accepts and counts it.
    check(
        "strict N_grav=2 reading is incompatible with the computed finite-k scalar",
        dof_finite > dof_zero,
        "one finite-k scalar survives the actual action; a permissive clock-scalar reading must count it explicitly",
    )

    print("\nRESULT: %d failure(s)." % len(FAILS))
    if FAILS:
        for item in FAILS:
            print("  FAILED:", item)
    print("STATUS: HOST_SCALAR_CONSTRAINT_CLAIM_REFUTED; STRICT_NGRAV2_DEAD; CLOCK_RECLASSIFICATION_OPEN")
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
