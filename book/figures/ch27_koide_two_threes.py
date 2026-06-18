import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"
fig, ax = plt.subplots(figsize=(7,4.3))

# Koide Q computed from measured charged-lepton masses (MeV), as a CHECK of the chapter's 2/3.
me, mmu, mtau = 0.51099895, 105.6583755, 1776.86   # MeV (measured constants)
Q = (me+mmu+mtau)/((np.sqrt(me)+np.sqrt(mmu)+np.sqrt(mtau))**2)

# Two distinct '3's the chapter warns are NOT linked.
labels = ["Koide   $Q=\\dfrac{m_e+m_\\mu+m_\\tau}{(\\sqrt{m_e}+\\sqrt{m_\\mu}+\\sqrt{m_\\tau})^2}$",
          "gravity kernel   $\\sqrt{8\\pi/3}$"]
vals = [Q, np.sqrt(8*np.pi/3)]
colors = [C_DATA, C_FW]
xpos = [0,1]
bars = ax.bar(xpos, vals, width=0.5, color=colors, alpha=0.85, edgecolor="white")

for x,v in zip(xpos,vals):
    ax.text(x, v+0.07, f"{v:.4f}", ha="center", fontsize=10, fontweight="bold",
            color=colors[x])

# annotate where the '3' lives in each
ax.text(0, 0.18, "the 3 = # of leptons\n(particle physics)", ha="center",
        fontsize=8.3, color="white", fontweight="bold")
ax.text(1, 0.18, "the 3 = Friedmann's 3\n(cosmic geometry)", ha="center",
        fontsize=8.3, color="white", fontweight="bold")

# guide line at 2/3 for Koide
ax.axhline(2/3, color=C_NEWTON, ls="--", lw=1.1)
ax.text(-0.42, 2/3+0.03, "$2/3$", fontsize=9, color=C_NEWTON)

ax.set_xticks(xpos)
ax.set_xticklabels(labels, fontsize=8.6)
ax.set_ylabel("value of the expression")
ax.set_ylim(0, 3.4)
ax.set_title("Two unrelated 3's: a coincidence the quarantine forbids us to bridge")

ax.text(0.5, 3.05, "different magnitudes, different origins — 'both contain a 3' is NOT evidence",
        ha="center", fontsize=8.4, color="#475569",
        bbox=dict(boxstyle="round,pad=0.35", fc="#f8fafc", ec="#cbd5e1"))
ax.text(0.99,0.02,"Q computed from measured lepton masses; kernel from framework geometry",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=7.0, color="#999999")
fig.tight_layout(); fig.savefig("ch27_koide_two_threes.png", bbox_inches="tight"); print("ok")
