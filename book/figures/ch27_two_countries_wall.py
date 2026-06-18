import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"
fig, ax = plt.subplots(figsize=(7.4,4.6))
ax.set_axis_off()
ax.set_xlim(0,10); ax.set_ylim(0,10)

# ---- left country: what the framework SPEAKS TO (gravity side) ----
left = plt.Rectangle((0.3,0.7),4.1,8.6, fc="#f5f0ff", ec=C_FW, lw=2.0, zorder=1)
ax.add_patch(left)
ax.text(2.35,9.0,"FRAMEWORK SPEAKS", ha="center", fontsize=11, color=C_FW, fontweight="bold")
ax.text(2.35,8.55,"gravity · inertia · dark sector", ha="center", fontsize=8.6, color=C_FW, style="italic")
speaks = ["a₀ FORM forced: $\\propto c^2\\sqrt{\\Lambda}$",
          "kernel $\\sqrt{8\\pi/3}$ forced",
          "dS–Unruh inertia mechanism",
          "a₀(z) tracks dark energy",
          "one posit $\\kappa=\\frac{1}{2}$ (geometry)"]
for i,t in enumerate(speaks):
    y=7.7-i*1.18
    ax.text(0.62, y, "✓", fontsize=12, color=C_FW)
    ax.text(1.05, y, t, fontsize=8.7, color="#3b1d6e", va="center")

# ---- the WALL ----
wall = plt.Rectangle((4.55,0.7),0.9,8.6, fc="#e2e8f0", ec=C_NEWTON, lw=1.4, hatch="////", zorder=2)
ax.add_patch(wall)
ax.text(5.0,5.0,"S T A N D A R D   M O D E L   W A L L", ha="center", va="center",
        rotation=90, fontsize=9.5, color=C_NEWTON, fontweight="bold")

# one-way bridge arrow (Ch.30): gravity -> SM only
ax.annotate("", xy=(6.0,1.45), xytext=(4.0,1.45),
            arrowprops=dict(arrowstyle="-|>", color=C_MOND, lw=2.0))
ax.text(5.0,1.05,"one narrow one-way bridge (Ch.30)", ha="center", fontsize=7.6, color=C_MOND)

# ---- right country: SILENT (Standard Model) ----
right = plt.Rectangle((5.6,0.7),4.1,8.6, fc="#f1f5f9", ec=C_NEWTON, lw=2.0, zorder=1)
ax.add_patch(right)
ax.text(7.65,9.0,"FRAMEWORK SILENT", ha="center", fontsize=11, color=C_NEWTON, fontweight="bold")
ax.text(7.65,8.55,"identities · masses · forces", ha="center", fontsize=8.6, color=C_NEWTON, style="italic")
silent = ["$m_p/m_e\\approx 1836$",
          "Koide $Q\\approx 2/3$",
          "Higgs / Yukawa couplings",
          "strong coupling, $\\Lambda_{QCD}$",
          "why 3 generations*"]
for i,t in enumerate(silent):
    y=7.7-i*1.18
    ax.text(5.92, y, "✗", fontsize=12, color=C_DATA)
    ax.text(6.35, y, t, fontsize=8.7, color="#334155", va="center")
ax.text(5.92,1.7,"* suggestive parity remark — NOT a derivation",
        fontsize=6.9, color="#94a3b8")

ax.text(5.0,9.75,"The quarantine: nothing on the right is ever called 'derived'",
        ha="center", fontsize=9.3, color="#475569", fontweight="bold")
ax.text(9.68,0.18,"schematic — Chapter 27", ha="right", fontsize=7.3, color="#bbbbbb")
fig.tight_layout(); fig.savefig("ch27_two_countries_wall.png", bbox_inches="tight"); print("ok")
