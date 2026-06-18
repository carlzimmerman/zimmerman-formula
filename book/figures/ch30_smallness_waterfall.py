import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"  # framework / Newton / MOND / data-or-obs

# Worked Example (Chapter 30): why s_lab ~ 5e-12 is INHERITED, not invented.
# Every value below is the framework's own / basic cosmology -- nothing from particle physics.
c    = 2.998e8        # m/s
H0   = 2.20e-18       # 1/s  (~70 km/s/Mpc)
a0   = 1.2e-10        # m/s^2 (framework value used in the chapter)
Z    = np.sqrt(32*np.pi/3)   # = 5.789, the framework kernel
beta = 1.23e-3        # Earth's boost relative to the CMB rest frame

cH0   = c*H0                  # ~6.6e-10 cosmic acceleration scale
ratio = a0/cH0                # ~0.18  ==  1/Z up to factors
s_lab = 4.8e-12               # the chapter's quoted laboratory-frame coefficient

# Stages: bare ratio (order one) -> suppression carrying it down to ~5e-12.
labels = [r"$a_0/cH_0$" + "\n(bare ratio)",
          r"$\approx 1/Z$" + "\n(framework kernel)",
          "+ metric &\nprojection\nsuppression",
          r"$s_{\rm lab}$" + "\n(inherited)"]
vals   = [ratio, 1/Z, None, s_lab]

fig, ax = plt.subplots(figsize=(7,4.3))

xs = np.arange(4)
# Plot the two order-one stages and the final tiny coefficient on a log scale.
plotted = [ratio, 1/Z, s_lab]
plotx   = [0, 1, 3]
colors  = [C_MOND, C_MOND, C_FW]
ax.scatter(plotx, plotted, s=130, color=colors, zorder=5)
for x, v in zip(plotx, plotted):
    ax.text(x, v*1.6, f"{v:.2g}".replace("e-0","e-").replace("e-","×10$^{-")+"}$" if v<1e-3 else f"{v:.2g}",
            ha="center", va="bottom", fontsize=9.5,
            color=(C_FW if v<1e-3 else "#0e7490"))

# A descending dashed connector to show the smallness entering in the middle.
ax.plot([1,3],[1/Z, s_lab], color=C_NEWTON, ls="--", lw=1.6, zorder=3)
ax.plot([0,1],[ratio, 1/Z], color=C_MOND, ls="-", lw=1.6, zorder=3)

# Mark the suppression factor in the gap.
supp = s_lab/(1/Z)
ax.annotate(f"x {supp:.1e}\nsuppression".replace("e-0","e-"),
            xy=(2, np.sqrt((1/Z)*s_lab)), ha="center", va="center",
            fontsize=9.5, color=C_NEWTON,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=C_NEWTON, alpha=0.9))

ax.set_yscale("log")
ax.set_ylim(1e-12, 3)
ax.set_xlim(-0.5, 3.6)
ax.set_xticks(xs); ax.set_xticklabels(labels, fontsize=9)
ax.set_ylabel("dimensionless magnitude")
ax.set_title("Where the smallness comes from: $s_{\\rm lab}$ is inherited from $a_0$")

ax.text(0.99, 0.97, "inputs: $a_0$, $c$, $H_0$, $Z$, $\\beta$ only\nnothing from the Standard Model",
        transform=ax.transAxes, fontsize=8.5, color=C_NEWTON, ha="right", va="top",
        bbox=dict(boxstyle="round,pad=0.35", fc="#f8fafc", ec=C_NEWTON, alpha=0.8))

fig.tight_layout(); fig.savefig("ch30_smallness_waterfall.png", bbox_inches="tight"); print("ok")
