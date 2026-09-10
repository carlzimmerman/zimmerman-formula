#!/usr/bin/env python3
"""Audit the CAM static reduction against the actual Einstein--Hilbert term.

The CAM gate used ``M2*(Phi'-Psi')**2`` as its static Einstein density.  This
script derives sqrt(-g) R directly for the isotropic Newtonian-gauge metric
with fields depending on one Cartesian coordinate and expands to quadratic
order.  After dropping total derivatives, the Einstein--Hilbert density is
``M2*(Psi')**2 - 2*M2*Phi'*Psi'``.  Therefore the CAM density contains an extra
``M2*(Phi')**2``.  The difference is not a harmless boundary term: it removes
the GR Poisson term and is exactly what made the previous AQUAL combination
pass.  The gate also computes the unique quadratic acceleration counterterm
needed to reproduce the advertised difference-square density.  That
counterterm is a genuine preferred-clock operator whose covariant constraint,
PPN and stability costs remain open.

This is a falsification gate, not a no-go theorem for every possible action.
It proves that the currently displayed CAM action does not derive the claimed
static density from S_EH alone.
"""

import json
import sys
import sympy as sp


FAILS = []
CHECKS = 0


def check(name, condition, detail=""):
    global CHECKS
    CHECKS += 1
    ok = bool(condition)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" ({detail})" if detail else ""), flush=True)
    if not ok:
        FAILS.append(name)


def derive_eh_static():
    eps, x = sp.symbols("eps x", real=True)
    t, ycoord, zcoord = sp.symbols("t y z", real=True)
    coords = (t, x, ycoord, zcoord)
    phi = sp.Function("Phi")(x)
    psi = sp.Function("Psi")(x)
    metric = sp.diag(-(1 + 2 * eps * phi),
                     1 - 2 * eps * psi,
                     1 - 2 * eps * psi,
                     1 - 2 * eps * psi)
    inverse = metric.inv()
    dim = 4
    gamma = [[[sp.S(0) for _ in range(dim)] for _ in range(dim)] for _ in range(dim)]
    for a in range(dim):
        for b in range(dim):
            for c in range(dim):
                gamma[a][b][c] = sp.simplify(sum(
                    inverse[a, d] * (
                        sp.diff(metric[d, c], coords[b])
                        + sp.diff(metric[d, b], coords[c])
                        - sp.diff(metric[b, c], coords[d])
                    ) / 2 for d in range(dim)
                ))
    ricci = [[sp.S(0) for _ in range(dim)] for _ in range(dim)]
    for a in range(dim):
        for b in range(dim):
            ricci[a][b] = sp.simplify(sum(
                sp.diff(gamma[c][a][b], coords[c])
                - sp.diff(gamma[c][a][c], coords[b])
                + sum(gamma[c][c][d] * gamma[d][a][b]
                      - gamma[c][b][d] * gamma[d][a][c]
                      for d in range(dim))
                for c in range(dim)
            ))
    scalar = sp.simplify(sum(inverse[a, b] * ricci[a][b]
                             for a in range(dim) for b in range(dim)))
    density = sp.sqrt(-metric.det()) * scalar
    quadratic = sp.expand(sp.series(density, eps, 0, 3).removeO()).coeff(eps, 2)
    # Integrate by parts algorithmically for terms f*g'' (boundary terms dropped).
    p, q = sp.diff(phi, x), sp.diff(psi, x)
    pp, qq = sp.diff(phi, x, 2), sp.diff(psi, x, 2)
    quadratic_ibp = sp.expand(quadratic).subs({
        phi * pp: -p ** 2,
        phi * qq: -p * q,
        psi * pp: -p * q,
        psi * qq: -q ** 2,
    })
    # The substitution above can leave products in a different factor order.
    quadratic_ibp = sp.expand(quadratic_ibp).subs({
        pp * phi: -p ** 2,
        qq * phi: -p * q,
        pp * psi: -p * q,
        qq * psi: -q ** 2,
    })
    quadratic_ibp = sp.simplify(quadratic_ibp)
    M2 = sp.symbols("M2", positive=True)
    eh_density = sp.simplify(M2 * quadratic_ibp / 2)
    cam_eh_density = M2 * (p - q) ** 2
    discrepancy = sp.simplify(cam_eh_density - eh_density)
    return {
        "symbols": {"eps": eps, "x": x, "Phi": phi, "Psi": psi, "M2": M2},
        "quadratic_raw": quadratic,
        "eh_density_ibp": eh_density,
        "cam_eh_density": cam_eh_density,
        "discrepancy": discrepancy,
    }


def main():
    data = derive_eh_static()
    phi = data["symbols"]["Phi"]
    psi = data["symbols"]["Psi"]
    x = data["symbols"]["x"]
    M2 = data["symbols"]["M2"]
    p, q = sp.diff(phi, x), sp.diff(psi, x)
    expected_eh = M2 * (q ** 2 - 2 * p * q)
    expected_discrepancy = M2 * p ** 2
    check("EH-1 direct Christoffel/Ricci expansion has the expected quadratic EH density after boundary terms",
          sp.simplify(data["eh_density_ibp"] - expected_eh) == 0,
          f"L_EH^(2)={data['eh_density_ibp']}")
    check("EH-2 the advertised CAM difference-square density is not the EH reduction",
          sp.simplify(data["cam_eh_density"] - data["eh_density_ibp"]) != 0,
          f"CAM-EH={data['discrepancy']}")
    check("EH-3 the mismatch is exactly a Phi-gradient-squared term, not a boundary term",
          sp.simplify(data["discrepancy"] - expected_discrepancy) == 0,
          f"Delta L={data['discrepancy']}")

    # Adding +M2 a_i a^i in unitary gauge contributes +M2*(Phi')^2 at this order.
    acceleration_counterterm = M2 * p ** 2
    repaired = sp.simplify(data["eh_density_ibp"] + acceleration_counterterm)
    check("EH-4 a +M2 a_mu a^mu counterterm is the unique displayed quadratic repair",
          sp.simplify(repaired - data["cam_eh_density"]) == 0,
          "repair = +M2(Phi')^2 in unitary static gauge")

    # Show why the prior AQUAL cancellation depended on the non-EH term.
    rho = sp.Function("rho")(x)
    ell = sp.Function("ell")(x)
    u = sp.Function("u")(x)
    a0 = sp.symbols("a0", positive=True)
    yy = sp.diff(u, x) / a0
    Q = yy ** 2 + 2 * (1 + yy) * sp.exp(-yy) - 2
    true_density = data["eh_density_ibp"] + 2 * M2 * a0 ** 2 * Q + ell * (sp.diff(u, x) - p) + rho * phi
    cam_density = data["cam_eh_density"] + 2 * M2 * a0 ** 2 * Q + ell * (sp.diff(u, x) - p) + rho * phi

    def euler(L, field):
        return sp.simplify(sp.diff(L, field) - sp.diff(sp.diff(L, sp.diff(field, x)), x))

    ephi_true = euler(true_density, phi)
    eu = euler(true_density, u)
    ephi_cam = euler(cam_density, phi)
    # Put u'=Phi' and Phi'=Psi' only after independent variation.
    subs_branch = {u: phi, psi: phi}
    true_sum = sp.simplify((ephi_true + eu).subs(subs_branch))
    cam_sum = sp.simplify((ephi_cam + eu).subs(subs_branch))
    flux = 4 * M2 * (1 - sp.exp(-p / a0)) * p
    check("AQUAL-1 true EH plus the auxiliary relation retains the GR Poisson term",
          sp.simplify(true_sum - (rho + 2 * M2 * sp.diff(phi, x, 2) - sp.diff(flux, x))) == 0,
          f"true Phi+u residual={true_sum}")
    check("AQUAL-2 the previous pure AQUAL equation occurs only after the extra Phi'^2 term is inserted",
          sp.simplify(cam_sum - (rho - sp.diff(flux, x))) == 0,
          f"CAM Phi+u residual={cam_sum}")

    result = {
        "checks": {"count": CHECKS, "passed": CHECKS - len(FAILS)},
        "derived": {
            "quadratic_raw": str(data["quadratic_raw"]),
            "eh_density_ibp": str(data["eh_density_ibp"]),
            "cam_eh_density": str(data["cam_eh_density"]),
            "discrepancy": str(data["discrepancy"]),
            "true_eh_plus_auxiliary_sum": str(true_sum),
            "cam_plus_auxiliary_sum": str(cam_sum),
        },
        "status": "CAM_STATIC_REDUCTION_OBSTRUCTION" if FAILS else "CAM_STATIC_REDUCTION_AUDITED",
        "scope": "1D static weak-field reduction of isotropic 4D EH metric; full covariant counterterm analysis remains open",
    }
    print("RESULT_JSON=" + json.dumps(result, sort_keys=True))
    if FAILS:
        print(f"EH STATIC REDUCTION GATE FAILED: {FAILS}")
        return 1
    print(f"EH STATIC REDUCTION GATE COMPLETE: {CHECKS}/{CHECKS} checks PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
