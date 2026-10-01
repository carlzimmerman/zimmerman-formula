#!/usr/bin/env python3
"""CFG258: the chart (plot only; reads cfg258_preflight_results.json): the slope estimators E1 (anchored) and E2 (within-sample) in the primary cell C0, per law (FLAT, RIVAL, ANCH) and budget level (none, A, B): the mean and the 5th-95th percentile range over mocks, per unit z, with the three
laws' slopes (0, the rival's noiseless slope, the anchored b3).  Run: python3 campaign_fresh_gravity/CFG258_mightee_a0z_preflight/cfg258_plot.py"""
import os, json, sys
sys.dont_write_bytecode = True
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "cfg258_preflight_results.json")))
S = R["stats"]["C0"]
b3 = R["part_a"]["canonical"]["0.09"]["f_iii"] - 1
b3 = (R["part_a"]["canonical"]["0.09"]["f_iii"] - 1) / 0.09
col = {"FLAT": "#1f77b4", "RIVAL": "#2ca02c", "ANCH": "#d62728"}
fig, axs = plt.subplots(1, 2, figsize=(12.5, 4.8), sharey=True)
for ax, (key, title) in zip(axs, (("b1", "E1: anchored slope (cannot attribute)"), ("b2", "E2: within-sample slope (decisive)"))):
    y = 0
    ticks, labels = [], []
    for law in ("FLAT", "RIVAL", "ANCH"):
        for lv, nm in ((None, "no systematics"), ("A", "level A"), ("B", "level B")):
            s = S[f"{law}_{lv or 'off'}"][key]
            ax.plot([s["p5"], s["p95"]], [y, y], color=col[law], lw=3, alpha=0.55 if lv else 0.9, solid_capstyle="butt")
            ax.plot([s["mean"]], [y], "o", color=col[law], ms=6)
            ticks.append(y); labels.append(f"{law} {nm}")
            y += 1
        y += 0.6
    ax.axvline(0, color="#1f77b4", ls=":", lw=1)
    ax.axvline(b3, color="#d62728", ls="--", lw=1.2)
    ax.set_yticks(ticks); ax.set_yticklabels(labels, fontsize=8)
    ax.invert_yaxis(); ax.set_title(title, fontsize=10); ax.set_xlabel("fitted slope b in a0(z) = a0 (1 + b z), per unit z  (dot: mean; bar: 5th-95th percentile over mocks)", fontsize=8)
    ax.grid(alpha=0.25)
axs[1].text(b3 + 0.3, 6.45, "anchored claim b3 = 5.59", color="#d62728", fontsize=8, va="center")
fig.suptitle("CFG258 (canonical footing, cell C0: 130 SPARC-resampled MIGHTEE-like galaxies, z 0.02-0.09). The flat law's level-B range contains the anchored claim's slope", fontsize=9.5)
fig.tight_layout(rect=(0, 0, 1, 0.94))
fig.savefig(os.path.join(HERE, "cfg258_preflight.png"), dpi=150)
print("wrote cfg258_preflight.png")
