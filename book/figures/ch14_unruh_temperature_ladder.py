import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

# Unruh temperature: k_B T = hbar a / (2 pi c)  ->  T = hbar a / (2 pi c k_B)
c    = 2.998e8       # m/s
kB   = 1.380649e-23  # J/K
hbar = 1.054571817e-34  # J s
def T_unruh(a):
    return hbar*a/(2*np.pi*c*kB)

# acceleration axis spanning the cosmic floor up past the 1-kelvin threshold
a = np.logspace(-11, 22, 400)
fig, ax = plt.subplots(figsize=(7,4.3))
ax.plot(a, T_unruh(a), color=C_FW, lw=2.4, label=r"$T=\hbar a/(2\pi c\,k_B)$  (Unruh)")
ax.set_xscale("log"); ax.set_yscale("log")

# special acceleration scales, all computed from the same formula
H0 = 70*1000/3.086e22            # s^-1  (H0 = 70 km/s/Mpc)
scales = [
    (c*H0,   r"cosmic floor  $cH_0\sim10^{-10}$", C_MOND),
    (9.8,    r"Earth gravity  $1\,g$",            C_NEWTON),
    (1e26,   r"proton in intense laser",           C_DATA),
    (2*np.pi*c*kB*1.0/hbar, r"warms vacuum to $1\,$K", "#b45309"),
]
for av, lab, col in scales:
    Tv = T_unruh(av)
    ax.scatter([av],[Tv], s=46, color=col, zorder=5, edgecolor="white", linewidth=0.7)
    ax.annotate(lab, (av,Tv), textcoords="offset points", xytext=(8,-2),
                fontsize=8.5, color=col, ha="left", va="top")

# reference horizontals
ax.axhline(300, color="#94a3b8", ls=":", lw=1)
ax.text(a[2], 300*1.6, "room temperature 300 K", fontsize=8, color="#64748b")
ax.axhline(2.725, color="#94a3b8", ls=":", lw=1)
ax.text(a[2], 2.725*1.6, "CMB 2.7 K", fontsize=8, color="#64748b")

ax.set_xlabel(r"proper acceleration $a$  (m/s$^2$)")
ax.set_ylabel(r"Unruh temperature $T$  (K)")
ax.set_title("The Unruh temperature ladder: warmth proportional to acceleration")
ax.set_ylim(1e-32, 1e9)
ax.legend(frameon=False, loc="upper left")
ax.text(0.99,0.02,"computed from $k_BT=\\hbar a/2\\pi c$", transform=ax.transAxes,
        ha="right", va="bottom", fontsize=7.5, color="#9ca3af")
fig.tight_layout(); fig.savefig("ch14_unruh_temperature_ladder.png", bbox_inches="tight"); print("ok")
