import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"
fig, ax = plt.subplots(figsize=(7,4.3))

# Relative size of the object: 1 -> 4 (i.e. up to quadrupling the radius)
R = np.linspace(1.0, 4.0, 400)
# Volume-scaling entropy (gas at fixed density): S ~ R^3, normalized to 1 at R=1
S_vol = R**3
# Area-scaling entropy (black-hole horizon): S ~ R^2, normalized to 1 at R=1
S_area = R**2

ax.plot(R, S_vol, color=C_NEWTON, ls="--", lw=2.4,
        label=r"Box of gas (volume law, $S\propto R^3$)")
ax.plot(R, S_area, color=C_FW, lw=2.6,
        label=r"Black-hole horizon (area law, $S\propto R^2$)")

# Mark the 'double the radius' reference the chapter calls out
ax.axvline(2.0, color="0.6", lw=1, ls=":")
ax.scatter([2.0,2.0],[8.0,4.0], color=[C_NEWTON,C_FW], zorder=5, s=45)
ax.annotate("x8", xy=(2.0,8.0), xytext=(2.12,8.3), color=C_NEWTON, fontsize=11, fontweight="bold")
ax.annotate("x4", xy=(2.0,4.0), xytext=(2.12,4.4), color=C_FW, fontsize=11, fontweight="bold")
ax.annotate("double the radius", xy=(2.0,0.6), xytext=(2.06,0.7), color="0.4", fontsize=9)

ax.set_xlim(1.0,4.0); ax.set_ylim(0.0,66)
ax.set_xlabel("size of the object  (radius, relative to start)")
ax.set_ylabel("entropy  (relative to start)")
ax.set_title("Volume entropy vs. area entropy: the holographic surprise")
ax.legend(frameon=False, loc="upper left")
ax.text(0.99,0.02,"S/k_B = A/4l_P^2  (Bekenstein-Hawking); gas S proportional to volume",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=7.5, color="0.5")
fig.tight_layout(); fig.savefig("ch16_area_vs_volume_entropy.png", bbox_inches="tight"); print("ok")
