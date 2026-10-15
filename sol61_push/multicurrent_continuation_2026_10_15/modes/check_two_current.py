#!/usr/bin/env python3
"""Exact, bounded checks for the co-moving two-current principal action.

No source report is parsed as executable mathematics. Snapshot paths are pinned
as provenance inputs by the enclosing computation-audit runner. This program
checks independently constructed algebraic objects described in PROOF.md.
"""
import argparse
import itertools
import json
from pathlib import Path

import sympy as s


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    checks = []

    def zero(name, expression):
        residual = s.factor(expression)
        assert residual == 0, (name, residual)
        checks.append({"name": name, "result": "exact zero"})

    def positive(name, expression):
        expression = s.factor(expression)
        assert expression.is_positive is True, (name, expression)
        return str(expression)

    # A direct tensor contraction, with F_i0=E_i and F_ij=eps_ijk B_k.
    lam = s.symbols("lam")
    E, vx, vy, vz, ex, ey, ez, bx, by, bz = s.symbols(
        "E vx vy vz ex ey ez bx by bz", real=True
    )
    metric = s.diag(-1, 1, 1, 1)
    F = s.zeros(4)
    electric = s.Matrix([lam * ex, lam * ey, E + lam * ez])
    magnetic = s.Matrix([lam * bx, lam * by, lam * bz])
    for i in range(3):
        F[i + 1, 0], F[0, i + 1] = electric[i], -electric[i]
        for j in range(3):
            F[i + 1, j + 1] = sum(
                s.LeviCivita(i, j, k) * magnetic[k] for k in range(3)
            )
    Fup = metric * F * metric
    star = s.zeros(4)
    for i, j in itertools.product(range(4), repeat=2):
        star[i, j] = sum(
            s.LeviCivita(i, j, k, ell) * Fup[k, ell] / 2
            for k, ell in itertools.product(range(4), repeat=2)
        )
    U = s.Matrix([
        1 + lam**2 * (vx**2 + vy**2 + vz**2) / 2,
        lam * vx, lam * vy, lam * vz,
    ])
    eu, bu = F * U, star * U
    ecoef = s.expand((eu.T * metric * eu)[0]).coeff(lam, 2)
    bcoef = s.expand((bu.T * metric * bu)[0]).coeff(lam, 2)
    boost = E**2 * (vx**2 + vy**2) + 2 * E * (vx * by - vy * bx)
    zero("direct_E_U_squared_quadratic", ecoef - ex**2 - ey**2 - ez**2 - boost)
    zero("direct_B_U_squared_quadratic", bcoef - bx**2 - by**2 - bz**2 - boost)

    # The nonlinear electric response has separate longitudinal/transverse Hessians.
    D, p, beta = s.symbols("D p beta", real=True)
    Er = E + lam * ez + lam**2 * (ecoef - ez**2) / (2 * E)
    Le2 = s.expand(D * (Er - E) + p * (Er - E)**2 / 2 - beta * lam**2 * bcoef / 2).coeff(lam, 2)
    t = s.symbols("t", real=True)
    expected = (p * ez**2 + t * (ex**2 + ey**2) - beta * (bx**2 + by**2 + bz**2)) / 2
    expected += (t - beta) * boost / 2
    zero("constitutive_quadratic_from_tensor_boost", Le2.subs(D, E * t) - expected)

    h1, h2, w1, w2, z, a, C, c1, c2 = s.symbols("h1 h2 w1 w2 z a C c1 c2", positive=True)
    H = s.diag(h1, h2)
    w = s.Matrix([w1, w2])
    W = w1**2 / h1 + w2**2 / h2
    hc = 1 / W
    V, r = s.symbols("V r", real=True)
    vv = s.Matrix([hc * w1 * V / h1 + w2 * r, hc * w2 * V / h2 - w1 * r])
    zero("H_orthogonal_average_is_V", (w.T * vv)[0] - V)
    zero("separate_inertia_decomposition", (vv.T * H * vv)[0] - hc * V**2 - (h1 * w2**2 + h2 * w1**2) * r**2)

    M = H + a * w * w.T
    pressure = s.diag(h1 * c1, h2 * c2)
    N = z * M - pressure
    pencil = s.zeros(3)
    pencil[0, 0] = p * z - beta
    pencil[1:3, 1:3] = N
    # Introduce c with z=c^2, then eliminate even powers only.
    speed = s.symbols("speed", real=True)
    for i in range(2):
        pencil[0, i + 1] = pencil[i + 1, 0] = speed * C * w[i]
    determinant = s.expand(pencil.det()).subs(speed**2, z)
    d1, d2 = h1 * (z - c1), h2 * (z - c2)
    S = w1**2 * d2 + w2**2 * d1
    cubic = (p * z - beta) * (d1 * d2 + z * a * S) - z * C**2 * S
    zero("perpendicular_cubic_direct_determinant", determinant - cubic)
    cs = s.symbols("cs", nonnegative=True)
    equal_factor = h1 * h2 * (z - cs) * ((p * z - beta) * ((1 + a * W) * z - cs) - z * C**2 * W)
    zero("equal_sound_relative_mode_factor", cubic.subs({c1: cs, c2: cs}) - equal_factor)
    single = h2 * (z - c2) * ((p * z - beta) * ((h1 + a) * z - h1 * c1) - z * C**2)
    zero("single_species_polynomial_control", cubic.subs({w1: 1, w2: 0}) - single)

    H1, H2 = s.symbols("H1 H2", positive=True)
    Wstar = w1**2 / H1 + w2**2 / H2
    shifted = s.diag(H1, H2) + a * w * w.T
    zero("rank_one_inverse_light_cone", (w.T * shifted.inv() * w)[0] - Wstar / (1 + a * Wstar))

    hs = s.symbols("hstar", positive=True)
    f = p - beta - E**2 * (t - beta)**2 / (hs + E**2 * (t - beta))
    hcrit = E**2 * t * (t - p) / p
    betaL = p * (hs - hcrit) / (hs - E**2 * (t - p))
    zero("beta_window_root", f.subs(beta, betaL))
    zero("beta_window_derivative", s.diff(f, beta) + hs**2 / (hs + E**2 * (t - beta))**2)
    zero("threshold_numerator", f.subs(beta, 0) - p * (hs - hcrit) / (hs + E**2 * t))

    # Dust rest-mass weights give the total inertia and actual relative velocity.
    rho1, rho2, rel = s.symbols("rho1 rho2 rel", positive=True)
    rho = rho1 + rho2
    wd = {w1: rho1 / rho, w2: rho2 / rho, h1: rho1, h2: rho2}
    zero("dust_collective_inertia_total_rest_mass", hc.subs(wd) - rho)
    vd1, vd2 = V + rho2 * rel / rho, V - rho1 * rel / rho
    zero("dust_relative_reduced_inertia", rho1 * vd1**2 + rho2 * vd2**2 - rho * V**2 - rho1 * rho2 * rel**2 / rho)

    # Electrostatic k parallel E: eliminating A_0 gives a positive rank-one plasma term.
    Q1, Q2 = s.symbols("Q1 Q2", real=True)
    Q = s.Matrix([Q1, Q2])
    plasma = H.inv() * Q * Q.T / p
    om = s.symbols("omega_squared", real=True)
    zero("dust_plasma_characteristic", (om * s.eye(2) - plasma).det() - om * (om - (Q1**2 / h1 + Q2**2 / h2) / p))
    # Actual portal masses; charge equality does not enter derivative kinetic matrices.
    mchi = s.Rational(93906542194, 100000000)
    zero("portal_actual_mass_charge_ratio", mchi / s.Integer(1) - s.Rational("939.06542194"))

    sample_rows = []
    for xx, fraction2, sounds, RR, direction in itertools.product(
        [s.Rational(1, 10), s.Rational(1, 2), s.Rational(9, 10)],
        [s.Rational(1, 1000), s.Rational(1, 2)],
        [(s.Integer(0), s.Integer(0)), (s.Rational(1, 10), s.Rational(1, 3))],
        [s.Rational(101, 100), s.Integer(2)],
        [(s.Integer(0), s.Integer(1)), (s.Rational(3, 5), s.Rational(4, 5)), (s.Integer(1), s.Integer(0))],
    ):
        tt, pp, EE = 1 - xx, (1 - xx)**2, xx / (1 - xx)  # D0=1
        crit = EE**2 * tt * (tt - pp) / pp
        hhstar = RR * crit
        ss1, ss2 = sounds
        ww = s.Matrix([1 - fraction2, fraction2])
        # At this local EOS point h_a=m_a n_a, including finite sound speed.
        rho_total = hhstar * ((1 - fraction2) / (1 - ss1) + fraction2 / (1 - ss2))
        hh = [rho_total * (1 - fraction2), rho_total * fraction2]
        bbL = pp * (RR - 1) / (RR - (1 - xx))
        bb = bbL * RR / (RR + 1)
        delta, mixing = tt - bb, EE * (tt - bb)
        aa = EE**2 * delta
        st, ct = direction
        kk = s.Matrix([st, 0, ct])
        TT = s.Matrix([[0, ct], [1, 0], [0, -st]])
        eps = s.diag(tt, tt, pp)
        KA = TT.T * (eps - eps * kk * kk.T * eps / (kk.T * eps * kk)[0]) * TT
        Bmap = s.Matrix.hstack(kk.cross(TT[:, 0]), kk.cross(TT[:, 1]))
        rotate = s.Matrix([[0, 1, 0], [-1, 0, 0], [0, 0, 0]])
        CC = mixing * s.kronecker_product(ww, rotate * Bmap)
        MM = s.kronecker_product(s.diag(*hh), s.eye(3)) + aa * s.kronecker_product(ww * ww.T, s.diag(1, 1, 0))
        PP = s.diag(hh[0] * ss1, hh[1] * ss2)
        PP = s.kronecker_product(PP, kk * kk.T)
        schur = KA - bb * s.eye(2) - CC.T * (MM - PP).inv() * CC
        row = {
            "x": str(xx), "mass_fraction_2": str(fraction2), "sound_squares": list(map(str, sounds)),
            "R": str(RR), "sin_cos": list(map(str, direction)),
            "hstar": str(hhstar), "total_rest_density": str(rho_total),
            "number_density_chi": str(hh[0] / mchi), "number_density_S": str(hh[1]),
            "beta": positive("sample_beta", bb),
            "schur_first_minor": positive("sample_schur_first_minor", schur[0, 0]),
            "schur_determinant": positive("sample_schur_determinant", schur.det()),
        }
        sample_rows.append(row)

    output = {
        "status": "all declared exact identities and finite matrix tests passed",
        "coefficient_domain": "Q with symbolic rational functions over Q; exact SymPy arithmetic",
        "symbolic_identity_count": len(checks), "symbolic_identities": checks,
        "finite_light_cone_cases": len(sample_rows), "finite_cases": sample_rows,
        "non_claims": [
            "No numerical eigenvalues, large simulation or on-shell halo solution was computed.",
            "The finite matrix cases do not prove the all-angle theorem; PROOF.md contains the separate analytic reduction.",
            "No metric constraints, nonzero background drift, B != 0 background, finite wavelength full spectrum, vacuum or interface completion was tested.",
        ],
    }
    Path(args.output).write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({k: output[k] for k in ["status", "symbolic_identity_count", "finite_light_cone_cases"]}, indent=2))


if __name__ == "__main__":
    main()
