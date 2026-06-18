import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

# ---- framework constants ----
c = 2.99792458e8
Lam = 1.1056e-52            # cosmological constant, m^-2 (Planck-scale value)
Z = np.sqrt(32*np.pi/3.0)  # = 5.789, the calibrated kernel
a0 = c**2 * np.sqrt(Lam/(32*np.pi))

fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.5, 4.4),
                               gridspec_kw={"width_ratios":[1.35,1]})

# ---- LEFT: the decomposition diagram ----
axL.set_title("The one knob, taken apart")
axL.grid(False); axL.axis("off"); axL.set_xlim(0,10); axL.set_ylim(0,10)

axL.text(5, 9.4, r"$a_0 \;=\; c^2\sqrt{\frac{\Lambda}{32\pi}} \;=\; \frac{c\,H_\Lambda}{Z}$",
         ha="center", fontsize=15)

# forced boxes
forced = [
  (r"FORM:  $a_0 \sim c^2\sqrt{\Lambda}$", "holographic bound, Unruh floor,\nde Sitter dimensional closure"),
  (r"KERNEL:  $\sqrt{8\pi/3}$", r"Einstein's $8\pi$  $\times$  Friedmann's $3$"),
]
for i,(t,s) in enumerate(forced):
    y = 7.7 - i*2.05
    box = FancyBboxPatch((0.6, y-0.7), 8.8, 1.45, boxstyle="round,pad=0.06",
                         linewidth=1.8, edgecolor=C_MOND, facecolor="#cffafe")
    axL.add_patch(box)
    axL.text(1.0, y+0.32, t, ha="left", va="center", fontsize=11.5, fontweight="bold")
    axL.text(1.0, y-0.30, s, ha="left", va="center", fontsize=8.6, color="#0e7490")
    axL.text(9.0, y, "FORCED", ha="right", va="center", fontsize=9, color=C_MOND, fontweight="bold")

# free box
y = 7.7 - 2*2.05
box = FancyBboxPatch((0.6, y-0.7), 8.8, 1.45, boxstyle="round,pad=0.06",
                     linewidth=2.2, edgecolor=C_FW, facecolor="#ede9fe")
axL.add_patch(box)
axL.text(1.0, y+0.32, r"GEOMETRIC KNOB:  $\kappa = \frac{1}{2}$", ha="left", va="center",
         fontsize=11.5, fontweight="bold")
axL.text(1.0, y-0.30, r"single-dof CKN limit;  $\frac{3}{8\pi}=\frac{(\frac{1}{2}\,\mathrm{Schw.})}{(\frac{4\pi}{3}\,\mathrm{ball})}$",
         ha="left", va="center", fontsize=8.6, color=C_FW)
axL.text(9.0, y, "FREE (1)", ha="right", va="center", fontsize=9, color=C_FW, fontweight="bold")

axL.text(5, 0.45, "value of $a_0$ is a one-parameter posit — not derived from nothing",
         ha="center", fontsize=8.6, color="#64748b", style="italic")

# ---- RIGHT: the arithmetic closes ----
axR.set_title("The arithmetic lands on the measured scale")
labels = [r"$Z=\sqrt{32\pi/3}$", r"$a_0 = c^2\sqrt{\Lambda/32\pi}$"]
vals = [Z, a0*1e11]
cols = [C_MOND, C_FW]
bars = axR.bar([0,1], vals, color=cols, alpha=0.9, width=0.55)
axR.set_xticks([0,1]); axR.set_xticklabels(["kernel $Z$", r"$a_0$ ($10^{-11}$ m/s$^2$)"], fontsize=9.5)
axR.bar_label(bars, labels=[f"{Z:.3f}", f"{a0*1e11:.2f}"], padding=3, fontsize=10)
axR.axhline(9.36, color=C_DATA, ls="--", lw=1.5)
axR.text(1.0, 9.36, "  measured\n  $a_0\\approx9.36$", color=C_DATA, fontsize=8.5, va="bottom", ha="center")
axR.set_ylim(0, 10.5)
axR.set_ylabel("value (units as labelled)")
fig.tight_layout(); fig.savefig("ch24_a0_forced_vs_free.png", bbox_inches="tight"); print("ok")
