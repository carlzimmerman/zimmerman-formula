#!/usr/bin/env python3
"""Check that the compact quadratic L used by the Dirac audit matches route B.

The route-B file performs the covariant Christoffel/Ricci expansion.  This
independent check imports its generated ``L2flat``, removes only the displayed
shift total derivative, and compares it exactly with the compact polynomial
used by ``aest_metric_scalar_dirac_audit.py``.
"""

from __future__ import annotations

import runpy
from pathlib import Path
import sympy as sp


def main() -> int:
    # Resolve the generated covariant source beside this verifier rather than
    # relative to the caller's working directory.  This keeps the advertised
    # repo-root and module-directory invocations equivalent.
    route_path = Path(__file__).resolve().with_name("fc_fk_routeB_covariant.py")
    source = runpy.run_path(str(route_path))
    t = source["t"]
    Phi_t, Bsh_t = source["Phi_t"], source["Bsh_t"]
    vv_t, chi_t = source["vv_t"], source["chi_t"]
    k, KB, K2, Q0 = source["k"], source["KB"], source["K2"], source["Q0"]

    P, V, C, vd, cd = sp.symbols("Phi v chi v_d chi_d", real=True)
    route = source["L2flat"]
    route = route.subs({
        Phi_t: P,
        Bsh_t: sp.Symbol("Bsh"),
        vv_t: V,
        chi_t: C,
        sp.Derivative(Phi_t, t): sp.Symbol("Phi_d"),
        sp.Derivative(Bsh_t, t): sp.Symbol("Bsh_d"),
        sp.Derivative(vv_t, t): vd,
        sp.Derivative(chi_t, t): cd,
    })
    route = sp.expand(route.subs({sp.Symbol("Bsh"): 0, sp.Symbol("Bsh_d"): 0}))

    manual = sp.expand((
        2*K2*P**2*Q0**2 - 4*K2*P*Q0*cd + 2*K2*cd**2
        + KB*P**2*k**2 - 2*KB*P*Q0*k**2*V - 2*KB*P*C*k**2
        + 2*KB*P*k**2*vd + KB*Q0**2*k**2*V**2
        + 2*KB*Q0*C*k**2*V - 2*KB*Q0*k**2*V*vd
        + KB*C**2*k**2 - 2*KB*C*k**2*vd + KB*k**2*vd**2
        + 4*P*Q0*k**2*V + 4*P*C*k**2 - 2*Q0**2*k**2*V**2
        - 4*Q0*C*k**2*V + 4*Q0*k**2*V*vd - 2*C**2*k**2
        + 4*C*k**2*vd
    ) / 2)
    residual = sp.factor(route - manual)
    print("SOURCE_MATCH_RESIDUAL=", residual)
    ok = residual == 0
    print("SOURCE_MATCH_STATUS=", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
