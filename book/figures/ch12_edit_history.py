import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

# Schematic edit-history timeline. Dates approximate, taken from the chapter's edit log.
fig, ax = plt.subplots(figsize=(7.2,4.5))

events = [
    (1931, "Λ switched OFF\n(Hubble expansion)", 1),
    (1975, "Dark matter added\n(rotation curves, clusters)", -1),
    (1981, "Inflation added\n(flatness, horizon)", 1),
    (1998, "Λ switched back ON\n(supernovae: 68%)", -1),
    (2005, "Small-scale patches\n(baryonic feedback)", 1),
    (2019, "Hubble & S₈ tensions\n(extra knobs proposed)", -1),
    (2024, "DESI: evolving w?\n(13th edit?)", 1),
]

t0, t1 = 1925, 2032
ax.plot([t0,t1],[0,0], color="#333", lw=2, zorder=1)

for yr, label, side in events:
    ax.plot([yr],[0], 'o', color=C_FW, ms=9, zorder=3)
    yt = 0.62*side
    ax.plot([yr,yr],[0, yt*0.72], color=C_NEWTON, lw=1, ls=":", zorder=2)
    va = "bottom" if side>0 else "top"
    ax.text(yr, yt, label, ha="center", va=va, fontsize=8.5,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=C_FW, alpha=0.95))

ax.set_xticks(range(1930,2031,20))
ax.set_yticks([])
ax.set_ylim(-1.2,1.2)
ax.set_xlim(t0,t1)
ax.spines['left'].set_visible(False)
ax.grid(axis='y', alpha=0)
ax.set_xlabel("year")
ax.set_title("The edit history: central features installed after the data, not before")
ax.text(0.5,-0.16,"each dot = a revision read off a measurement, not predicted in advance",
        transform=ax.transAxes, ha="center", va="center", fontsize=8.5, color="#666", style="italic")
fig.tight_layout(); fig.savefig("ch12_edit_history.png", bbox_inches="tight"); print("ok")
