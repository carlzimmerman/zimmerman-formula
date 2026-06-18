import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.5, 4.7))

# ---- LEFT PANEL: counting the knobs ----
axL.set_title("Read the top rows: free knobs in the sector")
axL.grid(False)
axL.set_xlim(0, 10); axL.set_ylim(0, 10)
axL.axis("off")

# LambdaCDM column: six knobs + a particle
lcdm_labels = [r"$\Omega_b h^2$", r"$\Omega_c h^2$", r"$H_0$", r"$\tau$", r"$A_s$", r"$n_s$"]
axL.text(2.5, 9.4, "ΛCDM", ha="center", fontsize=13, fontweight="bold", color=C_NEWTON)
for i, lab in enumerate(lcdm_labels):
    y = 8.3 - i*1.05
    box = FancyBboxPatch((1.2, y-0.35), 2.6, 0.7, boxstyle="round,pad=0.05",
                         linewidth=1.4, edgecolor=C_NEWTON, facecolor="#e2e8f0")
    axL.add_patch(box)
    axL.text(2.5, y, lab, ha="center", va="center", fontsize=11)
# the particle
box = FancyBboxPatch((1.2, 1.55-0.35), 2.6, 0.7, boxstyle="round,pad=0.05",
                     linewidth=1.6, edgecolor=C_DATA, facecolor="#fee2e2")
axL.add_patch(box)
axL.text(2.5, 1.55, "+ a particle", ha="center", va="center", fontsize=10.5, color=C_DATA)
axL.text(2.5, 0.55, "6 knobs + CDM", ha="center", fontsize=10, fontweight="bold", color=C_NEWTON)

# Framework column: one knob
axL.text(7.5, 9.4, "Framework", ha="center", fontsize=13, fontweight="bold", color=C_FW)
box = FancyBboxPatch((6.2, 8.3-0.35), 2.6, 0.7, boxstyle="round,pad=0.05",
                     linewidth=2.0, edgecolor=C_FW, facecolor="#ede9fe")
axL.add_patch(box)
axL.text(7.5, 8.3, r"$\kappa = \frac{1}{2}$", ha="center", va="center", fontsize=13)
axL.text(7.5, 7.45, "(argued irreducible,\npure geometry)", ha="center", va="top",
         fontsize=8.5, color=C_FW)
axL.text(7.5, 0.55, "1 knob, no particle", ha="center", fontsize=10, fontweight="bold", color=C_FW)

# ---- RIGHT PANEL: reach ----
axR.set_title("Read the bottom rows: reach of the explanation")
topics = ["CMB\nacoustic peaks", "Large-scale\nstructure", "Light-element\nabundances",
          "Expansion\nhistory", "Galaxy\nrotation curves", r"The $a_0$ scale" + "\n(= why $\\sim c^2\\sqrt{\\Lambda}$)",
          "Covariant\nlensing", "Galaxy\nclusters", "Standard\nModel"]
# 1 = handled, 0.5 = partial/phenomenological, 0 = not addressed / wall
lcdm_reach = [1, 1, 1, 1, 1, 0, 1, 0.7, 0]      # LCDM: a0 not a question it asks; SM separate
fw_reach   = [0, 0.2, 0, 0.3, 1, 1, 0.25, 0.3, 0]  # framework: narrow but explains a0
y = np.arange(len(topics))[::-1]
h = 0.36
axR.barh(y + h/2, lcdm_reach, height=h, color=C_NEWTON, alpha=0.85, label="ΛCDM")
axR.barh(y - h/2, fw_reach, height=h, color=C_FW, alpha=0.9, label="Framework")
axR.set_yticks(y); axR.set_yticklabels(topics, fontsize=8.3)
axR.set_xlim(0, 1.15); axR.set_xticks([0, 0.5, 1.0])
axR.set_xticklabels(["not\naddressed", "partial /\npheno.", "handled"], fontsize=8)
axR.set_xlabel("how the theory handles each front")
axR.legend(frameon=False, loc="lower right", fontsize=9)
axR.grid(axis="x", alpha=0.25); axR.grid(axis="y", alpha=0)

fig.text(0.5, 0.005, "schematic of the Chapter 24 scoreboard — conceptual, not measured",
         ha="center", fontsize=7.5, color="#94a3b8")
fig.tight_layout(rect=[0,0.03,1,1]); fig.savefig("ch24_scoreboard_two_stories.png", bbox_inches="tight"); print("ok")
