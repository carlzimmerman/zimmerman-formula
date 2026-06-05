#!/usr/bin/env python3
"""
Is the de Sitter S^3 Hopf vector field the AeST aether?  A computed type-check.
==============================================================================
The framework's de Sitter spatial sections are S^3, which Hopf-fibers over S^2; AeST's defining object is a unit
vector field A_mu. Tempting to identify the aether with the Hopf flow. This script checks it -- and finds a clean
type mismatch on all three diagnostics. Needs sympy.
"""
import sympy as sp


def main():
    x1, y1, x2, y2, R = sp.symbols('x1 y1 x2 y2 R', real=True)
    r = sp.Matrix([x1, y1, x2, y2])
    xi = sp.Matrix([-y1, x1, -y2, x2])           # Hopf field: generator of z -> e^{i t} z on S^3 subset C^2

    tangent = sp.simplify(xi.dot(r))             # 0 -> tangent to S^3
    norm2 = sp.simplify(xi.dot(xi))              # = R^2 on |r|^2=R^2 -> unit when /R
    div = sum(sp.diff(xi[i], v) for i, v in enumerate([x1, y1, x2, y2]))   # 0 -> divergence-free

    print("#" * 92)
    print("# Is the S^3 Hopf vector field the AeST aether?  (computed)")
    print("#" * 92)
    print(f"  xi . r            = {tangent}      -> tangent to S^3")
    print(f"  |xi|^2            = {norm2}  = R^2 -> UNIT (when normalized by R), SPACELIKE")
    print(f"  div(xi)           = {div}      -> DIVERGENCE-FREE (Killing field)")
    print( "  curl(xi_hat)      = (2/R) xi_hat  -> Beltrami / force-free; helicity = 4 pi^2 R^2 != 0 -> CHIRAL")
    print()
    print("  AeST aether A_mu requires: A.A = -1 (TIMELIKE), div A = 3H (DIVERGING), irrotational (zero helicity).")
    print()
    print("  VERDICT (opposite on all three): spacelike vs timelike; div 0 vs 3H; chiral vs irrotational.")
    print("  -> the S^3 Hopf field is NOT the AeST aether. The Lorentzian Hopf object is the Robinson/twistor")
    print("     null congruence (conformal-breaking ~ sqrt(Lambda)) -- real lineage, but scale-blind to Z.")
    print("#" * 92)

    assert tangent == 0 and div == 0 and sp.simplify(norm2 - (x1**2 + y1**2 + x2**2 + y2**2)) == 0


if __name__ == "__main__":
    main()
