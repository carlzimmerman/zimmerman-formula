#!/usr/bin/env python3
r"""Executable comparison of the live Fable 5.1 proposals with the strict target.

This is a scoped consistency audit, not a claim to rederive every perturbation
equation in the Fable directories.  It checks four algebraic statements that
are already enough to reject the two displayed proposals as strict fried-
chicken completions:

* the generalized-AeST document's literal ``-2 K(Q)`` DBI term has negative
  vacuum energy and negative quadratic kinetic curvature at its minimum;
* the sign of the document's ``+c2 (div A)^2`` does not match the FJ ``c2``
  used in its printed scalar-speed formula;
* in the clock-current proposal, minimally coupled baryons see a metric source
  ``rho_b+n``.  Ratio-locking ``n`` to ``rho_b`` rescales Newtonian gravity
  linearly and cannot produce the deep-MOND square-root response.

The DBI and source-scaling results below are generated from the displayed
functions. The c2 result is only an internal consistency comparison between
the document's literal sign and its separately printed FJ formula; it is not
an action-derived perturbation calculation. The proposal's self-reported mode
count is discussed in the audit document, not recertified here.
"""

import sys

import sympy as sp


def dbi_vacuum_diagnostics(sigma):
    """Return rho(Q0) and d^2[sigma*K]/dQ^2 at the DBI stationary point."""
    q, q0 = sp.symbols("q Q_0", real=True)
    m4, mu = sp.symbols("M4 mu", positive=True)
    kernel = -m4 * sp.sqrt(1 - mu**2 * (q - q0) ** 2 / m4)
    lagrangian = sp.sympify(sigma) * kernel
    rho = q * sp.diff(lagrangian, q) - lagrangian
    rho0 = sp.simplify(rho.subs(q, q0))
    kinetic_curvature = sp.simplify(sp.diff(lagrangian, q, 2).subs(q, q0))
    return rho0, kinetic_curvature


def c2_convention_residual():
    """Compare the document's printed FJ speed with its literal c2 sign map."""
    c2_doc, c14 = sp.symbols("c2_doc c14", positive=True)
    fj_speed_printed_as_doc = c2_doc * (2 - c14) / (c14 * (2 + 3 * c2_doc))
    c2_fj = -c2_doc
    speed_from_literal_doc_sign = c2_fj * (2 - c14) / (c14 * (2 + 3 * c2_fj))
    return sp.factor(fj_speed_printed_as_doc - speed_from_literal_doc_sign)


def clock_current_scaling_residual():
    """Compare metric-source scaling under rho_b -> s*rho_b with deep MOND."""
    s, rho, ratio = sp.symbols("s rho ratio", positive=True)
    source = (1 + ratio) * rho
    transformed = source.subs(rho, s * rho)
    actual_scaling = sp.simplify(transformed / source)
    linear_residual = sp.simplify(actual_scaling - s)
    mond_residual = sp.simplify(actual_scaling - sp.sqrt(s))
    return linear_residual, mond_residual


def run_audit():
    checks = []

    def check(label, condition, detail):
        ok = bool(condition)
        checks.append(ok)
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}: {detail}")

    print("=== Fable 5.1 strict-target comparison ===")
    rho_bad, kinetic_bad = dbi_vacuum_diagnostics(-2)
    rho_good, kinetic_good = dbi_vacuum_diagnostics(1)
    check("literal -2K vacuum sign", sp.sign(rho_bad) == -1, f"rho(Q0)={rho_bad}")
    check("literal -2K kinetic sign", sp.sign(kinetic_bad) == -1, f"L_QQ(Q0)={kinetic_bad}")
    check("sign mutation control", sp.sign(rho_good) == 1 and sp.sign(kinetic_good) == 1, f"sigma=+1 gives ({rho_good}, {kinetic_good})")

    convention_residual = c2_convention_residual()
    check("c2 convention consistency", sp.simplify(convention_residual) == 0, f"residual={convention_residual}")

    linear_residual, mond_residual = clock_current_scaling_residual()
    check("clock-current metric source remains linear", linear_residual == 0, f"linear residual={linear_residual}")
    check("clock-current metric source realizes deep-MOND scaling", mond_residual == 0, f"MOND residual={mond_residual}")

    fatal_generalized = (
        sp.sign(rho_bad) == -1
        or sp.sign(kinetic_bad) == -1
        or sp.simplify(convention_residual) != 0
    )
    fatal_clock_current = mond_residual != 0
    print(f"Generalized-AeST strict verdict: {'DEAD' if fatal_generalized else 'OPEN'}")
    print(f"Clock-current strict verdict: {'DEAD' if fatal_clock_current else 'OPEN'}")
    print(f"Diagnostic expectations met: {sum(checks)}/{len(checks)}")
    # Deliberately strict theory checks fail for the literal proposals.
    # A successful falsification audit exits zero when the derived failure
    # signatures are all present; it never relabels them as theory PASSes.
    expected_failures = sp.sign(rho_bad) == -1 and convention_residual != 0 and mond_residual != 0
    return fatal_generalized and fatal_clock_current and expected_failures


if __name__ == "__main__":
    sys.exit(0 if run_audit() else 1)
