"""POST-HOC, reported only (not frozen): does the fossil switch reduce the per-object scatter of resolved UFD residuals,
and where in the light-end window does the nominal-yield median cross zero? Choosing that m would be a one-parameter fit."""
import math, numpy as np, runpy, io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    g = runpy.run_path("fossil_switch.py")
RES, j317, sig_pred, km, HOM = g["RES"], g["j317"], g["sig_pred"], g["km_median"], g["HOM"]
UL = g["UL"]
R = {nm: (10 ** e["lR"] if e and e.get("lR") is not None else 1.0) for nm, e in zip(j317["NAMES"]["ufd"], j317["EST"]["-0.2|ufd"])}
Rul = [(10 ** e["lR"] if e and e.get("lR") is not None else 1.0) for e in j317["EST"]["-0.2|ul"]]
a0 = 9.36e-11
base = np.array([math.log10(d["sig"] / sig_pred(d, a0, 1.0)) for d in RES])
print(f"no switch: resolved scatter {base.std(ddof=1):.3f} dex")
for m in np.geomspace(2.0e-20, 4.4e-20, 9):
    sw = lambda d: 2 * math.pi * HOM(m) / d.get("sig", d.get("sig_ul")) > 4 / 3 * d["rh"]
    x = np.array([math.log10(d["sig"] / sig_pred(d, a0, R[d["name"]] if sw(d) else 1.0)) for d in RES])
    xu = [math.log10(d["sig_ul"] / sig_pred(d, a0, r if sw(d) else 1.0)) for d, r in zip(UL, Rul)]
    print(f"m {m:.2e}: KM median {km(x, xu):+.3f}, resolved scatter {x.std(ddof=1):.3f} dex")
