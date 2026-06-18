import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"  # framework / Newton / MOND / data-or-obs

# Figure 22.1 (schematic) -- four independent routes converge on the FORCED form a0 ~ c^2 sqrt(Lambda).
fig, ax = plt.subplots(figsize=(7.4,4.6))
ax.set_axis_off()

tx, ty = 0.5, 0.5
ax.add_patch(plt.Circle((tx,ty),0.085, color=C_FW, ec="white", lw=2, zorder=5, transform=ax.transAxes))
ax.text(tx,ty, r"$a_0 \sim c^2\sqrt{\Lambda}$", ha="center", va="center",
        color="white", fontsize=12, fontweight="bold", zorder=6, transform=ax.transAxes)
ax.text(tx, ty-0.135, "the FORCED form", ha="center", va="center",
        color=C_FW, fontsize=9, style="italic", transform=ax.transAxes)

routes = [
    (0.13, 0.86, "Route 1\nde Sitter-Unruh\ntemperature floor", "heat"),
    (0.87, 0.86, "Route 2\ndimensional analysis\n($c$, $\\Lambda$ only)", "units"),
    (0.13, 0.16, "Route 3\nCKN / holographic\nsingle-d.o.f. bound", "entropy"),
    (0.87, 0.16, "Route 4\n$SO(4,1)$ gauge gravity\n(machine-certified)", "symmetry"),
]
for x,y,label,room in routes:
    ax.annotate("", xy=(tx,ty), xytext=(x,y),
                arrowprops=dict(arrowstyle="-|>", color=C_NEWTON, lw=2,
                                shrinkA=22, shrinkB=26, alpha=0.8),
                transform=ax.transAxes)
    ax.text(x,y,label, ha="center", va="center", fontsize=8.5,
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=C_NEWTON, lw=1.3),
            transform=ax.transAxes)
    ax.text(x, y-(0.105 if y>0.5 else -0.105), f"[{room}]", ha="center", va="center",
            fontsize=8, color=C_MOND, style="italic", transform=ax.transAxes)

ax.text(0.5, 0.99, "Over-determination: four independent rooms of physics,\none forced shape",
        ha="center", va="top", fontsize=11, fontweight="bold", transform=ax.transAxes)
ax.text(0.99,0.01,"schematic -- Ch. 22", ha="right", va="bottom",
        fontsize=7, color=C_NEWTON, alpha=0.6, transform=ax.transAxes)
fig.tight_layout(); fig.savefig("ch22_four_routes_one_form.png", bbox_inches="tight"); print("ok")
