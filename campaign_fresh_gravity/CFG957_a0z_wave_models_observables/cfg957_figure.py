"""CFG957 figure: predicted a0(z) envelopes for the owner's idea (2026-10-21), a wave in a0(z), on the panel-(d) layout of
FIGURE_SUMMARY_2026-10-21 (points, flat line, rival a0 ∝ H(z), CFG689 band: all read from its plotted_numbers.json, read only).

Model curves: M1 (V = V0 + m^2 phi^2 / 2, two new constants m and r_i), masses m/H0 in {3, 5, 10, 20, 40}, readings eps / -p / V,
recomputed with cfg957.py's solver at r_max from cfg957.json (band-only, frozen rule) and at the post-hoc theta*-tight bracket
from cfg957_posthoc.json (reported only).  kappa = 1/2 FITTED; filled = canonical, open = alt footing, never pooled.

Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg957_figure.py      (seconds; < 0.5 GB) -> cfg957_a0z_envelopes.png
"""
import json
import math
import os
import sys

os.environ.setdefault("OMP_NUM_THREADS", "1")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

import cfg957 as C

PN = C.PN
MAIN = json.load(open(os.path.join(HERE, "cfg957.json")))["results"]
PH = json.load(open(os.path.join(HERE, "cfg957_posthoc.json")))
FOOTS = ("canonical", "alt")
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOTFAC = {f: A0["canonical"] / A0[f] for f in FOOTS}
COL = {"canonical": "#0072B2", "alt": "#D55E00"}
MFC = {"canonical": COL["canonical"], "alt": "white"}
INK, GREY = "#1a1a1a", "#6b6b6b"
GREEN, PURPLE, ORANGE, ORANGE_D = "#009E73", "#CC79A7", "#E69F00", "#9C5A00"

# ------------------------------------------------------------------ record items (read only)
BAND = []
for z in ("1.0", "1.2", "1.5", "2.0", "2.33"):
    BAND.append((float(z), PN[f"d.band.{z}.q16"]["value"], PN[f"d.band.{z}.q50"]["value"], PN[f"d.band.{z}.q84"]["value"]))
ZC, HZ = C.ZC223, C.HZ223
P6E = PN["d.p6_e20"]["value"]
PTS = []
for tag, mk, dz in (("meerkat", "D", 0), ("rc100_q1", "o", 0), ("rc100_q2", "o", 0), ("rc100_q3", "o", 0), ("aless", "*", 0),
                    ("alpine6", "s", 0), ("cristal_re", "p", -0.11), ("cristal_rout", "p", 0.11)):
    g = lambda k: PN[f"d.pt.{tag}.{k}"]["value"]
    PTS.append(dict(z=g("z") + dz, s=g("s"), l68=g("lo68"), h68=g("hi68"), l95=g("lo95"), h95=g("hi95"), mk=mk, ul=False))
PTS.append(dict(z=PN["d.pt.rc100_q4.z"]["value"], s=PN["d.pt.rc100_q4.s"]["value"], mk="o", ul=True))

# ------------------------------------------------------------------ model curves
ZG = np.linspace(0.0, 5.75, 700)


def curve(mH0, r_i, rd):
    o = C.model(mH0, r_i, ngrid=30001)
    rr = C.ratio(o, rd)
    return np.array([C.interp_z(o, rr, z) for z in ZG])


band_only, tight = [], []
for m in C.XMASS:
    for rd in C.READ:
        rmax = MAIN["M1_X"][str(m)]["rmax"]["r_max"][rd]
        band_only.append(curve(m, rmax, rd))
        tight.append(curve(m, min(PH["PH2"][str(m)]["r_theta"], rmax), rd))
band_only, tight = np.array(band_only), np.array(tight)
ex_mp = curve(10.0, MAIN["M1_X"]["10.0"]["rmax"]["r_max"]["-p"], "-p")
ex_eps = curve(10.0, MAIN["M1_X"]["10.0"]["rmax"]["r_max"]["eps"], "eps")

# ------------------------------------------------------------------ figure
plt.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Arial", "DejaVu Sans"], "mathtext.fontset": "dejavusans",
    "font.size": 10, "axes.titlesize": 11.5, "axes.labelsize": 10.5, "xtick.labelsize": 9.5, "ytick.labelsize": 9.5,
    "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": 0.8, "axes.edgecolor": "#333333",
    "savefig.facecolor": "white", "figure.facecolor": "white", "legend.frameon": False,
})
fig, ax = plt.subplots(figsize=(10.5, 7.6))
fig.subplots_adjust(left=0.08, right=0.985, top=0.885, bottom=0.215)
ax.set_yscale("log")
YLO, YHI, YCLIP = 0.042, 70.0, 0.115

# high-z prediction window
ax.axvspan(2.5, 5.75, color="#8c8c8c", alpha=0.08, lw=0, zorder=0)
ax.text(4.12, 48.0, "high-z prediction window (z > 2.5)\nno expansion datum here (CFG956 K5):\nonly kinematic a$_0$ can test the wave",
        fontsize=8.2, color=INK, ha="center", va="top", linespacing=1.15)

# envelopes
lo_b, hi_b = np.nanmin(band_only, axis=0), np.nanmax(band_only, axis=0)
lo_t, hi_t = np.nanmin(tight, axis=0), np.nanmax(tight, axis=0)
ax.fill_between(ZG, np.maximum(lo_b, YLO), hi_b, color=ORANGE, alpha=0.22, lw=0, zorder=1)
ax.fill_between(ZG, np.maximum(lo_t, YLO), hi_t, color=ORANGE, alpha=0.55, lw=0, zorder=1.2)
ax.plot(ZG, ex_mp, color=ORANGE_D, lw=1.7, zorder=3)
ax.plot(ZG, ex_eps, color=ORANGE_D, lw=1.4, ls=(0, (5, 2.5)), zorder=3)

# record curves
zc = ZC <= 5.75
ax.plot(ZC[zc], HZ[zc], color=PURPLE, lw=2.4, zorder=2)
ax.axhline(1.0, color=INK, lw=1.4, zorder=2)
zb = np.array([b[0] for b in BAND]); lo = np.array([b[1] for b in BAND]); md = np.array([b[2] for b in BAND]); hi = np.array([b[3] for b in BAND])
ax.fill_between(zb, lo, hi, color=GREEN, alpha=0.30, lw=0, zorder=1.5)
ax.plot(zb, md, color=GREEN, lw=1.5, zorder=2.5)
ax.fill_between([2.33, 2.5], [lo[-1]] * 2, [hi[-1]] * 2, color=GREEN, alpha=0.12, lw=0, zorder=1.5)

# decisive target at z 2.5 (CFG689 P6)
f = 10 ** P6E
ax.errorbar([2.5], [1.0], yerr=[[1 - 1 / f], [f - 1]], fmt="none", ecolor=INK, elinewidth=2.2, capsize=5, capthick=1.6, zorder=7)
ax.text(2.57, 0.80, f"decisive point:\nσ ≈ {P6E:.2f} dex at z ≈ 2.5\n(CFG689 P6)", fontsize=7.8, color=INK, ha="left", va="top")

# points
for p in PTS:
    for fo in FOOTS:
        k = FOOTFAC[fo]
        x = p["z"] + (-0.045 if fo == "canonical" else 0.045)
        if p["ul"]:
            ax.annotate("", xy=(x, p["s"] * k / 2.2), xytext=(x, p["s"] * k), arrowprops=dict(arrowstyle="-|>", color=COL[fo], lw=1.3), zorder=5)
            ax.plot([x], [p["s"] * k], marker="_", ms=9, mew=2.0, color=COL[fo], zorder=6)
            continue
        l95 = max(p["l95"] * k, YCLIP); l68 = max(p["l68"] * k, YCLIP)
        ax.plot([x, x], [l95, min(p["h95"] * k, YHI)], color=COL[fo], lw=0.9, zorder=4)
        ax.plot([x, x], [l68, min(p["h68"] * k, YHI)], color=COL[fo], lw=3.2, solid_capstyle="butt", zorder=4, alpha=0.9)
        if p["l95"] * k < YCLIP:
            ax.plot([x], [YCLIP], marker="v", ms=3.6, color=COL[fo], zorder=4)
        ax.plot([x], [p["s"] * k], marker=p["mk"], ms=9.5 if p["mk"] == "*" else 6.2, color=COL[fo], mfc=MFC[fo], mec=COL[fo], mew=1.3, zorder=6)

# direct labels
ax.text(3.0, 5.6, "rival: a$_0 \\propto$ H(z)", fontsize=9.0, color=PURPLE, fontweight="bold", ha="center", va="bottom")
ax.text(0.30, 1.05, "flat a$_0$", fontsize=8.8, color=INK, fontweight="bold", ha="left", va="bottom")
ax.text(0.22, 0.70, "CFG689 native band, 68%\n(ε reading of a$_0$)", fontsize=8.0, color=GREEN, fontweight="bold", ha="left", va="top")
i35 = int(np.argmin(np.abs(ZG - 3.6)))
ax.annotate("m = 10 H$_0$, −p reading:\nthe wave (5 extrema, z ≤ 5)", xy=(ZG[i35], ex_mp[i35]), xytext=(3.15, 0.22), fontsize=7.8, color=ORANGE_D,
            arrowprops=dict(arrowstyle="-", color=ORANGE_D, lw=0.8), ha="center", va="top")
i15 = int(np.argmin(np.abs(ZG - 1.62)))
ax.annotate("same m, ε reading:\nmonotone staircase\n(no peak possible)", xy=(ZG[i15], ex_eps[i15]), xytext=(0.62, 0.36), fontsize=7.8, color=ORANGE_D,
            arrowprops=dict(arrowstyle="-", color=ORANGE_D, lw=0.8), ha="center", va="top")

ax.set_xlim(-0.12, 5.75); ax.set_ylim(YLO, YHI)
ax.set_yticks([0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50]); ax.set_yticklabels(["0.1", "0.2", "0.5", "1", "2", "5", "10", "20", "50"])
ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
ax.set_xlabel("redshift  z")
ax.set_ylabel(r"a$_0$(z) / a$_0$(footing, today)")
fig.text(0.08, 0.955, "a$_0$ across redshift: the owner's idea (2026-10-21), a wave in a$_0$(z)", fontsize=13.5, fontweight="bold", color=INK, ha="left")
fig.text(0.08, 0.918, "Predicted envelopes from a light scalar dark-energy field, V = V$_0$ + m²φ²/2 (two new constants m, r$_i$; the record's own rates give no wave), "
         "on the panel-(d) layout", fontsize=9.2, color=GREY, ha="left")
leg = [Line2D([], [], marker="o", ls="none", ms=6.5, color=COL["canonical"], mfc=MFC["canonical"], label="canonical  a$_0$ = 9.3603×10$^{-11}$"),
       Line2D([], [], marker="o", ls="none", ms=6.5, color=COL["alt"], mfc="white", mec=COL["alt"], mew=1.3, label="alt  a$_0$ = 1.1312×10$^{-10}$ m s$^{-2}$"),
       Patch(color=ORANGE, alpha=0.22, label="M1 envelope, band-only r$_{max}$ (frozen rule; m 3–40 H$_0$, readings ε, −p, V)"),
       Patch(color=ORANGE, alpha=0.55, label="M1 envelope, θ*-tight bracket (post hoc, no class weight)")]
ax.legend(handles=leg, loc="upper left", fontsize=8.0, ncol=1, borderaxespad=0.3)
CAP = ("The owner's idea (2026-10-21): a0(z) oscillates like a wave, larger early, on the way down now. Points (filled canonical, open alt; thick 68%, thin 95% "
       "statistical; baryon-mass systematics not drawn) and the CFG689 band are the record's, read from the 2026-10-21 summary figure. Orange: the M1 scalar "
       "for m = 3–40 H0 in the ε, −p and V readings of a0; the record's own rates (H_Λ, a0/c, √(Gρ)) are overdamped and give no wave. Light orange uses "
       "r_max from CFG689's band (z ≤ 2.33) and −p ≥ 0 only; dark orange adds a post-hoc θ* limit (CFG689's θ* rows are held back, K9 failed). "
       "κ = ½ fitted; footings never pooled; not a closed theory; nothing here says the data favour the framework.")
import textwrap
fig.text(0.08, 0.018, "\n".join(textwrap.wrap(CAP, 175)), fontsize=7.7, color="#404040", ha="left", va="bottom", linespacing=1.3)
out = os.path.join(HERE, "cfg957_a0z_envelopes.png")
fig.savefig(out, dpi=200)
print(f"wrote {out}")
print("band-only envelope at z 2.5/3.5/4.5 (ratio):", [f"{np.nanmin(band_only[:, j]):.3f}-{np.nanmax(band_only[:, j]):.3f}" for j in (int(np.argmin(np.abs(ZG - z))) for z in (2.5, 3.5, 4.5))])
print("theta*-tight envelope at z 2.5/3.5/4.5 (ratio):", [f"{np.nanmin(tight[:, j]):.3f}-{np.nanmax(tight[:, j]):.3f}" for j in (int(np.argmin(np.abs(ZG - z))) for z in (2.5, 3.5, 4.5))])
