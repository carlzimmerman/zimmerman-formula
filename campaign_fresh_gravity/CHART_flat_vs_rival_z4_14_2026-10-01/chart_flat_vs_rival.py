#!/usr/bin/env python3
"""Plot only (no new analysis): where each z >= 4 galaxy of CFG269 sits between the FLAT law and the rival a0 ~ H(z).
Reads the committed campaign_fresh_gravity/CFG269_highest_z_dynamics/cfg269_rows.csv.
Position t = (log D_obs - log D_FLAT) / (log D_RIVAL - log D_FLAT): t = 0 on the flat law, t = 1 on the rival.
Error bar = the row's symmetric sigma (mean of sigma_FLAT and sigma_RIVAL, dex) divided by the gap G (dex), as in CFG269's P = G / sigma.
Top: COMPLETE rows (stars + gas; these decide each bin).  Bottom: LOWER-LIMIT rows (stars only; gas-limited, not a discrimination).
Run: python3 campaign_fresh_gravity/CHART_flat_vs_rival_z4_14_2026-10-01/chart_flat_vs_rival.py
"""
import csv, math, os, sys
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
rows = list(csv.DictReader(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG269_highest_z_dynamics", "cfg269_rows.csv"))))
CHK = [len(rows) == 100, sum(r["class"] == "COMPLETE" for r in rows) == 23]
def pos(r):
    dF, dR, dO = float(r["D_pred_FLAT"]), float(r["D_pred_RIVAL"]), float(r["D_obs"])
    G = math.log10(dR) - math.log10(dF)
    t = (math.log10(dO) - math.log10(dF)) / G
    s = 0.5 * (float(r["sigma_FLAT"]) + float(r["sigma_RIVAL"])) / G
    return t, s, G
fig, ax = plt.subplots(2, 1, figsize=(13, 10), sharex=True)
fig.suptitle("Does an early galaxy look like the flat law or like a₀ growing with H(z)?  Not separable with today's data",
             fontsize=13, fontweight="bold")
LIM = (-3.0, 4.0)
for k, (cls, title) in enumerate((("COMPLETE", "stars + gas measured (these decide each redshift bin)"),
                                   ("LOWER-LIMIT", "stars only (gas missing: both laws need more baryons, so not a discrimination)"))):
    a = ax[k]
    a.axhspan(-0.15, 0.15, color="black", alpha=0.10); a.axhline(0, color="black", lw=2)
    a.axhspan(0.85, 1.15, color="C3", alpha=0.10); a.axhline(1, color="C3", lw=2)
    a.text(15.15, 0, "flat a₀\n(the framework)", va="center", fontsize=9)
    a.text(15.15, 1, "a₀ ∝ H(z)\n(the rival)", va="center", fontsize=9, color="C3")
    sel = [r for r in rows if r["class"] == cls]
    for r in sel:
        t, s, G = pos(r); z = float(r["z"])
        flagged = "FLAG" in r["labels"] or "flag" in r["labels"]
        floor = r["floor"] == "True"
        col = "C0" if cls == "COMPLETE" else "0.55"
        mk = "v" if floor else ("s" if flagged else "o")
        tc = min(max(t, LIM[0] + 0.1), LIM[1] - 0.1)
        a.errorbar(z, tc, yerr=s, fmt=mk, color=col, ms=7 if cls == "COMPLETE" else 5, capsize=3,
                   lw=1.2 if cls == "COMPLETE" else 0.8, alpha=0.9 if cls == "COMPLETE" else 0.6, mfc="white" if flagged else col)
        if t != tc:
            a.annotate("", (z, tc + (0.35 if t > tc else -0.35)), (z, tc), arrowprops=dict(arrowstyle="->", color=col))
        if cls == "COMPLETE" and ("z14" in r["object"] or "Y1" in r["object"] or "REBELS" in r["object"]):
            a.annotate(r["object"].split(" [")[0], (z, tc), xytext=(6, 8), textcoords="offset points", fontsize=8)
    a.set_ylim(*LIM); a.set_ylabel("position between the laws\n(0 = flat, 1 = rival)")
    a.set_title(title, fontsize=10, loc="left")
    for edge in (6, 8): a.axvline(edge, color="0.8", ls=":")
ax[0].text(4.1, 3.4, "z 4–6: 14 objects, closer to flat but MARGINAL (P 1.45–1.94 at ±0.15 dex; NOT POSSIBLE at ±0.30)", fontsize=9)
ax[0].text(4.1, 2.9, "z 6–8: REBELS-25 only, NOT POSSIBLE      z 8–14: GS-z14-0 (with DLA gas) + MACS0416_Y1, MARGINAL", fontsize=9)
ax[0].text(4.1, -2.75, "▽ floor (stars+gas exceed the pull; the calibration band restores the rival)   □ flagged by another paper (AGN, merger, outflow or non-circular motions)", fontsize=8, color="0.3")
ax[1].set_xlabel("redshift z   (the rival's a₀ is ×6 at z 4, ×9 at z 6, ×20 at z 10, ×32 at z 14)")
ax[1].set_xlim(3.8, 15.0)
fig.text(0.01, 0.004, "Plot only, from CFG269 (cfg269_rows.csv). A discrimination between two a₀(z) laws under a declared dynamical estimator and baryon calibration, not a measurement of a₀.\n"
         "κ = ½ fitted. ΛCDM's effective-a₀ proxy lies within 10% of the rival at z ≥ 10. Error bars: σ/G as in CFG269's P. Points beyond the frame are drawn at the edge with an arrow.", fontsize=7.5, color="0.35")
plt.tight_layout(rect=(0, 0.035, 0.93, 0.95))
out = os.path.join(HERE, "chart_flat_vs_rival_z4_14.png"); plt.savefig(out, dpi=130)
print(f"checks {sum(CHK)}/{len(CHK)} -> {out}"); sys.exit(0 if all(CHK) else 1)
