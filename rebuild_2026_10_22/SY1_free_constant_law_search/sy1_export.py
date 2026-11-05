"""Inert SymPy export for SY1; does not change Julia search operators or loss."""
import sympy as s

def mappings():
    return {
        'inv1p': lambda x, **_: s.Pow(s.Add(1, x, evaluate=False), -1, evaluate=False),
        'sqrt': lambda x, **_: s.Pow(x, s.Rational(1, 2), evaluate=False),
        'square': lambda x, **_: s.Pow(x, 2, evaluate=False),
        'log1p': lambda x, **_: s.log(s.Add(1, x, evaluate=False), evaluate=False),
    }
