#!/usr/bin/env python3
"""AS042 T2: symbolic verification of the O(xi^2) identity (sympy).
Run as a SUBPROCESS by compute_as042.py so its memory footprint does not stack
on top of the numpy computation. Prints a single JSON object to stdout.
Claims proved symbolically here are exact within sympy's algebra (no numerics)."""
import json

res = {}
try:
    import sympy as sp
    xi, x = sp.symbols("xi x", real=True)
    nuf = sp.Function("nu")
    nup = sp.Function("nup")
    u_sym = x * (1 + x**2 + x**4 + x**6)          # u' = 1+3x^2+5x^4+7x^6 > 0 on R

    def M_expr(w):
        wx = w.diff(x)
        return ((nuf(wx) - 1) * wx).diff(x)

    m0 = M_expr(u_sym)
    Su_val = u_sym + (xi**2 / 2) * u_sym.diff(x, 2) + (xi**4 / 8) * u_sym.diff(x, 4)
    m1 = M_expr(Su_val)
    Sm1 = m1 + (xi**2 / 2) * m1.diff(x, 2) + (xi**4 / 8) * m1.diff(x, 4)
    up_s = u_sym.diff(x)
    dm = ((nuf(up_s) - 1 + up_s * nup(up_s)) * u_sym.diff(x, 3)).diff(x)
    pred = (xi**2 / 2) * (m0.diff(x, 2) + dm)
    resid = sp.simplify(sp.series(Sm1 - m0 - pred, xi, 0, 4).removeO().expand())
    c2 = sp.simplify(resid.coeff(xi, 2))
    res["1d_identity_O(xi2)_coeff(must_be_0)"] = str(c2)
    res["1d_identity_O(xi2)_exact_zero"] = bool(c2 == 0)
    # linear cell: truncated-filter series vs exact c*Lap e^{xi^2 Lap} u, through O(xi^4)
    c = sp.symbols("c", real=True)
    m0l = c * u_sym.diff(x, 2)
    m1l = c * Su_val.diff(x, 2)
    lhs_l = sp.series((m1l + (xi**2 / 2) * m1l.diff(x, 2) + (xi**4 / 8) * m1l.diff(x, 4)) - m0l,
                      xi, 0, 7).removeO().expand()
    exact_l = c * (u_sym.diff(x, 2) + xi**2 * u_sym.diff(x, 4) + (xi**4 / 2) * u_sym.diff(x, 6))
    diff_l = sp.simplify(sp.expand(lhs_l - exact_l.expand()))
    res["linear_cell_trunc4_vs_exact_thru_xi4_diff"] = str(diff_l)
    res["linear_cell_matches_thru_xi4"] = bool(diff_l == 0)
    # also: exact 1D linear-cell operator identity at the level of the interior
    # coefficient: S c Lap S u = c Lap S2 u for the FULL semigroup (not truncated):
    n = sp.symbols("n", integer=True, positive=True)
    res["note"] = "coefficient 1/2 enters through exp[(xi^2/2)Delta]: the factor 1/2 is the filter normalization, adopted as input"
except Exception as e:  # pragma: no cover
    res["error"] = repr(e)

print(json.dumps(res, indent=1))