#!/usr/bin/env python3
"""Audit the scale-output equation in the PAPER27 source.

The constitutive slope and the speed of light were both denoted by ``c`` in
one displayed equation. This script derives the relation with an explicit
slope ``n`` and flags the ambiguous source token without editing the published
paper silently.
"""

from __future__ import annotations

import re
from pathlib import Path

import sympy as sp


def main() -> int:
    s, n, g, g_n = sp.symbols("s n g g_N", positive=True)
    # Deep branch: mu(g/s) = n*g/s + O(g^2), so mu*g = g_N.
    deep_equation = sp.Eq(n * g**2 / s, g_n)
    derived_a0_over_s = sp.simplify(sp.solve(deep_equation, g**2)[0] / (s * g_n))
    checks = {
        "deep_branch_equation": sp.simplify(
            (n * g**2 / s - g_n).subs(g**2, s * g_n / n)
        ) == 0,
        "a0_over_s_is_inverse_slope": derived_a0_over_s == 1 / n,
    }
    # PAPER27 defines s=c_light*sqrt(G*rho), so the physical coefficient is
    # a0/[c_light*sqrt(G*rho)] = 1/n. Search the source for the overloaded c.
    tex = Path(__file__).resolve().parents[1] / "papers_2026" / "PAPER27_parameter_free_rar_2026.tex"
    source = tex.read_text(encoding="utf-8")
    checks["published_source_contains_ambiguous_c"] = bool(
        re.search(r"a_0=s/c", source) and re.search(r"kappa.*1/c", source)
    )
    for name, ok in checks.items():
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print("  deep equation:", deep_equation)
    print("  corrected: mu_n(g/s)=n*g/s+O(g^2) => a0=s/n")
    print("  corrected coefficient: kappa=a0/[c_light*sqrt(G*rho)] = 1/n")
    print("  the source display uses c for the slope in this line; rename it n")
    print("  to avoid confusing it with the speed of light c_light.")
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
