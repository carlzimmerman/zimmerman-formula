"""Symbolic contract for the localized V4 clock--York action.

This module deliberately stops at the local constrained action.  It does not
silently identify an elliptic inverse with a propagating field; that question
is left to localized_dirac.py.
"""
import sympy as sp


C = sp.Rational(5, 3)
ell = sp.Rational(1, 100)
eta_U = sp.Rational(1, 12)
eta_X = sp.Rational(1, 3)
eta_V = -sp.Rational(1, 3)
eta_TT = -sp.Rational(1, 6)


def action_data():
    return {
        "status": "LOCALIZED_V4_ACTION_SPECIFIED; FULL_THEORY_OPEN",
        "coefficients": {
            "C": str(C), "ell": str(ell), "eta_U": str(eta_U),
            "eta_X": str(eta_X), "eta_V": str(eta_V),
            "eta_TT": str(eta_TT),
        },
        "constitutive_law": "mu(y) = 1 - exp(-y)",
        "action_terms": [
            "R - 2 Lambda - ell theta^2 + a0^2 f(a/a0)",
            "eta_U U^2 + eta_X U chi, U = K - <K> - chi",
            "eta_V (2 A_i J^i - A_i H1 A^i), J_i = D^m K_im",
            "eta_TT (K_TT^ij K_TT_ij - 2 Q^ij R_TT_ij + Q^ij H_TT Q_ij)",
            "lambda_chi (Delta_h chi - D_iD_j K^ij)",
            "lambda_A^i D_i A_i",
            "lambda_Q^ij (D^k Q_ki, Q^i_i)",
            "S_m[g, psi_m]",
        ],
        "constraints": [
            "Delta_h chi - D_iD_j K^ij",
            "H1 A - P_T div K",
            "H_TT Q - P_TT(3Ric)",
            "D_i A^i",
            "D^i Q_ij",
            "Q^i_i",
        ],
        "kernel_conventions": {
            "scalar": "Delta_h dagger removes the constant leaf mode",
            "one_form": "H1 dagger removes harmonic one-forms",
            "tt": "H_TT dagger removes the TT kernel",
        },
        "non_claims": [
            "No nonlinear Dirac closure is assumed",
            "No global causal prescription for a spatial inverse is assumed",
            "No complete PPN or empirical fit is claimed",
        ],
    }


def _static_density():
    a0, rho = sp.symbols("a0 rho", positive=True)
    px, py, pz = sp.symbols("p_x p_y p_z", real=True)
    qx, qy, qz = sp.symbols("q_x q_y q_z", real=True)
    p = sp.Matrix([px, py, pz])
    q = sp.Matrix([qx, qy, qz])
    y = sp.sqrt(p.dot(p)) / a0
    G = y**2 + 2*(1+y)*sp.exp(-y) - 2
    f = 2*y**2 - C*G
    density = 2*q.dot(q) - 4*p.dot(q) + a0**2*f
    return p, q, density, y


def localized_static_variation():
    p, q, density, y = _static_density()
    grad_phi = sp.Matrix([sp.diff(density, component) for component in p])
    grad_psi = sp.Matrix([sp.diff(density, component) for component in q])
    mu = 1 - sp.exp(-y)
    target_phi = -4*q + 2*(2-C*mu)*p
    target_psi = 4*(q-p)
    return {
        "psi_gradient": [sp.simplify(x) for x in grad_psi],
        "phi_gradient": [sp.simplify(x) for x in grad_phi],
        "psi_target": [sp.simplify(x) for x in target_psi],
        "phi_target": [sp.simplify(x) for x in target_phi],
        "psi_equation_is_slip_laplacian": all(
            sp.simplify(a-b) == 0 for a, b in zip(grad_psi, target_psi)
        ),
        "phi_equation_is_exponential_aqual": all(
            sp.simplify(a-b) == 0 for a, b in zip(grad_phi, target_phi)
        ),
        "newton_coupling": str(2/C),
        "mu": str(mu),
        "scope": "independent fixed-a0 static variation with K_ij=0",
    }
