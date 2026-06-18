import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

# Figure 6.3 -- Three angles on the same suspect (SCHEMATIC).
# Conceptual diagram of the chapter's organizing idea: one dark-matter interaction vertex
# (chi chi <-> SM SM) read three ways -- collider (make it), indirect (watch it annihilate),
# direct (feel it hit). No data plotted; purely illustrative.

fig, ax = plt.subplots(figsize=(7.4,4.8))
ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis("off"); ax.grid(False)

cx, cy = 5, 5
ax.add_patch(Circle((cx,cy), 0.55, color=C_FW, alpha=0.18, ec=C_FW, lw=1.6))
ax.text(cx, cy, r"$\chi\,\chi \leftrightarrow$ SM SM", ha="center", va="center",
        fontsize=10, color=C_FW, fontweight="bold")
ax.text(cx, cy-0.95, "one interaction vertex", ha="center", va="center", fontsize=8, color="#64748b", style="italic")

boxes = [
    (1.7, 8.3, "1. MAKE IT", "Collider (LHC)", "missing transverse momentum", C_DATA),
    (8.3, 8.3, "2. WATCH IT ANNIHILATE", "Indirect (Fermi, AMS)", "gamma-ray / positron glow", C_MOND),
    (5.0, 1.4, "3. FEEL IT HIT", "Direct (LZ, XENONnT, PandaX-4T)", "nuclear recoil, a mile underground", C_FW),
]
for (x,y,title,sub,note,col) in boxes:
    w,h = 3.1, 1.45
    bb = FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle="round,pad=0.04,rounding_size=0.12",
                        linewidth=1.8, edgecolor=col, facecolor=col, alpha=0.10)
    ax.add_patch(bb)
    ax.text(x, y+0.36, title, ha="center", va="center", fontsize=9.5, fontweight="bold", color=col)
    ax.text(x, y+0.02, sub, ha="center", va="center", fontsize=8, color="#334155")
    ax.text(x, y-0.34, note, ha="center", va="center", fontsize=7.3, color="#64748b", style="italic")

arrow_targets = [(1.7,7.6,"read backward"), (8.3,7.6,"read forward"), (5.0,2.15,"read sideways")]
for (tx,ty,lab) in arrow_targets:
    arr = FancyArrowPatch((cx,cy),(tx,ty), arrowstyle="-|>", mutation_scale=14,
                          lw=1.6, color="#94a3b8", shrinkA=22, shrinkB=30)
    ax.add_patch(arr)
    mxp, myp = (cx+tx)/2, (cy+ty)/2
    ax.text(mxp+0.15, myp, lab, fontsize=7.2, color="#94a3b8", ha="left", va="center")

ax.text(5,9.6,"Three angles on the same suspect", ha="center", fontsize=12.5, fontweight="bold", color="#1e293b")
ax.text(5,9.05,"the same dark-matter coupling, read three ways -- all returned a careful nothing",
        ha="center", fontsize=8.5, color="#64748b", style="italic")
ax.text(0.05,0.02,"schematic / conceptual diagram",transform=ax.transAxes,
        ha="left",va="bottom",fontsize=7,color="#cbd5e1")

fig.tight_layout(); fig.savefig("ch06_three_strategies.png", bbox_inches="tight"); print("ok")
