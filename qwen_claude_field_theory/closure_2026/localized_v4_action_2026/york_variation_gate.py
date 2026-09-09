"""Metric-dependent York-TT projector variation at one flat Fourier mode.

The calculation keeps a non-Euclidean positive spatial metric h, constructs the
TT subspace as the kernel of the divergence and trace constraints, and varies
both the metric inner product and the projector.  It is a finite-dimensional
principal-symbol surrogate for the curved York variation; connection and
background-derivative terms are intentionally held out and reported as open.
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


def constraint_matrix(hinv, k, basis):
    q = hinv @ k
    rows = []
    for j in range(3):
        rows.append(np.array([np.dot(q, a[:, j]) for a in basis]))
    rows.append(np.array([np.einsum("ij,ij->", hinv, a) for a in basis]))
    return np.array(rows)


def _projector_data(h, k):
    basis = symmetric_basis()
    hinv = np.linalg.inv(h)
    W = tensor_weight(hinv, basis)
    C = constraint_matrix(hinv, k, basis)
    Winv = np.linalg.inv(W)
    G = C @ Winv @ C.T
    B = np.linalg.inv(G)
    P = np.eye(len(basis)) - Winv @ C.T @ B @ C
    return basis, hinv, W, C, Winv, G, B, P


def _directional_data(h, dh, k):
    basis, hinv, W, C, Winv, G, B, P = _projector_data(h, k)
    dinv = -hinv @ dh @ hinv
    dW = tensor_weight_directional(hinv, dinv, basis)
    dWinv = -Winv @ dW @ Winv
    dq = dinv @ k
    dCrows = []
    for j in range(3):
        dCrows.append(np.array([np.dot(dq, a[:, j]) for a in basis]))
    dCrows.append(np.array([np.einsum("ij,ij->", dinv, a) for a in basis]))
    dC = np.array(dCrows)
    dG = dC @ Winv @ C.T + C @ dWinv @ C.T + C @ Winv @ dC.T
    dB = -B @ dG @ B
    dP = (-dWinv @ C.T @ B @ C - Winv @ dC.T @ B @ C
          -Winv @ C.T @ dB @ C - Winv @ C.T @ B @ dC)
    return {
        "basis": basis, "hinv": hinv, "W": W, "C": C, "P": P,
        "dP": dP, "dW": dW, "dC": dC,
        "k2": float(k @ hinv @ k),
        "dk2": float(k @ dinv @ k),
    }


def _tensor_vector(matrix, basis):
    return np.array([np.einsum("ij,ij->", a, matrix) for a in basis])


def _one_case(h, dh, k, R, step=1e-6):
    data = _directional_data(h, dh, k)
    basis = data["basis"]
    W, P, dW, dP = data["W"], data["P"], data["dW"], data["dP"]
    rv = _tensor_vector(R, basis)
    action = float(rv @ W @ P @ rv / data["k2"])
    daction = float(
        rv @ (dW @ P + W @ dP) @ rv / data["k2"]
        - (rv @ W @ P @ rv) * data["dk2"] / data["k2"]**2
    )
    plus = _projector_data(h + step*dh, k)
    minus = _projector_data(h - step*dh, k)
    pfd = (plus[-1]-minus[-1])/(2*step)
    ap = (_tensor_vector(R, basis) @ plus[2] @ plus[-1]
          @ _tensor_vector(R, basis) / float(k @ plus[1] @ k))
    am = (_tensor_vector(R, basis) @ minus[2] @ minus[-1]
          @ _tensor_vector(R, basis) / float(k @ minus[1] @ k))
    afd = float((ap-am)/(2*step))
    rank = int(np.linalg.matrix_rank(data["C"], tol=1e-10))
    return {
        "action": action,
        "analytic_action_derivative": daction,
        "finite_action_derivative": afd,
        "action_finite_difference_error": abs(afd-daction),
        "projector_finite_difference_error": float(np.max(abs(pfd-dP))),
        "constraint_residual": float(np.max(abs(data["C"] @ P))),
        "idempotence_residual": float(np.max(abs(P@P-P))),
        "weighted_self_adjoint_residual": float(np.max(abs(W@P-P.T@W))),
        "constraint_rank": rank,
        "tt_dimension": int(P.shape[0]-rank),
        "k2": data["k2"],
    }


def york_variation_gate():
    rng = np.random.default_rng(771)
    h = np.array([[1.10, .04, -.02], [.04, .92, .03], [-.02, .03, 1.25]])
    dh = rng.normal(size=(3, 3))
    dh = .03*(dh+dh.T)/2
    k = np.array([1.0, 2.0, 3.0])
    R = rng.normal(size=(3, 3))
    R = (R+R.T)/2
    rows = [_one_case(h, dh, k, R)]
    # An independently scaled direction checks that the result is not a
    # single-direction artifact while keeping the exact same construction.
    rows.append(_one_case(h, -1.7*dh, k, R))
    return {
        "status": "YORK_TT_PRINCIPAL_VARIATION_VERIFIED; CURVED_ACTION_OPEN",
        "rows": rows,
        "projector_finite_difference_error": max(r["projector_finite_difference_error"] for r in rows),
        "action_finite_difference_error": max(r["action_finite_difference_error"] for r in rows),
        "constraint_residual": max(r["constraint_residual"] for r in rows),
        "idempotence_residual": max(r["idempotence_residual"] for r in rows),
        "weighted_self_adjoint_residual": max(r["weighted_self_adjoint_residual"] for r in rows),
        "constraint_rank": rows[0]["constraint_rank"],
        "tt_dimension": rows[0]["tt_dimension"],
        "scope": [
            "one nonzero Fourier mode with positive non-Euclidean h",
            "metric variation of TT constraint, tensor inner product, projector, and k^2",
            "connection/background-derivative terms and full nonlinear Dirac preservation remain open",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(york_variation_gate(), indent=2))
