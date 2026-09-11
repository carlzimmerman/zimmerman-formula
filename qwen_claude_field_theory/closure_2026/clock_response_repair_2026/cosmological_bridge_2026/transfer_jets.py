"""Extra derivatives of the unchanged logarithmic/cubic constitutive P.

All t subscripts mean partial tau derivatives holding X fixed. Coefficients
and their first two tau derivatives come from Model.background(tau)['raw'].
No new coefficient history or action is constructed.
"""
from functools import lru_cache
from math import isfinite

import sympy as s


@lru_cache(maxsize=1)
def _evaluator():
    base = s.symbols('qb U d Hb ell', positive=True)
    first = s.symbols('qb1 U1 d1 Hb1 ell1', real=True)
    second = s.symbols('qb2 U2 d2 Hb2 ell2', real=True)
    qb, U, d, Hb, _ = base
    X, gamma = s.symbols('X gamma', real=True)
    P = (-U*s.log((U-2*d*X)/(U-2*d*qb**2))/2
         +3*gamma*qb*Hb*(X-qb**2))

    def partial_tau(expression):
        return sum(s.diff(expression, z)*zd
                   for z, zd in zip(base+first, first+second))

    Pt = partial_tau(P)
    Ptt = partial_tau(Pt)
    expressions = dict(P_XXX=s.diff(P, X, 3), P_XXt=s.diff(Pt, X, 2),
                       P_Xtt=s.diff(Ptt, X), P=P, P_X=s.diff(P, X),
                       P_XX=s.diff(P, X, 2), P_t=Pt, P_Xt=s.diff(Pt, X), P_tt=Ptt)
    return tuple(expressions), s.lambdify(
        (*base, *first, *second, X, gamma), tuple(expressions.values()),
        'numpy', cse=True)


def extra_jets(model, tau, X, *, include_lower=False):
    """Return exactly P_XXX/P_XXt/P_Xtt as floats at an interior scalar X.

    include_lower=True also returns P/P_X/P_XX/P_t/P_Xt/P_tt for independent
    comparison with the original Model.jets evaluator. For physical-time
    evolution: d(P_Xt)/dt = tau_dot*P_Xtt + 2*q*qdot*P_XXt.
    """
    tau, X = float(tau), float(X)
    if not isfinite(tau) or not isfinite(X):
        raise ValueError('tau and X must be finite')
    background = model.background(tau)
    if (background['U']-2*background['d']*X <= 0
            or background['U']-2*background['d']*background['q']**2 <= 0):
        raise ValueError('constitutive logarithm domain boundary reached')
    names, evaluate = _evaluator()
    values = evaluate(*background['raw'], X, model.gamma)
    result = {name: float(value) for name, value in zip(names, values)}
    return result if include_lower else {name: result[name] for name in names[:3]}
