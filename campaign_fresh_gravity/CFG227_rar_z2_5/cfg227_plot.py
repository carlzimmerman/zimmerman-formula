#!/usr/bin/env python3
"""CFG227 figure: the compiled radial-acceleration relation at z = 2-5.  COMPILATION; CALIBRATION-LIMITED; NOT BLIND.  Classes present: S, L, D (class M absent).  Conversions as published; LambdaCDM has no a0.
Reads cfg227_points.csv and cfg227_rar_z2_5_results.json.  No law verdict."""
import os, csv, json, math, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
sys.path.insert(0, CFG)
import CFG4_common as K
J = json.load(open(os.path.join(LANE, "cfg227_rar_z2_5_results.json")))
R = list(csv.DictReader(open(os.path.join(LANE, "cfg227_points.csv"))))
A0, A0A = K.A0["canonical"], K.A0["alt"]
OM = 0.315
E = lambda z: math.sqrt(OM * (1 + z) ** 3 + 1 - OM)
fl = lambda x: float(x) if x not in ("", "nan") else float("nan")
fig, (ax, bx) = plt.subplots(1, 2, figsize=(17, 7.4), gridspec_kw=dict(width_ratios=[1.3, 1.0], wspace=0.2))
gb = np.logspace(-11.3, -7.6, 300)
def nu(y):
    return K.nu_mono(np.asarray(y))
ax.plot(gb, gb, color="#999999", lw=1, ls="-", label="Newtonian: g_obs = g_bar")
ax.plot(gb, gb * nu(gb / A0), color="k", lw=2.4, label="z = 0 RAR, flat a0 (canonical 9.36e-11)")
ax.plot(gb, gb * nu(gb / A0A), color="k", lw=1, ls="--", label="alt footing 1.13e-10")
for z, ls in ((2.5, "--"), (4.5, ":")):
    ax.plot(gb, gb * nu(gb / (A0 * E(z))), color="#d62828", lw=1.8, ls=ls, label=f"a0 x E(z), z = {z}")
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(2e-11, 4e-8); ax.set_ylim(2e-11, 4e-8)
CL = {"S": ("s", "#e07b00", "class S: Amvrosiadis (9), CO at alpha_CO = 0.92 (partly circular)"), "L": ("o", "#1d4e89", "class L: CRISTAL independent route (R_e, R_out; dust at T_d = 50 K)")}
for r in R:
    if r["class"] == "D":
        ax.plot([fl(r["g_bar"])], [fl(r["g_obs"])], ".", ms=4, color="#aaaaaa", alpha=0.6, zorder=1)
for r in R:
    c = r["class"]
    if c in CL:
        m, col, _ = CL[c]
        x, y = fl(r["g_bar"]), fl(r["g_obs"])
        lo_o, hi_o, lo_i, hi_i = fl(r["g_bar_outer_minus"]), fl(r["g_bar_outer_plus"]), fl(r["g_bar_inner_minus"]), fl(r["g_bar_inner_plus"])
        if math.isfinite(lo_o):
            ax.plot([min(lo_o, hi_o), max(lo_o, hi_o)], [y, y], color=col, lw=6, alpha=0.18, solid_capstyle="butt", zorder=2)
            ax.plot([min(lo_i, hi_i), max(lo_i, hi_i)], [y, y], color=col, lw=6, alpha=0.40, solid_capstyle="butt", zorder=3)
        ax.plot([x], [y], marker=m, ms=7.5, color=col, mec="k", mew=0.6, ls="none", zorder=5)
for r in R:
    if r["set"].startswith("S3"):
        x, y = fl(r["g_bar"]), fl(r["g_obs"])
        ax.annotate("", xy=(x * 2.4, y), xytext=(x, y), arrowprops=dict(arrowstyle="->", color="#2a9d55", lw=1.2), zorder=4)
        ax.plot([x], [y], marker="^", ms=6.5, mfc="white", mec="#2a9d55", mew=1.4, ls="none", zorder=5)
ax.set_xlabel(r"$g_{bar}$ (m s$^{-2}$)", fontsize=12); ax.set_ylabel(r"$g_{obs}=V^2/r$ (m s$^{-2}$)", fontsize=12)
ax.grid(True, which="major", color="#cccccc", lw=0.5, alpha=0.7)
h = [Line2D([], [], color="#999999", lw=1, label="Newtonian: g_obs = g_bar"), Line2D([], [], color="k", lw=2.4, label="z = 0 RAR, flat a0 (canonical 9.36e-11)"), Line2D([], [], color="k", lw=1, ls="--", label="alt footing 1.13e-10"),
     Line2D([], [], color="#d62828", lw=1.8, ls="--", label="a0 x E(z) at z = 2.5"), Line2D([], [], color="#d62828", lw=1.8, ls=":", label="a0 x E(z) at z = 4.5"),
     Line2D([], [], marker="s", color="#e07b00", mec="k", ls="none", ms=7.5, label=CL["S"][2]), Line2D([], [], marker="o", color="#1d4e89", mec="k", ls="none", ms=7.5, label=CL["L"][2]),
     Line2D([], [], marker="^", mfc="white", mec="#2a9d55", mew=1.4, ls="none", ms=7, label="ALPAKA (9): stars-only LOWER limit on g_bar (arrow)"), Line2D([], [], marker=".", color="#aaaaaa", ls="none", ms=6, label="class D, FLAGGED, not scored: CRISTAL fit route, RC100 z >= 2 (41)")]
ax.legend(handles=h, loc="upper left", fontsize=8.2, framealpha=0.93)
ax.set_title("the RAR at z = 2 to 5 (bars: gas-mass bands, dark = inner, light = outer)", fontsize=11.5, loc="left")
# right: delta_FLAT against z for the scored groups
cols = {"S1 Amvrosiadis": "#e07b00", "CRISTAL R_e independent (6)": "#1d4e89", "CRISTAL R_out independent (6)": "#5b8fd6"}
xs = {"S1 Amvrosiadis": 0.0, "CRISTAL R_e independent (6)": -0.07, "CRISTAL R_out independent (6)": 0.07}
for g, col in cols.items():
    pts = [r for r in R if r["group"] == g]
    z = np.array([fl(r["z"]) for r in pts]); d = np.array([fl(r["delta_FLAT"]) for r in pts]); dh = np.array([fl(r["delta_H(z)"]) for r in pts])
    ax2 = bx
    ax2.plot(z * (1 + xs[g] * 0.3), d, "s" if g.startswith("S1") else "o", ms=6.5, color=col, mec="k", mew=0.5, ls="none", alpha=0.85)
    q = J["groups"][g]["FLAT"]; qh = J["groups"][g]["H(z)"]
    xm = float(np.median(z)) * (1 + xs[g] * 0.3)
    bands = q["bands"]
    bx.errorbar([xm], [q["median"]], yerr=[[q["median"] - q["lo"]], [q["hi"] - q["median"]]], fmt="D", ms=11, color=col, mec="k", mew=1.2, elinewidth=2.4, capsize=6, zorder=6)
    if bands:
        bx.plot([xm * 1.03] * 2, [min(bands.values()), max(bands.values())], color=col, lw=9, alpha=0.25, solid_capstyle="butt", zorder=2)
        bx.plot([xm * 1.03] * 2, [min(bands["-inner"], bands["+inner"]), max(bands["-inner"], bands["+inner"])], color=col, lw=9, alpha=0.5, solid_capstyle="butt", zorder=3)
    bx.plot([xm], [qh["median"]], marker="v", ms=10, mfc="white", mec=col, mew=2, ls="none", zorder=6)
bx.axhline(0, color="k", lw=0.8)
bx.set_xscale("log"); bx.set_xticks([2, 2.5, 3, 4, 5, 6]); bx.set_xticklabels(["2", "2.5", "3", "4", "5", "6"]); bx.minorticks_off(); bx.set_xlim(1.8, 6.2)
bx.set_xlabel("redshift z", fontsize=12); bx.set_ylabel(r"$\delta=\log_{10}[g_{obs}/g_{pred}]$ (flat law: points and diamonds; open triangles: $a_0\propto H(z)$ group medians)", fontsize=10)
bx.grid(True, color="#cccccc", lw=0.5, alpha=0.7)
bx.set_title("delta against z: group medians with 95% bootstrap (diamonds); gas-shift bands", fontsize=11.5, loc="left")
fig.suptitle("Compiled RAR at z = 2-5: COMPILATION; CALIBRATION-LIMITED; NOT BLIND. Classes S, L, D present; class M absent (pooled class-M result: insufficient).", fontsize=12.3, x=0.06, ha="left", y=0.995)
pf = J["preflight"]
txt = ("Power pre-flight (mocks on these galaxies, sigma_int 0.15 dex): separating flat from a0 x E(z) is NOT possible in any scored group at the class bands (S1: signal 0.05 dex against a 0.39 requirement; "
       f"CRISTAL R_e {pf['CRISTAL R_e independent (6)']['signal']['H(z)']:.2f} vs {pf['CRISTAL R_e independent (6)']['syst'] + 2 * pf['CRISTAL R_e independent (6)']['sd_stat']:.2f}; R_out {pf['CRISTAL R_out independent (6)']['signal']['H(z)']:.2f} vs {pf['CRISTAL R_out independent (6)']['syst'] + 2 * pf['CRISTAL R_out independent (6)']['sd_stat']:.2f}).\n"
       "Conversions as published; the S1 baryon model is ours (thin discs at the CO half-light radius): 7 of 9 have g_obs below g_bar, so S1 cannot test any law. LambdaCDM has no a0. kappa = 1/2 is fitted. No law verdict.")
fig.text(0.06, 0.012, txt, fontsize=8.8, va="bottom", ha="left", linespacing=1.4)
fig.subplots_adjust(left=0.06, right=0.985, top=0.925, bottom=0.14)
out = os.path.join(LANE, "cfg227_rar_z2_5.png")
fig.savefig(out, dpi=150); print("wrote", out)
