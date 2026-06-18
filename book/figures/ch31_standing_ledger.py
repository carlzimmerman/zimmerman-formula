import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

# Schematic scorecard of the chapter's front-by-front standing ledger.
# Each front is placed on an honest 1-D axis from "weakness" to "distinctive
# strength", colored by category. NOT a measurement -- a faithful visual of the
# chapter's own verdicts (the words are the author's).
fronts = [
    ("Solar System (Cassini)",        4, "strength"),   # distinctive strength
    ("Rotation curves / RAR",         3, "shared"),      # viable, shared, non-diagnostic
    ("Baryonic Tully-Fisher",         3, "shared"),      # viable today, distinctive only in future
    ("a0(z) high-z BTFR sign",        3, "future"),      # falsifiable, future, DESI-hostage
    ("CMB / large-scale structure",   2, "undev"),       # underdeveloped
    ("Galaxy clusters",               2, "deficit"),     # soft, MOND-shared deficit
    ("Covariant lensing",             1, "wall"),         # hard wall
    ("Standard Model content",        1, "wall"),         # quarantined wall
]
fronts = fronts[::-1]  # plot top-to-bottom in listed order

catcolor = {
    "strength": C_MOND,
    "shared":   C_FW,
    "future":   "#a78bdf",
    "undev":    C_NEWTON,
    "deficit":  "#e0a030",
    "wall":     C_DATA,
}
catlabel = {
    "strength":"distinctive strength",
    "shared":  "viable but shared / non-diagnostic",
    "future":  "distinctive only in the future",
    "undev":   "underdeveloped (not a kill, not a win)",
    "deficit": "soft, MOND-shared deficit",
    "wall":    "hard wall / quarantine",
}

fig, ax = plt.subplots(figsize=(7.4,4.6))
ys = np.arange(len(fronts))
for y,(name,score,cat) in zip(ys, fronts):
    ax.barh(y, score, height=0.6, color=catcolor[cat], alpha=0.9, zorder=3)
    ax.text(score+0.07, y, name, va="center", ha="left", fontsize=9.2)

ax.set_yticks([])
ax.set_xlim(0, 5)
ax.set_ylim(-0.7, len(fronts)-0.3)
ax.set_xticks([1,2,3,4])
ax.set_xticklabels(["hard\nwall","soft /\nundeveloped","jointly\nviable","distinctive\nstrength"],
                   fontsize=8.6)
ax.set_xlabel("the framework's honest standing on this front")
ax.set_title("Standing, front by front: viable on most, strong on one, walled on two")

# the load-bearing caveat
ax.text(0.5, -0.62, "no referee-proof kill of $\\Lambda$CDM on ANY front",
        ha="left", va="center", fontsize=8.4, color="#666", style="italic")

legend_cats = ["strength","shared","future","undev","deficit","wall"]
handles = [Patch(facecolor=catcolor[c], label=catlabel[c]) for c in legend_cats]
ax.legend(handles=handles, frameon=False, fontsize=7.6, loc="lower right",
          ncol=1, handlelength=1.1)
fig.tight_layout(); fig.savefig("ch31_standing_ledger.png", bbox_inches="tight"); print("ok")
