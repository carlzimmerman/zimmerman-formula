"""SR3 candidate 2: found on real_alt_T0_free, formula unchanged on either footing. 2 fitted constant(s), labelled fitted. A description; no action, no field equation. kappa = 1/2 FITTED."""
import math
import numpy as np
from numpy import sqrt, exp, log1p, square
NAME = "SR3 form 2, real_alt_T0_free"; VERTICAL = ("R",); TRAINED_ON = ()
EQ = 'sqrt(log1p(f * square(square((yg / 0.014899191731101233) - two))) + 0.7493783437345501)'; T1 = False
_C = compile(EQ.replace("^", "**"), "f", "eval")
def g(Q):
    gb = np.asarray(Q["gb"], float); a = Q["a0"]; gg = np.maximum(np.asarray(Q["gg"], float), 0.0)
    with np.errstate(all="ignore"):
        s = np.where(gb > 0, gb, 1.0); L = np.where(gb > 0, gb * (0.5 + np.sqrt(0.25 + a / s)), gb); f = np.clip(gg / s, 0.0, 1.0); y = s / a
        v = eval(_C, dict(__builtins__={}, f=f, y=y, yg=f * y, ys=(1 - f) * y, one=1.0, two=2.0, pii=math.pi, sqrt=sqrt, exp=exp, log1p=log1p, square=square)) * np.ones_like(y)
        H = 1 + f * v if T1 else v
    return np.where(gb > 0, L * H, L)
