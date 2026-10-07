"""POST-HOC (reported only, after K-B failed as frozen): the non-singular isothermal sphere's M/r oscillates around 2 sigma^2/G with a slowly
decaying amplitude, so 10-100 r_M was too close for rho0 = 1. Check the median M/r over 100-1000 and with rho0 = 100 (smaller core)."""
import numpy as np, runpy, io, contextlib, sys
sys.argv = ["x"]
src = open("cfg472_l2.py").read(); g = {"__file__": "cfg472_l2.py", "__name__": "ph"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(src[:src.index("res = {}")], g)
R, integ = g["R"], g["integrate"]
for r0 in (1.0, 100.0):
    o = integ(lambda p, r0=r0: r0 * np.exp(-p / 0.5), np.array([r0]), lambda rr: 0 * rr)
    for lo, hi in ((10, 100), (100, 1000)):
        m = (R >= lo) & (R <= hi); print(f"rho0 {r0:6.1f}: median M/r over {lo}-{hi} = {np.median(o[m, 0] / R[m]):.4f}")
