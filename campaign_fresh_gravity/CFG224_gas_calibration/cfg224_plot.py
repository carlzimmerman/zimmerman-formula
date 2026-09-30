#!/usr/bin/env python3
"""CFG224 figure: tracer-to-tracer gas-mass offsets against redshift, and the calibration knowledge K against the K the flat-versus-H(z) test needs.
Reads cfg224_gas_calibration_results.json.  Conversions as each source states them; reconstructions unverified; a tracer agreement is not an absolute mass scale; no law verdict."""
import os, json, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

LANE = os.path.dirname(os.path.abspath(__file__))
J = json.load(open(os.path.join(LANE, "cfg224_gas_calibration_results.json")))
COL = {"CO-DUST": "#1f5fa8", "CI-DUST": "#e07b00", "CO-CI": "#2a9d55", "CO-CII": "#c0392b", "CII-DUST": "#7b2cbf"}
MK = {"Stripe82": ("o", 4), "Bourne+19": ("s", 7), "NOEMA3D": ("D", 8), "singles": ("*", 13)}
fig, (ax, bx) = plt.subplots(1, 2, figsize=(16.5, 7.6), gridspec_kw=dict(width_ratios=[1.35, 1.0], wspace=0.17))
ax.axhspan(-0.15, 0.15, color="#999999", alpha=0.13, zorder=0)
ax.axhspan(-0.10, 0.10, color="#999999", alpha=0.16, zorder=0)
ax.axhspan(-0.05, 0.05, color="#999999", alpha=0.18, zorder=0)
ax.axhline(0, color="#444444", lw=0.8)
rng = np.random.default_rng(1)
for r in J["rows"]:
    if not r["indep"] or r["src"].startswith("NOEMA3D-failing"):
        continue
    m, ms = MK.get(r["src"], ("o", 5))
    x = r["z"] * (1 + (0.02 * rng.standard_normal() if r["src"] == "Stripe82" else 0.0))
    ax.plot([x], [r["d"]], marker=m, ms=ms, ls="none", color=COL[r["pair"]], alpha=0.55 if r["src"] == "Stripe82" else 0.95, mec="white" if r["src"] != "Stripe82" else "none", mew=0.6, zorder=3)
BINS = [("B1 z<0.6", 0.12), ("B2 0.6<=z<1.6", 1.15), ("B3 1.6<=z<3.0", 2.4), ("B4 z>=3.0", 4.2)]
for b, xz in BINS:
    for pr in COL:
        st = J["primary"].get(f"{b}|{pr}")
        if st and st.get("N", 0) >= 3:
            ax.errorbar([xz * (1.25 if pr == "CI-DUST" else 1.0)], [st["mean"]], yerr=[[st["se"]], [st["se"]]], fmt="_", ms=26, mew=2.6, color="k", elinewidth=2.2, capsize=5, zorder=5)
            ax.annotate(f"K = {st['K']:.2f}\n(N = {st['N']}, {pr})", xy=(xz * (1.25 if pr == "CI-DUST" else 1.0), st["mean"]), xytext=(9, 14 if pr == "CI-DUST" else -28), textcoords="offset points", fontsize=8.6, color="k")
ax.set_xscale("log"); ax.set_xlim(0.03, 7); ax.set_ylim(-0.85, 0.75)
ax.set_xticks([0.05, 0.1, 0.2, 0.5, 1, 2, 3, 5]); ax.set_xticklabels(["0.05", "0.1", "0.2", "0.5", "1", "2", "3", "5"])
ax.set_xlabel("redshift z", fontsize=12); ax.set_ylabel(r"tracer offset $d=\log_{10}(M_A/M_B)$ (dex), conversions as each source states them", fontsize=11)
ax.set_title("independent tracer pairs (black = bin mean $\\pm$ SE; K = $\\sqrt{SE^2+(|\\mu|/2)^2}$)", fontsize=11.5, loc="left")
ax.grid(True, which="major", color="#cccccc", lw=0.5, alpha=0.7)
ax.text(0.031, 0.705, "grey bands: $\\pm$0.05, $\\pm$0.10 (CFG223) and $\\pm$0.15 dex (CFG221)", fontsize=9, color="#555555", va="center")
h = [Line2D([], [], marker="o", color=COL["CO-DUST"], ls="none", label="CO - dust"), Line2D([], [], marker="o", color=COL["CI-DUST"], ls="none", label="[CI] - dust"),
     Line2D([], [], marker="o", color=COL["CO-CI"], ls="none", label="CO - [CI]"), Line2D([], [], marker="o", color=COL["CO-CII"], ls="none", label="CO - [CII]"), Line2D([], [], marker="o", color=COL["CII-DUST"], ls="none", label="[CII] - dust"),
     Line2D([], [], marker="o", color="#777777", ls="none", ms=4, label="Stripe82 (78)"), Line2D([], [], marker="s", color="#777777", ls="none", ms=7, label="Bourne+19 (9)"), Line2D([], [], marker="D", color="#777777", ls="none", ms=7, label="NOEMA3D validated (5)"), Line2D([], [], marker="*", color="#777777", ls="none", ms=12, label="singles (3 galaxies)")]
ax.legend(handles=h, loc="lower left", fontsize=8.6, ncol=3, framealpha=0.92)
# right panel: K measured against K needed
bx.axhspan(0.05, 0.10, color="#999999", alpha=0.18); bx.axhline(0.15, color="#555555", ls="--", lw=1.2)
bx.text(0.09, 0.152, "CFG221 requirement (0.15 dex)", ha="left", va="bottom", fontsize=8.6, color="#555555"); bx.text(0.09, 0.052, "CFG223 range (0.05 to 0.10)", ha="left", va="bottom", fontsize=8.6, color="#555555")
for b, xz in BINS:
    hp = J["headline"].get(b)
    if hp:
        st = J["primary"][f"{b}|{hp}"]
        bx.plot([xz], [st["K"]], marker="s", ms=10, color="k", zorder=5); bx.annotate(f"measured K\n({hp}, N = {st['N']})", xy=(xz, st["K"]), xytext=(8, -4), textcoords="offset points", fontsize=8.6)
for (srcn, pr), st in J["sources"].items() if False else []:
    pass
for key, st in J["sources"].items():
    srcn, pr = key.split("|")
    if srcn == "Bourne+19":
        bx.plot([1.05], [st["K"]], marker="o", ms=7, mfc="white", mec="k", zorder=5); bx.annotate("Bourne+19 alone", xy=(1.05, st["K"]), xytext=(-78, 6), textcoords="offset points", fontsize=8.2)
    if srcn == "NOEMA3D" and pr == "CI-DUST":
        bx.plot([1.25], [st["K"]], marker="o", ms=7, mfc="white", mec="k", zorder=5); bx.annotate("NOEMA3D alone", xy=(1.25, st["K"]), xytext=(6, -12), textcoords="offset points", fontsize=8.2)
for p in J["implication"]:
    lo, mid, hi = p["K_needed"]["0.7"], p["K_needed"]["0.5"], p["K_needed"]["0.3"]
    c = "#1d4e89" if p["point"].startswith("RC100") else "#e07b00"
    bx.plot([p["z"]] * 2, [lo, hi], color=c, lw=2.2, alpha=0.6); bx.plot([p["z"]], [mid], marker="^", ms=8, color=c, zorder=4)
bx.plot([], [], marker="^", color="#1d4e89", ls="none", label="K needed, RC100 quartiles (bars: f_gas 0.7 to 0.3)"); bx.plot([], [], marker="^", color="#e07b00", ls="none", label="K needed, CRISTAL points"); bx.plot([], [], marker="s", color="k", ls="none", label="K measured (bin headline)")
bx.legend(loc="upper left", fontsize=8.6, framealpha=0.92)
bx.set_xscale("log"); bx.set_xlim(0.08, 7); bx.set_ylim(0, 0.68)
bx.set_xticks([0.1, 0.2, 0.5, 1, 2, 3, 5]); bx.set_xticklabels(["0.1", "0.2", "0.5", "1", "2", "3", "5"])
bx.set_xlabel("redshift z", fontsize=12); bx.set_ylabel("calibration knowledge K (dex on the gas mass)", fontsize=11)
bx.set_title("K measured against K needed: (half the flat-vs-$H(z)$ separation) / ($|$lever$|\\,f_{gas}$)", fontsize=10.6, loc="left")
bx.grid(True, which="major", color="#cccccc", lw=0.5, alpha=0.7)
fig.suptitle("How well is the gas-mass calibration known? Tracer offsets against redshift (conversions as stated; a tracer agreement is not an absolute mass scale; no law verdict)", fontsize=12.5, x=0.06, ha="left", y=0.99)
fig.text(0.06, 0.012, "z > 1.6: only three galaxies with stated multi-tracer masses (PKS 0529-549, Q1700-MD94, J081740), each with its own conversions, so K is not estimated there.\n"
         "Bins, K and the class thresholds are frozen in FROZEN_CRITERIA.md. Kirkpatrick+19 and H-ATLAS are excluded as not independent. kappa = 1/2 is fitted.", fontsize=8.8, va="bottom", ha="left", linespacing=1.4)
fig.subplots_adjust(left=0.065, right=0.985, top=0.91, bottom=0.14)
out = os.path.join(LANE, "cfg224_tracer_offsets_vs_z.png")
fig.savefig(out, dpi=150)
print("wrote", out)
