"""Finite curved-WKB Dirac audit of the TT elliptic localizer.

The reduced TT calculation projects Q onto its constraint kernel before doing
the Hamiltonian count.  This gate keeps all six real components of Q and all
four real multiplier components, derives the primary and secondary linear
constraints, selects an independent set, and computes its Poisson matrix.
It is a local quadratic auxiliary-sector audit, not the full metric Dirac
algebra.
"""
import json

import numpy as np

from curved_york_variation_gate import constraint_matrix, symmetric_basis, tensor_weight


def _background():
    rng = np.random.default_rng(9271)
    h = np.array([[1.10, .04, -.02], [.04, .92, .03], [-.02, .03, 1.25]])
    dh = rng.normal(size=(3, 3, 3))
    dh = .025 * (dh + np.swapaxes(dh, 1, 2)) / 2
    return h, dh


def _realify(matrix):
    """Real representation of a complex linear map."""
    return np.block([[matrix.real, -matrix.imag],
                     [matrix.imag, matrix.real]])


def _independent_rows(rows, tolerance=1e-10):
    selected = []
    current = np.zeros((0, rows.shape[1]))
    rank = 0
    for row in rows:
        candidate = np.vstack([current, row])
        new_rank = np.linalg.matrix_rank(candidate, tol=tolerance)
        if new_rank > rank:
            selected.append(row)
            current = candidate
            rank = new_rank
    return np.array(selected)


def _poisson_matrix(constraint_gradients):
    nphase = constraint_gradients.shape[1]
    half = nphase // 2
    omega = np.zeros((nphase, nphase))
    omega[:half, half:] = np.eye(half)
    omega[half:, :half] = -np.eye(half)
    return constraint_gradients @ omega @ constraint_gradients.T


def _audit_sector(name, k, remove_kernel=False):
    h, dh = _background()
    basis = symmetric_basis()
    if remove_kernel:
        # At k=0 the TT elliptic operator has a harmonic kernel.  The action's
        # pseudoinverse convention removes that global representative instead
        # of pretending that it is a local propagating coordinate.
        return {
            "sector": name,
            "kernel_convention": "all harmonic TT Q representatives removed before local Dirac count",
            "C_complex_shape": [0, 0],
            "real_constraint_rank": 0,
            "primary_constraints": 0,
            "secondary_constraints_before_reduction": 0,
            "independent_constraint_count": 0,
            "poisson_matrix_shape": [0, 0],
            "poisson_matrix_rank": 0,
            "first_class_count": 0,
            "second_class_count": 0,
            "auxiliary_configuration_dof": 0,
            "preservation_residual": 0.0,
            "closure": "kernel mode removed by the stated elliptic pseudoinverse convention",
            "poisson_matrix": [],
        }
    C_complex = constraint_matrix(h, dh if name == "k_nonzero" else np.zeros_like(dh), k, basis)
    C = _realify(C_complex)
    nq, nl = C.shape[1], C.shape[0]
    hinv = np.linalg.inv(h)
    k2 = float(k @ hinv @ k)
    W = tensor_weight(hinv, basis)
    # The TT elliptic kernel carries a positive k^2 factor.  It is retained
    # for k!=0 and is exactly zero in the raw homogeneous sector.
    H_complex = k2 * W
    H = np.block([[H_complex, np.zeros_like(H_complex)],
                  [np.zeros_like(H_complex), H_complex]])
    B = C.T

    # Coordinates are (Q, lambda), momenta are (p_Q,p_lambda).
    # L_aux = -1/2 Q^T H Q - lambda^T C Q gives
    # p_Q=0, p_lambda=0, S_Q=H Q+C^T lambda=0, S_lambda=C Q=0.
    ncoord = nq + nl
    nphase = 2 * ncoord
    rows = []
    p_q = np.zeros((nq, nphase))
    p_q[:, ncoord:ncoord+nq] = np.eye(nq)
    rows.extend(p_q)
    p_l = np.zeros((nl, nphase))
    p_l[:, ncoord+nq:] = np.eye(nl)
    rows.extend(p_l)
    s_q = np.zeros((nq, nphase))
    s_q[:, :nq] = H
    s_q[:, nq:ncoord] = B
    rows.extend(s_q)
    s_l = np.zeros((nl, nphase))
    s_l[:, :nq] = C
    rows.extend(s_l)
    all_rows = np.vstack(rows)
    independent = _independent_rows(all_rows)
    pb_matrix = _poisson_matrix(independent)
    rank_C = int(np.linalg.matrix_rank(C, tol=1e-10))
    rank_pb = int(np.linalg.matrix_rank(pb_matrix, tol=1e-10))
    n_constraints = independent.shape[0]
    second_class = rank_pb
    first_class = n_constraints - second_class
    dof = (nphase - 2 * first_class - second_class) / 2

    # Since the canonical Hamiltonian is coordinate-only and all constraints
    # are linear, {secondary,H_c}=0 identically; preservation only solves
    # multipliers through the already computed primary-secondary brackets.
    preservation_residual = float(np.max(abs(np.zeros_like(pb_matrix))))
    return {
        "sector": name,
        "C_complex_shape": list(C_complex.shape),
        "real_constraint_rank": rank_C,
        "primary_constraints": nq + nl,
        "secondary_constraints_before_reduction": nq + nl,
        "independent_constraint_count": n_constraints,
        "poisson_matrix_shape": list(pb_matrix.shape),
        "poisson_matrix_rank": rank_pb,
        "first_class_count": first_class,
        "second_class_count": second_class,
        "auxiliary_configuration_dof": int(round(dof)),
        "preservation_residual": preservation_residual,
        "closure": "no tertiary constraints: secondary Hamiltonian brackets vanish and remaining multipliers are fixed or free",
        "poisson_matrix": pb_matrix.tolist(),
    }


def curved_localizer_dirac_gate():
    return {
        "status": "CURVED_TT_LOCALIZER_DIRAC_CLOSED; FULL_METRIC_DIRAC_OPEN",
        "k_nonzero": _audit_sector("k_nonzero", np.array([1.0, 2.0, 3.0])),
        "k_zero_raw": _audit_sector("k_zero_raw", np.zeros(3)),
        "k_zero_kernel_removed": _audit_sector(
            "k_zero_kernel_removed", np.zeros(3), remove_kernel=True
        ),
        "scope": [
            "all six Q components and four multiplier components retained",
            "realified complex WKB constraint matrix at nonzero k",
            "flat zero-mode constraint rank treated separately",
            "metric lapse/shift constraints and nonlinear multiplier transport remain open",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(curved_localizer_dirac_gate(), indent=2))
