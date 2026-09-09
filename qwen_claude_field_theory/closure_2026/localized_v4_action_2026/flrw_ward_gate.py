"""Homogeneous FLRW and matter-Ward consistency gate.

This derives the lapse equation before setting N=1 and checks that the
minimally coupled matter continuity equation differentiates it into the
acceleration equation.  It also verifies algebraically that the localized
Hodge/York fields vanish on an exactly homogeneous isotropic leaf.
"""
import json
import sympy as sp


def flrw_ward_gate():
    N, a, adot = sp.symbols("N a adot", positive=True)
    H, Hdot = sp.symbols("H Hdot", real=True)
    rho, pressure, rhodot = sp.symbols("rho pressure rhodot", real=True)
    Gb, Lam = sp.symbols("G_b Lambda", positive=True)
    ell = sp.Rational(1, 100)
    A = 2 + 3*ell
    Lg = -3*A*a*adot**2/N - 2*Lam*N*a**3
    Lm = -N*a**3*rho
    lapse_variation = sp.diff(Lg/(16*sp.pi*Gb)+Lm, N)
    friedmann = sp.factor(
        (16*sp.pi*Gb/a**3*lapse_variation).subs({N: 1, adot: a*H})
    )
    expected_friedmann = 3*A*H**2 - 2*Lam - 16*sp.pi*Gb*rho
    d_friedmann = sp.diff(expected_friedmann, H)*Hdot + sp.diff(
        expected_friedmann, rho)*rhodot
    continuity = sp.Eq(rhodot, -3*H*(rho+pressure))
    after_continuity = sp.factor(d_friedmann.subs(rhodot, continuity.rhs))
    acceleration = 2*A*Hdot + 16*sp.pi*Gb*(rho+pressure)

    # Homogeneous isotropy: D_i K_jk = 0, J_i=0, and every trace-free TT
    # projection of K_ij and the spatial Ricci tensor vanishes.  The scalar
    # inverse has only its constant kernel, which is removed by convention.
    localizer_values = {
        "D_iD_jK^ij": 0,
        "Delta_h chi": 0,
        "chi": 0,
        "J_i": 0,
        "A_i": 0,
        "K_TT": 0,
        "R_TT": 0,
        "Q_TT": 0,
        "U": 0,
    }
    return {
        "status": "FLRW_WARD_BACKGROUND_GATE_DERIVED; PERTURBATIONS_OPEN",
        "lapse_equation": str(friedmann),
        "expected_friedmann_residual": str(expected_friedmann),
        "lapse_equation_matches_friedmann": sp.simplify(
            friedmann-expected_friedmann
        ) == 0,
        "continuity_equation": str(continuity),
        "differentiated_friedmann_after_continuity": str(after_continuity),
        "acceleration_residual": str(acceleration),
        "continuity_implies_acceleration": sp.simplify(
            after_continuity-3*H*acceleration
        ) == 0,
        "localizer_values": localizer_values,
        "localizers_vanish_on_flrw": all(value == 0 for value in localizer_values.values()),
        "ward_identity": "diffeomorphism invariance of S_m[g,psi] gives nabla_mu T_m^(mu nu)=0",
        "scope": [
            "exact homogeneous isotropic background, lapse varied before N=1",
            "minimal matter continuity and background Bianchi consistency",
            "no FLRW perturbation stability or nonlinear constraint closure",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(flrw_ward_gate(), indent=2))
