#!/usr/bin/env python3
"""CAM action audit, exact SymPy arithmetic; a successful audit is not closure.

Conventions: (-+++), positive EH coefficient m=M^2, Sm=-sum mass*proper_time.
Static tests are a Cartesian restriction of the 3D weak-field branch, u'>0.
The Dirac calculation is the actual quadratic ADM scalar action at Minkowski
in unitary clock gauge and spatial gauge E=0, for one real nonzero Fourier
mode. It is not the old auxiliary toy Hamiltonian and is not a nonlinear
Dirac certificate. Only PRIMARY multipliers enter its total Hamiltonian.
"""
import argparse
import json
import sympy as s

from eh_static_reduction_gate import derive_eh_static


def euler(L, f, x):
    return s.simplify(s.diff(L, f) - s.diff(s.diff(L, s.diff(f, x)), x))


def source_and_coefficients():
    eh = derive_eh_static()
    x, phi, psi, m = (eh["symbols"][key] for key in ("x", "Phi", "Psi", "M2"))
    eps, phiv, v2, mass = s.symbols("eps phi v2 mass", real=True)
    particle = -mass * s.sqrt(1 + eps * (2 * phiv - v2))
    particle_first = s.diff(particle, eps).subs(eps, 0)
    eta, sigma, a0 = s.symbols("eta sigma a0", real=True, nonzero=True)
    u, ell, rho = (s.Function(name)(x) for name in ("u", "ell", "rho"))
    p, q = s.diff(phi, x), s.diff(psi, x)
    y = s.diff(u, x) / a0
    Q = y**2 + 2 * (1 + y) * s.exp(-y) - 2
    L = (eh["eh_density_ibp"] + eta * m * p**2 + sigma * m * a0**2 * Q
         + ell * (s.diff(u, x) - p) - rho * phi)
    E = {name: euler(L, f, x) for name, f in
         (("Phi", phi), ("Psi", psi), ("u", u), ("ell", ell))}
    branch_sum = s.simplify((E["Phi"] + E["u"]).subs({u: phi, psi: phi}).doit())
    mu = 1 - s.exp(-p / a0)
    physical_target = 2 * m * s.diff((1 - eta - sigma * mu) * p, x) - rho
    b = s.symbols("mu", real=True)
    flux_coefficient = 1 - eta - sigma * b
    # Equality as a function of mu over an interval fixes both coefficients.
    coefficients = s.Poly(flux_coefficient - b, b).all_coeffs()
    matched = s.solve(coefficients, (eta, sigma), dict=True)[0]
    yy = s.symbols("y", nonnegative=True)
    primitive = yy**2 + 2 * (1 + yy) * s.exp(-yy) - 2
    minimal_F = s.simplify(m * a0**2 * (yy**2 - primitive))
    # Audit raw and integrated-by-parts EH Euler equations, not just expressions.
    raw = m * eh["quadratic_raw"] / 2
    def second_euler(density, f):
        return s.simplify(euler(density, f, x)
                          + s.diff(s.diff(density, s.diff(f, x, 2)), x, 2))
    return {
        "particle_first_order": particle_first,
        "particle_source_derivative": s.diff(particle_first, phiv),
        "source_expected": -mass,
        "eh_boundary_euler_residuals": [
            s.simplify(second_euler(raw, f) - euler(eh["eh_density_ibp"], f, x))
            for f in (phi, psi)],
        "static_equations": E,
        "physical_flux_identity_residual": s.simplify(branch_sum - physical_target),
        "flux_coefficient": flux_coefficient,
        "historical_unrepaired_coefficient": flux_coefficient.subs({eta: 0, sigma: 2}),
        "historical_counterterm_coefficient": flux_coefficient.subs({eta: 1, sigma: 2}),
        "matched_coefficients": {str(key): value for key, value in matched.items()},
        "minimal_F": minimal_F,
        "minimal_F_zero": minimal_F.subs(yy, 0),
        "minimal_F_infinity": s.limit(minimal_F, yy, s.oo),
        "Q_zero_series": s.series(primitive, yy, 0, 5),
        "G_measured": 1 / (8 * s.pi * m),
    }


def tensor_redundancy():
    coords = s.symbols("x y z", real=True)
    B = [s.Function(f"B{i}")(*coords) for i in range(3)]
    aa, bb, cc, dd, ee = [s.Function(n)(*coords) for n in ("a", "b", "c", "d", "e")]
    lam = s.Matrix([[aa, bb, cc], [bb, dd, ee], [cc, ee, -aa-dd]])
    tensor_term = sum(lam[i, j] * s.diff(B[j], coords[i])
                      for i in range(3) for j in range(3))
    boundary = sum(s.diff(lam[i, j] * B[j], coords[i])
                   for i in range(3) for j in range(3))
    div_lam_B = sum(s.diff(lam[i, j], coords[i]) * B[j]
                    for i in range(3) for j in range(3))
    k = s.symbols("k", positive=True)
    wave = s.Matrix([k, 0, 0])
    u, phi, psi = s.symbols("u phi psi", real=True)
    vector = wave * (u-phi)
    tf = (wave*wave.T - s.eye(3)*k**2/3) * (u-phi)
    vector_rows = vector.jacobian([u, phi, psi])
    all_rows = s.Matrix(list(vector) + list(tf)).jacobian([u, phi, psi])
    return {
        "trace": s.trace(lam),
        "ibp_residual": s.simplify(tensor_term + div_lam_B - boundary),
        "vector_constraint_rank": vector_rows.rank(),
        "vector_plus_tensor_rank": all_rows.rank(),
        "Psi_column": all_rows[:, 2],
        "constraints_on_no_lapse_nonzero_Psi": (all_rows * s.Matrix([0, 0, psi])),
        "zero_mode_rank": all_rows.subs(k, 0).rank(),
    }


def clock_background():
    X, C, V = s.symbols("X C V", positive=True)
    P = C * s.sqrt(X) - V
    energy = s.simplify(2 * X * s.diff(P, X) - P)
    t = s.symbols("t", real=True)
    A, N, tau = (s.Function(name)(t) for name in ("A", "N", "tau"))
    Cf, Vf = s.Function("C"), s.Function("V")
    # tau_dot>0: N A^3 sqrt(X)=A^3 tau_dot; keep lapse until variation.
    L = A**3 * (Cf(tau) * s.diff(tau, t) - N * Vf(tau))
    E_tau = euler(L, tau, t)
    lapse_energy = s.simplify(-s.diff(L, N) / A**3)
    m, Lam, rho = s.symbols("M2 Lambda rho", real=True)
    Lgr = -3*m*A*s.diff(A, t)**2/N - m*Lam*N*A**3
    E_N = s.simplify(s.diff(Lgr + L, N) - rho*A**3)
    H, C0 = s.symbols("H C0", positive=True)
    witness_clock_residual = -s.diff(C0*s.exp(-3*H*t), t) - 3*H*C0*s.exp(-3*H*t)
    return {
        "energy_density": energy,
        "pressure": P,
        "clock_Euler": s.simplify(E_tau / A**3),
        "lapse_energy_density": lapse_energy,
        "FLRW_lapse_equation": s.simplify(E_N / A**3),
        "claimed_stealth_clock_Euler_residual": s.simplify(witness_clock_residual),
        "claimed_stealth_energy": C0*s.exp(-3*H*t),
        "minimal_C_V_zero_FLRW_equation": s.simplify(
            (E_N/A**3).subs({Cf(tau): 0, Vf(tau): 0})),
    }


def pb(f, g, qs, ps):
    return s.simplify(sum(s.diff(f, q)*s.diff(g, p)-s.diff(f, p)*s.diff(g, q)
                          for q, p in zip(qs, ps)))


def scalar_dirac():
    m, k, eta = s.symbols("M2 k eta", positive=True)
    z, B, n, zd, p, pB, pn, vB, vn = s.symbols("z B n zd p pB pn vB vn", real=True)
    # Kij=zd*deltaij + ki*kj*B for Ni=partial_i B. Rotate nonzero k along x.
    K = s.diag(zd + k**2*B, zd, zd)
    kinetic = s.expand(m*(s.trace(K*K)-s.trace(K)**2)/2)
    # Curvature is the directly expanded EH scalar block with Phi=n,Psi=-z.
    # Fourier integration by parts: grad(z)^2=k² z².
    potential = m*k**2*(z**2 + 2*n*z + eta*n**2)
    L = kinetic + potential
    zd_solution = s.solve(s.Eq(p, s.diff(L, zd)), zd)[0]
    H = s.simplify((p*zd - L).subs(zd, zd_solution))
    qs, ps = [z, B, n], [p, pB, pn]
    primaries = [pB, pn]
    secondaries = [pb(c, H, qs, ps) for c in primaries]
    # Retain generated normalization of every secondary in PB computation.
    constraints = primaries + secondaries
    bracket = s.Matrix([[pb(f, g, qs, ps) for g in constraints] for f in constraints])
    total = H + vB*pB + vn*pn
    velocities = s.solve([pb(c, total, qs, ps) for c in secondaries], (vB, vn), dict=True)[0]
    surface = s.solve(secondaries, (B, n), dict=True)[0]
    preservation = [s.simplify(pb(c, total, qs, ps).subs(velocities).subs(surface))
                    for c in constraints]
    Hred = s.simplify(H.subs(surface))
    def dirac_bracket(f, g):
        left = s.Matrix([[pb(f, c, qs, ps) for c in constraints]])
        right = s.Matrix([pb(c, g, qs, ps) for c in constraints])
        return s.simplify(pb(f, g, qs, ps) - (left * bracket.inv() * right)[0])
    rank = bracket.rank()
    rank_at_mond = bracket.subs(eta, 1).rank()
    first = len(constraints) - rank
    count = s.Rational(2*len(qs) - 2*first - rank, 2)
    # At k=0 derive a fresh chain from primaries. Secondary formulas at k!=0
    # cannot be divided by k then specialized to zero.
    H0 = H.subs(k, 0)
    primary_preservation0 = [pb(c, H0, qs, ps) for c in primaries]
    return {
        "quadratic_L": L,
        "velocity_Hessian_rank": s.hessian(L, [zd, vB, vn]).rank(),
        "canonical_H": H,
        "primary_constraints": primaries,
        "secondary_constraints": secondaries,
        "primary_multiplier_solution": velocities,
        "constraint_preservation_residuals": preservation,
        "PB_matrix": bracket,
        "PB_determinant": s.factor(bracket.det()),
        "PB_rank": rank,
        "PB_rank_at_eta_1": rank_at_mond,
        "first_class": first,
        "second_class": rank,
        "scalar_canonical_pairs": count,
        "reduced_H": Hred,
        "reduced_H_at_eta_1": s.simplify(Hred.subs(eta, 1)),
        "reduced_bracket_z_p": dirac_bracket(z, p),
        "k_zero_H": H0,
        "k_zero_secondary_generation": primary_preservation0,
        "k_zero_primary_PB": s.Matrix([[pb(f, g, qs, ps) for g in primaries] for f in primaries]),
    }


def lapse_ellipticity():
    """Actual lapse-gradient Hessian, holding ADM canonical spatial data fixed.

    EH is linear in the lapse in the Hamiltonian and adds no lapse-gradient
    term to {p_N,C_N}. Overall signs do not affect principal ellipticity.
    """
    m, a0, N, A = s.symbols("M2 a0 N A", positive=True)
    vx, vy, vz = s.symbols("vx vy vz", real=True)
    gradient = s.Matrix([vx, vy, vz])
    anorm = s.sqrt(gradient.dot(gradient)) / N
    y = anorm/a0
    F = 2*m*a0**2*(1-(1+y)*s.exp(-y))
    lapse_density = N*F
    hess = s.hessian(lapse_density, [vx, vy, vz])
    aligned = hess.subs({vx: N*A, vy: 0, vz: 0}).applyfunc(s.simplify)
    yy, kpar, kperp = s.symbols("y k_parallel k_perp", positive=True)
    aligned = aligned.subs(A, yy*a0).applyfunc(s.simplify)
    symbol = s.simplify((s.Matrix([[kpar, kperp, 0]]) * aligned
                         * s.Matrix([kpar, kperp, 0]))[0])
    longitudinal = aligned[0, 0]
    transverse = aligned[1, 1]
    # Parametrize every y>1 by y=1+r² and choose a nonzero covector (1,r,0).
    r = s.symbols("r", positive=True)
    characteristic = s.simplify(symbol.subs({yy: 1+r**2, kpar: 1, kperp: r}))
    # Positive MOND flux stiffness is a different Hessian from the lapse one.
    mu = 1-s.exp(-yy)
    return {
        "lapse_gradient_Hessian": aligned,
        "lapse_principal_symbol": symbol,
        "transverse": transverse,
        "longitudinal": longitudinal,
        "longitudinal_at_y_1": longitudinal.subs(yy, 1),
        "longitudinal_above_y_1": s.simplify(longitudinal.subs(yy, 1+r**2)),
        "nonzero_characteristic_above_y_1": characteristic,
        "MOND_flux_transverse": mu,
        "MOND_flux_longitudinal": s.simplify(mu+yy*s.diff(mu, yy)),
    }


def cubic_scalar():
    """Scalar conformal ADM expansion; periodic/decaying, nonzero modes only.

    Second-order corrections to stationary lapse/shift solutions cannot
    enter H3 because the first derivatives of H2 vanish on the linear surface.
    This is not the full nonlinear reduced Hamiltonian or a stability proof.
    """
    m, a0 = s.symbols("M2 a0", positive=True)
    ep, z, n, p, vel = s.symbols("ep z n p vel", real=True)
    zv, bv = s.Matrix(s.symbols("z1:4")), s.Matrix(s.symbols("b1:4"))
    b11, b22, b33, b12, b13, b23 = s.symbols("b11 b22 b33 b12 b13 b23")
    Bij = s.Matrix([[b11, b12, b13], [b12, b22, b23], [b13, b23, b33]])
    T = -zv*bv.T-bv*zv.T+s.eye(3)*zv.dot(bv)
    S = ep*Bij+ep**2*T
    trS, S2 = s.trace(S), s.trace(S*S)
    # Perform the Legendre transform, including the conformal connection.
    Lkin = m*s.exp(ep*(3*z-n)) * (
        -3*vel**2+2*s.exp(-2*ep*z)*vel*trS
        + s.exp(-4*ep*z)*(S2-trS**2)/2)
    vsol = s.solve(s.Eq(s.diff(Lkin, vel), ep*p), vel)[0]
    H = s.simplify((ep*p*vel-Lkin).subs(vel, vsol))
    H3 = s.factor(s.expand(s.series(s.expand(H), ep, 0, 4).removeO()).coeff(ep, 3))
    H3branch = s.factor(H3.subs({n: -z, p: 2*m*s.trace(Bij)}))
    expected = 2*m*(zv.T*Bij*bv)[0]
    yy = s.symbols("y", nonnegative=True)
    Q = yy**2+2*(1+yy)*s.exp(-yy)-2
    cubic_coefficient = s.series(Q, yy, 0, 4).removeO().coeff(yy, 3)
    x = s.symbols("x", real=True)
    amplitude, momentum = s.symbols("amplitude momentum", real=True)
    witness_z = amplitude*s.cos(2*x)
    inverse_lap_p = -momentum*s.cos(x)
    witness_H = s.integrate(-s.diff(witness_z, x, 2)*s.diff(inverse_lap_p, x)**2/(4*m),
                            (x, 0, 2*s.pi))
    return {
        "kinetic_cubic_before_boundary_removal": H3branch,
        "kinetic_cubic_identity_residual": s.simplify(H3branch-expected),
        "Q_cubic_coefficient": cubic_coefficient,
        "periodic_kinetic_witness": witness_H,
        "periodic_kinetic_witness_residual": s.simplify(witness_H+s.pi*amplitude*momentum**2/(2*m)),
        "reduced_H3": "integral[-(Delta zeta)|grad Delta^-1 p|^2/(4 M2) + 2 M2 |grad zeta|^3/(3 a0)]",
        "scope": "scalar conformal reduction; norm-cubed MOND term uses positive amplitude scaling, not a C3 Taylor expansion at zero; no global stability conclusion",
    }


def encode(obj):
    if isinstance(obj, dict):
        return {str(k): encode(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [encode(v) for v in obj]
    if isinstance(obj, s.MatrixBase):
        return [[str(v) for v in row] for row in obj.tolist()]
    if isinstance(obj, s.Basic):
        return str(obj)
    return obj


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-closure", action="store_true",
                        help="Exit nonzero unless the tested theory meets full closure.")
    args = parser.parse_args()
    src, tf, clk, adm = source_and_coefficients(), tensor_redundancy(), clock_background(), scalar_dirac()
    lapse = lapse_ellipticity()
    cubic = cubic_scalar()
    checks = {
        "point-particle variation fixes negative matter source": src["particle_source_derivative"] == src["source_expected"],
        "EH boundary removal preserves both Euler equations": all(v == 0 for v in src["eh_boundary_euler_residuals"]),
        "physical static equation follows from independent variations": src["physical_flux_identity_residual"] == 0,
        "all-y MOND matching fixes eta=1 and sigma=-1": src["matched_coefficients"] == {"eta": 1, "sigma": -1},
        "tensor multiplier is a boundary term plus shifted vector multiplier": tf["ibp_residual"] == 0,
        "tensor multiplier adds no independent linear constraint": tf["vector_constraint_rank"] == tf["vector_plus_tensor_rank"],
        "tensor constraints contain no independent Psi term": tf["Psi_column"].is_zero_matrix,
        "nonzero Psi counterexample satisfies multiplier constraints": tf["constraints_on_no_lapse_nonzero_Psi"].is_zero_matrix,
        "cuscuton energy equals V": s.simplify(clk["energy_density"] - s.Symbol("V", positive=True)) == 0,
        "claimed stealth clock is on-shell but has positive energy": clk["claimed_stealth_clock_Euler_residual"] == 0 and clk["claimed_stealth_energy"].is_positive,
        "Dirac preservation closes using only primary multipliers": all(v == 0 for v in adm["constraint_preservation_residuals"]),
        "MOND tuning does not change finite-k constraint rank": adm["PB_rank_at_eta_1"] == adm["PB_rank"],
        "a canonical scalar pair survives at eta=1": adm["scalar_canonical_pairs"] == 1 and adm["reduced_bracket_z_p"] == 1,
        "quadratic scalar Hamiltonian degenerates at eta=1": adm["reduced_H_at_eta_1"] == 0,
        "k=0 chain is recomputed and generates no linear secondaries": all(v == 0 for v in adm["k_zero_secondary_generation"]),
        "lapse transverse Hessian eigenvalue is positive": lapse["transverse"].is_positive,
        "lapse longitudinal principal coefficient vanishes at y=1": lapse["longitudinal_at_y_1"] == 0,
        "lapse longitudinal coefficient is negative for every y=1+r^2, r>0": lapse["longitudinal_above_y_1"].is_negative,
        "nonzero lapse characteristic covector exists for every y>1": lapse["nonzero_characteristic_above_y_1"] == 0,
        "cubic scalar Legendre transform generates momentum interaction": cubic["kinetic_cubic_identity_residual"] == 0 and cubic["kinetic_cubic_before_boundary_removal"] != 0,
        "two periodic modes give a nonzero scalar momentum interaction": cubic["periodic_kinetic_witness_residual"] == 0 and cubic["periodic_kinetic_witness"] != 0,
    }
    for name, ok in checks.items():
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    result = {
        "status": "HISTORICAL_CAM_REFUTED_MINIMAL_REPAIR_SCALAR_AND_LAPSE_OBSTRUCTIONS",
        "checks": {"count": len(checks), "passed": sum(bool(v) for v in checks.values())},
        "source": src, "tensor": tf, "clock": clk, "ADM": adm, "lapse": lapse, "cubic": cubic,
        "non_claims": [
            "No nonlinear Dirac closure, no full PPN certificate, no empirical confirmation.",
            "The finite-k result refutes inference that no auxiliary velocity means no clock scalar.",
            "A zero quadratic Hamiltonian is not by itself a nonlinear no-go or quantified strong-coupling scale.",
            "k=0 quadratic Minkowski constraints do not replace the nonlinear FLRW lapse equation.",
            "Nonellipticity of the lapse principal symbol is not a proof of global noninvertibility or a ghost.",
        ],
    }
    print("RESULT_JSON=" + json.dumps(encode(result), sort_keys=True))
    if not all(checks.values()):
        return 1
    if args.require_closure:
        print("CLOSURE NOT CERTIFIED: scalar pair survives, and lapse principal ellipticity fails at y>=1.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
