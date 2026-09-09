"""Direct two-dimensional symbolic Ward identity for minimally coupled matter."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


def ward_identity():
    t, x = sp.symbols("t x")
    N = sp.Function("N")(t, x)
    A = sp.Function("A")(t, x)
    phi = sp.Function("phi")(t, x)
    Vfun = sp.Function("V")
    V = Vfun(phi)
    coords = (t, x)
    g = sp.diag(-N**2, A**2)
    gi = sp.simplify(g.inv())
    Gamma = [[[0 for _ in coords] for _ in coords] for _ in coords]
    for a in range(2):
        for b in range(2):
            for c in range(2):
                Gamma[a][b][c] = sp.simplify(
                    sum(
                        gi[a, d]
                        * (sp.diff(g[d, c], coords[b]) + sp.diff(g[d, b], coords[c]) - sp.diff(g[b, c], coords[d]))
                        / 2
                        for d in range(2)
                    )
                )
    grad = [sp.diff(phi, q) for q in coords]
    kinetic = sp.simplify(sum(gi[i, j] * grad[i] * grad[j] for i in range(2) for j in range(2)))
    T = [[sp.simplify(sum(gi[i, j] * grad[j] * grad[n] for j in range(2)) - (1 if i == n else 0) * (kinetic / 2 + V)) for n in range(2)] for i in range(2)]
    box_phi = sp.simplify(
        sum(
            sp.diff(N * A * gi[i, j] * grad[j], coords[i])
            for i in range(2)
            for j in range(2)
        )
        / (N * A)
    )
    eom = sp.simplify(box_phi - sp.diff(V, phi))
    residuals = []
    for n in range(2):
        div = sum(sp.diff(T[i][n], coords[i]) for i in range(2))
        div += sum(Gamma[i][i][l] * T[l][n] for i in range(2) for l in range(2))
        div -= sum(Gamma[l][i][n] * T[i][l] for l in range(2) for i in range(2))
        # With the stated stress convention, div(T) - E_phi*d_phi vanishes.
        residuals.append(sp.simplify(div - eom * grad[n]))
    return {
        "stress_definition": "T^mu_nu = grad^mu(phi) grad_nu(phi) - delta^mu_nu[(grad phi)^2/2 + V]",
        "residual_t": str(residuals[0]),
        "residual_x": str(residuals[1]),
        "ward_identity": all(r == 0 for r in residuals),
        "scope": "ordinary scalar matter minimally coupled to the same metric g; gravitational covariance is separate",
    }


if __name__ == "__main__":
    result = ward_identity()
    out = Path(__file__).with_name("run_001")
    out.mkdir(exist_ok=True)
    (out / "matter_ward_results.json").write_text(json.dumps(result, indent=2) + "\n")
    print("MINIMAL_MATTER_WARD_GATE")
    print(f"ward_identity: {result['ward_identity']}")
    status = "PASS" if result["ward_identity"] else "FAIL"
    print(f"STATUS: {status} (matter identity; full gravity algebra remains open)")
