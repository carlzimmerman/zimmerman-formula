import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"  # framework / Newton / MOND / data-or-obs

hbar=1.055e-34; kB=1.381e-23
H_L=1.8e-18                       # de Sitter Hubble rate, s^-1 (ch.15 worked example)
T_dS = hbar*H_L/(2*np.pi*kB)      # Gibbons-Hawking temperature ~2.2e-30 K
T_CMB = 2.725                     # K, Planck 2018
T_room = 293.0                    # K
T_lab = 1e-9                      # ~nanokelvin, coldest cold-atom ensembles (illustrative)

labels = ["Room\ntemperature", "CMB\n(2.725 K)", "Coldest lab\n(~nanokelvin)", r"de Sitter floor $T_{\rm dS}$"]
vals   = [T_room, T_CMB, T_lab, T_dS]
colors = [C_NEWTON, C_DATA, C_MOND, C_FW]

fig, ax = plt.subplots(figsize=(7,4.3))
ypos = np.arange(len(vals))[::-1]
ax.barh(ypos, vals, color=colors, height=0.55, log=True)
for y,v in zip(ypos, vals):
    ax.text(v*2.2, y, f"{v:.2g} K", va="center", fontsize=9)
ax.set_yticks(ypos); ax.set_yticklabels(labels, fontsize=9.5)
ax.set_xscale("log")
ax.set_xlim(1e-31, 1e4)
ax.set_xlabel("temperature  (kelvin, log scale)")
ax.set_title("The temperature floor: tiny, but never zero")
ax.grid(axis="y", alpha=0)
gap = np.log10(T_CMB/T_dS)        # ~30 orders of magnitude
ax.annotate(f"{gap:.0f} orders of magnitude\ncolder than the CMB",
            xy=(T_dS, ypos[-1]), xytext=(2e-22, 1.4),
            fontsize=9, color=C_FW,
            arrowprops=dict(arrowstyle="->", color=C_FW, lw=1.2))
ax.text(0.99,0.02,"computed from the framework's equations", transform=ax.transAxes,
        ha="right", va="bottom", fontsize=7, color="0.6")
fig.tight_layout(); fig.savefig("ch15_temperature_floor_scale.png", bbox_inches="tight"); print("ok")
