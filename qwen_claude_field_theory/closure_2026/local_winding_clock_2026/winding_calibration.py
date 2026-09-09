"""Bounded assembly-history calibration using the values recorded by L75."""

from functools import lru_cache

import sympy as sp


@lru_cache(None)
def calibration_report():
    Q_rec = sp.Integer(0)
    Q_gal = sp.log(3)
    Q_cl = sp.log(sp.Rational(17, 10))
    eta_ceiling = sp.Rational(248, 1000)
    beta_min = sp.simplify(-sp.log(eta_ceiling) / Q_gal)
    eta = lambda q, b: sp.exp(-b * q)
    eta_rec = sp.simplify(eta(Q_rec, beta_min))
    eta_gal = sp.simplify(eta(Q_gal, beta_min))
    eta_cl = sp.simplify(eta(Q_cl, beta_min))
    return {
        "source": "fable_independent_2026/L75_clock_winding_transmission.py",
        "Q_rec": Q_rec,
        "Q_gal": Q_gal,
        "Q_cl": Q_cl,
        "eta_ceiling": eta_ceiling,
        "beta_min": beta_min,
        "beta_interval": f"beta >= {beta_min}",
        "eta_rec_at_beta_min": eta_rec,
        "eta_gal_at_beta_min": eta_gal,
        "eta_cl_at_beta_min": eta_cl,
        "ordering_residual": sp.simplify(eta_cl - eta_gal),
    }


def encode(value):
    if isinstance(value, dict):
        return {str(key): encode(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(item) for item in value]
    if isinstance(value, sp.Basic):
        return str(value)
    return value


if __name__ == "__main__":
    import json

    print(json.dumps(encode(calibration_report()), indent=2))
