#!/usr/bin/env python3
"""Regression: the historical linear-invisibility inference must fail.

Admissible S(u)=exp(-u), q=2, C=Pi_c=k=1, P=epsilon*sin(x),
periodic x in [0,2*pi]. This script deliberately asserts the legacy claim.
The expected outcome is exit 1 with a nonzero quadratic action coefficient.
"""
import sympy as sp

eps, x = sp.symbols("epsilon x", real=True)
action_density = sp.exp(-eps * sp.cos(x))
coefficient = sp.integrate(sp.diff(action_density, eps, 2).subs(eps, 0) / 2,
                           (x, 0, 2 * sp.pi))
print("Admissible periodic witness, quadratic action coefficient:", coefficient)
assert coefficient == 0, "REFUTED: a linear action boundary term does not remove the quadratic action"
