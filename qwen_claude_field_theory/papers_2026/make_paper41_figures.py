"""PAPER41 figures + numbers: the kernel-tail fix (source lane: sonnet55_push/puzzle_32pi/p35_kernel_tail_fix.py).
fig1_paper41_tail.pdf  : nu - 1 vs y = g_N/a0 for the exact law and the fixed kernel (y_t = 128, 1e3, 1e5), with the SPARC range and the planetary bounds.
fig2_paper41_vacuum.pdf: the vacuum term Lambda/a0^2 = (1/2) int 2y (nu - 1) dy vs y_t for turn-off shapes k = 2, 3, 4, with 32 pi and the allowed y_t window.
Writes PAPER41_figures_numbers.json.  Palette: validated categorical slots 1-3 (dataviz reference), plus line style for secondary encoding.
"""
import json, math, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__))
C1, C2, C3, INK, MUTED = "#2a78d6", "#eb6834", "#1baf7a", "#1f1f1e", "#6f6e69"
a0 = 9.3603e-11
planets = {"Mercury": (4.228e8, 7.52e-13), "Venus": (1.211e8, 3.23e-11), "Earth": (6.336e7, 3.66e-14), "Mars": (2.729e7, 3.72e-14)}
def nm1(y, yt=None, k=2):
    base = math.expm1(0.5 * math.log1p(1 / y))
    return base if yt is None else base / (1 + (y / yt)**k)
def I(yt, k):
    segs = [(1e-9, 1e-3), (1e-3, 1), (1, 10), (10, 1e2), (1e2, 1e3), (1e3, 1e5), (1e5, 1e7)]
    return sum(quad(lambda y: 2 * y * nm1(y, yt, k), s, e, limit=4000, epsabs=1e-10, epsrel=1e-10)[0] for s, e in segs)
plt.rcParams.update({"font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED,
                     "axes.spines.top": False, "axes.spines.right": False})
# ---- fig 1
y = np.geomspace(1e-2, 1e9, 600)
fig, ax = plt.subplots(figsize=(5.6, 3.6))
ax.axvspan(1e-2, 1e2, color="#e9e8e2", lw=0)
ax.text(0.3, 2e-15, "SPARC range", color=MUTED, fontsize=8)
ax.loglog(y, [nm1(v) for v in y], color=INK, lw=2, label="exact law, $\\sqrt{1+1/y}$")
for yt, col, ls in ((128.0, C1, "-"), (1e3, C2, "--"), (1e5, C3, ":")):
    ax.loglog(y, [nm1(v, yt) for v in y], color=col, lw=2, ls=ls, label=f"fixed, $y_t$ = {yt:.0f}" if yt < 1e4 else "fixed, $y_t$ = $10^5$")
for nm, (yp, b) in planets.items():
    lim = b / (yp * a0)
    ax.plot(yp, lim, marker="v", ms=8, color=INK, mec="white", mew=1.5)
    off = {"Mars": (-30, -11), "Earth": (5, -11), "Mercury": (5, 5), "Venus": (5, 5)}[nm]
    ax.annotate(nm, (yp, lim), textcoords="offset points", xytext=off, fontsize=7, color=INK)
ax.set_xlabel("$y = g_N/a_0$"); ax.set_ylabel("$\\nu(y) - 1$ (fractional boost)")
ax.set_ylim(1e-24, 1e2); ax.grid(True, which="major", color="#e4e3dd", lw=0.5)
ax.legend(frameon=False, fontsize=7.5, loc="lower left")
fig.tight_layout(); fig.savefig(os.path.join(HERE, "fig1_paper41_tail.pdf")); plt.close(fig)
# ---- fig 2
yts = np.geomspace(30, 3e3, 40)
fig, ax = plt.subplots(figsize=(5.6, 3.4))
sol = {}
for k, col, ls in ((2, C1, "-"), (3, C2, "--"), (4, C3, ":")):
    vals = [I(v, k) / 2 for v in yts]
    ax.loglog(yts, vals, color=col, lw=2, ls=ls, label=f"turn-off shape $k$ = {k}")
    sol[k] = brentq(lambda v: I(v, k) - 64 * math.pi, 10, 1e4)
    ax.plot(sol[k], 32 * math.pi, marker="o", ms=8, color=col, mec="white", mew=2)
ax.axhline(32 * math.pi, color=INK, lw=1)
ax.text(32, 32 * math.pi * 1.12, "$32\\pi$", color=INK, fontsize=8)
ax.axvspan(100, 3e3, color="#e9e8e2", lw=0, zorder=0)
ax.text(1.1e2, 12, "allowed by SPARC and planets ($100 \\leq y_t \\leq 7.7\\times10^5$)", color=MUTED, fontsize=7)
ax.set_xlabel("turn-off $y_t$"); ax.set_ylabel("vacuum term $\\Lambda/a_0^2$")
ax.grid(True, which="major", color="#e4e3dd", lw=0.5); ax.legend(frameon=False, fontsize=7.5, loc="upper left")
fig.tight_layout(); fig.savefig(os.path.join(HERE, "fig2_paper41_vacuum.pdf")); plt.close(fig)
nums = {"yt_32pi": {str(k): round(v, 1) for k, v in sol.items()},
        "vac_k2": {"100": round(I(100.0, 2) / 2, 2), "128": round(I(128.0, 2) / 2, 2), "1000": round(I(1000.0, 2) / 2, 1)},
        "planet_ytmax": {nm: float(f"{10**brentq(lambda l: nm1(yp, 10**l) * yp * a0 - b, 0, 9):.3g}") for nm, (yp, b) in planets.items()},
        "worst_planet_ratio_128": float(f"{max(nm1(yp, 128.0) * yp * a0 / b for yp, b in planets.values()):.3g}"),
        "exact_law_earth_ratio": round(nm1(6.336e7) * 6.336e7 * a0 / 3.66e-14, 0)}
# offset reading with MEASURED a0: observed Lambda/a0^2 = 32 pi (9.3603e-11/a0)^2 -> y_t (k = 2)
off = {}
for lab, am in (("lane V ensemble 1.097e-10", 1.097e-10), ("SPARC record 1.0766e-10", 1.0766e-10), ("MIGHTEE 1.05e-10", 1.05e-10), ("framework footing 9.3603e-11", 9.3603e-11)):
    target = 32 * math.pi * (9.3603e-11 / am)**2
    off[lab] = {"Lambda_over_a0sq": round(target, 2), "yt_k2": round(brentq(lambda v: I(v, 2) / 2 - target, 5, 1e4), 1)}
nums["offset_reading_measured_a0"] = off
json.dump(nums, open(os.path.join(HERE, "PAPER41_figures_numbers.json"), "w"), indent=1)
print(json.dumps(nums, indent=1))
