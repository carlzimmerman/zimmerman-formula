#!/usr/bin/env python3
"""CFG515 library (FROZEN_CRITERIA.md sections 1-2): the census retention f_ret per object and the PAPER45 edge.  Nothing here is a
result; the scripts import it.

  f_ret   primary  = CFG416's declared fret_of(log10 M_ta [Msun/h]) with M_b,now = f_ret f_b16 M_ta / h (f_b16 = 0.157, h = 0.674,
                     CFG416's constants), solved self-consistently per object;
          bracket  = constant 0.07 and 0.18 (PAPER45 v1.0 census spread);
          MUTATE   = constant 1.0 (the PM value applied to real galaxies) and 0.01 (unphysically depleted).
  edge    supply M_cold = (1 - f_b)/f_b * M_b,now / f_ret, f_b = 0.02237/0.14237 (engine); point mass:
          r_edge = r_M / ln(1 + f_ret f_b/(1 - f_b)), r_M = sqrt(G M_b,now / a0).
"""
import math
import os
from scipy.optimize import brentq

FB = 0.02237 / 0.14237                      # engine f_b (CFG423/424/485/487)
COLD_PER_B = (1.0 - FB) / FB                # 5.364
FB16, H16 = 0.157, 0.674                    # CFG416's constants inside x_supply / fret_of


def fret_of(lM):
    """CFG416 cfg416_pm.py fret_of, copied verbatim (FRETX = 1)."""
    if lM < 12.5: f = 0.10
    elif lM < 13.5: f = 0.10 + 0.45 * (lM - 12.5)
    else: f = min(0.55 + 0.30 * (lM - 13.5), 0.90)
    return min(f, 1.0)


def fret_census(Mb_now):
    """self-consistent root of f = fret_of(log10(M_ta [Msun/h])), M_ta = M_b,now h / (f f_b16).  Returns (f_ret, log10 M_ta [Msun/h])."""
    lMta = lambda f: math.log10(Mb_now * H16 / (f * FB16))
    g = lambda f: fret_of(lMta(f)) - f
    lo, hi = 0.05, 0.95
    if g(lo) <= 0:            # cannot happen for fret_of >= 0.10
        f = lo
    elif g(hi) >= 0:
        f = hi
    else:
        f = brentq(g, lo, hi, xtol=1e-14, rtol=1e-14)
    return f, lMta(f)


MODES_MAIN = ("census", "lo07", "hi18")
MODES_MUT = ("one", "dep01")
CONST = {"lo07": 0.07, "hi18": 0.18, "one": 1.0, "dep01": 0.01}


def fret(mode, Mb_now):
    if mode == "census":
        return fret_census(Mb_now)[0]
    return CONST[mode]


def ln_fac(f):
    return math.log1p(f * FB / (1.0 - FB))


def r_edge_pm(Mb_now, G, a0, f):
    """point-mass edge in the units of G, a0 (any consistent set)."""
    return math.sqrt(G * Mb_now / a0) / ln_fac(f)


def modes():
    return MODES_MUT if os.environ.get("CFG515_MUTATE", "0") == "1" else MODES_MAIN
