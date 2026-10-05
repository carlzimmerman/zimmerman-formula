"""PAPER42 figure + numbers: dark energy as the vacuum energy of the MOND field.
fig1_paper42_band.pdf: Lambda/a0^2 = (1/2) int 2y (nu_fix - 1) dy vs the turn-off y_t (k = 2), with the band of Lambda_obs/a0^2 allowed by measured a0
(lane V ensemble 1.097e-10 +- 12%, so Lambda/a0^2 = 73.19 x (1 +- 0.24)), the framework footing 32 pi, and the SPARC/planet window. Writes PAPER42_figures_numbers.json.
"""
import json, math, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__))
C1, INK, MUTED, BAND = "#2a78d6", "#1f1f1e", "#6f6e69", "#cde2fb"
def nm1(y, yt):
    return math.expm1(0.5 * math.log1p(1 / y)) / (1 + (y / yt)**2)
def L(yt):
    segs = [(1e-9, 1e-3), (1e-3, 1), (1, 10), (10, 1e2), (1e2, 1e3), (1e3, 1e5), (1e5, 1e7)]
    return 0.5 * sum(quad(lambda y: 2 * y * nm1(y, yt), s, e, limit=4000, epsabs=1e-10, epsrel=1e-10)[0] for s, e in segs)
obs = 32 * math.pi * (9.3603e-11 / 1.097e-10)**2
lo, hi = obs * (1 - 2 * 0.122), obs * (1 + 2 * 0.122)
yt_obs = brentq(lambda v: L(v) - obs, 5, 1e4); yt_lo = brentq(lambda v: L(v) - lo, 5, 1e4); yt_hi = brentq(lambda v: L(v) - hi, 5, 1e4)
yt_fw = brentq(lambda v: L(v) - 32 * math.pi, 5, 1e4)
plt.rcParams.update({"font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED,
                     "axes.spines.top": False, "axes.spines.right": False})
yts = np.geomspace(20, 2e3, 50)
fig, ax = plt.subplots(figsize=(5.6, 3.4))
ax.axhspan(lo, hi, color=BAND, lw=0)
ax.text(22, hi * 1.05, "measured $a_0$ (ensemble, $\\pm2\\sigma$)", color=MUTED, fontsize=7)
ax.axvspan(100, 2e3, color="#e9e8e2", lw=0, zorder=0)
ax.text(1.1e2, 25, "SPARC- and planet-allowed $y_t$", color=MUTED, fontsize=7)
ax.loglog(yts, [L(v) for v in yts], color=C1, lw=2, label="vacuum energy of the MOND field")
ax.axhline(32 * math.pi, color=INK, lw=1); ax.text(22, 32 * math.pi * 1.06, "$32\\pi$ ($\\kappa=1/2$ footing)", color=INK, fontsize=7)
ax.plot(yt_obs, obs, marker="o", ms=8, color=C1, mec="white", mew=2)
ax.set_xlabel("MOND turn-off $y_t = g_t/a_0$"); ax.set_ylabel("$\\Lambda/a_0^2$")
ax.set_ylim(15, 2e3); ax.grid(True, which="major", color="#e4e3dd", lw=0.5); ax.legend(frameon=False, fontsize=7.5, loc="upper left")
fig.tight_layout(); fig.savefig(os.path.join(HERE, "fig1_paper42_band.pdf")); plt.close(fig)
nums = {"obs_Lambda_over_a0sq": round(obs, 2), "obs_band_2sigma": [round(lo, 1), round(hi, 1)], "yt_obs": round(yt_obs, 1),
        "yt_band": [round(yt_lo, 1), round(yt_hi, 1)], "yt_framework": round(yt_fw, 1), "gt_obs_ms2": float(f"{yt_obs*1.097e-10:.3g}")}
json.dump(nums, open(os.path.join(HERE, "PAPER42_figures_numbers.json"), "w"), indent=1); print(nums)
