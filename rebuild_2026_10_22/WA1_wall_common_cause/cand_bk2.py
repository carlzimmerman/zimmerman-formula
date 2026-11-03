"""BK2's closest no-fit row (a), g = I5(g_b, a0) [(8 pi/3) g_gas / sqrt(a0 g_b) + (g_star/g_b)^4], as a candidate for RQ3's rows. A description, no action; picked from about 2.7e10 expressions. kappa = 1/2 FITTED."""
import math
import numpy as np
NAME = "BK2 closest no-fit row (a)"; VERTICAL = ("R",)
def g(Q):
    gb = np.asarray(Q["gb"], float); a = Q["a0"]; gg = np.asarray(Q["gg"], float); pos = gb > 0; q = np.where(pos, gb, 1.0)
    gs = q - np.broadcast_to(gg, q.shape)
    with np.errstate(all="ignore"): v = q / -np.expm1(-np.sqrt(q / a)) * ((8 * math.pi / 3) * gg / np.sqrt(a * q) + (gs / q) ** 4)
    return np.where(pos, v, gb)
