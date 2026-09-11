#!/usr/bin/env python3
"""Action-derived coefficient jets at the fixed repaired background slice.

The dimensionless slice is a=1, m=.1, v=.5, M2=Qc=1, I=.1, Lambda=.7.
``A`` below is the homogeneous chi charge density I/a**3, not a radial metric
factor; ``v`` is the stationary profile variable, not the ADM radial shift.
P jets are evaluated at X=q**2 only AFTER differentiation at fixed X;
W jets are evaluated at Y=0. Gamma is a constant coefficient during every
derivative. No source constraint, imposed force law, or observed data enter.

Sources within this repository:
  ../nonlinear_transport/stationary.py: exact m,v flow in log(a).
  ../cubic_background_completion/README.md: reconstructed log/sqrt action.
  ../cubic_background_completion/derive.py: independent on-branch jet checks.

The flow formulas are transcribed explicitly to avoid importing the large
finite-wavelength/source derivations. Tests evaluate the original stationary
flow independently. This supplies coefficients, not a nonlinear solution or
first-principles selection of the reconstructed action.
"""
from functools import lru_cache
import math

import sympy as s


@lru_cache(maxsize=1)
def _slice_expressions():
    """Differentiate the actual reconstructed functions in exact arithmetic."""
    a, m, v = s.symbols("a m v", positive=True)
    X, Y, gamma = s.symbols("X Y gamma", real=True)
    M2 = Qc = s.Integer(1)
    I, Lambda = s.Rational(1, 10), s.Rational(7, 10)
    A = I/a**3
    q = Qc/(1+m)
    U = m*q*A
    d = s.cancel(A*U/(2*q*(q*A+U)))
    ell = q*q*m/2
    H = s.sqrt((M2*Lambda + q*A + U)/(3*M2))
    H = s.simplify(H)
    Omega = s.cancel((q*A+U)/(3*M2*H*H))

    # d/d(log a), from stationary.symbolic(), before multiplying by H.
    mprime = 3*m*(Omega*m + 2*Omega + 2*m*v + 2*v)/(2*(m+2))
    vprime = (v-1)*(9*Omega*m**3 + 42*Omega*m**2 + 66*Omega*m
                    + 36*Omega + 6*m**3*v - 4*m**3 + 18*m*m*v
                    - 20*m*m + 24*m*v - 32*m + 12*v - 16)
    vprime /= 2*(m+1)*(m+2)**2
    flow = ((a, a*H), (m, mprime*H), (v, vprime*H))

    def partial_t(expression):
        # X and Y are excluded: these are coefficient time partials.
        return sum(s.diff(expression, coordinate)*velocity
                   for coordinate, velocity in flow)

    qdot = s.factor(partial_t(q))
    P = -U*s.log((U-2*d*X)/(U-2*d*q*q))/2
    P += 3*gamma*q*H*(X-q*q)
    W = U + 2*d*ell*(s.sqrt(1+Y/ell)-1) - 2*gamma*q*q*qdot
    V = U
    Pt = partial_t(P)
    Vt = partial_t(V)
    expressions = {
        "M2": M2, "Qc": Qc, "I": I, "Lambda": Lambda,
        "a": a, "m": m, "v": v, "H": H, "q": q, "A": A,
        "U": U, "d": d, "ell": ell,
        "W0": W.subs(Y, 0), "WY": s.diff(W, Y).subs(Y, 0),
        "P": P, "PX": s.diff(P, X), "PXX": s.diff(P, X, 2),
        "Pt": Pt, "PXt": s.diff(Pt, X), "Ptt": partial_t(Pt),
        "V": V, "Vt": Vt, "Vtt": partial_t(Vt),
        "Wt": partial_t(W).subs(Y, 0), "qdot": qdot,
        "qddot": partial_t(qdot), "Hdot": partial_t(H),
        "B0": A/q + 2*A*A/U, "gamma": gamma,
    }
    fixed_slice = {a: s.Integer(1), m: s.Rational(1, 10), v: s.Rational(1, 2)}
    # Crucial order: differentiate first, restrict to the branch second.
    return gamma, {
        key: s.simplify(expression.subs(X, q*q).subs(fixed_slice))
        for key, expression in expressions.items()
    }


def background(gamma=1e-6):
    """Return a fresh float dictionary of fixed-slice action coefficients.

    Gamma=0 and gamma=1e-6 are the tested controls. The symbolic formulas keep
    gamma free, but values outside those controls receive no health claim.
    """
    coupling = float(gamma)
    if not math.isfinite(coupling):
        raise ValueError("gamma must be finite")
    symbol, expressions = _slice_expressions()
    exact_gamma = s.Rational(str(coupling))
    return {key: float(expression.subs(symbol, exact_gamma).evalf(30))
            for key, expression in expressions.items()}


if __name__ == "__main__":
    import json
    print(json.dumps(background(), indent=2, sort_keys=True))
