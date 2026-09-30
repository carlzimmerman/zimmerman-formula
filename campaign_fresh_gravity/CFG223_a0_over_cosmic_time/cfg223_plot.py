#!/usr/bin/env python3
"""CFG223 figure: a0 over cosmic time.  Reads cfg223_results.json (written by cfg223_a0_over_time.py) and draws the four laws and the implied a0 ratios of the real data.
LambdaCDM has no a0: the purple curve is an effective-a0 PROXY.  Author decompositions, gas-route-limited; not a detection.  kappa = 1/2 is FITTED, NOT DERIVED.
Run:  python3 campaign_fresh_gravity/CFG223_a0_over_cosmic_time/cfg223_plot.py"""
import os, json, textwrap
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

LANE = os.path.dirname(os.path.abspath(__file__))
J = json.load(open(os.path.join(LANE, "cfg223_results.json")))
cur = J["curves"]; Z = np.array(cur["z"]); PTS = J["points"]
COL = {"FLAT": "#222222", "PROXY": "#7b2cbf", "H(z)": "#d62828", "M-DEC": "#1b9aaa"}
C_RC, C_CR = "#1d4e89", "#e07b00"
FLOOR, CEIL = 0.04, 30.0


def dotted_split(arr, zcut):
    arr = np.array(arr); m = Z <= zcut + 1e-9
    return (Z[m], arr[m]), (Z[~m | (Z == zcut)] if False else Z[Z >= zcut - 1e-9], arr[Z >= zcut - 1e-9])


def draw_curves(ax, zmax):
    sel = Z <= zmax + 1e-9
    env_lo = np.minimum.reduce([np.array(cur[f"DESI {k}"]) for k in J["desi"]]); env_hi = np.maximum.reduce([np.array(cur[f"DESI {k}"]) for k in J["desi"]])
    ax.fill_between(Z[sel], env_lo[sel], env_hi[sel], color=COL["M-DEC"], alpha=0.16, lw=0, zorder=1)
    for L, zc in (("FLAT", 99), ("PROXY", 5.0), ("H(z)", 99), ("M-DEC", 2.5)):
        y = np.array(cur[L]); a = Z <= zc + 1e-9; b = Z >= zc - 1e-9
        lw = 2.4 if L != "FLAT" else 2.0
        ax.plot(Z[a & sel], y[a & sel], color=COL[L], lw=lw, zorder=3)
        if zc < 99:
            ax.plot(Z[b & sel], y[b & sel], color=COL[L], lw=lw, ls=(0, (1.2, 2.2)), zorder=3)


def draw_point(ax, r, x, color, filled, marker, ms, ceil=CEIL, floor=FLOOR, committed=False):
    b = {float(k): v for k, v in r["bands"].items()}; nr = {float(k): v for k, v in r["band_noroot"].items()}
    if not committed:
        for tau, al, w in ((0.30, 0.12, 17), (0.15, 0.24, 9)):
            lo = floor if (nr[tau] or nr[-tau]) else min(b[tau], b[-tau]); hi = max(b[tau], b[-tau])
            ax.plot([x, x], [max(lo, floor), min(hi, ceil)], color=color, alpha=al, lw=w, solid_capstyle="butt", zorder=2)
            if nr[tau] or nr[-tau]:
                ax.plot([x], [floor * 1.06], marker="v", ms=4.5 if tau < 0.2 else 5.5, color=color, alpha=0.55 if tau < 0.2 else 0.35, ls="none", zorder=2)
    zl, zh = r["z_min"], r["z_max"]
    if not committed and r["dataset"] == "RC100":
        ax.plot([zl, zh], [r["s"], r["s"]], color=color, lw=0.9, alpha=0.45, zorder=3)
    open_low = r["unb_frac"] > 0.05
    for lo, hi, w in ((r["lo95"], r["hi95"], 1.1), (r["lo68"], r["hi68"], 3.6 if not committed else 1.8)):
        if committed:
            continue
        lo_d = floor if (open_low and w < 2) else max(lo, floor)
        ax.plot([x, x], [lo_d, min(hi, ceil)], color=color, lw=w, solid_capstyle="butt", zorder=4)
        if hi > ceil:
            ax.plot([x], [ceil / 1.06], marker="^", ms=5, color=color, ls="none", zorder=4)
        if open_low and w < 2:
            ax.plot([x], [floor * 1.06], marker="v", ms=5, color=color, ls="none", zorder=4)
    face = color if filled else "white"
    if committed:
        ax.plot([x], [r["s"]], marker="s", ms=6, mfc="none", mec="#888888", mew=1.2, ls="none", zorder=4)
    else:
        ax.plot([x], [r["s"]], marker=marker, ms=ms, mfc=face, mec=color, mew=1.8, ls="none", zorder=6)


fig, (ax, bx) = plt.subplots(1, 2, figsize=(17, 10.6), gridspec_kw=dict(width_ratios=[1.45, 1.0], wspace=0.14))
rc = [r for r in PTS if r["dataset"] == "RC100" and r["table"] == "corrected"]
rcc = [r for r in PTS if r["dataset"] == "RC100" and r["table"] == "committed"]
cr = [r for r in PTS if r["dataset"] == "CRISTAL"]
CRSTYLE = {"CR R_e fit": ("D", True, -0.10), "CR R_out fit": ("s", True, -0.035), "CR R_e ind": ("D", False, 0.035), "CR R_out ind": ("s", False, 0.10)}
for a, zmax, ylim in ((ax, 6.0, (FLOOR, CEIL)), (bx, 2.65, (0.15, 8.0))):
    draw_curves(a, zmax)
    for r in rcc:
        draw_point(a, r, r["z_med"] + 0.02, C_RC, False, "s", 6, ceil=ylim[1], floor=ylim[0], committed=True)
    for r in rc:
        draw_point(a, r, r["z_med"], C_RC, True, "o", 9, ceil=ylim[1], floor=ylim[0])
    if a is ax:
        for r in cr:
            mk, fl, dx = CRSTYLE[r["short"]]
            draw_point(a, r, r["z_med"] + dx * 1.6, C_CR, fl, mk, 9, ceil=ylim[1], floor=ylim[0])
    a.set_yscale("log"); a.set_ylim(*ylim)
    a.set_xlim(0.0 if a is ax else 0.5, 7.9 if a is ax else zmax)
    a.grid(True, which="major", color="#bbbbbb", lw=0.6, alpha=0.6); a.grid(True, which="minor", color="#dddddd", lw=0.4, alpha=0.5)
    a.set_xlabel("redshift z", fontsize=12)
    a.tick_params(labelsize=11)
    a.set_yticks([0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20] if a is ax else [0.2, 0.5, 1, 2, 3, 5]); a.set_yticklabels([str(v) for v in ([0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20] if a is ax else [0.2, 0.5, 1, 2, 3, 5])])
    a.minorticks_off()
ax.set_ylabel(r"implied $a_0(z)\,/\,a_0(0)$   (ratio to the footing's local $a_0$ = 9.36e-11 m/s$^2$)", fontsize=12)
ax.set_title("full range", fontsize=12, loc="left")
bx.set_title("zoom on RC100 (z 0.6 to 2.5)", fontsize=12, loc="left")
for L, lab, y_off in (("FLAT", "flat $a_0$", 1.0), ("PROXY", r"$\Lambda$CDM effective-$a_0$ proxy", 1.0), ("H(z)", r"$a_0\propto H(z)$", 1.0), ("M-DEC", r"$a_0\propto\sqrt{\rho_{DE}}$ (DESI CPL)", 1.0)):
    y6 = cur[L][-1]
    ax.annotate(lab, xy=(6.0, y6), xytext=(6, 0), textcoords="offset points", ha="left", va="center", fontsize=10.5, color=COL[L], fontweight="bold")
handles = [Line2D([], [], color=COL["FLAT"], lw=2, label=r"flat $a_0$ (ratio 1)"),
           Line2D([], [], color=COL["PROXY"], lw=2.4, label=r"$\Lambda$CDM effective-$a_0$ PROXY (dotted above z = 5)"),
           Line2D([], [], color=COL["H(z)"], lw=2.4, label=r"$a_0\propto H(z)=E(z)$"),
           Line2D([], [], color=COL["M-DEC"], lw=2.4, label=r"$a_0\propto\sqrt{\rho_{DE}(z)}$, DESI DR2 CPL (dotted above z = 2.5; band = DESY5, Union3)"),
           Line2D([], [], marker="o", color=C_RC, mfc=C_RC, ls="none", ms=8, label="RC100, four z-quartiles, corrected table (authors' fit route)"),
           Line2D([], [], marker="s", color="#888888", mfc="none", ls="none", ms=6, mew=1.2, label="RC100, committed table (same bins)"),
           Line2D([], [], marker="D", color=C_CR, mfc=C_CR, ls="none", ms=8, label=r"CRISTAL $R_e$, fit route (12 discs)"),
           Line2D([], [], marker="s", color=C_CR, mfc=C_CR, ls="none", ms=8, label=r"CRISTAL $R_{out}$, fit route (6)"),
           Line2D([], [], marker="D", color=C_CR, mfc="white", ls="none", ms=8, mew=1.8, label=r"CRISTAL $R_e$, independent route (6 class-A)"),
           Line2D([], [], marker="s", color=C_CR, mfc="white", ls="none", ms=8, mew=1.8, label=r"CRISTAL $R_{out}$, independent route (6)"),
           Patch(facecolor="#777777", alpha=0.25, label=r"shaded bars: baryon mass $\pm0.15$ dex (dark), $\pm0.30$ dex (light); a triangle marks no solution"),
           ]
fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, 0.165), ncol=3, fontsize=9.6, frameon=False, columnspacing=1.6, labelspacing=0.55, handlelength=2.2)
cap = []
for i, c in enumerate(J["caption"]):
    c = (c.replace("LCDM", "ΛCDM").replace("kappa = 1/2", "κ = ½").replace("+-", "±").replace("a0", "a₀").replace("rho_DE", "ρ_DE").replace("sqrt(", "√("))
    cap.append(c)
wrapped = []
for c in cap:
    wrapped += textwrap.wrap(c, 200)
fig.suptitle(r"a$_0$ over cosmic time: the a$_0$ scale implied by author decompositions, against four laws", fontsize=15, x=0.06, ha="left", y=0.985)
fig.text(0.06, 0.008, "\n".join(wrapped).rstrip(), fontsize=9.4, va="bottom", ha="left", family="DejaVu Sans", linespacing=1.45)
fig.subplots_adjust(left=0.06, right=0.985, top=0.925, bottom=0.365)
out = os.path.join(LANE, "cfg223_a0_over_cosmic_time.png")
fig.savefig(out, dpi=150)
print("wrote", out)
