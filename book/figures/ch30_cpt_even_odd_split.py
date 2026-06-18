import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"  # framework / Newton / MOND / data-or-obs

# Schematic: the SME splits Lorentz violation into two families. The framework's
# thermal-geometric mechanism sources ONLY the CPT-even family; it predicts the
# CPT-odd photon coefficient k_AF = 0 exactly. Conceptual diagram, no data.

fig, ax = plt.subplots(figsize=(7.2,4.6))
ax.set_xlim(0,10); ax.set_ylim(0,7); ax.axis("off")

def box(x, y, w, h, text, fc, ec, tc, fs=10):
    ax.add_patch(FancyBboxPatch((x-w/2, y-h/2), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.12", linewidth=1.6,
        facecolor=fc, edgecolor=ec))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=tc, zorder=5)

# Top: the source.
box(5, 6.2, 4.6, 0.95,
    "preferred frame\n(de Sitter-Unruh: thermal + geometric)",
    "#ede9fe", C_FW, "#4c1d95", fs=10)

# Two families.
box(2.7, 3.9, 3.2, 1.5,
    "CPT-EVEN family\neven # of indices\nmatter = antimatter",
    "#ede9fe", C_FW, "#4c1d95", fs=9.5)
box(7.3, 3.9, 3.2, 1.5,
    "CPT-ODD family\nodd # of indices\nmatter $\\neq$ antimatter",
    "#f1f5f9", C_NEWTON, "#334155", fs=9.5)

# Outcomes.
box(2.7, 1.5, 3.2, 1.35,
    r"$s_{\mu\nu}\approx 4.8\times10^{-12}$" + "\nINDUCED (live, near edge)",
    "#ede9fe", C_FW, "#4c1d95", fs=9.5)
box(7.3, 1.5, 3.2, 1.35,
    r"$k_{AF} = 0$  exactly" + "\nNONE sourced (clean zero)",
    "#fef2f2", C_DATA, "#991b1b", fs=9.5)

def arrow(x1,y1,x2,y2,color,style="-|>",lw=1.8):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle=style,
        mutation_scale=14, lw=lw, color=color, shrinkA=2, shrinkB=2))

# Source -> the CPT-even branch is sourced (solid purple); the CPT-odd branch is NOT (grey, crossed).
arrow(4.2, 5.72, 2.9, 4.68, C_FW)
arrow(5.8, 5.72, 7.1, 4.68, C_NEWTON, lw=1.4)
# A small "blocked" mark on the odd branch.
ax.text(6.62, 5.18, "x", fontsize=15, color=C_DATA, ha="center", va="center", fontweight="bold")
ax.text(6.95, 5.05, "no odd\nstructure\navailable", fontsize=7.5, color=C_DATA, ha="left", va="center")

arrow(2.7, 3.13, 2.7, 2.20, C_FW)
arrow(7.3, 3.13, 7.3, 2.20, C_DATA, lw=1.4)

# Footnote about scale.
ax.text(7.3, 0.45, r"tested at $\hbar H_0\!\sim\!10^{-33}$ eV (cosmic birefringence)",
        ha="center", va="center", fontsize=8, color="#991b1b")
ax.text(2.7, 0.45, "tested by LLR, ephemerides, gravimeters",
        ha="center", va="center", fontsize=8, color="#4c1d95")

ax.set_title("Two SME families: the framework fills one, zeroes the other", fontsize=12)
fig.tight_layout(); fig.savefig("ch30_cpt_even_odd_split.png", bbox_inches="tight"); print("ok")
