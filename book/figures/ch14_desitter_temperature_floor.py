import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

c    = 2.998e8
kB   = 1.380649e-23
hbar = 1.054571817e-34
H0   = 70*1000/3.086e22     # s^-1
cH   = c*H0                 # ~6.8e-10 m/s^2, the de Sitter-Unruh floor scale
a0   = 9.36e-11             # framework a0 = c^2 sqrt(Lambda/32 pi)

# naive flat-space Unruh: T proportional to a (vanishes at a=0)
def T_naive(a): return hbar*a/(2*np.pi*c*kB)
# de Sitter-Unruh effective temperature (Deser-Levin): floor at a=0
def T_eff(a):   return hbar*np.sqrt(a**2 + cH**2)/(2*np.pi*c*kB)

a = np.logspace(-12, -7.5, 400)
fig, ax = plt.subplots(figsize=(7,4.3))
ax.plot(a, T_naive(a), color=C_NEWTON, lw=2.0, ls="--",
        label=r"naive Unruh  $T\propto a$  (no floor)")
ax.plot(a, T_eff(a),  color=C_FW,     lw=2.4,
        label=r"de Sitter–Unruh  $T\propto\sqrt{a^2+(cH_0)^2}$")
ax.set_xscale("log"); ax.set_yscale("log")

# the floor
Tfloor = hbar*cH/(2*np.pi*c*kB)
ax.axhline(Tfloor, color=C_MOND, ls=":", lw=1.4)
ax.text(a[3], Tfloor*1.25, r"thermal floor at $a\to0$", fontsize=8.5, color=C_MOND)

# mark the two acceleration scales
for av, lab, col, dy in [(a0, r"$a_0=9.36\times10^{-11}$", C_DATA, 1.5),
                          (cH, r"$cH_0\sim6.8\times10^{-10}$", C_MOND, 0.55)]:
    ax.axvline(av, color=col, ls=":", lw=1.1, alpha=0.8)
    ax.text(av, Tfloor*dy*2.4, lab, rotation=90, fontsize=8, color=col,
            ha="right", va="bottom")

ax.set_xlabel(r"acceleration $a$  (m/s$^2$)")
ax.set_ylabel(r"effective temperature $T$  (K)")
ax.set_title("The de Sitter–Unruh floor: warmth that never quite reaches zero")
ax.legend(frameon=False, loc="upper left")
ax.text(0.99,0.02,"framework-computed; floor scale $cH_0$, $a_0=c^2\\sqrt{\\Lambda/32\\pi}$",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=7, color="#9ca3af")
fig.tight_layout(); fig.savefig("ch14_desitter_temperature_floor.png", bbox_inches="tight"); print("ok")
