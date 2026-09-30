"""CFG233 systematics library: re-decomposition of the table under a stated systematic (used by attacks a, d, e and MUTATE-like checks)."""
import numpy as np
from CFG233_common import *


def redecompose(d, kfac=None, qtilt=0.0, s_press=3.0, zmed=None, pmin=0.0):
    """Return (mask, z, D, gbar, gobs) after: pressure scale s (V_c'^2 = V_c^2 - (1 - s/3) P, P = 3.356 sigma0^2 km^2/s^2),
    V_c tilt q (V_c' = V_c' 10^(q dz)), and a baryon-mass ratio kfac = assumed/true (g_bar' = g_bar/kfac), V_c fixed at V_c'."""
    z = d["z"]
    zmed = np.median(z) if zmed is None else zmed
    Vc2 = (d["Vc"]) ** 2
    Vb2 = (1 - d["f"]) * Vc2
    P = 2.0 * d["s0"] ** 2 * 1.678
    Vc2n = Vc2 - (1 - s_press / 3.0) * P
    Vc2n = Vc2n * 10 ** (2 * qtilt * (z - zmed))
    if kfac is not None:
        Vb2 = Vb2 / kfac
    f2 = 1 - Vb2 / Vc2n
    ok = (f2 > 0) & (f2 < 1) & (Vc2n > 0)
    gobs = Vc2n * 1e6 / (d["Re"] * KPC)
    gbar = Vb2 * 1e6 / (d["Re"] * KPC)
    D = gobs / gbar
    return ok, z, D, gbar, gobs


def measure(z, D, gbar, gobs, B=2000, seed=SEED_MAIN, kern="nu_mono", foot="canonical"):
    f_, r_ = delta_pair(D, gbar, z, kern, foot)
    ex = expected_slopes(gobs, z, kern, foot)
    sl = (ts(z, f_), ts(z, r_))
    out = dict(n=len(z), slope_flat=sl[0], slope_rival=sl[1], exp_R_flat=ex["rival"][0], exp_F_rival=ex["flat"][1])
    if B:
        bs = boot_ts(z, [f_, r_], B, seed)
        out.update(ci_flat=ci(bs[0]), ci_rival=ci(bs[1]), sd_flat=float(bs[0].std()), sd_rival=float(bs[1].std()))
        out["cls"] = classify(out["ci_flat"], out["ci_rival"])
        out["T_flat_vs_rival"] = (sl[0] - ex["rival"][0]) / out["sd_flat"]      # flat slope vs rival-true expectation
        out["T_rival_vs_rival"] = (sl[1] - 0.0) / out["sd_rival"]                # rival slope vs 0
        out["T_flat_vs_flat"] = (sl[0] - 0.0) / out["sd_flat"]
        out["T_rival_vs_flat"] = (sl[1] - ex["flat"][1]) / out["sd_rival"]
    return out
