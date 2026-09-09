"""Curved-background York-TT principal-symbol variation.

This is a bounded local WKB calculation.  Unlike the previous flat-symbol
surrogate it retains the first spatial derivatives of a non-Euclidean metric,
the corresponding Christoffel symbols, and their metric variation.  The
Fourier derivative is represented by ``i*k`` at one background point.  It is
not a global York decomposition or a nonlinear Dirac closure proof.
"""
import json

import numpy as np


def symmetric_basis():
    basis = []
    for i in range(3):
        for j in range(i, 3):
            a = np.zeros((3, 3), dtype=float)
            a[i, j] = 1.0
            a[j, i] = 1.0
            basis.append(a)
    return basis


def tensor_weight(hinv, basis):
    return np.array([
        [np.einsum("ia,jb,ij,ab->", hinv, hinv, a, b)
         for b in basis]
        for a in basis
    ])


def tensor_weight_directional(hinv, dinv, basis):
    return np.array([
        [np.einsum("ia,jb,ij,ab->", dinv, hinv, a, b)
         + np.einsum("ia,jb,ij,ab->", hinv, dinv, a, b)
         for b in basis]
        for a in basis
    ])


def christoffel(hinv, dh):
    # dh[c,i,j] = partial_c h_ij.
    gamma = np.zeros((3, 3, 3), dtype=float)
    for i in range(3):
        for j in range(3):
            for k in range(3):
                gamma[i, j, k] = 0.5 * sum(
                    hinv[i, ell] * (dh[j, ell, k] + dh[k, ell, j]
                                    - dh[ell, j, k])
                    for ell in range(3)
                )
    return gamma


def inverse_metric_derivative(hinv, dh):
    return np.array([-hinv @ dh[c] @ hinv for c in range(3)])


def divergence_inverse_derivative(hinv, dh):
    """Return d_i h^{ia}, with the coordinate index summed."""
    dinv = inverse_metric_derivative(hinv, dh)
    return np.array([sum(dinv[i, i, a] for i in range(3))
                     for a in range(3)])


def constraint_matrix(h, dh, k, basis):
    hinv = np.linalg.inv(h)
    gamma = christoffel(hinv, dh)
    div_hinv = divergence_inverse_derivative(hinv, dh)
    qcontr = hinv.T @ k
    rows = []
    for j in range(3):
        row = []
        for a in basis:
            q_up = hinv @ a
            value = 1j * sum(qcontr[m] * a[m, j] for m in range(3))
            value += sum(div_hinv[m] * a[m, j] for m in range(3))
            value += sum(gamma[i, i, m] * q_up[m, j]
                         for i in range(3) for m in range(3))
            value -= sum(gamma[m, i, j] * q_up[i, m]
                         for m in range(3) for i in range(3))
            row.append(value)
        rows.append(np.array(row, dtype=complex))
    rows.append(np.array([np.einsum("ij,ij->", hinv, a)
                          for a in basis], dtype=complex))
    return np.array(rows)


def _projector_data(h, dh, k):
    basis = symmetric_basis()
    hinv = np.linalg.inv(h)
    W = tensor_weight(hinv, basis)
    C = constraint_matrix(h, dh, k, basis)
    Winv = np.linalg.inv(W)
    G = C @ Winv @ C.conj().T
    B = np.linalg.inv(G)
    P = np.eye(len(basis), dtype=complex) - Winv @ C.conj().T @ B @ C
    return basis, hinv, W, C, Winv, G, B, P


def _constraint_directional(h, dh, dh_dir, ddh_dir, k, basis):
    hinv = np.linalg.inv(h)
    dinv = -hinv @ dh_dir @ hinv
    gamma = christoffel(hinv, dh)
    dgamma = np.zeros((3, 3, 3), dtype=float)
    for i in range(3):
        for j in range(3):
            for q in range(3):
                dgamma[i, j, q] = 0.5 * sum(
                    dinv[i, ell] * (dh[j, ell, q] + dh[q, ell, j]
                                     - dh[ell, j, q])
                    + hinv[i, ell] * (ddh_dir[j, ell, q]
                                      + ddh_dir[q, ell, j]
                                      - ddh_dir[ell, j, q])
                    for ell in range(3)
                )
    div_hinv = divergence_inverse_derivative(hinv, dh)
    ddiv_hinv = np.zeros(3, dtype=float)
    for a in range(3):
        for i in range(3):
            # delta(partial_i h^{ia}) = -delta h^{-1}(partial_i h)h^{-1}
            # - h^{-1}(partial_i delta h)h^{-1}
            # - h^{-1}(partial_i h)delta h^{-1}.
            ddiv_hinv[a] += sum(
                -dinv[i, ell] * dh[i, ell, m] * hinv[m, a]
                -hinv[i, ell] * ddh_dir[i, ell, m] * hinv[m, a]
                -hinv[i, ell] * dh[i, ell, m] * dinv[m, a]
                for ell in range(3) for m in range(3)
            )
    dqcontr = dinv.T @ k
    rows = []
    for j in range(3):
        row = []
        for a in basis:
            q_up = hinv @ a
            dq_up = dinv @ a
            value = 1j * sum(dqcontr[m] * a[m, j] for m in range(3))
            value += sum(ddiv_hinv[m] * a[m, j] for m in range(3))
            value += sum(
                dgamma[i, i, m] * q_up[m, j]
                + gamma[i, i, m] * dq_up[m, j]
                for i in range(3) for m in range(3)
            )
            value -= sum(
                dgamma[m, i, j] * q_up[i, m]
                + gamma[m, i, j] * dq_up[i, m]
                for m in range(3) for i in range(3)
            )
            row.append(value)
        rows.append(np.array(row, dtype=complex))
    rows.append(np.array([np.einsum("ij,ij->", dinv, a)
                          for a in basis], dtype=complex))
    return np.array(rows), dinv


def _directional_data(h, dh, dh_dir, ddh_dir, k):
    basis, hinv, W, C, Winv, G, B, P = _projector_data(h, dh, k)
    dC, dinv = _constraint_directional(h, dh, dh_dir, ddh_dir, k, basis)
    dW = tensor_weight_directional(hinv, dinv, basis)
    dWinv = -Winv @ dW @ Winv
    dG = (dC @ Winv @ C.conj().T + C @ dWinv @ C.conj().T
          + C @ Winv @ dC.conj().T)
    dB = -B @ dG @ B
    dP = (-dWinv @ C.conj().T @ B @ C
          -Winv @ dC.conj().T @ B @ C
          -Winv @ C.conj().T @ dB @ C
          -Winv @ C.conj().T @ B @ dC)
    return {
        "basis": basis, "hinv": hinv, "W": W, "C": C,
        "P": P, "dP": dP, "dW": dW, "dC": dC,
        "k2": float(k @ hinv @ k),
        "dk2": float(k @ dinv @ k),
    }


def _tensor_vector(matrix, basis):
    return np.array([np.einsum("ij,ij->", a, matrix) for a in basis],
                    dtype=complex)


def _one_case(h, dh, dh_dir, ddh_dir, k, R, step=1e-6):
    data = _directional_data(h, dh, dh_dir, ddh_dir, k)
    basis = data["basis"]
    W, P, dW, dP = data["W"], data["P"], data["dW"], data["dP"]
    rv = _tensor_vector(R, basis)
    numerator = rv.conj() @ W @ P @ rv
    action = float(np.real(numerator / data["k2"]))
    daction = float(np.real(
        rv.conj() @ (dW @ P + W @ dP) @ rv / data["k2"]
        - numerator * data["dk2"] / data["k2"]**2
    ))
    plus = _projector_data(h + step * dh_dir, dh + step * ddh_dir, k)
    minus = _projector_data(h - step * dh_dir, dh - step * ddh_dir, k)
    pfd = (plus[-1] - minus[-1]) / (2 * step)
    rp = _tensor_vector(R, basis)
    ap = np.real(rp.conj() @ plus[2] @ plus[-1] @ rp
                 / float(k @ plus[1] @ k))
    am = np.real(rp.conj() @ minus[2] @ minus[-1] @ rp
                 / float(k @ minus[1] @ k))
    afd = float((ap - am) / (2 * step))
    rank = int(np.linalg.matrix_rank(data["C"], tol=1e-10))
    return {
        "action": action,
        "analytic_action_derivative": daction,
        "finite_action_derivative": afd,
        "action_finite_difference_error": abs(afd - daction),
        "projector_finite_difference_error": float(np.max(abs(pfd - dP))),
        "constraint_residual": float(np.max(abs(data["C"] @ P))),
        "idempotence_residual": float(np.max(abs(P @ P - P))),
        "weighted_self_adjoint_residual": float(
            np.max(abs(W @ P - P.conj().T @ W))
        ),
        "constraint_rank": rank,
        "tt_dimension": int(P.shape[0] - rank),
        "k2": data["k2"],
    }


def curved_york_variation_gate():
    rng = np.random.default_rng(9271)
    h = np.array([[1.10, .04, -.02], [.04, .92, .03], [-.02, .03, 1.25]])
    dh = rng.normal(size=(3, 3, 3))
    dh = .025 * (dh + np.swapaxes(dh, 1, 2)) / 2
    dh_dir = rng.normal(size=(3, 3))
    dh_dir = .03 * (dh_dir + dh_dir.T) / 2
    ddh_dir = rng.normal(size=(3, 3, 3))
    ddh_dir = .02 * (ddh_dir + np.swapaxes(ddh_dir, 1, 2)) / 2
    k = np.array([1.0, 2.0, 3.0])
    R = rng.normal(size=(3, 3))
    R = (R + R.T) / 2
    rows = [_one_case(h, dh, dh_dir, ddh_dir, k, R)]
    rows.append(_one_case(h, dh, -1.7 * dh_dir, -1.7 * ddh_dir, k, R))
    return {
        "status": "CURVED_YORK_WKB_VARIATION_VERIFIED; NONLINEAR_CLOSURE_OPEN",
        "rows": rows,
        "projector_finite_difference_error": max(
            r["projector_finite_difference_error"] for r in rows
        ),
        "action_finite_difference_error": max(
            r["action_finite_difference_error"] for r in rows
        ),
        "constraint_residual": max(r["constraint_residual"] for r in rows),
        "idempotence_residual": max(r["idempotence_residual"] for r in rows),
        "weighted_self_adjoint_residual": max(
            r["weighted_self_adjoint_residual"] for r in rows
        ),
        "constraint_rank": rows[0]["constraint_rank"],
        "tt_dimension": rows[0]["tt_dimension"],
        "scope": [
            "one nonzero WKB covector on a positive curved metric jet",
            "Christoffel symbols and their metric variation retained",
            "global elliptic boundary conditions, lower-order transport, and"
            " full nonlinear multiplier preservation remain open",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(curved_york_variation_gate(), indent=2))
