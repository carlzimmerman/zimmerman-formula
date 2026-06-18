import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

fig, ax = plt.subplots(figsize=(7,4.3))

# Two columns: LCDM (gravity+dark sector) vs this framework, counting the
# free inputs each needs to describe galaxies + the dark sector.
# LCDM: 6 cosmological parameters + 1 undetected dark-matter particle.
# Framework: 1 irreducible geometric posit (kappa=1/2). a0's FORM and the
# sqrt(8pi/3) kernel are forced; only kappa is the free knob.
labels = ["$\\Lambda$CDM\n(standard model)", "This framework\n(gravity + dark sector)"]
x = [0, 1]

lcdm_params = 6          # six adjustable cosmological parameters
lcdm_particle = 1        # one hypothesized, undetected DM particle (drawn separately)
fw_knob = 1              # one irreducible geometric posit kappa=1/2

# LCDM bar: 6 params
ax.bar(0, lcdm_params, width=0.55, color=C_NEWTON, alpha=0.85,
       label="adjustable cosmological parameters", zorder=3)
# LCDM particle stacked on top, hatched red to flag "undetected"
ax.bar(0, lcdm_particle, width=0.55, bottom=lcdm_params, color="white",
       edgecolor=C_DATA, hatch="///", linewidth=1.4,
       label="hypothesized particle (undetected)", zorder=3)

# Framework bar: 1 geometric knob
ax.bar(1, fw_knob, width=0.55, color=C_FW, alpha=0.9,
       label="irreducible geometric knob ($\\kappa=\\frac{1}{2}$)", zorder=3)

# annotations
ax.text(0, lcdm_params/2, "6\nnumbers", ha="center", va="center",
        color="white", fontsize=11, fontweight="bold", zorder=5)
ax.text(0, lcdm_params+lcdm_particle/2, "+ particle", ha="center", va="center",
        color=C_DATA, fontsize=9.5, fontweight="bold", zorder=5)
ax.text(1, fw_knob+0.18, "1 knob", ha="center", va="bottom",
        color=C_FW, fontsize=12, fontweight="bold", zorder=5)
ax.annotate("$a_0\\sim c^2\\sqrt{\\Lambda}$ form  +  $\\sqrt{8\\pi/3}$ kernel\nare FORCED, not counted",
            xy=(1, 1), xytext=(1.0, 3.4), ha="center", fontsize=8.6, color=C_FW,
            arrowprops=dict(arrowstyle="->", color=C_FW, lw=1.1))

ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=10.5)
ax.set_ylabel("free inputs the theory cannot derive")
ax.set_ylim(0, 8)
ax.set_xlim(-0.6, 1.7)
ax.set_title("The economy claim, counted exactly: one knob vs six-plus-a-particle")
ax.legend(frameon=False, fontsize=8.4, loc="upper right")
ax.text(0.02,0.50,"framework counts as 1-parameter,\nNOT 0-parameter\n($a_0$ value not derived $-$ it\nfollows from $\\Lambda$ plus $\\kappa$)",
        transform=ax.transAxes, ha="left", va="center", fontsize=7.6, color="#888")
fig.tight_layout(); fig.savefig("ch31_economy_ledger.png", bbox_inches="tight"); print("ok")
