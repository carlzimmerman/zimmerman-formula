"""BF3 candidate, generated. Description, no action, no fitted float; chosen from a search of about 1e10 tries. kappa = 1/2 FITTED."""
import math, numpy as np
NAME = 'BF3 F2'; EXPR = '(1.0+f*((((y*pi)+(y+0.5))-(inv1p(2.0)/(ell+f)))))'; WRAP = 3; VERTICAL = ("R",); HMUT = 1.0
_F = dict(sqrt=np.sqrt, log1p=np.log1p, inv1p=lambda x: 1 / (1 + x), sq=lambda x: x * x, pi=math.pi)
_USES_ELL = True
def _law(g, a): return 0.5 * g + np.sqrt(0.25 * g * g + a * g)
def g(Q):
    gb = np.asarray(Q["gb"], float); a = Q["a0"]; gg = np.asarray(Q["gg"], float); pos = gb > 0; gq = np.where(pos, gb, 1.0)
    y = gq / a; f = np.clip(np.broadcast_to(gg, gq.shape) / gq, 0.0, 1.0)
    ell = np.broadcast_to(np.asarray(Q["r"], float), gq.shape) * a / 299792458.0 ** 2 if _USES_ELL else y * 0
    with np.errstate(all="ignore"):
        H = HMUT * (eval(EXPR, {"__builtins__": {}}, dict(_F, y=y, ell=ell, f=f)) * np.ones_like(y))
        v = _law(gq, a * H) if WRAP == 1 else _law(gq * H, a) if WRAP == 2 else _law(gq, a) * H
    return np.where(pos, v, gb)
