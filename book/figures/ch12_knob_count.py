import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

# Parameter count from the chapter's Worked Example: stacking fixes onto the Hubble tension.
# 6 baseline -> +N_eff (7) -> +w0,wa (9) -> +Early Dark Energy (~11).
steps = ["Baseline\nΛCDM", "+ free N_eff", "+ free w(a)\n(w0, wa)", "+ Early\nDark Energy"]
knobs = [6, 7, 9, 11]          # cumulative total
extra = [k-6 for k in knobs]   # knobs added above the original six

fig, ax = plt.subplots(figsize=(7,4.3))
x = np.arange(len(steps))
ax.bar(x, [6]*len(steps), color=C_NEWTON, alpha=0.55, label="original 6 fit parameters")
ax.bar(x, extra, bottom=6, color=C_FW, alpha=0.9, label="knobs added to relieve the tension")

for xi, k in zip(x, knobs):
    ax.annotate(f"{k}", (xi, k+0.15), ha="center", va="bottom", fontsize=11, fontweight="bold")

ax.set_xticks(x); ax.set_xticklabels(steps)
ax.set_ylabel("total adjustable parameters")
ax.set_ylim(0, 13)
ax.set_title("Knob count climbs as fixes are stacked on the Hubble tension")
ax.legend(frameon=False, loc="upper left")
ax.text(0.99,0.02,"counts from the chapter's Worked Example", transform=ax.transAxes,
        ha="right", va="bottom", fontsize=7, color="#888")
fig.tight_layout(); fig.savefig("ch12_knob_count.png", bbox_inches="tight"); print("ok")
