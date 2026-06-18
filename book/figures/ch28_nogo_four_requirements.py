import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":False,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

fig, ax = plt.subplots(figsize=(7.2,5.0))
ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis("off")

# four requirements as boxes around the top
reqs = [
    (1.7, 8.6, "(a) General\ncovariance"),
    (5.0, 8.6, "(b) GW speed\n$c_T=c$  (GW170817)"),
    (8.3, 8.6, "(c) Ghost-\nfreedom"),
    (5.0, 6.9, "(d) Cassini\nsafety"),
]
for (x,y,t) in reqs:
    box = FancyBboxPatch((x-1.15,y-0.55), 2.3, 1.1, boxstyle="round,pad=0.06,rounding_size=0.12",
                         fc="#ede9fe", ec=C_FW, lw=1.6)
    ax.add_patch(box)
    ax.text(x, y, t, ha="center", va="center", fontsize=9.5, color="#3b0764")

ax.text(5.0, 5.55, "want all FOUR at once\nfor a MOND-magnitude slip", ha="center", va="center",
        fontsize=10, style="italic", color=C_DATA)

# central RESULT box
result = FancyBboxPatch((3.2,3.55), 3.6, 1.25, boxstyle="round,pad=0.08,rounding_size=0.12",
                        fc="#fee2e2", ec=C_DATA, lw=2.0)
ax.add_patch(result)
ax.text(5.0, 4.18, "NO-GO\nall four are incompatible", ha="center", va="center",
        fontsize=11, fontweight="bold", color="#7f1d1d")

# arrows from the four reqs converging to result
for (x,y,_) in reqs:
    ar = FancyArrowPatch((x, y-0.6), (5.0, 4.85), arrowstyle="-", color=C_NEWTON,
                         lw=1.1, alpha=0.55, connectionstyle="arc3,rad=0.05")
    ax.add_patch(ar)

# the four covariant escape routes that were TRIED -> all close
routes = [
    "DHOST scalar-tensor",
    "aether shear-stress",
    "Horava / non-projectable",
    "khronometric multiplier",
]
rx0 = 0.9
for i, r in enumerate(routes):
    yy = 2.7 - i*0.62
    ax.text(rx0, yy, "x", ha="center", va="center", fontsize=13, fontweight="bold", color=C_DATA)
    ax.text(rx0+0.45, yy, r, ha="left", va="center", fontsize=9, color="#334155")
ax.text(rx0+0.0, 3.25, "covariant escapes tried:", ha="left", va="center",
        fontsize=9.5, fontweight="bold", color="#334155")

# the only surviving door
door = FancyBboxPatch((6.55,0.55), 3.0, 2.05, boxstyle="round,pad=0.08,rounding_size=0.12",
                      fc="#cffafe", ec=C_MOND, lw=1.8)
ax.add_patch(door)
ax.text(8.05, 2.15, "the only surviving door:", ha="center", va="center",
        fontsize=9.5, fontweight="bold", color="#155e75")
ax.text(8.05, 1.45, "PREFERRED-FRAME\n(Lorentz-violating)\nlensing sector", ha="center", va="center",
        fontsize=10, color="#155e75")
ax.text(8.05, 0.78, "-> slip is FITTED, not derived", ha="center", va="center",
        fontsize=8.5, style="italic", color="#155e75")

ar2 = FancyArrowPatch((6.8,4.0), (8.05,2.65), arrowstyle="-|>", color=C_MOND, lw=1.8,
                      mutation_scale=16, connectionstyle="arc3,rad=-0.2")
ax.add_patch(ar2)
ax.text(7.9, 3.55, "give up (a)\n(covariance)", ha="center", va="center", fontsize=8, color=C_MOND)

ax.set_title("The lensing wall as a theorem: pick any three of four", fontsize=12)
ax.text(0.0, -0.1, "schematic", ha="left", va="bottom", fontsize=7, color="#999999", transform=ax.transAxes)
fig.tight_layout(); fig.savefig("ch28_nogo_four_requirements.png", bbox_inches="tight"); print("ok")
