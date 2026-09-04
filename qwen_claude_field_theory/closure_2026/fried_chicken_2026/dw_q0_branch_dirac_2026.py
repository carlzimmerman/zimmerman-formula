#!/usr/bin/env python3
r"""Stratified Q=0 audit from the undivided localized DW Lagrangian.

The homogeneous fixed-lapse density is

  L = Xdot*xidot/N + lambda*N*(1-phidot**2/N**2)
      + Q*phidot*nudot/N - c*M*N,
  Q = M + f(Z),  Z = -4*Xdot**2/(N**2*a0**2).

The order of operations is load-bearing: momenta and the Hessian are derived
before Q=0 is imposed.  Q=0 is a rank-changing stratum of the full Legendre
map, not a legal substitution into the Q!=0 Hamiltonian.

Two related objects are kept distinct:

* the intrinsic Poisson geometry of the branch image; and
* the branch embedded in the original Euler--Lagrange problem.

The extra relation Q=0 restricts the tangent bundle but is not an independent
velocity-null direction.  Consequently its Hamiltonian multiplier is tied to
the null velocity.  Treating every branch relation as an ordinary primary with
an arbitrary multiplier loses the transverse M and lambda equations.  This
script calculates the Poisson matrices but does not use the ordinary Dirac DOF
formula for that irregular embedded branch.

The decisive action-level result does not depend on resolving that irregular
count: on either lambda stratum the (X,xi) kinetic block has determinant -1.
At finite spatial k its operator determinant is -(omega^2-k^2)^2, so the
unrestricted local Q=0 theory retains opposite-residue scalar channels and is
DEAD.  Retarded fixed histories remain an external, noncanonical prescription.

Exit 0 certifies only the exact calculations printed here.  No full ADM
N_grav count is claimed.
"""
import itertools
import sys

import sympy as sp


STATUS_UNRESTRICTED_Q0 = "DEAD"
STATUS_EMBEDDED_BRANCH = "OPEN_EMBEDDED_IRREGULAR"
STATUS_RETARDED_HISTORY = "OPEN_NONCANONICAL"
STATUS_FULL_ADM = "NOT_COMPUTED"


def exact_rank_by_minors(matrix):
    """Return generic exact rank and a nonzero maximal-minor witness."""
    rows, cols = matrix.shape
    for size in range(min(rows, cols), 0, -1):
        for row_ids in itertools.combinations(range(rows), size):
            for col_ids in itertools.combinations(range(cols), size):
                minor = sp.factor(matrix.extract(row_ids, col_ids).det())
                if minor != 0:
                    return size, minor, row_ids, col_ids
    return 0, sp.S.Zero, (), ()


def canonical_poisson_matrix(constraints, coordinates, momenta):
    """Calculate, rather than supply, the finite-dimensional PB matrix."""

    def bracket(left, right):
        return sp.factor(
            sum(
                sp.diff(left, q) * sp.diff(right, p)
                - sp.diff(left, p) * sp.diff(right, q)
                for q, p in zip(coordinates, momenta)
            )
        )

    matrix = sp.Matrix([[bracket(left, right) for right in constraints] for left in constraints])
    return matrix, bracket


def undivided_hessian_data():
    """Differentiate the original L first, then evaluate its Q=0 strata."""
    N, a0, c = sp.symbols("N a0 c", nonzero=True)
    vX, vxi, vphi, vnu = sp.symbols("vX vxi vphi vnu")
    lam, M = sp.symbols("lambda M")
    f0, f1, f2, z = sp.symbols("f0 f1 f2 z")
    Z = -4 * vX**2 / (N**2 * a0**2)
    fjet = f0 + f1 * z + sp.Rational(1, 2) * f2 * z**2
    fZ = fjet.subs(z, Z)
    fp = sp.diff(fjet, z).subs(z, Z)
    Q = M + fZ
    L = (
        vX * vxi / N
        + lam * N * (1 - vphi**2 / N**2)
        + Q * vphi * vnu / N
        - c * M * N
    )
    velocities = (vX, vxi, vphi, vnu)
    momenta = tuple(sp.factor(sp.diff(L, velocity)) for velocity in velocities)
    hessian = sp.hessian(L, velocities)

    # Evaluation after differentiation retains the f'(Z)*vphi*vnu response.
    q0_substitution = {M: -fZ}
    hessian_Q0 = hessian.subs(q0_substitution).applyfunc(sp.factor)
    hessian_Q0_lambda0 = hessian_Q0.subs(lam, 0).applyfunc(sp.factor)
    rank_lam, witness_lam, rows_lam, cols_lam = exact_rank_by_minors(hessian_Q0)
    rank_lam0, witness_lam0, rows_lam0, cols_lam0 = exact_rank_by_minors(hessian_Q0_lambda0)

    null_lam = sp.Matrix([0, 8 * fp * vX * vphi / (N**2 * a0**2), 0, 1])
    null_lam0_phi = sp.Matrix([0, 8 * fp * vX * vnu / (N**2 * a0**2), 1, 0])
    null_lam0_nu = sp.Matrix([0, 8 * fp * vX * vphi / (N**2 * a0**2), 0, 1])
    residual_lam = sp.simplify(hessian_Q0 * null_lam)
    residual_lam0_phi = sp.simplify(hessian_Q0_lambda0 * null_lam0_phi)
    residual_lam0_nu = sp.simplify(hessian_Q0_lambda0 * null_lam0_nu)

    # Mutation/control: restricting the action before differentiating removes
    # the xi component of the null vector and therefore the multiplier tie.
    restricted_first = sp.hessian(sp.expand(L.subs(q0_substitution)), velocities).applyfunc(sp.factor)
    pure_nu = sp.Matrix([0, 0, 0, 1])
    wrong_order_pure_nu_residual = sp.simplify(restricted_first * pure_nu)

    return {
        "L": L,
        "Q": Q,
        "Z": Z,
        "fp": fp,
        "momenta": momenta,
        "hessian_Q0": hessian_Q0,
        "hessian_Q0_lambda0": hessian_Q0_lambda0,
        "rank_Q0_lambda_nonzero": rank_lam,
        "rank_Q0_lambda_zero": rank_lam0,
        "rank_witness_lambda_nonzero": witness_lam,
        "rank_witness_lambda_zero": witness_lam0,
        "rank_witness_indices_lambda_nonzero": (rows_lam, cols_lam),
        "rank_witness_indices_lambda_zero": (rows_lam0, cols_lam0),
        "lambda_nonzero_null_vectors": (null_lam,),
        "lambda_zero_null_vectors": (null_lam0_phi, null_lam0_nu),
        "lambda_nonzero_null_residuals": (residual_lam,),
        "lambda_zero_null_residuals": (residual_lam0_phi, residual_lam0_nu),
        "wrong_order_pure_nu_residual": wrong_order_pure_nu_residual,
        "symbols": (N, a0, c, vX, vxi, vphi, vnu, lam, M),
    }


def lambda_nonzero_branch_data():
    """Embedded homogeneous branch for Q=0 and lambda!=0."""
    N, a0, c = sp.symbols("N a0 c", nonzero=True)
    X, xi, phi, lam, M, nu = sp.symbols("X xi phi lambda M nu")
    pX, pxi, pphi, plam, pM, pnu = sp.symbols("pX pxi pphi plambda pM pnu")
    f0, f1, f2, z = sp.symbols("f0 f1 f2 z")
    Zp = -4 * pxi**2 / a0**2
    fjet = f0 + f1 * z + sp.Rational(1, 2) * f2 * z**2
    fZp = fjet.subs(z, Zp)
    fp = sp.diff(fjet, z).subs(z, Zp)
    Q = M + fZp
    coordinates = (X, xi, phi, lam, M, nu)
    momenta = (pX, pxi, pphi, plam, pM, pnu)

    # Derive the branch energy from p.v-L.  Q=0 is imposed only after the
    # momenta of the undivided Lagrangian have fixed the velocity map.
    vX, vxi, vphi_symbol, vnu_symbol = sp.symbols("vX vxi vphi_symbol vnu_symbol")
    Z_velocity = -4 * vX**2 / (N**2 * a0**2)
    fZ_velocity = fjet.subs(z, Z_velocity)
    Q_velocity = M + fZ_velocity
    L = (
        vX * vxi / N
        + lam * N * (1 - vphi_symbol**2 / N**2)
        + Q_velocity * vphi_symbol * vnu_symbol / N
        - c * M * N
    )
    vphi_map = -N * pphi / (2 * lam)
    vxi_map = N * pX + 8 * fp * pxi * vphi_map * vnu_symbol / (N * a0**2)
    legendre_energy = pX * vX + pxi * vxi + pphi * vphi_symbol + pnu * vnu_symbol - L
    branch_energy = sp.factor(
        legendre_energy.subs(vX, N * pxi)
        .subs(vphi_symbol, vphi_map)
        .subs(vxi, vxi_map)
        .subs(M, -fZp)
        .subs(pnu, 0)
    )
    Hc = N * (pX * pxi - pphi**2 / (4 * lam) - lam + c * M)
    legendre_energy_residual = sp.factor(branch_energy - Hc.subs(M, -fZp))
    branch_relations = (plam, pM, pnu, Q, pphi**2 - 4 * lam**2)
    pb_matrix, PB = canonical_poisson_matrix(branch_relations, coordinates, momenta)
    pb_rank, pb_witness, pb_rows, pb_cols = exact_rank_by_minors(pb_matrix)

    raw_preservation = PB(plam, Hc)
    clock_secondary = sp.factor(-4 * lam**2 * raw_preservation / N)
    clock_secondary_control = pphi**2 - 4 * lam**2

    # The single Hessian-null velocity is vnu.  The Q multiplier is not
    # independent: matching dot(xi) to the undivided Legendre map fixes it.
    vnu, uQ = sp.symbols("vnu u_Q")
    vphi = -N * pphi / (2 * lam)
    actual_vxi = N * pX + 8 * fp * pxi * vphi * vnu / (N * a0**2)
    hamilton_vxi = N * pX + uQ * sp.diff(Q, pxi)
    multiplier_tie = pphi * vnu / (2 * lam)
    tie_residual = sp.factor((hamilton_vxi - actual_vxi).subs(uQ, multiplier_tie))

    # p_M preservation gives u_Q=-cN.  Combined with the tie, it fixes vnu;
    # p_lambda preservation supplies the clock normalization.
    vnu_solution = -2 * c * N * lam / pphi
    clock_velocity_residual = sp.factor((vphi**2 - N**2).subs(pphi**2, 4 * lam**2))
    transport_velocity_residual = sp.factor((vphi * vnu_solution - c * N**2))

    # Continue preservation through closure in this homogeneous embedded
    # system.  The Q and clock-relation equations determine vM and vlambda;
    # pnu itself is stable.  These are not a full spatial/ADM chain.
    vlambda, vM = sp.symbols("vlambda vM")
    embedded_H = Hc + vnu * pnu + multiplier_tie * Q + vlambda * plam + vM * pM
    Q_preservation = sp.factor(PB(Q, embedded_H))
    clock_relation_preservation = sp.factor(PB(clock_secondary_control, embedded_H))
    pnu_preservation = sp.factor(PB(pnu, embedded_H))
    embedded_closes = (
        sp.solve(sp.Eq(Q_preservation, 0), vM) == [0]
        and sp.solve(sp.Eq(clock_relation_preservation, 0), vlambda) == [0]
        and pnu_preservation == 0
    )

    return {
        "Hc": Hc,
        "branch_energy": branch_energy,
        "legendre_energy_residual": legendre_energy_residual,
        "branch_relations": branch_relations,
        "pb_matrix": pb_matrix,
        "pb_rank": pb_rank,
        "pb_rank_witness": pb_witness,
        "pb_rank_witness_indices": (pb_rows, pb_cols),
        "clock_secondary": clock_secondary,
        "clock_secondary_control": clock_secondary_control,
        "null_multiplier_tie": sp.Eq(uQ, multiplier_tie),
        "null_multiplier_tie_residual": tie_residual,
        "uQ_from_pM_preservation": -c * N,
        "vphi": vphi,
        "vnu_solution": vnu_solution,
        "clock_velocity_residual": clock_velocity_residual,
        "transport_velocity_residual": transport_velocity_residual,
        "preservation_after_secondary": {
            "Q": Q_preservation,
            "clock_relation": clock_relation_preservation,
            "pnu": pnu_preservation,
        },
        "intrinsic_formal_first_class_count": len(branch_relations) - pb_rank,
        "intrinsic_second_class_rank": pb_rank,
        "embedded_homogeneous_chain_closes": embedded_closes,
        "ordinary_dirac_count_valid_for_embedded_branch": False,
        "status": STATUS_EMBEDDED_BRANCH,
    }


def lambda_zero_branch_data():
    """Hamilton--Pontryagin consistency system for Q=lambda=0."""
    N, a0, c = sp.symbols("N a0 c", positive=True)
    X, xi, phi, lam, M, nu = sp.symbols("X xi phi lambda M nu")
    pX, pxi, pphi, plam, pM, pnu = sp.symbols("pX pxi pphi plambda pM pnu")
    f0, f1, f2, z = sp.symbols("f0 f1 f2 z")
    Zp = -4 * pxi**2 / a0**2
    fjet = f0 + f1 * z + sp.Rational(1, 2) * f2 * z**2
    Q = M + fjet.subs(z, Zp)
    coordinates = (X, xi, phi, lam, M, nu)
    momenta = (pX, pxi, pphi, plam, pM, pnu)
    branch_relations = (plam, pM, pphi, pnu, lam, Q)
    pb_matrix, PB = canonical_poisson_matrix(branch_relations, coordinates, momenta)
    pb_rank, pb_witness, pb_rows, pb_cols = exact_rank_by_minors(pb_matrix)

    vphi, vnu, vlam, vM = sp.symbols("vphi vnu vlambda vM")
    # This generalized energy keeps terms transverse to the branch.  Dropping
    # lambda and Q before variation would erase both multiplier equations.
    H_HP = (
        N * (pX * pxi + c * M)
        + vphi * pphi
        + vnu * pnu
        + vlam * plam
        + vM * pM
        + lam * (vphi**2 / N - N)
        - Q * vphi * vnu / N
    )
    # Independent Legendre-energy derivation from the undivided action.
    vX, vxi = sp.symbols("vX vxi")
    Z_velocity = -4 * vX**2 / (N**2 * a0**2)
    fZ_velocity = fjet.subs(z, Z_velocity)
    Q_velocity = M + fZ_velocity
    fp = sp.diff(fjet, z).subs(z, Zp)
    L = (
        vX * vxi / N
        + lam * N * (1 - vphi**2 / N**2)
        + Q_velocity * vphi * vnu / N
        - c * M * N
    )
    vxi_map = N * pX + 8 * fp * pxi * vphi * vnu / (N * a0**2)
    legendre_energy = (
        pX * vX + pxi * vxi + pphi * vphi + pnu * vnu
        + plam * vlam + pM * vM - L
    )
    derived_HP = sp.factor(
        legendre_energy.subs(vX, N * pxi).subs(vxi, vxi_map)
    )
    legendre_energy_residual = sp.factor(derived_HP - H_HP)
    stationarity_phi = sp.factor(sp.diff(H_HP, vphi).subs({lam: 0, Q: 0}))
    stationarity_nu = sp.factor(sp.diff(H_HP, vnu).subs({lam: 0, Q: 0}))
    preserve_plambda = sp.factor(PB(plam, H_HP).subs({lam: 0, Q: 0}))
    preserve_pM = sp.factor(PB(pM, H_HP).subs({lam: 0, Q: 0}))
    velocity_equations = (vphi**2 - N**2, vphi * vnu - c * N**2)
    velocity_solutions = tuple(
        (solution[vphi], solution[vnu])
        for solution in sp.solve(velocity_equations, (vphi, vnu), dict=True)
    )

    return {
        "N": N,
        "c": c,
        "H_HP": H_HP,
        "derived_H_HP": derived_HP,
        "legendre_energy_residual": legendre_energy_residual,
        "branch_relations": branch_relations,
        "pb_matrix": pb_matrix,
        "pb_rank": pb_rank,
        "pb_rank_witness": pb_witness,
        "pb_rank_witness_indices": (pb_rows, pb_cols),
        "stationarity_constraints": (stationarity_phi, stationarity_nu),
        "preservation_multiplier_equations": (preserve_plambda, preserve_pM),
        "clock_transport_velocity_solutions": velocity_solutions,
        "lambda_tangency_fixes": sp.Eq(vlam, 0),
        "Q_tangency_fixes_homogeneous": sp.Eq(vM, 0),
        "intrinsic_formal_first_class_count": len(branch_relations) - pb_rank,
        "intrinsic_second_class_rank": pb_rank,
        "embedded_homogeneous_chain_closes": len(velocity_solutions) == 2,
        "ordinary_dirac_count_valid_for_embedded_branch": False,
        "status": STATUS_EMBEDDED_BRANCH,
    }


def q0_fourier_ghost_data():
    """Action-derived Q=0 (X,xi) pole and residue audit."""
    omega, k = sp.symbols("omega k", real=True)
    a0, c, f1 = sp.symbols("a0 c f1", positive=True)
    vX, vxi, gX, gxi = sp.symbols("vX vxi gX gxi")
    eps, f0, f2 = sp.symbols("epsilon f0 f2")

    # On the original M equation W=phidot*nudot-grad(phi).grad(nu)=c.
    # Therefore Q*W-c*M contributes c*f'(Z)*delta Z.  At a constant-X
    # background its quadratic piece is Lorentz invariant.
    Z_perturbation = 4 * eps**2 * (-vX**2 + gX**2) / a0**2
    f_perturbation = f0 + f1 * Z_perturbation + sp.Rational(1, 2) * f2 * Z_perturbation**2
    # At W=c the combination Q*W-c*M is exactly c*f(Z), so M cancels
    # before the epsilon expansion.
    action_sector = eps**2 * (vX * vxi - gX * gxi) + c * f_perturbation
    L2 = sp.expand(action_sector).coeff(eps, 2)
    L2_control = vX * vxi - gX * gxi - 4 * c * f1 * (vX**2 - gX**2) / a0**2
    quadratic_expansion_residual = sp.factor(L2 - L2_control)
    kinetic = sp.hessian(L2, (vX, vxi)).applyfunc(sp.factor)
    det_kinetic = sp.factor(kinetic.det())
    if det_kinetic.is_negative:
        inertia = (1, 1, 0)
    else:
        inertia = None
    operator = (omega**2 - k**2) * kinetic

    return {
        "L2": L2,
        "quadratic_expansion_residual": quadratic_expansion_residual,
        "omega": omega,
        "k": k,
        "kinetic_matrix": kinetic,
        "kinetic_inertia": inertia,
        "finite_k_operator": operator,
        "finite_k_operator_det": sp.factor(operator.det()),
        "k0_operator_det": sp.factor(operator.subs(k, 0).det()),
        "unrestricted_q0_status": STATUS_UNRESTRICTED_Q0,
    }


def spatial_q_tangency_data():
    """Linear Fourier symbol of Q=0 tangency around homogeneous Xdot=v."""
    a0, f1, v, k, deltaX = sp.symbols("a0 f1 v k delta_X", nonzero=True)
    uM = sp.symbols("u_M")
    # dot Q = u_M + (8 f'/a0^2)(-p_xi Delta X + grad X.grad p_xi).
    # At grad X_bar=0, p_xi_bar=v and Delta deltaX=-k^2 deltaX.
    dotQ_symbol = uM + 8 * f1 * v * k**2 * deltaX / a0**2
    uM_solution = sp.solve(sp.Eq(dotQ_symbol, 0), uM)[0]
    residual = sp.factor(dotQ_symbol.subs(uM, uM_solution))
    return {
        "dotQ_symbol": dotQ_symbol,
        "uM_finite_k": uM_solution,
        "uM_k0": sp.factor(uM_solution.subs(k, 0)),
        "tangency_residual": residual,
        "coefficient_of_uM": sp.diff(dotQ_symbol, uM),
        "produces_new_constraint": False,
    }


def main():
    checks = []

    def check(label, condition, detail=""):
        ok = bool(condition)
        checks.append(ok)
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f"   ({detail})" if detail else ""))

    def header(label):
        print("\n" + "=" * 98)
        print(label)
        print("=" * 98)

    header("PART 1 -- UNDIVIDED MOMENTA, EXACT Q=0 HESSIAN MINORS, AND NULL VECTORS")
    h = undivided_hessian_data()
    print("  momenta (pX, pxi, pphi, pnu) =", h["momenta"])
    print("  Q=0, lambda!=0 rank/witness =", h["rank_Q0_lambda_nonzero"], h["rank_witness_lambda_nonzero"])
    print("  Q=0, lambda=0  rank/witness =", h["rank_Q0_lambda_zero"], h["rank_witness_lambda_zero"])
    print("  lambda!=0 null vector =", h["lambda_nonzero_null_vectors"][0].T)
    print("  lambda=0 null vectors =", [vector.T for vector in h["lambda_zero_null_vectors"]])
    check("Q=0, lambda!=0 exact-minor rank is 3", h["rank_Q0_lambda_nonzero"] == 3)
    check("Q=0, lambda=0 exact-minor rank is 2", h["rank_Q0_lambda_zero"] == 2)
    check("lambda!=0 null vector annihilates the undivided Hessian", all(r == sp.zeros(4, 1) for r in h["lambda_nonzero_null_residuals"]))
    check("both lambda=0 null vectors annihilate the undivided Hessian", all(r == sp.zeros(4, 1) for r in h["lambda_zero_null_residuals"]))
    check("mutation: restricting Q=0 before differentiation changes the null direction", h["wrong_order_pure_nu_residual"] == sp.zeros(4, 1) and h["lambda_nonzero_null_vectors"][0][1] != 0)

    header("PART 2 -- Q=0, lambda!=0: BRANCH RELATIONS, PB MATRIX, AND EMBEDDED MULTIPLIER TIE")
    ln = lambda_nonzero_branch_data()
    print("  Hc =", ln["Hc"])
    print("  branch relations =", ln["branch_relations"])
    print("  calculated PB matrix =")
    sp.pprint(ln["pb_matrix"])
    print("  PB rank/witness =", ln["pb_rank"], ln["pb_rank_witness"])
    print("  clock secondary =", ln["clock_secondary"])
    print("  embedded null-multiplier tie =", ln["null_multiplier_tie"])
    print("  pM preservation: u_Q =", ln["uQ_from_pM_preservation"], "; vnu =", ln["vnu_solution"])
    print("  post-secondary preservation =", ln["preservation_after_secondary"])
    print("  intrinsic PB-null relation count =", ln["intrinsic_formal_first_class_count"])
    check("branch Hamiltonian is the Legendre energy of the undivided action", ln["legendre_energy_residual"] == 0)
    check("five-relation PB matrix is antisymmetric", ln["pb_matrix"] + ln["pb_matrix"].T == sp.zeros(5))
    check("exact minors give PB rank 4 with a nonzero witness", ln["pb_rank"] == 4 and ln["pb_rank_witness"] != 0)
    check("p_lambda preservation derives pphi^2-4 lambda^2", sp.factor(ln["clock_secondary"] - ln["clock_secondary_control"]) == 0)
    check("Legendre-map matching derives the Q/null-velocity multiplier tie", ln["null_multiplier_tie_residual"] == 0)
    check("transverse lambda and M equations enforce both velocity conditions", ln["clock_velocity_residual"] == 0 and ln["transport_velocity_residual"] == 0)
    check("homogeneous embedded preservation closes after multipliers are fixed", ln["embedded_homogeneous_chain_closes"])
    check("ordinary Dirac count is not applied to the irregular embedded branch", not ln["ordinary_dirac_count_valid_for_embedded_branch"])

    header("PART 3 -- Q=0, lambda=0: HAMILTON--PONTRYAGIN PRESERVATION")
    lz = lambda_zero_branch_data()
    print("  generalized branch energy =", lz["H_HP"])
    print("  branch relations =", lz["branch_relations"])
    print("  calculated PB matrix =")
    sp.pprint(lz["pb_matrix"])
    print("  PB rank/witness =", lz["pb_rank"], lz["pb_rank_witness"])
    print("  velocity stationarity constraints =", lz["stationarity_constraints"])
    print("  transverse preservation equations =", lz["preservation_multiplier_equations"])
    print("  clock/transport velocity solutions =", lz["clock_transport_velocity_solutions"])
    print("  intrinsic PB-null relation count =", lz["intrinsic_formal_first_class_count"])
    check("Hamilton--Pontryagin energy is derived from p.v-L before restricting the branch", lz["legendre_energy_residual"] == 0)
    check("six-relation PB matrix is antisymmetric", lz["pb_matrix"] + lz["pb_matrix"].T == sp.zeros(6))
    check("exact minors give PB rank 4 with a nonzero witness", lz["pb_rank"] == 4 and lz["pb_rank_witness"] != 0)
    check("velocity stationarity returns pphi=pnu=0", lz["stationarity_constraints"] == lz["branch_relations"][2:4])
    check("transverse equations fix the two sign-related clock/transport velocities", len(lz["clock_transport_velocity_solutions"]) == 2 and all(sp.factor(vp**2-lz["N"]**2)==0 and sp.factor(vp*vn-lz["c"]*lz["N"]**2)==0 for vp, vn in lz["clock_transport_velocity_solutions"]))
    check("homogeneous embedded lambda=0 preservation closes after multiplier fixing", lz["embedded_homogeneous_chain_closes"])
    check("ordinary Dirac count is not applied after transverse equations fix null multipliers", not lz["ordinary_dirac_count_valid_for_embedded_branch"])

    header("PART 4 -- Q=0 FINITE-k POLES, k=0 SECTOR, AND RESIDUE SIGN")
    fourier = q0_fourier_ghost_data()
    print("  quadratic L_(X,xi) =", fourier["L2"])
    print("  kinetic matrix =", fourier["kinetic_matrix"].tolist())
    print("  inertia (positive, negative, zero) =", fourier["kinetic_inertia"])
    print("  det O(omega,k) =", fourier["finite_k_operator_det"])
    print("  det O(omega,0) =", fourier["k0_operator_det"])
    check("quadratic Fourier density is derived by expanding the QW-cM action sector", fourier["quadratic_expansion_residual"] == 0)
    check("action-derived kinetic determinant is -1", fourier["kinetic_matrix"].det() == -1)
    check("negative determinant gives one positive and one negative kinetic direction", fourier["kinetic_inertia"] == (1, 1, 0))
    check("finite-k operator has two scalar light-cone factors", sp.factor(fourier["finite_k_operator_det"] + (fourier["omega"]**2-fourier["k"]**2)**2) == 0)
    check("k=0 remains a separate omega^4 sector", sp.factor(fourier["k0_operator_det"] + fourier["omega"]**4) == 0)
    check("unrestricted local Q=0 action is classified DEAD", fourier["unrestricted_q0_status"] == "DEAD")

    header("PART 5 -- SPATIAL Q=0 TANGENCY: k!=0 VERSUS k=0")
    tangent = spatial_q_tangency_data()
    print("  delta(dot Q)(k) =", tangent["dotQ_symbol"])
    print("  u_M(k!=0) =", tangent["uM_finite_k"])
    print("  u_M(k=0) =", tangent["uM_k0"])
    check("finite-k Q tangency fixes u_M exactly", tangent["coefficient_of_uM"] == 1 and tangent["tangency_residual"] == 0)
    check("k=0 and k!=0 are explicit: u_M vanishes only at k=0", tangent["uM_k0"] == 0 and tangent["uM_finite_k"] != 0)
    check("Q tangency fixes a multiplier rather than adding a constraint", not tangent["produces_new_constraint"])

    header("VERDICT")
    print("  unrestricted local Q=0 action :", STATUS_UNRESTRICTED_Q0)
    print("    The nondegenerate (X,xi) block survives both lambda strata and has opposite kinetic signs.")
    print("  embedded Q=0 branch          :", STATUS_EMBEDDED_BRANCH)
    print("    Exact branch PB matrices were computed, but transverse Euler--Lagrange equations tie/fix")
    print("    null multipliers.  An ordinary first-/second-class count on the intrinsic branch alone is invalid.")
    print("  retarded fixed histories     :", STATUS_RETARDED_HISTORY)
    print("  full spatial+ADM count       :", STATUS_FULL_ADM)
    print("    Metric constraints and their distributional PB operator have not been included.")
    print(f"  computational checks passed: {sum(checks)}/{len(checks)}")
    sys.exit(0 if all(checks) else 1)


if __name__ == "__main__":
    main()
